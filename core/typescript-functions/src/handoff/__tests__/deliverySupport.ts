import { HandoffProperty, HandoffTenancy, HandoffWorkspace, HandoffCase, HandoffParty, HandoffDocument, HandoffWorkPlan, HandoffDecision,
  HandoffJob, HandoffInspection, HandoffQuote, HandoffInvoice, HandoffFunding, HandoffPayment } from "@ontology/sdk";
import type { CompileTimeMetadata, ObjectTypeDefinition } from "@osdk/client";
import { createEditBatch } from "@osdk/functions";
import type { HandoffEdit } from "../records.js";
import { WorkspaceStore } from "./workspaceSupport.js";
import { acceptedContent } from "../workPlans.js";
import { recordQuote, type DeliveryContext } from "../deliveryRecords.js";
import { preparedDetails } from "../sourceAccess.js";
import { recordOwnerFunding } from "../funding.js";
import type { CommissionInput, QuoteOffer, WorkMandate } from "../deliveryContracts.js";

export const NOW = "2026-09-23T10:00:00.000Z";
export const LATER = "2026-09-23T12:00:00.000Z";
export const WORKSPACE = "delivery-workspace", HANDOFF = "delivery-handoff", PROVIDER = "care-provider", OWNER = "property-owner", PERSON = "workspace-user";
const NEW_TYPES = [HandoffJob, HandoffInspection, HandoffQuote, HandoffInvoice, HandoffFunding, HandoffPayment];
type Props<T extends ObjectTypeDefinition> = Partial<CompileTimeMetadata<T>["props"]>;
/** Extends the existing test harness only for these tests. It is not a concurrency simulator. */
export class DeliveryStore extends WorkspaceStore {
  override apply(edits: HandoffEdit[]): void {
    edits.forEach((edit) => {
      if (edit.type === "updateObject") {
        const type = NEW_TYPES.find((candidate) => candidate.apiName === edit.obj.$apiName);
        if (type) { this.change(type, String(edit.obj.$primaryKey), edit.properties as Props<typeof type>); return; }
      }
      super.apply([edit]);
    });
  }
  context(now = NOW): DeliveryContext {
    return { client: this.client, batch: createEditBatch<HandoffEdit>(this.client),
      workspace: this.get(HandoffWorkspace, WORKSPACE), handoff: this.get(HandoffCase, HANDOFF),
      caller: { id: PERSON, name: "Operator" }, now };
  }
  async run<T>(operation: (context: DeliveryContext) => Promise<T>, now = NOW): Promise<{ result: T; edits: HandoffEdit[] }> {
    const context = this.context(now), result = await operation(context), edits = context.batch.getEdits();
    this.apply(edits); return { result, edits };
  }
}
export function offer(): QuoteOffer {
  return { title: "Inspect and report on the property", sourceSystem: "provider-records", sourceRecordId: "offer-17-v1",
    sourceDocumentId: "quote-source", providerPartyId: PROVIDER, kind: "Assessment", currency: "USD",
    lines: [{ lineId: "condition", description: "Inspect condition and provide a report.", amountCents: "18000" },
      { lineId: "access", description: "Test door access and report findings.", amountCents: "6500" }],
    totalCents: "24500", depositCents: "0", paymentTerms: "Balance due after the report; payment due in seven days.",
    requirements: ["No repairs are authorized."], availableFrom: "2026-09-24T09:00:00.000Z",
    validUntil: "2026-10-01T17:00:00.000Z", responseMinutes: 30, durationMinutes: 60 };
}
export function mandate(): WorkMandate {
  return { decisionId: "accepted-1", workPlanId: "plan-1", revision: "1", propertyId: "property-1", currency: "USD",
    budgetCents: "30000", scope: offer().lines.map((line) => line.description), requirements: offer().requirements,
    sourceDocumentIds: ["quote-source"] };
}
export async function preparedDelivery(advance = "0"): Promise<{ store: DeliveryStore; input: CommissionInput; quoteId: string; fundingId: string }> {
  const store = new DeliveryStore(), shared = { workspaceId: WORKSPACE, readerIds: [PERSON] };
  store.put(HandoffWorkspace, { ...shared, name: "Property work", revision: "1", currency: "USD", mode: "demo",
    workUserIds: [PERSON], decideUserIds: [PERSON], adminUserIds: [PERSON] });
  store.put(HandoffCase, { ...shared, handoffId: HANDOFF, propertyId: "property-1", tenancyId: "tenancy-1",
    workPlanId: "plan-1", title: "Prepare the property", status: "Open", revision: "2", goal: "Understand required work", physicalProgress: "Arranging work" });
  store.put(HandoffProperty, { ...shared, propertyId: "property-1", name: "Property", address: "1 Market Road", description: "Home" });
  store.put(HandoffTenancy, { ...shared, tenancyId: "tenancy-1", propertyId: "property-1", title: "Tenancy", landlordPartyId: OWNER, tenantPartyIds: [] });
  store.put(HandoffParty, { ...shared, partyId: PROVIDER, name: "Property Care", kind: "Organization" });
  store.put(HandoffParty, { ...shared, partyId: OWNER, name: "Property owner", kind: "Person" });
  ["quote-source", "funding-source", "report-source", "invoice-source", "historic-source"].forEach((id) => store.put(HandoffDocument,
    { ...shared, documentId: id, handoffId: HANDOFF, title: id, text: "Supporting source material.", kind: "Source" }));
  store.change(HandoffDocument, "quote-source", { kind: "Quote", partyId: PROVIDER });
  store.change(HandoffDocument, "invoice-source", { kind: "Invoice", partyId: PROVIDER });
  store.change(HandoffDocument, "funding-source", { kind: "Owner funding", sourceSystem: "owner-books", sourceRecordId: "allocation-1", partyId: OWNER,
    detailsJson: preparedDetails(JSON.stringify({ ownerPartyId: OWNER, currency: "USD", confirmedCents: "100000", confirmedAt: NOW, paymentBehavior: "Settle", responseMinutes: 1 }), { id: PERSON, name: "Operator" }) });
  const quote = { ...offer(), depositCents: advance };
  const plan = store.put(HandoffWorkPlan, { ...shared, workPlanId: "plan-1", handoffId: HANDOFF, title: quote.title,
    summary: "Obtain a condition report before recommending repairs.", desiredOutcome: "A usable report on the property.",
    scope: mandate().scope, estimatedCostCents: quote.totalCents, budgetCents: "30000", currency: "USD",
    fixedRequirements: quote.requirements, sourceDocumentIds: [quote.sourceDocumentId], providerPartyId: PROVIDER,
    rationale: "The provider can assess the property.", revision: "1", basisRevision: "2", status: "Accepted", acceptedDecisionId: "accepted-1" });
  store.put(HandoffDecision, { ...shared, decisionId: "accepted-1", handoffId: HANDOFF, workPlanId: "plan-1",
    acceptedRevision: "1", contentJson: acceptedContent(plan), decidedBy: PERSON, decidedAt: NOW });
  const { result: quoteId } = await store.run((context) => recordQuote(context, quote));
  const { result: fundingId } = await store.run((context) => recordOwnerFunding(context, { sourceSystem: "owner-books", sourceRecordId: "allocation-1",
    sourceDocumentId: "funding-source", title: "Property work funds", ownerPartyId: OWNER, currency: "USD", confirmedCents: "100000", confirmedAt: NOW }));
  return { store, quoteId, fundingId, input: { workPlanId: "plan-1", expectedRevision: "1", quoteId, fundingId,
    scope: quote.lines.map((line) => ({ quoteLineId: line.lineId, acceptedScope: line.description })) } };
}
