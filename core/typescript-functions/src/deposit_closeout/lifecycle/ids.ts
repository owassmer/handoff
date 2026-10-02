/** Deterministic identities only, never authority, effect, or current-state claims. */
import { ContractError } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import type {
  FinancialIntent, OperationInstructions, OperationInstructionsInput, OperationIntent,
  RawSimulatedResult, StatementContent, StatementDispatchIntent, StatementKind,
  WorkflowEventKind, WorkflowScope,
} from "./types.js";

export interface StatementIdentityBasis {
  kind: StatementKind;
  materialityHash: string;
  contentHash: string;
  recipientVersionId: string;
  supersedesStatementId: string | null;
}
export interface WorkflowEventIdentity {
  kind: WorkflowEventKind;
  requestId: string | null;
  attemptId: string | null;
  sourceEventId: string | null;
}
export type UntargetedIntent = Omit<FinancialIntent, "targetVersionId"> | Omit<StatementDispatchIntent, "targetVersionId">;

function scopeKey(scope: WorkflowScope): WorkflowScope {
  return { environmentId: scope.environmentId, managementCompanyId: scope.managementCompanyId, caseId: scope.caseId };
}

/**
 * Financial statements are display links, not entitlement. In particular this
 * deliberately excludes whole-case revision/inputHash, current held/unpaid
 * balances, statement-only route/text, approval/command identity, and timestamps.
 * The caller derives materialityHash from stable decisions/entitlement + own route.
 */
export function operationIdentity(intent: UntargetedIntent): UntargetedIntent {
  const common = {
    amountCents: intent.amountCents, currency: intent.currency, dispositionKey: intent.dispositionKey,
    recipientVersionId: intent.recipientVersionId, materialityHash: intent.materialityHash,
    replacesRequestId: intent.replacesRequestId, reversesTransactionId: intent.reversesTransactionId,
  };
  if (intent.kind === "STATEMENT_DISPATCH") {
    return { ...common, kind: intent.kind, amountCents: null, statementId: intent.statementId,
      recipientVersionId: intent.recipientVersionId, contentHash: intent.contentHash, reversesTransactionId: null };
  }
  return { ...common, kind: intent.kind, amountCents: intent.amountCents, statementId: null };
}

export function targetVersionIdFor(scope: WorkflowScope, intent: UntargetedIntent): string {
  return `dc-target:${fingerprint({ scope: scopeKey(scope), intent: operationIdentity(intent) })}`;
}

/** Different approvals and commands for the same scoped intent cannot double-request. */
export function instructionKeyFor(scope: WorkflowScope, intent: OperationIntent): string {
  return `dc-instruction:${fingerprint({ scope: scopeKey(scope), intent: operationIdentity(intent) })}`;
}
export function requestIdFor(scope: WorkflowScope, intent: OperationIntent): string {
  return `dc-request:${fingerprint({ scope: scopeKey(scope), intent: operationIdentity(intent) })}`;
}
export function instructionHashFor(
  scope: WorkflowScope, intent: OperationIntent, instructions: OperationInstructions | null,
): string {
  const route = instructions === null ? null : { versionId: instructions.versionId,
    partyIds: [...instructions.partyIds].sort(), state: instructions.state, method: instructions.method,
    routeReference: instructions.routeReference, evidenceIds: [...instructions.evidenceIds].sort() };
  return fingerprint({ scope: scopeKey(scope), intent: operationIdentity(intent), instructions: route });
}

/** Creation provenance and source review identity are deliberately outside content/statement identity. */
export function statementContentHash(content: StatementContent, renderedText: string): string {
  return fingerprint({ content, renderedText });
}
export function statementIdFor(scope: WorkflowScope, basis: StatementIdentityBasis): string {
  return `dc-statement:${fingerprint({ scope: scopeKey(scope), basis: {
    kind: basis.kind, materialityHash: basis.materialityHash, contentHash: basis.contentHash,
    recipientVersionId: basis.recipientVersionId, supersedesStatementId: basis.supersedesStatementId,
  } })}`;
}
export function approvalIdFor(scope: WorkflowScope, commandId: string, actorId: string): string {
  return `dc-approval:${fingerprint({ scope: scopeKey(scope), commandId, actorId })}`;
}
export function recipientVersionIdFor(
  scope: WorkflowScope, channel: "STATEMENT" | "REFUND", instructions: OperationInstructionsInput,
): string {
  return `dc-recipient:${fingerprint({ scope: scopeKey(scope), channel, instructions: {
    partyIds: [...instructions.partyIds].sort(), state: instructions.state, method: instructions.method,
    routeReference: instructions.routeReference, evidenceIds: [...instructions.evidenceIds].sort(),
  } })}`;
}
export function attemptIdFor(scope: WorkflowScope, requestId: string, attemptNumber: number): string {
  if (!Number.isSafeInteger(attemptNumber) || attemptNumber < 1) {
    throw new ContractError("Attempt number must be a positive exact integer");
  }
  return `dc-attempt:${fingerprint({ scope: scopeKey(scope), requestId, attemptNumber })}`;
}

/** One canonical economic operation per request, independent of delivery/source event IDs. */
export function canonicalTransactionIdFor(scope: WorkflowScope, requestId: string): string {
  return `dc-transaction:${fingerprint({ scope: scopeKey(scope), requestId })}`;
}
/** One full return identity per original operation; distinct from a separately authorized reversal request. */
export function returnTransactionIdFor(scope: WorkflowScope, originalCanonicalTransactionId: string): string {
  return `dc-transaction:${fingerprint({ scope: scopeKey(scope), returnOfCanonicalTransactionId: originalCanonicalTransactionId })}`;
}

/**
 * Source-event identity is actor/command independent. A conflicting redelivery
 * has the SAME ID and must be reconciled, never appended as a last-row-wins event.
 * Acceptance is distinct from raw receipt and carries no economic effect itself.
 */
export function workflowEventIdFor(scope: WorkflowScope, identity: WorkflowEventIdentity): string {
  if (identity.kind === "RAW_SIMULATED_RESULT" || identity.kind === "RESULT_ACCEPTED") {
    if (identity.sourceEventId === null) throw new ContractError("Result identity requires a source event ID");
    return `dc-workflow-event:${fingerprint({ scope: scopeKey(scope), kind: identity.kind,
      sourceEventId: identity.sourceEventId })}`;
  }
  return `dc-workflow-event:${fingerprint({ scope: scopeKey(scope), kind: identity.kind,
    requestId: identity.requestId, attemptId: identity.attemptId, sourceEventId: identity.sourceEventId })}`;
}

/** Compare payloads for a source identity without transport/provenance metadata. */
export function resultIdentityHash(result: RawSimulatedResult): string {
  return fingerprint({ requestId: result.requestId, attemptId: result.attemptId, sourceEventId: result.sourceEventId,
    kind: result.kind, operationKind: result.operationKind, instructionHash: result.instructionHash,
    amountCents: result.amountCents, currency: result.currency, recipientVersionId: result.recipientVersionId,
    canonicalTransactionId: result.canonicalTransactionId,
    returnOfCanonicalTransactionId: result.returnOfCanonicalTransactionId });
}

/** Compare canonical economic effects across distinct source deliveries/attempt metadata. */
export function economicResultIdentityHash(result: RawSimulatedResult): string {
  return fingerprint({ requestId: result.requestId, kind: result.kind, operationKind: result.operationKind,
    instructionHash: result.instructionHash, amountCents: result.amountCents, currency: result.currency,
    recipientVersionId: result.recipientVersionId, canonicalTransactionId: result.canonicalTransactionId,
    returnOfCanonicalTransactionId: result.returnOfCanonicalTransactionId });
}
