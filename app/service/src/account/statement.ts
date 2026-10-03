import { z } from "zod";

/** One line of the itemized statement. Amounts are positive; the kind says which way they go. */
export const StatementLine = z.object({
  lineKey: z.string().min(1),
  kind: z.enum(["rent_due", "charge", "credit"]),
  description: z.string().min(1),
  amountCents: z.number().int().positive(),
  /** The tree and effect the line rests on, e.g. "CA.deduct-repair#may-deduct". */
  rule: z.string().optional(),
  conditionId: z.string().optional(),
  workItemId: z.string().optional(),
  documentIds: z.array(z.string()).default([]),
  /** A good-faith estimate under 1950.5(h)(3), to be completed when the invoice arrives. */
  estimate: z.boolean().default(false),
});
export type StatementLine = z.infer<typeof StatementLine>;

/** The content of an `account.statement` decision: what the operator reviews and accepts. */
export const StatementContent = z.object({
  depositCents: z.number().int().nonnegative(),
  lines: z.array(StatementLine),
  refund: z.object({
    payeePartyId: z.string(),
    amountCents: z.number().int().positive(),
    method: z.enum(["mailed_check", "electronic_transfer"]),
  }).optional(),
  balanceDue: z.object({
    amountCents: z.number().int().positive(),
    dueOn: z.iso.date(),
  }).optional(),
  message: z.object({ toPartyId: z.string(), subject: z.string(), body: z.string() }),
});
export type StatementContent = z.infer<typeof StatementContent>;

/** What the deposit leaves after the lines: above zero is owed back to the tenant, below zero is owed by them. */
export function remainderCents(s: StatementContent): number {
  return s.lines.reduce((left, l) => left + (l.kind === "credit" ? l.amountCents : -l.amountCents), s.depositCents);
}

/** A reason the statement does not add up, or null. */
export function statementProblem(s: StatementContent): string | null {
  const keys = new Set<string>();
  for (const l of s.lines) {
    if (keys.has(l.lineKey)) return `line ${l.lineKey} appears twice`;
    keys.add(l.lineKey);
  }
  const left = remainderCents(s);
  if (left > 0 && s.refund?.amountCents !== left) return `the refund must be ${left} cents, the deposit less the lines`;
  if (left < 0 && s.balanceDue?.amountCents !== -left) return `the balance due must be ${-left} cents, the lines less the deposit`;
  if (left <= 0 && s.refund) return "there is nothing left to refund";
  if (left >= 0 && s.balanceDue) return "there is no balance due";
  return null;
}
