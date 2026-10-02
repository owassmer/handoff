import type { Client } from "@osdk/client";
import type { Long } from "@osdk/functions";
import type { HandoffEdit } from "../handoff/records.js";
import { changePlan } from "../handoff/workPlans.js";

/** Change the current proposal. Supply exactly one of budgetCents and changesJson. The Action binds currentUserId. */
export default async function changeHandoffWorkPlan(client: Client, workPlanId: string,
  expectedRevision: Long, commandId: string, currentUserId: string, budgetCents?: Long, changesJson?: string): Promise<HandoffEdit[]> {
  return changePlan(client, workPlanId, expectedRevision, budgetCents, commandId, currentUserId, changesJson);
}
