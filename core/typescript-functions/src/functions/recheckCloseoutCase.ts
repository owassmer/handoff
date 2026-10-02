import type { Client } from "@osdk/client";
import type { Integer, Long } from "@osdk/functions";
import { operateCase } from "../deposit_closeout/phase_c/operations.js";
import type { OntologyEdit } from "../deposit_closeout/phase_c/types.js";

/** Re-evaluate at the actual server clock without mutating financial facts.
 * @param client Platform-injected client.
 * @param caseId Server-loaded synthetic case primary key.
 * @param actorId Action-bound current user; must remain a case reader.
 * @param commandId Stable command ID; exact replay does not advance time again.
 * @param expectedRevision Observed revision as a canonical Long string.
 * @param testDelayMilliseconds Optional synthetic overlap probe, 0..3000 ms.
 * @returns A single guarded batch with a new review, or no edits for replay.
 */
export default async function recheckCloseoutCase(client: Client, caseId: string, actorId: string,
  commandId: string, expectedRevision: Long, testDelayMilliseconds?: Integer): Promise<OntologyEdit[]> {
  return operateCase(client, caseId, actorId, commandId, expectedRevision, "RECHECK", "{}", testDelayMilliseconds);
}
