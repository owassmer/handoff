export function money(cents: string, currency: string): string {
  try {
    const value = BigInt(cents);
    const format = new Intl.NumberFormat(undefined, {
      style: "currency",
      currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
    return format
      .formatToParts(value / 100n)
      .map((part) =>
        part.type === "fraction" ? (value % 100n).toString().padStart(2, "0") : part.value,
      )
      .join("");
  } catch {
    return "Amount unavailable";
  }
}
export function calendarDate(value: string): string {
  const date = new Date(value.slice(0, 10) + "T12:00:00Z");
  return Number.isNaN(date.getTime())
    ? "Date unavailable"
    : new Intl.DateTimeFormat(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
        timeZone: "UTC",
      }).format(date);
}
export function appointmentTime(value: string): string {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? "Time not available"
    : new Intl.DateTimeFormat(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        timeZoneName: "short",
      }).format(date);
}
export function readablePerson(value: string): string {
  return !value || /^(ri\.|[\da-f]{8}-[\da-f-]{27,})/i.test(value) ? "A team member" : value;
}
/** A short local time for correspondence and activity, e.g. "Sep 26, 3:04 PM". */
export function shortTime(value: string): string {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? ""
    : new Intl.DateTimeFormat(undefined, {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      }).format(date);
}
