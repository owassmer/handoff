/** Pure append/reduce helpers. Raw observations are never accepted facts. */
import { ContractError } from "../domain/codec.js";
import { compare_timestamps, timestamp_microseconds } from "../domain/datetime.js";
import { fingerprint } from "../domain/fingerprints.js";
import type { ReviewRequest, RequestFact, StatementFact } from "../domain/types.js";
import { canonicalTransactionIdFor, workflowEventIdFor } from "./ids.js";
import { parseWorkflowTimestamp } from "./codec.js";
import type { CurrentRequest, OperationKind, PureContext, WorkflowEvent, WorkflowEventBase, WorkflowStateV2 } from "./types.js";

export function requireLifecycle(condition: boolean, message: string): asserts condition {
  if (!condition) throw new ContractError(message);
}

/** Allocated times advance strictly even when many commands share a demo clock. */
export function nextBusinessInstant(state: WorkflowStateV2): string {
  const latest = state.events.reduce((at, event): string =>
    compare_timestamps(event.learnedAt, at) > 0 ? event.learnedAt : at, state.businessClock);
  const milliseconds = timestamp_microseconds(latest) / 1000n + 1n;
  return new Date(Number(milliseconds)).toISOString();
}

type EventBody = WorkflowEvent extends infer E ? E extends WorkflowEvent ? Omit<E, keyof WorkflowEventBase> : never : never;

/** Mutates ONLY the caller's private clone; complete events precede codec validation. */
export function appendWorkflowEvent(
  state: WorkflowStateV2, ctx: PureContext, requestId: string, attemptId: string | null,
  sourceEventId: string | null, body: EventBody, explicitOccurrence: string | null = null,
): WorkflowEvent {
  const occurredAt = explicitOccurrence === null ? nextBusinessInstant(state) : parseWorkflowTimestamp(explicitOccurrence);
  const learnedAt = compare_timestamps(occurredAt, state.businessClock) > 0 ? occurredAt : state.businessClock;
  const identity = { kind: body.kind, requestId, attemptId, sourceEventId };
  const eventId = workflowEventIdFor(state, identity);
  requireLifecycle(!state.events.some((event): boolean => event.eventId === eventId), "Lifecycle event already exists; reconcile instead of overwriting it.");
  const event: WorkflowEvent = { ...body, eventId, sequence: state.events.length + 1,
    caseId: state.caseId, commandId: ctx.commandId, requestId, attemptId, sourceEventId,
    occurredAt, learnedAt, recordedAt: ctx.serverNow, recordedBy: ctx.actorId, mode: "SIMULATED" };
  state.events.push(event);
  state.businessClock = learnedAt;
  return event;
}

export function simulatorEvidenceId(rawEventId: string): string {
  return `dc-simulator-proof:${fingerprint({ rawEventId })}`;
}

export function nativeActionKind(kind: OperationKind): string {
  if (kind === "STATEMENT_DISPATCH") return "REQUEST_STATEMENT_DISPATCH";
  if (kind === "REFUND") return "REQUEST_REFUND";
  return "REQUEST_LEDGER_POSTING";
}

/** One current state per immutable instruction, in instruction order. No writes. */
export function projectRequests(state: WorkflowStateV2): CurrentRequest[] {
  const rawById = new Map(state.events.filter((event): boolean => event.kind === "RAW_SIMULATED_RESULT")
    .map((event): [string, WorkflowEvent] => [event.eventId, event]));
  return state.requests.map((instruction): CurrentRequest => {
    const events = state.events.filter((event): boolean => event.requestId === instruction.requestId);
    requireLifecycle(events.filter((event): boolean => event.kind === "REQUEST_CREATED").length === 1,
      "Every instruction requires exactly one REQUEST_CREATED event.");
    const current: CurrentRequest = { requestId: instruction.requestId, kind: instruction.kind, state: "READY",
      amountCents: instruction.intent.amountCents, reservedAmountCents: instruction.intent.amountCents ?? 0,
      attemptId: null, lastEventId: null, canonicalTransactionId: null, reconciliationRequired: false,
      reason: "Approved immutable instruction is ready; no attempt claimed." };
    events.forEach((event): void => {
      if (event.kind === "RAW_SIMULATED_RESULT") return;
      current.lastEventId = event.eventId;
      switch (event.kind) {
        case "REQUEST_CREATED":
          requireLifecycle(current.attemptId === null, "Request creation cannot follow an attempt.");
          break;
        case "ATTEMPT_CLAIMED":
          requireLifecycle(current.state === "READY", "Only a ready instruction can be claimed.");
          current.state = "CLAIMED"; current.attemptId = event.attemptId;
          current.reason = "An attempt is claimed and may already have been sent.";
          break;
        case "REQUESTED":
          requireLifecycle(current.state === "CLAIMED" && current.attemptId === event.attemptId, "Send requires the current claimed attempt.");
          current.state = "REQUESTED"; current.reason = "Simulated operation requested; no accepted result.";
          break;
        case "ACKNOWLEDGED":
          requireLifecycle(["REQUESTED", "OUTCOME_UNKNOWN"].includes(current.state), "Acknowledgement requires an outstanding attempt.");
          current.state = "ACKNOWLEDGED"; current.reason = "Acknowledgement is not settlement proof.";
          break;
        case "OUTCOME_UNKNOWN":
          requireLifecycle(["CLAIMED", "REQUESTED", "ACKNOWLEDGED"].includes(current.state), "Only an outstanding attempt can have an unknown outcome.");
          current.state = "OUTCOME_UNKNOWN"; current.reason = event.payload.reason;
          break;
        case "CANCELLED_BEFORE_ATTEMPT":
        case "SUPERSEDED_BEFORE_ATTEMPT":
          requireLifecycle(current.state === "READY" && current.attemptId === null, "An attempted instruction cannot be cancelled or superseded.");
          current.state = event.kind === "CANCELLED_BEFORE_ATTEMPT" ? "CANCELLED" : "SUPERSEDED";
          current.reason = event.payload.reason;
          break;
        case "RESULT_ACCEPTED": {
          const raw = rawById.get(event.payload.rawEventId);
          requireLifecycle(raw?.kind === "RAW_SIMULATED_RESULT" && raw.sequence < event.sequence,
            "Acceptance needs an earlier raw observation.");
          requireLifecycle(raw.requestId === instruction.requestId && raw.attemptId === current.attemptId
            && raw.payload.instructionHash === instruction.instructionHash && raw.payload.operationKind === instruction.kind
            && raw.payload.recipientVersionId === instruction.intent.recipientVersionId && raw.payload.currency === "USD",
          "Accepted result does not match the immutable instruction and actual attempt.");
          requireLifecycle(raw.payload.kind === "RETURNED" ? instruction.kind === "REFUND"
            && raw.payload.amountCents !== null && raw.payload.amountCents > 0
            && raw.payload.amountCents <= instruction.intent.amountCents!
            && raw.payload.returnOfCanonicalTransactionId === current.canonicalTransactionId
            : raw.payload.amountCents === instruction.intent.amountCents,
          "Accepted amount or original transaction differs from the instruction.");
          if (raw.payload.kind === "SUCCEEDED" && instruction.kind !== "STATEMENT_DISPATCH") {
            requireLifecycle(raw.payload.canonicalTransactionId === canonicalTransactionIdFor(state, instruction.requestId),
              "Accepted settlement must use the request's scoped canonical payment identity.");
          }
          if (raw.payload.kind === "RETURNED") {
            requireLifecycle(current.state === "SUCCEEDED", "A return needs an accepted prior settlement.");
            // A returned payment remains a historically successful request. Native
            // REFUND_RETURNED, not a false FAILED request, reopens the liability.
            current.reason = "Historical success; verified return reopens unpaid liability.";
          } else {
            const targetState = raw.payload.kind;
            requireLifecycle(!["CANCELLED", "SUPERSEDED"].includes(current.state)
              && (!(current.state === "SUCCEEDED" || current.state === "FAILED") || current.state === targetState),
            "Accepted outcomes cannot contradict a terminal result.");
            requireLifecycle(current.attemptId !== null, "An accepted result requires a claimed attempt.");
            current.state = targetState;
            current.canonicalTransactionId = raw.payload.canonicalTransactionId;
            current.reason = targetState === "SUCCEEDED" ? "Accepted simulator proof confirms historical success." : "Accepted simulator proof confirms definitive failure.";
          }
          break;
        }
      }
    });
    const acceptedRawIds = new Set(events.filter((event): boolean => event.kind === "RESULT_ACCEPTED")
      .map((event): string => event.kind === "RESULT_ACCEPTED" ? event.payload.rawEventId : ""));
    const conflictingObservation = events.some((event): boolean => event.kind === "RAW_SIMULATED_RESULT"
      && !acceptedRawIds.has(event.eventId)
      && ((current.state === "SUCCEEDED" && event.payload.kind === "FAILED")
        || (current.state === "FAILED" && event.payload.kind !== "FAILED")));
    current.reconciliationRequired = conflictingObservation || current.state === "OUTCOME_UNKNOWN";
    if (conflictingObservation) current.reason = "Contradictory unaccepted observation requires explicit reconciliation.";
    current.reservedAmountCents = ["READY", "CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN"].includes(current.state)
      ? instruction.intent.amountCents ?? 0 : 0;
    return current;
  });
}

/** Replaces only sidecar-owned request facts, preserving native/external facts and proof. */
export function projectNativeFacts(request: ReviewRequest, state: WorkflowStateV2): ReviewRequest {
  const result = structuredClone(request);
  const currents = new Map(projectRequests(state).map((current): [string, CurrentRequest] => [current.requestId, current]));
  const facts = state.requests.map((instruction): RequestFact => {
    const current = currents.get(instruction.requestId)!;
    return { requestId: instruction.requestId, actionKind: nativeActionKind(instruction.kind),
      targetVersionId: instruction.intent.targetVersionId, payloadFingerprint: instruction.instructionHash,
      amountCents: instruction.intent.amountCents, state: current.state,
      approvalIds: [...instruction.approvalIds], externalReference: current.canonicalTransactionId };
  });
  result.snapshot.priorRequests = [...result.snapshot.priorRequests.filter((fact): boolean => !currents.has(fact.requestId)), ...facts];
  const acceptedRawIds = new Set(state.events.flatMap((event): string[] => event.kind === "RESULT_ACCEPTED" ? [event.payload.rawEventId] : []));
  const statements = state.statements.map((statement): StatementFact => {
    const successes = state.events.filter((event): boolean => event.kind === "RAW_SIMULATED_RESULT"
      && acceptedRawIds.has(event.eventId) && event.payload.kind === "SUCCEEDED"
      && state.requests.some((instruction): boolean => instruction.requestId === event.requestId
        && instruction.kind === "STATEMENT_DISPATCH" && instruction.intent.statementId === statement.statementId)
      && result.snapshot.evidence.some((proof): boolean => proof.evidenceId === simulatorEvidenceId(event.eventId)
        && proof.recordKind === "SOURCE_EVENT" && proof.sourceClass === "TEST_ASSUMPTION" && proof.associationAccepted))
      .sort((left, right): number => compare_timestamps(left.occurredAt, right.occurredAt));
    return { versionId: statement.statementId, kind: statement.kind === "CORRECTIVE" ? "CORRECTION" : statement.kind,
      reviewId: statement.sourceReviewId, contentHash: statement.contentHash,
      recipientInstructionsVersion: statement.recipientVersionId, issuedAt: successes[0]?.occurredAt ?? null,
      issuanceEvidenceIds: successes.map((event): string => simulatorEvidenceId(event.eventId)) };
  });
  const statementIds = new Set(state.statements.map((statement): string => statement.statementId));
  result.snapshot.priorStatements = [...result.snapshot.priorStatements.filter((fact): boolean => !statementIds.has(fact.versionId)), ...statements];
  result.reviewClock = state.businessClock;
  return result;
}
