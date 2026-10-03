import { describe, expect, it } from "vitest";
import { Duration, FormulaSyntaxError, UNKNOWN, parseFormula, runFormula } from "../src/index.js";

const run = (src: string, facts: Record<string, unknown> = {}, parameters: Record<string, unknown> = {}) =>
  runFormula(parseFormula(src), { facts, parameters });
const value = async (src: string, facts: Record<string, unknown> = {}, parameters: Record<string, unknown> = {}) => {
  const r = await run(src, facts, parameters);
  if (r.error) throw new Error(r.error);
  return r.value;
};

describe("parsing", () => {
  it("follows the usual precedence: arithmetic, then comparison, then not, and, or", () => {
    expect(parseFormula("a + b * c > d and not e or f")).toMatchObject({
      kind: "logical",
      op: "or",
      left: {
        kind: "logical",
        op: "and",
        left: { kind: "compare", op: ">", left: { kind: "arith", op: "+", right: { kind: "arith", op: "*" } } },
        right: { kind: "not" },
      },
      right: { kind: "name", name: "f" },
    });
  });

  it("parses paths, method calls with list and nested arguments, and `not in`", () => {
    expect(parseFormula('ledger.payments.anyElectronic(["security", "rent"])')).toMatchObject({
      kind: "call",
      callee: { kind: "member", property: "anyElectronic", object: { kind: "member", property: "payments" } },
      args: [{ kind: "list", items: [{ value: "security" }, { value: "rent" }] }],
    });
    expect(parseFormula("x not in [1, 2]")).toMatchObject({ kind: "compare", op: "not in" });
    expect(parseFormula("not x in y")).toMatchObject({ kind: "not", arg: { kind: "compare", op: "in" } });
  });

  it("rejects what it cannot read, with a position", () => {
    for (const bad of ["a +", "a < b < c", "(a", "a b", "1x", '"open', "a.(b)", "f(x)(y)", "and", "a ! b"]) {
      expect(() => parseFormula(bad), bad).toThrow(FormulaSyntaxError);
    }
    expect(() => parseFormula("a ! b")).toThrow(/unexpected character "!" at 2/);
  });

  it("is a parser, not eval: code in a formula is just an unknown name", async () => {
    const r = await run("process.exit(1)");
    expect(r.value).toBe(UNKNOWN);
    expect(r.missing).toEqual(["process"]);
    await expect(value("f.constructor", { f: {} })).rejects.toThrow(/cannot be read/);
    await expect(value("constructor")).rejects.toThrow(/cannot be read/);
    await expect(value("f.__proto__", { f: {} })).rejects.toThrow(/cannot be read/);
  });
});

describe("unknown and null", () => {
  it("an unsupplied fact is unknown, and unknown propagates through arithmetic and comparison", async () => {
    const r = await run("f.a + 1 > 2", { f: {} });
    expect(r.value).toBe(UNKNOWN);
    expect(r.missing).toEqual(["f.a"]);
    expect(await value("-f.a", { f: {} })).toBe(UNKNOWN);
    expect(await value("f.a == 1", { f: {} })).toBe(UNKNOWN);
  });

  it("and/or follow Kleene logic: unknown is never false", async () => {
    const f = { t: true, F: false };
    expect(await value("u and f.F", { f })).toBe(false);
    expect(await value("u and f.t", { f })).toBe(UNKNOWN);
    expect(await value("u or f.t", { f })).toBe(true);
    expect(await value("u or f.F", { f })).toBe(UNKNOWN);
    expect(await value("not u", { f })).toBe(UNKNOWN);
    expect(await value("f.F and u", { f })).toBe(false);
    expect(await value("f.t or u", { f })).toBe(true);
  });

  it("null is known absence: exists(null) is false, exists(unknown) is unknown", async () => {
    expect(await value("exists(f.a)", { f: { a: null } })).toBe(false);
    expect(await value("exists(f.a)", { f: {} })).toBe(UNKNOWN);
    expect(await value("exists(f.a)", { f: { a: "2026-11-02" } })).toBe(true);
    // A path through an absent record is absent too.
    expect(await value("exists(notices.offer.sentAt)", { notices: { offer: null } })).toBe(false);
  });

  it("null reads false where a truth value is needed, and an absent value is neither before nor after anything", async () => {
    expect(await value("not f.permission.given", { f: { permission: null } })).toBe(true);
    expect(await value("f.a > 0", { f: { a: null } })).toBe(false);
    expect(await value("f.a <= 0", { f: { a: null } })).toBe(false);
    expect(await value("f.a == null", { f: { a: null } })).toBe(true);
    expect(await value("f.a == null", { f: {} })).toBe(UNKNOWN);
    expect(await value("f.a + 1", { f: { a: null } })).toBe(null);
    expect(await value("count(f.a)", { f: { a: null } })).toBe(0);
    expect(await value("count(f.a)", { f: {} })).toBe(UNKNOWN);
  });

  it("a method is not called with an unknown argument, and an unsupplied method is unknown", async () => {
    let calls = 0;
    const ledger = { due: (d: string) => (calls++, d === "2026-11-10" ? 100 : 0) };
    expect(await value("ledger.due(f.d)", { ledger, f: {} })).toBe(UNKNOWN);
    expect(calls).toBe(0);
    expect(await value("ledger.due(f.d)", { ledger, f: { d: "2026-11-10" } })).toBe(100);
    const r = await run("ledger.other(1)", { ledger });
    expect(r.value).toBe(UNKNOWN);
    expect(r.missing).toEqual(["ledger.other"]);
    expect(await value("ledger.due(1)", { ledger: null })).toBe(null);
  });

  it("awaits asynchronous facts and methods", async () => {
    const ledger = { due: async () => 250, get late() { return Promise.resolve(true); } };
    expect(await value("ledger.due() + 1", { ledger })).toBe(251);
    expect(await value("ledger.late", { ledger })).toBe(true);
  });

  it("a type error leaves the formula unknown and says why", async () => {
    const r = await run('f.a + "x"', { f: { a: 1 } });
    expect(r.value).toBe(UNKNOWN);
    expect(r.error).toMatch(/cannot compute 1 \+ "x"/);
    expect((await run("f.a and true", { f: { a: 3 } })).error).toMatch(/expected true or false, got 3/);
    expect((await run("f.boom()", { f: { boom: () => { throw new Error("ledger offline"); } } })).error).toMatch(/ledger offline/);
  });
});

describe("functions", () => {
  it("sum, count, min, max, round, abs", async () => {
    expect(await value("sum([1, 2, 3])")).toBe(6);
    expect(await value("sum(1, 2, null)")).toBe(3);
    expect(await value("sum([1, u])")).toBe(UNKNOWN);
    expect(await value("min(5, 3, 9)")).toBe(3);
    expect(await value("max([5, 3, 9])")).toBe(9);
    expect(await value("min(f.cap, 7)", { f: { cap: null } })).toBe(7);
    expect(await value("min(f.cap, 7)", { f: {} })).toBe(UNKNOWN);
    expect(await value("max(0, f.a - f.b)", { f: { a: null, b: 1 } })).toBe(0);
    expect(await value("round(2.5)")).toBe(3);
    expect(await value("round(-2.5)")).toBe(-3);
    expect(await value("round(2.4999)")).toBe(2);
    expect(await value("abs(-4)")).toBe(4);
    expect(await value("len([1, 2])")).toBe(2);
  });

  it("any and all over a list, and a conditional", async () => {
    expect(await value("any([false, u, true])")).toBe(true);
    expect(await value("all([true, u])")).toBe(UNKNOWN);
    expect(await value("1 if f.x else 2", { f: { x: false } })).toBe(2);
    expect(await value("1 if u else 1")).toBe(1);
    expect(await value("1 if u else 2")).toBe(UNKNOWN);
  });

  it("a property of a list reads it from every element", async () => {
    const statement = { lines: { repairAndCleaning: [{ amount: 7_000 }, { amount: 5_000 }] } };
    expect(await value("sum(statement.lines.repairAndCleaning.amount) <= 12500", { statement })).toBe(true);
    const r = await run("sum(s.lines.amount)", { s: { lines: [{ amount: 1 }, {}] } });
    expect(r.value).toBe(UNKNOWN);
    expect(r.missing).toEqual(["s.lines.amount"]);
  });

  it("`in` tests membership, and a list on the left must be wholly inside the right", async () => {
    expect(await value('f.g in ["CCP 1161(2)", "CCP 1161(3)"]', { f: { g: "CCP 1161(3)" } })).toBe(true);
    expect(await value('f.g in ["CCP 1161(2)"]', { f: { g: null } })).toBe(false);
    expect(await value('f.g in ["a"]', { f: {} })).toBe(UNKNOWN);
    expect(await value('f.types in ["usage", "adminFee"]', { f: { types: ["usage", "adminFee"] } })).toBe(true);
    expect(await value('f.types in ["usage", "adminFee"]', { f: { types: ["usage", "penalty"] } })).toBe(false);
    expect(await value("f.id in f.list", { f: { id: "b", list: ["a", "b"] } })).toBe(true);
    expect(await value("f.id in f.list", { f: { id: "b", list: null } })).toBe(false);
    expect(await value("f.id not in f.list", { f: { id: "c", list: ["a"] } })).toBe(true);
  });

  it("holds() and amount() need the jurisdiction", async () => {
    expect((await run('holds("CA.x")')).error).toMatch(/needs the jurisdiction/);
    const r = await runFormula(parseFormula('holds("CA.x") and amount("CA.y", "e") > 5'), {
      facts: {},
      holds: async () => true,
      amount: async () => 10,
    });
    expect(r.value).toBe(true);
    expect(r.references).toEqual(["CA.x", "CA.y"]);
  });
});

describe("money and dates", () => {
  it("amounts are integer cents; the holdover's six November days are $547.00", async () => {
    const schedule = { holdoverDailyRate: 273_500 / 30 };
    const v = await value("days(tenancy.endDate, moveOut.vacateDate) * schedule.holdoverDailyRate", {
      tenancy: { endDate: "2026-11-10" },
      moveOut: { vacateDate: "2026-11-16" },
      schedule,
    });
    expect(Math.round(v as number)).toBe(54_700);
    expect(await value("round(f.cost * f.share)", { f: { cost: 42_000, share: 0.5 } })).toBe(21_000);
  });

  it("days(a, b) counts calendar days from a to b, and a date moves by whole days", async () => {
    expect(await value('days("2026-11-10", "2026-11-16")')).toBe(6);
    expect(await value('days("2026-12-07", "2026-11-16")')).toBe(-21);
    expect(await value('days("2026-02-27", "2026-03-01")')).toBe(2);
    expect(await value("moveOut.vacateDate + parameters.statementDays", { moveOut: { vacateDate: "2026-11-16" } }, { statementDays: 21 })).toBe("2026-12-07");
    expect(await value('"2026-11-10" - 14')).toBe("2026-10-27");
    expect(await value('21 + "2026-11-16"')).toBe("2026-12-07");
    expect(await value('"2026-12-07" - "2026-11-16"')).toBe(21);
    expect((await run('"2026-11-16" + 1.5')).error).toMatch(/whole days/);
    expect((await run('"2026-11-16" + "2026-11-17"')).error).toMatch(/cannot compute/);
  });

  it("compares dates, and a date against a date-time on the California calendar", async () => {
    expect(await value('"2026-11-16" > "2026-11-10"')).toBe(true);
    expect(await value('"2026-11-16T23:30" == "2026-11-16"')).toBe(true);
    // 23:30 in California is already the 17th in UTC; the business date is still the 16th.
    expect(await value('date("2026-11-17T07:30:00Z")')).toBe("2026-11-16");
    expect(await value('earliest("2026-10-12", "2026-09-11", null)')).toBe("2026-09-11");
    expect(await value('latest("2026-10-12", "2026-09-11")')).toBe("2026-10-12");
  });

  it("subtracts hours across the end of daylight time (November 1, 2026)", async () => {
    // 10:00 PST on November 2 less 48 real hours is 11:00 PDT on October 31.
    expect(await value('"2026-11-02T10:00" - hours(48)')).toBe("2026-10-31T11:00:00-07:00");
    expect(await value('"2026-11-02T18:00:00Z" - hours(48)')).toBe("2026-10-31T11:00:00-07:00");
    expect(await value('"2026-11-02T10:00" + hours(1)')).toBe("2026-11-02T11:00:00-08:00");
    expect(await value("hours(2)")).toEqual(new Duration(2));
  });

  it("refuses dates that do not exist", async () => {
    expect((await run('days("2026-02-30", "2026-03-01")')).error).toMatch(/needs two dates/);
  });
});
