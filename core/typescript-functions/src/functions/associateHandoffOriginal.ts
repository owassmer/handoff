import type { Client } from "@osdk/client";
import { associateOriginal, type OriginalAssociationEdit } from "../handoff/originals.js";

/** Associate a PDF source with a prepared document. The Action binds currentUserId, never the caller. */
export default async function associateHandoffOriginal(client: Client, handoffId: string, preparedDocumentId: string,
  sourceJson: string, expectedRevision: string, commandId: string, currentUserId: string): Promise<OriginalAssociationEdit[]> {
  return associateOriginal(client, handoffId, preparedDocumentId, sourceJson, expectedRevision, commandId, currentUserId);
}
