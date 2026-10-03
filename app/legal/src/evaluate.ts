import { type CompiledLeaf, type CompiledTree, EFFECT_FORMULAS, type EffectFormula, type Formula, compiled } from "./compile.js";
import { type FormulaRun, FormulaError, containsUnknown, runFormula, truthOf } from "./formula/evaluate.js";
import { parseFormula } from "./formula/parse.js";
import { type Jurisdiction, inForce } from "./loader.js";
import { combine, liveLeaves } from "./logic.js";
import type { Condition, Effect, LeafKind, Node, Question, Source, Tree } from "./schema.js";
import { isTemporal } from "./time.js";
import { type Truth, UNKNOWN, type Value, not3, roundHalfAway } from "./values.js";

// ---------------------------------------------------------------- inputs

/** The case facts, by input name: tenancy, deposit, moveOut, ledger, line... See the demo fixture. */
export type Facts = Readonly<Record<string, unknown>>;

export interface Answer {
  value: Truth;
  confidence?: number;
  provider?: string;
  rationale?: string;
}

export interface AnswerContext {
  treeId: string;
  leafId: string;
}

/**
 * Answers a semantic question. It is called only once every input in the question's evidence
 * contract is supplied; `inputs` holds those values by input name.
 */
export type AnswerProvider = (leaf: Condition, question: Question, inputs: Record<string, unknown>, context: AnswerContext) => Promise<Answer>;

export interface DecisionRecord {
  value: boolean;
  by?: string;
  note?: string;
}

/** Decisions on discretionary leaves, keyed by leaf id, or by "CA.tree#leaf-id" for one tree only. */
export type Decisions = Readonly<Record<string, boolean | DecisionRecord>>;

export interface EvaluateOptions {
  /** The trees that holds() and amount() reach. Needed when a tree refers to another. */
  jurisdiction?: Jurisdiction;
  /** The case's event date: selects the version in force of every tree reached. Defaults to the tree's own start. */
  eventDate?: string;
  /** Semantic leaves without a provider stay unknown. */
  answers?: AnswerProvider;
  decisions?: Decisions;
}

// ---------------------------------------------------------------- results

export interface FormulaOutcome {
  formula: string;
  /** known: a value; absent: the formula's facts say there is none; unknown: something is missing. */
  status: "known" | "absent" | "unknown";
  /** Integer cents for an amount; an ISO date or date-time for due, margin and notBefore; a truth value for compute. */
  value?: number | string | boolean;
  /** The amount before rounding to whole cents, when it was not whole. */
  exact?: number;
  missing?: string[];
  error?: string;
}

export type LeafBasis =
  | { by: "compute"; formula: string; result: FormulaOutcome; facts: string[]; references: string[] }
  | { by: "answer"; question: string; inputs: string[]; answer: Answer }
  | { by: "evidence-missing"; question: string; inputs: string[]; missing: string[] }
  | { by: "no-provider"; question: string; inputs: string[] }
  | { by: "decision"; decision: { by: "agent" | "operator"; what: string }; decided: DecisionRecord }
  | { by: "undecided"; decision: { by: "agent" | "operator"; what: string } }
  /** Not evaluated, because no value of it could change the result. */
  | { by: "not-needed" };

export interface LeafTrace {
  type: "condition";
  path: string;
  id: string;
  kind: LeafKind;
  statement: string;
  source: Source;
  contested?: string;
  value: Truth;
  basis: LeafBasis;
}

export type NodeTrace =
  | LeafTrace
  | { type: "all" | "any"; path: string; value: Truth; children: NodeTrace[] }
  | { type: "not"; path: string; value: Truth; child: NodeTrace }
  | { type: "unless"; path: string; value: Truth; rule: NodeTrace; exception: NodeTrace };

export interface EffectResult {
  id: string;
  kind: Effect["kind"];
  when: Effect["when"];
  statement: string;
  /** Whether the effect follows: the root's value for "holds", its negation for "fails". */
  applies: Truth;
  amount?: FormulaOutcome;
  due?: FormulaOutcome;
  margin?: FormulaOutcome;
  notBefore?: FormulaOutcome;
  consequence?: string;
  source?: Source;
}

export interface BranchResult {
  id: string;
  reading: string;
  statement: string;
  sets: Record<string, boolean>;
  exposure: boolean;
  root: Truth;
  effects: { id: string; applies: Truth }[];
}

export interface ContestedResult {
  issue: string;
  question: string;
  exposureBranch: string;
  branches: BranchResult[];
}

/** The tree on the branch least favorable to the operator, in it and in every tree it reaches. */
export interface ExposureResult {
  root: Truth;
  sets: Record<string, boolean>;
  effects: EffectResult[];
}

export type Settlement =
  | { by: "facts"; facts: string[]; missing: string[]; error?: string; via: InvestigationItem[] }
  | { by: "question"; question: string; inputs: string[]; missing: string[] }
  | { by: "decision"; decision: { by: "agent" | "operator"; what: string }; contested?: string };

/** An unknown leaf whose resolution could change the result, and what would settle it. */
export interface InvestigationItem {
  treeId: string;
  leafId: string;
  kind: LeafKind;
  statement: string;
  citation: string;
  /** The root if this leaf alone became true, or false. */
  ifTrue: Truth;
  ifFalse: Truth;
  /** Resolving this leaf alone settles the root one way or the other. */
  decisive: boolean;
  settle: Settlement;
}

export interface Diagnostic {
  treeId: string;
  where: string;
  message: string;
}

export interface EvaluationResult {
  treeId: string;
  title: string;
  decisionPoint: string;
  effective: Tree["effective"];
  eventDate: string;
  root: Truth;
  trace: NodeTrace;
  leaves: Record<string, LeafTrace>;
  effects: EffectResult[];
  contested: ContestedResult[];
  exposure: ExposureResult | null;
  investigation: InvestigationItem[];
  /** The trees reached through holds() and amount(), evaluated on the same facts (top level only). */
  references: Record<string, EvaluationResult>;
  diagnostics: Diagnostic[];
}

// ---------------------------------------------------------------- evaluation

type Mode = "base" | "exposure";

interface LeafEval {
  value: Truth;
  basis: LeafBasis;
  missing: string[];
  references: string[];
}

interface TreeRun {
  key: string;
  c: CompiledTree;
  leaves: Map<string, LeafEval>;
  root: Truth;
  effects: EffectResult[];
  result?: EvaluationResult;
}

const versionKey = (t: Tree) => `${t.id}@${t.effective.from}`;

function exposureSets(tree: Tree): Record<string, boolean> {
  const sets: Record<string, boolean> = {};
  for (const c of tree.contested) Object.assign(sets, c.branches.find((b) => b.id === c.exposureBranch)?.effect.sets ?? {});
  return sets;
}

const isCrossTree = (leaf: CompiledLeaf) => !!leaf.compute && (leaf.compute.analysis.holds.length > 0 || leaf.compute.analysis.amounts.length > 0);

function outcome(f: Formula, r: FormulaRun, expect: "truth" | "amount" | "date"): FormulaOutcome {
  const out: FormulaOutcome = { formula: f.source, status: "unknown" };
  if (r.missing.length) out.missing = r.missing;
  if (r.error !== undefined) return { ...out, error: r.error };
  const v = r.value;
  if (v === UNKNOWN) return out;
  if (v === null) return { ...out, status: "absent" };
  if (expect === "amount") {
    if (typeof v !== "number" || !Number.isFinite(v)) return { ...out, error: `an amount must be a number of cents, got ${JSON.stringify(v)}` };
    const cents = roundHalfAway(v);
    return Math.abs(cents - v) > 1e-6 ? { ...out, status: "known", value: cents, exact: v } : { ...out, status: "known", value: cents };
  }
  if (expect === "date") {
    if (!isTemporal(v)) return { ...out, error: `a date formula must give a date, got ${JSON.stringify(v)}` };
    return { ...out, status: "known", value: v };
  }
  if (typeof v !== "boolean") return { ...out, error: `a condition must be true or false, got ${JSON.stringify(v)}` };
  return { ...out, status: "known", value: v };
}

class Session {
  private readonly runs = new Map<string, Promise<TreeRun>>();
  private readonly done = new Map<string, TreeRun>();
  private readonly asked = new Map<string, Promise<LeafEval>>();
  private readonly plain = new Map<string, Promise<FormulaRun>>();
  private readonly paths = new Map<string, ReturnType<typeof parseFormula>>();
  private readonly seen = new Set<string>();
  readonly diagnostics: Diagnostic[] = [];

  constructor(
    private readonly facts: Facts,
    private readonly options: EvaluateOptions,
    readonly eventDate: string,
  ) {}

  private diagnose(treeId: string, where: string, message: string) {
    const k = `${treeId}|${where}|${message}`;
    if (this.seen.has(k)) return;
    this.seen.add(k);
    this.diagnostics.push({ treeId, where, message });
  }

  /** Base-mode results of every tree evaluated, except the one given. */
  references(except: string): Record<string, EvaluationResult> {
    const out: Record<string, EvaluationResult> = {};
    for (const [key, run] of this.done) if (key !== except && key.endsWith(":base") && run.result) out[run.c.tree.id] = run.result;
    return out;
  }

  run(c: CompiledTree, mode: Mode, chain: string[]): Promise<TreeRun> {
    const key = `${versionKey(c.tree)}:${mode}`;
    if (chain.includes(key)) {
      return Promise.reject(new FormulaError(`circular reference: ${[...chain, key].map((k) => k.split("@")[0]).join(" → ")}`));
    }
    let p = this.runs.get(key);
    if (!p) {
      p = this.evaluateTree(c, mode, key, [...chain, key]).then((r) => {
        this.done.set(key, r);
        return r;
      });
      this.runs.set(key, p);
    }
    return p;
  }

  private reference(id: string, mode: Mode, chain: string[]): Promise<TreeRun> {
    const jur = this.options.jurisdiction;
    if (!jur) throw new FormulaError(`${id} is another tree; evaluation needs the jurisdiction`);
    const tree = jur.select(id, this.eventDate);
    if (!tree) throw new FormulaError(`no version of ${id} is in force on ${this.eventDate}`);
    return this.run(compiled(tree), mode, chain);
  }

  private scope(c: CompiledTree, mode: Mode, chain: string[]) {
    return {
      facts: this.facts,
      parameters: c.parameters,
      holds: async (id: string) => (await this.reference(id, mode, chain)).root,
      amount: async (id: string, effectId: string): Promise<Value> => {
        const run = await this.reference(id, mode, chain);
        const a = run.effects.find((e) => e.id === effectId)?.amount;
        if (!a) throw new FormulaError(`${id} has no amount on effect ${effectId}`);
        return a.status === "known" ? (a.value as number) : a.status === "absent" ? null : UNKNOWN;
      },
    };
  }

  /** Runs a formula; one that reaches no other tree is the same in every mode, so it runs once. */
  private formula(c: CompiledTree, where: string, f: Formula, mode: Mode, chain: string[]): Promise<FormulaRun> {
    const crossTree = f.analysis.holds.length > 0 || f.analysis.amounts.length > 0;
    if (crossTree) return runFormula(f.expr, this.scope(c, mode, chain));
    const k = `${versionKey(c.tree)}|${where}`;
    let p = this.plain.get(k);
    if (!p) {
      p = runFormula(f.expr, this.scope(c, mode, chain));
      this.plain.set(k, p);
    }
    return p;
  }

  private async compute(c: CompiledTree, leaf: CompiledLeaf, mode: Mode, chain: string[]): Promise<LeafEval> {
    const f = leaf.compute!;
    const r = await this.formula(c, `${leaf.node.id}.compute`, f, mode, chain);
    const result = outcome(f, r, "truth");
    if (result.error !== undefined) this.diagnose(c.tree.id, leaf.node.id, result.error);
    const value: Truth = result.status === "known" ? (result.value as boolean) : result.status === "absent" ? false : "unknown";
    return {
      value,
      basis: { by: "compute", formula: f.source, result, facts: f.analysis.facts, references: r.references },
      missing: r.missing,
      references: r.references,
    };
  }

  private decide(tree: Tree, node: Condition): LeafEval {
    const decision = node.decision!;
    const d = this.options.decisions?.[`${tree.id}#${node.id}`] ?? this.options.decisions?.[node.id];
    if (d === undefined) return { value: "unknown", basis: { by: "undecided", decision }, missing: [], references: [] };
    const decided = typeof d === "boolean" ? { value: d } : d;
    return { value: decided.value, basis: { by: "decision", decision, decided }, missing: [], references: [] };
  }

  private async resolve(path: string): Promise<Value> {
    let expr = this.paths.get(path);
    if (!expr) {
      expr = parseFormula(path);
      this.paths.set(path, expr);
    }
    return (await runFormula(expr, { facts: this.facts })).value;
  }

  /** Asks a semantic question once per tree version, and only with its evidence contract met. */
  private ask(tree: Tree, node: Condition): Promise<LeafEval> {
    const k = `${versionKey(tree)}#${node.id}`;
    let p = this.asked.get(k);
    if (!p) {
      p = this.askNow(tree, node);
      this.asked.set(k, p);
    }
    return p;
  }

  private async askNow(tree: Tree, node: Condition): Promise<LeafEval> {
    const q = node.question!;
    const inputs: Record<string, unknown> = {};
    const missing: string[] = [];
    for (const path of q.inputs) {
      const v = await this.resolve(path);
      if (containsUnknown(v)) missing.push(path);
      else inputs[path] = v;
    }
    const none = { missing, references: [] };
    if (missing.length) return { value: "unknown", basis: { by: "evidence-missing", question: q.wording, inputs: q.inputs, missing }, ...none };
    const provider = this.options.answers;
    if (!provider) return { value: "unknown", basis: { by: "no-provider", question: q.wording, inputs: q.inputs }, ...none };
    let answer: Answer;
    try {
      answer = await provider(node, q, inputs, { treeId: tree.id, leafId: node.id });
      if (answer.value !== true && answer.value !== false && answer.value !== "unknown") {
        throw new Error(`answer must be true, false or "unknown", got ${JSON.stringify(answer.value)}`);
      }
    } catch (err) {
      const message = `the answer provider failed: ${(err as Error).message}`;
      this.diagnose(tree.id, node.id, message);
      answer = { value: "unknown", rationale: message };
    }
    return { value: answer.value, basis: { by: "answer", question: q.wording, inputs: q.inputs, answer }, ...none };
  }

  private async evaluateTree(c: CompiledTree, mode: Mode, key: string, chain: string[]): Promise<TreeRun> {
    const tree = c.tree;
    const leaves = new Map<string, LeafEval>();
    const modeSets = mode === "exposure" ? exposureSets(tree) : {};
    const scenarios: Record<string, boolean>[] =
      mode === "base" ? [{}, ...tree.contested.flatMap((ct) => ct.branches.map((b) => b.effect.sets ?? {}))] : [modeSets];
    const valueIn = (sets: Record<string, boolean>) => (id: string): Truth => sets[id] ?? leaves.get(id)?.value ?? "unknown";
    const needed = () => {
      const out = new Set<string>();
      for (const s of scenarios) liveLeaves(tree.root, valueIn(s), out);
      return out;
    };

    // 1. Leaves read straight from the facts, and decisions.
    const crossTree: CompiledLeaf[] = [];
    const semantic: CompiledLeaf[] = [];
    for (const leaf of c.leaves.values()) {
      const kind = leaf.node.kind;
      if (kind === "determinate" && isCrossTree(leaf)) crossTree.push(leaf);
      else if (kind === "determinate") leaves.set(leaf.node.id, await this.compute(c, leaf, mode, chain));
      else if (kind === "discretionary") leaves.set(leaf.node.id, this.decide(tree, leaf.node));
      else semantic.push(leaf);
    }
    // 2. Leaves that evaluate other trees, where they can still matter.
    for (const leaf of crossTree) {
      if (needed().has(leaf.node.id)) leaves.set(leaf.node.id, await this.compute(c, leaf, mode, chain));
    }
    // 3. Semantic questions, where they can still matter, asked together.
    const live = needed();
    await Promise.all(
      semantic.filter((l) => live.has(l.node.id)).map(async (l) => leaves.set(l.node.id, await this.ask(tree, l.node))),
    );
    for (const id of c.leaves.keys()) {
      if (!leaves.has(id)) leaves.set(id, { value: "unknown", basis: { by: "not-needed" }, missing: [], references: [] });
    }

    const root = combine(tree.root, valueIn(modeSets));
    const effects: EffectResult[] = [];
    for (const ce of c.effects) {
      const e = ce.effect;
      const r: EffectResult = { id: e.id, kind: e.kind, when: e.when, statement: e.statement, applies: e.when === "holds" ? root : not3(root) };
      for (const k of EFFECT_FORMULAS) {
        const f = ce.formulas[k];
        if (!f) continue;
        const o = outcome(f, await this.formula(c, `${e.id}.${k}`, f, mode, chain), k === "amount" ? "amount" : "date");
        if (o.error !== undefined) this.diagnose(tree.id, `${e.id}.${k}`, o.error);
        r[k as EffectFormula] = o;
      }
      if (e.consequence !== undefined) r.consequence = e.consequence;
      if (e.source !== undefined) r.source = e.source;
      effects.push(r);
    }

    const run: TreeRun = { key, c, leaves, root, effects };
    if (mode === "base") run.result = await this.result(run, valueIn, chain);
    return run;
  }

  private async result(run: TreeRun, valueIn: (s: Record<string, boolean>) => (id: string) => Truth, chain: string[]): Promise<EvaluationResult> {
    const { c, leaves, root, effects } = run;
    const tree = c.tree;
    const leafTraces: Record<string, LeafTrace> = {};
    const trace = (node: Node, path: string): NodeTrace => {
      const value = combine(node, valueIn({}));
      switch (node.type) {
        case "condition": {
          const le = leaves.get(node.id)!;
          const t: LeafTrace = { type: "condition", path, id: node.id, kind: node.kind, statement: node.statement, source: node.source, value, basis: le.basis };
          if (node.contested !== undefined) t.contested = node.contested;
          leafTraces[node.id] = t;
          return t;
        }
        case "all":
        case "any":
          return { type: node.type, path, value, children: node.children.map((ch, i) => trace(ch, `${path}/children/${i}`)) };
        case "not":
          return { type: "not", path, value, child: trace(node.child, `${path}/child`) };
        case "unless":
          return { type: "unless", path, value, rule: trace(node.rule, `${path}/rule`), exception: trace(node.exception, `${path}/exception`) };
      }
    };
    const traced = trace(tree.root, "/root");

    const contested: ContestedResult[] = tree.contested.map((ct) => ({
      issue: ct.issue,
      question: ct.question,
      exposureBranch: ct.exposureBranch,
      branches: ct.branches.map((b) => {
        const sets = b.effect.sets ?? {};
        const r = combine(tree.root, valueIn(sets));
        return {
          id: b.id,
          reading: b.reading,
          statement: b.effect.statement,
          sets,
          exposure: b.id === ct.exposureBranch,
          root: r,
          effects: tree.effects.map((e) => ({ id: e.id, applies: e.when === "holds" ? r : not3(r) })),
        };
      }),
    }));

    let exposure: ExposureResult | null = null;
    if (tree.contested.length) {
      const exp = await this.run(c, "exposure", chain);
      exposure = { root: exp.root, sets: exposureSets(tree), effects: exp.effects };
    }

    return {
      treeId: tree.id,
      title: tree.title,
      decisionPoint: tree.decisionPoint,
      effective: tree.effective,
      eventDate: this.eventDate,
      root,
      trace: traced,
      leaves: leafTraces,
      effects,
      contested,
      exposure,
      investigation: this.investigate(run),
      references: {},
      diagnostics: [],
    };
  }

  /**
   * The unknown leaves that could still change the root. Each is tried true and then false on its
   * own; a leaf that cannot settle the root alone is kept when it is on an open path (see liveLeaves),
   * because it matters together with the other unknowns.
   */
  private investigate(run: TreeRun): InvestigationItem[] {
    const { c, leaves, root } = run;
    if (root !== "unknown") return [];
    const valueOf = (id: string) => leaves.get(id)!.value;
    const live = liveLeaves(c.tree.root, valueOf);
    const items: InvestigationItem[] = [];
    for (const [id, leaf] of c.leaves) {
      const le = leaves.get(id)!;
      if (le.value !== "unknown" || !live.has(id)) continue;
      const ifTrue = combine(c.tree.root, (x) => (x === id ? true : valueOf(x)));
      const ifFalse = combine(c.tree.root, (x) => (x === id ? false : valueOf(x)));
      const node = leaf.node;
      let settle: Settlement;
      if (node.kind === "discretionary") {
        settle = { by: "decision", decision: node.decision! };
        if (node.contested !== undefined) settle.contested = node.contested;
      } else if (node.kind === "semantic") {
        settle = { by: "question", question: node.question!.wording, inputs: node.question!.inputs, missing: le.basis.by === "evidence-missing" ? le.basis.missing : [] };
      } else {
        const via = le.references.flatMap((ref) => {
          const t = this.options.jurisdiction?.select(ref, this.eventDate);
          return t ? (this.done.get(`${versionKey(t)}:base`)?.result?.investigation ?? []) : [];
        });
        settle = { by: "facts", facts: leaf.compute!.analysis.facts, missing: le.missing, via };
        if (le.basis.by === "compute" && le.basis.result.error !== undefined) settle.error = le.basis.result.error;
      }
      items.push({
        treeId: c.tree.id,
        leafId: id,
        kind: node.kind,
        statement: node.statement,
        citation: node.source.citation,
        ifTrue,
        ifFalse,
        decisive: ifTrue !== "unknown" || ifFalse !== "unknown",
        settle,
      });
    }
    return items;
  }
}

/**
 * Evaluates a tree against a case's facts: every node's value with its source, each effect with its
 * amount and dates, every contested branch, the exposure, and the unknowns worth investigating.
 * A tree may be given by id when options carry the jurisdiction and the event date.
 */
export async function evaluate(tree: Tree | string, facts: Facts, options: EvaluateOptions = {}): Promise<EvaluationResult> {
  let t: Tree;
  if (typeof tree === "string") {
    if (!options.jurisdiction || !options.eventDate) throw new Error("evaluating a tree by id needs the jurisdiction and the event date");
    t = options.jurisdiction.tree(tree, options.eventDate);
  } else {
    t = tree;
  }
  const eventDate = options.eventDate ?? t.effective.from;
  if (!inForce(t, eventDate)) throw new Error(`${t.id} (from ${t.effective.from}) is not in force on ${eventDate}`);
  const session = new Session(facts, options, eventDate);
  const run = await session.run(compiled(t), "base", []);
  return { ...run.result!, references: session.references(run.key), diagnostics: session.diagnostics };
}
