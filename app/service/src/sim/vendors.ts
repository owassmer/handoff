import type { QuoteRequest, VendorOrder, Vendors } from "../adapters/vendors.js";
import { businessNow } from "../clock.js";
import type { Db, Queryable } from "../db.js";
import { appendEvent } from "../events.js";
import { newId } from "../ids.js";
import { faultFor, readScenario } from "./scenarios.js";
import { type SimTimer, addBusinessDays, setTimer } from "./timers.js";

/** How a vendor will behave, keyed by its party id. Hidden from the agent. */
export interface VendorScenario {
  holidays?: string[];
  quote: { afterBusinessDays: number; options: Array<{ option: string; amountCents: number; description: string }> };
  job: { businessDays: number };
  /** The invoice amount; omitted means the order's not-to-exceed amount. */
  invoice: { afterBusinessDays: number; amountCents?: number };
}

export class SimVendors implements Vendors {
  constructor(private readonly db: Db) {}

  requestQuote(r: QuoteRequest, key: string): Promise<{ ref: string }> {
    return this.receive("quote", r.caseId, r.vendorPartyId, r.scope, null, key);
  }

  placeOrder(o: VendorOrder, key: string): Promise<{ ref: string }> {
    return this.receive("order", o.caseId, o.vendorPartyId, o.scope, o.notToExceedCents, key);
  }

  async find(key: string): Promise<{ ref: string } | null> {
    const [r] = await this.db.query<{ ref: string }>(`select ref from sim.vendor_requests where idempotency_key = $1`, [key]);
    return r ?? null;
  }

  private async receive(kind: "quote" | "order", caseId: string, vendorPartyId: string, scope: string, notToExceed: number | null, key: string): Promise<{ ref: string }> {
    const fault = await faultFor(this.db, "vendors", kind);
    fault.before();
    const now = await businessNow(this.db);
    await this.db.transaction(async (tx) => {
      const plan = await readScenario<VendorScenario>(tx, "vendors", vendorPartyId);
      if (!plan) throw new Error(`vendor ${vendorPartyId} does not respond`);
      const ref = newId(kind === "quote" ? "vq" : "vjob");
      const [inserted] = await tx.query(
        `insert into sim.vendor_requests (ref, idempotency_key, case_id, vendor_party_id, kind, scope, not_to_exceed_cents, status, created_at)
         values ($1, $2, $3, $4, $5, $6, $7, 'received', $8) on conflict (idempotency_key) do nothing returning ref`,
        [ref, key, caseId, vendorPartyId, kind, scope, notToExceed, now],
      );
      if (!inserted) return;
      if (kind === "quote") {
        await setTimer(tx, { system: "vendors", kind: "quote", dueAt: addBusinessDays(now, plan.quote.afterBusinessDays, plan.holidays), payload: { ref } });
      } else {
        await setTimer(tx, { system: "vendors", kind: "complete", dueAt: addBusinessDays(now, plan.job.businessDays, plan.holidays), payload: { ref } });
      }
    });
    fault.after();
    const found = await this.find(key);
    if (!found) throw new Error("vendor request not recorded");
    return found;
  }

  /** The vendor answers by email: a quote, a completion notice, an invoice. Untrusted, like any counterparty. */
  static async onTimer(q: Queryable, t: SimTimer): Promise<void> {
    const [r] = await q.query<{ ref: string; case_id: string; vendor_party_id: string; scope: string; not_to_exceed_cents: string | null }>(
      `select ref, case_id, vendor_party_id, scope, not_to_exceed_cents from sim.vendor_requests where ref = $1`,
      [t.payload.ref],
    );
    if (!r) return;
    const plan = await readScenario<VendorScenario>(q, "vendors", r.vendor_party_id);
    if (!plan) return;
    const event = (kind: string, payload: Record<string, unknown>) =>
      appendEvent(q, { caseId: r.case_id, kind, source: "counterparty", occurredAt: t.dueAt, payload: { vendorPartyId: r.vendor_party_id, ref: r.ref, ...payload } });

    if (t.kind === "quote") {
      await q.query(`update sim.vendor_requests set status = 'quoted' where ref = $1`, [r.ref]);
      await event("vendor.quote_received", { scope: r.scope, options: plan.quote.options, document: { name: "quote.pdf", ref: `sim://vendors/${r.ref}/quote.pdf` } });
    } else if (t.kind === "complete") {
      await q.query(`update sim.vendor_requests set status = 'completed' where ref = $1`, [r.ref]);
      await event("vendor.job_completed", { photos: [{ name: "after.jpg", ref: `sim://vendors/${r.ref}/after.jpg` }] });
      await setTimer(q, { system: "vendors", kind: "invoice", dueAt: addBusinessDays(t.dueAt, plan.invoice.afterBusinessDays, plan.holidays), payload: { ref: r.ref } });
    } else if (t.kind === "invoice") {
      await q.query(`update sim.vendor_requests set status = 'invoiced' where ref = $1`, [r.ref]);
      const amountCents = plan.invoice.amountCents ?? Number(r.not_to_exceed_cents ?? 0);
      await event("vendor.invoice_received", { amountCents, document: { name: "invoice.pdf", ref: `sim://vendors/${r.ref}/invoice.pdf` } });
    } else {
      throw new Error(`vendors has no timer ${t.kind}`);
    }
  }
}
