import { describe, expect, it } from "vitest";
import { type Node, type Truth, evaluate } from "../src/index.js";
import { fixtureAnswers } from "../src/demo/index.js";
import { discretionary, fact, jurisdictionOf, makeTree, semantic } from "./helpers.js";

const VALUES: Truth[] = [true, false, "unknown"];
/** Facts giving leaf `a` and `b` the values asked for; unknown is an unsupplied fact. */
const factsFor = (a: Truth, b: Truth) => ({ f: { ...(a === "unknown" ? {} : { a }), ...(b === "unknown" ? {} : { b }) } });

async function rootOf(root: Node, a: Truth, b: Truth): Promise<Truth> {
  const j = jurisdictionOf(makeTree("CA.logic", root));
  return (await evaluate("CA.logic", factsFor(a, b), { jurisdiction: j, eventDate: "2026-11-16" })).root;
}

describe("Kleene logic of the nodes", () => {
  const and = (x: Truth, y: Truth): Truth => (x === false || y === false ? false : x === true && y === true ? true : "unknown");
  const or = (x: Truth, y: Truth): Truth => (x === true || y === true ? true : x === false && y === false ? false : "unknown");
  const neg = (x: Truth): Truth => (x === "unknown" ? x : !x);

  for (const a of VALUES) {
    for (const b of VALUES) {
      it(`all/any/unless with a=${a}, b=${b}`, async () => {
        expect(await rootOf({ type: "all", children: [fact("a"), fact("b")] }, a, b)).toBe(and(a, b));
        expect(await rootOf({ type: "any", children: [fact("a"), fact("b")] }, a, b)).toBe(or(a, b));
        // unless: true when the rule holds and the exception does not; false whenever the exception holds.
        expect(await rootOf({ type: "unless", rule: fact("a"), exception: fact("b") }, a, b)).toBe(and(a, neg(b)));
      });
    }
    it(`not with a=${a}`, async () => {
      expect(await rootOf({ type: "not", child: fact("a") }, a, "unknown")).toBe(neg(a));
    });
  }

  it("unless is false when the exception holds even though the rule is unknown, and unknown when the exception is", async () => {
    const node: Node = { type: "unless", rule: fact("a"), exception: fact("b") };
    expect(await rootOf(node, "unknown", true)).toBe(false);
    expect(await rootOf(node, true, "unknown")).toBe("unknown");
  });

  it("a fact that is null reads false, not unknown", async () => {
    const j = jurisdictionOf(makeTree("CA.null", fact("a")));
    expect((await evaluate("CA.null", { f: { a: null } }, { jurisdiction: j, eventDate: "2026-11-16" })).root).toBe(false);
    expect((await evaluate("CA.null", { f: {} }, { jurisdiction: j, eventDate: "2026-11-16" })).root).toBe("unknown");
  });
});

describe("semantic leaves and the evidence contract", () => {
  const tree = makeTree("CA.sem", { type: "all", children: [fact("a"), semantic("damage", ["e.moveIn", "e.moveOut"])] }, { inputs: ["f", "e.moveIn", "e.moveOut"] });
  const j = jurisdictionOf(tree);
  const opts = (answers = fixtureAnswers({ damage: true })) => ({ jurisdiction: j, eventDate: "2026-11-16", answers });

  it("asks the provider with exactly the contract's inputs", async () => {
    const answers = fixtureAnswers({ damage: true });
    const r = await evaluate("CA.sem", { f: { a: true }, e: { moveIn: "clean", moveOut: "hole in door", other: "x" } }, opts(answers));
    expect(r.root).toBe(true);
    expect(answers.asked).toEqual([{ treeId: "CA.sem", leafId: "damage", inputs: { "e.moveIn": "clean", "e.moveOut": "hole in door" } }]);
    expect(r.leaves.damage!.basis).toMatchObject({ by: "answer", answer: { value: true, provider: "fixture" } });
  });

  it("does not call the provider while an input is missing; the leaf is unknown and goes on the investigation list", async () => {
    const answers = fixtureAnswers({ damage: true });
    const r = await evaluate("CA.sem", { f: { a: true }, e: { moveOut: "hole in door" } }, opts(answers));
    expect(answers.asked).toEqual([]);
    expect(r.root).toBe("unknown");
    expect(r.leaves.damage).toMatchObject({ value: "unknown", basis: { by: "evidence-missing", missing: ["e.moveIn"] } });
    expect(r.investigation).toEqual([
      expect.objectContaining({ leafId: "damage", ifTrue: true, ifFalse: false, decisive: true, settle: expect.objectContaining({ by: "question", missing: ["e.moveIn"] }) }),
    ]);
  });

  it("treats a null input as supplied evidence of absence", async () => {
    const answers = fixtureAnswers({ damage: false });
    const r = await evaluate("CA.sem", { f: { a: true }, e: { moveIn: null, moveOut: "hole" } }, opts(answers));
    expect(answers.asked).toHaveLength(1);
    expect(r.root).toBe(false);
  });

  it("does not ask a question whose answer cannot change the result", async () => {
    const answers = fixtureAnswers({ damage: true });
    const r = await evaluate("CA.sem", { f: { a: false }, e: { moveIn: "clean", moveOut: "hole" } }, opts(answers));
    expect(r.root).toBe(false);
    expect(answers.asked).toEqual([]);
    expect(r.leaves.damage!.basis).toEqual({ by: "not-needed" });
  });

  it("keeps an unknown answer unknown, and a failing provider is reported, not fatal", async () => {
    const r1 = await evaluate("CA.sem", { f: { a: true }, e: { moveIn: "x", moveOut: "y" } }, opts(fixtureAnswers({})));
    expect(r1.root).toBe("unknown");
    const r2 = await evaluate("CA.sem", { f: { a: true }, e: { moveIn: "x", moveOut: "y" } }, {
      ...opts(),
      answers: async () => {
        throw new Error("provider timeout");
      },
    });
    expect(r2.root).toBe("unknown");
    expect(r2.diagnostics).toEqual([{ treeId: "CA.sem", where: "damage", message: "the answer provider failed: provider timeout" }]);
  });

  it("without a provider a semantic leaf stays unknown", async () => {
    const r = await evaluate("CA.sem", { f: { a: true }, e: { moveIn: "x", moveOut: "y" } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(r.leaves.damage!.basis.by).toBe("no-provider");
    expect(r.root).toBe("unknown");
  });
});

describe("discretionary leaves and contested points", () => {
  const tree = makeTree(
    "CA.contest",
    { type: "all", children: [fact("owed"), { type: "any", children: [fact("is-rent"), discretionary("any-purpose", "C6")] }] },
    {
      effects: [
        { id: "may-deduct", kind: "permission", when: "holds", statement: "Deduct it.", amount: "f.amount" },
        { id: "bill-separately", kind: "prohibition", when: "fails", statement: "Bill it separately." },
      ],
      contested: [
        {
          issue: "C6",
          question: "Does the deposit reach any lease debt?",
          exposureBranch: "B",
          branches: [
            { id: "A", reading: "Any purpose.", authority: [{ citation: "Civ 1950.5(b)", quote: "any purpose" }], effect: { statement: "Deduct.", sets: { "any-purpose": true } } },
            { id: "B", reading: "Four purposes.", authority: [{ citation: "Civ 1950.5(b)", quote: "four purposes" }], effect: { statement: "Bill.", sets: { "any-purpose": false } } },
          ],
        },
      ],
    },
  );
  const j = jurisdictionOf(tree);
  const facts = { f: { owed: true, is_rent: false, amount: 12_000 } };

  it("is unknown until decided, and reports every branch with its root and effects", async () => {
    const r = await evaluate("CA.contest", facts, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(r.root).toBe("unknown");
    expect(r.leaves["any-purpose"]!.basis.by).toBe("undecided");
    const c6 = r.contested[0]!;
    expect(c6.branches.map((b) => [b.id, b.root, b.exposure])).toEqual([
      ["A", true, false],
      ["B", false, true],
    ]);
    expect(c6.branches[0]!.effects).toEqual([
      { id: "may-deduct", applies: true },
      { id: "bill-separately", applies: false },
    ]);
    expect(r.exposure).toMatchObject({ root: false, sets: { "any-purpose": false } });
    expect(r.exposure!.effects.find((e) => e.id === "bill-separately")!.applies).toBe(true);
    expect(r.investigation).toEqual([expect.objectContaining({ leafId: "any-purpose", settle: { by: "decision", decision: { by: "operator", what: "Whether any-purpose." }, contested: "C6" } })]);
  });

  it("takes a decision keyed by leaf id, or by tree and leaf", async () => {
    const r1 = await evaluate("CA.contest", facts, { jurisdiction: j, eventDate: "2026-11-16", decisions: { "any-purpose": true } });
    expect(r1.root).toBe(true);
    expect(r1.effects[0]).toMatchObject({ applies: true, amount: { status: "known", value: 12_000 } });
    const r2 = await evaluate("CA.contest", facts, {
      jurisdiction: j,
      eventDate: "2026-11-16",
      decisions: { "any-purpose": true, "CA.contest#any-purpose": { value: false, by: "operator-1", note: "Bill it." } },
    });
    expect(r2.root).toBe(false);
    expect(r2.leaves["any-purpose"]!.basis).toMatchObject({ by: "decision", decided: { value: false, by: "operator-1" } });
  });

  it("asks a question that matters only under one branch, so that branch can be reported", async () => {
    const t = makeTree("CA.branchq", { type: "all", children: [discretionary("reach", "C6"), semantic("owed", ["e.ledger"])] }, {
      inputs: ["f", "e.ledger"],
      contested: [
        {
          issue: "C6",
          question: "Does the deposit reach it?",
          exposureBranch: "B",
          branches: [
            { id: "A", reading: "Yes.", authority: [{ citation: "Civ 1950.5(b)", quote: "any purpose" }], effect: { statement: "Yes.", sets: { reach: true } } },
            { id: "B", reading: "No.", authority: [{ citation: "Civ 1950.5(b)", quote: "four purposes" }], effect: { statement: "No.", sets: { reach: false } } },
          ],
        },
      ],
    });
    const answers = fixtureAnswers({ owed: true });
    const r = await evaluate("CA.branchq", { e: { ledger: "late fee unpaid" } }, { jurisdiction: jurisdictionOf(t), eventDate: "2026-11-16", decisions: { reach: false }, answers });
    expect(r.root).toBe(false);
    expect(answers.asked.map((a) => a.leafId)).toEqual(["owed"]);
    expect(r.contested[0]!.branches.map((b) => [b.id, b.root])).toEqual([
      ["A", true],
      ["B", false],
    ]);
  });

  it("when the lease makes it rent, every branch agrees", async () => {
    const r = await evaluate("CA.contest", { f: { ...facts.f, is_rent: true } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(r.root).toBe(true);
    expect(r.contested[0]!.branches.map((b) => b.root)).toEqual([true, true]);
    expect(r.exposure!.root).toBe(true);
  });
});

describe("investigation by sensitivity", () => {
  it("lists only unknowns on an open path, and marks those that settle the root alone", async () => {
    // any(all(a, b), all(c, d)) with every leaf unknown: no single leaf settles it, but each matters.
    const t = makeTree("CA.inv", {
      type: "any",
      children: [
        { type: "all", children: [fact("a"), fact("b")] },
        { type: "all", children: [fact("c"), fact("d")] },
        fact("e"),
      ],
    });
    const j = jurisdictionOf(t);
    const r = await evaluate("CA.inv", { f: { e: false } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(r.root).toBe("unknown");
    expect(r.investigation.map((i) => [i.leafId, i.ifTrue, i.ifFalse, i.decisive])).toEqual([
      ["a", "unknown", "unknown", false],
      ["b", "unknown", "unknown", false],
      ["c", "unknown", "unknown", false],
      ["d", "unknown", "unknown", false],
    ]);
    expect(r.investigation[0]!.settle).toEqual({ by: "facts", facts: ["f.a"], missing: ["f.a"], via: [] });

    // Once c is known false, c and d are blocked; a and b each settle the root when false.
    const r2 = await evaluate("CA.inv", { f: { c: false, e: false } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(r2.investigation.map((i) => [i.leafId, i.ifTrue, i.ifFalse, i.decisive])).toEqual([
      ["a", "unknown", false, true],
      ["b", "unknown", false, true],
    ]);
  });

  it("is empty once the root is known", async () => {
    const t = makeTree("CA.known", { type: "any", children: [fact("a"), fact("b")] });
    const r = await evaluate("CA.known", { f: { a: true } }, { jurisdiction: jurisdictionOf(t), eventDate: "2026-11-16" });
    expect(r.root).toBe(true);
    expect(r.investigation).toEqual([]);
  });
});

describe("cross-tree formulas", () => {
  const charge = makeTree("CA.charge", fact("stayed"), {
    effects: [{ id: "charge", kind: "permission", when: "holds", statement: "Charge.", amount: "f.days * f.rate" }],
  });
  const deduct = makeTree("CA.deduct", { type: "all", children: [fact("chargeable", 'holds("CA.charge")'), fact("is-rent")] }, {
    effects: [{ id: "deduct", kind: "permission", when: "holds", statement: "Deduct.", amount: 'amount("CA.charge", "charge")' }],
  });

  it("holds() and amount() evaluate the referenced tree on the same facts", async () => {
    const j = jurisdictionOf(charge, deduct);
    const r = await evaluate("CA.deduct", { f: { stayed: true, is_rent: true, days: 6, rate: 273_500 / 30 } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(r.root).toBe(true);
    expect(r.effects[0]!.amount).toMatchObject({ status: "known", value: 54_700 });
    expect(r.leaves.chargeable!.basis).toMatchObject({ by: "compute", references: ["CA.charge"] });
    expect(Object.keys(r.references)).toEqual(["CA.charge"]);
    expect(r.references["CA.charge"]!.root).toBe(true);
  });

  it("passes the referenced tree's unknowns up the investigation list", async () => {
    const j = jurisdictionOf(charge, deduct);
    const r = await evaluate("CA.deduct", { f: { is_rent: true } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(r.root).toBe("unknown");
    expect(r.investigation).toEqual([
      expect.objectContaining({ leafId: "chargeable", settle: expect.objectContaining({ by: "facts", via: [expect.objectContaining({ treeId: "CA.charge", leafId: "stayed" })] }) }),
    ]);
  });

  it("does not evaluate a referenced tree that cannot matter", async () => {
    const j = jurisdictionOf(charge, deduct);
    const r = await evaluate("CA.deduct", { f: { is_rent: false } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(r.root).toBe(false);
    expect(r.leaves.chargeable!.basis.by).toBe("not-needed");
    expect(r.references).toEqual({});
  });

  it("amount() of an effect that does not follow is absent", async () => {
    const reader = makeTree("CA.reader", fact("x"), {
      effects: [{ id: "read", kind: "permission", when: "holds", statement: "Read.", amount: 'amount("CA.charge", "charge")' }],
    });
    const j = jurisdictionOf(charge, reader);
    const facts = { f: { x: true, days: 6, rate: 100 } };
    const off = await evaluate("CA.reader", { f: { ...facts.f, stayed: false } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(off.effects[0]!.amount).toMatchObject({ status: "absent" });
    const on = await evaluate("CA.reader", { f: { ...facts.f, stayed: true } }, { jurisdiction: j, eventDate: "2026-11-16" });
    expect(on.effects[0]!.amount).toMatchObject({ status: "known", value: 600 });
    expect(off.diagnostics).toEqual([]);
  });

  it("stops a cycle and reports it", async () => {
    const a = makeTree("CA.a", fact("b-holds", 'holds("CA.b")'));
    const b = makeTree("CA.b", fact("a-holds", 'holds("CA.a")'));
    const r = await evaluate("CA.a", {}, { jurisdiction: jurisdictionOf(a, b), eventDate: "2026-11-16" });
    expect(r.root).toBe("unknown");
    expect(r.diagnostics.map((d) => d.message)).toContain("circular reference: CA.a → CA.b → CA.a");
  });

  it("evaluates the referenced tree under its own exposure branch in the exposure result", async () => {
    const gate = makeTree("CA.gate", { type: "any", children: [fact("listed"), discretionary("skipped-no-bar", "C9")] }, {
      contested: [
        {
          issue: "C9",
          question: "Does a skipped inspection bar it?",
          exposureBranch: "B",
          branches: [
            { id: "A", reading: "No bar.", authority: [{ citation: "Civ 1950.5(f)(4)", quote: "if an initial inspection" }], effect: { statement: "No bar.", sets: { "skipped-no-bar": true } } },
            { id: "B", reading: "Bar.", authority: [{ citation: "Civ 1950.5(f)(1)", quote: "the purpose of" }], effect: { statement: "Bar.", sets: { "skipped-no-bar": false } } },
          ],
        },
      ],
    });
    const repair = makeTree("CA.repair", fact("gate", 'holds("CA.gate")'));
    const j = jurisdictionOf(gate, repair);
    const r = await evaluate("CA.repair", { f: { listed: false } }, { jurisdiction: j, eventDate: "2026-11-16", decisions: { "skipped-no-bar": true } });
    expect(r.root).toBe(true);
    // The repair tree has no contested point of its own, but its exposure puts the gate on branch B.
    expect(r.exposure).toMatchObject({ root: false, sets: {} });
    expect(r.references["CA.gate"]!.exposure!.root).toBe(false);
    // A tree that reaches nothing contested reports no exposure.
    const plain = await evaluate("CA.gate", { f: { listed: true } }, { jurisdiction: jurisdictionOf(makeTree("CA.gate", fact("listed"))), eventDate: "2026-11-16" });
    expect(plain.exposure).toBeNull();
  });
});

describe("the trace", () => {
  it("gives every node its value, and every leaf its statement, citation and basis", async () => {
    const t = makeTree("CA.trace", { type: "all", children: [fact("a"), { type: "not", child: fact("b") }] });
    const r = await evaluate("CA.trace", { f: { a: true, b: false } }, { jurisdiction: jurisdictionOf(t), eventDate: "2026-11-16" });
    expect(r.trace).toMatchObject({
      type: "all",
      path: "/root",
      value: true,
      children: [
        { type: "condition", path: "/root/children/0", id: "a", value: true, statement: "Leaf a.", source: { citation: "Civ 1950.5(b)" }, basis: { by: "compute", formula: "f.a", facts: ["f.a"] } },
        { type: "not", path: "/root/children/1", value: true, child: { id: "b", value: false } },
      ],
    });
    expect(JSON.parse(JSON.stringify(r)).root).toBe(true);
  });
});
