import { DcCloseoutCase } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import { createEditBatch, UserFacingError, type Integer, type Long } from "@osdk/functions";
import { logs, SeverityNumber } from "@opentelemetry/api-logs";
import { ContractError } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import type { ReviewRequest } from "../domain/types.js";
import { applyChange, parseChange } from "./changes.js";
import type { CaseChange, ChangeKind, WorkAssignment } from "./change_types.js";
import { appendProjections, loadProjections, type ProjectionState } from "./projections.js";
import { appendReviewAndReceipt, findReceiptByPk, isReplay, loadCurrentReview } from "./storage.js";
import { BOOTSTRAP_ACTOR_ID, ENVIRONMENT_ID, PROJECTION_VERSION, receiptIdFor, type CommandIdentity, type OntologyEdit, type StoredReview } from "./types.js";
import { checkedLong, hasAuthority, identifier, nativeReview, operatorIds, requireActorAccess,
  requireCondition, requireManagerAccess, serialize, validateDelay, validateRequest, validateRoot } from "./validation.js";
import { reconcileWorkflowAfterCaseChange } from "../lifecycle/commands.js";
import { parseWorkflowVersion } from "../lifecycle/codec.js";
import { appendLifecycleProjections, assertWorkflowHistory } from "../lifecycle/projections.js";
import { workflowContract, workflowSnapshotExtras } from "../lifecycle/storage.js";
import type { WorkflowStateV2 } from "../lifecycle/types.js";
import { loadWorkAssignments } from "./work_assignments.js";
import { projectQueue } from "../workspace/queue.js";

const LOGGER = logs.getLogger("deposit-closeout-phase-c");

export function decodeChange(kind: ChangeKind, payloadJson: string): CaseChange {
  try { return parseChange(kind, payloadJson); }
  catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    throw new UserFacingError(`Change payload does not satisfy the strict ${kind} contract: ${error.message}`);
  }
}

/** Current authority only, without reapplying old facts or checking applicability of a replay. */
function authorizeOperation(root: Osdk.Instance<DcCloseoutCase>, request: ReviewRequest,
  change: CaseChange, actorId: string, now: string): void {
  requireActorAccess(root, actorId);
  const administrator = (): void => requireCondition(root.adminIds?.includes(actorId) === true,
    "Only a trusted case administrator may perform this operation.");
  const manager = (action: string, amount: number | null = null): void => {
    requireManagerAccess(root, actorId);
    requireCondition(hasAuthority(request, actorId, "MANAGER", action, amount, now),
      "No current manager authority covers this operation.");
  };
  const accountant = (): void => {
    requireCondition(root.accountantIds?.includes(actorId) === true
      && hasAuthority(request, actorId, "ACCOUNTANT", "RECONCILE_MONEY_RECORD", null, now),
    "No current accountant authority covers this operation.");
  };
  switch (change.kind) {
    case "RECHECK": return;
    case "UPDATE_AUTHORITY": case "ADVANCE_DEMO_CLOCK": administrator(); return;
    case "RECORD_MONEY_EVENT": case "RECONCILE_BALANCE": accountant(); return;
    case "WAIVE_CHARGE": manager("CHOOSE_OR_WAIVE_CHARGE", 0); return;
    case "RECORD_CHARGE_DECISION":
      manager("RECORD_CHARGE_DECISION");
      if (["CHOSEN", "WAIVED"].includes(change.payload.charge.choiceState)) {
        manager("CHOOSE_OR_WAIVE_CHARGE", change.payload.charge.supportedAmountCents);
      }
      return;
    case "RECORD_RELATED_TASK": {
      const previous = request.snapshot.relatedTasks.find((entry): boolean => entry.taskId === change.payload.taskId);
      const roles = new Set([change.payload.responsibleRole, ...(previous === undefined ? [] : [previous.responsibleRole])]);
      roles.forEach((role): void => { if (role === "ACCOUNTANT") accountant(); else manager("ACCEPT_OR_CORRECT_FACT"); });
      return;
    }
    default: manager("ACCEPT_OR_CORRECT_FACT");
  }
}

export async function observedDelay(command: CommandIdentity, revision: number, delay?: Integer): Promise<void> {
  validateDelay(delay);
  if (delay === undefined || delay === 0) return;
  LOGGER.emit({ severityNumber: SeverityNumber.INFO, severityText: "INFO",
    body: "Synthetic operation validated before overlap delay",
    attributes: { LOG_MESSAGE: "Phase C observed revision", commandId: command.commandId,
      commandKind: command.commandKind, observedRevision: String(revision) } });
  // The exact loaded root is deliberately retained; no refresh masks the contender.
  await new Promise<void>((resolve): void => { setTimeout(resolve, delay); });
}

/** The single persistence path for open, choice and all operational commands.
 * One loaded-root update is the platform contention guard, not the child reads.
 * No deletes, outbox, ledger execution, or native financial calculations occur here.
 */
export function persistCase(client: Client, root: Osdk.Instance<DcCloseoutCase> | undefined,
  proposedRequest: ReviewRequest, assignments: readonly WorkAssignment[],
  command: CommandIdentity, now: string, projections: ProjectionState,
  previous?: StoredReview, workflowOverride?: WorkflowStateV2): OntologyEdit[] {
  let request = structuredClone(proposedRequest);
  let workflow = workflowOverride;
  if (root !== undefined) {
    const version = workflowContract(() => parseWorkflowVersion(root.workflowVersion));
    requireCondition(previous !== undefined && (version !== 2 || previous.workflow !== undefined),
      "The accepted previous workflow is required; a v2 case cannot be downgraded.");
    requireCondition(request.snapshot.revision === previous.request.snapshot.revision
      && command.previousRevision === root.revision, "Persist only one revision of the accepted loaded case.");
    if (workflow === undefined && previous.workflow !== undefined) {
      const reconciled = workflowContract(() => reconcileWorkflowAfterCaseChange(previous.request, request,
        assignments, previous.workflow!, { actorId: command.actorId, commandId: command.commandId,
          serverNow: now, basisReviewId: root.currentReviewId!, isAdministrator: root.adminIds?.includes(command.actorId) === true }));
      request = reconciled.request;
      workflow = reconciled.workflow;
    }
    requireCondition(Number.isSafeInteger(request.snapshot.revision + 1), "Case revision cannot be incremented exactly.");
    request.snapshot.revision += 1;
  }
  validateRequest(request);
  loadWorkAssignments(serialize(assignments), fingerprint(assignments), PROJECTION_VERSION, request, now);
  const review = nativeReview(request);
  const sidecar = workflow === undefined ? undefined : workflowSnapshotExtras(request, review, workflow, assignments, now);
  if (workflow !== undefined) assertWorkflowHistory(previous?.workflow, workflow);
  const batch = createEditBatch<OntologyEdit>(client);
  const currentReviewId = appendReviewAndReceipt(batch, request, review, command, now, assignments, sidecar?.extras);
  const properties = { ...projectQueue(request, review, sidecar?.review, assignments, currentReviewId),
    revision: String(request.snapshot.revision), currentReviewId,
    inputHash: review.metadata.inputHash, reviewClock: request.reviewClock,
    projectionVersion: PROJECTION_VERSION, ...operatorIds(request, now), updatedBy: command.actorId, updatedAt: now,
    ...(workflow === undefined ? {} : { workflowVersion: "2", currentStatementId: workflow.currentStatementId ?? undefined }) };
  if (root === undefined) {
    batch.create(DcCloseoutCase, { ...properties, caseId: request.snapshot.caseId,
      managementCompanyId: request.snapshot.managementCompanyId, environmentId: ENVIRONMENT_ID,
      tenancyId: request.snapshot.tenancyId, homeId: request.snapshot.homeId,
      readerIds: [BOOTSTRAP_ACTOR_ID], adminIds: [BOOTSTRAP_ACTOR_ID], createdBy: command.actorId });
  } else {
    batch.update(root, properties);
  }
  appendProjections(batch, request, sidecar?.review ?? review, assignments, projections);
  if (workflow !== undefined) {
    appendLifecycleProjections(batch, request, review, workflow, projections.lifecycle, now, currentReviewId);
  }
  return batch.getEdits();
}

/** Fixed-kind internal dispatch, never published as an arbitrary patch API.
 * Every accepted new command (including a factual no-op) records one review/revision.
 * Exact authorized replays return zero edits even after later revisions.
 */
export async function operateCase(client: Client, caseId: string, actorId: string,
  commandId: string, expectedRevision: Long, kind: ChangeKind, payloadJson: string,
  testDelayMilliseconds?: Integer): Promise<OntologyEdit[]> {
  identifier(caseId, "Case ID");
  identifier(commandId, "Command ID");
  const expected = checkedLong(expectedRevision, "Expected revision", 1n);
  validateDelay(testDelayMilliseconds);
  requireCondition(testDelayMilliseconds === undefined || kind === "RECHECK", "Only recheck accepts a synthetic delay.");
  const change = decodeChange(kind, payloadJson);
  const root = await client(DcCloseoutCase).fetchOne(caseId);
  const revision = validateRoot(root);
  requireActorAccess(root, actorId);
  const stored = await loadCurrentReview(client, root);
  authorizeOperation(root, stored.request, change, actorId, new Date().toISOString());
  const intent = { environmentId: ENVIRONMENT_ID, commandKind: kind, caseId,
    managementCompanyId: stored.request.snapshot.managementCompanyId, actorId, expectedRevision, payload: change.payload };
  const command: CommandIdentity = { caseId, managementCompanyId: intent.managementCompanyId, actorId,
    commandId, commandKind: kind, previousRevision: expectedRevision,
    payloadHash: fingerprint(intent), commandJson: serialize(intent) };
  const receipt = await findReceiptByPk(client, receiptIdFor(command.managementCompanyId, caseId, commandId));
  if (isReplay(receipt, command, revision)) return [];
  requireCondition(expected === revision, "Case revision changed; reload the case before applying this operation.");
  requireCondition(revision < Number.MAX_SAFE_INTEGER, "Case revision cannot be incremented exactly.");
  const isAdministrator = root.adminIds?.includes(actorId) === true;
  // Full applicability/source validation happens after replay. Any error aborts before a batch exists.
  applyChange(stored.request, stored.workAssignments, change, actorId, new Date().toISOString(), isAdministrator,
    stored.workflowReview?.result.scopeRequirements.requirements);
  const projections = await loadProjections(client, stored, root.projectionVersion);
  await observedDelay(command, revision, testDelayMilliseconds);
  const now = new Date().toISOString();
  authorizeOperation(root, stored.request, change, actorId, now);
  const result = applyChange(stored.request, stored.workAssignments, change, actorId, now, isAdministrator,
    stored.workflowReview?.result.scopeRequirements.requirements);
  return persistCase(client, root, result.request, result.workAssignments, command, now, projections, stored);
}
