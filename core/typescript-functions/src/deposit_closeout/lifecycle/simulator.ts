/** Deterministic demonstration producer and separate proof ingestion. No external effects. */
import { canonical_json, from_wire } from "../domain/codec.js";
import { compare_timestamps } from "../domain/datetime.js";
import { fingerprint } from "../domain/fingerprints.js";
import { _Problems, _evidence_checker, _requests, _transactions, type _Transaction } from "../domain/money.js";
import type { EvidenceInput, MoneyEvent, ReviewRequest } from "../domain/types.js";
import { canonicalTransactionIdFor, economicResultIdentityHash, resultIdentityHash } from "./ids.js";
import { appendWorkflowEvent, nextBusinessInstant, projectNativeFacts, projectRequests, requireLifecycle, simulatorEvidenceId } from "./events.js";
export { simulatorEvidenceId } from "./events.js";
import type { GenerateSimulatedResultPayload, PureContext, RawSimulatedResult, RequestInstruction, WorkflowEvent, WorkflowScope, WorkflowStateV2 } from "./types.js";

export type RawResultEvent = Extract<WorkflowEvent, { kind: "RAW_SIMULATED_RESULT" }>;
export interface RequestMutationResult {
  request: ReviewRequest;
  workflow: WorkflowStateV2;
  summary: Record<string, string | number | boolean | null>;
}

/** Delegate topology, proof, principal and reversal validation to the unchanged native ledger. */
export function verifiedNativeTransactions(request: ReviewRequest): Map<string, _Transaction> {
  const problems = new _Problems();
  // Native _requests intentionally makes the whole ACCOUNT unverified for an
  // unknown outcome. That must not prevent the very result ingestion that can
  // resolve it. For transaction topology inspection only, retain its outstanding
  // payload as REQUESTED. Never persist this inspection copy or use it for budget.
  const inspection = { ...request.snapshot, priorRequests: request.snapshot.priorRequests.map((fact) => ({
    ...fact, state: fact.state === "OUTCOME_UNKNOWN" ? "REQUESTED" : fact.state,
  })) };
  const requests = _requests(inspection, problems);
  const transactions = _transactions(inspection, requests, request.reviewClock,
    problems, _evidence_checker(inspection, request.reviewClock, problems));
  requireLifecycle(problems.entries.size === 0,
    `Accounting proof requires explicit reconciliation: ${problems.questions().map((problem): string => problem.reason).join(" ")}`);
  return transactions;
}

/** Canonical chain bounds only; all account/entitlement arithmetic remains in nativeReview. */
export function remainingCanonicalPrincipal(transactions: ReadonlyMap<string, _Transaction>, originalId: string): number {
  const original = transactions.get(originalId);
  requireLifecycle(original !== undefined && original.settlement_at() !== null, "Original canonical settlement is not verified.");
  const reductions = [...transactions.values()].filter((transaction): boolean => transaction.target === originalId);
  const remaining = reductions.reduce((sum, transaction): bigint => sum - BigInt(transaction.nominal),
    BigInt(original.nominal) - BigInt(original.returned()));
  requireLifecycle(remaining >= 0n && remaining <= BigInt(Number.MAX_SAFE_INTEGER), "Original principal requires reconciliation.");
  return Number(remaining);
}

/** The frozen two-argument ID helper describes one FULL return only. Each partial
 * source operation needs its own scoped identity; no frozen contract is changed.
 * Exact economic redeliveries are correlated by producer amount + occurrence below.
 */
export function partialReturnTransactionIdFor(scope: WorkflowScope, originalId: string, sourceEventId: string): string {
  return `dc-transaction:${fingerprint({ scope: { caseId: scope.caseId,
    managementCompanyId: scope.managementCompanyId, environmentId: scope.environmentId },
    returnOfCanonicalTransactionId: originalId, sourceEventId })}`;
}

export function acceptedRawResults(state: WorkflowStateV2): RawResultEvent[] {
  const ids = new Set(state.events.flatMap((event): string[] => event.kind === "RESULT_ACCEPTED" ? [event.payload.rawEventId] : []));
  return state.events.filter((event): event is RawResultEvent => event.kind === "RAW_SIMULATED_RESULT" && ids.has(event.eventId));
}

/** C manual facts must not be silently interpreted as a D result or lead to another send. */
export function requireNoUncorrelatedNativeFacts(request: ReviewRequest, state: WorkflowStateV2, requestId: string): void {
  const accepted = acceptedRawResults(state);
  requireLifecycle(!request.snapshot.moneyEvents.some((event): boolean => event.requestId === requestId
    && !accepted.some((raw): boolean => raw.payload.canonicalTransactionId === event.canonicalTransactionId
      && raw.sourceEventId === event.sourceEventId && event.sourceEvidenceId === simulatorEvidenceId(raw.eventId)
      && event.eventId === `dc-money:${fingerprint({ rawEventId: raw.eventId })}`
      && event.amountCents === raw.payload.amountCents && compare_timestamps(event.occurredAt, raw.occurredAt) === 0
      && event.reversesTransactionId === (raw.payload.returnOfCanonicalTransactionId
        ?? state.requests.find((instruction): boolean => instruction.requestId === raw.requestId)?.reversesTransactionId ?? null)
      && event.status === (raw.payload.kind === "RETURNED" ? "RETURNED" : "SETTLED")
      && event.kind === (raw.payload.kind === "RETURNED" ? "REFUND_RETURNED"
        : raw.payload.operationKind === "REFUND" ? "REFUND_SETTLED" : raw.payload.operationKind))),
  "A linked manual accounting fact has no accepted D correlation; reconcile it before sending.");
  requireLifecycle(!request.snapshot.executionEvents.some((event): boolean => event.requestId === requestId
    && ["RESULT", "MANUAL_CONFIRMATION", "RECONCILIATION"].includes(event.kind)
    && !accepted.some((raw): boolean => event.evidenceIds.includes(simulatorEvidenceId(raw.eventId)))),
  "A linked manual execution result requires explicit reconciliation before sending.");
}

function rawPayload(
  state: WorkflowStateV2, instruction: RequestInstruction, payload: GenerateSimulatedResultPayload, occurredAt: string,
): RawSimulatedResult {
  const amount = instruction.intent.amountCents;
  requireLifecycle(instruction.kind === "STATEMENT_DISPATCH" ? payload.amountCents === null
    : Number.isSafeInteger(payload.amountCents) && payload.amountCents !== null && payload.amountCents > 0,
  "Simulator amount must be positive known cents, or null for a statement.");
  requireLifecycle(payload.outcome === "RETURNED" ? instruction.kind === "REFUND"
    && payload.amountCents !== null && amount !== null && payload.amountCents <= amount
    : payload.amountCents === amount, "Simulator amount or outcome differs from the immutable instruction.");
  const original = canonicalTransactionIdFor(state, instruction.requestId);
  let transactionId: string | null = instruction.kind !== "STATEMENT_DISPATCH" && payload.outcome === "SUCCEEDED" ? original : null;
  if (payload.outcome === "RETURNED") {
    // A redelivery can name a different transport/source ID. Explicitly identical
    // producer occurrence and amount identify the same return, not a second effect.
    const corroborated = state.events.find((event): boolean => event.kind === "RAW_SIMULATED_RESULT"
      && event.requestId === instruction.requestId && event.payload.kind === "RETURNED"
      && event.payload.amountCents === payload.amountCents && compare_timestamps(event.occurredAt, occurredAt) === 0);
    transactionId = corroborated?.kind === "RAW_SIMULATED_RESULT" ? corroborated.payload.canonicalTransactionId
      : partialReturnTransactionIdFor(state, original, payload.sourceEventId);
  }
  return { requestId: instruction.requestId, attemptId: payload.attemptId, sourceEventId: payload.sourceEventId,
    kind: payload.outcome, operationKind: instruction.kind, instructionHash: instruction.instructionHash,
    amountCents: payload.amountCents, currency: "USD", recipientVersionId: instruction.intent.recipientVersionId,
    canonicalTransactionId: transactionId, returnOfCanonicalTransactionId: payload.outcome === "RETURNED" ? original : null };
}

/** Only writes RAW; the caller gates a first send, while late observations need no new approval. */
export function generateSimulatedResult(
  request: ReviewRequest, inputState: WorkflowStateV2, instruction: RequestInstruction,
  payload: GenerateSimulatedResultPayload, ctx: PureContext,
): RequestMutationResult {
  const state = structuredClone(inputState);
  requireLifecycle(ctx.isAdministrator, "Only the trusted demonstration administrator may select simulator outcomes.");
  requireLifecycle(payload.requestId === instruction.requestId && state.events.some((event): boolean =>
    event.kind === "ATTEMPT_CLAIMED" && event.requestId === instruction.requestId && event.attemptId === payload.attemptId),
  "The actual attempt must belong to this immutable request.");
  const existing = state.events.find((event): boolean => event.kind === "RAW_SIMULATED_RESULT" && event.sourceEventId === payload.sourceEventId);
  const equalReturns = state.events.filter((event): event is RawResultEvent => event.kind === "RAW_SIMULATED_RESULT"
    && event.requestId === instruction.requestId && event.payload.kind === "RETURNED" && event.payload.amountCents === payload.amountCents);
  const distinctReturns = new Set(equalReturns.map((event): string | null => event.payload.canonicalTransactionId));
  // The wire has no independent producer economic-return ID. Do not let a new
  // delivery ID silently manufacture another equal partial return. Null occurrence
  // conservatively corroborates the sole prior equal return; an actually separate
  // equal-valued return must provide its explicit distinct producer occurrence.
  if (payload.outcome === "RETURNED" && payload.occurredAt === null && existing === undefined) {
    requireLifecycle(distinctReturns.size <= 1, "Ambiguous equal partial returns: supply the explicit producer occurrence to correlate this delivery.");
  }
  const corroboratingOccurrence = payload.outcome === "RETURNED" && distinctReturns.size === 1 ? equalReturns[0]?.occurredAt : undefined;
  const occurredAt = payload.occurredAt ?? existing?.occurredAt ?? corroboratingOccurrence ?? nextBusinessInstant(state);
  const raw = rawPayload(state, instruction, payload, occurredAt);
  if (existing !== undefined) {
    requireLifecycle(existing.kind === "RAW_SIMULATED_RESULT" && resultIdentityHash(existing.payload) === resultIdentityHash(raw)
      && compare_timestamps(existing.occurredAt, occurredAt) === 0, "Conflicting source-event payload or occurrence; preserve the raw observation and reconcile.");
    return { request, workflow: state, summary: { requestId: instruction.requestId, rawEventId: existing.eventId, replayed: true } };
  }
  const event = appendWorkflowEvent(state, ctx, instruction.requestId, payload.attemptId, payload.sourceEventId,
    { category: "SIMULATED_RESULT", kind: "RAW_SIMULATED_RESULT", payload: raw }, occurredAt);
  return { request: projectNativeFacts(request, state), workflow: state,
    summary: { requestId: instruction.requestId, rawEventId: event.eventId, accepted: false } };
}

function validateRawCorrelation(state: WorkflowStateV2, instruction: RequestInstruction, raw: RawResultEvent): void {
  const payload = raw.payload;
  requireLifecycle(payload.requestId === instruction.requestId && payload.operationKind === instruction.kind
    && payload.instructionHash === instruction.instructionHash && payload.currency === "USD"
    && payload.recipientVersionId === instruction.intent.recipientVersionId,
  "Raw result kind, currency, route or immutable instruction correlation differs; reconcile explicitly.");
  const claim = state.events.find((event): boolean => event.kind === "ATTEMPT_CLAIMED"
    && event.requestId === instruction.requestId && event.attemptId === payload.attemptId && event.sequence < raw.sequence);
  requireLifecycle(claim !== undefined && compare_timestamps(claim.occurredAt, raw.occurredAt) <= 0,
    "Result must identify a preceding actual claim and cannot predate it.");
  const expected = rawPayload(state, instruction, { requestId: instruction.requestId, attemptId: payload.attemptId,
    sourceEventId: payload.sourceEventId, outcome: payload.kind, amountCents: payload.amountCents, occurredAt: raw.occurredAt }, raw.occurredAt);
  // Recompute return producer identity without allowing the row to validate itself.
  if (payload.kind === "RETURNED") {
    const earlier = state.events.find((event): boolean => event.kind === "RAW_SIMULATED_RESULT"
      && event.sequence < raw.sequence && event.requestId === raw.requestId && event.payload.kind === "RETURNED"
      && event.payload.amountCents === payload.amountCents && compare_timestamps(event.occurredAt, raw.occurredAt) === 0);
    expected.canonicalTransactionId = earlier?.kind === "RAW_SIMULATED_RESULT" ? earlier.payload.canonicalTransactionId
      : partialReturnTransactionIdFor(state, canonicalTransactionIdFor(state, instruction.requestId), payload.sourceEventId);
  }
  requireLifecycle(resultIdentityHash(payload) === resultIdentityHash(expected), "Result economic identity was not produced by this scoped simulator.");
}

/** Canonical proof is created only during acceptance, never by raw receipt. */
export function canonicalEvidenceInput(raw: RawResultEvent, learnedAt: string): EvidenceInput {
  return from_wire("EvidenceInput", { evidenceId: simulatorEvidenceId(raw.eventId), recordKind: "SOURCE_EVENT",
    sourceClass: "TEST_ASSUMPTION", externalRecordId: raw.payload.sourceEventId, sourceVersion: "phase-d-simulator-v1",
    locator: `demo:${raw.eventId}`, occurredAt: raw.occurredAt, learnedAt, supersedesEvidenceId: null,
    proposedItemIds: [], associationAccepted: true, excerpt: "Trusted synthetic simulator result; NOT legal or external performance." });
}

/** A new D reversal request remains the performing request in WorkflowEvent.
 * The NATIVE MoneyEvent.requestId MUST preserve the ORIGINAL canonical chain's
 * request identity (and charge item) because native _transactions enforces it.
 */
export function mapNativeMoneyEvent(
  instruction: RequestInstruction, raw: RawResultEvent, learnedAt: string, transactions: ReadonlyMap<string, _Transaction>,
): MoneyEvent | null {
  if (instruction.kind === "STATEMENT_DISPATCH" || raw.payload.kind === "FAILED") return null;
  const reverses = raw.payload.returnOfCanonicalTransactionId ?? instruction.reversesTransactionId;
  const original = reverses === null ? undefined : transactions.get(reverses);
  requireLifecycle(reverses === null || original !== undefined, "A reversal/return needs a verified original canonical transaction.");
  requireLifecycle(raw.payload.canonicalTransactionId !== null && raw.payload.amountCents !== null, "Missing monetary proof.");
  return from_wire("MoneyEvent", { eventId: `dc-money:${fingerprint({ rawEventId: raw.eventId })}`,
    canonicalTransactionId: raw.payload.canonicalTransactionId, sourceEventId: raw.payload.sourceEventId,
    kind: raw.payload.kind === "RETURNED" ? "REFUND_RETURNED" : instruction.kind === "REFUND" ? "REFUND_SETTLED" : instruction.kind,
    status: raw.payload.kind === "RETURNED" ? "RETURNED" : "SETTLED", amountCents: raw.payload.amountCents,
    occurredAt: raw.occurredAt, learnedAt, sourceEvidenceId: simulatorEvidenceId(raw.eventId),
    requestId: original === undefined ? instruction.requestId : original.request,
    reversesTransactionId: reverses, chargeItemId: original?.item ?? null });
}

/** Accept immutable, validated proof against the current case. No root revision or I/O. */
export function ingestSimulatedResult(
  request: ReviewRequest, inputState: WorkflowStateV2, sourceEventId: string, ctx: PureContext,
): RequestMutationResult {
  const state = structuredClone(inputState);
  const accepted = state.events.find((event): boolean => event.kind === "RESULT_ACCEPTED" && event.sourceEventId === sourceEventId);
  if (accepted !== undefined) return { request, workflow: state, summary: { acceptedEventId: accepted.eventId, replayed: true } };
  const raw = state.events.find((event): event is RawResultEvent => event.kind === "RAW_SIMULATED_RESULT" && event.sourceEventId === sourceEventId);
  requireLifecycle(raw !== undefined, "Ingestion requires a persisted raw simulator result.");
  const instruction = state.requests.find((entry): boolean => entry.requestId === raw.requestId);
  requireLifecycle(instruction !== undefined, "Raw result references a missing instruction.");
  validateRawCorrelation(state, instruction, raw);
  const current = projectRequests(state).find((entry): boolean => entry.requestId === instruction.requestId)!;
  requireLifecycle(current.attemptId === raw.attemptId && !["READY", "CANCELLED", "SUPERSEDED"].includes(current.state),
    "Result does not match the potentially attempted request.");
  const prior = acceptedRawResults(state).filter((entry): boolean => entry.requestId === instruction.requestId);
  requireLifecycle(!prior.some((entry): boolean => (entry.payload.kind === "FAILED" && raw.payload.kind !== "FAILED")
    || (entry.payload.kind !== "FAILED" && raw.payload.kind === "FAILED")),
  "A failure and settlement/return contradict each other; retain raw evidence for explicit reconciliation.");
  const economicDuplicate = prior.some((entry): boolean => economicResultIdentityHash(entry.payload) === economicResultIdentityHash(raw.payload));
  requireLifecycle(!prior.some((entry): boolean => entry.payload.kind === raw.payload.kind
    && entry.payload.canonicalTransactionId === raw.payload.canonicalTransactionId
    && economicResultIdentityHash(entry.payload) !== economicResultIdentityHash(raw.payload)),
  "Canonical transaction carries conflicting amount or correlation; reconcile explicitly.");
  let projected = projectNativeFacts(request, state);
  requireNoUncorrelatedNativeFacts(projected, state, instruction.requestId);
  const transactions = verifiedNativeTransactions(projected);
  if (raw.payload.kind === "RETURNED") {
    const original = transactions.get(raw.payload.returnOfCanonicalTransactionId!);
    requireLifecycle(prior.some((entry): boolean => entry.payload.kind === "SUCCEEDED") && original?.kind === "REFUND"
      && original.settlement_at() !== null && compare_timestamps(original.settlement_at()!, raw.occurredAt) < 0,
    "A return needs accepted prior settlement strictly before its occurrence; ingest that proof first.");
    requireLifecycle(economicDuplicate || raw.payload.amountCents! <= remainingCanonicalPrincipal(transactions, original.key),
      "Return exceeds the verified remaining settled principal.");
  }
  const event = appendWorkflowEvent(state, ctx, instruction.requestId, raw.attemptId, raw.sourceEventId,
    { category: "SIMULATED_RESULT", kind: "RESULT_ACCEPTED", payload: { rawEventId: raw.eventId,
      instructionHash: raw.payload.instructionHash, canonicalTransactionId: raw.payload.canonicalTransactionId,
      returnOfCanonicalTransactionId: raw.payload.returnOfCanonicalTransactionId } }, raw.occurredAt);
  const proof = canonicalEvidenceInput(raw, event.learnedAt);
  const existingProof = projected.snapshot.evidence.find((entry): boolean => entry.evidenceId === proof.evidenceId);
  requireLifecycle(existingProof === undefined || canonical_json(existingProof) === canonical_json(proof), "Simulator proof identity conflicts with existing evidence.");
  if (existingProof === undefined) projected.snapshot.evidence.push(proof);
  if (!economicDuplicate) {
    const money = mapNativeMoneyEvent(instruction, raw, event.learnedAt, transactions);
    if (money !== null) {
      requireLifecycle(!projected.snapshot.moneyEvents.some((entry): boolean => entry.canonicalTransactionId === money.canonicalTransactionId
        || entry.sourceEventId === money.sourceEventId || entry.eventId === money.eventId),
      "An uncorrelated accounting record already claims this economic identity; reconcile explicitly.");
      projected.snapshot.moneyEvents.push(money);
    }
  }
  projected = projectNativeFacts(projected, state);
  // Reject economic/topology/proof conflicts, but do not require a currently final
  // case account: late settlement must remain visible after entitlement changes.
  verifiedNativeTransactions(projected);
  return { request: projected, workflow: state, summary: { requestId: instruction.requestId,
    acceptedEventId: event.eventId, economicDuplicate, moneyEffectAdded: !economicDuplicate
      && raw.payload.kind !== "FAILED" && instruction.kind !== "STATEMENT_DISPATCH" } };
}
