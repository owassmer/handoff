import { z } from "zod";

/** The content of a `balance.pursuit` decision: what to do about a balance the deposit did not cover. */
export const BalancePursuitContent = z.object({
  route: z.enum(["collector", "operator_bill", "write_off"]),
  collector: z.object({
    debtorPartyId: z.string(),
    creditor: z.string(),
    components: z.array(z.object({
      componentId: z.string(),
      description: z.string(),
      amountCents: z.number().int().positive(),
      consumerCredit: z.boolean(),
    })).min(1),
    totalCents: z.number().int().positive(),
  }).optional(),
});
export type BalancePursuitContent = z.infer<typeof BalancePursuitContent>;

/** The content of a `balance.correction` decision: a placed component's corrected amount. */
export const BalanceCorrectionContent = z.object({
  placementRef: z.string(),
  componentId: z.string(),
  amountCents: z.number().int().nonnegative(),
  reason: z.string().min(1),
});
export type BalanceCorrectionContent = z.infer<typeof BalanceCorrectionContent>;
