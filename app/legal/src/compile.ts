import { type FormulaAnalysis, analyzeFormula } from "./formula/analyze.js";
import { type Expr, parseFormula } from "./formula/parse.js";
import type { Condition, Effect, Node, Tree } from "./schema.js";

/** A tree with every formula parsed and every internal reference checked. */
export interface CompiledTree {
  tree: Tree;
  leaves: Map<string, CompiledLeaf>;
  effects: CompiledEffect[];
  parameters: Readonly<Record<string, number | string>>;
  /** Trees this one evaluates through holds() or amount(), and the effects named by amount(). */
  holds: string[];
  amounts: { tree: string; effect: string }[];
}

export interface Formula {
  source: string;
  expr: Expr;
  analysis: FormulaAnalysis;
}

export interface CompiledLeaf {
  node: Condition;
  /** JSON pointer into the tree, e.g. "/root/children/3". */
  path: string;
  compute?: Formula;
}

export const EFFECT_FORMULAS = ["amount", "due", "margin", "notBefore"] as const;
export type EffectFormula = (typeof EFFECT_FORMULAS)[number];

export interface CompiledEffect {
  effect: Effect;
  formulas: Partial<Record<EffectFormula, Formula>>;
}

export class TreeValidationError extends Error {
  constructor(readonly problems: string[]) {
    super(`${problems.length} problem(s) in the legal trees:\n${problems.map((p) => `- ${p}`).join("\n")}`);
  }
}

/** Visits every node with its JSON pointer. */
export function walkNodes(node: Node, path: string, visit: (node: Node, path: string) => void): void {
  visit(node, path);
  switch (node.type) {
    case "all":
    case "any":
      node.children.forEach((c, i) => walkNodes(c, `${path}/children/${i}`, visit));
      return;
    case "not":
      return walkNodes(node.child, `${path}/child`, visit);
    case "unless":
      walkNodes(node.rule, `${path}/rule`, visit);
      walkNodes(node.exception, `${path}/exception`, visit);
      return;
    case "condition":
      return;
  }
}

/** Every formula in a tree, with where it sits. */
export function formulasOf(tree: Tree): { where: string; source: string }[] {
  const out: { where: string; source: string }[] = [];
  walkNodes(tree.root, "/root", (n) => {
    if (n.type === "condition" && n.compute !== undefined) out.push({ where: `${tree.id}:${n.id}.compute`, source: n.compute });
  });
  for (const e of tree.effects) {
    for (const k of EFFECT_FORMULAS) {
      const f = e[k];
      if (f !== undefined) out.push({ where: `${tree.id}:${e.id}.${k}`, source: f });
    }
  }
  return out;
}

const covered = (path: string, inputs: string[]) =>
  inputs.some((i) => path === i || path.startsWith(`${i}.`) || i.startsWith(`${path}.`));

/**
 * Compiles one tree and lists what is wrong inside it. References to other trees are checked by the
 * loader, which sees the whole jurisdiction.
 */
export function compileTree(tree: Tree): { compiled: CompiledTree; problems: string[] } {
  const problems: string[] = [];
  const where = (w: string) => `${tree.id}${w}`;
  const parameters: Record<string, number | string> = {};
  for (const p of tree.parameters) {
    if (p.id in parameters) problems.push(where(`: parameter ${p.id} is defined twice`));
    parameters[p.id] = p.value;
  }
  const holds = new Set<string>();
  const amounts: { tree: string; effect: string }[] = [];

  const formula = (source: string, w: string): Formula | undefined => {
    let expr: Expr;
    try {
      expr = parseFormula(source);
    } catch (err) {
      problems.push(where(`${w}: ${(err as Error).message}`));
      return undefined;
    }
    const analysis = analyzeFormula(expr);
    for (const p of analysis.problems) problems.push(where(`${w}: ${p}`));
    for (const p of analysis.parameters) if (!(p in parameters)) problems.push(where(`${w}: unknown parameter ${p}`));
    for (const f of analysis.facts) if (!covered(f, tree.inputs)) problems.push(where(`${w}: ${f} is not a declared input`));
    for (const h of analysis.holds) holds.add(h);
    amounts.push(...analysis.amounts);
    return { source, expr, analysis };
  };

  const leaves = new Map<string, CompiledLeaf>();
  walkNodes(tree.root, "/root", (node, path) => {
    if (node.type !== "condition") return;
    if (leaves.has(node.id)) problems.push(where(`: leaf ${node.id} appears twice`));
    const leaf: CompiledLeaf = { node, path };
    if (node.compute !== undefined) {
      const f = formula(node.compute, `:${node.id}.compute`);
      if (f) leaf.compute = f;
    }
    for (const input of node.question?.inputs ?? []) {
      if (!tree.inputs.includes(input)) problems.push(where(`:${node.id}: question input ${input} is not a declared input`));
    }
    leaves.set(node.id, leaf);
  });

  const effects: CompiledEffect[] = [];
  const effectIds = new Set<string>();
  for (const effect of tree.effects) {
    if (effectIds.has(effect.id)) problems.push(where(`: effect ${effect.id} appears twice`));
    effectIds.add(effect.id);
    const formulas: CompiledEffect["formulas"] = {};
    for (const k of EFFECT_FORMULAS) {
      const src = effect[k];
      if (src === undefined) continue;
      const f = formula(src, `:${effect.id}.${k}`);
      if (f) formulas[k] = f;
    }
    effects.push({ effect, formulas });
  }

  const issues = new Map<string, Set<string>>();
  for (const c of tree.contested) {
    if (issues.has(c.issue)) problems.push(where(`: contested point ${c.issue} appears twice`));
    const set = new Set<string>();
    const branchIds = new Set<string>();
    for (const b of c.branches) {
      if (branchIds.has(b.id)) problems.push(where(`: ${c.issue} has two branches ${b.id}`));
      branchIds.add(b.id);
      for (const leafId of Object.keys(b.effect.sets ?? {})) {
        if (!leaves.has(leafId)) problems.push(where(`: ${c.issue} branch ${b.id} sets ${leafId}, which is not a leaf of this tree`));
        set.add(leafId);
      }
    }
    if (!branchIds.has(c.exposureBranch)) problems.push(where(`: ${c.issue} exposure branch ${c.exposureBranch} is not one of its branches`));
    issues.set(c.issue, set);
  }
  for (const [id, leaf] of leaves) {
    const issue = leaf.node.contested;
    if (issue === undefined) continue;
    const set = issues.get(issue);
    if (!set) problems.push(where(`:${id}: contested ${issue} is not defined in this tree`));
    else if (!set.has(id)) problems.push(where(`:${id}: no branch of ${issue} sets this leaf`));
  }

  const { from, to } = tree.effective;
  if (to !== null && to < from) problems.push(where(`: effective.to ${to} is before effective.from ${from}`));

  return { compiled: { tree, leaves, effects, parameters, holds: [...holds], amounts }, problems };
}

const cache = new WeakMap<Tree, CompiledTree>();

/** The compiled form of a tree, compiled once. Throws if the tree is malformed. */
export function compiled(tree: Tree): CompiledTree {
  let c = cache.get(tree);
  if (!c) {
    const r = compileTree(tree);
    if (r.problems.length) throw new TreeValidationError(r.problems);
    c = r.compiled;
    cache.set(tree, c);
  }
  return c;
}

/** Registers an already compiled tree, so the loader's work is not repeated. */
export function remember(c: CompiledTree): void {
  cache.set(c.tree, c);
}

/** What a tree reads from the case: its declared inputs, the fact paths its formulas use, and each question's evidence. */
export function requiredFacts(tree: Tree): { inputs: string[]; formulas: string[]; questions: { leaf: string; inputs: string[] }[] } {
  const c = compiled(tree);
  const formulas = new Set<string>();
  for (const leaf of c.leaves.values()) for (const f of leaf.compute?.analysis.facts ?? []) formulas.add(f);
  for (const e of c.effects) for (const f of Object.values(e.formulas)) for (const p of f.analysis.facts) formulas.add(p);
  const questions = [...c.leaves.values()].filter((l) => l.node.question).map((l) => ({ leaf: l.node.id, inputs: l.node.question!.inputs }));
  return { inputs: tree.inputs, formulas: [...formulas].sort(), questions };
}
