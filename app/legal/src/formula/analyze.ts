import { type Expr, pathOf } from "./parse.js";

/** Built-in functions and how many arguments each takes ([min, max]; max Infinity for a list). */
export const BUILTINS: Readonly<Record<string, readonly [number, number]>> = {
  days: [2, 2],
  count: [1, 1],
  len: [1, 1],
  exists: [1, 1],
  sum: [1, Infinity],
  min: [1, Infinity],
  max: [1, Infinity],
  round: [1, 1],
  abs: [1, 1],
  earliest: [1, Infinity],
  latest: [1, Infinity],
  hours: [1, 1],
  date: [1, 1],
  any: [1, 1],
  all: [1, 1],
  holds: [1, 1],
  amount: [2, 2],
};

/** Names a formula may not use as a property: they belong to JavaScript objects, not to facts. */
export const FORBIDDEN_PROPERTIES = new Set(Object.getOwnPropertyNames(Object.prototype).concat(["prototype"]));

export interface FormulaAnalysis {
  /** Fact paths the formula reads, e.g. "moveOut.vacateDate" or "ledger.unpaidRentThrough" (a method). */
  facts: string[];
  /** Tree parameters it reads, by id. */
  parameters: string[];
  /** Trees it evaluates through holds() or amount(). */
  holds: string[];
  amounts: { tree: string; effect: string }[];
  problems: string[];
}

export function analyzeFormula(expr: Expr): FormulaAnalysis {
  const facts = new Set<string>();
  const parameters = new Set<string>();
  const holds = new Set<string>();
  const amounts: { tree: string; effect: string }[] = [];
  const problems: string[] = [];

  // A member chain is recorded once, at its longest path; a call cuts the chain there.
  const chain = (e: Expr): void => {
    const p = pathOf(e);
    if (p === undefined || p.includes("(")) {
      // A property of a computed value: only the computation reads facts.
      if (e.kind === "member") walk(e.object);
      return;
    }
    const [root, second] = p.split(".");
    if (root === "parameters") {
      if (!second) problems.push("parameters must be followed by a parameter id");
      else parameters.add(second);
      if (p.split(".").length > 2) problems.push(`parameter ${second} has no properties`);
      return;
    }
    for (const part of p.split(".")) if (FORBIDDEN_PROPERTIES.has(part)) problems.push(`"${part}" cannot be used in a path`);
    facts.add(p);
  };

  const walk = (e: Expr): void => {
    switch (e.kind) {
      case "number":
      case "string":
      case "boolean":
      case "null":
        return;
      case "name":
      case "member":
        return chain(e);
      case "call": {
        if (e.callee.kind === "name") {
          const name = e.callee.name;
          const arity = BUILTINS[name];
          if (!arity) problems.push(`unknown function ${name}()`);
          else if (e.args.length < arity[0] || e.args.length > arity[1]) problems.push(`${name}() takes ${arity[0] === arity[1] ? arity[0] : `${arity[0]} or more`} argument(s)`);
          if (name === "holds" || name === "amount") {
            const lits = e.args.map((a) => (a.kind === "string" ? a.value : undefined));
            if (lits.some((l) => l === undefined)) problems.push(`${name}() takes string literals`);
            else if (name === "holds" && lits[0]) holds.add(lits[0]);
            else if (name === "amount" && lits[0] && lits[1]) amounts.push({ tree: lits[0], effect: lits[1] });
            return;
          }
        } else {
          // A method: record its path (ledger.unpaidRentThrough) as a fact the binding supplies.
          chain(e.callee);
        }
        for (const a of e.args) walk(a);
        return;
      }
      case "list":
        for (const a of e.items) walk(a);
        return;
      case "negate":
      case "not":
        return walk(e.arg);
      case "arith":
      case "compare":
      case "logical":
        walk(e.left);
        walk(e.right);
        return;
      case "conditional":
        walk(e.test);
        walk(e.then);
        walk(e.otherwise);
        return;
    }
  };

  walk(expr);
  return { facts: [...facts], parameters: [...parameters], holds: [...holds], amounts, problems };
}
