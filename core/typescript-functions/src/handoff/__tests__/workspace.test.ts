import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Admin } from "@osdk/foundry";
import { Aliases } from "@osdk/functions";
import { HandoffWorkspace, HandoffCase, HandoffProperty, HandoffParty, HandoffDocument, HandoffAgreement,
  HandoffObligation, HandoffWorkPlan, HandoffAgentWork, HandoffDecision, HandoffMessage, HandoffActivity } from "@ontology/sdk";
import createHandoffWorkspace from "../../functions/createHandoffWorkspace.js";
import receiveMoveOutNotice from "../../functions/receiveMoveOutNotice.js";
import prepareHandoffWorkPlan from "../../functions/prepareHandoffWorkPlan.js";
import changeHandoffWorkPlan from "../../functions/changeHandoffWorkPlan.js";
import acceptHandoffWorkPlan from "../../functions/acceptHandoffWorkPlan.js";
import { continueWork as continueHandoff } from "../correspondence.js";
import listHandoffs from "../../functions/listHandoffs.js";
import getHandoffWorkspace from "../../functions/getHandoffWorkspace.js";
import * as reasoner from "../reasoner.js";
import { readMoveOutNotice } from "../notice.js";
import { digest, reference } from "../values.js";
import { handoffUnchanged } from "../records.js";
import { loadDetails, workContext } from "../workDetails.js";
import { acceptedContent } from "../workPlans.js";
import type { HandoffWorkspaceView, HandoffList } from "../contracts.js";
import { WorkspaceStore, PERSON, MODEL, WORKSPACE, HANDOFF, seedQuotedWork, notice, proposedWork, sourceId, workModel } from "./workspaceSupport.js";

vi.mock("@osdk/foundry", () => ({ Admin: { Users: { getCurrent: vi.fn() } } }));
vi.mock("@osdk/functions", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@osdk/functions")>();
  return { ...actual, Aliases: { ...actual.Aliases, model: vi.fn() } };
});

beforeEach(() => {
  vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: PERSON, username: "morgan", givenName: "Morgan", familyName: "Reed", attributes: {}, realm: "workspace-users", status: "ACTIVE" });
  vi.mocked(Aliases.model).mockReturnValue({ rid: MODEL });
});
afterEach(() => vi.restoreAllMocks());

async function opened(): Promise<WorkspaceStore> {
  const store = new WorkspaceStore();
  store.apply(await createHandoffWorkspace(store.client, "Meadow homes", "open-workspace", PERSON));
  return store;
}
async function received(): Promise<WorkspaceStore> {
  const store = await opened();
  store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "receive-notice", PERSON));
  seedQuotedWork(store);
  return store;
}
async function prepared(): Promise<WorkspaceStore> {
  const store = await received();
  seedQuotedWork(store);
  vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(workModel());
  store.apply(await prepareHandoffWorkPlan(store.client, HANDOFF, "prepare-plan", PERSON));
  return store;
}
function planId(store: WorkspaceStore): string { return store.get(HandoffCase, HANDOFF).workPlanId!; }
async function accepted(): Promise<WorkspaceStore> {
  const store = await prepared();
  store.apply(await acceptHandoffWorkPlan(store.client, planId(store), "1", "accept-plan", PERSON));
  return store;
}

describe("opening a workspace and receiving notices", () => {
  it("opens only a new workspace with grants for the signed-in person and supports an exact repeat", async () => {
    const store = await opened();
    expect(store.get(HandoffWorkspace, WORKSPACE)).toMatchObject({ name: "Meadow homes", mode: "demo", currency: "USD",
      readerIds: [PERSON], workUserIds: [PERSON], decideUserIds: [PERSON], adminUserIds: [PERSON], modelRid: MODEL, revision: "1" });
    expect(await createHandoffWorkspace(store.client, "Meadow homes", "open-workspace", PERSON)).toEqual([]);
    await expect(createHandoffWorkspace(store.client, "Different homes", "open-workspace", PERSON)).rejects.toThrow("already used");
  });
  it("rejects a supplied identity that is not the signed-in person before querying any workspace", async () => {
    const store = new WorkspaceStore();
    await expect(createHandoffWorkspace(store.client, "Other workspace", "open-other", "someone-else")).rejects.toThrow("signed-in person");
    expect(store.calls).toEqual([]);
  });
  it("creates scoped business records and resolves document providers and every reference without making a plan", async () => {
    const store = await received();
    expect(store.all(HandoffWorkPlan)).toHaveLength(0);
    expect(store.get(HandoffCase, HANDOFF)).toMatchObject({ propertyId: sourceId("property", "home-1"),
      tenancyId: sourceId("tenancy", "tenancy-1"), revision: "1", physicalProgress: "Preparing plan", financialProgress: "Not started" });
    expect(store.get(HandoffDocument, sourceId("document", "quote"))).toMatchObject({ kind: "Quote", partyId: sourceId("party", "provider"), sourceKind: "Source" });
    expect(store.get(HandoffAgreement, sourceId("agreement", "terms"))).toMatchObject({ sourceDocumentId: sourceId("document", "lease") });
    expect(store.get(HandoffObligation, sourceId("obligation", "retain"))).toMatchObject({ basisAgreementId: sourceId("agreement", "terms"), responsiblePartyIds: [sourceId("party", "owner")] });
    expect(store.all(HandoffAgentWork)[0]).toMatchObject({ status: "Plan requested", operationKey: `prepare:${HANDOFF}` });
    [HandoffCase, HandoffProperty, HandoffParty, HandoffDocument].forEach((type) => {
      store.all(type).forEach((record) => expect(record).toMatchObject({ workspaceId: WORKSPACE, readerIds: [PERSON] }));
    });
    expect(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "receive-notice", PERSON)).toEqual([]);
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify({ ...notice(), goal: "A different goal" }), "receive-notice", PERSON)).rejects.toThrow("already used");
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "different-request", PERSON)).rejects.toThrow("already been received");
  });
  it("retains explicit handoff requirements and treats changes as different notice intent", async () => {
    const store = await opened();
    const input = { ...notice(), fixedRequirements: ["Keep serviceable fittings."] };
    const json = JSON.stringify(input);
    store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, json, "receive-notice", PERSON));
    expect(store.get(HandoffCase, HANDOFF).fixedRequirements).toEqual(input.fixedRequirements);
    expect(await receiveMoveOutNotice(store.client, WORKSPACE, json, "receive-notice", PERSON)).toEqual([]);
    await Promise.all([[], ["Retain the entrance door."]].map(async (fixedRequirements): Promise<void> => {
      await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify({ ...input, fixedRequirements }),
        "receive-notice", PERSON)).rejects.toThrow("already used");
    }));
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()),
      "receive-notice", PERSON)).rejects.toThrow("already used");
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, json, "another-request", PERSON)).rejects.toThrow("already been received");
    seedQuotedWork(store);
    const provider = workModel();
    vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(provider);
    store.apply(await prepareHandoffWorkPlan(store.client, HANDOFF, "prepare-plan", PERSON));
    const supplied: reasoner.WorkContext = JSON.parse(String(provider.requests[0]?.messages.find((message) => message.role === "user")?.content));
    expect(supplied.fixedRequirements).toEqual(input.fixedRequirements);
    expect(store.get(HandoffWorkPlan, planId(store)).fixedRequirements).toEqual(expect.arrayContaining(input.fixedRequirements));
  });
  it("keeps earlier notice hashes and absent requirements compatible without updating the handoff", async () => {
    const store = await received();
    const receipt = store.all(HandoffActivity).find((entry) => entry.kind === "Notice received")!;
    const saved: { payloadHash: string } = JSON.parse(receipt.detail!);
    expect(saved.payloadHash).toBe(digest(notice()));
    expect(store.get(HandoffCase, HANDOFF).fixedRequirements).toEqual([]);
    store.change(HandoffCase, HANDOFF, { fixedRequirements: undefined });
    expect(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "receive-notice", PERSON)).toEqual([]);
    expect(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify({ ...notice(), fixedRequirements: [] }),
      "receive-notice", PERSON)).toEqual([]);
    expect(store.get(HandoffCase, HANDOFF).fixedRequirements).toBeUndefined();
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify({ ...notice(), fixedRequirements: ["Keep the entrance door."] }),
      "receive-notice", PERSON)).rejects.toThrow("already used");
  });
  it("requires work permission and rejects cross-workspace access", async () => {
    const store = await opened();
    store.change(HandoffWorkspace, WORKSPACE, { workUserIds: [] });
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "receive", PERSON)).rejects.toThrow("permission");
    store.change(HandoffWorkspace, WORKSPACE, { workUserIds: [PERSON], readerIds: ["other-person"] });
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "receive", PERSON)).rejects.toThrow("not available");
  });
  it("retains shared source records only if their business values match", async () => {
    const store = await received();
    const second = notice();
    second.sourceRecordId = "notice-2";
    second.documents.forEach((doc) => { doc.sourceId += "-second"; });
    second.agreements = [];
    second.obligations = [];
    const edits = await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(second), "receive-second", PERSON);
    expect(edits.some((edit) => edit.type === "createObject" && edit.obj.apiName === "HandoffProperty")).toBe(false);
    second.property.address = "Different address";
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(second), "receive-second", PERSON)).rejects.toThrow("different details");
  });
  it("keeps source identifiers separate across workspaces", async () => {
    const store = await received();
    store.apply(await createHandoffWorkspace(store.client, "Other homes", "open-other", PERSON));
    const other = reference("workspace", PERSON, "open-other");
    store.apply(await receiveMoveOutNotice(store.client, other, JSON.stringify(notice()), "receive-notice", PERSON));
    expect(store.all(HandoffCase)).toHaveLength(2);
    expect(new Set(store.all(HandoffProperty).map((record) => record.propertyId)).size).toBe(2);
  });
});

describe("notice validation", () => {
  it("accepts the defined adapter shape without unbounded or unknown fields", () => {
    expect(readMoveOutNotice(JSON.stringify(notice()))).toEqual({ ...notice(), tenancy: { ...notice().tenancy, endingKind: "Tenancy ending" }, fixedRequirements: [] });
    expect(() => readMoveOutNotice("not json")).toThrow("format");
    expect(() => readMoveOutNotice(JSON.stringify({ ...notice(), readerIds: ["other"] }))).toThrow("unexpected");
    const input = notice();
    input.documents[0]!.text = "x".repeat(24001);
    expect(() => readMoveOutNotice(JSON.stringify(input))).toThrow("size limit");
  });
  it("accepts empty or bounded explicit requirements without deriving them from obligations", () => {
    expect(readMoveOutNotice(JSON.stringify({ ...notice(), fixedRequirements: [] })).fixedRequirements).toEqual([]);
    const fixedRequirements = Array.from({ length: 24 }, (_, index) => `${index.toString().padStart(2, "0")}${"x".repeat(998)}`);
    expect(readMoveOutNotice(JSON.stringify({ ...notice(), fixedRequirements })).fixedRequirements).toEqual(fixedRequirements);
  });
  it.each([null, "Keep the entrance door.", [null], [""], [" Extra spaces "], ["Same", "Same"],
    ["x".repeat(1001)], Array.from({ length: 25 }, (_, index) => `Condition ${index}`)]
    .map((fixedRequirements, index) => ({ fixedRequirements, index })))
    ("rejects malformed or excessive requirements $index", ({ fixedRequirements }) => {
      expect(() => readMoveOutNotice(JSON.stringify({ ...notice(), fixedRequirements }))).toThrow("Requirements");
    });
  it("rejects missing references, duplicate source keys, invalid dates and unsupported source pages", () => {
    const missing = notice(); missing.tenancy.landlordPartySourceId = "missing";
    expect(() => readMoveOutNotice(JSON.stringify(missing))).toThrow("Every referenced");
    const duplicate = notice(); duplicate.parties.push({ ...duplicate.parties[0]! });
    expect(() => readMoveOutNotice(JSON.stringify(duplicate))).toThrow("different source");
    const date = notice(); date.businessDate = "2026-02-30";
    expect(() => readMoveOutNotice(JSON.stringify(date))).toThrow("calendar date");
    const pages = notice(); pages.documents[0]!.pageStart = 0;
    expect(() => readMoveOutNotice(JSON.stringify(pages))).toThrow("positive whole");
    const quote = notice(); delete quote.documents[2]!.partySourceId;
    expect(() => readMoveOutNotice(JSON.stringify(quote))).toThrow("party offering");
    expect(() => readMoveOutNotice(JSON.stringify({ ...notice(), workPlan: proposedWork() }))).toThrow("unexpected");
  });
});

describe("work recommendations and authority", () => {
  it("reads actual records and stores the tool-checked model proposal without a pre-assigned budget", async () => {
    const store = await received();
    const provider = workModel();
    vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(provider);
    const caseBefore = store.get(HandoffCase, HANDOFF), workspaceBefore = store.get(HandoffWorkspace, WORKSPACE);
    const edits = await prepareHandoffWorkPlan(store.client, HANDOFF, "prepare-plan", PERSON);
    expect(edits.some((edit) => edit.type === "updateObject" && edit.obj === caseBefore)).toBe(true);
    expect(edits.some((edit) => edit.type === "updateObject" && edit.obj === workspaceBefore)).toBe(true);
    store.apply(edits);
    expect(store.get(HandoffWorkPlan, planId(store))).toMatchObject({ ...proposedWork(), fixedRequirements: [], status: "Ready", revision: "1", basisRevision: "2" });
    const initial = JSON.stringify(provider.requests[0]?.messages);
    expect(initial).not.toContain('"budgetCents"');
    expect(initial).not.toContain('"budgetLimitCents"');
    expect(JSON.stringify(provider.requests[1]?.messages)).toContain(notice().documents[2]!.text);
    expect(provider.requests).toHaveLength(3);
    expect(await prepareHandoffWorkPlan(store.client, HANDOFF, "prepare-plan", PERSON)).toEqual([]);
    expect(provider.requests).toHaveLength(3);
  });
  it.each(["Completed", "Performed", "Assessed", "Being assessed", "Open", "Cancelled"])("keeps %s obligations as context, not fixed requirements", async (status) => {
    const store = await received();
    store.change(HandoffCase, HANDOFF, { fixedRequirements: undefined });
    store.change(HandoffObligation, sourceId("obligation", "retain"), { status });
    const handoff = store.get(HandoffCase, HANDOFF), workspace = store.get(HandoffWorkspace, WORKSPACE);
    const details = await loadDetails(store.client, handoff, workspace, { id: PERSON, name: "Morgan Reed" });
    const context = workContext(handoff, workspace, details);
    expect(context.fixedRequirements).toEqual([]);
    expect(context.obligations).toEqual([`Retain serviceable fittings: Keep serviceable fittings.. Status: ${status}.`]);
    expect(context.agreements[0]).toContain(notice().agreements[0]!.termsText);
    expect(context.documents.find((document) => document.kind === "Agreement")?.body).toBe(notice().documents[0]!.text);
    store.change(HandoffCase, HANDOFF, { fixedRequirements: ["Retain the entrance door."] });
    expect(workContext(store.get(HandoffCase, HANDOFF), workspace, details).fixedRequirements).toEqual(["Retain the entrance door."]);
  });
  it("treats a requirement change during preparation as material even without a revision change", async () => {
    const store = await received();
    vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(workModel(() => {
      store.change(HandoffCase, HANDOFF, { fixedRequirements: ["Retain the entrance door."] });
    }));
    await expect(prepareHandoffWorkPlan(store.client, HANDOFF, "prepare", PERSON)).rejects.toThrow("changed while");
    expect(store.all(HandoffWorkPlan)).toHaveLength(0);
  });
  it("treats absent and empty requirements alike in case coherence checks", async () => {
    const store = await received();
    const before = store.get(HandoffCase, HANDOFF);
    store.change(HandoffCase, HANDOFF, { fixedRequirements: undefined });
    expect(handoffUnchanged(before, store.get(HandoffCase, HANDOFF))).toBe(true);
  });
  it("checks permission and scope before the model call", async () => {
    const store = await received();
    const factory = vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(workModel());
    store.change(HandoffWorkspace, WORKSPACE, { workUserIds: [] });
    await expect(prepareHandoffWorkPlan(store.client, HANDOFF, "prepare", PERSON)).rejects.toThrow("permission");
    store.change(HandoffWorkspace, WORKSPACE, { workUserIds: [PERSON] });
    store.change(HandoffProperty, sourceId("property", "home-1"), { workspaceId: "different-workspace" });
    await expect(prepareHandoffWorkPlan(store.client, HANDOFF, "prepare", PERSON)).rejects.toThrow("not available in this workspace");
    expect(factory).not.toHaveBeenCalled();
  });
  it("rejects a permission change while the model is running", async () => {
    const store = await received();
    vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(workModel(() => store.change(HandoffWorkspace, WORKSPACE, { workUserIds: [] })));
    await expect(prepareHandoffWorkPlan(store.client, HANDOFF, "prepare", PERSON)).rejects.toThrow("permission");
    expect(store.all(HandoffWorkPlan)).toHaveLength(0);
  });
  it("rejects a material business-date change while the model is running", async () => {
    const store = await received();
    vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(workModel(() => store.change(HandoffCase, HANDOFF, { businessDate: "2026-09-23" })));
    await expect(prepareHandoffWorkPlan(store.client, HANDOFF, "prepare", PERSON)).rejects.toThrow("changed while");
    expect(store.all(HandoffWorkPlan)).toHaveLength(0);
  });
});

describe("budget changes and acceptance", () => {
  it("changes only the budget, rejects stale requests, and remembers an exact old repeat after later changes", async () => {
    const store = await prepared();
    const id = planId(store);
    const scope = store.get(HandoffWorkPlan, id).scope;
    await expect(changeHandoffWorkPlan(store.client, id, "0", "budget-stale", PERSON, "26000")).rejects.toThrow("has changed");
    await expect(changeHandoffWorkPlan(store.client, id, "1", "budget-small", PERSON, "10000")).rejects.toThrow("budget must cover");
    store.apply(await changeHandoffWorkPlan(store.client, id, "1", "budget-one", PERSON, "26000"));
    store.apply(await changeHandoffWorkPlan(store.client, id, "2", "budget-two", PERSON, "27000"));
    expect(store.get(HandoffWorkPlan, id)).toMatchObject({ revision: "3", budgetCents: "27000", scope });
    expect(await changeHandoffWorkPlan(store.client, id, "1", "budget-one", PERSON, "26000")).toEqual([]);
    await expect(changeHandoffWorkPlan(store.client, id, "1", "budget-one", PERSON, "28000")).rejects.toThrow("already used");
    expect(reasoner.createFoundryWorkModel).toHaveBeenCalledTimes(1);
  });
  it("requires decision permission even if work is allowed, including old repeats", async () => {
    const store = await prepared();
    const id = planId(store);
    store.apply(await changeHandoffWorkPlan(store.client, id, "1", "budget-one", PERSON, "26000"));
    store.change(HandoffWorkspace, WORKSPACE, { decideUserIds: [] });
    await expect(changeHandoffWorkPlan(store.client, id, "1", "budget-one", PERSON, "26000")).rejects.toThrow("permission");
    await expect(acceptHandoffWorkPlan(store.client, id, "2", "accept", PERSON)).rejects.toThrow("permission");
  });
  it("snapshots exactly the accepted proposal and queues continuation without completing work", async () => {
    const store = await prepared();
    const id = planId(store), before = store.get(HandoffWorkPlan, id);
    await expect(acceptHandoffWorkPlan(store.client, id, "0", "stale", PERSON)).rejects.toThrow("has changed");
    const edits = await acceptHandoffWorkPlan(store.client, id, "1", "accept-plan", PERSON);
    expect(edits.some((edit) => edit.type === "updateObject" && edit.obj === before)).toBe(true);
    store.apply(edits);
    expect(store.all(HandoffDecision)[0]).toMatchObject({ acceptedRevision: "1", contentJson: acceptedContent(before), decidedBy: PERSON });
    expect(store.get(HandoffCase, HANDOFF)).toMatchObject({ physicalProgress: "Arranging work", financialProgress: "Not started" });
    expect(store.all(HandoffAgentWork)[0]).toMatchObject({ status: "Ready to continue", operationKey: `continue:${store.all(HandoffDecision)[0]!.decisionId}` });
    expect(await acceptHandoffWorkPlan(store.client, id, "1", "accept-plan", PERSON)).toEqual([]);
    const original = store.get(HandoffWorkPlan, id);
    const changed = await changeHandoffWorkPlan(store.client, id, "1", "budget-late", PERSON, "26000");
    expect(changed.some((edit) => edit.type === "createObject" && edit.obj.apiName === "HandoffWorkPlan")).toBe(true);
    expect(store.get(HandoffWorkPlan, id)).toBe(original);
    await expect(acceptHandoffWorkPlan(store.client, id, "1", "accept-again", PERSON)).rejects.toThrow("already been accepted");
  });
});

describe("recognizing earlier accepted correspondence", () => {
  it("records one outgoing request and an acknowledgement and deduplicates different request references", async () => {
    const store = await accepted();
    const first = await continueHandoff(store.client, HANDOFF, "continue-one", PERSON);
    store.apply(first);
    expect(store.all(HandoffMessage)).toHaveLength(2);
    expect(store.all(HandoffMessage).find((message) => message.direction === "Outgoing")).toMatchObject({
      recipientPartyId: sourceId("party", "provider"), status: "Sent" });
    expect(store.all(HandoffMessage).find((message) => message.direction === "Incoming")!.body).toContain("Scheduling confirmation is still pending");
    expect(store.all(HandoffAgentWork)[0]).toMatchObject({ status: "Waiting for provider" });
    expect(Date.parse(store.all(HandoffAgentWork)[0]!.nextWakeAt!)).toBeGreaterThan(Date.parse(store.all(HandoffAgentWork)[0]!.updatedAt!));
    expect(await continueHandoff(store.client, HANDOFF, "continue-one", PERSON)).toEqual([]);
    expect(await continueHandoff(store.client, HANDOFF, "continue-other", PERSON)).toEqual([]);
    expect(store.all(HandoffMessage)).toHaveLength(2);
    expect(store.get(HandoffCase, HANDOFF).financialProgress).toBe("Not started");
  });
  it("requires an accepted plan and refuses a changed decision binding or unsupported workspace", async () => {
    const store = await prepared();
    await expect(continueHandoff(store.client, HANDOFF, "continue", PERSON)).rejects.toThrow("Accept a work plan");
    store.apply(await acceptHandoffWorkPlan(store.client, planId(store), "1", "accept", PERSON));
    store.change(HandoffWorkPlan, planId(store), { budgetCents: "99999" });
    await expect(continueHandoff(store.client, HANDOFF, "continue", PERSON)).rejects.toThrow("no longer matches");
    store.change(HandoffWorkspace, WORKSPACE, { mode: "live" });
    await expect(continueHandoff(store.client, HANDOFF, "continue", PERSON)).rejects.toThrow("not set up");
    expect(store.all(HandoffMessage)).toHaveLength(0);
  });
});

describe("workspace views", () => {
  it("returns coherent business JSON with decimal money and no authority or model execution details", async () => {
    const store = await accepted();
    store.apply(await continueHandoff(store.client, HANDOFF, "continue", PERSON));
    const view: HandoffWorkspaceView = JSON.parse(await getHandoffWorkspace(store.client, HANDOFF));
    expect(view.version).toBe("2");
    expect(view.workPlan).toMatchObject({ budgetCents: "25000", estimatedCostCents: "20500", revision: "1", status: "Accepted" });
    expect(view.decisions[0]).toMatchObject({ by: "Morgan Reed", revision: "1", budgetCents: "25000" });
    expect(view.agent.status).toBe("Waiting for provider");
    expect(view.documents.every((document) => document.mediaSetRid === null && document.pageStart === null)).toBe(true);
    expect(view.permissions).toEqual({ canWork: true, canDecide: true, canConfigure: true });
    expect(JSON.stringify(view)).not.toMatch(/signed-in-person|payloadHash|toolCallCount|usedDocumentIds|readerIds|lastCommandId/);
    const list: HandoffList = JSON.parse(await listHandoffs(store.client, WORKSPACE));
    expect(list.handoffs).toHaveLength(1);
    expect(list.handoffs[0]).toMatchObject({ id: HANDOFF, propertyName: "Garden house", physicalProgress: "Waiting for provider" });
    expect(store.all(HandoffActivity).some((activity) => activity.detail?.includes("toolCallCount"))).toBe(true);
  });
  it("derives actual read identity and rejects unscoped related records", async () => {
    const store = await received();
    vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: "other-person", username: "other", attributes: {}, realm: "workspace-users", status: "ACTIVE" });
    await expect(getHandoffWorkspace(store.client, HANDOFF)).rejects.toThrow("not available");
    await expect(listHandoffs(store.client, WORKSPACE)).rejects.toThrow("not available");
    vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: PERSON, username: "morgan", attributes: {}, realm: "workspace-users", status: "ACTIVE" });
    store.change(HandoffParty, sourceId("party", "provider"), { readerIds: ["other-person"] });
    await expect(getHandoffWorkspace(store.client, HANDOFF)).rejects.toThrow("not available in this workspace");
  });
  it("does not broaden source visibility when workspace readers change", async () => {
    const store = await received();
    store.change(HandoffWorkspace, WORKSPACE, { readerIds: [PERSON, "new-reader"] });
    await expect(getHandoffWorkspace(store.client, HANDOFF)).rejects.toThrow("different access settings");
    const factory = vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(workModel());
    await expect(prepareHandoffWorkPlan(store.client, HANDOFF, "prepare", PERSON)).rejects.toThrow("different access settings");
    expect(factory).not.toHaveBeenCalled();
  });
  it("reads an agreement's source document without including other unlinked documents", async () => {
    const store = await received();
    const second = notice();
    second.sourceRecordId = "notice-2";
    second.documents.forEach((document) => { document.sourceId += "-second"; });
    second.agreements = [];
    second.obligations = [];
    store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(second), "second-notice", PERSON));
    const view: HandoffWorkspaceView = JSON.parse(await getHandoffWorkspace(store.client, sourceId("handoff", "notice-2")));
    expect(view.documents.map((document) => document.id)).toContain(sourceId("document", "lease"));
    expect(view.documents.map((document) => document.id)).not.toContain(sourceId("document", "inspection"));
    expect(view.documents).toHaveLength(4);
  });
  it("returns a bounded first list page", async () => {
    const store = await received();
    const original = store.get(HandoffCase, HANDOFF);
    Array.from({ length: 30 }, (_, index) => `handoff-${index.toString().padStart(2, "0")}`).forEach((handoffId) => {
      store.put(HandoffCase, { handoffId, workspaceId: WORKSPACE, readerIds: [PERSON], propertyId: original.propertyId,
        title: `House return ${handoffId.slice(-2)}`, physicalProgress: "Preparing plan", financialProgress: "Not started", nextStep: "Prepare the work plan.", revision: "1" });
    });
    const list: HandoffList = JSON.parse(await listHandoffs(store.client, WORKSPACE));
    expect(list.handoffs).toHaveLength(25);
    expect(list.handoffs[0]?.id).toBe("handoff-00");
    expect(list.handoffs[24]?.id).toBe("handoff-24");
  });
  it("does not expose the case requirements through a new DTO field and detects changes during reads", async () => {
    const store = await received();
    store.change(HandoffCase, HANDOFF, { fixedRequirements: ["Retain the entrance door."] });
    const view: HandoffWorkspaceView = JSON.parse(await getHandoffWorkspace(store.client, HANDOFF));
    expect(view.handoff).not.toHaveProperty("fixedRequirements");
    store.onRead = (type): void => {
      if (type.apiName === "HandoffDocument") store.change(HandoffCase, HANDOFF, { fixedRequirements: ["Keep the timber frame."] });
    };
    await expect(getHandoffWorkspace(store.client, HANDOFF)).rejects.toThrow("changed while it was being read");
  });
  it("refuses a mixed read if the handoff changes while related records load", async () => {
    const store = await received();
    store.onRead = (type): void => { if (type.apiName === "HandoffDocument") store.change(HandoffCase, HANDOFF, { revision: "2" }); };
    await expect(getHandoffWorkspace(store.client, HANDOFF)).rejects.toThrow("changed while it was being read");
  });
});
