import { beforeEach, describe, expect, it, vi } from "vitest";
import { Admin, MediaSets } from "@osdk/foundry";
import { Aliases } from "@osdk/functions";
import { HandoffCase, HandoffDocument, HandoffWorkspace, HandoffAgentWork, HandoffWorkPlan, HandoffDecision } from "@ontology/sdk";
import createHandoffWorkspace from "../../functions/createHandoffWorkspace.js";
import receiveMoveOutNotice from "../../functions/receiveMoveOutNotice.js";
import associateHandoffOriginal from "../../functions/associateHandoffOriginal.js";
import getHandoffWorkspace from "../../functions/getHandoffWorkspace.js";
import { checkDocumentSources } from "../originals.js";
import { readReceivedDocument } from "../documentIntake.js";
import { preparation } from "../sourceAccess.js";
import { loadDetails, workContext } from "../workDetails.js";
import { materialBasis } from "../proposal.js";
import { readMoveOutNotice } from "../notice.js";
import { WorkspaceStore, PERSON, MODEL, WORKSPACE, HANDOFF, notice, sourceId } from "./workspaceSupport.js";
import type { HandoffWorkspaceView } from "../contracts.js";

vi.mock("@osdk/foundry", () => ({ Admin: { Users: { getCurrent: vi.fn() } }, MediaSets: { MediaSets: { readOriginal: vi.fn(), info: vi.fn() } } }));
vi.mock("@osdk/functions", async (original) => { const actual = await original<typeof import("@osdk/functions")>();
  return { ...actual, Aliases: { ...actual.Aliases, model: vi.fn() } }; });
const TARGET = sourceId("document", "inspection");
const FILE = { mediaSetRid: "ri.mio.main.media-set.00000000-0000-0000-0000-000000000001",
  mediaItemRid: "ri.mio.main.media-item.00000000-0000-0000-0000-000000000002", kind: "Reconstructed material" };
beforeEach(() => {
  vi.resetAllMocks();
  vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: PERSON, username: "operator", attributes: {}, realm: "users", status: "ACTIVE" });
  vi.mocked(Aliases.model).mockReturnValue({ rid: MODEL });
  vi.mocked(MediaSets.MediaSets.readOriginal).mockImplementation(async () => new Response("Do not copy this protected body"));
  vi.mocked(MediaSets.MediaSets.info).mockResolvedValue({ viewRid: "media-view", path: "Protected filename.pdf", logicalTimestamp: "12345", mimeType: "application/pdf" });
});
async function setup(): Promise<WorkspaceStore> {
  const store = new WorkspaceStore();
  store.apply(await createHandoffWorkspace(store.client, "Property work", "open-workspace", PERSON));
  store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "notice", PERSON));
  store.change(HandoffDocument, TARGET, { sourceKind: "Prepared" });
  return store;
}
async function attach(store: WorkspaceStore, input = FILE, commandId = "attach"): Promise<void> {
  store.apply(await associateHandoffOriginal(store.client, HANDOFF, TARGET, JSON.stringify(input), store.get(HandoffCase, HANDOFF).revision!, commandId, PERSON));
}
async function view(store: WorkspaceStore): Promise<HandoffWorkspaceView> {
  return JSON.parse(await getHandoffWorkspace(store.client, HANDOFF)) as HandoffWorkspaceView;
}
describe("protected first original association", () => {
  it("creates a separate file identity without copying text or filenames, relabelling the summary, waking work or changing a decision", async () => {
    const store = await setup(), before = store.get(HandoffDocument, TARGET), work = JSON.stringify(store.all(HandoffAgentWork));
    const edits = await associateHandoffOriginal(store.client, HANDOFF, TARGET, JSON.stringify(FILE), "1", "attach", PERSON);
    expect(JSON.stringify(edits)).not.toContain("Protected filename"); expect(JSON.stringify(edits)).not.toContain("Do not copy");
    expect(edits.filter((edit) => edit.type === "updateObject" && edit.obj.$apiName === "HandoffDocument").map((edit) => edit.type === "updateObject" ? Object.keys(edit.properties) : [])).toEqual([["sourceDocumentIds"]]);
    store.apply(edits);
    const original = store.all(HandoffDocument).find((doc) => doc.sourceKind === "Original")!;
    expect(original).toMatchObject({ readerIds: [PERSON], handoffId: HANDOFF, workspaceId: WORKSPACE, sourceVersion: "12345", kind: "Reconstructed material", text: "Open the attached file." });
    expect(preparation(original).actorId).toBe(PERSON);
    expect(store.get(HandoffDocument, TARGET)).toMatchObject({ sourceKind: "Prepared", text: before.text, title: before.title, sourceDocumentIds: [original.documentId] });
    expect(store.get(HandoffDocument, TARGET).mediaItemRid).toBeUndefined();
    expect(JSON.stringify(store.all(HandoffAgentWork))).toBe(work);
    expect(store.all(HandoffWorkPlan)).toHaveLength(0); expect(store.all(HandoffDecision)).toHaveLength(0);
    const result = await view(store);
    expect(result.version).toBe("2");
    expect(result.documents.find((doc) => doc.id === TARGET)).toMatchObject({ sourceKind: "Prepared", sourceDocumentIds: [original.documentId], mediaSetRid: null });
    expect(result.documents.find((doc) => doc.id === original.documentId)).toMatchObject({ sourceKind: "Original", title: "Protected filename.pdf", kind: "Reconstructed material", mediaItemRid: FILE.mediaItemRid });
  });
  it("supports multiple separately readable files, deduplicates repeated association and allows a file to support another prepared document", async () => {
    const store = await setup(); await attach(store);
    await attach(store, { ...FILE, mediaItemRid: "ri.mio.main.media-item.00000000-0000-0000-0000-000000000003", kind: "Archival material" }, "attach-other");
    await attach(store, FILE, "same-new-command");
    const result = await view(store), ids = result.documents.find((doc) => doc.id === TARGET)!.sourceDocumentIds!;
    expect(ids).toHaveLength(2); expect(new Set(ids).size).toBe(2);
    expect(ids.every((id) => result.documents.some((doc) => doc.id === id && doc.sourceKind === "Original"))).toBe(true);
    const other = sourceId("document", "lease"); store.change(HandoffDocument, other, { sourceKind: "Prepared" });
    store.apply(await associateHandoffOriginal(store.client, HANDOFF, other, JSON.stringify(FILE), "3", "other-summary", PERSON));
    expect(store.all(HandoffDocument).filter((doc) => doc.sourceKind === "Original")).toHaveLength(2);
    expect(store.get(HandoffDocument, other).sourceDocumentIds).toHaveLength(1);
  });
  it("rejects worker-only configuration and forged actors before checking source access", async () => {
    const store = await setup(); store.change(HandoffWorkspace, WORKSPACE, { adminUserIds: [] });
    await expect(attach(store)).rejects.toThrow("permission");
    await expect(associateHandoffOriginal(store.client, HANDOFF, TARGET, JSON.stringify(FILE), "1", "forge", "other-user")).rejects.toThrow("signed-in person");
    expect(MediaSets.MediaSets.readOriginal).not.toHaveBeenCalled();
  });
  it.each([{ workspaceId: "other-workspace" }, { handoffId: "other-handoff" }, { readerIds: [PERSON, "extra"] }, { sourceKind: "Original" }])("rejects crossscope or relabelled targets: %j", async (change) => {
    const store = await setup(); store.change(HandoffDocument, TARGET, change);
    await expect(attach(store)).rejects.toThrow(); expect(MediaSets.MediaSets.readOriginal).not.toHaveBeenCalled();
  });
  it("checks stale revision, exact replay and conflicting replay without creating duplicates", async () => {
    const store = await setup(); await attach(store);
    expect(await associateHandoffOriginal(store.client, HANDOFF, TARGET, JSON.stringify(FILE), "1", "attach", PERSON)).toEqual([]);
    await expect(associateHandoffOriginal(store.client, HANDOFF, TARGET, JSON.stringify(FILE), "0", "new-stale", PERSON)).rejects.toThrow("changed");
    await expect(associateHandoffOriginal(store.client, HANDOFF, TARGET, JSON.stringify(FILE), "2", "attach", PERSON)).rejects.toThrow("already used");
    expect(store.all(HandoffDocument).filter((doc) => doc.sourceKind === "Original")).toHaveLength(1);
  });
  it("fails closed on denied sources, revocation on later reads, and replay after revocation", async () => {
    const store = await setup();
    vi.mocked(MediaSets.MediaSets.readOriginal).mockResolvedValueOnce(new Response(null, { status: 403 }));
    await expect(attach(store)).rejects.toThrow("unavailable");
    expect(store.all(HandoffDocument)).toHaveLength(3); await attach(store);
    vi.mocked(MediaSets.MediaSets.readOriginal).mockRejectedValue(new Error("Source access revoked"));
    await expect(view(store)).rejects.toThrow("revoked");
    await expect(associateHandoffOriginal(store.client, HANDOFF, TARGET, JSON.stringify(FILE), "1", "attach", PERSON)).rejects.toThrow("revoked");
  });
  it("validates read access separately for every reader instead of sharing the configurator's grant", async () => {
    const store = await setup(); await attach(store);
    const other = "second-reader";
    const workspace = store.get(HandoffWorkspace, WORKSPACE), handoff = store.get(HandoffCase, HANDOFF);
    vi.mocked(MediaSets.MediaSets.readOriginal).mockRejectedValue(new Error("Reader lacks file permission"));
    // The same workspace audience is not treated as upstream media authorization.
    const shared = [PERSON, other];
    store.change(HandoffWorkspace, WORKSPACE, { readerIds: shared });
    store.all(HandoffDocument).forEach((doc) => store.change(HandoffDocument, doc.documentId, { readerIds: shared }));
    await expect(checkDocumentSources(store.client, handoff, store.get(HandoffWorkspace, WORKSPACE), { id: other, name: "Other" }, store.all(HandoffDocument))).rejects.toThrow("permission");
    expect(workspace.readerIds).toEqual([PERSON]);
  });
  it.each(["other-handoff", "missing", "future", "prepared", "audience"])("rejects broken supporting identities on read: %s", async (failure) => {
    const store = await setup(); await attach(store);
    const original = store.all(HandoffDocument).find((doc) => doc.sourceKind === "Original")!;
    if (failure === "missing") store.change(HandoffDocument, TARGET, { sourceDocumentIds: ["missing"] });
    if (failure === "other-handoff") store.change(HandoffDocument, original.documentId, { handoffId: "elsewhere" });
    if (failure === "future") store.change(HandoffDocument, original.documentId, { availableFrom: "2099-01-01" });
    if (failure === "prepared") store.change(HandoffDocument, original.documentId, { sourceKind: "Prepared" });
    if (failure === "audience") store.change(HandoffDocument, original.documentId, { readerIds: [PERSON, "extra"] });
    await expect(view(store)).rejects.toThrow();
  });
  it("rejects source identity/version changes and authority changes during verification", async () => {
    const store = await setup(); await attach(store);
    vi.mocked(MediaSets.MediaSets.info).mockResolvedValue({ viewRid: "view", logicalTimestamp: "12346", mimeType: "application/pdf" });
    await expect(view(store)).rejects.toThrow("changed");
    await expect(attach(store, FILE, "new")).rejects.toThrow("changed");
    const fresh = await setup();
    vi.mocked(MediaSets.MediaSets.info).mockImplementation(async () => {
      fresh.change(HandoffWorkspace, WORKSPACE, { adminUserIds: [] });
      return { viewRid: "view", logicalTimestamp: "1", mimeType: "application/pdf" };
    });
    await expect(attach(fresh)).rejects.toThrow("permission");
  });
  it("leaves active decisions, planning facts and materiality unchanged by pointer-only attachments", async () => {
    const store = await setup(), caller = { id: PERSON, name: "Operator" };
    store.put(HandoffWorkPlan, { workPlanId: "active-plan", handoffId: HANDOFF, workspaceId: WORKSPACE, readerIds: [PERSON], status: "Accepted", revision: "4" });
    store.put(HandoffDecision, { decisionId: "active-decision", handoffId: HANDOFF, workspaceId: WORKSPACE, readerIds: [PERSON], acceptedRevision: "4" });
    store.change(HandoffCase, HANDOFF, { workPlanId: "active-plan", operativeDecisionId: "active-decision" });
    const handoff = store.get(HandoffCase, HANDOFF), workspace = store.get(HandoffWorkspace, WORKSPACE);
    const before = await loadDetails(store.client, handoff, workspace, caller);
    const decisions = JSON.stringify(store.all(HandoffDecision)), plans = JSON.stringify(store.all(HandoffWorkPlan));
    await attach(store);
    const after = await loadDetails(store.client, store.get(HandoffCase, HANDOFF), store.get(HandoffWorkspace, WORKSPACE), caller);
    expect(after.supportingFiles).toHaveLength(1);
    expect(materialBasis(handoff, workspace, after)).toBe(materialBasis(handoff, workspace, before));
    expect(workContext(handoff, workspace, after)).toEqual(workContext(handoff, workspace, before));
    expect(JSON.stringify(store.all(HandoffDecision))).toBe(decisions); expect(JSON.stringify(store.all(HandoffWorkPlan))).toBe(plans);
    expect(store.get(HandoffCase, HANDOFF)).toMatchObject({ workPlanId: "active-plan", operativeDecisionId: "active-decision" });
  });
  it("enforces the reference bound and rejects invalid source metadata", async () => {
    const store = await setup(); await attach(store);
    store.change(HandoffDocument, TARGET, { sourceDocumentIds: Array.from({ length: 33 }, (_, i) => `source-${i}`) });
    await expect(view(store)).rejects.toThrow("between 0 and 32");
    const fresh = await setup();
    vi.mocked(MediaSets.MediaSets.info).mockResolvedValue({ viewRid: "view", logicalTimestamp: "12345", mimeType: "text/plain" });
    await expect(attach(fresh)).rejects.toThrow("PDF");
    vi.mocked(MediaSets.MediaSets.info).mockResolvedValue({ viewRid: "view", logicalTimestamp: "not-a-version", mimeType: "application/pdf" });
    await expect(attach(fresh)).rejects.toThrow("stored version");
  });
  it("rejects source text, identity, audience and extraction assertions in the bootstrap input", async () => {
    const store = await setup();
    for (const extra of [{ text: "fabricated extracted content" }, { title: "invented" }, { sourceDocumentIds: [] }, { readerIds: [PERSON] }, { actorId: PERSON }, { pageStart: 1 }]) {
      await expect(associateHandoffOriginal(store.client, HANDOFF, TARGET, JSON.stringify({ ...FILE, ...extra }), "1", "forge", PERSON)).rejects.toThrow("unexpected");
    }
    expect(MediaSets.MediaSets.readOriginal).not.toHaveBeenCalled();
    expect(() => readMoveOutNotice(JSON.stringify({ ...notice(), documents: notice().documents.map((doc) => ({ ...doc, sourceDocumentIds: ["forged"] })) }))).toThrow();
    expect(() => readReceivedDocument(JSON.stringify({ sourceDocumentIds: ["forged"] }))).toThrow();
  });
});
