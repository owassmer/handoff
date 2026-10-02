/** Pure request admission and commands; the parent owns root concurrency/revision and persistence. */
import { canonical_json, from_wire } from "../domain/codec.js";
import { compare_timestamps } from "../domain/datetime.js";
import type { ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import { hasAuthority, nativeReview } from "../phase_c/validation.js";
import { approvalValidity, buildIntent } from "./approvals.js";
import { financialAvailability, sumCents } from "./availability.js";
import { isUnresolvedFinancialRequest, requireResolvedFinancialRequests } from "./financial_reconciliation.js";
import { financialMaterialityHash, statementMaterialityHash } from "./materiality.js";
import { parseLifecycleCommand, parsePureContext, parseWorkflowState, validateWorkflowCaseReferences } from "./codec.js";
import { attemptIdFor, instructionHashFor, instructionKeyFor, operationIdentity, requestIdFor } from "./ids.js";
import { appendWorkflowEvent, nativeActionKind, projectNativeFacts, projectRequests, requireLifecycle } from "./events.js";
import { acceptedRawResults, generateSimulatedResult, ingestSimulatedResult, remainingCanonicalPrincipal,
  requireNoUncorrelatedNativeFacts, verifiedNativeTransactions, type RequestMutationResult } from "./simulator.js";
import { WORKFLOW_COMPANY_ID, WORKFLOW_ENVIRONMENT_ID } from "./types.js";
import type { ApprovalRecord, LifecycleCommand, OperationIntent, OperationIntentSpec, PureContext, RequestInstruction, WorkflowStateV2 } from "./types.js";

export { projectRequests, projectNativeFacts } from "./events.js";
export type { RequestMutationResult } from "./simulator.js";

function requireOperationAuthority(request: ReviewRequest, intent: OperationIntent, ctx: PureContext): void {
  const role = intent.kind === "STATEMENT_DISPATCH" ? "MANAGER" : "ACCOUNTANT";
  requireLifecycle(hasAuthority(request, ctx.actorId, role, nativeActionKind(intent.kind), intent.amountCents, ctx.serverNow),
    `No current ${role.toLowerCase()} authority covers this operation and amount at actual server time.`);
}

function findInstruction(state: WorkflowStateV2, requestId: string): RequestInstruction {
  const instruction = state.requests.find((entry): boolean => entry.requestId === requestId);
  requireLifecycle(instruction !== undefined, "Request does not belong to this workflow.");
  return instruction;
}

function intentSpec(intent: OperationIntent): OperationIntentSpec {
  return { kind: intent.kind, amountCents: intent.amountCents, dispositionKey: intent.dispositionKey,
    statementId: intent.statementId, replacesRequestId: intent.replacesRequestId, reversesTransactionId: intent.reversesTransactionId };
}

function requireExactApproval(
  request: ReviewRequest, state: WorkflowStateV2, approval: ApprovalRecord, ctx: PureContext,
): ReviewEnvelope {
  const baseReview = nativeReview(projectNativeFacts(request, state));
  const validity = approvalValidity(request, baseReview, state, approval, ctx.serverNow);
  requireLifecycle(validity.valid, `An exact current approval is required: ${validity.reason}`);
  const currentIntent = buildIntent(request, baseReview, state, intentSpec(approval.intent));
  requireLifecycle(canonical_json(operationIdentity(currentIntent)) === canonical_json(operationIdentity(approval.intent))
    && currentIntent.targetVersionId === approval.intent.targetVersionId,
  "Approved materiality or own recipient instructions are stale.");
  return baseReview;
}

function safeSum(values: readonly number[]): number {
  return sumCents(values);
}

/** Native finalRefund is unpaid INCLUDING reservations, never an already unreserved balance. */
function requireBudget(
  request: ReviewRequest, state: WorkflowStateV2, intent: OperationIntent, review: ReviewEnvelope, excludeRequestId: string | null = null,
): void {
  if (intent.kind === "STATEMENT_DISPATCH") return;
  requireLifecycle(request.snapshot.currency === "USD" && Number.isSafeInteger(intent.amountCents) && intent.amountCents > 0,
    "New money operations require positive known USD cents.");
  const account = review.result.account;
  requireLifecycle(account.finalAccountReady && account.reconciliationState === "RECONCILED",
    "The full native account must be verified before a new financial instruction.");
  const current = projectRequests(state);
  requireResolvedFinancialRequests(request.snapshot.priorRequests, current);
  const budget = financialAvailability(account, current, request.snapshot.priorRequests, intent.kind, excludeRequestId);
  if (intent.kind === "REFUND" || intent.kind === "DEPOSIT_APPLICATION") {
    requireLifecycle(budget.heldCashBudgetCents !== null,
      "Verified held cash and commitments must be known nonnegative exact cents; reconcile unclassified ledger requests; unknown is not zero.");
    requireLifecycle(BigInt(intent.amountCents) <= BigInt(budget.heldCashBudgetCents),
      "Operation exceeds verified held deposit cash less other refund reservations and deposit-application commitments.");
  }
  if (intent.kind === "REFUND") {
    requireLifecycle(budget.kindBudgetCents !== null,
      "Unpaid liability and reserved funds must both be known; unknown is not zero.");
    requireLifecycle(BigInt(intent.amountCents) <= BigInt(budget.kindBudgetCents),
      "Refund exceeds the native unpaid liability less existing reservations.");
    return;
  }
  const posting = intent.kind === "CHARGE_POSTING" || intent.kind === "CHARGE_POSTING_REVERSAL";
  requireLifecycle(budget.kindBudgetCents !== null, "The kind-specific native accounting adjustment is unknown.");
  const reversal = intent.kind.endsWith("_REVERSAL");
  requireLifecycle(BigInt(intent.amountCents) <= BigInt(budget.kindBudgetCents), "Operation exceeds its kind-specific uncommitted native adjustment.");
  // Opposite pending instructions cannot be netted away as if already performed.
  const opposite = reversal ? (posting ? "CHARGE_POSTING" : "DEPOSIT_APPLICATION")
    : (posting ? "CHARGE_POSTING_REVERSAL" : "DEPOSIT_APPLICATION_REVERSAL");
  requireLifecycle(!current.some((entry): boolean => entry.kind === opposite && entry.reservedAmountCents > 0),
    "An opposite accounting instruction is unresolved; reconcile rather than netting pending work.");
  if (reversal) {
    const transactions = verifiedNativeTransactions(projectNativeFacts(request, state));
    const original = transactions.get(intent.reversesTransactionId!);
    requireLifecycle(original !== undefined && original.kind === (posting ? "CHARGE_POSTING" : "DEPOSIT_APPLICATION")
      && original.settlement_at() !== null, "Reversal must target a verified original transaction of the same accounting kind.");
    const onOriginal = safeSum(state.requests.filter((entry): boolean => entry.reversesTransactionId === original.key
      && entry.requestId !== excludeRequestId).map((entry): number => current.find((fact): boolean => fact.requestId === entry.requestId)!.reservedAmountCents));
    requireLifecycle(intent.amountCents <= remainingCanonicalPrincipal(transactions, original.key) - onOriginal,
      "Reversal exceeds the original transaction's uncommitted remaining principal.");
  }
}

function requireReplacement(request: ReviewRequest, state: WorkflowStateV2, intent: OperationIntent): void {
  if (intent.replacesRequestId === null) return;
  const parent = findInstruction(state, intent.replacesRequestId);
  requireLifecycle(parent.kind === intent.kind, "Replacement must have the same operation kind as its parent.");
  const current = projectRequests(state);
  const parentState = current.find((entry): boolean => entry.requestId === parent.requestId)!;
  requireLifecycle(!isUnresolvedFinancialRequest(parentState),
    "Replacement requires explicit reconciliation of the parent's unresolved financial evidence.");
  const returned = acceptedRawResults(state).filter((entry): boolean => entry.requestId === parent.requestId && entry.payload.kind === "RETURNED");
  requireLifecycle(parentState.state === "FAILED" || (parentState.state === "SUCCEEDED" && parent.kind === "REFUND" && returned.length > 0),
    "Replacement requires a definitively failed instruction or verified returned refund; attempted/unknown work is not replaceable.");
  requireLifecycle(!state.requests.some((entry): boolean => entry.replacesRequestId === parent.requestId
    && current.some((fact): boolean => fact.requestId === entry.requestId && (fact.reservedAmountCents > 0
      || (fact.kind === "STATEMENT_DISPATCH" && !["FAILED", "CANCELLED", "SUPERSEDED"].includes(fact.state))))),
  "A conflicting replacement is still current.");
  if (intent.kind !== "STATEMENT_DISPATCH") {
    let replacementBudget = parent.intent.amountCents!;
    if (returned.length > 0) {
      const transactions = verifiedNativeTransactions(projectNativeFacts(request, state));
      const canonical = parentState.canonicalTransactionId!;
      const original = transactions.get(canonical);
      requireLifecycle(original !== undefined, "Returned replacement requires verified settlement evidence.");
      replacementBudget = original.nominal - remainingCanonicalPrincipal(transactions, canonical);
    }
    const alreadyReplaced = safeSum(state.requests.filter((entry): boolean => entry.replacesRequestId === parent.requestId
      && current.some((fact): boolean => fact.requestId === entry.requestId && fact.state === "SUCCEEDED"))
      .map((entry): number => entry.intent.amountCents!));
    requireLifecycle(intent.amountCents <= replacementBudget - alreadyReplaced,
      "Replacement exceeds the verified remaining parent liability.");
  }
}

function requestOperation(request: ReviewRequest, state: WorkflowStateV2, approvalId: string, ctx: PureContext): RequestMutationResult {
  const approval = state.approvals.find((entry): boolean => entry.approvalId === approvalId);
  requireLifecycle(approval !== undefined && approval.decision === "APPROVED", "Select an approved immutable intent.");
  requireOperationAuthority(request, approval.intent, ctx);
  const key = instructionKeyFor(state, approval.intent);
  const existing = state.requests.find((entry): boolean => entry.instructionKey === key);
  // Economic idempotency precedes materiality re-check, budget and reservation.
  // Historical instructions do not become new payments because their approval expires.
  if (existing !== undefined) {
    requireLifecycle(existing.requestId === requestIdFor(state, approval.intent)
      && canonical_json(operationIdentity(existing.intent)) === canonical_json(operationIdentity(approval.intent))
      && existing.instructionHash === instructionHashFor(state, approval.intent, existing.instructions),
    "Instruction key has conflicting immutable payload; reconcile explicitly.");
    return { request, workflow: state, summary: { requestId: existing.requestId, replayed: true } };
  }
  const baseReview = requireExactApproval(request, state, approval, ctx);
  requireBudget(request, state, approval.intent, baseReview);
  requireReplacement(request, state, approval.intent);
  const instructions = approval.intent.kind === "REFUND" ? state.refundInstructions
    : approval.intent.kind === "STATEMENT_DISPATCH" ? state.statementInstructions : null;
  const instruction: RequestInstruction = { caseId: state.caseId, managementCompanyId: state.managementCompanyId,
    environmentId: state.environmentId, requestId: requestIdFor(state, approval.intent), instructionKey: key,
    createdCommandId: ctx.commandId, kind: approval.intent.kind, intent: structuredClone(approval.intent),
    instructions: structuredClone(instructions), instructionHash: instructionHashFor(state, approval.intent, instructions),
    approvalIds: [approval.approvalId], createdBy: ctx.actorId, createdAt: ctx.serverNow,
    businessCreatedAt: state.businessClock, replacesRequestId: approval.intent.replacesRequestId,
    reversesTransactionId: approval.intent.reversesTransactionId };
  state.requests.push(instruction);
  const created = appendWorkflowEvent(state, ctx, instruction.requestId, null, null,
    { category: "REQUEST_LIFECYCLE", kind: "REQUEST_CREATED", payload: { instructionHash: instruction.instructionHash } });
  instruction.businessCreatedAt = created.occurredAt;
  const projected = projectNativeFacts(request, state);
  if (instruction.kind !== "STATEMENT_DISPATCH") {
    const updated = nativeReview(projected).result.account;
    requireLifecycle(updated.reconciliationState === "RECONCILED" && updated.finalAccountReady,
      "The newly reserved instruction makes the native account unverified.");
  }
  return { request: projected, workflow: state, summary: { requestId: instruction.requestId, replayed: false } };
}

function requireFreshAttempt(request: ReviewRequest, state: WorkflowStateV2, instruction: RequestInstruction, ctx: PureContext): void {
  requireOperationAuthority(request, instruction.intent, ctx);
  requireNoUncorrelatedNativeFacts(request, state, instruction.requestId);
  const approval = state.approvals.find((entry): boolean => instruction.approvalIds.includes(entry.approvalId));
  requireLifecycle(approval !== undefined, "Instruction has no approval.");
  const baseReview = requireExactApproval(request, state, approval, ctx);
  requireBudget(request, state, instruction.intent, baseReview, instruction.requestId);
}

/**
 * Commands run on private clones. Failure cannot leak partially accepted events or money.
 * Actual ctx.serverNow gates authority; the explicit business clock never grants it.
 * @param request Current native request; revision is left unchanged.
 * @param state Strict v2 sidecar; all effects are returned, not persisted.
 * @param command One of the six request/simulator commands.
 * @param ctx Trusted adapter actor, actual clock and command provenance.
 */
export function applyRequestCommand(
  request: ReviewRequest, state: WorkflowStateV2, command: LifecycleCommand, ctx: PureContext,
): RequestMutationResult {
  const workflow = parseWorkflowState(canonical_json(state));
  const trusted = parsePureContext(ctx);
  const parsed = parseLifecycleCommand(command.kind, canonical_json(command.payload));
  requireLifecycle(workflow.mode === "SIMULATED" && workflow.environmentId === WORKFLOW_ENVIRONMENT_ID
    && workflow.managementCompanyId === WORKFLOW_COMPANY_ID && request.snapshot.origin === "CONSTRUCTED",
  "Only the fixed constructed simulator environment is enabled.");
  validateWorkflowCaseReferences(workflow, request.snapshot);
  requireLifecycle(compare_timestamps(trusted.serverNow, workflow.initializedAt) >= 0,
    "Actual recording time cannot precede workflow initialization.");
  const projected = projectNativeFacts(request, workflow);
  let result: RequestMutationResult;
  switch (parsed.kind) {
    case "REQUEST_OPERATION": result = requestOperation(projected, workflow, parsed.payload.approvalId, trusted); break;
    case "CLAIM_REQUEST": {
      const instruction = findInstruction(workflow, parsed.payload.requestId);
      const current = projectRequests(workflow).find((entry): boolean => entry.requestId === instruction.requestId)!;
      requireOperationAuthority(projected, instruction.intent, trusted);
      requireNoUncorrelatedNativeFacts(projected, workflow, instruction.requestId);
      if (current.state === "CLAIMED") {
        result = { request: projected, workflow, summary: { requestId: instruction.requestId, attemptId: current.attemptId, replayed: true } };
        break;
      }
      requireLifecycle(current.state === "READY", "Only READY, never an attempted or unknown request, can be claimed.");
      requireFreshAttempt(projected, workflow, instruction, trusted);
      const attemptId = attemptIdFor(workflow, instruction.requestId, 1);
      appendWorkflowEvent(workflow, trusted, instruction.requestId, attemptId, null,
        { category: "REQUEST_LIFECYCLE", kind: "ATTEMPT_CLAIMED", payload: { instructionHash: instruction.instructionHash } });
      result = { request: projected, workflow, summary: { requestId: instruction.requestId, attemptId } }; break;
    }
    case "RECORD_OUTCOME_UNKNOWN": {
      const instruction = findInstruction(workflow, parsed.payload.requestId);
      // Conservative observation, not new financial authority. Adapter access
      // gates the trusted recording actor; grant expiry must not hide uncertainty.
      const current = projectRequests(workflow).find((entry): boolean => entry.requestId === instruction.requestId)!;
      requireLifecycle(current.attemptId === parsed.payload.attemptId, "Unknown outcome must reference the claimed attempt.");
      if (current.state === "OUTCOME_UNKNOWN") {
        result = { request: projected, workflow, summary: { requestId: instruction.requestId, replayed: true } }; break;
      }
      requireLifecycle(["CLAIMED", "REQUESTED", "ACKNOWLEDGED"].includes(current.state), "Only an outstanding attempt can have an unknown outcome.");
      appendWorkflowEvent(workflow, trusted, instruction.requestId, current.attemptId, null,
        { category: "REQUEST_LIFECYCLE", kind: "OUTCOME_UNKNOWN", payload: { reason: parsed.payload.reason } });
      result = { request: projected, workflow, summary: { requestId: instruction.requestId, outcomeUnknown: true } }; break;
    }
    case "GENERATE_SIMULATED_RESULT": {
      const instruction = findInstruction(workflow, parsed.payload.requestId);
      requireLifecycle(trusted.isAdministrator, "Only the trusted demonstration administrator may select simulator outcomes.");
      const current = projectRequests(workflow).find((entry): boolean => entry.requestId === instruction.requestId)!;
      const replay = workflow.events.some((event): boolean => event.kind === "RAW_SIMULATED_RESULT" && event.sourceEventId === parsed.payload.sourceEventId);
      if (!replay && current.state === "CLAIMED") {
        requireLifecycle(current.attemptId === parsed.payload.attemptId, "Send must reference the claimed attempt.");
        requireFreshAttempt(projected, workflow, instruction, trusted);
        appendWorkflowEvent(workflow, trusted, instruction.requestId, current.attemptId, null,
          { category: "REQUEST_LIFECYCLE", kind: "REQUESTED", payload: { instructionHash: instruction.instructionHash } });
      }
      requireLifecycle(["CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN", "SUCCEEDED", "FAILED"].includes(current.state),
        "Only a potentially attempted instruction can produce an observation.");
      result = generateSimulatedResult(projected, workflow, instruction, parsed.payload, trusted); break;
    }
    case "INGEST_RESULT": result = ingestSimulatedResult(projected, workflow, parsed.payload.sourceEventId, trusted); break;
    case "CANCEL_UNATTEMPTED_REQUEST": {
      const instruction = findInstruction(workflow, parsed.payload.requestId);
      // Withdrawing unattempted intent is not permission to create new financial work.
      requireLifecycle(trusted.isAdministrator || instruction.createdBy === trusted.actorId,
        "Only the requester or case administrator may withdraw a request.");
      requireNoUncorrelatedNativeFacts(projected, workflow, instruction.requestId);
      const current = projectRequests(workflow).find((entry): boolean => entry.requestId === instruction.requestId)!;
      requireLifecycle(current.state === "READY" && current.attemptId === null, "Only an unattempted READY request can be cancelled.");
      appendWorkflowEvent(workflow, trusted, instruction.requestId, null, null,
        { category: "REQUEST_LIFECYCLE", kind: "CANCELLED_BEFORE_ATTEMPT", payload: { reason: parsed.payload.reason } });
      result = { request: projected, workflow, summary: { requestId: instruction.requestId, cancelled: true } }; break;
    }
    default: throw new Error("This pure reducer handles only request and simulator commands.");
  }
  const finalState = parseWorkflowState(canonical_json(result.workflow));
  const finalRequest = from_wire("ReviewRequest", projectNativeFacts(result.request, finalState));
  validateWorkflowCaseReferences(finalState, finalRequest.snapshot);
  return { ...result, request: finalRequest, workflow: finalState };
}

/** READY-only reconciliation; claimed and unknown commitments survive every case edit. */
export function reconcileRequestsAfterChange(
  request: ReviewRequest, state: WorkflowStateV2, ctx: PureContext,
): { request: ReviewRequest; workflow: WorkflowStateV2 } {
  const workflow = parseWorkflowState(canonical_json(state));
  ctx = parsePureContext(ctx);
  validateWorkflowCaseReferences(workflow, request.snapshot);
  requireLifecycle(request.snapshot.origin === "CONSTRUCTED" && compare_timestamps(ctx.serverNow, workflow.initializedAt) >= 0,
    "Reconciliation requires the constructed scope and a valid actual recording clock.");
  const projected = projectNativeFacts(request, workflow);
  const review = nativeReview(projected);
  projectRequests(workflow).filter((current): boolean => current.state === "READY").forEach((current): void => {
    const instruction = findInstruction(workflow, current.requestId);
    const approval = workflow.approvals.find((entry): boolean => instruction.approvalIds.includes(entry.approvalId));
    const validity = approval === undefined ? { valid: false, reason: "Approval is missing." }
      : approvalValidity(projected, review, workflow, approval, ctx.serverNow);
    if (validity.valid) return;
    const intent = instruction.intent;
    const routeChanged = intent.kind === "REFUND" ? intent.recipientVersionId !== workflow.refundInstructions.versionId
      : intent.kind === "STATEMENT_DISPATCH" && intent.recipientVersionId !== workflow.statementInstructions.versionId;
    const explicitlyRevoked = workflow.approvals.some((entry): boolean => entry.decision === "REVOKED"
      && instruction.approvalIds.includes(entry.revokesApprovalId ?? "") && compare_timestamps(entry.decidedAt, ctx.serverNow) <= 0);
    let basisChanged: boolean;
    if (intent.kind === "STATEMENT_DISPATCH") {
      const statement = workflow.statements.find((entry): boolean => entry.statementId === intent.statementId);
      basisChanged = workflow.currentStatementId !== intent.statementId || statement === undefined
        || statementMaterialityHash(projected, workflow, statement.kind) !== intent.materialityHash;
    } else {
      const hash = financialMaterialityHash(projected, workflow, intent.kind);
      basisChanged = hash !== null && hash !== intent.materialityHash;
    }
    // Inability to verify a basis is NOT evidence that the previous instruction
    // became different. Keep its reserve; admission/claim still fails closed.
    if (!routeChanged && !explicitlyRevoked && !basisChanged) return;
    // Never release a reservation hiding an uncorrelated manual accounting fact.
    requireNoUncorrelatedNativeFacts(projected, workflow, instruction.requestId);
    const replacement = workflow.requests.find((entry): boolean => entry.replacesRequestId === instruction.requestId
      && entry.kind === instruction.kind);
    // A known-changed basis retires the old intent, but does not authorize a new
    // instruction. Cancellation remains an explicit operator command.
    appendWorkflowEvent(workflow, ctx, instruction.requestId, null, null,
      { category: "REQUEST_LIFECYCLE", kind: "SUPERSEDED_BEFORE_ATTEMPT",
        payload: { reason: validity.reason, replacementRequestId: replacement?.requestId ?? null } });
  });
  const validated = parseWorkflowState(canonical_json(workflow));
  return { request: projectNativeFacts(projected, validated), workflow: validated };
}
