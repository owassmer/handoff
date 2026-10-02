import { describe, expect, it } from "vitest";
import { HandoffDocument, HandoffDecision, HandoffWorkPlan, HandoffMessage, HandoffParty, HandoffJob } from "@ontology/sdk";
import { recognizeAcceptedWork } from "../acceptedWork.js";
import { loadDeliveryRecords } from "../deliveryRecords.js";
import { loadDetails } from "../workDetails.js";
import { planDraft } from "../workPlans.js";
import { preparedDetails } from "../sourceAccess.js";
import { requestWorkCorrespondence } from "../correspondence.js";
import { reference } from "../values.js";
import { preparedDelivery, WORKSPACE, HANDOFF, PERSON, PROVIDER, NOW } from "./deliverySupport.js";
import { queueProviderRequest, respondToProviderRequest } from "../counterparts.js";

async function setup(): Promise<Awaited<ReturnType<typeof preparedDelivery>>> {
  const prepared = await preparedDelivery(), { store, fundingId } = prepared;
  const plan = store.get(HandoffWorkPlan, "plan-1"), provider = store.get(HandoffParty, PROVIDER);
  const correspondence = requestWorkCorrespondence("demo", "continue:accepted-1", provider, planDraft(plan));
  const common = { workspaceId: WORKSPACE, readerIds: [PERSON], handoffId: HANDOFF, workPlanId: plan.workPlanId,
    recipientPartyId: PROVIDER, createdAt: NOW, externalReference: correspondence.externalReference };
  store.put(HandoffMessage, { ...common, messageId: reference("message", WORKSPACE, "continue:accepted-1", "request"), direction: "Outgoing", status: "Sent", body: correspondence.body });
  store.put(HandoffMessage, { ...common, messageId: reference("message", WORKSPACE, "continue:accepted-1", "acknowledgement"), direction: "Incoming", status: "Received", body: correspondence.replyBody });
  const scope = [
    { quoteLineId: "condition", acceptedScope: plan.scope![0]!, reason: "The offered inspection provides the accepted condition report.", sourcePassage: "Supporting source material." },
    { quoteLineId: "access", acceptedScope: plan.scope![1]!, reason: "The offered door check covers the accepted access test.", sourcePassage: "Supporting source material." },
  ];
  store.put(HandoffDocument, { workspaceId: WORKSPACE, readerIds: [PERSON], handoffId: HANDOFF, documentId: "mapping",
    title: "Earlier accepted assessment", kind: "Accepted work mapping", text: "Mapping of the actual earlier work request.",
    detailsJson: preparedDetails(JSON.stringify({ decisionId: "accepted-1", quoteDocumentId: "quote-source", fundingId, scope }), { id: PERSON, name: "Operator" }) });
  return prepared;
}
async function recognize(prepared: Awaited<ReturnType<typeof preparedDelivery>>): Promise<boolean> {
  const { store } = prepared;
  const result = await store.run(async (context) => recognizeAcceptedWork(context,
    await loadDetails(context.client, context.handoff, context.workspace, context.caller),
    await loadDeliveryRecords(context.client, context.workspace, context.caller, context.handoff)));
  return result.result;
}
describe("recognizing the original accepted Handoff instruction", () => {
  it("continues exactly once under the original decision and request without a new approval or order", async () => {
    const prepared = await setup(), { store } = prepared;
    const capture = store.get(HandoffDecision, "accepted-1").contentJson;
    const originalMessages = store.all(HandoffMessage).map((row) => [row.messageId, row.body]);
    expect(await recognize(prepared)).toBe(true); expect(await recognize(prepared)).toBe(false);
    const job = store.all(HandoffJob)[0]!;
    expect(job).toMatchObject({ origin: "Handoff", decisionId: "accepted-1", requestMessageId: originalMessages[0]![0], committedCents: "24500", status: "Commissioned" });
    expect(store.get(HandoffDecision, "accepted-1").contentJson).toBe(capture);
    expect(store.get(HandoffWorkPlan, "plan-1").selectionJson).toBeUndefined();
    expect(store.all(HandoffDecision)).toHaveLength(1);
    expect(store.all(HandoffMessage).map((row) => [row.messageId, row.body])).toEqual(originalMessages);
    const followup = await store.run((context) => queueProviderRequest(context, { purpose: "Appointment", providerPartyId: PROVIDER, quoteId: prepared.quoteId,
      jobId: job.jobId, scopeLineIds: ["condition", "access"], previousReplyId: reference("message", WORKSPACE, "continue:accepted-1", "acknowledgement") }));
    await store.run((context) => respondToProviderRequest(context, followup.result), "2026-09-23T11:00:00.000Z");
    expect(store.get(HandoffJob, job.jobId).status).toBe("Scheduled");
    expect(store.all(HandoffMessage).filter((message) => message.direction === "Outgoing")).toHaveLength(2);
    expect(store.all(HandoffMessage).filter((message) => originalMessages.some(([id]) => id === message.messageId)).map((row) => [row.messageId, row.body])).toEqual(originalMessages);
  });
  it.each(["request", "acknowledgement"])("rejects a missing or changed original %s rather than silently commissioning", async (suffix) => {
    const prepared = await setup();
    prepared.store.change(HandoffMessage, reference("message", WORKSPACE, "continue:accepted-1", suffix), { body: "An unrelated request or reply" });
    await expect(recognize(prepared)).rejects.toThrow("correspondence");
    expect(prepared.store.all(HandoffJob)).toHaveLength(0);
  });
  it("does not normalize new repairs into the old assessment", async () => {
    const prepared = await setup(); const { HandoffQuote } = await import("@ontology/sdk");
    prepared.store.change(HandoffQuote, prepared.quoteId, { kind: "Repair" });
    await expect(recognize(prepared)).rejects.toThrow("not repairs");
  });
  it("rejects invented evidence or changed accepted captures", async () => {
    const prepared = await setup();
    prepared.store.change(HandoffDocument, "quote-source", { text: "Different evidence" });
    await expect(recognize(prepared)).rejects.toThrow("quoted evidence");
    prepared.store.change(HandoffDocument, "quote-source", { text: "Supporting source material." });
    prepared.store.change(HandoffDecision, "accepted-1", { contentJson: "{}" });
    await expect(recognize(prepared)).rejects.toThrow("unchanged original acceptance");
  });
});
