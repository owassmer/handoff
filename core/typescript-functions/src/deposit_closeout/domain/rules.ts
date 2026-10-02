/** Bounded synthetic NC decisions, not an approved interpretation of NC law. */
import { isDeepStrictEqual } from "node:util";
import type { ReviewRuleRelease } from "./phase_b_types.js";
import type { CaseSnapshot, OpenQuestion } from "./types.js";
import { question, valid_evidence } from "./validation.js";

export interface ScopeReview {
  supported: boolean;
  state: string;
  trigger: string | null;
  ordinaryDue: string | null;
  finalDue: string | null;
  interimQualified: boolean;
  questions: OpenQuestion[];
  limitations: string[];
}

/** Compare DTOs structurally, including ordered lists. */
export function _same(left: unknown, right: unknown): boolean {
  return isDeepStrictEqual(left, right);
}

/** Sort by Unicode code points, not JavaScript UTF-16 code units or locale collation. */
export function _compare_text(left: string, right: string): number {
  const a = Array.from(left);
  const b = Array.from(right);
  for (let index = 0; index < Math.min(a.length, b.length); index += 1) {
    const delta = a[index]!.codePointAt(0)! - b[index]!.codePointAt(0)!;
    if (delta !== 0) return delta;
  }
  return a.length - b.length;
}

export function _sorted_unique(values: Iterable<string>): string[] {
  return [...new Set(values)].sort(_compare_text);
}

/** Inputs are canonical UTC from the codec. Padding preserves microsecond ordering. */
export function _compare_timestamps(left: string, right: string): number {
  const key = (value: string): string => {
    const body = value.slice(0, -1);
    const [seconds, fraction = ""] = body.split(".");
    return `${seconds}.${fraction.padEnd(6, "0")}Z`;
  };
  const a = key(left);
  const b = key(right);
  return a < b ? -1 : a > b ? 1 : 0;
}

/** Calendar date is derived only from the supplied instant, never the host date/time zone. */
export function _local_date(clock: string, time_zone: string): string {
  const parts = new Intl.DateTimeFormat("en-US-u-ca-gregory-nu-latn", {
    timeZone: time_zone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    era: "short",
  }).formatToParts(new Date(clock));
  const fields = new Map(parts.map((part) => [part.type, part.value]));
  const year = fields.get("year")!;
  if (fields.get("era") !== "AD" || Number(year) > 9999) {
    throw new RangeError("The supplied clock is outside the supported local calendar range");
  }
  return `${year.padStart(4, "0")}-${fields.get("month")!}-${fields.get("day")!}`;
}

function _date_plus_days(value: string, days: number): string | null {
  const date = new Date(`${value}T00:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  if (!Number.isFinite(date.getTime()) || date.getUTCFullYear() > 9999 || date.getUTCFullYear() < 1) {
    return null;
  }
  return date.toISOString().slice(0, 10);
}

/**
 * Project scope and the separately accepted synthetic accounting trigger.
 * @param snapshot Complete constructed snapshot; never mutated.
 * @param release Explicit validated Phase B release, not the Phase A manifest.
 * @param clock Canonical UTC timestamp supplied by the caller.
 */
export function review_scope(
  snapshot: CaseSnapshot,
  release: ReviewRuleRelease,
  clock: string,
): ScopeReview {
  const limitations = [
    "SYNTHETIC_ONLY: accepted legal and causation assumptions are constructed test inputs, not legal findings.",
    "Primary-source/legal review remains pending. Thirty/sixty days are supplied test assumptions relative to the separately accepted ACCOUNTING_TRIGGER.",
    "Phase B is a read-only projection: no Actions, dispatch, ledger posting, payment or authority is executed or granted.",
    "Interim money, missing-address and legal-performance predicates remain unresolved; no automatic full withholding or check-clearance rule.",
  ];
  const questions: OpenQuestion[] = [];
  const unsupported = !["NC", "UNKNOWN", "UNCONFIRMED"].includes(snapshot.jurisdiction)
    || !["CONVENTIONAL_RESIDENTIAL", "UNKNOWN", "UNCONFIRMED"].includes(snapshot.tenancyRegime)
    || snapshot.tenancyEndsInFull === false || snapshot.cashSecurityDeposit === false
    || snapshot.specialCircumstances.length > 0;
  let missing = ["UNKNOWN", "UNCONFIRMED"].includes(snapshot.jurisdiction)
    || ["UNKNOWN", "UNCONFIRMED"].includes(snapshot.tenancyRegime)
    || snapshot.tenancyEndsInFull === null || snapshot.cashSecurityDeposit === null;
  if (unsupported) {
    questions.push(question("scope:unsupported", "Which reviewed rules cover these circumstances?", "This release covers only constructed NC conventional residential full-ending cash-deposit cases. No NC fallback is applied.", "REVIEWER", [], ["ADD_EVIDENCE"], "Reviewed jurisdiction/regime-specific rule release"));
    return { supported: false, state: "UNSUPPORTED", trigger: null, ordinaryDue: null, finalDue: null, interimQualified: false, questions, limitations };
  }
  if (missing) {
    questions.push(question("scope:facts", "Confirm jurisdiction, tenancy regime, full ending and deposit type.", "One or more scope-defining facts is explicitly unknown; do not infer conventional scope.", "MANAGER", [], undefined, "Operative agreement and scope facts"));
  }
  if (!valid_evidence(snapshot, snapshot.agreementEvidenceIds, clock)) {
    questions.push(question("scope:agreement", "Which operative agreement establishes this tenancy?", "Agreement evidence is missing, conflicting, unassociated or not yet known.", "MANAGER", [], undefined, "Operative agreement and amendments"));
    missing = true;
  }
  const resident = snapshot.parties.filter((party) => party.roles.some((role) => ["RESIDENT", "SIGNATORY"].includes(role)));
  if (resident.length === 0 || resident.some((party) => !valid_evidence(snapshot, party.evidenceIds, clock))) {
    questions.push(question("scope:parties", "Confirm the tenancy's resident/signatory membership.", "Identity and agreement membership cannot be inferred from the most recent payer or email.", "MANAGER", [], undefined, "Agreement membership and effective dates"));
    missing = true;
  }
  if (missing) {
    return { supported: false, state: "MISSING_FACTS", trigger: null, ordinaryDue: null, finalDue: null, interimQualified: false, questions, limitations };
  }
  const triggers = snapshot.dates.filter((fact) => fact.factKey === "ACCOUNTING_TRIGGER");
  const today = _local_date(clock, release.timeZone);
  const known_parties = new Set(snapshot.parties.map((party) => party.partyId));
  let trigger: string | null = null;
  if (triggers.length > 0 && triggers.every((fact) => _same(fact, triggers[0]))) {
    const fact = triggers[0]!;
    if (fact.state === "ACCEPTED" && fact.value !== null && fact.value <= today
      && fact.acceptedBy !== null && known_parties.has(fact.acceptedBy)
      && valid_evidence(snapshot, fact.evidenceIds, clock)) {
      trigger = fact.value;
    }
  }
  if (trigger === null) {
    questions.push(question("scope:trigger", "What accepted event establishes the accounting trigger?", "Keep notice, intended departure, agreement end, vacancy, key return and legal possession distinct. No definitive deadline is computed from an unconfirmed/disputed/future trigger.", "MANAGER", [], ["ACCEPT_OR_CORRECT_FACT"], "Separately accepted trigger, evidence, actor and reason"));
  }
  const qualifies = snapshot.interimConditionState === "ACCEPTED"
    && valid_evidence(snapshot, snapshot.interimConditionEvidenceIds, clock);
  if (["ACCEPTED", "DISPUTED"].includes(snapshot.interimConditionState) && !qualifies) {
    questions.push(question("scope:interim-qualification", "What evidence supports the separate interim condition?", "An accepted flag without usable evidence or a disputed condition does not select the interim route; a missing invoice alone is insufficient.", "REVIEWER", [], undefined, "Accepted qualifying condition and supporting facts"));
  }
  let ordinary = trigger === null ? null : _date_plus_days(trigger, release.ordinaryPeriodDays);
  let final = trigger === null ? null : _date_plus_days(trigger, release.finalPeriodDays);
  if (trigger !== null && (ordinary === null || final === null)) {
    ordinary = null;
    final = null;
    questions.push(question("scope:date-range", "Supply dates within the supported calendar range.", "The synthetic period calculation exceeds the representable calendar; no truncated or wrapped deadline is used.", "MANAGER", [], undefined, "Corrected trigger date"));
  }
  return { supported: true, state: "SUPPORTED", trigger, ordinaryDue: ordinary, finalDue: final, interimQualified: qualifies, questions, limitations };
}
