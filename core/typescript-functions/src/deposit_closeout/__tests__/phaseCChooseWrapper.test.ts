import { afterEach, beforeEach, describe, expect, expectTypeOf, it, vi } from "vitest";
import { DcCloseoutCase } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import { createMockOsdkObject } from "@osdk/unit-testing";
import chooseCloseoutCharge from "../../functions/chooseCloseoutCharge.js";
import {
  BOOTSTRAP_ACTOR_ID as ACTOR, caseIdFor, COMPANY_ID, receiptIdFor, type OntologyEdit,
} from "../phase_c/types.js";
import {
  apiError, nextInputs, opened, receiptCreate, rootUpdate, type TestState,
} from "./phaseCTestSupport.js";

const COMMAND_ID = "choose-wrapper";
const REASON = "Synthetic wrapper chooses a reduced supported charge.";

function chooseById(state: TestState, caseId: string = state.root.caseId): Promise<OntologyEdit[]> {
  return chooseCloseoutCharge(state.store.client, caseId, ACTOR, COMMAND_ID,
    "1", "repair-250", "20000", REASON);
}

beforeEach((): void => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date("2026-09-17T12:00:00.000Z"));
});
afterEach((): void => { vi.useRealTimers(); });

// Explicit SDK fixtures only; these tests cannot establish platform atomicity or race handling.
describe("C0 public charge wrapper loads its required root server-side", (): void => {
  it("fetches exactly the supplied ID and retains that loaded instance in the single root update", async (): Promise<void> => {
    expectTypeOf<Parameters<typeof chooseCloseoutCharge>[1]>().toEqualTypeOf<string>();
    const state = await opened();
    const readsBefore = state.store.reads.length;
    const fetchOne = vi.fn((caseId: string): Promise<Osdk.Instance<DcCloseoutCase>> =>
      state.store.client(DcCloseoutCase).fetchOne(caseId));
    const client = new Proxy(state.store.client, {
      apply: (target: Client, _this: unknown, args: unknown[]): unknown => {
        // No optional/filter lookup surface is offered for the required root read.
        if (args[0] === DcCloseoutCase) return { fetchOne };
        return Reflect.apply(target, undefined, args);
      },
    });
    const edits = await chooseCloseoutCharge(client, state.root.caseId, ACTOR, COMMAND_ID,
      "1", "repair-250", "20000", REASON, 0);
    expect(fetchOne).toHaveBeenCalledExactlyOnceWith(state.root.caseId);
    const projectionReads = ["DcChargeItem", "DcEvidenceRecord", "DcMoneyEvent", "DcCaseParty", "DcRequirement"]
      .flatMap((apiName): string[] => [`${apiName}/case:${state.root.caseId}`,
        ...[...state.store.data.values()].filter((row): boolean => row.$apiName === apiName)
          .map((row): string => `${apiName}/${row.$primaryKey}`)]);
    expect(state.store.reads.slice(readsBefore)).toEqual([
      `DcCloseoutCase/${state.root.caseId}`,
      `DcReviewSnapshot/${state.root.currentReviewId}`,
      `DcExecutionEvent/${receiptIdFor(COMPANY_ID, state.root.caseId, COMMAND_ID)}`,
      ...projectionReads,
    ]);
    expect(edits).toHaveLength(state.edits.length);
    expect(edits.filter((edit): boolean => edit.type === "updateObject"
      && edit.obj.$apiName === "DcCloseoutCase")).toHaveLength(1);
    expect(rootUpdate(edits).obj).toBe(state.root);
    expect(rootUpdate(edits).properties).toMatchObject({ revision: "2", updatedBy: ACTOR });
    expect(receiptCreate(edits).properties).toMatchObject({
      actorId: ACTOR, commandId: COMMAND_ID, previousRevision: "1", caseRevision: "2",
    });
    expect(state.root.revision).toBe("1");
  });

  const lookupFailures: [string, () => Error][] = [
    ["ObjectNotFound", (): Error => apiError("ObjectNotFound", "NOT_FOUND", 404)],
    ["permission denial", (): Error => apiError("PermissionDenied", "PERMISSION_DENIED", 403)],
    ["timeout", (): Error => new Error("Synthetic root lookup timeout")],
  ];
  it.each(lookupFailures)("propagates required root %s without returning empty edits or reading children", async (_name, makeError): Promise<void> => {
    const state = await opened();
    const error = makeError();
    state.store.fail("DcCloseoutCase", state.root.caseId, error);
    const readsBefore = state.store.reads.length;
    await expect(chooseById(state)).rejects.toBe(error);
    expect(state.store.reads.slice(readsBefore)).toEqual([`DcCloseoutCase/${state.root.caseId}`]);
  });

  it.each(["wrong ID", "missing root"])("fails closed for %s rather than using a fixture or another available case", async (kind): Promise<void> => {
    const state = await opened();
    const caseId = kind === "wrong ID" ? caseIdFor(COMPANY_ID, "different-tenancy") : state.root.caseId;
    if (kind === "missing root") state.store.data.delete(`DcCloseoutCase/${caseId}`);
    const readsBefore = state.store.reads.length;
    await expect(chooseById(state, caseId)).rejects.toMatchObject({
      errorName: "ObjectNotFound", errorCode: "NOT_FOUND", statusCode: 404,
    });
    expect(state.store.reads.slice(readsBefore)).toEqual([`DcCloseoutCase/${caseId}`]);
  });

  const malformedIds: [string, unknown][] = [
    ["empty", ""], ["whitespace", " "], ["invalid characters", "bad/id"],
    ["oversized", "x".repeat(201)], ["omitted", undefined], ["null", null],
  ];
  it.each(malformedIds)("rejects %s case ID before any SDK access", async (_name, caseId): Promise<void> => {
    const state = await opened();
    const readsBefore = state.store.reads.length;
    // Exercise malformed runtime inputs without weakening the published string signature.
    await expect(Reflect.apply(chooseCloseoutCharge, undefined, [state.store.client, caseId,
      ACTOR, COMMAND_ID, "1", "repair-250", "20000", REASON])).rejects.toThrow(/Case ID/);
    expect(state.store.reads).toHaveLength(readsBefore);
  });

  it("does not accept or coerce a caller root with redirecting or authorizing fields", async (): Promise<void> => {
    const state = await opened();
    const toString = vi.fn((): string => state.root.caseId);
    const callerRoot = {
      ...state.root, currentReviewId: "caller-review", managementCompanyId: "caller-company",
      revision: "999", inputHash: "f".repeat(64), managerIds: [ACTOR], toString,
    };
    const readsBefore = state.store.reads.length;
    await expect(Reflect.apply(chooseCloseoutCharge, undefined, [state.store.client, callerRoot,
      ACTOR, COMMAND_ID, "1", "repair-250", "20000", REASON])).rejects.toThrow(/Case ID/);
    expect(toString).not.toHaveBeenCalled();
    expect(state.store.reads).toHaveLength(readsBefore);
  });

  const serverRootChanges: [string, Partial<DcCloseoutCase.Props>, RegExp][] = [
    ["manager access", { managerIds: [] }, /manager access/],
    ["synthetic environment", { environmentId: "LIVE" }, /synthetic stored-case environment/],
  ];
  it.each(serverRootChanges)("uses current server %s, not the caller's older root fields", async (_name, patch, message): Promise<void> => {
    const state = await opened();
    state.store.put(createMockOsdkObject(DcCloseoutCase, { ...state.root, ...patch }));
    const readsBefore = state.store.reads.length;
    await expect(chooseById(state)).rejects.toThrow(message);
    expect(state.store.reads.slice(readsBefore)).toEqual([`DcCloseoutCase/${state.root.caseId}`]);
  });

  it("preserves receipt replay through a freshly loaded root without a stale caller object", async (): Promise<void> => {
    const state = await opened();
    const later = nextInputs(state, await chooseById(state));
    const readsBefore = state.store.reads.length;
    expect(await chooseById(state)).toEqual([]);
    expect(state.root.revision).toBe("1");
    expect(later.root.revision).toBe("2");
    expect(state.store.reads.slice(readsBefore)[0]).toBe(`DcCloseoutCase/${later.root.caseId}`);
  });
});
