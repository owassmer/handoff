import { z } from "zod";
import type { UtilityBiller } from "../adapters/utilities.js";
import type { ActionSpec } from "../gateway.js";
import { caseTenancy } from "./records.js";

export const RequestFinalBillsRequest = z.object({ moveOutOn: z.iso.date() });
export type RequestFinalBillsRequest = z.infer<typeof RequestFinalBillsRequest>;

/** Asks the billing agent for the final reads and bills. Every move-out needs them, and asking commits no money. */
export function requestFinalBills(biller: UtilityBiller): ActionSpec<RequestFinalBillsRequest> {
  return {
    kind: "utility.request_final_bills",
    description: "Ask the utility billing agent for the final meter reads and bills for this move-out. Routine.",
    request: RequestFinalBillsRequest,
    key: (_req, caseId) => `${caseId}`,
    authorize: async () => ({ basis: "routine", why: "every move-out needs its final utility reads; the request commits no money" }),
    async perform(ctx, req, key) {
      const { tenancyId } = await caseTenancy(ctx.q, ctx.caseId!);
      return { status: "succeeded", result: { ...(await biller.requestFinalBills({ caseId: ctx.caseId!, tenancyRef: tenancyId, moveOutOn: req.moveOutOn }, key)) } };
    },
    async lookup(_ctx, _req, key) {
      const found = await biller.findRequest(key);
      return found ? { status: "succeeded", result: { ...found } } : null;
    },
  };
}
