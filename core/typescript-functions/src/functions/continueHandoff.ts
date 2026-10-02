import type { Client } from "@osdk/client";
import type { HandoffEdit } from "../handoff/records.js";
import { coordinateHandoff } from "../handoff/coordinator.js";

/** Resume due work. Use a fresh commandId per turn; business instructions retain their stable identities. */
export default async function continueHandoff(client: Client, handoffId: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  return coordinateHandoff(client, handoffId, commandId, currentUserId);
}
