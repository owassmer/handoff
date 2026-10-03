import { z } from "zod";
import type { Maintenance } from "../adapters/maintenance.js";
import { type ActionSpec, byDecision, byStanding, eitherOf } from "../gateway.js";
import { caseWorkItems, updateWorkItem } from "../records.js";
import { WorkPlanContent } from "../work/plan.js";
import { caseTenancy } from "./records.js";

export const CreateWorkOrderRequest = z.object({
  /** The agent's name for this order within the case. Asking again under it does nothing. */
  key: z.string().min(1).max(120),
  category: z.enum(["inspection", "paint", "cleaning", "repair", "other"]),
  description: z.string().min(1),
  /** The planned work this order carries out, under an accepted work plan. */
  workItemId: z.string().optional(),
  decisionId: z.string().optional(),
});
export type CreateWorkOrderRequest = z.infer<typeof CreateWorkOrderRequest>;

/** Orders in-house work: planned work under an accepted plan, or routine work a standing instruction allows. */
export function createWorkOrder(maintenance: Maintenance): ActionSpec<CreateWorkOrderRequest> {
  return {
    kind: "maintenance.create_work_order",
    request: CreateWorkOrderRequest,
    key: (req, caseId) => `${caseId}:${req.key}`,
    authorize: eitherOf(
      byDecision(["work.plan"], (req) => req.decisionId, (content, req) => {
        const plan = WorkPlanContent.safeParse(content);
        if (!plan.success) return "the decision is not a well-formed work plan";
        const item = plan.data.items.find((i) => i.workItemId === req.workItemId);
        if (!item) return "the plan has no such work";
        if (item.performer !== "in_house") return "the plan gives this work to a vendor";
        if (item.category !== req.category) return `the plan lists this as ${item.category}`;
        if (item.description !== req.description) return "the scope differs from the plan";
        return null;
      }),
      byStanding("standing.routine-work", (content, req) => {
        if (req.workItemId) return "planned work needs the accepted plan";
        const categories = (content.categories as string[] | undefined) ?? [];
        return categories.includes(req.category) ? null : `${req.category} is not routine work`;
      }),
    ),
    checks: [
      async (ctx, req) => {
        if (!req.workItemId) return null;
        const item = (await caseWorkItems(ctx.q, ctx.caseId!)).find((w) => w.id === req.workItemId);
        if (!item) return `no work item ${req.workItemId} on this case`;
        if (item.performer !== "in_house") return "that work is for a vendor";
        return item.status === "planned" ? null : `that work is already ${item.status}`;
      },
    ],
    async perform(ctx, req, key) {
      const { unitId } = await caseTenancy(ctx.q, ctx.caseId!);
      const order = await maintenance.createWorkOrder({ caseId: ctx.caseId!, unitRef: unitId, category: req.category, description: req.description }, key);
      return { status: "succeeded", result: { ...order } };
    },
    async lookup(_ctx, _req, key) {
      const order = await maintenance.find(key);
      return order ? { status: "succeeded", result: { ...order } } : null;
    },
    async onSucceeded(tx, _ctx, req, result) {
      if (!req.workItemId) return;
      await updateWorkItem(tx, req.workItemId, {
        externalRef: String(result.ref), status: "scheduled",
        scheduledFor: result.scheduledFor ? new Date(String(result.scheduledFor)) : undefined,
      });
    },
  };
}
