import type { Ledger, LedgerCode, LedgerPosting, LedgerTransaction } from "../adapters/ledger.js";
import { businessNow } from "../clock.js";
import type { Db, Queryable } from "../db.js";
import { newId } from "../ids.js";
import { faultFor } from "./scenarios.js";

export class SimLedger implements Ledger {
  constructor(private readonly db: Db) {}

  async transactions(tenancyRef: string): Promise<LedgerTransaction[]> {
    const rows = await this.db.query<{ ref: string; posted_on: string | Date; code: LedgerCode; description: string; amount_cents: string }>(
      `select ref, posted_on, code, description, amount_cents from sim.ledger_transactions where tenancy_ref = $1 order by posted_on, seq`,
      [tenancyRef],
    );
    return rows.map((r) => ({ ref: r.ref, postedOn: isoDate(r.posted_on), code: r.code, description: r.description, amountCents: Number(r.amount_cents) }));
  }

  async post(p: LedgerPosting, key: string): Promise<{ ref: string }> {
    const fault = await faultFor(this.db, "ledger", "post");
    fault.before();
    await insertTransaction(this.db, p, key, await businessNow(this.db));
    fault.after();
    const found = await this.find(key);
    if (!found) throw new Error("posting not recorded");
    return found;
  }

  async find(key: string): Promise<{ ref: string } | null> {
    const [r] = await this.db.query<{ ref: string }>(`select ref from sim.ledger_transactions where idempotency_key = $1`, [key]);
    return r ?? null;
  }
}

/** Puts history on the ledger when a world is staged: the deposit, rent and payments before the case began. */
export async function seedLedger(q: Queryable, history: LedgerPosting[], at: Date): Promise<void> {
  for (const p of history) await insertTransaction(q, p, null, at);
}

async function insertTransaction(q: Queryable, p: LedgerPosting, key: string | null, at: Date): Promise<void> {
  await q.query(
    `insert into sim.ledger_transactions (ref, idempotency_key, tenancy_ref, posted_on, code, description, amount_cents, posted_at)
     values ($1, $2, $3, $4, $5, $6, $7, $8) on conflict (idempotency_key) do nothing`,
    [newId("txn"), key, p.tenancyRef, p.postedOn, p.code, p.description, p.amountCents, at],
  );
}

export function isoDate(v: string | Date): string {
  return typeof v === "string" ? v.slice(0, 10) : v.toISOString().slice(0, 10);
}
