import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DcCloseoutCase, DcExecutionEvent } from "@ontology/sdk";
import { createMockOsdkObject } from "@osdk/unit-testing";
import initializeCloseoutWorkflow from "../../functions/initializeCloseoutWorkflow.js";
import acceptCloseoutScopeFacts from "../../functions/acceptCloseoutScopeFacts.js";
import qualifyCloseoutInterim from "../../functions/qualifyCloseoutInterim.js";
import upsertCloseoutRecipientParty from "../../functions/upsertCloseoutRecipientParty.js";
import setCloseoutStatementInstructions from "../../functions/setCloseoutStatementInstructions.js";
import setCloseoutRefundInstructions from "../../functions/setCloseoutRefundInstructions.js";
import prepareCloseoutStatement from "../../functions/prepareCloseoutStatement.js";
import decideCloseoutApproval from "../../functions/decideCloseoutApproval.js";
import revokeCloseoutApproval from "../../functions/revokeCloseoutApproval.js";
import requestCloseoutOperation from "../../functions/requestCloseoutOperation.js";
import claimCloseoutRequest from "../../functions/claimCloseoutRequest.js";
import markCloseoutOutcomeUnknown from "../../functions/markCloseoutOutcomeUnknown.js";
import simulateCloseoutResult from "../../functions/simulateCloseoutResult.js";
import ingestCloseoutResult from "../../functions/ingestCloseoutResult.js";
import cancelUnattemptedCloseoutRequest from "../../functions/cancelUnattemptedCloseoutRequest.js";
import getCloseoutWorkflow from "../../functions/getCloseoutWorkflow.js";
import recheckCloseoutCase from "../../functions/recheckCloseoutCase.js";
import updateCloseoutAuthority from "../../functions/updateCloseoutAuthority.js";
import { canonical_json, from_json } from "../domain/codec.js";
import { parseWorkflowReview } from "../lifecycle/codec.js";
import { projectRequests } from "../lifecycle/requests.js";
import { receiptIdFor, reviewIdFor } from "../phase_c/types.js";
import { nativeReview, serialize } from "../phase_c/validation.js";
import { loadCurrentReview } from "../phase_c/storage.js";
import { nextInputs, opened, present, rootUpdate } from "./phaseCTestSupport.js";
import { refundSpec } from "./phaseDRequestsSupport.js";
import { ACTOR, NOW, WHY, act, approved, current, initialized, requested, settled, storageRequest, workflow, type Wrapper } from "./phaseDStorageSupport.js";

const WRAPPERS: [string, Wrapper][] = [
  ["INIT_WORKFLOW", initializeCloseoutWorkflow], ["ACCEPT_SCOPE_FACTS", acceptCloseoutScopeFacts],
  ["SET_INTERIM_QUALIFICATION", qualifyCloseoutInterim], ["UPSERT_RECIPIENT_PARTY", upsertCloseoutRecipientParty],
  ["SET_STATEMENT_INSTRUCTIONS", setCloseoutStatementInstructions], ["SET_REFUND_INSTRUCTIONS", setCloseoutRefundInstructions],
  ["PREPARE_STATEMENT", prepareCloseoutStatement], ["DECIDE_APPROVAL", decideCloseoutApproval],
  ["REVOKE_APPROVAL", revokeCloseoutApproval], ["REQUEST_OPERATION", requestCloseoutOperation],
  ["CLAIM_REQUEST", claimCloseoutRequest], ["RECORD_OUTCOME_UNKNOWN", markCloseoutOutcomeUnknown],
  ["GENERATE_SIMULATED_RESULT", simulateCloseoutResult], ["INGEST_RESULT", ingestCloseoutResult],
  ["CANCEL_UNATTEMPTED_REQUEST", cancelUnattemptedCloseoutRequest],
];
beforeEach((): void => { vi.useFakeTimers(); vi.setSystemTime(new Date(NOW)); });
afterEach((): void => { vi.useRealTimers(); });

describe("fixed public D command admission", (): void => {
  it.each(WRAPPERS)("%s rejects arbitrary payload fields before reading any case", async (_kind, wrapper): Promise<void> => {
    const state = await opened(storageRequest());
    const before = state.store.reads.length;
    await expect(wrapper(state.store.client, state.root.caseId, ACTOR, "bad", "1", '{"admin":true}')).rejects.toThrow();
    expect(state.store.reads).toHaveLength(before);
  });
  it("initialization replay stays empty after later revisions, with strict canonical command intent", async (): Promise<void> => {
    let state = await initialized();
    state = nextInputs(state, await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "later", "2"));
    const count = state.store.data.size;
    expect(await initializeCloseoutWorkflow(state.store.client, state.root.caseId, ACTOR, "init", "1", " {} ")).toEqual([]);
    expect(state.store.data.size).toBe(count);
    await expect(initializeCloseoutWorkflow(state.store.client, state.root.caseId, ACTOR, "init", "2", "{}")).rejects.toThrow(/different payload/);
    const repeated = await act(state, initializeCloseoutWorkflow, {}, "new-init");
    expect(workflow(repeated).initializedAt).toBe(workflow(state).initializedAt);
    expect(workflow(repeated).initializedBy).toBe(workflow(state).initializedBy);
    expect(repeated.root.revision).toBe("4");
    state = repeated;
    const receipt = state.store.data.get(`DcExecutionEvent/${receiptIdFor(state.request.snapshot.managementCompanyId, state.root.caseId, "init")}`);
    if (receipt?.$apiName !== "DcExecutionEvent") throw new Error("Missing receipt");
    expect({ category: receipt.eventCategory, kind: receipt.commandKind }).toEqual({ category: "COMMAND_RECEIPT", kind: "INIT_WORKFLOW" });
    state.store.put(createMockOsdkObject(DcExecutionEvent, { ...receipt, commandJson: undefined }));
    await expect(initializeCloseoutWorkflow(state.store.client, state.root.caseId, ACTOR, "init", "1", "{}")).rejects.toThrow(/intent/);
  });
  it("checks actual actor scope before replay and does not admit a payload administrator", async (): Promise<void> => {
    const state = await initialized();
    await expect(initializeCloseoutWorkflow(state.store.client, state.root.caseId, "other-principal", "init", "1", "{}")).rejects.toThrow(/access/);
    const wrongRoot = createMockOsdkObject(DcCloseoutCase, { ...state.root, environmentId: "OTHER" });
    state.store.put(wrongRoot);
    await expect(initializeCloseoutWorkflow(state.store.client, state.root.caseId, ACTOR, "init", "1", "{}")).rejects.toThrow(/environment/);
  });
  it("rechecks present-day financial authority before an early receipt replay", async (): Promise<void> => {
    const input = storageRequest();
    input.snapshot.authorityGrants.find((grant): boolean => grant.partyId === "demo-accountant")!.effectiveUntil = "2026-09-19T00:00:00Z";
    const initial = await approved(await initialized(input));
    const payload = { approvalId: workflow(initial).approvals[0]!.approvalId };
    const state = await act(initial, requestCloseoutOperation, payload, "admit");
    expect(await requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "admit", present(initial.root.revision), serialize(payload))).toEqual([]);
    vi.setSystemTime(new Date("2026-09-20T00:00:00Z"));
    await expect(requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "admit", present(initial.root.revision), serialize(payload))).rejects.toThrow(/authority/);
  });
  it("allows authorized early replay after applicability changes, without rereading child projections", async (): Promise<void> => {
    const before = await approved(await initialized());
    const approvalId = workflow(before).approvals[0]!.approvalId;
    let state = await act(before, requestCloseoutOperation, { approvalId }, "admit");
    const requestId = workflow(state).requests[0]!.requestId;
    state = await act(state, cancelUnattemptedCloseoutRequest, { requestId, reason: WHY }, "cancel");
    const readCount = state.store.reads.length;
    expect(await requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "admit", present(before.root.revision), serialize({ approvalId }))).toEqual([]);
    expect(state.store.reads.slice(readCount).filter((key): boolean => key.includes("/case:"))).toEqual([]);
    await expect(requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "different-command", present(before.root.revision), serialize({ approvalId }))).rejects.toThrow(/revision changed/);
    await expect(requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "admit", present(before.root.revision), serialize({ approvalId: "wrong" }))).rejects.toThrow();
  });
  it("records decisions and independent routes through all preparation-side wrappers", async (): Promise<void> => {
    let state = await initialized();
    state = await act(state, acceptCloseoutScopeFacts, { jurisdiction: "NC", tenancyRegime: storageRequest().snapshot.tenancyRegime, tenancyEndsInFull: true,
      cashSecurityDeposit: true, evidenceIds: ["ev-agreement"], reason: WHY }, "scope");
    state = await act(state, qualifyCloseoutInterim, { state: "NOT_APPLICABLE", evidenceIds: ["ev-agreement"], reason: WHY }, "interim");
    const resident = current(state).snapshot.parties.find((party): boolean => party.partyId === "demo-resident")!;
    state = await act(state, upsertCloseoutRecipientParty, { party: { ...resident, displayLabel: "Accepted resident label" } }, "party");
    const refund = workflow(state).refundInstructions;
    const { versionId: _version, ...statement } = workflow(state).statementInstructions;
    state = await act(state, setCloseoutStatementInstructions, { ...statement, routeReference: "demo-statement-only" }, "statement-route");
    expect(workflow(state).refundInstructions).toEqual(refund);
    const statementVersion = workflow(state).statementInstructions;
    const { versionId: _refundVersion, ...refundInput } = refund;
    state = await act(state, setCloseoutRefundInstructions, { ...refundInput, routeReference: "demo-refund-only" }, "refund-route");
    expect(workflow(state).statementInstructions).toEqual(statementVersion);
    state = await act(state, prepareCloseoutStatement, { kind: "FINAL", supersedesId: null, reason: WHY }, "prepare");
    const statementId = workflow(state).currentStatementId;
    expect(statementId).not.toBeNull();
    state = await approved(state, { ...refundSpec(), kind: "STATEMENT_DISPATCH", amountCents: null, statementId }, "approve-statement");
    const approvalId = workflow(state).approvals.at(-1)!.approvalId;
    state = await act(state, revokeCloseoutApproval, { approvalId, reason: WHY }, "withdraw");
    expect(workflow(state).approvals.at(-1)).toMatchObject({ decision: "REVOKED", revokesApprovalId: approvalId });
    expect(workflow(state).statements[0]!.sourceReviewId).toContain("dc-review:");
    await loadCurrentReview(state.store.client, state.root);
  });
  it("withdraws an unattempted reservation after grant expiry as trusted admin, without a current financial grant", async (): Promise<void> => {
    const input = storageRequest();
    input.snapshot.authorityGrants.find((grant): boolean => grant.partyId === "demo-accountant")!.effectiveUntil = "2026-09-19T00:00:00Z";
    let state = await requested(await initialized(input));
    vi.setSystemTime(new Date("2026-09-20T00:00:00Z"));
    state = await act(state, cancelUnattemptedCloseoutRequest, { requestId: workflow(state).requests[0]!.requestId, reason: WHY }, "expired-withdraw");
    expect(projectRequests(workflow(state))[0]).toMatchObject({ state: "CANCELLED", reservedAmountCents: 0 });
    expect(state.root.accountantIds).toEqual([]);
    await loadCurrentReview(state.store.client, state.root);
  });
});

describe("append-only lifecycle observations are not receipts", (): void => {
  it("claims, records unknown, accepts late result after revocation, and ingests only at latest case revision", async (): Promise<void> => {
    let state = await requested(await initialized());
    const requestId = workflow(state).requests[0]!.requestId;
    state = await act(state, claimCloseoutRequest, { requestId }, "claim");
    const attemptId = projectRequests(workflow(state))[0]!.attemptId;
    state = await act(state, markCloseoutOutcomeUnknown, { requestId, attemptId, reason: WHY }, "unknown");
    const unknown = workflow(state);
    expect(projectRequests(unknown)[0]).toMatchObject({ state: "OUTCOME_UNKNOWN", reservedAmountCents: 600 });
    const approvalId = unknown.approvals[0]!.approvalId;
    state = await act(state, revokeCloseoutApproval, { approvalId, reason: WHY }, "revoke");
    const rawPayload = { requestId, attemptId, sourceEventId: "late-proof", outcome: "SUCCEEDED", amountCents: 600, occurredAt: null };
    state = await act(state, simulateCloseoutResult, rawPayload, "raw");
    const rawState = state;
    expect(projectRequests(workflow(state))[0]).toMatchObject({ state: "OUTCOME_UNKNOWN", reservedAmountCents: 600 });
    const beforeIngestRevision = present(state.root.revision);
    state = nextInputs(state, await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "between", beforeIngestRevision));
    await expect(ingestCloseoutResult(state.store.client, state.root.caseId, ACTOR, "ingest", beforeIngestRevision,
      serialize({ sourceEventId: "late-proof" }))).rejects.toThrow(/revision changed/);
    const latestRevision = present(state.root.revision);
    state = await act(state, ingestCloseoutResult, { sourceEventId: "late-proof" }, "ingest");
    expect(projectRequests(workflow(state))[0]).toMatchObject({ state: "SUCCEEDED", reservedAmountCents: 0 });
    expect(await ingestCloseoutResult(state.store.client, state.root.caseId, ACTOR, "ingest", latestRevision, serialize({ sourceEventId: "late-proof" }))).toEqual([]);
    const emitted = state.edits.filter((edit) => edit.type === "createObject" && edit.obj.apiName === "DcExecutionEvent");
    expect(emitted).toHaveLength(2);
    expect(workflow(state).events.filter((event): boolean => event.kind === "RESULT_ACCEPTED")).toHaveLength(1);
    workflow(state).events.forEach((event): void => {
      const row = state.store.data.get(`DcExecutionEvent/${event.eventId}`);
      expect(row).toMatchObject({ eventId: event.eventId, eventJson: canonical_json(event), actorId: ACTOR,
        occurredAt: event.recordedAt, eventSequence: String(event.sequence), businessOccurredAtIso: event.occurredAt,
        learnedAtIso: event.learnedAt, requestId, mode: "SIMULATED", resultCode: undefined, resultJson: undefined });
      if (row?.$apiName !== "DcExecutionEvent") throw new Error("Missing event");
      expect(row.reviewId).toBe(reviewIdFor(state.request.snapshot.managementCompanyId, state.root.caseId, present(row.caseRevision), event.commandId));
      expect(event.eventId.startsWith("dc-workflow-event:")).toBe(true);
      expect(row.eventCategory).not.toBe("COMMAND_RECEIPT");
    });
    const raw = workflow(rawState).events.find((event): boolean => event.kind === "RAW_SIMULATED_RESULT")!;
    const rawRow = state.store.data.get(`DcExecutionEvent/${raw.eventId}`);
    expect(rawRow).toMatchObject({ eventCategory: "RAW_SIMULATED_RESULT", caseRevision: rawState.root.revision });
    expect(state.edits.some((edit): boolean => edit.type === "updateObject" && edit.obj.$apiName === "DcExecutionEvent")).toBe(false);
    expect(from_json("ReviewEnvelope", present(state.snapshot.reviewJson))).toEqual(nativeReview(current(state)));
    await loadCurrentReview(state.store.client, state.root);
  });
  it("validates event category, canonical JSON, creation revision and review identity before further writes", async (): Promise<void> => {
    const state = await requested(await initialized());
    const event = workflow(state).events[0]!;
    const row = state.store.data.get(`DcExecutionEvent/${event.eventId}`);
    if (row?.$apiName !== "DcExecutionEvent") throw new Error("Missing event");
    const corruptions: Partial<DcExecutionEvent.Props>[] = [
      { eventCategory: "COMMAND_RECEIPT" }, { eventJson: "{}" }, { caseRevision: "999" }, { reviewId: "wrong-review" },
      { commandId: "wrong-command" }, { readerIds: ["wrong-reader"] }, { resultCode: "APPLIED" },
    ];
    for (const patch of corruptions) {
      state.store.put(createMockOsdkObject(DcExecutionEvent, { ...row, ...patch }));
      await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "must-fail", present(state.root.revision))).rejects.toThrow();
    }
  });
  it("completes the ordinary synthetic case through persisted edit arrays without making v1 legal completion true", async (): Promise<void> => {
    let state = await act(await initialized(), prepareCloseoutStatement, { kind: "FINAL", supersedesId: null, reason: WHY }, "statement");
    for (const [kind, amount] of [["STATEMENT_DISPATCH", null], ["REFUND", 1600], ["CHARGE_POSTING", 400], ["DEPOSIT_APPLICATION", 400]] as const) {
      state = await requested(state, { ...refundSpec(), kind, amountCents: amount,
        statementId: kind === "STATEMENT_DISPATCH" ? workflow(state).currentStatementId : null,
        dispositionKey: `complete-${kind}` }, `complete-${kind}`);
      state = await settled(state, workflow(state).requests.at(-1)!.requestId, `proof-${kind}`, amount);
    }
    const v2 = parseWorkflowReview(await getCloseoutWorkflow(state.store.client, state.root.caseId));
    expect(v2.result.outcomes).toMatchObject({ simulatedDepositWorkflowComplete: true, simulatedOverallWorkflowComplete: true,
      depositComplete: false, overallCaseComplete: false, legalPerformanceConfirmed: false, completionMode: "SIMULATED" });
    expect(from_json("ReviewEnvelope", present(state.snapshot.reviewJson)).result.outcomes.depositComplete).toBe(false);
    const requirements = [...state.store.data.values()].filter((row) => row.$apiName === "DcRequirement" && row.isCurrent);
    expect(requirements).toHaveLength(v2.result.scopeRequirements.requirements.length);
    v2.result.scopeRequirements.requirements.forEach((entry): void => {
      expect(requirements.some((row): boolean => row.$apiName === "DcRequirement" && row.resultJson === serialize(entry))).toBe(true);
    });
  }, 30000);
});

describe("synthetic request overlap hook retains observed root", (): void => {
  it.each([-1, 0.5, 3001])("rejects invalid delay %s before reads", async (delay): Promise<void> => {
    const state = await approved(await initialized());
    const before = state.store.reads.length;
    await expect(requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "request", present(state.root.revision),
      serialize({ approvalId: workflow(state).approvals[0]!.approvalId }), delay)).rejects.toThrow(/delay/);
    expect(state.store.reads).toHaveLength(before);
  });
  it("retains the loaded root after a competing input is observed in the mock store, without claiming a platform race result", async (): Promise<void> => {
    const state = await approved(await initialized());
    const start = state.store.reads.length;
    const pending = requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "delayed", present(state.root.revision),
      serialize({ approvalId: workflow(state).approvals[0]!.approvalId }), 1000);
    await vi.advanceTimersByTimeAsync(0);
    expect(vi.getTimerCount()).toBe(1);
    state.store.put(createMockOsdkObject(DcCloseoutCase, { ...state.root, revision: "999" }));
    await vi.advanceTimersByTimeAsync(1000);
    const edits = await pending;
    expect(rootUpdate(edits).obj).toBe(state.root);
    expect(rootUpdate(edits).properties.revision).toBe(String(Number(state.root.revision) + 1));
    expect(state.store.reads.slice(start).filter((entry): boolean => entry.startsWith("DcCloseoutCase/"))).toHaveLength(1);
  });
  it("rechecks authority after the delay instead of using the pre-delay grant", async (): Promise<void> => {
    const input = storageRequest();
    input.snapshot.authorityGrants.find((grant): boolean => grant.partyId === "demo-accountant")!.effectiveUntil = "2026-09-18T12:00:01Z";
    const state = await approved(await initialized(input));
    const pending = requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "delayed", present(state.root.revision),
      serialize({ approvalId: workflow(state).approvals[0]!.approvalId }), 2000);
    const expectation = expect(pending).rejects.toThrow(/authority/);
    await vi.advanceTimersByTimeAsync(2000);
    await expectation;
  });
});
