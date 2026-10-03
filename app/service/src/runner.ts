import { businessNow } from "./clock.js";
import type { Db, Queryable } from "./db.js";
import { type Decision, type Proposal, propose } from "./decisions.js";
import { type CaseEvent, appendEvent, casesWithWork, markProcessed, unprocessedEvents } from "./events.js";
import type { ActionRecord, Gateway } from "./gateway.js";
import { newId } from "./ids.js";
import type { Principal } from "./principals.js";
import { type Wakeup, cancelWakeup, scheduleWakeup } from "./wakeups.js";

/**
 * What one wake of a case can see and do. The agent reads the records and acts only through
 * here: actions go through the gateway, decisions are proposed for an operator, and later work
 * is scheduled as a wake-up. Nothing is held in memory between wakes.
 */
export interface TurnContext {
  caseId: string;
  runId: string;
  /** Business time when the case woke. */
  wokeAt: Date;
  /** The events that woke it, oldest first. */
  events: CaseEvent[];
  db: Queryable;
  act(kind: string, request: unknown): Promise<ActionRecord>;
  propose(p: Omit<Proposal, "caseId">): Promise<Decision>;
  schedule(w: Omit<Wakeup, "caseId">): Promise<void>;
  cancel(key: string): Promise<void>;
  /** Records something Handoff did or concluded, without waking the case again. */
  note(kind: string, payload: Record<string, unknown>): Promise<void>;
  /** The actions on offer through the gateway. */
  catalog(): ReturnType<Gateway["catalog"]>;
}

export type CaseTurn = (ctx: TurnContext) => Promise<void>;

export type RunResult =
  | { status: "busy" | "idle" }
  | { status: "completed"; runId: string; events: number }
  | { status: "failed"; runId: string; error: string };

export class CaseRunner {
  constructor(
    private readonly db: Db,
    private readonly gateway: Gateway,
    private readonly turn: CaseTurn,
    readonly owner: string = newId("worker"),
    private readonly leaseMs: number = 10 * 60 * 1000,
  ) {}

  /** One wake: claim the case, hand its pending events to a fresh turn, mark them handled if it finishes. */
  async runCase(caseId: string): Promise<RunResult> {
    if (!(await this.claim(caseId))) return { status: "busy" };
    try {
      const events = await unprocessedEvents(this.db, caseId);
      if (events.length === 0) return { status: "idle" };
      const runId = newId("run");
      const wokeAt = await businessNow(this.db);
      await this.db.query(
        `insert into runs (id, case_id, owner, event_ids, business_time, status) values ($1, $2, $3, $4, $5, 'running')`,
        [runId, caseId, this.owner, events.map((e) => e.id), wokeAt],
      );
      try {
        await this.turn(this.context(caseId, runId, wokeAt, events));
      } catch (e) {
        const error = e instanceof Error ? e.message : String(e);
        await this.db.query(`update runs set status = 'failed', error = $2, finished_at = now() where id = $1`, [runId, error]);
        return { status: "failed", runId, error };
      }
      await this.db.transaction(async (tx) => {
        await markProcessed(tx, events.map((e) => e.id));
        await tx.query(`update runs set status = 'completed', finished_at = now() where id = $1`, [runId]);
      });
      return { status: "completed", runId, events: events.length };
    } finally {
      await this.release(caseId);
    }
  }

  /** Runs every case with pending events until none are left. A case whose turn fails is not retried in the same pass. */
  async runUntilQuiet(maxRuns = 500): Promise<{ runs: number; failed: Array<{ caseId: string; error: string }> }> {
    const skip = new Set<string>();
    const failed: Array<{ caseId: string; error: string }> = [];
    let runs = 0;
    for (;;) {
      const cases = (await casesWithWork(this.db)).filter((c) => !skip.has(c));
      if (cases.length === 0) return { runs, failed };
      for (const caseId of cases) {
        if (++runs > maxRuns) throw new Error(`more than ${maxRuns} runs without the cases going quiet`);
        const r = await this.runCase(caseId);
        if (r.status === "failed") {
          skip.add(caseId);
          failed.push({ caseId, error: r.error });
        } else if (r.status === "busy") {
          skip.add(caseId);
        }
      }
    }
  }

  private context(caseId: string, runId: string, wokeAt: Date, events: CaseEvent[]): TurnContext {
    const agent: Principal = { kind: "agent", runId };
    return {
      caseId,
      runId,
      wokeAt,
      events,
      db: this.db,
      act: (kind, request) => this.gateway.execute(agent, caseId, kind, request),
      propose: async (p) => propose(this.db, agent, { ...p, caseId }, await businessNow(this.db)),
      schedule: (w) => scheduleWakeup(this.db, { ...w, caseId }),
      cancel: async (key) => cancelWakeup(this.db, caseId, key, await businessNow(this.db)),
      note: async (kind, payload) => {
        await appendEvent(this.db, { caseId, kind, source: "handoff", payload: { runId, ...payload }, occurredAt: await businessNow(this.db), wakes: false });
      },
      catalog: () => this.gateway.catalog(),
    };
  }

  private async claim(caseId: string): Promise<boolean> {
    const rows = await this.db.query(
      `update cases set run_lease_owner = $2, run_lease_until = now() + $3 * interval '1 millisecond'
       where id = $1 and (run_lease_until is null or run_lease_until < now() or run_lease_owner = $2) returning id`,
      [caseId, this.owner, this.leaseMs],
    );
    return rows.length > 0;
  }

  private async release(caseId: string): Promise<void> {
    await this.db.query(`update cases set run_lease_owner = null, run_lease_until = null where id = $1 and run_lease_owner = $2`, [caseId, this.owner]);
  }
}
