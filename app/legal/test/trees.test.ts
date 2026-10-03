import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { TreeValidationError, analyzeFormula, buildJurisdiction, formulasOf, inForce, parseFormula, requiredFacts } from "../src/index.js";
import { TREES_DIR, california, fact, jurisdictionOf, makeTree, semantic } from "./helpers.js";

const treeFiles = readdirSync(TREES_DIR).filter((n) => n.endsWith(".json") && n !== "JEV_CHECK.json");

describe("the California account-core trees", () => {
  it("all 34 load, validate and cross-check", async () => {
    const j = await california();
    expect(treeFiles).toHaveLength(34);
    expect(j.ids()).toHaveLength(34);
    expect(j.ids()).toContain("CA.deduct-repair");
    for (const id of j.ids()) expect(j.versions(id)).toHaveLength(1);
  });

  it("every formula parses: the inventory is 119 distinct formulas across compute, amount, due, margin and notBefore", async () => {
    const j = await california();
    const all = j.trees.flatMap(formulasOf);
    const distinct = new Set(all.map((f) => f.source));
    expect(distinct.size).toBe(119);
    for (const f of all) expect(() => parseFormula(f.source), f.where).not.toThrow();
    for (const f of all) expect(analyzeFormula(parseFormula(f.source)).problems, f.where).toEqual([]);
    // The functions the trees use are all built in.
    const used = new Set([...distinct].flatMap((s) => [...s.matchAll(/\b([a-z]+)\(/g)].map((m) => m[1])));
    for (const fn of ["days", "count", "exists", "sum", "min", "max", "round", "holds", "amount", "earliest", "latest", "hours"]) {
      expect(used.has(fn), fn).toBe(true);
    }
  });

  it("reads the inventory straight from the JSON files, so no formula escapes the loader", () => {
    const raw: string[] = [];
    const visit = (n: Record<string, unknown>) => {
      if (typeof n.compute === "string") raw.push(n.compute);
      for (const k of ["children"]) for (const c of (n[k] as Record<string, unknown>[] | undefined) ?? []) visit(c);
      for (const k of ["child", "rule", "exception"]) if (n[k]) visit(n[k] as Record<string, unknown>);
    };
    for (const name of treeFiles) {
      const t = JSON.parse(readFileSync(join(TREES_DIR, name), "utf8"));
      visit(t.root);
      for (const e of t.effects) for (const k of ["amount", "due", "margin", "notBefore"]) if (e[k]) raw.push(e[k]);
    }
    expect(new Set(raw).size).toBe(119);
    for (const s of raw) expect(() => parseFormula(s), s).not.toThrow();
  });

  it("selects the version in force on the event date", async () => {
    const j = await california();
    expect(j.select("CA.statement-due", "2026-11-16")?.id).toBe("CA.statement-due");
    expect(j.select("CA.statement-due", "2025-12-31")).toBeUndefined();
    expect(() => j.tree("CA.statement-due", "2025-12-31")).toThrow(/no version of CA.statement-due is in force on 2025-12-31/);
  });

  it("lists the facts a tree reads", async () => {
    const j = await california();
    const r = requiredFacts(j.tree("CA.holdover-charge", "2026-11-16"));
    expect(r.formulas).toEqual(["landlord.holdoverPermission.given", "lease.holdoverClause.fixesRate", "moveOut.vacateDate", "schedule.holdoverDailyRate", "tenancy.endDate", "udAction.filed"]);
    expect(r.questions.map((q) => q.leaf)).toEqual(["rate-within-rental-value", "mistake-of-fact", "rate-within-benefit", "actual-damage-impracticable"]);
  });
});

describe("tree versions", () => {
  const v1 = makeTree("CA.versioned", fact("a"), { effective: { from: "2026-01-01", to: "2026-12-31" } });
  const v2 = makeTree("CA.versioned", fact("b"), { effective: { from: "2027-01-01", to: null } });

  it("a null end is open-ended and the end date is the last day in force", () => {
    expect(inForce(v1, "2026-12-31")).toBe(true);
    expect(inForce(v1, "2027-01-01")).toBe(false);
    expect(inForce(v2, "2099-06-01")).toBe(true);
    const j = jurisdictionOf(v1, v2);
    expect(j.select("CA.versioned", "2026-06-01")?.root).toMatchObject({ id: "a" });
    expect(j.select("CA.versioned", "2027-06-01")?.root).toMatchObject({ id: "b" });
  });

  it("refuses overlapping versions", () => {
    const v3 = makeTree("CA.versioned", fact("c"), { effective: { from: "2026-06-01", to: null } });
    expect(() => jurisdictionOf(v1, v3)).toThrow(/overlap/);
  });
});

describe("the loader refuses a malformed jurisdiction, listing every problem", () => {
  const problemsOf = (fn: () => unknown): string[] => {
    try {
      fn();
    } catch (err) {
      if (err instanceof TreeValidationError) return err.problems;
      throw err;
    }
    throw new Error("expected a validation error");
  };

  it("checks structure against the format", () => {
    const bad = { ...makeTree("CA.bad", fact("a")), extra: 1 };
    const noCompute = makeTree("CA.no-compute", { type: "all", children: [{ ...fact("a"), compute: undefined } as never, fact("b")] });
    const lonely = makeTree("CA.lonely", { type: "all", children: [fact("a")] });
    const problems = problemsOf(() =>
      buildJurisdiction([
        { name: "bad.json", json: bad },
        { name: "no-compute.json", json: JSON.parse(JSON.stringify(noCompute)) },
        { name: "lonely.json", json: lonely },
      ]),
    );
    expect(problems.some((p) => p.startsWith("bad.json") && /extra/.test(p))).toBe(true);
    expect(problems.some((p) => p.startsWith("no-compute.json") && /needs compute/.test(p))).toBe(true);
    expect(problems.some((p) => p.startsWith("lonely.json") && /children/.test(p))).toBe(true);
  });

  it("resolves cross-references and contested points", () => {
    const t = makeTree(
      "CA.refs",
      {
        type: "all",
        children: [
          fact("a", 'holds("CA.missing")'),
          fact("b", 'amount("CA.target", "nope") > 0'),
          fact("c", "parameters.absent > 0"),
          fact("d", "undeclared.path"),
          semantic("e", ["not.an.input"]),
          { ...fact("x"), contested: "C9" } as never,
        ],
      },
      {
        effects: [{ id: "eff", kind: "duty", when: "holds", statement: "Do it.", consequence: "CA.nowhere" }],
        contested: [
          {
            issue: "C1",
            question: "Which?",
            exposureBranch: "Z",
            branches: [
              { id: "A", reading: "One.", authority: [{ citation: "Civ 1", quote: "quote quote" }], effect: { statement: "One.", sets: { "no-such-leaf": true } } },
              { id: "B", reading: "Two.", authority: [{ citation: "Civ 1", quote: "quote quote" }], effect: { statement: "Two." } },
            ],
          },
        ],
      },
    );
    const target = makeTree("CA.target", fact("a"), { effects: [{ id: "pay", kind: "permission", when: "holds", statement: "Pay.", amount: "f.amount" }] });
    const problems = problemsOf(() => jurisdictionOf(t, target));
    const expected = [
      /holds\("CA.missing"\) names no tree/,
      /amount\("CA.target", "nope"\) names no effect/,
      /unknown parameter absent/,
      /undeclared.path is not a declared input/,
      /question input not.an.input is not a declared input/,
      /contested C9 is not defined/,
      /consequence CA.nowhere, which names no tree/,
      /sets no-such-leaf, which is not a leaf/,
      /exposure branch Z is not one of its branches/,
    ];
    for (const re of expected) expect(problems.some((p) => re.test(p)), String(re)).toBe(true);
  });

  it("reports a formula that does not parse, with its place", () => {
    const t = makeTree("CA.syntax", fact("a", "f.a and (f.b"));
    expect(problemsOf(() => jurisdictionOf(t)).join("\n")).toMatch(/CA.syntax:a.compute: expected "\)"/);
  });
});
