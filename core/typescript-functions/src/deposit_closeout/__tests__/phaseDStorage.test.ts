import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DcActionRequest, DcApproval, DcCloseoutCase, DcExecutionEvent, DcReviewSnapshot, DcStatementVersion } from "@ontology/sdk";
import { createMockOsdkObject } from "@osdk/unit-testing";
import initializeCloseoutWorkflow from "../../functions/initializeCloseoutWorkflow.js";
import getCloseoutReview from "../../functions/getCloseoutReview.js";
import getCloseoutWorkflow from "../../functions/getCloseoutWorkflow.js";
import prepareCloseoutStatement from "../../functions/prepareCloseoutStatement.js";
import requestCloseoutOperation from "../../functions/requestCloseoutOperation.js";
import recheckCloseoutCase from "../../functions/recheckCloseoutCase.js";
import { canonical_json, from_json } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import { parseWorkflowReview } from "../lifecycle/codec.js";
import { loadCurrentReview } from "../phase_c/storage.js";
import { loadProjections } from "../phase_c/projections.js";
import { nativeReview, serialize } from "../phase_c/validation.js";
import { apiError, nextInputs, opened, present, rootUpdate, type TestState } from "./phaseCTestSupport.js";
import { ACTOR, NOW, WHY, act, approved, current, initialized, requested, storageRequest, workflow } from "./phaseDStorageSupport.js";

beforeEach((): void => { vi.useFakeTimers(); vi.setSystemTime(new Date(NOW)); });
afterEach((): void => { vi.useRealTimers(); });

function replaceSnapshot(state: TestState, patch: Partial<DcReviewSnapshot.Props>): void {
  state.store.put(createMockOsdkObject(DcReviewSnapshot, { ...state.snapshot, ...patch }));
}
async function check(state: TestState): Promise<unknown> { return loadCurrentReview(state.store.client, state.root); }

describe("v2 sidecar boundary and native compatibility", (): void => {
  it("reads legacy JSON exactly, requires explicit initialization and preserves historical v1 snapshots", async (): Promise<void> => {
    const old = await opened(storageRequest());
    const oldJson = await getCloseoutReview(old.store.client, old.root);
    await expect(getCloseoutWorkflow(old.store.client, old.root.caseId)).rejects.toThrow(/Initialize/);
    const next = await act(old, initializeCloseoutWorkflow, {}, "init");
    expect(next.root.workflowVersion).toBe("2");
    expect(next.root.revision).toBe("2");
    expect(rootUpdate(next.edits).obj).toBe(old.root);
    expect(next.edits.filter((edit): boolean => edit.type === "updateObject" && edit.obj.$apiName === "DcCloseoutCase")).toHaveLength(1);
    expect(next.edits.filter((edit): boolean => edit.type === "createObject" && edit.obj.apiName === "DcReviewSnapshot")).toHaveLength(1);
    expect(next.edits.some((edit): boolean => edit.type === "updateObject" && edit.obj.$apiName === "DcReviewSnapshot")).toBe(false);
    expect(await getCloseoutReview(old.store.client, old.root)).toBe(oldJson);
    expect(next.store.data.get(`DcReviewSnapshot/${old.snapshot.reviewId}`)).toBe(old.snapshot);
    expect(await getCloseoutReview(next.store.client, next.root)).toBe(next.snapshot.reviewJson);
    expect(await getCloseoutWorkflow(next.store.client, next.root.caseId)).toBe(next.snapshot.workflowReviewJson);
    expect(from_json("ReviewEnvelope", present(next.snapshot.reviewJson))).toEqual(nativeReview(current(next)));
    expect(() => from_json("ReviewEnvelope", present(next.snapshot.workflowReviewJson))).toThrow();
    const v2 = parseWorkflowReview(present(next.snapshot.workflowReviewJson));
    expect(v2.metadata).toMatchObject({ schemaVersion: "1.1.0", workflowSchemaVersion: "2.0.0", baseCaseRevision: 2 });
    expect(next.snapshot.workflowStateHash).toBe(fingerprint(workflow(next)));
    expect(next.snapshot.workflowReviewHash).toBe(fingerprint(v2));
    expect(next.snapshot.workflowStateJson).toBe(canonical_json(workflow(next)));
    expect(next.snapshot.workflowReviewJson).toBe(canonical_json(v2));
  });
  it("validates at recorded createdAt rather than reinterpreting an old review after grant expiry", async (): Promise<void> => {
    const input = storageRequest();
    input.snapshot.authorityGrants.forEach((grant): void => { grant.effectiveUntil = "2026-09-19T00:00:00Z"; });
    const state = await approved(await initialized(input));
    const original = state.snapshot.workflowReviewJson;
    vi.setSystemTime(new Date("2026-09-20T00:00:00Z"));
    expect(await getCloseoutWorkflow(state.store.client, state.root.caseId)).toBe(original);
    await loadProjections(state.store.client, await loadCurrentReview(state.store.client, state.root), state.root.projectionVersion);
    await expect(requestCloseoutOperation(state.store.client, state.root.caseId, ACTOR, "expired", present(state.root.revision),
      serialize({ approvalId: workflow(state).approvals[0]!.approvalId }))).rejects.toThrow(/authority/);
  });
  it.each(["1", "3", "02", "-1", "9007199254740992", "garbage"])("rejects unknown stored workflow version %s", async (version): Promise<void> => {
    const state = await initialized();
    const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, workflowVersion: version });
    await expect(loadCurrentReview(state.store.client, root)).rejects.toThrow(/version/);
  });
  it.each([undefined, "0"])("never interprets sidecars as legacy for root version %s", async (version): Promise<void> => {
    const state = await initialized();
    const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, workflowVersion: version });
    await expect(loadCurrentReview(state.store.client, root)).rejects.toThrow(/V0/);
  });
  it.each(["workflowStateJson", "workflowStateHash", "workflowReviewJson", "workflowReviewHash"] as const)("rejects missing %s", async (key): Promise<void> => {
    const state = await initialized();
    replaceSnapshot(state, { [key]: undefined });
    await expect(check(state)).rejects.toThrow();
  });
  it.each(["workflowStateHash", "workflowReviewHash"] as const)("rejects corrupt %s", async (key): Promise<void> => {
    const state = await initialized();
    replaceSnapshot(state, { [key]: "a".repeat(64) });
    await expect(check(state)).rejects.toThrow(/hash/);
  });
  it.each(["workflowStateJson", "workflowReviewJson"] as const)("rejects noncanonical %s even though the semantic hash still matches", async (key): Promise<void> => {
    const state = await initialized();
    replaceSnapshot(state, { [key]: ` ${state.snapshot[key]}` });
    await expect(check(state)).rejects.toThrow(/canonical/);
  });
  it("binds the v2 review to native revision/hash, not merely its own self-consistent hash", async (): Promise<void> => {
    const state = await initialized();
    const review = parseWorkflowReview(present(state.snapshot.workflowReviewJson));
    review.metadata.baseCaseRevision += 1;
    replaceSnapshot(state, { workflowReviewJson: serialize(review), workflowReviewHash: fingerprint(review) });
    await expect(check(state)).rejects.toThrow(/canonical review/);
  });
  it("binds authority evaluation to snapshot createdAt", async (): Promise<void> => {
    const state = await initialized();
    const review = parseWorkflowReview(present(state.snapshot.workflowReviewJson));
    review.metadata.authorityEvaluatedAt = "2026-09-18T12:00:01Z";
    replaceSnapshot(state, { workflowReviewJson: serialize(review), workflowReviewHash: fingerprint(review) });
    await expect(check(state)).rejects.toThrow(/recorded snapshot/);
  });
  it("requires a matching current statement pointer", async (): Promise<void> => {
    const state = await act(await initialized(), prepareCloseoutStatement, { kind: "FINAL", supersedesId: null, reason: WHY }, "prepare");
    const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, currentStatementId: undefined });
    await expect(loadCurrentReview(state.store.client, root)).rejects.toThrow(/pointer/);
  });
  it("rejects even a lone current statement pointer on a legacy root", async (): Promise<void> => {
    const state = await opened(storageRequest());
    const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, currentStatementId: "dc-statement:unexpected" });
    await expect(loadCurrentReview(state.store.client, root)).rejects.toThrow(/legacy/);
  });
});

describe("bounded scope projections and immutable contents", (): void => {
  it("initialization refuses unexpected future projections instead of adopting them", async (): Promise<void> => {
    const state = await opened(storageRequest());
    state.store.put(createMockOsdkObject(DcApproval, { approvalId: "unexpected", caseId: state.root.caseId }));
    await expect(initializeCloseoutWorkflow(state.store.client, state.root.caseId, ACTOR, "init", "1", "{}")).rejects.toThrow(/unexpected/);
  });
  it.each(["DcStatementVersion", "DcApproval", "DcActionRequest", "DcExecutionEvent"])("propagates required %s case lookup failures", async (type): Promise<void> => {
    const state = await initialized();
    const denied = apiError("PermissionDenied", "PERMISSION_DENIED", 403);
    state.store.fail(type, `case:${state.root.caseId}`, denied);
    await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", "2")).rejects.toBe(denied);
  });
  it.each(["statement", "approval", "request", "event"])("rejects a next page of %s projections rather than silently truncating", async (type): Promise<void> => {
    const state = await initialized();
    for (let index = 0; index <= 1000; index += 1) {
      const caseId = state.root.caseId;
      if (type === "statement") state.store.put(createMockOsdkObject(DcStatementVersion, { statementId: `extra-${index}`, caseId }));
      if (type === "approval") state.store.put(createMockOsdkObject(DcApproval, { approvalId: `extra-${index}`, caseId }));
      if (type === "request") state.store.put(createMockOsdkObject(DcActionRequest, { requestId: `extra-${index}`, caseId }));
      if (type === "event") state.store.put(createMockOsdkObject(DcExecutionEvent, { eventId: `extra-${index}`, caseId }));
    }
    await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", "2")).rejects.toThrow(/bound/);
  });
  it("validates frozen request JSON and refuses absent projections rather than recreating them", async (): Promise<void> => {
    const state = await requested(await initialized());
    const id = workflow(state).requests[0]!.requestId;
    const object = state.store.data.get(`DcActionRequest/${id}`);
    if (object?.$apiName !== "DcActionRequest") throw new Error("Missing request projection");
    state.store.put(createMockOsdkObject(DcActionRequest, { ...object, requestJson: "{}" }));
    await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "corrupt", present(state.root.revision))).rejects.toThrow(/requestJson/);
    state.store.data.delete(`DcActionRequest/${id}`);
    await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "absent", present(state.root.revision))).rejects.toThrow(/missing/);
  });
  it("scopes projected approvals to the same company and readers", async (): Promise<void> => {
    const state = await approved(await initialized());
    const object = state.store.data.get(`DcApproval/${workflow(state).approvals[0]!.approvalId}`);
    if (object?.$apiName !== "DcApproval") throw new Error("Missing approval projection");
    state.store.put(createMockOsdkObject(DcApproval, { ...object, managementCompanyId: "other-company" }));
    await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "wrong-company", present(state.root.revision))).rejects.toThrow(/managementCompanyId/);
    state.store.put(createMockOsdkObject(DcApproval, { ...object, readerIds: ["other-principal"] }));
    await expect(recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "wrong-reader", present(state.root.revision))).rejects.toThrow(/readerIds/);
  });
  it("does not update any frozen columns or historical events on a later recheck", async (): Promise<void> => {
    let state = await act(await initialized(), prepareCloseoutStatement, { kind: "FINAL", supersedesId: null, reason: WHY }, "prepare");
    state = await requested(state);
    const initial = workflow(state);
    const edits = await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck", present(state.root.revision));
    edits.forEach((edit): void => {
      if (edit.type !== "updateObject") return;
      expect(edit.obj.$apiName).not.toBe("DcExecutionEvent");
      if (edit.obj.$apiName === "DcStatementVersion") expect(Object.keys(edit.properties).sort()).toEqual(["basisCurrent", "caseRevision", "isCurrent", "issueState"]);
      if (edit.obj.$apiName === "DcApproval") expect(Object.keys(edit.properties).sort()).toEqual(["caseRevision", "validity"]);
      if (edit.obj.$apiName === "DcActionRequest") expect(Object.keys(edit.properties).sort()).toEqual(["caseRevision", "currentAttemptId", "externalReference", "reservationCents", "state"]);
    });
    const keys = edits.filter((edit): boolean => edit.type === "updateObject")
      .map((edit): string => edit.type === "updateObject" ? `${edit.obj.$apiName}/${edit.obj.$primaryKey}` : "");
    expect(new Set(keys).size).toBe(keys.length);
    const next = nextInputs(state, edits);
    expect(workflow(next).statements).toEqual(initial.statements);
    expect(workflow(next).approvals).toEqual(initial.approvals);
    expect(workflow(next).requests).toEqual(initial.requests);
    expect(workflow(next).events).toEqual(initial.events);
    await check(next);
  });
});
