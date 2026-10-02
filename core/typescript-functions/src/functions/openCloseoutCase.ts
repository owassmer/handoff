import type { Client } from "@osdk/client";
import { openCase } from "../deposit_closeout/phase_c/commands.js";
import type { OntologyEdit } from "../deposit_closeout/phase_c/types.js";

/**
 * Open a constructed C0 case, returning one edit batch for its guarded Action.
 * @param client Platform-injected Ontology client.
 * @param requestJson Strict ReviewRequest with deterministic case ID and explicit release.
 * @param actorId Must be server-bound to current user by the guarded bootstrap Action.
 * @param commandId Stable caller command ID, reused verbatim for retries.
 * @returns Case, immutable review, receipt and charge projection edits; replay returns no edits.
 */
export default async function openCloseoutCase(
  client: Client, requestJson: string, actorId: string, commandId: string,
): Promise<OntologyEdit[]> {
  return openCase(client, requestJson, actorId, commandId);
}
