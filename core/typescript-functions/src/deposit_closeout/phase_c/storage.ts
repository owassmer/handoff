import { DcCloseoutCase, DcExecutionEvent, DcReviewSnapshot } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import type { EditBatch, Long } from "@osdk/functions";
import { canonical_json } from "../domain/codec.js";
import { normalize_timestamp } from "../domain/datetime.js";
import { fingerprint } from "../domain/fingerprints.js";
import { loadWorkflowSnapshot } from "../lifecycle/storage.js";
import { LIFECYCLE_COMMAND_KINDS, type WorkflowSnapshotExtras } from "../lifecycle/types.js";
import { loadWorkAssignments } from "./work_assignments.js";
import { validateQueue } from "../workspace/queue.js";
import type { WorkAssignment } from "./change_types.js";
import type { ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import {
  BOOTSTRAP_ACTOR_ID, CHOOSE_COMMAND, OPEN_COMMAND, ENVIRONMENT_ID, receiptIdFor, reviewIdFor,
  type CommandIdentity, type OntologyEdit, type StoredReview,
} from "./types.js";
import {
  checkedLong, nativeReview, parseRequest, parseReview, requireCondition, sameInstant,
  sameReaders, serialize, validateRequest, validateRoot,
} from "./validation.js";

/** Only the documented Ontologies ObjectNotFound response is optional.
 * NOTE: Foundry may mask an inaccessible object as ObjectNotFound. This is not a
 * uniqueness lock; Action create/collision behavior must be verified on-platform.
 * Permission, transport, timeout and generic 404 errors always propagate.
 */
export async function optionalObject<T>(lookup: Promise<T>): Promise<T | undefined> {
  try {
    return await lookup;
  } catch (error: unknown) {
    if (error instanceof Error && "errorName" in error && error.errorName === "ObjectNotFound"
      && "errorCode" in error && error.errorCode === "NOT_FOUND"
      && "statusCode" in error && error.statusCode === 404) return undefined;
    throw error;
  }
}

interface PkPage<T> {
  data: readonly T[];
  nextPageToken?: string;
}

async function oneOrAbsent<T extends { $primaryKey: string }>(
  lookup: Promise<PkPage<T>>, primaryKey: string,
): Promise<T | undefined> {
  const page = await optionalObject(lookup);
  if (page === undefined) return undefined;
  requireCondition(page.data.length <= 1 && page.nextPageToken === undefined,
    "Primary-key lookup returned an ambiguous result.");
  const object = page.data[0];
  requireCondition(object === undefined || object.$primaryKey === primaryKey,
    "Primary-key lookup returned a different object.");
  return object;
}

/** Exact indexed PK queries return explicit empty pages on the branch. The local
 * SDK's fetchOne instead throws an unclassified 'Expected a single result' error
 * for zero rows; that error must NOT be caught or message-matched as absence.
 */
export function findCaseByPk(client: Client, caseId: string): Promise<Osdk.Instance<DcCloseoutCase> | undefined> {
  return oneOrAbsent(client(DcCloseoutCase).where({ caseId: { $eq: caseId } })
    .fetchPage({ $pageSize: 2 }), caseId);
}

export function findReceiptByPk(client: Client, eventId: string): Promise<Osdk.Instance<DcExecutionEvent> | undefined> {
  return oneOrAbsent(client(DcExecutionEvent).where({ eventId: { $eq: eventId } })
    .fetchPage({ $pageSize: 2 }), eventId);
}

/** Validate the full JSON and rerun the unchanged native core, never a child projection. */
export async function loadCurrentReview(client: Client, root: Osdk.Instance<DcCloseoutCase>): Promise<StoredReview> {
  const revision = validateRoot(root);
  const snapshot = await client(DcReviewSnapshot).fetchOne(root.currentReviewId!);
  requireCondition(snapshot.reviewId === root.currentReviewId && snapshot.$primaryKey === snapshot.reviewId
    && snapshot.caseId === root.caseId && snapshot.managementCompanyId === root.managementCompanyId
    && snapshot.environmentId === ENVIRONMENT_ID && snapshot.caseRevision === root.revision
    && snapshot.inputHash === root.inputHash && snapshot.createdBy === BOOTSTRAP_ACTOR_ID
    && typeof snapshot.createdAt === "string" && normalize_timestamp(snapshot.createdAt) !== null
    && sameInstant(snapshot.createdAt, root.updatedAt!)
    && sameReaders(snapshot.readerIds)
    && typeof snapshot.requestJson === "string" && typeof snapshot.reviewJson === "string",
  "Stored review identity, revision or access configuration does not match this case.");
  const request = parseRequest(snapshot.requestJson);
  const review = parseReview(snapshot.reviewJson);
  validateRequest(request);
  requireCondition(request.snapshot.caseId === root.caseId
    && request.snapshot.managementCompanyId === root.managementCompanyId
    && request.snapshot.tenancyId === root.tenancyId && request.snapshot.homeId === root.homeId
    && request.snapshot.revision === revision && sameInstant(root.reviewClock, request.reviewClock)
    && review.metadata.baseCaseRevision === revision && review.metadata.inputHash === root.inputHash
    && sameInstant(review.metadata.reviewClock, request.reviewClock)
    && review.metadata.ruleReleaseId === request.ruleReleaseId,
  "Stored request or review metadata does not match this case.");
  const baseline = nativeReview(request);
  requireCondition(snapshot.inputHash === baseline.metadata.inputHash
    && snapshot.resultHash === fingerprint(review)
    && canonical_json(review) === canonical_json(baseline)
    && snapshot.requestJson === serialize(request) && snapshot.reviewJson === serialize(review),
  "Stored request or review content hash is inconsistent.");
  const workAssignments = loadWorkAssignments(snapshot.workAssignmentsJson, snapshot.workAssignmentsHash,
    root.projectionVersion, request, snapshot.createdAt);
  const workflow = loadWorkflowSnapshot(root, snapshot, request, review, workAssignments);
  validateQueue(root, request, review, workflow?.review, workAssignments, root.currentReviewId!);
  return { request, review, reviewJson: snapshot.reviewJson, workAssignments, createdAt: snapshot.createdAt,
    workflow: workflow?.state, workflowReview: workflow?.review, workflowReviewJson: snapshot.workflowReviewJson };
}

export function receiptResult(command: CommandIdentity, reviewId: string, revision: Long): string {
  return serialize({ caseId: command.caseId, caseRevision: revision, reviewId, resultCode: "APPLIED" });
}

/** Called after present-day access/authority checks but before expected-revision comparison. */
export function isReplay(
  receipt: Osdk.Instance<DcExecutionEvent> | undefined, command: CommandIdentity, currentRevision: number,
): boolean {
  if (receipt === undefined) return false;
  requireCondition(receipt.eventId === receiptIdFor(command.managementCompanyId, command.caseId, command.commandId)
    && receipt.$primaryKey === receipt.eventId && receipt.caseId === command.caseId
    && receipt.managementCompanyId === command.managementCompanyId && receipt.environmentId === ENVIRONMENT_ID
    && sameReaders(receipt.readerIds)
    && (receipt.eventCategory === "COMMAND_RECEIPT" || (receipt.eventCategory === undefined
      && !LIFECYCLE_COMMAND_KINDS.some((kind): boolean => kind === command.commandKind)))
    && receipt.eventJson === undefined && receipt.eventSequence === undefined,
  "Stored command receipt identity is inconsistent.");
  requireCondition(receipt.payloadHash === command.payloadHash && receipt.commandKind === command.commandKind
    && receipt.commandId === command.commandId && receipt.actorId === command.actorId,
  "Command ID has already been used with a different payload.");
  const previousRevision = checkedLong(receipt.previousRevision, "Receipt previous revision");
  const revision = checkedLong(receipt.caseRevision, "Receipt revision", 1n);
  const expectedReviewId = reviewIdFor(command.managementCompanyId, command.caseId, String(revision), command.commandId);
  requireCondition(receipt.previousRevision === command.previousRevision && revision === previousRevision + 1
    && revision <= currentRevision && receipt.reviewId === expectedReviewId && receipt.resultCode === "APPLIED"
    && typeof receipt.occurredAt === "string" && normalize_timestamp(receipt.occurredAt) !== null
    && receipt.resultJson === receiptResult(command, expectedReviewId, String(revision)),
  "Stored command receipt result is inconsistent.");
  // Only the two historical C0 command kinds predate canonical operational details.
  requireCondition((receipt.commandJson === undefined && [OPEN_COMMAND, CHOOSE_COMMAND].includes(command.commandKind))
    || (command.commandJson !== undefined && receipt.commandJson === command.commandJson),
  "Stored operational command intent is inconsistent.");
  return true;
}

/** All writes use the caller's single batch; the core never sees storage edits. */
export function appendReviewAndReceipt(
  batch: EditBatch<OntologyEdit>, request: ReviewRequest, review: ReviewEnvelope,
  command: CommandIdentity, now: string, workAssignments: readonly WorkAssignment[],
  workflowExtras: WorkflowSnapshotExtras = {},
): string {
  const revision = String(request.snapshot.revision);
  const reviewId = reviewIdFor(command.managementCompanyId, command.caseId, revision, command.commandId);
  const requestJson = serialize(request);
  const reviewJson = serialize(review);
  batch.create(DcReviewSnapshot, {
    reviewId, caseId: command.caseId, managementCompanyId: command.managementCompanyId,
    environmentId: ENVIRONMENT_ID, caseRevision: revision, requestJson, reviewJson,
    inputHash: review.metadata.inputHash, resultHash: fingerprint(review),
    workAssignmentsJson: serialize(workAssignments), workAssignmentsHash: fingerprint(workAssignments), ...workflowExtras,
    createdBy: command.actorId, createdAt: now, readerIds: [BOOTSTRAP_ACTOR_ID],
  });
  batch.create(DcExecutionEvent, {
    eventId: receiptIdFor(command.managementCompanyId, command.caseId, command.commandId),
    caseId: command.caseId, managementCompanyId: command.managementCompanyId,
    environmentId: ENVIRONMENT_ID, commandId: command.commandId, commandKind: command.commandKind,
    payloadHash: command.payloadHash, commandJson: command.commandJson, previousRevision: command.previousRevision,
    caseRevision: revision, reviewId, actorId: command.actorId, occurredAt: now,
    eventCategory: "COMMAND_RECEIPT", resultCode: "APPLIED", resultJson: receiptResult(command, reviewId, revision),
    readerIds: [BOOTSTRAP_ACTOR_ID],
  });
  return reviewId;
}
