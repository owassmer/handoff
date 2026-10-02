/** Internal fixed-kind adapter, never exported as a registered generic command. */
import { DcCloseoutCase } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import type { Integer, Long } from "@osdk/functions";
import { fingerprint } from "../domain/fingerprints.js";
import { observedDelay, persistCase } from "../phase_c/operations.js";
import { loadProjections } from "../phase_c/projections.js";
import { findReceiptByPk, isReplay, loadCurrentReview } from "../phase_c/storage.js";
import { ENVIRONMENT_ID, receiptIdFor, type CommandIdentity, type OntologyEdit } from "../phase_c/types.js";
import { checkedLong, identifier, requireActorAccess, requireCondition, serialize, validateDelay, validateRoot } from "../phase_c/validation.js";
import { parseLifecycleCommand } from "./codec.js";
import { applyLifecycleCommand, authorizeLifecycleCommand } from "./commands.js";
import { workflowContract } from "./storage.js";
import type { LifecycleCommandKind, PureContext } from "./types.js";

/**
 * Read/authorize/receipt/revision/applicability precede one root-guarded batch.
 * @param client Platform injected client; all scoped records are policy-visible reads.
 * @param caseId Deterministic native case primary key.
 * @param actorId Current principal bound by the Action, never accepted from payload JSON.
 * @param commandId Stable retry identifier; a different intent conflicts.
 * @param expectedRevision Latest observed root version, including for delayed result ingestion.
 * @param kind Fixed by each public wrapper, not a public parameter.
 * @param payloadJson Strict kind-specific JSON; canonical parsed intent is the receipt identity.
 * @param testDelayMilliseconds Request-only synthetic overlap probe, 0..3000ms; not economic intent.
 */
export async function operateWorkflow(client: Client, caseId: string, actorId: string, commandId: string,
  expectedRevision: Long, kind: LifecycleCommandKind, payloadJson: string, testDelayMilliseconds?: Integer): Promise<OntologyEdit[]> {
  identifier(caseId, "Case ID");
  identifier(commandId, "Command ID");
  const expected = checkedLong(expectedRevision, "Expected revision", 1n);
  validateDelay(testDelayMilliseconds);
  requireCondition(testDelayMilliseconds === undefined || kind === "REQUEST_OPERATION", "Only request operation accepts a synthetic delay.");
  const change = workflowContract(() => parseLifecycleCommand(kind, payloadJson));
  const root = await client(DcCloseoutCase).fetchOne(caseId);
  requireCondition(root.caseId === caseId, "The case lookup returned a different case.");
  const revision = validateRoot(root);
  requireActorAccess(root, actorId);
  const stored = await loadCurrentReview(client, root);
  const context: PureContext = { actorId, commandId, serverNow: new Date().toISOString(),
    isAdministrator: root.adminIds?.includes(actorId) === true, basisReviewId: root.currentReviewId! };
  workflowContract(() => authorizeLifecycleCommand(stored.request, stored.workflow ?? null, change, context));
  const intent = { environmentId: ENVIRONMENT_ID, managementCompanyId: stored.request.snapshot.managementCompanyId,
    caseId, actorId, commandKind: kind, expectedRevision, payload: change.payload };
  const command: CommandIdentity = { caseId, managementCompanyId: intent.managementCompanyId, actorId, commandId,
    commandKind: kind, previousRevision: expectedRevision, payloadHash: fingerprint(intent), commandJson: serialize(intent) };
  const receipt = await findReceiptByPk(client, receiptIdFor(command.managementCompanyId, caseId, commandId));
  if (isReplay(receipt, command, revision)) return [];
  requireCondition(expected === revision, "Case revision changed; reload the case before applying this workflow operation.");
  requireCondition(revision < Number.MAX_SAFE_INTEGER, "Case revision cannot be incremented exactly.");
  // Pure validation has no external side effects and does not build an edit batch.
  let result = workflowContract(() => applyLifecycleCommand(stored.request, stored.workAssignments, stored.workflow ?? null, change, context));
  const projections = await loadProjections(client, stored, root.projectionVersion, true);
  await observedDelay(command, revision, testDelayMilliseconds);
  if (testDelayMilliseconds !== undefined && testDelayMilliseconds > 0) {
    context.serverNow = new Date().toISOString();
    workflowContract(() => authorizeLifecycleCommand(stored.request, stored.workflow ?? null, change, context));
    result = workflowContract(() => applyLifecycleCommand(stored.request, stored.workAssignments, stored.workflow ?? null, change, context));
  }
  // Retain this exact loaded root after overlap; never refresh a competing revision away.
  return persistCase(client, root, result.request, stored.workAssignments, command, context.serverNow, projections, stored, result.workflow);
}
