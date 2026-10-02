import { sourceDetails } from "./sourceAccess.js";
import type { Osdk } from "@osdk/client";
import { HandoffDocument } from "@ontology/sdk";
import { details, entries, parseDetails, requireHandoff, wordList, words } from "./values.js";
import { currencyCode, instant, minutes, money, quoteLines, type QuoteLine } from "./deliveryContracts.js";

/** Provider's bounded service/availability information. It is not an executable model instruction. */
export interface ProviderService {
  serviceId: string; title: string; kind: "Assessment" | "Repair" | "Cleaning" | "Verification";
  currency: string; lines: QuoteLine[]; depositCents: string; paymentTerms: string; requirements: string[];
  availableFrom: string; validUntil: string; durationMinutes: number; responseMinutes: number;
  invoiceDueMinutes?: number;
  effects: Array<{ lineId: string; conditionIds: string[]; method: string; deliverables?: AssessmentDeliverable[] }>;
}
/** Configured report evidence, not an assertion that an entire prose scope is complete. */
export interface AssessmentDeliverable {
  acceptedScope: string; observation: string; method: string; sourceDocumentIds: string[]; conditionIds: string[];
}
export interface PropertyCondition {
  conditionId: string; description: string; state: "Satisfied" | "Deficient" | "Not checked";
  repairable: boolean; accessible: boolean;
}
export interface FundingInformation {
  ownerPartyId: string; currency: string; confirmedCents: string; confirmedAt: string;
  paymentBehavior: "Settle" | "Reject" | "Uncertain"; responseMinutes: number;
}
export type SourceDocument = { documentId: string } & Partial<Pick<Osdk.Instance<HandoffDocument>, "title" | "text" | "kind" | "partyId" | "detailsJson" | "sourceVersion" | "availableFrom">>;
export function providerServices(doc: SourceDocument): ProviderService[] {
  requireHandoff(doc.kind === "Provider information" && doc.partyId, "The provider information needs its sender.");
  const body = details(sourceDetails(words(doc.detailsJson, "Provider information", 140000)), ["services"], [], "Provider information");
  const result = entries(body.services, "Services", 16, 1).map((item): ProviderService => {
    const row = details(item, ["serviceId", "title", "kind", "currency", "lines", "depositCents", "paymentTerms", "requirements", "availableFrom", "validUntil", "durationMinutes", "responseMinutes", "effects"], ["invoiceDueMinutes"], "Provider service");
    requireHandoff(row.kind === "Assessment" || row.kind === "Repair" || row.kind === "Cleaning" || row.kind === "Verification", "The service needs a supported purpose.");
    const lines = quoteLines(row.lines), depositCents = money(row.depositCents);
    requireHandoff(BigInt(depositCents) <= lines.reduce((sum, line) => sum + BigInt(line.amountCents), 0n), "The advance exceeds the service price.");
    const effects = entries(row.effects, "Service checks", 48, 1).map((value) => {
      const effect = details(value, ["lineId", "conditionIds", "method"], ["deliverables"], "Service check");
      const deliverables = effect.deliverables === undefined ? undefined : entries(effect.deliverables, "Assessment deliverables", 48, 1).map((entry): AssessmentDeliverable => {
        const report = details(entry, ["acceptedScope", "observation", "method", "sourceDocumentIds", "conditionIds"], [], "Assessment deliverable");
        return { acceptedScope: words(report.acceptedScope, "Accepted scope", 1000), observation: words(report.observation, "Report observation", 3000),
          method: words(report.method, "Report method", 1000), sourceDocumentIds: wordList(report.sourceDocumentIds, "Report evidence", 16, 1),
          conditionIds: wordList(report.conditionIds, "Observed conditions", 48, 0) };
      });
      requireHandoff(!deliverables || new Set(deliverables.map((item) => item.acceptedScope)).size === deliverables.length,
        "Do not repeat a deliverable in a service line's report.");
      return { lineId: words(effect.lineId, "Service line", 160), conditionIds: wordList(effect.conditionIds, "Conditions", 48, 1), method: words(effect.method, "Check method", 1000),
        ...(deliverables ? { deliverables } : {}) };
    });
    requireHandoff(lines.every((line) => effects.some((effect) => effect.lineId === line.lineId))
      && effects.every((effect) => lines.some((line) => line.lineId === effect.lineId))
      && new Set(effects.map((effect) => effect.lineId)).size === effects.length, "Each service line needs one described physical effect or check.");
    requireHandoff(instant(row.availableFrom) <= instant(row.validUntil), "The provider availability starts after this offer expires.");
    return { serviceId: words(row.serviceId, "Service reference", 160), title: words(row.title, "Service title", 200), kind: row.kind,
      currency: currencyCode(row.currency), lines, depositCents, paymentTerms: words(row.paymentTerms, "Payment terms", 3000),
      requirements: wordList(row.requirements, "Confirmed requirements", 32, 0, 1000), availableFrom: instant(row.availableFrom),
      validUntil: instant(row.validUntil), durationMinutes: minutes(row.durationMinutes, "Duration"), responseMinutes: minutes(row.responseMinutes, "Reply time"), effects,
      ...(row.invoiceDueMinutes === undefined ? {} : { invoiceDueMinutes: minutes(row.invoiceDueMinutes, "Invoice payment period") }) };
  });
  requireHandoff(new Set(result.map((service) => service.serviceId)).size === result.length, "Provider services repeat a reference.");
  return result;
}
export function propertyConditions(doc: SourceDocument): PropertyCondition[] {
  requireHandoff(doc.kind === "Property condition", "Use property condition information.");
  const body = details(sourceDetails(words(doc.detailsJson, "Condition information", 140000)), ["conditions"], ["jobId", "priorDocumentId", "coverage"], "Condition information");
  const result = entries(body.conditions, "Conditions", 48, 1).map((value): PropertyCondition => {
    const row = details(value, ["conditionId", "description", "state", "repairable", "accessible"], [], "Condition");
    requireHandoff(row.state === "Satisfied" || row.state === "Deficient" || row.state === "Not checked", "Identify the observed condition.");
    requireHandoff(typeof row.repairable === "boolean" && typeof row.accessible === "boolean", "State the known access and repair limits.");
    return { conditionId: words(row.conditionId, "Condition reference", 160), description: words(row.description, "Condition", 2000),
      state: row.state, repairable: row.repairable, accessible: row.accessible };
  });
  requireHandoff(new Set(result.map((item) => item.conditionId)).size === result.length, "Conditions repeat a reference.");
  return result;
}
export function fundingInformation(doc: SourceDocument): FundingInformation {
  requireHandoff(doc.kind === "Owner funding", "Use an owner funding confirmation.");
  const row = details(sourceDetails(words(doc.detailsJson, "Funding information", 140000)),
    ["ownerPartyId", "currency", "confirmedCents", "confirmedAt", "paymentBehavior", "responseMinutes"], [], "Funding information");
  requireHandoff(row.paymentBehavior === "Settle" || row.paymentBehavior === "Reject" || row.paymentBehavior === "Uncertain", "Identify the payment service behavior.");
  const result: FundingInformation = { ownerPartyId: words(row.ownerPartyId, "Funding owner", 160), currency: currencyCode(row.currency), confirmedCents: money(row.confirmedCents),
    confirmedAt: instant(row.confirmedAt), paymentBehavior: row.paymentBehavior, responseMinutes: minutes(row.responseMinutes, "Payment response time") };
  requireHandoff(result.ownerPartyId === doc.partyId, "The funding confirmation must identify its owner.");
  return result;
}
export function validateSupportingDocument(doc: SourceDocument): void {
  if (!doc.detailsJson) return;
  if (doc.kind === "Provider information") providerServices(doc);
  else if (doc.kind === "Property condition") propertyConditions(doc);
  else if (doc.kind === "Owner funding") fundingInformation(doc);
}

/** A few satisfied checks are not proof of a broader property outcome. Coverage is explicitly prepared. */
export function readinessCoverage(doc: SourceDocument, goal: string): boolean {
  const body = sourceDetails(words(doc.detailsJson, "Condition information", 140000));
  if (!body.coverage) return false;
  const coverage = details(body.coverage, ["goal", "conditionIds", "reason"], [], "Outcome coverage");
  const ids = wordList(coverage.conditionIds, "Outcome checks", 48, 1);
  words(coverage.reason, "Coverage explanation", 3000);
  const conditions = propertyConditions(doc);
  return coverage.goal === goal && ids.length === conditions.length && conditions.every((item) => ids.includes(item.conditionId));
}
