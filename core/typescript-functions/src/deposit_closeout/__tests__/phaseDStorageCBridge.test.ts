import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import addCloseoutEvidence from "../../functions/addCloseoutEvidence.js";
import associateCloseoutEvidence from "../../functions/associateCloseoutEvidence.js";
import acceptCloseoutDateFact from "../../functions/acceptCloseoutDateFact.js";
import recordCloseoutChargeDecision from "../../functions/recordCloseoutChargeDecision.js";
import waiveCloseoutCharge from "../../functions/waiveCloseoutCharge.js";
import chooseCloseoutCharge from "../../functions/chooseCloseoutCharge.js";
import setCloseoutRecipients from "../../functions/setCloseoutRecipients.js";
import recordCloseoutMoneyEvent from "../../functions/recordCloseoutMoneyEvent.js";
import reconcileCloseoutBalance from "../../functions/reconcileCloseoutBalance.js";
import updateCloseoutAuthority from "../../functions/updateCloseoutAuthority.js";
import assignCloseoutWork from "../../functions/assignCloseoutWork.js";
import recordCloseoutRelatedTask from "../../functions/recordCloseoutRelatedTask.js";
import advanceCloseoutDemoClock from "../../functions/advanceCloseoutDemoClock.js";
import recheckCloseoutCase from "../../functions/recheckCloseoutCase.js";
import setCloseoutStatementInstructions from "../../functions/setCloseoutStatementInstructions.js";
import setCloseoutRefundInstructions from "../../functions/setCloseoutRefundInstructions.js";
import prepareCloseoutStatement from "../../functions/prepareCloseoutStatement.js";
import claimCloseoutRequest from "../../functions/claimCloseoutRequest.js";
import requestCloseoutOperation from "../../functions/requestCloseoutOperation.js";
import { from_json } from "../domain/codec.js";
import type { MoneyEvent } from "../domain/types.js";
import { normalize_timestamp, compare_timestamps } from "../domain/datetime.js";
import { approvalValidity } from "../lifecycle/approvals.js";
import { parseWorkflowReview } from "../lifecycle/codec.js";
import { projectRequests } from "../lifecycle/requests.js";
import { loadCurrentReview } from "../phase_c/storage.js";
import { nativeReview, serialize } from "../phase_c/validation.js";
import { nextInputs, present, rootUpdate, type TestState } from "./phaseCTestSupport.js";
import { ACTOR, NOW, WHY, act, approved, current, initialized, requested, storageRequest, workflow, type Wrapper } from "./phaseDStorageSupport.js";
import { refundSpec } from "./phaseDRequestsSupport.js";

beforeEach((): void => { vi.useFakeTimers(); vi.setSystemTime(new Date(NOW)); });
afterEach((): void => { vi.useRealTimers(); });

const MONEY: MoneyEvent = { eventId: "manual-receipt", canonicalTransactionId: "manual-transaction", sourceEventId: "manual-source",
  kind: "DEPOSIT_RECEIPT", status: "SETTLED", amountCents: 1000, occurredAt: "2026-09-03T12:00:00.000001Z",
  learnedAt: "2026-09-03T12:00:00.000002Z", sourceEvidenceId: "ev-balance", requestId: null, reversesTransactionId: null, chargeItemId: null };
const mutations = (): [string, Wrapper, (state: TestState) => unknown][] => [
  ["ADD_EVIDENCE", addCloseoutEvidence, () => ({ ...storageRequest().snapshot.evidence[0]!, evidenceId: "additional-proof",
    externalRecordId: "additional-record", sourceVersion: "2", supersedesEvidenceId: null, associationAccepted: false })],
  ["ASSOCIATE_EVIDENCE", associateCloseoutEvidence, () => ({ evidenceId: "ev-repair", itemIds: ["repair-250"], accepted: true, reason: WHY })],
  ["ACCEPT_DATE_FACT", acceptCloseoutDateFact, (state) => current(state).snapshot.dates[0]!],
  ["RECORD_CHARGE_DECISION", recordCloseoutChargeDecision, (state) => ({ charge: current(state).snapshot.charges[0]!, resolvedQuestionIds: [] })],
  ["WAIVE_CHARGE", waiveCloseoutCharge, () => ({ itemId: "repair-250", reason: WHY })],
  ["SET_RECIPIENTS", setCloseoutRecipients, (state) => current(state).snapshot.recipients],
  ["RECORD_MONEY_EVENT", recordCloseoutMoneyEvent, () => MONEY],
  ["RECONCILE_BALANCE", reconcileCloseoutBalance, (state) => current(state).snapshot.depositBalance],
  ["UPDATE_AUTHORITY", updateCloseoutAuthority, (state) => current(state).snapshot.authorityGrants[0]!],
  ["ASSIGN_WORK", assignCloseoutWork, () => ({ requirementKey: "NC:ordinary-account", assigneePartyId: "demo-manager", internalTargetAt: null, reason: WHY })],
  ["RECORD_RELATED_TASK", recordCloseoutRelatedTask, () => ({ taskId: "additional-task", description: "Independent work", state: "OPEN", responsibleRole: "MANAGER", completionEvidenceIds: [] })],
  ["ADVANCE_DEMO_CLOCK", advanceCloseoutDemoClock, () => ({ reviewClock: "2026-09-20T12:00:00Z", reason: WHY })],
];

describe("every C mutation retains a v2 case and reprojects effective requirements", (): void => {
  it.each(mutations())("%s persists native+v2 together without changing its public replay contract", async (_kind, wrapper, payload): Promise<void> => {
    const before = await initialized();
    const commandPayload = payload(before);
    const state = await act(before, wrapper, commandPayload, "c-operation");
    expect(state.root.workflowVersion).toBe("2");
    expect(state.root.revision).toBe("3");
    expect(rootUpdate(state.edits).obj).toBe(before.root);
    expect(state.edits.filter((edit): boolean => edit.type === "updateObject" && edit.obj.$apiName === "DcCloseoutCase")).toHaveLength(1);
    const stored = await loadCurrentReview(state.store.client, state.root);
    expect(stored.review).toEqual(nativeReview(current(state)));
    expect(stored.workflowReview?.metadata.baseCaseRevision).toBe(3);
    expect(stored.workflowReview?.metadata.inputHash).toBe(stored.review.metadata.inputHash);
    expect(stored.workflow?.businessClock).toBe(normalize_timestamp(stored.request.reviewClock));
    expect(stored.workflow?.initializedAt).toBe(workflow(before).initializedAt);
    expect(await wrapper(state.store.client, state.root.caseId, ACTOR, "c-operation", "2", serialize(commandPayload))).toEqual([]);
    const later = nextInputs(state, await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "later", "3"));
    await loadCurrentReview(later.store.client, later.root);
  });
  it("choice updates both native and v2 materiality while preserving frozen decisions", async (): Promise<void> => {
    const before = await requested(await initialized());
    const frozen = workflow(before);
    const edits = await chooseCloseoutCharge(before.store.client, before.root.caseId, ACTOR, "reduce", present(before.root.revision), "repair-250", "350", WHY);
    const state = nextInputs(before, edits);
    expect(rootUpdate(edits).obj).toBe(before.root);
    expect(projectRequests(workflow(state))[0]).toMatchObject({ state: "SUPERSEDED", reservedAmountCents: 0 });
    expect(workflow(state).approvals).toEqual(frozen.approvals);
    expect(workflow(state).requests).toEqual(frozen.requests);
    expect(workflow(state).events.at(-1)).toMatchObject({ kind: "SUPERSEDED_BEFORE_ATTEMPT", commandId: "reduce" });
    const base = from_json("ReviewEnvelope", present(state.snapshot.reviewJson));
    expect(base.result.account.finalRefundCents).toBe(1650);
    expect(approvalValidity(current(state), base, workflow(state), frozen.approvals[0]!, NOW).valid).toBe(false);
    expect(await chooseCloseoutCharge(state.store.client, state.root.caseId, ACTOR, "reduce", present(before.root.revision), "repair-250", "350", WHY)).toEqual([]);
    await loadCurrentReview(state.store.client, state.root);
  });
  it("does not erase an attempted reservation on C materiality changes", async (): Promise<void> => {
    let state = await requested(await initialized());
    const requestId = workflow(state).requests[0]!.requestId;
    state = await act(state, claimCloseoutRequest, { requestId }, "claim");
    state = nextInputs(state, await chooseCloseoutCharge(state.store.client, state.root.caseId, ACTOR, "reduce-after-claim", present(state.root.revision), "repair-250", "350", WHY));
    expect(projectRequests(workflow(state))[0]).toMatchObject({ state: "CLAIMED", reservedAmountCents: 600 });
    await loadCurrentReview(state.store.client, state.root);
  });
  it("preserves independent instructions across unrelated C mutations and explicit combined-recipient no-ops", async (): Promise<void> => {
    let state = await initialized();
    const { versionId: _s, ...s } = workflow(state).statementInstructions;
    const { versionId: _r, ...r } = workflow(state).refundInstructions;
    state = await act(state, setCloseoutStatementInstructions, { ...s, routeReference: "demo-statement-separate" }, "statement-route");
    state = await act(state, setCloseoutRefundInstructions, { ...r, routeReference: "demo-refund-separate" }, "refund-route");
    const before = workflow(state);
    state = await act(state, setCloseoutRecipients, current(state).snapshot.recipients, "unchanged-legacy");
    state = await act(state, recordCloseoutRelatedTask, { taskId: "preserve-routes", description: "Unrelated task", state: "OPEN", responsibleRole: "MANAGER", completionEvidenceIds: [] }, "task");
    state = nextInputs(state, await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", present(state.root.revision)));
    expect(workflow(state).statementInstructions).toEqual(before.statementInstructions);
    expect(workflow(state).refundInstructions).toEqual(before.refundInstructions);
    state = await act(state, setCloseoutRecipients, { ...current(state).snapshot.recipients, versionId: "explicit-new-legacy",
      state: "VERIFIED", verifiedRouteReference: "demo-explicit-combined", statementMethod: "DEMO_OUTBOX", refundMethod: "DEMO_OUTBOX" }, "combined-change");
    expect(workflow(state).statementInstructions.routeReference).toBe("demo-explicit-combined");
    expect(workflow(state).refundInstructions.routeReference).toBe("demo-explicit-combined");
    await loadCurrentReview(state.store.client, state.root);
  });
  it("keeps v2 business time monotonic after a C recheck whose actual time is behind the demo clock", async (): Promise<void> => {
    let state = await requested(await initialized());
    state = await act(state, advanceCloseoutDemoClock, { reviewClock: "2026-10-02T12:00:00Z", reason: WHY }, "advance");
    const before = workflow(state);
    state = nextInputs(state, await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", present(state.root.revision)));
    expect(compare_timestamps(workflow(state).businessClock, before.businessClock)).toBeGreaterThanOrEqual(0);
    expect(workflow(state).businessClock).toBe(current(state).reviewClock);
    expect(parseWorkflowReview(present(state.snapshot.workflowReviewJson)).metadata.authorityEvaluatedAt).toBe(normalize_timestamp(NOW));
    expect(state.snapshot.createdAt).toBe(NOW);
    await loadCurrentReview(state.store.client, state.root);
  });
  it("assignment sidecar survives subsequent D changes and does not stale financial approvals", async (): Promise<void> => {
    let state = await approved(await initialized());
    const approval = workflow(state).approvals[0]!;
    state = await act(state, assignCloseoutWork, { requirementKey: "NC:ordinary-account", assigneePartyId: "demo-manager", internalTargetAt: "2026-09-21T12:00:00Z", reason: WHY }, "assign");
    const assignmentJson = state.snapshot.workAssignmentsJson;
    const assignmentHash = state.snapshot.workAssignmentsHash;
    state = await act(state, prepareCloseoutStatement, { kind: "FINAL", supersedesId: null, reason: WHY }, "prepare");
    expect(state.snapshot.workAssignmentsJson).toBe(assignmentJson);
    expect(state.snapshot.workAssignmentsHash).toBe(assignmentHash);
    expect(approvalValidity(current(state), nativeReview(current(state)), workflow(state), approval, NOW).valid).toBe(true);
    state = await act(state, requestCloseoutOperation, { approvalId: approval.approvalId }, "request");
    expect(state.snapshot.workAssignmentsJson).toBe(assignmentJson);
    const stored = await loadCurrentReview(state.store.client, state.root);
    const requirement = stored.workflowReview!.result.scopeRequirements.requirements.find((entry): boolean => entry.requirementKey === "NC:ordinary-account")!;
    expect(requirement.internalTargetAt).toBe("2026-09-21T12:00:00Z");
  });
  it("C authority revocation blocks new D requests and replays but cannot reinterpret the historical decision", async (): Promise<void> => {
    let state = await approved(await initialized());
    const decision = workflow(state).approvals[0]!;
    const grant = current(state).snapshot.authorityGrants.find((entry): boolean => entry.partyId === "demo-accountant")!;
    state = await act(state, updateCloseoutAuthority, { ...grant, authorityVersion: "accountant-revoked-v2", revoked: true }, "revoke-grant");
    expect(workflow(state).approvals[0]).toEqual(decision);
    expect(state.root.accountantIds).toEqual([]);
    await expect(requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "request", present(state.root.revision), serialize({ approvalId: decision.approvalId }))).rejects.toThrow(/authority/);
    const row = state.store.data.get(`DcApproval/${decision.approvalId}`);
    expect(row?.$apiName === "DcApproval" ? row.validity : null).toBe("INVALID");
  });
});
