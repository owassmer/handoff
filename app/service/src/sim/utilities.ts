import type { UtilityBill, UtilityBiller } from "../adapters/utilities.js";
import { DAY_MS, businessDate, businessNow } from "../clock.js";
import type { Db, Queryable } from "../db.js";
import { appendEvent } from "../events.js";
import { newId } from "../ids.js";
import { isoDate } from "./ledger.js";
import { faultFor, readScenario } from "./scenarios.js";
import { type SimTimer, setTimer } from "./timers.js";

/**
 * How the final bills will come out, set when a world is staged and hidden from the agent.
 * `readWithinDays` null means the submeter could not be read in time, so water is billed from the previous month.
 */
export interface FinalBillsScenario {
  water?: { readWithinDays: number | null; amountCents: number; periodStart: string };
  others?: Array<{ utility: "gas" | "electric" | "sewer" | "trash"; issueOn: string; amountCents: number; periodStart: string }>;
}

export class SimUtilities implements UtilityBiller {
  constructor(private readonly db: Db) {}

  async requestFinalBills(r: { caseId: string; tenancyRef: string; moveOutOn: string }, key: string): Promise<{ ref: string }> {
    const fault = await faultFor(this.db, "utilities", "request");
    fault.before();
    const now = await businessNow(this.db);
    await this.db.transaction(async (tx) => {
      const ref = newId("ureq");
      const [inserted] = await tx.query(
        `insert into sim.utility_requests (ref, idempotency_key, case_id, tenancy_ref, move_out_on, requested_at)
         values ($1, $2, $3, $4, $5, $6) on conflict (idempotency_key) do nothing returning ref`,
        [ref, key, r.caseId, r.tenancyRef, r.moveOutOn, now],
      );
      if (!inserted) return;
      const plan = (await readScenario<FinalBillsScenario>(tx, "utilities", r.tenancyRef)) ?? {};
      const moveOut = new Date(`${r.moveOutOn}T17:00:00Z`);
      if (plan.water) {
        const read = plan.water.readWithinDays;
        // An actual read within five days is billed the next business day after it; otherwise the previous month's bill stands in.
        const issueAt = new Date(moveOut.getTime() + ((read ?? 6) + 1) * DAY_MS);
        await setTimer(tx, {
          system: "utilities", kind: "issue", dueAt: issueAt,
          payload: { caseId: r.caseId, tenancyRef: r.tenancyRef, utility: "water", periodStart: plan.water.periodStart, periodEnd: r.moveOutOn,
            amountCents: plan.water.amountCents, readType: read !== null && read <= 5 ? "actual" : "previous_month" },
        });
      }
      for (const o of plan.others ?? []) {
        await setTimer(tx, {
          system: "utilities", kind: "issue", dueAt: new Date(`${o.issueOn}T17:00:00Z`),
          payload: { caseId: r.caseId, tenancyRef: r.tenancyRef, utility: o.utility, periodStart: o.periodStart, periodEnd: r.moveOutOn, amountCents: o.amountCents, readType: "actual" },
        });
      }
    });
    fault.after();
    const found = await this.findRequest(key);
    if (!found) throw new Error("request not recorded");
    return found;
  }

  async findRequest(key: string): Promise<{ ref: string } | null> {
    const [r] = await this.db.query<{ ref: string }>(`select ref from sim.utility_requests where idempotency_key = $1`, [key]);
    return r ?? null;
  }

  async bills(tenancyRef: string): Promise<UtilityBill[]> {
    const rows = await this.db.query<{ ref: string; utility: UtilityBill["utility"]; period_start: string | Date; period_end: string | Date; amount_cents: string; read_type: UtilityBill["readType"]; issued_on: string | Date }>(
      `select * from sim.utility_bills where tenancy_ref = $1 order by issued_on, ref`,
      [tenancyRef],
    );
    return rows.map((r) => ({ ref: r.ref, utility: r.utility, periodStart: isoDate(r.period_start), periodEnd: isoDate(r.period_end), amountCents: Number(r.amount_cents), readType: r.read_type, issuedOn: isoDate(r.issued_on) }));
  }

  /** A bill is issued: it is recorded at the biller and reaches the case. */
  static async onTimer(q: Queryable, t: SimTimer): Promise<void> {
    if (t.kind !== "issue") throw new Error(`utilities has no timer ${t.kind}`);
    const p = t.payload as { caseId: string; tenancyRef: string; utility: string; periodStart: string; periodEnd: string; amountCents: number; readType: string };
    const ref = newId("ubill");
    const issuedOn = businessDate(t.dueAt);
    await q.query(
      `insert into sim.utility_bills (ref, case_id, tenancy_ref, utility, period_start, period_end, amount_cents, read_type, issued_on)
       values ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
      [ref, p.caseId, p.tenancyRef, p.utility, p.periodStart, p.periodEnd, p.amountCents, p.readType, issuedOn],
    );
    await appendEvent(q, {
      caseId: p.caseId, kind: "utility.bill_issued", source: "outside_system", occurredAt: t.dueAt,
      payload: { billRef: ref, utility: p.utility, periodStart: p.periodStart, periodEnd: p.periodEnd, amountCents: p.amountCents, readType: p.readType, issuedOn,
        document: { name: `${p.utility}-final-bill.pdf`, ref: `sim://utilities/${ref}` } },
    });
  }
}
