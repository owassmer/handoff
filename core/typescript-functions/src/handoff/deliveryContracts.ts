import type { Integer, Long, TimestampISOString } from "@osdk/functions";
import { details, entries, requireHandoff, wordList, words } from "./values.js";

export interface SourceRecord { sourceSystem: string; sourceRecordId: string; sourceDocumentId: string }
/** Gross quoted amounts, already expressed in the currency's minor units. No floating-point prices. */
export interface QuoteLine { lineId: string; description: string; amountCents: Long }
export interface QuoteOffer extends SourceRecord {
  title: string; providerPartyId: string; kind: string; currency: string; lines: QuoteLine[];
  totalCents: Long; depositCents: Long; paymentTerms: string; requirements: string[];
  availableFrom: TimestampISOString; validUntil: TimestampISOString;
  durationMinutes: Integer; responseMinutes: Integer;
}
export interface ScopeLine extends QuoteLine { acceptedScope: string }
export interface WorkMandate {
  decisionId: string; workPlanId: string; revision: Long; propertyId: string; currency: string;
  budgetCents: Long; scope: string[]; requirements: string[]; sourceDocumentIds: string[];
  /** Set only for a genuinely fixed provider choice, not the plan's ordinary suggestion. */
  fixedProviderPartyId?: string;
  reviewedSelections?: Array<{ quoteId: string; quoteLineId: string; scope: string; reason: string }>;
  quoteId?: string;
}
export interface CommissionInput {
  workPlanId: string; expectedRevision: Long; quoteId: string; fundingId: string;
  scope: { quoteLineId: string; acceptedScope: string }[]; obligationId?: string;
}
export interface ExistingJob extends SourceRecord {
  title: string; providerPartyId: string; kind: string; currency: string; scope: QuoteLine[];
  committedCents?: Long; status: "Underway" | "Awaiting check" | "Complete";
  startedAt: TimestampISOString; summary: string;
}
export interface Finding {
  lineId: string; result: "Satisfied" | "Deficient" | "Not checked";
  observation: string; method: string;
}
export interface InspectionReport extends SourceRecord {
  title: string; observerPartyId: string; jobId?: string;
  observedAt: TimestampISOString; purpose: "Condition report" | "Completion check"; findings: Finding[];
}
export interface SupplierInvoice extends SourceRecord {
  title: string; jobId: string; providerPartyId: string; payerPartyId: string;
  currency: string; lines: QuoteLine[]; totalCents: Long;
  issuedAt: TimestampISOString; dueAt: TimestampISOString; paymentTerms: string;
}
export interface OwnerAllocation extends SourceRecord {
  title: string; ownerPartyId: string; currency: string; confirmedCents: Long; confirmedAt: TimestampISOString;
}
export interface ProviderRequest {
  purpose: "Quote" | "Appointment" | "Progress" | "Invoice";
  providerPartyId: string; quoteId: string; scopeLineIds: string[]; jobId?: string;
  /** A material reply can prompt a new follow-up; an empty retry cannot create another request. */
  previousReplyId?: string;
}
export interface ProviderReply {
  outcome: "Offer" | "Alternative" | "Unavailable" | "Appointment" | "Advance required" | "Waiting"
    | "Partial" | "Deficiency" | "Reported complete" | "Invoice";
  summary: string; quoteIds: string[]; inspectionIds: string[]; invoiceIds: string[];
  appointmentAt?: TimestampISOString;
  /** Job requirements the provider confirmed in this reply, beyond those stated in its offer. */
  confirmedRequirements?: string[];
}
export interface PaymentObservation {
  instructionKey: string; sourceReference: string; amountCents: Long; currency: string;
  status: "Confirming" | "Settled" | "Failed" | "Returned"; observedAt: TimestampISOString;
  /** Only the adapter can establish a definitive result. A missing lookup is not definitive failure. */
  definitive: boolean;
}

export function money(value: unknown, label = "Amount"): Long {
  requireHandoff(typeof value === "string" && /^(0|[1-9][0-9]{0,18})$/.test(value)
    && BigInt(value) <= 9223372036854775807n, `${label} must be a nonnegative amount in whole minor units.`);
  return value;
}
/** Exact display of a whole minor-unit amount, for example "$37,912.49". No floating point. */
export function formatAmount(cents: unknown, currency: string): string {
  const value = BigInt(money(cents));
  const whole = (value / 100n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  const amount = `${whole}.${(value % 100n).toString().padStart(2, "0")}`;
  return currency === "USD" ? `$${amount}` : `${currency} ${amount}`;
}
export function currencyCode(value: unknown): string {
  const result = words(value, "Currency", 3);
  requireHandoff(/^[A-Z]{3}$/.test(result), "Use the stated three-letter currency code.");
  return result;
}
export function instant(value: unknown, label = "Time"): TimestampISOString {
  const result = words(value, label, 24);
  // The SDK omits trailing fractional zeroes (for example .030Z becomes .03Z).
  const normalized = result.replace(/(?:\.(\d{1,3}))?Z$/, (_match: string, fraction?: string) => `.${(fraction ?? "").padEnd(3, "0")}Z`);
  requireHandoff(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/.test(result)
    && Number.isFinite(Date.parse(result))
    && new Date(result).toISOString() === normalized,
  `${label} must be a valid UTC timestamp.`);
  return normalized;
}
export function minutes(value: unknown, label: string): Integer {
  requireHandoff(typeof value === "number" && Number.isSafeInteger(value) && value > 0 && value <= 525600,
    `${label} must be a positive number of minutes within one year.`);
  return value;
}
export function afterMinutes(at: TimestampISOString, duration: Integer): TimestampISOString {
  return new Date(Date.parse(instant(at)) + minutes(duration, "Reply interval") * 60000).toISOString();
}
export function sourceRecord(value: Record<string, unknown>): SourceRecord {
  return { sourceSystem: words(value.sourceSystem, "Source system", 160),
    sourceRecordId: words(value.sourceRecordId, "Source reference", 200),
    sourceDocumentId: words(value.sourceDocumentId, "Supporting document", 160) };
}
export function quoteLines(value: unknown): QuoteLine[] {
  const result = entries(value, "Price lines", 48, 1).map((entry): QuoteLine => {
    const line = details(entry, ["lineId", "description", "amountCents"], [], "Price line");
    return { lineId: words(line.lineId, "Line reference", 160), description: words(line.description, "Work description", 1000), amountCents: money(line.amountCents) };
  });
  requireHandoff(new Set(result.map((line) => line.lineId)).size === result.length, "Price lines repeat a reference.");
  return result;
}
export function scopeLines(value: unknown): ScopeLine[] {
  return entries(value, "Job scope", 48, 1).map((entry): ScopeLine => {
    const line = details(entry, ["lineId", "description", "amountCents", "acceptedScope"], [], "Job scope line");
    return { ...quoteLines([{ lineId: line.lineId, description: line.description, amountCents: line.amountCents }])[0]!,
      acceptedScope: words(line.acceptedScope, "Accepted scope", 50000) };
  });
}
export function findings(value: unknown): Finding[] {
  const result = entries(value, "Findings", 48, 1).map((entry): Finding => {
    const row = details(entry, ["lineId", "result", "observation", "method"], [], "Finding");
    requireHandoff(row.result === "Satisfied" || row.result === "Deficient" || row.result === "Not checked", "Choose the actual finding.");
    return { lineId: words(row.lineId, "Observed scope reference", 160), result: row.result,
      observation: words(row.observation, "Observation", 50000), method: words(row.method, "How this was checked", 48000) };
  });
  requireHandoff(new Set(result.map((row) => row.lineId)).size === result.length, "A report repeats an observed scope line.");
  return result;
}
export function providerRequest(value: unknown): ProviderRequest {
  const row = details(value, ["purpose", "providerPartyId", "quoteId", "scopeLineIds"], ["jobId", "previousReplyId"], "Provider request");
  requireHandoff(row.purpose === "Quote" || row.purpose === "Appointment" || row.purpose === "Progress" || row.purpose === "Invoice", "Choose a supported provider request.");
  return { purpose: row.purpose, providerPartyId: words(row.providerPartyId, "Provider", 160),
    quoteId: words(row.quoteId, "Quote", 160), scopeLineIds: wordList(row.scopeLineIds, "Requested lines", 48, 1),
    ...(row.jobId === undefined ? {} : { jobId: words(row.jobId, "Job", 160) }),
    ...(row.previousReplyId === undefined ? {} : { previousReplyId: words(row.previousReplyId, "Earlier reply", 160) }) };
}
