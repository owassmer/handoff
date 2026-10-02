/** Persistence boundaries for the v2 sidecar; native JSON remains the C contract. */
import type { DcCloseoutCase, DcReviewSnapshot } from "@ontology/sdk";
import type { Osdk } from "@osdk/client";
import { UserFacingError } from "@osdk/functions";
import { canonical_json, ContractError } from "../domain/codec.js";
import type { ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import type { WorkAssignment } from "../phase_c/change_types.js";
import { ENVIRONMENT_ID } from "../phase_c/types.js";
import { requireCondition, sameInstant } from "../phase_c/validation.js";
import { hashWorkflowReview, hashWorkflowState, parseWorkflowSnapshot, serializeWorkflowReview,
  serializeWorkflowState, validateWorkflowCaseReferences } from "./codec.js";
import { reviewWorkflow } from "./review.js";
import { projectNativeFacts } from "./requests.js";
import type { ParsedWorkflowSnapshot, WorkflowSnapshotExtras, WorkflowStateV2 } from "./types.js";

/** Only known contract failures become actionable messages; SDK/access errors propagate. */
export function workflowContract<T>(operation: () => T): T {
  try { return operation(); }
  catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    throw new UserFacingError(`Closeout workflow: ${error.message}`);
  }
}

export function loadWorkflowSnapshot(root: Osdk.Instance<DcCloseoutCase>, snapshot: Osdk.Instance<DcReviewSnapshot>,
  request: ReviewRequest, base: ReviewEnvelope, assignments: readonly WorkAssignment[]): ParsedWorkflowSnapshot | null {
  return workflowContract((): ParsedWorkflowSnapshot | null => {
    const extras: WorkflowSnapshotExtras = { workflowStateJson: snapshot.workflowStateJson,
      workflowStateHash: snapshot.workflowStateHash, workflowReviewJson: snapshot.workflowReviewJson,
      workflowReviewHash: snapshot.workflowReviewHash };
    const parsed = parseWorkflowSnapshot(root.workflowVersion, extras, snapshot.createdAt!);
    if (parsed === null) {
      requireCondition(root.currentStatementId === undefined, "A legacy case cannot contain a workflow statement pointer.");
      return null;
    }
    const { state, review } = parsed;
    validateWorkflowCaseReferences(state, request.snapshot);
    requireCondition(state.environmentId === ENVIRONMENT_ID && state.caseId === root.caseId
      && state.managementCompanyId === root.managementCompanyId
      && root.currentStatementId === (state.currentStatementId ?? undefined)
      && sameInstant(state.businessClock, request.reviewClock),
    "Workflow scope, business clock or current statement pointer is inconsistent.");
    requireCondition(canonical_json(projectNativeFacts(request, state)) === canonical_json(request),
      "Stored native request and statement facts do not match their accepted workflow history.");
    const recomputed = reviewWorkflow(request, base, state, assignments, snapshot.createdAt!);
    requireCondition(snapshot.workflowStateJson === serializeWorkflowState(state)
      && snapshot.workflowReviewJson === serializeWorkflowReview(review)
      && canonical_json(review) === canonical_json(recomputed),
    "Stored workflow review is not the canonical review at its recorded authority time.");
    return parsed;
  });
}

export function workflowSnapshotExtras(request: ReviewRequest, base: ReviewEnvelope, workflow: WorkflowStateV2,
  assignments: readonly WorkAssignment[], now: string): { extras: WorkflowSnapshotExtras; review: ParsedWorkflowSnapshot["review"] } {
  return workflowContract(() => {
    validateWorkflowCaseReferences(workflow, request.snapshot);
    requireCondition(sameInstant(workflow.businessClock, request.reviewClock), "Workflow and native clocks must agree.");
    requireCondition(canonical_json(projectNativeFacts(request, workflow)) === canonical_json(request),
      "Persist only reconciled native request and statement facts.");
    const review = reviewWorkflow(request, base, workflow, assignments, now);
    const extras = { workflowStateJson: serializeWorkflowState(workflow), workflowStateHash: hashWorkflowState(workflow),
      workflowReviewJson: serializeWorkflowReview(review), workflowReviewHash: hashWorkflowReview(review) };
    // Validate times and complete sidecars before creating any storage edits.
    parseWorkflowSnapshot("2", extras, now);
    return { extras, review };
  });
}
