import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Admin } from "@osdk/foundry";
import { Aliases } from "@osdk/functions";
import { HandoffActivity, HandoffCase, HandoffDocument, HandoffFunding, HandoffJob, HandoffInspection, HandoffInvoice, HandoffMessage, HandoffPayment,
  HandoffQuote, HandoffWorkPlan, HandoffWorkspace, HandoffDecision, HandoffAgentWork } from "@ontology/sdk";
import type { ChatCompletion, ChatCompletionCreateParamsNonStreaming } from "openai/resources/chat/completions";
import type { WorkModel } from "../reasoner.js";
import type { QuoteLine } from "../deliveryContracts.js";
import type { WorkSelection } from "../proposal.js";
import type { ProviderService } from "../supportingSources.js";
import { preparedDetails } from "../sourceAccess.js";
import { performService } from "../providerDelivery.js";
import { coordinateHandoff } from "../coordinator.js";
import { acceptedContent, changePlan, readAcceptedContent } from "../workPlans.js";
import { readMoveOutNotice } from "../notice.js";
import { readInquiry } from "../coordinateReasoning.js";
import { queueInquiry } from "../inquiries.js";
import * as reasoner from "../reasoner.js";
import createHandoffWorkspace from "../../functions/createHandoffWorkspace.js";
import receiveMoveOutNotice from "../../functions/receiveMoveOutNotice.js";
import continueHandoff from "../../functions/continueHandoff.js";
import acceptHandoffWorkPlan from "../../functions/acceptHandoffWorkPlan.js";
import sendHandoffMessage from "../../functions/sendHandoffMessage.js";
import getHandoffWorkspace from "../../functions/getHandoffWorkspace.js";
import getHandoffChange from "../../functions/getHandoffChange.js";
import { WorkspaceStore, PERSON, MODEL, WORKSPACE, HANDOFF, notice, sourceId } from "./workspaceSupport.js";
import type { HandoffWorkspaceView } from "../contracts.js";
import { digest } from "../values.js";
import { formatAmount } from "../deliveryContracts.js";
import { caseTime } from "../clock.js";

vi.mock("@osdk/foundry", () => ({ Admin: { Users: { getCurrent: vi.fn() } } }));
vi.mock("@osdk/functions", async (original) => {
  const actual = await original<typeof import("@osdk/functions")>();
  return { ...actual, Aliases: { ...actual.Aliases, model: vi.fn() } };
});
const NOW = "2026-09-23T10:00:00.000Z";
beforeEach(() => {
  vi.useFakeTimers(); vi.setSystemTime(NOW);
  vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: PERSON, username: "morgan", attributes: {}, realm: "users", status: "ACTIVE" });
  vi.mocked(Aliases.model).mockReturnValue({ rid: MODEL });
});
afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks(); });
function service(kind: ProviderService["kind"] = "Repair"): ProviderService {
  return { serviceId: "entrance", title: "Make the entrance secure", kind, currency: "USD",
    lines: [{ lineId: "latch", description: "Adjust and function-check entrance latch", amountCents: "12500" }],
    depositCents: "2500", paymentTerms: "Advance of 2500; balance after completion", requirements: [],
    availableFrom: NOW, validUntil: "2026-10-01T00:00:00.000Z", durationMinutes: 2, responseMinutes: 1,
    effects: [{ lineId: "latch", conditionIds: ["entrance"], method: "Operate the latch and check that the door secures." }] };
}
async function setup(options: { kind?: ProviderService["kind"]; repairable?: boolean; accessible?: boolean; payment?: "Settle" | "Reject" | "Uncertain"; funds?: string; requirements?: string[] } = {}): Promise<WorkspaceStore> {
  const store = new WorkspaceStore();
  store.apply(await createHandoffWorkspace(store.client, "Meadow homes", "open-workspace", PERSON));
  const input = notice(); input.businessDate = "2026-09-23"; input.goal = "A secure entrance.";
  if (options.requirements) input.fixedRequirements = options.requirements;
  input.documents = [input.documents[0]!,
    { sourceId: "services", title: "House Care services", kind: "Provider information", partySourceId: "provider", sourceKind: "Prepared", sourceVersion: "1",
      text: "House Care adjusts and checks entrance latches. Advance payment is required.", detailsJson: JSON.stringify({ services: [service(options.kind)] }) },
    { sourceId: "condition", title: "Entrance condition", kind: "Property condition", partySourceId: "owner", sourceKind: "Prepared", sourceVersion: "1",
      text: "The entrance latch does not catch reliably.", detailsJson: JSON.stringify({ coverage: { goal: input.goal, conditionIds: ["entrance"], reason: "The handoff concerns only the entrance latch, checked by operation." }, conditions: [{ conditionId: "entrance", description: "Entrance latch",
        state: "Deficient", repairable: options.repairable ?? true, accessible: options.accessible ?? true }] }) },
    { sourceId: "funds", title: "Owner funding confirmation", kind: "Owner funding", partySourceId: "owner", sourceKind: "Prepared", sourceVersion: "1",
      text: "Owner funds are confirmed for property work.", detailsJson: JSON.stringify({ ownerPartyId: sourceId("party", "owner"), currency: "USD",
        confirmedCents: options.funds ?? "30000", confirmedAt: NOW, paymentBehavior: options.payment ?? "Settle", responseMinutes: 1 }) },
  ];
  store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(input), "notice", PERSON));
  return store;
}
interface ModelContext {
  currency: string; fixedRequirements: string[];
  documents: Array<{ id: string; kind: string }>;
  services: Array<{ documentId: string; providerPartyId: string; serviceId: string }>;
  quotes: Array<{ id: string; kind: string; sourceDocumentId: string; providerPartyId: string; lines: QuoteLine[] }>;
  currentProposal: { status: string; budgetCents: string } | null;
  jobs: Array<{ status: string }>;
  messages: Array<{ direction: string; body: string }>;
}
/** Test model exercises real typed tools; counterpart behavior is never supplied by this mock. */
function model(onFinal?: () => void, change?: (result: Record<string, unknown>) => void): WorkModel {
  return { model: MODEL, complete: async (request: ChatCompletionCreateParamsNonStreaming): Promise<Pick<ChatCompletion, "choices">> => {
    const input = JSON.parse(String(request.messages.find((message) => message.role === "user")!.content)) as ModelContext;
    const tools = request.messages.filter((message) => message.role === "tool");
    const quote = input.quotes[0];
    const selection: WorkSelection[] = quote ? quote.lines.map((line) => ({ quoteId: quote.id, quoteLineId: line.lineId,
      scope: "Make the entrance secure.", reason: "Adjustment and function checking address the latch condition without replacement." })) : [];
    const isDiscussion = input.messages.at(-1)?.direction === "Operator";
    const propose = quote && (!input.currentProposal || isDiscussion);
    const tool = (name: string, args: unknown): Pick<ChatCompletion, "choices"> => ({ choices: [{ index: 0, logprobs: null, finish_reason: "tool_calls",
      message: { role: "assistant", content: null, refusal: null, tool_calls: [{ id: `tool-${tools.length}`, type: "function", function: { name, arguments: JSON.stringify(args) } }] } }] });
    if (!tools.length) return tool("readDocuments", { ids: input.documents.map((doc) => doc.id).slice(-16) });
    if (propose && tools.length === 1) return tool("quoteCosts", { selections: selection });
    const result: Record<string, unknown> = { summary: "Handoff has considered the current work.", proposal: propose ? {
      title: "Secure the entrance", summary: "Adjust the latch and check its operation.", desiredOutcome: "A secure entrance.",
      estimatedCostCents: "12500", budgetCents: isDiscussion ? "17000" : "15000", currency: input.currency, fixedRequirements: input.fixedRequirements,
      rationale: "The condition and quoted adjustment support targeted work rather than replacement.", sourceDocumentIds: input.documents.map((doc) => doc.id),
      providerPartyId: quote!.providerPartyId, selections: selection, fixedProviderPartyId: null,
    } : null, requests: !quote ? [{ purpose: "Quote", recipientPartyId: input.services[0]!.providerPartyId,
      question: "Please quote to adjust and check the entrance latch.", providerDocumentId: input.services[0]!.documentId, serviceId: input.services[0]!.serviceId }] : [],
      propertyReady: false };
    onFinal?.(); change?.(result);
    return { choices: [{ index: 0, logprobs: null, finish_reason: "stop", message: { role: "assistant", refusal: null, content: JSON.stringify(result) } }] };
  } };
}
let turn = 0;
async function run(store: WorkspaceStore, useModel: WorkModel = model()): Promise<void> {
  turn += 1;
  store.apply(await coordinateHandoff(store.client, HANDOFF, `turn-${turn}`, PERSON, { model: useModel }));
}
async function offered(store: WorkspaceStore): Promise<string> {
  await run(store);
  expect(store.all(HandoffQuote)).toHaveLength(0);
  vi.advanceTimersByTime(61000); await run(store);
  expect(store.all(HandoffQuote)).toHaveLength(1);
  await run(store);
  return store.get(HandoffCase, HANDOFF).workPlanId!;
}
async function accepted(store: WorkspaceStore): Promise<string> {
  const id = await offered(store);
  store.apply(await acceptHandoffWorkPlan(store.client, id, "1", "accept", PERSON));
  return id;
}
async function deliver(store: WorkspaceStore): Promise<void> {
  for (let step = 0; step < 18; step += 1) { vi.advanceTimersByTime(61000); await run(store); }
}

describe("SDK timestamp representations through the coordinator", () => {
  it("completes the minimal flow with whole-second wire values, keeping accepted contents and source versions intact", async () => {
    const store = await setup(); await accepted(store);
    const decision = store.all(HandoffDecision)[0]!.contentJson;
    const source = store.get(HandoffDocument, sourceId("document", "services"));
    const sourceBody = source.detailsJson, sourceVersion = source.sourceVersion;
    const wire = (time?: string): string | undefined => time?.replace(/\.000Z$/, "Z");
    // Simulate only the typed properties a real persistence/OSDK round trip can reformat.
    // Source JSON, accepted capture, identity strings and date-only availableFrom are not changed.
    for (let step = 0; step < 22; step += 1) {
      store.all(HandoffFunding).forEach((row) => store.change(HandoffFunding, row.fundingId, { confirmedAt: wire(row.confirmedAt) }));
      store.all(HandoffQuote).forEach((row) => store.change(HandoffQuote, row.quoteId, { availableFrom: wire(row.availableFrom), validUntil: wire(row.validUntil) }));
      store.all(HandoffMessage).forEach((row) => store.change(HandoffMessage, row.messageId, { createdAt: wire(row.createdAt), responseDueAt: wire(row.responseDueAt) }));
      store.all(HandoffJob).forEach((row) => store.change(HandoffJob, row.jobId, { createdAt: wire(row.createdAt), updatedAt: wire(row.updatedAt), appointmentAt: wire(row.appointmentAt), appointmentEndsAt: wire(row.appointmentEndsAt), nextResponseAt: wire(row.nextResponseAt) }));
      store.all(HandoffPayment).forEach((row) => store.change(HandoffPayment, row.paymentId, { requestedAt: wire(row.requestedAt), observedAt: wire(row.observedAt), settledAt: wire(row.settledAt) }));
      store.all(HandoffInspection).forEach((row) => store.change(HandoffInspection, row.inspectionId, { observedAt: wire(row.observedAt) }));
      store.all(HandoffInvoice).forEach((row) => store.change(HandoffInvoice, row.invoiceId, { issuedAt: wire(row.issuedAt), dueAt: wire(row.dueAt) }));
      store.all(HandoffAgentWork).forEach((row) => store.change(HandoffAgentWork, row.workId, { businessTime: wire(row.businessTime), nextBusinessAt: wire(row.nextBusinessAt), nextWakeAt: wire(row.nextWakeAt), updatedAt: wire(row.updatedAt) }));
      vi.advanceTimersByTime(61000); await run(store);
    }
    expect(store.all(HandoffJob)).toHaveLength(1);
    expect(store.all(HandoffJob)[0]).toMatchObject({ status: "Complete", committedCents: "12500", depositCents: "2500" });
    expect(store.all(HandoffInspection)).toHaveLength(1);
    expect(store.all(HandoffInvoice)).toHaveLength(1);
    expect(store.all(HandoffPayment).map((row) => [row.purpose, row.status, row.amountCents])).toEqual([["Advance", "Settled", "2500"], ["Invoice", "Settled", "10000"]]);
    expect(store.all(HandoffDecision)[0]!.contentJson).toBe(decision);
    expect(store.get(HandoffDocument, source.documentId)).toMatchObject({ detailsJson: sourceBody, sourceVersion });
  });
  it("answers a whole-second inquiry exactly when its wake and reply become due", async () => {
    const store = await setup(); await run(store);
    const request = store.all(HandoffMessage)[0]!, work = store.all(HandoffAgentWork)[0]!;
    const due = request.responseDueAt!, wireDue = due.replace(/\.000Z$/, "Z");
    expect(due).not.toBe(wireDue);
    store.change(HandoffMessage, request.messageId, { responseDueAt: wireDue });
    store.change(HandoffAgentWork, work.workId, { businessTime: due, nextBusinessAt: wireDue, nextWakeAt: wireDue });
    vi.setSystemTime(due); await run(store);
    expect(store.all(HandoffQuote)).toHaveLength(1);
    expect(store.all(HandoffMessage)).toHaveLength(2);
  });
  it("delivers a scheduled report and invoice exactly at a persisted whole-second appointment end", async () => {
    const store = await setup(); await accepted(store);
    for (let step = 0; step < 12 && !store.all(HandoffJob).some((job) => job.status === "Scheduled"); step += 1) {
      vi.advanceTimersByTime(61000); await run(store);
    }
    const job = store.all(HandoffJob)[0]!, work = store.all(HandoffAgentWork)[0]!;
    expect(job.status).toBe("Scheduled");
    const end = job.appointmentEndsAt!, wireEnd = end.replace(/\.000Z$/, "Z");
    expect(end).not.toBe(wireEnd);
    store.change(HandoffJob, job.jobId, { appointmentEndsAt: wireEnd });
    store.change(HandoffAgentWork, work.workId, { status: "Ready to continue", businessTime: end, nextBusinessAt: undefined, nextWakeAt: undefined });
    expect(store.all(HandoffInspection)).toHaveLength(0);
    await run(store);
    expect(store.all(HandoffInspection)).toHaveLength(1);
    expect(store.all(HandoffInspection)[0]!.observedAt).toBe(end);
    expect(store.all(HandoffInvoice)).toHaveLength(1);
    expect(store.all(HandoffInvoice)[0]!.issuedAt).toBe(end);
  });
  it("does not treat whole-second formatting during a reasoning save check as a concurrent update", async () => {
    const store = await setup(), work = store.all(HandoffAgentWork)[0]!;
    await run(store, model(() => store.change(HandoffAgentWork, work.workId, { updatedAt: "2026-09-23T10:00:00Z" })));
    expect(store.all(HandoffMessage)).toHaveLength(1);
  });
  it("still rejects an actual 1ms concurrent work update during reasoning", async () => {
    const store = await setup(), work = store.all(HandoffAgentWork)[0]!;
    await expect(run(store, model(() => store.change(HandoffAgentWork, work.workId, { updatedAt: "2026-09-23T10:00:00.001Z" })))).rejects.toThrow(/changed while/);
    expect(store.all(HandoffMessage)).toHaveLength(0);
  });
});

describe("connected Handoff coordination", () => {
  it("investigates without an existing offer, saves a reviewed plan, accepts, funds, commissions, obtains reports and pays confirmed results", async () => {
    const store = await setup(); const id = await offered(store);
    const plan = store.get(HandoffWorkPlan, id);
    expect(plan.selectionJson).toContain("Adjustment and function checking");
    expect(plan.sourceBasis).toMatch(/^[a-f0-9]{64}$/);
    expect(store.all(HandoffJob)).toHaveLength(0);
    store.apply(await changePlan(store.client, id, "1", "16000", "budget", PERSON));
    store.apply(await acceptHandoffWorkPlan(store.client, id, "2", "accept", PERSON));
    expect(readAcceptedContent(store.all(HandoffDecision)[0]!.contentJson!).budgetCents).toBe("16000");
    await deliver(store);
    expect(store.all(HandoffJob)).toHaveLength(1);
    expect(store.all(HandoffJob)[0]).toMatchObject({ status: "Complete", committedCents: "12500", depositCents: "2500" });
    expect(store.all(HandoffInspection)).toHaveLength(1);
    expect(store.all(HandoffInvoice)).toHaveLength(1);
    expect(store.all(HandoffPayment).map((payment) => [payment.purpose, payment.status, payment.amountCents])).toEqual([
      ["Advance", "Settled", "2500"], ["Invoice", "Settled", "10000"],
    ]);
    const original = store.get(HandoffDocument, sourceId("document", "condition"));
    expect(original.detailsJson).toContain("Deficient");
    expect(store.all(HandoffDocument).filter((doc) => doc.kind === "Property condition")).toHaveLength(2);
    const view = JSON.parse(await getHandoffWorkspace(store.client, HANDOFF)) as HandoffWorkspaceView;
    expect(view.version).toBe("2"); expect(view.jobs[0]?.status).toBe("Complete");
    expect(view.funding[0]).toMatchObject({ availableCents: "17500", committedOrSpentCents: "12500" });
    expect(view.decisions[0]?.content).toMatchObject({ budgetCents: "16000", status: "Accepted" });
    expect(view.handoff.financialProgress).toBe("Not started");
    const booking = store.all(HandoffMessage).find((message) => message.direction === "Outgoing" && message.title === "Booking: Make the entrance secure")!;
    expect(booking.body).toContain("The advance is paid. Please book the visit for make the entrance secure");
    const report = store.all(HandoffMessage).find((message) => message.title === "Report and invoice: Make the entrance secure")!;
    expect(report.body).toMatch(/^Hello,\n\nWe've finished the make the entrance secure on .+\. Our report and invoice are attached\.\n\nBest,\nHouse Care$/);
    expect(JSON.parse(report.detailsJson!).attachments).toHaveLength(2);
    expect(view.messages.find((message) => message.id === report.messageId)?.attachmentDocumentIds).toHaveLength(2);
    const activity = JSON.stringify(store.all(HandoffActivity));
    ["Ordered Make the entrance secure from House Care for $125.00.", "Requested the $25.00 advance for House Care.", "Paid House Care's $25.00 advance.",
      "Requested payment of House Care's invoice.", "Paid House Care $100.00 on its invoice.", "Checked House Care's report. The work is complete."]
      .forEach((sentence) => expect(activity).toContain(sentence));
    expect(activity).not.toMatch(/payment service|correspondent has replied|commissioned within/);
  });
  it("stamps messages, replies and decisions on one case clock that runs ahead of real time", async () => {
    expect(caseTime({ businessTime: "2026-09-30T13:00:00.000Z", updatedAt: NOW }, "2026-09-23T10:00:05.000Z")).toBe("2026-09-30T13:00:05.000Z");
    expect(caseTime(undefined, NOW)).toBe(NOW);
    const store = await setup(); const id = await offered(store);
    const work = store.all(HandoffAgentWork)[0]!;
    store.change(HandoffAgentWork, work.workId, { businessTime: "2026-09-30T13:00:00.000Z", updatedAt: new Date().toISOString() });
    vi.advanceTimersByTime(5000);
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Please keep the existing latch if you can.", "case-clock", PERSON));
    const sent = store.all(HandoffMessage).find((message) => message.direction === "Operator")!;
    expect(sent.createdAt).toBe("2026-09-30T13:00:05.000Z");
    await run(store);
    const replies = store.all(HandoffActivity).filter((row) => ["Handoff next step", "Work plan ready", "Handoff progressed"].includes(row.title ?? "")
      && (row.occurredAt ?? "") >= sent.createdAt!);
    expect(replies.length).toBeGreaterThan(0);
    const plan = store.get(HandoffCase, HANDOFF).workPlanId!;
    store.apply(await acceptHandoffWorkPlan(store.client, plan, store.get(HandoffWorkPlan, plan).revision!, "accept-on-case-clock", PERSON));
    expect(store.all(HandoffDecision)[0]!.decidedAt! >= sent.createdAt!).toBe(true);
    expect(store.all(HandoffDecision)[0]!.decidedAt!.startsWith("2026-09-30")).toBe(true);
    expect(id).toBeTruthy();
  });
  it("uses the public continuation wrapper and one model for operator conversation and timer work", async () => {
    const store = await setup(); const id = await offered(store);
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Use a budget of 17000 cents and retain the same work.", "discussion", PERSON, "1"));
    const factory = vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(model());
    store.apply(await continueHandoff(store.client, HANDOFF, "resume-conversation", PERSON));
    expect(factory).toHaveBeenCalledOnce();
    expect(store.get(HandoffWorkPlan, id)).toMatchObject({ budgetCents: "17000", revision: "2" });
    const asked = store.all(HandoffMessage).find((message) => message.direction === "Operator")!;
    const replies = store.all(HandoffMessage).filter((message) => message.direction === "Handoff");
    expect(replies).toHaveLength(1);
    expect(replies[0]).toMatchObject({ replyToMessageId: asked.messageId, body: store.all(HandoffAgentWork)[0]!.nextStep });
    store.apply(await continueHandoff(store.client, HANDOFF, "resume-again", PERSON));
    expect(store.all(HandoffMessage).filter((message) => message.direction === "Handoff")).toHaveLength(1);
    expect(store.all(HandoffDecision)).toHaveLength(0);
    const receipt = JSON.parse(await getHandoffChange(store.client, HANDOFF, "discussion")) as { kind: string; payloadHash: string };
    expect(receipt).toMatchObject({ kind: "Message sent", payloadHash: digest({ handoffId: HANDOFF, message: "Use a budget of 17000 cents and retain the same work.", expectedPlanRevision: "1" }) });
    expect(await sendHandoffMessage(store.client, HANDOFF, "Use a budget of 17000 cents and retain the same work.", "discussion", PERSON, "1")).toEqual([]);
  });
  it("preserves accepted contents and receipt identity after a later draft", async () => {
    const store = await setup(); const id = await accepted(store), content = store.all(HandoffDecision)[0]!.contentJson;
    store.apply(await changePlan(store.client, id, "1", "17000", "later-budget", PERSON));
    expect(store.get(HandoffCase, HANDOFF).workPlanId).not.toBe(id);
    expect(store.get(HandoffCase, HANDOFF).operativeDecisionId).toBe(store.all(HandoffDecision)[0]!.decisionId);
    expect(store.get(HandoffWorkPlan, id).status).toBe("Accepted"); expect(store.all(HandoffDecision)[0]!.contentJson).toBe(content);
    expect(await acceptHandoffWorkPlan(store.client, id, "1", "accept", PERSON)).toEqual([]);
    expect(JSON.parse(await getHandoffChange(store.client, HANDOFF, "accept"))).toMatchObject({ status: "Saved", subjectId: id });
    expect(readAcceptedContent(content!).version).toBe("2");
  });
  it.each(["Reject", "Uncertain"] as const)("does not manufacture settlement or resend a %s payment", async (payment) => {
    const store = await setup({ payment }); await accepted(store); await deliver(store);
    expect(store.all(HandoffPayment)).toHaveLength(1);
    expect(store.all(HandoffPayment)[0]?.status).toBe(payment === "Reject" ? "Failed" : "Confirming");
    expect(store.all(HandoffJob)[0]?.status).toBe("Awaiting advance");
    expect(store.all(HandoffInspection)).toHaveLength(0);
    const funding = store.all(HandoffFunding)[0]!;
    expect(funding.confirmedCents).toBe("30000");
  });
  it("does not pretend a budget is available funds, and says why the accepted work waits", async () => {
    const store = await setup({ funds: "2000" }); await accepted(store); await deliver(store);
    expect(store.all(HandoffJob)).toHaveLength(0); expect(store.all(HandoffPayment)).toHaveLength(0);
    expect(store.all(HandoffFunding)[0]?.confirmedCents).toBe("2000");
    expect(store.all(HandoffAgentWork)[0]).toMatchObject({ status: "Needs attention",
      nextStep: "The accepted work can't be ordered yet. The confirmed owner funds don't cover the $125.00 order for House Care." });
    expect(store.get(HandoffCase, HANDOFF).nextStep).toBe(store.all(HandoffAgentWork)[0]!.nextStep);
  });
  it("orders accepted work with a requirement the offer does not state, and the vendor confirms it before booking", async () => {
    const requirement = "Keep the existing entrance door.";
    const store = await setup({ requirements: [requirement] }); await accepted(store); await deliver(store);
    expect(store.all(HandoffJob)).toHaveLength(1);
    expect(store.all(HandoffJob)[0]).toMatchObject({ status: "Complete", requirements: [requirement] });
    const order = store.all(HandoffMessage).find((message) => message.direction === "Outgoing" && message.purpose === "Appointment" && message.jobId)!;
    expect(order.body).toContain(`- ${requirement}\nPlease confirm these requirements when you book the visit.`);
    expect(order.body).toMatch(/^Hello,\n\nPlease go ahead with the following work at Garden house, as quoted \(\$125\.00\):\n\n- Adjust and function-check entrance latch\n\nRequirements for all work on this unit:\n- /);
    expect(order.title).toBe("Work order: Make the entrance secure");
    const confirmations = store.all(HandoffMessage).filter((message) => message.direction === "Incoming" && message.body?.includes("Confirmed requirements:"));
    expect(confirmations).toHaveLength(1);
    expect(confirmations[0]!.body).toContain(requirement);
  });
  it("preserves a genuine deficiency and withholds the final payment", async () => {
    const store = await setup({ repairable: false }); await accepted(store); await deliver(store);
    expect(store.all(HandoffJob)[0]?.status).toBe("Needs attention");
    expect(store.all(HandoffPayment)).toHaveLength(1);
    expect(store.all(HandoffInspection)[0]?.findingsJson).toContain("Deficient");
  });
  it("an assessment can finish without authorizing or performing repairs", async () => {
    const store = await setup({ kind: "Assessment" }); await accepted(store); await deliver(store);
    expect(store.all(HandoffJob)[0]).toMatchObject({ kind: "Assessment", status: "Complete" });
    const latest = store.all(HandoffDocument).filter((doc) => doc.kind === "Property condition").at(-1)!;
    expect(latest.detailsJson).toContain("Deficient");
    expect(store.all(HandoffJob)).toHaveLength(1);
  });
  it("does not report completed performance when access is unavailable", async () => {
    const store = await setup({ accessible: false }); await accepted(store); await deliver(store);
    expect(store.all(HandoffJob)[0]?.status).toBe("Awaiting check");
    expect(store.all(HandoffInspection)[0]?.findingsJson).toContain("Not checked");
  });
  it("rejects a changed source version during a reasoning turn", async () => {
    const store = await setup();
    await expect(run(store, model(() => store.change(HandoffDocument, sourceId("document", "services"), { sourceVersion: "2" })))).rejects.toThrow("changed while");
    expect(store.all(HandoffMessage)).toHaveLength(0);
  });
  it("ignores unrelated workspace activity while reasoning but rejects actual authority changes", async () => {
    const store = await setup();
    await run(store, model(() => store.change(HandoffWorkspace, WORKSPACE, { revision: "99", lastCommandId: "another-handoff" })));
    expect(store.all(HandoffMessage)).toHaveLength(1);
    const second = await setup();
    await expect(run(second, model(() => second.change(HandoffWorkspace, WORKSPACE, { workUserIds: [] })))).rejects.toThrow("permission");
  });
  it("rejects acceptance after source content changes without a revision bump", async () => {
    const store = await setup(), id = await offered(store);
    store.change(HandoffDocument, sourceId("document", "condition"), { text: "New damage has been observed." });
    await expect(acceptHandoffWorkPlan(store.client, id, "1", "accept", PERSON)).rejects.toThrow("facts supporting");
    expect(store.all(HandoffDecision)).toHaveLength(0);
  });
  it("does not disclose narrower-reader source text to a broader derived recommendation", async () => {
    const store = await setup();
    store.change(HandoffDocument, sourceId("document", "condition"), { readerIds: [PERSON, "private-reader"] });
    const boundary = model(), complete = vi.spyOn(boundary, "complete");
    await expect(run(store, boundary)).rejects.toThrow("different access settings");
    expect(complete).not.toHaveBeenCalled();
  });
  it("excludes future material and keeps incomplete or occupant-only notices distinct", () => {
    const input = notice(); input.tenancy.endDate = undefined; input.tenancy.endingKind = "Occupant departure"; input.documents = []; input.agreements = []; input.obligations = [];
    const parsed = readMoveOutNotice(JSON.stringify(input)); expect(parsed.tenancy.endDate).toBeUndefined();
    expect(parsed.tenancy.endingKind).toBe("Occupant departure");
    input.tenancy.endDate = "2026-09-24";
    expect(() => readMoveOutNotice(JSON.stringify(input))).toThrow("Do not record a tenancy end date");
  });
  it("keeps an earlier version-one acceptance parseable without upgrading its contents", async () => {
    const store = await setup(); const id = await offered(store);
    store.change(HandoffWorkPlan, id, { selectionJson: undefined, sourceBasis: undefined });
    const original = acceptedContent(store.get(HandoffWorkPlan, id));
    expect(readAcceptedContent(original)).toMatchObject({ version: "1", selections: [], budgetCents: "15000" });
    expect(acceptedContent(store.get(HandoffWorkPlan, id))).toBe(original);
  });
  it("rejects a model invented total and a cross-case recipient", async () => {
    const store = await setup(); await run(store); vi.advanceTimersByTime(61000); await run(store);
    await run(store, model(undefined, (result) => { (result.proposal as Record<string, unknown>).estimatedCostCents = "1"; }));
    expect(store.all(HandoffAgentWork)[0]?.status).toBe("Recommendation unavailable");
    expect(store.all(HandoffWorkPlan)).toHaveLength(0);
    const second = await setup();
    // A persistent cross-case recipient is refused through corrections, then saved as unavailable; nothing is sent.
    await run(second, model(undefined, (result) => { result.requests = [{ purpose: "Information", recipientPartyId: "other-case-person", question: "Send private information." }]; }));
    expect(second.all(HandoffAgentWork)[0]?.status).toBe("Recommendation unavailable");
    expect(second.all(HandoffMessage).filter((message) => message.recipientPartyId === "other-case-person")).toHaveLength(0);
  });
  it("information requests never accept order or payment instructions", () => {
    expect(() => readInquiry({ purpose: "Commission", recipientPartyId: "provider", question: "Order repairs" })).toThrow("not an order");
    expect(() => readInquiry({ purpose: "Quote", recipientPartyId: "provider", question: "Quote work" })).toThrow("Identify the service");
  });
  it("only commissioned service effects can change physical condition", () => {
    const conditions = [{ conditionId: "entrance", description: "Latch", state: "Deficient" as const, repairable: true, accessible: true },
      { conditionId: "roof", description: "Roof", state: "Deficient" as const, repairable: true, accessible: true }];
    const result = performService(service(), ["latch"], conditions);
    expect(result.conditions.map((item) => item.state)).toEqual(["Satisfied", "Deficient"]);
    expect(result.findings[0]?.observation).toBe("Latch: satisfactory");
    expect(conditions.map((item) => item.state)).toEqual(["Deficient", "Deficient"]);
  });

  it("moves from an accepted assessment to a separately reviewed repair proposal without repairing under the assessment", async () => {
    const store = await setup({ kind: "Assessment" });
    store.change(HandoffDocument, sourceId("document", "services"), { detailsJson: preparedDetails(JSON.stringify({ services: [service("Assessment"), { ...service("Repair"), serviceId: "repair" }] }), { id: PERSON, name: "Operator" }) });
    const assessmentId = await accepted(store), originalAcceptance = store.all(HandoffDecision)[0]!.contentJson;
    await deliver(store);
    const followThrough: WorkModel = { model: MODEL, complete: async (request) => {
      const user = request.messages.find((message) => message.role === "user")!;
      const context = JSON.parse(String(user.content)) as ModelContext & { quotes: Array<{ id: string; kind: string; lines: QuoteLine[]; providerPartyId: string; sourceDocumentId: string }> };
      const repair = context.quotes.find((quote) => quote.kind === "Repair");
      if (!repair) return model(undefined, (result) => {
        result.proposal = null;
        result.requests = [{ purpose: "Quote", recipientPartyId: sourceId("party", "provider"), providerDocumentId: sourceId("document", "services"), serviceId: "repair", question: "Please quote the repair recommended by the assessment." }];
      }).complete(request);
      const revised = { ...context, quotes: [repair], currentProposal: context.currentProposal?.status === "Accepted" ? null : context.currentProposal };
      return model().complete({ ...request, messages: request.messages.map((message) => message === user ? { role: "user", content: JSON.stringify(revised) } : message) });
    } };
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Please recommend the next work using the assessment.", "assessment-discussion", PERSON));
    await run(store, followThrough); vi.advanceTimersByTime(61000); await run(store, followThrough); await run(store, followThrough);
    // The trade quotes against the assessment: its report travels with the quote request; the earlier request had none.
    const report = store.all(HandoffDocument).find((doc) => doc.kind === "Inspection" && doc.title?.endsWith("— report"))!;
    const quoteRequests = store.all(HandoffMessage).filter((message) => message.direction === "Outgoing" && message.purpose === "Quote");
    const attached = (message: typeof quoteRequests[number]) => (JSON.parse(message.detailsJson ?? "{}") as { attachments?: string[] }).attachments ?? [];
    expect(quoteRequests.filter((message) => attached(message).includes(report.documentId))).toHaveLength(1);
    expect(quoteRequests.filter((message) => attached(message).length === 0)).toHaveLength(1);
    const repairId = store.get(HandoffCase, HANDOFF).workPlanId!;
    expect(repairId).not.toBe(assessmentId);
    expect(store.all(HandoffJob)).toHaveLength(1);
    expect(store.all(HandoffJob)[0]?.kind).toBe("Assessment");
    expect(store.all(HandoffDecision)[0]?.contentJson).toBe(originalAcceptance);
    store.apply(await acceptHandoffWorkPlan(store.client, repairId, "1", "accept-repair", PERSON));
    await deliver(store);
    expect(store.all(HandoffJob).map((job) => [job.kind, job.status])).toEqual([["Assessment", "Complete"], ["Repair", "Complete"]]);
    expect(store.all(HandoffDecision)).toHaveLength(2);
  });
  function informationModel(recipient: string, question: string): WorkModel {
    return { model: MODEL, complete: async () => ({ choices: [{ index: 0, logprobs: null, finish_reason: "stop", message: {
      role: "assistant", refusal: null, content: JSON.stringify({ summary: "Ask for the missing information.", proposal: null, propertyReady: false,
        requests: [{ purpose: "Information", recipientPartyId: sourceId("party", recipient), question }] }) } }] }) };
  }
  async function exchange(store: WorkspaceStore, inquiryModel: WorkModel): Promise<void> {
    await run(store, inquiryModel); vi.advanceTimersByTime(61000); await run(store, inquiryModel); await run(store, inquiryModel);
    vi.advanceTimersByTime(61000); await run(store, inquiryModel);
  }
  const information = (store: WorkspaceStore, direction: "Incoming" | "Outgoing") =>
    store.all(HandoffMessage).filter((message) => message.purpose === "Information" && message.direction === direction);
  it("has a correspondent point to its documents instead of pasting them back", async () => {
    const store = await setup();
    await exchange(store, informationModel("owner", "Do you approve booking House Care for the latch?"));
    const [reply] = information(store, "Incoming");
    expect(reply?.body).toBe("Hello,\n\nPlease see my Owner funding confirmation, attached again here.\n\nBest,\nMorgan");
    expect(reply?.body).not.toContain("Owner funds are confirmed for property work.");
    expect(JSON.parse(reply!.detailsJson!).attachments).toEqual([sourceId("document", "funds")]);
    const question = information(store, "Outgoing")[0]!;
    expect(question.body).toBe("Hi Morgan,\n\nDo you approve booking House Care for the latch?\n\nThanks,\nMeadow homes");
    expect(question.title).toBe("Question about Garden house");
  });
  it("closes an information question once when the correspondent has nothing on file", async () => {
    const store = await setup(), inquiryModel = informationModel("tenant", "When can the provider access the entrance?");
    await exchange(store, inquiryModel);
    const [reply] = information(store, "Incoming");
    expect(information(store, "Incoming").length).toBe(1);
    expect(reply?.body).toContain("I'm afraid I don't have anything more on this.");
    expect(JSON.parse(reply!.detailsJson!)).toMatchObject({ unanswered: false });
    expect(reply?.responseDueAt).toBeUndefined();
    vi.advanceTimersByTime(24 * 60 * 60000); await run(store, inquiryModel); await run(store, inquiryModel);
    expect(information(store, "Outgoing").length).toBe(1);
    expect(store.all(HandoffPayment).length).toBe(0);
  });
  it("writes provider quote amounts in the offer's currency, exactly", async () => {
    const store = await setup(); await offered(store);
    const reply = store.all(HandoffMessage).find((message) => message.direction === "Incoming" && message.purpose === "Quote")!;
    expect(reply.body).toBe("Hello,\n\nThanks for your request. Our quote for make the entrance secure is attached: $125.00 in total. Advance of 2500; balance after completion\n\nBest,\nHouse Care");
    const quoteDoc = store.all(HandoffDocument).find((doc) => doc.kind === "Quote" && doc.text === "Make the entrance secure. Adjust and function-check entrance latch: $125.00. Advance of 2500; balance after completion");
    expect(JSON.parse(reply.detailsJson!).attachments).toEqual([quoteDoc!.documentId]);
    expect(formatAmount("3791249", "USD")).toBe("$37,912.49");
    expect(formatAmount("0", "USD")).toBe("$0.00");
    expect(formatAmount("123456789", "EUR")).toBe("EUR 1,234,567.89");
    expect(() => formatAmount("12.5", "USD")).toThrow();
  });
  it("answers a provider's information question from its own service terms, not its earlier documents", async () => {
    const store = await setup();
    await exchange(store, informationModel("provider", "When can you visit, and how long will the visit take?"));
    const replies = information(store, "Incoming");
    expect(replies.length).toBe(1);
    expect(replies[0]?.body).toBe("Hello,\n\nMake the entrance secure: our earliest visit is Wednesday, September 23 and the work takes about 2 minutes. "
      + "We usually reply within 1 minute, and our offer is valid until Thursday, October 1. Advance of 2500; balance after completion. "
      + "We'll agree the visit time once the work is ordered.\n\nBest,\nHouse Care");
    expect(replies[0]?.body).not.toContain("Cleaning and repair quote");
    expect(JSON.parse(replies[0]!.detailsJson!)).toMatchObject({ unanswered: false });
  });
  it("still follows up an earlier open reply once, under a new message identity, never a repeated payment protocol", async () => {
    const store = await setup(), inquiryModel = informationModel("tenant", "When can the provider access the entrance?");
    await exchange(store, inquiryModel);
    const [earlier] = information(store, "Incoming"), work = store.all(HandoffAgentWork)[0]!;
    // Replies saved before this release could remain open, with the agent's wake scheduled for the reminder.
    // They keep one reminder and then close.
    const dueAt = new Date(Date.parse(work.businessTime!) + 60000).toISOString();
    store.change(HandoffMessage, earlier!.messageId, { detailsJson: JSON.stringify({ quoteId: null, unanswered: true }), responseDueAt: dueAt });
    store.change(HandoffAgentWork, work.workId, { status: "Waiting for information", nextBusinessAt: dueAt, nextWakeAt: new Date(Date.now() + 60000).toISOString() });
    for (let step = 0; step < 4; step += 1) { vi.advanceTimersByTime(61000); await run(store, inquiryModel); }
    vi.advanceTimersByTime(24 * 60 * 60000); await run(store, inquiryModel); await run(store, inquiryModel);
    const outgoing = information(store, "Outgoing").map((message) => message.detailsJson ?? "");
    expect(outgoing.length).toBe(2);
    expect(outgoing[1]).toContain("previousReplyId");
    expect(information(store, "Incoming").map((reply) => JSON.parse(reply.detailsJson!).unanswered)).toEqual([true, false]);
    expect(store.all(HandoffPayment).length).toBe(0);
  });
  it("preserves document versions, wakes the same coordinator and refuses changed content under one source version", async () => {
    const { default: receiveHandoffDocument } = await import("../../functions/receiveHandoffDocument.js");
    const store = await setup();
    const document = { sourceSystem: "Mailbox", sourceRecordId: "letter-7", sourceVersion: "1", title: "Access confirmed", kind: "Correspondence",
      text: "Access is available in the morning.", partyId: sourceId("party", "tenant"), availableFrom: "2026-09-23", sourceKind: "Prepared" };
    store.apply(await receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(document), "receive-letter", PERSON));
    expect(store.all(HandoffDocument).filter((doc) => doc.title === "Access confirmed")).toHaveLength(1);
    expect(store.all(HandoffAgentWork)[0]?.status).toBe("Ready to continue");
    expect(JSON.parse(await getHandoffChange(store.client, HANDOFF, "receive-letter"))).toMatchObject({ status: "Saved", kind: "Document received" });
    expect(await receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(document), "receive-letter", PERSON)).toEqual([]);
    await expect(receiveHandoffDocument(store.client, HANDOFF, JSON.stringify({ ...document, text: "Different access." }), "changed-letter", PERSON)).rejects.toThrow("different saved details");
    store.apply(await receiveHandoffDocument(store.client, HANDOFF, JSON.stringify({ ...document, sourceVersion: "2", text: "Access is now available in the afternoon." }), "next-letter", PERSON));
    expect(store.all(HandoffDocument).filter((doc) => doc.title === "Access confirmed")).toHaveLength(2);
  });
  it("recognizes work already underway from the same source records without inventing a decision or instruction", async () => {
    const { default: receiveHandoffDocument } = await import("../../functions/receiveHandoffDocument.js");
    const store = await setup();
    const document = { sourceSystem: "Provider records", sourceRecordId: "existing-1", sourceVersion: "1", title: "Existing work order", kind: "Job record", text: "Work was arranged before Handoff.",
      partyId: sourceId("party", "provider"), availableFrom: "2026-09-23", sourceKind: "Prepared", detailsJson: JSON.stringify({ job: {
        title: "Earlier door inspection", providerPartyId: sourceId("party", "provider"), kind: "Assessment", currency: "USD",
        scope: [{ lineId: "inspection", description: "Inspect the entrance", amountCents: "5000" }], committedCents: "5000", status: "Underway", startedAt: NOW, summary: "Inspection has started.",
      } }) };
    store.apply(await receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(document), "existing-work", PERSON));
    await run(store);
    expect(store.all(HandoffJob)[0]).toMatchObject({ origin: "Existing", status: "Underway", committedCents: "5000" });
    expect(store.all(HandoffJob)[0]?.instructionKey).toBeUndefined();
    expect(store.all(HandoffDecision)).toHaveLength(0);
  });
  it("does not include future judicial or other source material in a current reasoning context", async () => {
    const store = await setup();
    store.change(HandoffDocument, sourceId("document", "condition"), { availableFrom: "2027-01-01", text: "FUTURE-PROTECTED-ASSERTION" });
    const boundary = model(); const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    expect(JSON.stringify(complete.mock.calls)).not.toContain("FUTURE-PROTECTED-ASSERTION");
    expect(JSON.stringify(complete.mock.calls)).not.toContain(sourceId("document", "condition"));
  });
  it("rejects model tooling that attempts to approve or directly patch the world", async () => {
    const store = await setup();
    const boundary: WorkModel = { model: MODEL, complete: async () => ({ choices: [{ index: 0, logprobs: null, finish_reason: "tool_calls", message: {
      role: "assistant", content: null, refusal: null, tool_calls: [{ id: "bad", type: "function", function: { name: "approveAndPatch", arguments: "{}" } }] } }] }) };
    await expect(run(store, boundary)).rejects.toThrow("not available to the coordinator");
    expect(store.all(HandoffDecision)).toHaveLength(0); expect(store.all(HandoffJob)).toHaveLength(0);
  });
  it("does not manufacture property readiness from a model assertion or a completed assessment", async () => {
    const store = await setup({ kind: "Assessment" }); await accepted(store); await deliver(store);
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Is the property ready?", "readiness-question", PERSON));
    const readyModel = model(undefined, (result) => { result.proposal = null; result.requests = []; result.propertyReady = true; });
    // A readiness claim the records don't support goes back as a correction; a model that insists ends the turn as
    // Recommendation unavailable. The turn never fails and the unit is never marked ready.
    const complete = vi.spyOn(readyModel, "complete");
    await run(store, readyModel);
    expect(JSON.stringify(complete.mock.calls.map((call) => call[0].messages))).toMatch(/\\"code\\":\\"readiness\\"/);
    expect(store.get(HandoffCase, HANDOFF).physicalProgress).not.toBe("Ready");
    expect(store.all(HandoffAgentWork)[0]?.status).toBe("Recommendation unavailable");
  });
  it("can record evidence-supported property readiness without completing the financial relationship", async () => {
    const store = await setup(); await accepted(store); await deliver(store);
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Confirm the physical outcome.", "readiness-question", PERSON));
    const readyModel = model(undefined, (result) => { result.proposal = null; result.requests = []; result.propertyReady = true; });
    await run(store, readyModel);
    expect(store.get(HandoffCase, HANDOFF)).toMatchObject({ physicalProgress: "Ready", financialProgress: "Not started" });
    expect(store.all(HandoffAgentWork)[0]).toMatchObject({ status: "Complete",
      nextStep: expect.stringMatching(/^All work is complete and checked\. The unit is ready for the next tenant\./) });
  });


  it("keeps historical business dates coherent while server wake-ups use current time", async () => {
    const { HandoffTenancy } = await import("@ontology/sdk");
    const store = await setup();
    store.change(HandoffCase, HANDOFF, { businessDate: "2018-03-02" });
    store.change(HandoffTenancy, sourceId("tenancy", "tenancy-1"), { startDate: "2015-01-01", endDate: "2018-02-28", noticeDate: "2018-02-01" });
    store.change(HandoffDocument, sourceId("document", "services"), { detailsJson: preparedDetails(JSON.stringify({ services: [{ ...service(), availableFrom: "2018-03-05T09:00:00.000Z", validUntil: "2018-03-09T17:00:00.000Z" }] }), { id: PERSON, name: "Operator" }) });
    store.change(HandoffDocument, sourceId("document", "funds"), { detailsJson: preparedDetails(JSON.stringify({ ownerPartyId: sourceId("party", "owner"), currency: "USD", confirmedCents: "30000", confirmedAt: "2018-03-02T09:00:00.000Z", paymentBehavior: "Settle", responseMinutes: 1 }), { id: PERSON, name: "Operator" }) });
    await run(store);
    expect(store.all(HandoffAgentWork)[0]?.nextWakeAt?.startsWith("2026-")).toBe(true);
    expect(store.all(HandoffAgentWork)[0]?.nextBusinessAt?.startsWith("2018-")).toBe(true);
    vi.advanceTimersByTime(61000); await run(store); await run(store);
    const planId = store.get(HandoffCase, HANDOFF).workPlanId!;
    store.apply(await acceptHandoffWorkPlan(store.client, planId, "1", "historical-accept", PERSON));
    await deliver(store);
    expect(store.all(HandoffJob)[0]?.status).toBe("Complete");
    expect(store.all(HandoffJob)[0]?.appointmentAt?.startsWith("2018-03-05")).toBe(true);
    expect(store.all(HandoffInspection)[0]?.observedAt?.startsWith("2018-03-05")).toBe(true);
    // One case clock: correspondence is dated on the case's business time, not the server's.
    expect(store.all(HandoffMessage).every((message) => message.createdAt?.startsWith("2018-"))).toBe(true);
  });
  it("allows an information request to reference an existing quote without treating it as a service catalogue", async () => {
    const store = await setup(); await offered(store);
    const quote = store.all(HandoffQuote)[0]!;
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Please ask the provider about access.", "access-question", PERSON));
    const boundary = model(undefined, (result) => { result.proposal = null; result.requests = [{ purpose: "Information", recipientPartyId: sourceId("party", "provider"),
      question: "Please confirm who should provide access to the premises for the visit. ".repeat(5).trim(), providerDocumentId: quote.sourceDocumentId }]; });
    await run(store, boundary);
    const view = JSON.parse(await getHandoffWorkspace(store.client, HANDOFF)) as HandoffWorkspaceView;
    const inquiry = view.messages.find((message) => message.purpose === "Information" && message.direction === "Outgoing")!;
    expect(inquiry.title.length).toBeLessThanOrEqual(200);
    expect(inquiry.body.length).toBeGreaterThan(200);
  });


  it("keeps the funding owner distinct from the tenancy landlord", async () => {
    const { HandoffParty } = await import("@ontology/sdk");
    const store = await setup();
    store.put(HandoffParty, { partyId: "property-funder", workspaceId: WORKSPACE, readerIds: [PERSON], name: "Property owner", kind: "Organization", description: "Provides funds for work." });
    store.change(HandoffDocument, sourceId("document", "funds"), { partyId: "property-funder", detailsJson: preparedDetails(JSON.stringify({ ownerPartyId: "property-funder", currency: "USD", confirmedCents: "30000", confirmedAt: NOW, paymentBehavior: "Settle", responseMinutes: 1 }), { id: PERSON, name: "Operator" }) });
    await accepted(store); await deliver(store);
    expect(store.all(HandoffFunding)[0]?.ownerPartyId).toBe("property-funder");
    expect(store.all(HandoffInvoice)[0]?.payerPartyId).toBe("property-funder");
    expect(store.all(HandoffPayment).every((payment) => payment.status === "Settled")).toBe(true);
  });
  it("uses a newly confirmed independent allocation without treating the budget as cash or rewriting the accepted scope", async () => {
    const { default: receiveHandoffDocument } = await import("../../functions/receiveHandoffDocument.js");
    const store = await setup({ funds: "2000" }); const id = await accepted(store); await deliver(store);
    const acceptedBefore = store.all(HandoffDecision)[0]!.contentJson;
    store.apply(await receiveHandoffDocument(store.client, HANDOFF, JSON.stringify({ sourceSystem: "Owner books", sourceRecordId: "additional-allocation", sourceVersion: "1", title: "Additional owner funds", kind: "Owner funding",
      text: "A separate allocation of 20000 minor units is confirmed for this property's work.", partyId: sourceId("party", "owner"), availableFrom: "2026-09-23", sourceKind: "Prepared",
      detailsJson: JSON.stringify({ ownerPartyId: sourceId("party", "owner"), currency: "USD", confirmedCents: "20000", confirmedAt: NOW, paymentBehavior: "Settle", responseMinutes: 1 }) }), "more-funds", PERSON));
    await deliver(store);
    expect(store.all(HandoffJob)[0]?.status).toBe("Complete");
    expect(store.all(HandoffFunding)).toHaveLength(2);
    expect(store.get(HandoffWorkPlan, id).status).toBe("Accepted");
    expect(store.all(HandoffDecision)[0]?.contentJson).toBe(acceptedBefore);
  });

});


describe("coordinator admission boundaries", () => {
  it("returns no edits or model work before a waiting wake is due", async () => {
    const store = await setup(); const work = store.all(HandoffAgentWork)[0]!;
    store.change(HandoffAgentWork, work.workId, { status: "Waiting for provider", businessTime: NOW,
      nextBusinessAt: "2026-09-24T10:00:00.000Z", nextWakeAt: "2026-09-23T10:01:00.000Z" });
    const boundary = model(), complete = vi.spyOn(boundary, "complete");
    expect(await coordinateHandoff(store.client, HANDOFF, "early-wake", PERSON, { model: boundary })).toEqual([]);
    expect(await coordinateHandoff(store.client, HANDOFF, "another-early-wake", PERSON, { model: boundary })).toEqual([]);
    expect(complete).not.toHaveBeenCalled();
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Please check the current access information.", "new-information", PERSON));
    await run(store, boundary); expect(complete).toHaveBeenCalled();
    expect(store.all(HandoffAgentWork)[0]?.businessTime).toBe(NOW);
  });
  it("does not reason again while waiting on an unchanged offered plan", async () => {
    const store = await setup(); await offered(store);
    const boundary = model(), complete = vi.spyOn(boundary, "complete");
    await run(store, boundary); await run(store, boundary);
    expect(complete).not.toHaveBeenCalled();
  });
  it.each(["Do not use House Care.", "Someone suggested House Care but I have not chosen them.", "Could House Care do this?"])("does not manufacture an explicit provider requirement from %s", async (message) => {
    const store = await setup(); await offered(store);
    store.apply(await sendHandoffMessage(store.client, HANDOFF, message, "provider-discussion", PERSON));
    const boundary = model(undefined, (result) => { (result.proposal as Record<string, unknown>).fixedProviderPartyId = sourceId("party", "provider"); });
    await expect(run(store, boundary)).rejects.toThrow("explicit operator choice");
  });
  it("retains a provider fixed through the structured operator choice", async () => {
    const store = await setup(); const id = await offered(store);
    store.apply(await changePlan(store.client, id, "1", undefined, "provider-choice", PERSON, JSON.stringify({ fixedProviderPartyId: sourceId("party", "provider") })));
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Please refine the explanation.", "discuss-fixed-plan", PERSON));
    await run(store, model(undefined, (result) => { (result.proposal as Record<string, unknown>).fixedProviderPartyId = sourceId("party", "provider"); }));
    expect(store.get(HandoffWorkPlan, id).fixedProviderPartyId).toBe(sourceId("party", "provider"));
  });
  it("does not mark the entire property ready on limited completed checks", async () => {
    const store = await setup(); await accepted(store); await deliver(store);
    store.change(HandoffCase, HANDOFF, { goal: "The entire property is ready for its next occupants." });
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Is the entire property ready?", "broader-outcome", PERSON));
    await run(store, model(undefined, (result) => { result.proposal = null; result.requests = []; result.propertyReady = true; }));
    expect(store.get(HandoffCase, HANDOFF).physicalProgress).not.toBe("Ready");
    expect(store.all(HandoffAgentWork)[0]?.status).toBe("Recommendation unavailable");
  });
});


describe("checked recommendation recovery", () => {
  async function quoted(): Promise<WorkspaceStore> {
    const store = await setup();
    await run(store); vi.advanceTimersByTime(61000); await run(store);
    expect(store.all(HandoffQuote)).toHaveLength(1);
    expect(store.all(HandoffWorkPlan)).toHaveLength(0);
    return store;
  }
  it("derives the public scope from selections, allowing revised prose for the identical priced work", async () => {
    const store = await quoted();
    const boundary = model(undefined, (result) => {
      const proposal = result.proposal as Record<string, unknown>;
      (proposal.selections as WorkSelection[])[0]!.scope = "Adjust the entrance latch and verify secure closure.";
      (proposal.selections as WorkSelection[])[0]!.reason = "The offered adjustment addresses unreliable closure while retaining the existing fitting.";
    });
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    const plan = store.all(HandoffWorkPlan)[0]!;
    expect(plan.scope).toEqual(["Adjust the entrance latch and verify secure closure."]);
    expect(plan.desiredOutcome).toBe("A secure entrance.");
    expect(plan.estimatedCostCents).toBe("12500");
    expect(JSON.parse(plan.selectionJson!)[0]).toMatchObject({ scope: plan.scope![0], quoteLineId: "latch" });
    const format = complete.mock.calls[0]![0].response_format;
    expect(format?.type).toBe("json_schema");
    if (format?.type !== "json_schema") throw new Error("Expected the model response contract");
    const schema = format.json_schema.schema as { properties: { proposal: { anyOf: Array<{ required: string[]; properties: Record<string, unknown> }> } } };
    expect(schema.properties.proposal.anyOf[0]!.required).not.toContain("scope");
    expect(schema.properties.proposal.anyOf[0]!.properties).not.toHaveProperty("scope");
    expect(complete).toHaveBeenCalledTimes(3);
    expect(store.all(HandoffJob)).toHaveLength(0); expect(store.all(HandoffDecision)).toHaveLength(0);
  });
  it("asks for plain wording when a draft cites shortened record references", async () => {
    const store = await quoted(); let drafts = 0;
    const boundary = model(undefined, (result) => {
      drafts += 1;
      if (drafts === 1) (result.proposal as { selections: WorkSelection[] }).selections[0]!.reason += " Sources: document:b80d602..., quote:a56fe7...";
    });
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    expect(drafts).toBe(2);
    const feedback = JSON.parse(String(complete.mock.calls[3]![0].messages.at(-1)!.content)) as { validationFeedback: { code: string } };
    expect(feedback.validationFeedback.code).toBe("copy");
    const reasons = (JSON.parse(store.all(HandoffWorkPlan)[0]!.selectionJson!) as WorkSelection[]).map((line) => line.reason).join(" ");
    expect(reasons).not.toMatch(/document:|quote:/);
  });
  it.each([
    ["an unknown recipient", (): Record<string, unknown> => ({ purpose: "Information", recipientPartyId: "party:not-in-this-handoff",
      question: "Can you attend on Monday?", providerDocumentId: null, serviceId: null })],
    ["a service the provider does not list", (): Record<string, unknown> => ({ purpose: "Quote", recipientPartyId: sourceId("party", "provider"),
      question: "Please quote to replace the door.", providerDocumentId: sourceId("document", "services"), serviceId: "not-a-service" })],
  ] as const)("asks the model to correct a request to %s instead of failing the turn", async (_name, request) => {
    const store = await quoted(); let drafts = 0;
    const boundary = model(undefined, (result) => { drafts += 1; if (drafts === 1) result.requests = [request()]; });
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    expect(drafts).toBe(2);
    const feedback = JSON.parse(String(complete.mock.calls[3]![0].messages.at(-1)!.content)) as { validationFeedback: { code: string } };
    expect(feedback.validationFeedback.code).toBe("requests");
    expect(store.all(HandoffWorkPlan)).toHaveLength(1);
    expect(store.all(HandoffMessage).filter((message) => message.direction === "Outgoing" && message.body?.includes("not-a-service"))).toHaveLength(0);
  });
  it("asks every vendor service in one turn, more than four, without a correction", async () => {
    const store = await setup();
    const many = Array.from({ length: 6 }, (_, n) => ({ ...service(), serviceId: `service-${n + 1}`, title: `Service ${n + 1}` }));
    store.change(HandoffDocument, sourceId("document", "services"), { detailsJson: preparedDetails(JSON.stringify({ services: many }), { id: PERSON, name: "Operator" }) });
    let drafts = 0;
    const boundary = model(undefined, (result) => {
      drafts += 1;
      result.requests = many.map((item) => ({ purpose: "Quote", recipientPartyId: sourceId("party", "provider"),
        question: `Please quote ${item.title.toLowerCase()}.`, providerDocumentId: sourceId("document", "services"), serviceId: item.serviceId }));
    });
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    expect(drafts).toBe(1);
    expect(JSON.stringify(complete.mock.calls.map((call) => call[0].messages))).not.toContain("validationFeedback");
    expect(store.all(HandoffMessage).filter((message) => message.direction === "Outgoing" && message.purpose === "Quote")).toHaveLength(6);
  });
  it("caps a proposed budget at the confirmed owner funds when the quoted work fits within them", async () => {
    const store = await setup({ funds: "13000" }); const id = await offered(store);
    expect(store.get(HandoffWorkPlan, id)).toMatchObject({ estimatedCostCents: "12500", budgetCents: "13000" });
  });
  it("asks for plain request wording without field names or amounts in cents", async () => {
    const store = await quoted(); let drafts = 0;
    const boundary = model(undefined, (result) => {
      drafts += 1;
      if (drafts === 1) result.requests = [{ purpose: "Information", recipientPartyId: sourceId("party", "provider"),
        question: "Please confirm the deposit of 2,500 cents for serviceId entrance.", providerDocumentId: null, serviceId: null }];
    });
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    const feedback = JSON.parse(String(complete.mock.calls[3]![0].messages.at(-1)!.content)) as { validationFeedback: { code: string } };
    expect(feedback.validationFeedback.code).toBe("copy");
    expect(store.all(HandoffMessage).some((message) => message.body?.includes("serviceId"))).toBe(false);
  });
  it("asks for a plain plan title without shorthand", async () => {
    const store = await quoted(); let drafts = 0;
    const boundary = model(undefined, (result) => { drafts += 1; if (drafts === 1) (result.proposal as Record<string, unknown>).title = "Latch + door (entrance)"; });
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    const feedback = JSON.parse(String(complete.mock.calls[3]![0].messages.at(-1)!.content)) as { validationFeedback: { code: string } };
    expect(feedback.validationFeedback.code).toBe("copy");
    // The rejected draft stays in the turn, so the correction edits it.
    const draft = complete.mock.calls[3]![0].messages.at(-2)!;
    expect(draft.role).toBe("assistant"); expect(String(draft.content)).toContain("Latch + door");
    expect(store.all(HandoffWorkPlan)[0]?.title).toBe("Secure the entrance");
  });
  it("checks a selection reason for record IDs when it is first written, at the price check", async () => {
    const store = await quoted(); const base = model(); let tampered = false;
    const boundary: WorkModel = { model: MODEL, complete: async (request) => {
      const response = await base.complete(request);
      const call = response.choices[0]?.message.tool_calls?.[0];
      if (!tampered && call?.type === "function" && call.function.name === "quoteCosts") {
        tampered = true;
        const args = JSON.parse(call.function.arguments) as { selections: WorkSelection[] };
        args.selections[0]!.reason = `Quoted by the vendor (${store.all(HandoffQuote)[0]!.sourceDocumentId}).`;
        call.function.arguments = JSON.stringify(args);
      }
      return response;
    } };
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    const toolFeedback = complete.mock.calls.flatMap(([request]) => request.messages)
      .filter((message) => message.role === "tool" && String(message.content).includes("validationFeedback"));
    expect(String(toolFeedback[0]?.content)).toContain("\"code\":\"copy\"");
  });
  it("tells the model which services are already quoted", async () => {
    const store = await quoted(); const base = model(); const seen: string[] = [];
    const boundary: WorkModel = { model: MODEL, complete: async (request) => {
      const input = JSON.parse(String(request.messages.find((message) => message.role === "user")!.content)) as { services: Array<{ status: string }> };
      seen.push(...input.services.map((service) => service.status));
      return base.complete(request);
    } };
    await run(store, boundary);
    expect(seen).toContain("quoted");
    expect(seen.every((status) => ["quoted", "ordered", "not quoted"].includes(status))).toBe(true);
  });
  it("reads a quote by its quote ID and reports an unknown ID instead of failing the turn", async () => {
    const store = await quoted(); const base = model(); let first = true;
    const boundary: WorkModel = { model: MODEL, complete: async (request) => {
      if (!first) return base.complete(request);
      first = false;
      const input = JSON.parse(String(request.messages.find((message) => message.role === "user")!.content)) as ModelContext;
      const ids = [...input.documents.map((doc) => doc.id).slice(-14), input.quotes[0]!.id, "document:missing"];
      return { choices: [{ index: 0, logprobs: null, finish_reason: "tool_calls", message: { role: "assistant", content: null, refusal: null,
        tool_calls: [{ id: "read-odd", type: "function", function: { name: "readDocuments", arguments: JSON.stringify({ ids }) } }] } }] };
    } };
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    expect(store.all(HandoffWorkPlan)).toHaveLength(1);
    expect(String(complete.mock.calls[1]![0].messages.find((message) => message.role === "tool")!.content)).toContain("Not an available document");
  });
  it("uses concise structured feedback to correct one invalid draft, kept only in the turn and never saved", async () => {
    const store = await quoted(); let drafts = 0;
    const boundary = model(undefined, (result) => {
      drafts += 1;
      if (drafts === 1) {
        (result.proposal as Record<string, unknown>).estimatedCostCents = "1";
        result.summary = "PRIVATE-INVALID-DRAFT-MARKER";
      }
    });
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    expect(drafts).toBe(2); expect(complete).toHaveBeenCalledTimes(4);
    const correction = complete.mock.calls[3]![0];
    const feedback = JSON.parse(String(correction.messages.at(-1)!.content)) as { validationFeedback: { code: string; correctionsRemaining: number } };
    expect(feedback.validationFeedback).toMatchObject({ code: "selection", correctionsRemaining: 3 });
    // The draft is in front of the model for this correction only, as its own assistant message.
    const kept = correction.messages.filter((message) => JSON.stringify(message).includes("PRIVATE-INVALID-DRAFT-MARKER"));
    expect(kept.map((message) => message.role)).toEqual(["assistant"]);
    expect(JSON.stringify(store.all(HandoffActivity))).not.toContain("PRIVATE-INVALID-DRAFT-MARKER");
    expect(JSON.stringify(store.all(HandoffWorkPlan))).not.toContain("PRIVATE-INVALID-DRAFT-MARKER");
    expect(store.all(HandoffWorkPlan)[0]?.estimatedCostCents).toBe("12500");
  });
  it.each([
    ["missing quote", (p: Record<string, unknown>) => { (p.selections as WorkSelection[])[0]!.quoteId = "missing"; }],
    ["missing line", (p: Record<string, unknown>) => { (p.selections as WorkSelection[])[0]!.quoteLineId = "missing"; }],
    ["duplicate price", (p: Record<string, unknown>) => { (p.selections as WorkSelection[]).push({ ...(p.selections as WorkSelection[])[0]! }); }],
    ["different currency", (p: Record<string, unknown>) => { p.currency = "EUR"; }],
    ["invented price", (p: Record<string, unknown>) => { p.estimatedCostCents = "0"; }],
    ["insufficient budget", (p: Record<string, unknown>) => { p.budgetCents = "1"; }],
    ["missing quote source", (p: Record<string, unknown>) => { p.sourceDocumentIds = [sourceId("document", "lease")]; }],
    ["blank scope", (p: Record<string, unknown>) => { (p.selections as WorkSelection[])[0]!.scope = " "; }],
    ["invented requirement", (p: Record<string, unknown>) => { p.fixedRequirements = ["Replace the latch only if adjustment fails."]; }],
  ] as const)("fails closed after four corrections for %s and does not schedule model-only retries", async (_name, corrupt) => {
    const store = await quoted();
    const boundary = model(undefined, (result) => { corrupt(result.proposal as Record<string, unknown>); result.summary = "PRIVATE-FAILED-DRAFT-MARKER"; });
    const complete = vi.spyOn(boundary, "complete");
    await run(store, boundary);
    expect(complete).toHaveBeenCalledTimes(7); // Read, price, first draft and exactly four corrections.
    const work = store.all(HandoffAgentWork)[0]!;
    expect(work).toMatchObject({ status: "Recommendation unavailable", operationKey: expect.stringMatching(/^reason:/) });
    expect(work.nextWakeAt).toBeUndefined(); expect(work.nextBusinessAt).toBeUndefined();
    expect(work.nextStep).toContain("couldn't finish a plan");
    expect(store.all(HandoffWorkPlan)).toHaveLength(0); expect(store.all(HandoffJob)).toHaveLength(0);
    expect(store.all(HandoffDecision)).toHaveLength(0);
    expect(JSON.stringify(store.all(HandoffActivity))).not.toContain("PRIVATE-FAILED-DRAFT-MARKER");
    vi.advanceTimersByTime(61000); await run(store, boundary);
    vi.advanceTimersByTime(86400000); await run(store, boundary);
    expect(complete).toHaveBeenCalledTimes(7);
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Please consider the current quoted work again.", "reconsider-after-failure", PERSON));
    await run(store);
    expect(store.all(HandoffWorkPlan)[0]?.estimatedCostCents).toBe("12500");
  });
  it("recovers a malformed quoteCosts input inside the same bounded tool loop", async () => {
    const store = await quoted(), base = model(); let priceCalls = 0;
    const boundary: WorkModel = { model: MODEL, complete: async (request) => {
      const response = await base.complete(request);
      const call = response.choices[0]?.message.tool_calls?.[0];
      if (call?.type === "function" && call.function.name === "quoteCosts" && priceCalls++ === 0) call.function.arguments = "{broken";
      const last = request.messages.at(-1);
      if (last?.role === "tool" && String(last.content).includes("validationFeedback")) {
        return { choices: [{ index: 0, logprobs: null, finish_reason: "tool_calls", message: { role: "assistant", refusal: null, content: null,
          tool_calls: [{ id: "corrected-price", type: "function", function: { name: "quoteCosts", arguments: JSON.stringify({ selections: [{
            quoteId: store.all(HandoffQuote)[0]!.quoteId, quoteLineId: "latch", scope: "Secure the entrance latch.", reason: "The quoted adjustment addresses unreliable closure.",
          }] }) } }] } }] };
      }
      return response;
    } };
    await run(store, boundary);
    expect(store.all(HandoffWorkPlan)[0]?.estimatedCostCents).toBe("12500");
  });
  it("rejects a same-priced line substitution that was never priced by the tool", async () => {
    const store = await quoted(), quote = store.all(HandoffQuote)[0]!;
    store.change(HandoffQuote, quote.quoteId, { totalCents: "25000", linesJson: JSON.stringify([
      { lineId: "latch", description: "Adjust latch", amountCents: "12500" },
      { lineId: "assessment", description: "Assess without repair", amountCents: "12500" },
    ]) });
    const base = model(undefined, (result) => {
      const proposal = result.proposal as Record<string, unknown>;
      proposal.selections = [{ quoteId: quote.quoteId, quoteLineId: "assessment", scope: "Assess the latch only.", reason: "The assessment does not repair the latch." }];
    });
    const boundary: WorkModel = { model: MODEL, complete: async (request) => {
      const response = await base.complete(request), call = response.choices[0]?.message.tool_calls?.[0];
      if (call?.type === "function" && call.function.name === "quoteCosts") {
        const args = JSON.parse(call.function.arguments) as { selections: WorkSelection[] };
        args.selections = args.selections.filter((line) => line.quoteLineId === "latch");
        call.function.arguments = JSON.stringify(args);
      }
      return response;
    } };
    await run(store, boundary);
    expect(store.all(HandoffWorkPlan)).toHaveLength(0);
    expect(store.all(HandoffAgentWork)[0]?.status).toBe("Recommendation unavailable");
  });
  it.each(["source", "request", "authority"])("rechecks %s freshness before persisting failed reasoning", async (changed) => {
    const store = await quoted(), original = store.all(HandoffAgentWork)[0]!;
    const boundary = model(() => {
      if (changed === "source") store.change(HandoffDocument, sourceId("document", "services"), { sourceVersion: "changed-during-reasoning" });
      if (changed === "request") store.change(HandoffAgentWork, original.workId, { operationKey: "new-request" });
      if (changed === "authority") store.change(HandoffWorkspace, WORKSPACE, { workUserIds: [] });
    }, (result) => { (result.proposal as Record<string, unknown>).estimatedCostCents = "1"; });
    await expect(run(store, boundary)).rejects.toThrow(changed === "authority" ? "permission" : "changed while");
    expect(store.all(HandoffWorkPlan)).toHaveLength(0);
    expect(store.all(HandoffAgentWork)[0]?.status).not.toBe("Recommendation unavailable");
  });
  it("leaves authentication, transport and arbitrary business errors visible, without treating them as validation corrections", async () => {
    const { UserFacingError } = await import("@osdk/functions");
    for (const failure of [new Error("transport unavailable"), new UserFacingError("permission denied")]) {
      const store = await quoted(), boundary: WorkModel = { model: MODEL, complete: vi.fn().mockRejectedValue(failure) };
      await expect(run(store, boundary)).rejects.toBe(failure);
      expect(boundary.complete).toHaveBeenCalledOnce();
      expect(store.all(HandoffAgentWork)[0]?.status).not.toBe("Recommendation unavailable");
    }
  });
  it("preserves actual provider wakes after failed reasoning and handles the reply before any further model call", async () => {
    const store = await setup();
    await run(store); // An actual quote inquiry is pending.
    store.apply(await sendHandoffMessage(store.client, HANDOFF, "Please consider the work while the quote is pending.", "pending-discussion", PERSON));
    const failing = model(undefined, (result) => { result.summary = ""; }), complete = vi.spyOn(failing, "complete");
    await run(store, failing);
    expect(store.all(HandoffAgentWork)[0]).toMatchObject({ status: "Recommendation unavailable", nextWakeAt: expect.any(String) });
    expect(complete).toHaveBeenCalledTimes(6); // Read and five invalid final attempts; no invented price.
    vi.advanceTimersByTime(61000); await run(store, failing);
    expect(store.all(HandoffQuote)).toHaveLength(1); expect(complete).toHaveBeenCalledTimes(6);
    await run(store);
    expect(store.all(HandoffWorkPlan)[0]?.estimatedCostCents).toBe("12500");
  });
  it("handles incoming payment outcomes even when the saved reasoning state is unavailable", async () => {
    const store = await setup(); await accepted(store);
    for (let step = 0; step < 8 && !store.all(HandoffPayment).length; step += 1) { vi.advanceTimersByTime(61000); await run(store); }
    expect(store.all(HandoffPayment)[0]?.status).toBe("Requested");
    const work = store.all(HandoffAgentWork)[0]!;
    store.change(HandoffAgentWork, work.workId, { status: "Recommendation unavailable" });
    const boundary: WorkModel = { model: MODEL, complete: vi.fn().mockRejectedValue(new Error("Must not reason before payment results")) };
    for (let step = 0; step < 4 && store.all(HandoffPayment)[0]?.status === "Requested"; step += 1) {
      vi.advanceTimersByTime(61000); await run(store, boundary);
    }
    expect(store.all(HandoffPayment)[0]?.status).toBe("Settled"); expect(boundary.complete).not.toHaveBeenCalled();
  });
});
