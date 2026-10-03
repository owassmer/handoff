import type { Collector, Placement, PlacementStatus } from "../adapters/collector.js";
import { DAY_MS, businessNow } from "../clock.js";
import type { Db, Queryable } from "../db.js";
import { appendEvent } from "../events.js";
import { newId } from "../ids.js";
import { faultFor, readScenario } from "./scenarios.js";
import { type SimTimer, setTimer } from "./timers.js";

/** How long the collector takes to apply a correction. Real agencies lag; this is where Holland's complaints came from. */
export interface CollectorScenario {
  applyAdjustmentAfterDays: number;
}

export class SimCollector implements Collector {
  constructor(private readonly db: Db) {}

  async place(p: Placement, key: string): Promise<{ ref: string }> {
    const fault = await faultFor(this.db, "collector", "place");
    fault.before();
    const now = await businessNow(this.db);
    await this.db.transaction(async (tx) => {
      const ref = newId("plc");
      const [inserted] = await tx.query(
        `insert into sim.collector_placements (ref, idempotency_key, case_id, debtor_party_id, creditor, placed_at)
         values ($1, $2, $3, $4, $5, $6) on conflict (idempotency_key) do nothing returning ref`,
        [ref, key, p.caseId, p.debtorPartyId, p.creditor, now],
      );
      if (!inserted) return;
      for (const c of p.components) {
        await tx.query(
          `insert into sim.collector_components (placement_ref, component_id, description, amount_cents, consumer_credit) values ($1, $2, $3, $4, $5)`,
          [ref, c.componentId, c.description, c.amountCents, c.consumerCredit],
        );
      }
    });
    fault.after();
    const found = await this.find(key);
    if (!found) throw new Error("placement not recorded");
    return found;
  }

  async adjust(a: { placementRef: string; componentId: string; amountCents: number; reason: string }, key: string): Promise<{ ref: string }> {
    const fault = await faultFor(this.db, "collector", "adjust");
    fault.before();
    const now = await businessNow(this.db);
    await this.db.transaction(async (tx) => {
      const ref = newId("adj");
      const [inserted] = await tx.query(
        `insert into sim.collector_adjustments (ref, idempotency_key, placement_ref, component_id, amount_cents, reason, received_at)
         values ($1, $2, $3, $4, $5, $6, $7) on conflict (idempotency_key) do nothing returning ref`,
        [ref, key, a.placementRef, a.componentId, a.amountCents, a.reason, now],
      );
      if (!inserted) return;
      const plan = (await readScenario<CollectorScenario>(tx, "collector", "behavior")) ?? { applyAdjustmentAfterDays: 0 };
      await setTimer(tx, { system: "collector", kind: "apply", dueAt: new Date(now.getTime() + plan.applyAdjustmentAfterDays * DAY_MS), payload: { ref } });
    });
    fault.after();
    const [r] = await this.db.query<{ ref: string }>(`select ref from sim.collector_adjustments where idempotency_key = $1`, [key]);
    if (!r) throw new Error("adjustment not recorded");
    return r;
  }

  async find(key: string): Promise<{ ref: string } | null> {
    const [r] = await this.db.query<{ ref: string }>(
      `select ref from sim.collector_placements where idempotency_key = $1 union all select ref from sim.collector_adjustments where idempotency_key = $1`,
      [key],
    );
    return r ?? null;
  }

  async status(placementRef: string): Promise<PlacementStatus> {
    return statusOf(this.db, placementRef);
  }

  /** The collector applies a correction and reports the new balance. */
  static async onTimer(q: Queryable, t: SimTimer): Promise<void> {
    if (t.kind !== "apply") throw new Error(`collector has no timer ${t.kind}`);
    const [a] = await q.query<{ placement_ref: string; component_id: string; amount_cents: string }>(
      `update sim.collector_adjustments set applied_at = $2 where ref = $1 and applied_at is null returning placement_ref, component_id, amount_cents`,
      [t.payload.ref, t.dueAt],
    );
    if (!a) return;
    await q.query(`update sim.collector_components set amount_cents = $3 where placement_ref = $1 and component_id = $2`, [a.placement_ref, a.component_id, a.amount_cents]);
    const [p] = await q.query<{ case_id: string | null }>(`select case_id from sim.collector_placements where ref = $1`, [a.placement_ref]);
    if (!p?.case_id) return;
    const status = await statusOf(q, a.placement_ref);
    await appendEvent(q, { caseId: p.case_id, kind: "collector.balance_reported", source: "counterparty", occurredAt: t.dueAt, payload: { ...status } });
  }
}

async function statusOf(q: Queryable, placementRef: string): Promise<PlacementStatus> {
  const rows = await q.query<{ component_id: string; amount_cents: string }>(
    `select component_id, amount_cents from sim.collector_components where placement_ref = $1 order by component_id`,
    [placementRef],
  );
  const components = rows.map((r) => ({ componentId: r.component_id, amountCents: Number(r.amount_cents) }));
  return { ref: placementRef, balanceCents: components.reduce((t, c) => t + c.amountCents, 0), components };
}
