/** Strict bounded transport, composed from the existing native/workflow codecs. */
import { UserFacingError } from "@osdk/functions";
import {
  canonical_json,
  ContractError,
  from_wire,
  is_plain_object,
  parse_json,
} from "../domain/codec.js";
import { fingerprint } from "../domain/fingerprints.js";
import type { ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import { buildIntent } from "../lifecycle/approvals.js";
import {
  parseLifecycleCommand,
  parseWorkflowReview,
  parseWorkflowSnapshot,
  parseWorkflowState,
  parseWorkflowTimestamp,
  validateWorkflowCaseReferences,
} from "../lifecycle/codec.js";
import { projectNativeFacts } from "../lifecycle/requests.js";
import { reviewWorkflow } from "../lifecycle/review.js";
import type { OperationIntentSpec, WorkflowStateV2 } from "../lifecycle/types.js";
import type { WorkAssignment } from "../phase_c/change_types.js";
import { COMPANY_ID, ENVIRONMENT_ID, MAX_PAYLOAD_BYTES } from "../phase_c/types.js";
import { checkedLong, nativeReview, validateRequest } from "../phase_c/validation.js";
import { loadWorkAssignments } from "../phase_c/work_assignments.js";
import {
  MAX_INTENT_SPEC_JSON_BYTES,
  MAX_WORKSPACE_JSON_BYTES,
  WORKSPACE_SCHEMA_VERSION,
  type CloseoutWorkspaceV1,
  type IntentPreview,
  type WorkspaceErrorCode,
  type WorkspaceMetadata,
  type WorkspaceReview,
} from "./types.js";

export class WorkspaceError extends UserFacingError {
  public readonly retryable: boolean;
  public constructor(
    public readonly code: WorkspaceErrorCode,
    message: string,
  ) {
    super(`Closeout workspace [${code}]: ${message}`);
    this.retryable = code === "GENERATION_CHANGED";
  }
}

/** Translate only known contract failures; never hide SDK, access or programming errors. */
export function workspaceContract<T>(
  code: "INVALID_INTENT_SPEC" | "INVALID_WORKSPACE",
  operation: () => T,
): T {
  try {
    return operation();
  } catch (error: unknown) {
    if (!(error instanceof ContractError) && !(error instanceof UserFacingError)) throw error;
    throw new WorkspaceError(code, error.message);
  }
}

function check(condition: boolean, message: string): asserts condition {
  if (!condition) throw new ContractError(message);
}
function object(value: unknown, keys: readonly string[], path: string): Record<string, unknown> {
  check(
    is_plain_object(value) &&
      Object.keys(value).length === keys.length &&
      keys.every((key): boolean => Object.hasOwn(value, key)),
    `${path}: expected exact fields`,
  );
  return value;
}
function bounded(json: string, maximum: number, label: string): string {
  check(
    typeof json === "string" && Buffer.byteLength(json, "utf8") <= maximum,
    `${label}: exceeds ${maximum} UTF-8 bytes; never truncated`,
  );
  return json;
}

/** Wrap only for the existing strict decoder; this does NOT execute a command or decision. */
export function parseIntentSpec(json: string): OperationIntentSpec {
  const raw = parse_json(bounded(json, MAX_INTENT_SPEC_JSON_BYTES, "Intent spec"));
  const command = parseLifecycleCommand(
    "DECIDE_APPROVAL",
    canonical_json({ intent: raw, decision: "APPROVED" }),
  );
  if (command.kind !== "DECIDE_APPROVAL")
    throw new ContractError("Expected the intent-spec decoder");
  return command.payload.intent;
}

/** Target construction only: no actor, current authority, request admission, reservation or edit batch. */
export function previewIntent(
  request: ReviewRequest,
  base: ReviewEnvelope,
  workflow: WorkflowStateV2 | null,
  spec: OperationIntentSpec | undefined,
): IntentPreview {
  if (spec === undefined) return { status: "NOT_REQUESTED" };
  if (workflow === null)
    return {
      status: "BLOCKED",
      spec,
      reason: {
        code: "WORKFLOW_NOT_INITIALIZED",
        message: "Initialize the workflow before constructing an operation target.",
      },
    };
  try {
    return { status: "CONSTRUCTED", spec, intent: buildIntent(request, base, workflow, spec) };
  } catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    return {
      status: "BLOCKED",
      spec,
      reason: { code: "INTENT_CONSTRUCTION_BLOCKED", message: error.message },
    };
  }
}

interface MetadataBasis {
  caseRevision: string;
  currentReviewId: string;
  projectionVersion: "0" | "1";
  snapshotCreatedAt: string;
  readAt: string;
}

export function workspaceMetadata(
  request: ReviewRequest,
  review: WorkspaceReview,
  workflow: WorkflowStateV2 | null,
  assignments: WorkAssignment[],
  basis: MetadataBasis,
): WorkspaceMetadata {
  check(
    checkedLong(basis.caseRevision, "Workspace revision", 1n) === request.snapshot.revision,
    "Workspace revision differs from the accepted safe-native revision",
  );
  check(/^dc-review:[a-f0-9]{64}$/.test(basis.currentReviewId), "Invalid current review pointer");
  check(
    request.snapshot.managementCompanyId === COMPANY_ID &&
      request.snapshot.schemaVersion === "1.0.0" &&
      review.value.metadata.schemaVersion === "1.1.0" &&
      review.value.metadata.codeVersion === "phase-b.1" &&
      request.ruleReleaseId === "NC_SYNTHETIC_REVIEW_V1",
    "Unknown workspace component version or scope",
  );
  return {
    schemaVersion: WORKSPACE_SCHEMA_VERSION,
    caseId: request.snapshot.caseId,
    managementCompanyId: COMPANY_ID,
    environmentId: ENVIRONMENT_ID,
    homeId: request.snapshot.homeId,
    tenancyId: request.snapshot.tenancyId,
    caseRevision: basis.caseRevision,
    currentReviewId: basis.currentReviewId,
    inputHash: review.value.metadata.inputHash,
    effectiveReviewHash: fingerprint(review.value),
    workAssignmentsHash: fingerprint(assignments),
    workflowStateHash: workflow === null ? null : fingerprint(workflow),
    inputSchemaVersion: "1.0.0",
    reviewSchemaVersion: "1.1.0",
    codeVersion: "phase-b.1",
    ruleReleaseId: "NC_SYNTHETIC_REVIEW_V1",
    projectionVersion: basis.projectionVersion,
    workflowVersion: workflow === null ? "0" : "2",
    workflowSchemaVersion: workflow === null ? null : "2.0.0",
    reviewClock: parseWorkflowTimestamp(request.reviewClock),
    snapshotCreatedAt: parseWorkflowTimestamp(basis.snapshotCreatedAt),
    authorityEvaluatedAt:
      review.kind === "WORKFLOW_V2"
        ? review.value.metadata.authorityEvaluatedAt
        : request.reviewClock,
    authorityEvaluationBasis:
      review.kind === "WORKFLOW_V2" ? "RECORDED_SNAPSHOT_TIME" : "LEGACY_REVIEW_CLOCK",
    readAt: parseWorkflowTimestamp(basis.readAt),
    actionAvailabilityScope: "CASE_WIDE_NOT_ACTOR_AUTHORIZATION",
    intentPreviewSemantics: "TARGET_CONSTRUCTION_ONLY_NOT_AUTHORIZATION_OR_RESERVATION",
  };
}

/** Public transport decoder: exact keys, component bounds, known versions, scope and hashes. */
export function parseWorkspace(json: string): CloseoutWorkspaceV1 {
  const raw = object(
    parse_json(bounded(json, MAX_WORKSPACE_JSON_BYTES, "Workspace")),
    ["metadata", "request", "workAssignments", "workflow", "review", "intentPreview"],
    "Workspace",
  );
  canonical_json(raw); // Reject malformed Unicode, including in native nested payloads.
  const request = from_wire("ReviewRequest", raw.request);
  bounded(canonical_json(request), MAX_PAYLOAD_BYTES, "Accepted request");
  validateRequest(request);
  const base = nativeReview(request);
  check(is_plain_object(raw.metadata), "Expected workspace metadata");
  const m = raw.metadata;
  check(
    typeof m.caseRevision === "string" &&
      typeof m.currentReviewId === "string" &&
      (m.projectionVersion === "0" || m.projectionVersion === "1"),
    "Invalid workspace revision/version fields",
  );
  const snapshotCreatedAt = parseWorkflowTimestamp(m.snapshotCreatedAt);
  const readAt = parseWorkflowTimestamp(m.readAt);
  const assignmentsJson = bounded(
    canonical_json(raw.workAssignments),
    MAX_PAYLOAD_BYTES,
    "Work assignments",
  );
  check(
    m.projectionVersion !== "0" || assignmentsJson === "[]",
    "Legacy projection cannot have assignments",
  );
  const workAssignments = loadWorkAssignments(
    m.projectionVersion === "0" ? undefined : assignmentsJson,
    m.projectionVersion === "0" ? undefined : fingerprint(raw.workAssignments),
    m.projectionVersion,
    request,
    snapshotCreatedAt,
  );
  const rawReview = object(raw.review, ["kind", "value"], "Workspace review");
  let workflow: WorkflowStateV2 | null;
  let review: WorkspaceReview;
  if (rawReview.kind === "LEGACY_BASE") {
    check(raw.workflow === null, "Legacy base review cannot accompany workflow state");
    workflow = null;
    const value = from_wire("ReviewEnvelope", rawReview.value);
    bounded(canonical_json(value), MAX_PAYLOAD_BYTES, "Legacy review");
    check(
      canonical_json(value) === canonical_json(base),
      "Legacy review differs from the accepted native request",
    );
    review = { kind: "LEGACY_BASE", value };
  } else {
    check(rawReview.kind === "WORKFLOW_V2", "Unknown effective review kind");
    workflow = parseWorkflowState(canonical_json(raw.workflow));
    const value = parseWorkflowReview(canonical_json(rawReview.value));
    parseWorkflowSnapshot(
      "2",
      {
        workflowStateJson: canonical_json(workflow),
        workflowStateHash: fingerprint(workflow),
        workflowReviewJson: canonical_json(value),
        workflowReviewHash: fingerprint(value),
      },
      snapshotCreatedAt,
    );
    validateWorkflowCaseReferences(workflow, request.snapshot);
    check(
      canonical_json(projectNativeFacts(request, workflow)) === canonical_json(request),
      "Workflow facts differ from accepted request",
    );
    check(
      canonical_json(value) ===
        canonical_json(reviewWorkflow(request, base, workflow, workAssignments, snapshotCreatedAt)),
      "Effective workflow review differs from its recorded basis",
    );
    review = { kind: "WORKFLOW_V2", value };
  }
  const metadata = workspaceMetadata(request, review, workflow, workAssignments, {
    caseRevision: m.caseRevision,
    currentReviewId: m.currentReviewId,
    projectionVersion: m.projectionVersion,
    snapshotCreatedAt,
    readAt,
  });
  check(
    canonical_json(m) === canonical_json(metadata),
    "Workspace metadata fields, versions, clocks or hashes differ",
  );
  check(is_plain_object(raw.intentPreview), "Expected intent preview");
  const spec =
    raw.intentPreview.status === "NOT_REQUESTED"
      ? undefined
      : parseIntentSpec(canonical_json(raw.intentPreview.spec));
  const intentPreview = previewIntent(request, base, workflow, spec);
  check(
    canonical_json(raw.intentPreview) === canonical_json(intentPreview),
    "Intent preview is not the exact construction result",
  );
  return { metadata, request, workAssignments, workflow, review, intentPreview };
}

export function serializeWorkspace(workspace: CloseoutWorkspaceV1): string {
  const json = bounded(canonical_json(workspace), MAX_WORKSPACE_JSON_BYTES, "Workspace");
  const validated = canonical_json(parseWorkspace(json));
  check(json === validated, "Workspace must be canonical without coercion or omitted fields");
  return bounded(validated, MAX_WORKSPACE_JSON_BYTES, "Workspace");
}
