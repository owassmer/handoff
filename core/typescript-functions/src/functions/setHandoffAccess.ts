import type { Client } from "@osdk/client";
import type { HandoffEdit } from "../handoff/records.js";
import { setAccess } from "../handoff/team.js";

/** Grant a person None, Read, Work, Decide or Admin access to a workspace. currentUserId must be bound by the Action. */
export default async function setHandoffAccess(client: Client, workspaceId: string, userId: string, level: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  return setAccess(client, workspaceId, userId, level, commandId, currentUserId);
}
