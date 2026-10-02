import { HandoffWorkPlan, HandoffDecision, HandoffFunding, HandoffMessage } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import { Aliases, createEditBatch } from "@osdk/functions";
import { addActivity, command, wasApplied } from "./activity.js";
import { bounded, currentCaller, guardWorkspace, inWorkspace, loadAgentWork, loadHandoff, one, type HandoffEdit } from "./records.js";
import { loadDetails } from "./workDetails.js";
import { createFoundryWorkModel, type WorkModel } from "./reasoner.js";
import { loadDeliveryRecords, jobScope, type DeliveryContext } from "./deliveryRecords.js";
import { dueProviderRequests, providerResponseId, queueProviderRequest, respondToProviderRequest } from "./counterparts.js";
import { commissionJob, checkJobCompletion } from "./delivery.js";
import { bindExistingJobFunding, loadOwnerFunding, recordOwnerFunding, requestProviderPayment } from "./funding.js";
import { answerInquiry, queueInquiry } from "./inquiries.js";
import { readInquiry, reasonNextWork, type CoordinatorRecommendation } from "./coordinateReasoning.js";
import { RecommendationValidationExhausted } from "./recommendationValidation.js";
import { deliverScheduledJob, latestCondition, respondToPayment } from "./providerDelivery.js";
import { fundingInformation, propertyConditions } from "./supportingSources.js";
import { materialBasis, planSelections, selectedCost } from "./proposal.js";
import { businessMoment, caseTime, wakeTime } from "./clock.js";
import { sourceDetails } from "./sourceAccess.js";
import { recognizeAcceptedWork } from "./acceptedWork.js";
import { readinessCoverage } from "./supportingSources.js";
import { recognizeSourceRecord } from "./sourceRecords.js";
import { acceptedContent, planDraft } from "./workPlans.js";
import { afterMinutes, formatAmount, instant, type ProviderReply } from "./deliveryContracts.js";
import { deliveryStatus, longDate, plainList } from "./wording.js";
import { digest, nextRevision, orderedJson, parseDetails, reference, requireHandoff } from "./values.js";

export interface CoordinatorDependencies { now?: string; model?: WorkModel }
/** What a vendor's reply means for the operator, in Handoff's words. */
function providerUpdate(reply: ProviderReply, vendor: string): string {
  const what: Record<ProviderReply["outcome"], string> = {
    Offer: `${vendor} sent a quote.`,
    Alternative: `${vendor}'s earlier offer lapsed. They sent a current one.`,
    Unavailable: `${vendor} can't go ahead on the earlier terms.`,
    Appointment: reply.appointmentAt ? `${vendor} booked the visit for ${longDate(reply.appointmentAt)}.` : `${vendor} confirmed the visit.`,
    "Advance required": `${vendor} needs the agreed advance before booking the visit.`,
    Waiting: `Waiting for ${vendor}'s report or invoice.`,
    Partial: `${vendor}'s report covers part of the work so far.`,
    Deficiency: `${vendor}'s report shows work still to fix.`,
    "Reported complete": `${vendor} reports the work complete. Handoff is checking the report.`,
    Invoice: `${vendor} sent the invoice.`,
  };
  return `${reply.confirmedRequirements?.length ? `${vendor} confirmed the requirements. ` : ""}${what[reply.outcome]}`;
}
/** A bounded turn; future effects are driven by saved records and due work, not an open browser. */
export async function coordinateHandoff(client: Client, handoffId: string, commandId: string, currentUserId: string,
  dependencies: CoordinatorDependencies = {}): Promise<HandoffEdit[]> {
  const caller = await currentCaller(client, currentUserId), wallTime = instant(dependencies.now ?? new Date().toISOString());
  const { handoff: savedHandoff, workspace } = await loadHandoff(client, handoffId, caller, "work");
  const work = await loadAgentWork(client, savedHandoff, workspace, caller);
  if (work.status !== "Ready to continue" && work.status !== "Plan requested"
    && (!work.nextWakeAt || instant(work.nextWakeAt) > wallTime)) return [];
  const now = businessMoment(work, savedHandoff.businessDate!, wallTime);
  const handoff = { ...savedHandoff, businessDate: now.slice(0, 10) };
  const intent = command(workspace.workspaceId, handoffId, handoffId, commandId, caller.id, "Handoff continued", { handoffId });
  if (await wasApplied(client, workspace, caller, intent)) return [];
  const [world, records, currentPlan, funding] = await Promise.all([
    loadDetails(client, handoff, workspace, caller), loadDeliveryRecords(client, workspace, caller, handoff),
    handoff.workPlanId ? one(client(HandoffWorkPlan).where({ workPlanId: { $eq: handoff.workPlanId } })) : Promise.resolve(undefined),
    bounded(client(HandoffFunding).where({ workspaceId: { $eq: workspace.workspaceId }, propertyId: { $eq: handoff.propertyId! } })),
  ]);
  [...funding, ...(currentPlan ? [currentPlan] : [])].forEach((row) => inWorkspace(row, workspace, caller));
  const batch = createEditBatch<HandoffEdit>(client), context: DeliveryContext = { client, batch, workspace, caller, handoff, now, recordedAt: now };
  const revision = nextRevision(handoff.revision);
  const soon = new Date(Date.parse(now) + 1000).toISOString();
  const unanswered = records.messages.filter((message) => message.direction === "Incoming" && ["Information", "Funding"].includes(message.purpose ?? "")
    && message.detailsJson && (parseDetails(message.detailsJson, "Reply") as Record<string, unknown>).unanswered === true
    && !records.messages.some((later) => later.direction === "Outgoing" && later.detailsJson
      && (parseDetails(later.detailsJson, "Follow-up") as Record<string, unknown>).previousReplyId === message.messageId));
  const nextDue = (): string | undefined => {
    const pending = records.messages.filter((message) => message.direction === "Outgoing" && message.responseDueAt
      && !records.messages.some((reply) => reply.messageId === providerResponseId(workspace.workspaceId, message.messageId))).map((message) => message.responseDueAt!);
    pending.push(...records.jobs.filter((job) => job.nextResponseAt).map((job) => job.nextResponseAt!));
    pending.push(...records.jobs.filter((job) => job.status === "Scheduled" && job.appointmentEndsAt).map((job) => job.appointmentEndsAt!));
    pending.push(...records.payments.filter((payment) => payment.status === "Requested").map((payment) => {
      const sourceId = funding.find((item) => item.fundingId === payment.fundingId)?.sourceDocumentId;
      const document = world.documents.find((doc) => doc.documentId === sourceId && doc.kind === "Owner funding" && doc.detailsJson);
      return afterMinutes(payment.requestedAt!, document ? fundingInformation(document).responseMinutes : 1);
    }));
    pending.push(...unanswered.map((reply) => reply.responseDueAt ?? afterMinutes(reply.createdAt!, 1440)));
    return pending.map((dueAt) => instant(dueAt)).filter((dueAt) => dueAt > now).sort()[0];
  };
  // The first reasoning turn after an operator message answers it in the conversation, once, as a saved message.
  const answered = new Set(records.messages.map((message) => message.messageId));
  const reply = (summary: string): void => {
    if (!work.operationKey?.startsWith("message:")) return;
    const operatorMessageId = work.operationKey.slice("message:".length);
    const replyId = reference("message", workspace.workspaceId, operatorMessageId, "handoff-reply");
    if (answered.has(replyId) || !records.messages.some((message) => message.messageId === operatorMessageId && message.direction === "Operator")) return;
    answered.add(replyId);
    batch.create(HandoffMessage, { workspaceId: workspace.workspaceId, readerIds: [...workspace.readerIds!], handoffId, messageId: replyId,
      replyToMessageId: operatorMessageId, title: "Handoff", body: summary, direction: "Handoff", purpose: "Discussion", status: "Sent", createdAt: now });
  };
  const finish = (summary: string, nextWakeAt: string | undefined = soon, status = "Ready to continue", operationKey?: string): HandoffEdit[] => {
    batch.update(savedHandoff, { revision, nextStep: summary, businessDate: handoff.businessDate });
    batch.update(work, { title: "Continue the handoff", status, nextStep: summary, updatedAt: wallTime, businessTime: now, nextBusinessAt: nextWakeAt, nextWakeAt: wakeTime(wallTime, now, nextWakeAt),
      operationKey: operationKey ?? work.operationKey });
    // Delivery helpers may already have touched the shared authority record.
    if (!batch.getEdits().some((edit) => edit.type === "updateObject" && edit.obj.$apiName === "HandoffWorkspace")) guardWorkspace(batch, workspace, commandId);
    addActivity(batch, intent, [...workspace.readerIds!], "Handoff progressed", summary, revision, now);
    return batch.getEdits();
  };
  const nameOf = (partyId?: string): string => world.parties.find((party) => party.partyId === partyId)?.name ?? "The vendor";
  const jobVendor = (jobId?: string): string => nameOf(records.jobs.find((job) => job.jobId === jobId)?.providerPartyId);
  if (await recognizeSourceRecord(context, world, records)) return finish("Checked a new work record against its source document.");
  const mappingNeedsFunds = world.documents.some((doc) => doc.kind === "Accepted work mapping")
    && world.documents.find((doc) => doc.kind === "Owner funding" && doc.detailsJson && fundingInformation(doc).confirmedAt <= now
      && !funding.some((item) => item.sourceSystem === (doc.sourceSystem ?? "Owner funding confirmation") && item.sourceRecordId === (doc.sourceRecordId ?? doc.documentId)));
  if (mappingNeedsFunds) {
    const info = fundingInformation(mappingNeedsFunds);
    await recordOwnerFunding(context, { title: mappingNeedsFunds.title!, ownerPartyId: info.ownerPartyId, currency: info.currency,
      confirmedCents: info.confirmedCents, confirmedAt: info.confirmedAt, sourceSystem: mappingNeedsFunds.sourceSystem ?? "Owner funding confirmation",
      sourceRecordId: mappingNeedsFunds.sourceRecordId ?? mappingNeedsFunds.documentId, sourceDocumentId: mappingNeedsFunds.documentId });
    return finish("Recorded the owner's funds for the work already ordered.");
  }
  if (await recognizeAcceptedWork(context, world, records)) return finish("Recorded the earlier accepted work request. Its vendor correspondence continues.");
  // Incoming results remain recognizable even when new commitments have been paused.
  const paid = await respondToPayment(context, records, world);
  if (paid) {
    const vendor = jobVendor(paid.jobId), amount = formatAmount(paid.amountCents, paid.currency), what = paid.purpose === "Advance" ? "advance" : "invoice";
    return finish(paid.status === "Settled" ? (what === "advance" ? `Paid ${vendor}'s ${amount} advance.` : `Paid ${vendor} ${amount} on its invoice.`)
      : paid.status === "Failed" ? `The ${amount} ${what} payment to ${vendor} failed. It needs your attention.`
        : `The ${amount} ${what} payment to ${vendor} is still being confirmed.`);
  }
  const due = dueProviderRequests(records, now)[0];
  if (due) {
    const request = records.messages.find((message) => message.messageId === due.requestId)!;
    if (["Information", "Funding"].includes(request.purpose ?? "") || (request.purpose === "Quote" && request.detailsJson?.includes('"serviceId"'))) {
      await answerInquiry(context, due.requestId, records, world);
      return finish(request.purpose === "Quote" ? `${nameOf(request.recipientPartyId)} sent a quote.` : `${nameOf(request.recipientPartyId)} replied.`);
    }
    const result = await respondToProviderRequest(context, due.requestId);
    return finish(providerUpdate(result, nameOf(request.recipientPartyId)));
  }
  const reminder = unanswered.find((reply) => instant(reply.responseDueAt ?? afterMinutes(reply.createdAt!, 1440)) <= now);
  if (reminder) {
    const request = records.messages.find((message) => message.messageId === reminder.replyToMessageId);
    requireHandoff(request?.detailsJson, "The original question is unavailable.");
    const before = batch.getEdits().length;
    await queueInquiry(context, { ...readInquiry(parseDetails(request.detailsJson, "Question")), previousReplyId: reminder.messageId });
    if (batch.getEdits().length > before) return finish(`Followed up with ${nameOf(request.recipientPartyId)}, who hasn't answered yet.`);
    // No new source facts: do not claim another send or keep an expired reminder spinning.

  }
  const observed = records.inspections.find((report) => report.jobId && report.purpose === "Completion check"
    && records.jobs.some((job) => job.jobId === report.jobId && job.verificationInspectionId !== report.inspectionId
      && (!job.verificationInspectionId || instant(report.observedAt) > instant(records.inspections.find((earlier) => earlier.inspectionId === job.verificationInspectionId)?.observedAt))));
  if (observed) {
    const status = await checkJobCompletion(context, observed.jobId!, observed.inspectionId);
    const vendor = jobVendor(observed.jobId);
    return finish(status === "Complete" ? `Checked ${vendor}'s report. The work is complete.`
      : status === "Needs attention" ? `${vendor}'s report shows work still to fix.` : `${vendor}'s report doesn't cover all the work yet.`);
  }
  const dueJob = records.jobs.find((job) => job.status === "Scheduled" && job.appointmentEndsAt && instant(job.appointmentEndsAt) <= now
    && !records.inspections.some((report) => report.jobId === job.jobId));
  if (dueJob?.fundingId && deliverScheduledJob(context, dueJob, world, records, funding.find((item) => item.fundingId === dueJob.fundingId)?.ownerPartyId)) return finish(`${nameOf(dueJob.providerPartyId)} sent the report and invoice.`);
  let blocked: string | undefined;
  if (handoff.status === "Open") {
    const unscheduled = records.jobs.find((job) => job.status === "Commissioned" && !job.appointmentAt
      && job.requestMessageId && !records.messages.some((message) => message.jobId === job.jobId && message.direction === "Outgoing" && message.purpose === "Appointment"));
    if (unscheduled) {
      const acknowledgment = records.messages.find((message) => message.messageId === reference("message", workspace.workspaceId, `continue:${unscheduled.decisionId}`, "acknowledgement"));
      if (acknowledgment) {
        await queueProviderRequest(context, { purpose: "Appointment", providerPartyId: unscheduled.providerPartyId!, quoteId: unscheduled.quoteId!,
          scopeLineIds: jobScope(unscheduled).map((line) => line.lineId), jobId: unscheduled.jobId, previousReplyId: acknowledgment.messageId });
        return finish(`Asked ${nameOf(unscheduled.providerPartyId)} to confirm the visit time.`);
      }
    }
    const unfunded = records.jobs.find((job) => job.origin === "Handoff" && !job.fundingId && job.status !== "Cancelled");
    if (unfunded) {
      const mapping = world.documents.find((doc) => doc.documentId === unfunded.sourceDocumentId && doc.kind === "Accepted work mapping");
      const preferred = mapping?.detailsJson ? sourceDetails(mapping.detailsJson).fundingId : undefined;
      const candidates = funding.filter((item) => item.currency === unfunded.currency && (preferred === undefined || item.fundingId === preferred));
      for (const candidate of candidates) {
        const available = await loadOwnerFunding(context, candidate.fundingId);
        if (BigInt(available.position.availableCents) < BigInt(unfunded.committedCents!)) continue;
        await bindExistingJobFunding(context, unfunded.jobId, candidate.fundingId);
        return finish(`Confirmed owner funds now cover the work ordered from ${nameOf(unfunded.providerPartyId)}.`);
      }
      await queueInquiry(context, { purpose: "Funding", recipientPartyId: candidates[0]?.ownerPartyId ?? world.tenancy.landlordPartyId!,
        question: `Please confirm an owner allocation covering the existing commitment for ${unfunded.title} (${formatAmount(unfunded.committedCents, unfunded.currency!)}). The work is already accepted; this is a funding question, not a request for another approval.` });
      const queuedDue = batch.getEdits().flatMap((edit) => edit.type === "createObject" && edit.obj.apiName === "HandoffMessage"
        && typeof Reflect.get(edit.properties, "responseDueAt") === "string" ? [Reflect.get(edit.properties, "responseDueAt") as string] : []);
      const pendingDue = nextDue();
      return finish(`Waiting for the owner to confirm funds for ${unfunded.title} (${formatAmount(unfunded.committedCents, unfunded.currency!)}).`,
        [...queuedDue, ...(pendingDue && pendingDue > now ? [pendingDue] : [])].sort()[0], "Waiting for funding");
    }
    const advanceJob = records.jobs.find((job) => job.origin === "Handoff" && job.fundingId && ["Commissioned", "Awaiting advance"].includes(job.status ?? "")
      && BigInt(job.depositCents ?? "0") > 0n && !records.payments.some((payment) => payment.jobId === job.jobId));
    if (advanceJob) { await requestProviderPayment(context, advanceJob.jobId, "Advance"); return finish(`Requested the ${formatAmount(advanceJob.depositCents!, advanceJob.currency!)} advance for ${nameOf(advanceJob.providerPartyId)}.`); }
    const readyJob = records.jobs.find((job) => job.status === "Awaiting advance"
      && records.payments.some((payment) => payment.jobId === job.jobId && payment.purpose === "Advance" && payment.status === "Settled")
      && !records.messages.some((message) => message.jobId === job.jobId && message.direction === "Outgoing" && message.purpose === "Appointment"
        && !records.messages.some((reply) => reply.messageId === providerResponseId(workspace.workspaceId, message.messageId))));
    if (readyJob) {
      const earlier = records.messages.filter((message) => message.direction === "Incoming" && message.jobId === readyJob.jobId && message.purpose === "Appointment")
        .sort((a, b) => (b.createdAt ? instant(b.createdAt) : "").localeCompare(a.createdAt ? instant(a.createdAt) : ""))[0];
      await queueProviderRequest(context, { purpose: "Appointment", providerPartyId: readyJob.providerPartyId!, quoteId: readyJob.quoteId!,
        scopeLineIds: jobScope(readyJob).map((line) => line.lineId), jobId: readyJob.jobId, previousReplyId: earlier?.messageId });
      return finish(`The advance to ${nameOf(readyJob.providerPartyId)} is paid. Asked them to book the visit.`);
    }
    const invoice = records.invoices.find((item) => ["Received", "Agreed"].includes(item.status ?? "")
      && records.jobs.some((job) => job.jobId === item.jobId && job.status === "Complete" && job.origin === "Handoff" && job.fundingId)
      && !records.payments.some((payment) => payment.jobId === item.jobId && (payment.purpose === "Invoice" || ["Requested", "Confirming"].includes(payment.status ?? "")))
      && BigInt(item.totalCents!) > records.payments.filter((payment) => payment.jobId === item.jobId && payment.status === "Settled").reduce((sum, payment) => sum + BigInt(payment.amountCents!), 0n));
    if (invoice) { await requestProviderPayment(context, invoice.jobId!, "Invoice", invoice.invoiceId); return finish(`Requested payment of ${nameOf(invoice.providerPartyId)}'s invoice.`); }
    const acceptedId = handoff.operativeDecisionId ?? currentPlan?.acceptedDecisionId;
    const decision = acceptedId ? await one(client(HandoffDecision).where({ decisionId: { $eq: acceptedId } })) : undefined;
    if (decision) {
      inWorkspace(decision, workspace, caller);
      const plan = currentPlan?.workPlanId === decision.workPlanId ? currentPlan : await one(client(HandoffWorkPlan).where({ workPlanId: { $eq: decision.workPlanId! } }));
      requireHandoff(plan && decision.contentJson === acceptedContent(plan), "The accepted work no longer matches its saved decision.");
      inWorkspace(plan, workspace, caller);
      const selections = planSelections(plan), quoteId = selections.find((line) => !records.jobs.some((job) => job.quoteId === line.quoteId
        && jobScope(job).some((scope) => scope.lineId === line.quoteLineId)))?.quoteId;
      if (quoteId) {
        const quote = records.quotes.find((item) => item.quoteId === quoteId);
        const cost = selectedCost(selections.filter((line) => line.quoteId === quoteId), records.quotes, plan.currency!);
        const positions = await Promise.all(funding.filter((item) => item.currency === plan.currency).map((item) => loadOwnerFunding(context, item.fundingId)));
        const available = positions.find((item) => BigInt(item.position.availableCents) >= BigInt(cost));
        const funds = available?.funding, position = available?.position;
        if (funds && position && BigInt(position.availableCents) >= BigInt(cost) && quote?.status === "Offered" && instant(quote.validUntil) >= now
          && (!plan.sourceBasis || records.jobs.some((job) => job.decisionId === decision.decisionId) || plan.sourceBasis === materialBasis(handoff, workspace, world))) {
          await commissionJob(context, { workPlanId: plan.workPlanId, expectedRevision: plan.revision!, quoteId, fundingId: funds.fundingId,
            scope: selections.filter((line) => line.quoteId === quoteId).map((line) => ({ quoteLineId: line.quoteLineId, acceptedScope: line.scope })) });
          return finish(`Ordered ${quote!.title} from ${nameOf(quote!.providerPartyId)} for ${formatAmount(cost, plan.currency!)}.`);
        }
        const confirmation = world.documents.find((doc) => doc.kind === "Owner funding" && doc.detailsJson
          && !funding.some((item) => item.sourceSystem === (doc.sourceSystem ?? "Owner funding confirmation") && item.sourceRecordId === (doc.sourceRecordId ?? doc.documentId)));
        if (confirmation && !funds) {
          const info = fundingInformation(confirmation);
          await recordOwnerFunding(context, { title: confirmation.title!, ownerPartyId: info.ownerPartyId, currency: info.currency,
            confirmedCents: info.confirmedCents, confirmedAt: info.confirmedAt, sourceSystem: confirmation.sourceSystem ?? "Owner funding confirmation",
            sourceRecordId: confirmation.sourceRecordId ?? confirmation.documentId, sourceDocumentId: confirmation.documentId });
          return finish("Recorded the owner's funding confirmation.");
        }
        // Say why accepted work cannot be ordered; reasoning below may still obtain a current offer.
        const vendor = world.parties.find((party) => party.partyId === quote?.providerPartyId)?.name ?? "the vendor";
        blocked = `The accepted work can't be ordered yet. ${!quote || quote.status !== "Offered" || instant(quote.validUntil) < now
          ? `The offer from ${vendor} is no longer valid. Ask them for a current offer.`
          : !funds ? `The confirmed owner funds don't cover the ${formatAmount(cost, plan.currency!)} order for ${vendor}.`
            : "The case records changed after the plan was accepted. Review the plan before the work is ordered."}`;
      }
    }
  }
  const pendingAt = nextDue();
  if (pendingAt && pendingAt > now && (records.jobs.some((job) => ["Commissioned", "Scheduled", "Awaiting advance"].includes(job.status ?? ""))
    || records.payments.some((payment) => payment.status === "Requested"))
    && !records.messages.some((message) => message.direction === "Operator" && instant(message.createdAt) > caseTime(work, work.updatedAt!))) {
    // Booked visits are named with their date; only vendors still to book or be paid an advance are "waited on".
    const open = records.jobs.filter((job) => ["Commissioned", "Scheduled", "Awaiting advance"].includes(job.status ?? ""));
    const summary = deliveryStatus(open.map((job) => ({ vendor: nameOf(job.providerPartyId), status: job.status ?? "",
      appointmentAt: job.appointmentAt ? instant(job.appointmentAt) : undefined, appointmentEndsAt: job.appointmentEndsAt ? instant(job.appointmentEndsAt) : undefined })), now);
    return finish(summary, pendingAt, "Waiting for provider");
  }
  const basis = materialBasis(handoff, workspace, world);
  const reasoningKey = `reason:${digest({ basis, planId: currentPlan?.workPlanId, planRevision: currentPlan?.revision,
    funding: funding.map((item) => [item.fundingId, item.revision, item.confirmedCents]),
    jobs: records.jobs.map((job) => [job.jobId, job.status, job.revision]), quotes: records.quotes.map((quote) => [quote.quoteId, quote.status]),
    messages: records.messages.filter((message) => message.direction !== "Handoff").map((message) => message.messageId), payments: records.payments.map((payment) => [payment.paymentId, payment.status]) })}`;
  if (work.operationKey === reasoningKey) {
    if (work.nextWakeAt && instant(work.nextWakeAt) <= wallTime) {
      const dueAt = nextDue();
      batch.update(work, { businessTime: now, updatedAt: wallTime, nextBusinessAt: dueAt && dueAt > now ? dueAt : undefined,
        nextWakeAt: wakeTime(wallTime, now, dueAt && dueAt > now ? dueAt : undefined) });
      return batch.getEdits();
    }
    return [];
  }
  if (currentPlan?.status === "Ready" && work.status === "Waiting for decision" && currentPlan.sourceBasis === basis
    && !records.jobs.length && !records.messages.some((message) => message.direction === "Operator" && instant(message.createdAt) > caseTime(work, work.updatedAt!))) {
    const dueAt = nextDue();
    batch.update(work, { businessTime: now, updatedAt: wallTime, nextBusinessAt: dueAt, nextWakeAt: wakeTime(wallTime, now, dueAt) });
    return batch.getEdits();
  }
  if (handoff.status !== "Open") return finish("New work is paused. Work already ordered continues.", nextDue(), "Paused", reasoningKey);
  requireHandoff(workspace.modelRid === Aliases.model("workReasoner").rid, "Ask the workspace owner to select the available reasoning service.");
  const model = dependencies.model ?? await createFoundryWorkModel(client, { modelAlias: "workReasoner" });
  let recommendation: CoordinatorRecommendation | undefined;
  try {
    recommendation = await reasonNextWork(handoff, workspace, world, records, currentPlan ? {
      ...planDraft(currentPlan), selections: planSelections(currentPlan), status: currentPlan.status, fixedProviderPartyId: currentPlan.fixedProviderPartyId ?? null,
    } : null, model);
  } catch (error: unknown) {
    if (!(error instanceof RecommendationValidationExhausted)) throw error;
    // Recovery is limited to checked model-output failures. Authority, source and service errors propagate.
  }
  const latest = await loadHandoff(client, handoffId, caller, "work");
  const latestBusinessHandoff = { ...latest.handoff, businessDate: handoff.businessDate };
  const [latestWorld, latestWork] = await Promise.all([loadDetails(client, latestBusinessHandoff, latest.workspace, caller), loadAgentWork(client, latest.handoff, latest.workspace, caller)]);
  requireHandoff(basis === materialBasis(latestBusinessHandoff, latest.workspace, latestWorld) && savedHandoff.businessDate === latest.handoff.businessDate
    && handoff.workPlanId === latest.handoff.workPlanId && instant(work.updatedAt) === instant(latestWork.updatedAt) && work.operationKey === latestWork.operationKey,
  "The material facts or current request changed while Handoff was reasoning. Reconsider the latest information.");
  if (currentPlan) {
    const latestPlan = await one(client(HandoffWorkPlan).where({ workPlanId: { $eq: currentPlan.workPlanId } }));
    requireHandoff(latestPlan && latestPlan.revision === currentPlan.revision && latestPlan.status === currentPlan.status,
      "The work proposal changed while Handoff was reasoning. Review the latest proposal.");
  }
  if (!recommendation) {
    const summary = "Handoff couldn't finish a plan this time, so nothing new was proposed or ordered. Work already ordered carries on. Send a message to try again.";
    // No model-only wake: unchanged failed input must not incur another minute-by-minute model call.
    // Real provider/payment work keeps its own due time and still runs before reasoning on the next turn.
    const nextBusinessAt = nextDue();
    batch.update(savedHandoff, { revision, nextStep: summary, businessDate: handoff.businessDate });
    batch.update(work, { status: "Recommendation unavailable", title: "Continue the handoff", nextStep: summary,
      operationKey: reasoningKey, updatedAt: wallTime, businessTime: now, nextBusinessAt,
      nextWakeAt: wakeTime(wallTime, now, nextBusinessAt) });
    guardWorkspace(batch, latest.workspace, commandId);
    reply(summary);
    addActivity(batch, intent, [...workspace.readerIds!], "Recommendation unavailable", summary, revision, now);
    return batch.getEdits();
  }
  // A trade quotes against the assessment: every quote request carries the reports of completed assessments.
  const assessmentReports = records.jobs.filter((job) => job.kind === "Assessment" && job.status === "Complete")
    .flatMap((job) => records.inspections.filter((report) => report.jobId === job.jobId).map((report) => report.sourceDocumentId))
    .filter((id): id is string => typeof id === "string" && world.documents.some((doc) => doc.documentId === id));
  for (const inquiry of recommendation.requests) await queueInquiry(context, inquiry, inquiry.purpose === "Quote" ? assessmentReports : []);
  let status = currentPlan?.status === "Ready" ? "Waiting for decision" : "Waiting for information", nextWakeAt = nextDue();
  if (nextWakeAt && nextWakeAt <= now) nextWakeAt = undefined;
  const newReplyTimes = batch.getEdits().flatMap((edit) => {
    if (edit.type !== "createObject" || edit.obj.apiName !== "HandoffMessage") return [];
    const due = Reflect.get(edit.properties, "responseDueAt") as unknown;
    return typeof due === "string" ? [due] : [];
  });
  nextWakeAt = [...newReplyTimes, ...(nextWakeAt ? [nextWakeAt] : [])].sort()[0];
  if (recommendation.proposal) {
    const { selections, fixedProviderPartyId, ...draft } = recommendation.proposal;
    // A proposed budget does not exceed the owner funds still available when the quoted work fits within them.
    const recorded = await Promise.all(funding.filter((item) => item.currency === draft.currency).map((item) => loadOwnerFunding(context, item.fundingId, false)));
    const available = recorded.length ? recorded.reduce((sum, item) => sum + BigInt(item.position.availableCents), 0n)
      : world.documents.filter((doc) => doc.kind === "Owner funding" && doc.detailsJson).map(fundingInformation)
        .filter((info) => info.currency === draft.currency).reduce((sum, info) => sum + BigInt(info.confirmedCents), 0n);
    if (available > 0n && BigInt(draft.budgetCents) > available && BigInt(draft.estimatedCostCents) <= available) draft.budgetCents = available.toString();
    // The reasoning model cannot manufacture an explicitly required provider.
    requireHandoff(!fixedProviderPartyId || fixedProviderPartyId === currentPlan?.fixedProviderPartyId,
      "A required provider must come from an explicit operator choice.");
    const replace = currentPlan?.status === "Ready";
    const workPlanId = replace ? currentPlan.workPlanId : reference("plan", workspace.workspaceId, handoffId, digest({ basis, draft, selections }));
    const props = { ...draft, selectionJson: orderedJson(selections), fixedProviderPartyId, sourceBasis: basis,
      revision: replace ? nextRevision(currentPlan.revision) : "1", basisRevision: revision, status: "Ready" };
    if (replace) batch.update(currentPlan, props);
    else batch.create(HandoffWorkPlan, { ...props, workPlanId, workspaceId: workspace.workspaceId, readerIds: [...workspace.readerIds!], handoffId });
    batch.update(handoff, { workPlanId, physicalProgress: "Plan ready", operativeDecisionId: handoff.operativeDecisionId ?? currentPlan?.acceptedDecisionId });
    status = "Waiting for decision";
  }
  // Accepted work that cannot be ordered, with nothing new proposed or asked, waits for the operator with the reason.
  const unpaid = records.payments.some((payment) => payment.status === "Requested");
  const stepSummary = recommendation.propertyReady
    ? `All work is complete and checked. The unit is ready for the next tenant.${unpaid ? " Invoice payments are still being confirmed." : ""}`
    : blocked && !recommendation.proposal && !recommendation.requests.length ? blocked : recommendation.summary;
  if (stepSummary === blocked) status = "Needs attention";
  if (recommendation.propertyReady) {
    const condition = latestCondition(world.documents);
    requireHandoff(condition && readinessCoverage(condition, handoff.goal!)
      && recommendation.trace.usedDocumentIds.includes(condition.documentId) && propertyConditions(condition).every((item) => item.state === "Satisfied" && item.accessible)
      && records.jobs.length > 0 && records.jobs.every((job) => job.status === "Complete")
      && (world.tenancy.endingKind ?? "Tenancy ending") === "Tenancy ending" && !recommendation.proposal,
    "The property still needs supporting completion observations or remaining work.");
    batch.update(handoff, { physicalProgress: "Ready" });
    status = "Complete";
  }
  batch.update(savedHandoff, { revision, nextStep: stepSummary, businessDate: handoff.businessDate });
  batch.update(work, { status, title: "Continue the handoff", nextStep: stepSummary, operationKey: reasoningKey, updatedAt: wallTime, businessTime: now, nextBusinessAt: nextWakeAt, nextWakeAt: wakeTime(wallTime, now, nextWakeAt) });
  if (!batch.getEdits().some((edit) => edit.type === "updateObject" && edit.obj.$apiName === "HandoffWorkspace")) guardWorkspace(batch, latest.workspace, commandId);
  reply(stepSummary);
  addActivity(batch, intent, [...workspace.readerIds!], recommendation.proposal ? "Work plan ready" : stepSummary === blocked ? "Work can't be ordered" : "Handoff next step", stepSummary, revision, now, recommendation.trace);
  return batch.getEdits();
}
