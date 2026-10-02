import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Admin } from "@osdk/foundry";
import { Aliases } from "@osdk/functions";
import { HandoffActivity, HandoffCase, HandoffDocument, HandoffWorkspace } from "@ontology/sdk";
import createHandoffWorkspace from "../../functions/createHandoffWorkspace.js";
import receiveMoveOutNotice from "../../functions/receiveMoveOutNotice.js";
import getHandoffWorkspace from "../../functions/getHandoffWorkspace.js";
import setHandoffAccess from "../../functions/setHandoffAccess.js";
import { WorkspaceStore, PERSON, MODEL, WORKSPACE, HANDOFF, notice } from "./workspaceSupport.js";

vi.mock("@osdk/foundry", () => ({ Admin: { Users: { getCurrent: vi.fn(), get: vi.fn(), } } }));
vi.mock("@osdk/functions", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@osdk/functions")>();
  return { ...actual, Aliases: { ...actual.Aliases, model: vi.fn() } };
});

const PARTNER = "co-founder";
const people = {
  [PERSON]: { id: PERSON, username: "morgan", givenName: "Morgan", familyName: "Reed", attributes: {}, realm: "users", status: "ACTIVE" as const },
  [PARTNER]: { id: PARTNER, username: "sam", givenName: "Sam", familyName: "Ortiz", attributes: {}, realm: "users", status: "ACTIVE" as const },
};
function signedIn(id: keyof typeof people): void {
  vi.mocked(Admin.Users.getCurrent).mockResolvedValue(people[id]);
}
beforeEach(() => {
  signedIn(PERSON);
  vi.mocked(Admin.Users.get).mockImplementation(async (_client, id) => {
    const user = people[id as keyof typeof people];
    if (!user) throw new Error("User not found");
    return user;
  });
  vi.mocked(Aliases.model).mockReturnValue({ rid: MODEL });
});
afterEach(() => vi.restoreAllMocks());

async function workspace(): Promise<WorkspaceStore> {
  const store = new WorkspaceStore();
  store.apply(await createHandoffWorkspace(store.client, "Meadow homes", "open-workspace", PERSON));
  store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "receive-notice", PERSON));
  return store;
}

describe("teammates", () => {
  it("lets an admin add a teammate, who can then open the workspace, and remove them again", async () => {
    const store = await workspace();
    signedIn(PARTNER);
    await expect(getHandoffWorkspace(store.client, HANDOFF)).rejects.toThrow(/not available/);
    signedIn(PERSON);
    store.apply(await setHandoffAccess(store.client, WORKSPACE, PARTNER, "Work", "add-sam", PERSON));
    const ws = store.get(HandoffWorkspace, WORKSPACE);
    expect([ws.readerIds, ws.workUserIds, ws.decideUserIds, ws.adminUserIds]).toEqual([[PERSON, PARTNER], [PERSON, PARTNER], [PERSON], [PERSON]]);
    expect(store.all(HandoffDocument).every((doc) => JSON.stringify(doc.readerIds) === JSON.stringify([PERSON, PARTNER]))).toBe(true);
    expect(store.get(HandoffCase, HANDOFF).readerIds).toEqual([PERSON, PARTNER]);
    expect(JSON.stringify(store.all(HandoffActivity))).toContain("Sam Ortiz now has work access.");
    expect(await setHandoffAccess(store.client, WORKSPACE, PARTNER, "Work", "add-sam", PERSON)).toEqual([]);

    signedIn(PARTNER);
    const view = JSON.parse(await getHandoffWorkspace(store.client, HANDOFF)) as { permissions: { canWork: boolean; canDecide: boolean } };
    expect(view.permissions).toMatchObject({ canWork: true, canDecide: false });
    await expect(setHandoffAccess(store.client, WORKSPACE, PARTNER, "Admin", "self-promote", PARTNER)).rejects.toThrow(/permission/);

    signedIn(PERSON);
    store.apply(await setHandoffAccess(store.client, WORKSPACE, PARTNER, "None", "remove-sam", PERSON));
    expect(store.get(HandoffWorkspace, WORKSPACE).readerIds).toEqual([PERSON]);
    expect(store.get(HandoffCase, HANDOFF).readerIds).toEqual([PERSON]);
    signedIn(PARTNER);
    await expect(getHandoffWorkspace(store.client, HANDOFF)).rejects.toThrow(/not available/);
  });
  it("refuses changes to your own access, unknown people and invalid levels", async () => {
    const store = await workspace();
    await expect(setHandoffAccess(store.client, WORKSPACE, PERSON, "Read", "demote-self", PERSON)).rejects.toThrow(/your own access/);
    await expect(setHandoffAccess(store.client, WORKSPACE, "nobody", "Read", "unknown", PERSON)).rejects.toThrow();
    await expect(setHandoffAccess(store.client, WORKSPACE, PARTNER, "Owner", "bad-level", PERSON)).rejects.toThrow(/Choose/);
  });
});
