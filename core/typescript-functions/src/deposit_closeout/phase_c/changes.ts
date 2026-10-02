/** Pure Phase C transitions. Storage, concurrency, actors and receipts belong to the adapter. */
import {
  canonical_json, ContractError, from_wire, is_plain_object, parse_json,
  type ContractName, type ContractTypes,
} from "../domain/codec.js";
import { compare_timestamps, normalize_timestamp, timestamp_microseconds } from "../domain/datetime.js";
import { _authority } from "../domain/review.js";
import { _local_date } from "../domain/rules.js";
import type { CaseParty, CaseSnapshot, ChargeInput, EvidenceInput, RequirementResult, ReviewRequest } from "../domain/types.js";
import { valid_evidence } from "../domain/validation.js";
import { VOCABULARY } from "../domain/vocabulary.js";
import type { CaseChange, ChangeKind, ChangeResult, WorkAssignment } from "./change_types.js";
import { BOOTSTRAP_ACTOR_ID, MAX_PAYLOAD_BYTES } from "./types.js";
import { hasAuthority, identifier, nativeReview, requireCondition, requireSupportedChoice } from "./validation.js";

export type { CaseChange, ChangeKind, ChangeResult, WorkAssignment } from "./change_types.js";

function reason(value: unknown): string {
  if (typeof value !== "string" || value.trim().length === 0
    || Buffer.byteLength(value, "utf8") > 2000) {
    throw new ContractError("Supply a non-empty reason of at most 2000 UTF-8 bytes.");
  }
  return value;
}

function text(value: unknown, label: string): string {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new ContractError(`${label} must be a non-empty string.`);
  }
  return value;
}

function strings(value: unknown, label: string): string[] {
  if (!Array.isArray(value)) throw new ContractError(`${label} must be an array.`);
  const result = Array.from(value as unknown[], (entry): string => text(entry, label));
  if (new Set(result).size !== result.length) throw new ContractError(`${label} must not repeat IDs.`);
  return result;
}

function object(value: unknown, keys: readonly string[]): Record<string, unknown> {
  if (!is_plain_object(value) || Object.keys(value).length !== keys.length
    || !keys.every((key): boolean => Object.hasOwn(value, key))) {
    throw new ContractError(`Payload must contain exactly: ${keys.join(", ") || "no keys"}.`);
  }
  return value;
}

/** Do not let the native codec's submicrosecond truncation conceal lost precision. */
function exactTimestamp(value: unknown, milliseconds: boolean = false): string {
  const input = text(value, "Timestamp");
  const fraction = /[.,](\d+)Z$/.exec(input)?.[1] ?? "";
  const normalized = normalize_timestamp(input);
  if (normalized === null || /[1-9]/.test(fraction.slice(6))) {
    throw new ContractError("Use an explicit UTC timestamp representable exactly to microseconds.");
  }
  if (milliseconds && timestamp_microseconds(normalized) % 1000n !== 0n) {
    throw new ContractError("The review clock must be exactly representable in milliseconds; it is never rounded.");
  }
  return normalized;
}

function native<K extends ContractName>(name: K, value: unknown, timestamps: readonly string[] = []): ContractTypes[K] {
  if (is_plain_object(value)) {
    timestamps.forEach((key): void => {
      if (value[key] !== null && value[key] !== undefined) exactTimestamp(value[key]);
    });
    if (Object.hasOwn(value, "reason")) reason(value.reason);
  }
  return from_wire(name, value);
}

/** Strict, duplicate-key-safe, bounded decoding; a kind never enables arbitrary JSON patches. */
export function parseChange(kind: ChangeKind, payloadJson: string): CaseChange {
  if (typeof payloadJson !== "string" || Buffer.byteLength(payloadJson, "utf8") > MAX_PAYLOAD_BYTES) {
    throw new ContractError("Change payload must be at most 256 KiB in UTF-8; it is never truncated.");
  }
  const raw = parse_json(payloadJson);
  canonical_json(raw); // Validate Unicode too, including opaque source text.
  switch (kind) {
    case "ADD_EVIDENCE": return { kind, payload: native("EvidenceInput", raw, ["occurredAt", "learnedAt"]) };
    case "ASSOCIATE_EVIDENCE": {
      const value = object(raw, ["evidenceId", "itemIds", "accepted", "reason"]);
      if (typeof value.accepted !== "boolean") throw new ContractError("accepted must be a boolean.");
      return { kind, payload: { evidenceId: text(value.evidenceId, "Evidence ID"),
        itemIds: strings(value.itemIds, "Item IDs"), accepted: value.accepted, reason: reason(value.reason) } };
    }
    case "ACCEPT_DATE_FACT": return { kind, payload: native("DateFact", raw) };
    case "RECORD_CHARGE_DECISION": {
      const value = object(raw, ["charge", "resolvedQuestionIds"]);
      return { kind, payload: { charge: native("ChargeInput", value.charge),
        resolvedQuestionIds: strings(value.resolvedQuestionIds, "Resolved question IDs") } };
    }
    case "WAIVE_CHARGE": {
      const value = object(raw, ["itemId", "reason"]);
      return { kind, payload: { itemId: text(value.itemId, "Item ID"), reason: reason(value.reason) } };
    }
    case "SET_RECIPIENTS": return { kind, payload: native("RecipientInstructions", raw) };
    case "RECORD_MONEY_EVENT": return { kind, payload: native("MoneyEvent", raw, ["occurredAt", "learnedAt"]) };
    case "RECONCILE_BALANCE": return { kind, payload: native("BalanceSnapshot", raw, ["asOf"]) };
    case "UPDATE_AUTHORITY": return { kind, payload: native("AuthorityGrant", raw, ["effectiveFrom", "effectiveUntil"]) };
    case "ASSIGN_WORK": {
      const value = object(raw, ["requirementKey", "assigneePartyId", "internalTargetAt", "reason"]);
      return { kind, payload: { requirementKey: text(value.requirementKey, "Requirement key"),
        assigneePartyId: text(value.assigneePartyId, "Assignee party ID"),
        internalTargetAt: value.internalTargetAt === null ? null : exactTimestamp(value.internalTargetAt),
        reason: reason(value.reason) } };
    }
    case "RECORD_RELATED_TASK": return { kind, payload: native("RelatedTaskFact", raw) };
    case "RECHECK": object(raw, []); return { kind, payload: {} };
    case "ADVANCE_DEMO_CLOCK": {
      const value = object(raw, ["reviewClock", "reason"]);
      return { kind, payload: { reviewClock: exactTimestamp(value.reviewClock, true), reason: reason(value.reason) } };
    }
    default: throw new ContractError("Unsupported Phase C change kind.");
  }
}

function same(left: unknown, right: unknown): boolean {
  return canonical_json(left) === canonical_json(right);
}

function one<T>(values: readonly T[], predicate: (value: T) => boolean, label: string): T {
  const matches = values.filter(predicate);
  const value = matches[0];
  requireCondition(value !== undefined && matches.every((other): boolean => same(other, value)),
    `${label} must identify an unambiguous record in this case.`);
  return value;
}

function replaceOrAdd<T>(values: readonly T[], value: T, keyOf: (entry: T) => string): T[] {
  const key = keyOf(value);
  const previous = values.filter((entry): boolean => keyOf(entry) === key);
  requireCondition(previous.length <= 1, "Resolve duplicate identities before changing this record.");
  return previous.length === 0 ? [...values, value]
    : values.map((entry): T => keyOf(entry) === key ? value : entry);
}

function evidence(snapshot: CaseSnapshot, ids: readonly string[], now: string): void {
  requireCondition(new Set(ids).size === ids.length && valid_evidence(snapshot, ids, now),
    "Use accepted, current case evidence with consistent source history and knowledge times, not a model proposal.");
}

function party(snapshot: CaseSnapshot, id: string): CaseParty {
  return one(snapshot.parties, (entry): boolean => entry.partyId === id, "Party ID");
}

function activeParty(snapshot: CaseSnapshot, value: CaseParty, now: string): void {
  const today = _local_date(now, "America/New_York");
  requireCondition((value.effectiveFrom === null || value.effectiveFrom <= today)
    && (value.effectiveUntil === null || today <= value.effectiveUntil), "The case party is not currently active.");
  evidence(snapshot, value.evidenceIds, now);
}

function requireAuthority(request: ReviewRequest, actorId: string, now: string,
  role: string, action: string, amount: number | null = null): void {
  requireCondition(hasAuthority(request, actorId, role, action, amount, now),
    `No current ${role.toLowerCase()} authority covers ${action} and its full amount.`);
}

function requireEvidenceChain(snapshot: CaseSnapshot, entry: EvidenceInput): void {
  const visited = new Set([entry.evidenceId]);
  let parentId = entry.supersedesEvidenceId;
  while (parentId !== null) {
    requireCondition(!visited.has(parentId), "Evidence supersession cannot contain a cycle or self-reference.");
    visited.add(parentId);
    const parent = one(snapshot.evidence, (value): boolean => value.evidenceId === parentId,
      "Superseded evidence ID");
    parentId = parent.supersedesEvidenceId;
  }
}

function requireChargeEvidence(snapshot: CaseSnapshot, item: ChargeInput, now: string): void {
  if (item.evidenceIds.length > 0) {
    evidence(snapshot, item.evidenceIds, now);
    item.evidenceIds.forEach((id): void => {
      const source = one(snapshot.evidence, (entry): boolean => entry.evidenceId === id, "Item evidence ID");
      requireCondition(source.proposedItemIds.includes(item.itemId), "Charge evidence must be associated with this item.");
    });
  }
  if (item.costVersionId !== null) {
    requireCondition(item.evidenceIds.includes(item.costVersionId), "The accepted cost version must be among this item's evidence IDs.");
    evidence(snapshot, [item.costVersionId], now);
  }
  if (item.costState === "KNOWN" || item.allowabilityState === "SUPPORTED"
    || ["CHOSEN", "WAIVED"].includes(item.choiceState)) {
    requireCondition(item.evidenceIds.length > 0 && item.costVersionId !== null
      && item.vendorCostCents !== null, "A supported or known cost needs its accepted item source and amount.");
  }
}

function requireExplicitChoice(request: ReviewRequest, item: ChargeInput, actorId: string, now: string): void {
  requireCondition(item.supportedAmountCents !== null && item.chosenAmountCents !== null,
    "An explicit charge choice needs the supported amount and chosen amount.");
  requireCondition(item.choiceState !== "WAIVED" || item.chosenAmountCents === 0,
    "A waiver must explicitly choose zero; it does not make an owner cost chargeable.");
  // Waiving 25000 cents exercises discretion over 25000, not over the zero outcome.
  requireAuthority(request, actorId, now, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", item.supportedAmountCents);
  const review = nativeReview(request);
  requireSupportedChoice(review, item.itemId, item.chosenAmountCents);
  const decision = review.result.itemDecisions.find((entry): boolean => entry.itemId === item.itemId);
  requireCondition(decision?.choiceState === item.choiceState
    && decision.chosenAmountCents === item.chosenAmountCents
    && decision.supportedAmountCents === item.supportedAmountCents,
  "The accepted decision must preserve the explicit choice without clamping or reinterpreting it.");
}

function recordCharge(request: ReviewRequest, change: Extract<CaseChange, { kind: "RECORD_CHARGE_DECISION" }>,
  actorId: string, now: string): void {
  requireAuthority(request, actorId, now, "MANAGER", "RECORD_CHARGE_DECISION");
  const snapshot = request.snapshot;
  const { charge: item, resolvedQuestionIds: resolved } = change.payload;
  identifier(item.itemId, "Item ID");
  requireChargeEvidence(snapshot, item, now);
  const previous = snapshot.charges.find((entry): boolean => entry.itemId === item.itemId);
  if (previous !== undefined && (previous.category === "ORDINARY_OWNER_REPAINTING"
    || previous.allowabilityState === "DISALLOWED")) {
    requireCondition(item.category === previous.category && item.allowabilityState !== "SUPPORTED"
      && !["CHOSEN", "WAIVED"].includes(item.choiceState),
    "An existing owner/disallowed cost cannot be relabeled as a supported tenant charge or waiver.");
  }
  if (item.choiceState === "NOT_DECIDED") {
    requireCondition(item.chosenAmountCents === null, "An undecided charge must retain an unknown chosen amount, not zero.");
  }
  resolved.forEach((id): void => {
    const question = snapshot.questions.find((entry): boolean => entry.questionId === id);
    requireCondition(previous?.unresolvedQuestionIds.includes(id) === true
      || question?.affectedItemIds.includes(item.itemId) === true, "Resolve only this item's existing question references.");
    requireCondition(!snapshot.charges.some((entry): boolean => entry.itemId !== item.itemId
      && entry.unresolvedQuestionIds.includes(id))
      && !snapshot.questions.some((entry): boolean => entry.questionId === id
        && entry.affectedItemIds.some((itemId): boolean => itemId !== item.itemId)),
    "A question still affecting another item cannot be cleared by this decision.");
  });
  const remaining = item.unresolvedQuestionIds.filter((id): boolean => !resolved.includes(id));
  requireCondition(new Set(remaining).size === remaining.length
    && (previous?.unresolvedQuestionIds ?? []).every((id): boolean => resolved.includes(id) || remaining.includes(id)),
  "Keep unresolved references unless they are explicitly listed for resolution.");
  remaining.forEach((id): void => {
    requireCondition(previous?.unresolvedQuestionIds.includes(id) === true
      || snapshot.questions.some((entry): boolean => entry.questionId === id && entry.affectedItemIds.includes(item.itemId)),
    "Unresolved question references must belong to this case item.");
  });
  item.unresolvedQuestionIds = remaining;
  snapshot.charges = replaceOrAdd(snapshot.charges, item, (entry): string => entry.itemId);
  // Tentative copy only: errors below cannot leak question removals to caller-owned state.
  snapshot.questions = snapshot.questions.filter((entry): boolean => !resolved.includes(entry.questionId));
  if (["CHOSEN", "WAIVED"].includes(item.choiceState)) requireExplicitChoice(request, item, actorId, now);
  const decision = nativeReview(request).result.itemDecisions.find((entry): boolean => entry.itemId === item.itemId);
  if (item.choiceState === "NOT_APPLICABLE") {
    requireCondition(decision?.allowability === "DISALLOWED" && decision.choiceState === "NOT_APPLICABLE"
      && item.chosenAmountCents === 0, "Not-applicable is exclusion of a disallowed cost, not a substitute for a charge decision.");
  }
  if (resolved.length > 0) {
    requireCondition(decision !== undefined && !decision.requiresReviewer && decision.missingInputIds.length === 0
      && ["SUPPORTED", "DISALLOWED"].includes(decision.allowability),
    "Resolve item questions only after establishing a valid complete native decision.");
  }
}

/**
 * Apply one human-requested transition to cloned native DTOs only.
 * @param request Trusted case snapshot; strict shape is checked, revision is never incremented here.
 * @param workAssignments Existing internal-only sidecar work assignments.
 * @param change One explicit supported operation; decoded again to prevent typed-call bypasses.
 * @param actorId Actual principal supplied by the server adapter, not the payload.
 * @param now Actual server time for authority/evidence; independent of the historical review clock.
 * @param isAdministrator Trusted root permission from the adapter, never a case role claim.
 * @param requirements Trusted current effective review requirements from the adapter, never payload or permission overrides.
 * @returns New state and scalar audit summary. No storage, external effects, or clock source is used.
 */
export function applyChange(request: ReviewRequest, workAssignments: readonly WorkAssignment[],
  change: CaseChange, actorId: string, now: string, isAdministrator: boolean,
  requirements?: readonly RequirementResult[]): ChangeResult {
  const next = from_wire("ReviewRequest", request);
  const assignments = structuredClone([...workAssignments]);
  const input = parseChange(change.kind, canonical_json(change.payload));
  const serverNow = exactTimestamp(now, true);
  const snapshot = next.snapshot;
  const summary: ChangeResult["summary"] = { kind: input.kind };
  const manager = (): void => requireAuthority(next, actorId, serverNow, "MANAGER", "ACCEPT_OR_CORRECT_FACT");
  const accountant = (): void => requireAuthority(next, actorId, serverNow, "ACCOUNTANT", "RECONCILE_MONEY_RECORD");

  switch (input.kind) {
    case "ADD_EVIDENCE": {
      manager();
      const entry = input.payload;
      identifier(entry.evidenceId, "Evidence ID");
      const existing = snapshot.evidence.filter((value): boolean => value.evidenceId === entry.evidenceId);
      if (existing.length > 0) {
        // Association is separate mutable context. An intake retry must not undo a later human association.
        requireCondition(existing.every((value): boolean => same(
          { ...value, associationAccepted: false, proposedItemIds: [] },
          { ...entry, associationAccepted: false, proposedItemIds: [] },
        )), "Changed evidence content requires a new evidence version ID; source records are immutable.");
        break;
      }
      requireCondition(!entry.associationAccepted, "New intake evidence cannot auto-accept its own association; associate it explicitly later.");
      requireCondition(entry.occurredAt === null || compare_timestamps(entry.occurredAt, entry.learnedAt) <= 0,
        "Evidence occurrence cannot follow its learned time.");
      requireEvidenceChain(snapshot, entry);
      snapshot.evidence.push(entry);
      summary.evidenceId = entry.evidenceId;
      break;
    }
    case "ASSOCIATE_EVIDENCE": {
      manager();
      const { evidenceId, itemIds, accepted } = input.payload;
      const entry = one(snapshot.evidence, (value): boolean => value.evidenceId === evidenceId, "Evidence ID");
      itemIds.forEach((id): void => { one(snapshot.charges, (value): boolean => value.itemId === id, "Item ID"); });
      requireEvidenceChain(snapshot, entry);
      snapshot.evidence = snapshot.evidence.map((value): EvidenceInput => value.evidenceId === evidenceId
        ? { ...value, associationAccepted: accepted, proposedItemIds: [...itemIds] } : value);
      if (accepted) evidence(snapshot, [evidenceId], serverNow);
      summary.evidenceId = evidenceId;
      summary.reason = input.payload.reason;
      break;
    }
    case "ACCEPT_DATE_FACT": {
      manager();
      const fact = input.payload;
      requireCondition(snapshot.dates.some((value): boolean => value.factKey === fact.factKey)
        || VOCABULARY.dateKey.some((key): boolean => key === fact.factKey), "Use a known native date fact key.");
      const actorParty = party(snapshot, fact.acceptedBy ?? "");
      activeParty(snapshot, actorParty, serverNow);
      const grants = new Set(_authority(snapshot, "ACCEPT_OR_CORRECT_FACT", "MANAGER", null, serverNow));
      requireCondition(actorParty.principalId === actorId && actorParty.roles.includes("MANAGER")
        && snapshot.authorityGrants.some((grant): boolean => grant.partyId === actorParty.partyId && grants.has(grant.grantId)),
      "acceptedBy must be the actual actor's currently authorized case party ID.");
      if (fact.state === "ACCEPTED") {
        requireCondition(fact.value !== null, "An accepted date fact needs its explicit date value.");
        evidence(snapshot, fact.evidenceIds, serverNow);
      } else if (fact.evidenceIds.length > 0) evidence(snapshot, fact.evidenceIds, serverNow);
      snapshot.dates = replaceOrAdd(snapshot.dates, fact, (entry): string => entry.factKey);
      summary.factKey = fact.factKey;
      summary.reason = fact.reason;
      break;
    }
    case "RECORD_CHARGE_DECISION":
      recordCharge(next, input, actorId, serverNow);
      summary.itemId = input.payload.charge.itemId;
      summary.reason = input.payload.charge.reason;
      summary.resolvedQuestionCount = input.payload.resolvedQuestionIds.length;
      break;
    case "WAIVE_CHARGE": {
      const item = one(snapshot.charges, (entry): boolean => entry.itemId === input.payload.itemId, "Item ID");
      const review = nativeReview(next);
      const supported = review.result.itemDecisions.find((entry): boolean => entry.itemId === item.itemId)?.supportedAmountCents;
      requireCondition(supported !== undefined && supported !== null, "Only an existing supported charge can be waived.");
      requireSupportedChoice(review, item.itemId, supported);
      requireChargeEvidence(snapshot, item, serverNow);
      requireAuthority(next, actorId, serverNow, "MANAGER", "CHOOSE_OR_WAIVE_CHARGE", supported);
      item.choiceState = "WAIVED";
      item.chosenAmountCents = 0;
      item.reason = input.payload.reason;
      requireExplicitChoice(next, item, actorId, serverNow);
      summary.itemId = item.itemId;
      summary.reason = item.reason;
      break;
    }
    case "SET_RECIPIENTS": {
      manager();
      const recipients = input.payload;
      identifier(recipients.versionId, "Recipient version ID");
      if (recipients.versionId === snapshot.recipients.versionId) {
        requireCondition(same(recipients, snapshot.recipients), "Changed recipient content requires a new version ID.");
        break;
      }
      requireCondition(recipients.statementMethod === "DEMO_OUTBOX" && recipients.refundMethod === "DEMO_OUTBOX",
        "Only DEMO_OUTBOX methods are enabled; no external delivery or payment route is accepted.");
      requireCondition(recipients.verifiedRouteReference === null
        || /^demo-[A-Za-z0-9][A-Za-z0-9._-]{0,199}$/.test(recipients.verifiedRouteReference),
      "Use an opaque demo- route reference, never an external address or payment destination.");
      [recipients.statementPartyIds, recipients.refundPartyIds].forEach((ids): void => {
        requireCondition(new Set(ids).size === ids.length, "Recipient party IDs must be unique.");
        ids.forEach((id): void => {
          const selected = party(snapshot, id);
          requireCondition(selected.roles.some((role): boolean => ["RESIDENT", "SIGNATORY"].includes(role)),
            "Select only this tenancy's resident/signatory recipients.");
          evidence(snapshot, selected.evidenceIds, serverNow);
        });
      });
      if (recipients.evidenceIds.length > 0) evidence(snapshot, recipients.evidenceIds, serverNow);
      if (recipients.state === "VERIFIED") {
        requireCondition(recipients.statementPartyIds.length > 0 && recipients.refundPartyIds.length > 0
          && recipients.verifiedRouteReference !== null, "Verification needs statement/refund recipients and a demo route.");
        evidence(snapshot, recipients.evidenceIds, serverNow);
      }
      snapshot.recipients = recipients;
      summary.versionId = recipients.versionId;
      break;
    }
    case "RECORD_MONEY_EVENT": {
      accountant();
      const event = input.payload;
      [event.eventId, event.canonicalTransactionId, event.sourceEventId].forEach((id): void => identifier(id, "Money record ID"));
      const previous = snapshot.moneyEvents.filter((entry): boolean => entry.eventId === event.eventId);
      if (previous.length > 0) {
        requireCondition(previous.every((entry): boolean => same(entry, event)), "Changed event content requires a new event ID.");
        break;
      }
      evidence(snapshot, [event.sourceEvidenceId], serverNow);
      if (event.chargeItemId !== null) one(snapshot.charges, (entry): boolean => entry.itemId === event.chargeItemId, "Money charge item ID");
      if (event.requestId !== null) one(snapshot.priorRequests, (entry): boolean => entry.requestId === event.requestId, "Money request ID");
      if (event.reversesTransactionId !== null) {
        requireCondition(snapshot.moneyEvents.some((entry): boolean => entry.canonicalTransactionId === event.reversesTransactionId),
          "A reversal must reference a recorded case transaction.");
      }
      // Canonical/source aliases and financial inconsistencies remain facts for native reconciliation.
      snapshot.moneyEvents.push(event);
      summary.eventId = event.eventId;
      break;
    }
    case "RECONCILE_BALANCE": {
      accountant();
      const balance = input.payload;
      identifier(balance.balanceId, "Balance version ID");
      if (balance.balanceId === snapshot.depositBalance.balanceId) {
        requireCondition(same(balance, snapshot.depositBalance), "Changed balance content requires a new balance version ID.");
        break;
      }
      evidence(snapshot, [balance.sourceEvidenceId], serverNow);
      if (balance.custodianPartyId !== null) party(snapshot, balance.custodianPartyId);
      // Included transactions, unknown amounts and contradictory accounting facts are assessed by the core.
      snapshot.depositBalance = balance;
      summary.balanceId = balance.balanceId;
      break;
    }
    case "UPDATE_AUTHORITY": {
      requireCondition(isAdministrator === true, "Only a trusted case administrator may update authority.");
      const grant = input.payload;
      identifier(grant.grantId, "Grant ID");
      identifier(grant.authorityVersion, "Authority version ID");
      const target = party(snapshot, grant.partyId);
      requireCondition(target.principalId === BOOTSTRAP_ACTOR_ID,
        "Authority may reference only a case party mapped to the approved synthetic principal.");
      evidence(snapshot, target.evidenceIds, serverNow);
      evidence(snapshot, grant.evidenceIds, serverNow);
      requireCondition(grant.evidenceIds.every((id): boolean => snapshot.evidence
        .some((entry): boolean => entry.evidenceId === id && entry.recordKind === "AUTHORITY_RECORD")),
      "Authority changes require an accepted AUTHORITY_RECORD, not a party label or source instruction.");
      requireCondition(grant.effectiveUntil === null || compare_timestamps(grant.effectiveFrom, grant.effectiveUntil) < 0,
        "Authority expiry must be strictly after its effective start.");
      requireCondition(new Set(grant.allowedActionKinds).size === grant.allowedActionKinds.length,
        "Authority action kinds must not repeat.");
      const previous = snapshot.authorityGrants.find((entry): boolean => entry.grantId === grant.grantId);
      requireCondition(previous === undefined || previous.authorityVersion !== grant.authorityVersion || same(previous, grant),
        "Changed grant content requires a new authority version.");
      snapshot.authorityGrants = replaceOrAdd(snapshot.authorityGrants, grant, (entry): string => entry.grantId);
      summary.grantId = grant.grantId;
      summary.authorityVersion = grant.authorityVersion;
      break;
    }
    case "ASSIGN_WORK": {
      manager();
      const payload = input.payload;
      const requirement = (requirements ?? nativeReview(next).result.scopeRequirements.requirements)
        .find((entry): boolean => entry.requirementKey === payload.requirementKey);
      requireCondition(requirement !== undefined, "Assign only a requirement in the current review.");
      const assignee = party(snapshot, payload.assigneePartyId);
      requireCondition(assignee.roles.includes(requirement.responsibleRole), "The assignee must match the requirement's responsible role.");
      activeParty(snapshot, assignee, serverNow);
      const assignment: WorkAssignment = { ...payload, assignedBy: actorId, assignedAt: serverNow };
      const updated = replaceOrAdd(assignments, assignment, (entry): string => entry.requirementKey);
      assignments.splice(0, assignments.length, ...updated);
      summary.requirementKey = payload.requirementKey;
      summary.reason = payload.reason;
      break;
    }
    case "RECORD_RELATED_TASK": {
      const task = input.payload;
      identifier(task.taskId, "Related task ID");
      const previous = snapshot.relatedTasks.find((entry): boolean => entry.taskId === task.taskId);
      const roles = new Set([task.responsibleRole, ...(previous === undefined ? [] : [previous.responsibleRole])]);
      // A role change cannot downgrade the authority needed for existing accounting work.
      roles.forEach((role): void => { if (role === "ACCOUNTANT") accountant(); else manager(); });
      if (["FULFILLED", "NOT_APPLICABLE"].includes(task.state) || task.completionEvidenceIds.length > 0) {
        evidence(snapshot, task.completionEvidenceIds, serverNow);
      }
      snapshot.relatedTasks = replaceOrAdd(snapshot.relatedTasks, task, (entry): string => entry.taskId);
      summary.taskId = task.taskId;
      break;
    }
    case "RECHECK": next.reviewClock = serverNow; break;
    case "ADVANCE_DEMO_CLOCK":
      requireCondition(isAdministrator === true && snapshot.origin === "CONSTRUCTED",
        "Only a trusted administrator may advance the synthetic demonstration clock.");
      requireCondition(compare_timestamps(input.payload.reviewClock, next.reviewClock) >= 0,
        "The demonstration clock may only advance, never move backward.");
      next.reviewClock = input.payload.reviewClock;
      summary.reason = input.payload.reason;
      break;
  }
  summary.changed = !same(request, next) || !same(workAssignments, assignments);
  return { request: next, workAssignments: assignments, summary };
}
