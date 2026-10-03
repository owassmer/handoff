import type { Queryable } from "./db.js";

/**
 * Business time. In production it is real time. In a simulated world it is a stored value that
 * only moves forward, when the world is advanced.
 */
export type ClockMode = "real" | "simulated";

export async function setupClock(q: Queryable, mode: ClockMode, start: Date = new Date()): Promise<void> {
  await q.query(
    `insert into clock (only_row, mode, now) values (true, $1, $2)
     on conflict (only_row) do update set mode = excluded.mode, now = excluded.now`,
    [mode, start],
  );
}

export async function clockMode(q: Queryable): Promise<ClockMode> {
  const [row] = await q.query<{ mode: ClockMode }>(`select mode from clock`);
  if (!row) throw new Error("clock is not set up");
  return row.mode;
}

export async function businessNow(q: Queryable): Promise<Date> {
  const [row] = await q.query<{ mode: ClockMode; now: Date }>(`select mode, now from clock`);
  if (!row) throw new Error("clock is not set up");
  return row.mode === "real" ? new Date() : new Date(row.now);
}

/** Moves a simulated clock forward. Time never runs backwards. */
export async function setSimulatedNow(q: Queryable, to: Date): Promise<void> {
  const [row] = await q.query<{ mode: ClockMode; now: Date }>(`select mode, now from clock`);
  if (!row) throw new Error("clock is not set up");
  if (row.mode !== "simulated") throw new Error("only a simulated clock can be moved");
  if (to.getTime() < new Date(row.now).getTime()) throw new Error(`clock cannot go back from ${new Date(row.now).toISOString()} to ${to.toISOString()}`);
  await q.query(`update clock set now = $1`, [to]);
}

export const DAY_MS = 24 * 60 * 60 * 1000;

export function addDays(t: Date, days: number): Date {
  return new Date(t.getTime() + days * DAY_MS);
}
