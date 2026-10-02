import { beforeEach, describe, expect, it, vi } from "vitest";
import { Admin, MediaSets } from "@osdk/foundry";
import { Aliases } from "@osdk/functions";
import { HandoffDocument, HandoffFunding, HandoffWorkspace, HandoffCase } from "@ontology/sdk";
import createHandoffWorkspace from "../../functions/createHandoffWorkspace.js";
import receiveMoveOutNotice from "../../functions/receiveMoveOutNotice.js";
import receiveHandoffDocument from "../../functions/receiveHandoffDocument.js";
import { preparedDetails, preparation } from "../sourceAccess.js";
import { loadOwnerFunding, recordOwnerFunding } from "../funding.js";
import { WorkspaceStore, PERSON, MODEL, WORKSPACE, HANDOFF, notice, sourceId } from "./workspaceSupport.js";
import { preparedDelivery, PERSON as DELIVERY_PERSON } from "./deliverySupport.js";
import type { ReceivedDocument } from "../documentIntake.js";

vi.mock("@osdk/foundry", () => ({ Admin: { Users: { getCurrent: vi.fn() } }, MediaSets: { MediaSets: { readOriginal: vi.fn() } } }));
vi.mock("@osdk/functions", async (original) => { const actual = await original<typeof import("@osdk/functions")>();
  return { ...actual, Aliases: { ...actual.Aliases, model: vi.fn() } }; });
beforeEach(() => {
  vi.resetAllMocks();
  vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: PERSON, username: "operator", attributes: {}, realm: "users", status: "ACTIVE" });
  vi.mocked(Aliases.model).mockReturnValue({ rid: MODEL });
  vi.mocked(MediaSets.MediaSets.readOriginal).mockImplementation(async () => new Response("Original file"));
});
async function setup(): Promise<WorkspaceStore> {
  const store = new WorkspaceStore();
  store.apply(await createHandoffWorkspace(store.client, "Property work", "open-workspace", PERSON));
  store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "notice", PERSON));
  return store;
}
function incoming(): ReceivedDocument {
  return { sourceSystem: "Owner books", sourceRecordId: "allocation", sourceVersion: "1", title: "Owner funds", kind: "Owner funding",
    text: "Funds allocated for property work.", partyId: sourceId("party", "owner"), availableFrom: "2026-09-23", sourceKind: "Prepared",
    detailsJson: JSON.stringify({ ownerPartyId: sourceId("party", "owner"), currency: "USD", confirmedCents: "20000", confirmedAt: "2026-09-23T00:00:00.000Z", paymentBehavior: "Settle", responseMinutes: 1 }) };
}
function associated(store: WorkspaceStore): ReceivedDocument {
  const id = sourceId("document", "inspection");
  store.change(HandoffDocument, id, { sourceKind: "Original", mediaSetRid: "protected-collection", mediaItemRid: "protected-file", partyId: sourceId("party", "owner"), sourceVersion: "1" });
  const doc = store.get(HandoffDocument, id);
  return { sourceSystem: doc.sourceSystem!, sourceRecordId: doc.sourceRecordId!, sourceVersion: "1", associatedDocumentId: id,
    title: doc.title!, text: doc.text!, kind: doc.kind!, partyId: doc.partyId!, sourceKind: "Original",
    mediaSetRid: doc.mediaSetRid!, mediaItemRid: doc.mediaItemRid!, availableFrom: store.get(HandoffCase, HANDOFF).businessDate!,
    detailsJson: JSON.stringify({ report: { observation: "The already recorded inspection." } }) };
}
describe("authenticated source setup", () => {
  it("does not let a work user mint a funding confirmation or impersonate a sender through prepared intake", async () => {
    const store = await setup(); store.change(HandoffWorkspace, WORKSPACE, { adminUserIds: [] });
    await expect(receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(incoming()), "forged-funds", PERSON)).rejects.toThrow("permission");
    await expect(receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify({ ...notice(), sourceRecordId: "new" }), "forged-source", PERSON)).rejects.toThrow("permission");
    expect(store.all(HandoffFunding)).toHaveLength(0);
  });
  it("server-records configuration provenance and rejects client-invented provenance", async () => {
    const store = await setup(), input = incoming();
    await expect(receiveHandoffDocument(store.client, HANDOFF, JSON.stringify({ ...input, detailsJson: preparedDetails(input.detailsJson, { id: "someone-else", name: "other" }) }), "forge", PERSON)).rejects.toThrow("server");
    store.apply(await receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(input), "configured", PERSON));
    expect(preparation(store.all(HandoffDocument).find((doc) => doc.kind === "Owner funding")!)).toMatchObject({ actorId: PERSON, purpose: "Demonstration configuration" });
    expect(store.all(HandoffFunding)).toHaveLength(0);
  });
  it("rejects an arbitrary original RID even if the caller could read it", async () => {
    const store = await setup();
    await expect(receiveHandoffDocument(store.client, HANDOFF, JSON.stringify({ ...incoming(), sourceKind: "Original", mediaSetRid: "private", mediaItemRid: "file", associatedDocumentId: "not-associated" }), "arbitrary", PERSON)).rejects.toThrow("already associated");
    expect(MediaSets.MediaSets.readOriginal).not.toHaveBeenCalled();
  });
  it.each(["broader", "narrower"])("rejects a %s audience before fetching an original", async (scope) => {
    const store = await setup(), input = associated(store);
    if (scope === "broader") store.change(HandoffDocument, input.associatedDocumentId!, { readerIds: [PERSON, "other-reader"] });
    else store.change(HandoffWorkspace, WORKSPACE, { readerIds: [PERSON, "other-reader"] });
    await expect(receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(input), "copy", PERSON)).rejects.toThrow("access settings");
    expect(MediaSets.MediaSets.readOriginal).not.toHaveBeenCalled();
  });
  it("fails closed if the actual original is unavailable or denied", async () => {
    const store = await setup(), input = associated(store);
    vi.mocked(MediaSets.MediaSets.readOriginal).mockRejectedValue(new Error("source access denied"));
    await expect(receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(input), "denied", PERSON)).rejects.toThrow("source access denied");
  });
  it("enriches only the existing audience and document identity, without altering original text or source facts", async () => {
    const store = await setup(), input = associated(store), before = store.get(HandoffDocument, input.associatedDocumentId!);
    const edits = await receiveHandoffDocument(store.client, HANDOFF, JSON.stringify(input), "enrich", PERSON);
    expect(MediaSets.MediaSets.readOriginal).toHaveBeenCalledWith(store.client, input.mediaSetRid, input.mediaItemRid);
    const sourceEdits = edits.filter((edit) => edit.type === "updateObject" && edit.obj.$apiName === "HandoffDocument");
    expect(sourceEdits).toHaveLength(1); expect(Object.keys(sourceEdits[0]!.type === "updateObject" ? sourceEdits[0]!.properties : {})).toEqual(["detailsJson"]);
    store.apply(edits); const after = store.get(HandoffDocument, input.associatedDocumentId!);
    expect(after.text).toBe(before.text); expect(after.sourceVersion).toBe(before.sourceVersion); expect(after.readerIds).toEqual(before.readerIds);
    expect(store.all(HandoffDocument)).toHaveLength(3);
    await expect(receiveHandoffDocument(store.client, HANDOFF, JSON.stringify({ ...input, text: "Injected court conclusion" }), "rewrite", PERSON)).rejects.toThrow("unchanged");
    await expect(receiveHandoffDocument(store.client, HANDOFF, JSON.stringify({ ...input, availableFrom: "2020-01-01" }), "backdate", PERSON)).rejects.toThrow("unchanged");
  });
  it("freezes business funding identity and rejects changed amounts, aliases and duplicate allocations", async () => {
    const { store, fundingId } = await preparedDelivery(); const funding = store.all(HandoffFunding)[0]!;
    const request = { sourceSystem: funding.sourceSystem!, sourceRecordId: funding.sourceRecordId!, sourceDocumentId: funding.sourceDocumentId!, title: funding.title!, ownerPartyId: funding.ownerPartyId!, currency: funding.currency!, confirmedCents: funding.confirmedCents!, confirmedAt: funding.confirmedAt! };
    await expect(store.run((context) => recordOwnerFunding(context, { ...request, sourceRecordId: "second-name" }))).rejects.toThrow("without substitutions");
    await expect(store.run((context) => recordOwnerFunding(context, { ...request, confirmedCents: "200000" }))).rejects.toThrow("without substitutions");
    store.put(HandoffFunding, { ...funding, fundingId: "duplicate-allocation" });
    await expect(loadOwnerFunding(store.context(), fundingId)).rejects.toThrow("more than once");
    expect(DELIVERY_PERSON).toBe(store.context().caller.id);
  });
  it("does not add or silently spend a changed version of the same allocation, while retaining outcome reconciliation", async () => {
    const { store, fundingId } = await preparedDelivery();
    const source = store.get(HandoffDocument, "funding-source");
    store.put(HandoffDocument, { ...source, documentId: "funding-source-v2", sourceVersion: "2",
      detailsJson: source.detailsJson!.replace('"confirmedCents":"100000"', '"confirmedCents":"50000"') });
    await expect(loadOwnerFunding(store.context(), fundingId)).rejects.toThrow("allocation has changed");
    expect((await loadOwnerFunding(store.context(), fundingId, false)).funding.fundingId).toBe(fundingId);
    expect(store.all(HandoffFunding)).toHaveLength(1);
  });
});
