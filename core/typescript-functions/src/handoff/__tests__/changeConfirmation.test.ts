import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Admin } from "@osdk/foundry";
import { Aliases } from "@osdk/functions";
import { HandoffActivity, HandoffCase, HandoffDecision, HandoffWorkPlan, HandoffWorkspace } from "@ontology/sdk";
import createHandoffWorkspace from "../../functions/createHandoffWorkspace.js";
import receiveMoveOutNotice from "../../functions/receiveMoveOutNotice.js";
import prepareHandoffWorkPlan from "../../functions/prepareHandoffWorkPlan.js";
import changeHandoffWorkPlan from "../../functions/changeHandoffWorkPlan.js";
import acceptHandoffWorkPlan from "../../functions/acceptHandoffWorkPlan.js";
import getHandoffChange, { config, type HandoffChange } from "../../functions/getHandoffChange.js";
import getHandoffWorkspace from "../../functions/getHandoffWorkspace.js";
import type { HandoffWorkspaceView } from "../contracts.js";
import * as reasoner from "../reasoner.js";
import { digest, reference } from "../values.js";
import { HANDOFF, MODEL, PERSON, WORKSPACE, WorkspaceStore, seedQuotedWork, notice, workModel } from "./workspaceSupport.js";

vi.mock("@osdk/foundry", () => ({ Admin: { Users: { getCurrent: vi.fn() } } }));
vi.mock("@osdk/functions", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@osdk/functions")>();
  return { ...actual, Aliases: { ...actual.Aliases, model: vi.fn() } };
});
beforeEach(() => {
  vi.mocked(Admin.Users.getCurrent).mockResolvedValue({ id: PERSON, username: "morgan", attributes: {}, realm: "workspace-users", status: "ACTIVE" });
  vi.mocked(Aliases.model).mockReturnValue({ rid: MODEL });
});
afterEach(() => vi.restoreAllMocks());

async function prepared(): Promise<{ store: WorkspaceStore; workPlanId: string }> {
  const store = new WorkspaceStore();
  store.apply(await createHandoffWorkspace(store.client, "Meadow homes", "open-workspace", PERSON));
  store.apply(await receiveMoveOutNotice(store.client, WORKSPACE, JSON.stringify(notice()), "receive-notice", PERSON));
  seedQuotedWork(store);
  vi.spyOn(reasoner, "createFoundryWorkModel").mockResolvedValue(workModel());
  store.apply(await prepareHandoffWorkPlan(store.client, HANDOFF, "prepare-plan", PERSON));
  return { store, workPlanId: store.get(HandoffCase, HANDOFF).workPlanId! };
}
async function read(store: WorkspaceStore, commandId: string): Promise<HandoffChange> {
  return JSON.parse(await getHandoffChange(store.client, HANDOFF, commandId)) as HandoffChange;
}

describe("saved change confirmations", () => {
  it("is a read query and returns absence only when no activity was saved", async () => {
    const { store } = await prepared();
    expect(config.apiName).toBe("getHandoffChange");
    expect(await read(store, "missing")).toEqual({ version: "2", commandId: "missing", status: "Not found",
      subjectId: null, kind: null, payloadHash: null, resultRevision: null, at: null });
    store.onRead = (type): void => { if (type.apiName === "HandoffActivity") throw new Error("Read unavailable"); };
    await expect(read(store, "missing")).rejects.toThrow("Read unavailable");
  });
  it("confirms an exact budget request even after a later budget change", async () => {
    const { store, workPlanId } = await prepared();
    store.apply(await changeHandoffWorkPlan(store.client, workPlanId, "1", "budget", PERSON, "26000"));
    store.apply(await changeHandoffWorkPlan(store.client, workPlanId, "2", "later", PERSON, "27000"));
    const result = await read(store, "budget");
    expect(result).toMatchObject({ version: "2", commandId: "budget", status: "Saved", subjectId: workPlanId,
      kind: "Work budget changed", payloadHash: digest({ workPlanId, expectedRevision: "1", budgetCents: "26000" }), resultRevision: "2" });
    expect(Object.keys(result).sort()).toEqual(["at", "commandId", "kind", "payloadHash", "resultRevision", "status", "subjectId", "version"]);
    expect(await read(store, "another-request")).toMatchObject({ status: "Not found" });
    // This confirmation remains available to readers after decision permission is removed.
    store.change(HandoffWorkspace, WORKSPACE, { decideUserIds: [], workUserIds: [], adminUserIds: [] });
    expect(await read(store, "budget")).toEqual(result);
  });
  it("accepts the reviewed revision without incrementing the plan revision", async () => {
    const { store, workPlanId } = await prepared();
    store.apply(await acceptHandoffWorkPlan(store.client, workPlanId, "1", "accept", PERSON));
    expect(store.get(HandoffWorkPlan, workPlanId)).toMatchObject({ revision: "1", status: "Accepted" });
    expect(store.all(HandoffDecision)[0]).toMatchObject({ acceptedRevision: "1", commandId: "accept" });
    const view: HandoffWorkspaceView = JSON.parse(await getHandoffWorkspace(store.client, HANDOFF));
    expect(view.workPlan?.revision).toBe("1");
    expect(view.decisions[0]?.revision).toBe("1");
    expect(await read(store, "accept")).toMatchObject({ status: "Saved", kind: "Work plan accepted", subjectId: workPlanId,
      payloadHash: digest({ workPlanId, expectedRevision: "1" }), resultRevision: view.handoff.revision });
  });
  it.each([
    { actorId: "another-person" }, { commandId: "another-command" }, { handoffId: "another-handoff" },
    { subjectId: "another-plan" }, { workspaceId: "another-workspace" }, { readerIds: ["another-person"] },
    { kind: "Work plan prepared" }, { detail: "not json" },
    { detail: JSON.stringify({ version: "1", payloadHash: "invalid", summary: "Changed" }) },
    { detail: JSON.stringify({ version: "2", payloadHash: "a".repeat(64), summary: "Changed" }) },
    { resultRevision: undefined }, { occurredAt: "not a date" },
  ])("refuses a mismatched or incomplete saved activity: %j", async (patch) => {
    const { store, workPlanId } = await prepared();
    store.apply(await changeHandoffWorkPlan(store.client, workPlanId, "1", "budget", PERSON, "26000"));
    store.change(HandoffActivity, reference("activity", WORKSPACE, "budget"), patch);
    await expect(read(store, "budget")).rejects.toThrow();
  });
  it("checks both handoff access and the plan's scope", async () => {
    const { store, workPlanId } = await prepared();
    store.apply(await changeHandoffWorkPlan(store.client, workPlanId, "1", "budget", PERSON, "26000"));
    store.change(HandoffWorkPlan, workPlanId, { handoffId: "another-handoff" });
    await expect(read(store, "budget")).rejects.toThrow("does not belong");
    store.change(HandoffWorkspace, WORKSPACE, { readerIds: [] });
    await expect(read(store, "missing")).rejects.toThrow("not available");
  });
});
