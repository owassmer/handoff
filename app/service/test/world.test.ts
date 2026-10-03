import { afterEach, describe, expect, it } from "vitest";
import { type Decision, decide, propose } from "../src/decisions.js";
import { appendEvent, caseEvents } from "../src/events.js";
import type { CaseTurn } from "../src/runner.js";
import { scheduleWakeup } from "../src/wakeups.js";
import { World } from "../src/world.js";
import { DECIDER, at, noTurn, recordingTurn, seedCase, statement } from "./helpers.js";

const worlds: World[] = [];
async function world(start: Date, turn: CaseTurn): Promise<World> {
  const w = await World.create(start, turn);
  worlds.push(w);
  await seedCase(w.db);
  return w;
}
afterEach(async () => {
  for (const w of worlds.splice(0)) await w.close();
});

/** A stand-in agent: pays the refund when the operator accepts the statement, and notes settlement. */
const payOnAcceptance: CaseTurn = async (ctx) => {
  for (const e of ctx.events) {
    if (e.kind === "decision.decided" && e.payload.verdict !== "decline") {
      const [d] = await ctx.db.query<{ content: ReturnType<typeof statement> }>(`select content from decisions where id = $1`, [e.payload.decisionId]);
      await ctx.act("payment.refund", { decisionId: e.payload.decisionId, ...d!.content.refund });
    }
    if (e.kind === "payment.settled") await ctx.note("refund.confirmed", { paymentId: e.payload.paymentId });
  }
};

describe("the business clock", () => {
  it("fires wake-ups in time order and wakes each case at the due time", async () => {
    const { turn, seen } = recordingTurn();
    const w = await world(at("2026-11-16T17:00:00Z"), turn);
    await w.runner.runUntilQuiet();
    await scheduleWakeup(w.db, { caseId: "case-1", dueAt: at("2026-12-07T08:00:00Z"), reason: "statement deadline", key: "statement-deadline" });
    await scheduleWakeup(w.db, { caseId: "case-1", dueAt: at("2026-11-17T09:00:00Z"), reason: "plan the turn", key: "plan-the-turn" });
    const report = await w.advanceTo(at("2026-12-08T00:00:00Z"));
    expect(seen.map((s) => s.wokeAt.toISOString())).toEqual(["2026-11-17T09:00:00.000Z", "2026-12-07T08:00:00.000Z"]);
    expect(report.fired).toHaveLength(2);
    expect((await w.now()).toISOString()).toBe("2026-12-08T00:00:00.000Z");
  });

  it("fires work a case schedules along the way within the same advance", async () => {
    const woke: string[] = [];
    const turn: CaseTurn = async (ctx) => {
      woke.push(ctx.wokeAt.toISOString());
      if (woke.length === 1) await ctx.schedule({ dueAt: new Date(ctx.wokeAt.getTime() + 2 * 86400000), reason: "follow up with vendor", key: "vendor-follow-up" });
    };
    const w = await world(at("2026-11-18T17:00:00Z"), turn);
    await appendEvent(w.db, { caseId: "case-1", kind: "work.planned", source: "operator", payload: {}, occurredAt: at("2026-11-18T17:00:00Z") });
    await w.advanceTo(at("2026-11-25T00:00:00Z"));
    expect(woke).toEqual(["2026-11-18T17:00:00.000Z", "2026-11-20T17:00:00.000Z"]);
  });

  it("moves a rescheduled deadline instead of adding a second one", async () => {
    const woke: string[] = [];
    const turn: CaseTurn = async (ctx) => {
      woke.push(ctx.wokeAt.toISOString());
      if (ctx.events.some((e) => e.kind === "start")) {
        await ctx.schedule({ dueAt: at("2026-11-20T17:00:00Z"), reason: "check", key: "check" });
        await ctx.schedule({ dueAt: at("2026-11-21T17:00:00Z"), reason: "check", key: "check" });
      }
    };
    const w = await world(at("2026-11-18T17:00:00Z"), turn);
    await appendEvent(w.db, { caseId: "case-1", kind: "start", source: "operator", payload: {}, occurredAt: at("2026-11-18T17:00:00Z") });
    await w.advanceTo(at("2026-11-25T00:00:00Z"));
    expect(woke).toEqual(["2026-11-18T17:00:00.000Z", "2026-11-21T17:00:00.000Z"]);
  });

  it("never runs backwards", async () => {
    const w = await world(at("2026-12-01T17:00:00Z"), noTurn);
    await expect(w.advanceTo(at("2026-11-30T00:00:00Z"))).rejects.toThrow(/cannot go back/);
  });

  it("settles an electronic refund two business days later, and the case hears of it then", async () => {
    const w = await world(at("2026-12-01T17:00:00Z"), payOnAcceptance);
    const d = await propose(w.db, { kind: "agent", runId: "r0" }, { caseId: "case-1", kind: "account.statement", content: statement() }, at("2026-12-01T17:00:00Z"));
    await decide(w.db, DECIDER, d.id, d.contentHash, { verdict: "accept" }, at("2026-12-01T17:00:00Z"));
    await w.advanceTo(at("2026-12-05T00:00:00Z"));
    expect(await w.payments.all()).toMatchObject([{ status: "settled" }]);
    const settled = (await caseEvents(w.db, "case-1")).find((e) => e.kind === "payment.settled");
    expect(settled?.occurredAt.toISOString()).toBe("2026-12-03T17:00:00.000Z");
    expect((await caseEvents(w.db, "case-1")).some((e) => e.kind === "refund.confirmed")).toBe(true);
  });
});

describe("copies of a world", () => {
  it("branches at a pending decision into independent worlds that each pay once", async () => {
    const start = at("2026-12-01T17:00:00Z");
    const w = await world(start, payOnAcceptance);
    const pending: Decision = await propose(w.db, { kind: "agent", runId: "r0" }, { caseId: "case-1", kind: "account.statement", content: statement() }, start);

    const accepts = await w.copy();
    const changes = await w.copy();
    worlds.push(accepts, changes);

    await decide(accepts.db, DECIDER, pending.id, pending.contentHash, { verdict: "accept" }, start);
    // The operator lowers the closet charge, so the refund rises to $900.00.
    await decide(changes.db, DECIDER, pending.id, pending.contentHash, { verdict: "change", content: statement({ closetCents: 38259 }) }, start);
    await accepts.advanceTo(at("2026-12-02T00:00:00Z"));
    await changes.advanceTo(at("2026-12-02T00:00:00Z"));
    // Replaying the same branch again pays nothing more.
    await accepts.runner.runUntilQuiet();

    expect((await accepts.payments.all()).map((p) => p.amountCents)).toEqual([73259]);
    expect((await changes.payments.all()).map((p) => p.amountCents)).toEqual([90000]);
    expect(await w.payments.all()).toHaveLength(0);
    expect((await w.now()).toISOString()).toBe(start.toISOString());
    expect((await accepts.now()).toISOString()).toBe("2026-12-02T00:00:00.000Z");
  });
});
