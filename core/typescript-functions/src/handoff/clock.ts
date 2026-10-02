import type { Osdk } from "@osdk/client";
import type { HandoffAgentWork } from "@ontology/sdk";
import { instant } from "./deliveryContracts.js";
import { dateOnly } from "./values.js";

/**
 * The case clock: the business time saved at the handoff's last step plus the real time since that step.
 * Every visible record (messages, activity, decisions) is stamped on it, so dates on screen agree even though
 * waiting periods are compressed. Scheduling (nextWakeAt, updatedAt) stays on real time.
 */
export function caseTime(work: Pick<Osdk.Instance<HandoffAgentWork>, "businessTime" | "updatedAt"> | undefined, wallTime: string): string {
  const wall = instant(wallTime);
  if (!work?.businessTime) return wall;
  if (!work.updatedAt) return instant(work.businessTime);
  return new Date(Date.parse(instant(work.businessTime)) + Math.max(0, Date.parse(wall) - Date.parse(instant(work.updatedAt)))).toISOString();
}
/** Counterpart business dates and server scheduling are separate; no operator clock command is needed. */
export function businessMoment(work: Osdk.Instance<HandoffAgentWork>, businessDate: string, wallTime: string): string {
  const wall = instant(wallTime), date = dateOnly(businessDate, "Business date");
  const current = instant(work.businessTime ? caseTime(work, wall) : `${date}T${wall.slice(11)}`);
  if (work.nextBusinessAt && work.nextWakeAt && instant(work.nextWakeAt) <= wall && instant(work.nextBusinessAt) > current) return instant(work.nextBusinessAt);
  return instant(current);
}
/** Test counterparts compress long waiting periods, not event ordering or quoted business dates. */
export function wakeTime(wallTime: string, businessTime: string, businessDue?: string): string | undefined {
  if (!businessDue) return undefined;
  const delay = Math.min(60000, Math.max(1000, Date.parse(instant(businessDue)) - Date.parse(instant(businessTime))));
  return new Date(Date.parse(instant(wallTime)) + delay).toISOString();
}
