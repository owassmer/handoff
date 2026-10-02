import { preparation } from "./sourceAccess.js";
import { fundingInformation } from "./supportingSources.js";
import { HandoffFunding, HandoffJob, HandoffPayment, HandoffInvoice, HandoffDocument } from "@ontology/sdk";
import type { Osdk } from "@osdk/client";
import type { Long } from "@osdk/functions";
import { bounded, inWorkspace, one } from "./records.js";
import { details, nextRevision, reference, requireHandoff, words } from "./values.js";
import { currencyCode, instant, money, sourceRecord, type OwnerAllocation, type PaymentObservation } from "./deliveryContracts.js";
import { deliveryAccess, deliveryJob, pendingDeliveryRecord, requireDeliverySource, requireSavedFinancialState, sameRecord, sourceIdentity, touchDelivery,
  type DeliveryContext, type Job, type Payment } from "./deliveryRecords.js";

export type Funding = Osdk.Instance<HandoffFunding>;
export interface FundingPosition { confirmedCents: Long; committedOrSpentCents: Long; availableCents: Long }

/** Count a job's commitment once, not again when it becomes a payment. Unknown outcomes keep funds held. */
export function fundingPosition(funding: Pick<Funding, "fundingId" | "currency" | "confirmedCents">,
  jobs: readonly Job[], payments: readonly Payment[]): FundingPosition {
  const confirmed = BigInt(money(funding.confirmedCents, "Confirmed owner funds"));
  currencyCode(funding.currency);
  requireHandoff(new Set(jobs.map((job) => job.jobId)).size === jobs.length
    && new Set(payments.map((payment) => payment.paymentId)).size === payments.length, "Funding records repeat an identity.");
  payments.forEach((payment) => {
    requireHandoff(payment.fundingId === funding.fundingId && payment.currency === funding.currency
      && jobs.some((job) => job.jobId === payment.jobId), "A payment does not match these owner funds and jobs.");
    requireHandoff(["Requested", "Confirming", "Settled", "Failed", "Returned"].includes(payment.status ?? ""), "A payment outcome needs checking before funds can be used.");
    money(payment.amountCents);
  });
  const committed = jobs.reduce((total, job) => {
    requireHandoff(job.fundingId === funding.fundingId && job.currency === funding.currency, "A job does not match these owner funds.");
    const amount = BigInt(money(job.committedCents, "Job commitment"));
    const activePayments = payments.filter((payment) => payment.jobId === job.jobId
      && ["Requested", "Confirming", "Settled"].includes(payment.status!))
      .reduce((sum, payment) => sum + BigInt(payment.amountCents!), 0n);
    const remainingCommitment = job.status === "Cancelled" ? 0n : amount;
    return total + (activePayments > remainingCommitment ? activePayments : remainingCommitment);
  }, 0n);
  requireHandoff(committed <= confirmed, "Existing commitments exceed the confirmed owner funds. Reconcile the allocation before adding work.");
  return { confirmedCents: confirmed.toString(), committedOrSpentCents: committed.toString(), availableCents: (confirmed - committed).toString() };
}
export async function loadOwnerFunding(context: DeliveryContext, fundingId: string, forNewSpending = true): Promise<{ funding: Funding; jobs: Job[]; payments: Payment[]; position: FundingPosition }> {
  deliveryAccess(context);
  const [funding, jobs, payments] = await Promise.all([
    one(context.client(HandoffFunding).where({ fundingId: { $eq: words(fundingId, "Owner funds", 160) } })),
    bounded(context.client(HandoffJob).where({ fundingId: { $eq: fundingId }, workspaceId: { $eq: context.workspace.workspaceId } })),
    bounded(context.client(HandoffPayment).where({ fundingId: { $eq: fundingId }, workspaceId: { $eq: context.workspace.workspaceId } })),
  ]);
  requireHandoff(funding, "Confirm an owner funding allocation before committing money.");
  const duplicates = await bounded(context.client(HandoffFunding).where({ workspaceId: { $eq: context.workspace.workspaceId },
    sourceSystem: { $eq: words(funding.sourceSystem, "Funding source", 160) }, sourceRecordId: { $eq: words(funding.sourceRecordId, "Allocation reference", 200) } }));
  requireHandoff(duplicates.length === 1 && duplicates[0]?.fundingId === fundingId, "The same owner allocation has been recorded more than once. Reconcile it before using the funds.");
  const [versions, source] = await Promise.all([
    bounded(context.client(HandoffDocument).where({ workspaceId: { $eq: context.workspace.workspaceId },
      sourceSystem: { $eq: funding.sourceSystem! }, sourceRecordId: { $eq: funding.sourceRecordId! } })),
    one(context.client(HandoffDocument).where({ workspaceId: { $eq: context.workspace.workspaceId }, documentId: { $eq: words(funding.sourceDocumentId, "Funding confirmation", 160) } })),
  ]);
  requireHandoff(source, "The funding confirmation is unavailable; confirm the actual allocation before using it.");
  const confirmations = [...versions, ...(versions.some((doc) => doc.documentId === source.documentId) ? [] : [source])];
  confirmations.forEach((document) => {
    inWorkspace(document, context.workspace, context.caller);
    if (!forNewSpending || document.kind !== "Owner funding" || (document.availableFrom && document.availableFrom > context.now.slice(0, 10))) return;
    preparation(document);
    const current = fundingInformation(document);
    requireHandoff(current.ownerPartyId === funding.ownerPartyId && current.currency === funding.currency
      && current.confirmedCents === funding.confirmedCents && instant(current.confirmedAt) === instant(funding.confirmedAt),
    "The same owner allocation has changed. Reconcile it before making another commitment or payment.");
  });
  [funding, ...jobs, ...payments].forEach((record) => inWorkspace(record, context.workspace, context.caller));
  requireHandoff(funding.propertyId === context.handoff.propertyId && instant(funding.confirmedAt) <= instant(context.now), "The owner funding confirmation does not cover this property and time.");
  return { funding, jobs, payments, position: fundingPosition(funding, jobs, payments) };
}
export async function recordOwnerFunding(context: DeliveryContext, input: OwnerAllocation): Promise<string> {
  const shared = deliveryAccess(context);
  const row = details(input, ["sourceSystem", "sourceRecordId", "sourceDocumentId", "title", "ownerPartyId", "currency", "confirmedCents", "confirmedAt"], [], "Owner funding");
  const source = sourceRecord(row), confirmedAt = instant(input.confirmedAt);
  requireHandoff(confirmedAt <= instant(context.now), "Owner funding has not yet been confirmed.");
  const document = await requireDeliverySource(context, source.sourceDocumentId, [words(input.ownerPartyId, "Funding owner", 160)]);
  preparation(document);
  const info = fundingInformation(document);
  requireHandoff((document.sourceSystem ?? "Owner funding confirmation") === source.sourceSystem && (document.sourceRecordId ?? document.documentId) === source.sourceRecordId
    && info.ownerPartyId === input.ownerPartyId && info.currency === input.currency && info.confirmedCents === input.confirmedCents
    && info.confirmedAt === confirmedAt, "Use the configured funding source identity and confirmed terms without substitutions.");
  const fundingId = sourceIdentity("funding", shared.workspaceId, source);
  const saved = { workspaceId: shared.workspaceId, readerIds: shared.readerIds, propertyId: shared.propertyId,
    fundingId, ...source, title: words(input.title, "Funding title", 200), ownerPartyId: input.ownerPartyId,
    currency: currencyCode(input.currency), confirmedCents: money(input.confirmedCents), confirmedAt, revision: "1" };
  if (pendingDeliveryRecord(context, "HandoffFunding", fundingId, saved, ["confirmedAt"])) return fundingId;
  const prior = await one(context.client(HandoffFunding).where({ fundingId: { $eq: fundingId } }));
  if (prior) { inWorkspace(prior, context.workspace, context.caller); sameRecord(prior, saved, ["revision"], ["confirmedAt"]); return fundingId; }
  context.batch.create(HandoffFunding, saved); touchDelivery(context, fundingId);
  return fundingId;
}

/** Assign current funds to an already recorded Handoff commitment, without rewriting its authority. */
export async function bindExistingJobFunding(context: DeliveryContext, jobId: string, fundingId: string): Promise<void> {
  requireSavedFinancialState(context);
  const job = await deliveryJob(context, jobId);
  requireHandoff(job.origin === "Handoff" && job.decisionId && job.instructionKey && job.status !== "Cancelled",
    "Bind funds only to an existing accepted Handoff commitment.");
  if (job.fundingId) {
    requireHandoff(job.fundingId === fundingId, "This job already has a funding allocation; reconcile it rather than rebinding it.");
    return;
  }
  const { funding, position } = await loadOwnerFunding(context, fundingId);
  requireHandoff(funding.currency === job.currency && BigInt(position.availableCents) >= BigInt(money(job.committedCents)),
    "Confirm sufficient current owner funds for the whole existing commitment before payment.");
  const payments = await bounded(context.client(HandoffPayment).where({ jobId: { $eq: jobId }, workspaceId: { $eq: context.workspace.workspaceId } }));
  payments.forEach((payment) => inWorkspace(payment, context.workspace, context.caller));
  requireHandoff(payments.length === 0, "Reconcile earlier payments before assigning a funding source.");
  context.batch.update(job, { fundingId, revision: nextRevision(job.revision), updatedAt: context.now });
  context.batch.update(funding, { revision: nextRevision(funding.revision) });
  touchDelivery(context, fundingId);
}

/** Stage a payment intent only. No network call and no invented settlement. Commit before obtaining an outcome. */
export async function requestProviderPayment(context: DeliveryContext, jobId: string, purpose: "Advance" | "Invoice", invoiceId?: string): Promise<string> {
  const shared = deliveryAccess(context);
  requireSavedFinancialState(context);
  const job = await deliveryJob(context, jobId);
  requireHandoff(job.origin === "Handoff" && job.decisionId && job.fundingId && job.instructionKey,
    "This job needs accepted payment authority and owner funding before a payment can be requested.");
  requireHandoff(job.status !== "Cancelled", "Do not request a new payment for cancelled work.");
  requireHandoff(purpose === "Advance" || purpose === "Invoice", "Choose an advance or invoice payment.");
  const { funding, payments, position } = await loadOwnerFunding(context, job.fundingId);
  requireHandoff(funding.currency === job.currency && BigInt(position.availableCents) >= 0n, "Reconcile current funds and commitments before requesting payment.");
  const related = payments.filter((payment) => payment.jobId === job.jobId);
  const paymentId = reference("payment", shared.workspaceId, job.instructionKey, purpose);
  const prior = related.find((payment) => payment.paymentId === paymentId);
  if (prior) {
    requireHandoff(prior.invoiceId === invoiceId && prior.purpose === purpose && prior.providerPartyId === job.providerPartyId,
      "The saved payment request differs from this request.");
    return prior.paymentId;
  }
  let amountCents = money(job.depositCents, "Quoted advance");
  if (purpose === "Invoice") {
    requireHandoff(invoiceId && job.status === "Complete", "Check the completed job and identify its invoice before requesting the balance.");
    const invoice = await one(context.client(HandoffInvoice).where({ invoiceId: { $eq: invoiceId } }));
    requireHandoff(invoice, "The supplier invoice is not available."); inWorkspace(invoice, context.workspace, context.caller);
    requireHandoff(invoice.jobId === job.jobId && invoice.providerPartyId === job.providerPartyId
      && invoice.payerPartyId === funding.ownerPartyId && invoice.currency === job.currency
      && ["Received", "Agreed"].includes(invoice.status ?? "") && invoice.totalCents === job.committedCents,
    "Resolve the invoice's scope, payer or amount before payment. Partial invoices need an explicit allocation.");
    requireHandoff(!related.some((payment) => ["Requested", "Confirming"].includes(payment.status ?? "")),
      "Confirm the earlier payment outcome before requesting the balance.");
    const paid = related.filter((payment) => payment.status === "Settled").reduce((sum, payment) => sum + BigInt(money(payment.amountCents)), 0n);
    requireHandoff(paid <= BigInt(invoice.totalCents!), "Recorded payments exceed the invoice total.");
    amountCents = (BigInt(invoice.totalCents!) - paid).toString();
    context.batch.update(invoice, { status: "Agreed" });
  } else requireHandoff(invoiceId === undefined && !related.length, "The advance already has a payment record.");
  const heldOrPaid = related.filter((payment) => ["Requested", "Confirming", "Settled"].includes(payment.status ?? ""))
    .reduce((sum, payment) => sum + BigInt(money(payment.amountCents)), 0n);
  requireHandoff(BigInt(amountCents) + heldOrPaid <= BigInt(money(job.committedCents)), "The payment would exceed this job's accepted commitment.");
  requireHandoff(BigInt(amountCents) > 0n, "There is no unpaid amount to request.");
  context.batch.create(HandoffPayment, { workspaceId: shared.workspaceId, readerIds: shared.readerIds, handoffId: shared.handoffId,
    paymentId, title: purpose === "Advance" ? `Advance for ${job.title}` : `Pay ${job.title}`,
    jobId, fundingId: funding.fundingId, invoiceId, providerPartyId: job.providerPartyId, amountCents, currency: job.currency,
    purpose, status: "Requested", instructionKey: paymentId, requestedAt: context.now, revision: "1" });
  context.batch.update(funding, { revision: nextRevision(funding.revision) });
  context.batch.update(job, { revision: nextRevision(job.revision) }); touchDelivery(context, paymentId);
  return paymentId;
}

/** Only an authenticated adapter may supply observations; do not expose this as an unrestricted model tool. */
export async function observeProviderPayment(context: DeliveryContext, paymentId: string, input: PaymentObservation): Promise<void> {
  deliveryAccess(context);
  requireSavedFinancialState(context);
  details(input, ["instructionKey", "sourceReference", "amountCents", "currency", "status", "observedAt", "definitive"], [], "Payment result");
  requireHandoff(typeof input.definitive === "boolean" && (input.status === "Confirming" ? !input.definitive : input.definitive),
    "Only a definitive provider confirmation establishes payment, return or failure; otherwise keep the outcome uncertain.");
  const observedAt = instant(input.observedAt);
  const payment = await one(context.client(HandoffPayment).where({ paymentId: { $eq: words(paymentId, "Payment", 160) } }));
  requireHandoff(payment && payment.handoffId === context.handoff.handoffId, "This payment is not available for this handoff.");
  inWorkspace(payment, context.workspace, context.caller);
  requireHandoff(payment.instructionKey === input.instructionKey && payment.currency === currencyCode(input.currency)
    && payment.amountCents === money(input.amountCents) && observedAt <= instant(context.now)
    && observedAt >= instant(payment.requestedAt), "The result does not match the saved payment instruction.");
  words(input.sourceReference, "Payment result reference", 200);
  requireHandoff(["Confirming", "Settled", "Failed", "Returned"].includes(input.status), "Choose the observed payment outcome.");
  if (payment.status === input.status) {
    requireHandoff(payment.sourceReference === input.sourceReference && instant(payment.observedAt) === observedAt,
      "The same payment outcome has conflicting confirmation details.");
    return;
  }
  requireHandoff(observedAt >= instant(payment.observedAt ?? payment.requestedAt), "An older payment result cannot replace a later one.");
  const mayChange = ((payment.status === "Requested" || payment.status === "Confirming") && input.status !== "Returned")
    || (payment.status === "Settled" && input.status === "Returned");
  requireHandoff(mayChange, "Investigate the conflicting payment result; do not send another payment.");
  const { funding } = await loadOwnerFunding(context, words(payment.fundingId, "Owner funds", 160), false);
  const matches = await Promise.all([
    bounded(context.client(HandoffPayment).where({ workspaceId: { $eq: context.workspace.workspaceId }, sourceReference: { $eq: input.sourceReference } }), 2),
    bounded(context.client(HandoffPayment).where({ workspaceId: { $eq: context.workspace.workspaceId }, settlementReference: { $eq: input.sourceReference } }), 2),
    bounded(context.client(HandoffPayment).where({ workspaceId: { $eq: context.workspace.workspaceId }, returnReference: { $eq: input.sourceReference } }), 2),
  ]);
  matches.flat().forEach((other) => {
    inWorkspace(other, context.workspace, context.caller);
    requireHandoff(other.paymentId === paymentId, "This confirmation already belongs to another payment. Reconcile the shared movement rather than count it twice.");
  });
  requireHandoff(input.status !== "Returned" || input.sourceReference !== payment.settlementReference,
    "The return needs its own observed movement reference.");
  context.batch.update(payment, { status: input.status, observedAt, sourceReference: input.sourceReference, revision: nextRevision(payment.revision),
    ...(input.status === "Settled" ? { settlementReference: input.sourceReference, settledAt: observedAt } : {}),
    ...(input.status === "Returned" ? { returnReference: input.sourceReference, returnedAt: observedAt } : {}) });
  context.batch.update(funding, { revision: nextRevision(funding.revision) }); touchDelivery(context, payment.paymentId);
}
