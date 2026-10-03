import { readFile, readdir } from "node:fs/promises";
import { join } from "node:path";
import { TreeValidationError, compileTree, remember } from "./compile.js";
import { type Tree, TreeSchema } from "./schema.js";
import { isDate } from "./time.js";

/** Whether a tree version is in force on a date. A null `to` is open-ended; `to` is the last day. */
export function inForce(tree: Tree, date: string): boolean {
  return tree.effective.from <= date && (tree.effective.to === null || date <= tree.effective.to);
}

/** The trees of one jurisdiction, every version of each, validated and cross-checked. */
export class Jurisdiction {
  private readonly byId = new Map<string, Tree[]>();

  constructor(trees: readonly Tree[]) {
    for (const t of trees) {
      const list = this.byId.get(t.id) ?? [];
      list.push(t);
      this.byId.set(t.id, list);
    }
    for (const list of this.byId.values()) list.sort((a, b) => a.effective.from.localeCompare(b.effective.from));
  }

  get trees(): Tree[] {
    return [...this.byId.values()].flat();
  }

  ids(): string[] {
    return [...this.byId.keys()].sort();
  }

  has(id: string): boolean {
    return this.byId.has(id);
  }

  versions(id: string): readonly Tree[] {
    return this.byId.get(id) ?? [];
  }

  /** The version of a tree in force on an event date, if any. */
  select(id: string, eventDate: string): Tree | undefined {
    if (!isDate(eventDate)) throw new Error(`event date must be an ISO date, got ${JSON.stringify(eventDate)}`);
    return this.versions(id).find((t) => inForce(t, eventDate));
  }

  /** Like select, but throws when no version is in force. */
  tree(id: string, eventDate: string): Tree {
    const t = this.select(id, eventDate);
    if (!t) throw new Error(this.has(id) ? `no version of ${id} is in force on ${eventDate}` : `no tree ${id}`);
    return t;
  }
}

/**
 * Validates trees given as parsed JSON and builds their jurisdiction. Every problem across every tree
 * is collected before throwing, so one load reports them all.
 */
export function buildJurisdiction(files: readonly { name: string; json: unknown }[]): Jurisdiction {
  const problems: string[] = [];
  const trees: Tree[] = [];
  const compiledTrees = [];
  for (const { name, json } of files) {
    const parsed = TreeSchema.safeParse(json);
    if (!parsed.success) {
      for (const issue of parsed.error.issues) problems.push(`${name}: ${issue.path.join(".") || "(top)"}: ${issue.message}`);
      continue;
    }
    const tree = parsed.data as Tree;
    const { compiled, problems: own } = compileTree(tree);
    problems.push(...own.map((p) => `${name}: ${p}`));
    trees.push(tree);
    compiledTrees.push({ name, compiled });
  }

  const jur = new Jurisdiction(trees);
  for (const id of jur.ids()) {
    const versions = jur.versions(id);
    for (let i = 1; i < versions.length; i++) {
      const prev = versions[i - 1]!;
      const cur = versions[i]!;
      if (prev.effective.to === null || prev.effective.to >= cur.effective.from) {
        problems.push(`${id}: versions from ${prev.effective.from} and ${cur.effective.from} overlap`);
      }
    }
  }

  // Cross-references: holds() and amount() targets, amount effects and consequences.
  for (const { name, compiled } of compiledTrees) {
    for (const target of compiled.holds) {
      if (!jur.has(target)) problems.push(`${name}: holds("${target}") names no tree`);
    }
    for (const { tree, effect } of compiled.amounts) {
      if (!jur.has(tree)) problems.push(`${name}: amount("${tree}", "${effect}") names no tree`);
      else if (jur.versions(tree).some((v) => !v.effects.some((e) => e.id === effect && e.amount !== undefined))) {
        problems.push(`${name}: amount("${tree}", "${effect}") names no effect with an amount`);
      }
    }
    for (const e of compiled.tree.effects) {
      if (e.consequence !== undefined && !jur.has(e.consequence)) problems.push(`${name}: effect ${e.id} has consequence ${e.consequence}, which names no tree`);
    }
  }

  if (problems.length) throw new TreeValidationError(problems);
  for (const { compiled } of compiledTrees) remember(compiled);
  return jur;
}

export interface LoadOptions {
  /** File names in the folder that are not trees. Defaults to the research folder's JEV_CHECK.json. */
  exclude?: string[];
}

/** Loads and validates every tree (*.json) in a folder. */
export async function loadJurisdiction(dir: string, options: LoadOptions = {}): Promise<Jurisdiction> {
  const exclude = new Set(options.exclude ?? ["JEV_CHECK.json"]);
  const names = (await readdir(dir)).filter((n) => n.endsWith(".json") && !exclude.has(n)).sort();
  const files = [];
  for (const name of names) {
    const raw = await readFile(join(dir, name), "utf8");
    let json: unknown;
    try {
      json = JSON.parse(raw);
    } catch (err) {
      throw new TreeValidationError([`${name}: invalid JSON (${(err as Error).message})`]);
    }
    files.push({ name, json });
  }
  return buildJurisdiction(files);
}
