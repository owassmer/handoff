import { z } from "zod";
import { isDate } from "./time.js";

/**
 * The tree format of design/legal-trees.md, with the additions adopted on October 3, 2026: branch
 * effects, contested leaves, discretionary decisions, question basis, effect source, margin and
 * notBefore, cross-tree references and the extra parameter units. Objects are strict, as in the
 * research checker, so a misspelt field fails loading instead of being ignored.
 */

export interface Source {
  citation: string;
  quote: string;
}

export type LeafKind = "determinate" | "semantic" | "discretionary";

export interface Question {
  type: "yesno" | "choice" | "score";
  wording: string;
  options?: string[];
  /** The evidence contract: the question is not asked while any of these is missing. */
  inputs: string[];
  basis?: Source[];
}

export interface Condition {
  type: "condition";
  id: string;
  statement: string;
  source: Source;
  kind: LeafKind;
  compute?: string;
  question?: Question;
  decision?: { by: "agent" | "operator"; what: string };
  contested?: string;
}

export type Node =
  | { type: "all"; children: Node[] }
  | { type: "any"; children: Node[] }
  | { type: "not"; child: Node }
  | { type: "unless"; rule: Node; exception: Node }
  | Condition;

export type ParameterUnit = "calendarDays" | "cents" | "hours" | "date" | "multiplier" | "months";

export interface Parameter {
  id: string;
  value: number | string;
  unit: ParameterUnit;
  source: Source;
}

export interface Effect {
  id: string;
  kind: "permission" | "prohibition" | "duty";
  statement: string;
  when: "holds" | "fails";
  amount?: string;
  due?: string;
  margin?: string;
  notBefore?: string;
  consequence?: string;
  source?: Source;
}

export interface Branch {
  id: string;
  reading: string;
  authority: Source[];
  effect: { statement: string; sets?: Record<string, boolean> };
}

export interface Contested {
  issue: string;
  question: string;
  branches: Branch[];
  exposureBranch: string;
}

export interface Tree {
  id: string;
  title: string;
  decisionPoint: string;
  layer: "US" | "CA" | "CA-OC" | "CA-HB";
  effective: { from: string; to: string | null };
  inputs: string[];
  parameters: Parameter[];
  root: Node;
  effects: Effect[];
  contested: Contested[];
}

const text = z.string().trim().min(1);
const isoDate = z.string().refine(isDate, "must be an ISO date (YYYY-MM-DD)");

export const SourceSchema = z.strictObject({ citation: text, quote: text });

export const QuestionSchema = z
  .strictObject({
    type: z.enum(["yesno", "choice", "score"]),
    wording: text,
    options: z.array(text).optional(),
    inputs: z.array(text).min(1),
    basis: z.array(SourceSchema).optional(),
  })
  .refine((q) => q.type !== "choice" || (q.options?.length ?? 0) >= 2, "a choice question needs at least two options");

const ConditionSchema = z
  .strictObject({
    type: z.literal("condition"),
    id: z.string().regex(/^[a-z0-9][a-z0-9-]*$/, "leaf ids are lower-case kebab"),
    statement: text,
    source: SourceSchema,
    kind: z.enum(["determinate", "semantic", "discretionary"]),
    compute: text.optional(),
    question: QuestionSchema.optional(),
    decision: z.strictObject({ by: z.enum(["agent", "operator"]), what: text }).optional(),
    contested: text.optional(),
  })
  .superRefine((leaf, ctx) => {
    const needs = { determinate: "compute", semantic: "question", discretionary: "decision" } as const;
    for (const [kind, field] of Object.entries(needs)) {
      const has = leaf[field] !== undefined;
      if (leaf.kind === kind && !has) ctx.addIssue({ code: "custom", message: `a ${kind} leaf needs ${field}`, path: [field] });
      if (leaf.kind !== kind && has) ctx.addIssue({ code: "custom", message: `${field} belongs only on a ${kind} leaf`, path: [field] });
    }
  });

export const NodeSchema: z.ZodType<Node> = z.lazy(() =>
  z.discriminatedUnion("type", [
    z.strictObject({ type: z.literal("all"), children: z.array(NodeSchema).min(2) }),
    z.strictObject({ type: z.literal("any"), children: z.array(NodeSchema).min(2) }),
    z.strictObject({ type: z.literal("not"), child: NodeSchema }),
    z.strictObject({ type: z.literal("unless"), rule: NodeSchema, exception: NodeSchema }),
    ConditionSchema,
  ]),
);

export const ParameterSchema = z
  .strictObject({
    id: z.string().regex(/^[A-Za-z][A-Za-z0-9]*$/),
    value: z.union([z.number(), z.string()]),
    unit: z.enum(["calendarDays", "cents", "hours", "date", "multiplier", "months"]),
    source: SourceSchema,
  })
  .superRefine((p, ctx) => {
    const ok =
      p.unit === "date" ? isDate(p.value) : p.unit === "cents" || p.unit === "calendarDays" ? Number.isInteger(p.value) : typeof p.value === "number";
    if (!ok) ctx.addIssue({ code: "custom", message: `value ${JSON.stringify(p.value)} does not fit unit ${p.unit}`, path: ["value"] });
  });

export const EffectSchema = z.strictObject({
  id: text,
  kind: z.enum(["permission", "prohibition", "duty"]),
  statement: text,
  when: z.enum(["holds", "fails"]),
  amount: text.optional(),
  due: text.optional(),
  margin: text.optional(),
  notBefore: text.optional(),
  consequence: text.optional(),
  source: SourceSchema.optional(),
});

export const ContestedSchema = z.strictObject({
  issue: text,
  question: text,
  branches: z
    .array(
      z.strictObject({
        id: text,
        reading: text,
        authority: z.array(SourceSchema).min(1),
        effect: z.strictObject({ statement: text, sets: z.record(z.string(), z.boolean()).optional() }),
      }),
    )
    .min(2),
  exposureBranch: text,
});

export const TreeSchema = z.strictObject({
  id: z.string().regex(/^[A-Z]{2}(-[A-Z]{2})?\.[a-z0-9-]+$/, "tree ids look like CA.deduct-repair"),
  title: text,
  decisionPoint: z.string().regex(/^(DP|PW)\d+(\.\d+)?$/),
  layer: z.enum(["US", "CA", "CA-OC", "CA-HB"]),
  effective: z.strictObject({ from: isoDate, to: isoDate.nullable() }),
  inputs: z.array(text),
  parameters: z.array(ParameterSchema),
  root: NodeSchema,
  effects: z.array(EffectSchema).min(1),
  contested: z.array(ContestedSchema),
}) satisfies z.ZodType<Tree>;
