import { createHash } from "node:crypto";
import { UserFacingError } from "@osdk/functions";

export function requireHandoff(condition: unknown, message: string): asserts condition {
  if (!condition) throw new UserFacingError(message);
}

export function words(value: unknown, label: string, max = 4000): string {
  requireHandoff(typeof value === "string" && value.trim().length > 0 && value === value.trim()
    && value.length <= max, `${label} must be complete and within its size limit.`);
  return value;
}

export function details(value: unknown, required: string[], optional: string[], label: string): Record<string, unknown> {
  requireHandoff(typeof value === "object" && value !== null && !Array.isArray(value), `${label} needs more details.`);
  const result = value as Record<string, unknown>;
  requireHandoff(required.every((key) => Object.hasOwn(result, key))
    && Object.keys(result).every((key) => required.includes(key) || optional.includes(key)),
  `${label} has missing or unexpected details.`);
  return result;
}

export function entries(value: unknown, label: string, max = 24, min = 0): unknown[] {
  requireHandoff(Array.isArray(value) && value.length >= min && value.length <= max,
    `${label} must contain between ${min} and ${max} entries.`);
  return value as unknown[];
}

export function wordList(value: unknown, label: string, max = 24, min = 0, width = 160): string[] {
  const result = entries(value, label, max, min).map((entry) => words(entry, label, width));
  requireHandoff(new Set(result).size === result.length, `${label} repeats an entry.`);
  return result;
}

export function dateOnly(value: unknown, label: string): string {
  const date = words(value, label, 10);
  requireHandoff(/^\d{4}-\d{2}-\d{2}$/.test(date) && !Number.isNaN(Date.parse(`${date}T00:00:00Z`))
    && new Date(`${date}T00:00:00Z`).toISOString().slice(0, 10) === date, `${label} must be a calendar date.`);
  return date;
}

export function whole(value: unknown, label: string, max = 1_000_000_000n): string {
  requireHandoff(typeof value === "string" && /^(0|[1-9][0-9]{0,9})$/.test(value)
    && BigInt(value) <= max, `${label} must be a supported nonnegative whole number.`);
  return value;
}

export function cents(value: unknown): string {
  return whole(value, "Work budget in cents", 100_000_000n);
}

export function nextRevision(value: unknown): string {
  return whole((BigInt(whole(value, "Revision")) + 1n).toString(), "Revision");
}

export function parseDetails(value: string, label: string, max = 400000): unknown {
  requireHandoff(value.length <= max, `${label} is too long. Choose a smaller set of details.`);
  try {
    return JSON.parse(value) as unknown;
  } catch (error: unknown) {
    if (!(error instanceof SyntaxError)) throw error;
    throw new UserFacingError(`${label} could not be read. Check its format and try again.`);
  }
}

/** Stable serialization for comparing command intent, not for editing records. */
export function orderedJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(orderedJson).join(",")}]`;
  if (typeof value === "object" && value !== null) {
    return `{${Object.entries(value).filter(([, entry]) => entry !== undefined)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([key, entry]) => `${JSON.stringify(key)}:${orderedJson(entry)}`).join(",")}}`;
  }
  return JSON.stringify(value) ?? "null";
}

export function digest(value: unknown): string {
  return createHash("sha256").update(orderedJson(value)).digest("hex");
}

export function reference(kind: string, ...parts: string[]): string {
  return `${kind}:${digest(parts)}`;
}
