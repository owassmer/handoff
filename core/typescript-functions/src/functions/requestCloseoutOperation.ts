import type { Client } from "@osdk/client";
import type { Integer, Long } from "@osdk/functions";
import type { OntologyEdit } from "../deposit_closeout/phase_c/types.js";
import { operateWorkflow } from "../deposit_closeout/lifecycle/adapter.js";

/**
 * Reserve a single approved immutable simulated operation; this does not move money or dispatch.
 * @param client Platform-injected Ontology client.
 * @param caseId Policy-visible native case primary key, loaded server-side.
 * @param actorId Server-bound current user; not editable Action form input.
 * @param commandId Stable command retry ID; reuse for different intent is refused.
 * @param expectedRevision Latest observed case revision as an exact Long string.
 * @param payloadJson Strict REQUEST_OPERATION payload; unknown fields are rejected.
 * @param testDelayMilliseconds Synthetic-only overlap probe (0..3000ms); excluded from immutable intent.
 * @returns One shared root/review/receipt/projection batch, or no edits for an authorized exact replay.
 */
export default async function requestCloseoutOperation(
  client: Client, caseId: string, actorId: string, commandId: string,
  expectedRevision: Long, payloadJson: string, testDelayMilliseconds?: Integer,
): Promise<OntologyEdit[]> {
  return operateWorkflow(client, caseId, actorId, commandId, expectedRevision, "REQUEST_OPERATION", payloadJson, testDelayMilliseconds);
}
