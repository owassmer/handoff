/**
 * Calendar dates and moments in California business time.
 *
 * A date is an ISO calendar date, "2026-12-07". A moment is an ISO date-time; one written without an
 * offset ("2026-11-02T10:00") is a California wall-clock time. Results are written back the same way:
 * dates as "YYYY-MM-DD", moments as California time with its offset ("2026-10-31T11:00:00-07:00").
 */

export const BUSINESS_TIME_ZONE = "America/Los_Angeles";

const DATE = /^(\d{4})-(\d{2})-(\d{2})$/;
const DATE_TIME = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?(Z|[+-]\d{2}:\d{2})?$/;
const DAY_MS = 86_400_000;

function validDay(y: number, m: number, d: number): boolean {
  const t = new Date(Date.UTC(y, m - 1, d));
  return t.getUTCFullYear() === y && t.getUTCMonth() === m - 1 && t.getUTCDate() === d;
}

export function isDate(v: unknown): v is string {
  if (typeof v !== "string") return false;
  const m = DATE.exec(v);
  return !!m && validDay(Number(m[1]), Number(m[2]), Number(m[3]));
}

export function isDateTime(v: unknown): v is string {
  if (typeof v !== "string") return false;
  const m = DATE_TIME.exec(v);
  if (!m || !validDay(Number(m[1]), Number(m[2]), Number(m[3]))) return false;
  return Number(m[4]) < 24 && Number(m[5]) < 60 && Number(m[6] ?? 0) < 60;
}

export function isTemporal(v: unknown): v is string {
  return isDate(v) || isDateTime(v);
}

/** Days since 1970-01-01 for a calendar date. */
function dayNumber(date: string): number {
  const [y, m, d] = date.split("-").map(Number) as [number, number, number];
  return Date.UTC(y, m - 1, d) / DAY_MS;
}

function fromDayNumber(n: number): string {
  return new Date(n * DAY_MS).toISOString().slice(0, 10);
}

export function addDays(date: string, n: number): string {
  return fromDayNumber(dayNumber(date) + n);
}

/** Calendar days from a to b (positive when b is later). */
export function daysBetween(a: string, b: string): number {
  return dayNumber(b) - dayNumber(a);
}

const parts = new Intl.DateTimeFormat("en-US", {
  timeZone: BUSINESS_TIME_ZONE,
  hourCycle: "h23",
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
});

/** The California wall clock at an instant, as UTC-shaped fields. */
function wallClock(ms: number): { y: number; mo: number; d: number; h: number; mi: number; s: number } {
  const p: Record<string, number> = {};
  for (const part of parts.formatToParts(new Date(ms))) if (part.type !== "literal") p[part.type] = Number(part.value);
  return { y: p.year!, mo: p.month!, d: p.day!, h: p.hour!, mi: p.minute!, s: p.second! };
}

/** Minutes California time is ahead of UTC at an instant (negative: -480 or -420). */
function offsetMinutes(ms: number): number {
  const w = wallClock(ms);
  const wall = Date.UTC(w.y, w.mo - 1, w.d, w.h, w.mi, w.s);
  return Math.round((wall - Math.floor(ms / 1000) * 1000) / 60_000);
}

/** The instant (epoch ms) of a date-time; one without an offset is California time. */
export function instantOf(dateTime: string): number {
  const m = DATE_TIME.exec(dateTime);
  if (!m) throw new Error(`not a date-time: ${dateTime}`);
  const ms = m[7] ? Number(`0.${m[7]}`) * 1000 : 0;
  const wall = Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3]), Number(m[4]), Number(m[5]), Number(m[6] ?? 0), Math.round(ms));
  const zone = m[8];
  if (zone === "Z") return wall;
  if (zone) {
    const sign = zone.startsWith("-") ? -1 : 1;
    const [hh, mm] = zone.slice(1).split(":").map(Number) as [number, number];
    return wall - sign * (hh * 60 + mm) * 60_000;
  }
  // Wall-clock time in California: correct the guess once for the offset in force then.
  const first = wall - offsetMinutes(wall) * 60_000;
  const second = wall - offsetMinutes(first) * 60_000;
  return second;
}

const pad = (n: number, w = 2) => String(Math.abs(n)).padStart(w, "0");

/** An instant written as California time with its offset. */
export function formatInstant(ms: number): string {
  const w = wallClock(ms);
  const off = offsetMinutes(ms);
  const sign = off < 0 ? "-" : "+";
  return `${pad(w.y, 4)}-${pad(w.mo)}-${pad(w.d)}T${pad(w.h)}:${pad(w.mi)}:${pad(w.s)}${sign}${pad(Math.trunc(Math.abs(off) / 60))}:${pad(Math.abs(off) % 60)}`;
}

/** The California calendar date of a date or date-time. */
export function businessDate(v: string): string {
  if (isDate(v)) return v;
  const w = wallClock(instantOf(v));
  return `${pad(w.y, 4)}-${pad(w.mo)}-${pad(w.d)}`;
}

/** Orders two dates or date-times. A date against a date-time compares California calendar dates. */
export function compareTemporal(a: string, b: string): number {
  if (isDateTime(a) && isDateTime(b)) return Math.sign(instantOf(a) - instantOf(b));
  return Math.sign(daysBetween(businessDate(b), businessDate(a)));
}

/** Days in the calendar month of a date. */
export function daysInMonth(date: string): number {
  const [y, m] = date.split("-").map(Number) as [number, number];
  return new Date(Date.UTC(y, m, 0)).getUTCDate();
}
