/** V2 six-section review, retaining native classification/accounting and explicit simulator performance. */
import { canonical_json, ContractError } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import { _local_date } from "../domain/rules.js";
import type { OpenQuestion, RequirementResult, ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import { question } from "../domain/validation.js";
import type { WorkAssignment } from "../phase_c/change_types.js";
import { hasAuthority } from "../phase_c/validation.js";
import { buildIntent } from "./approvals.js";
import { desiredOperationCents, financialAvailability } from "./availability.js";
import { hashWorkflowState, parseWorkflowReview, parseWorkflowTimestamp } from "./codec.js";
import { nativeActionKind } from "./events.js";
import { assertWorkflowScope, routeUsable } from "./materiality.js";
import { ACTIVE_WORKFLOW_STATES, FINANCIAL_KINDS, performanceOutcomes, performedStatementForRequirement,
  projectPerformance } from "./performance.js";
import type { WorkflowPerformance } from "./performance.js";
import { remainingCanonicalPrincipal, verifiedNativeTransactions } from "./simulator.js";
import type { FinancialOperationKind, OperationIntent, OperationIntentSpec, OperationKind, WorkflowAction, WorkflowActionDetails,
  WorkflowReviewV2, WorkflowStateV2 } from "./types.js";

const COMMUNICATION_KEYS = new Set(["NC:ordinary-account", "NC:interim-account", "NC:final-account"]);
const RECIPIENT_QUESTIONS = new Set(["recipient:instructions", "recipient:method", "recipient:missing-address-policy"]);
const REPLACED_ACTION_KEYS = new Set(["prepare:statement", "approve:statement", "request:dispatch", "request:refund"]);
const REPLACED_AUTHORITY_KEYS = new Set(["authority:PREPARE_STATEMENT", "authority:APPROVE_EXACT_VERSION",
  "authority:REQUEST_STATEMENT_DISPATCH", "authority:REQUEST_REFUND"]);

function authorityExists(request: ReviewRequest, role: string, action: string, amount: number | null, at: string): boolean {
  return request.snapshot.parties.some((party): boolean => party.principalId !== null
    && hasAuthority(request, party.principalId, role, action, amount, at));
}
function oppositeKind(kind: OperationKind): FinancialOperationKind | null {
  if (kind === "CHARGE_POSTING") return "CHARGE_POSTING_REVERSAL";
  if (kind === "CHARGE_POSTING_REVERSAL") return "CHARGE_POSTING";
  if (kind === "DEPOSIT_APPLICATION") return "DEPOSIT_APPLICATION_REVERSAL";
  if (kind === "DEPOSIT_APPLICATION_REVERSAL") return "DEPOSIT_APPLICATION";
  return null;
}
function details(kind: OperationKind, state: WorkflowStateV2, p: WorkflowPerformance, intent: OperationIntent | null = null): WorkflowActionDetails {
  const approvalIds = new Set(state.approvals.filter((entry): boolean => entry.scope === kind).map((entry): string => entry.approvalId));
  return { operationKind: kind, intent, approvalDetails: p.approvalDetails.filter((entry): boolean => approvalIds.has(entry.approvalId)),
    requestDetails: p.currentRequests.filter((entry): boolean => entry.kind === kind),
    statementDetails: kind === "STATEMENT_DISPATCH" ? p.statementDetails : [] };
}
function attemptedUnknown(p: WorkflowPerformance): boolean {
  return p.currentRequests.some((entry): boolean => entry.state === "OUTCOME_UNKNOWN" || entry.reconciliationRequired);
}

/** Candidate intent is explanatory, never a substitute for per-actor admission. */
function candidateIntent(request: ReviewRequest, base: ReviewEnvelope, state: WorkflowStateV2, kind: OperationKind, amount: number | null): OperationIntent | null {
  const spec: OperationIntentSpec = { kind, amountCents: amount, statementId: kind === "STATEMENT_DISPATCH" ? state.currentStatementId : null,
    dispositionKey: `workflow-${kind.toLowerCase()}`, replacesRequestId: null, reversesTransactionId: null };
  if (kind !== "STATEMENT_DISPATCH" && (amount === null || amount === 0)) return null;
  try {
    if (kind.endsWith("_REVERSAL")) {
      const originalKind = kind === "CHARGE_POSTING_REVERSAL" ? "CHARGE_POSTING" : "DEPOSIT_APPLICATION";
      const txs = verifiedNativeTransactions(request);
      const original = [...txs.values()].find((entry): boolean => entry.kind === originalKind && entry.settlement_at() !== null
        && remainingCanonicalPrincipal(txs, entry.key) >= amount!);
      if (original === undefined) return null;
      spec.reversesTransactionId = original.key;
    }
    return buildIntent(request, base, state, spec);
  } catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    return null; // Unverifiable candidates are BLOCKED, never invented approvals.
  }
}
function questionRequirement(q: OpenQuestion, track: string): RequirementResult {
  return { requirementKey: `question:${q.questionId}`, question: q.question, ruleQuestionId: null, track,
    dueKind: "UNCONFIRMED", legalDueDate: null, internalTargetAt: null, triggerFactKeys: [], state: "BLOCKED",
    responsibleRole: q.resolverRole, prerequisiteIds: [q.questionId], completionCondition: "Resolve this named prerequisite with case-specific evidence.",
    completionEvidenceIds: [], reason: q.reason };
}

/**
 * Pure historical/live projection. The caller supplies unchanged nativeReview on
 * projectNativeFacts(request, workflow). Recompute stored snapshots using their
 * createdAt as authorityEvaluatedAt; admission uses a fresh actual server time.
 */
export function reviewWorkflow(request: ReviewRequest, baseReview: ReviewEnvelope, workflow: WorkflowStateV2,
  workAssignments: readonly WorkAssignment[], authorityEvaluatedAt: string): WorkflowReviewV2 {
  assertWorkflowScope(request, workflow);
  authorityEvaluatedAt = parseWorkflowTimestamp(authorityEvaluatedAt);
  const base = structuredClone(baseReview);
  const p = projectPerformance(request, base, workflow, authorityEvaluatedAt);
  const a = base.result.account;
  const statementRoute = routeUsable(request, workflow.statementInstructions, authorityEvaluatedAt);
  const refundRoute = routeUsable(request, workflow.refundInstructions, authorityEvaluatedAt);
  const refundNeeded = a.finalRefundCents === null || a.finalRefundCents > 0;
  const suppliedQuestions = new Set(request.snapshot.questions.map((q): string => q.questionId));
  // Explicit machine-key substitution ONLY. Never filter free-text reasons or
  // discard an input question merely because its name resembles a placeholder.
  const missingInputs = base.result.missingInputs.filter((q): boolean => suppliedQuestions.has(q.questionId)
    || (!RECIPIENT_QUESTIONS.has(q.questionId) && !REPLACED_AUTHORITY_KEYS.has(q.questionId)));
  const addQuestion = (q: OpenQuestion): void => { if (!missingInputs.some((entry): boolean => entry.questionId === q.questionId)) missingInputs.push(q); };
  if (!statementRoute) addQuestion(question("workflow:statement-route", "Verify the independent statement delivery instructions.",
    "No statement delivery route is inferred from a refund route. Missing-address legal policy remains unreviewed; independent supported preparation can continue.",
    "MANAGER", [], ["SET_RECIPIENT_INSTRUCTIONS"], "Verified synthetic statement parties, method, route and evidence"));
  if (refundNeeded && !refundRoute) addQuestion(question("workflow:refund-route", "Verify the independent refund instructions before new payment work.",
    "No refund route is inferred from a statement route. This does not prevent independent statement preparation or dispatch.",
    "MANAGER", [], ["SET_RECIPIENT_INSTRUCTIONS"], "Verified synthetic refund parties, method, route and evidence"));

  const retainedQuestionIds = new Set(missingInputs.map((q): string => q.questionId));
  const requirements = base.result.scopeRequirements.requirements.filter((entry): boolean => !entry.requirementKey.startsWith("question:")
    || retainedQuestionIds.has(entry.requirementKey.slice("question:".length)));
  missingInputs.filter((q): boolean => q.questionId.startsWith("workflow:")).forEach((q): void => {
    requirements.push(questionRequirement(q, q.questionId === "workflow:statement-route" ? "COMMUNICATIONS" : "MONEY"));
  });
  const today = _local_date(request.reviewClock, "America/New_York");
  requirements.filter((entry): boolean => COMMUNICATION_KEYS.has(entry.requirementKey)).forEach((entry): void => {
    const performed = performedStatementForRequirement(request, base, workflow, p, entry.requirementKey);
    const current = workflow.statements.find((statement): boolean => statement.statementId === workflow.currentStatementId);
    const matchingKind = entry.requirementKey === "NC:interim-account" ? current?.kind === "INTERIM" : current !== undefined && current.kind !== "INTERIM";
    const currentReady = matchingKind && p.statementDetails.some((status): boolean => status.isCurrent);
    const active = currentReady && p.currentRequests.some((fact): boolean => fact.kind === "STATEMENT_DISPATCH" && ACTIVE_WORKFLOW_STATES.has(fact.state)
      && workflow.requests.some((instruction): boolean => instruction.requestId === fact.requestId && instruction.intent.statementId === workflow.currentStatementId));
    if (performed !== null) {
      entry.state = "FULFILLED";
      entry.completionEvidenceIds = [...(request.snapshot.priorStatements.find((fact): boolean => fact.versionId === performed)?.issuanceEvidenceIds ?? [])];
      entry.prerequisiteIds = [];
      entry.reason = "Accepted simulator dispatch matches this requirement's exact statement version. Legal sufficiency/performance is not confirmed.";
    } else {
      entry.state = !statementRoute || entry.state === "BLOCKED" ? "BLOCKED" : active ? "PENDING" : "OPEN";
      entry.completionEvidenceIds = [];
      entry.prerequisiteIds = [...new Set([...entry.prerequisiteIds, ...(statementRoute ? [] : ["workflow:statement-route"]),
        ...(currentReady ? ["accepted-current-dispatch-result"] : ["current-immutable-statement-version"])])];
      entry.reason = "Current requirement-specific statement dispatch is not yet performed; prepared text, approval and a claimed attempt are not delivery."
        + (entry.legalDueDate !== null && entry.legalDueDate < today ? " Overdue under the synthetic calendar." : " The synthetic deadline remains open.");
    }
    entry.completionCondition = "Accept matching simulator dispatch proof for this exact required statement version; legal performance remains false.";
  });

  const actions: WorkflowAction[] = base.result.actions.filter((entry): boolean => !REPLACED_ACTION_KEYS.has(entry.actionKey))
    .map((entry): WorkflowAction => ({ ...entry, workflow: null }));
  const makeAction = (key: string, actionKind: string, role: string, kind: OperationKind, intent: OperationIntent | null,
    blockers: string[], amount: number | null, reason: string, needed: boolean = true): WorkflowAction => {
    const pending = [...blockers];
    if (needed && !authorityExists(request, role, actionKind, amount, authorityEvaluatedAt)) {
      const id = `workflow:authority:${key}`;
      pending.push(id);
      const q = question(id, "Who has current role-specific authority for this operation and amount?",
        "Authority is checked at actual recording time, not the demonstration clock. A draft or an old approval grants no permission.",
        "AUTHORITY_ADMIN", [], ["SET_OR_REVOKE_AUTHORITY"], `${role} grant for ${actionKind}`);
      addQuestion(q);
      requirements.push(questionRequirement(q, "APPROVALS"));
    }
    const action: WorkflowAction = { actionKey: key, actionKind, responsibleRole: role,
      availability: !needed ? "NOT_APPLICABLE" : pending.length === 0 ? "AVAILABLE" : "BLOCKED",
      targetVersionId: intent?.targetVersionId ?? null, payloadFingerprint: intent === null ? null : fingerprint(intent), amountCents: amount,
      prerequisiteIds: [...new Set(pending)].sort(), requiredApprovalScopes: actionKind.startsWith("REQUEST_") ? [kind] : [], reason,
      fallbackDescription: pending.length === 0 ? null : "Continue independent supported preparation; actual actor admission remains mandatory.",
      workflow: details(kind, workflow, p, intent) };
    actions.push(action);
    return action;
  };

  const statementStatus = p.statementDetails.find((entry): boolean => entry.isCurrent);
  const currentStatement = workflow.statements.find((entry): boolean => entry.statementId === statementStatus?.statementId);
  const communicationsDone = requirements.filter((entry): boolean => COMMUNICATION_KEYS.has(entry.requirementKey)).length > 0
    && requirements.filter((entry): boolean => COMMUNICATION_KEYS.has(entry.requirementKey)).every((entry): boolean => entry.state === "FULFILLED");
  const nativePrepare = base.result.actions.find((entry): boolean => entry.actionKey === "prepare:statement");
  const prepareBlockers = (nativePrepare?.prerequisiteIds ?? ["supported-scope-trigger-and-account"])
    .filter((key): boolean => key !== "authority:PREPARE_STATEMENT");
  if (workflow.statementInstructions.partyIds.length === 0) prepareBlockers.push("intended-statement-parties");
  makeAction("prepare:statement", "PREPARE_STATEMENT", "MANAGER", "STATEMENT_DISPATCH", null, prepareBlockers, null,
    "Prepare immutable synthetic text using native scope/amounts; an independent refund route is not required. Preparation is not dispatch.", !communicationsDone && currentStatement === undefined);

  const approvalNeeds: { kind: OperationKind; needed: boolean; satisfied: boolean; blocked: boolean }[] = [];
  const buildOperationActions = (kind: OperationKind): void => {
    const role = kind === "STATEMENT_DISPATCH" ? "MANAGER" : "ACCOUNTANT";
    const amount = kind === "STATEMENT_DISPATCH" ? null : desiredOperationCents(a, kind);
    const budget = kind === "STATEMENT_DISPATCH" ? null : financialAvailability(a, p.currentRequests, request.snapshot.priorRequests, kind);
    const available = kind === "REFUND" ? p.newlyRequestableRefundCents : budget?.availableCents ?? null;
    const required = kind === "STATEMENT_DISPATCH" ? !communicationsDone : amount === null || amount > 0;
    const ownRoute = kind === "STATEMENT_DISPATCH" ? statementRoute : kind !== "REFUND" || refundRoute;
    const active = p.currentRequests.filter((entry): boolean => entry.kind === kind && ACTIVE_WORKFLOW_STATES.has(entry.state));
    const validApproval = workflow.approvals.find((entry): boolean => entry.scope === kind
      && p.approvalDetails.some((valid): boolean => valid.approvalId === entry.approvalId && valid.valid)
      && (kind === "STATEMENT_DISPATCH" || (available !== null && entry.intent.amountCents! <= available && entry.intent.amountCents! > 0))
      && !workflow.requests.some((instruction): boolean => instruction.intent.targetVersionId === entry.intent.targetVersionId));
    const candidate = validApproval?.intent ?? candidateIntent(request, base, workflow, kind, available);
    const blocked: string[] = [];
    if (kind === "STATEMENT_DISPATCH") {
      if (statementStatus === undefined) blocked.push("current-immutable-statement-version");
      if (!statementRoute) blocked.push("workflow:statement-route");
    } else {
      if (!p.accountVerified) blocked.push("final-verified-native-account");
      if (!ownRoute) blocked.push("workflow:refund-route");
      if (attemptedUnknown(p) || request.snapshot.priorRequests.some((entry): boolean => entry.state === "OUTCOME_UNKNOWN")) blocked.push("reconcile-unknown-result");
      if (available === null || available <= 0) blocked.push("no-unreserved-kind-specific-budget");
      if (kind.endsWith("_REVERSAL") && candidate === null) blocked.push("verified-canonical-original");
      if (p.currentRequests.some((entry): boolean => entry.kind === oppositeKind(kind) && entry.reservedAmountCents > 0)) {
        blocked.push("reconcile-opposite-accounting-instruction");
      }
    }
    const hasCoverage = validApproval !== undefined || active.length > 0 && active.every((fact): boolean => workflow.requests.some((instruction): boolean =>
      instruction.requestId === fact.requestId && instruction.approvalIds.some((id): boolean => p.approvalDetails.some((valid): boolean => valid.approvalId === id && valid.valid))));
    approvalNeeds.push({ kind, needed: required, satisfied: !required || hasCoverage, blocked: required && blocked.length > 0 && !hasCoverage });
    const key = kind === "STATEMENT_DISPATCH" ? "statement" : kind.toLowerCase();
    // Unfunded liability is BLOCKED, not NOT_APPLICABLE. Fully reserved ordinary
    // work retains its existing status; cash-in cannot be anticipated as funding.
    const freshNeeded = required && (kind === "STATEMENT_DISPATCH" ? active.length === 0
      : available === null || budget!.kindBudgetCents === null || budget!.kindBudgetCents > 0);
    makeAction(`approve:${key}`, "APPROVE_EXACT_VERSION", role, kind, candidate,
      [...blocked, ...(candidate === null ? ["supported-exact-intent"] : [])], available,
      "Approve a selected exact intent/version, not a whole case. Final actor, amount, original/replacement and materiality checks run in the command.", freshNeeded && validApproval === undefined);
    makeAction(kind === "STATEMENT_DISPATCH" ? "request:dispatch" : `request:${key}`, nativeActionKind(kind), role, kind,
      validApproval?.intent ?? null, [...blocked, ...(validApproval === undefined ? ["exact-current-operation-approval"] : [])],
      validApproval?.intent.amountCents ?? available,
      "Request only the selected approved immutable operation. Request/claim is not settlement or dispatch; full per-actor admission is still required.", freshNeeded);
  };
  buildOperationActions("STATEMENT_DISPATCH");
  FINANCIAL_KINDS.forEach(buildOperationActions);

  p.currentRequests.forEach((current): void => {
    const instruction = workflow.requests.find((entry): boolean => entry.requestId === current.requestId)!;
    const role = current.kind === "STATEMENT_DISPATCH" ? "MANAGER" : "ACCOUNTANT";
    if (current.state === "READY") {
      const valid = instruction.approvalIds.some((id): boolean => p.approvalDetails.some((entry): boolean => entry.approvalId === id && entry.valid));
      const blockers = valid ? [] : ["exact-current-operation-approval"];
      if (current.kind !== "STATEMENT_DISPATCH") {
        if (!p.accountVerified || attemptedUnknown(p)) blockers.push("reconcile-native-account-before-attempt");
        const available = financialAvailability(a, p.currentRequests, request.snapshot.priorRequests, current.kind, current.requestId).availableCents;
        if (available === null || BigInt(current.amountCents!) > BigInt(available)) blockers.push("insufficient-current-kind-specific-budget");
        if (p.currentRequests.some((entry): boolean => entry.kind === oppositeKind(current.kind) && entry.reservedAmountCents > 0)) {
          blockers.push("reconcile-opposite-accounting-instruction");
        }
      }
      makeAction(`claim:${current.requestId}`, nativeActionKind(current.kind), role, current.kind, instruction.intent, blockers, current.amountCents,
        "Claim this READY request using its frozen instruction. No send or settlement is established; command admission rechecks budget and authority.");
    }
    if (["CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN"].includes(current.state) || current.reconciliationRequired
        || workflow.events.some((event): boolean => event.kind === "RAW_SIMULATED_RESULT" && event.requestId === current.requestId
          && !workflow.events.some((accepted): boolean => accepted.kind === "RESULT_ACCEPTED" && accepted.payload.rawEventId === event.eventId))) {
      const recordingAction = current.kind !== "STATEMENT_DISPATCH" ? "RECONCILE_MONEY_RECORD"
        : authorityExists(request, "MANAGER", "ACCEPT_OR_CORRECT_FACT", null, authorityEvaluatedAt)
          ? "ACCEPT_OR_CORRECT_FACT" : "REQUEST_STATEMENT_DISPATCH";
      makeAction(`reconcile:${current.requestId}`, recordingAction,
        role, current.kind, instruction.intent, [], current.amountCents,
        "Retain attempted/unknown commitments. Ingest a persisted matching source event; neither stale approval nor grant expiry erases historical results.");
    }
  });
  const approvalRequirement = requirements.find((entry): boolean => entry.requirementKey === "approval:current-version");
  if (approvalRequirement !== undefined) {
    approvalRequirement.state = approvalNeeds.every((entry): boolean => entry.satisfied) ? "FULFILLED"
      : approvalNeeds.some((entry): boolean => entry.blocked) ? "BLOCKED" : "OPEN";
    approvalRequirement.prerequisiteIds = approvalNeeds.filter((entry): boolean => !entry.satisfied).map((entry): string => `approval:${entry.kind}`);
    approvalRequirement.reason = "Each unperformed operation needs its own current exact approval. Revoking permission for future work does not undo accepted historical performance.";
    approvalRequirement.completionCondition = "Obtain current exact approvals for remaining intents, or establish no further intent is needed after accepted performance.";
  }
  const moneyRequirement = requirements.find((entry): boolean => entry.requirementKey === "money:outstanding-work");
  if (moneyRequirement !== undefined) {
    moneyRequirement.state = p.moneyComplete ? "FULFILLED" : !p.accountVerified || attemptedUnknown(p) ? "BLOCKED"
      : p.currentRequests.some((entry): boolean => entry.kind !== "STATEMENT_DISPATCH" && ACTIVE_WORKFLOW_STATES.has(entry.state)) ? "PENDING" : "OPEN";
    moneyRequirement.reason = p.moneyComplete ? "Native unpaid refund and separate posting/application deltas are zero; simulator proof is not legal performance."
      : "Resolve native unpaid liability, all independent ledger adjustments and unresolved attempts; posting is not deposit application.";
    moneyRequirement.completionEvidenceIds = p.moneyComplete ? [...new Set(request.snapshot.moneyEvents.map((entry): string => entry.sourceEvidenceId))].sort() : [];
  }
  // Internal targets affect work organization only, never legal dates or intent materiality.
  const assignmentByKey = new Map(workAssignments.map((entry) => [entry.requirementKey, entry]));
  requirements.forEach((entry): void => { entry.internalTargetAt = assignmentByKey.get(entry.requirementKey)?.internalTargetAt ?? entry.internalTargetAt; });
  requirements.sort((left, right): number => left.requirementKey < right.requirementKey ? -1 : left.requirementKey > right.requirementKey ? 1 : 0);
  missingInputs.sort((left, right): number => left.questionId < right.questionId ? -1 : left.questionId > right.questionId ? 1 : 0);
  actions.sort((left, right): number => left.actionKey < right.actionKey ? -1 : left.actionKey > right.actionKey ? 1 : 0);
  const result: WorkflowReviewV2 = { metadata: { ...base.metadata, workflowSchemaVersion: "2.0.0",
    workflowStateHash: hashWorkflowState(workflow), authorityEvaluatedAt }, result: { ...base.result,
    scopeRequirements: { ...base.result.scopeRequirements, requirements }, missingInputs, actions,
    account: { ...a, financialCommitments: p.financialCommitments, newlyRequestableRefundCents: p.newlyRequestableRefundCents },
    outcomes: performanceOutcomes(base, requirements, missingInputs, p) } };
  return parseWorkflowReview(canonical_json(result));
}
