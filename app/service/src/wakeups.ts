import type { Queryable } from "./db.js";
import { appendEvent } from "./events.js";

export interface Wakeup {
  caseId: string;
  dueAt: Date;
  reason: string;
  payload?: Record<string, unknown>;
  /** Scheduling again under the same key moves the existing wake-up instead of adding one. */
  key?: string;
}

export async function scheduleWakeup(q: Queryable, w: Wakeup): Promise<void> {
  if (w.key === undefined) {
    await q.query(`insert into wakeups (case_id, due_at, reason, payload) values ($1, $2, $3, $4)`, [w.caseId, w.dueAt, w.reason, w.payload ?? {}]);
    return;
  }
  await q.query(
    `insert into wakeups (case_id, due_at, reason, payload, key) values ($1, $2, $3, $4, $5)
     on conflict (case_id, key) do update
       set due_at = excluded.due_at, reason = excluded.reason, payload = excluded.payload, cancelled_at = null, fired_at = null`,
    [w.caseId, w.dueAt, w.reason, w.payload ?? {}, w.key],
  );
}

export async function cancelWakeup(q: Queryable, caseId: string, key: string, at: Date): Promise<void> {
  await q.query(`update wakeups set cancelled_at = $3 where case_id = $1 and key = $2 and fired_at is null`, [caseId, key, at]);
}

export interface DueWakeup {
  id: number;
  caseId: string;
  dueAt: Date;
  reason: string;
  payload: Record<string, unknown>;
  key: string | null;
}

export async function nextWakeup(q: Queryable, notAfter: Date): Promise<DueWakeup | null> {
  const [r] = await q.query<{ id: string; case_id: string; due_at: Date; reason: string; payload: Record<string, unknown>; key: string | null }>(
    `select id, case_id, due_at, reason, payload, key from wakeups
     where fired_at is null and cancelled_at is null and due_at <= $1 order by due_at, id limit 1`,
    [notAfter],
  );
  return r ? { id: Number(r.id), caseId: r.case_id, dueAt: new Date(r.due_at), reason: r.reason, payload: r.payload, key: r.key } : null;
}

/** A due wake-up becomes a clock event in the case's inbox. */
export async function fireWakeup(q: Queryable, w: DueWakeup): Promise<void> {
  const [fired] = await q.query(`update wakeups set fired_at = $2 where id = $1 and fired_at is null and cancelled_at is null returning id`, [w.id, w.dueAt]);
  if (!fired) return;
  await appendEvent(q, {
    caseId: w.caseId,
    kind: "wakeup",
    source: "clock",
    payload: { reason: w.reason, key: w.key, ...w.payload },
    occurredAt: w.dueAt,
  });
}
