import type { DcCloseoutCase } from "@ontology/sdk";
import type { Osdk } from "@osdk/client";
import { UserFacingError, type Integer, type Long } from "@osdk/functions";
import { canonical_json, ContractError, from_json, from_wire } from "../domain/codec.js";
import { normalize_timestamp, timestamp_microseconds } from "../domain/datetime.js";
import { _authority, review_request } from "../domain/review.js";
import type { ReviewEnvelope, ReviewRequest } from "../domain/types.js";
import { valid_evidence } from "../domain/validation.js";
import ruleRelease from "../resources/rules/nc_synthetic_review_v1.json" with { type: "json" };
import { BOOTSTRAP_ACTOR_ID, caseIdFor, COMPANY_ID, ENVIRONMENT_ID, MAX_PAYLOAD_BYTES } from "./types.js";

export function requireCondition(condition: boolean, message: string): asserts condition {
  if (!condition) throw new UserFacingError(message);
}

export function boundedJson(value: string): string {
  requireCondition(typeof value === "string" && Buffer.byteLength(value, "utf8") <= MAX_PAYLOAD_BYTES,
    "Stored-case JSON must be at most 256 KiB in UTF-8; inputs are never truncated.");
  return value;
}

export function serialize(value: unknown): string {
  return boundedJson(canonical_json(value));
}

export function parseRequest(json: string): ReviewRequest {
  boundedJson(json);
  try {
    return from_json("ReviewRequest", json);
  } catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    throw new UserFacingError("Case input does not satisfy the strict structured-review contract.");
  }
}

export function parseReview(json: string): ReviewEnvelope {
  boundedJson(json);
  try {
    return from_json("ReviewEnvelope", json);
  } catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    throw new UserFacingError("Stored review does not satisfy the structured-review contract.");
  }
}

/** The only native core invocation. No stored-case money or deadline implementation. */
export function nativeReview(request: ReviewRequest): ReviewEnvelope {
  return review_request(request, from_wire("ReviewRuleRelease", ruleRelease));
}

export function identifier(value: string, label: string): void {
  requireCondition(typeof value === "string" && /^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$/.test(value),
    `${label} must be a non-empty identifier of at most 200 ASCII characters.`);
}

/** Long is a decimal string; the native JSON core additionally requires exact safe integers. */
export function checkedLong(value: Long | undefined, label: string, minimum: bigint = 0n): number {
  requireCondition(typeof value === "string" && /^(0|[1-9][0-9]{0,18})$/.test(value),
    `${label} must be a canonical nonnegative Long.`);
  const exact = BigInt(value);
  requireCondition(exact >= minimum && exact <= 9223372036854775807n
    && exact <= BigInt(Number.MAX_SAFE_INTEGER), `${label} is outside the exact native integer range.`);
  return Number(exact);
}

export function validateChoiceInput(itemId: string, reason: string, delay?: Integer): void {
  identifier(itemId, "Item ID");
  requireCondition(typeof reason === "string" && reason.trim().length > 0
    && Buffer.byteLength(reason, "utf8") <= 2000, "Supply a non-empty reason of at most 2000 UTF-8 bytes.");
  requireCondition(delay === undefined || (Number.isInteger(delay) && delay >= 0 && delay <= 3000),
    "Synthetic test delay must be an integer between 0 and 3000 milliseconds.");
}

function uniqueIds(values: readonly string[]): boolean {
  return new Set(values).size === values.length;
}

export function validateRequest(request: ReviewRequest): void {
  // Ontology timestamp edits currently serialize to milliseconds. Reject a clock
  // that cannot be represented exactly instead of persisting a rounded value.
  requireCondition(timestamp_microseconds(request.reviewClock) % 1000n === 0n,
    "The stored review clock must have millisecond precision or less; it is never rounded.");
  const snapshot = request.snapshot;
  requireCondition(snapshot.origin === "CONSTRUCTED" && snapshot.managementCompanyId === COMPANY_ID,
    "Only the constructed demonstration company is enabled.");
  requireCondition(request.ruleReleaseId === ruleRelease.ruleReleaseId,
    "Supply the explicitly installed NC_SYNTHETIC_REVIEW_V1 rule release.");
  identifier(snapshot.tenancyId, "Ending tenancy ID");
  identifier(snapshot.homeId, "Home ID");
  requireCondition(snapshot.caseId === caseIdFor(snapshot.managementCompanyId, snapshot.tenancyId),
    "Case ID must match the deterministic company and ending-tenancy identity.");
  requireCondition(snapshot.revision >= 1 && Number.isSafeInteger(snapshot.revision),
    "Case revision must be a positive exact integer.");
  requireCondition(uniqueIds(snapshot.charges.map((item): string => item.itemId))
    && uniqueIds(snapshot.parties.map((party): string => party.partyId))
    && uniqueIds(snapshot.authorityGrants.map((grant): string => grant.grantId))
    && uniqueIds(snapshot.evidence.map((entry): string => entry.evidenceId))
    && uniqueIds(snapshot.moneyEvents.map((entry): string => entry.eventId)),
  "Charge, party, authority, evidence and money record identities must be unique.");
  snapshot.charges.forEach((item): void => identifier(item.itemId, "Item ID"));
  const operators = snapshot.parties.filter((party): boolean =>
    party.roles.some((role): boolean => role === "MANAGER" || role === "ACCOUNTANT"));
  requireCondition(operators.some((party): boolean => party.roles.includes("MANAGER"))
    && operators.some((party): boolean => party.roles.includes("ACCOUNTANT"))
    && operators.every((party): boolean => party.principalId === BOOTSTRAP_ACTOR_ID)
    && snapshot.parties.every((party): boolean =>
      party.principalId === null || party.principalId === BOOTSTRAP_ACTOR_ID),
  "Synthetic manager and accountant parties must map to the approved bootstrap principal only.");
  // Persistence caps are independent of the legacy review adapter's larger input limit.
  serialize(request);
}

export function sameReaders(readers: readonly string[] | undefined): boolean {
  return readers?.length === 1 && readers[0] === BOOTSTRAP_ACTOR_ID;
}

function validOperatorIds(ids: readonly string[] | undefined): boolean {
  return ids !== undefined && (ids.length === 0 || sameReaders(ids));
}

/** Fail closed on optional SDK fields; no absent field is interpreted as authority. */
export function validateRoot(root: Osdk.Instance<DcCloseoutCase>): number {
  requireCondition(root.environmentId === ENVIRONMENT_ID && root.managementCompanyId === COMPANY_ID,
    "This case is outside the synthetic stored-case environment.");
  requireCondition(typeof root.tenancyId === "string" && typeof root.homeId === "string"
    && root.caseId === caseIdFor(COMPANY_ID, root.tenancyId) && root.$primaryKey === root.caseId,
  "Stored case identity is inconsistent.");
  identifier(root.tenancyId, "Ending tenancy ID");
  identifier(root.homeId, "Home ID");
  requireCondition(sameReaders(root.readerIds) && sameReaders(root.adminIds)
    && validOperatorIds(root.managerIds) && validOperatorIds(root.accountantIds)
    && root.createdBy === BOOTSTRAP_ACTOR_ID && root.updatedBy === BOOTSTRAP_ACTOR_ID,
  "Stored case access configuration is inconsistent.");
  requireCondition(typeof root.currentReviewId === "string" && /^dc-review:[a-f0-9]{64}$/.test(root.currentReviewId)
    && typeof root.inputHash === "string" && /^[a-f0-9]{64}$/.test(root.inputHash)
    && typeof root.reviewClock === "string" && normalize_timestamp(root.reviewClock) !== null
    && typeof root.updatedAt === "string" && normalize_timestamp(root.updatedAt) !== null,
  "Stored case review reference is incomplete.");
  requireCondition(root.projectionVersion === undefined || root.projectionVersion === "0" || root.projectionVersion === "1",
    "Unknown stored projection version.");
  return checkedLong(root.revision, "Stored revision", 1n);
}

export function requireManagerAccess(root: Osdk.Instance<DcCloseoutCase>, actorId: string): void {
  requireCondition(actorId === BOOTSTRAP_ACTOR_ID && root.readerIds?.includes(actorId) === true
    && root.managerIds?.includes(actorId) === true, "You do not have manager access to this case.");
}

/** Party dates are local calendar dates; grant expiry is an exclusive UTC timestamp.
 * The unchanged native authority evaluator implements both, at actual server time.
 */
export function hasAuthority(
  request: ReviewRequest, actorId: string, role: string, action: string,
  amount: number | null, serverNow: string,
): boolean {
  const snapshot = request.snapshot;
  const eligibleGrantIds = new Set(_authority(snapshot, action, role, amount, serverNow));
  return snapshot.authorityGrants.some((grant): boolean => eligibleGrantIds.has(grant.grantId)
    && snapshot.parties.some((party): boolean => party.partyId === grant.partyId
      && party.principalId === actorId && party.roles.includes(role)
      && valid_evidence(snapshot, party.evidenceIds, serverNow)));
}

export function requireChoiceAuthority(request: ReviewRequest, actorId: string, amount: number, now: string): void {
  requireCondition(hasAuthority(request, actorId, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", amount, now),
    "No current manager authority covers this charge amount.");
}

export function requireSupportedChoice(review: ReviewEnvelope, itemId: string, amount: number): void {
  const decision = review.result.itemDecisions.find((item): boolean => item.itemId === itemId);
  requireCondition(decision !== undefined && ["TENANT", "SPLIT"].includes(decision.allocation)
    && decision.allowability === "SUPPORTED" && decision.supportedAmountCents !== null
    && decision.vendorCostCents !== null && decision.costVersionId !== null
    && !decision.requiresReviewer && decision.missingInputIds.length === 0
    && amount <= decision.supportedAmountCents && amount <= decision.vendorCostCents,
  "Choose only a supported tenant charge within its accepted cost and allowance; resolve review questions first.");
}

export function sameInstant(left: string | undefined, right: string): boolean {
  return left !== undefined && normalize_timestamp(left) !== null
    && timestamp_microseconds(left) === timestamp_microseconds(right);
}

/** Coarse membership is supplemental; current native grants still gate each write. */
export function requireActorAccess(root: Osdk.Instance<DcCloseoutCase>, actorId: string): void {
  requireCondition(actorId === BOOTSTRAP_ACTOR_ID && root.readerIds?.includes(actorId) === true,
    "You do not have access to this case.");
}

export function operatorIds(request: ReviewRequest, now: string): { managerIds: string[]; accountantIds: string[] } {
  const actor = BOOTSTRAP_ACTOR_ID;
  const manager = hasAuthority(request, actor, "MANAGER", "ACCEPT_OR_CORRECT_FACT", null, now)
    || hasAuthority(request, actor, "MANAGER", "RECORD_CHARGE_DECISION", null, now)
    || hasAuthority(request, actor, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", 0, now);
  return { managerIds: manager ? [actor] : [],
    accountantIds: hasAuthority(request, actor, "ACCOUNTANT", "RECONCILE_MONEY_RECORD", null, now) ? [actor] : [] };
}

export function validateDelay(delay?: Integer): void {
  requireCondition(delay === undefined || (Number.isInteger(delay) && delay >= 0 && delay <= 3000),
    "Synthetic test delay must be an integer between 0 and 3000 milliseconds.");
}
