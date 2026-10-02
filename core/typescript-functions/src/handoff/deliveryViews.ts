import { HandoffFunding, HandoffJob, HandoffPayment } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import type { HandoffWorkspaceView } from "./contracts.js";
import { bounded, inWorkspace, type Caller, type Handoff, type Workspace } from "./records.js";
import { loadDeliveryRecords, jobScope, offerFromRecord } from "./deliveryRecords.js";
import { fundingPosition } from "./funding.js";
import { findings, money, quoteLines } from "./deliveryContracts.js";
import { orderedJson, parseDetails, requireHandoff, words } from "./values.js";

type DeliveryView = Pick<HandoffWorkspaceView, "jobs" | "quotes" | "inspections" | "invoices" | "funding" | "payments">;
export async function deliveryViews(client: Client, workspace: Workspace, caller: Caller, handoff: Handoff): Promise<DeliveryView> {
  const [records, funding] = await Promise.all([loadDeliveryRecords(client, workspace, caller, handoff, false),
    bounded(client(HandoffFunding).where({ workspaceId: { $eq: workspace.workspaceId }, propertyId: { $eq: handoff.propertyId! } }))]);
  funding.forEach((row) => inWorkspace(row, workspace, caller));
  requireHandoff(new Set(funding.map((row) => orderedJson([row.sourceSystem, row.sourceRecordId]))).size === funding.length,
    "The same owner allocation has been recorded more than once. Reconcile it before displaying available funds.");
  const ids = funding.map((row) => row.fundingId);
  const [fundedJobs, fundedPayments] = ids.length ? await Promise.all([
    bounded(client(HandoffJob).where({ workspaceId: { $eq: workspace.workspaceId }, fundingId: { $in: ids } })),
    bounded(client(HandoffPayment).where({ workspaceId: { $eq: workspace.workspaceId }, fundingId: { $in: ids } })),
  ]) : [[], []];
  [...fundedJobs, ...fundedPayments].forEach((row) => inWorkspace(row, workspace, caller));
  return {
    jobs: records.jobs.map((job) => ({ id: job.jobId, title: words(job.title, "Job title", 200), kind: job.kind!, status: job.status!, origin: job.origin!,
      providerPartyId: job.providerPartyId!, workPlanId: job.workPlanId ?? null, decisionId: job.decisionId ?? null, quoteId: job.quoteId ?? null,
      scope: jobScope(job), committedCents: job.committedCents === undefined ? null : money(job.committedCents), currency: job.currency!,
      appointmentAt: job.appointmentAt ?? null, appointmentEndsAt: job.appointmentEndsAt ?? null, progressSummary: job.progressSummary ?? "",
      verificationInspectionId: job.verificationInspectionId ?? null })),
    quotes: records.quotes.map((quote) => {
      const offer = offerFromRecord(quote);
      return { id: quote.quoteId, title: offer.title, providerPartyId: offer.providerPartyId, kind: offer.kind, status: quote.status!, currency: offer.currency,
        lines: offer.lines, totalCents: offer.totalCents, depositCents: offer.depositCents, paymentTerms: offer.paymentTerms,
        requirements: offer.requirements, availableFrom: offer.availableFrom, validUntil: offer.validUntil, sourceDocumentId: offer.sourceDocumentId };
    }),
    inspections: records.inspections.map((inspection) => ({ id: inspection.inspectionId, title: inspection.title!, jobId: inspection.jobId ?? null,
      observerPartyId: inspection.observerPartyId!, purpose: inspection.purpose!, observedAt: inspection.observedAt!,
      findings: findings(parseDetails(inspection.findingsJson!, "Findings")), sourceDocumentId: inspection.sourceDocumentId! })),
    invoices: records.invoices.map((invoice) => ({ id: invoice.invoiceId, title: invoice.title!, jobId: invoice.jobId!, providerPartyId: invoice.providerPartyId!,
      payerPartyId: invoice.payerPartyId!, status: invoice.status!, lines: quoteLines(parseDetails(invoice.linesJson!, "Invoice lines")),
      totalCents: money(invoice.totalCents), currency: invoice.currency!, dueAt: invoice.dueAt!, sourceDocumentId: invoice.sourceDocumentId! })),
    funding: funding.map((row) => ({ id: row.fundingId, title: row.title!, ownerPartyId: row.ownerPartyId!, currency: row.currency!,
      ...fundingPosition(row, fundedJobs.filter((job) => job.fundingId === row.fundingId), fundedPayments.filter((payment) => payment.fundingId === row.fundingId)), sourceDocumentId: row.sourceDocumentId! })),
    payments: records.payments.map((payment) => ({ id: payment.paymentId, title: payment.title!, jobId: payment.jobId!, purpose: payment.purpose!,
      status: payment.status!, amountCents: money(payment.amountCents), currency: payment.currency!, requestedAt: payment.requestedAt!, observedAt: payment.observedAt ?? null })),
  };
}
