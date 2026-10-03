import { type PaymentOrder, type PaymentReceipt, type Payments, PaymentDeclined } from "../adapters/payments.js";
import { businessNow } from "../clock.js";
import type { Db, Queryable } from "../db.js";
import { appendEvent } from "../events.js";
import { newId } from "../ids.js";
import { useScenario } from "./scenarios.js";
import { type SimTimer, addBusinessDays, setTimer } from "./timers.js";

/** Electronic transfers settle in two business days; a mailed check is cashed about a week later. */
const SETTLE = { electronic_transfer: 2, mailed_check: 5 } as const;

interface PaymentRow {
  id: string;
  status: PaymentReceipt["status"];
  submitted_at: Date;
}

export class SimPayments implements Payments {
  constructor(private readonly db: Db) {}

  async send(order: PaymentOrder, key: string): Promise<PaymentReceipt> {
    const fault = await useScenario(this.db, "payments", "send");
    if (fault?.mode === "decline") throw new PaymentDeclined(String(fault.reason ?? "declined by the bank"));
    if (fault?.mode === "timeout-before-send") throw new Error("bank did not respond");

    const now = await businessNow(this.db);
    await this.db.transaction(async (tx) => {
      const [inserted] = await tx.query<{ id: string }>(
        `insert into sim.payments (id, idempotency_key, case_id, payee_party_id, amount_cents, method, memo, status, submitted_at)
         values ($1, $2, $3, $4, $5, $6, $7, 'submitted', $8) on conflict (idempotency_key) do nothing returning id`,
        [newId("pay"), key, order.caseId, order.payeePartyId, order.amountCents, order.method, order.memo, now],
      );
      if (inserted) {
        await setTimer(tx, { system: "payments", kind: "settle", dueAt: addBusinessDays(now, SETTLE[order.method]), payload: { paymentId: inserted.id } });
      }
    });
    if (fault?.mode === "timeout-after-send") throw new Error("bank did not respond");
    const receipt = await this.find(key);
    if (!receipt) throw new Error("payment not recorded");
    return receipt;
  }

  async find(key: string): Promise<PaymentReceipt | null> {
    const [r] = await this.db.query<PaymentRow>(`select id, status, submitted_at from sim.payments where idempotency_key = $1`, [key]);
    return r ? { paymentId: r.id, status: r.status, submittedAt: new Date(r.submitted_at).toISOString() } : null;
  }

  /** The bank's own view, for tests and the staging tools. Never exposed to the agent. */
  async all(): Promise<Array<{ id: string; caseId: string | null; payeePartyId: string; amountCents: number; method: string; status: string }>> {
    const rows = await this.db.query<{ id: string; case_id: string | null; payee_party_id: string; amount_cents: string; method: string; status: string }>(
      `select id, case_id, payee_party_id, amount_cents, method, status from sim.payments order by submitted_at, id`,
    );
    return rows.map((r) => ({ id: r.id, caseId: r.case_id, payeePartyId: r.payee_party_id, amountCents: Number(r.amount_cents), method: r.method, status: r.status }));
  }

  /** Runs when a settlement timer comes due: the bank reports the payment settled. */
  static async onTimer(q: Queryable, t: SimTimer): Promise<void> {
    if (t.kind !== "settle") throw new Error(`payments has no timer ${t.kind}`);
    const [p] = await q.query<{ id: string; case_id: string | null; amount_cents: string }>(
      `update sim.payments set status = 'settled', settled_at = $2 where id = $1 and status = 'submitted' returning id, case_id, amount_cents`,
      [t.payload.paymentId, t.dueAt],
    );
    if (p?.case_id) {
      await appendEvent(q, {
        caseId: p.case_id,
        kind: "payment.settled",
        source: "outside_system",
        payload: { paymentId: p.id, amountCents: Number(p.amount_cents) },
        occurredAt: t.dueAt,
      });
    }
  }
}
