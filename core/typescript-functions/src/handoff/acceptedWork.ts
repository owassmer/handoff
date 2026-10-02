import { HandoffDecision, HandoffJob, HandoffWorkPlan } from "@ontology/sdk";
import { inWorkspace, one } from "./records.js";
import { acceptedContent, planDraft } from "./workPlans.js";
import { recognizedWorkRequest } from "./delivery.js";
import { requestWorkCorrespondence } from "./correspondence.js";
import { deliveryAccess, jobScope, offerFromRecord, type DeliveryContext, type DeliveryRecords } from "./deliveryRecords.js";
import type { HandoffDetails } from "./workDetails.js";
import { preparation, sourceDetails } from "./sourceAccess.js";
import { instant } from "./deliveryContracts.js";
import { details, digest, entries, orderedJson, reference, requireHandoff, wordList, words } from "./values.js";

/** A quote charge is counted once even when it supports several accepted prose deliverables. */
export function mappedAcceptedScopes(value: unknown): string[] {
  const row = details(value, ["quoteLineId", "reason", "sourcePassage"], ["acceptedScope", "acceptedScopes"], "Accepted scope mapping");
  requireHandoff((row.acceptedScope === undefined) !== (row.acceptedScopes === undefined), "Supply acceptedScopes or the legacy acceptedScope, not both.");
  const terms = row.acceptedScopes === undefined ? [words(row.acceptedScope, "Accepted scope", 1000)]
    : wordList(row.acceptedScopes, "Accepted scopes", 48, 1, 1000);
  requireHandoff(new Set(terms).size === terms.length, "Do not repeat an accepted term within a quote line.");
  return terms;
}

/** Recognize an actual saved Handoff instruction, never place a new order or amend its acceptance. */
export async function recognizeAcceptedWork(context: DeliveryContext, world: HandoffDetails, records: DeliveryRecords): Promise<boolean> {
  const mapping = world.documents.find((doc) => doc.kind === "Accepted work mapping" && doc.detailsJson);
  if (!mapping) return false;
  preparation(mapping);
  const input = details(sourceDetails(mapping.detailsJson!), ["decisionId", "quoteDocumentId", "scope"], ["fundingId"], "Accepted work mapping");
  const decisionId = words(input.decisionId, "Decision", 160), quoteDocumentId = words(input.quoteDocumentId, "Accepted quote", 160);
  const decision = await one(context.client(HandoffDecision).where({ decisionId: { $eq: decisionId } }));
  requireHandoff(decision?.workPlanId && decision.handoffId === context.handoff.handoffId, "The earlier work needs its original decision.");
  inWorkspace(decision, context.workspace, context.caller);
  const plan = await one(context.client(HandoffWorkPlan).where({ workPlanId: { $eq: decision.workPlanId } }));
  requireHandoff(plan && plan.status === "Accepted" && !plan.selectionJson && plan.acceptedDecisionId === decisionId
    && plan.revision === decision.acceptedRevision && decision.contentJson === acceptedContent(plan),
  "Recognize only the unchanged original acceptance; do not create a replacement decision.");
  inWorkspace(plan, context.workspace, context.caller);
  const source = world.documents.find((doc) => doc.documentId === quoteDocumentId);
  requireHandoff(source && source.kind === "Quote" && plan.sourceDocumentIds?.includes(source.documentId), "Use the quote that supported the original acceptance.");
  const quote = records.quotes.find((row) => row.sourceDocumentId === quoteDocumentId);
  if (!quote) return false; // Source normalization is committed in its own turn.
  const offer = offerFromRecord(quote), draft = planDraft(plan), provider = world.parties.find((party) => party.partyId === offer.providerPartyId);
  requireHandoff(provider && provider.partyId === draft.providerPartyId && source.partyId === provider.partyId
    && ["Assessment", "Verification"].includes(offer.kind), "This recognition is limited to the originally requested assessment or check, not repairs.");
  const correspondence = requestWorkCorrespondence(context.workspace.mode!, `continue:${decisionId}`, provider, draft);
  const request = recognizedWorkRequest(records.messages, context.workspace.workspaceId, context.handoff.handoffId,
    plan.workPlanId, decisionId, provider.partyId, correspondence.body, correspondence.replyBody);
  requireHandoff(request?.externalReference, "The original instruction and matching acknowledgment must already be saved.");
  if (input.fundingId !== undefined) words(input.fundingId, "Owner funds", 160);
  const mapped = entries(input.scope, "Accepted scope mapping", 48, 1).map((value) => {
    const row = details(value, ["quoteLineId", "reason", "sourcePassage"], ["acceptedScope", "acceptedScopes"], "Accepted scope mapping");
    const line = offer.lines.find((item) => item.lineId === row.quoteLineId);
    const acceptedScopes = mappedAcceptedScopes(value), passage = words(row.sourcePassage, "Source passage", 4000);
    requireHandoff(line && acceptedScopes.every((term) => draft.scope.includes(term)) && source.text?.includes(passage),
      "The scope mapping needs the actual accepted work and its quoted evidence.");
    words(row.reason, "Scope explanation", 1500);
    return { line, acceptedScopes };
  });
  const scope = mapped.map(({ line, acceptedScopes }) => ({ ...line, acceptedScope: acceptedScopes.join("\n") }));
  requireHandoff(new Set(scope.map((line) => line.lineId)).size === scope.length && scope.length === offer.lines.length
    && draft.scope.every((item) => mapped.some((line) => line.acceptedScopes.includes(item)))
    && offer.totalCents === draft.estimatedCostCents && offer.currency === draft.currency
    && BigInt(offer.totalCents) <= BigInt(draft.budgetCents)
    && draft.fixedRequirements.every((requirement) => offer.requirements.includes(requirement)),
  "Recognition must cover the same whole assessment, cost and requirements without additions.");
  requireHandoff(orderedJson(scope).length <= 100000, "The accepted scope mapping exceeds the bounded job record.");
  const instructionKey = request.externalReference, jobId = reference("job", context.workspace.workspaceId, instructionKey);
  const instructionHash = digest({ decisionId, content: decision.contentJson, requestId: request.messageId, quoteId: quote.quoteId, scope, fundingId: input.fundingId });
  const prior = records.jobs.find((job) => job.jobId === jobId || job.requestMessageId === request.messageId);
  if (prior) {
    requireHandoff(prior.jobId === jobId && prior.instructionHash === instructionHash && prior.decisionId === decisionId,
      "The original instruction already has different recorded work. Resolve it without another order.");
    return false;
  }
  requireHandoff(!records.jobs.some((job) => job.quoteId === quote.quoteId && jobScope(job).some((line) => scope.some((item) => item.lineId === line.lineId))),
    "This quoted work is already recorded. Continue the original job.");
  // Recognition records an already-issued instruction, not a new spend. Funding is bound in a later
  // committed turn with current coverage; unknown cash must neither erase history nor become zero.
  const shared = deliveryAccess(context);
  context.batch.create(HandoffJob, { ...shared, jobId, title: offer.title, providerPartyId: provider.partyId,
    workPlanId: plan.workPlanId, decisionId, quoteId: quote.quoteId,
    origin: "Handoff", kind: offer.kind, status: "Commissioned", scopeJson: orderedJson(scope), requirements: draft.fixedRequirements,
    currency: offer.currency, committedCents: offer.totalCents, depositCents: offer.depositCents, instructionKey, instructionHash,
    requestMessageId: request.messageId,
    sourceSystem: "Accepted Handoff correspondence", sourceRecordId: request.messageId, sourceDocumentId: mapping.documentId,
    progressSummary: "The original accepted work request is awaiting scheduling confirmation.", revision: "1",
    createdAt: instant(request.createdAt), updatedAt: context.now });
  // No new Message, Decision or WorkPlan edit: original intent and issued correspondence remain exact.
  return true;
}
