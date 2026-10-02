/** Decision/entitlement identity, deliberately separate from current execution admission. */
import { ContractError } from "../domain/codec.js";
import { _ancestors } from "../domain/charges.js";
import { compare_timestamps } from "../domain/datetime.js";
import { fingerprint } from "../domain/fingerprints.js";
import type { AccountResult, ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import { valid_evidence } from "../domain/validation.js";
import { nativeReview } from "../phase_c/validation.js";
import { parseWorkflowTimestamp } from "./codec.js";
import { recipientVersionIdFor } from "./ids.js";
import type { FinancialOperationKind, OperationInstructions, StatementKind, WorkflowScope, WorkflowStateV2 } from "./types.js";
import { WORKFLOW_COMPANY_ID, WORKFLOW_ENVIRONMENT_ID } from "./types.js";

export const STATEMENT_TEMPLATE_VERSION = "dc-synthetic-text-v1";

export function workflowScope(request: ReviewRequest): WorkflowScope {
  if (request.snapshot.origin !== "CONSTRUCTED" || request.snapshot.managementCompanyId !== WORKFLOW_COMPANY_ID
      || request.snapshot.currency !== "USD") throw new ContractError("Only the constructed USD workflow scope is enabled");
  return { caseId: request.snapshot.caseId, managementCompanyId: request.snapshot.managementCompanyId,
    environmentId: WORKFLOW_ENVIRONMENT_ID };
}

export function assertWorkflowScope(request: ReviewRequest, state: WorkflowStateV2): void {
  const scope = workflowScope(request);
  if (state.caseId !== scope.caseId || state.managementCompanyId !== scope.managementCompanyId
      || state.environmentId !== scope.environmentId) throw new ContractError("Workflow scope does not match this case");
}

export function nextBusinessClock(request: ReviewRequest, state: WorkflowStateV2 | null, serverNow: string): string {
  return [request.reviewClock, state?.businessClock ?? request.reviewClock, serverNow]
    .map((clock): string => parseWorkflowTimestamp(clock))
    .reduce((latest, clock): string => compare_timestamps(latest, clock) >= 0 ? latest : clock);
}

/** Only the referenced evidence contributes; recording/learning time is not identity. */
export function evidenceBasis(request: ReviewRequest, ids: readonly string[]): unknown {
  const evidenceById = new Map(request.snapshot.evidence.map((entry) => [entry.evidenceId, entry]));
  return [...new Set(ids)].sort().map((id): unknown => ({ id,
    usable: valid_evidence(request.snapshot, [id], request.reviewClock),
    supersedingSources: request.snapshot.evidence.filter((entry): boolean => !ids.includes(entry.evidenceId)
      && _ancestors(entry.evidenceId, evidenceById).has(id)
      && valid_evidence(request.snapshot, [entry.evidenceId], request.reviewClock))
      .sort((a, b): number => a.evidenceId < b.evidenceId ? -1 : a.evidenceId > b.evidenceId ? 1 : 0)
      .map((entry): unknown => ({ evidenceId: entry.evidenceId, sourceVersion: entry.sourceVersion, locator: entry.locator, excerpt: entry.excerpt })),
    records: request.snapshot.evidence.filter((entry): boolean => entry.evidenceId === id).map((entry): unknown => ({
      evidenceId: entry.evidenceId, recordKind: entry.recordKind, sourceClass: entry.sourceClass,
      externalRecordId: entry.externalRecordId, sourceVersion: entry.sourceVersion, locator: entry.locator,
      supersedesEvidenceId: entry.supersedesEvidenceId, associationAccepted: entry.associationAccepted, excerpt: entry.excerpt,
    })),
  }));
}

export function routeUsable(request: ReviewRequest, route: OperationInstructions, clock: string): boolean {
  return route.state === "VERIFIED" && route.method === "DEMO_OUTBOX"
    && route.routeReference !== null && /^demo-[A-Za-z0-9][A-Za-z0-9._-]{0,199}$/.test(route.routeReference)
    && route.partyIds.length > 0 && valid_evidence(request.snapshot, route.evidenceIds, clock)
    && route.partyIds.every((id): boolean => {
      const matches = request.snapshot.parties.filter((party): boolean => party.partyId === id);
      return matches.length === 1 && matches[0]!.roles.some((role): boolean => ["RESIDENT", "SIGNATORY"].includes(role))
        && valid_evidence(request.snapshot, matches[0]!.evidenceIds, clock);
    });
}

function routeBasis(request: ReviewRequest, route: OperationInstructions): unknown {
  return { version: route.versionId, evidence: evidenceBasis(request, route.evidenceIds),
    parties: [...route.partyIds].sort().map((id): unknown => {
      const party = request.snapshot.parties.find((entry): boolean => entry.partyId === id);
      return { partyId: id, displayLabel: party?.displayLabel ?? null, roles: party?.roles.slice().sort() ?? [],
        evidence: evidenceBasis(request, party?.evidenceIds ?? []) };
    }) };
}

/**
 * HASH-ONLY native projection. Removing our request-control facts and all their
 * money associations prevents normal reservations/results invalidating the
 * decision they implement. Economic events, amounts, kinds, IDs and evidence
 * remain intact (including both sides of a reversal). Never use for admission.
 */
export function entitlementReview(request: ReviewRequest, state: WorkflowStateV2): ReviewEnvelope {
  const copy = structuredClone(request);
  const ownIds = new Set(state.requests.map((entry): string => entry.requestId));
  copy.snapshot.priorRequests = copy.snapshot.priorRequests.filter((entry): boolean => !ownIds.has(entry.requestId));
  copy.snapshot.moneyEvents = copy.snapshot.moneyEvents.map((entry) => ({ ...entry,
    requestId: entry.requestId !== null && ownIds.has(entry.requestId) ? null : entry.requestId }));
  return nativeReview(copy);
}

/** Sum native verified components once; no alternate entitlement/refund calculator. */
export function nativeGross(account: AccountResult): number | null {
  if (account.reconciliationState !== "RECONCILED" || account.recordedDepositCents === null
      || account.existingDepositApplicationsCents === null || account.priorNetRefundsCents === null) return null;
  const components = [account.recordedDepositCents, account.existingDepositApplicationsCents, account.priorNetRefundsCents];
  if (components.some((value): boolean => !Number.isSafeInteger(value) || value < 0)) return null;
  const gross = components.reduce((sum, value): bigint => sum + BigInt(value), 0n);
  return gross <= BigInt(Number.MAX_SAFE_INTEGER) ? Number(gross) : null;
}

function commonBasis(request: ReviewRequest, review: ReviewEnvelope): unknown {
  const s = request.snapshot;
  const trigger = s.dates.filter((fact): boolean => fact.factKey === "ACCOUNTING_TRIGGER");
  const itemIds = new Set(s.charges.map((item): string => item.itemId));
  const acceptedIds = new Set(s.charges.flatMap((item): string[] => item.evidenceIds));
  const evidenceById = new Map(s.evidence.map((entry) => [entry.evidenceId, entry]));
  const relevantItemSources = s.evidence.filter((entry): boolean => acceptedIds.has(entry.evidenceId)
    || (["INVOICE", "CONDITION_OBSERVATION", "WORK_COMPLETION", "FACT_ASSERTION", "ESTIMATE"].includes(entry.recordKind)
      && (entry.proposedItemIds.some((id): boolean => itemIds.has(id))
        || [..._ancestors(entry.evidenceId, evidenceById)].some((id): boolean => acceptedIds.has(id)))))
    .filter((entry): boolean => compare_timestamps(entry.learnedAt, request.reviewClock) <= 0);
  return { scope: workflowScope(request), ruleReleaseId: review.metadata.ruleReleaseId, codeVersion: review.metadata.codeVersion,
    jurisdiction: s.jurisdiction, tenancyRegime: s.tenancyRegime, tenancyEndsInFull: s.tenancyEndsInFull,
    cashSecurityDeposit: s.cashSecurityDeposit, specialCircumstances: [...s.specialCircumstances].sort(),
    agreement: evidenceBasis(request, s.agreementEvidenceIds), trigger,
    triggerEvidence: evidenceBasis(request, trigger.flatMap((fact): string[] => fact.evidenceIds)),
    membership: s.parties.filter((party): boolean => party.roles.some((role): boolean => ["RESIDENT", "SIGNATORY"].includes(role)))
      .sort((a, b): number => a.partyId < b.partyId ? -1 : a.partyId > b.partyId ? 1 : 0)
      .map((party): unknown => ({ partyId: party.partyId, roles: [...party.roles].sort(), effectiveFrom: party.effectiveFrom,
        effectiveUntil: party.effectiveUntil, evidence: evidenceBasis(request, party.evidenceIds) })),
    scopeState: review.result.scopeRequirements.scopeState,
    decisions: review.result.itemDecisions.map((item): string => item.fingerprint),
    relevantItemEvidence: evidenceBasis(request, relevantItemSources.map((entry): string => entry.evidenceId)),
    grossDepositCents: nativeGross(review.result.account), deductionsCents: review.result.account.totalDeductionsCents,
    balanceEvidence: evidenceBasis(request, [s.depositBalance.sourceEvidenceId]),
    custodianPartyId: s.depositBalance.custodianPartyId,
  };
}

export function financialMaterialityHash(
  request: ReviewRequest, state: WorkflowStateV2, kind: FinancialOperationKind,
): string | null {
  // A projection may encounter a previously valid basis that is now outside
  // exact bounds. That is unverifiable, not a claim that approval never existed.
  try {
    const review = entitlementReview(request, state);
    if (review.result.scopeRequirements.scopeState !== "SUPPORTED" || !review.result.account.finalAccountReady
        || nativeGross(review.result.account) === null) return null;
    return fingerprint({ basis: commonBasis(request, review),
      refundRoute: kind === "REFUND" ? routeBasis(request, state.refundInstructions) : null });
  } catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    return null;
  }
}

export function statementMaterialityHash(request: ReviewRequest, state: WorkflowStateV2, kind: StatementKind): string {
  const review = entitlementReview(request, state);
  return fingerprint({ template: STATEMENT_TEMPLATE_VERSION, kind, basis: commonBasis(request, review),
    statementRoute: routeBasis(request, state.statementInstructions),
    dates: request.snapshot.dates, dateEvidence: evidenceBasis(request, request.snapshot.dates.flatMap((fact): string[] => fact.evidenceIds)),
    descriptions: request.snapshot.charges.map((item): unknown => ({ itemId: item.itemId, location: item.location, description: item.description })),
    interim: kind === "INTERIM" ? { state: request.snapshot.interimConditionState, reason: request.snapshot.interimConditionReason,
      evidence: evidenceBasis(request, request.snapshot.interimConditionEvidenceIds) } : null,
  });
}

/** Conservative C compatibility: neither split channel can certify the other. */
export function mapLegacyRecipients(request: ReviewRequest, state: WorkflowStateV2): void {
  const statement = state.statementInstructions;
  const refund = state.refundInstructions;
  const verified = routeUsable(request, statement, request.reviewClock) && routeUsable(request, refund, request.reviewClock);
  request.snapshot.recipients = {
    versionId: `dc-recipient:${fingerprint({ statement: statement.versionId, refund: refund.versionId })}`,
    statementPartyIds: [...statement.partyIds], refundPartyIds: [...refund.partyIds],
    state: verified ? "VERIFIED" : "MISSING", statementMethod: statement.method ?? "UNCONFIRMED",
    refundMethod: refund.method ?? "UNCONFIRMED", verifiedRouteReference: verified ? statement.routeReference : null,
    evidenceIds: [...new Set([...statement.evidenceIds, ...refund.evidenceIds])].sort(),
  };
}

export function versionedRoute(scope: WorkflowScope, channel: "STATEMENT" | "REFUND", route: Omit<OperationInstructions, "versionId">): OperationInstructions {
  const normalized = { ...structuredClone(route), partyIds: [...route.partyIds].sort(), evidenceIds: [...route.evidenceIds].sort() };
  return { ...normalized, versionId: recipientVersionIdFor(scope, channel, normalized) };
}
