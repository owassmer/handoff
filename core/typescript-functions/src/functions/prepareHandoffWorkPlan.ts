import type { Client } from "@osdk/client";
import type { HandoffEdit } from "../handoff/records.js";
import { preparePlan } from "../handoff/workPlans.js";

/** Read the handoff's evidence and propose its work. currentUserId must be bound by the Action. */
export default async function prepareHandoffWorkPlan(client: Client, handoffId: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  return preparePlan(client, handoffId, commandId, currentUserId);
}
