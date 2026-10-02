import { instant } from "./deliveryContracts.js";

/** One working day. Work longer than this runs in daily windows, Monday to Friday. */
export const WORKDAY_MINUTES = 480;
const DAY = 86400000, MINUTE = 60000;
const WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

/** A date as an operator reads it, e.g. "Monday, October 5". Business times are saved at local working hours, so the UTC date is the local date. */
export function longDate(value: string): string {
  const at = new Date(instant(value));
  return `${WEEKDAYS[at.getUTCDay()]}, ${MONTHS[at.getUTCMonth()]} ${at.getUTCDate()}`;
}
function count(value: number, unit: string): string {
  return `${value} ${unit}${value === 1 ? "" : "s"}`;
}
/** A length of work: minutes or hours within a day, working days beyond it. */
export function workingSpan(minutes: number): string {
  if (minutes > WORKDAY_MINUTES) return count(Math.ceil(minutes / WORKDAY_MINUTES), "working day");
  return minutes % 60 === 0 ? count(minutes / 60, "hour") : count(minutes, "minute");
}
/** A plain list: "A", "A and B", "A, B and C". */
export function plainList(items: readonly string[]): string {
  return items.length <= 1 ? items.join("") : `${items.slice(0, -1).join(", ")} and ${items[items.length - 1]}`;
}

function windowStart(day: number, dayStartMs: number): number {
  return day * DAY + dayStartMs;
}
function weekday(ms: number): boolean {
  const d = new Date(ms).getUTCDay();
  return d !== 0 && d !== 6;
}
/** The earliest moment at or after `from` inside a working window that starts daily at `dayStart`'s time of day. */
export function nextWorkingStart(from: string, dayStart: string): string {
  const t = Date.parse(instant(from)), dayStartMs = Date.parse(instant(dayStart)) % DAY, length = WORKDAY_MINUTES * MINUTE;
  for (let day = Math.floor(t / DAY) - 1; ; day += 1) {
    const start = windowStart(day, dayStartMs);
    if (!weekday(start)) continue;
    if (t < start) return new Date(start).toISOString();
    if (t < start + length) return new Date(t).toISOString();
  }
}
/** Add working minutes from a start inside a working window, skipping nights and weekends. */
export function workingEnd(start: string, minutes: number, dayStart: string): string {
  const dayStartMs = Date.parse(instant(dayStart)) % DAY, length = WORKDAY_MINUTES * MINUTE;
  let cursor = Date.parse(nextWorkingStart(start, dayStart)), remaining = minutes * MINUTE;
  for (;;) {
    const day = Math.floor((cursor - dayStartMs) / DAY), end = windowStart(day, dayStartMs) + length;
    const take = Math.min(remaining, end - cursor);
    remaining -= take;
    if (remaining <= 0) return new Date(cursor + take).toISOString();
    cursor = Date.parse(nextWorkingStart(new Date(end).toISOString(), dayStart));
  }
}

/**
 * What the unit is waiting for while vendors work: vendors on site until their end date, then vendors still to book or
 * paid an advance, then the next booked visit. Times are ISO instants on the case clock.
 */
export function deliveryStatus(jobs: ReadonlyArray<{ vendor: string; status: string; appointmentAt?: string; appointmentEndsAt?: string }>, now: string): string {
  const booked = jobs.filter((job) => job.status === "Scheduled" && job.appointmentAt && job.appointmentAt > now)
    .sort((a, b) => a.appointmentAt!.localeCompare(b.appointmentAt!));
  const onSite = jobs.filter((job) => job.status === "Scheduled" && job.appointmentAt && job.appointmentEndsAt
    && job.appointmentAt <= now && job.appointmentEndsAt > now);
  const waitingOn = [...new Set(jobs.filter((job) => !booked.includes(job) && !onSite.includes(job)).map((job) => job.vendor))];
  const working = [...new Map(onSite.map((job) => [job.vendor, job])).values()]
    .map((job) => `${job.vendor} on site until ${longDate(job.appointmentEndsAt!)}.`);
  const next = booked[0] ? `Next visit: ${booked[0].vendor} on ${longDate(booked[0].appointmentAt!)}.` : "";
  return [...working, waitingOn.length ? `Waiting on ${plainList(waitingOn)}.` : "", next].filter(Boolean).join(" ")
    || "Waiting for a payment to be confirmed.";
}
