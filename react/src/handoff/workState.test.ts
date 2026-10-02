import { createHash } from "node:crypto";
import { describe, expect, it, vi } from "vitest";
import { type Change, HandoffError } from "./contracts";
import {
  acceptWork,
  deferred,
  exampleGateway,
  exampleWorkspace,
  memoryStorage,
  savedChange,
} from "./examples.test-support";
import { HandoffStore, changePayloadHash } from "./state";
import { workExample } from "./work.test-support";

function setup(data = workExample()) {
  const mock = exampleGateway(data),
    storage = memoryStorage();
  return { ...mock, storage, store: new HandoffStore(mock.gateway, storage, "work", 0) };
}
describe("Proposal and conversation recovery", () => {
  it("hashes recursively sorted structured changes exactly like the service", async () => {
    const change: Change = {
      kind: "plan",
      handoffId: "h",
      workPlanId: "p",
      expectedRevision: "2",
      budgetCents: "100",
      commandId: "c",
      changes: {
        selections: [{ scope: "Scope", reason: "Reason", quoteLineId: "l", quoteId: "q" }],
        fixedProviderPartyId: null,
        budgetCents: "100",
      },
    };
    const canonical =
      '{"changes":{"budgetCents":"100","fixedProviderPartyId":null,"selections":[{"quoteId":"q","quoteLineId":"l","reason":"Reason","scope":"Scope"}]},"expectedRevision":"2","workPlanId":"p"}';
    expect(await changePayloadHash(change)).toBe(
      createHash("sha256").update(canonical).digest("hex"),
    );
    const message: Change = {
      kind: "message",
      handoffId: "h",
      message: "Question",
      commandId: "c",
    };
    expect(await changePayloadHash(message)).toBe(
      createHash("sha256").update('{"handoffId":"h","message":"Question"}').digest("hex"),
    );
  });
  it("confirms an older exact acceptance even after a later repair proposal", async () => {
    const initial = exampleWorkspace();
    initial.workPlan!.title = "Assessment only";
    const { store, state, gateway } = setup(initial);
    vi.mocked(gateway.apply).mockRejectedValue(new Error("response lost"));
    await store.submit(initial, "accept");
    const sent = store.pending(initial.handoff.id)!.change!;
    state.data = acceptWork(initial);
    state.receipts.set(sent.commandId, await savedChange(sent, state.data));
    state.data.workPlan = { ...exampleWorkspace().workPlan!, id: "repair-proposal", revision: "1" };
    await store.workspace(initial.handoff.id).fresh();
    expect(store.pending(initial.handoff.id)).toBeUndefined();
    expect(state.data.decisions[0].content.title).toBe("Assessment only");
    expect(state.data.workPlan.acceptedDecisionId).toBeNull();
    store.dispose();
  });
  it.each(["budget", "plan"] as const)(
    "confirms a %s change of accepted work using the old subject and new proposal",
    async (kind) => {
      const initial = acceptWork(exampleWorkspace()),
        { store, gateway, state, recordChange } = setup(initial);
      vi.mocked(gateway.apply).mockImplementation(async (change) => {
        const next = structuredClone(initial);
        next.workPlan = {
          ...initial.workPlan!,
          id: "new-proposal",
          revision: "1",
          acceptedDecisionId: null,
          status: "Ready",
          budgetCents: "120000",
        };
        state.data = next;
        await recordChange(change);
        return "saved";
      });
      await store.submit(initial, kind, "120000", { budgetCents: "120000" });
      expect(store.pending(initial.handoff.id)).toBeUndefined();
      expect(state.data.decisions[0].content.budgetCents).toBe("100000");
      expect(state.data.workPlan?.acceptedDecisionId).toBeNull();
      store.dispose();
    },
  );
  it("confirms an earlier budget after that revision was accepted and another proposal appeared", async () => {
    const initial = exampleWorkspace(),
      { store, gateway, state } = setup(initial);
    vi.mocked(gateway.apply).mockRejectedValue(new Error("lost"));
    await store.submit(initial, "budget", "120000");
    const change = store.pending(initial.handoff.id)!.change!;
    state.data.workPlan = { ...state.data.workPlan!, budgetCents: "120000", revision: "3" };
    const receipt = await savedChange(change, state.data);
    state.data = acceptWork(state.data);
    state.data.workPlan = { ...exampleWorkspace().workPlan!, id: "later", revision: "1" };
    state.receipts.set(change.commandId, receipt);
    await store.workspace(initial.handoff.id).fresh();
    expect(store.pending(initial.handoff.id)).toBeUndefined();
    store.dispose();
  });
  it("does not confirm structured edits from matching present values or a different payload", async () => {
    const { store, gateway, state } = setup();
    const data = state.data;
    vi.mocked(gateway.apply).mockRejectedValue(new Error("lost"));
    await store.submit(data, "plan", undefined, { fixedProviderPartyId: "provider" });
    const sent = store.pending(data.handoff.id)!.change!;
    state.data.workPlan = { ...data.workPlan!, fixedProviderPartyId: "provider", revision: "2" };
    await store.workspace(data.handoff.id).fresh();
    expect(store.pending(data.handoff.id)).toBeDefined();
    const receipt = await savedChange(sent, state.data);
    state.receipts.set(sent.commandId, { ...receipt, payloadHash: "0".repeat(64) });
    await store.workspace(data.handoff.id).fresh();
    expect(store.pending(data.handoff.id)).toBeDefined();
    state.receipts.set(sent.commandId, receipt);
    await store.workspace(data.handoff.id).fresh();
    expect(store.pending(data.handoff.id)).toBeUndefined();
    store.dispose();
  });
  it("saves a work-user message promptly and waits for its receipt without requiring decision access", async () => {
    const { store, gateway, state, storage } = setup();
    state.data.permissions.canDecide = false;
    const waiting = deferred<"saved">();
    vi.mocked(gateway.apply).mockReturnValue(waiting.promise);
    store.editMessage(state.data, " Please keep the door. ");
    const sent = store.sendMessage(state.data);
    await vi.waitFor(() => expect(gateway.apply).toHaveBeenCalledOnce());
    expect(store.pending(state.data.handoff.id)?.status).toBe("sending");
    const change = vi.mocked(gateway.apply).mock.calls[0][0];
    expect(change).toMatchObject({
      kind: "message",
      message: "Please keep the door.",
      expectedPlanRevision: "1",
    });
    expect(storage.getItem("work")).not.toContain("Please keep");
    waiting.resolve("saved");
    await sent;
    expect(store.pending(state.data.handoff.id)?.acknowledged).toBe(true);
    state.data.handoff.revision = "9";
    state.receipts.set(change.commandId, await savedChange(change, state.data));
    await store.workspace(state.data.handoff.id).fresh();
    expect(store.pending(state.data.handoff.id)).toBeUndefined();
    expect(store.messageDraft(state.data.handoff.id)).toBeUndefined();
    expect(store.notice(state.data.handoff.id)).toMatch(/message is saved/);
    store.dispose();
  });
  it("keeps only recovery references on reload; no reconstructed retry of a message", async () => {
    const { store, gateway, state, storage } = setup();
    vi.mocked(gateway.apply).mockRejectedValue(new Error("lost"));
    store.editMessage(state.data, "Private context");
    await store.sendMessage(state.data);
    store.dispose();
    const restored = new HandoffStore(gateway, storage, "work", 0);
    expect(restored.pending(state.data.handoff.id)?.change).toBeUndefined();
    await restored.replay(state.data.handoff.id);
    expect(gateway.apply).toHaveBeenCalledOnce();
    expect(restored.pending(state.data.handoff.id)).toBeDefined();
    restored.dispose();
  });
  it("blocks stale callbacks and retains a message draft until its new proposal is reviewed", async () => {
    const { store, gateway, state } = setup();
    const reviewed = structuredClone(state.data);
    await store.workspace(reviewed.handoff.id).fresh();
    store.editMessage(reviewed, "A different finish please");
    state.data.workPlan = { ...state.data.workPlan!, revision: "2" };
    await store.workspace(reviewed.handoff.id).fresh();
    await store.submit(reviewed, "accept");
    await store.sendMessage(state.data);
    expect(gateway.apply).not.toHaveBeenCalled();
    expect(store.messageDraft(reviewed.handoff.id)?.value).toBe("A different finish please");
    store.reviewMessage(state.data);
    await store.sendMessage(state.data);
    expect(gateway.apply).toHaveBeenCalledOnce();
    store.dispose();
  });
  it("clears sensitive drafts on lost access but retains uncertain recovery references", async () => {
    const { store, gateway, state } = setup();
    const data = state.data;
    store.edit(data.workPlan!, "1200");
    store.editMessage(data, "Private message");
    vi.mocked(gateway.apply).mockRejectedValue(new Error("lost"));
    await store.sendMessage(data);
    vi.mocked(gateway.workspace).mockRejectedValue(new HandoffError("permission"));
    await store.workspace(data.handoff.id).fresh();
    expect(store.workspace(data.handoff.id).getSnapshot().data).toBeUndefined();
    expect(store.draft(data.workPlan!)).toBeUndefined();
    expect(store.messageDraft(data.handoff.id)).toBeUndefined();
    expect(store.pending(data.handoff.id)?.reference).toBeDefined();
    expect(store.pending(data.handoff.id)?.change).toBeUndefined();
    store.dispose();
  });
});
