import type { Client } from "@osdk/client";
import type { Long } from "@osdk/functions";
import type { OntologyEdit } from "../deposit_closeout/phase_c/types.js";
import { operateWorkflow } from "../deposit_closeout/lifecycle/adapter.js";

/**
 * Append an approval withdrawal without rewriting its original decision.
 * @param client Platform-injected Ontology client.
 * @param caseId Policy-visible native case primary key, loaded server-side.
 * @param actorId Server-bound current user; not editable Action form input.
 * @param commandId Stable command retry ID; reuse for different intent is refused.
 * @param expectedRevision Latest observed case revision as an exact Long string.
 * @param payloadJson Strict REVOKE_APPROVAL payload; unknown fields are rejected.
 * @returns One shared root/review/receipt/projection batch, or no edits for an authorized exact replay.
 */
export default async function revokeCloseoutApproval(
  client: Client, caseId: string, actorId: string, commandId: string,
  expectedRevision: Long, payloadJson: string,
): Promise<OntologyEdit[]> {
  return operateWorkflow(client, caseId, actorId, commandId, expectedRevision, "REVOKE_APPROVAL", payloadJson);
}
