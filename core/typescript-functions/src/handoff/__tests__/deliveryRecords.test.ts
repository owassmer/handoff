import { describe, expect, it } from "vitest";
import { HandoffCase, HandoffDecision, HandoffDocument, HandoffFunding, HandoffInspection, HandoffInvoice,
  HandoffJob, HandoffMessage, HandoffParty, HandoffPayment, HandoffQuote, HandoffWorkPlan, HandoffWorkspace } from "@ontology/sdk";
import { recordExistingJob, recordInspection, recordInvoice, recordQuote, loadDeliveryRecords } from "../deliveryRecords.js";
import { commissionJob, checkJobCompletion } from "../delivery.js";
import { dueProviderRequests, prepareProviderReply, queueProviderRequest, respondToProviderRequest } from "../counterparts.js";
import { loadOwnerFunding, observeProviderPayment, requestProviderPayment } from "../funding.js";
import { requestWorkCorrespondence } from "../correspondence.js";
import { planDraft } from "../workPlans.js";
import { orderedJson, reference } from "../values.js";
import type { InspectionReport, SupplierInvoice } from "../deliveryContracts.js";
import { HANDOFF, LATER, NOW, OWNER, PERSON, PROVIDER, WORKSPACE, offer, preparedDelivery, type DeliveryStore } from "./deliverySupport.js";

const COMPLETION = "2026-09-24T11:00:00.000Z";
function report(jobId: string): InspectionReport {
  return { sourceSystem: "inspection-service", sourceRecordId: "report-1", sourceDocumentId: "report-source", title: "Condition report delivered",
    observerPartyId: PROVIDER, jobId, observedAt: COMPLETION, purpose: "Completion check",
    findings: offer().lines.map((line) => ({ lineId: line.lineId, result: "Satisfied", observation: "The requested assessment and report were supplied.", method: "Reviewed the report and access test result." })) };
}
function invoice(jobId: string): SupplierInvoice {
  return { sourceSystem: "provider-books", sourceRecordId: "invoice-1", sourceDocumentId: "invoice-source", title: "Assessment invoice",
    jobId, providerPartyId: PROVIDER, payerPartyId: OWNER, currency: "USD", lines: offer().lines, totalCents: offer().totalCents,
    issuedAt: COMPLETION, dueAt: "2026-10-01T11:00:00.000Z", paymentTerms: "Due seven days after the report." };
}
async function records(store: DeliveryStore): ReturnType<typeof loadDeliveryRecords> {
  const context = store.context();
  return loadDeliveryRecords(context.client, context.workspace, context.caller, context.handoff);
}
async function completeJob(store: DeliveryStore, jobId: string): Promise<void> {
  const { result: inspectionId } = await store.run((context) => recordInspection(context, report(jobId)), COMPLETION);
  await store.run((context) => checkJobCompletion(context, jobId, inspectionId), COMPLETION);
}

describe("source records and historical work", () => {
  it("deduplicates offers without replacing their source facts", async () => {
    const { store, quoteId } = await preparedDelivery();
    expect((await store.run((context) => recordQuote(context, offer()))).edits).toEqual([]);
    await expect(store.run((context) => recordQuote(context, { ...offer(), title: "Changed source" }))).rejects.toThrow(/different saved details/);
    expect(store.get(HandoffQuote, quoteId).title).toBe(offer().title);
  });
  it("recognizes pre-existing work without inventing acceptance, funding, requests or success", async () => {
    const { store } = await preparedDelivery();
    const input = { sourceSystem: "contractor", sourceRecordId: "earlier-1", sourceDocumentId: "historic-source", title: "Earlier assessment",
      providerPartyId: PROVIDER, kind: "Assessment", currency: "USD", scope: offer().lines,
      status: "Complete" as const, startedAt: "2026-09-20T10:00:00.000Z", summary: "Provider reports the assessment completed." };
    const { result: id } = await store.run((context) => recordExistingJob(context, input));
    const job = store.get(HandoffJob, id);
    expect(job.origin).toBe("Existing"); expect(job.status).toBe("Awaiting check");
    expect(job.decisionId).toBeUndefined(); expect(job.instructionKey).toBeUndefined(); expect(job.committedCents).toBeUndefined();
    expect(store.all(HandoffMessage)).toEqual([]); expect(store.all(HandoffPayment)).toEqual([]);
    expect((await store.run((context) => recordExistingJob(context, input))).edits).toEqual([]);
  });
  it("rejects foreign handoff evidence, inaccessible sources, malformed input and future observations", async () => {
    const { store } = await preparedDelivery();
    store.change(HandoffDocument, "quote-source", { handoffId: "other" });
    await expect(store.run((context) => recordQuote(context, offer()))).rejects.toThrow(/linked to this handoff/);
    store.change(HandoffDocument, "quote-source", { handoffId: HANDOFF, readerIds: [PERSON, "someone-else"] });
    await expect(store.run((context) => recordQuote(context, offer()))).rejects.toThrow(/access settings/);
    await expect(store.run((context) => recordQuote(context, { ...offer(), approve: true }))).rejects.toThrow(/unexpected/);
    await expect(store.run((context) => recordInspection(context, report("missing-job")))).rejects.toThrow(/future/);
  });
});

describe("accepted work and commitments", () => {
  it("saves commitment and request together, retains assessment scope, and replays without creating another job", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const job = store.get(HandoffJob, jobId);
    expect(job.kind).toBe("Assessment"); expect(job.status).toBe("Commissioned"); expect(job.committedCents).toBe("24500");
    expect(job.requirements).toEqual(["No repairs are authorized."]);
    expect(store.all(HandoffMessage)).toHaveLength(1);
    expect(store.all(HandoffMessage)[0]?.status).toBe("Queued");
    expect(store.all(HandoffPayment)).toHaveLength(0);
    expect((await store.run((context) => commissionJob(context, input))).edits).toEqual([]);
    expect(store.get(HandoffCase, HANDOFF).physicalProgress).toBe("Arranging work");
  });
  it("rejects stale acceptance, changed accepted content and insufficient owner funds", async () => {
    const { store, input, fundingId } = await preparedDelivery();
    await expect(store.run((context) => commissionJob(context, { ...input, expectedRevision: "2" }))).rejects.toThrow(/current accepted/);
    store.change(HandoffDecision, "accepted-1", { contentJson: "{}" });
    await expect(store.run((context) => commissionJob(context, input))).rejects.toThrow(/accepted decision/);
    const ready = await preparedDelivery();
    ready.store.change(HandoffFunding, ready.fundingId, { confirmedCents: "20000" });
    ready.store.change(HandoffDocument, "funding-source", { detailsJson: ready.store.get(HandoffDocument, "funding-source").detailsJson!.replace('"confirmedCents":"100000"', '"confirmedCents":"20000"') });
    await expect(ready.store.run((context) => commissionJob(context, ready.input))).rejects.toThrow(/funds/);
    expect(store.all(HandoffJob)).toHaveLength(0); expect(fundingId).toBeTruthy();
  });
  it("sends a requirement the offer does not state with the order; the provider confirms it once before booking", async () => {
    const { store, input, quoteId } = await preparedDelivery();
    store.change(HandoffQuote, quoteId, { requirements: [] });
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const order = store.all(HandoffMessage)[0]!;
    expect(order.body).toContain("- No repairs are authorized.\nPlease confirm these requirements when you book the visit.\n");
    expect(store.get(HandoffJob, jobId).progressSummary).toMatch(/confirm the requirements/);
    const request = JSON.parse(order.detailsJson!) as Parameters<typeof prepareProviderReply>[0];
    const reply = prepareProviderReply(request, await records(store), LATER);
    expect(reply.confirmedRequirements).toEqual(["No repairs are authorized."]);
    expect(reply.summary).toMatch(/^Confirmed requirements: No repairs are authorized\. /);
    await store.run((context) => respondToProviderRequest(context, order.messageId), LATER);
    const saved = store.all(HandoffMessage).find((message) => message.direction === "Incoming")!;
    expect(saved.body).toContain(reply.summary);
    expect(prepareProviderReply(request, await records(store), LATER).confirmedRequirements).toBeUndefined();
  });
  it("does not restate requirements the offer already confirms", async () => {
    const { store, input } = await preparedDelivery();
    await store.run((context) => commissionJob(context, input));
    const order = store.all(HandoffMessage)[0]!;
    expect(order.body).not.toContain("Please confirm");
    expect(prepareProviderReply(JSON.parse(order.detailsJson!) as Parameters<typeof prepareProviderReply>[0], await records(store), LATER).confirmedRequirements).toBeUndefined();
  });
  it("prevents overlap across differently grouped commands", async () => {
    const { store, input } = await preparedDelivery();
    await store.run((context) => commissionJob(context, { ...input, scope: [input.scope[0]!] }));
    await expect(store.run((context) => commissionJob(context, input))).rejects.toThrow(/already been commissioned/);
  });
  it("denies unauthorized work and crossed funding property", async () => {
    const { store, input, fundingId } = await preparedDelivery();
    store.change(HandoffWorkspace, WORKSPACE, { workUserIds: [] });
    await expect(store.run((context) => commissionJob(context, input))).rejects.toThrow(/permission/);
    store.change(HandoffWorkspace, WORKSPACE, { workUserIds: [PERSON] });
    store.change(HandoffFunding, fundingId, { propertyId: "other-property" });
    await expect(store.run((context) => commissionJob(context, input))).rejects.toThrow(/property/);
  });
  it("recognizes the earlier request and acknowledgment by correlation without recreating or rewriting them", async () => {
    const { store, input } = await preparedDelivery();
    const plan = store.get(HandoffWorkPlan, "plan-1"), provider = store.get(HandoffParty, PROVIDER);
    const correspondence = requestWorkCorrespondence("demo", "continue:accepted-1", provider, planDraft(plan));
    const requestId = reference("message", WORKSPACE, "continue:accepted-1", "request"), replyId = reference("message", WORKSPACE, "continue:accepted-1", "acknowledgement");
    const shared = { workspaceId: WORKSPACE, readerIds: [PERSON], handoffId: HANDOFF, workPlanId: "plan-1", recipientPartyId: PROVIDER,
      createdAt: NOW, externalReference: correspondence.externalReference };
    store.put(HandoffMessage, { ...shared, messageId: requestId, title: correspondence.title, body: correspondence.body, direction: "Outgoing", status: "Sent" });
    store.put(HandoffMessage, { ...shared, messageId: replyId, title: correspondence.replyTitle, body: correspondence.replyBody, direction: "Incoming", status: "Received" });
    const original = orderedJson(store.all(HandoffMessage));
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    expect(store.get(HandoffJob, jobId).requestMessageId).toBe(requestId);
    expect(orderedJson(store.all(HandoffMessage))).toBe(original);
    const { result: followupId } = await store.run((context) => queueProviderRequest(context, { purpose: "Appointment", providerPartyId: PROVIDER,
      quoteId: input.quoteId, scopeLineIds: input.scope.map((line) => line.quoteLineId), jobId, previousReplyId: replyId }));
    await store.run((context) => respondToProviderRequest(context, followupId), LATER);
    expect(store.all(HandoffMessage)).toHaveLength(4);
    expect(orderedJson(store.all(HandoffMessage).filter((message) => [requestId, replyId].includes(message.messageId)))).toBe(original);
    expect(store.get(HandoffMessage, requestId).body).toBe(correspondence.body);
    expect(store.get(HandoffMessage, replyId).body).toBe(correspondence.replyBody);
  });
});

describe("persisted responsive provider correspondence", () => {
  it("answers a saved request in a later invocation and preserves the same reply on retries", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const requestId = store.get(HandoffJob, jobId).requestMessageId!;
    expect(dueProviderRequests(await records(store), NOW)).toEqual([]);
    await expect(store.run((context) => respondToProviderRequest(context, requestId), NOW)).rejects.toThrow(/not due/);
    const { result: response } = await store.run((context) => respondToProviderRequest(context, requestId), LATER);
    expect(response.outcome).toBe("Appointment"); expect(response.appointmentAt).toBe(offer().availableFrom);
    expect(store.get(HandoffJob, jobId).status).toBe("Scheduled");
    expect((await store.run((context) => respondToProviderRequest(context, requestId), COMPLETION)).edits).toEqual([]);
    expect(dueProviderRequests(await records(store), COMPLETION)).toEqual([]);
    expect(store.all(HandoffMessage)).toHaveLength(2);
  });
  it("returns current alternatives rather than accepting new costs or producing a fixed success", async () => {
    const { store, quoteId } = await preparedDelivery();
    store.change(HandoffQuote, quoteId, { status: "Withdrawn" });
    const { result: alternativeId } = await store.run((context) => recordQuote(context, { ...offer(), sourceRecordId: "offer-17-v2", title: "Later availability", availableFrom: "2026-09-30T10:00:00.000Z" }));
    const response = prepareProviderReply({ purpose: "Quote", providerPartyId: PROVIDER, quoteId, scopeLineIds: ["condition"] }, await records(store), NOW);
    expect(response.outcome).toBe("Alternative"); expect(response.quoteIds).toEqual([alternativeId]);
    expect(store.all(HandoffJob)).toHaveLength(0);
  });
  it("requires a settled advance, not a payment request or approved budget", async () => {
    const { store, input } = await preparedDelivery("5000");
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const requestId = store.get(HandoffJob, jobId).requestMessageId!;
    await store.run((context) => requestProviderPayment(context, jobId, "Advance"));
    const response = await store.run((context) => respondToProviderRequest(context, requestId), LATER);
    expect(response.result.outcome).toBe("Advance required");
    expect(store.get(HandoffJob, jobId).appointmentAt).toBeUndefined();
    expect(store.get(HandoffJob, jobId).status).toBe("Awaiting advance");
  });
  it("describes waiting, partial progress and deficiencies from observations without marking the job complete", async () => {
    const { store, input, quoteId } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const request = { purpose: "Progress" as const, providerPartyId: PROVIDER, quoteId, jobId, scopeLineIds: ["condition", "access"] };
    expect(prepareProviderReply(request, await records(store), COMPLETION).outcome).toBe("Waiting");
    const partial = report(jobId); partial.findings = [partial.findings[0]!];
    await store.run((context) => recordInspection(context, partial), COMPLETION);
    expect(prepareProviderReply(request, await records(store), COMPLETION).outcome).toBe("Partial");
    const later = { ...report(jobId), sourceRecordId: "report-2", observedAt: "2026-09-24T12:00:00.000Z" };
    later.findings[1]!.result = "Deficient"; later.findings[1]!.observation = "The requested access test is absent from the report.";
    await store.run((context) => recordInspection(context, later), later.observedAt);
    expect(prepareProviderReply(request, await records(store), later.observedAt).outcome).toBe("Deficiency");
    expect(store.get(HandoffJob, jobId).status).toBe("Commissioned");
  });
  it("queues only one equivalent request and rejects a follow-up to another conversation", async () => {
    const { store, quoteId } = await preparedDelivery();
    const input = { purpose: "Quote" as const, providerPartyId: PROVIDER, quoteId, scopeLineIds: ["condition"] };
    const first = await store.run((context) => queueProviderRequest(context, input));
    expect((await store.run((context) => queueProviderRequest(context, input))).result).toBe(first.result);
    expect(store.all(HandoffMessage)).toHaveLength(1);
    await expect(store.run((context) => queueProviderRequest(context, { ...input, previousReplyId: "foreign" }))).rejects.toThrow(/unavailable/);
  });
});

describe("checks, invoices and payment outcomes", () => {
  it("completes the job from a dated check, never the whole property or tenant account", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    await completeJob(store, jobId);
    expect(store.get(HandoffJob, jobId).status).toBe("Complete");
    expect(store.get(HandoffCase, HANDOFF).physicalProgress).toBe("Arranging work");
    expect(store.all(HandoffInspection)).toHaveLength(1);
    const id = store.all(HandoffInspection)[0]!.inspectionId;
    expect((await store.run((context) => checkJobCompletion(context, jobId, id), COMPLETION)).edits).toEqual([]);
  });
  it("uses a partial check or deficiency honestly and preserves earlier reports", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const partial = report(jobId); partial.findings = [partial.findings[0]!];
    const { result: firstId } = await store.run((context) => recordInspection(context, partial), COMPLETION);
    expect((await store.run((context) => checkJobCompletion(context, jobId, firstId), COMPLETION)).result).toBe("Awaiting check");
    const deficient = { ...report(jobId), sourceRecordId: "report-2", observedAt: "2026-09-24T12:00:00.000Z" };
    deficient.findings[1]!.result = "Deficient";
    const { result: secondId } = await store.run((context) => recordInspection(context, deficient), deficient.observedAt);
    expect((await store.run((context) => checkJobCompletion(context, jobId, secondId), deficient.observedAt)).result).toBe("Needs attention");
    await expect(store.run((context) => checkJobCompletion(context, jobId, firstId), deficient.observedAt)).rejects.toThrow(/older/);
    expect(store.all(HandoffInspection)).toHaveLength(2);
  });
  it("records disputed cost without treating an invoice as performance or tenant liability", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const changed = invoice(jobId); changed.lines = [{ ...changed.lines[0]!, amountCents: "30000" }]; changed.totalCents = "30000";
    const { result: invoiceId } = await store.run((context) => recordInvoice(context, changed), COMPLETION);
    expect(store.get(HandoffInvoice, invoiceId).status).toBe("Disputed");
    expect(store.get(HandoffJob, jobId).status).toBe("Commissioned"); expect(store.all(HandoffPayment)).toHaveLength(0);
    expect((await store.run((context) => recordInvoice(context, changed), COMPLETION)).edits).toEqual([]);
    await expect(store.run((context) => recordInvoice(context, invoice(jobId)), COMPLETION)).rejects.toThrow(/different saved details/);
  });
  it("saves payment intent once, requires correlation, and preserves uncertainty and return", async () => {
    const { store, input, fundingId } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    await completeJob(store, jobId);
    const { result: invoiceId } = await store.run((context) => recordInvoice(context, invoice(jobId)), COMPLETION);
    const { result: paymentId } = await store.run((context) => requestProviderPayment(context, jobId, "Invoice", invoiceId), COMPLETION);
    expect(store.get(HandoffPayment, paymentId).status).toBe("Requested");
    expect((await store.run((context) => requestProviderPayment(context, jobId, "Invoice", invoiceId), COMPLETION)).edits).toEqual([]);
    const result = { instructionKey: paymentId, sourceReference: "confirmation-1", amountCents: "24500", currency: "USD", status: "Confirming" as const, observedAt: COMPLETION, definitive: false };
    await expect(store.run((context) => observeProviderPayment(context, paymentId, { ...result, amountCents: "24501" }), COMPLETION)).rejects.toThrow(/match/);
    await store.run((context) => observeProviderPayment(context, paymentId, result), COMPLETION);
    expect((await loadOwnerFunding(store.context(COMPLETION), fundingId)).position.availableCents).toBe("75500");
    const settledAt = "2026-09-24T12:00:00.000Z";
    await store.run((context) => observeProviderPayment(context, paymentId, { ...result, status: "Settled", sourceReference: "settled-1", observedAt: settledAt, definitive: true }), settledAt);
    await expect(store.run((context) => observeProviderPayment(context, paymentId, { ...result, status: "Failed", observedAt: settledAt, definitive: true }), settledAt)).rejects.toThrow(/conflicting/);
    const returnedAt = "2026-09-24T13:00:00.000Z";
    await store.run((context) => observeProviderPayment(context, paymentId, { ...result, status: "Returned", sourceReference: "return-1", observedAt: returnedAt, definitive: true }), returnedAt);
    expect(store.get(HandoffPayment, paymentId).status).toBe("Returned");
    expect(store.get(HandoffPayment, paymentId).settlementReference).toBe("settled-1");
    expect(store.get(HandoffPayment, paymentId).settledAt).toBe(settledAt);
    expect(store.get(HandoffPayment, paymentId).returnReference).toBe("return-1");
    expect(store.all(HandoffPayment)).toHaveLength(1);
    expect((await loadOwnerFunding(store.context(returnedAt), fundingId)).position.availableCents).toBe("75500");
  });
});
