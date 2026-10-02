import { HandoffJob, HandoffDecision, HandoffInspection, HandoffObligation, HandoffParty, HandoffMessage } from "@ontology/sdk";
import type { Osdk } from "@osdk/client";
import { inWorkspace, loadPlan, one } from "./records.js";
import { loadDetails } from "./workDetails.js";
import { materialBasis, planSelections, validateSelection } from "./proposal.js";
import { acceptedContent, planDraft } from "./workPlans.js";
import { requestWorkCorrespondence } from "./correspondence.js";
import { details, digest, entries, nextRevision, orderedJson, reference, requireHandoff, whole, words } from "./values.js";
import { afterMinutes, findings, formatAmount, instant, money, type CommissionInput, type WorkMandate } from "./deliveryContracts.js";
import { bullets, letter } from "./email.js";
import { deliveryAccess, deliveryJob, deliveryQuote, jobScope, loadDeliveryRecords, offerFromRecord,
  requireDeliverySource, requireSavedFinancialState, touchDelivery, type DeliveryContext, type Inspection, type Job } from "./deliveryRecords.js";
import { priceCommission } from "./quoteCosts.js";
import { loadOwnerFunding } from "./funding.js";

/** Finds the original request/receipt pair. Merely having a similar message body is insufficient. */
export function recognizedWorkRequest(messages: readonly Osdk.Instance<HandoffMessage>[], workspaceId: string,
  handoffId: string, workPlanId: string, decisionId: string, providerId: string,
  expectedBody: string, expectedAcknowledgment: string): Osdk.Instance<HandoffMessage> | undefined {
  const operation = `continue:${decisionId}`, requestId = reference("message", workspaceId, operation, "request"),
    replyId = reference("message", workspaceId, operation, "acknowledgement"),
    externalReference = reference("correspondence", providerId, operation);
  const request = messages.find((message) => message.messageId === requestId), reply = messages.find((message) => message.messageId === replyId);
  if (!request && !reply) return undefined;
  requireHandoff(request && reply, "Check the earlier work request and acknowledgment before continuing.");
  [request, reply].forEach((message) => requireHandoff(message.workspaceId === workspaceId && message.handoffId === handoffId
    && message.workPlanId === workPlanId && message.recipientPartyId === providerId && message.externalReference === externalReference,
  "The earlier correspondence belongs to different work."));
  requireHandoff(request.direction === "Outgoing" && request.status === "Sent" && request.body === expectedBody
    && reply.direction === "Incoming" && reply.status === "Received" && reply.body === expectedAcknowledgment,
  "The earlier work correspondence needs to be checked.");
  return request;
}

/**
 * Admit one provider commitment against saved acceptance and source costs. The batch must be committed
 * before respondToProviderRequest is invoked. No callback here claims to perform work or transfer money.
 */
export async function commissionJob(context: DeliveryContext, rawInput: CommissionInput): Promise<string> {
  const shared = deliveryAccess(context);
  requireSavedFinancialState(context);
  requireHandoff(context.handoff.status === "Open", "Resume the handoff before making a new commitment.");
  const row = details(rawInput, ["workPlanId", "expectedRevision", "quoteId", "fundingId", "scope"], ["obligationId"], "Work instruction");
  const input: CommissionInput = { workPlanId: words(row.workPlanId, "Work plan", 160), expectedRevision: whole(row.expectedRevision, "Plan version"),
    quoteId: words(row.quoteId, "Quote", 160), fundingId: words(row.fundingId, "Owner funds", 160),
    scope: entries(row.scope, "Work selection", 48, 1).map((entry) => {
      const line = details(entry, ["quoteLineId", "acceptedScope"], [], "Work selection");
      return { quoteLineId: words(line.quoteLineId, "Quoted line", 160), acceptedScope: words(line.acceptedScope, "Accepted scope", 1000) };
    }), ...(row.obligationId === undefined ? {} : { obligationId: words(row.obligationId, "Obligation", 160) }) };
  const { plan, workspace, handoff } = await loadPlan(context.client, input.workPlanId, context.caller, "work", false);
  requireHandoff(workspace.workspaceId === shared.workspaceId && handoff.handoffId === shared.handoffId
    && handoff.status === "Open" && handoff.propertyId === shared.propertyId
    && plan.revision === input.expectedRevision && plan.status === "Accepted" && plan.acceptedDecisionId
    && (!handoff.operativeDecisionId || handoff.operativeDecisionId === plan.acceptedDecisionId),
  "Review the current accepted work before commissioning.");
  inWorkspace(context.handoff, workspace, context.caller);
  context = { ...context, workspace, handoff };
  const [decision, quote, records, funded] = await Promise.all([
    one(context.client(HandoffDecision).where({ decisionId: { $eq: plan.acceptedDecisionId } })),
    deliveryQuote(context, input.quoteId), loadDeliveryRecords(context.client, workspace, context.caller, handoff),
    loadOwnerFunding(context, input.fundingId),
  ]);
  requireHandoff(decision, "The work acceptance is not available."); inWorkspace(decision, workspace, context.caller);
  requireHandoff(decision.handoffId === handoff.handoffId && decision.workPlanId === plan.workPlanId
    && decision.acceptedRevision === plan.revision && decision.contentJson === acceptedContent(plan),
  "The work no longer matches its accepted decision.");
  const offer = offerFromRecord(quote), draft = planDraft(plan);
  if (plan.selectionJson) validateSelection({ ...draft, selections: planSelections(plan), fixedProviderPartyId: plan.fixedProviderPartyId }, records.quotes);
  const world = await loadDetails(context.client, handoff, workspace, context.caller);
  if (plan.sourceBasis && !records.jobs.some((job) => job.decisionId === decision.decisionId)) requireHandoff(plan.sourceBasis === materialBasis(handoff, workspace, world),
    "The facts supporting the accepted work changed before commissioning. Reconsider the work before sending an order.");
  const quoteDocument = world.documents.find((doc) => doc.documentId === offer.sourceDocumentId);
  if (quoteDocument?.detailsJson) {
    const mapping = JSON.parse(quoteDocument.detailsJson) as Record<string, unknown>;
    if (typeof mapping.providerDocumentId === "string") {
      const providerSource = world.documents.find((doc) => doc.documentId === mapping.providerDocumentId);
      requireHandoff(providerSource && (providerSource.sourceVersion ?? digest(providerSource.detailsJson)) === mapping.providerSourceVersion,
        "The provider terms changed after the offer. Obtain a current offer before commissioning.");
    }
  }
  await requireDeliverySource(context, offer.sourceDocumentId, [offer.providerPartyId]);
  if (input.obligationId) {
    const duty = await one(context.client(HandoffObligation).where({ obligationId: { $eq: input.obligationId } }));
    requireHandoff(duty && duty.handoffId === handoff.handoffId, "The obligation is not part of this handoff.");
    inWorkspace(duty, workspace, context.caller);
  }
  const mandate: WorkMandate = { decisionId: decision.decisionId, workPlanId: plan.workPlanId, revision: plan.revision!,
    propertyId: shared.propertyId, currency: draft.currency, budgetCents: draft.budgetCents, scope: draft.scope,
    requirements: draft.fixedRequirements, sourceDocumentIds: draft.sourceDocumentIds, fixedProviderPartyId: plan.fixedProviderPartyId,
    ...(plan.selectionJson ? { reviewedSelections: planSelections(plan), quoteId: quote.quoteId } : {}) };
  const instructionKey = reference("work-instruction", shared.workspaceId, handoff.handoffId, quote.quoteId, ...input.scope.map((line) => line.quoteLineId).sort());
  const jobId = reference("job", shared.workspaceId, instructionKey);
  const instructionHash = digest({ mandate, quote: offer, fundingId: input.fundingId,
    scope: [...input.scope].sort((a, b) => a.quoteLineId.localeCompare(b.quoteLineId)), obligationId: input.obligationId });
  const prior = records.jobs.find((job) => job.jobId === jobId);
  if (prior) {
    requireHandoff(prior.instructionKey === instructionKey && prior.instructionHash === instructionHash,
      "The job already has different agreed instructions. Preserve its commitments and prepare the necessary change.");
    return jobId;
  }
  requireHandoff(quote.status === "Offered", "Obtain a current provider offer before commissioning.");
  requireHandoff(!records.jobs.some((job) => job.quoteId === quote.quoteId
    && jobScope(job).some((line) => input.scope.some((selected) => selected.quoteLineId === line.lineId))),
  "Some of this offered work has already been commissioned. Continue that job rather than ordering it twice.");
  const alreadyCommitted = records.jobs.filter((job) => job.workPlanId === plan.workPlanId)
    .reduce((sum, job) => sum + BigInt(money(job.committedCents, "Existing commitment")), 0n).toString();
  const price = priceCommission(mandate, offer, input.scope, alreadyCommitted, context.now);
  requireHandoff(funded.funding.currency === offer.currency && BigInt(funded.position.availableCents) >= BigInt(price.totalCents),
    "The confirmed owner funds do not cover this commitment. The work budget is not a cash balance.");
  const provider = await one(context.client(HandoffParty).where({ partyId: { $eq: offer.providerPartyId } }));
  requireHandoff(provider, "The provider is not available."); inWorkspace(provider, workspace, context.caller);
  // Earlier correspondence concerned the whole accepted plan. Recognize it only for exactly that scope/provider.
  let earlier: Osdk.Instance<HandoffMessage> | undefined;
  if (draft.providerPartyId === offer.providerPartyId) {
    const correspondence = requestWorkCorrespondence(workspace.mode!, `continue:${decision.decisionId}`, provider, draft);
    earlier = recognizedWorkRequest(records.messages, shared.workspaceId, handoff.handoffId, plan.workPlanId,
      decision.decisionId, provider.partyId, correspondence.body, correspondence.replyBody);
    if (earlier) requireHandoff(price.scope.length === draft.scope.length
      && draft.scope.every((scope) => price.scope.some((line) => line.acceptedScope === scope)),
    "The earlier request covers the whole accepted plan. Do not reinterpret it as different or partial work.");
  }
  const unconfirmed = mandate.requirements.filter((item) => !offer.requirements.includes(item));
  const requestId = earlier?.messageId ?? reference("message", shared.workspaceId, instructionKey, "appointment");
  const responseDueAt = afterMinutes(earlier?.createdAt ?? context.now, offer.responseMinutes);
  context.batch.create(HandoffJob, { ...shared, jobId, title: offer.title, providerPartyId: offer.providerPartyId,
    workPlanId: plan.workPlanId, decisionId: decision.decisionId, quoteId: quote.quoteId, fundingId: funded.funding.fundingId,
    obligationId: input.obligationId, origin: "Handoff", kind: offer.kind, status: "Commissioned",
    scopeJson: orderedJson(price.scope), requirements: [...mandate.requirements], currency: offer.currency,
    committedCents: price.totalCents, depositCents: price.depositCents, instructionKey, instructionHash,
    requestMessageId: requestId, nextResponseAt: responseDueAt,
    progressSummary: earlier ? "The vendor has acknowledged the order."
      : unconfirmed.length ? "Order sent. Waiting for the vendor to confirm the requirements."
        : "Order sent. Waiting for the vendor to book the visit.",
    revision: "1", createdAt: context.now, updatedAt: context.now });
  if (!earlier) context.batch.create(HandoffMessage, { workspaceId: shared.workspaceId, readerIds: shared.readerIds,
    handoffId: shared.handoffId, workPlanId: plan.workPlanId, jobId, messageId: requestId, title: `Work order: ${offer.title}`.slice(0, 200),
    body: letter(provider, [`Please go ahead with the following work at ${world.property.name}, as quoted (${formatAmount(price.totalCents, offer.currency)}):`,
      bullets(price.scope.map((line) => line.description)),
      ...(mandate.requirements.length ? [`Requirements for all work on this unit:\n${bullets(mandate.requirements)}${
        unconfirmed.length ? "\nPlease confirm these requirements when you book the visit." : ""}`] : []),
      `Payment terms: ${offer.paymentTerms}`, "Please reply with your first available date."].join("\n\n"), (workspace.name ?? "Property management")),
    purpose: "Appointment", direction: "Outgoing", recipientPartyId: offer.providerPartyId, status: "Queued",
    createdAt: context.recordedAt ?? context.now, responseDueAt, externalReference: instructionKey,
    detailsJson: orderedJson({ purpose: "Appointment", providerPartyId: offer.providerPartyId, quoteId: quote.quoteId,
      scopeLineIds: price.scope.map((line) => line.lineId), jobId }) });
  context.batch.update(plan, { status: "Accepted", acceptedDecisionId: decision.decisionId });
  context.batch.update(quote, { status: quote.status });
  context.batch.update(funded.funding, { revision: nextRevision(funded.funding.revision) });
  touchDelivery(context, instructionKey);
  return jobId;
}

/** Read a report as observations, not as an instruction or a substitute for the whole property's outcome. */
export function completionFromInspection(job: Job, inspection: Inspection, now: string): "Complete" | "Needs attention" | "Awaiting check" {
  requireHandoff(inspection.jobId === job.jobId && inspection.propertyId === job.propertyId
    && inspection.handoffId === job.handoffId && inspection.purpose === "Completion check",
  "This observation is not a completion check for this job.");
  const at = instant(inspection.observedAt);
  requireHandoff(at <= instant(now) && at >= instant(job.appointmentAt ?? job.createdAt), "The observation predates the job or is in the future.");
  words(inspection.sourceDocumentId, "Observation evidence", 160); words(inspection.observerPartyId, "Observer", 160);
  const observed = findings(JSON.parse(words(inspection.findingsJson, "Findings", 100000)) as unknown), scope = jobScope(job);
  requireHandoff(observed.every((finding) => scope.some((line) => line.lineId === finding.lineId)), "The report includes work outside this job.");
  if (observed.some((finding) => finding.result === "Deficient")) return "Needs attention";
  return scope.every((line) => observed.some((finding) => finding.lineId === line.lineId && finding.result === "Satisfied")) ? "Complete" : "Awaiting check";
}
export async function checkJobCompletion(context: DeliveryContext, jobId: string, inspectionId: string): Promise<string> {
  deliveryAccess(context);
  const job = await deliveryJob(context, jobId);
  const inspection = await one(context.client(HandoffInspection).where({ inspectionId: { $eq: words(inspectionId, "Inspection", 160) } }));
  requireHandoff(inspection, "The job observation is not available."); inWorkspace(inspection, context.workspace, context.caller);
  await requireDeliverySource(context, words(inspection.sourceDocumentId, "Report", 160), [words(inspection.observerPartyId, "Observer", 160)]);
  const status = completionFromInspection(job, inspection, context.now);
  if (job.verificationInspectionId === inspectionId && job.status === status) return status;
  requireHandoff(job.status !== "Cancelled", "Resolve the cancellation before changing the job's delivery state.");
  if (job.verificationInspectionId) {
    const previous = await one(context.client(HandoffInspection).where({ inspectionId: { $eq: job.verificationInspectionId } }));
    requireHandoff(previous, "The earlier job check is unavailable."); inWorkspace(previous, context.workspace, context.caller);
    requireHandoff(instant(inspection.observedAt) > instant(previous.observedAt), "An older or simultaneous report cannot replace the job's later check.");
  }
  context.batch.update(job, { status, verificationInspectionId: inspectionId,
    progressSummary: status === "Complete" ? "Report checked. The work is complete."
      : status === "Needs attention" ? "Report checked. Some of the work still needs fixing." : "Report checked. Part of the work isn't covered yet.",
    revision: nextRevision(job.revision), updatedAt: context.now });
  touchDelivery(context, reference("job-check", jobId, inspectionId));
  return status;
}
