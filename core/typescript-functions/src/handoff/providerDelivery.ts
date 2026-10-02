import { preparation, sourceDetails } from "./sourceAccess.js";
import { mappedAcceptedScopes } from "./acceptedWork.js";
import { HandoffDocument, HandoffInspection, HandoffInvoice, HandoffMessage } from "@ontology/sdk";
import type { HandoffDetails } from "./workDetails.js";
import { jobScope, offerFromRecord, type DeliveryContext, type DeliveryRecords, type Job } from "./deliveryRecords.js";
import { propertyConditions, providerServices, fundingInformation, type PropertyCondition, type ProviderService, type SourceDocument } from "./supportingSources.js";
import { afterMinutes, formatAmount, instant, type Finding } from "./deliveryContracts.js";
import { details, digest, entries, nextRevision, orderedJson, parseDetails, reference, requireHandoff, words } from "./values.js";
import { loadOwnerFunding, observeProviderPayment } from "./funding.js";
import { letter } from "./email.js";
import { longDate } from "./wording.js";

export function latestCondition(documents: readonly SourceDocument[]): SourceDocument | undefined {
  const candidates = documents.filter((doc) => doc.kind === "Property condition" && doc.detailsJson);
  const superseded = new Set(candidates.map((doc) => {
    const row = details(sourceDetails(doc.detailsJson!), ["conditions"], ["jobId", "priorDocumentId", "coverage"], "Condition information");
    return row.priorDocumentId;
  }));
  const current = candidates.filter((doc) => !superseded.has(doc.documentId));
  requireHandoff(current.length <= 1, "The property has competing condition reports. Resolve their relationship before recording performance.");
  return current[0];
}
/** One condition as an operator reads it in a report. */
function conditionLabel(condition: PropertyCondition): string {
  if (!condition.accessible) return "no access";
  return condition.state === "Satisfied" ? "satisfactory" : condition.state === "Deficient" ? "needs work" : "not checked";
}
/** Only selected physical effects can change condition; known inaccessible/unrepairable issues remain. */
export function performService(service: ProviderService, selectedLineIds: string[], conditions: PropertyCondition[]): { conditions: PropertyCondition[]; findings: Finding[] } {
  const selected = service.effects.filter((effect) => selectedLineIds.includes(effect.lineId));
  requireHandoff(selected.length === selectedLineIds.length, "The provider has not described how to perform or check this scope.");
  const changes = new Set(selected.flatMap((effect) => effect.conditionIds));
  const resulting = conditions.map((condition): PropertyCondition => ({ ...condition,
    state: changes.has(condition.conditionId) && condition.accessible && condition.repairable
      && (service.kind === "Repair" || service.kind === "Cleaning") ? "Satisfied" : condition.state }));
  const findings = selected.map((effect): Finding => {
    const subjects = resulting.filter((condition) => effect.conditionIds.includes(condition.conditionId));
    const allObserved = subjects.length === effect.conditionIds.length && subjects.every((condition) => condition.accessible && condition.state !== "Not checked");
    const isAssessment = service.kind === "Assessment";
    const result = !allObserved ? "Not checked" : (isAssessment || subjects.every((condition) => condition.state === "Satisfied")) ? "Satisfied" : "Deficient";
    return { lineId: effect.lineId, result, method: effect.method,
      observation: subjects.length ? subjects.map((condition) => `${condition.description.replace(/[.\s]+$/, "")}: ${conditionLabel(condition)}`).join("\n")
        : "The required condition information is not available." };
  });
  return { conditions: resulting, findings };
}

/** Stateful test provider: work starts only from a saved commission, appointment and paid advance. */
export function deliverScheduledJob(context: DeliveryContext, job: Job, world: HandoffDetails, records: DeliveryRecords, payerPartyId?: string): boolean {
  if (job.status !== "Scheduled" || !job.appointmentEndsAt || instant(job.appointmentEndsAt) > instant(context.now)) return false;
  const reportId = reference("inspection", context.workspace.workspaceId, job.instructionKey!, "completion");
  if (records.inspections.some((report) => report.inspectionId === reportId)) return false;
  requireHandoff(payerPartyId, "The work needs its confirmed funding owner.");
  const quote = records.quotes.find((candidate) => candidate.quoteId === job.quoteId);
  requireHandoff(quote, "The commissioned quote is unavailable.");
  const quoteSource = world.documents.find((doc) => doc.documentId === quote.sourceDocumentId);
  if (!quoteSource?.detailsJson) return false; // Imported work is not invented by this counterpart.
  const mapping = details(sourceDetails(quoteSource.detailsJson), ["providerDocumentId", "serviceId", "providerSourceVersion"], ["offer", "sourcePassages"], "Quote terms");
  const source = world.documents.find((doc) => doc.documentId === mapping.providerDocumentId);
  requireHandoff(source && source.partyId === job.providerPartyId, "The provider's service information is unavailable.");
  requireHandoff((source.sourceVersion ?? digest(source.detailsJson)) === mapping.providerSourceVersion, "The provider terms changed after the offer. Obtain confirmation before delivery.");
  preparation(source);
  const service = providerServices(source).find((candidate) => candidate.serviceId === mapping.serviceId);
  requireHandoff(service, "The agreed provider service is unavailable.");
  const agreed = offerFromRecord(quote);
  requireHandoff(service.kind === agreed.kind && service.currency === agreed.currency
    && service.depositCents === agreed.depositCents && service.paymentTerms === agreed.paymentTerms
    && agreed.requirements.every((requirement) => service.requirements.includes(requirement))
    && orderedJson(service.lines) === orderedJson(agreed.lines),
  "The configured service must perform exactly the quoted work and price, without added scope.");
  const condition = latestCondition(world.documents);
  if (!condition) return false;
  const conditionPreparation = preparation(condition);
  const settled = records.payments.filter((payment) => payment.jobId === job.jobId && payment.status === "Settled")
    .reduce((sum, payment) => sum + BigInt(payment.amountCents!), 0n);
  requireHandoff(settled >= BigInt(job.depositCents!), "Confirm the agreed advance before delivery.");
  const result = performService(service, jobScope(job).map((line) => line.lineId), propertyConditions(condition));
  const acceptedMapping = world.documents.find((doc) => doc.documentId === job.sourceDocumentId && doc.kind === "Accepted work mapping");
  if (acceptedMapping?.detailsJson) {
    const scope = entries(sourceDetails(acceptedMapping.detailsJson).scope, "Accepted scope mapping", 48, 1);
    result.findings = result.findings.map((finding): Finding => {
      const mapping = scope.find((item) => (item as Record<string, unknown>).quoteLineId === finding.lineId);
      requireHandoff(mapping, "The original accepted scope mapping is unavailable.");
      const terms = mappedAcceptedScopes(mapping), effect = service.effects.find((item) => item.lineId === finding.lineId)!;
      const reports = terms.map((term) => {
        const report = effect.deliverables?.find((item) => item.acceptedScope === term);
        const observed = report && report.conditionIds.every((id) => result.conditions.some((item) => item.conditionId === id && item.accessible && item.state !== "Not checked"));
        const evidence = report && report.sourceDocumentIds.every((id) => world.documents.some((doc) => doc.documentId === id))
          && report.sourceDocumentIds.some((id) => world.documents.find((doc) => doc.documentId === id)?.text?.includes(report.observation));
        return { term, report, supported: Boolean(observed && evidence) };
      });
      return { ...finding, result: finding.result === "Deficient" ? "Deficient" : finding.result === "Satisfied" && reports.every((item) => item.supported) ? "Satisfied" : "Not checked",
        observation: reports.map(({ term, report, supported }) => `${term}\n${supported ? report!.observation : "Not checked: supporting report evidence or access is unavailable."}`).join("\n\n"),
        method: reports.map(({ report, supported }) => supported ? report!.method : "Supporting evidence still required.").join("; ") };
    });
  }
  requireHandoff(orderedJson(result.findings).length <= 100000, "The report exceeds the bounded evidence record.");
  const common = { workspaceId: context.workspace.workspaceId, readerIds: [...context.workspace.readerIds!], handoffId: context.handoff.handoffId };
  const documentId = reference("document", common.workspaceId, reportId), observedAt = instant(job.appointmentEndsAt);
  // Each condition once, even when several report lines cover it; then how the work was checked.
  const conditionLines = [...new Set(result.findings.flatMap((finding) => finding.observation.split("\n")))];
  const reportText = `${conditionLines.join("\n")}\n\nMethod: ${[...new Set(result.findings.map((finding) => finding.method))].join(" ")}`;
  words(reportText, "Report text", 24000);
  context.batch.create(HandoffDocument, { ...common, documentId, title: `${job.title} — report`, kind: "Inspection", partyId: job.providerPartyId,
    text: reportText, sourceKind: "Prepared", sourceVersion: "1", availableFrom: context.handoff.businessDate });
  context.batch.create(HandoffInspection, { ...common, propertyId: context.handoff.propertyId, inspectionId: reportId,
    title: `${job.title} — completion check`, observerPartyId: job.providerPartyId, observedAt, purpose: "Completion check", jobId: job.jobId,
    findingsJson: orderedJson(result.findings), sourceSystem: "Provider correspondence", sourceRecordId: job.instructionKey,
    sourceDocumentId: documentId, recordedAt: context.now });
  const conditionId = reference("document", common.workspaceId, job.instructionKey!, "condition-after-work");
  context.batch.create(HandoffDocument, { ...common, documentId: conditionId, title: "Property condition after work", kind: "Property condition",
    partyId: job.providerPartyId, text: result.conditions.map((item) => `${item.description}: ${item.state}`).join("\n"),
    sourceKind: "Prepared", sourceVersion: nextRevision(condition.sourceVersion && /^\d+$/.test(condition.sourceVersion) ? condition.sourceVersion : "1"),
    availableFrom: context.handoff.businessDate, detailsJson: orderedJson({ ...sourceDetails(condition.detailsJson!), conditions: result.conditions, jobId: job.jobId, priorDocumentId: condition.documentId, _preparation: conditionPreparation }) });
  const invoiceId = reference("invoice", common.workspaceId, job.instructionKey!), invoiceDocumentId = reference("document", common.workspaceId, invoiceId);
  const offer = offerFromRecord(quote), lines = jobScope(job).map(({ acceptedScope: _accepted, ...line }) => line);
  context.batch.create(HandoffDocument, { ...common, documentId: invoiceDocumentId, title: `Invoice for ${job.title}`, kind: "Invoice", partyId: job.providerPartyId,
    text: `${job.title}: ${formatAmount(job.committedCents, job.currency!)}. ${offer.paymentTerms}`, sourceKind: "Prepared", sourceVersion: "1", availableFrom: context.handoff.businessDate });
  context.batch.create(HandoffInvoice, { ...common, invoiceId, title: `Invoice for ${job.title}`, jobId: job.jobId, providerPartyId: job.providerPartyId,
    payerPartyId, currency: job.currency, totalCents: job.committedCents, linesJson: orderedJson(lines),
    issuedAt: observedAt, dueAt: afterMinutes(observedAt, service.invoiceDueMinutes ?? 1440), paymentTerms: offer.paymentTerms, status: "Received",
    sourceSystem: "Provider correspondence", sourceRecordId: job.instructionKey, sourceDocumentId: invoiceDocumentId, recordedAt: context.now });
  const vendor = world.parties.find((party) => party.partyId === job.providerPartyId)?.name ?? "";
  context.batch.create(HandoffMessage, { ...common, messageId: reference("message", common.workspaceId, reportId), title: `Report and invoice: ${job.title}`.slice(0, 200),
    body: letter(undefined, `We've finished the ${(job.title ?? "work").toLowerCase()} on ${longDate(observedAt)}. Our report and invoice are attached.`, vendor, "Best,"),
    senderPartyId: job.providerPartyId, recipientPartyId: job.providerPartyId, jobId: job.jobId, direction: "Incoming", purpose: "Progress", status: "Received",
    createdAt: context.recordedAt ?? context.now, externalReference: job.instructionKey, detailsJson: orderedJson({ attachments: [documentId, invoiceDocumentId] }) });
  return true;
}

/** Payment counterpart answers the same saved instruction; uncertain results never authorize resending. */
export async function respondToPayment(context: DeliveryContext, records: DeliveryRecords, world: HandoffDetails): Promise<false | { status: string; jobId?: string; amountCents: string; currency: string; purpose?: string }> {
  const payment = records.payments.find((candidate) => candidate.status === "Requested");
  if (!payment) return false;
  const { funding } = await loadOwnerFunding(context, words(payment.fundingId, "Owner funds", 160), false);
  const doc = world.documents.find((candidate) => candidate.documentId === funding.sourceDocumentId && candidate.kind === "Owner funding" && candidate.detailsJson);
  if (!doc) return false;
  preparation(doc);
  const info = fundingInformation(doc), due = afterMinutes(payment.requestedAt!, info.responseMinutes);
  if (due > instant(context.now)) return false;
  requireHandoff(info.currency === payment.currency && info.ownerPartyId === funding.ownerPartyId, "The payment service does not match the owner's funding.");
  const status = info.paymentBehavior === "Settle" ? "Settled" : info.paymentBehavior === "Reject" ? "Failed" : "Confirming";
  await observeProviderPayment(context, payment.paymentId, { instructionKey: words(payment.instructionKey, "Payment instruction", 200),
    sourceReference: reference("payment-result", payment.instructionKey!, status), amountCents: payment.amountCents!, currency: payment.currency!,
    status, definitive: status !== "Confirming", observedAt: due });
  return { status, jobId: payment.jobId, amountCents: payment.amountCents!, currency: payment.currency!, purpose: payment.purpose };
}
