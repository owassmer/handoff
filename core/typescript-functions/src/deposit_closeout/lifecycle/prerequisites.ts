/** Narrow semantic commands. No generic patch, authority creation, money, I/O or implicit clock reads. */
import { canonical_json, ContractError, from_wire } from "../domain/codec.js";
import { valid_evidence } from "../domain/validation.js";
import type { ReviewRequest } from "../domain/types.js";
import { hasAuthority, nativeReview } from "../phase_c/validation.js";
import { decideApproval, revokeApproval } from "./approvals.js";
import { parseLifecycleCommand, parsePureContext, validateWorkflowCaseReferences } from "./codec.js";
import { assertWorkflowScope, mapLegacyRecipients, nextBusinessClock, routeUsable, versionedRoute, workflowScope } from "./materiality.js";
import { prepareStatement } from "./statements.js";
import type { LifecycleCommand, OperationInstructionsInput, PureContext, WorkflowStateV2 } from "./types.js";

function requireManager(request: ReviewRequest, ctx: PureContext, action: string = "ACCEPT_OR_CORRECT_FACT"): void {
  if (!hasAuthority(request, ctx.actorId, "MANAGER", action, null, ctx.serverNow)) {
    throw new ContractError(`No current actor-specific manager authority for ${action}`);
  }
}

function requireProof(request: ReviewRequest, ids: readonly string[], ctx: PureContext): void {
  if (!valid_evidence(request.snapshot, ids, ctx.serverNow)) {
    throw new ContractError("Supply accepted current-case evidence known at actual server time; model proposals are not proof");
  }
}

/** Split C's shared reference without upgrading unconfirmed instructions or inventing a route. */
export function initializeWorkflow(request: ReviewRequest, ctx: PureContext): WorkflowStateV2 {
  ctx = parsePureContext(ctx);
  if (!ctx.isAdministrator) throw new ContractError("Only a trusted case administrator may initialize the workflow");
  const scope = workflowScope(request);
  const legacy = request.snapshot.recipients;
  const route = legacy.verifiedRouteReference !== null && /^demo-[A-Za-z0-9][A-Za-z0-9._-]{0,199}$/.test(legacy.verifiedRouteReference)
    ? legacy.verifiedRouteReference : null;
  const split = (channel: "STATEMENT" | "REFUND"): ReturnType<typeof versionedRoute> => {
    const method = channel === "STATEMENT" ? legacy.statementMethod : legacy.refundMethod;
    const input: OperationInstructionsInput = { partyIds: [...(channel === "STATEMENT" ? legacy.statementPartyIds : legacy.refundPartyIds)],
      state: "UNCONFIRMED", method: method === "DEMO_OUTBOX" ? "DEMO_OUTBOX" : null,
      routeReference: route, evidenceIds: [...legacy.evidenceIds] };
    const candidate = versionedRoute(scope, channel, { ...input, state: "VERIFIED" });
    if (legacy.state === "VERIFIED" && routeUsable(request, candidate, ctx.serverNow)) input.state = "VERIFIED";
    return versionedRoute(scope, channel, input);
  };
  const state: WorkflowStateV2 = { ...scope, schemaVersion: "2.0.0", mode: "SIMULATED", initializedBy: ctx.actorId,
    initializedAt: ctx.serverNow, businessClock: nextBusinessClock(request, null, ctx.serverNow),
    statementInstructions: split("STATEMENT"), refundInstructions: split("REFUND"),
    statements: [], approvals: [], requests: [], events: [], currentStatementId: null };
  validateWorkflowCaseReferences(state, request.snapshot);
  return state;
}

export interface DecisionCommandResult {
  request: ReviewRequest;
  workflow: WorkflowStateV2;
  summary: Record<string, string | number | boolean | null>;
}

/**
 * Clone all inputs, authorize against actual server time, advance only business
 * time, and perform one whitelisted semantic update. Revision belongs to adapter.
 */
export function applyDecisionCommand(request: ReviewRequest, state: WorkflowStateV2 | null, command: LifecycleCommand, ctx: PureContext): DecisionCommandResult {
  const supported = ["INIT_WORKFLOW", "ACCEPT_SCOPE_FACTS", "SET_INTERIM_QUALIFICATION", "UPSERT_RECIPIENT_PARTY",
    "SET_STATEMENT_INSTRUCTIONS", "SET_REFUND_INSTRUCTIONS", "PREPARE_STATEMENT", "DECIDE_APPROVAL", "REVOKE_APPROVAL"];
  if (!supported.includes(command.kind)) throw new ContractError(`Decision reducer does not support ${command.kind}`);
  ctx = parsePureContext(ctx);
  command = parseLifecycleCommand(command.kind, canonical_json(command.payload));
  const next = from_wire("ReviewRequest", structuredClone(request));
  if (command.kind === "INIT_WORKFLOW" && !ctx.isAdministrator) throw new ContractError("Only an administrator may initialize the workflow");
  if (state === null && command.kind !== "INIT_WORKFLOW") throw new ContractError("Initialize the workflow before lifecycle decisions");
  const workflow = state === null ? initializeWorkflow(next, ctx) : structuredClone(state);
  assertWorkflowScope(next, workflow);
  workflow.businessClock = nextBusinessClock(next, workflow, ctx.serverNow);
  next.reviewClock = workflow.businessClock;
  const summary: DecisionCommandResult["summary"] = { commandKind: command.kind };
  switch (command.kind) {
    case "INIT_WORKFLOW": summary.initialized = state === null; break;
    case "ACCEPT_SCOPE_FACTS": {
      requireManager(next, ctx);
      const p = command.payload;
      requireProof(next, p.evidenceIds, ctx);
      next.snapshot.jurisdiction = p.jurisdiction;
      next.snapshot.tenancyRegime = p.tenancyRegime;
      next.snapshot.tenancyEndsInFull = p.tenancyEndsInFull;
      next.snapshot.cashSecurityDeposit = p.cashSecurityDeposit;
      next.snapshot.agreementEvidenceIds = [...p.evidenceIds];
      summary.reason = p.reason;
      break;
    }
    case "SET_INTERIM_QUALIFICATION": {
      requireManager(next, ctx);
      const p = command.payload;
      // A deliberate negative/unconfirmed decision can explain missing proof;
      // an acceptance cannot manufacture an exception from an invoice delay.
      if (p.state === "ACCEPTED" || p.evidenceIds.length > 0) requireProof(next, p.evidenceIds, ctx);
      next.snapshot.interimConditionState = p.state;
      next.snapshot.interimConditionEvidenceIds = [...p.evidenceIds];
      next.snapshot.interimConditionReason = p.reason;
      summary.interimConditionState = p.state;
      break;
    }
    case "UPSERT_RECIPIENT_PARTY": {
      requireManager(next, ctx);
      const party = command.payload.party;
      requireProof(next, party.evidenceIds, ctx);
      const old = next.snapshot.parties.find((entry): boolean => entry.partyId === party.partyId);
      if (old !== undefined && (old.principalId !== null
          || old.roles.some((role): boolean => !["RESIDENT", "SIGNATORY"].includes(role))
          || next.snapshot.authorityGrants.some((grant): boolean => grant.partyId === old.partyId)
          || next.snapshot.depositBalance.custodianPartyId === old.partyId)) {
        throw new ContractError("Recipient upsert cannot overwrite an operator, custodian, principal or authority-bearing party");
      }
      if (old === undefined) next.snapshot.parties.push(structuredClone(party));
      else next.snapshot.parties = next.snapshot.parties.map((entry) => entry.partyId === party.partyId ? structuredClone(party) : entry);
      summary.partyId = party.partyId;
      break;
    }
    case "SET_STATEMENT_INSTRUCTIONS":
    case "SET_REFUND_INSTRUCTIONS": {
      requireManager(next, ctx);
      const p = command.payload;
      if (p.evidenceIds.length > 0 || p.state === "VERIFIED") requireProof(next, p.evidenceIds, ctx);
      if (!p.partyIds.every((id): boolean => next.snapshot.parties.some((party): boolean => party.partyId === id
          && party.roles.some((role): boolean => ["RESIDENT", "SIGNATORY"].includes(role))))) {
        throw new ContractError("Instructions must select case-local resident/signatory parties, not an owner or operator default");
      }
      const channel = command.kind === "SET_STATEMENT_INSTRUCTIONS" ? "STATEMENT" : "REFUND";
      const route = versionedRoute(workflow, channel, p);
      if (p.state === "VERIFIED" && !routeUsable(next, route, ctx.serverNow)) throw new ContractError("Verify recipient membership and route evidence first");
      if (channel === "STATEMENT") workflow.statementInstructions = route;
      else workflow.refundInstructions = route;
      summary.recipientVersionId = route.versionId;
      break;
    }
    case "PREPARE_STATEMENT": {
      requireManager(next, ctx, "PREPARE_STATEMENT");
      mapLegacyRecipients(next, workflow);
      const statement = prepareStatement(next, nativeReview(next), workflow, command.payload, ctx);
      if (!workflow.statements.some((entry): boolean => entry.statementId === statement.statementId)) workflow.statements.push(statement);
      workflow.currentStatementId = statement.statementId;
      summary.statementId = statement.statementId;
      break;
    }
    case "DECIDE_APPROVAL": {
      mapLegacyRecipients(next, workflow);
      const record = decideApproval(next, nativeReview(next), workflow, command.payload, ctx);
      const old = workflow.approvals.find((entry): boolean => entry.approvalId === record.approvalId);
      if (old !== undefined && canonical_json(old) !== canonical_json(record)) throw new ContractError("Approval command identity was already used with different content");
      if (old === undefined) workflow.approvals.push(record);
      summary.approvalId = record.approvalId;
      summary.decision = record.decision;
      break;
    }
    case "REVOKE_APPROVAL": {
      const record = revokeApproval(next, workflow, command.payload.approvalId, ctx);
      const old = workflow.approvals.find((entry): boolean => entry.approvalId === record.approvalId);
      if (old !== undefined && canonical_json(old) !== canonical_json(record)) throw new ContractError("Revocation command identity was already used with different content");
      if (old === undefined) workflow.approvals.push(record);
      summary.approvalId = record.approvalId;
      summary.revokesApprovalId = command.payload.approvalId;
      summary.reason = command.payload.reason;
      break;
    }
    default: throw new ContractError(`Decision reducer does not support ${command.kind}`);
  }
  mapLegacyRecipients(next, workflow);
  validateWorkflowCaseReferences(workflow, next.snapshot);
  return { request: next, workflow, summary };
}
