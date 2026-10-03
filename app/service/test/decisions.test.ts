import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { setupClock } from "../src/clock.js";
import { type PgliteDb, openMemoryDb } from "../src/db.js";
import { DecisionRefused, decide, getDecision, propose, standingInstruction } from "../src/decisions.js";
import { caseEvents } from "../src/events.js";
import { NotAllowed } from "../src/principals.js";
import { ADMIN, COORDINATOR, DECIDER, at, seedCase, statement } from "./helpers.js";

const AGENT = { kind: "agent", runId: "run-1" } as const;
const NOW = at("2026-11-30T17:00:00Z");

let db: PgliteDb;
beforeEach(async () => {
  db = await openMemoryDb();
  await setupClock(db, "simulated", NOW);
  await seedCase(db);
});
afterEach(() => db.close());

const proposeStatement = (content = statement(), supersedes?: string) =>
  propose(db, AGENT, { caseId: "case-1", kind: "account.statement", content, supersedes }, NOW);

describe("decisions", () => {
  it("lets only an operator with decide permission accept", async () => {
    const d = await proposeStatement();
    await expect(decide(db, AGENT, d.id, d.contentHash, { verdict: "accept" }, NOW)).rejects.toThrow(NotAllowed);
    await expect(decide(db, COORDINATOR, d.id, d.contentHash, { verdict: "accept" }, NOW)).rejects.toThrow(/decide permission/);
    const accepted = await decide(db, DECIDER, d.id, d.contentHash, { verdict: "accept" }, NOW);
    expect(accepted).toMatchObject({ status: "accepted", decidedBy: "op-decider" });
  });

  it("binds acceptance to the content the operator reviewed", async () => {
    const first = await proposeStatement();
    const revised = await proposeStatement(statement({ amountCents: 72359 }), first.id);
    expect((await getDecision(db, first.id))?.status).toBe("superseded");
    // Accepting the version on screen after the agent revised it is refused.
    await expect(decide(db, DECIDER, first.id, first.contentHash, { verdict: "accept" }, NOW)).rejects.toThrow(DecisionRefused);
    // So is accepting the revision with the hash of what was reviewed before.
    await expect(decide(db, DECIDER, revised.id, first.contentHash, { verdict: "accept" }, NOW)).rejects.toThrow(/not the content that was reviewed/);
    expect((await decide(db, DECIDER, revised.id, revised.contentHash, { verdict: "accept" }, NOW)).status).toBe("accepted");
  });

  it("records an operator's change as their own accepted decision", async () => {
    const d = await proposeStatement();
    const changed = await decide(db, DECIDER, d.id, d.contentHash, { verdict: "change", content: statement({ amountCents: 80000 }), note: "waive part of cleaning" }, NOW);
    expect(changed).toMatchObject({ status: "accepted", proposedBy: "operator:op-decider", supersedes: d.id });
    expect((changed.content as { refund: { amountCents: number } }).refund.amountCents).toBe(80000);
    expect((await getDecision(db, d.id))?.status).toBe("superseded");
  });

  it("keeps an accepted decision in force until its correction is accepted", async () => {
    const d = await proposeStatement();
    await decide(db, DECIDER, d.id, d.contentHash, { verdict: "accept" }, NOW);
    const correction = await proposeStatement(statement({ amountCents: 128259 }), d.id);
    expect((await getDecision(db, d.id))?.status).toBe("accepted");
    await decide(db, DECIDER, correction.id, correction.contentHash, { verdict: "accept" }, NOW);
    expect((await getDecision(db, d.id))?.status).toBe("superseded");
  });

  it("wakes the case with the operator's decision", async () => {
    const d = await proposeStatement();
    await decide(db, DECIDER, d.id, d.contentHash, { verdict: "decline", note: "recheck the closet" }, NOW);
    const [e] = (await caseEvents(db, "case-1")).filter((x) => x.kind === "decision.decided");
    expect(e).toMatchObject({ source: "operator", trusted: true, payload: { proposedId: d.id, verdict: "decline" } });
  });

  it("needs configure permission for a company-wide standing instruction", async () => {
    const s = await propose(db, DECIDER, { caseId: null, kind: "standing.routine-messages", content: { purposes: ["acknowledge"] } }, NOW);
    await expect(decide(db, DECIDER, s.id, s.contentHash, { verdict: "accept" }, NOW)).rejects.toThrow(/configure permission/);
    await decide(db, ADMIN, s.id, s.contentHash, { verdict: "accept" }, NOW);
    expect((await standingInstruction(db, "standing.routine-messages"))?.id).toBe(s.id);
  });
});
