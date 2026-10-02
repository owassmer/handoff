import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DcCloseoutCase, DcExecutionEvent, DcReviewSnapshot } from "@ontology/sdk";
import { createMockOsdkObject } from "@osdk/unit-testing";
import openCloseoutCase from "../../functions/openCloseoutCase.js";
import { chooseCharge } from "../phase_c/commands.js";
import getCloseoutReview from "../../functions/getCloseoutReview.js";
import { canonical_json, from_json } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import type { ReviewRequest } from "../domain/types.js";
import {
  BOOTSTRAP_ACTOR_ID as ACTOR, caseIdFor, chargeIdFor, CHOOSE_COMMAND, COMPANY_ID,
  ENVIRONMENT_ID, MAX_PAYLOAD_BYTES, OPEN_COMMAND, receiptIdFor, reviewIdFor, type OntologyEdit,
} from "../phase_c/types.js";
import { nativeReview, parseReview, serialize } from "../phase_c/validation.js";
import {
  apiError, chargeCreates, chargeUpdates, nextInputs, opened, PkStore, present,
  receiptCreate, rootCreate, rootUpdate, snapshotCreate, syntheticRequest, type TestState,
} from "./phaseCTestSupport.js";

const NOW = "2026-09-17T12:00:00.000Z";
const REASON = "Synthetic manager chooses a reduced supported amount.";

function choose(
  state: TestState, commandId: string = "choose-1", amount: string = "20000",
  expected: string = "1", reason: string = REASON, delay?: number, itemId: string = "repair-250",
): Promise<OntologyEdit[]> {
  return chooseCharge(state.store.client, state.root, ACTOR, commandId,
    expected, itemId, amount, reason, delay);
}

beforeEach((): void => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(NOW));
});
afterEach((): void => { vi.useRealTimers(); });

describe("C0 bootstrap batch (unit edit shapes, not a platform atomicity proof)", (): void => {
  it("creates the root, immutable snapshot, receipt and all three native charge projections", async (): Promise<void> => {
    const state = await opened();
    expect(state.edits).toHaveLength(6 + state.request.snapshot.evidence.length
      + state.request.snapshot.moneyEvents.length + state.request.snapshot.parties.length
      + nativeReview(state.request).result.scopeRequirements.requirements.length);
    expect(state.root.projectionVersion).toBe("1");
    expect(state.snapshot.workAssignmentsJson).toBe("[]");
    expect(state.snapshot.workAssignmentsHash).toBe(fingerprint([]));
    expect(state.edits.every((edit): boolean => edit.type === "createObject")).toBe(true);
    expect(rootCreate(state.edits).properties).toMatchObject({
      caseId: caseIdFor(COMPANY_ID, state.request.snapshot.tenancyId), revision: "1",
      environmentId: ENVIRONMENT_ID, readerIds: [ACTOR], managerIds: [ACTOR],
      accountantIds: [ACTOR], adminIds: [ACTOR], createdBy: ACTOR, updatedBy: ACTOR,
    });
    expect(state.snapshot.requestJson).toBe(canonical_json(state.request));
    expect(parseReview(present(state.snapshot.reviewJson))).toEqual(nativeReview(state.request));
    expect(state.root.inputHash).toBe(nativeReview(state.request).metadata.inputHash);
    expect(state.snapshot.resultHash).toBe(fingerprint(nativeReview(state.request)));
    expect(state.receipt).toMatchObject({ commandKind: OPEN_COMMAND, previousRevision: "0", caseRevision: "1", actorId: ACTOR });
    const charges = chargeCreates(state.edits).map((edit) => edit.properties);
    expect(charges).toHaveLength(3);
    expect(charges.find((charge): boolean => charge.itemId === "repair-250")).toMatchObject({ chosenAmountCents: "25000", vendorCostCents: "25000" });
    expect(charges.find((charge): boolean => charge.itemId === "paint-800")).toMatchObject({ chosenAmountCents: "0", allocation: "OWNER", allowability: "DISALLOWED" });
    expect(charges.find((charge): boolean => charge.itemId === "additional-item")).toMatchObject({ chosenAmountCents: undefined, vendorCostCents: undefined, costVersionId: undefined, reviewRequired: true });
    charges.forEach((charge): void => {
      expect(charge.readerIds).toEqual([ACTOR]);
      expect(charge.chargeRecordId).toBe(chargeIdFor(COMPANY_ID, state.root.caseId, present(charge.itemId)));
    });
  });

  it("does not mutate the existing native fixture or the caller's request", async (): Promise<void> => {
    const request = syntheticRequest();
    const before = structuredClone(request);
    await opened(request);
    expect(request).toEqual(before);
    expect(syntheticRequest()).toEqual(before);
  });

  it("does not rewrite an existing case and replays only the identical opening command", async (): Promise<void> => {
    const state = await opened();
    expect(await openCloseoutCase(state.store.client, serialize(state.request), ACTOR, "open-1")).toEqual([]);
    await expect(openCloseoutCase(state.store.client, serialize(state.request), ACTOR, "different-open")).rejects.toThrow(/already exists/);
    const different = structuredClone(state.request);
    different.snapshot.homeId = "different-home";
    await expect(openCloseoutCase(state.store.client, serialize(different), ACTOR, "open-1")).rejects.toThrow(/different payload/);
  });

  it("refuses an orphan receipt instead of recreating a case", async (): Promise<void> => {
    const state = await opened();
    state.store.data.delete(`DcCloseoutCase/${state.root.caseId}`);
    await expect(openCloseoutCase(state.store.client, serialize(state.request), ACTOR, "open-1")).rejects.toThrow(/without its case/);
  });

  const badOpenInputs: [string, (request: ReviewRequest) => void][] = [
    ["live origin", (request): void => { request.snapshot.origin = "LIVE"; }],
    ["another company", (request): void => { request.snapshot.managementCompanyId = "other-company"; }],
    ["revision two", (request): void => { request.snapshot.revision = 2; }],
    ["implicit or legacy release", (request): void => { request.ruleReleaseId = "NC_SYNTHETIC_DEMO_V1"; }],
    ["arbitrary case ID", (request): void => { request.snapshot.caseId = "caller-case-id"; }],
    ["missing principal", (request): void => { present(request.snapshot.parties.find((party): boolean => party.roles.includes("MANAGER"))).principalId = null; }],
    ["arbitrary principal grant", (request): void => { present(request.snapshot.parties.find((party): boolean => party.roles.includes("ACCOUNTANT"))).principalId = "another-principal"; }],
    ["duplicate charge IDs", (request): void => { request.snapshot.charges.push(structuredClone(present(request.snapshot.charges[0]))); }],
    ["duplicate authority IDs", (request): void => { request.snapshot.authorityGrants.push(structuredClone(present(request.snapshot.authorityGrants[0]))); }],
  ];
  it.each(badOpenInputs)("refuses %s", async (_label, change): Promise<void> => {
    const request = syntheticRequest();
    change(request);
    const store = new PkStore();
    await expect(openCloseoutCase(store.client, JSON.stringify(request), ACTOR, "open-1")).rejects.toThrow();
    expect(store.reads).toEqual([]);
  });

  it("restricts the runtime bootstrap actor and does not derive actors from request data", async (): Promise<void> => {
    const store = new PkStore();
    await expect(openCloseoutCase(store.client, serialize(syntheticRequest()), "other-user", "open-1")).rejects.toThrow(/approved synthetic bootstrap/);
    expect(store.reads).toEqual([]);
  });

  it("enforces the independent UTF-8 cap and strict JSON shape without truncating", async (): Promise<void> => {
    const store = new PkStore();
    const request = syntheticRequest();
    present(request.snapshot.charges[0]).reason = "é".repeat(MAX_PAYLOAD_BYTES / 2);
    const json = JSON.stringify(request);
    expect(json.length).toBeLessThan(MAX_PAYLOAD_BYTES);
    expect(Buffer.byteLength(json, "utf8")).toBeGreaterThan(MAX_PAYLOAD_BYTES);
    await expect(openCloseoutCase(store.client, json, ACTOR, "cap-1")).rejects.toThrow(/256 KiB/);
    await expect(openCloseoutCase(store.client, '{"snapshot":', ACTOR, "bad-1")).rejects.toThrow(/strict/);
    await expect(openCloseoutCase(store.client, JSON.stringify({ ...syntheticRequest(), unknown: true }), ACTOR, "bad-2")).rejects.toThrow(/strict/);
  });
});

describe("C0 supported charge choice", (): void => {
  it("uses the unchanged native account, updates the loaded root once and returns one complete batch", async (): Promise<void> => {
    const state = await opened();
    const requestBefore = structuredClone(state.request);
    const jsonBefore = state.snapshot.requestJson;
    const edits = await choose(state);
    expect(edits).toHaveLength(state.edits.length);
    const update = rootUpdate(edits);
    expect(update.obj).toBe(state.root);
    expect(update.properties).toMatchObject({ revision: "2", updatedBy: ACTOR });
    expect(Object.keys(update.properties).sort()).toEqual(["accountantIds", "currentReviewId", "inputHash", "managerIds", "projectionVersion", "queueAttentionKind", "queueNearestInternalTargetAtIso", "queueNearestLegalDueDate", "queueNextAssigneePartyId", "queueNextRequirementKey", "queueNextResponsibleRole", "queueSummaryJson", "queueSummaryVersion", "reviewClock", "revision", "updatedAt", "updatedBy"]);
    expect(edits.filter((edit): boolean => edit.type === "updateObject" && edit.obj.$apiName === "DcCloseoutCase")).toHaveLength(1);
    const expectedRequest = structuredClone(state.request);
    expectedRequest.snapshot.revision = 2;
    const repair = present(expectedRequest.snapshot.charges.find((item): boolean => item.itemId === "repair-250"));
    repair.chosenAmountCents = 20000;
    repair.reason = REASON;
    const expectedReview = nativeReview(expectedRequest);
    expect(snapshotCreate(edits).properties.requestJson).toBe(serialize(expectedRequest));
    expect(parseReview(present(snapshotCreate(edits).properties.reviewJson))).toEqual(expectedReview);
    expect(expectedReview.result.account.knownChosenDeductionsCents).toBe(20000);
    expect(expectedReview.result.account.finalRefundCents).toBeNull();
    expect(expectedReview.result.outcomes.depositComplete).toBe(false);
    expect(expectedReview.result.outcomes.overallCaseComplete).toBe(false);
    expect(state.request).toEqual(requestBefore);
    expect(state.snapshot.requestJson).toBe(jsonBefore);
    expect(state.root.revision).toBe("1");
    expect(receiptCreate(edits).properties).toMatchObject({ commandKind: CHOOSE_COMMAND, previousRevision: "1", caseRevision: "2", resultCode: "APPLIED" });
    expect(chargeUpdates(edits)).toHaveLength(3);
    chargeUpdates(edits).forEach((projection): void => {
      expect(Object.keys(projection.obj).sort()).toEqual(["$apiName", "$primaryKey"]);
      expect(projection.properties.caseRevision).toBe("2");
      expect(projection.properties.readerIds).toEqual([ACTOR]);
    });
    // Projections are now consistency-checked for safe create/update classification;
    // the exact core result above proves they are not an alternate financial input.
    expect(state.store.reads.some((read): boolean => read.startsWith("DcChargeItem/"))).toBe(true);
  });

  it("zero waives only the supported tenant charge and preserves owner exclusion", async (): Promise<void> => {
    const state = await opened();
    const edits = await choose(state, "waive", "0");
    const request = from_json("ReviewRequest", present(snapshotCreate(edits).properties.requestJson));
    expect(request.snapshot.charges.find((item): boolean => item.itemId === "repair-250")).toMatchObject({ chosenAmountCents: 0, choiceState: "WAIVED" });
    expect(request.snapshot.charges.find((item): boolean => item.itemId === "paint-800")).toMatchObject({ chosenAmountCents: 0, choiceState: "NOT_APPLICABLE" });
  });

  it.each(["paint-800", "additional-item", "unknown-item"])("refuses unsupported/owner item %s, even with an owner approval record", async (itemId): Promise<void> => {
    const request = syntheticRequest();
    request.snapshot.priorApprovals.push({ approvalId: "owner-approval", decision: "APPROVED", actionKind: "CHOOSE_OR_WAIVE_CHARGE", targetVersionId: "owner-paint", payloadFingerprint: "not-authority", authorityVersion: "owner-v1", actorPartyId: "demo-resident", decidedAt: "2026-09-16T00:00:00Z", revokedApprovalId: null });
    const state = await opened(request);
    await expect(choose(state, "choose-1", "0", "1", REASON, undefined, itemId)).rejects.toThrow(/supported tenant charge/);
  });

  it("rejects a native supported item still requiring evidence review", async (): Promise<void> => {
    const request = syntheticRequest();
    present(request.snapshot.charges[0]).reviewRequired = true;
    const state = await opened(request);
    await expect(choose(state)).rejects.toThrow(/supported tenant charge/);
  });

  it("keeps a calculated final refund proposed, not executed or complete", async (): Promise<void> => {
    const request = syntheticRequest();
    const extra = present(request.snapshot.charges.find((item): boolean => item.itemId === "additional-item"));
    Object.assign(extra, { acceptedAllocation: "OWNER", allowabilityState: "DISALLOWED", supportedAmountCents: 0, chosenAmountCents: 0, choiceState: "NOT_APPLICABLE", unresolvedQuestionIds: [], reviewRequired: false });
    request.snapshot.questions = [];
    const state = await opened(request);
    const edits = await choose(state);
    const stored = from_json("ReviewRequest", present(snapshotCreate(edits).properties.requestJson));
    const review = parseReview(present(snapshotCreate(edits).properties.reviewJson));
    expect(review.result.account.finalRefundCents).toBe(180000);
    expect(review.result.outcomes.depositComplete).toBe(false);
    expect(review.result.outcomes.overallCaseComplete).toBe(false);
    expect(stored.snapshot.moneyEvents).toEqual([]);
    expect(stored.snapshot.executionEvents).toEqual([]);
    expect(stored.snapshot.priorRequests).toEqual([]);
    expect(stored.snapshot.priorStatements).toEqual([]);
    expect(stored.snapshot.priorApprovals).toEqual([]);
  });

  it.each(["-1", "1.0", "01", "+1", "1e3", "9223372036854775808", "9007199254740992", "", " 1"])("rejects invalid/out-of-native-range Long %s", async (amount): Promise<void> => {
    await expect(choose(await opened(), "bad-long", amount)).rejects.toThrow(/Long|integer range/);
  });

  it.each(["0", "-1", "1.5", "9007199254740992"])("rejects invalid expected revision %s", async (revision): Promise<void> => {
    await expect(choose(await opened(), "bad-revision", "20000", revision)).rejects.toThrow(/Long|integer range/);
  });

  it("compares expected revision and accepted support bounds before producing edits", async (): Promise<void> => {
    const state = await opened();
    await expect(choose(state, "stale", "20000", "2")).rejects.toThrow(/revision changed/);
    await expect(choose(state, "too-high", "25001")).rejects.toThrow(/supported tenant charge/);
  });

  it.each(["", "   ", "é".repeat(1001)])("refuses empty or byte-oversized reasons", async (reason): Promise<void> => {
    await expect(choose(await opened(), "bad-reason", "20000", "1", reason)).rejects.toThrow(/reason/);
  });

  it.each([-1, 3001, 0.5])("rejects invalid sandbox delay %s", async (delay): Promise<void> => {
    await expect(choose(await opened(), "bad-delay", "20000", "1", REASON, delay)).rejects.toThrow(/delay/);
  });

  it("stable review/receipt keys include command while projections use only case/item", async (): Promise<void> => {
    const state = await opened();
    const a = await choose(state, "choose-a");
    const b = await choose(state, "choose-b");
    expect(snapshotCreate(a).properties.reviewId).toBe(reviewIdFor(COMPANY_ID, state.root.caseId, "2", "choose-a"));
    expect(snapshotCreate(a).properties.reviewId).not.toBe(snapshotCreate(b).properties.reviewId);
    expect(receiptCreate(a).properties.eventId).toBe(receiptIdFor(COMPANY_ID, state.root.caseId, "choose-a"));
    expect(receiptCreate(a).properties.eventId).not.toBe(receiptCreate(b).properties.eventId);
    expect(chargeUpdates(a).map((edit) => edit.obj)).toEqual(chargeUpdates(b).map((edit) => edit.obj));
  });

  it("allows two unit invocations to carry the same observed root through the delay without hiding contenders", async (): Promise<void> => {
    const state = await opened();
    const pendingA = choose(state, "overlap-a", "20000", "1", REASON, 3000);
    const pendingB = choose(state, "overlap-b", "21000", "1", REASON, 3000);
    await vi.advanceTimersByTimeAsync(3000);
    const [a, b] = await Promise.all([pendingA, pendingB]);
    expect(rootUpdate(a).obj).toBe(state.root);
    expect(rootUpdate(b).obj).toBe(state.root);
    expect(snapshotCreate(a).properties.reviewId).not.toBe(snapshotCreate(b).properties.reviewId);
    // No assertion here about real Action conflict detection or atomic persistence.
  });
});

describe("C0 idempotency and authorization", (): void => {
  it("replays before revision comparison even after later commands; hash ignores delay and generated time", async (): Promise<void> => {
    const state = await opened();
    const first = await choose(state);
    const second = await choose(state, "choose-1", "20000", "1", REASON, 0);
    expect(receiptCreate(first).properties.payloadHash).toBe(receiptCreate(second).properties.payloadHash);
    const afterFirst = nextInputs(state, first);
    expect(await choose(afterFirst, "choose-1", "20000", "1", REASON, 3000)).toEqual([]);
    vi.setSystemTime(new Date("2026-09-18T12:00:00Z"));
    const laterEdits = await choose(afterFirst, "choose-later", "19000", "2");
    const afterLater = nextInputs(afterFirst, laterEdits);
    expect(await choose(afterLater, "choose-1", "20000", "1")).toEqual([]);
    expect(await openCloseoutCase(afterLater.store.client, serialize(state.request), ACTOR, "open-1")).toEqual([]);
  });

  it.each(["amount", "reason", "expectedRevision", "item"])("same ID with changed %s conflicts", async (field): Promise<void> => {
    const state = await opened();
    const later = nextInputs(state, await choose(state));
    await expect(choose(later, "choose-1", field === "amount" ? "19000" : "20000",
      field === "expectedRevision" ? "2" : "1", field === "reason" ? "New reason" : REASON,
      undefined, field === "item" ? "paint-800" : "repair-250")).rejects.toThrow(/different payload/);
  });

  it("cannot reuse an open command ID for a charge command", async (): Promise<void> => {
    await expect(choose(await opened(), "open-1")).rejects.toThrow(/different payload/);
  });

  it("checks real access before looking up receipts and never allows accountant/owner/admin alone", async (): Promise<void> => {
    const state = await opened();
    const later = nextInputs(state, await choose(state));
    const noManager = createMockOsdkObject(DcCloseoutCase, { ...later.root, managerIds: [] });
    const readsBefore = later.store.reads.length;
    await expect(choose({ ...later, root: noManager })).rejects.toThrow(/manager access/);
    expect(later.store.reads).toHaveLength(readsBefore);
    await expect(chooseCharge(later.store.client, later.root, "other-user", "choose-1", "1", "repair-250", "20000", REASON)).rejects.toThrow(/manager access/);
  });

  it.each(["revoked", "expired", "future", "limit", "no-role", "no-action", "party-expired", "party-future", "no-evidence"])("requires current accepted authority: %s", async (kind): Promise<void> => {
    const request = syntheticRequest();
    const grant = present(request.snapshot.authorityGrants.find((entry): boolean => entry.partyId === "demo-manager"));
    const party = present(request.snapshot.parties.find((entry): boolean => entry.partyId === "demo-manager"));
    if (kind === "revoked") grant.revoked = true;
    if (kind === "expired") grant.effectiveUntil = "2026-09-17T12:00:00Z";
    if (kind === "future") grant.effectiveFrom = "2026-09-18T00:00:00Z";
    if (kind === "limit") grant.amountLimitCents = 19999;
    if (kind === "no-role") { party.roles = ["ACCOUNTANT"]; request.snapshot.parties.push({ ...party, partyId: "ungranted-manager", roles: ["MANAGER"] }); }
    if (kind === "no-action") grant.allowedActionKinds = ["APPROVE_EXACT_VERSION"];
    if (kind === "party-expired") party.effectiveUntil = "2026-09-16";
    if (kind === "party-future") party.effectiveFrom = "2026-09-18";
    if (kind === "no-evidence") party.evidenceIds = [];
    const state = await opened(request);
    // A root permission alone is deliberately insufficient to authorize the command.
    const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, managerIds: [ACTOR] });
    await expect(choose({ ...state, root })).rejects.toThrow(/current manager authority/);
  });

  it("uses actual server time for authority, not the old review clock, also on receipt replay", async (): Promise<void> => {
    const request = syntheticRequest();
    present(request.snapshot.authorityGrants.find((entry): boolean => entry.partyId === "demo-manager")).effectiveUntil = "2026-09-18T00:00:00Z";
    const state = await opened(request);
    const next = nextInputs(state, await choose(state));
    vi.setSystemTime(new Date("2026-09-18T00:00:00Z"));
    await expect(choose(next)).rejects.toThrow(/current manager authority/);
    expect(next.root.reviewClock).toBe("2026-09-16T12:00:00Z");
  });

  it("rechecks grant expiry after the synthetic delay", async (): Promise<void> => {
    const request = syntheticRequest();
    present(request.snapshot.authorityGrants.find((entry): boolean => entry.partyId === "demo-manager")).effectiveUntil = "2026-09-17T12:00:01Z";
    const state = await opened(request);
    const result = expect(choose(state, "delayed", "20000", "1", REASON, 3000)).rejects.toThrow(/current manager authority/);
    await vi.advanceTimersByTimeAsync(3000);
    await result;
  });

  it("reads the exact canonical envelope without rewriting the review clock or exposing an actor argument", async (): Promise<void> => {
    const state = await opened();
    expect(await getCloseoutReview(state.store.client, state.root)).toBe(state.snapshot.reviewJson);
    const next = nextInputs(state, await choose(state));
    expect(await getCloseoutReview(next.store.client, next.root)).toBe(next.snapshot.reviewJson);
    expect(next.root.reviewClock).toBe(state.root.reviewClock);
  });
});
