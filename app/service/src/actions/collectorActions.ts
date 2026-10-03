import { z } from "zod";
import { BalanceCorrectionContent, BalancePursuitContent } from "../account/pursuit.js";
import type { Collector } from "../adapters/collector.js";
import { getDecision } from "../decisions.js";
import { type ActionSpec, byDecision } from "../gateway.js";
import { caseParties } from "./records.js";

export const PlaceWithCollectorRequest = z.object({ decisionId: z.string() });
export type PlaceWithCollectorRequest = z.infer<typeof PlaceWithCollectorRequest>;

/** Hands a balance to the licensed collector exactly as the operator accepted it: every component, every amount. */
export function placeWithCollector(collector: Collector): ActionSpec<PlaceWithCollectorRequest> {
  return {
    kind: "collector.place",
    description: "Hand a balance to the licensed collector exactly as an accepted balance decision sets it out.",
    request: PlaceWithCollectorRequest,
    key: (req) => req.decisionId,
    authorize: byDecision(["balance.pursuit"], (req) => req.decisionId, (content) => {
      const p = BalancePursuitContent.safeParse(content);
      if (!p.success) return "the decision is not a well-formed balance decision";
      return p.data.route === "collector" && p.data.collector ? null : "the decision does not send the balance to a collector";
    }),
    checks: [
      async (ctx, req) => {
        const c = BalancePursuitContent.parse((await getDecision(ctx.q, req.decisionId))?.content).collector!;
        const sum = c.components.reduce((t, x) => t + x.amountCents, 0);
        if (sum !== c.totalCents) return `the components add to ${sum} cents, not the accepted ${c.totalCents}`;
        const debtor = (await caseParties(ctx.q, ctx.caseId!)).find((p) => p.partyId === c.debtorPartyId);
        return debtor?.relationship === "tenant" ? null : `${c.debtorPartyId} is not a tenant on this tenancy`;
      },
    ],
    async perform(ctx, req, key) {
      const c = BalancePursuitContent.parse((await getDecision(ctx.q, req.decisionId))?.content).collector!;
      const placed = await collector.place({ caseId: ctx.caseId!, debtorPartyId: c.debtorPartyId, creditor: c.creditor, components: c.components }, key);
      return { status: "succeeded", result: { ...placed } };
    },
    async lookup(_ctx, _req, key) {
      const found = await collector.find(key);
      return found ? { status: "succeeded", result: { ...found } } : null;
    },
  };
}

export const AdjustCollectorRequest = z.object({ decisionId: z.string() });
export type AdjustCollectorRequest = z.infer<typeof AdjustCollectorRequest>;

/** Sends an accepted correction to the collector. The account is not resolved until the collector reports it applied. */
export function adjustCollector(collector: Collector): ActionSpec<AdjustCollectorRequest> {
  return {
    kind: "collector.adjust",
    description: "Send an accepted balance correction to the collector.",
    request: AdjustCollectorRequest,
    key: (req) => req.decisionId,
    authorize: byDecision(["balance.correction"], (req) => req.decisionId, (content) =>
      BalanceCorrectionContent.safeParse(content).success ? null : "the decision is not a well-formed correction"),
    async perform(ctx, req, key) {
      const c = BalanceCorrectionContent.parse((await getDecision(ctx.q, req.decisionId))?.content);
      return { status: "succeeded", result: { ...(await collector.adjust(c, key)) } };
    },
    async lookup(_ctx, _req, key) {
      const found = await collector.find(key);
      return found ? { status: "succeeded", result: { ...found } } : null;
    },
  };
}
