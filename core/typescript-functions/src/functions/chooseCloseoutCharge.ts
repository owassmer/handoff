import { DcCloseoutCase } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import type { Integer, Long } from "@osdk/functions";
import { chooseCharge } from "../deposit_closeout/phase_c/commands.js";
import type { OntologyEdit } from "../deposit_closeout/phase_c/types.js";
import { identifier } from "../deposit_closeout/phase_c/validation.js";

/**
 * Choose or waive an already supported tenant charge; never approve, send or pay.
 * @param client Platform-injected Ontology client.
 * @param caseId Case primary key; the policy-visible root is loaded server-side and retained in the update.
 * @param actorId Server-bound current user, checked against root access and accepted authority.
 * @param commandId Stable command ID; different intent under the same ID is refused.
 * @param expectedRevision Observed revision as an exact Long string, not a locking guarantee.
 * @param itemId Accepted stable charge item ID.
 * @param chosenAmountCents Exact nonnegative Long string, bounded by accepted cost/allowance/authority.
 * @param reason Non-empty reason, at most 2000 UTF-8 bytes.
 * @param testDelayMilliseconds Synthetic-only overlap probe, 0..3000 ms after reads/validation.
 * @returns One batch of root/review/receipt/projection edits, or no edits for a valid retry.
 */
export default async function chooseCloseoutCharge(
  client: Client, caseId: string, actorId: string,
  commandId: string, expectedRevision: Long, itemId: string, chosenAmountCents: Long,
  reason: string, testDelayMilliseconds?: Integer,
): Promise<OntologyEdit[]> {
  identifier(caseId, "Case ID");
  // Required read: not-found and access failures propagate; no caller root or PK-only update.
  const closeoutCase = await client(DcCloseoutCase).fetchOne(caseId);
  return chooseCharge(client, closeoutCase, actorId, commandId, expectedRevision,
    itemId, chosenAmountCents, reason, testDelayMilliseconds);
}
