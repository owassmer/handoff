import type { Mail, OutgoingMessage, SentMessage } from "../adapters/mail.js";
import { businessNow } from "../clock.js";
import type { Db } from "../db.js";
import { newId } from "../ids.js";
import { useScenario } from "./scenarios.js";

export class SimMail implements Mail {
  constructor(private readonly db: Db) {}

  async send(m: OutgoingMessage, key: string): Promise<SentMessage> {
    const fault = await useScenario(this.db, "mail", "send");
    if (fault?.mode === "timeout-before-send") throw new Error("mail provider timed out");
    const sentAt = await businessNow(this.db);
    await this.db.query(
      `insert into sim.outbox (id, idempotency_key, case_id, to_party_id, to_address, subject, body, attachments, sent_at)
       values ($1, $2, $3, $4, $5, $6, $7, $8, $9) on conflict (idempotency_key) do nothing`,
      [newId("msg"), key, m.caseId, m.toPartyId, m.toAddress, m.subject, m.body, m.attachments, sentAt],
    );
    if (fault?.mode === "timeout-after-send") throw new Error("mail provider timed out");
    const sent = await this.find(key);
    if (!sent) throw new Error("message not recorded");
    return sent;
  }

  async find(key: string): Promise<SentMessage | null> {
    const [r] = await this.db.query<{ id: string; sent_at: Date }>(`select id, sent_at from sim.outbox where idempotency_key = $1`, [key]);
    return r ? { messageId: r.id, sentAt: new Date(r.sent_at).toISOString() } : null;
  }

  /** What a recipient has received, oldest first. Used by the simulated tenant and by tests. */
  async inbox(partyId: string): Promise<Array<{ id: string; subject: string; body: string; attachments: unknown[]; sentAt: Date }>> {
    const rows = await this.db.query<{ id: string; subject: string; body: string; attachments: unknown[]; sent_at: Date }>(
      `select id, subject, body, attachments, sent_at from sim.outbox where to_party_id = $1 order by sent_at, id`,
      [partyId],
    );
    return rows.map((r) => ({ id: r.id, subject: r.subject, body: r.body, attachments: r.attachments, sentAt: new Date(r.sent_at) }));
  }
}
