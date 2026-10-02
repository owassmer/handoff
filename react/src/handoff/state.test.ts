import { createHash } from "node:crypto";
import { describe, expect, it, vi } from "vitest";
import type { ApplyResult, Change } from "./contracts";
import {
  acceptWork,
  deferred,
  exampleGateway,
  memoryStorage,
  savedChange,
} from "./examples.test-support";
import { money } from "./format";
import { HandoffStore, changePayloadHash, matchesChange, parseBudget } from "./state";

describe("Saved work and budget drafts", () => {
  it("retries the identical in-memory change, but cannot replay after reopening the page", async () => {
    const { state, gateway, recordChange } = exampleGateway();
    const storage = memoryStorage();
    const store = new HandoffStore(gateway, storage, "changes", 0);
    vi.mocked(gateway.apply).mockRejectedValueOnce(new Error("no response"));
    await store.submit(state.data, "accept");
    const pending = store.pending(state.data.handoff.id)!;
    const first = pending.change!;
    expect(Object.isFrozen(first)).toBe(true);
    const reopened = new HandoffStore(gateway, storage, "changes", 0);
    expect(reopened.pending(state.data.handoff.id)?.change).toBeUndefined();
    expect(reopened.pending(state.data.handoff.id)?.reference).toEqual(pending.reference);
    await reopened.replay(state.data.handoff.id);
    await reopened.submit(state.data, "accept");
    expect(gateway.apply).toHaveBeenCalledTimes(1);
    expect(reopened.pending(state.data.handoff.id)).toBeDefined();
    vi.mocked(gateway.apply).mockImplementationOnce(async (change) => {
      state.data = acceptWork(state.data);
      await recordChange(change);
      return "saved";
    });
    await store.replay(state.data.handoff.id);
    expect(vi.mocked(gateway.apply).mock.calls[1][0]).toEqual(first);
    expect(store.pending(state.data.handoff.id)).toBeUndefined();
    await reopened.workspace(state.data.handoff.id).fresh();
    expect(reopened.pending(state.data.handoff.id)).toBeUndefined();
    store.dispose();
    reopened.dispose();
  });
  it("does not let a rejected retry erase an earlier uncertain result", async () => {
    const { state, gateway } = exampleGateway();
    const store = new HandoffStore(gateway, memoryStorage(), "changes", 0);
    vi.mocked(gateway.apply)
      .mockRejectedValueOnce(new Error("no response"))
      .mockResolvedValueOnce("rejected");
    await store.submit(state.data, "accept");
    const commandId = store.pending(state.data.handoff.id)!.reference.commandId;
    await store.replay(state.data.handoff.id);
    expect(store.pending(state.data.handoff.id)?.reference.commandId).toBe(commandId);
    store.dispose();
  });
  it("blocks duplicate submissions before hashing or sending finishes", async () => {
    const { state, gateway } = exampleGateway();
    const store = new HandoffStore(gateway, memoryStorage(), "changes", 0);
    const sent = deferred<ApplyResult>();
    vi.mocked(gateway.apply).mockReturnValue(sent.promise);
    const first = store.submit(state.data, "accept");
    await store.submit(state.data, "accept");
    expect(store.isSending(state.data.handoff.id)).toBe(true);
    await vi.waitFor(() => expect(gateway.apply).toHaveBeenCalledTimes(1));
    sent.resolve("saved");
    await first;
    expect(store.pending(state.data.handoff.id)).toBeDefined();
    store.dispose();
  });
  it("confirms acceptance at the unchanged reviewed plan revision", async () => {
    const { state, gateway, recordChange } = exampleGateway();
    const store = new HandoffStore(gateway, memoryStorage(), "changes", 0);
    const revision = state.data.workPlan!.revision;
    vi.mocked(gateway.apply).mockImplementationOnce(async (change) => {
      state.data = acceptWork(state.data);
      expect(state.data.workPlan!.revision).toBe(revision);
      expect(state.data.decisions[0].revision).toBe(revision);
      expect(matchesChange(state.data, change)).toBe(true);
      await recordChange(change);
      return "saved";
    });
    await store.submit(state.data, "accept");
    expect(store.pending(state.data.handoff.id)).toBeUndefined();
    expect(store.notice(state.data.handoff.id)).toBe("Your change was saved.");
    store.dispose();
  });
  it.each(["budget", "accept"] as const)(
    "never confirms %s from matching state saved by another request",
    async (kind) => {
      const { state, gateway, recordChange } = exampleGateway();
      const store = new HandoffStore(gateway, memoryStorage(), "changes", 0);
      vi.mocked(gateway.apply).mockRejectedValueOnce(new Error("no response"));
      await store.submit(state.data, kind, "100125");
      const pending = store.pending(state.data.handoff.id)!;
      if (kind === "accept") {
        state.data = acceptWork(state.data);
      } else {
        Object.assign(state.data.workPlan!, { revision: "3", budgetCents: "100125" });
      }
      expect(matchesChange(state.data, pending.change!)).toBe(true);
      await recordChange({ ...pending.change!, commandId: "someone-elses-request" });
      await store.workspace(state.data.handoff.id).fresh();
      expect(store.pending(state.data.handoff.id)).toBe(pending);
      expect(store.notice(state.data.handoff.id)).toBeUndefined();
      store.dispose();
    },
  );
  it.each(["missing", "error", "hash", "command", "subject", "kind", "revision"])(
    "keeps the change pending when its confirmation has a %s problem",
    async (problem) => {
      const { state, gateway, recordChange } = exampleGateway();
      const store = new HandoffStore(gateway, memoryStorage(), "changes", 0);
      await store.submit(state.data, "budget", "100125");
      const pending = store.pending(state.data.handoff.id)!;
      Object.assign(state.data.workPlan!, { revision: "3", budgetCents: "100125" });
      if (problem !== "missing") {
        await recordChange(pending.change!);
        const receipt = state.receipts.get(pending.reference.commandId)!;
        if (problem === "error") {
          vi.mocked(gateway.receipt).mockRejectedValue(new Error("not available"));
        }
        if (problem === "hash") {
          receipt.payloadHash = "a".repeat(64);
        }
        if (problem === "command") {
          receipt.commandId = "different-command";
        }
        if (problem === "subject") {
          receipt.subjectId = "different-plan";
        }
        if (problem === "kind") {
          receipt.kind = "Work plan accepted";
        }
        if (problem === "revision") {
          receipt.resultRevision = "4";
        }
      }
      await store.workspace(state.data.handoff.id).fresh();
      expect(store.pending(state.data.handoff.id)).toBe(pending);
      expect(store.workspace(state.data.handoff.id).getSnapshot().failed).toBe(false);
      store.dispose();
    },
  );
  it("waits for a coherent fresh read after confirmation and does not misattribute a later budget", async () => {
    const { state, gateway, recordChange } = exampleGateway();
    const store = new HandoffStore(gateway, memoryStorage(), "changes", 0);
    await store.submit(state.data, "budget", "100125");
    const pending = store.pending(state.data.handoff.id)!;
    Object.assign(state.data.workPlan!, { revision: "3", budgetCents: "100125" });
    await recordChange(pending.change!);
    vi.mocked(gateway.workspace).mockRejectedValueOnce(new Error("changed during read"));
    await store.workspace(state.data.handoff.id).fresh();
    expect(store.pending(state.data.handoff.id)).toBe(pending);
    Object.assign(state.data.workPlan!, { revision: "2", budgetCents: "100000" });
    await store.workspace(state.data.handoff.id).fresh();
    expect(store.pending(state.data.handoff.id)).toBe(pending);
    Object.assign(state.data.workPlan!, { revision: "4", budgetCents: "110000" });
    await store.workspace(state.data.handoff.id).fresh();
    expect(store.pending(state.data.handoff.id)).toBeUndefined();
    expect(store.workspace(state.data.handoff.id).getSnapshot().data?.workPlan?.budgetCents).toBe(
      "110000",
    );
    expect(store.notice(state.data.handoff.id)).toBe("Your change was saved.");
    expect(vi.mocked(gateway.receipt).mock.invocationCallOrder.slice(-1)[0]).toBeLessThan(
      vi.mocked(gateway.workspace).mock.invocationCallOrder.slice(-1)[0],
    );
    store.dispose();
  });
  it("hashes only the actual backend payload, with ordered keys and lossless strings", async () => {
    const change: Change = {
      kind: "budget",
      handoffId: "garden",
      workPlanId: "plan",
      expectedRevision: "2",
      budgetCents: "120025",
      commandId: "request",
    };
    expect(await changePayloadHash(change)).toBe(
      createHash("sha256")
        .update('{"budgetCents":"120025","expectedRevision":"2","workPlanId":"plan"}')
        .digest("hex"),
    );
    const accepted = { ...change, kind: "accept" as const };
    expect(await changePayloadHash(accepted)).toBe(
      createHash("sha256").update('{"expectedRevision":"2","workPlanId":"plan"}').digest("hex"),
    );
    expect(await changePayloadHash({ ...accepted, budgetCents: "1", commandId: "other" })).toBe(
      await changePayloadHash(accepted),
    );
  });
  it("persists only bounded recovery references, never a draft or exact financial request", async () => {
    const { state, gateway } = exampleGateway();
    const storage = memoryStorage();
    const store = new HandoffStore(gateway, storage, "changes", 0);
    store.edit(state.data.workPlan!, "1105.25");
    expect(storage.getItem("changes")).toBeNull();
    await store.submit(state.data, "budget", "110525");
    const text = storage.getItem("changes")!;
    expect(text).not.toMatch(
      /budgetCents|originalBudget|draft|acknowledged|financialProgress|110525|1105.25|100000|token|currency/,
    );
    expect(JSON.parse(text)).toEqual({
      version: "2",
      pending: [store.pending(state.data.handoff.id)!.reference],
    });
    expect(new TextEncoder().encode(text).length).toBeLessThanOrEqual(64 * 1024);
    store.clear();
    expect(store.draft(state.data.workPlan!)).toBeUndefined();
    expect(store.pending(state.data.handoff.id)).toBeUndefined();
    expect(storage.getItem("changes")).toBe(text);
    const anotherPerson = new HandoffStore(gateway, storage, "changes:another-person", 0);
    expect(anotherPerson.pending(state.data.handoff.id)).toBeUndefined();
    expect(anotherPerson.draft(state.data.workPlan!)).toBeUndefined();
    anotherPerson.dispose();
    store.dispose();
  });
  it("retains the scoped recovery reference if identity changes while a request is running", async () => {
    const { state, gateway } = exampleGateway();
    const storage = memoryStorage();
    const store = new HandoffStore(gateway, storage, "changes:person", 0);
    const request = deferred<ApplyResult>();
    vi.mocked(gateway.apply).mockReturnValue(request.promise);
    const sending = store.submit(state.data, "accept");
    await vi.waitFor(() => expect(gateway.apply).toHaveBeenCalledTimes(1));
    const original = store.pending(state.data.handoff.id)!;
    store.clear();
    request.resolve("saved");
    await sending;
    const resumed = new HandoffStore(gateway, storage, "changes:person", 0);
    expect(resumed.pending(state.data.handoff.id)?.reference).toEqual(original.reference);
    expect(resumed.pending(state.data.handoff.id)?.change).toBeUndefined();
    resumed.dispose();
  });
  it("keeps at most 32 unresolved references without evicting any earlier change", async () => {
    const { state, gateway } = exampleGateway();
    const storage = memoryStorage();
    const change: Change = {
      kind: "accept",
      handoffId: "garden-home",
      workPlanId: "work-garden",
      expectedRevision: "2",
      budgetCents: "100000",
      commandId: "command",
    };
    const receipt = await savedChange(change, state.data);
    const pending = Array.from({ length: 32 }, (_, i) => ({
      kind: "accept",
      handoffId: `handoff-${i}`,
      workPlanId: `plan-${i}`,
      expectedRevision: "2",
      commandId: `request-${i}`,
      payloadHash: receipt.payloadHash,
    }));
    storage.setItem("changes", JSON.stringify({ version: "2", pending }));
    const store = new HandoffStore(gateway, storage, "changes", 0);
    await store.submit(state.data, "accept");
    expect(gateway.apply).not.toHaveBeenCalled();
    expect(JSON.parse(storage.getItem("changes")!).pending).toEqual(pending);
    store.dispose();
  });
  it.each([
    "incomplete",
    "",
    "x".repeat(65537),
    JSON.stringify({ drafts: { plan: { value: "1105.25" } }, pending: {} }),
    JSON.stringify({ version: "2", pending: Array.from({ length: 33 }, () => ({})) }),
  ])("locks ambiguous or oversized stored changes and removes their contents", async (value) => {
    const { state, gateway } = exampleGateway();
    const storage = memoryStorage();
    storage.setItem("changes", value);
    const broken = new HandoffStore(gateway, storage, "changes", 0);
    await broken.submit(state.data, "accept");
    expect(gateway.apply).not.toHaveBeenCalled();
    expect(broken.blocked()).toBe(true);
    expect(storage.getItem("changes")).toBe('{"version":"2","pending":[],"unreadable":true}');
    broken.clear();
    const reopened = new HandoffStore(gateway, storage, "changes", 0);
    expect(reopened.blocked()).toBe(true);
    reopened.dispose();
  });
  it("does not send without recoverable browser storage", async () => {
    const { state, gateway } = exampleGateway();
    const noStorage = new HandoffStore(gateway, undefined, "changes", 0);
    await noStorage.submit(state.data, "accept");
    expect(gateway.apply).not.toHaveBeenCalled();
    noStorage.dispose();
  });
  it("requires decision permission for both actions, not work permission", async () => {
    const { state, gateway } = exampleGateway();
    const store = new HandoffStore(gateway, memoryStorage(), "changes", 0);
    state.data.permissions.canDecide = false;
    await store.submit(state.data, "budget", "120000");
    await store.submit(state.data, "accept");
    expect(gateway.apply).not.toHaveBeenCalled();
    state.data.permissions.canDecide = true;
    state.data.permissions.canWork = false;
    await store.submit(state.data, "budget", "120000");
    expect(gateway.apply).toHaveBeenCalledTimes(1);
    store.dispose();
  });
  it("checks the published budget limit before sending a change", async () => {
    const { state, gateway } = exampleGateway();
    const store = new HandoffStore(gateway, memoryStorage(), "changes", 0);
    for (const amount of ["100000001", "9007199254740993", "0100000"]) {
      await store.submit(state.data, "budget", amount);
    }
    expect(gateway.apply).not.toHaveBeenCalled();
    await store.submit(state.data, "budget", "100000000");
    expect(gateway.apply).toHaveBeenCalledTimes(1);
    store.dispose();
  });
  it("retains cent precision for large amounts and rejects incomplete budget inputs", () => {
    expect(parseBudget("90071992547409.93")).toBe("9007199254740993");
    expect(money("9007199254740993", "GBP")).toContain("90,071,992,547,409.93");
    expect(parseBudget("2.123")).toBeUndefined();
    expect(parseBudget("-1")).toBeUndefined();
    expect(parseBudget("1,250")).toBeUndefined();
    expect(parseBudget(" ")).toBeUndefined();
  });
});
