import type { DcCloseoutCase } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import type { Integer, Long } from "@osdk/functions";
import { fingerprint } from "../domain/fingerprints.js";
import type { ReviewRequest } from "../domain/types.js";
import { valid_evidence } from "../domain/validation.js";
import { BOOTSTRAP_ACTOR_ID, CHOOSE_COMMAND, ENVIRONMENT_ID, OPEN_COMMAND, receiptIdFor,
  type CommandIdentity, type OntologyEdit } from "./types.js";
import { findCaseByPk, findReceiptByPk, isReplay, loadCurrentReview } from "./storage.js";
import { emptyProjections, loadProjections } from "./projections.js";
import { observedDelay, persistCase } from "./operations.js";
import { checkedLong, identifier, parseRequest, requireChoiceAuthority,
  requireCondition, requireManagerAccess, requireSupportedChoice, serialize,
  validateChoiceInput, validateRequest, validateRoot } from "./validation.js";

/** Bootstrap only: the Action binds actorId to current user, never form input.
 * The identity and open intent are unchanged from C0; new cases atomically start v1.
 */
export async function openCase(client: Client, requestJson: string, actorId: string,
  commandId: string): Promise<OntologyEdit[]> {
  requireCondition(actorId === BOOTSTRAP_ACTOR_ID, "Only the approved synthetic bootstrap principal may open cases.");
  identifier(commandId, "Command ID");
  const request = parseRequest(requestJson);
  validateRequest(request);
  requireCondition(request.snapshot.revision === 1, "Open a synthetic case at revision 1 only.");
  const { caseId, managementCompanyId } = request.snapshot;
  const intent = { environmentId: ENVIRONMENT_ID, commandKind: OPEN_COMMAND,
    caseId, managementCompanyId, actorId, request };
  const command: CommandIdentity = { caseId, managementCompanyId, actorId, commandId,
    commandKind: OPEN_COMMAND, previousRevision: "0", payloadHash: fingerprint(intent), commandJson: serialize(intent) };
  const [existing, receipt] = await Promise.all([findCaseByPk(client, caseId),
    findReceiptByPk(client, receiptIdFor(managementCompanyId, caseId, commandId))]);
  if (existing !== undefined) {
    const revision = validateRoot(existing);
    requireCondition(existing.readerIds?.includes(actorId) === true, "You do not have access to this case.");
    await loadCurrentReview(client, existing);
    if (isReplay(receipt, command, revision)) return [];
    requireCondition(false, "A case already exists for this ending tenancy; use its guarded actions.");
  }
  requireCondition(receipt === undefined, "A command receipt exists without its case; no bootstrap edits were produced.");
  return persistCase(client, undefined, request, [], command,
    new Date().toISOString(), emptyProjections());
}

function requireFinancialWrite(request: ReviewRequest, actorId: string, itemId: string,
  fullSupportedAmount: number, now: string): void {
  // Discretion over a supported amount includes its waived portion, even for a zero outcome.
  requireChoiceAuthority(request, actorId, fullSupportedAmount, now);
  const item = request.snapshot.charges.find((entry): boolean => entry.itemId === itemId);
  requireCondition(item !== undefined && item.costVersionId !== null
    && item.evidenceIds.includes(item.costVersionId) && valid_evidence(request.snapshot, item.evidenceIds, now),
  "The charge needs accepted, current source evidence before a financial decision.");
}

/** Preserve C0 replay ordering and intent, but carry assignments and every v1 projection. */
export async function chooseCharge(client: Client, closeoutCase: Osdk.Instance<DcCloseoutCase>, actorId: string,
  commandId: string, expectedRevision: Long, itemId: string, chosenAmountCents: Long,
  reason: string, testDelayMilliseconds?: Integer): Promise<OntologyEdit[]> {
  identifier(commandId, "Command ID");
  validateChoiceInput(itemId, reason, testDelayMilliseconds);
  const expected = checkedLong(expectedRevision, "Expected revision", 1n);
  const amount = checkedLong(chosenAmountCents, "Chosen amount");
  const revision = validateRoot(closeoutCase);
  requireManagerAccess(closeoutCase, actorId);
  const stored = await loadCurrentReview(client, closeoutCase);
  requireChoiceAuthority(stored.request, actorId, amount, new Date().toISOString());
  const intent = { environmentId: ENVIRONMENT_ID, commandKind: CHOOSE_COMMAND,
    caseId: closeoutCase.caseId, managementCompanyId: stored.request.snapshot.managementCompanyId,
    actorId, expectedRevision, itemId, chosenAmountCents, reason };
  const command: CommandIdentity = { caseId: closeoutCase.caseId, managementCompanyId: intent.managementCompanyId,
    actorId, commandId, commandKind: CHOOSE_COMMAND, previousRevision: expectedRevision,
    payloadHash: fingerprint(intent), commandJson: serialize(intent) };
  const receipt = await findReceiptByPk(client, receiptIdFor(command.managementCompanyId, command.caseId, commandId));
  if (isReplay(receipt, command, revision)) return [];
  requireCondition(expected === revision, "Case revision changed; reload the case before choosing a charge.");
  requireCondition(revision < Number.MAX_SAFE_INTEGER, "Case revision cannot be incremented exactly.");
  requireSupportedChoice(stored.review, itemId, amount);
  const supported = stored.review.result.itemDecisions.find((entry): boolean => entry.itemId === itemId)?.supportedAmountCents;
  requireCondition(supported !== undefined && supported !== null, "The supported charge amount is missing.");
  requireFinancialWrite(stored.request, actorId, itemId, supported, new Date().toISOString());
  const projections = await loadProjections(client, stored, closeoutCase.projectionVersion);
  await observedDelay(command, revision, testDelayMilliseconds);
  const now = new Date().toISOString();
  requireFinancialWrite(stored.request, actorId, itemId, supported, now);
  const request = structuredClone(stored.request);
  const item = request.snapshot.charges.find((entry): boolean => entry.itemId === itemId);
  requireCondition(item !== undefined, "Charge is not part of the accepted case.");
  item.chosenAmountCents = amount;
  item.choiceState = amount === 0 ? "WAIVED" : "CHOSEN";
  item.reason = reason;
  return persistCase(client, closeoutCase, request, stored.workAssignments,
    command, now, projections, stored);
}
