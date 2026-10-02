/** Pure Gregorian/UTC helpers. Never round microseconds through JavaScript Date. */

export function is_calendar_date(value: string): boolean {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (match === null) return false;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  if (year < 1 || year > 9999 || month < 1 || month > 12) return false;
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const length = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1];
  return length !== undefined && day >= 1 && day <= length;
}

/** Accept supported ISO calendar, basic and week-date forms. */
function iso_date(value: string): string | null {
  const basic = /^(\d{4})(\d{2})(\d{2})$/.exec(value);
  const calendar = basic === null ? value : `${basic[1]}-${basic[2]}-${basic[3]}`;
  if (is_calendar_date(calendar)) return calendar;
  const week = /^(\d{4})(-?)W(\d{2})(?:\2([1-7]))?$/.exec(value);
  if (week === null) return null;
  const year = Number(week[1]);
  const weekNumber = Number(week[3]);
  const weekday = Number(week[4] ?? "1");
  if (year < 1 || year > 9999 || weekNumber < 1 || weekNumber > 53) return null;
  const january4 = new Date(`${week[1]}-01-04T00:00:00Z`);
  const mondayOffset = (january4.getUTCDay() + 6) % 7;
  const firstMonday = january4.getTime() - mondayOffset * 86_400_000;
  const result = new Date(firstMonday + ((weekNumber - 1) * 7 + weekday - 1) * 86_400_000);
  const thursday = new Date(firstMonday + ((weekNumber - 1) * 7 + 3) * 86_400_000);
  if (thursday.getUTCFullYear() !== year) return null;
  const normalized = result.toISOString().slice(0, 10);
  return is_calendar_date(normalized) ? normalized : null;
}

/**
 * Normalize explicit UTC input: no fraction when zero,
 * otherwise exactly six microsecond digits. Extra submicrosecond digits truncate.
 * Return null for invalid values, so codec owns the user-visible ContractError.
 */
export function normalize_timestamp(value: string): string | null {
  if (!value.endsWith("Z")) return null;
  const split = value.slice(0, -1).split("T");
  if (split.length !== 2) return null;
  const datePart = iso_date(split[0] ?? "");
  const timePart = split[1] ?? "";
  if (datePart === null) return null;
  const time = /^(\d{2})(?:(:?)(\d{2})(?:\2(\d{2}))?)?(?:[.,](\d+))?$/.exec(timePart);
  if (time === null) return null;
  const hours = Number(time[1]);
  const minutes = Number(time[3] ?? "0");
  const seconds = Number(time[4] ?? "0");
  if (hours > 23 || minutes > 59 || seconds > 59) return null;
  const micros = (time[5] ?? "").slice(0, 6).padEnd(6, "0");
  const fraction = micros === "000000" ? "" : `.${micros}`;
  return `${datePart}T${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}${fraction}Z`;
}

/** Exact instant for chronological comparison, including submillisecond precision. */
export function timestamp_microseconds(value: string): bigint {
  const normalized = normalize_timestamp(value);
  if (normalized === null) throw new RangeError("Expected a valid explicit UTC timestamp");
  const seconds = normalized.slice(0, 19);
  const microseconds = normalized.length > 20 ? normalized.slice(20, 26) : "000000";
  return BigInt(Date.parse(`${seconds}Z`)) * 1000n + BigInt(microseconds);
}

export function compare_timestamps(left: string, right: string): number {
  const a = timestamp_microseconds(left);
  const b = timestamp_microseconds(right);
  return a < b ? -1 : a > b ? 1 : 0;
}

export function add_days(value: string, days: number): string {
  if (!is_calendar_date(value) || !Number.isSafeInteger(days)) {
    throw new RangeError("Expected a calendar date and exact integer day count");
  }
  const result = new Date(`${value}T00:00:00Z`);
  result.setUTCDate(result.getUTCDate() + days);
  const normalized = result.toISOString().slice(0, 10);
  if (!is_calendar_date(normalized)) throw new RangeError("Calendar date outside years 1..9999");
  return normalized;
}
