/** Native Phase D regression: terminal failure does not erase contradictory raw success. */
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { canonical_json } from "../domain/codec.js";
import { approvalValidity, revokeApproval } from "../lifecycle/approvals.js";
import { applyLifecycleCommand } from "../lifecycle/commands.js";
import { parseWorkflowState } from "../lifecycle/codec.js";
import { canonicalTransactionIdFor } from "../lifecycle/ids.js";
import { projectNativeFacts, projectRequests, reconcileRequestsAfterChange } from "../lifecycle/requests.js";
import { reviewWorkflow } from "../lifecycle/review.js";
import type { FinancialOperationKind, OperationIntentSpec, WorkflowReviewV2 } from "../lifecycle/types.js";
import { loadCurrentReview } from "../phase_c/storage.js";
import { nativeReview, serialize } from "../phase_c/validation.js";
import decideCloseoutApproval from "../../functions/decideCloseoutApproval.js";
import requestCloseoutOperation from "../../functions/requestCloseoutOperation.js";
import claimCloseoutRequest from "../../functions/claimCloseoutRequest.js";
import simulateCloseoutResult from "../../functions/simulateCloseoutResult.js";
import ingestCloseoutResult from "../../functions/ingestCloseoutResult.js";
import { present } from "./phaseCTestSupport.js";
import { RequestHarness, refundSpec, REQUEST_NOW } from "./phaseDRequestsSupport.js";
import { ACTOR, NOW, act, current, initialized, requested, workflow } from "./phaseDStorageSupport.js";

const FINANCIAL_KINDS: readonly FinancialOperationKind[] = ["REFUND", "CHARGE_POSTING", "DEPOSIT_APPLICATION",
  "CHARGE_POSTING_REVERSAL", "DEPOSIT_APPLICATION_REVERSAL"];
const RECONCILIATION_ERROR = /reconcil/i;

function view(h: RequestHarness): WorkflowReviewV2 {
  const projected = projectNativeFacts(h.request, h.workflow);
  return reviewWorkflow(projected, nativeReview(projected), h.workflow, [], REQUEST_NOW);
}
function financialFixture(kind: FinancialOperationKind = "REFUND"): { h: RequestHarness; spec: OperationIntentSpec } {
  const h = new RequestHarness();
  if (!kind.endsWith("_REVERSAL")) return { h, spec: refundSpec(kind === "REFUND" ? 1600 : 400, "original", { kind }) };
  const originalKind = kind === "CHARGE_POSTING_REVERSAL" ? "CHARGE_POSTING" : "DEPOSIT_APPLICATION";
  const original = h.admit(refundSpec(400, "canonical-original", { kind: originalKind }));
  h.settle(original, "canonical-original-success", 400);
  h.request.snapshot.charges[0]!.chosenAmountCents = 100;
  return { h, spec: refundSpec(300, "original", { kind,
    reversesTransactionId: canonicalTransactionIdFor(h.workflow, original) }) };
}
function failedFixture(kind: FinancialOperationKind = "REFUND"): { h: RequestHarness; spec: OperationIntentSpec; failed: string } {
  const { h, spec } = financialFixture(kind);
  const failed = h.admit(spec);
  h.claim(failed); h.raw(failed, "original-failure", "FAILED", spec.amountCents); h.ingest("original-failure");
  return { h, failed, spec };
}
function contradict(h: RequestHarness, failed: string, amountCents: number | null): void {
  h.raw(failed, "late-contradictory-success", "SUCCEEDED", amountCents);
  expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === failed)).toMatchObject({
    state: "FAILED", reservedAmountCents: 0, reconciliationRequired: true,
  });
  const before = canonical_json({ request: h.request, workflow: h.workflow });
  expect((): unknown => h.ingest("late-contradictory-success")).toThrow(/contradict/);
  expect(canonical_json({ request: h.request, workflow: h.workflow })).toBe(before);
}

// Each row has real native capacity and a valid exact approval before the raw conflict.
// The reversal rows use accepted canonical original settlements, not fabricated balances.
describe.each(FINANCIAL_KINDS)("unresolved %s evidence gates every new financial boundary", (kind): void => {
  it.each(["approval", "request", "claim", "first-send"] as const)("blocks replacement %s without changing history or commitments", (boundary): void => {
    const { h, failed, spec } = failedFixture(kind);
    const replacement = { ...spec, dispositionKey: "replacement", replacesRequestId: failed };
    let approvalId = "";
    let replacementId = "";
    if (boundary !== "approval") approvalId = h.approve(replacement);
    if (boundary === "claim" || boundary === "first-send") {
      replacementId = String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
    }
    if (boundary === "first-send") h.claim(replacementId);
    const approvals = parseWorkflowState(canonical_json(h.workflow)).approvals;
    const money = structuredClone(h.request.snapshot.moneyEvents);
    contradict(h, failed, spec.amountCents);
    const before = canonical_json({ request: h.request, workflow: h.workflow });
    const attempt = (): unknown => {
      if (boundary === "approval") return h.approve(replacement);
      if (boundary === "request") return h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } });
      if (boundary === "claim") return h.claim(replacementId);
      return h.raw(replacementId, "must-not-send", "SUCCEEDED", spec.amountCents);
    };
    expect(attempt).toThrow(RECONCILIATION_ERROR);
    expect(canonical_json({ request: h.request, workflow: h.workflow })).toBe(before);
    expect(h.workflow.approvals).toEqual(approvals);
    expect(h.request.snapshot.moneyEvents).toEqual(money);
    expect(h.workflow.events.some((event): boolean => event.sourceEventId === "must-not-send")).toBe(false);
    if (replacementId !== "") expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === replacementId))
      .toMatchObject({ state: boundary === "claim" ? "READY" : "CLAIMED", reservedAmountCents: spec.amountCents });
    expect(parseWorkflowState(canonical_json(h.workflow))).toEqual(h.workflow);
  });

  it("also rejects a new independent approval, not only a labeled replacement", (): void => {
    const { h, failed, spec } = failedFixture(kind);
    contradict(h, failed, spec.amountCents);
    expect((): unknown => h.approve({ ...spec, dispositionKey: "independent", replacesRequestId: null }))
      .toThrow(RECONCILIATION_ERROR);
  });

  it("still permits a definitively failed replacement without contradictory evidence", (): void => {
    const { h, failed, spec } = failedFixture(kind);
    const replacement = h.admit({ ...spec, dispositionKey: "replacement", replacesRequestId: failed });
    expect(replacement).not.toBe(failed);
    expect(canonicalTransactionIdFor(h.workflow, replacement)).not.toBe(canonicalTransactionIdFor(h.workflow, failed));
    h.settle(replacement, "replacement-success", spec.amountCents);
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === failed))
      .toMatchObject({ state: "FAILED", reconciliationRequired: false });
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === replacement))
      .toMatchObject({ state: "SUCCEEDED", reconciliationRequired: false, reservedAmountCents: 0 });
    expect(h.account().reconciliationState).toBe("RECONCILED");
  });
});

describe("conflict scope, evidence preservation and supported resolution", (): void => {
  it.each(["request", "claim", "first-send"] as const)("refund uncertainty blocks unrelated posting %s, not merely the parent kind", (boundary): void => {
    const { h, failed } = failedFixture();
    const approvalId = h.approve(refundSpec(400, "independent-posting", { kind: "CHARGE_POSTING" }));
    const posting = boundary === "request" ? "" : String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
    if (boundary === "first-send") h.claim(posting);
    contradict(h, failed, 1600);
    expect((): unknown => boundary === "request" ? h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } })
      : boundary === "claim" ? h.claim(posting) : h.raw(posting, "must-not-post", "SUCCEEDED", 400)).toThrow(RECONCILIATION_ERROR);
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
  });

  it("keeps the concrete 2000/400/1600 case blocked and named for reconciliation; rechecks/replays do not choose a winning fact", (): void => {
    const { h, failed } = failedFixture();
    const replacementApproval = h.approve(refundSpec(1600, "replacement", { replacesRequestId: failed }));
    const replacement = String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId: replacementApproval } }).summary.requestId);
    contradict(h, failed, 1600);
    const account = h.account();
    expect(account).toMatchObject({ recordedDepositCents: 2000, finalRefundCents: 1600, priorNetRefundsCents: 0,
      pendingReservedRefundCents: 1600, reconciliationState: "RECONCILED" });
    const history = structuredClone(h.workflow);
    const approval = h.workflow.approvals.find((entry): boolean => entry.approvalId === replacementApproval)!;
    expect(approvalValidity(h.request, nativeReview(h.request), h.workflow, approval, REQUEST_NOW).valid).toBe(true);
    const r = view(h);
    expect(r.result.outcomes.simulatedDepositWorkflowComplete).toBe(false);
    expect(r.result.outcomes.tracks.find((entry): boolean => entry.track === "MONEY")!.state).toBe("BLOCKED");
    expect(r.result.actions.find((entry): boolean => entry.actionKey === `claim:${replacement}`)!.availability).toBe("BLOCKED");
    expect(r.result.actions.find((entry): boolean => entry.actionKey === `reconcile:${failed}`)).toMatchObject({
      actionKind: "RECONCILE_MONEY_RECORD", availability: "AVAILABLE",
    });
    const { financialCommitments: _commitments, newlyRequestableRefundCents: _capacity, ...baseAccount } = r.result.account;
    expect(baseAccount).toEqual(account);
    const rechecked = reconcileRequestsAfterChange(h.request, h.workflow, h.ctx());
    expect(rechecked.workflow).toEqual(history);
    h.raw(failed, "late-contradictory-success", "SUCCEEDED", 1600);
    expect(h.ingest("original-failure").summary.replayed).toBe(true);
    expect(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId: replacementApproval } }).summary.replayed).toBe(true);
    expect(h.workflow).toEqual(history);
    h.raw(failed, "corroborating-failure", "FAILED", 1600); h.ingest("corroborating-failure");
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === failed)!.reconciliationRequired).toBe(true);
    expect((): unknown => h.claim(replacement)).toThrow(RECONCILIATION_ERROR);
    expect(h.account()).toEqual(account);
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
  });

  it("does not block independent statement preparation, approval, admission, claim, send or ingestion", (): void => {
    const { h, failed } = failedFixture(); contradict(h, failed, 1600);
    const statementId = h.prepare();
    const dispatch = h.admit(refundSpec(0, "independent-statement", { kind: "STATEMENT_DISPATCH", amountCents: null, statementId }));
    h.settle(dispatch, "independent-dispatch", null);
    expect(h.request.snapshot.priorStatements.find((entry): boolean => entry.versionId === statementId)!.issuedAt).not.toBeNull();
    expect(h.account()).toMatchObject({ priorNetRefundsCents: 0, finalRefundCents: 1600 });
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === failed)!.reconciliationRequired).toBe(true);
  });

  it.each(["CANCEL_UNATTEMPTED_REQUEST", "REVOKE_APPROVAL"] as const)("still allows explicit %s while the separate contradiction remains unresolved", (kind): void => {
    const { h, failed } = failedFixture();
    const replacement = h.admit(refundSpec(1600, "withdrawable", { replacesRequestId: failed }));
    contradict(h, failed, 1600);
    const command = kind === "CANCEL_UNATTEMPTED_REQUEST"
      ? { kind, payload: { requestId: replacement, reason: "Explicitly withdraw unsent replacement." } }
      : { kind, payload: { approvalId: h.workflow.requests.at(-1)!.approvalIds[0]!, reason: "Explicitly revoke unsent replacement." } };
    const result = applyLifecycleCommand(h.request, [], h.workflow, command, h.ctx());
    expect(projectRequests(result.workflow).find((entry): boolean => entry.requestId === failed))
      .toMatchObject({ state: "FAILED", reconciliationRequired: true });
    expect(projectRequests(result.workflow).find((entry): boolean => entry.requestId === replacement))
      .toMatchObject({ state: kind === "CANCEL_UNATTEMPTED_REQUEST" ? "CANCELLED" : "SUPERSEDED", reservedAmountCents: 0 });
    expect(result.request.snapshot.moneyEvents).toHaveLength(0);
  });

  it("unknown then late success resolves normally after approval revocation, with one canonical money effect", (): void => {
    const h = new RequestHarness(); const id = h.admit(refundSpec(1600)); const attemptId = h.claim(id);
    h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: id, attemptId, reason: "Response lost." } });
    h.workflow.approvals.push(revokeApproval(h.request, h.workflow, h.workflow.approvals[0]!.approvalId, h.ctx()));
    expect((): unknown => h.approve(refundSpec(400, "posting", { kind: "CHARGE_POSTING" }))).toThrow();
    h.raw(id, "late-success", "SUCCEEDED", 1600); h.ingest("late-success");
    expect(projectRequests(h.workflow)[0]).toMatchObject({ state: "SUCCEEDED", reconciliationRequired: false, reservedAmountCents: 0 });
    expect(h.account()).toMatchObject({ finalRefundCents: 0, priorNetRefundsCents: 1600 });
    const posting = h.admit(refundSpec(400, "posting", { kind: "CHARGE_POSTING" }));
    h.claim(posting);
    expect(h.ingest("late-success").summary.replayed).toBe(true);
    h.raw(id, "success-redelivery", "SUCCEEDED", 1600); h.ingest("success-redelivery");
    expect(h.request.snapshot.moneyEvents).toHaveLength(1);
  });

  it.each(["REQUESTED", "OUTCOME_UNKNOWN", "FAILED"] as const)("permits late %s facts and eligible ingestion despite another conflict and now-revoked approval", (state): void => {
    const { h, failed } = failedFixture();
    const observed = h.admit(refundSpec(600, "already-attempted")); const attemptId = h.claim(observed);
    if (state === "OUTCOME_UNKNOWN") h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: observed, attemptId, reason: "Uncertain." } });
    else {
      h.raw(observed, "first-observation", state === "FAILED" ? "FAILED" : "SUCCEEDED", 600);
      if (state === "FAILED") h.ingest("first-observation");
    }
    const approvalId = h.workflow.requests.at(-1)!.approvalIds[0]!;
    h.workflow.approvals.push(revokeApproval(h.request, h.workflow, approvalId, h.ctx()));
    contradict(h, failed, 1600);
    h.raw(observed, "late-observation", state === "FAILED" ? "FAILED" : "SUCCEEDED", 600);
    h.ingest("late-observation");
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === observed)!.state)
      .toBe(state === "FAILED" ? "FAILED" : "SUCCEEDED");
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === failed)!.reconciliationRequired).toBe(true);
    expect(h.account().priorNetRefundsCents).toBe(state === "FAILED" ? 0 : 600);
  });

  it("a statement contradiction alone is not unresolved financial evidence", (): void => {
    const h = new RequestHarness(); const statementId = h.prepare();
    const dispatch = h.admit(refundSpec(0, "statement", { kind: "STATEMENT_DISPATCH", amountCents: null, statementId }));
    h.claim(dispatch); h.raw(dispatch, "dispatch-failed", "FAILED", null); h.ingest("dispatch-failed");
    h.raw(dispatch, "dispatch-possible-success", "SUCCEEDED", null);
    expect(projectRequests(h.workflow)[0]!.reconciliationRequired).toBe(true);
    const refund = h.admit(refundSpec(1600)); h.settle(refund, "refund-success", 1600);
    expect(h.account().priorNetRefundsCents).toBe(1600);
  });
});

describe("native SDK edit-array admission and receipt replay (no real Actions)", (): void => {
  beforeEach((): void => { vi.useFakeTimers(); vi.setSystemTime(new Date(NOW)); });
  afterEach((): void => { vi.useRealTimers(); });

  it.each(["READY", "CLAIMED"] as const)("rejects new work on a conflicted parent and %s replacement; authorized receipts remain effect-free", async (replacementState): Promise<void> => {
    let state = await requested(await initialized(), refundSpec(1600), "original");
    const failed = workflow(state).requests[0]!.requestId;
    state = await act(state, claimCloseoutRequest, { requestId: failed }, "original-claim");
    const attemptId = projectRequests(workflow(state))[0]!.attemptId!;
    state = await act(state, simulateCloseoutResult, { requestId: failed, attemptId, sourceEventId: "failure",
      outcome: "FAILED", amountCents: 1600, occurredAt: null }, "failure-raw");
    const ingestRevision = present(state.root.revision);
    state = await act(state, ingestCloseoutResult, { sourceEventId: "failure" }, "failure-ingest");
    const replacementSpec = refundSpec(1600, "replacement", { replacesRequestId: failed });
    const approvalRevision = present(state.root.revision);
    state = await act(state, decideCloseoutApproval, { intent: replacementSpec, decision: "APPROVED" }, "replacement-approval");
    const approvalId = workflow(state).approvals.at(-1)!.approvalId;
    const requestRevision = present(state.root.revision);
    state = await act(state, requestCloseoutOperation, { approvalId }, "replacement-request");
    const replacement = workflow(state).requests.at(-1)!.requestId;
    const claimRevision = present(state.root.revision);
    if (replacementState === "CLAIMED") state = await act(state, claimCloseoutRequest, { requestId: replacement }, "replacement-claim");
    const rawPayload = { requestId: failed, attemptId, sourceEventId: "contradiction", outcome: "SUCCEEDED", amountCents: 1600, occurredAt: null };
    const rawRevision = present(state.root.revision);
    state = await act(state, simulateCloseoutResult, rawPayload, "contradiction-raw");
    const revision = present(state.root.revision);
    const requestJson = state.snapshot.requestJson;
    const workflowJson = state.snapshot.workflowStateJson;
    const rowCount = state.store.data.size;
    await expect(ingestCloseoutResult(state.store.client, state.root.caseId, ACTOR, "contradiction-ingest", revision,
      serialize({ sourceEventId: "contradiction" }))).rejects.toThrow(/contradict/);
    await expect(decideCloseoutApproval(state.store.client, state.root.caseId, ACTOR, "new-approval", revision,
      serialize({ intent: { ...replacementSpec, dispositionKey: "another-replacement" }, decision: "APPROVED" }))
      .then((edits): number => edits.length)).rejects.toThrow(RECONCILIATION_ERROR);
    if (replacementState === "READY") {
      await expect(claimCloseoutRequest(state.store.client, state.root.caseId, ACTOR, "new-claim", revision,
        serialize({ requestId: replacement }))).rejects.toThrow(RECONCILIATION_ERROR);
    } else {
      await expect(simulateCloseoutResult(state.store.client, state.root.caseId, ACTOR, "must-not-send", revision,
        serialize({ requestId: replacement, attemptId: projectRequests(workflow(state)).at(-1)!.attemptId,
          sourceEventId: "must-not-send", outcome: "SUCCEEDED", amountCents: 1600, occurredAt: null }))).rejects.toThrow(RECONCILIATION_ERROR);
      expect(await claimCloseoutRequest(state.store.client, state.root.caseId, ACTOR, "replacement-claim", claimRevision,
        serialize({ requestId: replacement }))).toEqual([]);
    }
    expect(await decideCloseoutApproval(state.store.client, state.root.caseId, ACTOR, "replacement-approval", approvalRevision,
      serialize({ intent: replacementSpec, decision: "APPROVED" }))).toEqual([]);
    expect(await requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "replacement-request", requestRevision, serialize({ approvalId }))).toEqual([]);
    expect(await ingestCloseoutResult(state.store.client, state.root.caseId, ACTOR, "failure-ingest", ingestRevision,
      serialize({ sourceEventId: "failure" }))).toEqual([]);
    expect(await simulateCloseoutResult(state.store.client, state.root.caseId, ACTOR, "contradiction-raw", rawRevision, serialize(rawPayload))).toEqual([]);
    expect(state.root.revision).toBe(revision);
    expect(state.snapshot.requestJson).toBe(requestJson); expect(state.snapshot.workflowStateJson).toBe(workflowJson);
    expect(state.store.data.size).toBe(rowCount);
    expect(current(state).snapshot.moneyEvents).toHaveLength(0);
    expect(projectRequests(workflow(state))).toMatchObject([
      { state: "FAILED", reconciliationRequired: true, reservedAmountCents: 0 },
      { state: replacementState, reservedAmountCents: 1600 },
    ]);
    await loadCurrentReview(state.store.client, state.root);
  });
});
