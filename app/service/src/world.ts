import { standardActions } from "./actions/index.js";
import { businessNow, setSimulatedNow, setupClock } from "./clock.js";
import { type PgliteDb, openDbFromDump, openMemoryDb } from "./db.js";
import { Gateway } from "./gateway.js";
import { type CaseTurn, CaseRunner } from "./runner.js";
import { SimMail, SimPayments } from "./sim/index.js";
import { fire, nextDue } from "./timeline.js";

export interface AdvanceReport {
  fired: string[];
  runs: number;
  failed: Array<{ caseId: string; error: string }>;
}

/**
 * A whole simulated world in one database: Handoff's records, the imitated outside systems and
 * the business clock. It moves only when advanced, and it can be copied at any moment so a staged
 * point can be replayed or branched.
 */
export class World {
  readonly mail: SimMail;
  readonly payments: SimPayments;
  readonly gateway: Gateway;
  readonly runner: CaseRunner;

  private constructor(readonly db: PgliteDb, private readonly turn: CaseTurn) {
    this.mail = new SimMail(db);
    this.payments = new SimPayments(db);
    this.gateway = new Gateway(db, standardActions({ mail: this.mail, payments: this.payments }));
    this.runner = new CaseRunner(db, this.gateway, turn);
  }

  static async create(start: Date, turn: CaseTurn): Promise<World> {
    const db = await openMemoryDb();
    await setupClock(db, "simulated", start);
    return new World(db, turn);
  }

  now(): Promise<Date> {
    return businessNow(this.db);
  }

  /**
   * Moves business time to `target`. Everything due on the way fires in time order, and cases
   * handle what it brings before time moves on, so work a case schedules along the way still fires.
   */
  async advanceTo(target: Date): Promise<AdvanceReport> {
    const start = await this.now();
    if (target.getTime() < start.getTime()) throw new Error(`cannot go back from ${start.toISOString()} to ${target.toISOString()}`);
    const report: AdvanceReport = { fired: [], runs: 0, failed: [] };
    const drain = async () => {
      const r = await this.runner.runUntilQuiet();
      report.runs += r.runs;
      report.failed.push(...r.failed);
    };

    await drain();
    for (;;) {
      const due = await nextDue(this.db, target);
      if (!due) break;
      const now = await this.now();
      const at = due.dueAt.getTime() < now.getTime() ? now : due.dueAt;
      await setSimulatedNow(this.db, at);
      report.fired.push(await fire(this.db, due, at));
      await drain();
    }
    await setSimulatedNow(this.db, target);
    await drain();
    return report;
  }

  advanceBy(ms: number): Promise<AdvanceReport> {
    return this.now().then((now) => this.advanceTo(new Date(now.getTime() + ms)));
  }

  /** An independent copy of the whole world as it stands. The copy can take a different turn. */
  async copy(turn: CaseTurn = this.turn): Promise<World> {
    return new World(await openDbFromDump(await this.db.dump()), turn);
  }

  close(): Promise<void> {
    return this.db.close();
  }
}
