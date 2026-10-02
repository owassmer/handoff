import type { Client } from "@osdk/client";
import type { Long } from "@osdk/functions";
import { operateCase } from "../deposit_closeout/phase_c/operations.js";
import type { OntologyEdit } from "../deposit_closeout/phase_c/types.js";

/** Guarded synthetic ADD_EVIDENCE operation; never sends, pays, or executes an account.
 * @param client Platform-injected Ontology client.
 * @param caseId Server-loaded case primary key.
 * @param actorId Action-bound current user; never a user-editable form parameter.
 * @param commandId Stable idempotency key for exactly this intent.
 * @param expectedRevision Observed case revision as a canonical Long string.
 * @param payloadJson Strict ADD_EVIDENCE payload, not a generic JSON patch.
 * @returns One atomic root/review/receipt/projection batch, or no edits for replay.
 */
export default async function addCloseoutEvidence(client: Client, caseId: string, actorId: string,
  commandId: string, expectedRevision: Long, payloadJson: string): Promise<OntologyEdit[]> {
  return operateCase(client, caseId, actorId, commandId, expectedRevision, "ADD_EVIDENCE", payloadJson);
}
