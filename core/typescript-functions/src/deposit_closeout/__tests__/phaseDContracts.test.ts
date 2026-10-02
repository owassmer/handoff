import { describe, expect, it } from "vitest";
import { canonical_json, ContractError } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import {
  assertMonotonicBusinessClock, centsToLong, checkedMoneyLong, hashWorkflowReview, hashWorkflowState,
  parseLifecycleCommand, parsePureContext, parseWorkflowReview, parseWorkflowSnapshot, parseWorkflowState,
  parseWorkflowTimestamp, parseWorkflowVersion, serializeWorkflowReview, serializeWorkflowState,
  validateWorkflowCaseReferences,
} from "../lifecycle/codec.js";
import {
  approvalIdFor, attemptIdFor, canonicalTransactionIdFor, economicResultIdentityHash, instructionHashFor, instructionKeyFor,
  recipientVersionIdFor, requestIdFor, resultIdentityHash, returnTransactionIdFor, statementContentHash, statementIdFor,
  targetVersionIdFor, workflowEventIdFor,
} from "../lifecycle/ids.js";
import {
  MAX_WORKFLOW_JSON_BYTES, MAX_WORKFLOW_RECORDS, SYNTHETIC_STATEMENT_BADGE,
  WORKFLOW_COMPANY_ID, WORKFLOW_ENVIRONMENT_ID,
} from "../lifecycle/types.js";
import type * as T from "../lifecycle/types.js";
import { asRecord, atPointer, baseRequest, requireElement, resultFor } from "./fixtures/helpers.js";

const SCOPE: T.WorkflowScope = {
  caseId: "demo-phase-d-case", managementCompanyId: WORKFLOW_COMPANY_ID, environmentId: WORKFLOW_ENVIRONMENT_ID,
};
const ACTOR = "c47a52a0-0048-4607-931f-f4df283ae7c4";
const INITIALIZED_AT = "2026-09-18T10:00:00Z";
const RECORDED_AT = "2026-09-18T10:01:00Z";
const SNAPSHOT_AT = "2026-09-18T10:02:00Z";
const BUSINESS_CLOCK = "2026-09-05T12:00:00Z";
const MATERIALITY = fingerprint({ stableEntitlementCents: 200000, decision: "accepted" });

function route(): T.OperationInstructions {
  return { versionId: "demo-recipients-v1", partyIds: ["demo-resident"], state: "VERIFIED",
    method: "DEMO_OUTBOX", routeReference: "demo-route-no-real-destination", evidenceIds: ["ev-recipients"] };
}
function emptyState(): T.WorkflowStateV2 {
  return { ...SCOPE, schemaVersion: "2.0.0", mode: "SIMULATED", initializedBy: ACTOR,
    initializedAt: INITIALIZED_AT, businessClock: BUSINESS_CLOCK, statementInstructions: route(), refundInstructions: route(),
    statements: [], approvals: [], requests: [], events: [], currentStatementId: null };
}
function financialIntent(patch: Partial<T.FinancialIntent> = {}): T.FinancialIntent {
  const result: T.FinancialIntent = { kind: "REFUND", amountCents: 15000, currency: "USD", dispositionKey: "refund-installment-1",
    statementId: null, recipientVersionId: "demo-recipients-v1", materialityHash: MATERIALITY,
    targetVersionId: "placeholder", replacesRequestId: null, reversesTransactionId: null, ...patch };
  result.targetVersionId = targetVersionIdFor(SCOPE, result);
  return result;
}
function approvalFor(intent: T.OperationIntent, commandId: string = "approve-1"): T.ApprovalRecord {
  return { ...SCOPE, approvalId: approvalIdFor(SCOPE, commandId, ACTOR), createdCommandId: commandId,
    actorId: ACTOR, actorPartyId: "demo-manager", authorityVersion: "authority-v1", scope: intent.kind,
    intent, decision: "APPROVED", decidedAt: RECORDED_AT, revokesApprovalId: null };
}
function requestFor(intent: T.OperationIntent, approvalId: string): T.RequestInstruction {
  const instructions = intent.kind === "REFUND" || intent.kind === "STATEMENT_DISPATCH" ? route() : null;
  return { ...SCOPE, requestId: requestIdFor(SCOPE, intent), instructionKey: instructionKeyFor(SCOPE, intent),
    createdCommandId: "request-1", kind: intent.kind, intent, instructions,
    instructionHash: instructionHashFor(SCOPE, intent, instructions), approvalIds: [approvalId],
    createdBy: ACTOR, createdAt: RECORDED_AT, businessCreatedAt: BUSINESS_CLOCK,
    replacesRequestId: intent.replacesRequestId, reversesTransactionId: intent.reversesTransactionId };
}
function baseEvent(requestId: string, attemptId: string | null = null, sourceEventId: string | null = null): T.WorkflowEventBase {
  return { eventId: "placeholder", sequence: 1, caseId: SCOPE.caseId, commandId: "record-event", requestId,
    attemptId, sourceEventId, occurredAt: BUSINESS_CLOCK, learnedAt: BUSINESS_CLOCK,
    recordedAt: RECORDED_AT, recordedBy: ACTOR, mode: "SIMULATED" };
}
function appendEvent(state: T.WorkflowStateV2, event: T.WorkflowEvent): void {
  state.events.push({ ...event, sequence: state.events.length + 1, eventId: workflowEventIdFor(state, event) });
}
function statementRecord(): T.StatementVersionRecord {
  const native = resultFor(baseRequest());
  const content: T.StatementContent = {
    mode: "SIMULATED", syntheticBadge: SYNTHETIC_STATEMENT_BADGE, title: "Synthetic interim statement",
    parties: [{ partyId: "demo-resident", displayLabel: "Constructed resident" }],
    dates: [{ factKey: "VACANCY", state: "ACCEPTED", value: "2026-09-02" }],
    items: native.result.itemDecisions.map((decision): T.StatementLine => ({ itemId: decision.itemId,
      location: "Synthetic home", description: "Constructed item", decision })),
    account: native.result.account, sourceReferences: requireElement(native.result.itemDecisions, 0).sourceReferences,
  };
  const renderedText = `${SYNTHETIC_STATEMENT_BADGE}\nSynthetic statement; no legal performance.`;
  const record: T.StatementVersionRecord = { ...SCOPE, statementId: "placeholder", kind: "INTERIM",
    createdCommandId: "prepare-1", createdBy: ACTOR, createdAt: RECORDED_AT, businessCreatedAt: BUSINESS_CLOCK,
    sourceReviewId: "native-review-1", materialityHash: MATERIALITY, contentHash: statementContentHash(content, renderedText),
    recipientVersionId: route().versionId, content, renderedText, supersedesStatementId: null };
  record.statementId = statementIdFor(SCOPE, record);
  return record;
}
function fullState(): T.WorkflowStateV2 {
  const state = emptyState();
  const statement = statementRecord();
  state.statements = [statement];
  state.currentStatementId = statement.statementId;
  const intent = financialIntent({ statementId: statement.statementId });
  const approval = approvalFor(intent);
  const request = requestFor(intent, approval.approvalId);
  state.approvals = [approval];
  state.requests = [request];
  appendEvent(state, { ...baseEvent(request.requestId), category: "REQUEST_LIFECYCLE", kind: "REQUEST_CREATED",
    payload: { instructionHash: request.instructionHash } });
  const attemptId = attemptIdFor(state, request.requestId, 1);
  (["ATTEMPT_CLAIMED", "REQUESTED", "ACKNOWLEDGED"] as const).forEach((kind): void => {
    appendEvent(state, { ...baseEvent(request.requestId, attemptId), category: "REQUEST_LIFECYCLE", kind,
      payload: { instructionHash: request.instructionHash } });
  });
  appendEvent(state, { ...baseEvent(request.requestId, attemptId), category: "REQUEST_LIFECYCLE", kind: "OUTCOME_UNKNOWN",
    payload: { reason: "Synthetic transport status unavailable" } });
  const raw: T.RawSimulatedResult = { requestId: request.requestId, attemptId, sourceEventId: "source-1", kind: "SUCCEEDED",
    operationKind: request.kind, instructionHash: request.instructionHash, amountCents: intent.amountCents, currency: "USD",
    recipientVersionId: intent.recipientVersionId, canonicalTransactionId: canonicalTransactionIdFor(state, request.requestId),
    returnOfCanonicalTransactionId: null };
  appendEvent(state, { ...baseEvent(request.requestId, attemptId, raw.sourceEventId), category: "SIMULATED_RESULT",
    kind: "RAW_SIMULATED_RESULT", payload: raw });
  const rawEvent = requireElement(state.events, state.events.length - 1);
  appendEvent(state, { ...baseEvent(request.requestId, attemptId, raw.sourceEventId), category: "SIMULATED_RESULT",
    kind: "RESULT_ACCEPTED", payload: { rawEventId: rawEvent.eventId, instructionHash: raw.instructionHash,
      canonicalTransactionId: raw.canonicalTransactionId, returnOfCanonicalTransactionId: null } });
  return state;
}
function workflowReview(state: T.WorkflowStateV2): T.WorkflowReviewV2 {
  const native = resultFor(baseRequest());
  const instruction = state.requests[0];
  const approval = state.approvals[0];
  const details: T.WorkflowActionDetails = { operationKind: "REFUND", intent: instruction?.intent ?? null,
    approvalDetails: approval === undefined ? [] : [{ approvalId: approval.approvalId, valid: true, reason: "Synthetic authority" }],
    requestDetails: instruction === undefined ? [] : [{ requestId: instruction.requestId, kind: instruction.kind,
      state: "SUCCEEDED", amountCents: instruction.intent.amountCents, reservedAmountCents: 0,
      attemptId: attemptIdFor(state, instruction.requestId, 1), lastEventId: state.events.at(-1)?.eventId ?? null,
      canonicalTransactionId: canonicalTransactionIdFor(state, instruction.requestId), reconciliationRequired: false, reason: "Simulated result accepted" }],
    statementDetails: state.statements.map((statement): T.StatementStatus => ({ statementId: statement.statementId,
      isCurrent: statement.statementId === state.currentStatementId, dispatchRequestIds: [], issued: false })),
  };
  return { metadata: { ...native.metadata, reviewClock: state.businessClock, workflowSchemaVersion: "2.0.0",
    workflowStateHash: hashWorkflowState(state), authorityEvaluatedAt: SNAPSHOT_AT }, result: { ...native.result,
    account: { ...native.result.account, financialCommitments: [{ kind: "REFUND", reservedCents: 0, requestIds: [] }], newlyRequestableRefundCents: null },
    actions: native.result.actions.map((action, index): T.WorkflowAction => ({ ...action, workflow: index === 0 ? details : null })),
    outcomes: { ...native.result.outcomes, depositComplete: false, overallCaseComplete: false,
      simulatedDepositWorkflowComplete: false, simulatedOverallWorkflowComplete: false,
      completionMode: "SIMULATED", legalPerformanceConfirmed: false } } };
}
function mutate(source: unknown, pointer: string, value: unknown): string {
  const raw: unknown = structuredClone(source);
  const parts = pointer.split("/");
  const key = parts.pop();
  if (key === undefined) throw new Error("Expected test pointer");
  const parent = parts.length === 0 ? raw : atPointer(raw, `/${parts.join("/")}`);
  if (Array.isArray(parent)) parent[Number(key)] = value;
  else asRecord(parent)[key] = value;
  return JSON.stringify(raw);
}

const COMMANDS: T.LifecycleCommand[] = [
  { kind: "INIT_WORKFLOW", payload: {} },
  { kind: "ACCEPT_SCOPE_FACTS", payload: { jurisdiction: "NC", tenancyRegime: "RESIDENTIAL", tenancyEndsInFull: true,
    cashSecurityDeposit: true, evidenceIds: ["ev-agreement"], reason: "Constructed scope accepted" } },
  { kind: "SET_INTERIM_QUALIFICATION", payload: { state: "ACCEPTED", evidenceIds: ["ev-agreement"], reason: "Constructed qualification" } },
  { kind: "UPSERT_RECIPIENT_PARTY", payload: { party: { partyId: "resident-2", displayLabel: "Constructed signatory",
    roles: ["SIGNATORY"], effectiveFrom: null, effectiveUntil: null, principalId: null, evidenceIds: ["ev-recipients"] } } },
  { kind: "SET_STATEMENT_INSTRUCTIONS", payload: { partyIds: ["demo-resident"], state: "UNCONFIRMED", method: null, routeReference: null, evidenceIds: [] } },
  { kind: "SET_REFUND_INSTRUCTIONS", payload: { partyIds: ["demo-resident"], state: "VERIFIED", method: "DEMO_OUTBOX",
    routeReference: "demo-no-real-route", evidenceIds: ["ev-recipients"] } },
  { kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "Prepare simulated statement" } },
  { kind: "DECIDE_APPROVAL", payload: { intent: { kind: "REFUND", amountCents: 15000, dispositionKey: "installment-1",
    statementId: null, replacesRequestId: null, reversesTransactionId: null }, decision: "APPROVED" } },
  { kind: "REVOKE_APPROVAL", payload: { approvalId: "approval-1", reason: "Withdraw simulated approval" } },
  { kind: "REQUEST_OPERATION", payload: { approvalId: "approval-1" } },
  { kind: "CLAIM_REQUEST", payload: { requestId: "request-1" } },
  { kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: "request-1", attemptId: "attempt-1", reason: "Unknown transport" } },
  { kind: "GENERATE_SIMULATED_RESULT", payload: { requestId: "request-1", attemptId: "attempt-1", sourceEventId: "source-1",
    outcome: "SUCCEEDED", amountCents: 15000, occurredAt: null } },
  { kind: "INGEST_RESULT", payload: { sourceEventId: "source-1" } },
  { kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId: "request-1", reason: "Cancel unattempted instruction" } },
];

describe("Phase D frozen command codecs", (): void => {
  it.each(COMMANDS)("round-trips $kind and rejects unknown fields", (command): void => {
    expect(parseLifecycleCommand(command.kind, canonical_json(command.payload))).toEqual(command);
    expect((): unknown => parseLifecycleCommand(command.kind, JSON.stringify({ ...command.payload, actorId: ACTOR }))).toThrow(ContractError);
    Object.keys(command.payload).forEach((key): void => {
      const omitted = { ...command.payload };
      Reflect.deleteProperty(omitted, key);
      expect((): unknown => parseLifecycleCommand(command.kind, JSON.stringify(omitted))).toThrow(ContractError);
    });
  });
  it("rejects unsupported/arbitrary dispatch, duplicate keys and escaped aliases", (): void => {
    expect((): unknown => parseLifecycleCommand("PATCH", "{}")).toThrow(ContractError);
    expect((): unknown => parseLifecycleCommand("INIT_WORKFLOW", '{"x":1,"x":2}')).toThrow(/duplicate/);
    expect((): unknown => parseLifecycleCommand("REQUEST_OPERATION", '{"approvalId":"a","\\u0061pprovalId":"b"}')).toThrow(/duplicate/);
  });
  it.each(["9007199254740992", "1.0", "1e3", "-1", '"1"', "true", "0"])("rejects unsafe money token %s", (token): void => {
    const payload = JSON.stringify(requireElement(COMMANDS, 12).payload).replace('"amountCents":15000', `"amountCents":${token}`);
    expect((): unknown => parseLifecycleCommand("GENERATE_SIMULATED_RESULT", payload)).toThrow(ContractError);
  });
  it("keeps required null distinct from zero, omission and false", (): void => {
    const command = requireElement(COMMANDS, 12);
    expect(parseLifecycleCommand(command.kind, mutate(command.payload, "amountCents", null)).payload).toHaveProperty("amountCents", null);
    expect((): unknown => parseLifecycleCommand(command.kind, mutate(command.payload, "occurredAt", false))).toThrow(ContractError);
    expect((): unknown => parseLifecycleCommand(command.kind, mutate(command.payload, "amountCents", 0))).toThrow(ContractError);
  });
  it("requires positive linked reversals, not negative generic movements", (): void => {
    const payload: T.DecideApprovalPayload = { decision: "APPROVED", intent: { kind: "CHARGE_POSTING_REVERSAL", amountCents: 20,
      dispositionKey: "reverse-posting-1", statementId: null, replacesRequestId: null, reversesTransactionId: "original-txn" } };
    expect(parseLifecycleCommand("DECIDE_APPROVAL", JSON.stringify(payload))).toHaveProperty("payload.intent.amountCents", 20);
    expect((): unknown => parseLifecycleCommand("DECIDE_APPROVAL", mutate(payload, "intent/reversesTransactionId", null))).toThrow(ContractError);
    expect((): unknown => parseLifecycleCommand("DECIDE_APPROVAL", mutate(payload, "intent/amountCents", -20))).toThrow(ContractError);
    expect((): unknown => parseLifecycleCommand("DECIDE_APPROVAL", mutate(payload, "intent/kind", "REFUND"))).toThrow(ContractError);
    expect((): unknown => parseLifecycleCommand("DECIDE_APPROVAL", mutate(payload, "decision", "REVOKED"))).toThrow(ContractError);
  });
  it("does not allow clients to supply authority, intent hashes, versions, or approvals", (): void => {
    const command = requireElement(COMMANDS, 7);
    expect((): unknown => parseLifecycleCommand(command.kind, mutate(command.payload, "intent/targetVersionId", "forged"))).toThrow(ContractError);
    const routeCommand = requireElement(COMMANDS, 5);
    expect((): unknown => parseLifecycleCommand(routeCommand.kind, JSON.stringify({ ...routeCommand.payload, versionId: "forged" }))).toThrow(ContractError);
    const partyCommand = requireElement(COMMANDS, 3);
    expect((): unknown => parseLifecycleCommand(partyCommand.kind, mutate(partyCommand.payload, "party/principalId", ACTOR))).toThrow(ContractError);
    expect((): unknown => parseLifecycleCommand(partyCommand.kind, mutate(partyCommand.payload, "party/roles", ["MANAGER"]))).toThrow(ContractError);
  });
  it.each(["https://example.test", "resident@example.test", "123 Main Street", "bank-account-123"])("rejects real/non-demo route %s", (routeReference): void => {
    const command = requireElement(COMMANDS, 5);
    expect((): unknown => parseLifecycleCommand(command.kind, mutate(command.payload, "routeReference", routeReference))).toThrow(ContractError);
  });
  it("rejects incomplete verified instructions and duplicate party/evidence identifiers", (): void => {
    const command = requireElement(COMMANDS, 5);
    ["partyIds", "evidenceIds"].forEach((key): void => {
      expect((): unknown => parseLifecycleCommand(command.kind, mutate(command.payload, key, []))).toThrow(ContractError);
      expect((): unknown => parseLifecycleCommand(command.kind, mutate(command.payload, key, ["same", "same"]))).toThrow(ContractError);
    });
    expect((): unknown => parseLifecycleCommand(command.kind, mutate(command.payload, "method", "EMAIL"))).toThrow(ContractError);
    expect((): unknown => parseLifecycleCommand(command.kind, mutate(command.payload, "routeReference", null))).toThrow(ContractError);
  });
});

describe("Phase D exact timestamps, Longs, bounds and versions", (): void => {
  it("normalizes exact UTC instants and separates trusted actual context from business clock", (): void => {
    expect(parseWorkflowTimestamp("2026-09-18T10:00:00.000Z")).toBe(INITIALIZED_AT);
    expect(parseWorkflowTimestamp("2026-09-18T10:00:00.000001Z")).toBe("2026-09-18T10:00:00.000001Z");
    expect(parsePureContext({ actorId: ACTOR, serverNow: INITIALIZED_AT, isAdministrator: false,
      commandId: "command-1", basisReviewId: "review-1" }).serverNow).toBe(INITIALIZED_AT);
    expect(parseWorkflowState(JSON.stringify(emptyState())).businessClock).toBe(BUSINESS_CLOCK);
    expect(assertMonotonicBusinessClock(INITIALIZED_AT, "2026-09-18T10:00:00.000001Z")).toContain(".000001Z");
    expect((): unknown => assertMonotonicBusinessClock(INITIALIZED_AT, BUSINESS_CLOCK)).toThrow(ContractError);
  });
  it.each(["2026-02-29T00:00:00Z", "2026-09-18T10:00:00+00:00", "2026-09-18", "2026-09-18T10:00:00.0000001Z",
    "20260918T100000Z", "2026-09-18T24:00:00Z", "2026-09-18T10:00:00"])("rejects nonexact/invalid UTC %s", (value): void => {
    expect((): unknown => parseWorkflowTimestamp(value)).toThrow(ContractError);
  });
  it("converts exact Long money strings without lossy coercion", (): void => {
    expect(checkedMoneyLong("9007199254740991")).toBe(Number.MAX_SAFE_INTEGER);
    expect(centsToLong(Number.MAX_SAFE_INTEGER)).toBe("9007199254740991");
    expect(checkedMoneyLong("0")).toBe(0);
    ["9007199254740992", "9223372036854775807", "01", "+1", "1.0", "1e3", "-1", "-0", 1, null, true, undefined].forEach((value): void => {
      expect((): unknown => checkedMoneyLong(value)).toThrow(ContractError);
    });
    [1.5, -1, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1].forEach((value): void => {
      expect((): unknown => centsToLong(value)).toThrow(ContractError);
    });
  });
  it("accepts only absent/0 legacy or explicit Long 2", (): void => {
    expect(parseWorkflowVersion(undefined)).toBe(0);
    expect(parseWorkflowVersion("0")).toBe(0);
    expect(parseWorkflowVersion("2")).toBe(2);
    [null, 0, 2, "1", "02", "3", "", false].forEach((value): void => {
      expect((): unknown => parseWorkflowVersion(value)).toThrow(ContractError);
    });
    ["1.0.0", "2", "2.0.1", null].forEach((value): void => {
      expect((): unknown => parseWorkflowState(mutate(emptyState(), "schemaVersion", value))).toThrow(ContractError);
    });
  });
  it("enforces byte and array bounds and never truncates", (): void => {
    expect((): unknown => parseWorkflowState(" ".repeat(MAX_WORKFLOW_JSON_BYTES))).toThrow(/256 KiB/);
    expect((): unknown => parseLifecycleCommand("INIT_WORKFLOW", " ".repeat(MAX_WORKFLOW_JSON_BYTES))).toThrow(/256 KiB/);
    expect((): unknown => parseWorkflowState(mutate(emptyState(), "events", Array.from({ length: MAX_WORKFLOW_RECORDS + 1 }, (): null => null)))).toThrow(/bounded array/);
    expect((): unknown => parseWorkflowState(mutate(emptyState(), "initializedBy", "\ud800"))).toThrow(ContractError);
    expect((): unknown => parseLifecycleCommand("INIT_WORKFLOW", '{"__proto__":{}}')).toThrow(ContractError);
  });
});

describe("Phase D nested state integrity", (): void => {
  it("round-trips complete immutable history with canonical hashes", (): void => {
    const state = fullState();
    expect(parseWorkflowState(serializeWorkflowState(state))).toEqual(state);
    expect(hashWorkflowState(state)).toBe(fingerprint(state));
    expect(parseWorkflowState(JSON.stringify(emptyState()))).toEqual(emptyState());
    expect(hashWorkflowState({ ...emptyState(), initializedAt: "2026-09-18T10:00:00.000Z" })).toBe(hashWorkflowState(emptyState()));
  });
  it.each([
    ["currentStatementId", "missing"], ["environmentId", "OTHER"], ["managementCompanyId", "other-company"],
    ["mode", "LIVE"], ["statements/0/caseId", "other-case"], ["statements/0/content/items/0/decision/vendorCostCents", "25000"],
    ["statements/0/content/parties/0/address", "invented"], ["statements/0/content/syntheticBadge", "REAL"],
    ["statements/0/content/items/0/itemId", "wrong-item"], ["statements/0/content/account/finalRefundCents", false],
    ["statements/0/content/dates/0/value", "2026-02-30"], ["statements/0/renderedText", "tampered text"],
    ["statements/0/contentHash", "a".repeat(64)], ["statements/0/statementId", "wrong-statement-id"],
    ["approvals/0/scope", "CHARGE_POSTING"], ["approvals/0/intent/targetVersionId", "wrong-target"],
    ["approvals/0/revokesApprovalId", "missing"], ["approvals/0/decision", "HUMAN_APPROVED"],
    ["requests/0/instructionHash", "a".repeat(64)], ["requests/0/approvalIds", ["missing"]],
    ["requests/0/kind", "STATEMENT_DISPATCH"], ["requests/0/instructions", null],
    ["events/1/sequence", 12], ["events/2/attemptId", "missing"], ["events/5/category", "COMMAND_RECEIPT"],
    ["events/5/payload/requestId", "wrong-request"], ["events/5/payload/amountCents", -1],
    ["events/5/payload/returnOfCanonicalTransactionId", "wrong-return"],
    ["events/6/payload/rawEventId", "missing"], ["events/6/payload/canonicalTransactionId", "wrong-transaction"],
    ["events/6/occurredAt", "2027-01-01T00:00:00Z"], ["events/6/recordedAt", "2020-01-01T00:00:00Z"],
  ] as [string, unknown][])("rejects nested corruption at %s", (pointer, value): void => {
    expect((): unknown => parseWorkflowState(mutate(fullState(), pointer, value))).toThrow(ContractError);
  });
  it("requires every nested field and rejects arbitrary fields at each record boundary", (): void => {
    const state = fullState();
    const pointers = ["", "statementInstructions", "statements/0", "statements/0/content", "statements/0/content/items/0",
      "statements/0/content/dates/0", "statements/0/content/parties/0", "approvals/0", "approvals/0/intent",
      "requests/0", "requests/0/instructions", "events/0", "events/0/payload", "events/5/payload", "events/6/payload"];
    pointers.forEach((pointer): void => {
      const record = pointer === "" ? state : atPointer(state, `/${pointer}`);
      expect((): unknown => parseWorkflowState(mutate(state, pointer === "" ? "unexpected" : `${pointer}/unexpected`, true))).toThrow(ContractError);
      Object.keys(asRecord(record)).forEach((key): void => {
        const raw: unknown = structuredClone(state);
        const target = pointer === "" ? raw : atPointer(raw, `/${pointer}`);
        Reflect.deleteProperty(asRecord(target), key);
        expect((): unknown => parseWorkflowState(JSON.stringify(raw))).toThrow(ContractError);
      });
    });
  });
  it("rejects duplicate identities, mutable request states, missing creation and orphan acceptance", (): void => {
    const state = fullState();
    (["statements", "approvals", "requests", "events"] as const).forEach((key): void => {
      expect((): unknown => parseWorkflowState(mutate(state, key, [...state[key], state[key][0]]))).toThrow(/duplicate/i);
    });
    expect((): unknown => parseWorkflowState(mutate(state, "currentRequests", []))).toThrow(ContractError);
    expect((): unknown => parseWorkflowState(mutate(state, "requests/0/state", "SUCCEEDED"))).toThrow(ContractError);
    expect((): unknown => parseWorkflowState(mutate(state, "events", []))).toThrow(/creation/);
    const noRaw = structuredClone(state);
    noRaw.events.splice(5, 1);
    noRaw.events.forEach((event, index): void => { event.sequence = index + 1; });
    expect((): unknown => parseWorkflowState(JSON.stringify(noRaw))).toThrow(/raw result/);
  });
  it("permits unaccepted raw results without inventing performed RequestFact state", (): void => {
    const state = fullState();
    state.events.pop();
    const parsed = parseWorkflowState(JSON.stringify(state));
    expect(parsed.events.at(-1)?.kind).toBe("RAW_SIMULATED_RESULT");
    expect(parsed.requests[0]).not.toHaveProperty("state");
    // Raw mismatches are data for reconciliation, not automatically accepted performance.
    expect((): unknown => parseWorkflowState(mutate(state, "events/5/payload/amountCents", 19999))).not.toThrow();
  });
  it("validates separate actual/business ordering without imposing wall-clock time", (): void => {
    const state = fullState();
    state.businessClock = "2099-01-01T00:00:00Z";
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
    expect((): unknown => parseWorkflowState(mutate(state, "events/5/learnedAt", "2026-09-05T11:00:00Z"))).toThrow(ContractError);
    expect((): unknown => parseWorkflowState(mutate(state, "businessClock", "2020-01-01T00:00:00Z"))).toThrow(ContractError);
  });
  it("binds party/evidence references to the existing native case, not the caller", (): void => {
    const state = fullState();
    const snapshot = { ...baseRequest().snapshot, caseId: state.caseId, managementCompanyId: state.managementCompanyId };
    expect((): void => validateWorkflowCaseReferences(state, snapshot)).not.toThrow();
    expect((): void => validateWorkflowCaseReferences(state, { ...snapshot, caseId: "another-case" })).toThrow(ContractError);
    state.refundInstructions.partyIds = ["outsider"];
    expect((): void => validateWorkflowCaseReferences(state, snapshot)).toThrow(/parties/);
  });
  it("supports positive explicit posting/application reversals without requiring a current request fact", (): void => {
    (["CHARGE_POSTING", "DEPOSIT_APPLICATION", "CHARGE_POSTING_REVERSAL", "DEPOSIT_APPLICATION_REVERSAL"] as const).forEach((kind): void => {
      const state = emptyState();
      const intent = financialIntent({ kind, recipientVersionId: null,
        reversesTransactionId: kind.endsWith("_REVERSAL") ? "native-original-transaction" : null });
      const approval = approvalFor(intent);
      const request = requestFor(intent, approval.approvalId);
      state.approvals.push(approval);
      state.requests.push(request);
      appendEvent(state, { ...baseEvent(request.requestId), category: "REQUEST_LIFECYCLE", kind: "REQUEST_CREATED", payload: { instructionHash: request.instructionHash } });
      expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
    });
  });
  it("preserves route version immutability within a channel but keeps channels separate", (): void => {
    const state = fullState();
    state.statementInstructions.routeReference = "demo-other-statement-route";
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
    state.refundInstructions.routeReference = "demo-other-refund-route";
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).toThrow(/version reused/);
    state.refundInstructions.versionId = "new-refund-version";
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
  });
  it("accepts distinct cancellation and supersession payloads with replacement references", (): void => {
    const state = fullState();
    state.events = state.events.slice(0, 1);
    const original = requireElement(state.requests, 0);
    appendEvent(state, { ...baseEvent(original.requestId), category: "REQUEST_LIFECYCLE", kind: "CANCELLED_BEFORE_ATTEMPT",
      payload: { reason: "Cancel before dispatch" } });
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
    state.events.pop();
    const intent = financialIntent({ replacesRequestId: original.requestId });
    const approval = approvalFor(intent, "replacement-approval");
    const replacement = requestFor(intent, approval.approvalId);
    state.approvals.push(approval);
    state.requests.push(replacement);
    appendEvent(state, { ...baseEvent(replacement.requestId), category: "REQUEST_LIFECYCLE", kind: "REQUEST_CREATED",
      payload: { instructionHash: replacement.instructionHash } });
    appendEvent(state, { ...baseEvent(original.requestId), category: "REQUEST_LIFECYCLE", kind: "SUPERSEDED_BEFORE_ATTEMPT",
      payload: { reason: "Replace before dispatch", replacementRequestId: replacement.requestId } });
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
    expect((): unknown => parseWorkflowState(mutate(state, "events/2/payload/replacementRequestId", original.requestId))).toThrow(/replacement/);
  });
  it("round-trips supersession with a required null replacement and no invented instruction", (): void => {
    const state = fullState();
    state.events = state.events.slice(0, 1);
    const original = requireElement(state.requests, 0);
    appendEvent(state, { ...baseEvent(original.requestId), category: "REQUEST_LIFECYCLE", kind: "SUPERSEDED_BEFORE_ATTEMPT",
      payload: { reason: "Known basis changed before another instruction was authorized", replacementRequestId: null } });
    const serialized = serializeWorkflowState(state);
    const parsed = parseWorkflowState(serialized);
    expect(parsed.events.at(-1)?.payload).toEqual(state.events.at(-1)?.payload);
    expect(serializeWorkflowState(parsed)).toBe(serialized);
    expect(parsed.requests).toHaveLength(1);
    expect(parsed.approvals).toHaveLength(1);
    [undefined, "", 42, true, {}].forEach((value): void => {
      expect((): unknown => parseWorkflowState(mutate(state, "events/1/payload/replacementRequestId", value)))
        .toThrow(/replacementRequestId/);
    });
  });
  it.each(["missing", "unrelated", "wrong-kind"])("rejects a non-null %s supersession replacement", (caseName): void => {
    const state = fullState();
    state.events = state.events.slice(0, 1);
    const original = requireElement(state.requests, 0);
    const intent = financialIntent({ dispositionKey: "another-instruction",
      replacesRequestId: caseName === "unrelated" ? null : original.requestId,
      kind: caseName === "wrong-kind" ? "CHARGE_POSTING" : "REFUND",
      recipientVersionId: caseName === "wrong-kind" ? null : original.intent.recipientVersionId });
    const approval = approvalFor(intent, "replacement-approval");
    const replacement = requestFor(intent, approval.approvalId);
    if (caseName !== "missing") {
      state.approvals.push(approval);
      state.requests.push(replacement);
      appendEvent(state, { ...baseEvent(replacement.requestId), category: "REQUEST_LIFECYCLE", kind: "REQUEST_CREATED",
        payload: { instructionHash: replacement.instructionHash } });
    }
    appendEvent(state, { ...baseEvent(original.requestId), category: "REQUEST_LIFECYCLE", kind: "SUPERSEDED_BEFORE_ATTEMPT",
      payload: { reason: "Changed before dispatch", replacementRequestId: replacement.requestId } });
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).toThrow(/replacement instruction/);
  });
  it("keeps returned and failed raw result structures distinct from accepted success", (): void => {
    const state = fullState();
    const success = requireElement(state.events, 5);
    if (success.kind !== "RAW_SIMULATED_RESULT" || success.payload.canonicalTransactionId === null) throw new Error("Expected financial success fixture");
    const returned: T.RawSimulatedResult = { ...success.payload, kind: "RETURNED", sourceEventId: "return-source-1",
      canonicalTransactionId: returnTransactionIdFor(state, success.payload.canonicalTransactionId),
      returnOfCanonicalTransactionId: success.payload.canonicalTransactionId };
    appendEvent(state, { ...baseEvent(returned.requestId, returned.attemptId, returned.sourceEventId), category: "SIMULATED_RESULT",
      kind: "RAW_SIMULATED_RESULT", payload: returned });
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
    expect((): unknown => parseWorkflowState(mutate(state, "events/7/payload/returnOfCanonicalTransactionId", null))).toThrow(ContractError);
    state.events = state.events.slice(0, 5);
    const failed: T.RawSimulatedResult = { ...success.payload, kind: "FAILED", canonicalTransactionId: null };
    appendEvent(state, { ...baseEvent(failed.requestId, failed.attemptId, failed.sourceEventId), category: "SIMULATED_RESULT",
      kind: "RAW_SIMULATED_RESULT", payload: failed });
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
  });
  it("supports statement-specific approval content/delivery and explicit revocations", (): void => {
    const state = emptyState();
    const statement = statementRecord();
    state.statements.push(statement);
    const intent: T.StatementDispatchIntent = { kind: "STATEMENT_DISPATCH", amountCents: null, currency: "USD", dispositionKey: "dispatch-statement-1",
      statementId: statement.statementId, recipientVersionId: statement.recipientVersionId, materialityHash: statement.materialityHash,
      contentHash: statement.contentHash, targetVersionId: "placeholder", replacesRequestId: null, reversesTransactionId: null };
    intent.targetVersionId = targetVersionIdFor(state, intent);
    const approved = approvalFor(intent);
    const revoked: T.ApprovalRecord = { ...approved, approvalId: approvalIdFor(state, "revoke-1", ACTOR), createdCommandId: "revoke-1",
      decision: "REVOKED", revokesApprovalId: approved.approvalId };
    state.approvals.push(approved, revoked);
    expect((): unknown => parseWorkflowState(JSON.stringify(state))).not.toThrow();
    expect((): unknown => parseWorkflowState(mutate(state, "approvals/1/revokesApprovalId", revoked.approvalId))).toThrow(ContractError);
  });
});

describe("Phase D identity semantics", (): void => {
  it("deduplicates the same financial intent across commands/approvals and display statements", (): void => {
    const intent = financialIntent();
    const approval1 = approvalFor(intent, "approval-command-1");
    const approval2 = approvalFor(intent, "approval-command-2");
    const first = requestFor(intent, approval1.approvalId);
    const second = { ...requestFor({ ...intent, statementId: "corrected-display-statement" }, approval2.approvalId), createdCommandId: "new-command", createdAt: SNAPSHOT_AT };
    expect(approval1.approvalId).not.toBe(approval2.approvalId);
    expect(second.requestId).toBe(first.requestId);
    expect(second.instructionKey).toBe(first.instructionKey);
    expect(second.instructionHash).toBe(first.instructionHash);
    expect(targetVersionIdFor(SCOPE, { ...intent, statementId: "corrected-display-statement" })).toBe(intent.targetVersionId);
  });
  it("separates partial installments, changed amount, own route, replacements and scope", (): void => {
    const original = financialIntent();
    [financialIntent({ dispositionKey: "installment-2" }), financialIntent({ amountCents: 1 }),
      financialIntent({ recipientVersionId: "new-refund-route" }), financialIntent({ materialityHash: fingerprint("changed entitlement") }),
      financialIntent({ replacesRequestId: "failed-request" })].forEach((intent): void => {
      expect(requestIdFor(SCOPE, intent)).not.toBe(requestIdFor(SCOPE, original));
    });
    expect(requestIdFor({ ...SCOPE, caseId: "another-case" }, original)).not.toBe(requestIdFor(SCOPE, original));
    expect(canonicalTransactionIdFor(SCOPE, requestIdFor(SCOPE, original)))
      .not.toBe(canonicalTransactionIdFor(SCOPE, "different-request"));
  });
  it("deduplicates statement preparation independently of new timestamps/commands/review IDs", (): void => {
    const statement = statementRecord();
    const retry = { ...statement, sourceReviewId: "review-2", createdCommandId: "prepare-2", createdAt: SNAPSHOT_AT };
    expect(statementIdFor(SCOPE, retry)).toBe(statement.statementId);
    expect(statementContentHash(retry.content, retry.renderedText)).toBe(statement.contentHash);
    expect(statementIdFor(SCOPE, { ...statement, recipientVersionId: "statement-route-2" })).not.toBe(statement.statementId);
  });
  it("separates statement/refund route versions and normalizes set-like route identities", (): void => {
    const first = { ...route(), partyIds: ["b", "a"], evidenceIds: ["e2", "e1"] };
    const reordered = { ...first, partyIds: ["a", "b"], evidenceIds: ["e1", "e2"] };
    expect(recipientVersionIdFor(SCOPE, "REFUND", first)).toBe(recipientVersionIdFor(SCOPE, "REFUND", reordered));
    expect(recipientVersionIdFor(SCOPE, "REFUND", first)).not.toBe(recipientVersionIdFor(SCOPE, "STATEMENT", first));
    expect(instructionHashFor(SCOPE, financialIntent(), first)).toBe(instructionHashFor(SCOPE, financialIntent(), reordered));
  });
  it("uses actor-independent source identity and distinguishes acceptance from receipt", (): void => {
    const state = fullState();
    const raw = requireElement(state.events, 5);
    if (raw.kind !== "RAW_SIMULATED_RESULT") throw new Error("Expected raw fixture");
    const redelivered = { ...raw, recordedBy: "other-actor", commandId: "delivery-2", recordedAt: SNAPSHOT_AT };
    expect(workflowEventIdFor(SCOPE, redelivered)).toBe(raw.eventId);
    expect(workflowEventIdFor(SCOPE, { ...raw, requestId: "conflicting-request" })).toBe(raw.eventId);
    expect(workflowEventIdFor(SCOPE, { ...raw, kind: "RESULT_ACCEPTED" })).not.toBe(raw.eventId);
    expect(resultIdentityHash({ ...raw.payload, amountCents: 10 })).not.toBe(resultIdentityHash(raw.payload));
    const anotherSource = { ...raw.payload, sourceEventId: "another-source-event", attemptId: "another-attempt" };
    expect(economicResultIdentityHash(anotherSource)).toBe(economicResultIdentityHash(raw.payload));
    expect(resultIdentityHash(anotherSource)).not.toBe(resultIdentityHash(raw.payload));
    expect(economicResultIdentityHash({ ...anotherSource, amountCents: 10 })).not.toBe(economicResultIdentityHash(raw.payload));
    expect((): unknown => workflowEventIdFor(SCOPE, { ...raw, sourceEventId: null })).toThrow(ContractError);
    expect(attemptIdFor(SCOPE, "request-1", 1)).not.toBe(attemptIdFor(SCOPE, "request-1", 2));
    expect((): unknown => attemptIdFor(SCOPE, "request-1", 0)).toThrow(ContractError);
  });
});

describe("Phase D v2 review/snapshot extras", (): void => {
  it("retains six native sections and explicit simulation outcomes without mutating v1", (): void => {
    const state = fullState();
    const review = workflowReview(state);
    const serialized = serializeWorkflowReview(review);
    expect(parseWorkflowReview(serialized)).toEqual(review);
    expect(Object.keys(review.result).sort()).toEqual(["scopeRequirements", "itemDecisions", "account", "missingInputs", "actions", "outcomes"].sort());
    expect(review.result.outcomes.depositComplete).toBe(false);
    expect(review.result.outcomes.legalPerformanceConfirmed).toBe(false);
    expect(resultFor(baseRequest()).metadata).not.toHaveProperty("workflowSchemaVersion");
    expect(hashWorkflowReview(review)).toBe(fingerprint(review));
  });
  it("requires all sidecars and verifies their hashes at recorded snapshot time", (): void => {
    const state = fullState();
    const review = workflowReview(state);
    const extras: T.WorkflowSnapshotExtras = { workflowStateJson: serializeWorkflowState(state), workflowStateHash: hashWorkflowState(state),
      workflowReviewJson: serializeWorkflowReview(review), workflowReviewHash: hashWorkflowReview(review) };
    expect(parseWorkflowSnapshot("2", extras, SNAPSHOT_AT)).toEqual({ state, review });
    expect(parseWorkflowSnapshot(undefined, {}, SNAPSHOT_AT)).toBeNull();
    expect(parseWorkflowSnapshot("0", {}, SNAPSHOT_AT)).toBeNull();
    expect((): unknown => parseWorkflowSnapshot(undefined, extras, SNAPSHOT_AT)).toThrow(ContractError);
    expect((): unknown => parseWorkflowSnapshot("2", {}, SNAPSHOT_AT)).toThrow(ContractError);
    Object.keys(extras).forEach((key): void => {
      const partial = { ...extras };
      Reflect.deleteProperty(partial, key);
      expect((): unknown => parseWorkflowSnapshot("2", partial, SNAPSHOT_AT)).toThrow(ContractError);
    });
    expect((): unknown => parseWorkflowSnapshot("2", { ...extras, workflowStateHash: "a".repeat(64) }, SNAPSHOT_AT)).toThrow(/hash/);
    expect((): unknown => parseWorkflowSnapshot("2", { ...extras, workflowReviewHash: "a".repeat(64) }, SNAPSHOT_AT)).toThrow(/hash/);
    expect((): unknown => parseWorkflowSnapshot("2", extras, "2099-01-01T00:00:00Z")).toThrow(/recorded snapshot/);
  });
  it.each([
    ["metadata/workflowSchemaVersion", "3.0.0"], ["metadata/authorityEvaluatedAt", null],
    ["result/outcomes/legalPerformanceConfirmed", true], ["result/outcomes/depositComplete", true],
    ["result/outcomes/overallCaseComplete", true], ["result/outcomes/completionMode", "LIVE"],
    ["result/account/newlyRequestableRefundCents", 0], ["result/actions/0/workflow/requestDetails/0/state", "RETURNED"],
    ["result/actions/0/workflow/requestDetails/0/reservedAmountCents", 900000],
    ["result/actions/0/workflow/approvalDetails/0/valid", "true"], ["result/anotherSection", {}],
  ] as [string, unknown][])("rejects corrupt/unsafe review extension at %s", (pointer, value): void => {
    expect((): unknown => parseWorkflowReview(mutate(workflowReview(fullState()), pointer, value))).toThrow(ContractError);
  });
  it("keeps final refund unpaid INCLUDING reserves; newly requestable is separate", (): void => {
    const review = workflowReview(fullState());
    review.result.account.finalRefundCents = 15000;
    review.result.account.pendingReservedRefundCents = 10000;
    review.result.account.financialCommitments = [{ kind: "REFUND", reservedCents: 10000, requestIds: ["refund-1"] }];
    review.result.account.newlyRequestableRefundCents = 5000;
    const parsed = parseWorkflowReview(JSON.stringify(review));
    expect(parsed.result.account.finalRefundCents).toBe(15000);
    expect(parsed.result.account.newlyRequestableRefundCents).toBe(5000);
    expect((): unknown => parseWorkflowReview(mutate(review, "result/account/newlyRequestableRefundCents", 16000))).toThrow(ContractError);
    expect((): unknown => parseWorkflowReview(mutate(review, "result/account/reconciliationState", "UNRECONCILED"))).toThrow(ContractError);
    expect((): unknown => parseWorkflowReview(mutate(review, "result/account/financialCommitments", [...review.result.account.financialCommitments, ...review.result.account.financialCommitments]))).toThrow(/duplicate/);
  });
});
