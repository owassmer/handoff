import { describe, expect, it } from "vitest";
import { HandoffCase, HandoffDocument, HandoffInspection, HandoffJob, HandoffMessage, HandoffPayment } from "@ontology/sdk";
import { commissionJob } from "../delivery.js";
import { loadDeliveryRecords, recordInspection, recordQuote } from "../deliveryRecords.js";
import { prepareProviderReply, queueProviderRequest, respondToProviderRequest } from "../counterparts.js";
import { observeProviderPayment, requestProviderPayment } from "../funding.js";
import { HANDOFF, LATER, NOW, PERSON, PROVIDER, WORKSPACE, offer, preparedDelivery } from "./deliverySupport.js";
import { orderedJson } from "../values.js";

describe("delivery recovery and adverse calls", () => {
  it("rechecks a pause even when the caller initially loaded an open handoff", async () => {
    const { store, input } = await preparedDelivery();
    const context = store.context();
    store.change(HandoffCase, HANDOFF, { status: "Paused" });
    await expect(commissionJob(context, input)).rejects.toThrow(/current accepted/);
    expect(store.all(HandoffJob)).toHaveLength(0);
  });
  it("deduplicates a source ingested twice in one shared batch", async () => {
    const { store } = await preparedDelivery();
    const context = store.context(), input = { ...offer(), sourceRecordId: "another-offer" };
    const first = await recordQuote(context, input), second = await recordQuote(context, input);
    expect(first).toBe(second);
    expect(context.batch.getEdits().filter((edit) => edit.type === "createObject")).toHaveLength(1);
    store.apply(context.batch.getEdits());
  });
  it("rejects conflicting ingestions inside the same batch", async () => {
    const { store } = await preparedDelivery();
    const context = store.context(), input = { ...offer(), sourceRecordId: "another-offer" };
    await recordQuote(context, input);
    await expect(recordQuote(context, { ...input, title: "Another service" })).rejects.toThrow(/different saved/);
  });
  it("does not make two commitments against invisible in-flight balances", async () => {
    const { store, input } = await preparedDelivery();
    const context = store.context();
    await commissionJob(context, { ...input, scope: [input.scope[0]!] });
    await expect(commissionJob(context, { ...input, scope: [input.scope[1]!] })).rejects.toThrow(/Save the earlier/);
    expect(store.all(HandoffJob)).toHaveLength(0);
  });
  it("will not answer a request that has not been committed", async () => {
    const { store, input } = await preparedDelivery();
    const context = store.context();
    await commissionJob(context, input);
    const create = context.batch.getEdits().find((edit) => edit.type === "createObject" && edit.obj.apiName === "HandoffMessage");
    if (!create || create.type !== "createObject") throw new Error("Missing request in edit batch");
    const id = String(Reflect.get(create.properties, "messageId"));
    await expect(respondToProviderRequest({ ...context, now: LATER }, id)).rejects.toThrow(/saved provider request/);
    expect(store.all(HandoffMessage)).toHaveLength(0);
  });
  it("uses the commissioning request for an initial appointment tool call", async () => {
    const { store, input, quoteId } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const original = store.get(HandoffJob, jobId).requestMessageId;
    const { result: id, edits } = await store.run((context) => queueProviderRequest(context,
      { purpose: "Appointment", providerPartyId: PROVIDER, quoteId, jobId, scopeLineIds: ["condition", "access"] }));
    expect(id).toBe(original); expect(edits).toEqual([]); expect(store.all(HandoffMessage)).toHaveLength(1);
  });
  it("deduplicates repeated provider replies within one batch", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const context = store.context(LATER), id = store.get(HandoffJob, jobId).requestMessageId!;
    const first = await respondToProviderRequest(context, id), second = await respondToProviderRequest(context, id);
    expect(second).toEqual(first);
    expect(context.batch.getEdits().filter((edit) => edit.type === "createObject")).toHaveLength(1);
  });
  it("does not hide simultaneous contradictory observations behind record order", async () => {
    const { store, input, quoteId } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const shared = { workspaceId: WORKSPACE, readerIds: [PERSON], handoffId: HANDOFF, propertyId: "property-1", jobId,
      observerPartyId: PROVIDER, sourceDocumentId: "report-source", observedAt: LATER, purpose: "Completion check" };
    const findings = offer().lines.map((line) => ({ lineId: line.lineId, result: "Satisfied", observation: "Report supplied", method: "Document review" }));
    store.put(HandoffInspection, { ...shared, inspectionId: "a", findingsJson: orderedJson(findings) });
    findings[0]!.result = "Deficient";
    store.put(HandoffInspection, { ...shared, inspectionId: "z", findingsJson: orderedJson(findings) });
    const context = store.context(LATER), records = await loadDeliveryRecords(context.client, context.workspace, context.caller, context.handoff);
    const response = prepareProviderReply({ purpose: "Progress", providerPartyId: PROVIDER, quoteId, jobId, scopeLineIds: ["condition", "access"] }, records, LATER);
    expect(response.outcome).toBe("Deficiency"); expect(response.inspectionIds.sort()).toEqual(["a", "z"]);
  });
  it("does not lose an uncertain payment on a nondefinitive negative lookup", async () => {
    const { store, input } = await preparedDelivery("5000");
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const { result: paymentId } = await store.run((context) => requestProviderPayment(context, jobId, "Advance"));
    const observation = { instructionKey: paymentId, sourceReference: "lookup", amountCents: "5000", currency: "USD",
      status: "Confirming" as const, observedAt: NOW, definitive: false };
    await store.run((context) => observeProviderPayment(context, paymentId, observation));
    await expect(store.run((context) => observeProviderPayment(context, paymentId,
      { ...observation, status: "Failed", observedAt: LATER }), LATER)).rejects.toThrow(/definitive/);
    expect(store.get(HandoffPayment, paymentId).status).toBe("Confirming");
    expect((await store.run((context) => requestProviderPayment(context, jobId, "Advance"), LATER)).edits).toEqual([]);
  });
  it("cannot count one external settlement under two logical payments", async () => {
    const { store, input } = await preparedDelivery("5000");
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const { result: paymentId } = await store.run((context) => requestProviderPayment(context, jobId, "Advance"));
    const original = store.get(HandoffPayment, paymentId);
    store.put(HandoffPayment, { ...original, paymentId: "another-payment", instructionKey: "another-payment",
      status: "Settled", amountCents: "1000", sourceReference: "other-current", settlementReference: "shared-settlement", settledAt: NOW });
    await expect(store.run((context) => observeProviderPayment(context, paymentId, { instructionKey: paymentId,
      sourceReference: "shared-settlement", amountCents: "5000", currency: "USD", status: "Settled", definitive: true, observedAt: LATER }), LATER)).rejects.toThrow(/another payment/);
    expect(store.get(HandoffPayment, paymentId).status).toBe("Requested");
  });
  it("requires provider, source access and nonfuture time for an actual report", async () => {
    const { store, input } = await preparedDelivery();
    const { result: jobId } = await store.run((context) => commissionJob(context, input));
    const report = { sourceSystem: "provider", sourceRecordId: "inspection-1", sourceDocumentId: "report-source",
      title: "Assessment result", observerPartyId: PROVIDER, jobId, observedAt: LATER, purpose: "Completion check" as const,
      findings: [{ lineId: "not-agreed", result: "Satisfied" as const, observation: "Unrequested work", method: "Visual check" }] };
    await expect(store.run((context) => recordInspection(context, report), LATER)).rejects.toThrow(/outside this job/);
    store.change(HandoffDocument, "report-source", { readerIds: ["other-user"] });
    await expect(store.run((context) => recordInspection(context, { ...report, findings: [{ ...report.findings[0]!, lineId: "condition" }] }), LATER)).rejects.toThrow(/not available/);
  });
});
