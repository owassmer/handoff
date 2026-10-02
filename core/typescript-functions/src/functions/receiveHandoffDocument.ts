import type { Client } from "@osdk/client";
import type { HandoffEdit } from "../handoff/records.js";
import { receiveDocument } from "../handoff/documentIntake.js";

/** Receive a source version and wake the coordinator. The Action supplies currentUserId. */
export default async function receiveHandoffDocument(client: Client, handoffId: string, documentJson: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  return receiveDocument(client, handoffId, documentJson, commandId, currentUserId);
}
