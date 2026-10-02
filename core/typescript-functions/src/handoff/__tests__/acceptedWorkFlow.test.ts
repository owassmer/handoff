import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Admin, MediaSets } from "@osdk/foundry";
import { Aliases, createEditBatch } from "@osdk/functions";
import { HandoffAgentWork, HandoffCase, HandoffDecision, HandoffDocument, HandoffFunding, HandoffInspection, HandoffInvoice,
  HandoffJob, HandoffMessage, HandoffParty, HandoffPayment, HandoffQuote, HandoffWorkPlan, HandoffWorkspace } from "@ontology/sdk";
import createHandoffWorkspace from "../../functions/createHandoffWorkspace.js";
import receiveMoveOutNotice from "../../functions/receiveMoveOutNotice.js";
import receiveHandoffDocument from "../../functions/receiveHandoffDocument.js";
import getHandoffWorkspace from "../../functions/getHandoffWorkspace.js";
import { coordinateHandoff } from "../coordinator.js";
import { acceptedContent, planDraft } from "../workPlans.js";
import { requestWorkCorrespondence } from "../correspondence.js";
import { jobScope, loadDeliveryRecords, sourceIdentity, type DeliveryContext } from "../deliveryRecords.js";
import { loadDetails } from "../workDetails.js";
import { recognizeAcceptedWork } from "../acceptedWork.js";
import { bindExistingJobFunding, requestProviderPayment } from "../funding.js";
import { preparation, sourceDetails } from "../sourceAccess.js";
import { reference } from "../values.js";
import type { ReceivedDocument } from "../documentIntake.js";
import type { ProviderService } from "../supportingSources.js";
import type { WorkModel } from "../reasoner.js";
import type { HandoffEdit } from "../records.js";
import { WorkspaceStore, PERSON, MODEL, WORKSPACE, HANDOFF, sourceId, notice } from "./workspaceSupport.js";

vi.mock("@osdk/foundry", () => ({ Admin: { Users: { getCurrent: vi.fn() } }, MediaSets: { MediaSets: { readOriginal: vi.fn() } } }));
vi.mock("@osdk/functions", async (original) => { const actual = await original<typeof import("@osdk/functions")>();
  return { ...actual, Aliases: { ...actual.Aliases, model: vi.fn() } }; });
const NOW = "2026-09-23T10:00:00.000Z", QUOTE = sourceId("document", "quote"), PROVIDER = sourceId("party", "provider"), OWNER = sourceId("party", "owner");
const SCOPE = [
  "Attend the facility for the agreed visual survey, without altering equipment.",
  "Review the storage and reception areas against the supplied departure notes.",
  "Record the locations and dimensions of the observed defects for later trade pricing.",
  "Compare the observed items with the supplied earlier maintenance record.",
  "Identify access limits and flag any observable hazards without concealed investigation.",
  "Provide a written report and indicative cost note, not authority to undertake repairs.",
  "Keep roof maintenance outside this commission and identify it separately.",
];
const REQUIREMENT = "Keep roof maintenance separate.";
const TERMS = "Invoice on report delivery, payable within nine days; no advance is required.";
const QUOTE_TEXT = `Facility survey includes written advice. Fixed charges: visual visit $175; measured schedule $92; written advice $133. Total $400 USD. ${TERMS} ${REQUIREMENT} No equipment alterations or concealed investigation. The quoted work covers a visual survey, locations, dimensions, historical comparison, access limits, hazards and indicative costing.`;
const LINES = [
  { lineId: "visit", description: "visual visit", amountCents: "17500" },
  { lineId: "schedule", description: "measured schedule", amountCents: "9200" },
  { lineId: "advice", description: "written advice", amountCents: "13300" },
];
const GROUPS = [[0, 1, 2], [2, 3, 4], [5, 6]];
const OBSERVATIONS = [
  "The visual facility visit covered both accessible areas. Equipment was not altered.",
  "The departure notes identify a damaged storage shelf and scuffed reception panel; both are visible.",
  "The shelf has a 12 cm split at its exposed end; the panel scuff measures 15 by 8 cm.",
  "The earlier record already lists the panel scuff; it does not record the shelf split. Responsibility is not determined.",
  "The accessible shelf edge is sharp; restrict contact pending repair advice. Concealed fixings were not examined.",
  "Written advice: seek a shelf repair quotation. Indicative allowance is 7000 minor units, not an approved repair price.",
  "Roof maintenance remains a separate owner matter and is excluded from this report's priced work.",
];
const noModel: WorkModel = { model: MODEL, complete: async () => { throw new Error("Existing accepted work must progress without another approval or model proposal"); } };
let turn = 0;
beforeEach(() => {
  turn = 0; vi.useFakeTimers(); vi.setSystemTime(NOW); vi.resetAllMocks();
  vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: PERSON, username: "operator", attributes: {}, realm: "users", status: "ACTIVE" });
  vi.mocked(Aliases.model).mockReturnValue({ rid: MODEL });
});
afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks(); });
function service(withReports = true): ProviderService {
  return { serviceId: "survey", title: "Facility survey", kind: "Assessment", currency: "USD", lines: LINES,
    depositCents: "0", paymentTerms: TERMS, requirements: [REQUIREMENT], availableFrom: NOW,
    validUntil: "2026-10-08T00:00:00.000Z", responseMinutes: 1, durationMinutes: 2, invoiceDueMinutes: 12960,
    effects: LINES.map((line, i) => ({ lineId: line.lineId, conditionIds: ["shelf", "panel"], method: "Visual examination and recorded measurements.",
      ...(withReports ? { deliverables: GROUPS[i]!.map((index) => ({ acceptedScope: SCOPE[index]!, observation: OBSERVATIONS[index]!,
        method: "Compare the dated survey observations and measurement notes with supplied records.", sourceDocumentIds: [sourceId("document", "inspection")], conditionIds: ["shelf", "panel"] })) } : {}) })) };
}
function envelope(kind: string, id: string, details: object, partyId = PROVIDER): ReceivedDocument {
  return { sourceSystem: "Demonstration source", sourceRecordId: id, sourceVersion: "1", kind, title: kind,
    text: `${kind} supplied for the facility survey.`, partyId, sourceKind: "Prepared", availableFrom: "2026-09-23", detailsJson: JSON.stringify(details) };
}
async function intake(store: WorkspaceStore, input: ReceivedDocument): Promise<void> {
  store.apply(await receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(input), `source-${++turn}`, PERSON));
}
function context(store: WorkspaceStore): DeliveryContext {
  return { client: store.client, batch: createEditBatch<HandoffEdit>(store.client), workspace: store.get(HandoffWorkspace, WORKSPACE),
    handoff: store.get(HandoffCase, HANDOFF), caller: { id: PERSON, name: "Operator" }, now: NOW };
}
async function tick(store: WorkspaceStore): Promise<HandoffEdit[]> {
  const work = store.all(HandoffAgentWork)[0]!;
  if (work.nextWakeAt && work.nextWakeAt > new Date().toISOString()) vi.setSystemTime(work.nextWakeAt);
  const edits = await coordinateHandoff(store.client, HANDOFF, `turn-${++turn}`, PERSON, { model: noModel });
  store.apply(edits); return edits;
}
async function until(store: WorkspaceStore, predicate: () => boolean): Promise<void> {
  for (let i = 0; i < 30 && !predicate(); i++) await tick(store);
  expect(predicate()).toBe(true);
}
function quoteInput(providerDocumentId: string): ReceivedDocument {
  const { effects: _effects, serviceId: _serviceId, invoiceDueMinutes: _invoiceDueMinutes, ...offer } = service();
  return { sourceSystem: "Received document", sourceRecordId: QUOTE, sourceVersion: "1", title: "Facility survey quote", kind: "Quote", text: QUOTE_TEXT,
    partyId: PROVIDER, sourceKind: "Prepared", associatedDocumentId: QUOTE, availableFrom: "2026-09-23",
    detailsJson: JSON.stringify({ offer: { ...offer, providerPartyId: PROVIDER, totalCents: "40000" }, sourcePassages: [QUOTE_TEXT], providerDocumentId, serviceId: "survey", providerSourceVersion: "1" }) };
}
async function setup(options: { funds?: string | null; reports?: boolean; accessible?: boolean; enrich?: boolean; map?: boolean } = {}): Promise<WorkspaceStore> {
  const store = new WorkspaceStore();
  store.apply(await createHandoffWorkspace(store.client, "Facility work", "open-workspace", PERSON));
  const input = notice(); input.businessDate = NOW.slice(0, 10); input.goal = "Understand the facility condition before authorizing repairs.";
  input.documents = [input.documents[0]!, { ...input.documents[1]!, text: OBSERVATIONS.join("\n"), sourceKind: "Prepared" },
    { ...input.documents[2]!, title: "Facility survey quote", kind: "Quote", text: QUOTE_TEXT, sourceKind: "Prepared" }];
  input.fixedRequirements = [REQUIREMENT];
  store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(input), "notice", PERSON));
  // A saved legacy text association: absent metadata is not rewritten during enrichment.
  store.change(HandoffDocument, QUOTE, { detailsJson: undefined, sourceSystem: undefined, sourceRecordId: undefined, sourceVersion: undefined, availableFrom: undefined });
  const plan = store.put(HandoffWorkPlan, { workPlanId: "old-plan", workspaceId: WORKSPACE, readerIds: [PERSON], handoffId: HANDOFF,
    title: "Facility survey", summary: "Survey and report before deciding repairs.", desiredOutcome: input.goal, scope: SCOPE,
    currency: "USD", estimatedCostCents: "40000", budgetCents: "46000", fixedRequirements: [REQUIREMENT], providerPartyId: PROVIDER,
    rationale: "The saved quote supplies the accepted survey.", sourceDocumentIds: [QUOTE, sourceId("document", "inspection")],
    revision: "1", basisRevision: "1", status: "Accepted", acceptedDecisionId: "old-acceptance" });
  store.put(HandoffDecision, { decisionId: "old-acceptance", workspaceId: WORKSPACE, readerIds: [PERSON], handoffId: HANDOFF,
    title: "Accepted facility survey", workPlanId: plan.workPlanId, acceptedRevision: "1", contentJson: acceptedContent(plan), decidedBy: PERSON, decidedAt: NOW });
  store.change(HandoffCase, HANDOFF, { workPlanId: plan.workPlanId, status: "Open" });
  const original = requestWorkCorrespondence("demo", "continue:old-acceptance", store.get(HandoffParty, PROVIDER), planDraft(plan));
  const common = { workspaceId: WORKSPACE, readerIds: [PERSON], handoffId: HANDOFF, workPlanId: plan.workPlanId,
    recipientPartyId: PROVIDER, createdAt: NOW, externalReference: original.externalReference, purpose: "Work", title: "Original correspondence" };
  store.put(HandoffMessage, { ...common, messageId: reference("message", WORKSPACE, "continue:old-acceptance", "request"), direction: "Outgoing", status: "Sent", body: original.body });
  store.put(HandoffMessage, { ...common, messageId: reference("message", WORKSPACE, "continue:old-acceptance", "acknowledgement"), direction: "Incoming", status: "Received", body: original.replyBody });
  await intake(store, envelope("Provider information", "services", { services: [service(options.reports)] }));
  await intake(store, envelope("Property condition", "conditions", { conditions: [
    { conditionId: "shelf", description: "Storage shelf split", state: "Deficient", repairable: true, accessible: options.accessible ?? true },
    { conditionId: "panel", description: "Reception panel scuff", state: "Deficient", repairable: true, accessible: true },
  ] }, OWNER));
  if (options.funds !== null) await intake(store, envelope("Owner funding", "allocation", { ownerPartyId: OWNER, currency: "USD", confirmedCents: options.funds ?? "80000",
    confirmedAt: NOW, paymentBehavior: "Settle", responseMinutes: 1 }, OWNER));
  const providerDoc = store.all(HandoffDocument).find((doc) => doc.kind === "Provider information")!;
  if (options.enrich !== false) await intake(store, quoteInput(providerDoc.documentId));
  if (options.map !== false) await intake(store, envelope("Accepted work mapping", "mapping", { decisionId: "old-acceptance", quoteDocumentId: QUOTE,
    scope: LINES.map((line, index) => ({ quoteLineId: line.lineId, acceptedScopes: GROUPS[index]!.map((i) => SCOPE[i]),
      reason: "These accepted survey deliverables are supported by this priced service line.", sourcePassage: QUOTE_TEXT })) }));
  return store;
}
function originals(store: WorkspaceStore): string {
  return JSON.stringify([store.get(HandoffWorkPlan, "old-plan"), store.get(HandoffDecision, "old-acceptance"),
    ...["request", "acknowledgement"].map((suffix) => store.get(HandoffMessage, reference("message", WORKSPACE, "continue:old-acceptance", suffix)))]);
}

describe("accepted prose work with prepared quote, committed-turn delivery", () => {
  it("enriches legacy Prepared text and completes seven deliverables over three charges without another order or acceptance", async () => {
    const store = await setup({ enrich: false }), before = originals(store), quoteBefore = store.get(HandoffDocument, QUOTE);
    await intake(store, quoteInput(store.all(HandoffDocument).find((doc) => doc.kind === "Provider information")!.documentId));
    const quoteAfter = store.get(HandoffDocument, QUOTE);
    expect({ ...quoteAfter, detailsJson: undefined }).toEqual({ ...quoteBefore, detailsJson: undefined });
    expect(quoteAfter.sourceKind).toBe("Prepared"); expect(quoteAfter.mediaItemRid).toBeUndefined();
    expect(preparation(quoteAfter)).toEqual({ actorId: PERSON, purpose: "Demonstration configuration", sourceDocumentIds: [QUOTE] });
    expect(MediaSets.MediaSets.readOriginal).not.toHaveBeenCalled();
    await tick(store); expect(store.all(HandoffQuote)).toHaveLength(1); expect(store.all(HandoffFunding)).toHaveLength(0);
    await tick(store); expect(store.all(HandoffFunding)).toHaveLength(1); expect(store.all(HandoffJob)).toHaveLength(0);
    await tick(store); expect(store.all(HandoffJob)).toHaveLength(1); expect(store.all(HandoffJob)[0]?.fundingId).toBeUndefined();
    await until(store, () => store.all(HandoffPayment)[0]?.status === "Settled");
    const job = store.all(HandoffJob)[0]!;
    expect(job).toMatchObject({ status: "Complete", committedCents: "40000", decisionId: "old-acceptance", origin: "Handoff" });
    expect(jobScope(job)).toHaveLength(3);
    expect(jobScope(job).map((line) => line.amountCents)).toEqual(LINES.map((line) => line.amountCents));
    expect(SCOPE.every((term) => jobScope(job).some((line) => line.acceptedScope.includes(term)))).toBe(true);
    expect(store.all(HandoffInvoice)[0]).toMatchObject({ totalCents: "40000", paymentTerms: TERMS, payerPartyId: OWNER });
    expect(Date.parse(store.all(HandoffInvoice)[0]!.dueAt!) - Date.parse(store.all(HandoffInvoice)[0]!.issuedAt!)).toBe(12960 * 60000);
    expect(store.all(HandoffPayment)).toHaveLength(1);
    expect(store.all(HandoffFunding)).toHaveLength(1);
    const report = store.all(HandoffInspection)[0]!;
    expect(OBSERVATIONS.every((text) => report.findingsJson?.includes(text))).toBe(true);
    expect(SCOPE.every((text) => report.findingsJson?.includes(text))).toBe(true);
    expect(store.get(HandoffCase, HANDOFF).physicalProgress).not.toBe("Ready");
    expect(originals(store)).toBe(before); expect(store.all(HandoffWorkPlan)).toHaveLength(1); expect(store.all(HandoffDecision)).toHaveLength(1);
    const outgoing = store.all(HandoffMessage).filter((message) => message.direction === "Outgoing");
    expect(outgoing).toHaveLength(2); expect(outgoing.filter((message) => message.purpose === "Appointment")).toHaveLength(1);
    expect(outgoing.find((message) => message.purpose === "Appointment")?.responseDueAt).toBeDefined();
    const view = JSON.parse(await getHandoffWorkspace(store.client, HANDOFF)) as { jobs: Array<{ scope: object[] }> };
    expect(Object.keys(view.jobs[0]!.scope[0]!).sort()).toEqual(["acceptedScope", "amountCents", "description", "lineId"]);
    const ctx = context(store); ctx.now = store.all(HandoffAgentWork)[0]!.businessTime!;
    expect(await recognizeAcceptedWork(ctx, await loadDetails(ctx.client, ctx.handoff, ctx.workspace, ctx.caller), await loadDeliveryRecords(ctx.client, ctx.workspace, ctx.caller, ctx.handoff))).toBe(false);
    expect(ctx.batch.getEdits()).toHaveLength(0);
  });
  it.each([null, "1000"])("keeps the commitment visible with %s funds, asks about funding and never dispatches payment", async (funds) => {
    const store = await setup({ funds }); const before = originals(store);
    await until(store, () => store.all(HandoffMessage).some((message) => message.direction === "Outgoing" && message.purpose === "Funding"));
    expect(store.all(HandoffJob)).toHaveLength(1); expect(store.all(HandoffPayment)).toHaveLength(0);
    expect(store.all(HandoffJob)[0]?.fundingId).toBeUndefined(); expect(originals(store)).toBe(before);
    const ctx = context(store);
    await expect(requestProviderPayment(ctx, store.all(HandoffJob)[0]!.jobId, "Advance")).rejects.toThrow("owner funding");
    if (funds !== null) await expect(bindExistingJobFunding(ctx, store.all(HandoffJob)[0]!.jobId, store.all(HandoffFunding)[0]!.fundingId)).rejects.toThrow("sufficient current");
    expect(ctx.batch.getEdits()).toHaveLength(0);
    // New actual confirmation wakes and funds this same commitment, not a second approval/order.
    await intake(store, envelope("Owner funding", "later-allocation", { ownerPartyId: OWNER, currency: "USD", confirmedCents: "55000", confirmedAt: NOW, paymentBehavior: "Settle", responseMinutes: 1 }, OWNER));
    await until(store, () => store.all(HandoffPayment)[0]?.status === "Settled");
    expect(store.all(HandoffJob)).toHaveLength(1); expect(originals(store)).toBe(before);
  });
  it.each([{ reports: false }, { accessible: false }])("does not collapse incomplete evidence or inaccessible checks into completion: %j", async (options) => {
    const store = await setup(options);
    await until(store, () => store.all(HandoffJob)[0]?.status === "Awaiting check");
    expect(store.all(HandoffInspection)[0]?.findingsJson).toContain("Not checked");
    expect(store.all(HandoffPayment)).toHaveLength(0);
    expect(store.get(HandoffCase, HANDOFF).physicalProgress).not.toBe("Ready");
  });
  it.each(["omitted term", "new term", "duplicate charge", "missing charge", "unrelated quote", "currency", "requirement", "price"])("fails closed on %s without hiding it through repricing", async (change) => {
    const store = await setup(); await tick(store);
    const mapping = store.all(HandoffDocument).find((doc) => doc.kind === "Accepted work mapping")!;
    const body = JSON.parse(mapping.detailsJson!) as { scope: Array<{ quoteLineId: string; acceptedScopes: string[] }>; quoteDocumentId: string };
    const quote = store.all(HandoffQuote)[0]!;
    if (change === "omitted term") body.scope[2]!.acceptedScopes.pop();
    if (change === "new term") body.scope[2]!.acceptedScopes.push("Replace all equipment.");
    if (change === "duplicate charge") body.scope.push(body.scope[0]!);
    if (change === "missing charge") body.scope.pop();
    if (change === "unrelated quote") body.quoteDocumentId = sourceId("document", "inspection");
    if (change === "currency") store.change(HandoffQuote, quote.quoteId, { currency: "EUR" });
    if (change === "requirement") store.change(HandoffQuote, quote.quoteId, { requirements: [] });
    if (change === "price") store.change(HandoffQuote, quote.quoteId, { totalCents: "39999" });
    store.change(HandoffDocument, mapping.documentId, { detailsJson: JSON.stringify(body) });
    const ctx = context(store);
    await expect(recognizeAcceptedWork(ctx, await loadDetails(ctx.client, ctx.handoff, ctx.workspace, ctx.caller), await loadDeliveryRecords(ctx.client, ctx.workspace, ctx.caller, ctx.handoff))).rejects.toThrow();
    expect(ctx.batch.getEdits()).toHaveLength(0); expect(store.all(HandoffJob)).toHaveLength(0);
  });
  it("rejects Prepared reclassification, invented prices, empty evidence and metadata aliases", async () => {
    const store = await setup({ enrich: false });
    const original = quoteInput(store.all(HandoffDocument).find((doc) => doc.kind === "Provider information")!.documentId);
    await expect(intake(store, { ...original, sourceKind: "Original", mediaSetRid: "arbitrary", mediaItemRid: "file" })).rejects.toThrow("already associated");
    await expect(intake(store, { ...original, sourceSystem: "Invented original publisher" })).rejects.toThrow("unchanged");
    const wrong = JSON.parse(original.detailsJson!) as { offer: { lines: Array<{ amountCents: string }>; totalCents: string }; sourcePassages: string[] };
    wrong.offer.lines[0]!.amountCents = "20000"; wrong.offer.totalCents = "42500";
    await expect(intake(store, { ...original, detailsJson: JSON.stringify(wrong) })).rejects.toThrow("actual verbatim");
    wrong.sourcePassages = [];
    await expect(intake(store, { ...original, detailsJson: JSON.stringify(wrong) })).rejects.toThrow();
    expect(store.get(HandoffDocument, QUOTE).detailsJson).toBeUndefined(); expect(MediaSets.MediaSets.readOriginal).not.toHaveBeenCalled();
  });
  it("normalizes a legacy funding confirmation with missing source metadata exactly once", async () => {
    const store = await setup(); const doc = store.all(HandoffDocument).find((item) => item.kind === "Owner funding")!;
    store.change(HandoffDocument, doc.documentId, { sourceSystem: undefined, sourceRecordId: undefined });
    await tick(store); await tick(store);
    const expected = sourceIdentity("funding", WORKSPACE, { sourceSystem: "Owner funding confirmation", sourceRecordId: doc.documentId });
    expect(store.all(HandoffFunding)[0]?.fundingId).toBe(expected);
    await until(store, () => store.all(HandoffPayment)[0]?.status === "Settled");
    expect(store.all(HandoffFunding)).toHaveLength(1);
    expect(sourceDetails(store.get(HandoffDocument, doc.documentId).detailsJson!).confirmedCents).toBe("80000");
  });
});
