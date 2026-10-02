/** Private, pure organizational display projection. Never a second business/financial reducer. */
import type { DcCloseoutCase } from "@ontology/sdk";
import { canonical_json } from "../domain/codec.js";
import { compare_timestamps, normalize_timestamp } from "../domain/datetime.js";
import { fingerprint } from "../domain/fingerprints.js";
import type {
  AvailableAction,
  RequirementResult,
  ReviewEnvelope,
  ReviewRequest,
} from "../domain/types.js";
import type { CurrentRequest, WorkflowReviewV2 } from "../lifecycle/types.js";
import type { WorkAssignment } from "../phase_c/change_types.js";
import { ENVIRONMENT_ID } from "../phase_c/types.js";
import { requireCondition } from "../phase_c/validation.js";

export const QUEUE_SUMMARY_VERSION = "1";
export const MAX_QUEUE_JSON_BYTES = 32 * 1024;
export const QUEUE_PROPERTY_KEYS = [
  "queueSummaryVersion",
  "queueAttentionKind",
  "queueNearestLegalDueDate",
  "queueNearestInternalTargetAtIso",
  "queueNextRequirementKey",
  "queueNextResponsibleRole",
  "queueNextAssigneePartyId",
  "queueSummaryJson",
] as const;
const DONE = new Set(["FULFILLED", "NOT_APPLICABLE"]);
const LABELS = {
  RECONCILIATION: "Reconciliation needs attention",
  UNSUPPORTED_SCOPE: "Scope needs specialist review",
  NEEDS_FACTS_OR_DECISION: "Facts or a decision are needed",
  LEGACY_INITIALIZATION: "Workflow initialization is needed",
  READY_WORK: "Supported work is available",
  WAITING: "Waiting on prerequisites or results",
  SIMULATED_COMPLETE: "Simulated workflow complete — not legal performance",
} as const;
type AttentionKind = keyof typeof LABELS;
type QueueProperties = Pick<
  DcCloseoutCase.Props,
  (typeof QUEUE_PROPERTY_KEYS)[number]
>;

export interface QueueNextWork {
  workKey: string;
  requirementKey: string | null;
  question: string;
  responsibleRole: string;
  assigneePartyId: string | null;
  actionKey: string | null;
  selectionBasis:
    | "RECONCILIATION"
    | "SCOPE"
    | "INITIALIZATION"
    | "AVAILABLE_ACTION"
    | "MISSING_INPUT"
    | "OPEN_REQUIREMENT";
}

function text(left: string, right: string): number {
  return left < right ? -1 : left > right ? 1 : 0;
}
function fixedTimestamp(value: string): string {
  const normalized = normalize_timestamp(value);
  requireCondition(
    normalized !== null,
    "Queue internal target must be an explicit UTC timestamp.",
  );
  return normalized.length === 20
    ? `${normalized.slice(0, -1)}.000000Z`
    : normalized;
}
function actionRank(action: AvailableAction): number {
  if (action.actionKey.startsWith("reconcile:")) return 0;
  if (action.actionKey.startsWith("claim:")) return 1;
  if (action.actionKey.startsWith("request:")) return 2;
  if (action.actionKey.startsWith("approve:")) return 3;
  if (action.actionKey === "prepare:statement") return 4;
  return 5;
}

/** The same request detail appears on several actions. Deduplicate IDs, never sum repeated amounts. */
function requestDetails(
  review: WorkflowReviewV2 | undefined,
): CurrentRequest[] {
  const byId = new Map<string, CurrentRequest>();
  review?.result.actions.forEach((action): void =>
    action.workflow?.requestDetails.forEach((entry): void => {
      const previous = byId.get(entry.requestId);
      requireCondition(
        previous === undefined ||
          canonical_json(previous) === canonical_json(entry),
        "Queue request details disagree within the effective review.",
      );
      byId.set(entry.requestId, entry);
    }),
  );
  return [...byId.values()].sort((a, b): number =>
    text(a.requestId, b.requestId),
  );
}

/**
 * Project only accepted request + authoritative effective review + work assignments.
 * @param request Accepted native state, with the revision to be persisted.
 * @param base Validated native review (used only for a known uninitialized workflow).
 * @param workflowReview Validated v2 review at the snapshot authority clock, when initialized.
 * @param assignments Validated organizational assignments, including retained history.
 * @param currentReviewId The exact pointer returned by appendReviewAndReceipt (or the loaded root).
 * @returns Bounded canonical summary plus explicitly clearable root properties. No wall-clock reads.
 */
export function projectQueue(
  request: ReviewRequest,
  base: ReviewEnvelope,
  workflowReview: WorkflowReviewV2 | undefined,
  assignments: readonly WorkAssignment[],
  currentReviewId: string,
): QueueProperties {
  const review = workflowReview ?? base;
  const result = review.result;
  const a = result.account;
  const open = result.scopeRequirements.requirements.filter(
    (entry): boolean => !DONE.has(entry.state),
  );
  const byAssignment = new Map(
    assignments.map((entry) => [entry.requirementKey, entry]),
  );
  const target = (entry: RequirementResult): string | null => {
    const assignment = byAssignment.get(entry.requirementKey);
    return assignment === undefined
      ? entry.internalTargetAt
      : assignment.internalTargetAt;
  };
  const legal = open
    .filter(
      (entry): boolean =>
        entry.dueKind === "LEGAL" && entry.legalDueDate !== null,
    )
    .sort(
      (x, y): number =>
        text(x.legalDueDate!, y.legalDueDate!) ||
        text(x.requirementKey, y.requirementKey),
    )[0];
  const internal = open
    .filter((entry): boolean => target(entry) !== null)
    .sort(
      (x, y): number =>
        compare_timestamps(target(x)!, target(y)!) ||
        text(x.requirementKey, y.requirementKey),
    )[0];
  const ordered = [...open].sort((x, y): number => {
    const xDate = x.dueKind === "LEGAL" ? x.legalDueDate : null;
    const yDate = y.dueKind === "LEGAL" ? y.legalDueDate : null;
    if (xDate !== yDate)
      return xDate === null ? 1 : yDate === null ? -1 : text(xDate, yDate);
    const xTarget = target(x),
      yTarget = target(y);
    if (xTarget !== yTarget)
      return xTarget === null
        ? 1
        : yTarget === null
          ? -1
          : compare_timestamps(xTarget, yTarget) ||
            text(x.requirementKey, y.requirementKey);
    return text(x.requirementKey, y.requirementKey);
  });
  const currentRequests = requestDetails(workflowReview);
  const reconcileIds = currentRequests
    .filter(
      (entry): boolean =>
        entry.reconciliationRequired || entry.state === "OUTCOME_UNKNOWN",
    )
    .map((entry): string => entry.requestId);
  const needsReconciliation =
    reconcileIds.length > 0 ||
    a.reconciliationState !== "RECONCILED" ||
    request.snapshot.priorRequests.some(
      (entry): boolean => entry.state === "OUTCOME_UNKNOWN",
    ) ||
    result.missingInputs.some((entry): boolean =>
      entry.questionId.startsWith("money:"),
    );
  const unsupported = ["UNSUPPORTED", "INTERPRETATION_REQUIRED"].includes(
    result.scopeRequirements.scopeState,
  );
  const needsFacts =
    result.missingInputs.length > 0 ||
    result.itemDecisions.some((entry): boolean => entry.requiresReviewer) ||
    result.scopeRequirements.scopeState === "MISSING_FACTS";
  // Maintenance/recheck and general fact correction are not execution readiness.
  const available = result.actions
    .filter(
      (entry): boolean =>
        entry.availability === "AVAILABLE" &&
        entry.actionKey !== "review:repeat" &&
        entry.actionKey !== "prepare:correct-facts",
    )
    .sort(
      (x, y): number =>
        actionRank(x) - actionRank(y) || text(x.actionKey, y.actionKey),
    );
  const simulatedComplete =
    workflowReview?.result.outcomes.simulatedOverallWorkflowComplete === true;
  let kind: AttentionKind = "WAITING";
  if (needsReconciliation) kind = "RECONCILIATION";
  else if (unsupported) kind = "UNSUPPORTED_SCOPE";
  else if (needsFacts) kind = "NEEDS_FACTS_OR_DECISION";
  else if (workflowReview === undefined) kind = "LEGACY_INITIALIZATION";
  else if (simulatedComplete) kind = "SIMULATED_COMPLETE";
  else if (available.length > 0) kind = "READY_WORK";

  const nextFor = (
    requirement: RequirementResult | undefined,
    action: AvailableAction | undefined,
    basis: QueueNextWork["selectionBasis"],
  ): QueueNextWork | null => {
    if (requirement === undefined && action === undefined) return null;
    return {
      workKey: requirement?.requirementKey ?? `action:${action!.actionKey}`,
      requirementKey: requirement?.requirementKey ?? null,
      question:
        requirement?.question ?? `Review supported action ${action!.actionKey}`,
      responsibleRole: action?.responsibleRole ?? requirement!.responsibleRole,
      assigneePartyId:
        requirement === undefined
          ? null
          : (byAssignment.get(requirement.requirementKey)?.assigneePartyId ??
            null),
      actionKey: action?.actionKey ?? null,
      selectionBasis: basis,
    };
  };
  const requirementForAction = (
    action: AvailableAction,
  ): RequirementResult | undefined => {
    if (action.actionKey.startsWith("approve:"))
      return open.find(
        (entry): boolean => entry.requirementKey === "approval:current-version",
      );
    const detail = workflowReview?.result.actions.find(
      (entry): boolean => entry.actionKey === action.actionKey,
    )?.workflow;
    if (detail !== null && detail !== undefined)
      return ordered.find((entry): boolean =>
        detail.operationKind === "STATEMENT_DISPATCH"
          ? entry.track === "COMMUNICATIONS"
          : entry.requirementKey === "money:outstanding-work",
      );
    if (action.actionKey === "prepare:statement")
      return ordered.find((entry): boolean => entry.track === "COMMUNICATIONS");
    if (action.actionKey === "reconcile:money")
      return open.find(
        (entry): boolean => entry.requirementKey === "money:outstanding-work",
      );
    return ordered.find((entry): boolean =>
      entry.prerequisiteIds.some((id): boolean =>
        action.prerequisiteIds.includes(id),
      ),
    );
  };
  let nextWork: QueueNextWork | null = null;
  if (needsReconciliation) {
    const action = [...available, ...result.actions].find(
      (entry): boolean =>
        entry.actionKey.startsWith("reconcile:") &&
        (reconcileIds.includes(entry.actionKey.slice("reconcile:".length)) ||
          entry.actionKey === "reconcile:money"),
    );
    nextWork = nextFor(
      action === undefined
        ? open.find(
            (entry): boolean =>
              entry.requirementKey === "money:outstanding-work",
          )
        : requirementForAction(action),
      action,
      "RECONCILIATION",
    );
  } else if (unsupported) {
    nextWork = nextFor(
      open.find(
        (entry): boolean =>
          entry.requirementKey === "prepare:scope-and-trigger",
      ),
      undefined,
      "SCOPE",
    );
  } else if (kind === "LEGACY_INITIALIZATION") {
    nextWork = {
      workKey: "workflow:initialize",
      requirementKey: null,
      question: "Initialize the synthetic workflow before operation execution",
      responsibleRole: "AUTHORITY_ADMIN",
      assigneePartyId: null,
      actionKey: null,
      selectionBasis: "INITIALIZATION",
    };
  } else if (!simulatedComplete && available[0] !== undefined) {
    nextWork = nextFor(
      requirementForAction(available[0]),
      available[0],
      "AVAILABLE_ACTION",
    );
  }
  if (nextWork === null && !simulatedComplete) {
    const missing = new Set(
      result.missingInputs.map(
        (entry): string => `question:${entry.questionId}`,
      ),
    );
    const requirement = ordered.find((entry): boolean =>
      missing.has(entry.requirementKey),
    );
    nextWork = nextFor(
      requirement ?? ordered[0],
      undefined,
      requirement === undefined ? "OPEN_REQUIREMENT" : "MISSING_INPUT",
    );
  }
  const queue = {
    schemaVersion: "1.0.0",
    metadata: {
      caseId: request.snapshot.caseId,
      managementCompanyId: request.snapshot.managementCompanyId,
      environmentId: ENVIRONMENT_ID,
      homeId: request.snapshot.homeId,
      tenancyId: request.snapshot.tenancyId,
      caseRevision: String(request.snapshot.revision),
      currentReviewId,
      reviewClock: request.reviewClock,
      inputHash: review.metadata.inputHash,
      effectiveReviewHash: fingerprint(review),
      workAssignmentsHash: fingerprint(assignments),
      effectiveReviewKind:
        workflowReview === undefined ? "LEGACY_BASE" : "WORKFLOW_V2",
    },
    scopeState: result.scopeRequirements.scopeState,
    attention: { kind, label: LABELS[kind], reasonCode: kind },
    nearestLegalDue:
      legal === undefined
        ? null
        : {
            requirementKey: legal.requirementKey,
            date: legal.legalDueDate,
            dueKind: legal.dueKind,
            ruleQuestionId: legal.ruleQuestionId,
            triggerFactKeys: legal.triggerFactKeys,
          },
    nearestInternalTarget:
      internal === undefined
        ? null
        : {
            requirementKey: internal.requirementKey,
            atIso: fixedTimestamp(target(internal)!),
          },
    nextWork,
    availableActionKeys: [
      ...new Set(available.map((entry): string => entry.actionKey)),
    ].sort(text),
    reconciliationRequestIds: reconcileIds,
    account: {
      currency: a.currency,
      recordedDepositCents: a.recordedDepositCents,
      knownChosenDeductionsCents: a.knownChosenDeductionsCents,
      totalDeductionsCents: a.totalDeductionsCents,
      existingNetPostingCents: a.existingNetPostingCents,
      postingDeltaCents: a.postingDeltaCents,
      existingDepositApplicationsCents: a.existingDepositApplicationsCents,
      depositApplicationDeltaCents: a.depositApplicationDeltaCents,
      priorNetRefundsCents: a.priorNetRefundsCents,
      pendingReservedRefundCents: a.pendingReservedRefundCents,
      finalRefundCents: a.finalRefundCents,
      proposedExcessReceivableCents: a.proposedExcessReceivableCents,
      newlyRequestableRefundCents:
        workflowReview?.result.account.newlyRequestableRefundCents ?? null,
      finalAccountReady: a.finalAccountReady,
      reconciliationState: a.reconciliationState,
    },
    tracks: result.outcomes.tracks.map((entry) => ({
      track: entry.track,
      state: entry.state,
    })),
    completion: {
      simulatedDepositWorkflowComplete:
        workflowReview?.result.outcomes.simulatedDepositWorkflowComplete ??
        false,
      simulatedOverallWorkflowComplete:
        workflowReview?.result.outcomes.simulatedOverallWorkflowComplete ??
        false,
      depositComplete: false,
      overallCaseComplete: false,
      legalPerformanceConfirmed: false,
      mode: "SIMULATED",
    },
  };
  const queueSummaryJson = canonical_json(queue);
  requireCondition(
    Buffer.byteLength(queueSummaryJson, "utf8") <= MAX_QUEUE_JSON_BYTES,
    "Queue summary exceeds the supported UTF-8 bound; no partial command or truncated summary was produced.",
  );
  return {
    queueSummaryVersion: QUEUE_SUMMARY_VERSION,
    queueAttentionKind: kind,
    queueNearestLegalDueDate: legal?.legalDueDate ?? undefined,
    queueNearestInternalTargetAtIso:
      queue.nearestInternalTarget?.atIso ?? undefined,
    queueNextRequirementKey: nextWork?.requirementKey ?? undefined,
    queueNextResponsibleRole: nextWork?.responsibleRole ?? undefined,
    queueNextAssigneePartyId: nextWork?.assigneePartyId ?? undefined,
    queueSummaryJson,
  };
}

/** Only all-absent is pre-E. Partial, unknown, stale or mixed generations fail closed; reads never repair. */
export function validateQueue(
  root: Partial<QueueProperties>,
  request: ReviewRequest,
  base: ReviewEnvelope,
  workflowReview: WorkflowReviewV2 | undefined,
  assignments: readonly WorkAssignment[],
  currentReviewId: string,
): void {
  if (QUEUE_PROPERTY_KEYS.every((key): boolean => root[key] === undefined))
    return;
  requireCondition(
    root.queueSummaryVersion === QUEUE_SUMMARY_VERSION,
    "Unknown or partial queue summary version.",
  );
  const expected = projectQueue(
    request,
    base,
    workflowReview,
    assignments,
    currentReviewId,
  );
  requireCondition(
    QUEUE_PROPERTY_KEYS.every((key): boolean => root[key] === expected[key]),
    "Stored queue summary differs from the accepted current review generation.",
  );
}
