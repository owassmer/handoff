import { z } from "zod";

/** The content of a `work.plan` decision: who does what to which conditions, and within what budget. */
export const WorkPlanItem = z.object({
  workItemId: z.string(),
  performer: z.enum(["in_house", "vendor"]),
  vendorPartyId: z.string().optional(),
  category: z.enum(["inspection", "paint", "cleaning", "repair", "other"]),
  description: z.string().min(1),
  budgetCents: z.number().int().nonnegative(),
});
export type WorkPlanItem = z.infer<typeof WorkPlanItem>;

export const WorkPlanContent = z.object({
  items: z.array(WorkPlanItem).min(1),
  totalBudgetCents: z.number().int().nonnegative(),
});
export type WorkPlanContent = z.infer<typeof WorkPlanContent>;
