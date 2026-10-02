import { describe, expect, it } from "vitest";
import { HandoffAgentWork, HandoffDocument, HandoffFunding, HandoffInspection, HandoffInvoice, HandoffJob, HandoffMessage, HandoffPayment, HandoffQuote } from "@ontology/sdk";
import { loadOwnerFunding, observeProviderPayment, recordOwnerFunding, requestProviderPayment } from "../funding.js";
import { commissionJob, checkJobCompletion } from "../delivery.js";
import { loadDeliveryRecords, recordExistingJob, recordInspection, recordInvoice, recordQuote } from "../deliveryRecords.js";
import { dueProviderRequests, providerAppointment, respondToProviderRequest } from "../counterparts.js";
import { priceCommission } from "../quoteCosts.js";
import { businessMoment } from "../clock.js";
import { preparedDetails, sourceDetails } from "../sourceAccess.js";
import { LATER, NOW, OWNER, PERSON, PROVIDER, mandate, offer, preparedDelivery } from "./deliverySupport.js";
import type { ExistingJob, InspectionReport, OwnerAllocation, SupplierInvoice } from "../deliveryContracts.js";

// Intentionally literal wire strings. Do not pass these through Date/instant or a date-shaping fixture.
const WIRE_NOW = "2026-09-23T10:00:00Z";
const WIRE_AVAILABLE = "2026-09-24T09:00:00Z";
const WIRE_EXPIRES = "2026-10-01T17:00:00Z";
const WIRE_COMPLETION = "2026-09-24T11:00:00Z";
const COMPLETION = "2026-09-24T11:00:00.000Z";
const allocation = (): OwnerAllocation => ({ sourceSystem: "owner-books", sourceRecordId: "allocation-1", sourceDocumentId: "funding-source",
  title: "Property work funds", ownerPartyId: OWNER, currency: "USD", confirmedCents: "100000", confirmedAt: NOW });
const historical = (): ExistingJob => ({ sourceSystem: "provider-books", sourceRecordId: "existing-job", sourceDocumentId: "historic-source",
  title: "Earlier assessment", providerPartyId: PROVIDER, kind: "Assessment", currency: "USD", scope: offer().lines,
  status: "Underway", startedAt: NOW, summary: "Assessment underway." });
const report = (jobId: string): InspectionReport => ({ sourceSystem: "provider-books", sourceRecordId: "report-1", sourceDocumentId: "report-source",
  title: "Assessment report", observerPartyId: PROVIDER, jobId, observedAt: COMPLETION, purpose: "Completion check",
  findings: offer().lines.map((line) => ({ lineId: line.lineId, result: "Satisfied", observation: "The requested assessment was completed.", method: "Review report." })) });
const invoice = (jobId: string): SupplierInvoice => ({ sourceSystem: "provider-books", sourceRecordId: "invoice-1", sourceDocumentId: "invoice-source",
  title: "Assessment invoice", jobId, providerPartyId: PROVIDER, payerPartyId: OWNER, currency: "USD", lines: offer().lines, totalCents: "24500",
  issuedAt: COMPLETION, dueAt: "2026-10-01T11:00:00.000Z", paymentTerms: "Due seven days after assessment." });

describe("owner funding wire representation at creation, replay and commission", () => {
  it("replays the same allocation and commissions within real funds when the saved SDK time omits milliseconds", async () => {
    const { store, input, fundingId } = await preparedDelivery();
    store.change(HandoffFunding, fundingId, { confirmedAt: WIRE_NOW });
    expect(store.get(HandoffFunding, fundingId).confirmedAt).toBe(WIRE_NOW);
    expect((await store.run((context) => recordOwnerFunding(context, allocation()), LATER)).edits).toEqual([]);
    const { position } = await loadOwnerFunding(store.context(), fundingId);
    expect(position.availableCents).toBe("100000");
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    expect(store.get(HandoffJob, jobId).committedCents).toBe("24500");
    expect((await loadOwnerFunding(store.context(), fundingId)).position.availableCents).toBe("75500");
    expect(store.all(HandoffMessage)).toHaveLength(1);
    expect(store.all(HandoffPayment)).toHaveLength(0);
    expect((await store.run((context) => commissionJob(context, input))).edits).toEqual([]);
  });
  it.each(["confirmedAt", "confirmedCents", "currency", "ownerPartyId"] as const)("still rejects a changed %s under a new version of the same allocation", async (field) => {
    const { store, input, fundingId } = await preparedDelivery();
    store.change(HandoffFunding, fundingId, { confirmedAt: WIRE_NOW });
    const original = store.get(HandoffDocument, "funding-source");
    const changed = { ...sourceDetails(original.detailsJson!), [field]: { confirmedAt: "2026-09-23T10:00:00.001Z", confirmedCents: "99999", currency: "CAD", ownerPartyId: "another-owner" }[field] };
    store.put(HandoffDocument, { ...original, documentId: "funding-source-v2", sourceVersion: "2",
      partyId: field === "ownerPartyId" ? "another-owner" : OWNER, detailsJson: preparedDetails(JSON.stringify(changed), { id: PERSON, name: "Operator" }) });
    await expect(store.run((context) => commissionJob(context, input))).rejects.toThrow(/same owner allocation has changed/);
    expect(store.all(HandoffJob)).toHaveLength(0);
    // Outcome reconciliation retains its pre-existing exception; it does not authorize new spending.
    await expect(loadOwnerFunding(store.context(), fundingId, false)).resolves.toHaveProperty("funding.fundingId", fundingId);
  });
  it.each(["sourceSystem", "sourceRecordId", "sourceDocumentId", "confirmedAt"] as const)("does not let an instant-only fix substitute %s on replay", async (field) => {
    const { store } = await preparedDelivery();
    const changed = { ...allocation(), [field]: field === "confirmedAt" ? "2026-09-23T09:59:59.999Z" : "other-source" };
    await expect(store.run((context) => recordOwnerFunding(context, changed))).rejects.toThrow();
    expect(store.all(HandoffFunding)).toHaveLength(1);
  });
  it("creates a new allocation canonically from a valid whole-second source and keeps timestamp validation", async () => {
    const { store } = await preparedDelivery();
    const original = store.get(HandoffDocument, "funding-source");
    const body = { ...sourceDetails(original.detailsJson!), confirmedAt: WIRE_NOW };
    store.put(HandoffDocument, { ...original, documentId: "funding-other", sourceRecordId: "allocation-2", detailsJson: preparedDetails(JSON.stringify(body), { id: PERSON, name: "Operator" }) });
    const { result } = await store.run((context) => recordOwnerFunding(context, { ...allocation(), sourceRecordId: "allocation-2", sourceDocumentId: "funding-other", confirmedAt: WIRE_NOW }));
    expect(store.get(HandoffFunding, result).confirmedAt).toBe(NOW);
    store.change(HandoffFunding, result, { confirmedAt: "bad-timestamp" });
    await expect(loadOwnerFunding(store.context(), result)).rejects.toThrow(/valid UTC/);
  });
});

describe("source-record replay with literal stored timestamps", () => {
  it("deduplicates a quote's availability and expiry, but not a different instant", async () => {
    const { store, quoteId } = await preparedDelivery();
    store.change(HandoffQuote, quoteId, { availableFrom: WIRE_AVAILABLE, validUntil: WIRE_EXPIRES });
    expect((await store.run((context) => recordQuote(context, offer()))).edits).toEqual([]);
    await expect(store.run((context) => recordQuote(context, { ...offer(), availableFrom: "2026-09-24T09:00:00.001Z" }))).rejects.toThrow(/different saved details/);
  });
  it("deduplicates the actual start time of existing work, not an altered start time", async () => {
    const { store } = await preparedDelivery();
    const { result } = await store.run((context) => recordExistingJob(context, historical()));
    store.change(HandoffJob, result, { createdAt: WIRE_NOW });
    expect((await store.run((context) => recordExistingJob(context, historical()), LATER)).edits).toEqual([]);
    await expect(store.run((context) => recordExistingJob(context, { ...historical(), startedAt: "2026-09-23T09:59:59.999Z" }))).rejects.toThrow(/different saved details/);
  });
  it("keeps inspection actual time and invoice issue/due time strict on replay", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const { result: inspectionId } = await store.run((context) => recordInspection(context, report(jobId)), COMPLETION);
    store.change(HandoffInspection, inspectionId, { observedAt: WIRE_COMPLETION });
    expect((await store.run((context) => recordInspection(context, report(jobId)), COMPLETION)).edits).toEqual([]);
    await expect(store.run((context) => recordInspection(context, { ...report(jobId), observedAt: "2026-09-24T10:59:59.999Z" }), COMPLETION)).rejects.toThrow(/different saved details/);
    const { result: invoiceId } = await store.run((context) => recordInvoice(context, invoice(jobId)), COMPLETION);
    store.change(HandoffInvoice, invoiceId, { issuedAt: WIRE_COMPLETION, dueAt: "2026-10-01T11:00:00Z" });
    expect((await store.run((context) => recordInvoice(context, invoice(jobId)), COMPLETION)).edits).toEqual([]);
    await expect(store.run((context) => recordInvoice(context, { ...invoice(jobId), dueAt: "2026-10-01T11:00:00.001Z" }), COMPLETION)).rejects.toThrow(/different saved details/);
    await expect(store.run((context) => recordInvoice(context, { ...invoice(jobId), dueAt: "2026-09-24T10:59:59.999Z" }), COMPLETION)).rejects.toThrow(/issue and due/);
  });
  it("compares pending same-batch timestamps without duplicating objects or ignoring changed time", async () => {
    const { store } = await preparedDelivery();
    const context = store.context();
    await recordExistingJob(context, historical());
    expect(await recordExistingJob(context, { ...historical(), startedAt: WIRE_NOW })).toBeDefined();
    expect(context.batch.getEdits().filter((edit) => edit.type === "createObject")).toHaveLength(1);
    await expect(recordExistingJob(context, { ...historical(), startedAt: "2026-09-23T09:59:59.999Z" })).rejects.toThrow(/different saved details/);
  });
});

describe("semantic ordering, expiry, actual observations and payment outcomes", () => {
  it("rejects an offer 1ms after expiry instead of treating Z as later than .001Z", () => {
    const quoted = { ...offer(), availableFrom: WIRE_AVAILABLE, validUntil: WIRE_EXPIRES };
    const scope = quoted.lines.map((line) => ({ quoteLineId: line.lineId, acceptedScope: line.description }));
    expect(priceCommission(mandate(), quoted, scope, "0", "2026-10-01T17:00:00.000Z").totalCents).toBe("24500");
    expect(() => priceCommission(mandate(), quoted, scope, "0", "2026-10-01T17:00:00.001Z")).toThrow(/expired/);
  });
  it("starts no earlier than now when availability is persisted as whole seconds", () => {
    const quoted = { ...offer(), availableFrom: WIRE_AVAILABLE };
    expect(providerAppointment(quoted, "2026-09-24T09:00:00.001Z", [], "job")).toEqual({ start: "2026-09-24T09:00:00.001Z", end: "2026-09-24T10:00:00.001Z" });
  });
  it("recognizes a due whole-second wake and never moves business time backwards", async () => {
    const { store } = await preparedDelivery();
    const work = store.put(HandoffAgentWork, { workId: "wire-work", businessTime: WIRE_NOW, nextWakeAt: WIRE_NOW, nextBusinessAt: "2026-09-23T10:00:00.001Z" });
    expect(businessMoment(work, "2026-09-23", NOW)).toBe("2026-09-23T10:00:00.001Z");
    store.change(HandoffAgentWork, "wire-work", { businessTime: "2026-09-23T10:00:00.001Z", nextBusinessAt: WIRE_NOW });
    expect(businessMoment(store.get(HandoffAgentWork, "wire-work"), "2026-09-23", NOW)).toBe("2026-09-23T10:00:00.001Z");
  });
  it("recognizes appointment replies exactly when due and checks real inspection time against the appointment", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const requestId = store.get(HandoffJob, jobId).requestMessageId!;
    store.change(HandoffMessage, requestId, { responseDueAt: "2026-09-23T10:30:00Z" });
    const context = store.context();
    const records = await loadDeliveryRecords(context.client, context.workspace, context.caller, context.handoff);
    expect(dueProviderRequests(records, "2026-09-23T10:30:00.000Z")).toHaveLength(1);
    expect(dueProviderRequests(records, "2026-09-23T10:29:59.999Z")).toHaveLength(0);
    await store.run((ctx) => respondToProviderRequest(ctx, requestId), LATER);
    store.change(HandoffJob, jobId, { appointmentAt: WIRE_AVAILABLE });
    const { result: inspectionId } = await store.run((ctx) => recordInspection(ctx, report(jobId)), COMPLETION);
    store.change(HandoffInspection, inspectionId, { observedAt: WIRE_COMPLETION });
    expect((await store.run((ctx) => checkJobCompletion(ctx, jobId, inspectionId), COMPLETION)).result).toBe("Complete");
    const { result: tooEarlyId } = await store.run((ctx) => recordInspection(ctx, { ...report(jobId), sourceRecordId: "early", observedAt: "2026-09-24T08:59:59.999Z" }), COMPLETION);
    await expect(store.run((ctx) => checkJobCompletion(ctx, jobId, tooEarlyId), COMPLETION)).rejects.toThrow(/predates|older/);
  });
  it("replays a payment result at the same wire instant, not a different confirmation time", async () => {
    const { store, input } = await preparedDelivery("5000");
    const { result: jobId } = await store.run((ctx) => commissionJob(ctx, input));
    const { result: paymentId } = await store.run((ctx) => requestProviderPayment(ctx, jobId, "Advance"));
    store.change(HandoffPayment, paymentId, { requestedAt: WIRE_NOW });
    const result = { instructionKey: paymentId, sourceReference: "settled-1", amountCents: "5000", currency: "USD", status: "Settled" as const, observedAt: LATER, definitive: true };
    await store.run((ctx) => observeProviderPayment(ctx, paymentId, result), LATER);
    store.change(HandoffPayment, paymentId, { observedAt: "2026-09-23T12:00:00Z" });
    expect((await store.run((ctx) => observeProviderPayment(ctx, paymentId, result), LATER)).edits).toEqual([]);
    await expect(store.run((ctx) => observeProviderPayment(ctx, paymentId, { ...result, observedAt: "2026-09-23T11:59:59.999Z" }), LATER)).rejects.toThrow(/conflicting confirmation/);
  });
});
