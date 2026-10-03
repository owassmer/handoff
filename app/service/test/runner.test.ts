import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { decide, propose } from "../src/decisions.js";
import { appendEvent, unprocessedEvents } from "../src/events.js";
import { CaseRunner, type CaseTurn } from "../src/runner.js";
import { World } from "../src/world.js";
import { DECIDER, at, noTurn, recordingTurn, refundOf, seedCase, statement } from "./helpers.js";

const NOW = at("2026-12-01T17:00:00Z");

let w: World;
beforeEach(async () => {
  w = await World.create(NOW, noTurn);
  await seedCase(w.db);
});
afterEach(() => w.close());

const tenantWrites = (text: string) =>
  appendEvent(w.db, { caseId: "case-1", kind: "message.received", source: "tenant", payload: { text }, occurredAt: NOW });

describe("case runs", () => {
  it("hands a fresh turn every pending event, in order, then marks them handled", async () => {
    const { turn, seen } = recordingTurn();
    const runner = new CaseRunner(w.db, w.gateway, turn);
    await tenantWrites("first");
    await tenantWrites("second");
    expect(await runner.runCase("case-1")).toMatchObject({ status: "completed", events: 2 });
    expect(seen).toEqual([{ wokeAt: NOW, kinds: ["message.received", "message.received"] }]);
    expect(await unprocessedEvents(w.db, "case-1")).toHaveLength(0);
    expect(await runner.runCase("case-1")).toEqual({ status: "idle" });
  });

  it("leaves events pending when a turn fails, and retries them on the next wake", async () => {
    let fail = true;
    const turn: CaseTurn = async () => { if (fail) throw new Error("model unavailable"); };
    const runner = new CaseRunner(w.db, w.gateway, turn);
    await tenantWrites("hello");
    expect(await runner.runCase("case-1")).toMatchObject({ status: "failed", error: "model unavailable" });
    expect(await unprocessedEvents(w.db, "case-1")).toHaveLength(1);
    fail = false;
    expect(await runner.runCase("case-1")).toMatchObject({ status: "completed" });
  });

  it("runs one wake of a case at a time", async () => {
    await tenantWrites("hello");
    await w.db.query(`update cases set run_lease_owner = 'worker-other', run_lease_until = now() + interval '1 minute' where id = 'case-1'`);
    const runner = new CaseRunner(w.db, w.gateway, noTurn, "worker-me");
    expect(await runner.runCase("case-1")).toEqual({ status: "busy" });
    await w.db.query(`update cases set run_lease_until = now() - interval '1 second' where id = 'case-1'`);
    expect(await runner.runCase("case-1")).toMatchObject({ status: "completed" });
  });

  it("does not repeat a payment when a turn crashes after paying and runs again", async () => {
    const content = statement();
    const d = await propose(w.db, { kind: "agent", runId: "r0" }, { caseId: "case-1", kind: "account.statement", content }, NOW);
    await decide(w.db, DECIDER, d.id, d.contentHash, { verdict: "accept" }, NOW);
    let crashes = 1;
    const turn: CaseTurn = async (ctx) => {
      await ctx.act("payment.refund", refundOf(d.id, content));
      if (crashes-- > 0) throw new Error("process died");
    };
    const runner = new CaseRunner(w.db, w.gateway, turn);
    expect((await runner.runCase("case-1")).status).toBe("failed");
    expect((await runner.runCase("case-1")).status).toBe("completed");
    expect(await w.payments.all()).toHaveLength(1);
  });
});
