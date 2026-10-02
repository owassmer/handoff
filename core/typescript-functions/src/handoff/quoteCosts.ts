import type { Long } from "@osdk/functions";
import { details, requireHandoff, wordList, words } from "./values.js";
import { currencyCode, instant, minutes, money, quoteLines, sourceRecord,
  type CommissionInput, type QuoteLine, type QuoteOffer, type ScopeLine, type WorkMandate } from "./deliveryContracts.js";

export function sumQuotedCosts(lines: readonly QuoteLine[]): Long {
  quoteLines(lines);
  return money(lines.reduce((sum, line) => sum + BigInt(money(line.amountCents)), 0n).toString(), "Quoted total");
}
export function validateQuoteOffer(value: unknown): QuoteOffer {
  const row = details(value, ["sourceSystem", "sourceRecordId", "sourceDocumentId", "title", "providerPartyId", "kind", "currency", "lines", "totalCents", "depositCents", "paymentTerms", "requirements", "availableFrom", "validUntil", "durationMinutes", "responseMinutes"], [], "Provider offer");
  const lines = quoteLines(row.lines), totalCents = money(row.totalCents), depositCents = money(row.depositCents);
  requireHandoff(sumQuotedCosts(lines) === totalCents, "The quoted lines do not add up to the provider's total.");
  requireHandoff(BigInt(depositCents) <= BigInt(totalCents), "The advance payment exceeds the quoted total.");
  return { ...sourceRecord(row), title: words(row.title, "Quote title", 200), providerPartyId: words(row.providerPartyId, "Provider", 160),
    kind: words(row.kind, "Service type", 100), currency: currencyCode(row.currency), lines, totalCents, depositCents,
    paymentTerms: words(row.paymentTerms, "Payment terms", 3000), requirements: wordList(row.requirements, "Confirmed requirements", 32, 0, 1000),
    availableFrom: instant(row.availableFrom), validUntil: instant(row.validUntil),
    durationMinutes: minutes(row.durationMinutes, "Expected duration"), responseMinutes: minutes(row.responseMinutes, "Expected reply time") };
}

/** Exact costs and limits only. The coordinator reasons about suitability before offering the plan. */
export function priceCommission(mandate: WorkMandate, quote: QuoteOffer,
  selection: CommissionInput["scope"], alreadyCommittedCents: Long, now: string): { scope: ScopeLine[]; totalCents: Long; depositCents: Long } {
  validateQuoteOffer(quote);
  requireHandoff(instant(now) <= instant(quote.validUntil), "The provider's offer has expired. Obtain current terms before commissioning.");
  requireHandoff(currencyCode(mandate.currency) === quote.currency, "The offer and accepted work use different currencies.");
  requireHandoff(!mandate.fixedProviderPartyId || mandate.fixedProviderPartyId === quote.providerPartyId,
    "The accepted work requires a different provider.");
  requireHandoff(mandate.sourceDocumentIds.includes(quote.sourceDocumentId), "This offer was not part of the accepted work recommendation.");
  // Requirements the offer does not state go to the provider with the order for confirmation (commissionJob).
  requireHandoff(selection.length > 0 && selection.length <= 48
    && new Set(selection.map((line) => line.quoteLineId)).size === selection.length, "Choose each quoted scope line once.");
  const scope = selection.map((selectionLine): ScopeLine => {
    const line = quote.lines.find((candidate) => candidate.lineId === selectionLine.quoteLineId);
    requireHandoff(line, "A selected line is not in the provider's offer.");
    requireHandoff(mandate.scope.includes(selectionLine.acceptedScope), "The selected work is outside the accepted scope.");
    // Current proposals carry a reviewed equivalence; older acceptances retain the exact-scope guard.
    requireHandoff(mandate.reviewedSelections ? mandate.reviewedSelections.some((reviewed) => reviewed.quoteId === mandate.quoteId
      && reviewed.quoteLineId === selectionLine.quoteLineId && reviewed.scope === selectionLine.acceptedScope) : line.description === selectionLine.acceptedScope,
      "The quote describes different work. Prepare a matching recommendation before commissioning.");
    return { ...line, acceptedScope: selectionLine.acceptedScope };
  });
  const totalCents = sumQuotedCosts(scope.map(({ acceptedScope: _scope, ...line }) => line));
  requireHandoff(BigInt(totalCents) + BigInt(money(alreadyCommittedCents)) <= BigInt(money(mandate.budgetCents)),
    "This commitment would exceed the accepted work budget.");
  // A partial package cannot assume a pro-rata advance; obtain a separate offer with actual terms.
  requireHandoff(scope.length === quote.lines.length || quote.depositCents === "0",
    "Obtain advance-payment terms for the selected part of this offer.");
  return { scope, totalCents, depositCents: quote.depositCents };
}

export function invoiceMatchesJob(invoiceLines: readonly QuoteLine[], agreedLines: readonly QuoteLine[], currency: string, jobCurrency: string): boolean {
  quoteLines(invoiceLines); quoteLines(agreedLines);
  if (currencyCode(currency) !== currencyCode(jobCurrency)) return false;
  return invoiceLines.every((line) => agreedLines.some((agreed) => agreed.lineId === line.lineId
    && agreed.amountCents === line.amountCents && agreed.description === line.description));
}
