/**
 * Values in the three-valued world of the trees.
 *
 * - A fact that was not supplied (undefined) is unknown. Unknown is never false.
 * - null means known to be absent: there is no such record.
 */

export type Truth = true | false | "unknown";

/** The internal marker for an unknown value inside formula evaluation. */
export const UNKNOWN: unique symbol = Symbol("unknown");
export type Unknown = typeof UNKNOWN;

/** A span of hours, from hours(n). Added to or taken from a date-time. */
export class Duration {
  constructor(readonly hours: number) {}
  toJSON() {
    return { hours: this.hours };
  }
}

export type Value = Unknown | null | boolean | number | string | Duration | readonly Value[] | object;

export function isUnknown(v: unknown): v is Unknown {
  return v === UNKNOWN;
}

export const not3 = (v: Truth): Truth => (v === "unknown" ? v : !v);

/** Kleene conjunction: false if any is false, true if all are true, otherwise unknown. */
export function and3(values: Iterable<Truth>): Truth {
  let all = true;
  for (const v of values) {
    if (v === false) return false;
    if (v !== true) all = false;
  }
  return all ? true : "unknown";
}

/** Kleene disjunction: true if any is true, false if all are false, otherwise unknown. */
export function or3(values: Iterable<Truth>): Truth {
  let none = true;
  for (const v of values) {
    if (v === true) return true;
    if (v !== false) none = false;
  }
  return none ? false : "unknown";
}

/** Rule and not exception: false when the exception holds, whatever the rule. */
export const unless3 = (rule: Truth, exception: Truth): Truth => and3([rule, not3(exception)]);

/** Rounds half away from zero, tolerating binary floating-point noise. */
export function roundHalfAway(x: number): number {
  const snapped = Math.abs(x - Math.round(x)) < 1e-9 ? Math.round(x) : x;
  return Math.sign(snapped) * Math.floor(Math.abs(snapped) + 0.5 + 1e-9);
}
