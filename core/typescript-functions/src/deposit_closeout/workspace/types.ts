/** Phase E.0/E.1a read transport only. No persisted schema or command changes. */
import type { ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import type {
  OperationIntent,
  OperationIntentSpec,
  WorkflowReviewV2,
  WorkflowStateV2,
} from "../lifecycle/types.js";
import type { WorkAssignment } from "../phase_c/change_types.js";

export const WORKSPACE_SCHEMA_VERSION = "1.0.0";
export const MAX_WORKSPACE_JSON_BYTES = 1024 * 1024;
export const MAX_INTENT_SPEC_JSON_BYTES = 4096;

export type IntentPreview =
  | { status: "NOT_REQUESTED" }
  | { status: "CONSTRUCTED"; spec: OperationIntentSpec; intent: OperationIntent }
  | {
      status: "BLOCKED";
      spec: OperationIntentSpec;
      reason: {
        code: "WORKFLOW_NOT_INITIALIZED" | "INTENT_CONSTRUCTION_BLOCKED";
        message: string;
      };
    };

export interface WorkspaceMetadata {
  schemaVersion: "1.0.0";
  caseId: string;
  managementCompanyId: "constructed-company-001";
  environmentId: "DC_PHASE_C_SYNTHETIC";
  homeId: string;
  tenancyId: string;
  /** SDK Long: canonical decimal string. request.snapshot.revision stays a safe JSON integer. */
  caseRevision: string;
  currentReviewId: string;
  inputHash: string;
  effectiveReviewHash: string;
  workAssignmentsHash: string;
  workflowStateHash: string | null;
  inputSchemaVersion: "1.0.0";
  reviewSchemaVersion: "1.1.0";
  codeVersion: "phase-b.1";
  ruleReleaseId: "NC_SYNTHETIC_REVIEW_V1";
  projectionVersion: "0" | "1";
  workflowVersion: "0" | "2";
  workflowSchemaVersion: "2.0.0" | null;
  reviewClock: string;
  snapshotCreatedAt: string;
  authorityEvaluatedAt: string;
  authorityEvaluationBasis: "LEGACY_REVIEW_CLOCK" | "RECORDED_SNAPSHOT_TIME";
  readAt: string;
  actionAvailabilityScope: "CASE_WIDE_NOT_ACTOR_AUTHORIZATION";
  intentPreviewSemantics: "TARGET_CONSTRUCTION_ONLY_NOT_AUTHORIZATION_OR_RESERVATION";
}

export type WorkspaceReview =
  { kind: "LEGACY_BASE"; value: ReviewEnvelope } | { kind: "WORKFLOW_V2"; value: WorkflowReviewV2 };

export interface CloseoutWorkspaceV1 {
  metadata: WorkspaceMetadata;
  request: ReviewRequest;
  workAssignments: WorkAssignment[];
  workflow: WorkflowStateV2 | null;
  /** Exactly one effective review; never duplicate base and workflow envelopes. */
  review: WorkspaceReview;
  intentPreview: IntentPreview;
}

export type WorkspaceErrorCode = "INVALID_INTENT_SPEC" | "INVALID_WORKSPACE" | "GENERATION_CHANGED";
