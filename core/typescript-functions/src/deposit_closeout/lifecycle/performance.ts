/** Performance projections are evidence-specific; approvals and intentions are never performance. */
import { compare_timestamps } from "../domain/datetime.js";
import type { OpenQuestion, RequirementResult, ReviewEnvelope, ReviewRequest, TrackOutcome } from "../domain/types.js";
import { valid_evidence } from "../domain/validation.js";
import { approvalValidity } from "./approvals.js";
import { ACTIVE_WORKFLOW_STATES, financialAvailability, sumCents } from "./availability.js";
import { projectRequests } from "./requests.js";
import { statementBasisCurrent } from "./statements.js";
import type { ApprovalValidity, CurrentRequest, FinancialCommitment, FinancialOperationKind, StatementStatus,
  WorkflowOutcomes, WorkflowStateV2 } from "./types.js";

export { ACTIVE_WORKFLOW_STATES, checkedCents, sumCents, unreservedCents } from "./availability.js";

export const FINANCIAL_KINDS: readonly FinancialOperationKind[] = ["REFUND", "CHARGE_POSTING", "DEPOSIT_APPLICATION",
  "CHARGE_POSTING_REVERSAL", "DEPOSIT_APPLICATION_REVERSAL"];

export interface WorkflowPerformance {
  currentRequests: CurrentRequest[];
  approvalDetails: ApprovalValidity[];
  statementDetails: StatementStatus[];
  financialCommitments: FinancialCommitment[];
  newlyRequestableRefundCents: number | null;
  accountVerified: boolean;
  hasUnresolvedExecution: boolean;
  moneyComplete: boolean;
}

/** Use supplied authority time (snapshot createdAt for replay), never Date.now(). */
export function projectPerformance(request: ReviewRequest, base: ReviewEnvelope, state: WorkflowStateV2, authorityEvaluatedAt: string): WorkflowPerformance {
  const currentRequests = projectRequests(state);
  const approvalDetails = state.approvals.map((approval): ApprovalValidity => approvalValidity(request, base, state, approval, authorityEvaluatedAt));
  const acceptedRawIds = new Set(state.events.flatMap((event): string[] => event.kind === "RESULT_ACCEPTED" ? [event.payload.rawEventId] : []));
  const statementDetails = state.statements.map((statement): StatementStatus => {
    const dispatches = state.requests.filter((entry): boolean => entry.kind === "STATEMENT_DISPATCH" && entry.intent.statementId === statement.statementId);
    const fact = request.snapshot.priorStatements.find((entry): boolean => entry.versionId === statement.statementId
      && entry.contentHash === statement.contentHash && entry.recipientInstructionsVersion === statement.recipientVersionId);
    const issued = fact !== undefined && fact.issuedAt !== null && compare_timestamps(fact.issuedAt, request.reviewClock) <= 0
      && valid_evidence(request.snapshot, fact.issuanceEvidenceIds, request.reviewClock)
      && dispatches.some((dispatch): boolean => currentRequests.some((current): boolean => current.requestId === dispatch.requestId && current.state === "SUCCEEDED")
        && state.events.some((event): boolean => event.kind === "RAW_SIMULATED_RESULT" && event.requestId === dispatch.requestId
          && event.payload.kind === "SUCCEEDED" && acceptedRawIds.has(event.eventId)));
    return { statementId: statement.statementId, isCurrent: state.currentStatementId === statement.statementId
      && statementBasisCurrent(request, base, state, statement), dispatchRequestIds: dispatches.map((entry): string => entry.requestId), issued };
  });
  const financialCommitments = FINANCIAL_KINDS.map((kind): FinancialCommitment => {
    const active = currentRequests.filter((entry): boolean => entry.kind === kind && ACTIVE_WORKFLOW_STATES.has(entry.state));
    return { kind, reservedCents: sumCents(active.map((entry): number => entry.reservedAmountCents)), requestIds: active.map((entry): string => entry.requestId) };
  });
  const a = base.result.account;
  const accountVerified = base.result.scopeRequirements.scopeState === "SUPPORTED" && a.finalAccountReady
    && a.reconciliationState === "RECONCILED" && a.finalRefundCents !== null && a.pendingReservedRefundCents !== null;
  const newlyRequestableRefundCents = accountVerified
    ? financialAvailability(a, currentRequests, request.snapshot.priorRequests, "REFUND").availableCents : null;
  const hasUnresolvedExecution = currentRequests.some((entry): boolean => entry.reconciliationRequired || ACTIVE_WORKFLOW_STATES.has(entry.state))
    || request.snapshot.priorRequests.some((entry): boolean => ACTIVE_WORKFLOW_STATES.has(entry.state))
    || request.snapshot.moneyEvents.some((entry): boolean => entry.status === "UNKNOWN" || entry.status === "PENDING")
    || state.events.some((event): boolean => event.kind === "RAW_SIMULATED_RESULT" && !acceptedRawIds.has(event.eventId));
  const unresolvedMoney = currentRequests.some((entry): boolean => entry.kind !== "STATEMENT_DISPATCH"
      && (entry.reconciliationRequired || ACTIVE_WORKFLOW_STATES.has(entry.state)))
    || request.snapshot.priorRequests.some((entry): boolean => ["REQUEST_REFUND", "REQUEST_LEDGER_POSTING"].includes(entry.actionKind)
      && ACTIVE_WORKFLOW_STATES.has(entry.state))
    || request.snapshot.moneyEvents.some((entry): boolean => entry.status === "UNKNOWN" || entry.status === "PENDING")
    || state.events.some((event): boolean => event.kind === "RAW_SIMULATED_RESULT" && event.payload.operationKind !== "STATEMENT_DISPATCH"
      && !acceptedRawIds.has(event.eventId));
  const moneyComplete = accountVerified && a.finalRefundCents === 0 && a.pendingReservedRefundCents === 0
    && a.postingDeltaCents === 0 && a.depositApplicationDeltaCents === 0 && !unresolvedMoney;
  return { currentRequests, approvalDetails, statementDetails, financialCommitments, newlyRequestableRefundCents,
    accountVerified, hasUnresolvedExecution, moneyComplete };
}

/** Corrective/final dispatch satisfies only its own current version; interim proof remains separate. */
export function performedStatementForRequirement(request: ReviewRequest, base: ReviewEnvelope, state: WorkflowStateV2,
  performance: WorkflowPerformance, requirementKey: string): string | null {
  const interim = requirementKey === "NC:interim-account";
  const candidates = state.statements.filter((statement): boolean => interim ? statement.kind === "INTERIM"
    : statement.statementId === state.currentStatementId && statement.kind !== "INTERIM");
  const latest = [...candidates].reverse().find((statement): boolean => statementBasisCurrent(request, base, state, statement));
  if (latest === undefined || !performance.statementDetails.some((entry): boolean => entry.statementId === latest.statementId && entry.issued)) return null;
  return latest.statementId;
}

const DONE = new Set(["FULFILLED", "NOT_APPLICABLE"]);

/** Derive all five independent tracks; no generic completion override is accepted. */
export function performanceOutcomes(base: ReviewEnvelope, requirements: readonly RequirementResult[], questions: readonly OpenQuestion[],
  performance: WorkflowPerformance): WorkflowOutcomes {
  const relatedIds = new Set(requirements.filter((entry): boolean => entry.track === "RELATED_ACCOUNT")
    .flatMap((entry): string[] => entry.prerequisiteIds));
  const materialQuestions = questions.filter((entry): boolean => !relatedIds.has(entry.questionId)
    && !entry.questionId.startsWith("related:"));
  const forTrack = (track: string): RequirementResult[] => requirements.filter((entry): boolean => entry.track === track);
  const open = (track: string): RequirementResult[] => forTrack(track).filter((entry): boolean => !DONE.has(entry.state));
  const decisionsReady = base.result.scopeRequirements.scopeState === "SUPPORTED" && !base.result.itemDecisions.some((item): boolean => item.requiresReviewer)
    && open("DECISIONS").length === 0;
  const communicationsDone = forTrack("COMMUNICATIONS").length > 0 && open("COMMUNICATIONS").length === 0;
  const approvalsDone = open("APPROVALS").length === 0;
  const relatedDone = open("RELATED_ACCOUNT").length === 0;
  const depositDone = decisionsReady && materialQuestions.length === 0 && communicationsDone && approvalsDone
    && performance.moneyComplete && !performance.hasUnresolvedExecution;
  const pendingMoney = performance.currentRequests.some((entry): boolean => entry.kind !== "STATEMENT_DISPATCH" && ACTIVE_WORKFLOW_STATES.has(entry.state));
  const trackStates: [string, string, string][] = [
    ["DECISIONS", decisionsReady ? "READY" : "BLOCKED", decisionsReady ? "Native scope and item decisions are ready; this is not performance." : "Specific native facts or material questions remain unresolved."],
    ["COMMUNICATIONS", communicationsDone ? "FULFILLED" : open("COMMUNICATIONS").some((entry): boolean => entry.state === "BLOCKED") ? "BLOCKED" : "OPEN",
      communicationsDone ? "Accepted simulator dispatch proof matches every required statement version. Not legal performance." : "Preparation and approval are not dispatch; perform the current requirement-specific version."],
    ["APPROVALS", approvalsDone ? "FULFILLED" : open("APPROVALS").some((entry): boolean => entry.state === "BLOCKED") ? "BLOCKED" : "OPEN",
      approvalsDone ? "Current unperformed intents are approved, or no further approval is needed after historical performance." : "Exact operation/version approvals remain necessary; historical approvals do not authorize changed work."],
    ["MONEY", performance.moneyComplete ? "FULFILLED" : !performance.accountVerified || performance.currentRequests.some((entry): boolean => entry.reconciliationRequired) ? "BLOCKED" : pendingMoney ? "PENDING" : "READY",
      performance.moneyComplete ? "Native verified unpaid refund and posting/application deltas are zero, with no unresolved execution." : "Native unpaid liability and separate posting/application adjustments remain authoritative; reserved/requested funds are not settlement."],
    ["RELATED_ACCOUNT", forTrack("RELATED_ACCOUNT").length === 0 ? "NOT_APPLICABLE" : relatedDone ? "FULFILLED" : "OPEN", "Related balances/tasks require their own scope-specific evidence and do not settle deposit obligations."],
  ];
  const tracks = trackStates.map(([track, state, reason]): TrackOutcome => ({ track, state, reason,
    openRequirementKeys: open(track).map((entry): string => entry.requirementKey).sort(),
    completionEvidenceIds: [...new Set(forTrack(track).flatMap((entry): string[] => entry.completionEvidenceIds))].sort() }));
  return { tracks, depositComplete: false, overallCaseComplete: false, simulatedDepositWorkflowComplete: depositDone,
    simulatedOverallWorkflowComplete: depositDone && relatedDone, completionMode: "SIMULATED", legalPerformanceConfirmed: false,
    summary: tracks.map((track): string => `${track.track}: ${track.state}`).join("; ") + ". SIMULATED only; no actual money movement or legal performance is asserted." };
}
