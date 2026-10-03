import type { Maintenance, WorkCategory, WorkOrder, WorkOrderRequest } from "../adapters/maintenance.js";
import { businessNow } from "../clock.js";
import type { Db, Queryable } from "../db.js";
import { appendEvent } from "../events.js";
import { newId } from "../ids.js";
import { faultFor, readScenario } from "./scenarios.js";
import { type SimTimer, addBusinessDays, setTimer } from "./timers.js";

/** How the in-house team works each kind of job, and the days it is closed. Hidden from the agent. */
export interface MaintenanceScenario {
  holidays?: string[];
  technician?: string;
  byCategory: Partial<Record<WorkCategory, { businessDays: number; hours: number; hourlyRateCents: number; materialsCents: number }>>;
}

interface WorkOrderRow {
  ref: string;
  status: WorkOrder["status"];
  scheduled_for: Date | null;
  completed_at: Date | null;
  technician: string | null;
  hours: string | null;
  hourly_rate_cents: string | null;
  materials_cents: string | null;
}

export class SimMaintenance implements Maintenance {
  constructor(private readonly db: Db) {}

  async createWorkOrder(r: WorkOrderRequest, key: string): Promise<WorkOrder> {
    const fault = await faultFor(this.db, "maintenance", "create");
    fault.before();
    const now = await businessNow(this.db);
    await this.db.transaction(async (tx) => {
      const plan = (await readScenario<MaintenanceScenario>(tx, "maintenance", "team")) ?? { byCategory: {} };
      const job = plan.byCategory[r.category] ?? { businessDays: 1, hours: 1, hourlyRateCents: 4500, materialsCents: 0 };
      const scheduledFor = addBusinessDays(now, 1, plan.holidays);
      const ref = newId("wo");
      const [inserted] = await tx.query(
        `insert into sim.work_orders (ref, idempotency_key, case_id, unit_ref, category, description, status, scheduled_for, technician, created_at)
         values ($1, $2, $3, $4, $5, $6, 'scheduled', $7, $8, $9) on conflict (idempotency_key) do nothing returning ref`,
        [ref, key, r.caseId, r.unitRef, r.category, r.description, scheduledFor, plan.technician ?? "On-site technician", now],
      );
      if (inserted) {
        await setTimer(tx, {
          system: "maintenance", kind: "complete", dueAt: addBusinessDays(scheduledFor, Math.max(job.businessDays - 1, 0), plan.holidays),
          payload: { ref, hours: job.hours, hourlyRateCents: job.hourlyRateCents, materialsCents: job.materialsCents },
        });
      }
    });
    fault.after();
    const found = await this.find(key);
    if (!found) throw new Error("work order not recorded");
    return found;
  }

  async find(key: string): Promise<WorkOrder | null> {
    const [r] = await this.db.query<WorkOrderRow>(`select * from sim.work_orders where idempotency_key = $1`, [key]);
    return r ? toWorkOrder(r) : null;
  }

  static async onTimer(q: Queryable, t: SimTimer): Promise<void> {
    if (t.kind !== "complete") throw new Error(`maintenance has no timer ${t.kind}`);
    const p = t.payload as { ref: string; hours: number; hourlyRateCents: number; materialsCents: number };
    const [wo] = await q.query<WorkOrderRow & { case_id: string | null; category: string }>(
      `update sim.work_orders set status = 'completed', completed_at = $2, hours = $3, hourly_rate_cents = $4, materials_cents = $5
       where ref = $1 and status <> 'cancelled' returning *`,
      [p.ref, t.dueAt, p.hours, p.hourlyRateCents, p.materialsCents],
    );
    if (!wo?.case_id) return;
    await appendEvent(q, {
      caseId: wo.case_id, kind: "work_order.completed", source: "outside_system", occurredAt: t.dueAt,
      payload: { workOrderRef: wo.ref, category: wo.category, technician: wo.technician, hours: p.hours, hourlyRateCents: p.hourlyRateCents,
        materialsCents: p.materialsCents, photos: [{ name: "after.jpg", ref: `sim://maintenance/${wo.ref}/after.jpg` }] },
    });
  }
}

function toWorkOrder(r: WorkOrderRow): WorkOrder {
  const num = (v: string | null) => (v === null ? null : Number(v));
  return {
    ref: r.ref, status: r.status,
    scheduledFor: r.scheduled_for ? new Date(r.scheduled_for).toISOString() : null,
    completedAt: r.completed_at ? new Date(r.completed_at).toISOString() : null,
    technician: r.technician, hours: num(r.hours), hourlyRateCents: num(r.hourly_rate_cents), materialsCents: num(r.materials_cents),
  };
}
