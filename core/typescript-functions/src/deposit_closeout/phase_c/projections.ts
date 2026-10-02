import { DcCaseParty, DcChargeItem, DcEvidenceRecord, DcMoneyEvent, DcRequirement } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import type { EditBatch } from "@osdk/functions";
import { canonical_json, from_json } from "../domain/codec.js";
import type { CaseParty, EvidenceInput, ItemDecision, MoneyEvent, RequirementResult, ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import type { WorkAssignment } from "./change_types.js";
import { BOOTSTRAP_ACTOR_ID, chargeIdFor, ENVIRONMENT_ID, projectionIdFor, type OntologyEdit, type StoredReview } from "./types.js";
import { emptyLifecycleProjections, loadLifecycleProjections, type LifecycleProjectionState } from "../lifecycle/projections.js";
import { boundedJson, checkedLong, requireCondition, serialize } from "./validation.js";

// Bound each exact-case indexed read. A next page is an explicit unsupported size,
// not absence. Five reads together can load at most 5000 child objects.
export const MAX_CASE_PROJECTIONS = 1000;
export interface ProjectionState {
  lifecycle: LifecycleProjectionState;
  chargeIds: Set<string>;
  evidenceIds: Set<string>;
  moneyIds: Set<string>;
  partyIds: Set<string>;
  requirements: Osdk.Instance<DcRequirement>[];
}
export function emptyProjections(): ProjectionState {
  return { lifecycle: emptyLifecycleProjections(), chargeIds: new Set(), evidenceIds: new Set(), moneyIds: new Set(), partyIds: new Set(), requirements: [] };
}
function common(request: ReviewRequest): { caseId: string; managementCompanyId: string; environmentId: string; caseRevision: string; readerIds: string[] } {
  return { caseId: request.snapshot.caseId, managementCompanyId: request.snapshot.managementCompanyId,
    environmentId: ENVIRONMENT_ID, caseRevision: String(request.snapshot.revision), readerIds: [BOOTSTRAP_ACTOR_ID] };
}
function id(request: ReviewRequest, kind: "evidence" | "money" | "party" | "requirement", localId: string): string {
  return projectionIdFor(kind, request.snapshot.managementCompanyId, request.snapshot.caseId, localId);
}
function chargeProps(request: ReviewRequest, item: ItemDecision): DcChargeItem.Props {
  return { ...common(request), chargeRecordId: chargeIdFor(request.snapshot.managementCompanyId, request.snapshot.caseId, item.itemId),
    itemId: item.itemId, allocation: item.allocation, allowability: item.allowability,
    vendorCostCents: item.vendorCostCents === null ? undefined : String(item.vendorCostCents),
    chosenAmountCents: item.chosenAmountCents === null ? undefined : String(item.chosenAmountCents),
    costVersionId: item.costVersionId ?? undefined, reviewRequired: item.requiresReviewer, reason: item.reason };
}
function evidenceProps(request: ReviewRequest, entry: EvidenceInput): DcEvidenceRecord.Props {
  return { ...common(request), recordId: id(request, "evidence", entry.evidenceId), evidenceId: entry.evidenceId,
    recordKind: entry.recordKind, sourceClass: entry.sourceClass, sourceVersion: entry.sourceVersion,
    externalRecordId: entry.externalRecordId, locator: entry.locator,
    occurredAtIso: entry.occurredAt ?? undefined, learnedAtIso: entry.learnedAt,
    supersedesEvidenceId: entry.supersedesEvidenceId ?? undefined, associationAccepted: entry.associationAccepted,
    recordJson: serialize(entry) };
}
function moneyProps(request: ReviewRequest, entry: MoneyEvent): DcMoneyEvent.Props {
  return { ...common(request), recordId: id(request, "money", entry.eventId), eventId: entry.eventId, recordJson: serialize(entry) };
}
function partyProps(request: ReviewRequest, entry: CaseParty): DcCaseParty.Props {
  return { ...common(request), recordId: id(request, "party", entry.partyId), partyId: entry.partyId,
    displayLabel: entry.displayLabel, principalId: entry.principalId ?? undefined, roles: [...entry.roles],
    recordJson: serialize(entry), grantsJson: serialize(request.snapshot.authorityGrants.filter((grant): boolean => grant.partyId === entry.partyId)) };
}
function requirementProps(request: ReviewRequest, entry: RequirementResult,
  assignments: readonly WorkAssignment[], isCurrent: boolean): DcRequirement.Props {
  const assignment = assignments.find((value): boolean => value.requirementKey === entry.requirementKey);
  return { ...common(request), requirementId: id(request, "requirement", entry.requirementKey),
    requirementKey: entry.requirementKey, question: entry.question, track: entry.track, state: entry.state,
    responsibleRole: entry.responsibleRole, dueKind: entry.dueKind, legalDueDate: entry.legalDueDate ?? undefined,
    internalTargetAtIso: (assignment === undefined ? entry.internalTargetAt : assignment.internalTargetAt) ?? undefined,
    assigneePartyId: assignment?.assigneePartyId, isCurrent, resultJson: serialize(entry) };
}
function assertProps(actual: object, expected: object): void {
  Object.entries(expected).forEach(([key, expectedValue]: [string, unknown]): void => {
    const actualValue: unknown = Reflect.get(actual, key);
    requireCondition(expectedValue === undefined ? actualValue === undefined
      : actualValue !== undefined && canonical_json(actualValue) === canonical_json(expectedValue),
    `Stored projection ${key} is inconsistent with the accepted case; no edits were produced.`);
  });
}
function boundedPage<T>(page: { data: readonly T[]; nextPageToken?: string }): T[] {
  requireCondition(page.nextPageToken === undefined && page.data.length <= MAX_CASE_PROJECTIONS,
    "Case projections exceed the supported bound; no partial edits were produced.");
  return [...page.data];
}
function validateRows<T extends { $primaryKey: string }>(rows: readonly T[], expected: readonly object[], primaryKey: string): void {
  requireCondition(rows.length === expected.length && new Set(rows.map((row): string => row.$primaryKey)).size === rows.length,
    "Stored projections are missing, duplicated or unexpected.");
  const byId = new Map(rows.map((row): [string, T] => [row.$primaryKey, row]));
  expected.forEach((properties): void => {
    const key: unknown = Reflect.get(properties, primaryKey);
    requireCondition(typeof key === "string", "Projection identity is missing.");
    const row = byId.get(key);
    requireCondition(row !== undefined, "Stored projection is missing; it is not a new record.");
    assertProps(row, properties);
  });
}

/** These rows are validated for safe update classification, never used to calculate money or authority.
 * Required indexed queries propagate every access/transport failure. Inactive work is loaded as well
 * so a reappearing requirement cannot be mistaken for a new primary key or lose its assignment.
 */
export async function loadProjections(client: Client, stored: StoredReview, version: string | undefined,
  includeWorkflow: boolean = stored.workflow !== undefined): Promise<ProjectionState> {
  const { request, review, workAssignments } = stored;
  const effectiveReview = stored.workflowReview ?? review;
  const where = { caseId: { $eq: request.snapshot.caseId } };
  const options = { $pageSize: MAX_CASE_PROJECTIONS };
  const [charges, evidence, money, parties, requirements, lifecycle] = await Promise.all([
    client(DcChargeItem).where(where).fetchPage(options).then(boundedPage),
    client(DcEvidenceRecord).where(where).fetchPage(options).then(boundedPage),
    client(DcMoneyEvent).where(where).fetchPage(options).then(boundedPage),
    client(DcCaseParty).where(where).fetchPage(options).then(boundedPage),
    client(DcRequirement).where(where).fetchPage(options).then(boundedPage),
    includeWorkflow ? loadLifecycleProjections(client, stored) : Promise.resolve(emptyLifecycleProjections()),
  ]);
  validateRows(charges, review.result.itemDecisions.map((entry): DcChargeItem.Props => chargeProps(request, entry)), "chargeRecordId");
  if (version === undefined || version === "0") {
    requireCondition(evidence.length + money.length + parties.length + requirements.length === 0,
      "C0 case unexpectedly contains full-phase projections.");
  } else {
    requireCondition(version === "1", "Unknown projection version.");
    validateRows(evidence, request.snapshot.evidence.map((entry): DcEvidenceRecord.Props => evidenceProps(request, entry)), "recordId");
    validateRows(money, request.snapshot.moneyEvents.map((entry): DcMoneyEvent.Props => moneyProps(request, entry)), "recordId");
    validateRows(parties, request.snapshot.parties.map((entry): DcCaseParty.Props => partyProps(request, entry)), "recordId");
    validateRows(requirements.filter((row): boolean => row.isCurrent === true),
      effectiveReview.result.scopeRequirements.requirements.map((entry): DcRequirement.Props => requirementProps(request, entry, workAssignments, true)), "requirementId");
    requireCondition(new Set(requirements.map((row): string => row.$primaryKey)).size === requirements.length,
      "Stored requirement identities are duplicated.");
    const currentKeys = new Set(effectiveReview.result.scopeRequirements.requirements.map((entry): string => entry.requirementKey));
    requirements.filter((row): boolean => row.isCurrent !== true).forEach((row): void => {
      requireCondition(row.isCurrent === false && typeof row.resultJson === "string", "Inactive requirement is incomplete.");
      const result = from_json("RequirementResult", boundedJson(row.resultJson));
      requireCondition(!currentKeys.has(result.requirementKey) && row.$primaryKey === id(request, "requirement", result.requirementKey)
        && checkedLong(row.caseRevision, "Inactive requirement revision", 1n) <= request.snapshot.revision,
      "Inactive requirement identity or revision is inconsistent.");
      assertProps(row, { ...requirementProps(request, result, workAssignments, false), caseRevision: row.caseRevision });
    });
    requireCondition(workAssignments.every((entry): boolean => requirements.some((row): boolean => row.requirementKey === entry.requirementKey)),
      "An assigned requirement is missing from current and retained work.");
  }
  return { lifecycle, chargeIds: new Set(charges.map((row): string => row.chargeRecordId)),
    evidenceIds: new Set(evidence.map((row): string => row.recordId)), moneyIds: new Set(money.map((row): string => row.recordId)),
    partyIds: new Set(parties.map((row): string => row.recordId)), requirements };
}

/** All current projections and disappeared work rows join the same root-guarded batch. */
export function appendProjections(batch: EditBatch<OntologyEdit>, request: ReviewRequest, review: ReviewEnvelope,
  assignments: readonly WorkAssignment[], previous: ProjectionState): void {
  const snapshot = request.snapshot;
  const requirements = review.result.scopeRequirements.requirements;
  const requirementIds = new Set(previous.requirements.map((row): string => row.requirementId));
  const currentIds = new Set(requirements.map((entry): string => id(request, "requirement", entry.requirementKey)));
  [review.result.itemDecisions.length, snapshot.evidence.length, snapshot.moneyEvents.length, snapshot.parties.length,
    new Set([...requirementIds, ...currentIds]).size].forEach((count): void => requireCondition(count <= MAX_CASE_PROJECTIONS,
    "Case projections exceed the supported bound; no partial edits were produced."));
  review.result.itemDecisions.forEach((entry): void => {
    const { chargeRecordId, ...properties } = chargeProps(request, entry);
    if (previous.chargeIds.has(chargeRecordId)) batch.update({ $apiName: "DcChargeItem", $primaryKey: chargeRecordId }, properties);
    else batch.create(DcChargeItem, { chargeRecordId, ...properties });
  });
  snapshot.evidence.forEach((entry): void => {
    const { recordId, ...properties } = evidenceProps(request, entry);
    if (previous.evidenceIds.has(recordId)) batch.update({ $apiName: "DcEvidenceRecord", $primaryKey: recordId }, properties);
    else batch.create(DcEvidenceRecord, { recordId, ...properties });
  });
  snapshot.moneyEvents.forEach((entry): void => {
    const { recordId, ...properties } = moneyProps(request, entry);
    if (previous.moneyIds.has(recordId)) batch.update({ $apiName: "DcMoneyEvent", $primaryKey: recordId }, properties);
    else batch.create(DcMoneyEvent, { recordId, ...properties });
  });
  snapshot.parties.forEach((entry): void => {
    const { recordId, ...properties } = partyProps(request, entry);
    if (previous.partyIds.has(recordId)) batch.update({ $apiName: "DcCaseParty", $primaryKey: recordId }, properties);
    else batch.create(DcCaseParty, { recordId, ...properties });
  });
  requirements.forEach((entry): void => {
    const { requirementId, ...properties } = requirementProps(request, entry, assignments, true);
    if (requirementIds.has(requirementId)) batch.update({ $apiName: "DcRequirement", $primaryKey: requirementId }, properties);
    else batch.create(DcRequirement, { requirementId, ...properties });
  });
  previous.requirements.filter((row): boolean => row.isCurrent === true && !currentIds.has(row.requirementId))
    .forEach((row): void => {
      // Disappearance is not evidence of performance. Preserve the last native result,
      // its dates/state and the assigned work rather than marking it completed.
      batch.update(row, { isCurrent: false, caseRevision: String(snapshot.revision) });
    });
}
