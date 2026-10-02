/** Exact-version immutable decisions; current validity never rewrites historical approval. */
import { canonical_json, ContractError } from "../domain/codec.js";
import { compare_timestamps } from "../domain/datetime.js";
import { _authority } from "../domain/review.js";
import type { AuthorityGrant, ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import { valid_evidence } from "../domain/validation.js";
import { hasAuthority } from "../phase_c/validation.js";
import { parseLifecycleCommand, parseWorkflowTimestamp } from "./codec.js";
import { approvalIdFor, targetVersionIdFor } from "./ids.js";
import { projectRequests } from "./events.js";
import { requireResolvedFinancialRequests } from "./financial_reconciliation.js";
import { assertWorkflowScope, financialMaterialityHash, routeUsable, workflowScope } from "./materiality.js";
import { statementBasisCurrent } from "./statements.js";
import type { ApprovalRecord, ApprovalValidity, DecideApprovalPayload, OperationIntent, OperationIntentSpec,
  PureContext, WorkflowStateV2 } from "./types.js";

/** Select a real current grant belonging to this actual principal and needed role. */
export function approvalGrant(request: ReviewRequest, actorId: string, kind: OperationIntent["kind"], amount: number | null, serverNow: string): AuthorityGrant | undefined {
  const now = parseWorkflowTimestamp(serverNow);
  const role = kind === "STATEMENT_DISPATCH" ? "MANAGER" : "ACCOUNTANT";
  if (!hasAuthority(request, actorId, role, "APPROVE_EXACT_VERSION", amount, now)) return undefined;
  const eligible = new Set(_authority(request.snapshot, "APPROVE_EXACT_VERSION", role, amount, now));
  return request.snapshot.authorityGrants.filter((grant): boolean => eligible.has(grant.grantId)
    && request.snapshot.parties.some((party): boolean => party.partyId === grant.partyId && party.principalId === actorId
      && party.roles.includes(role) && valid_evidence(request.snapshot, party.evidenceIds, now)))
    .sort((a, b): number => a.grantId < b.grantId ? -1 : a.grantId > b.grantId ? 1 : 0)[0];
}

function verifiedFinancialAmount(base: ReviewEnvelope, spec: OperationIntentSpec): void {
  const account = base.result.account;
  if (base.result.scopeRequirements.scopeState !== "SUPPORTED" || !account.finalAccountReady
      || account.reconciliationState !== "RECONCILED") {
    throw new ContractError("New financial approval requires the full verified native account; reconcile unknown results first");
  }
  let maximum: number | null;
  switch (spec.kind) {
    case "REFUND": maximum = account.finalRefundCents; break;
    case "CHARGE_POSTING": maximum = account.postingDeltaCents; break;
    case "DEPOSIT_APPLICATION": maximum = account.depositApplicationDeltaCents; break;
    case "CHARGE_POSTING_REVERSAL": maximum = account.postingDeltaCents === null ? null : -account.postingDeltaCents; break;
    case "DEPOSIT_APPLICATION_REVERSAL": maximum = account.depositApplicationDeltaCents === null ? null : -account.depositApplicationDeltaCents; break;
    default: throw new ContractError("Expected financial disposition");
  }
  // Refund liability includes live reservations. Request admission (not this
  // approval identity) must additionally enforce newly unreserved availability.
  if (spec.amountCents === null || maximum === null || maximum <= 0 || spec.amountCents > maximum) {
    throw new ContractError("Exact positive amount exceeds the current unpaid refund or required ledger adjustment; use a positive reversal for negative adjustments");
  }
}

/** Business applicability only. Actor authority is intentionally checked by the caller. */
export function buildIntent(request: ReviewRequest, base: ReviewEnvelope, state: WorkflowStateV2, spec: OperationIntentSpec): OperationIntent {
  assertWorkflowScope(request, state);
  parseLifecycleCommand("DECIDE_APPROVAL", canonical_json({ intent: spec, decision: "APPROVED" }));
  if (spec.statementId !== null && !state.statements.some((entry): boolean => entry.statementId === spec.statementId)) {
    throw new ContractError("Intent display statement is outside this workflow");
  }
  if (spec.replacesRequestId !== null) {
    const previous = state.requests.find((entry): boolean => entry.requestId === spec.replacesRequestId);
    if (previous === undefined || previous.kind !== spec.kind) throw new ContractError("Replacement needs a prior operation of the same kind");
  }
  if (spec.kind === "STATEMENT_DISPATCH") {
    const statement = state.statements.find((entry): boolean => entry.statementId === spec.statementId);
    if (statement === undefined || state.currentStatementId !== statement.statementId
        || !statementBasisCurrent(request, base, state, statement)) throw new ContractError("Dispatch needs the exact current supported statement");
    if (!routeUsable(request, state.statementInstructions, request.reviewClock)) throw new ContractError("Verify the statement delivery channel before approval");
    const intent = { kind: spec.kind, amountCents: null, currency: "USD" as const, dispositionKey: spec.dispositionKey,
      statementId: statement.statementId, recipientVersionId: statement.recipientVersionId,
      materialityHash: statement.materialityHash, contentHash: statement.contentHash,
      replacesRequestId: spec.replacesRequestId, reversesTransactionId: null };
    return { ...intent, targetVersionId: targetVersionIdFor(state, intent) };
  }
  verifiedFinancialAmount(base, spec);
  if (spec.kind === "REFUND" && !routeUsable(request, state.refundInstructions, request.reviewClock)) {
    throw new ContractError("Verify the refund channel before approval");
  }
  if (spec.reversesTransactionId !== null) {
    const originalKind = spec.kind === "CHARGE_POSTING_REVERSAL" ? "CHARGE_POSTING" : "DEPOSIT_APPLICATION";
    const original = request.snapshot.moneyEvents.find((entry): boolean => entry.canonicalTransactionId === spec.reversesTransactionId
      && entry.kind === originalKind && entry.status === "SETTLED");
    if (original === undefined || spec.amountCents === null || spec.amountCents > original.amountCents) {
      throw new ContractError("Reversal requires its verified canonical original settlement and positive bounded principal");
    }
  }
  const materialityHash = financialMaterialityHash(request, state, spec.kind);
  if (materialityHash === null) throw new ContractError("Financial entitlement basis is currently unverifiable");
  // validateFinancialAmount and the codec have established a positive exact amount.
  if (spec.amountCents === null) throw new ContractError("Financial amount is required");
  const intent = { ...spec, kind: spec.kind, amountCents: spec.amountCents, currency: "USD" as const,
    recipientVersionId: spec.kind === "REFUND" ? state.refundInstructions.versionId : null, materialityHash };
  return { ...intent, targetVersionId: targetVersionIdFor(state, intent) };
}

export function decideApproval(request: ReviewRequest, base: ReviewEnvelope, state: WorkflowStateV2, payload: DecideApprovalPayload, ctx: PureContext): ApprovalRecord {
  const intent = buildIntent(request, base, state, payload.intent);
  if (intent.kind !== "STATEMENT_DISPATCH") {
    // Native-only decision inputs have no D observations to reconcile. Once D
    // events exist, their projection supplies uncertainty absent from native facts.
    requireResolvedFinancialRequests(request.snapshot.priorRequests, state.events.length === 0 ? [] : projectRequests(state));
  }
  const grant = approvalGrant(request, ctx.actorId, intent.kind, intent.amountCents, ctx.serverNow);
  if (grant === undefined) throw new ContractError("No current actor-specific approval authority covers this exact financial disposition or statement");
  const route = intent.kind === "STATEMENT_DISPATCH" ? state.statementInstructions : intent.kind === "REFUND" ? state.refundInstructions : null;
  if (route !== null && !routeUsable(request, route, ctx.serverNow)) throw new ContractError("Recipient proof must be known at actual server time");
  return { ...workflowScope(request), approvalId: approvalIdFor(state, ctx.commandId, ctx.actorId), createdCommandId: ctx.commandId,
    actorId: ctx.actorId, actorPartyId: grant.partyId, authorityVersion: grant.authorityVersion, scope: intent.kind,
    intent, decision: payload.decision, decidedAt: ctx.serverNow, revokesApprovalId: null };
}

export function revokeApproval(request: ReviewRequest, state: WorkflowStateV2, approvalId: string, ctx: PureContext): ApprovalRecord {
  const old = state.approvals.find((entry): boolean => entry.approvalId === approvalId);
  if (old === undefined || old.decision !== "APPROVED") throw new ContractError("Select an earlier approved decision to revoke");
  if (old.actorId !== ctx.actorId && !ctx.isAdministrator) throw new ContractError("Only the original approver or a trusted case administrator may revoke");
  // The original decision binds its actor immutably. Revoking one's own grant
  // or removing its principal mapping cannot prevent withdrawing that approval.
  const party = request.snapshot.parties.find((entry): boolean => old.actorId === ctx.actorId
    ? entry.partyId === old.actorPartyId : entry.principalId === ctx.actorId);
  if (party === undefined) throw new ContractError("Revocation actor must identify an existing case party");
  return { ...workflowScope(request), approvalId: approvalIdFor(state, ctx.commandId, ctx.actorId), createdCommandId: ctx.commandId,
    actorId: ctx.actorId, actorPartyId: party.partyId,
    authorityVersion: old.actorId === ctx.actorId ? old.authorityVersion : "trusted-case-administrator",
    scope: old.scope, intent: structuredClone(old.intent), decision: "REVOKED", decidedAt: ctx.serverNow,
    revokesApprovalId: old.approvalId };
}

/**
 * Current permission to use the approval, NOT whether it historically happened.
 * Never compare its amount to shrinking execution deltas or the unpaid balance.
 */
export function approvalValidity(request: ReviewRequest, base: ReviewEnvelope, state: WorkflowStateV2, approval: ApprovalRecord, serverNow: string): ApprovalValidity {
  const answer = (valid: boolean, reason: string): ApprovalValidity => ({ approvalId: approval.approvalId, valid, reason });
  const now = parseWorkflowTimestamp(serverNow);
  if (approval.caseId !== state.caseId || approval.managementCompanyId !== state.managementCompanyId
      || approval.environmentId !== state.environmentId) return answer(false, "Approval belongs to another scope");
  if (approval.decision !== "APPROVED") return answer(false, "This immutable record is not an approving decision");
  if (compare_timestamps(approval.decidedAt, now) > 0) return answer(false, "Approval is not yet known at actual server time");
  if (state.approvals.some((entry): boolean => entry.decision === "REVOKED" && entry.revokesApprovalId === approval.approvalId
      && compare_timestamps(entry.decidedAt, now) <= 0)) return answer(false, "Approval revoked; historical performance is not undone");
  const role = approval.scope === "STATEMENT_DISPATCH" ? "MANAGER" : "ACCOUNTANT";
  const amount = approval.intent.amountCents;
  const eligible = new Set(_authority(request.snapshot, "APPROVE_EXACT_VERSION", role, amount, now));
  const authority = hasAuthority(request, approval.actorId, role, "APPROVE_EXACT_VERSION", amount, now)
    && request.snapshot.authorityGrants.some((grant): boolean => eligible.has(grant.grantId)
      && grant.partyId === approval.actorPartyId && grant.authorityVersion === approval.authorityVersion)
    && request.snapshot.parties.some((party): boolean => party.partyId === approval.actorPartyId
      && party.principalId === approval.actorId && party.roles.includes(role) && valid_evidence(request.snapshot, party.evidenceIds, now));
  if (!authority) return answer(false, "Recorded approver authority is no longer current for this role and exact amount");
  const intent = approval.intent;
  if (intent.kind === "STATEMENT_DISPATCH") {
    const statement = state.statements.find((entry): boolean => entry.statementId === intent.statementId);
    if (statement === undefined || state.currentStatementId !== statement.statementId
        || !statementBasisCurrent(request, base, state, statement) || statement.contentHash !== intent.contentHash
        || statement.materialityHash !== intent.materialityHash || statement.recipientVersionId !== intent.recipientVersionId) {
      return answer(false, "Statement basis or exact current version changed; prior approval remains recorded");
    }
    if (!routeUsable(request, state.statementInstructions, now)) return answer(false, "Statement recipient proof is not currently verified");
  } else {
    if (intent.reversesTransactionId !== null) {
      const originalKind = intent.kind === "CHARGE_POSTING_REVERSAL" ? "CHARGE_POSTING" : "DEPOSIT_APPLICATION";
      const originalExists = request.snapshot.moneyEvents.some((entry): boolean => entry.canonicalTransactionId === intent.reversesTransactionId
        && entry.kind === originalKind && entry.status === "SETTLED" && entry.amountCents >= intent.amountCents);
      if (!originalExists) return answer(false, "Canonical original reversal basis is currently unverifiable");
    }
    const hash = financialMaterialityHash(request, state, intent.kind);
    if (hash === null) return answer(false, "Financial basis is currently unverifiable; this does not deny historical approval");
    if (hash !== intent.materialityHash) return answer(false, "Material financial entitlement or own route changed");
    if (intent.kind === "REFUND" && (intent.recipientVersionId !== state.refundInstructions.versionId
        || !routeUsable(request, state.refundInstructions, now))) return answer(false, "Refund recipient proof or route changed");
  }
  if (intent.targetVersionId !== targetVersionIdFor(state, intent)) return answer(false, "Exact target identity does not match");
  return answer(true, "Exact decision basis and current actor authority match; separate request admission still applies");
}
