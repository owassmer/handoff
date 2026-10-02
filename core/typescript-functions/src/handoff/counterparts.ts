import { HandoffJob, HandoffMessage, HandoffParty } from "@ontology/sdk";
import type { Osdk } from "@osdk/client";
import { bounded, inWorkspace, one } from "./records.js";
import { WORKDAY_MINUTES, longDate, nextWorkingStart, workingEnd } from "./wording.js";
import { letter } from "./email.js";
import { nextRevision, orderedJson, parseDetails, reference, requireHandoff, wordList, words } from "./values.js";
import { afterMinutes, findings, instant, money, providerRequest,
  type ProviderReply, type ProviderRequest, type QuoteOffer } from "./deliveryContracts.js";
import { deliveryAccess, deliveryJob, deliveryQuote, jobScope, loadDeliveryRecords, offerFromRecord,
  pendingDeliveryRecord, sameRecord, touchDelivery, type DeliveryContext, type DeliveryRecords, type Job } from "./deliveryRecords.js";

export interface DueProviderRequest { requestId: string; dueAt: string; purpose: string; jobId?: string }
export function providerResponseId(workspaceId: string, requestId: string): string {
  return reference("message", workspaceId, requestId, "provider-response");
}
/** An acknowledgment is not the requested appointment, report or invoice. */
export function dueProviderRequests(records: DeliveryRecords, now: string): DueProviderRequest[] {
  const time = instant(now);
  return records.messages.filter((message) => message.direction === "Outgoing"
    && ["Queued", "Sent"].includes(message.status ?? ""))
    .flatMap((message): DueProviderRequest[] => {
      const job = records.jobs.find((candidate) => candidate.requestMessageId === message.messageId);
      const oldAcknowledgment = job?.decisionId && records.messages.some((reply) => reply.messageId === reference("message", message.workspaceId!, `continue:${job.decisionId}`, "acknowledgement"));
      if (oldAcknowledgment && !message.detailsJson && !message.responseDueAt) return [];
      const dueAt = message.responseDueAt ?? job?.nextResponseAt;
      if (!dueAt || instant(dueAt) > time) return [];
      const replyId = providerResponseId(words(message.workspaceId, "Workspace", 160), message.messageId);
      if (records.messages.some((reply) => reply.messageId === replyId)) return [];
      return [{ requestId: message.messageId, dueAt: instant(dueAt), purpose: message.purpose ?? "Appointment",
        ...(message.jobId ?? job?.jobId ? { jobId: message.jobId ?? job!.jobId } : {}) }];
    }).sort((a, b) => a.dueAt.localeCompare(b.dueAt) || a.requestId.localeCompare(b.requestId));
}

/** Place a bounded business request in the shared batch; the counterpart answers only after it is saved. */
export async function queueProviderRequest(context: DeliveryContext, rawInput: ProviderRequest): Promise<string> {
  const shared = deliveryAccess(context), input = providerRequest(rawInput), quote = await deliveryQuote(context, input.quoteId), offer = offerFromRecord(quote);
  requireHandoff(input.providerPartyId === offer.providerPartyId && input.scopeLineIds.every((id) => offer.lines.some((line) => line.lineId === id)),
    "The request does not match this provider's offer.");
  let job: Job | undefined;
  if (input.jobId) {
    job = await deliveryJob(context, input.jobId);
    requireHandoff(job.providerPartyId === input.providerPartyId && job.quoteId === input.quoteId
      && input.scopeLineIds.every((id) => jobScope(job!).some((line) => line.lineId === id)), "The request does not match the commissioned job.");
    requireHandoff(job.status !== "Cancelled", "Resolve cancelled work before requesting another appointment or delivery update.");
  }
  requireHandoff(input.purpose === "Quote" || job, "Commission the accepted job before requesting delivery.");
  if (input.purpose === "Appointment" && !input.previousReplyId && job?.requestMessageId) {
    const original = await one(context.client(HandoffMessage).where({ messageId: { $eq: job.requestMessageId } }));
    requireHandoff(original && original.handoffId === shared.handoffId && original.recipientPartyId === input.providerPartyId,
      "The original work request needs checking before another appointment request is sent.");
    inWorkspace(original, context.workspace, context.caller);
    requireHandoff(input.scopeLineIds.length === jobScope(job).length, "Continue the original whole-job appointment request.");
    return original.messageId;
  }
  if (input.previousReplyId) {
    const reply = await one(context.client(HandoffMessage).where({ messageId: { $eq: input.previousReplyId } }));
    requireHandoff(reply, "The earlier reply is unavailable."); inWorkspace(reply, context.workspace, context.caller);
    const legacyReply = job?.decisionId && reply.messageId === reference("message", shared.workspaceId, `continue:${job.decisionId}`, "acknowledgement");
    const original = legacyReply && job?.requestMessageId ? await one(context.client(HandoffMessage).where({ messageId: { $eq: job.requestMessageId } })) : undefined;
    if (original) inWorkspace(original, context.workspace, context.caller);
    const originalAcknowledgment = legacyReply && original?.messageId === reference("message", shared.workspaceId, `continue:${job!.decisionId}`, "request")
      && original?.handoffId === shared.handoffId && original?.recipientPartyId === input.providerPartyId && original?.workPlanId === job?.workPlanId
      && reply.workPlanId === job?.workPlanId && reply.externalReference === original?.externalReference && reply.recipientPartyId === input.providerPartyId;
    requireHandoff(reply.handoffId === shared.handoffId && reply.direction === "Incoming"
      && (originalAcknowledgment || (reply.senderPartyId === input.providerPartyId && reply.jobId === input.jobId)),
    "The follow-up does not belong to this provider conversation.");
  }
  const logicalSubject = job?.instructionKey ?? input.quoteId;
  const requestId = reference("message", shared.workspaceId, shared.handoffId, words(logicalSubject, "Request subject", 200), input.purpose,
    ...[...input.scopeLineIds].sort(), input.previousReplyId ?? "initial");
  const ask = input.purpose === "Appointment" ? `Please book the visit for ${offer.title.toLowerCase()} and let us know the date.`
    : input.purpose === "Invoice" ? `Please send your invoice for ${offer.title.toLowerCase()}.`
      : input.purpose === "Progress" ? `Please send an update or your report for ${offer.title.toLowerCase()}.`
        : `Please confirm your current quote for ${offer.title.toLowerCase()}.`;
  const body = letter(undefined, job && input.purpose === "Appointment" && job.status === "Awaiting advance" ? `The advance is paid. ${ask}` : ask,
    (context.workspace.name ?? "Property management"));
  const saved = { workspaceId: shared.workspaceId, readerIds: shared.readerIds, handoffId: shared.handoffId,
    messageId: requestId, jobId: input.jobId, workPlanId: job?.workPlanId,
    title: `${input.purpose === "Appointment" ? "Booking" : input.purpose}: ${offer.title}`.slice(0, 200), body,
    purpose: input.purpose, direction: "Outgoing", recipientPartyId: input.providerPartyId, status: "Queued", createdAt: context.recordedAt ?? context.now,
    responseDueAt: afterMinutes(context.now, offer.responseMinutes), externalReference: logicalSubject, detailsJson: orderedJson(input) };
  if (pendingDeliveryRecord(context, "HandoffMessage", requestId, saved, ["createdAt", "responseDueAt"])) return requestId;
  const prior = await one(context.client(HandoffMessage).where({ messageId: { $eq: requestId } }));
  // Wording may change between releases; the request's identity and details must not.
  if (prior) { inWorkspace(prior, context.workspace, context.caller); sameRecord(prior, saved, ["createdAt", "responseDueAt", "status", "title", "body"]); return requestId; }
  context.batch.create(HandoffMessage, saved);
  // Once the advance is paid the job waits on the booking, not the advance.
  if (job && input.purpose === "Appointment") context.batch.update(job, { nextResponseAt: saved.responseDueAt, revision: nextRevision(job.revision), updatedAt: context.now,
    ...(job.status === "Awaiting advance" ? { status: "Commissioned", progressSummary: "Advance paid. Waiting for the vendor to book the visit." } : {}) });
  touchDelivery(context, requestId);
  return requestId;
}

/** When a visit ends: clock time within a day; multi-day work runs in daily working windows from the offer's start time. */
export function visitEnd(offer: QuoteOffer, start: string): string {
  return offer.durationMinutes > WORKDAY_MINUTES ? workingEnd(start, offer.durationMinutes, offer.availableFrom) : afterMinutes(start, offer.durationMinutes);
}
/** Reserve the first fitting time from actual offer availability and existing appointments. */
export function providerAppointment(offer: QuoteOffer, now: string, providerJobs: readonly Job[], currentJobId: string): { start: string; end: string } {
  const snap = (at: string): string => offer.durationMinutes > WORKDAY_MINUTES ? nextWorkingStart(at, offer.availableFrom) : at;
  let start = snap(instant(now) > instant(offer.availableFrom) ? instant(now) : instant(offer.availableFrom));
  const occupied = providerJobs.filter((job) => job.jobId !== currentJobId && job.providerPartyId === offer.providerPartyId
    && job.status !== "Cancelled" && job.appointmentAt).map((job) => {
      requireHandoff(job.appointmentEndsAt, "A provider appointment is missing its end time.");
      return { start: instant(job.appointmentAt), end: instant(job.appointmentEndsAt) };
    }).sort((a, b) => a.start.localeCompare(b.start));
  occupied.forEach((slot) => {
    requireHandoff(slot.end > slot.start, "A provider appointment has inconsistent times.");
    const end = visitEnd(offer, start);
    if (start < slot.end && end > slot.start) start = snap(slot.end);
  });
  return { start, end: visitEnd(offer, start) };
}
function reply(outcome: ProviderReply["outcome"], summary: string, extra: Partial<ProviderReply> = {}): ProviderReply {
  return { outcome, summary, quoteIds: [], inspectionIds: [], invoiceIds: [], ...extra };
}
/** Pure provider behavior from source offers, availability and attributed observations; no event counter. */
export function prepareProviderReply(input: ProviderRequest, records: DeliveryRecords, now: string,
  providerJobs: readonly Job[] = records.jobs): ProviderReply {
  providerRequest(input); instant(now);
  const quote = records.quotes.find((candidate) => candidate.quoteId === input.quoteId);
  requireHandoff(quote && quote.providerPartyId === input.providerPartyId, "The requested provider offer is unavailable.");
  const offer = offerFromRecord(quote);
  requireHandoff(input.scopeLineIds.every((id) => offer.lines.some((line) => line.lineId === id)), "The request refers to work absent from the offer.");
  if (input.purpose === "Quote") {
    if (quote.status === "Offered" && offer.validUntil >= instant(now)) return reply("Offer", `${offer.title}. ${offer.paymentTerms}`, { quoteIds: [quote.quoteId] });
    const requested = offer.lines.filter((line) => input.scopeLineIds.includes(line.lineId)).map((line) => line.description);
    const alternatives = records.quotes.filter((candidate) => candidate.quoteId !== quote.quoteId && candidate.providerPartyId === input.providerPartyId
      && candidate.status === "Offered" && instant(candidate.validUntil) >= instant(now))
      .filter((candidate) => requested.every((scope) => offerFromRecord(candidate).lines.some((line) => line.description === scope)));
    return alternatives.length ? reply("Alternative", "Our earlier offer has lapsed. Our current offers cover this work.", { quoteIds: alternatives.map((candidate) => candidate.quoteId) })
      : reply("Unavailable", "We can no longer offer this work on the earlier terms.");
  }
  const job = records.jobs.find((candidate) => candidate.jobId === input.jobId);
  requireHandoff(job && job.providerPartyId === input.providerPartyId && job.quoteId === input.quoteId,
    "The provider request does not match a saved job.");
  requireHandoff(input.scopeLineIds.every((id) => jobScope(job).some((line) => line.lineId === id)), "The request exceeds the saved job scope.");
  if (input.purpose === "Appointment") {
    if (job.status === "Cancelled") return reply("Unavailable", "We have this job as cancelled. Let us know if any of the work is still needed.");
    // The provider confirms the order's requirements that its offer did not already state, once, before booking.
    const pending = unconfirmedRequirements(job, offer, records);
    const confirmed = (result: ProviderReply): ProviderReply => pending.length
      ? { ...result, summary: `Confirmed requirements: ${pending.join(" ")} ${result.summary}`, confirmedRequirements: pending } : result;
    if (job.appointmentAt) return confirmed(reply("Appointment", `The visit is already booked for ${longDate(job.appointmentAt)}.`, { appointmentAt: instant(job.appointmentAt) }));
    const settled = records.payments.filter((payment) => payment.jobId === job.jobId && payment.status === "Settled")
      .reduce((sum, payment) => sum + BigInt(money(payment.amountCents)), 0n);
    if (settled < BigInt(money(job.depositCents))) return confirmed(reply("Advance required", `We need the agreed advance before we book the visit. ${offer.paymentTerms}`));
    if (quote.status !== "Offered") return reply("Unavailable", "We have withdrawn this offer. Please contact us about the work already agreed.");
    const appointment = providerAppointment(offer, now, providerJobs, job.jobId);
    return confirmed(reply("Appointment", `We can start on ${longDate(appointment.start)}.`, { appointmentAt: appointment.start }));
  }
  if (input.purpose === "Invoice") {
    const invoices = records.invoices.filter((invoice) => invoice.jobId === job.jobId && invoice.providerPartyId === input.providerPartyId
      && instant(invoice.issuedAt) <= instant(now));
    return invoices.length ? reply("Invoice", "Our invoice is attached.", { invoiceIds: invoices.map((invoice) => invoice.invoiceId) })
      : reply("Waiting", "We haven't issued an invoice for this job yet.");
  }
  const reports = records.inspections.filter((inspection) => inspection.jobId === job.jobId
    && instant(inspection.observedAt) <= instant(now) && instant(inspection.observedAt) >= instant(job.appointmentAt ?? job.createdAt))
    .sort((a, b) => instant(b.observedAt).localeCompare(instant(a.observedAt)) || a.inspectionId.localeCompare(b.inspectionId));
  if (!reports.length) return reply("Waiting", "We don't have a report for this job yet.");
  // Prefer the latest observation for each requested line; retain all report references used.
  const observed = new Map<string, { result: string; at: string; inspectionIds: string[] }>();
  reports.forEach((report) => findings(parseDetails(words(report.findingsJson, "Findings", 100000), "Findings"))
    .forEach((finding) => {
      if (!input.scopeLineIds.includes(finding.lineId)) return;
      const previous = observed.get(finding.lineId), at = instant(report.observedAt);
      if (!previous) observed.set(finding.lineId, { result: finding.result, at, inspectionIds: [report.inspectionId] });
      else if (previous.at === at) {
        previous.inspectionIds.push(report.inspectionId);
        if (finding.result === "Deficient") previous.result = "Deficient";
        else if (finding.result === "Not checked" && previous.result === "Satisfied") previous.result = "Not checked";
      }
    }));
  const inspectionIds = [...new Set([...observed.values()].flatMap((finding) => finding.inspectionIds))];
  if ([...observed.values()].some((finding) => finding.result === "Deficient")) return reply("Deficiency", "Our report lists work that still needs attention.", { inspectionIds });
  if (input.scopeLineIds.every((id) => observed.get(id)?.result === "Satisfied")) return reply("Reported complete", "The work is complete. Our report is attached.", { inspectionIds });
  return reply("Partial", "Part of the work is done. Our report covers what we've checked so far.", { inspectionIds });
}

/** Job requirements that neither the offer states nor an earlier provider reply confirmed. */
function unconfirmedRequirements(job: Job, offer: QuoteOffer, records: DeliveryRecords): string[] {
  const confirmed = records.messages.filter((message) => message.direction === "Incoming" && message.jobId === job.jobId
    && message.senderPartyId === job.providerPartyId && message.detailsJson)
    .flatMap((message) => {
      const row = parseDetails(message.detailsJson!, "Provider reply");
      const value = row && typeof row === "object" ? Reflect.get(row, "confirmedRequirements") : undefined;
      return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
    });
  return (job.requirements ?? []).filter((item) => !offer.requirements.includes(item) && !confirmed.includes(item));
}
/** Respond to a persisted request in a later invocation. A saved response is returned unchanged on replay. */
export async function respondToProviderRequest(context: DeliveryContext, requestId: string): Promise<ProviderReply> {
  const shared = deliveryAccess(context), records = await loadDeliveryRecords(context.client, context.workspace, context.caller, context.handoff);
  const request = records.messages.find((message) => message.messageId === words(requestId, "Provider request", 160));
  requireHandoff(request && request.direction === "Outgoing", "The saved provider request is unavailable.");
  const responseId = providerResponseId(shared.workspaceId, request.messageId);
  const prior = records.messages.find((message) => message.messageId === responseId);
  if (prior) {
    requireHandoff(prior.replyToMessageId === requestId && prior.direction === "Incoming" && prior.senderPartyId === request.recipientPartyId,
      "The saved reply does not match the provider request.");
    return readProviderReply(prior.detailsJson);
  }
  const due = dueProviderRequests(records, context.now).find((item) => item.requestId === requestId);
  requireHandoff(due, "The provider request is not due for a response.");
  const legacyJob = records.jobs.find((job) => job.requestMessageId === requestId);
  const input = request.detailsJson ? providerRequest(parseDetails(request.detailsJson, "Provider request")) : providerRequest({
    purpose: "Appointment", providerPartyId: legacyJob?.providerPartyId, quoteId: legacyJob?.quoteId,
    scopeLineIds: legacyJob ? jobScope(legacyJob).map((line) => line.lineId) : [], jobId: legacyJob?.jobId,
  });
  requireHandoff(request.recipientPartyId === input.providerPartyId && (!request.jobId || request.jobId === input.jobId), "The request's provider or job has changed.");
  const [provider, providerJobs] = await Promise.all([
    one(context.client(HandoffParty).where({ partyId: { $eq: input.providerPartyId } })),
    bounded(context.client(HandoffJob).where({ providerPartyId: { $eq: input.providerPartyId }, workspaceId: { $eq: shared.workspaceId } })),
  ]);
  requireHandoff(provider, "The provider is unavailable.");
  [provider, ...providerJobs].forEach((row) => inWorkspace(row, context.workspace, context.caller));
  const result = prepareProviderReply(input, records, context.now, providerJobs);
  const attachments = [...result.inspectionIds.map((id) => records.inspections.find((row) => row.inspectionId === id)?.sourceDocumentId),
    ...result.invoiceIds.map((id) => records.invoices.find((row) => row.invoiceId === id)?.sourceDocumentId),
    ...result.quoteIds.map((id) => records.quotes.find((row) => row.quoteId === id)?.sourceDocumentId)].filter((id): id is string => Boolean(id));
  const responseRecord = { workspaceId: shared.workspaceId, readerIds: shared.readerIds, handoffId: shared.handoffId,
    messageId: responseId, replyToMessageId: requestId, jobId: input.jobId, workPlanId: request.workPlanId,
    senderPartyId: input.providerPartyId, title: `Re: ${request.title ?? offerTitle(records, input.quoteId)}`.slice(0, 200),
    body: letter(undefined, result.summary, provider.name ?? "", "Best,"), purpose: input.purpose,
    direction: "Incoming", status: "Received", createdAt: context.recordedAt ?? context.now, externalReference: request.externalReference,
    detailsJson: orderedJson({ ...result, ...(attachments.length ? { attachments: [...new Set(attachments)] } : {}) }) };
  if (pendingDeliveryRecord(context, "HandoffMessage", responseId, responseRecord)) return result;
  context.batch.create(HandoffMessage, responseRecord);
  if (request.status === "Queued") context.batch.update(request, { status: "Sent" });
  // Preserve the earlier request and acknowledgment exactly; a reply is a new business record.
  if (input.jobId) {
    const job = records.jobs.find((candidate) => candidate.jobId === input.jobId)!;
    if (result.appointmentAt && !job.appointmentAt) {
      const offer = offerFromRecord(records.quotes.find((candidate) => candidate.quoteId === input.quoteId)!);
      context.batch.update(job, { status: "Scheduled", appointmentAt: result.appointmentAt,
        appointmentEndsAt: visitEnd(offer, result.appointmentAt), nextResponseAt: undefined,
        progressSummary: `Visit booked for ${longDate(result.appointmentAt)}.`, revision: nextRevision(job.revision), updatedAt: context.now });
      // Touch the same provider when reserving availability. This is not a general distributed lock.
      context.batch.update(provider, { name: provider.name });
    } else if (result.outcome === "Advance required" || result.outcome === "Unavailable") {
      context.batch.update(job, { status: result.outcome === "Advance required" ? "Awaiting advance" : "Needs attention",
        nextResponseAt: undefined, progressSummary: result.outcome === "Advance required" ? "Waiting for the advance payment before the visit is booked."
          : "The vendor can't go ahead on the agreed terms.", revision: nextRevision(job.revision), updatedAt: context.now });
    }
  }
  touchDelivery(context, responseId);
  return result;
}
function offerTitle(records: DeliveryRecords, quoteId: string): string {
  return records.quotes.find((quote) => quote.quoteId === quoteId)?.title ?? "your request";
}
function readProviderReply(value: unknown): ProviderReply {
  const parsed = parseDetails(words(value, "Provider reply", 100000), "Provider reply");
  requireHandoff(typeof parsed === "object" && parsed !== null && !Array.isArray(parsed), "The provider reply needs checking.");
  const row = parsed as Record<string, unknown>;
  const outcomes: ProviderReply["outcome"][] = ["Offer", "Alternative", "Unavailable", "Appointment", "Advance required", "Waiting", "Partial", "Deficiency", "Reported complete", "Invoice"];
  requireHandoff(typeof row.outcome === "string" && outcomes.includes(row.outcome as ProviderReply["outcome"]), "The provider reply has an unsupported outcome.");
  const refs = (key: string): string[] => {
    requireHandoff(Array.isArray(row[key]) && row[key].length <= 100, "The provider reply has too many references.");
    return (row[key] as unknown[]).map((item) => words(item, "Reply reference", 160));
  };
  return { outcome: row.outcome as ProviderReply["outcome"], summary: words(row.summary, "Provider reply", 4000),
    quoteIds: refs("quoteIds"), inspectionIds: refs("inspectionIds"), invoiceIds: refs("invoiceIds"),
    ...(row.appointmentAt === undefined ? {} : { appointmentAt: instant(row.appointmentAt) }),
    ...(row.confirmedRequirements === undefined ? {} : { confirmedRequirements: wordList(row.confirmedRequirements, "Confirmed requirements", 32, 0, 1000) }) };
}
