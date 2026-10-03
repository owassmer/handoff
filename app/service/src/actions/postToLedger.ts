import { z } from "zod";
import { StatementContent } from "../account/statement.js";
import type { Ledger, LedgerCode } from "../adapters/ledger.js";
import { businessDate } from "../clock.js";
import { getDecision } from "../decisions.js";
import { type ActionContext, type ActionSpec, byDecision } from "../gateway.js";
import { NotAllowed } from "../principals.js";
import { addEntry } from "../records.js";
import { caseTenancy } from "./records.js";

/** Names a line of an accepted statement. Its amount and wording come from the decision, never from the request. */
export const PostToLedgerRequest = z.object({ decisionId: z.string(), lineKey: z.string() });
export type PostToLedgerRequest = z.infer<typeof PostToLedgerRequest>;

const CODE = { rent_due: "rent", charge: "charge", credit: "credit" } as const satisfies Record<string, LedgerCode>;

async function acceptedLine(ctx: ActionContext, req: PostToLedgerRequest) {
  const statement = StatementContent.parse((await getDecision(ctx.q, req.decisionId))?.content);
  const line = statement.lines.find((l) => l.lineKey === req.lineKey);
  if (!line) throw new NotAllowed(`the statement has no line ${req.lineKey}`);
  return line;
}

export function postToLedger(ledger: Ledger): ActionSpec<PostToLedgerRequest> {
  return {
    kind: "ledger.post",
    description: "Post one line of an accepted account statement to the property-management ledger. The amount and wording come from the statement.",
    request: PostToLedgerRequest,
    key: (req) => `${req.decisionId}:${req.lineKey}`,
    authorize: byDecision(["account.statement"], (req) => req.decisionId, (content, req) => {
      const parsed = StatementContent.safeParse(content);
      if (!parsed.success) return "the decision is not a well-formed statement";
      return parsed.data.lines.some((l) => l.lineKey === req.lineKey) ? null : `the statement has no line ${req.lineKey}`;
    }),
    async perform(ctx, req, key) {
      const line = await acceptedLine(ctx, req);
      const { tenancyId } = await caseTenancy(ctx.q, ctx.caseId!);
      const posted = await ledger.post(
        { tenancyRef: tenancyId, postedOn: businessDate(ctx.now), code: CODE[line.kind], description: line.description,
          amountCents: line.kind === "credit" ? -line.amountCents : line.amountCents },
        key,
      );
      return { status: "succeeded", result: { ...posted } };
    },
    async lookup(_ctx, _req, key) {
      const found = await ledger.find(key);
      return found ? { status: "succeeded", result: { ...found } } : null;
    },
    async onSucceeded(tx, ctx, req, result) {
      const line = await acceptedLine({ ...ctx, q: tx }, req);
      await addEntry(tx, {
        caseId: ctx.caseId!, kind: line.kind, lineKey: line.lineKey, description: line.description, amountCents: line.amountCents,
        effectiveOn: businessDate(ctx.now), conditionId: line.conditionId, workItemId: line.workItemId, rule: line.rule,
        documentIds: line.documentIds, decisionId: req.decisionId, source: "handoff", ledgerRef: String(result.ref), recordedAt: ctx.now,
      });
    },
  };
}
