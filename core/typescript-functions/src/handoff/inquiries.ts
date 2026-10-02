import { preparation } from "./sourceAccess.js";
import { HandoffDocument, HandoffMessage, HandoffQuote } from "@ontology/sdk";
import { deliveryAccess, touchDelivery, type DeliveryContext, type DeliveryRecords } from "./deliveryRecords.js";
import { inWorkspace, one } from "./records.js";
import { loadDetails, type HandoffDetails } from "./workDetails.js";
import { readInquiry, type Inquiry } from "./coordinateReasoning.js";
import { providerServices, type ProviderService } from "./supportingSources.js";
import { afterMinutes, formatAmount, instant } from "./deliveryContracts.js";
import { digest, orderedJson, parseDetails, reference, requireHandoff, words } from "./values.js";
import { sumQuotedCosts } from "./quoteCosts.js";
import { providerResponseId } from "./counterparts.js";
import { longDate, plainList, workingSpan } from "./wording.js";
import { letter } from "./email.js";

/** An inquiry has a stable content/source identity; coordinator turn identities never cause a resend. */
/** attachments: documents sent with a quote request, e.g. the assessment report the trade quotes against. */
export async function queueInquiry(context: DeliveryContext, value: Inquiry, attachments: string[] = []): Promise<string> {
  const shared = deliveryAccess(context), input = readInquiry(value);
  const world = await loadDetails(context.client, context.handoff, context.workspace, context.caller);
  requireHandoff(world.parties.some((party) => party.partyId === input.recipientPartyId), "The recipient is not part of this handoff.");
  if (input.previousReplyId) {
    const previous = await one(context.client(HandoffMessage).where({ messageId: { $eq: input.previousReplyId } }));
    requireHandoff(previous, "The earlier reply is unavailable."); inWorkspace(previous, context.workspace, context.caller);
    requireHandoff(previous.handoffId === shared.handoffId && previous.direction === "Incoming" && previous.senderPartyId === input.recipientPartyId, "This follow-up belongs to a different conversation.");
  }
  const source = input.purpose === "Quote" && input.providerDocumentId ? world.documents.find((doc) => doc.documentId === input.providerDocumentId) : undefined;
  const service = source ? providerServices(source).find((candidate) => candidate.serviceId === input.serviceId) : undefined;
  if (input.purpose === "Quote") requireHandoff(source && service && source.partyId === input.recipientPartyId, "Choose a service supplied by this provider.");
  // This correspondence adapter discloses the current supplied facts. Rephrasing a question
  // cannot produce new facts or justify another send. A changed source/mandate can.
  const sourceBasis = world.documents.map((doc) => [doc.documentId, doc.sourceVersion, doc.text, doc.detailsJson, doc.availableFrom])
    .sort((a, b) => String(a[0]).localeCompare(String(b[0])));
  const instruction = input.purpose === "Quote"
    ? { purpose: input.purpose, recipientPartyId: input.recipientPartyId, providerDocumentId: input.providerDocumentId,
      serviceId: input.serviceId, sourceVersion: source?.sourceVersion, sourceContent: digest([source?.text, source?.detailsJson]),
      ...(attachments.length ? { scopeDocuments: [...attachments].sort() } : {}) }
    : { purpose: input.purpose, recipientPartyId: input.recipientPartyId, sourceBasis: digest(sourceBasis),
      mandate: context.handoff.operativeDecisionId ?? null, followUp: Boolean(input.previousReplyId) };

  const requestId = reference("message", shared.workspaceId, shared.handoffId, "inquiry", digest(instruction));
  const props = { workspaceId: shared.workspaceId, readerIds: shared.readerIds, handoffId: shared.handoffId,
    messageId: requestId, recipientPartyId: input.recipientPartyId,
    title: (input.purpose === "Quote" ? `Quote request: ${service!.title}` : input.purpose === "Funding" ? `Funds for ${world.property.name}` : `Question about ${world.property.name}`).slice(0, 200),
    body: letter(world.parties.find((party) => party.partyId === input.recipientPartyId), input.question, (context.workspace.name ?? "Property management")), purpose: input.purpose, direction: "Outgoing", status: "Queued", createdAt: context.recordedAt ?? context.now,
    responseDueAt: afterMinutes(context.now, service?.responseMinutes ?? 1), externalReference: requestId,
    detailsJson: orderedJson(input.purpose === "Quote" && attachments.length ? { ...input, attachments: [...new Set(attachments)] } : input) };
  const queued = context.batch.getEdits().find((edit) => edit.type === "createObject" && edit.obj.apiName === "HandoffMessage"
    && Reflect.get(edit.properties, "messageId") === requestId);
  if (queued) return requestId;
  const prior = await one(context.client(HandoffMessage).where({ messageId: { $eq: requestId } }));
  if (prior) {
    inWorkspace(prior, context.workspace, context.caller);
    requireHandoff(prior.handoffId === shared.handoffId && prior.purpose === input.purpose
      && prior.recipientPartyId === input.recipientPartyId, "This inquiry belongs to a different conversation.");
    return requestId;
  }
  context.batch.create(HandoffMessage, props); touchDelivery(context, requestId); return requestId;
}

/** Respond using current permitted counterpart information, not a stored answer to the Handoff. */
export async function answerInquiry(context: DeliveryContext, requestId: string, records: DeliveryRecords, world: HandoffDetails): Promise<string> {
  const shared = deliveryAccess(context), request = records.messages.find((message) => message.messageId === requestId);
  requireHandoff(request && request.direction === "Outgoing" && instant(request.responseDueAt) <= instant(context.now), "This inquiry is not due for a reply.");
  const input = readInquiry(parseDetails(words(request.detailsJson, "Inquiry", 100000), "Inquiry"));
  requireHandoff(input.recipientPartyId === request.recipientPartyId, "The inquiry recipient has changed.");
  const replyId = providerResponseId(shared.workspaceId, requestId);
  if (records.messages.some((message) => message.messageId === replyId)) return replyId;
  let body: string, quoteId: string | undefined, unanswered = false;
  const attachments: string[] = [];
  const sender = world.parties.find((party) => party.partyId === input.recipientPartyId)?.name ?? "";
  if (input.purpose === "Quote") {
    const source = world.documents.find((doc) => doc.documentId === input.providerDocumentId);
    requireHandoff(source && source.partyId === input.recipientPartyId, "The provider's current service information is unavailable.");
    preparation(source);
    const service = providerServices(source).find((candidate) => candidate.serviceId === input.serviceId);
    requireHandoff(service, "The requested service is not in the provider's information.");
    if (service.validUntil < instant(context.now)) body = "We can no longer offer this work on the earlier terms. Let us know if you'd like a current quote.";
    else {
      quoteId = reference("quote", shared.workspaceId, requestId);
      const documentId = reference("document", shared.workspaceId, quoteId), totalCents = sumQuotedCosts(service.lines);
      const quoteText = `${service.title}. ${service.lines.map((line) => `${line.description}: ${formatAmount(line.amountCents, service.currency)}`).join("; ")}. ${service.paymentTerms}`;
      body = `Thanks for your request. Our quote for ${service.title.toLowerCase()} is attached: ${formatAmount(totalCents, service.currency)} in total. ${service.paymentTerms}`;
      attachments.push(documentId);
      const quoteDetails = { providerDocumentId: source.documentId, serviceId: service.serviceId, providerSourceVersion: source.sourceVersion ?? digest(source.detailsJson) };
      context.batch.create(HandoffDocument, { workspaceId: shared.workspaceId, readerIds: shared.readerIds, handoffId: shared.handoffId,
        documentId, title: service.title, text: quoteText, kind: "Quote", partyId: source.partyId, sourceKind: "Prepared", sourceVersion: "1",
        availableFrom: context.handoff.businessDate, detailsJson: orderedJson(quoteDetails) });
      context.batch.create(HandoffQuote, { ...shared, quoteId, title: service.title, providerPartyId: source.partyId, kind: service.kind,
        currency: service.currency, linesJson: orderedJson(service.lines), totalCents, depositCents: service.depositCents,
        paymentTerms: service.paymentTerms, requirements: service.requirements, availableFrom: service.availableFrom,
        validUntil: service.validUntil, durationMinutes: service.durationMinutes, responseMinutes: service.responseMinutes,
        sourceSystem: "Provider correspondence", sourceRecordId: requestId, sourceDocumentId: documentId, status: "Offered", recordedAt: context.now });
    }
  } else {
    // The test correspondence interface can disclose only material attributed to this sender.
    const offers = input.purpose === "Information" ? world.documents.filter((doc) => doc.partyId === input.recipientPartyId
      && doc.kind === "Provider information" && doc.detailsJson).flatMap((doc) => { preparation(doc); return providerServices(doc); }) : [];
    const documents = world.documents.filter((doc) => doc.partyId === input.recipientPartyId
      && (input.purpose !== "Funding" || doc.kind === "Owner funding") && !["Provider information", "Property condition"].includes(doc.kind ?? ""));
    if (offers.length) body = offers.map(serviceTerms).join("\n");
    // A correspondent points to what it already sent rather than pasting it back; the documents stay readable in full.
    else if (documents.length) {
      body = `Please see my ${plainList([...new Set(documents.map((doc) => doc.title!))])}, attached again here.`;
      attachments.push(...documents.map((doc) => doc.documentId));
    }
    // Funds can be confirmed later, so a funding question stays open. An information correspondent
    // with nothing on file answers once and definitively; repeating the question cannot create facts.
    else if (input.purpose === "Funding") { unanswered = true; body = "I don't have that confirmation yet. I'll come back to you."; }
    else body = "I'm afraid I don't have anything more on this.";
  }
  // Nothing is cut to fit: a reply the workspace view could not read (60,000 characters) fails here, where its cause is.
  requireHandoff(body.length <= 50000, "This reply is too long to send as one message.");
  context.batch.create(HandoffMessage, { workspaceId: shared.workspaceId, readerIds: shared.readerIds, handoffId: shared.handoffId,
    messageId: replyId, replyToMessageId: requestId, senderPartyId: input.recipientPartyId, recipientPartyId: input.recipientPartyId,
    direction: "Incoming", purpose: input.purpose, status: "Received", createdAt: context.recordedAt ?? context.now,
    title: `Re: ${request.title ?? "your message"}`.slice(0, 200), body: letter(undefined, body, sender, "Best,"), externalReference: requestId,
    responseDueAt: unanswered ? afterMinutes(context.now, 1440) : undefined,
    detailsJson: orderedJson({ quoteId: quoteId ?? null, unanswered, ...(attachments.length ? { attachments } : {}) }) });
  context.batch.update(request, { status: "Sent" }); touchDelivery(context, replyId); return replyId;
}

/** A provider's own published terms. A visit time is agreed only after the work is commissioned. */
function serviceTerms(service: ProviderService): string {
  const sentence = (text: string): string => /[.!?]$/.test(text) ? text : `${text}.`;
  const requirements = service.requirements.length ? ` Requirements: ${service.requirements.join("; ")}.` : "";
  return `${service.title}: our earliest visit is ${longDate(service.availableFrom)} and the work takes about ${workingSpan(service.durationMinutes)}. `
    + `We usually reply within ${workingSpan(service.responseMinutes)}, and our offer is valid until ${longDate(service.validUntil)}. ${sentence(service.paymentTerms)}${requirements} `
    + "We'll agree the visit time once the work is ordered.";
}
