import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DcCloseoutCase, DcExecutionEvent, DcReviewSnapshot } from "@ontology/sdk";
import { createMockOsdkObject } from "@osdk/unit-testing";
import openCloseoutCase from "../../functions/openCloseoutCase.js";
import { chooseCharge } from "../phase_c/commands.js";
import getCloseoutReview from "../../functions/getCloseoutReview.js";
import { from_json } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import { BOOTSTRAP_ACTOR_ID as ACTOR, COMPANY_ID, MAX_PAYLOAD_BYTES, receiptIdFor } from "../phase_c/types.js";
import { optionalObject } from "../phase_c/storage.js";
import { checkedLong, hasAuthority, nativeReview, serialize } from "../phase_c/validation.js";
import {
  apiError, nextInputs, opened, PkStore, present, syntheticRequest, type TestState,
} from "./phaseCTestSupport.js";

const NOW = "2026-09-17T12:00:00Z";
const REASON = "Synthetic test choice";

function choose(state: TestState): ReturnType<typeof chooseCharge> {
  return chooseCharge(state.store.client, state.root, ACTOR, "choose-1", "1", "repair-250", "20000", REASON);
}

beforeEach((): void => { vi.useFakeTimers(); vi.setSystemTime(new Date(NOW)); });
afterEach((): void => { vi.useRealTimers(); });

describe("stored snapshot and root consistency", (): void => {
  const rootPatches: [string, Partial<DcCloseoutCase.Props>][] = [
    ["environment", { environmentId: "LIVE" }],
    ["company", { managementCompanyId: "different-company" }],
    ["tenancy", { tenancyId: "other-tenancy" }],
    ["home", { homeId: "other-home" }],
    ["revision", { revision: "2" }],
    ["noncanonical revision", { revision: "01" }],
    ["missing revision", { revision: undefined }],
    ["hash", { inputHash: "a".repeat(64) }],
    ["missing hash", { inputHash: undefined }],
    ["missing current review", { currentReviewId: undefined }],
    ["review clock", { reviewClock: "2026-09-16T12:00:00.000001Z" }],
    ["missing readers", { readerIds: undefined }],
    ["empty readers", { readerIds: [] }],
    ["extra readers", { readerIds: [ACTOR, "other-principal"] }],
    ["foreign manager", { managerIds: ["other-principal"] }],
    ["missing administrators", { adminIds: undefined }],
    ["missing update time", { updatedAt: undefined }],
  ];
  it.each(rootPatches)("fails closed for root %s mismatch", async (_name, patch): Promise<void> => {
    const state = await opened();
    const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, ...patch });
    await expect(getCloseoutReview(state.store.client, root)).rejects.toThrow();
    await expect(choose({ ...state, root })).rejects.toThrow();
  });

  const snapshotPatches: [string, Partial<DcReviewSnapshot.Props>][] = [
    ["case", { caseId: "other-case" }],
    ["company", { managementCompanyId: "other-company" }],
    ["environment", { environmentId: "LIVE" }],
    ["revision", { caseRevision: "2" }],
    ["missing revision", { caseRevision: undefined }],
    ["input hash", { inputHash: "b".repeat(64) }],
    ["result hash", { resultHash: "b".repeat(64) }],
    ["missing result hash", { resultHash: undefined }],
    ["missing request", { requestJson: undefined }],
    ["missing review", { reviewJson: undefined }],
    ["foreign readers", { readerIds: ["other-principal"] }],
    ["missing readers", { readerIds: undefined }],
    ["missing creator", { createdBy: undefined }],
    ["missing creation time", { createdAt: undefined }],
    ["malformed request", { requestJson: "{}" }],
    ["malformed review", { reviewJson: "{}" }],
    ["oversized request", { requestJson: "x".repeat(MAX_PAYLOAD_BYTES + 1) }],
    ["oversized review", { reviewJson: "x".repeat(MAX_PAYLOAD_BYTES + 1) }],
  ];
  it.each(snapshotPatches)("fails closed for snapshot %s mismatch", async (_name, patch): Promise<void> => {
    const state = await opened();
    state.store.put(createMockOsdkObject(DcReviewSnapshot, { ...state.snapshot, ...patch }));
    await expect(getCloseoutReview(state.store.client, state.root)).rejects.toThrow();
    await expect(choose(state)).rejects.toThrow();
  });

  it("rejects a self-consistent forged review hash using native baseline equality", async (): Promise<void> => {
    const state = await opened();
    const forged = from_json("ReviewEnvelope", present(state.snapshot.reviewJson));
    forged.result.account.knownChosenDeductionsCents = 999;
    state.store.put(createMockOsdkObject(DcReviewSnapshot, {
      ...state.snapshot, reviewJson: serialize(forged), resultHash: fingerprint(forged),
    }));
    await expect(getCloseoutReview(state.store.client, state.root)).rejects.toThrow(/content hash/);
    await expect(choose(state)).rejects.toThrow(/content hash/);
  });

  it("rejects changed request content even if the JSON parses and revision stays the same", async (): Promise<void> => {
    const state = await opened();
    const forged = from_json("ReviewRequest", present(state.snapshot.requestJson));
    present(forged.snapshot.charges[0]).reason = "Changed outside the command";
    state.store.put(createMockOsdkObject(DcReviewSnapshot, { ...state.snapshot, requestJson: serialize(forged) }));
    await expect(getCloseoutReview(state.store.client, state.root)).rejects.toThrow(/content hash/);
  });

  it("checks request identities independently of root/child columns", async (): Promise<void> => {
    const state = await opened();
    const forged = from_json("ReviewRequest", present(state.snapshot.requestJson));
    forged.snapshot.homeId = "another-home";
    const review = nativeReview(forged);
    const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, inputHash: review.metadata.inputHash });
    state.store.put(createMockOsdkObject(DcReviewSnapshot, {
      ...state.snapshot, inputHash: review.metadata.inputHash, requestJson: serialize(forged),
      reviewJson: serialize(review), resultHash: fingerprint(review),
    }));
    await expect(getCloseoutReview(state.store.client, root)).rejects.toThrow(/metadata does not match/);
  });

  it("does not accept noncanonical stored JSON representations", async (): Promise<void> => {
    const state = await opened();
    state.store.put(createMockOsdkObject(DcReviewSnapshot, {
      ...state.snapshot, requestJson: `${state.snapshot.requestJson}\n`,
    }));
    await expect(getCloseoutReview(state.store.client, state.root)).rejects.toThrow(/content hash/);
  });

  it("accepts equivalent timestamp transport formatting but not differing microseconds", async (): Promise<void> => {
    const state = await opened();
    const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, reviewClock: "2026-09-16T12:00:00.000Z" });
    expect(await getCloseoutReview(state.store.client, root)).toBe(state.snapshot.reviewJson);
  });
});

describe("receipt consistency and PK lookup failures", (): void => {
  const receiptPatches: [string, Partial<DcExecutionEvent.Props>][] = [
    ["foreign case", { caseId: "another-case" }],
    ["foreign company", { managementCompanyId: "another-company" }],
    ["foreign environment", { environmentId: "LIVE" }],
    ["missing readers", { readerIds: undefined }],
    ["different actor", { actorId: "other-principal" }],
    ["missing payload hash", { payloadHash: undefined }],
    ["previous revision", { previousRevision: "0" }],
    ["result revision", { caseRevision: "3" }],
    ["review reference", { reviewId: "other-review" }],
    ["result code", { resultCode: "FAILED" }],
    ["missing result JSON", { resultJson: undefined }],
    ["missing occurrence time", { occurredAt: undefined }],
  ];
  it.each(receiptPatches)("does not silently replay a receipt with %s", async (_name, patch): Promise<void> => {
    const state = await opened();
    const next = nextInputs(state, await choose(state));
    state.store.put(createMockOsdkObject(DcExecutionEvent, { ...next.receipt, ...patch }));
    await expect(choose(next)).rejects.toThrow();
  });

  const errors: [string, () => Error][] = [
    ["permission denied", (): Error => apiError("PermissionDenied", "PERMISSION_DENIED", 403)],
    ["timeout", (): Error => new Error("Synthetic timeout")],
    ["generic 404", (): Error => Object.assign(new Error("Not found"), { statusCode: 404 })],
    ["wrong error name", (): Error => apiError("ObjectTypeNotFound", "NOT_FOUND", 404)],
    ["wrong error code", (): Error => apiError("ObjectNotFound", "PERMISSION_DENIED", 404)],
    ["wrong status", (): Error => apiError("ObjectNotFound", "NOT_FOUND", 403)],
  ];
  it.each(errors)("propagates %s for every optional lookup, never treating it as absence", async (_name, makeError): Promise<void> => {
    const request = syntheticRequest();
    const rootStore = new PkStore();
    const error = makeError();
    rootStore.fail("DcCloseoutCase", request.snapshot.caseId, error);
    await expect(openCloseoutCase(rootStore.client, serialize(request), ACTOR, "open-1")).rejects.toBe(error);
    const eventStore = new PkStore();
    eventStore.fail("DcExecutionEvent", receiptIdFor(COMPANY_ID, request.snapshot.caseId, "open-1"), error);
    await expect(openCloseoutCase(eventStore.client, serialize(request), ACTOR, "open-1")).rejects.toBe(error);
    const state = await opened();
    state.store.fail("DcExecutionEvent", receiptIdFor(COMPANY_ID, state.root.caseId, "choose-1"), error);
    await expect(choose(state)).rejects.toBe(error);
  });

  it("only treats the specifically documented ObjectNotFound error as optional", async (): Promise<void> => {
    expect(await optionalObject(Promise.reject(apiError("ObjectNotFound", "NOT_FOUND", 404)))).toBeUndefined();
    await expect(optionalObject(Promise.reject({ errorName: "ObjectNotFound", errorCode: "NOT_FOUND", statusCode: 404 }))).rejects.toEqual({ errorName: "ObjectNotFound", errorCode: "NOT_FOUND", statusCode: 404 });
  });

  it.each(["ObjectNotFound", "PermissionDenied", "Timeout"])("never swallows current snapshot lookup %s", async (name): Promise<void> => {
    const state = await opened();
    const error = name === "ObjectNotFound" ? apiError(name, "NOT_FOUND", 404) : new Error(name);
    state.store.fail("DcReviewSnapshot", present(state.root.currentReviewId), error);
    await expect(getCloseoutReview(state.store.client, state.root)).rejects.toBe(error);
    await expect(choose(state)).rejects.toBe(error);
  });
});

describe("authority and exact arithmetic boundaries", (): void => {
  it("compares timestamp grants to microsecond precision, with exclusive expiry", (): void => {
    const request = syntheticRequest();
    const grant = present(request.snapshot.authorityGrants.find((entry): boolean => entry.partyId === "demo-manager"));
    grant.effectiveFrom = "2026-09-17T12:00:00.000001Z";
    grant.effectiveUntil = "2026-09-17T12:00:00.000003Z";
    const canChoose = (now: string): boolean => hasAuthority(request, ACTOR, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", 20000, now);
    expect(canChoose("2026-09-17T12:00:00Z")).toBe(false);
    expect(canChoose("2026-09-17T12:00:00.000001Z")).toBe(true);
    expect(canChoose("2026-09-17T12:00:00.000002Z")).toBe(true);
    expect(canChoose("2026-09-17T12:00:00.000003Z")).toBe(false);
  });

  it("uses the configured local calendar for inclusive party effective dates", (): void => {
    const request = syntheticRequest();
    const party = present(request.snapshot.parties.find((entry): boolean => entry.partyId === "demo-manager"));
    party.effectiveFrom = "2026-09-17";
    party.effectiveUntil = "2026-09-17";
    expect(hasAuthority(request, ACTOR, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", 1, "2026-09-17T03:59:59Z")).toBe(false);
    expect(hasAuthority(request, ACTOR, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", 1, "2026-09-17T04:00:00Z")).toBe(true);
    expect(hasAuthority(request, ACTOR, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", 1, "2026-09-18T03:59:59Z")).toBe(true);
    expect(hasAuthority(request, ACTOR, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", 1, "2026-09-18T04:00:00Z")).toBe(false);
  });

  it("never treats a null amount limit as unbounded authority", async (): Promise<void> => {
    const request = syntheticRequest();
    present(request.snapshot.authorityGrants.find((entry): boolean => entry.partyId === "demo-manager")).amountLimitCents = null;
    const state = await opened(request);
    // Non-financial fact authority still projects coarse manager membership in full C.
    expect(state.root.managerIds).toEqual([ACTOR]);
    expect(hasAuthority(request, ACTOR, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", 0, NOW)).toBe(false);
    await expect(choose(state)).rejects.toThrow(/current manager authority/);
  });

  it("accepts only exact native integers within the Long range", (): void => {
    expect(checkedLong("9007199254740991", "Maximum")).toBe(Number.MAX_SAFE_INTEGER);
    expect(checkedLong("0", "Zero")).toBe(0);
    expect((): number => checkedLong(undefined, "Absent")).toThrow();
    expect((): number => checkedLong("9223372036854775807", "Long max outside native range")).toThrow();
    expect((): number => checkedLong("9007199254740992", "Too large")).toThrow();
  });
});
