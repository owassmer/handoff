import type { Client } from "@osdk/client";
import { readWorkspace } from "../deposit_closeout/workspace/read.js";

export const config = { apiName: "getCloseoutWorkspace" };

/**
 * Read one bounded, generation-checked workspace; no edits, reservations or current-actor authorization.
 * @param client Platform-injected client; existing root and snapshot policies govern full-case visibility.
 * @param caseId Policy-visible synthetic case ID. No caller-supplied actor or permission bypass.
 * @param intentSpecJson Optional exact OperationIntentSpec JSON, including every nullable field.
 * @returns Canonical CloseoutWorkspaceV1 JSON, with one effective review and an advisory target preview.
 */
export default async function getCloseoutWorkspace(
  client: Client,
  caseId: string,
  intentSpecJson?: string,
): Promise<string> {
  return readWorkspace(client, caseId, intentSpecJson);
}
