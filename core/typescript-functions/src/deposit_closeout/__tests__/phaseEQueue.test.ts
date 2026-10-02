import {
  afterEach,
  beforeAll,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";
import { DcCloseoutCase } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import { createMockOsdkObject } from "@osdk/unit-testing";
import {
  canonical_json,
  is_plain_object,
  parse_json,
} from "../domain/codec.js";
import { normalize_timestamp } from "../domain/datetime.js";
import { fingerprint } from "../domain/fingerprints.js";
import type {
  RequirementResult,
  ReviewEnvelope,
  ReviewRequest,
} from "../domain/types.js";
import { parseWorkflowReview } from "../lifecycle/codec.js";
import { reviewWorkflow } from "../lifecycle/review.js";
import type { WorkflowReviewV2 } from "../lifecycle/types.js";
import type { WorkAssignment } from "../phase_c/change_types.js";
import { loadCurrentReview } from "../phase_c/storage.js";
import { nativeReview, serialize } from "../phase_c/validation.js";
import {
  MAX_QUEUE_JSON_BYTES,
  projectQueue,
  QUEUE_PROPERTY_KEYS,
  validateQueue,
} from "../workspace/queue.js";
import getCloseoutWorkspace from "../../functions/getCloseoutWorkspace.js";
import recheckCloseoutCase from "../../functions/recheckCloseoutCase.js";
import initializeCloseoutWorkflow from "../../functions/initializeCloseoutWorkflow.js";
import assignCloseoutWork from "../../functions/assignCloseoutWork.js";
import setCloseoutRefundInstructions from "../../functions/setCloseoutRefundInstructions.js";
import chooseCloseoutCharge from "../../functions/chooseCloseoutCharge.js";
import {
  nextInputs,
  opened,
  PkStore,
  present,
  rootUpdate,
  snapshotCreate,
  type TestState,
} from "./phaseCTestSupport.js";
import {
  ACTOR,
  act,
  current,
  initialized,
  NOW,
  WHY,
  workflow,
} from "./phaseDStorageSupport.js";
import {
  refundSpec,
  RequestHarness,
  requestContext,
} from "./phaseDRequestsSupport.js";
import { applyDecisionCommand } from "../lifecycle/prerequisites.js";
import { baseRequest } from "./fixtures/helpers.js";

let legacy: TestState;
let initializedState: TestState;
let accepted: ReviewRequest;
let base: ReviewEnvelope;
let effective: WorkflowReviewV2;
beforeAll(async (): Promise<void> => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(NOW));
  try {
    legacy = await opened();
    initializedState = await initialized();
    accepted = current(initializedState);
    base = nativeReview(accepted);
    effective = parseWorkflowReview(
      present(initializedState.snapshot.workflowReviewJson),
    );
  } finally {
    vi.useRealTimers();
  }
});
beforeEach((): void => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(NOW));
});
afterEach((): void => {
  vi.restoreAllMocks();
  vi.useRealTimers();
});
function stateCopy(source: TestState = initializedState): TestState {
  const store = new PkStore();
  source.store.data.forEach((object): void => store.put(object));
  return { ...source, store, request: structuredClone(source.request) };
}
function object(value: unknown): Record<string, unknown> {
  if (!is_plain_object(value)) throw new Error("Expected test object");
  return value;
}
function json(
  props: Partial<ReturnType<typeof projectQueue>>,
): Record<string, unknown> {
  return object(parse_json(present(props.queueSummaryJson)));
}
function project(
  review: WorkflowReviewV2 | undefined = effective,
  assignments: WorkAssignment[] = [],
): ReturnType<typeof projectQueue> {
  return projectQueue(
    accepted,
    base,
    review,
    assignments,
    present(initializedState.root.currentReviewId),
  );
}
function assignment(
  requirementKey: string,
  internalTargetAt: string | null,
): WorkAssignment {
  return {
    requirementKey,
    internalTargetAt,
    assigneePartyId: "demo-manager",
    assignedBy: ACTOR,
    assignedAt: normalize_timestamp(NOW)!,
    reason: WHY,
  };
}
function requirement(patch: Partial<RequirementResult>): RequirementResult {
  return {
    ...structuredClone(effective.result.scopeRequirements.requirements[0]!),
    ...patch,
  };
}
const EMPTY_QUEUE = Object.fromEntries(
  QUEUE_PROPERTY_KEYS.map((key) => [key, undefined]),
);

// Deliberately vary authoritative review fields in these pure display tests. They do not test/reimplement business reducers.
describe("pure compact queue", (): void => {
  it("copies current-generation metadata, selected native account fields and all independent tracks", (): void => {
    const result = project();
    const summary = json(result);
    expect(result.queueSummaryVersion).toBe("1");
    expect(summary.metadata).toMatchObject({
      caseRevision: initializedState.root.revision,
      currentReviewId: initializedState.root.currentReviewId,
      reviewClock: accepted.reviewClock,
      inputHash: effective.metadata.inputHash,
      effectiveReviewHash: fingerprint(effective),
      workAssignmentsHash: fingerprint([]),
      effectiveReviewKind: "WORKFLOW_V2",
    });
    const account = object(summary.account);
    Object.entries(account).forEach(([key, value]): void =>
      expect(value).toEqual(Reflect.get(effective.result.account, key)),
    );
    expect(summary.tracks).toEqual(
      effective.result.outcomes.tracks.map(({ track, state }) => ({
        track,
        state,
      })),
    );
    expect(summary.completion).toMatchObject({
      depositComplete: false,
      overallCaseComplete: false,
      legalPerformanceConfirmed: false,
    });
    expect(summary).not.toHaveProperty("evidence");
    expect(summary).not.toHaveProperty("workflow");
  });
  it.each([null, 0, 12, -12])(
    "preserves null/zero/signed accounting value %s without arithmetic",
    (amount): void => {
      const review = structuredClone(effective);
      review.result.account.postingDeltaCents = amount;
      review.result.account.finalRefundCents = amount;
      review.result.account.newlyRequestableRefundCents = amount;
      expect(json(project(review)).account).toMatchObject({
        postingDeltaCents: amount,
        finalRefundCents: amount,
        newlyRequestableRefundCents: amount,
      });
    },
  );
  it("does not mutate accepted inputs or change its output with the actual wall clock", (): void => {
    const before = canonical_json({ accepted, base, effective });
    const first = project();
    vi.setSystemTime(new Date("2090-01-01T00:00:00Z"));
    expect(project()).toEqual(first);
    expect(canonical_json({ accepted, base, effective })).toBe(before);
    expect(present(first.queueSummaryJson)).not.toContain('"overdue"');
  });
  it.each(["UNSUPPORTED", "INTERPRETATION_REQUIRED"])(
    "labels %s without inventing deadlines",
    (scopeState): void => {
      const review = structuredClone(effective);
      review.result.scopeRequirements.scopeState = scopeState;
      review.result.scopeRequirements.requirements = [
        requirement({
          requirementKey: "prepare:scope-and-trigger",
          legalDueDate: null,
        }),
      ];
      const result = project(review);
      expect(result.queueAttentionKind).toBe("UNSUPPORTED_SCOPE");
      expect(result.queueNearestLegalDueDate).toBeUndefined();
    },
  );
  it.each(["MISSING_FACTS", "SUPPORTED"])(
    "recognizes named missing input independently of scope %s",
    (scopeState): void => {
      const review = structuredClone(effective);
      review.result.scopeRequirements.scopeState = scopeState;
      review.result.missingInputs = [
        {
          questionId: "named-fact",
          question: "A fact?",
          reason: "No English matching",
          resolverRole: "MANAGER",
          resolverPartyId: null,
          neededRecord: null,
          affectedItemIds: [],
          affectedActionKinds: [],
        },
      ];
      expect(project(review).queueAttentionKind).toBe(
        "NEEDS_FACTS_OR_DECISION",
      );
    },
  );
  it("does not classify by English reasons or count repeated request details", (): void => {
    const review = structuredClone(effective);
    const details = {
      requestId: "r",
      kind: "REFUND" as const,
      state: "OUTCOME_UNKNOWN" as const,
      amountCents: 600,
      reservedAmountCents: 600,
      attemptId: "a",
      lastEventId: "e",
      canonicalTransactionId: null,
      reconciliationRequired: true,
      reason: "all fine",
    };
    review.result.actions.forEach((action): void => {
      action.reason = "Simulated complete unsupported reconciliation overdue";
      if (action.workflow !== null) action.workflow.requestDetails = [details];
    });
    const result = project(review);
    expect(result.queueAttentionKind).toBe("RECONCILIATION");
    expect(json(result).reconciliationRequestIds).toEqual(["r"]);
    expect(json(result).account).toEqual(json(project()).account);
    review.result.actions.forEach((action): void => {
      if (action.workflow !== null) action.workflow.requestDetails = [];
    });
    expect(project(review).queueAttentionKind).toBe(
      project().queueAttentionKind,
    );
  });
  it("rejects disagreeing repeated current request identities", (): void => {
    const review = structuredClone(effective);
    const details = review.result.actions.filter(
      (entry): boolean => entry.workflow !== null,
    );
    const currentRequest = {
      requestId: "r",
      kind: "REFUND" as const,
      state: "READY" as const,
      amountCents: 3,
      reservedAmountCents: 3,
      attemptId: null,
      lastEventId: null,
      canonicalTransactionId: null,
      reconciliationRequired: false,
      reason: "ready",
    };
    details[0]!.workflow!.requestDetails = [currentRequest];
    details[1]!.workflow!.requestDetails = [
      { ...currentRequest, reservedAmountCents: 4 },
    ];
    expect((): unknown => project(review)).toThrow(/disagree/);
  });
  it("keeps reconciliation attention independent from earliest communications deadline and available preparation", (): void => {
    const review = structuredClone(effective);
    review.result.account.reconciliationState = "CONFLICT";
    const result = project(review);
    expect(result.queueAttentionKind).toBe("RECONCILIATION");
    expect(result.queueNearestLegalDueDate).toBe(
      project().queueNearestLegalDueDate,
    );
    expect(json(result).availableActionKeys).toContain("prepare:statement");
  });
  it.each(["FULFILLED", "NOT_APPLICABLE"])(
    "clears legal and internal dates for %s requirements",
    (state): void => {
      const review = structuredClone(effective);
      review.result.scopeRequirements.requirements = [
        requirement({
          requirementKey: "done",
          state,
          legalDueDate: "2026-09-01",
          dueKind: "LEGAL",
        }),
      ];
      const result = project(review, [
        assignment("done", "2026-09-01T00:00:00Z"),
      ]);
      expect(result.queueNearestLegalDueDate).toBeUndefined();
      expect(result.queueNearestInternalTargetAtIso).toBeUndefined();
      expect(json(result)).toMatchObject({
        nearestLegalDue: null,
        nearestInternalTarget: null,
      });
    },
  );
  it("uses provided legal applicability and breaks equal-date ties by requirement key", (): void => {
    const review = structuredClone(effective);
    review.result.scopeRequirements.requirements = [
      requirement({
        requirementKey: "z",
        state: "PENDING",
        legalDueDate: "2026-09-02",
        dueKind: "LEGAL",
      }),
      requirement({
        requirementKey: "a",
        state: "BLOCKED",
        legalDueDate: "2026-09-02",
        dueKind: "LEGAL",
      }),
      requirement({
        requirementKey: "no",
        state: "OPEN",
        legalDueDate: "2026-09-01",
        dueKind: "UNCONFIRMED",
      }),
    ];
    expect(json(project(review)).nearestLegalDue).toMatchObject({
      requirementKey: "a",
      date: "2026-09-02",
    });
    review.result.scopeRequirements.requirements.reverse();
    expect(json(project(review)).nearestLegalDue).toMatchObject({
      requirementKey: "a",
    });
  });
  it.each([
    [
      "2026-09-01T00:00:00Z",
      "2026-09-01T00:00:00.000001Z",
      "z",
      "2026-09-01T00:00:00.000000Z",
    ],
    [
      "2026-09-01T00:00:00.000002Z",
      "2026-09-01T00:00:00.000001Z",
      "a",
      "2026-09-01T00:00:00.000001Z",
    ],
    [
      "2026-09-01T00:00:00Z",
      "2026-09-01T00:00:00.000000Z",
      "a",
      "2026-09-01T00:00:00.000000Z",
    ],
  ])(
    "sorts exact microseconds and serializes fixed UTC digits #%#",
    (z, a, key, atIso): void => {
      const review = structuredClone(effective);
      review.result.scopeRequirements.requirements = [
        requirement({ requirementKey: "z", state: "OPEN" }),
        requirement({ requirementKey: "a", state: "OPEN" }),
      ];
      const assignments = [
        assignment("z", z),
        assignment("a", a),
        assignment("inactive", "2000-01-01T00:00:00Z"),
      ];
      const result = project(review, assignments);
      expect(result.queueNearestInternalTargetAtIso).toBe(atIso);
      expect(json(result).nearestInternalTarget).toEqual({
        requirementKey: key,
        atIso,
      });
    },
  );
  it("explicit null assignment target clears a review target and ignores historical assignments", (): void => {
    const review = structuredClone(effective);
    review.result.scopeRequirements.requirements = [
      requirement({
        requirementKey: "a",
        state: "OPEN",
        internalTargetAt: "2026-09-01T00:00:00Z",
      }),
    ];
    expect(
      project(review, [
        assignment("a", null),
        assignment("absent", "2000-01-01T00:00:00Z"),
      ]).queueNearestInternalTargetAtIso,
    ).toBeUndefined();
  });
  it("selects one stable next assignment rather than any other work assigned to a party", (): void => {
    const review = structuredClone(effective);
    review.result.actions = [];
    review.result.missingInputs = [];
    review.result.scopeRequirements.requirements = [
      requirement({
        requirementKey: "a",
        state: "OPEN",
        dueKind: "LEGAL",
        legalDueDate: "2026-09-01",
      }),
      requirement({
        requirementKey: "b",
        state: "OPEN",
        dueKind: "LEGAL",
        legalDueDate: "2026-09-02",
      }),
    ];
    const result = project(review, [
      { ...assignment("b", null), assigneePartyId: "demo-accountant" },
      assignment("a", null),
    ]);
    expect(result.queueNextRequirementKey).toBe("a");
    expect(result.queueNextAssigneePartyId).toBe("demo-manager");
    expect(json(result).nextWork).toMatchObject({
      workKey: "a",
      selectionBasis: "OPEN_REQUIREMENT",
    });
  });
  it("does not label maintenance-only work as ready or simulated deposit-only completion as overall complete", (): void => {
    const review = structuredClone(effective);
    review.result.missingInputs = [];
    review.result.actions = review.result.actions.filter(
      (entry): boolean => entry.actionKey === "review:repeat",
    );
    review.result.outcomes.simulatedDepositWorkflowComplete = true;
    expect(project(review).queueAttentionKind).toBe("WAITING");
    review.result.outcomes.simulatedOverallWorkflowComplete = true;
    const result = project(review);
    expect(result.queueAttentionKind).toBe("SIMULATED_COMPLETE");
    expect(json(result).nextWork).toBeNull();
    expect(result.queueNextRequirementKey).toBeUndefined();
    expect(result.queueNextResponsibleRole).toBeUndefined();
    expect(result.queueNextAssigneePartyId).toBeUndefined();
  });
  it("labels known uninitialized state and does not fabricate v2 balances or completion", (): void => {
    const result = projectQueue(accepted, base, undefined, [], "review");
    expect(result.queueAttentionKind).toBe("LEGACY_INITIALIZATION");
    expect(json(result).account).toMatchObject({
      newlyRequestableRefundCents: null,
    });
    expect(json(result).nextWork).toMatchObject({
      workKey: "workflow:initialize",
      requirementKey: null,
      actionKey: null,
    });
    expect(json(result).completion).toMatchObject({
      simulatedDepositWorkflowComplete: false,
      simulatedOverallWorkflowComplete: false,
    });
  });
  it("bounds the canonical summary in UTF-8 bytes inclusively and never truncates", (): void => {
    const review = structuredClone(effective);
    review.result.actions = [];
    review.result.missingInputs = [];
    review.result.scopeRequirements.requirements = [
      requirement({ requirementKey: "only", state: "OPEN", question: "" }),
    ];
    const length = Buffer.byteLength(
      present(project(review).queueSummaryJson),
      "utf8",
    );
    review.result.scopeRequirements.requirements[0]!.question =
      "é".repeat(Math.floor((MAX_QUEUE_JSON_BYTES - length) / 2)) +
      "x".repeat((MAX_QUEUE_JSON_BYTES - length) % 2);
    expect(
      Buffer.byteLength(present(project(review).queueSummaryJson), "utf8"),
    ).toBe(MAX_QUEUE_JSON_BYTES);
    review.result.scopeRequirements.requirements[0]!.question += "é";
    expect((): unknown => project(review)).toThrow(/UTF-8/);
  });
});

describe("accepted storage generations", (): void => {
  it("writes all eight explicit keys in the one existing root edit and matches the created snapshot", async (): Promise<void> => {
    const state = stateCopy();
    const edits = await recheckCloseoutCase(
      state.store.client,
      state.root.caseId,
      ACTOR,
      "queue-recheck",
      present(state.root.revision),
    );
    const props = rootUpdate(edits).properties;
    const snapshot = snapshotCreate(edits).properties;
    expect(
      edits.filter(
        (edit): boolean =>
          edit.type === "updateObject" &&
          edit.obj.$apiName === "DcCloseoutCase",
      ),
    ).toHaveLength(1);
    QUEUE_PROPERTY_KEYS.forEach((key): void =>
      expect(Object.hasOwn(props, key)).toBe(true),
    );
    expect(json(props).metadata).toMatchObject({
      currentReviewId: snapshot.reviewId,
      caseRevision: snapshot.caseRevision,
      effectiveReviewHash: snapshot.workflowReviewHash,
      workAssignmentsHash: snapshot.workAssignmentsHash,
    });
    const next = nextInputs(state, edits);
    await expect(
      loadCurrentReview(next.store.client, next.root),
    ).resolves.toBeDefined();
    expect(
      await recheckCloseoutCase(
        next.store.client,
        next.root.caseId,
        ACTOR,
        "queue-recheck",
        present(state.root.revision),
      ),
    ).toEqual([]);
    await expect(
      recheckCloseoutCase(
        next.store.client,
        next.root.caseId,
        ACTOR,
        "loser",
        present(state.root.revision),
      ),
    ).rejects.toThrow(/revision/);
  });
  it("open, C choice, C operational and D lifecycle all refresh the same projection", async (): Promise<void> => {
    const state = stateCopy(legacy);
    const item = current(state).snapshot.charges[0]!;
    const chosen = nextInputs(
      state,
      await chooseCloseoutCharge(
        state.store.client,
        state.root.caseId,
        ACTOR,
        "queue-choice",
        present(state.root.revision),
        item.itemId,
        "100",
        WHY,
      ),
    );
    expect(chosen.root.queueSummaryVersion).toBe("1");
    const init = await act(
      chosen,
      initializeCloseoutWorkflow,
      {},
      "queue-init",
    );
    expect(json(init.root).metadata).toMatchObject({
      effectiveReviewKind: "WORKFLOW_V2",
      currentReviewId: init.root.currentReviewId,
    });
    expect(json(state.root).metadata).toMatchObject({
      effectiveReviewKind: "LEGACY_BASE",
    });
  });
  it("uses organizational assignments without changing native money or intents and explicitly clears a removed target", async (): Promise<void> => {
    let state = stateCopy();
    const requirementKey = present(state.root.queueNextRequirementKey);
    const assign = {
      requirementKey,
      assigneePartyId: "demo-manager",
      internalTargetAt: "2026-09-01T00:00:00.000001Z",
      reason: WHY,
    };
    const before = json(state.root).account;
    state = await act(state, assignCloseoutWork, assign, "queue-assign");
    expect(state.root.queueNextAssigneePartyId).toBe("demo-manager");
    expect(state.root.queueNearestInternalTargetAtIso).toBe(
      assign.internalTargetAt,
    );
    expect(json(state.root).account).toEqual(before);
    state = await act(
      state,
      assignCloseoutWork,
      { ...assign, internalTargetAt: null },
      "queue-clear",
    );
    expect(
      Object.hasOwn(
        rootUpdate(state.edits).properties,
        "queueNearestInternalTargetAtIso",
      ),
    ).toBe(true);
    expect(
      rootUpdate(state.edits).properties.queueNearestInternalTargetAtIso,
    ).toBeUndefined();
    expect(json(state.root).nearestInternalTarget).toBeNull();
  });
  it("keeps independent communication work available when refund instructions become incomplete", async (): Promise<void> => {
    const state = stateCopy();
    const { versionId: _version, ...instructions } =
      workflow(state).refundInstructions;
    const next = await act(
      state,
      setCloseoutRefundInstructions,
      { ...instructions, state: "UNCONFIRMED" },
      "queue-route",
    );
    expect(next.root.queueAttentionKind).toBe("NEEDS_FACTS_OR_DECISION");
    expect(json(next.root).availableActionKeys).toContain("prepare:statement");
    expect(next.root.queueNearestLegalDueDate).toBe(
      state.root.queueNearestLegalDueDate,
    );
  });
  it("allows only all-absent pre-E state without read writes; a later accepted command initializes it", async (): Promise<void> => {
    const state = stateCopy();
    const root = createMockOsdkObject(DcCloseoutCase, {
      ...state.root,
      ...EMPTY_QUEUE,
    });
    state.store.put(root);
    const count = state.store.data.size;
    await getCloseoutWorkspace(state.store.client, root.caseId);
    expect(state.store.data.size).toBe(count);
    expect(root.queueSummaryVersion).toBeUndefined();
    const edits = await recheckCloseoutCase(
      state.store.client,
      root.caseId,
      ACTOR,
      "pre-e-recheck",
      present(root.revision),
    );
    expect(rootUpdate(edits).properties.queueSummaryVersion).toBe("1");
  });
  it.each([undefined, "0", "2", "01", "", null])(
    "rejects partial/unknown queue version %s",
    (version): void => {
      const props = { ...project(), queueSummaryVersion: version };
      // Intentionally invalid wire property; no SDK cast or lossy Long conversion in production.
      expect((): void =>
        validateQueue(
          props as ReturnType<typeof projectQueue>,
          accepted,
          base,
          effective,
          [],
          present(initializedState.root.currentReviewId),
        ),
      ).toThrow(/version/);
    },
  );
  it.each(QUEUE_PROPERTY_KEYS)(
    "rejects corrupted or mixed queue field %s before serving a workspace",
    async (key): Promise<void> => {
      const state = stateCopy();
      const patch = {
        [key]: key === "queueNearestLegalDueDate" ? "1900-01-01" : "corrupt",
      };
      state.store.put(
        createMockOsdkObject(DcCloseoutCase, { ...state.root, ...patch }),
      );
      await expect(
        getCloseoutWorkspace(state.store.client, state.root.caseId),
      ).rejects.toThrow(/queue/i);
    },
  );
  it("rejects a version-only/all-nil versioned summary and mismatched generation even at equal clocks", (): void => {
    expect((): void =>
      validateQueue(
        { queueSummaryVersion: "1" },
        accepted,
        base,
        effective,
        [],
        "review",
      ),
    ).toThrow(/generation/);
    expect((): void =>
      validateQueue(
        project(),
        accepted,
        base,
        effective,
        [],
        "different-review",
      ),
    ).toThrow(/generation/);
    const next = structuredClone(accepted);
    next.snapshot.revision++;
    expect((): void =>
      validateQueue(
        project(),
        next,
        base,
        effective,
        [],
        present(initializedState.root.currentReviewId),
      ),
    ).toThrow(/generation/);
  });
  it.each(QUEUE_PROPERTY_KEYS)(
    "includes %s in the final root freshness check",
    async (key): Promise<void> => {
      const state = stateCopy();
      let count = 0;
      const changed = createMockOsdkObject(DcCloseoutCase, {
        ...state.root,
        [key]: undefined,
      });
      const finalRoot =
        state.root[key] === undefined
          ? createMockOsdkObject(DcCloseoutCase, {
              ...state.root,
              [key]: "changed",
            })
          : changed;
      const client = new Proxy(state.store.client, {
        apply: (target: Client, _this: unknown, args: unknown[]): unknown => {
          if (args[0] !== DcCloseoutCase)
            return Reflect.apply(target, undefined, args);
          return {
            fetchOne: async (
              id: string,
            ): Promise<Osdk.Instance<DcCloseoutCase>> =>
              ++count === 1 ? target(DcCloseoutCase).fetchOne(id) : finalRoot,
          };
        },
      });
      await expect(
        getCloseoutWorkspace(client, state.root.caseId),
      ).rejects.toMatchObject({ code: "GENERATION_CHANGED", retryable: true });
    },
  );
});

describe("existing financial/lifecycle engine remains the only calculator", (): void => {
  it("clears fulfilled legal deadlines after actual simulated dispatch, with zero money kept distinct from unknown", (): void => {
    const h = new RequestHarness();
    h.request.snapshot.charges = [];
    h.request.snapshot.depositBalance.amountCents = 0;
    const before = nativeReview(h.request);
    expect(
      projectQueue(
        h.request,
        before,
        reviewWorkflow(h.request, before, h.workflow, [], NOW),
        [],
        "before",
      ).queueNearestLegalDueDate,
    ).toBeDefined();
    const statementId = h.prepare();
    const id = h.admit({
      ...refundSpec(),
      kind: "STATEMENT_DISPATCH",
      amountCents: null,
      statementId,
    });
    h.settle(id, "zero-case-dispatch", null);
    const native = nativeReview(h.request);
    const review = reviewWorkflow(h.request, native, h.workflow, [], NOW);
    const props = projectQueue(h.request, native, review, [], "after");
    expect(props.queueNearestLegalDueDate).toBeUndefined();
    expect(props.queueAttentionKind).toBe("SIMULATED_COMPLETE");
    expect(json(props).account).toMatchObject({
      finalRefundCents: 0,
      newlyRequestableRefundCents: 0,
    });
    expect(json(props).completion).toMatchObject({
      simulatedOverallWorkflowComplete: true,
      legalPerformanceConfirmed: false,
    });
  });
  it.each([false, true])(
    "preserves unknown accounting and review-provided deadlines for qualified interim=%s",
    (qualified): void => {
      const h = new RequestHarness();
      const unresolved = baseRequest();
      h.request.snapshot.charges = unresolved.snapshot.charges;
      h.request.snapshot.questions = unresolved.snapshot.questions;
      if (qualified) {
        const updated = applyDecisionCommand(
          h.request,
          h.workflow,
          {
            kind: "SET_INTERIM_QUALIFICATION",
            payload: {
              state: "ACCEPTED",
              evidenceIds: ["ev-extent"],
              reason: WHY,
            },
          },
          requestContext("queue-interim"),
        );
        h.request = updated.request;
        h.workflow = updated.workflow;
      }
      const native = nativeReview(h.request);
      const review = reviewWorkflow(h.request, native, h.workflow, [], NOW);
      const props = projectQueue(h.request, native, review, [], "interim");
      expect(json(props).account).toMatchObject({
        finalRefundCents: null,
        totalDeductionsCents: null,
        finalAccountReady: false,
      });
      expect(json(props).nearestLegalDue).toMatchObject({
        requirementKey: qualified
          ? "NC:interim-account"
          : "NC:ordinary-account",
      });
      expect(json(props).completion).toMatchObject({
        simulatedOverallWorkflowComplete: false,
      });
    },
  );
  it("uses existing conflict flags even when the native reconciled balance has not changed", (): void => {
    const h = new RequestHarness();
    const id = h.admit();
    h.claim(id);
    h.raw(id, "failed", "FAILED");
    h.ingest("failed");
    h.raw(id, "contradictory-success");
    const native = nativeReview(h.request);
    const review = reviewWorkflow(h.request, native, h.workflow, [], NOW);
    expect(native.result.account.reconciliationState).toBe("RECONCILED");
    const props = projectQueue(h.request, native, review, [], "conflict");
    expect(props.queueAttentionKind).toBe("RECONCILIATION");
    expect(json(props).reconciliationRequestIds).toEqual([id]);
    expect(json(props).account).toMatchObject({
      finalRefundCents: native.result.account.finalRefundCents,
    });
    expect(json(props).availableActionKeys).toContain("prepare:statement");
    expect((): unknown => h.ingest("contradictory-success")).toThrow(
      /contradict/,
    );
  });
  it("copies accepted paid and corrected amounts without deducting reservations twice", (): void => {
    const h = new RequestHarness();
    const requestId = h.admit(refundSpec());
    const check = (): void => {
      const native = nativeReview(h.request);
      const review = reviewWorkflow(h.request, native, h.workflow, [], NOW);
      const props = projectQueue(h.request, native, review, [], "review");
      expect(json(props).account).toMatchObject({
        finalRefundCents: native.result.account.finalRefundCents,
        pendingReservedRefundCents:
          native.result.account.pendingReservedRefundCents,
        newlyRequestableRefundCents:
          review.result.account.newlyRequestableRefundCents,
      });
    };
    check();
    h.settle(requestId);
    check();
    h.request.snapshot.charges[0]!.chosenAmountCents = 200;
    check();
  });
  it("retains reconciliation and commitments for conflicting results without resolving them", (): void => {
    const h = new RequestHarness();
    const id = h.admit();
    h.claim(id);
    h.run(
      {
        kind: "RECORD_OUTCOME_UNKNOWN",
        payload: {
          requestId: id,
          attemptId: h.workflow.events.find(
            (event): boolean => event.kind === "ATTEMPT_CLAIMED",
          )!.attemptId!,
          reason: WHY,
        },
      },
      requestContext("unknown"),
    );
    const native = nativeReview(h.request);
    const review = reviewWorkflow(h.request, native, h.workflow, [], NOW);
    const before = canonical_json(h.workflow);
    const props = projectQueue(h.request, native, review, [], "review");
    expect(props.queueAttentionKind).toBe("RECONCILIATION");
    expect(json(props).reconciliationRequestIds).toEqual([id]);
    expect(canonical_json(h.workflow)).toBe(before);
    expect(json(props).account).toMatchObject({
      pendingReservedRefundCents:
        native.result.account.pendingReservedRefundCents,
    });
  });
});
