import type { Client } from "@osdk/client";
import type { Long } from "@osdk/functions";
import type { HandoffEdit } from "../handoff/records.js";
import { acceptPlan } from "../handoff/workPlans.js";

/** Accept the exact scope, budget and requirements being reviewed. currentUserId must be bound by the Action. */
export default async function acceptHandoffWorkPlan(client: Client, workPlanId: string,
  expectedRevision: Long, commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  return acceptPlan(client, workPlanId, expectedRevision, commandId, currentUserId);
}
