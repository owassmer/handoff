/** Test-only PK store. This does NOT model transactions, permissions, races or create/upsert semantics. */
import { DcChargeItem, DcCloseoutCase, DcExecutionEvent, DcReviewSnapshot, DcEvidenceRecord, DcMoneyEvent, DcCaseParty, DcRequirement, DcStatementVersion, DcApproval, DcActionRequest } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import type { Edits } from "@osdk/functions";
import { createMockClient, createMockOsdkObject } from "@osdk/unit-testing";
import openCloseoutCase from "../../functions/openCloseoutCase.js";
import { from_wire, is_plain_object } from "../domain/codec.js";
import type { ReviewRequest } from "../domain/types.js";
import { BOOTSTRAP_ACTOR_ID, caseIdFor, type OntologyEdit } from "../phase_c/types.js";
import { serialize } from "../phase_c/validation.js";
import { baseRequest, loadReviewRelease } from "./fixtures/helpers.js";

type StoredObject = Osdk.Instance<DcCloseoutCase> | Osdk.Instance<DcReviewSnapshot>
  | Osdk.Instance<DcExecutionEvent> | Osdk.Instance<DcChargeItem>
  | Osdk.Instance<DcEvidenceRecord> | Osdk.Instance<DcMoneyEvent> | Osdk.Instance<DcCaseParty> | Osdk.Instance<DcRequirement>
  | Osdk.Instance<DcStatementVersion> | Osdk.Instance<DcApproval> | Osdk.Instance<DcActionRequest>;
type RootCreate = Extract<Edits.Object<DcCloseoutCase>, { type: "createObject" }>;
type RootUpdate = Extract<Edits.Object<DcCloseoutCase>, { type: "updateObject" }>;
type SnapshotCreate = Extract<Edits.Object<DcReviewSnapshot>, { type: "createObject" }>;
type ReceiptCreate = Extract<Edits.Object<DcExecutionEvent>, { type: "createObject" }>;
export type ChargeCreate = Extract<Edits.Object<DcChargeItem>, { type: "createObject" }>;
export type ChargeUpdate = Extract<Edits.Object<DcChargeItem>, { type: "updateObject" }>;

export function present<T>(value: T | undefined): T {
  if (value === undefined) throw new Error("Required test value missing");
  return value;
}

export function apiError(errorName: string, errorCode: string, statusCode: number): Error {
  return Object.assign(new Error(errorName), { errorName, errorCode, statusCode });
}

interface TestPkPage { data: StoredObject[]; nextPageToken?: string; }
interface TestPkLookup {
  fetchOne: (pk: string) => Promise<StoredObject>;
  where: (filter: unknown) => { fetchPage: (options: unknown) => Promise<TestPkPage> };
}

export class PkStore {
  readonly data = new Map<string, StoredObject>();
  readonly failures = new Map<string, Error>();
  readonly reads: string[] = [];
  readonly client: Client;

  constructor() {
    // Preserve the official Client's metadata; intercept only the eleven explicitly imported lookup surfaces.
    // A typed Proxy supports failure injection without any/ts-ignore or fake successful reads.
    this.client = new Proxy(createMockClient(), {
      apply: (_target: Client, _this: unknown, args: unknown[]): TestPkLookup => {
        const definition = [DcCloseoutCase, DcReviewSnapshot, DcExecutionEvent, DcChargeItem, DcEvidenceRecord, DcMoneyEvent, DcCaseParty, DcRequirement, DcStatementVersion, DcApproval, DcActionRequest]
          .find((candidate): boolean => candidate === args[0]);
        if (definition === undefined) throw new Error("Unexpected object type in closeout test");
        const read = (pk: string): StoredObject | undefined => {
          const key = `${definition.apiName}/${pk}`;
          this.reads.push(key);
          const failure = this.failures.get(key);
          if (failure !== undefined) throw failure;
          return this.data.get(key);
        };
        return {
          fetchOne: async (pk: string): Promise<StoredObject> => {
            const object = read(pk);
            if (object === undefined) throw apiError("ObjectNotFound", "NOT_FOUND", 404);
            return object;
          },
          where: (filter: unknown): { fetchPage: (options: unknown) => Promise<TestPkPage> } => {
            if (!is_plain_object(filter)) throw new Error("Expected exact PK filter");
            const expression = filter[definition.primaryKeyApiName];
            if (expression === undefined && is_plain_object(filter.caseId) && typeof filter.caseId.$eq === "string") {
              const caseId = filter.caseId.$eq;
              return { fetchPage: async (options: unknown): Promise<TestPkPage> => {
                if (!is_plain_object(options) || options.$pageSize !== 1000) throw new Error("Expected bounded case projection lookup");
                read(`case:${caseId}`);
                const values = [...this.data.values()].filter((row): boolean => row.$apiName === definition.apiName && row.caseId === caseId);
                values.forEach((row): void => { read(row.$primaryKey); });
                return { data: values.slice(0, 1000), nextPageToken: values.length > 1000 ? "more" : undefined };
              } };
            }
            if (!is_plain_object(expression) || typeof expression.$eq !== "string") {
              throw new Error("Expected exact PK equality");
            }
            const pk = expression.$eq;
            return { fetchPage: async (options: unknown): Promise<TestPkPage> => {
              if (!is_plain_object(options) || options.$pageSize !== 2) throw new Error("Expected bounded PK lookup");
              const object = read(pk);
              return { data: object === undefined ? [] : [object] };
            } };
          },
        };
      },
    });
  }

  put(object: StoredObject): void {
    this.data.set(`${object.$apiName}/${object.$primaryKey}`, object);
  }

  fail(type: string, pk: string, error: Error): void {
    this.failures.set(`${type}/${pk}`, error);
  }
}

export function syntheticRequest(): ReviewRequest {
  const request = structuredClone(baseRequest());
  request.ruleReleaseId = loadReviewRelease().ruleReleaseId;
  request.snapshot.caseId = caseIdFor(request.snapshot.managementCompanyId, request.snapshot.tenancyId);
  request.snapshot.parties.forEach((party): void => {
    if (party.roles.some((role): boolean => role === "MANAGER" || role === "ACCOUNTANT")) {
      party.principalId = BOOTSTRAP_ACTOR_ID;
    }
  });
  return from_wire("ReviewRequest", request);
}

export function rootCreate(edits: OntologyEdit[]): RootCreate {
  return present(edits.find((edit): edit is RootCreate =>
    edit.type === "createObject" && edit.obj.apiName === "DcCloseoutCase"));
}

export function rootUpdate(edits: OntologyEdit[]): RootUpdate {
  return present(edits.find((edit): edit is RootUpdate =>
    edit.type === "updateObject" && edit.obj.$apiName === "DcCloseoutCase"));
}

export function snapshotCreate(edits: OntologyEdit[]): SnapshotCreate {
  return present(edits.find((edit): edit is SnapshotCreate =>
    edit.type === "createObject" && edit.obj.apiName === "DcReviewSnapshot"));
}

export function receiptCreate(edits: OntologyEdit[]): ReceiptCreate {
  return present(edits.find((edit): edit is ReceiptCreate =>
    edit.type === "createObject" && edit.obj.apiName === "DcExecutionEvent"));
}

export function chargeCreates(edits: OntologyEdit[]): ChargeCreate[] {
  return edits.filter((edit): edit is ChargeCreate =>
    edit.type === "createObject" && edit.obj.apiName === "DcChargeItem");
}

export function chargeUpdates(edits: OntologyEdit[]): ChargeUpdate[] {
  return edits.filter((edit): edit is ChargeUpdate =>
    edit.type === "updateObject" && edit.obj.$apiName === "DcChargeItem");
}

export interface TestState {
  store: PkStore;
  request: ReviewRequest;
  root: Osdk.Instance<DcCloseoutCase>;
  snapshot: Osdk.Instance<DcReviewSnapshot>;
  receipt: Osdk.Instance<DcExecutionEvent>;
  edits: OntologyEdit[];
}

export async function opened(request: ReviewRequest = syntheticRequest()): Promise<TestState> {
  const store = new PkStore();
  const edits = await openCloseoutCase(store.client, serialize(request), BOOTSTRAP_ACTOR_ID, "open-1");
  const root = createMockOsdkObject(DcCloseoutCase, rootCreate(edits).properties);
  const snapshot = createMockOsdkObject(DcReviewSnapshot, snapshotCreate(edits).properties);
  const receipt = createMockOsdkObject(DcExecutionEvent, receiptCreate(edits).properties);
  feedEdits(store, edits);
  [root, snapshot, receipt].forEach((object): void => store.put(object));
  return { store, request, root, snapshot, receipt, edits };
}

/** Feed emitted edits back as explicitly constructed test inputs, not a platform commit simulation. */
export function nextInputs(state: TestState, edits: OntologyEdit[]): TestState {
  const root = createMockOsdkObject(DcCloseoutCase, { ...state.root, ...rootUpdate(edits).properties });
  const snapshot = createMockOsdkObject(DcReviewSnapshot, snapshotCreate(edits).properties);
  const receipt = createMockOsdkObject(DcExecutionEvent, receiptCreate(edits).properties);
  feedEdits(state.store, edits);
  [root, snapshot, receipt].forEach((object): void => state.store.put(object));
  return { ...state, root, snapshot, receipt, edits };
}

/** Materialize only returned test inputs; deliberately not a concurrency/permissions model. */
export function feedEdits(store: PkStore, edits: OntologyEdit[]): void {
  edits.forEach((edit): void => {
    if (edit.type === "createObject") {
      if (edit.obj.apiName === "DcCloseoutCase") store.put(createMockOsdkObject(DcCloseoutCase, edit.properties));
      if (edit.obj.apiName === "DcReviewSnapshot") store.put(createMockOsdkObject(DcReviewSnapshot, edit.properties));
      if (edit.obj.apiName === "DcExecutionEvent") store.put(createMockOsdkObject(DcExecutionEvent, edit.properties));
      if (edit.obj.apiName === "DcChargeItem") store.put(createMockOsdkObject(DcChargeItem, edit.properties));
      if (edit.obj.apiName === "DcEvidenceRecord") store.put(createMockOsdkObject(DcEvidenceRecord, edit.properties));
      if (edit.obj.apiName === "DcMoneyEvent") store.put(createMockOsdkObject(DcMoneyEvent, edit.properties));
      if (edit.obj.apiName === "DcCaseParty") store.put(createMockOsdkObject(DcCaseParty, edit.properties));
      if (edit.obj.apiName === "DcRequirement") store.put(createMockOsdkObject(DcRequirement, edit.properties));
      if (edit.obj.apiName === "DcStatementVersion") store.put(createMockOsdkObject(DcStatementVersion, edit.properties));
      if (edit.obj.apiName === "DcApproval") store.put(createMockOsdkObject(DcApproval, edit.properties));
      if (edit.obj.apiName === "DcActionRequest") store.put(createMockOsdkObject(DcActionRequest, edit.properties));
    } else if (edit.type === "updateObject") {
      const previous = present(store.data.get(`${edit.obj.$apiName}/${edit.obj.$primaryKey}`));
      if (edit.obj.$apiName === "DcCloseoutCase" && previous.$apiName === "DcCloseoutCase") store.put(createMockOsdkObject(DcCloseoutCase, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcReviewSnapshot" && previous.$apiName === "DcReviewSnapshot") store.put(createMockOsdkObject(DcReviewSnapshot, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcExecutionEvent" && previous.$apiName === "DcExecutionEvent") store.put(createMockOsdkObject(DcExecutionEvent, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcChargeItem" && previous.$apiName === "DcChargeItem") store.put(createMockOsdkObject(DcChargeItem, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcEvidenceRecord" && previous.$apiName === "DcEvidenceRecord") store.put(createMockOsdkObject(DcEvidenceRecord, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcMoneyEvent" && previous.$apiName === "DcMoneyEvent") store.put(createMockOsdkObject(DcMoneyEvent, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcCaseParty" && previous.$apiName === "DcCaseParty") store.put(createMockOsdkObject(DcCaseParty, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcRequirement" && previous.$apiName === "DcRequirement") store.put(createMockOsdkObject(DcRequirement, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcStatementVersion" && previous.$apiName === "DcStatementVersion") store.put(createMockOsdkObject(DcStatementVersion, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcApproval" && previous.$apiName === "DcApproval") store.put(createMockOsdkObject(DcApproval, { ...previous, ...edit.properties }));
      if (edit.obj.$apiName === "DcActionRequest" && previous.$apiName === "DcActionRequest") store.put(createMockOsdkObject(DcActionRequest, { ...previous, ...edit.properties }));
    } else throw new Error("Unexpected deletion or link edit");
  });
}
