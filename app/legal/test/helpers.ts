import { type Jurisdiction, type Node, type Tree, buildJurisdiction, loadJurisdiction } from "../src/index.js";

export const TREES_DIR = new URL("../../../research/legal-engine/jurisdictions/CA/account_core/trees", import.meta.url).pathname;

let ca: Promise<Jurisdiction> | undefined;
/** The California account-core trees from the research folder, loaded once per test file. */
export function california(): Promise<Jurisdiction> {
  ca ??= loadJurisdiction(TREES_DIR);
  return ca;
}

const SRC = { citation: "Civ 1950.5(b)", quote: "test quote, not checked here" };

/** A determinate leaf reading a fact path. */
export const fact = (id: string, compute = `f.${id.replace(/-/g, "_")}`): Node => ({
  type: "condition",
  id,
  kind: "determinate",
  statement: `Leaf ${id}.`,
  source: SRC,
  compute,
});

export const semantic = (id: string, inputs: string[]): Node => ({
  type: "condition",
  id,
  kind: "semantic",
  statement: `Leaf ${id}.`,
  source: SRC,
  question: { type: "yesno", wording: `Is ${id} so?`, inputs },
});

export const discretionary = (id: string, contested?: string): Node => ({
  type: "condition",
  id,
  kind: "discretionary",
  statement: `Leaf ${id}.`,
  source: SRC,
  decision: { by: "operator", what: `Whether ${id}.` },
  ...(contested ? { contested } : {}),
});

/** A minimal valid tree around a root; inputs default to "f" and any question inputs. */
export function makeTree(id: string, root: Node, extra: Partial<Tree> = {}): Tree {
  return {
    id,
    title: `Does ${id} hold?`,
    decisionPoint: "DP5.1",
    layer: "CA",
    effective: { from: "2026-01-01", to: null },
    inputs: ["f", "g", "e"],
    parameters: [],
    root,
    effects: [{ id: "follows", kind: "permission", when: "holds", statement: "It follows." }],
    contested: [],
    ...extra,
  };
}

export function jurisdictionOf(...trees: Tree[]): Jurisdiction {
  return buildJurisdiction(trees.map((t) => ({ name: `${t.id}.json`, json: structuredClone(t) })));
}
