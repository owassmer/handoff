import type { Client } from "@osdk/client";
import type { HandoffEdit } from "../handoff/records.js";
import { receiveNotice } from "../handoff/receiveNotice.js";

/** Receive a move-out notice and its related business records. currentUserId must be bound by the Action. */
export default async function receiveMoveOutNotice(client: Client, workspaceId: string, noticeJson: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  return receiveNotice(client, workspaceId, noticeJson, commandId, currentUserId);
}
