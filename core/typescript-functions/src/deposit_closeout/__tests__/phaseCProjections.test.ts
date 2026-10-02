import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DcCaseParty, DcChargeItem, DcCloseoutCase, DcEvidenceRecord, DcExecutionEvent, DcMoneyEvent, DcRequirement, DcReviewSnapshot } from "@ontology/sdk";
import { createMockOsdkObject } from "@osdk/unit-testing";
import addCloseoutEvidence from "../../functions/addCloseoutEvidence.js";
import recordCloseoutChargeDecision from "../../functions/recordCloseoutChargeDecision.js";
import recordCloseoutMoneyEvent from "../../functions/recordCloseoutMoneyEvent.js";
import recheckCloseoutCase from "../../functions/recheckCloseoutCase.js";
import chooseCloseoutCharge from "../../functions/chooseCloseoutCharge.js";
import getCloseoutReview from "../../functions/getCloseoutReview.js";
import openCloseoutCase from "../../functions/openCloseoutCase.js";
import { from_json, parse_json } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import { BOOTSTRAP_ACTOR_ID as ACTOR, chargeIdFor, projectionIdFor } from "../phase_c/types.js";
import { loadCurrentReview } from "../phase_c/storage.js";
import { nativeReview, serialize } from "../phase_c/validation.js";
import { apiError, chargeCreates, chargeUpdates, nextInputs, opened, present, snapshotCreate, type TestState } from "./phaseCTestSupport.js";

beforeEach((): void => { vi.useFakeTimers(); vi.setSystemTime(new Date("2026-09-17T12:00:00Z")); });
afterEach((): void => { vi.useRealTimers(); });
const recheck = (state: TestState): ReturnType<typeof recheckCloseoutCase> =>
  recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", present(state.root.revision));

function legacy(state: TestState): TestState {
  const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, projectionVersion: undefined });
  const snapshot = createMockOsdkObject(DcReviewSnapshot, { ...state.snapshot, workAssignmentsJson: undefined, workAssignmentsHash: undefined });
  const receipt = createMockOsdkObject(DcExecutionEvent, { ...state.receipt, commandJson: undefined });
  [...state.store.data].forEach(([key, row]): void => {
    if (["DcEvidenceRecord", "DcMoneyEvent", "DcCaseParty", "DcRequirement"].includes(row.$apiName)) state.store.data.delete(key);
  });
  [root, snapshot, receipt].forEach((row): void => state.store.put(row));
  return { ...state, root, snapshot, receipt };
}

describe("versioned full projections and C0 compatibility", (): void => {
  it("reads legacy C0, replays its receipt without writing, and initializes all new types only on the first real write", async (): Promise<void> => {
    const state = legacy(await opened());
    expect((await loadCurrentReview(state.store.client, state.root)).workAssignments).toEqual([]);
    expect(await getCloseoutReview(state.store.client, state.root)).toBe(state.snapshot.reviewJson);
    expect(await openCloseoutCase(state.store.client, serialize(state.request), ACTOR, "open-1")).toEqual([]);
    const edits = await chooseCloseoutCharge(state.store.client, state.root.caseId, ACTOR, "choose", "1", "repair-250", "18000", "Legacy choice");
    expect(chargeUpdates(edits)).toHaveLength(3);
    expect(chargeCreates(edits)).toHaveLength(0);
    expect(edits.filter((entry): boolean => entry.type === "createObject" && entry.obj.apiName === "DcEvidenceRecord"))
      .toHaveLength(state.request.snapshot.evidence.length);
    expect(edits.filter((entry): boolean => entry.type === "createObject" && entry.obj.apiName === "DcCaseParty"))
      .toHaveLength(state.request.snapshot.parties.length);
    const next = nextInputs(state, edits);
    expect(next.root.projectionVersion).toBe("1");
    expect(next.snapshot.workAssignmentsJson).toBe("[]");
    expect((await state.store.client(DcReviewSnapshot).fetchOne(state.snapshot.reviewId)).workAssignmentsJson).toBeUndefined();
    await expect(recheck(next)).resolves.toBeDefined();
  });

  it.each(["missing-json", "missing-hash", "wrong-hash", "bad-json", "noncanonical", "extra-key", "duplicate-key", "foreign-actor", "unknown-party", "future-assignment", "imprecise-time"])
    ("rejects v1 sidecar %s in query and writes", async (kind): Promise<void> => {
      const state = await opened();
      let json: string | undefined = "[]";
      let hash: string | undefined = fingerprint([]);
      const base = { requirementKey: "NC:ordinary-account", assigneePartyId: "demo-manager", internalTargetAt: null,
        assignedBy: ACTOR, assignedAt: "2026-09-17T12:00:00Z", reason: "Work" };
      if (kind === "missing-json") json = undefined;
      if (kind === "missing-hash") hash = undefined;
      if (kind === "wrong-hash") hash = "a".repeat(64);
      if (kind === "bad-json") json = "{}";
      if (kind === "noncanonical") json = "[ ]";
      if (kind === "extra-key") { const value = [{ ...base, legalDeadlineOverride: "2027-01-01" }]; json = serialize(value); hash = fingerprint(value); }
      if (kind === "duplicate-key") json = '[{"reason":"a","reason":"b"}]';
      if (kind === "foreign-actor") { const value = [{ ...base, assignedBy: "other-user" }]; json = serialize(value); hash = fingerprint(value); }
      if (kind === "unknown-party") { const value = [{ ...base, assigneePartyId: "unknown-party" }]; json = serialize(value); hash = fingerprint(value); }
      if (kind === "future-assignment") { const value = [{ ...base, assignedAt: "2027-01-01T00:00:00Z" }]; json = serialize(value); hash = fingerprint(value); }
      if (kind === "imprecise-time") { const value = [{ ...base, internalTargetAt: "2026-09-18T00:00:00.1234567Z" }]; json = serialize(value); hash = fingerprint(value); }
      state.store.put(createMockOsdkObject(DcReviewSnapshot, { ...state.snapshot, workAssignmentsJson: json, workAssignmentsHash: hash }));
      await expect(getCloseoutReview(state.store.client, state.root)).rejects.toThrow();
      await expect(recheck(state)).rejects.toThrow();
    });

  it("unknown root projection versions and v0 unexpected sidecars fail closed", async (): Promise<void> => {
    const state = await opened();
    const unknown = createMockOsdkObject(DcCloseoutCase, { ...state.root, projectionVersion: "2" });
    await expect(loadCurrentReview(state.store.client, unknown)).rejects.toThrow(/version/);
    const unexpected = createMockOsdkObject(DcCloseoutCase, { ...state.root, projectionVersion: undefined });
    await expect(loadCurrentReview(state.store.client, unexpected)).rejects.toThrow(/C0/);
  });

  it("creates a new source and a newly recorded charge without trying to update nonexistent keys", async (): Promise<void> => {
    let state = await opened();
    const source = { ...present(state.request.snapshot.evidence[5]), evidenceId: "new-source", sourceVersion: "2",
      associationAccepted: false, occurredAt: "2026-09-15T12:00:00.123456Z", learnedAt: "2026-09-15T12:00:00.654321Z" };
    let edits = await addCloseoutEvidence(state.store.client, state.root.caseId, ACTOR, "source", "1", serialize(source));
    expect(edits.filter((entry): boolean => entry.type === "createObject" && entry.obj.apiName === "DcEvidenceRecord")).toHaveLength(1);
    state = nextInputs(state, edits);
    const sourceId = projectionIdFor("evidence", state.request.snapshot.managementCompanyId, state.root.caseId, "new-source");
    const projected = await state.store.client(DcEvidenceRecord).fetchOne(sourceId);
    expect(projected).toMatchObject({ recordJson: serialize(source), occurredAtIso: source.occurredAt, learnedAtIso: source.learnedAt,
      readerIds: [ACTOR], caseRevision: "2" });
    const charge = { ...present(state.request.snapshot.charges[2]), itemId: "new-charge", evidenceIds: [], unresolvedQuestionIds: [] };
    edits = await recordCloseoutChargeDecision(state.store.client, state.root.caseId, ACTOR, "charge", "2", serialize({ charge, resolvedQuestionIds: [] }));
    expect(chargeCreates(edits)).toHaveLength(1);
    expect(chargeCreates(edits)[0]?.properties.chargeRecordId).toBe(chargeIdFor(state.request.snapshot.managementCompanyId, state.root.caseId, "new-charge"));
    expect(chargeUpdates(edits)).toHaveLength(3);
    state = nextInputs(state, edits);
    await expect(recheck(state)).resolves.toBeDefined();
  });

  it("money projections preserve canonical source facts and microseconds, not a new execution ledger", async (): Promise<void> => {
    const state = await opened();
    const event = { eventId: "money-1", canonicalTransactionId: "txn-1", sourceEventId: "source-1", kind: "DEPOSIT_RECEIPT",
      status: "SETTLED", amountCents: 1000, occurredAt: "2026-09-03T12:00:00.123456Z", learnedAt: "2026-09-03T12:00:00.654321Z",
      sourceEvidenceId: "ev-balance", requestId: null, reversesTransactionId: null, chargeItemId: null };
    const edits = await recordCloseoutMoneyEvent(state.store.client, state.root.caseId, ACTOR, "event", "1", serialize(event));
    const result = nextInputs(state, edits);
    const row = await result.store.client(DcMoneyEvent).fetchOne(projectionIdFor("money", state.request.snapshot.managementCompanyId, state.root.caseId, event.eventId));
    expect(row.recordJson).toBe(serialize(event));
    expect(from_json("ReviewRequest", present(result.snapshot.requestJson)).snapshot.executionEvents).toEqual([]);
    expect(result.snapshot.reviewJson).toBe(serialize(nativeReview(from_json("ReviewRequest", present(result.snapshot.requestJson)))));
  });
});

describe("projection reads never conceal corruption as absence", (): void => {
  it.each(["record", "readers", "revision", "company", "source-time", "missing"]) ("rejects evidence %s", async (kind): Promise<void> => {
    const state = await opened();
    const pk = projectionIdFor("evidence", state.request.snapshot.managementCompanyId, state.root.caseId, "ev-repair");
    const row = await state.store.client(DcEvidenceRecord).fetchOne(pk);
    const patch: { -readonly [K in keyof DcEvidenceRecord.Props]?: DcEvidenceRecord.Props[K] } = {};
    if (kind === "record") patch.recordJson = "{}";
    if (kind === "readers") patch.readerIds = ["other-user"];
    if (kind === "revision") patch.caseRevision = "2";
    if (kind === "company") patch.managementCompanyId = "foreign";
    if (kind === "source-time") patch.learnedAtIso = "2026-09-04T12:00:00.000001Z";
    state.store.put(createMockOsdkObject(DcEvidenceRecord, { ...row, ...patch }));
    if (kind === "missing") state.store.data.delete(`DcEvidenceRecord/${pk}`);
    await expect(recheck(state)).rejects.toThrow(/projection/);
  });

  it("rejects a charge projection's forged zero instead of using or overwriting it", async (): Promise<void> => {
    const state = await opened();
    const pk = chargeIdFor(state.request.snapshot.managementCompanyId, state.root.caseId, "repair-250");
    const row = await state.store.client(DcChargeItem).fetchOne(pk);
    state.store.put(createMockOsdkObject(DcChargeItem, { ...row, chosenAmountCents: "0" }));
    await expect(recheck(state)).rejects.toThrow(/chosenAmountCents/);
  });

  it("rejects party grant projection tampering and never trusts stated roles as permission", async (): Promise<void> => {
    const state = await opened();
    const pk = projectionIdFor("party", state.request.snapshot.managementCompanyId, state.root.caseId, "demo-manager");
    const row = await state.store.client(DcCaseParty).fetchOne(pk);
    state.store.put(createMockOsdkObject(DcCaseParty, { ...row, grantsJson: "[]" }));
    await expect(recheck(state)).rejects.toThrow(/grantsJson/);
  });

  it("rejects missing/corrupt work rows rather than recreating them or hiding assignments", async (): Promise<void> => {
    const state = await opened();
    const pk = projectionIdFor("requirement", state.request.snapshot.managementCompanyId, state.root.caseId, "NC:ordinary-account");
    const row = await state.store.client(DcRequirement).fetchOne(pk);
    state.store.put(createMockOsdkObject(DcRequirement, { ...row, resultJson: "{}" }));
    await expect(recheck(state)).rejects.toThrow(/resultJson/);
    state.store.data.delete(`DcRequirement/${pk}`);
    await expect(recheck(state)).rejects.toThrow(/projection/);
  });

  it.each(["ObjectNotFound", "PermissionDenied", "Timeout"]) ("required work query %s propagates rather than meaning absence", async (kind): Promise<void> => {
    const state = await opened();
    const error = kind === "ObjectNotFound" ? apiError(kind, "NOT_FOUND", 404) : new Error(kind);
    state.store.fail("DcRequirement", `case:${state.root.caseId}`, error);
    await expect(recheck(state)).rejects.toBe(error);
  });

  it("a bounded query with another page fails rather than emitting a partial case write", async (): Promise<void> => {
    const state = await opened();
    const source = await state.store.client(DcRequirement).fetchOne(projectionIdFor("requirement", state.request.snapshot.managementCompanyId, state.root.caseId, "NC:ordinary-account"));
    Array.from({ length: 1001 }, (_, index): void => state.store.put(createMockOsdkObject(DcRequirement,
      { ...source, requirementId: `overflow-${index}`, requirementKey: `overflow:${index}` })));
    await expect(recheck(state)).rejects.toThrow(/bound/);
  });

  it("recheck canonical work hash always survives an immediate validated read", async (): Promise<void> => {
    const state = await opened();
    const edits = await recheck(state);
    const snapshot = snapshotCreate(edits).properties;
    expect(snapshot.workAssignmentsHash).toBe(fingerprint(parse_json(present(snapshot.workAssignmentsJson))));
    const next = nextInputs(state, edits);
    expect(await getCloseoutReview(next.store.client, next.root)).toBe(snapshot.reviewJson);
  });
});
