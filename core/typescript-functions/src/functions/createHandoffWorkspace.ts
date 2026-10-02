import type { Client } from "@osdk/client";
import type { HandoffEdit } from "../handoff/records.js";
import { openWorkspace } from "../handoff/receiveNotice.js";

/** Open a workspace for the signed-in person. currentUserId must be bound by the Action. */
export default async function createHandoffWorkspace(client: Client, name: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  return openWorkspace(client, name, commandId, currentUserId);
}
