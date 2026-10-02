import type { Client } from "@osdk/client";
import type { Long } from "@osdk/functions";
import type { HandoffEdit } from "../handoff/records.js";
import { discussHandoff } from "../handoff/conversation.js";

/** Save a message for the shared coordinator. The Action supplies the actual currentUserId. */
export default async function sendHandoffMessage(client: Client, handoffId: string, message: string,
  commandId: string, currentUserId: string, expectedPlanRevision?: Long): Promise<HandoffEdit[]> {
  return discussHandoff(client, handoffId, message, commandId, currentUserId, expectedPlanRevision);
}
