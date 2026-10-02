import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";
import { DcCloseoutCase, DcReviewSnapshot } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import * as functionRuntime from "@osdk/functions";
import { createMockOsdkObject } from "@osdk/unit-testing";
import getCloseoutWorkspace, { config } from "../../functions/getCloseoutWorkspace.js";
import { canonical_json, is_plain_object, parse_json } from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import { buildIntent } from "../lifecycle/approvals.js";
import { authorizeLifecycleCommand } from "../lifecycle/commands.js";
import { hasAuthority, nativeReview } from "../phase_c/validation.js";
import {
  parseIntentSpec,
  parseWorkspace,
  serializeWorkspace,
  WorkspaceError,
} from "../workspace/codec.js";
import {
  MAX_INTENT_SPEC_JSON_BYTES,
  MAX_WORKSPACE_JSON_BYTES,
  type CloseoutWorkspaceV1,
} from "../workspace/types.js";
import { apiError, opened, PkStore, present, type TestState } from "./phaseCTestSupport.js";
import {
  ACTOR,
  current,
  initialized,
  NOW,
  requested,
  storageRequest,
  workflow,
} from "./phaseDStorageSupport.js";
import { parseWorkflowReview, parseWorkflowTimestamp } from "../lifecycle/codec.js";
import { projectQueue } from "../workspace/queue.js";

import { refundSpec, requestContext } from "./phaseDRequestsSupport.js";

vi.mock("@osdk/functions", { spy: true });
const NORMALIZED_NOW = parseWorkflowTimestamp(NOW);
let legacyFixture: TestState | undefined;
let workflowFixture: TestState | undefined;

// Arrange accepted inputs once; every test gets an isolated store. The reader and codecs always run.
beforeAll(async (): Promise<void> => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(NOW));
  try {
    legacyFixture = await opened();
    workflowFixture = await initialized();
  } finally {
    vi.useRealTimers();
  }
});

function storedFixture(kind: "legacy" | "initialized"): TestState {
  const source = present(kind === "legacy" ? legacyFixture : workflowFixture);
  const store = new PkStore();
  source.store.data.forEach((object): void => {
    store.put(object);
  });
  return { ...source, store, request: structuredClone(source.request) };
}

beforeEach((): void => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(NOW));
});
afterEach((): void => {
  vi.restoreAllMocks();
  vi.useRealTimers();
});

async function read(state: TestState, intent?: string): Promise<CloseoutWorkspaceV1> {
  return parseWorkspace(await getCloseoutWorkspace(state.store.client, state.root.caseId, intent));
}
function rootPatch(state: TestState, patch: Partial<DcCloseoutCase.Props>): void {
  state.store.put(createMockOsdkObject(DcCloseoutCase, { ...state.root, ...patch }));
}
function snapshotPatch(state: TestState, patch: Partial<DcReviewSnapshot.Props>): void {
  state.store.put(createMockOsdkObject(DcReviewSnapshot, { ...state.snapshot, ...patch }));
}
function rawObject(value: unknown): Record<string, unknown> {
  if (!is_plain_object(value)) throw new Error("Expected object in test");
  return value;
}
function rereadClient(state: TestState, last: Osdk.Instance<DcCloseoutCase> | Error): Client {
  let reads = 0;
  return new Proxy(state.store.client, {
    apply: (target: Client, _this: unknown, args: unknown[]): unknown => {
      if (args[0] !== DcCloseoutCase) return Reflect.apply(target, undefined, args);
      return {
        fetchOne: async (pk: string): Promise<Osdk.Instance<DcCloseoutCase>> => {
          if (++reads === 1) return target(DcCloseoutCase).fetchOne(pk);
          if (last instanceof Error) throw last;
          return last;
        },
      };
    },
  });
}

describe("Phase E bounded read-only workspace", (): void => {
  it("exposes only the business query signature and keeps accepted legacy input and one exact base review", async (): Promise<void> => {
    const state = storedFixture("legacy");
    state.store.reads.length = 0;
    const workspace = await read(state);
    expect(config).toEqual({ apiName: "getCloseoutWorkspace" });
    expect(getCloseoutWorkspace.length).toBe(3);
    expect(workspace.request).toEqual(current(state));
    expect(workspace.workflow).toBeNull();
    expect(workspace.review).toEqual({
      kind: "LEGACY_BASE",
      value: parse_json(present(state.snapshot.reviewJson)),
    });
    expect(workspace.intentPreview).toEqual({ status: "NOT_REQUESTED" });
    expect(workspace.metadata).toMatchObject({
      schemaVersion: "1.0.0",
      projectionVersion: "1",
      workflowVersion: "0",
      caseRevision: state.root.revision,
      currentReviewId: state.root.currentReviewId,
      caseId: state.root.caseId,
      environmentId: "DC_PHASE_C_SYNTHETIC",
      managementCompanyId: "constructed-company-001",
      homeId: state.root.homeId,
      tenancyId: state.root.tenancyId,
      inputHash: state.root.inputHash,
      workflowStateHash: null,
      workflowSchemaVersion: null,
      authorityEvaluationBasis: "LEGACY_REVIEW_CLOCK",
      authorityEvaluatedAt: workspace.request.reviewClock,
      snapshotCreatedAt: NORMALIZED_NOW,
      readAt: NORMALIZED_NOW,
    });
    expect(typeof workspace.metadata.caseRevision).toBe("string");
    expect(typeof workspace.request.snapshot.revision).toBe("number");
    expect(state.store.reads).toEqual([
      `DcCloseoutCase/${state.root.caseId}`,
      `DcReviewSnapshot/${state.root.currentReviewId}`,
      `DcCloseoutCase/${state.root.caseId}`,
    ]);
    expect(serializeWorkspace(workspace)).toBe(canonical_json(workspace));
  });

  it.each([undefined, "0"])(
    "supports known C0 projection version %s without invented assignments",
    async (version): Promise<void> => {
      const state = storedFixture("legacy");
      rootPatch(state, { projectionVersion: version });
      snapshotPatch(state, { workAssignmentsJson: undefined, workAssignmentsHash: undefined });
      expect((await read(state)).workAssignments).toEqual([]);
      expect((await read(state)).metadata.projectionVersion).toBe("0");
    },
  );

  it("returns canonical initialized state and only the effective v2 review at its recorded clock", async (): Promise<void> => {
    const state = storedFixture("initialized");
    const old = await read(state);
    vi.setSystemTime(new Date("2040-01-01T00:00:00.000Z"));
    const later = await read(state);
    expect(later.workflow).toEqual(workflow(state));
    expect(later.review).toEqual({
      kind: "WORKFLOW_V2",
      value: parse_json(present(state.snapshot.workflowReviewJson)),
    });
    expect(later.review).toEqual(old.review);
    expect(later.metadata).toMatchObject({
      workflowVersion: "2",
      workflowSchemaVersion: "2.0.0",
      workflowStateHash: state.snapshot.workflowStateHash,
      effectiveReviewHash: state.snapshot.workflowReviewHash,
      authorityEvaluationBasis: "RECORDED_SNAPSHOT_TIME",
      authorityEvaluatedAt: NORMALIZED_NOW,
      snapshotCreatedAt: NORMALIZED_NOW,
      readAt: "2040-01-01T00:00:00Z",
      actionAvailabilityScope: "CASE_WIDE_NOT_ACTOR_AUTHORIZATION",
    });
    expect(Object.keys(later)).toEqual([
      "metadata",
      "request",
      "workAssignments",
      "workflow",
      "review",
      "intentPreview",
    ]);
    expect(later).not.toHaveProperty("baseReview");
  });

  it("validates and retains assignment sidecars instead of fetching child projections", async (): Promise<void> => {
    const state = storedFixture("initialized");
    const assignments = [
      {
        requirementKey: "historical-work",
        assigneePartyId: "demo-resident",
        internalTargetAt: null,
        reason: "Historical assignment retained",
        assignedAt: NORMALIZED_NOW,
        assignedBy: ACTOR,
      },
    ];
    // The review contains assignments only for matching requirements. An inactive historic key stays in the sidecar.
    snapshotPatch(state, {
      workAssignmentsJson: canonical_json(assignments),
      workAssignmentsHash: fingerprint(assignments),
    });
    // Keep this manually constructed accepted generation coherent with its new E queue hash.
    rootPatch(state, projectQueue(current(state), nativeReview(current(state)),
      parseWorkflowReview(present(state.snapshot.workflowReviewJson)), assignments,
      present(state.root.currentReviewId)));
    expect((await read(state)).workAssignments).toEqual(assignments);
  });

  it("constructs the exact pure target without an edit batch, decision, request or reserve", async (): Promise<void> => {
    const state = storedFixture("initialized");
    const before = [...state.store.data.entries()];
    const batch = vi.mocked(functionRuntime.createEditBatch);
    batch.mockClear();
    const result = await read(state, canonical_json(refundSpec()));
    expect(result.intentPreview).toEqual({
      status: "CONSTRUCTED",
      spec: refundSpec(),
      intent: buildIntent(
        current(state),
        nativeReview(current(state)),
        workflow(state),
        refundSpec(),
      ),
    });
    expect(batch).not.toHaveBeenCalled();
    expect([...state.store.data.entries()]).toEqual(before);
    expect(result.workflow?.approvals).toEqual([]);
    expect(result.workflow?.requests).toEqual([]);
    expect(result.workflow?.events).toEqual([]);
    expect(result.metadata.intentPreviewSemantics).toBe(
      "TARGET_CONSTRUCTION_ONLY_NOT_AUTHORIZATION_OR_RESERVATION",
    );
  });

  it("does not confuse case-wide availability or a constructed target with current actor permission", async (): Promise<void> => {
    const request = storageRequest();
    request.snapshot.authorityGrants.forEach((grant): void => {
      grant.effectiveUntil = "2027-01-01T00:00:00Z";
    });
    const state = await initialized(request);
    const farFuture = "2040-01-01T00:00:00.000Z";
    vi.setSystemTime(new Date(farFuture));
    expect(
      hasAuthority(current(state), ACTOR, "ACCOUNTANT", "APPROVE_EXACT_VERSION", 600, farFuture),
    ).toBe(false);
    expect((): void =>
      authorizeLifecycleCommand(
        current(state),
        workflow(state),
        { kind: "DECIDE_APPROVAL", payload: { intent: refundSpec(), decision: "APPROVED" } },
        requestContext("not-executed", { actorId: ACTOR, serverNow: farFuture }),
      ),
    ).toThrow(/authority|grant/);
    const result = await read(state, canonical_json(refundSpec()));
    expect(result.intentPreview.status).toBe("CONSTRUCTED");
    expect(result.metadata.authorityEvaluatedAt).toBe(NORMALIZED_NOW);
    expect(result.metadata.actionAvailabilityScope).toBe("CASE_WIDE_NOT_ACTOR_AUTHORIZATION");
    expect(result).not.toHaveProperty("actorId");
    expect(result).not.toHaveProperty("permissions");
  });

  it("uses stored native base rather than a v2 cast and preserves live commitments", async (): Promise<void> => {
    const state = await requested(storedFixture("initialized"));
    const result = await read(state, canonical_json(refundSpec(600, "another-installment")));
    expect(result.intentPreview).toEqual({
      status: "CONSTRUCTED",
      spec: refundSpec(600, "another-installment"),
      intent: buildIntent(
        current(state),
        nativeReview(current(state)),
        workflow(state),
        refundSpec(600, "another-installment"),
      ),
    });
    expect(result.review).toEqual({
      kind: "WORKFLOW_V2",
      value: parse_json(present(state.snapshot.workflowReviewJson)),
    });
    expect(result.workflow?.requests).toHaveLength(1);
  });

  it("separates known legacy and business construction blocks from workspace errors", async (): Promise<void> => {
    const legacy = await read(storedFixture("legacy"), canonical_json(refundSpec()));
    expect(legacy.intentPreview).toMatchObject({
      status: "BLOCKED",
      reason: { code: "WORKFLOW_NOT_INITIALIZED" },
    });
    const initializedResult = await read(
      storedFixture("initialized"),
      canonical_json(refundSpec(999999)),
    );
    expect(initializedResult.intentPreview).toMatchObject({
      status: "BLOCKED",
      reason: { code: "INTENT_CONSTRUCTION_BLOCKED" },
    });
    const outside = await read(
      storedFixture("initialized"),
      canonical_json(refundSpec(600, "item", { statementId: "other-case-statement" })),
    );
    expect(outside.intentPreview).toMatchObject({
      status: "BLOCKED",
      reason: { code: "INTENT_CONSTRUCTION_BLOCKED" },
    });
  });

  it.each([
    { environmentId: "OTHER" },
    { managementCompanyId: "other-company" },
    { homeId: "other-home" },
    { tenancyId: "other-tenancy" },
    { readerIds: [] },
    { adminIds: [] },
    { revision: "9007199254740992" },
    { revision: "01" },
    { projectionVersion: "8" },
    { workflowVersion: "8" },
    { inputHash: "0".repeat(64) },
  ] satisfies Partial<DcCloseoutCase.Props>[])(
    "rejects wrong root scope/version/basis %j",
    async (patch): Promise<void> => {
      const state = storedFixture("initialized");
      rootPatch(state, patch);
      await expect(read(state)).rejects.toThrow();
    },
  );

  it.each([
    { environmentId: "OTHER" },
    { managementCompanyId: "other-company" },
    { caseId: "other-case" },
    { caseRevision: "999" },
    { resultHash: "0".repeat(64) },
    { workflowStateHash: "0".repeat(64) },
    { workAssignmentsHash: "0".repeat(64) },
    { workflowReviewJson: undefined },
    { readerIds: [] },
    { workflowStateJson: "{}" },
    { workflowStateJson: " ".repeat(256 * 1024) },
    { requestJson: " ".repeat(256 * 1024 + 1) },
    { reviewJson: "{}" },
  ] satisfies Partial<DcReviewSnapshot.Props>[])(
    "rejects missing, malformed or mismatched snapshot #%#",
    async (patch): Promise<void> => {
      const state = storedFixture("initialized");
      snapshotPatch(state, patch);
      await expect(read(state)).rejects.toThrow();
    },
  );

  it.each([
    { revision: "3" },
    { currentReviewId: `dc-review:${"0".repeat(64)}` },
    { homeId: "changed-home" },
    { tenancyId: "changed-tenancy" },
    { environmentId: "OTHER" },
    { managementCompanyId: "other-company" },
    { workflowVersion: "0" },
    { projectionVersion: "0" },
    { readerIds: [] },
    { managerIds: [] },
    { currentStatementId: "other-statement" },
    { inputHash: "0".repeat(64) },
    { updatedAt: "2026-09-19T12:00:00.000Z" },
  ] satisfies Partial<DcCloseoutCase.Props>[])(
    "rejects a final root generation change %j as explicitly retryable",
    async (patch): Promise<void> => {
      const state = storedFixture("initialized");
      const client = rereadClient(
        state,
        createMockOsdkObject(DcCloseoutCase, { ...state.root, ...patch }),
      );
      await expect(getCloseoutWorkspace(client, state.root.caseId)).rejects.toMatchObject({
        code: "GENERATION_CHANGED",
        retryable: true,
      });
    },
  );

  it.each(["root", "snapshot", "reread"])(
    "propagates %s policy/transport errors instead of fallback data",
    async (where): Promise<void> => {
      const state = storedFixture("initialized");
      const error = apiError("PermissionDenied", "PERMISSION_DENIED", 403);
      if (where === "root") state.store.fail("DcCloseoutCase", state.root.caseId, error);
      if (where === "snapshot")
        state.store.fail("DcReviewSnapshot", present(state.root.currentReviewId), error);
      const client = where === "reread" ? rereadClient(state, error) : state.store.client;
      await expect(getCloseoutWorkspace(client, state.root.caseId)).rejects.toBe(error);
    },
  );
});

describe("Phase E strict intent and workspace codecs", (): void => {
  it.each(Object.keys(refundSpec()))(
    "requires nullable intent field %s explicitly",
    (field): void => {
      const value: Record<string, unknown> = { ...refundSpec() };
      delete value[field];
      expect((): unknown => parseIntentSpec(canonical_json(value))).toThrow();
    },
  );
  it.each([
    "null",
    "[]",
    "{}",
    "{",
    '{"kind":"REFUND","kind":"REFUND"}',
    canonical_json({ ...refundSpec(), actorId: ACTOR }),
    canonical_json({ ...refundSpec(), amountCents: "600" }),
    canonical_json({ ...refundSpec(), amountCents: 0 }),
    JSON.stringify({ ...refundSpec(), amountCents: 0.5 }),
    JSON.stringify({ ...refundSpec(), amountCents: Number.MAX_SAFE_INTEGER + 1 }),
    canonical_json({ ...refundSpec(), kind: "UNKNOWN" }),
    canonical_json({ ...refundSpec(), reversesTransactionId: "other" }),
    canonical_json({ ...refundSpec(), kind: "STATEMENT_DISPATCH" }),
    canonical_json({ ...refundSpec(), kind: "CHARGE_POSTING_REVERSAL" }),
    `${" ".repeat(MAX_INTENT_SPEC_JSON_BYTES - 1)}é`,
    '{"kind":"REFUND","amountCents":600,"dispositionKey":"\\ud800","statementId":null,"replacesRequestId":null,"reversesTransactionId":null}',
  ])("rejects malformed intent #%# before any lookup", async (json): Promise<void> => {
    const state = storedFixture("legacy");
    state.store.reads.length = 0;
    await expect(read(state, json)).rejects.toMatchObject({
      code: "INVALID_INTENT_SPEC",
      retryable: false,
    });
    expect(state.store.reads).toEqual([]);
  });

  it("accepts only exact spec and leaves business-block handling to the preview", (): void => {
    expect(parseIntentSpec(canonical_json(refundSpec()))).toEqual(refundSpec());
    expect(
      parseIntentSpec(
        canonical_json(
          refundSpec(600, "rev", {
            kind: "CHARGE_POSTING_REVERSAL",
            reversesTransactionId: "original-transaction",
          }),
        ),
      ),
    ).toMatchObject({ kind: "CHARGE_POSTING_REVERSAL" });
  });

  it("requires every top-level and metadata field and rejects unknown fields at both boundaries", async (): Promise<void> => {
    const valid = await read(storedFixture("initialized"));
    [valid, valid.metadata].forEach((value): void => {
      Object.keys(value).forEach((key): void => {
        const copy = rawObject(parse_json(canonical_json(valid)));
        const selected = value === valid ? copy : rawObject(copy.metadata);
        delete selected[key];
        expect((): unknown => parseWorkspace(canonical_json(copy))).toThrow();
      });
      const copy = rawObject(parse_json(canonical_json(valid)));
      const selected = value === valid ? copy : rawObject(copy.metadata);
      selected.actorAuthorized = true;
      expect((): unknown => parseWorkspace(canonical_json(copy))).toThrow();
    });
  });

  it.each([
    { schemaVersion: "2.0.0" },
    { caseRevision: 2 },
    { caseRevision: "9007199254740992" },
    { workflowVersion: "0" },
    { inputSchemaVersion: "8.0.0" },
    { reviewSchemaVersion: "8.0.0" },
    { workflowSchemaVersion: "8.0.0" },
    { codeVersion: "phase-e" },
    { environmentId: "OTHER" },
    { authorityEvaluatedAt: "2040-01-01T00:00:00.000Z" },
    { inputHash: "0".repeat(64) },
    { workAssignmentsHash: "0".repeat(64) },
    { workflowStateHash: "0".repeat(64) },
    { readAt: "not-a-time" },
    { actionAvailabilityScope: "ACTOR_AUTHORIZED" },
  ])("rejects malformed output metadata %j", async (patch): Promise<void> => {
    const valid = await read(storedFixture("initialized"));
    expect((): unknown =>
      parseWorkspace(canonical_json({ ...valid, metadata: { ...valid.metadata, ...patch } })),
    ).toThrow();
  });

  it("rejects malformed nested output, duplicate reviews, forged targets and omitted nested nullables", async (): Promise<void> => {
    const valid = await read(storedFixture("initialized"), canonical_json(refundSpec()));
    const malformed: unknown[] = [
      { ...valid, review: { ...valid.review, base: nativeReview(valid.request) } },
      { ...valid, workflow: null },
      { ...valid, request: { ...valid.request, extra: true } },
      { ...valid, intentPreview: { ...valid.intentPreview, authorized: true } },
      { ...valid, intentPreview: { status: "NOT_REQUESTED", spec: refundSpec() } },
      {
        ...valid,
        intentPreview: {
          status: "BLOCKED",
          spec: refundSpec(),
          reason: { code: "INTENT_CONSTRUCTION_BLOCKED", message: "Forged" },
        },
      },
    ];
    if (valid.intentPreview.status !== "CONSTRUCTED") throw new Error("Expected target");
    malformed.push({
      ...valid,
      intentPreview: {
        ...valid.intentPreview,
        intent: { ...valid.intentPreview.intent, targetVersionId: "forged" },
      },
    });
    malformed.forEach((value): void => {
      expect((): unknown => parseWorkspace(canonical_json(value))).toThrow();
    });
  });

  it("enforces aggregate UTF-8 bounds independently and never truncates arrays or strings", async (): Promise<void> => {
    const valid = await read(storedFixture("initialized"));
    const json = canonical_json(valid);
    const atLimit = json + " ".repeat(MAX_WORKSPACE_JSON_BYTES - Buffer.byteLength(json, "utf8"));
    expect(parseWorkspace(atLimit)).toEqual(valid);
    expect((): unknown => parseWorkspace(atLimit + " ")).toThrow(/UTF-8/);
    const multibyte = "é".repeat(Math.floor(MAX_WORKSPACE_JSON_BYTES / 2) + 1);
    expect(multibyte.length).toBeLessThan(MAX_WORKSPACE_JSON_BYTES);
    expect((): unknown => parseWorkspace(multibyte)).toThrow(/UTF-8/);
    expect((): unknown =>
      serializeWorkspace({
        ...valid,
        workAssignments: Array.from({ length: 600 }, (_, index) => ({
          requirementKey: `work-${index}`,
          assigneePartyId: "demo-resident",
          internalTargetAt: null,
          assignedBy: ACTOR,
          assignedAt: NOW,
          reason: "é".repeat(1000),
        })),
      }),
    ).toThrow(/UTF-8/);
    expect(new WorkspaceError("INVALID_WORKSPACE", "bad output").retryable).toBe(false);
  });
});
