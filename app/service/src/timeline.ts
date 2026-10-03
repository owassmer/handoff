import type { Db, Queryable } from "./db.js";
import { timerHandlers } from "./sim/index.js";
import { type SimTimer, claimTimer, nextTimer } from "./sim/timers.js";
import { type DueWakeup, fireWakeup, nextWakeup } from "./wakeups.js";

/** The next thing due on the business clock: a case wake-up, or something an imitated system does. */
export type Due = { type: "wakeup"; dueAt: Date; item: DueWakeup } | { type: "timer"; dueAt: Date; item: SimTimer };

/** The earliest item due no later than `notAfter`. The outside world acts before a case wakes at the same moment. */
export async function nextDue(q: Queryable, notAfter: Date): Promise<Due | null> {
  const [w, t] = await Promise.all([nextWakeup(q, notAfter), nextTimer(q, notAfter)]);
  if (t && (!w || t.dueAt.getTime() <= w.dueAt.getTime())) return { type: "timer", dueAt: t.dueAt, item: t };
  if (w) return { type: "wakeup", dueAt: w.dueAt, item: w };
  return null;
}

/** Fires one due item at business time `at`. Returns a line describing it. */
export async function fire(db: Db, due: Due, at: Date): Promise<string> {
  return db.transaction(async (tx) => {
    if (due.type === "wakeup") {
      await fireWakeup(tx, { ...due.item, dueAt: at });
      return `${at.toISOString()} wake ${due.item.caseId}: ${due.item.reason}`;
    }
    if (!(await claimTimer(tx, due.item.id, at))) return `${at.toISOString()} ${due.item.system}.${due.item.kind} already fired`;
    const handler = timerHandlers[due.item.system];
    if (!handler) throw new Error(`no imitated system ${due.item.system}`);
    await handler(tx, { ...due.item, dueAt: at });
    return `${at.toISOString()} ${due.item.system}.${due.item.kind}`;
  });
}
