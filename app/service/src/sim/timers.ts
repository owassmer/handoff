import { DAY_MS, businessDate } from "../clock.js";
import type { Queryable } from "../db.js";

export interface SimTimer {
  id: number;
  system: string;
  kind: string;
  dueAt: Date;
  payload: Record<string, unknown>;
}

export async function setTimer(q: Queryable, t: Omit<SimTimer, "id">): Promise<void> {
  await q.query(`insert into sim.timers (system, kind, due_at, payload) values ($1, $2, $3, $4)`, [t.system, t.kind, t.dueAt, t.payload]);
}

export async function nextTimer(q: Queryable, notAfter: Date): Promise<SimTimer | null> {
  const [r] = await q.query<{ id: string; system: string; kind: string; due_at: Date; payload: Record<string, unknown> }>(
    `select id, system, kind, due_at, payload from sim.timers where fired_at is null and due_at <= $1 order by due_at, id limit 1`,
    [notAfter],
  );
  return r ? { id: Number(r.id), system: r.system, kind: r.kind, dueAt: new Date(r.due_at), payload: r.payload } : null;
}

/** Marks a timer fired; false if it already was. */
export async function claimTimer(q: Queryable, id: number, at: Date): Promise<boolean> {
  return (await q.query(`update sim.timers set fired_at = $2 where id = $1 and fired_at is null returning id`, [id, at])).length > 0;
}

/** Business days forward from `t`: weekdays in business time, skipping the given holidays (YYYY-MM-DD). */
export function addBusinessDays(t: Date, days: number, holidays: readonly string[] = []): Date {
  let d = new Date(t);
  let left = days;
  while (left > 0) {
    d = new Date(d.getTime() + DAY_MS);
    const date = businessDate(d);
    const weekday = new Date(`${date}T12:00:00Z`).getUTCDay();
    if (weekday !== 0 && weekday !== 6 && !holidays.includes(date)) left--;
  }
  return d;
}
