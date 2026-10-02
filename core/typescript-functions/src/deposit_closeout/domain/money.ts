/**
 * Pure money projection with no I/O, implicit clock or action authority.
 * Representation errors throw; incomplete/conflicting records produce questions.
 * Monetary aggregates are computed as bigint and bounded before conversion to wire numbers.
 */
import { ContractError } from "./codec.js";
import type {
  AccountResult, CaseSnapshot, ChargeInput, EvidenceInput, ItemDecision,
  MoneyEvent, OpenQuestion, RequestFact,
} from "./types.js";
import { MAX_SAFE_INTEGER } from "./vocabulary.js";

export interface MoneyReview {
  account: AccountResult;
  questions: OpenQuestion[];
  moneyState: string;
  moneyReason: string;
  hasUnknownResult: boolean;
  hasReturn: boolean;
}

export const _KIND_STATUS: ReadonlyMap<string, ReadonlySet<string>> = new Map([
  ["DEPOSIT_RECEIPT", new Set(["SETTLED"])],
  ["DEPOSIT_TRANSFER_IN", new Set(["SETTLED"])],
  ["DEPOSIT_TRANSFER_OUT", new Set(["SETTLED"])],
  ["DEPOSIT_APPLICATION", new Set(["SETTLED", "REVERSED"])],
  ["CHARGE_POSTING", new Set(["SETTLED", "REVERSED"])],
  ["DEPOSIT_APPLICATION_REVERSAL", new Set(["SETTLED"])],
  ["CHARGE_POSTING_REVERSAL", new Set(["SETTLED"])],
  ["REFUND_INITIATED", new Set(["PENDING"])],
  ["REFUND_SETTLED", new Set(["SETTLED"])],
  ["REFUND_FAILED", new Set(["FAILED"])],
  ["REFUND_RETURNED", new Set(["RETURNED"])],
]);
export const _REFUND_KINDS: ReadonlySet<string> = new Set([
  "REFUND_INITIATED", "REFUND_SETTLED", "REFUND_FAILED", "REFUND_RETURNED",
]);
export const _ACTIVE_REQUESTS: ReadonlySet<string> = new Set([
  "READY", "CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN",
]);
export const _REQUEST_STATES: ReadonlySet<string> = new Set([
  ..._ACTIVE_REQUESTS, "SUCCEEDED", "FAILED", "CANCELLED", "SUPERSEDED",
]);
export const _MONEY_ACTIONS: ReadonlySet<string> = new Set([
  "REQUEST_REFUND", "REQUEST_LEDGER_POSTING",
]);
const EFFECT_STATES: ReadonlySet<string> = new Set(["SETTLED", "RETURNED", "REVERSED"]);
const BOUND = BigInt(MAX_SAFE_INTEGER);

export function _bounded(value: unknown, name: string, nonnegative: boolean = false): number {
  const lower = nonnegative ? 0 : -MAX_SAFE_INTEGER;
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value < lower || value > MAX_SAFE_INTEGER) {
    throw new ContractError(`${name}: expected an exact bounded integer, not bool/float/string or overflow`);
  }
  return value === 0 ? 0 : value;
}

/** A bigint is internal only; wire/programmatic monetary inputs still require numbers. */
function bounded_integer(value: bigint, name: string, nonnegative: boolean = false): number {
  const lower = nonnegative ? 0n : -BOUND;
  if (value < lower || value > BOUND) {
    throw new ContractError(`${name}: expected an exact bounded integer, not bool/float/string or overflow`);
  }
  return Number(value);
}

function sum_money(values: Iterable<number | bigint>): bigint {
  let total = 0n;
  for (const value of values) total += BigInt(value);
  return total;
}

export function _amount(value: unknown, name: string): void {
  if (value !== null) _bounded(value, name, true);
}

/** Preserve microsecond timestamp precision beyond JavaScript Date milliseconds. */
function instant(value: unknown, name: string): bigint {
  const fail = (): never => {
    throw new ContractError(`${name}: expected a timezone-aware timestamp`);
  };
  if (typeof value !== "string") return fail();
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:[.,](\d+))?(Z|[+-]\d{2}:?\d{2})$/.exec(value);
  if (match === null) return fail();
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const hour = Number(match[4]);
  const minute = Number(match[5]);
  const second = Number(match[6]);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (year < 1 || month < 1 || month > 12 || day < 1 || day > days[month - 1]! || hour > 23 || minute > 59 || second > 59) return fail();
  const milliseconds = Date.parse(`${match[1]}-${match[2]}-${match[3]}T${match[4]}:${match[5]}:${match[6]}Z`);
  if (!Number.isFinite(milliseconds)) return fail();
  const zone = match[8]!;
  let offsetSeconds = 0;
  if (zone !== "Z") {
    const compact = zone.slice(1).replace(":", "");
    const hours = Number(compact.slice(0, 2));
    const minutes = Number(compact.slice(2, 4));
    if (hours > 23 || minutes > 59) return fail();
    offsetSeconds = (hours * 3600 + minutes * 60) * (zone[0] === "+" ? 1 : -1);
  }
  const fraction = (match[7] ?? "").padEnd(6, "0").slice(0, 6);
  return BigInt(milliseconds) * 1000n + BigInt(fraction) - BigInt(offsetSeconds) * 1000000n;
}

export function _time(value: unknown, name: string): string {
  instant(value, name);
  return value as string;
}

export function _id(value: unknown, name: string): string {
  if (typeof value !== "string" || value.length === 0) {
    throw new ContractError(`${name}: expected a non-empty identifier`);
  }
  return value;
}

/** Use Unicode code-point ordering, including supplementary characters. */
function compare_text(left: string, right: string): number {
  const a = Array.from(left);
  const b = Array.from(right);
  for (let index = 0; index < Math.min(a.length, b.length); index += 1) {
    const difference = a[index]!.codePointAt(0)! - b[index]!.codePointAt(0)!;
    if (difference !== 0) return difference;
  }
  return a.length - b.length;
}

function sorted_text(values: Iterable<string>): string[] {
  return [...values].sort(compare_text);
}

function sorted_entries<T>(values: ReadonlyMap<string, T>): [string, T][] {
  return [...values.entries()].sort(([a], [b]) => compare_text(a, b));
}

function equal_value(left: unknown, right: unknown): boolean {
  if (left === right) return true;
  if (Array.isArray(left) || Array.isArray(right)) {
    if (!Array.isArray(left) || !Array.isArray(right) || left.length !== right.length) return false;
    return (left as unknown[]).every((value: unknown, index: number): boolean => equal_value(value, (right as unknown[])[index]));
  }
  if (left === null || right === null || typeof left !== "object" || typeof right !== "object") return false;
  const a = left as Record<string, unknown>;
  const b = right as Record<string, unknown>;
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every((key: string): boolean => Object.prototype.hasOwnProperty.call(b, key) && equal_value(a[key], b[key]));
}

function evidence_payload(evidence: EvidenceInput): unknown {
  return {
    ...evidence,
    learnedAt: instant(evidence.learnedAt, `evidence:${evidence.evidenceId}.learnedAt`).toString(),
    occurredAt: evidence.occurredAt === null ? null : instant(evidence.occurredAt, `evidence:${evidence.evidenceId}.occurredAt`).toString(),
  };
}

interface ProblemOptions {
  item?: string | null;
  ledger?: boolean;
  conflict?: boolean;
}

type ProblemEntry = [Set<string>, string, Set<string>];

export class _Problems {
  readonly entries = new Map<string, ProblemEntry>();
  ledger_bad = false;
  conflict = false;

  add(key: string, reason: string, record: string, options: ProblemOptions = {}): void {
    const { item = null, ledger = true, conflict = false } = options;
    if (!this.entries.has(key)) this.entries.set(key, [new Set(), record, new Set()]);
    const [reasons, , items] = this.entries.get(key)!;
    reasons.add(reason);
    if (item !== null) items.add(item);
    this.ledger_bad ||= ledger;
    this.conflict ||= ledger && conflict;
  }

  questions(): OpenQuestion[] {
    return sorted_entries(this.entries).map(([key, [reasons, record, items]]): OpenQuestion => ({
      questionId: key,
      question: "What verified accounting record resolves this money review issue?",
      reason: sorted_text(reasons).join(" "),
      resolverRole: "ACCOUNTANT",
      resolverPartyId: null,
      neededRecord: record,
      affectedItemIds: sorted_text(items),
      affectedActionKinds: ["RECONCILE_MONEY_RECORD", "PREPARE_STATEMENT", "REQUEST_REFUND", "REQUEST_LEDGER_POSTING"],
    }));
  }
}

export function _chosen(snapshot: CaseSnapshot, decisions: readonly ItemDecision[], p: _Problems): [number, string[]] {
  const charges = new Map<string, ChargeInput>();
  const ambiguous = new Set<string>();
  snapshot.charges.forEach((charge: ChargeInput): void => {
    _id(charge.itemId, "charge.itemId");
    (["vendorCostCents", "supportedAmountCents", "chosenAmountCents"] as const).forEach((name): void => {
      _amount(charge[name], `charge:${charge.itemId}.${name}`);
    });
    if (charges.has(charge.itemId) && !equal_value(charges.get(charge.itemId), charge)) ambiguous.add(charge.itemId);
    charges.set(charge.itemId, charge);
  });
  const by_id = new Map<string, ItemDecision>();
  decisions.forEach((decision: ItemDecision): void => {
    _id(decision.itemId, "decision.itemId");
    (["vendorCostCents", "supportedAmountCents", "chosenAmountCents"] as const).forEach((name): void => {
      _amount(decision[name], `decision:${decision.itemId}.${name}`);
    });
    if (by_id.has(decision.itemId) && !equal_value(by_id.get(decision.itemId), decision)) ambiguous.add(decision.itemId);
    by_id.set(decision.itemId, decision);
  });
  const known: number[] = [];
  const unresolved: string[] = [];
  sorted_text(new Set([...charges.keys(), ...by_id.keys()])).forEach((item: string): void => {
    const d = by_id.get(item);
    let reason: string | null = null;
    if (ambiguous.has(item) || !charges.has(item) || d === undefined) {
      reason = "Provide one consistent decision for this supplied charge; missing, extra or contradictory decisions cannot be totaled.";
    } else if (d.allocation === "OWNER") {
      if (d.chosenAmountCents !== null && d.chosenAmountCents !== 0) reason = "Owner cost cannot also be a chosen resident deduction.";
    } else if (d.choiceState === "WAIVED" && d.chosenAmountCents === 0) {
      // Deliberate zero, not an estimate of an unknown cost.
    } else if (d.allowability === "DISALLOWED" && d.chosenAmountCents === 0 && d.choiceState === "NOT_APPLICABLE") {
      // Explicitly disallowed, with no resident deduction.
    } else if ((d.allocation === "TENANT" || d.allocation === "SPLIT") && d.allowability === "SUPPORTED"
      && d.choiceState === "CHOSEN" && d.chosenAmountCents !== null
      && d.supportedAmountCents !== null && d.chosenAmountCents <= d.supportedAmountCents) {
      known.push(d.chosenAmountCents);
      if (d.requiresReviewer || d.missingInputIds.length > 0) reason = "The supported chosen subtotal is known, but the decision still identifies a required review or missing input.";
    } else {
      reason = "Resolve the allocation, category/allowability, supported amount and explicit choice; unknown is not zero.";
    }
    if (reason === null && d !== undefined && (d.requiresReviewer || d.missingInputIds.length > 0)) {
      reason = "An explicit required review or unresolved basis remains, including for a waiver or owner exclusion; zero does not complete that work.";
    }
    if (reason !== null) {
      unresolved.push(item);
      p.add(`money:item:${item}`, reason, `Accepted item decision and supporting record for ${item}`, { item, ledger: false });
    }
  });
  return [bounded_integer(sum_money(known), "knownChosenDeductionsCents", true), unresolved];
}

export function _requests(snapshot: CaseSnapshot, p: _Problems): Map<string, RequestFact> {
  const grouped = new Map<string, RequestFact[]>();
  snapshot.priorRequests.forEach((r: RequestFact): void => {
    _id(r.requestId, "request.requestId");
    _amount(r.amountCents, `request:${r.requestId}.amountCents`);
    if (!grouped.has(r.requestId)) grouped.set(r.requestId, []);
    grouped.get(r.requestId)!.push(r);
  });
  const result = new Map<string, RequestFact>();
  sorted_entries(grouped).forEach(([key, records]): void => {
    const r = records[0]!;
    if (records.some((other: RequestFact): boolean => !equal_value(other, r))) {
      if (records.some((record: RequestFact): boolean => _MONEY_ACTIONS.has(record.actionKind)) || snapshot.moneyEvents.some((e: MoneyEvent): boolean => e.requestId === key)) {
        p.add(`money:request:${key}`, "Contradictory records share a request ID; request states have no timestamp and cannot be ordered.",
          `Authoritative request payload and state for ${key}`, { conflict: true });
      }
      return;
    }
    result.set(key, r);
    if (_MONEY_ACTIONS.has(r.actionKind)) {
      if (!_REQUEST_STATES.has(r.state) || r.amountCents === null) {
        p.add(`money:request:${key}`, "Money request needs a supported state and an explicit amount.", `Money request ${key}`);
      }
      if (r.state === "OUTCOME_UNKNOWN") {
        p.add(`money:request:${key}`, "The external result is unknown; do not infer settlement, failure or permission to retry.", `Reconciled external result for request ${key}`);
      }
    }
  });
  const external_ids = new Map<string, string>();
  sorted_entries(result).forEach(([key, r]): void => {
    if (r.actionKind === "REQUEST_REFUND" && r.externalReference !== null) {
      if (external_ids.has(r.externalReference)) {
        const pair = sorted_text([external_ids.get(r.externalReference)!, key]);
        p.add(`money:duplicate-external-reference:${pair.join(":")}`, "Distinct refund request IDs share an external payment identity, including terminal requests; reconcile aliases before counting settlements.", "Authoritative request-to-external-payment identity", { conflict: true });
      }
      external_ids.set(r.externalReference, key);
    }
  });
  return result;
}

export type _EvidenceChecker = (evidence_id: string, key: string, record: string) => EvidenceInput | null;

export function _evidence_checker(snapshot: CaseSnapshot, clock: string, p: _Problems): _EvidenceChecker {
  const grouped = new Map<string, EvidenceInput[]>();
  snapshot.evidence.forEach((evidence: EvidenceInput): void => {
    if (!grouped.has(evidence.evidenceId)) grouped.set(evidence.evidenceId, []);
    grouped.get(evidence.evidenceId)!.push(evidence);
  });
  return (evidence_id: string, key: string, record: string): EvidenceInput | null => {
    _id(evidence_id, "sourceEvidenceId");
    const records = grouped.get(evidence_id) ?? [];
    if (records.length === 0) {
      p.add(key, `Missing source evidence ${evidence_id}.`, record);
      return null;
    }
    const e = records[0]!;
    if (records.some((other: EvidenceInput): boolean => !equal_value(evidence_payload(other), evidence_payload(e)))) {
      p.add(key, `Contradictory source evidence shares ID ${evidence_id}.`, record, { conflict: true });
      return null;
    }
    const learned = instant(_time(e.learnedAt, `evidence:${evidence_id}.learnedAt`), "learnedAt");
    const occurred = e.occurredAt !== null ? instant(_time(e.occurredAt, `evidence:${evidence_id}.occurredAt`), "occurredAt") : null;
    if (e.associationAccepted !== true || learned > instant(clock, "clock") || (occurred !== null && occurred > learned)) {
      p.add(key, `Source evidence ${evidence_id} must have an accepted association and consistent occurrence/knowledge at or before the review clock.`, record);
    }
    if (e.sourceClass === "MODEL_PROPOSAL" || e.recordKind === "MODEL_PROPOSAL") {
      p.add(key, `Model proposal ${evidence_id} is not verified accounting proof.`, record);
    }
    return e;
  };
}

export function _event_payload(e: MoneyEvent, include_event_id: boolean = true): unknown[] {
  const fields: unknown[] = [
    e.canonicalTransactionId, e.sourceEventId, e.kind, e.status, e.amountCents,
    instant(e.occurredAt, `event:${e.eventId}.occurredAt`).toString(),
    instant(e.learnedAt, `event:${e.eventId}.learnedAt`).toString(),
    e.sourceEvidenceId, e.requestId, e.reversesTransactionId, e.chargeItemId,
  ];
  return include_event_id ? [e.eventId, ...fields] : fields;
}

export function _economic(e: MoneyEvent): unknown[] {
  return [e.kind, e.status, e.amountCents, e.requestId, e.reversesTransactionId, e.chargeItemId];
}

export class _Transaction {
  constructor(
    readonly key: string,
    readonly kind: string,
    readonly events: readonly MoneyEvent[],
    readonly request: string | null,
    readonly target: string | null,
    readonly item: string | null,
    readonly nominal: number,
  ) {}

  /** Holdings, applications, postings, refunds; one canonical effect. */
  at(clock: string): [number, number, number, number] {
    const seen = this.events.filter((e: MoneyEvent): boolean => instant(e.occurredAt, "occurredAt") <= instant(clock, "clock"));
    if (seen.length === 0) return [0, 0, 0, 0];
    if (this.kind === "REFUND") {
      const settled = seen.find((e: MoneyEvent): boolean => e.status === "SETTLED")?.amountCents ?? 0;
      const returned = seen.find((e: MoneyEvent): boolean => e.status === "RETURNED")?.amountCents ?? 0;
      const net = BigInt(settled) - BigInt(returned);
      return [bounded_integer(-net, "transaction holdings"), 0, 0, bounded_integer(net, "transaction refunds")];
    }
    let amount = seen[0]!.amountCents;
    if (seen[seen.length - 1]!.status === "REVERSED") amount = 0;
    const negative = amount === 0 ? 0 : -amount;
    if (this.kind === "DEPOSIT_RECEIPT" || this.kind === "DEPOSIT_TRANSFER_IN") return [amount, 0, 0, 0];
    if (this.kind === "DEPOSIT_TRANSFER_OUT") return [negative, 0, 0, 0];
    if (this.kind === "DEPOSIT_APPLICATION") return [negative, amount, 0, 0];
    if (this.kind === "DEPOSIT_APPLICATION_REVERSAL") return [amount, negative, 0, 0];
    if (this.kind === "CHARGE_POSTING") return [0, 0, amount, 0];
    if (this.kind === "CHARGE_POSTING_REVERSAL") return [0, 0, negative, 0];
    return [amount, 0, 0, negative]; // Separately identified refund return.
  }

  settlement_at(): string | null {
    return this.events.find((e: MoneyEvent): boolean => e.status === "SETTLED")?.occurredAt ?? null;
  }

  returned(): number {
    return this.events.find((e: MoneyEvent): boolean => e.status === "RETURNED" || e.status === "REVERSED")?.amountCents ?? 0;
  }
}

export function _transactions(
  snapshot: CaseSnapshot, requests: ReadonlyMap<string, RequestFact>, clock: string,
  p: _Problems, check_evidence: _EvidenceChecker,
): Map<string, _Transaction> {
  const by_event = new Map<string, MoneyEvent>();
  const by_source = new Map<string, MoneyEvent>();
  snapshot.moneyEvents.forEach((e: MoneyEvent): void => {
    (["eventId", "canonicalTransactionId", "sourceEventId"] as const).forEach((name): void => {
      _id(e[name], `moneyEvent.${name}`);
    });
    _bounded(e.amountCents, `event:${e.eventId}.amountCents`, true);
    const occurred = instant(_time(e.occurredAt, `event:${e.eventId}.occurredAt`), "occurredAt");
    const learned = instant(_time(e.learnedAt, `event:${e.eventId}.learnedAt`), "learnedAt");
    const key = `money:event:${e.eventId}`;
    const record = `Source accounting event ${e.eventId} and its canonical/source aliases`;
    const proof = check_evidence(e.sourceEvidenceId, key, record);
    if (proof !== null && !(occurred <= instant(proof.learnedAt, "learnedAt") && instant(proof.learnedAt, "learnedAt") <= learned)) {
      p.add(key, "Source accounting proof must exist after occurrence and no later than the claimed event knowledge time.", record);
    }
    if (occurred > learned || learned > instant(clock, "clock")) {
      p.add(key, "Event occurrence must not follow its learned time, and neither may follow the review clock.", record);
    }
    if (!_KIND_STATUS.get(e.kind)?.has(e.status)) {
      p.add(key, "Unsupported event kind/status combination (including unspecified corrections) needs explicit reconciliation.", record);
    }
    if (by_event.has(e.eventId) && !equal_value(_event_payload(by_event.get(e.eventId)!), _event_payload(e))) {
      p.add(key, "Contradictory payloads share an event ID.", record, { conflict: true });
    }
    by_event.set(e.eventId, e);
    if (by_source.has(e.sourceEventId) && !equal_value(_event_payload(by_source.get(e.sourceEventId)!, false), _event_payload(e, false))) {
      p.add(`money:source-event:${e.sourceEventId}`, "Contradictory payloads share a source event ID.", `Source accounting event ${e.sourceEventId}`, { conflict: true });
    }
    by_source.set(e.sourceEventId, e);
    if (e.chargeItemId !== null && !snapshot.charges.some((c: ChargeInput): boolean => c.itemId === e.chargeItemId)) {
      p.add(key, "Event references an absent charge item.", record);
    }
    if (e.requestId !== null) {
      const r = requests.get(e.requestId);
      const expected_action = _REFUND_KINDS.has(e.kind) ? "REQUEST_REFUND" : "REQUEST_LEDGER_POSTING";
      if (r === undefined || r.actionKind !== expected_action) {
        p.add(key, "Event request reference is absent, contradictory or belongs to a different action kind.", record);
      }
    }
    if (_REFUND_KINDS.has(e.kind) && e.chargeItemId !== null) {
      p.add(key, "Refunds cannot silently double as a charge-item application.", record, { conflict: true });
    }
  });
  if (p.ledger_bad) return new Map(); // Conflicting aliases never select an input row.
  const grouped = new Map<string, MoneyEvent[]>();
  by_source.forEach((e: MoneyEvent): void => {
    if (!grouped.has(e.canonicalTransactionId)) grouped.set(e.canonicalTransactionId, []);
    grouped.get(e.canonicalTransactionId)!.push(e);
  });
  const result = new Map<string, _Transaction>();
  sorted_entries(grouped).forEach(([txid, rows]): void => {
    const key = `money:transaction:${txid}`;
    const record = `Canonical transaction lifecycle ${txid}`;
    const ordered = [...rows].sort((a: MoneyEvent, b: MoneyEvent): number => {
      const difference = instant(a.occurredAt, "occurredAt") - instant(b.occurredAt, "occurredAt");
      return difference < 0n ? -1 : difference > 0n ? 1 : compare_text(a.eventId, b.eventId);
    });
    const first = ordered[0]!;
    const kinds = new Set(ordered.map((e: MoneyEvent): string => e.kind));
    const independent_return = kinds.size === 1 && kinds.has("REFUND_RETURNED") && first.reversesTransactionId !== null && first.reversesTransactionId !== txid;
    const family = independent_return ? "REFUND_RETURN" : [...kinds].every((kind: string): boolean => _REFUND_KINDS.has(kind)) ? "REFUND" : first.kind;
    if ((family !== "REFUND" && family !== "REFUND_RETURN" && kinds.size !== 1)
      || ordered.some((e: MoneyEvent): boolean => e.requestId !== first.requestId || e.chargeItemId !== first.chargeItemId)) {
      p.add(key, "Canonical identity changes family, request or charge association across lifecycle events.", record, { conflict: true });
      return;
    }
    const allowed_target = first.reversesTransactionId;
    if (family === "REFUND") {
      if (ordered.some((e: MoneyEvent): boolean => e.reversesTransactionId !== null && !(e.status === "RETURNED" && e.reversesTransactionId === txid))) {
        p.add(key, "An in-transaction return may reference only its own canonical transaction.", record, { conflict: true });
      }
    } else if (ordered.some((e: MoneyEvent): boolean => e.reversesTransactionId !== allowed_target)) {
      p.add(key, "Reversal target changes across the canonical transaction.", record, { conflict: true });
    }
    const is_reversal = ["REFUND_RETURN", "DEPOSIT_APPLICATION_REVERSAL", "CHARGE_POSTING_REVERSAL"].includes(family);
    if (is_reversal !== (allowed_target !== null) && family !== "REFUND") {
      p.add(key, "Only an explicit reversal/return may carry a reversal target, and it must have one.", record);
    }
    const seen_states = new Map<string, MoneyEvent>();
    const by_time = new Map<bigint, unknown[]>();
    const sequence: MoneyEvent[] = [];
    ordered.forEach((e: MoneyEvent): void => {
      const economic = _economic(e);
      const at = instant(e.occurredAt, "occurredAt");
      if (by_time.has(at) && !equal_value(by_time.get(at), economic)) {
        p.add(key, "Conflicting lifecycle states or amounts have the same event time; input order is not authority.", record, { conflict: true });
      }
      by_time.set(at, economic);
      if (seen_states.has(e.status)) {
        if (!equal_value(_economic(seen_states.get(e.status)!), economic)) {
          p.add(key, "A repeated lifecycle state changes its amount or references; cumulative versus incremental effect is ambiguous.", record, { conflict: true });
        }
        if (sequence.length > 0 && sequence[sequence.length - 1]!.status !== e.status) {
          p.add(key, "A lifecycle regresses to an earlier state; a replacement needs its own reconciled identity.", record, { conflict: true });
        }
      } else {
        sequence.push(e);
        seen_states.set(e.status, e);
      }
    });
    const statuses = sequence.map((e: MoneyEvent): string => e.status).join(",");
    let nominal: number;
    if (family === "REFUND") {
      if (!["PENDING", "SETTLED", "FAILED", "PENDING,SETTLED", "PENDING,FAILED", "SETTLED,RETURNED", "PENDING,SETTLED,RETURNED"].includes(statuses)) {
        p.add(key, "Refund lifecycle is orphaned or unsupported; a return requires prior settlement and a failed/returned payment cannot be reused.", record);
      }
      nominal = sequence.find((e: MoneyEvent): boolean => e.status !== "RETURNED")?.amountCents ?? first.amountCents;
      if (sequence.some((e: MoneyEvent): boolean => e.status !== "RETURNED" && e.amountCents !== nominal)
        || sequence.some((e: MoneyEvent): boolean => e.status === "RETURNED" && e.amountCents > nominal)) {
        p.add(key, "Refund lifecycle amounts disagree or the return exceeds its settled principal.", record, { conflict: true });
      }
    } else {
      nominal = first.amountCents;
      let allowed = new Set(["SETTLED"]);
      if (family === "DEPOSIT_APPLICATION" || family === "CHARGE_POSTING") allowed.add("SETTLED,REVERSED");
      if (family === "REFUND_RETURN") allowed = new Set(["RETURNED"]);
      if (!allowed.has(statuses) || sequence.some((e: MoneyEvent): boolean => e.amountCents !== nominal)) {
        p.add(key, "Orphan reversal, unsupported lifecycle or inconsistent transaction amount.", record, { conflict: true });
      }
    }
    if (first.requestId !== null) {
      const r = requests.get(first.requestId)!;
      if (!is_reversal && r.amountCents !== nominal) {
        p.add(key, "Payment/posting principal disagrees with the referenced request amount; partial execution needs reconciliation.", record, { conflict: true });
      }
    }
    result.set(txid, new _Transaction(txid, family, sequence, first.requestId, is_reversal ? allowed_target : null, first.chargeItemId, nominal));
  });
  const reversed_amounts = new Map<string, number[]>();
  result.forEach((t: _Transaction): void => {
    if (t.target === null) return;
    const target = result.get(t.target);
    const expected = new Map([
      ["REFUND_RETURN", "REFUND"],
      ["DEPOSIT_APPLICATION_REVERSAL", "DEPOSIT_APPLICATION"],
      ["CHARGE_POSTING_REVERSAL", "CHARGE_POSTING"],
    ]).get(t.kind);
    const key = `money:transaction:${t.key}`;
    const record = `Original settlement and explicit reversal ${t.key} -> ${t.target}`;
    if (target === undefined || target.kind !== expected || t.target === t.key) {
      p.add(key, "Reversal target is missing, incompatible, itself a reversal, or self-referential.", record);
      return;
    }
    const settled_at = target.settlement_at();
    if (settled_at === null || instant(settled_at, "settlement_at") >= instant(t.events[0]!.occurredAt, "occurredAt")
      || target.request !== t.request || target.item !== t.item) {
      p.add(key, "Reversal must follow the original settlement and preserve its request/charge identity.", record, { conflict: true });
    }
    if (!reversed_amounts.has(t.target)) reversed_amounts.set(t.target, []);
    reversed_amounts.get(t.target)!.push(t.nominal);
  });
  reversed_amounts.forEach((amounts: number[], key: string): void => {
    const target = result.get(key)!;
    if (target.returned() !== 0) {
      p.add(`money:transaction:${key}`, "Both an in-transaction return/reversal and separate reversing transactions claim the same principal.", `Unambiguous reversal identity for ${key}`, { conflict: true });
    }
    if (bounded_integer(sum_money(amounts), `reversal total:${key}`, true) > target.nominal) {
      p.add(`money:transaction:${key}`, "Total reversals exceed the original settled principal.", `Reconciled reversal total for ${key}`, { conflict: true });
    }
  });
  return result;
}

export function _holdings(
  snapshot: CaseSnapshot, txs: ReadonlyMap<string, _Transaction>, clock: string,
  p: _Problems, check_evidence: _EvidenceChecker,
): [number | null, number, number, number] {
  const b = snapshot.depositBalance;
  const key = "money:balance-basis";
  const record = `Verified balance ${b.balanceId}, as-of time and canonical included-transaction list`;
  _id(b.balanceId, "depositBalance.balanceId");
  _amount(b.amountCents, "depositBalance.amountCents");
  _time(b.asOf, "depositBalance.asOf");
  const proof = check_evidence(b.sourceEvidenceId, key, record);
  if (proof !== null && instant(b.asOf, "asOf") > instant(proof.learnedAt, "learnedAt")) {
    p.add(key, "The balance as-of time cannot postdate the knowledge time of its supporting accounting record.", record);
  }
  if (b.amountCents === null || instant(b.asOf, "asOf") > instant(clock, "clock") || b.basis !== "SNAPSHOT_WITH_EXPLICIT_INCLUDED_TRANSACTIONS" || b.reconciliationState !== "RECONCILED") {
    p.add(key, "The recorded amount, as-of time and explicit inclusion basis must be verified and reconciled.", record, { conflict: b.reconciliationState === "CONFLICT" });
  }
  const included = new Set<string>();
  b.includedTransactionIds.forEach((txid: string): void => {
    _id(txid, "depositBalance.includedTransactionIds");
    if (included.has(txid)) p.add(key, "The included-transaction list repeats a canonical ID.", record, { conflict: true });
    included.add(txid);
  });
  if (p.ledger_bad) return [null, 0, 0, 0];
  sorted_text(included).forEach((txid: string): void => {
    const t = txs.get(txid);
    if (t === undefined || !t.events.some((e: MoneyEvent): boolean => instant(e.occurredAt, "occurredAt") <= instant(b.asOf, "asOf") && EFFECT_STATES.has(e.status))) {
      p.add(key, `Included canonical transaction ${txid} has no established accounting effect by the snapshot time.`, record);
    }
  });
  sorted_entries(txs).forEach(([txid, t]): void => {
    const cash_history = t.kind !== "CHARGE_POSTING" && t.kind !== "CHARGE_POSTING_REVERSAL" && t.events.some((e: MoneyEvent): boolean => instant(e.occurredAt, "occurredAt") <= instant(b.asOf, "asOf") && EFFECT_STATES.has(e.status));
    if (cash_history && !included.has(txid)) p.add(key, `Pre-snapshot cash transaction ${txid} is absent from the explicit inclusion list.`, record);
  });
  if (p.ledger_bad) return [null, 0, 0, 0];
  const now = [...txs.values()].map((t: _Transaction): [number, number, number, number] => t.at(clock));
  const reflected = sorted_text(included).map((k: string): number => txs.get(k)!.at(b.asOf)[0]);
  const holdings = bounded_integer(BigInt(b.amountCents!) + sum_money(now.map((e): number => e[0])) - sum_money(reflected), "actual current holdings");
  const apps = bounded_integer(sum_money(now.map((e): number => e[1])), "existingDepositApplicationsCents");
  const postings = bounded_integer(sum_money(now.map((e): number => e[2])), "existingNetPostingCents");
  const refunds = bounded_integer(sum_money(now.map((e): number => e[3])), "priorNetRefundsCents");
  // A later receipt/return cannot conceal an earlier post-snapshot overdraft.
  const movements = new Map<bigint, bigint[]>();
  txs.forEach((t: _Transaction): void => {
    let previous = BigInt(t.at(b.asOf)[0]);
    t.events.forEach((event: MoneyEvent): void => {
      const at = instant(event.occurredAt, "occurredAt");
      if (at > instant(b.asOf, "asOf")) {
        const current = BigInt(t.at(event.occurredAt)[0]);
        if (!movements.has(at)) movements.set(at, []);
        movements.get(at)!.push(current - previous);
        previous = current;
      }
    });
  });
  let running = BigInt(b.amountCents!);
  let negative_history = false;
  [...movements.keys()].sort((a: bigint, c: bigint): number => a < c ? -1 : a > c ? 1 : 0).forEach((at: bigint): void => {
    running = BigInt(bounded_integer(running + sum_money(movements.get(at)!), "post-snapshot holdings"));
    negative_history ||= running < 0n;
  });
  if (Math.min(holdings, apps, postings, refunds) < 0 || negative_history) {
    p.add("money:negative-funds", "Current/historical post-snapshot holdings or a net application/posting/refund is negative; do not manufacture a refund or write-off.", "Custodian balance and complete original/reversal ledger", { conflict: true });
    return [null, apps, postings, refunds];
  }
  return [holdings, apps, postings, refunds];
}

export function _reservations(requests: ReadonlyMap<string, RequestFact>, txs: ReadonlyMap<string, _Transaction>, p: _Problems): number {
  if (p.ledger_bad) return 0;
  const refunds = [...txs.values()].filter((t: _Transaction): boolean => t.kind === "REFUND");
  const reservations: number[] = [];
  const active_keys = new Map<string, string>();
  const external_keys = new Map<string, string>();
  sorted_entries(requests).forEach(([key, r]): void => {
    if (r.actionKind !== "REQUEST_REFUND") return;
    const linked = refunds.filter((t: _Transaction): boolean => t.request === key);
    if (linked.length > 1) {
      p.add(`money:request:${key}`, "Distinct payment identities claim the same refund request; reconcile attempts instead of adding or choosing one.", `Request-to-payment identity for ${key}`, { conflict: true });
      return;
    }
    const t = linked[0];
    const state = t === undefined ? null : t.events[t.events.length - 1]!.status;
    const settled = t !== undefined && t.settlement_at() !== null;
    if (r.state === "SUCCEEDED" && !settled) {
      p.add(`money:request:${key}`, "A succeeded request is not settlement proof; supply a verified matching money event.", `Settlement evidence for request ${key}`);
    }
    if ((r.state === "FAILED" || r.state === "CANCELLED" || r.state === "SUPERSEDED") && state !== null && state !== "FAILED") {
      p.add(`money:request:${key}`, "Terminal request state contradicts a pending or settled payment.", `Reconciled terminal result for request ${key}`, { conflict: true });
    }
    const active = !settled && state !== "FAILED" && _ACTIVE_REQUESTS.has(r.state);
    if (active) {
      const payload = JSON.stringify([r.targetVersionId, r.payloadFingerprint]);
      if (active_keys.has(payload)) {
        const pair = sorted_text([active_keys.get(payload)!, key]);
        p.add(`money:duplicate-active-requests:${pair.join(":")}`, "Distinct active request IDs claim the same target and payload; do not reserve or execute both.", "Authoritative idempotency and refund request records", { conflict: true });
      }
      active_keys.set(payload, key);
      if (r.externalReference !== null) {
        if (external_keys.has(r.externalReference)) {
          const pair = sorted_text([external_keys.get(r.externalReference)!, key]);
          p.add(`money:duplicate-external-reference:${pair.join(":")}`, "Distinct active refund requests share an external payment reference.", "Authoritative external payment identity", { conflict: true });
        }
        external_keys.set(r.externalReference, key);
      }
      if (r.amountCents !== null) reservations.push(r.amountCents);
    }
  });
  refunds.forEach((t: _Transaction): void => {
    if (t.request === null && t.events[t.events.length - 1]!.status === "PENDING") reservations.push(t.nominal);
  });
  return bounded_integer(sum_money(reservations), "pendingReservedRefundCents", true);
}

/**
 * Review immutable inputs at the supplied explicit clock.
 * @param snapshot - Case accounting facts; nullable unknowns are not zero.
 * @param decisions - Charge-classification boundary, one consistent decision per charge.
 * @param scope_supported - Accepted scope determination, never inferred here.
 * @param review_clock - Timezone-aware review timestamp, never an implicit wall clock.
 * @returns Account and Accountant questions. finalRefundCents includes reservations,
 * which reduce unreserved funds, not liability. This is not approval/execution authority.
 */
export function review_money(snapshot: CaseSnapshot, decisions: readonly ItemDecision[], scope_supported: boolean, review_clock: string): MoneyReview {
  const clock = _time(review_clock, "review_clock");
  if (typeof scope_supported !== "boolean") throw new ContractError("scope_supported: expected boolean");
  const p = new _Problems();
  const [known, unresolved] = _chosen(snapshot, decisions, p);
  const requests = _requests(snapshot, p);
  const checker = _evidence_checker(snapshot, clock, p);
  const txs = _transactions(snapshot, requests, clock, p, checker);
  const [holdings, apps, postings, refunds] = _holdings(snapshot, txs, clock, p, checker);
  const has_return = !p.ledger_bad && [...txs.values()].some((t: _Transaction): boolean => t.returned() > 0 && (t.kind === "REFUND" || t.kind === "REFUND_RETURN"));
  const reserved = _reservations(requests, txs, p);
  const unknown = snapshot.priorRequests.some((r: RequestFact): boolean => _MONEY_ACTIONS.has(r.actionKind) && r.state === "OUTCOME_UNKNOWN")
    || snapshot.moneyEvents.some((e: MoneyEvent): boolean => e.status === "UNKNOWN");
  snapshot.otherBalances.forEach((other): void => {
    _id(other.balanceId, "otherBalance.balanceId");
    _amount(other.amountCents, `otherBalance:${other.balanceId}.amountCents`);
  });
  if (snapshot.currency !== "USD") {
    p.add("money:currency", "This account contract supports USD only; do not mix or convert currencies.", "Single-currency USD deposit ledger");
  }
  const total = unresolved.length === 0 ? known : null;
  let posting_delta = total !== null && !p.ledger_bad ? bounded_integer(BigInt(total) - BigInt(postings), "postingDeltaCents") : null;
  let application_delta: number | null = null;
  let excess: number | null = null;
  let final_refund: number | null = null;
  if (holdings !== null && !p.ledger_bad) {
    const gross = bounded_integer(sum_money([holdings, apps, refunds]), "gross deposit basis", true);
    if (total !== null) {
      const deductible = BigInt(Math.min(total, gross));
      application_delta = bounded_integer(deductible - BigInt(apps), "depositApplicationDeltaCents");
      const beyond_deposit = BigInt(total) - BigInt(gross);
      excess = bounded_integer(beyond_deposit > 0n ? beyond_deposit : 0n, "proposedExcessReceivableCents", true);
      const remaining = bounded_integer(BigInt(gross) - deductible - BigInt(refunds), "remaining refund");
      if (remaining < 0 || reserved > remaining) {
        p.add("money:overpayment", "Settled refunds or pending reservations exceed the reconciled entitlement; resolve overpayment, competing requests or changed deductions explicitly.", "Reconciled deposit entitlement, payments and live refund requests", { conflict: true });
      } else {
        final_refund = remaining;
      }
    }
  }
  if (!scope_supported) p.add("money:scope", "Scope is unsupported or unresolved; arithmetic preparation is not a final deposit account.", "Accepted supported scope determination", { ledger: false });
  const ready = total !== null && p.entries.size === 0 && scope_supported;
  if (!ready) final_refund = null;
  if (p.ledger_bad) {
    posting_delta = null;
    application_delta = null;
    excess = null;
  }
  const questions = p.questions();
  const account: AccountResult = {
    currency: "USD", recordedDepositCents: holdings,
    balanceSourceEvidenceId: snapshot.depositBalance.sourceEvidenceId, balanceAsOf: snapshot.depositBalance.asOf,
    reconciliationState: p.conflict ? "CONFLICT" : p.ledger_bad ? "UNRECONCILED" : "RECONCILED",
    knownChosenDeductionsCents: known, totalDeductionsCents: total,
    existingNetPostingCents: p.ledger_bad ? null : postings, postingDeltaCents: posting_delta,
    existingDepositApplicationsCents: p.ledger_bad ? null : apps, depositApplicationDeltaCents: application_delta,
    priorNetRefundsCents: p.ledger_bad ? null : refunds, pendingReservedRefundCents: p.ledger_bad ? null : reserved,
    finalRefundCents: final_refund, proposedExcessReceivableCents: excess,
    unresolvedItemIds: unresolved, otherBalanceIds: sorted_text(new Set(snapshot.otherBalances.map((o): string => o.balanceId))),
    finalAccountReady: ready, notFinalReasons: questions.map((q: OpenQuestion): string => q.reason),
    recipientInstructionsVersion: snapshot.recipients.versionId, recipientState: snapshot.recipients.state,
  };
  const work = posting_delta !== 0 || application_delta !== 0;
  let state: string;
  let reason: string;
  if (!ready) {
    state = "BLOCKED";
    reason = "Resolve the named questions; there is no final refund authorization or assumed withholding policy.";
  } else if (reserved > 0) {
    state = "PENDING";
    reason = "Verified pending requests/initiation reserve part or all of the unpaid refund; reservation is not settlement.";
  } else if (has_return && final_refund! > 0) {
    state = "REOPENED";
    reason = "A verified returned refund leaves unpaid liability; prior request completion is not continuing performance.";
  } else if (final_refund! > 0 || work) {
    state = "READY";
    reason = "Confirmed refund or ledger work remains unpaid/unperformed; preparation does not imply execution or approval.";
  } else if (refunds > 0) {
    state = "FULFILLED";
    reason = "Verified net settlements satisfy the refund with no outstanding refund or ledger delta; legal performance is separate.";
  } else {
    state = "NOT_APPLICABLE";
    reason = "No refund liability or remaining deposit ledger work is established.";
  }
  return { account, questions, moneyState: state, moneyReason: reason, hasUnknownResult: unknown, hasReturn: has_return };
}
