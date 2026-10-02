import type { DcChargeItem, DcCloseoutCase, DcExecutionEvent, DcReviewSnapshot,
  DcEvidenceRecord, DcMoneyEvent, DcCaseParty, DcRequirement, DcStatementVersion, DcApproval, DcActionRequest } from "@ontology/sdk";
import type { Edits, Long } from "@osdk/functions";
import type { ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import type { WorkflowStateV2, WorkflowReviewV2 } from "../lifecycle/types.js";
import type { WorkAssignment } from "./change_types.js";
import { fingerprint } from "../domain/fingerprints.js";

export type OntologyEdit =
  | Edits.Object<DcCloseoutCase>
  | Edits.Object<DcReviewSnapshot>
  | Edits.Object<DcExecutionEvent>
  | Edits.Object<DcChargeItem>
  | Edits.Object<DcEvidenceRecord>
  | Edits.Object<DcMoneyEvent>
  | Edits.Object<DcCaseParty>
  | Edits.Object<DcRequirement>
  | Edits.Object<DcStatementVersion>
  | Edits.Object<DcApproval>
  | Edits.Object<DcActionRequest>;

export const ENVIRONMENT_ID = "DC_PHASE_C_SYNTHETIC";
export const COMPANY_ID = "constructed-company-001";
export const BOOTSTRAP_ACTOR_ID = "c47a52a0-0048-4607-931f-f4df283ae7c4";
export const MAX_PAYLOAD_BYTES = 256 * 1024;
export const OPEN_COMMAND = "OPEN_CLOSEOUT_CASE";
export const CHOOSE_COMMAND = "CHOOSE_CLOSEOUT_CHARGE";
export const PROJECTION_VERSION = "1";

export interface StoredReview {
  request: ReviewRequest;
  review: ReviewEnvelope;
  reviewJson: string;
  workAssignments: WorkAssignment[];
  createdAt?: string;
  workflow?: WorkflowStateV2;
  workflowReview?: WorkflowReviewV2;
  workflowReviewJson?: string;
}

export interface CommandIdentity {
  caseId: string;
  managementCompanyId: string;
  actorId: string;
  commandId: string;
  commandKind: string;
  payloadHash: string;
  previousRevision: Long;
  /** Canonical operational intent, not a trusted input to subsequent commands. */
  commandJson?: string;
}

/** One case per company/ending tenancy, independent of retries or command IDs. */
export function caseIdFor(managementCompanyId: string, tenancyId: string): string {
  return `dc-case:${fingerprint({ environmentId: ENVIRONMENT_ID, managementCompanyId, tenancyId })}`;
}

/** Command kind is deliberately absent: reusing an ID for a different command conflicts. */
export function receiptIdFor(managementCompanyId: string, caseId: string, commandId: string): string {
  return `dc-command:${fingerprint({ environmentId: ENVIRONMENT_ID, managementCompanyId, caseId, commandId })}`;
}

/** Include the command so two contenders for revision R+1 cannot hide a lost update. */
export function reviewIdFor(managementCompanyId: string, caseId: string, revision: Long, commandId: string): string {
  return `dc-review:${fingerprint({ environmentId: ENVIRONMENT_ID, managementCompanyId, caseId, revision, commandId })}`;
}

export function chargeIdFor(managementCompanyId: string, caseId: string, itemId: string): string {
  return `dc-charge:${fingerprint({ environmentId: ENVIRONMENT_ID, managementCompanyId, caseId, itemId })}`;
}

export function projectionIdFor(kind: "evidence" | "money" | "party" | "requirement",
  managementCompanyId: string, caseId: string, localId: string): string {
  return `dc-${kind}:${fingerprint({ environmentId: ENVIRONMENT_ID, managementCompanyId, caseId, localId })}`;
}
