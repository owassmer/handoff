import { z } from "zod";
import type { Vendors } from "../adapters/vendors.js";
import { type ActionSpec, byDecision } from "../gateway.js";
import { caseWorkItems, updateWorkItem } from "../records.js";
import { WorkPlanContent } from "../work/plan.js";

async function isVendor(ctx: { q: import("../db.js").Queryable }, partyId: string): Promise<string | null> {
  const [p] = await ctx.q.query<{ kind: string }>(`select kind from parties where id = $1`, [partyId]);
  return p?.kind === "organization" ? null : `${partyId} is not a known vendor`;
}

export const RequestQuoteRequest = z.object({
  key: z.string().min(1).max(120),
  vendorPartyId: z.string(),
  scope: z.string().min(1),
});
export type RequestQuoteRequest = z.infer<typeof RequestQuoteRequest>;

/** Asks a vendor for a quote. A quote commits no money, so it needs no decision. */
export function requestQuote(vendors: Vendors): ActionSpec<RequestQuoteRequest> {
  return {
    kind: "vendor.request_quote",
    description: "Ask a vendor for a quote on a scope of work. Commits no money, so it needs no decision.",
    request: RequestQuoteRequest,
    key: (req, caseId) => `${caseId}:${req.key}`,
    authorize: async () => ({ basis: "routine", why: "a quote request commits no money" }),
    checks: [(ctx, req) => isVendor(ctx, req.vendorPartyId)],
    async perform(ctx, req, key) {
      return { status: "succeeded", result: { ...(await vendors.requestQuote({ caseId: ctx.caseId!, vendorPartyId: req.vendorPartyId, scope: req.scope }, key)) } };
    },
    async lookup(_ctx, _req, key) {
      const found = await vendors.find(key);
      return found ? { status: "succeeded", result: { ...found } } : null;
    },
  };
}

export const PlaceVendorOrderRequest = z.object({
  decisionId: z.string(),
  workItemId: z.string(),
  vendorPartyId: z.string(),
  scope: z.string().min(1),
  notToExceedCents: z.number().int().positive(),
});
export type PlaceVendorOrderRequest = z.infer<typeof PlaceVendorOrderRequest>;

/** Orders vendor work the operator accepted in the work plan, within its budget. */
export function placeVendorOrder(vendors: Vendors): ActionSpec<PlaceVendorOrderRequest> {
  return {
    kind: "vendor.place_order",
    description: "Order vendor work the accepted work plan gives to that vendor, with the scope exactly as planned and a not-to-exceed amount within its budget.",
    request: PlaceVendorOrderRequest,
    key: (req) => `${req.decisionId}:${req.workItemId}`,
    authorize: byDecision(["work.plan"], (req) => req.decisionId, (content, req) => {
      const plan = WorkPlanContent.safeParse(content);
      if (!plan.success) return "the decision is not a well-formed work plan";
      const item = plan.data.items.find((i) => i.workItemId === req.workItemId);
      if (!item) return "the plan has no such work";
      if (item.performer !== "vendor" || item.vendorPartyId !== req.vendorPartyId) return "the plan gives this work to someone else";
      if (item.description !== req.scope) return "the scope differs from the plan";
      if (req.notToExceedCents > item.budgetCents) return `the order exceeds the accepted budget of ${item.budgetCents} cents`;
      return null;
    }),
    checks: [
      (ctx, req) => isVendor(ctx, req.vendorPartyId),
      async (ctx, req) => {
        const item = (await caseWorkItems(ctx.q, ctx.caseId!)).find((w) => w.id === req.workItemId);
        if (!item) return `no work item ${req.workItemId} on this case`;
        return item.status === "planned" ? null : `that work is already ${item.status}`;
      },
    ],
    async perform(ctx, req, key) {
      const order = await vendors.placeOrder({ caseId: ctx.caseId!, vendorPartyId: req.vendorPartyId, scope: req.scope, notToExceedCents: req.notToExceedCents }, key);
      return { status: "succeeded", result: { ...order } };
    },
    async lookup(_ctx, _req, key) {
      const found = await vendors.find(key);
      return found ? { status: "succeeded", result: { ...found } } : null;
    },
    async onSucceeded(tx, _ctx, req, result) {
      await updateWorkItem(tx, req.workItemId, { externalRef: String(result.ref), status: "ordered", estimateCents: req.notToExceedCents });
    },
  };
}
