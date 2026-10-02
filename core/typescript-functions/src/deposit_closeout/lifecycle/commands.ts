/** Pure Phase D orchestration. Persistence, receipt replay and root revisions belong to the adapter. */
import { canonical_json, ContractError, from_wire } from "../domain/codec.js";
import type { ReviewRequest } from "../domain/types.js";
import type { WorkAssignment } from "../phase_c/change_types.js";
import { hasAuthority } from "../phase_c/validation.js";
import { approvalGrant } from "./approvals.js";
import { parseLifecycleCommand, parsePureContext } from "./codec.js";
import { nativeActionKind } from "./events.js";
import { assertWorkflowScope, mapLegacyRecipients, nextBusinessClock, versionedRoute } from "./materiality.js";
import { applyDecisionCommand } from "./prerequisites.js";
import { applyRequestCommand, projectNativeFacts, reconcileRequestsAfterChange } from "./requests.js";
import type { LifecycleCommand, OperationInstructionsInput, OperationIntent, PureContext, WorkflowStateV2 } from "./types.js";

function requireAuthority(request: ReviewRequest, ctx: PureContext, role: string, action: string, amount: number | null = null): void {
  if (!hasAuthority(request, ctx.actorId, role, action, amount, ctx.serverNow)) {
    throw new ContractError(`No current actor-specific ${role} authority for ${action} and this amount`);
  }
}
function requireState(state: WorkflowStateV2 | null): WorkflowStateV2 {
  if (state === null) throw new ContractError("Initialize the workflow before lifecycle work");
  return state;
}
function instructionIntent(state: WorkflowStateV2 | null, id: string): OperationIntent {
  const instruction = requireState(state).requests.find((entry): boolean => entry.requestId === id);
  if (instruction === undefined) throw new ContractError("Request is not in this workflow");
  return instruction.intent;
}
function authorizeObservation(request: ReviewRequest, ctx: PureContext, intent: OperationIntent): void {
  if (intent.kind !== "STATEMENT_DISPATCH") {
    requireAuthority(request, ctx, "ACCOUNTANT", "RECONCILE_MONEY_RECORD", intent.amountCents);
    return;
  }
  if (!hasAuthority(request, ctx.actorId, "MANAGER", "ACCEPT_OR_CORRECT_FACT", null, ctx.serverNow)
      && !hasAuthority(request, ctx.actorId, "MANAGER", "REQUEST_STATEMENT_DISPATCH", null, ctx.serverNow)) {
    throw new ContractError("Recording statement outcomes requires current manager fact or dispatch authority");
  }
}

/**
 * Authorization only, safe BEFORE the adapter's early receipt replay. Immutable
 * targets supply kind/amount, never current applicability, budget or materiality.
 * @param request Current case access/membership and grants, already scope-gated by adapter.
 * @param workflow Current immutable records, or null for initialization.
 * @param command Strict semantic command; never an actor supplied by its payload.
 * @param ctx Trusted actor and actual server time, NOT the demonstration clock.
 */
export function authorizeLifecycleCommand(request: ReviewRequest, workflow: WorkflowStateV2 | null, command: LifecycleCommand, ctx: PureContext): void {
  ctx = parsePureContext(ctx);
  command = parseLifecycleCommand(command.kind, canonical_json(command.payload));
  switch (command.kind) {
    case "INIT_WORKFLOW":
    case "GENERATE_SIMULATED_RESULT":
      if (!ctx.isAdministrator) throw new ContractError("A trusted case administrator is required");
      return;
    case "ACCEPT_SCOPE_FACTS": case "SET_INTERIM_QUALIFICATION": case "UPSERT_RECIPIENT_PARTY":
    case "SET_STATEMENT_INSTRUCTIONS": case "SET_REFUND_INSTRUCTIONS":
      return requireAuthority(request, ctx, "MANAGER", "ACCEPT_OR_CORRECT_FACT");
    case "PREPARE_STATEMENT": return requireAuthority(request, ctx, "MANAGER", "PREPARE_STATEMENT");
    case "DECIDE_APPROVAL":
      if (approvalGrant(request, ctx.actorId, command.payload.intent.kind, command.payload.intent.amountCents, ctx.serverNow) === undefined) {
        throw new ContractError("No current actor-specific exact-version approval grant covers this kind and amount");
      }
      return;
    case "REQUEST_OPERATION": {
      const approval = requireState(workflow).approvals.find((entry): boolean => entry.approvalId === command.payload.approvalId);
      if (approval === undefined) throw new ContractError("Approval is not in this workflow");
      return requireAuthority(request, ctx, approval.scope === "STATEMENT_DISPATCH" ? "MANAGER" : "ACCOUNTANT",
        nativeActionKind(approval.scope), approval.intent.amountCents);
    }
    case "CLAIM_REQUEST": {
      const intent = instructionIntent(workflow, command.payload.requestId);
      return requireAuthority(request, ctx, intent.kind === "STATEMENT_DISPATCH" ? "MANAGER" : "ACCOUNTANT", nativeActionKind(intent.kind), intent.amountCents);
    }
    case "INGEST_RESULT": {
      const raw = requireState(workflow).events.find((entry): boolean => entry.kind === "RAW_SIMULATED_RESULT"
        && entry.sourceEventId === command.payload.sourceEventId);
      if (raw?.requestId === null || raw === undefined) throw new ContractError("Result is not in this workflow");
      return authorizeObservation(request, ctx, instructionIntent(workflow, raw.requestId));
    }
    case "RECORD_OUTCOME_UNKNOWN":
      // Recording uncertainty is conservative observation, not another payment.
      // Case access is trusted from the adapter, as in the request reducer.
      return;
    case "REVOKE_APPROVAL": {
      if (ctx.isAdministrator) return;
      const old = requireState(workflow).approvals.find((entry): boolean => entry.approvalId === command.payload.approvalId);
      if (old?.actorId !== ctx.actorId) throw new ContractError("Only the original approver or case administrator may withdraw approval");
      if (!request.snapshot.parties.some((party): boolean => party.partyId === old.actorPartyId)) {
        throw new ContractError("Withdrawing actor must identify an existing case party");
      }
      return;
    }
    case "CANCEL_UNATTEMPTED_REQUEST": {
      if (ctx.isAdministrator) return;
      const old = requireState(workflow).requests.find((entry): boolean => entry.requestId === command.payload.requestId);
      if (old?.createdBy !== ctx.actorId) throw new ContractError("Only the requester or case administrator may withdraw a request");
      return;
    }
  }
}

export interface LifecycleCommandResult {
  request: ReviewRequest;
  workflow: WorkflowStateV2;
  summary: Record<string, string | number | boolean | null>;
}

function reconcile(request: ReviewRequest, workflow: WorkflowStateV2, ctx: PureContext): { request: ReviewRequest; workflow: WorkflowStateV2 } {
  const next = structuredClone(request);
  const state = structuredClone(workflow);
  assertWorkflowScope(next, state);
  state.businessClock = nextBusinessClock(next, state, ctx.serverNow);
  next.reviewClock = state.businessClock;
  mapLegacyRecipients(next, state);
  const result = reconcileRequestsAfterChange(projectNativeFacts(next, state), state, ctx);
  result.workflow.businessClock = nextBusinessClock(result.request, result.workflow, ctx.serverNow);
  result.request.reviewClock = result.workflow.businessClock;
  mapLegacyRecipients(result.request, result.workflow);
  return { request: from_wire("ReviewRequest", projectNativeFacts(result.request, result.workflow)), workflow: result.workflow };
}

/** Apply one whitelisted pure reducer, then reconcile projections. No revision increment or I/O. */
export function applyLifecycleCommand(request: ReviewRequest, _workAssignments: readonly WorkAssignment[], workflow: WorkflowStateV2 | null,
  command: LifecycleCommand, ctx: PureContext): LifecycleCommandResult {
  ctx = parsePureContext(ctx);
  authorizeLifecycleCommand(request, workflow, command, ctx);
  const next = structuredClone(request);
  const state = workflow === null ? null : structuredClone(workflow);
  if (state !== null) {
    state.businessClock = nextBusinessClock(next, state, ctx.serverNow);
    next.reviewClock = state.businessClock;
  }
  let result: LifecycleCommandResult;
  switch (command.kind) {
    case "INIT_WORKFLOW": case "ACCEPT_SCOPE_FACTS": case "SET_INTERIM_QUALIFICATION": case "UPSERT_RECIPIENT_PARTY":
    case "SET_STATEMENT_INSTRUCTIONS": case "SET_REFUND_INSTRUCTIONS": case "PREPARE_STATEMENT":
    case "DECIDE_APPROVAL": case "REVOKE_APPROVAL":
      result = applyDecisionCommand(next, state, command, ctx); break;
    case "REQUEST_OPERATION": case "CLAIM_REQUEST": case "RECORD_OUTCOME_UNKNOWN":
    case "GENERATE_SIMULATED_RESULT": case "INGEST_RESULT": case "CANCEL_UNATTEMPTED_REQUEST":
      result = applyRequestCommand(next, requireState(state), command, ctx); break;
  }
  return { ...reconcile(result.request, result.workflow, ctx), summary: result.summary };
}

/**
 * Call after EVERY C mutation once v2 exists. Only an explicit change to C's
 * combined recipient content maps both channels. A D single-channel command
 * never uses this bridge. Historical instructions/statements stay frozen.
 */
export function reconcileWorkflowAfterCaseChange(previousRequest: ReviewRequest, nextRequest: ReviewRequest,
  _workAssignments: readonly WorkAssignment[], workflow: WorkflowStateV2, ctx: PureContext): { request: ReviewRequest; workflow: WorkflowStateV2 } {
  ctx = parsePureContext(ctx);
  const next = structuredClone(nextRequest);
  const state = structuredClone(workflow);
  const content = (r: ReviewRequest): Omit<ReviewRequest["snapshot"]["recipients"], "versionId"> => {
    const { versionId: _version, ...value } = r.snapshot.recipients;
    return { ...value, statementPartyIds: [...value.statementPartyIds].sort(), refundPartyIds: [...value.refundPartyIds].sort(), evidenceIds: [...value.evidenceIds].sort() };
  };
  if (canonical_json(content(previousRequest)) !== canonical_json(content(next))) {
    const legacy = next.snapshot.recipients;
    const channel = (kind: "STATEMENT" | "REFUND"): OperationInstructionsInput => ({
      partyIds: [...(kind === "STATEMENT" ? legacy.statementPartyIds : legacy.refundPartyIds)],
      state: legacy.state === "VERIFIED" ? "VERIFIED" : "UNCONFIRMED",
      method: (kind === "STATEMENT" ? legacy.statementMethod : legacy.refundMethod) === "DEMO_OUTBOX" ? "DEMO_OUTBOX" : null,
      routeReference: legacy.verifiedRouteReference !== null && /^demo-[A-Za-z0-9][A-Za-z0-9._-]{0,199}$/.test(legacy.verifiedRouteReference)
        ? legacy.verifiedRouteReference : null,
      evidenceIds: [...legacy.evidenceIds],
    });
    state.statementInstructions = versionedRoute(state, "STATEMENT", channel("STATEMENT"));
    state.refundInstructions = versionedRoute(state, "REFUND", channel("REFUND"));
  }
  // C's RECHECK may propose actual now behind a demo clock; v2 never rewinds.
  state.businessClock = nextBusinessClock(previousRequest, state, ctx.serverNow);
  return reconcile(next, state, ctx);
}
