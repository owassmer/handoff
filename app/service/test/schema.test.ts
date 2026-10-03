import { readdir } from "node:fs/promises";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { contentHash } from "../src/canonical.js";
import { setupClock } from "../src/clock.js";
import { type PgliteDb, migrate, openMemoryDb } from "../src/db.js";
import { appendEvent } from "../src/events.js";
import { at, seedCase } from "./helpers.js";

let db: PgliteDb;
beforeEach(async () => {
  db = await openMemoryDb();
  await setupClock(db, "simulated", at("2026-10-12T16:00:00Z"));
  await seedCase(db);
});
afterEach(() => db.close());

describe("records the database itself protects", () => {
  it("applies migrations once", async () => {
    await migrate(db);
    const rows = await db.query<{ name: string }>(`select name from schema_migrations order by name`);
    const files = (await readdir(new URL("../src/migrations/", import.meta.url))).filter((f) => f.endsWith(".sql")).sort();
    expect(rows.map((r) => r.name)).toEqual(files);
  });

  it("keeps events append-only, letting processed_at be set once", async () => {
    const e = await appendEvent(db, { caseId: "case-1", kind: "notice", source: "tenant", payload: { text: "moving out" }, occurredAt: at("2026-10-12T16:00:00Z") });
    await expect(db.query(`delete from events where id = $1`, [e.id])).rejects.toThrow(/append-only/);
    await expect(db.query(`update events set payload = '{"text":"staying"}' where id = $1`, [e.id])).rejects.toThrow(/append-only/);
    await db.query(`update events set processed_at = now() where id = $1`, [e.id]);
    await expect(db.query(`update events set processed_at = now() + interval '1 day' where id = $1`, [e.id])).rejects.toThrow(/append-only/);
  });

  it("derives trust from the source, so a tenant message can never be marked trusted", async () => {
    const e = await appendEvent(db, { caseId: "case-1", kind: "message.received", source: "tenant", payload: {}, occurredAt: at("2026-10-12T16:00:00Z") });
    expect(e.trusted).toBe(false);
    await expect(db.query(
      `insert into events (case_id, kind, source, trusted, payload, occurred_at) values ('case-1', 'message.received', 'counterparty', true, '{}', now())`,
    )).rejects.toThrow(/check constraint/);
  });

  it("fixes decision content once proposed, and a decision once decided", async () => {
    const content = { refund: { amountCents: 100 } };
    await db.query(
      `insert into decisions (id, case_id, kind, content, content_hash, status, proposed_by, proposed_at, decided_by, decided_at)
       values ('d1', 'case-1', 'account.statement', $1, $2, 'accepted', 'agent:r', now(), 'op-decider', now())`,
      [content, contentHash(content)],
    );
    await expect(db.query(`update decisions set content = '{"refund":{"amountCents":999}}' where id = 'd1'`)).rejects.toThrow(/cannot change/);
    await expect(db.query(`update decisions set note = 'edited later' where id = 'd1'`)).rejects.toThrow(/cannot change/);
    await expect(db.query(`update decisions set status = 'declined' where id = 'd1'`)).rejects.toThrow(/cannot change/);
    await db.query(`update decisions set status = 'superseded' where id = 'd1'`);
    await expect(db.query(`delete from decisions where id = 'd1'`)).rejects.toThrow(/kept/);
  });

  it("makes an action's outcome final once it has one", async () => {
    await db.query(
      `insert into actions (case_id, kind, idempotency_key, requested_by, request, status, result, requested_at)
       values ('case-1', 'payment.refund', 'k1', 'agent:r', '{}', 'succeeded', '{"paymentId":"p1"}', now())`,
    );
    await expect(db.query(`update actions set status = 'failed' where idempotency_key = 'k1'`)).rejects.toThrow(/final/);
    await expect(db.query(`update actions set request = '{"amountCents":1}' where idempotency_key = 'k1'`)).rejects.toThrow(/cannot change/);
  });
});
