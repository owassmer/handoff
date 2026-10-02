import type { WorkPlanDraft } from "./reasoner.js";
import type { Plan, Handoff, Workspace } from "./records.js";
import type { HandoffDetails } from "./workDetails.js";
import type { Quote } from "./deliveryRecords.js";
import { offerFromRecord } from "./deliveryRecords.js";
import { money } from "./deliveryContracts.js";
import { details, digest, entries, orderedJson, parseDetails, requireHandoff, words } from "./values.js";

/** A reviewed interpretation of a quoted line, not permission to substitute arbitrary work. */
export interface WorkSelection {
  quoteId: string; quoteLineId: string; scope: string; reason: string;
}
export interface Proposal extends WorkPlanDraft {
  selections: WorkSelection[];
  fixedProviderPartyId?: string;
}
export function readSelections(value: unknown): WorkSelection[] {
  const result = entries(value, "Quoted work", 48, 1).map((entry): WorkSelection => {
    const row = details(entry, ["quoteId", "quoteLineId", "scope", "reason"], [], "Quoted work");
    return { quoteId: words(row.quoteId, "Quote", 160), quoteLineId: words(row.quoteLineId, "Quote line", 160),
      scope: words(row.scope, "Proposed work", 1000), reason: words(row.reason, "Scope explanation", 1500) };
  });
  requireHandoff(new Set(result.map((line) => `${line.quoteId}/${line.quoteLineId}`)).size === result.length,
    "Choose each quoted line once.");
  return result;
}
export function planSelections(plan: Plan): WorkSelection[] {
  return plan.selectionJson ? readSelections(parseDetails(plan.selectionJson, "Quoted work")) : [];
}
export function selectedCost(selections: WorkSelection[], quotes: readonly Quote[], currency: string): string {
  readSelections(selections);
  const total = selections.reduce((sum, selected) => {
    const quote = quotes.find((item) => item.quoteId === selected.quoteId);
    requireHandoff(quote && quote.status === "Offered" && quote.currency === currency,
      "The selected offer is unavailable or uses a different currency.");
    const line = offerFromRecord(quote).lines.find((item) => item.lineId === selected.quoteLineId);
    requireHandoff(line, "The selected work is not in this quote.");
    return sum + BigInt(line.amountCents);
  }, 0n);
  return money(total.toString());
}
/** Pricing identity excludes presentation text but includes each actual source price and currency. */
export function selectedPriceIdentity(selections: WorkSelection[], quotes: readonly Quote[], currency: string): string {
  selectedCost(selections, quotes, currency);
  const prices = selections.map((selection) => {
    const quote = quotes.find((item) => item.quoteId === selection.quoteId)!;
    const line = offerFromRecord(quote).lines.find((item) => item.lineId === selection.quoteLineId)!;
    return [selection.quoteId, selection.quoteLineId, line.amountCents, quote.currency];
  });
  return orderedJson(prices.sort((a, b) => orderedJson(a).localeCompare(orderedJson(b))));
}
export function validateSelection(draft: Proposal, quotes: readonly Quote[]): Proposal {
  requireHandoff(draft.selections.every((line) => draft.scope.includes(line.scope))
    && draft.scope.every((scope) => draft.selections.some((line) => line.scope === scope)),
  "Each proposed work item needs its reviewed quote selection.");
  requireHandoff(selectedCost(draft.selections, quotes, draft.currency) === draft.estimatedCostCents,
    "The estimate must equal the selected quoted costs.");
  requireHandoff(BigInt(draft.budgetCents) >= BigInt(draft.estimatedCostCents), "The budget must cover the selected work.");
  draft.selections.forEach((line) => {
    const quote = quotes.find((item) => item.quoteId === line.quoteId)!;
    requireHandoff(draft.sourceDocumentIds.includes(quote.sourceDocumentId!), "Include each selected quote with the proposal.");
    requireHandoff(!draft.fixedProviderPartyId || quote.providerPartyId === draft.fixedProviderPartyId,
      "The selected work must use the explicitly required provider.");
  });
  return draft;
}
/** Fingerprint only material facts, source versions and authority, never unrelated workspace activity. */
export function materialBasis(handoff: Handoff, workspace: Workspace, world: HandoffDetails): string {
  const fields = (record: object, keys: string[]): object => Object.fromEntries(keys.map((key) => [key, Reflect.get(record, key)]));
  const sorted = (rows: object[]): object[] => rows.sort((a, b) => orderedJson(a).localeCompare(orderedJson(b)));
  return digest({ handoff: fields(handoff, ["handoffId", "propertyId", "tenancyId", "goal", "businessDate", "fixedRequirements", "status"]),
    authority: fields(workspace, ["readerIds", "workUserIds", "decideUserIds", "adminUserIds", "currency", "mode", "modelRid"]),
    property: fields(world.property, ["propertyId", "address", "description", "readerIds"]),
    tenancy: fields(world.tenancy, ["tenancyId", "startDate", "endDate", "noticeDate", "endingKind", "landlordPartyId", "tenantPartyIds", "readerIds"]),
    documents: sorted(world.documents.filter((doc) => doc.kind !== "Owner funding").map((doc) => fields(doc, ["documentId", "sourceSystem", "sourceRecordId", "sourceVersion", "text", "detailsJson", "kind", "partyId", "availableFrom", "mediaSetRid", "mediaItemRid", "readerIds"]))),
    agreements: sorted(world.agreements.map((row) => fields(row, ["agreementId", "termsText", "effectiveFrom", "sourceDocumentId", "readerIds"]))),
    obligations: sorted(world.obligations.map((row) => fields(row, ["obligationId", "description", "status", "dueDate", "readerIds"]))),
    parties: sorted(world.parties.filter((row) => row.partyId === world.tenancy.landlordPartyId || world.tenancy.tenantPartyIds?.includes(row.partyId)
      || world.documents.some((doc) => doc.kind !== "Owner funding" && doc.partyId === row.partyId)).map((row) => fields(row, ["partyId", "name", "description", "email", "readerIds"]))) });
}
