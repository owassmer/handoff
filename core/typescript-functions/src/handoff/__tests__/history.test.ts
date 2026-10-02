import { beforeEach, describe, expect, it, vi } from "vitest";
import { Admin } from "@osdk/foundry";
import { HandoffMessage, HandoffActivity, HandoffCase, HandoffTenancy, HandoffParty, HandoffAgentWork, HandoffDocument, HandoffDecision } from "@ontology/sdk";
import { preparedDelivery, WORKSPACE, HANDOFF, PERSON, OWNER, PROVIDER, NOW } from "./deliverySupport.js";
import { loadDeliveryRecords } from "../deliveryRecords.js";
import { queueInquiry } from "../inquiries.js";
import { workspaceView } from "../readWorkspace.js";
import { reference } from "../values.js";

vi.mock("@osdk/foundry", () => ({ Admin: { Users: { getCurrent: vi.fn() } } }));
beforeEach(() => {
  vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: PERSON, username: "Operator", attributes: {}, realm: "users", status: "ACTIVE" });
});

describe("growing correspondence history", () => {
  it("retains more than one page of correlations without lifting business-record guards", async () => {
    const { store } = await preparedDelivery();
    for (let i = 0; i < 150; i += 1) store.put(HandoffMessage, { messageId: `history-${i}`, workspaceId: WORKSPACE,
      handoffId: HANDOFF, readerIds: [PERSON], direction: "Incoming", purpose: "Information", status: "Received",
      title: "Earlier correspondence", body: "Earlier information", createdAt: new Date(Date.parse(NOW) + i * 1000).toISOString() });
    const context = store.context();
    const records = await loadDeliveryRecords(context.client, context.workspace, context.caller, context.handoff);
    expect(records.messages).toHaveLength(150);
    expect(store.all(HandoffMessage)).toHaveLength(150);
    store.change(HandoffMessage, "history-0", { readerIds: ["another-user"] });
    await expect(loadDeliveryRecords(context.client, context.workspace, context.caller, context.handoff)).rejects.toThrow(/not available|access settings/);
  });
  it("serves a recent operator window while preserving the full stored history", async () => {
    const { store } = await preparedDelivery();
    store.change(HandoffCase, HANDOFF, { businessDate: "2026-09-23", financialProgress: "Not started", nextStep: "Wait for the provider." });
    store.change(HandoffTenancy, "tenancy-1", { startDate: "2025-01-01" });
    store.change(HandoffDecision, "accepted-1", { title: "Accepted assessment", decidedBy: PERSON, decidedAt: NOW });
    for (const id of [OWNER, PROVIDER]) store.change(HandoffParty, id, { description: "Property contact" });
    store.put(HandoffAgentWork, { workId: reference("work", WORKSPACE, HANDOFF), workspaceId: WORKSPACE, handoffId: HANDOFF, readerIds: [PERSON],
      status: "Waiting for provider", nextStep: "Wait for the provider.", updatedAt: NOW });
    for (let i = 0; i < 150; i += 1) {
      const at = new Date(Date.parse(NOW) + i * 1000).toISOString();
      store.put(HandoffMessage, { messageId: `history-${i}`, workspaceId: WORKSPACE, handoffId: HANDOFF, readerIds: [PERSON],
        direction: "Incoming", purpose: "Information", status: "Received", title: "Earlier correspondence", body: "Earlier information", createdAt: at });
      store.put(HandoffActivity, { activityId: `history-${i}`, workspaceId: WORKSPACE, handoffId: HANDOFF, readerIds: [PERSON],
        title: "Earlier progress", occurredAt: at, detail: JSON.stringify({ version: "1", payloadHash: "history", summary: "Earlier progress" }) });
    }
    const view = await workspaceView(store.client, HANDOFF);
    expect(view.messages).toHaveLength(50);
    expect(view.messages[0]?.id).toBe("history-100");
    expect(view.activity).toHaveLength(100);
    expect(view.activity[0]?.id).toBe("history-50");
    expect(store.all(HandoffMessage)).toHaveLength(150);
    expect(store.all(HandoffActivity)).toHaveLength(150);
  });
  it("coalesces paraphrases but permits a request after the source facts change", async () => {
    const { store } = await preparedDelivery();
    const context = store.context();
    const first = await queueInquiry(context, { purpose: "Information", recipientPartyId: OWNER, question: "Who provides access?" });
    const sameBatch = await queueInquiry(context, { purpose: "Information", recipientPartyId: OWNER, question: "Please confirm the access contact." });
    expect(sameBatch).toBe(first);
    expect(context.batch.getEdits().filter((edit) => edit.type === "createObject" && edit.obj.apiName === "HandoffMessage")).toHaveLength(1);
    store.apply(context.batch.getEdits());
    const replay = store.context();
    expect(await queueInquiry(replay, { purpose: "Information", recipientPartyId: OWNER, question: "Please supply access arrangements." })).toBe(first);
    expect(replay.batch.getEdits()).toEqual([]);
    store.change(HandoffDocument, "historic-source", { text: "The owner has supplied new access arrangements.", sourceVersion: "2" });
    expect(await queueInquiry(store.context(), { purpose: "Information", recipientPartyId: OWNER, question: "Please confirm access." })).not.toBe(first);
  });
  it("does not turn an unchanged unanswered reply into another automatic send", async () => {
    const { store } = await preparedDelivery();
    const context = store.context();
    const first = await queueInquiry(context, { purpose: "Information", recipientPartyId: PROVIDER, question: "Please provide your access requirements." });
    store.apply(context.batch.getEdits());
    store.put(HandoffMessage, { messageId: "no-new-information", workspaceId: WORKSPACE, handoffId: HANDOFF, readerIds: [PERSON],
      direction: "Incoming", senderPartyId: PROVIDER, replyToMessageId: first, body: "No new information yet." });
    const followup = store.context();
    const reminder = await queueInquiry(followup, { purpose: "Information", recipientPartyId: PROVIDER, question: "Following up on access.", previousReplyId: "no-new-information" });
    expect(reminder).not.toBe(first);
    store.apply(followup.batch.getEdits());
    store.put(HandoffMessage, { messageId: "still-no-new-information", workspaceId: WORKSPACE, handoffId: HANDOFF, readerIds: [PERSON],
      direction: "Incoming", senderPartyId: PROVIDER, replyToMessageId: reminder, body: "Still no new information." });
    const repeated = store.context();
    expect(await queueInquiry(repeated, { purpose: "Information", recipientPartyId: PROVIDER, question: "Checking again.", previousReplyId: "still-no-new-information" })).toBe(reminder);
    expect(repeated.batch.getEdits()).toEqual([]);
  });
});
