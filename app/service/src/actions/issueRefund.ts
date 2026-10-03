import { z } from "zod";
import { StatementContent, statementProblem } from "../account/statement.js";
import { PaymentDeclined, type Payments } from "../adapters/payments.js";
import { businessDate } from "../clock.js";
import { getDecision } from "../decisions.js";
import { type ActionSpec, byDecision } from "../gateway.js";
import { addEntry } from "../records.js";
import { caseParties } from "./records.js";

export const IssueRefundRequest = z.object({
  /** The accepted account statement that sets the refund. */
  decisionId: z.string(),
  payeePartyId: z.string(),
  amountCents: z.number().int().positive(),
  method: z.enum(["mailed_check", "electronic_transfer"]),
});
export type IssueRefundRequest = z.infer<typeof IssueRefundRequest>;

/** Pays the refund an operator accepted, exactly as accepted, once per decision. */
export function issueRefund(payments: Payments): ActionSpec<IssueRefundRequest> {
  return {
    kind: "payment.refund",
    description: "Pay the deposit refund set by an accepted account statement, to the payee, amount and method in it. Paid once per statement.",
    request: IssueRefundRequest,
    key: (req) => req.decisionId,
    authorize: byDecision(["account.statement"], (req) => req.decisionId, (content, req) => {
      const r = content.refund as Record<string, unknown> | undefined;
      if (!r) return "the statement sets no refund";
      if (r.amountCents !== req.amountCents) return `amount ${req.amountCents} is not the accepted ${String(r.amountCents)}`;
      if (r.payeePartyId !== req.payeePartyId) return "different payee";
      if (r.method !== req.method) return "different payment method";
      return null;
    }),
    checks: [
      async (ctx, req) => {
        if (!ctx.caseId) return "a refund belongs to a case";
        const payee = (await caseParties(ctx.q, ctx.caseId)).find((p) => p.partyId === req.payeePartyId);
        return payee?.relationship === "tenant" ? null : `${req.payeePartyId} is not a tenant on this tenancy`;
      },
      async (ctx, req) => {
        const parsed = StatementContent.safeParse((await getDecision(ctx.q, req.decisionId))?.content);
        if (!parsed.success) return "the accepted statement is not a well-formed statement";
        const problem = statementProblem(parsed.data);
        return problem ? `the accepted statement does not add up: ${problem}` : null;
      },
    ],
    async perform(ctx, req, key) {
      try {
        const receipt = await payments.send(
          { caseId: ctx.caseId, payeePartyId: req.payeePartyId, amountCents: req.amountCents, method: req.method, memo: `Deposit refund, case ${ctx.caseId}` },
          key,
        );
        return { status: "succeeded", result: { ...receipt } };
      } catch (e) {
        if (e instanceof PaymentDeclined) return { status: "failed", reason: `declined: ${e.message}` };
        throw e;
      }
    },
    async lookup(_ctx, _req, key) {
      const receipt = await payments.find(key);
      return receipt ? { status: "succeeded", result: { ...receipt } } : null;
    },
    async onSucceeded(tx, ctx, req, result) {
      await addEntry(tx, {
        caseId: ctx.caseId!,
        kind: "refund_paid",
        lineKey: "refund",
        description: `Deposit refund by ${req.method === "electronic_transfer" ? "electronic transfer" : "mailed check"}`,
        amountCents: req.amountCents,
        effectiveOn: businessDate(ctx.now),
        decisionId: req.decisionId,
        source: "handoff",
        ledgerRef: String(result.paymentId ?? ""),
        recordedAt: ctx.now,
      });
    },
  };
}
