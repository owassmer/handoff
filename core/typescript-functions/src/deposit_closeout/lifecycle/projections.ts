/** Typed, bounded SDK projections. None of these rows is an accounting input. */
import { DcActionRequest, DcApproval, DcExecutionEvent, DcStatementVersion } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import type { EditBatch } from "@osdk/functions";
import { canonical_json } from "../domain/codec.js";
import type { ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import { BOOTSTRAP_ACTOR_ID, ENVIRONMENT_ID, receiptIdFor, reviewIdFor,
  type OntologyEdit, type StoredReview } from "../phase_c/types.js";
import { checkedLong, requireCondition, sameInstant, sameReaders, serialize } from "../phase_c/validation.js";
import { centsToLong } from "./codec.js";
import { projectPerformance } from "./performance.js";
import { statementBasisCurrent } from "./statements.js";
import { LIFECYCLE_COMMAND_KINDS, type WorkflowEvent, type WorkflowStateV2 } from "./types.js";

const MAX_ROWS = 1000;
export interface LifecycleProjectionState {
  statementIds: Set<string>;
  approvalIds: Set<string>;
  requestIds: Set<string>;
  eventIds: Set<string>;
  /** Includes retained C command receipts so an event read never silently truncates. */
  eventRowCount: number;
}
export function emptyLifecycleProjections(): LifecycleProjectionState {
  return { statementIds: new Set(), approvalIds: new Set(), requestIds: new Set(), eventIds: new Set(), eventRowCount: 0 };
}
function common(request: ReviewRequest): { caseId: string; managementCompanyId: string; environmentId: string; caseRevision: string; readerIds: string[] } {
  return { caseId: request.snapshot.caseId, managementCompanyId: request.snapshot.managementCompanyId,
    environmentId: ENVIRONMENT_ID, caseRevision: centsToLong(request.snapshot.revision), readerIds: [BOOTSTRAP_ACTOR_ID] };
}
interface Properties {
  statements: DcStatementVersion.Props[];
  approvals: DcApproval.Props[];
  requests: DcActionRequest.Props[];
}
function properties(request: ReviewRequest, base: ReviewEnvelope, workflow: WorkflowStateV2, at: string): Properties {
  const performance = projectPerformance(request, base, workflow, at);
  const currentRequests = new Map(performance.currentRequests.map((entry) => [entry.requestId, entry]));
  const statements = new Map(performance.statementDetails.map((entry) => [entry.statementId, entry]));
  const approvals = new Map(performance.approvalDetails.map((entry) => [entry.approvalId, entry]));
  return {
    statements: workflow.statements.map((entry): DcStatementVersion.Props => ({
      ...common(request), statementId: entry.statementId, kind: entry.kind, sourceReviewId: entry.sourceReviewId,
      createdCommandId: entry.createdCommandId, createdBy: entry.createdBy, createdAt: entry.createdAt,
      materialityHash: entry.materialityHash, contentHash: entry.contentHash, recipientVersionId: entry.recipientVersionId,
      statementJson: serialize(entry), renderedText: entry.renderedText, supersedesStatementId: entry.supersedesStatementId ?? undefined,
      issueState: statements.get(entry.statementId)!.issued ? "SIMULATED_ISSUED" : "NOT_ISSUED",
      basisCurrent: statementBasisCurrent(request, base, workflow, entry), isCurrent: workflow.currentStatementId === entry.statementId,
    })),
    approvals: workflow.approvals.map((entry): DcApproval.Props => ({
      ...common(request), approvalId: entry.approvalId, targetVersionId: entry.intent.targetVersionId,
      scope: entry.scope, decision: entry.decision, validity: approvals.get(entry.approvalId)!.valid ? "VALID" : "INVALID",
      materialityHash: entry.intent.materialityHash,
      contentHash: entry.intent.kind === "STATEMENT_DISPATCH" ? entry.intent.contentHash : undefined,
      actorId: entry.actorId, actorPartyId: entry.actorPartyId, authorityVersion: entry.authorityVersion,
      createdCommandId: entry.createdCommandId, decidedAt: entry.decidedAt,
      amountCents: entry.intent.amountCents === null ? undefined : centsToLong(entry.intent.amountCents),
      recipientVersionId: entry.intent.recipientVersionId ?? undefined, revokesApprovalId: entry.revokesApprovalId ?? undefined,
      approvalJson: serialize(entry),
    })),
    requests: workflow.requests.map((entry): DcActionRequest.Props => {
      const current = currentRequests.get(entry.requestId)!;
      return { ...common(request), requestId: entry.requestId, instructionKey: entry.instructionKey, kind: entry.kind,
        state: current.state, payloadHash: entry.instructionHash, targetVersionId: entry.intent.targetVersionId,
        createdCommandId: entry.createdCommandId, createdBy: entry.createdBy, createdAt: entry.createdAt,
        amountCents: entry.intent.amountCents === null ? undefined : centsToLong(entry.intent.amountCents),
        currency: entry.intent.currency, recipientVersionId: entry.intent.recipientVersionId ?? undefined,
        approvalIds: [...entry.approvalIds], replacementOfRequestId: entry.replacesRequestId ?? undefined,
        reversesTransactionId: entry.reversesTransactionId ?? undefined, reservationCents: centsToLong(current.reservedAmountCents),
        currentAttemptId: current.attemptId ?? undefined, externalReference: current.canonicalTransactionId ?? undefined,
        requestJson: serialize(entry) };
    }),
  };
}
function eventProperties(request: ReviewRequest, state: WorkflowStateV2, event: WorkflowEvent,
  revision: string, reviewId: string | undefined): DcExecutionEvent.Props {
  const instruction = state.requests.find((entry): boolean => entry.requestId === event.requestId);
  return { ...common(request), caseRevision: revision, eventId: event.eventId,
    eventCategory: event.kind === "RAW_SIMULATED_RESULT" || event.kind === "RESULT_ACCEPTED" ? event.kind : event.category,
    commandId: event.commandId, commandKind: event.kind, actorId: event.recordedBy, occurredAt: event.recordedAt,
    requestId: event.requestId ?? undefined, attemptId: event.attemptId ?? undefined, sourceEventId: event.sourceEventId ?? undefined,
    canonicalTransactionId: event.kind === "RAW_SIMULATED_RESULT" || event.kind === "RESULT_ACCEPTED"
      ? event.payload.canonicalTransactionId ?? undefined : undefined,
    targetVersionId: instruction?.intent.targetVersionId, eventSequence: centsToLong(event.sequence),
    businessOccurredAtIso: event.occurredAt, learnedAtIso: event.learnedAt, mode: event.mode, eventJson: serialize(event), reviewId,
    // An observation is not an APPLIED command receipt.
    previousRevision: undefined, payloadHash: undefined, commandJson: undefined, resultCode: undefined, resultJson: undefined };
}
function assertProps(actual: object, expected: object): void {
  Object.entries(expected).forEach(([key, value]): void => {
    const actualValue: unknown = Reflect.get(actual, key);
    const timestamp = ["createdAt", "decidedAt", "occurredAt"].includes(key);
    requireCondition(value === undefined ? actualValue === undefined
      : timestamp && typeof value === "string" && typeof actualValue === "string" ? sameInstant(actualValue, value)
      : actualValue !== undefined && canonical_json(actualValue) === canonical_json(value),
    `Stored workflow projection ${key} is inconsistent with its accepted immutable record.`);
  });
}
function bounded<T>(page: { data: readonly T[]; nextPageToken?: string }): T[] {
  requireCondition(page.nextPageToken === undefined && page.data.length <= MAX_ROWS,
    "Workflow case projections exceed the supported bound; no partial edits were produced.");
  return [...page.data];
}
function assertRows<T extends { $primaryKey: string }>(rows: readonly T[], expected: readonly object[], key: string): void {
  const byId = new Map(rows.map((row) => [row.$primaryKey, row]));
  requireCondition(rows.length === expected.length && byId.size === rows.length,
    "Workflow projections are missing, duplicated or unexpected.");
  expected.forEach((props): void => {
    const id: unknown = Reflect.get(props, key);
    requireCondition(typeof id === "string", "Workflow projection identity is missing.");
    const row = byId.get(id);
    requireCondition(row !== undefined, "Workflow projection is missing; it is not a new record.");
    assertProps(row, props);
  });
}

/** One bounded case read per type, including history; never one lookup per instruction/event. */
export async function loadLifecycleProjections(client: Client, stored: StoredReview): Promise<LifecycleProjectionState> {
  const { request, review, workflow } = stored;
  const where = { caseId: { $eq: request.snapshot.caseId } };
  const options = { $pageSize: MAX_ROWS };
  const [statements, approvals, requests, events] = await Promise.all([
    client(DcStatementVersion).where(where).fetchPage(options).then(bounded),
    client(DcApproval).where(where).fetchPage(options).then(bounded),
    client(DcActionRequest).where(where).fetchPage(options).then(bounded),
    client(DcExecutionEvent).where(where).fetchPage(options).then(bounded),
  ]);
  const expected = workflow === undefined ? { statements: [], approvals: [], requests: [] }
    : properties(request, review, workflow, stored.createdAt!);
  assertRows(statements, expected.statements, "statementId");
  assertRows(approvals, expected.approvals, "approvalId");
  assertRows(requests, expected.requests, "requestId");
  requireCondition(new Set(events.map((entry): string => entry.$primaryKey)).size === events.length,
    "Stored case event identities are duplicated.");
  const historicalEvents = events.filter((row): boolean => row.eventCategory !== undefined && row.eventCategory !== "COMMAND_RECEIPT");
  const historicalById = new Map(historicalEvents.map((row) => [row.$primaryKey, row]));
  requireCondition(historicalEvents.length === (workflow?.events.length ?? 0), "Workflow event projections are missing or unexpected.");
  workflow?.events.forEach((event): void => {
    const row = historicalById.get(event.eventId);
    requireCondition(row !== undefined, "Stored workflow event is missing.");
    const recordedRevision = checkedLong(row.caseRevision, "Workflow event revision", 1n);
    requireCondition(recordedRevision <= request.snapshot.revision, "Workflow event is newer than the accepted root.");
    const expectedReview = row.reviewId === undefined ? undefined
      : reviewIdFor(request.snapshot.managementCompanyId, request.snapshot.caseId, String(recordedRevision), event.commandId);
    assertProps(row, eventProperties(request, workflow, event, String(recordedRevision), expectedReview));
  });
  // Legacy receipts keep their original content/category absence. They must not masquerade as workflow observations.
  events.filter((row): boolean => row.eventCategory === undefined || row.eventCategory === "COMMAND_RECEIPT")
    .forEach((row): void => {
      requireCondition(typeof row.commandId === "string" && row.$primaryKey === row.eventId
        && row.eventId === receiptIdFor(request.snapshot.managementCompanyId, request.snapshot.caseId, row.commandId)
        && row.caseId === request.snapshot.caseId && row.managementCompanyId === request.snapshot.managementCompanyId
        && row.environmentId === ENVIRONMENT_ID && sameReaders(row.readerIds)
        && row.eventJson === undefined && row.eventSequence === undefined
        && (!LIFECYCLE_COMMAND_KINDS.some((kind): boolean => kind === row.commandKind)
          || (row.eventCategory === "COMMAND_RECEIPT" && typeof row.commandJson === "string"))
        && checkedLong(row.caseRevision, "Command receipt revision", 1n) <= request.snapshot.revision,
      "Stored case event is neither a valid receipt identity nor a workflow observation.");
    });
  return { statementIds: new Set(statements.map((entry): string => entry.statementId)),
    approvalIds: new Set(approvals.map((entry): string => entry.approvalId)),
    requestIds: new Set(requests.map((entry): string => entry.requestId)),
    eventIds: new Set(historicalEvents.map((entry): string => entry.eventId)), eventRowCount: events.length };
}

function appendOnly<T>(previous: readonly T[], next: readonly T[], key: (entry: T) => string): void {
  const byId = new Map(next.map((entry) => [key(entry), entry]));
  requireCondition(byId.size === next.length, "Workflow history contains duplicate identities.");
  previous.forEach((entry): void => {
    const current = byId.get(key(entry));
    requireCondition(current !== undefined && canonical_json(entry) === canonical_json(current),
      "Historical workflow content cannot be removed or rewritten.");
  });
}
export function assertWorkflowHistory(previous: WorkflowStateV2 | undefined, next: WorkflowStateV2): void {
  if (previous === undefined) return;
  requireCondition(previous.initializedBy === next.initializedBy && previous.initializedAt === next.initializedAt,
    "Workflow initialization history cannot change.");
  appendOnly(previous.statements, next.statements, (entry): string => entry.statementId);
  appendOnly(previous.approvals, next.approvals, (entry): string => entry.approvalId);
  appendOnly(previous.requests, next.requests, (entry): string => entry.requestId);
  appendOnly(previous.events, next.events, (entry): string => entry.eventId);
}

/** Existing immutable content is never updated. Only derived columns change; new observations append. */
export function appendLifecycleProjections(batch: EditBatch<OntologyEdit>, request: ReviewRequest, base: ReviewEnvelope,
  workflow: WorkflowStateV2, previous: LifecycleProjectionState, now: string, reviewId: string): void {
  const values = properties(request, base, workflow, now);
  const newEvents = workflow.events.filter((entry): boolean => !previous.eventIds.has(entry.eventId));
  [values.statements.length, values.approvals.length, values.requests.length,
    previous.eventRowCount + newEvents.length + 1].forEach((count): void => requireCondition(count <= MAX_ROWS,
    "Workflow case projections exceed the supported bound; no partial edits were produced."));
  values.statements.forEach((entry): void => {
    if (!previous.statementIds.has(entry.statementId)) batch.create(DcStatementVersion, entry);
    else batch.update({ $apiName: "DcStatementVersion", $primaryKey: entry.statementId }, {
      caseRevision: entry.caseRevision, issueState: entry.issueState, basisCurrent: entry.basisCurrent, isCurrent: entry.isCurrent });
  });
  values.approvals.forEach((entry): void => {
    if (!previous.approvalIds.has(entry.approvalId)) batch.create(DcApproval, entry);
    else batch.update({ $apiName: "DcApproval", $primaryKey: entry.approvalId }, {
      caseRevision: entry.caseRevision, validity: entry.validity });
  });
  values.requests.forEach((entry): void => {
    if (!previous.requestIds.has(entry.requestId)) batch.create(DcActionRequest, entry);
    else batch.update({ $apiName: "DcActionRequest", $primaryKey: entry.requestId }, {
      caseRevision: entry.caseRevision, state: entry.state, reservationCents: entry.reservationCents,
      currentAttemptId: entry.currentAttemptId, externalReference: entry.externalReference });
  });
  newEvents.forEach((event): void => batch.create(DcExecutionEvent,
    eventProperties(request, workflow, event, centsToLong(request.snapshot.revision), reviewId)));
}
