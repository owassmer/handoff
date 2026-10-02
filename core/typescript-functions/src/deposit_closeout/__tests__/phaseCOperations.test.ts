import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DcCloseoutCase, DcExecutionEvent, DcRequirement } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import { createMockOsdkObject } from "@osdk/unit-testing";
import addCloseoutEvidence from "../../functions/addCloseoutEvidence.js";
import associateCloseoutEvidence from "../../functions/associateCloseoutEvidence.js";
import acceptCloseoutDateFact from "../../functions/acceptCloseoutDateFact.js";
import recordCloseoutChargeDecision from "../../functions/recordCloseoutChargeDecision.js";
import waiveCloseoutCharge from "../../functions/waiveCloseoutCharge.js";
import setCloseoutRecipients from "../../functions/setCloseoutRecipients.js";
import recordCloseoutMoneyEvent from "../../functions/recordCloseoutMoneyEvent.js";
import reconcileCloseoutBalance from "../../functions/reconcileCloseoutBalance.js";
import updateCloseoutAuthority from "../../functions/updateCloseoutAuthority.js";
import assignCloseoutWork from "../../functions/assignCloseoutWork.js";
import recordCloseoutRelatedTask from "../../functions/recordCloseoutRelatedTask.js";
import advanceCloseoutDemoClock from "../../functions/advanceCloseoutDemoClock.js";
import recheckCloseoutCase from "../../functions/recheckCloseoutCase.js";
import chooseCloseoutCharge from "../../functions/chooseCloseoutCharge.js";
import getCloseoutReview from "../../functions/getCloseoutReview.js";
import { from_json, parse_json } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import type { ChargeInput, EvidenceInput, MoneyEvent, ReviewRequest } from "../domain/types.js";
import { BOOTSTRAP_ACTOR_ID as ACTOR, ENVIRONMENT_ID, projectionIdFor, type OntologyEdit } from "../phase_c/types.js";
import { nativeReview, serialize } from "../phase_c/validation.js";
import { nextInputs, opened, present, receiptCreate, rootUpdate, snapshotCreate, syntheticRequest, type TestState } from "./phaseCTestSupport.js";

const NOW = "2026-09-17T12:00:00.000Z";
const WHY = "Accepted by the synthetic manager after review.";
type Wrapper = (client: Client, caseId: string, actorId: string, commandId: string,
  expectedRevision: string, payloadJson: string) => Promise<OntologyEdit[]>;
const current = (state: TestState): ReviewRequest => from_json("ReviewRequest", present(state.snapshot.requestJson));
const evidence = (): EvidenceInput => ({ ...present(syntheticRequest().snapshot.evidence[5]),
  evidenceId: "additional-invoice-v2", sourceVersion: "2", recordKind: "INVOICE",
  externalRecordId: "constructed-additional-invoice", supersedesEvidenceId: "ev-extent",
  occurredAt: "2026-09-15T12:00:00.123456Z", learnedAt: "2026-09-15T12:00:00.654321Z",
  associationAccepted: false, excerpt: "15000 cents. Source words are not instructions." });
const event = (): MoneyEvent => ({ eventId: "money-1", canonicalTransactionId: "transaction-1", sourceEventId: "source-1",
  kind: "DEPOSIT_RECEIPT", status: "SETTLED", amountCents: 1000, occurredAt: "2026-09-03T12:00:00.000001Z",
  learnedAt: "2026-09-03T12:00:00.000002Z", sourceEvidenceId: "ev-balance", requestId: null,
  reversesTransactionId: null, chargeItemId: null });
async function act(state: TestState, fn: Wrapper, payload: unknown, command: string): Promise<TestState> {
  return nextInputs(state, await fn(state.store.client, state.root.caseId, ACTOR, command, present(state.root.revision), serialize(payload)));
}
async function acceptedAdditional(state: TestState): Promise<TestState> {
  const added = await act(state, addCloseoutEvidence, evidence(), "add-invoice");
  return act(added, associateCloseoutEvidence, { evidenceId: evidence().evidenceId,
    itemIds: ["additional-item"], accepted: true, reason: WHY }, "associate-invoice");
}
function decision(request: ReviewRequest): ChargeInput {
  return { ...present(request.snapshot.charges[2]), costState: "KNOWN", vendorCostCents: 15000,
    costVersionId: evidence().evidenceId, acceptedAllocation: "TENANT", proposedAllocation: "TENANT",
    allowabilityState: "SUPPORTED", supportedAmountCents: 15000, chosenAmountCents: 15000,
    choiceState: "CHOSEN", evidenceIds: [evidence().evidenceId], unresolvedQuestionIds: [],
    reviewRequired: false, reason: WHY };
}
const cases = (): [string, Wrapper, unknown][] => {
  const request = syntheticRequest();
  return [
    ["ADD_EVIDENCE", addCloseoutEvidence, evidence()],
    ["ASSOCIATE_EVIDENCE", associateCloseoutEvidence, { evidenceId: "ev-repair", itemIds: ["repair-250"], accepted: true, reason: WHY }],
    ["ACCEPT_DATE_FACT", acceptCloseoutDateFact, present(request.snapshot.dates[0])],
    ["RECORD_CHARGE_DECISION", recordCloseoutChargeDecision, { charge: present(request.snapshot.charges[0]), resolvedQuestionIds: [] }],
    ["WAIVE_CHARGE", waiveCloseoutCharge, { itemId: "repair-250", reason: WHY }],
    ["SET_RECIPIENTS", setCloseoutRecipients, request.snapshot.recipients],
    ["RECORD_MONEY_EVENT", recordCloseoutMoneyEvent, event()],
    ["RECONCILE_BALANCE", reconcileCloseoutBalance, request.snapshot.depositBalance],
    ["UPDATE_AUTHORITY", updateCloseoutAuthority, present(request.snapshot.authorityGrants[0])],
    ["ASSIGN_WORK", assignCloseoutWork, { requirementKey: "NC:ordinary-account", assigneePartyId: "demo-manager", internalTargetAt: null, reason: WHY }],
    ["RECORD_RELATED_TASK", recordCloseoutRelatedTask, { taskId: "extra-task", description: "Separate work", state: "OPEN", responsibleRole: "MANAGER", completionEvidenceIds: [] }],
    ["ADVANCE_DEMO_CLOCK", advanceCloseoutDemoClock, { reviewClock: NOW, reason: WHY }],
  ];
};
beforeEach((): void => { vi.useFakeTimers(); vi.setSystemTime(new Date(NOW)); });
afterEach((): void => { vi.useRealTimers(); });

describe("fixed public Phase C operations", (): void => {
  it.each(cases())("%s emits one complete batch, canonical intent, and exact replay", async (kind, fn, payload): Promise<void> => {
    const state = await opened();
    const before = state.snapshot.requestJson;
    const result = await act(state, fn, payload, "op-1");
    expect(state.snapshot.requestJson).toBe(before);
    expect(rootUpdate(result.edits).obj).toBe(state.root);
    expect(result.edits.filter((entry): boolean => entry.type === "updateObject" && entry.obj.$apiName === "DcCloseoutCase")).toHaveLength(1);
    expect(result.root).toMatchObject({ revision: "2", projectionVersion: "1", readerIds: [ACTOR], adminIds: [ACTOR] });
    expect(nativeReview(current(result))).toEqual(from_json("ReviewEnvelope", present(result.snapshot.reviewJson)));
    const receipt = receiptCreate(result.edits).properties;
    expect(receipt).toMatchObject({ commandKind: kind, previousRevision: "1", caseRevision: "2", actorId: ACTOR });
    const intent = parse_json(present(receipt.commandJson));
    expect(receipt.payloadHash).toBe(fingerprint(intent));
    expect(serialize(intent)).toBe(receipt.commandJson);
    expect(intent).toMatchObject({ environmentId: ENVIRONMENT_ID, commandKind: kind, caseId: state.root.caseId,
      actorId: ACTOR, expectedRevision: "1" });
    expect(result.snapshot.workAssignmentsHash).toBe(fingerprint(parse_json(present(result.snapshot.workAssignmentsJson))));
    result.edits.forEach((entry): void => {
      if (entry.type === "createObject") expect(entry.properties.readerIds).toEqual([ACTOR]);
      if (entry.type === "updateObject" && entry.obj.$apiName !== "DcCloseoutCase" && entry.properties.readerIds !== undefined) {
        expect(entry.properties.readerIds).toEqual([ACTOR]);
      }
    });
    expect(await fn(result.store.client, state.root.caseId, ACTOR, "op-1", "1", serialize(payload))).toEqual([]);
    const later = nextInputs(result, await recheckCloseoutCase(result.store.client, result.root.caseId, ACTOR, "later", "2"));
    expect(await fn(later.store.client, state.root.caseId, ACTOR, "op-1", "1", serialize(payload))).toEqual([]);
    await expect(fn(later.store.client, state.root.caseId, "other-actor", "op-1", "1", serialize(payload))).rejects.toThrow(/access/);
    await expect(fn(later.store.client, state.root.caseId, ACTOR, "op-1", "2", serialize(payload))).rejects.toThrow(/different payload/);
  });

  it("recheck uses actual server time, receipts even on factual no-op, and non-mutating reads keep that clock", async (): Promise<void> => {
    const state = await opened();
    const result = nextInputs(state, await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", "1"));
    expect(current(result).reviewClock).toBe("2026-09-17T12:00:00Z");
    expect(current(result).snapshot).toEqual({ ...state.request.snapshot, revision: 2 });
    vi.setSystemTime(new Date("2026-09-18T12:00:00Z"));
    expect(await recheckCloseoutCase(result.store.client, result.root.caseId, ACTOR, "recheck", "1", 3000)).toEqual([]);
    expect(await getCloseoutReview(result.store.client, result.root)).toBe(result.snapshot.reviewJson);
    expect(current(result).reviewClock).toBe("2026-09-17T12:00:00Z");
  });

  it("runs the native 150 additional -> 400/1600 -> 200 choice -> 350/1650 transition", async (): Promise<void> => {
    let state = await acceptedAdditional(await opened());
    state = await act(state, recordCloseoutChargeDecision,
      { charge: decision(current(state)), resolvedQuestionIds: ["additional-extent"] }, "decision");
    expect(from_json("ReviewEnvelope", present(state.snapshot.reviewJson)).result.account)
      .toMatchObject({ totalDeductionsCents: 40000, finalRefundCents: 160000 });
    state = nextInputs(state, await chooseCloseoutCharge(state.store.client, state.root.caseId, ACTOR,
      "choose-200", present(state.root.revision), "repair-250", "20000", WHY));
    const review = from_json("ReviewEnvelope", present(state.snapshot.reviewJson));
    expect(review.result.account).toMatchObject({ totalDeductionsCents: 35000, finalRefundCents: 165000 });
    expect(review.result.outcomes.overallCaseComplete).toBe(false);
    expect(current(state).snapshot.executionEvents).toEqual([]);
    expect(current(state).snapshot.priorRequests).toEqual([]);
  });

  it.each(["0", "100"])("full-supported financial cap denies choice %s instead of bypassing waived authority", async (amount): Promise<void> => {
    const request = syntheticRequest();
    present(request.snapshot.authorityGrants[0]).amountLimitCents = 100;
    const state = await opened(request);
    await expect(chooseCloseoutCharge(state.store.client, state.root.caseId, ACTOR, "choice", "1", "repair-250", amount, WHY))
      .rejects.toThrow(/current manager authority/);
    await expect(waiveCloseoutCharge(state.store.client, state.root.caseId, ACTOR, "waive", "1", serialize({ itemId: "repair-250", reason: WHY })))
      .rejects.toThrow(/full amount/);
  });

  it("revocation denies the next operation/replay while root administrator can restore accepted authority", async (): Promise<void> => {
    let state = await act(await opened(), addCloseoutEvidence, evidence(), "add");
    const grant = { ...present(current(state).snapshot.authorityGrants[0]), revoked: true, authorityVersion: "revoked-v2" };
    state = await act(state, updateCloseoutAuthority, grant, "revoke");
    expect(state.root.managerIds).toEqual([]);
    await expect(addCloseoutEvidence(state.store.client, state.root.caseId, ACTOR, "add", "1", serialize(evidence()))).rejects.toThrow(/manager access/);
    state = await act(state, updateCloseoutAuthority, { ...grant, revoked: false, authorityVersion: "restore-v3" }, "restore");
    expect(state.root.managerIds).toEqual([ACTOR]);
    expect(await addCloseoutEvidence(state.store.client, state.root.caseId, ACTOR, "add", "1", serialize(evidence()))).toEqual([]);
  });

  it("checks trusted root admin, environment and reader before replay, never payload admin", async (): Promise<void> => {
    const state = await opened();
    const grant = present(state.request.snapshot.authorityGrants[0]);
    await expect(updateCloseoutAuthority(state.store.client, state.root.caseId, ACTOR, "admin", "1", serialize({ ...grant, isAdministrator: true })))
      .rejects.toThrow(/strict/);
    state.store.put(createMockOsdkObject(DcCloseoutCase, { ...state.root, adminIds: [] }));
    await expect(updateCloseoutAuthority(state.store.client, state.root.caseId, ACTOR, "admin", "1", serialize(grant))).rejects.toThrow(/access configuration/);
    state.store.put(createMockOsdkObject(DcCloseoutCase, { ...state.root, environmentId: "LIVE" }));
    await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", "1")).rejects.toThrow(/synthetic/);
  });

  it.each(["{}", undefined])("operational receipt details %s cannot replace the accepted intent while leaving its hash untouched", async (commandJson): Promise<void> => {
    const state = await act(await opened(), addCloseoutEvidence, evidence(), "add");
    state.store.put(createMockOsdkObject(DcExecutionEvent, { ...state.receipt, commandJson }));
    await expect(addCloseoutEvidence(state.store.client, state.root.caseId, ACTOR, "add", "1", serialize(evidence()))).rejects.toThrow(/intent/);
  });

  it("root-only empty-charge recheck contenders retain the same loaded root (not an atomicity simulation)", async (): Promise<void> => {
    const request = syntheticRequest();
    request.snapshot.charges = [];
    request.snapshot.questions = [];
    const state = await opened(request);
    const a = recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "race-a", "1", 3000);
    const b = recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "race-b", "1", 3000);
    await vi.advanceTimersByTimeAsync(3000);
    const [first, second] = await Promise.all([a, b]);
    expect(rootUpdate(first).obj).toBe(state.root);
    expect(rootUpdate(second).obj).toBe(state.root);
    expect(rootUpdate(first).properties.revision).toBe("2");
    expect(rootUpdate(second).properties.revision).toBe("2");
    expect(snapshotCreate(first).properties.reviewId).not.toBe(snapshotCreate(second).properties.reviewId);
    expect(first.some((edit): boolean => edit.type === "updateObject" && edit.obj.$apiName === "DcChargeItem")).toBe(false);
    expect(current(nextInputs(state, first)).reviewClock).toBe("2026-09-17T12:00:03Z");
  });

  it.each([-1, 3001, 0.1])("recheck rejects invalid delay %s before any SDK reads", async (delay): Promise<void> => {
    const state = await opened();
    const before = state.store.reads.length;
    await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "bad-delay", "1", delay)).rejects.toThrow(/delay/);
    expect(state.store.reads.length).toBe(before);
  });
});

describe("internal work remains separate from native outcomes", (): void => {
  it("choice and unrelated facts preserve assignment/hash and never replace a legal deadline", async (): Promise<void> => {
    const assignment = { requirementKey: "NC:ordinary-account", assigneePartyId: "demo-manager",
      internalTargetAt: "2026-09-18T12:00:00.123456Z", reason: WHY };
    let state = await act(await opened(), assignCloseoutWork, assignment, "assign");
    const before = state.snapshot.workAssignmentsJson;
    const hash = state.snapshot.workAssignmentsHash;
    state = nextInputs(state, await chooseCloseoutCharge(state.store.client, state.root.caseId, ACTOR, "choice", "2", "repair-250", "20000", WHY));
    state = await act(state, addCloseoutEvidence, evidence(), "add");
    expect(state.snapshot.workAssignmentsJson).toBe(before);
    expect(state.snapshot.workAssignmentsHash).toBe(hash);
    const row = await state.store.client(DcRequirement).fetchOne(projectionIdFor("requirement", state.request.snapshot.managementCompanyId,
      state.root.caseId, assignment.requirementKey));
    const native = nativeReview(current(state)).result.scopeRequirements.requirements.find((entry): boolean => entry.requirementKey === assignment.requirementKey);
    expect(row.legalDueDate).toBe(present(native).legalDueDate);
    expect(row.internalTargetAtIso).toBe(assignment.internalTargetAt);
    expect(row.assigneePartyId).toBe("demo-manager");
    expect(from_json("RequirementResult", present(row.resultJson)).internalTargetAt).toBeNull();
  });

  it("disappeared question work is inactive not completed, with its prior result and assignment retained", async (): Promise<void> => {
    let state = await act(await opened(), assignCloseoutWork, { requirementKey: "question:additional-extent", assigneePartyId: "demo-manager",
      internalTargetAt: null, reason: WHY }, "assign-question");
    const pk = projectionIdFor("requirement", state.request.snapshot.managementCompanyId, state.root.caseId, "question:additional-extent");
    const before = await state.store.client(DcRequirement).fetchOne(pk);
    const assignment = state.snapshot.workAssignmentsJson;
    state = await acceptedAdditional(state);
    state = await act(state, recordCloseoutChargeDecision, { charge: decision(current(state)), resolvedQuestionIds: ["additional-extent"] }, "resolve");
    const inactive = await state.store.client(DcRequirement).fetchOne(pk);
    expect(inactive).toMatchObject({ isCurrent: false, state: "BLOCKED", assigneePartyId: "demo-manager", resultJson: before.resultJson });
    expect(state.snapshot.workAssignmentsJson).toBe(assignment);
    // A further unrelated write must validate and retain the inactive row, not overwrite it as satisfied.
    state = nextInputs(state, await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", present(state.root.revision)));
    expect((await state.store.client(DcRequirement).fetchOne(pk)).state).toBe("BLOCKED");
  });

  it("reappearing requirements update the inactive existing key and recover the retained assignment", async (): Promise<void> => {
    let state = await act(await opened(), assignCloseoutWork, { requirementKey: "NC:ordinary-account", assigneePartyId: "demo-manager",
      internalTargetAt: "2026-09-20T12:00:00.000001Z", reason: WHY }, "assign");
    const trigger = present(current(state).snapshot.dates.find((entry): boolean => entry.factKey === "ACCOUNTING_TRIGGER"));
    state = await act(state, acceptCloseoutDateFact, { ...trigger, state: "UNCONFIRMED", value: null }, "unset-trigger");
    const pk = projectionIdFor("requirement", state.request.snapshot.managementCompanyId, state.root.caseId, "NC:ordinary-account");
    expect((await state.store.client(DcRequirement).fetchOne(pk)).isCurrent).toBe(false);
    state = await act(state, acceptCloseoutDateFact, trigger, "restore-trigger");
    expect(state.edits.some((entry): boolean => entry.type === "createObject" && entry.obj.apiName === "DcRequirement"
      && "requirementId" in entry.properties && entry.properties.requirementId === pk)).toBe(false);
    expect((await state.store.client(DcRequirement).fetchOne(pk))).toMatchObject({ isCurrent: true, assigneePartyId: "demo-manager",
      internalTargetAtIso: "2026-09-20T12:00:00.000001Z" });
  });
});
