import { addDays, businessDate, compareTemporal, daysBetween, formatInstant, instantOf, isDateTime, isTemporal } from "../time.js";
import { Duration, type Truth, UNKNOWN, type Value, and3, not3, or3, roundHalfAway } from "../values.js";
import { FORBIDDEN_PROPERTIES } from "./analyze.js";
import { type Expr, pathOf } from "./parse.js";

/**
 * Evaluates a parsed formula against the case facts.
 *
 * Three values run through every operation:
 * - unknown (a fact not supplied) propagates through arithmetic, comparisons and calls; and/or follow
 *   Kleene logic, so "false and unknown" is false and "true or unknown" is true;
 * - null (known to be absent) is false where a truth value is needed, makes arithmetic absent, makes an
 *   ordering comparison false, counts as an empty list, and is skipped by min, max, earliest and latest;
 * - anything else is a known value: a number (money in integer cents), a string, an ISO date or
 *   date-time, a boolean, a list, or a fact object.
 * A type error (adding a date to a date, a method that throws) leaves the formula unknown and reports it.
 */

export class FormulaError extends Error {}

export interface FormulaScope {
  facts: Readonly<Record<string, unknown>>;
  parameters?: Readonly<Record<string, unknown>>;
  holds?: (treeId: string) => Promise<Truth>;
  amount?: (treeId: string, effectId: string) => Promise<Value>;
}

export interface FormulaRun {
  value: Value;
  /** Fact paths the formula needed that were not supplied. */
  missing: string[];
  /** Trees evaluated through holds() or amount(). */
  references: string[];
  error?: string;
}

export async function runFormula(expr: Expr, scope: FormulaScope): Promise<FormulaRun> {
  const run = new Run(scope);
  try {
    const value = await run.eval(expr);
    return { value, missing: [...run.missing], references: [...run.references] };
  } catch (err) {
    return { value: UNKNOWN, missing: [...run.missing], references: [...run.references], error: (err as Error).message };
  }
}

export function truthOf(v: Value): Truth {
  if (v === true || v === false) return v;
  if (v === null) return false;
  if (v === UNKNOWN) return "unknown";
  throw new FormulaError(`expected true or false, got ${describe(v)}`);
}

const fromTruth = (t: Truth): Value => (t === "unknown" ? UNKNOWN : t);

function describe(v: unknown): string {
  if (v === UNKNOWN) return "unknown";
  if (v === null) return "null";
  if (Array.isArray(v)) return "a list";
  if (v instanceof Duration) return `${v.hours} hours`;
  if (typeof v === "string") return JSON.stringify(v);
  if (typeof v === "object") return "an object";
  return String(v);
}

function isThenable(v: unknown): v is PromiseLike<unknown> {
  return typeof v === "object" && v !== null && typeof (v as { then?: unknown }).then === "function";
}

/** True if the value is unknown or a list holding an unknown anywhere. */
export function containsUnknown(v: Value): boolean {
  return v === UNKNOWN || (Array.isArray(v) && v.some((x) => x === undefined || containsUnknown(x)));
}

const element = (x: unknown): Value => (x === undefined ? UNKNOWN : (x as Value));

export function equal3(a: Value, b: Value): Truth {
  if (a === UNKNOWN || b === UNKNOWN) return "unknown";
  if (a === null || b === null) return a === b;
  if (isTemporal(a) && isTemporal(b)) return compareTemporal(a, b) === 0;
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return and3(a.map((x, i) => equal3(element(x), element(b[i]))));
  }
  if (a instanceof Duration && b instanceof Duration) return a.hours === b.hours;
  return a === b;
}

class Run {
  readonly missing = new Set<string>();
  readonly references = new Set<string>();
  constructor(private readonly scope: FormulaScope) {}

  private async read(v: unknown, path: string | undefined): Promise<Value> {
    if (isThenable(v)) v = await v;
    if (v === undefined) {
      if (path) this.missing.add(path);
      return UNKNOWN;
    }
    if (v instanceof Date) return formatInstant(v.getTime());
    return v as Value;
  }

  async eval(e: Expr): Promise<Value> {
    switch (e.kind) {
      case "number":
      case "string":
      case "boolean":
        return e.value;
      case "null":
        return null;
      case "name":
        if (e.name === "parameters") return this.scope.parameters ?? {};
        if (FORBIDDEN_PROPERTIES.has(e.name)) throw new FormulaError(`"${e.name}" cannot be read`);
        return this.read(this.scope.facts[e.name], e.name);
      case "member":
        return this.member(await this.eval(e.object), e.property, pathOf(e));
      case "call":
        return this.call(e);
      case "list": {
        const out: Value[] = [];
        for (const item of e.items) out.push(await this.eval(item));
        return out;
      }
      case "negate": {
        const v = await this.eval(e.arg);
        if (v === UNKNOWN || v === null) return v;
        if (typeof v === "number") return -v;
        if (v instanceof Duration) return new Duration(-v.hours);
        throw new FormulaError(`cannot negate ${describe(v)}`);
      }
      case "not":
        return fromTruth(not3(truthOf(await this.eval(e.arg))));
      case "logical":
        return this.logical(e.op, e.left, e.right);
      case "arith":
        return arith(e.op, await this.eval(e.left), await this.eval(e.right));
      case "compare":
        return fromTruth(compare(e.op, await this.eval(e.left), await this.eval(e.right)));
      case "conditional": {
        const t = truthOf(await this.eval(e.test));
        if (t === true) return this.eval(e.then);
        if (t === false) return this.eval(e.otherwise);
        const a = await this.eval(e.then);
        const b = await this.eval(e.otherwise);
        return equal3(a, b) === true ? a : UNKNOWN;
      }
    }
  }

  private async logical(op: "and" | "or", left: Expr, right: Expr): Promise<Value> {
    const decisive = op === "or";
    const l = truthOf(await this.eval(left));
    if (l === decisive) return l;
    const r = truthOf(await this.eval(right));
    return fromTruth(op === "and" ? and3([l, r]) : or3([l, r]));
  }

  private async member(obj: Value, prop: string, path: string | undefined): Promise<Value> {
    if (obj === UNKNOWN || obj === null) return obj;
    // A property of a list reads it from every element: statement.lines.repairAndCleaning.amount.
    if (Array.isArray(obj)) {
      const out: Value[] = [];
      for (const x of obj) out.push(await this.member(element(x), prop, path));
      return out;
    }
    if ((typeof obj !== "object" && typeof obj !== "function") || obj instanceof Duration) {
      throw new FormulaError(`cannot read "${prop}" of ${describe(obj)}`);
    }
    if (FORBIDDEN_PROPERTIES.has(prop)) throw new FormulaError(`"${prop}" cannot be read`);
    return this.read((obj as Record<string, unknown>)[prop], path);
  }

  private async call(e: Extract<Expr, { kind: "call" }>): Promise<Value> {
    if (e.callee.kind === "name") return this.builtin(e.callee.name, e.args);
    if (e.callee.kind !== "member") throw new FormulaError("only a function or a fact method can be called");
    const receiver = await this.eval(e.callee.object);
    if (receiver === UNKNOWN || receiver === null) return receiver;
    if (Array.isArray(receiver) || typeof receiver !== "object" || receiver instanceof Duration) {
      throw new FormulaError(`cannot call "${e.callee.property}" on ${describe(receiver)}`);
    }
    const path = pathOf(e.callee);
    if (FORBIDDEN_PROPERTIES.has(e.callee.property)) throw new FormulaError(`"${e.callee.property}" cannot be called`);
    const fn = (receiver as Record<string, unknown>)[e.callee.property];
    if (fn === undefined) {
      if (path) this.missing.add(path);
      return UNKNOWN;
    }
    if (typeof fn !== "function") throw new FormulaError(`${path ?? e.callee.property} is not a method`);
    const args: Value[] = [];
    for (const a of e.args) args.push(await this.eval(a));
    // A method is never asked about an unknown: its answer would be unknown too.
    if (args.some(containsUnknown)) return UNKNOWN;
    return this.read(await (fn as (...a: unknown[]) => unknown).apply(receiver, args), path && `${path}(…)`);
  }

  private async builtin(name: string, argExprs: Expr[]): Promise<Value> {
    if (name === "holds" || name === "amount") {
      const ids = argExprs.map((a) => (a.kind === "string" ? a.value : undefined));
      if (ids.some((x) => x === undefined)) throw new FormulaError(`${name}() takes string literals`);
      const [tree, effect] = ids as string[];
      this.references.add(tree!);
      if (name === "holds") {
        if (!this.scope.holds) throw new FormulaError("holds() needs the jurisdiction's trees");
        return fromTruth(await this.scope.holds(tree!));
      }
      if (!this.scope.amount) throw new FormulaError("amount() needs the jurisdiction's trees");
      return this.scope.amount(tree!, effect!);
    }
    const args: Value[] = [];
    for (const a of argExprs) args.push(await this.eval(a));
    const one = args[0] as Value;
    switch (name) {
      case "exists":
        return one === UNKNOWN ? UNKNOWN : one !== null;
      case "count":
      case "len":
        if (one === UNKNOWN || one === null) return one === null ? 0 : UNKNOWN;
        if (Array.isArray(one)) return one.length;
        throw new FormulaError(`${name}() needs a list, got ${describe(one)}`);
      case "days": {
        const [a, b] = args as [Value, Value];
        if (a === null || b === null) return null;
        if (a === UNKNOWN || b === UNKNOWN) return UNKNOWN;
        if (!isTemporal(a) || !isTemporal(b)) throw new FormulaError(`days() needs two dates, got ${describe(a)} and ${describe(b)}`);
        return daysBetween(businessDate(a), businessDate(b));
      }
      case "round":
      case "abs":
        if (one === UNKNOWN || one === null) return one;
        if (typeof one !== "number") throw new FormulaError(`${name}() needs a number, got ${describe(one)}`);
        return name === "round" ? roundHalfAway(one) : Math.abs(one);
      case "hours":
        if (one === UNKNOWN || one === null) return one;
        if (typeof one !== "number") throw new FormulaError(`hours() needs a number, got ${describe(one)}`);
        return new Duration(one);
      case "date":
        if (one === UNKNOWN || one === null) return one;
        if (!isTemporal(one)) throw new FormulaError(`date() needs a date or date-time, got ${describe(one)}`);
        return businessDate(one);
      case "any":
      case "all": {
        if (one === UNKNOWN || one === null) return one === null ? name === "all" : UNKNOWN;
        if (!Array.isArray(one)) throw new FormulaError(`${name}() needs a list, got ${describe(one)}`);
        const truths = one.map((x) => truthOf(element(x)));
        return fromTruth(name === "any" ? or3(truths) : and3(truths));
      }
      case "sum": {
        const items = listArgs(args);
        if (items === UNKNOWN) return UNKNOWN;
        let total = 0;
        for (const x of items) {
          if (x === UNKNOWN) return UNKNOWN;
          if (x === null) continue;
          if (typeof x !== "number") throw new FormulaError(`sum() needs numbers, got ${describe(x)}`);
          total += x;
        }
        return total;
      }
      case "min":
      case "max":
      case "earliest":
      case "latest": {
        const items = listArgs(args);
        if (items === UNKNOWN) return UNKNOWN;
        const temporal = name === "earliest" || name === "latest";
        const lowest = name === "min" || name === "earliest";
        let best: Value | undefined;
        for (const x of items) {
          if (x === UNKNOWN) return UNKNOWN;
          if (x === null) continue;
          if (temporal ? !isTemporal(x) : typeof x !== "number") {
            throw new FormulaError(`${name}() needs ${temporal ? "dates" : "numbers"}, got ${describe(x)}`);
          }
          const cmp = best === undefined ? 0 : temporal ? compareTemporal(x as string, best as string) : Math.sign((x as number) - (best as number));
          if (best === undefined || (lowest ? cmp < 0 : cmp > 0)) best = x;
        }
        return best === undefined ? null : best;
      }
    }
    throw new FormulaError(`unknown function ${name}()`);
  }
}

/** The values a list function works over: one list argument, or the arguments themselves. */
function listArgs(args: Value[]): Value[] | typeof UNKNOWN {
  if (args.length === 1) {
    const [only] = args as [Value];
    if (only === UNKNOWN) return UNKNOWN;
    if (only === null) return [];
    if (Array.isArray(only)) return only.map(element);
  }
  return args;
}

function arith(op: string, a: Value, b: Value): Value {
  if (a === null || b === null) return null;
  if (a === UNKNOWN || b === UNKNOWN) return UNKNOWN;
  if (typeof a === "number" && typeof b === "number") {
    switch (op) {
      case "+":
        return a + b;
      case "-":
        return a - b;
      case "*":
        return a * b;
      case "/":
        if (b === 0) throw new FormulaError("division by zero");
        return a / b;
    }
  }
  const days = (n: number) => {
    if (!Number.isInteger(n)) throw new FormulaError(`a date moves by whole days, not ${n}`);
    return n;
  };
  if (op === "+" || op === "-") {
    const sign = op === "+" ? 1 : -1;
    // A date-time moved by whole days lands on a California calendar date.
    if (isTemporal(a) && typeof b === "number") return addDays(businessDate(a), sign * days(b));
    if (op === "+" && typeof a === "number" && isTemporal(b)) return addDays(businessDate(b), days(a));
    if (isDateTime(a) && b instanceof Duration) return formatInstant(instantOf(a) + sign * b.hours * 3_600_000);
    if (op === "+" && a instanceof Duration && isDateTime(b)) return formatInstant(instantOf(b) + a.hours * 3_600_000);
    if (a instanceof Duration && b instanceof Duration) return new Duration(a.hours + sign * b.hours);
    if (op === "-" && isTemporal(a) && isTemporal(b)) return daysBetween(businessDate(b), businessDate(a));
  }
  throw new FormulaError(`cannot compute ${describe(a)} ${op} ${describe(b)}`);
}

function compare(op: string, a: Value, b: Value): Truth {
  if (op === "==" || op === "!=") {
    const eq = equal3(a, b);
    return op === "==" ? eq : not3(eq);
  }
  if (op === "in" || op === "not in") {
    const m = membership(a, b);
    return op === "in" ? m : not3(m);
  }
  // An absent value is neither before nor after anything.
  if (a === null || b === null) return false;
  if (a === UNKNOWN || b === UNKNOWN) return "unknown";
  let c: number;
  if (typeof a === "number" && typeof b === "number") c = Math.sign(a - b);
  else if (isTemporal(a) && isTemporal(b)) c = compareTemporal(a, b);
  else if (a instanceof Duration && b instanceof Duration) c = Math.sign(a.hours - b.hours);
  else throw new FormulaError(`cannot order ${describe(a)} and ${describe(b)}`);
  switch (op) {
    case "<":
      return c < 0;
    case "<=":
      return c <= 0;
    case ">":
      return c > 0;
    default:
      return c >= 0;
  }
}

/** x in list; a list on the left asks whether every element is in the right-hand list. */
function membership(a: Value, b: Value): Truth {
  if (b === null) return false;
  if (b === UNKNOWN) return "unknown";
  if (!Array.isArray(b)) throw new FormulaError(`"in" needs a list on the right, got ${describe(b)}`);
  const list = b.map(element);
  if (a === UNKNOWN) return list.length === 0 ? false : "unknown";
  const one = (x: Value) => or3(list.map((y) => equal3(x, y)));
  return Array.isArray(a) ? and3(a.map((x) => one(element(x)))) : one(a);
}
