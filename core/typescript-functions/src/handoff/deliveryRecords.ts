import { HandoffJob, HandoffInspection, HandoffQuote, HandoffInvoice, HandoffPayment,
  HandoffDocument, HandoffParty, HandoffMessage } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import type { EditBatch } from "@osdk/functions";
import { authorize, bounded, historyRecords, guardWorkspace, inWorkspace, one, type Caller, type Handoff,
  type HandoffEdit, type Workspace } from "./records.js";
import { details, digest, orderedJson, parseDetails, reference, requireHandoff, words } from "./values.js";
import { currencyCode, findings, instant, money, quoteLines, scopeLines, sourceRecord,
  type ExistingJob, type InspectionReport, type QuoteOffer, type ScopeLine, type SourceRecord, type SupplierInvoice } from "./deliveryContracts.js";
import { invoiceMatchesJob, sumQuotedCosts, validateQuoteOffer } from "./quoteCosts.js";

/** Internal server context. The Action obtains caller with currentCaller; never expose this as model input. */
export interface DeliveryContext {
  client: Client; batch: EditBatch<HandoffEdit>; workspace: Workspace; caller: Caller; handoff: Handoff; now: string; recordedAt?: string;
}
export type Job = Osdk.Instance<HandoffJob>;
export type Quote = Osdk.Instance<HandoffQuote>;
export type Inspection = Osdk.Instance<HandoffInspection>;
export type Invoice = Osdk.Instance<HandoffInvoice>;
export type Payment = Osdk.Instance<HandoffPayment>;
export interface DeliveryRecords {
  jobs: Job[]; quotes: Quote[]; inspections: Inspection[]; invoices: Invoice[];
  payments: Payment[]; messages: Osdk.Instance<HandoffMessage>[];
}
export function deliveryAccess(context: DeliveryContext): { workspaceId: string; readerIds: string[]; handoffId: string; propertyId: string } {
  authorize(context.workspace, context.caller, "work");
  inWorkspace(context.handoff, context.workspace, context.caller);
  instant(context.now);
  return { workspaceId: context.workspace.workspaceId, readerIds: [...context.workspace.readerIds!],
    handoffId: context.handoff.handoffId, propertyId: words(context.handoff.propertyId, "Property", 160) };
}
export function sourceIdentity(kind: string, workspaceId: string, source: Pick<SourceRecord, "sourceSystem" | "sourceRecordId">): string {
  return reference(kind, workspaceId, words(source.sourceSystem, "Source system", 160), words(source.sourceRecordId, "Source reference", 200));
}
/** Validate every record before returning content to either the model or an operator. */
export async function loadDeliveryRecords(client: Client, workspace: Workspace, caller: Caller, handoff: Handoff, includeMessages = true): Promise<DeliveryRecords> {
  authorize(workspace, caller, "read"); inWorkspace(handoff, workspace, caller);
  const filter = { workspaceId: { $eq: workspace.workspaceId }, handoffId: { $eq: handoff.handoffId } };
  const [jobs, quotes, inspections, invoices, payments, messages] = await Promise.all([
    bounded(client(HandoffJob).where(filter)), bounded(client(HandoffQuote).where(filter)),
    bounded(client(HandoffInspection).where(filter)), bounded(client(HandoffInvoice).where(filter)),
    bounded(client(HandoffPayment).where(filter)), includeMessages ? historyRecords(client(HandoffMessage).where(filter)) : Promise.resolve([]),
  ]);
  [...jobs, ...quotes, ...inspections, ...invoices, ...payments, ...messages].forEach((row) => inWorkspace(row, workspace, caller));
  return { jobs, quotes, inspections, invoices, payments, messages };
}
export async function deliveryJob(context: DeliveryContext, jobId: string): Promise<Job> {
  deliveryAccess(context);
  const job = await one(context.client(HandoffJob).where({ jobId: { $eq: words(jobId, "Job", 160) } }));
  requireHandoff(job, "This job is not available."); inWorkspace(job, context.workspace, context.caller);
  requireHandoff(job.handoffId === context.handoff.handoffId && job.propertyId === context.handoff.propertyId,
    "The job belongs to a different handoff or property.");
  return job;
}
export async function deliveryQuote(context: DeliveryContext, quoteId: string): Promise<Quote> {
  deliveryAccess(context);
  const quote = await one(context.client(HandoffQuote).where({ quoteId: { $eq: words(quoteId, "Quote", 160) } }));
  requireHandoff(quote, "This offer is not available."); inWorkspace(quote, context.workspace, context.caller);
  requireHandoff(quote.handoffId === context.handoff.handoffId && quote.propertyId === context.handoff.propertyId,
    "The offer belongs to a different handoff or property.");
  return quote;
}
export function offerFromRecord(quote: Quote): QuoteOffer {
  return validateQuoteOffer({ sourceSystem: quote.sourceSystem, sourceRecordId: quote.sourceRecordId,
    sourceDocumentId: quote.sourceDocumentId, title: quote.title, providerPartyId: quote.providerPartyId,
    kind: quote.kind, currency: quote.currency, lines: parseDetails(words(quote.linesJson, "Quoted lines", 100000), "Quoted lines"),
    totalCents: quote.totalCents, depositCents: quote.depositCents, paymentTerms: quote.paymentTerms,
    requirements: quote.requirements, availableFrom: quote.availableFrom, validUntil: quote.validUntil,
    durationMinutes: quote.durationMinutes, responseMinutes: quote.responseMinutes });
}
export function jobScope(job: Job): ScopeLine[] {
  const parsed = parseDetails(words(job.scopeJson, "Job scope", 100000), "Job scope");
  if (job.origin === "Existing") return quoteLines(parsed).map((line) => ({ ...line, acceptedScope: line.description }));
  return scopeLines(parsed);
}
export async function requireDeliverySource(context: DeliveryContext, documentId: string, partyIds: string[]): Promise<Osdk.Instance<HandoffDocument>> {
  const [document, parties] = await Promise.all([
    one(context.client(HandoffDocument).where({ documentId: { $eq: words(documentId, "Source document", 160) } })),
    bounded(context.client(HandoffParty).where({ partyId: { $in: [...new Set(partyIds)] }, workspaceId: { $eq: context.workspace.workspaceId } }), 32),
  ]);
  requireHandoff(document && parties.length === new Set(partyIds).size, "The source document and named parties must be available.");
  [document, ...parties].forEach((row) => inWorkspace(row, context.workspace, context.caller));
  requireHandoff(document.handoffId === context.handoff.handoffId, "Use a source linked to this handoff.");
  return document;
}
/** Only call-site-declared timestamp properties have instant semantics. In particular, a
 * document's availableFrom is a calendar date, unlike a quote's availableFrom timestamp.
 * Do not normalize source JSON, version identities, money, or other string properties. */
export type RecordTimestampKey = "confirmedAt" | "availableFrom" | "validUntil" | "createdAt"
  | "observedAt" | "issuedAt" | "dueAt" | "responseDueAt";
/** Same identity with changed content is not a retry. Never overwrite an issued or historical record. */
export function sameRecord(record: object, expected: object, ignored: string[] = [], timestampKeys: readonly RecordTimestampKey[] = []): void {
  const comparable = (key: string, value: unknown): unknown =>
    timestampKeys.some((field) => field === key) && value !== undefined && value !== null ? instant(value) : value;
  requireHandoff(Object.entries(expected).every(([key, value]) => ignored.includes(key)
    || orderedJson(comparable(key, Reflect.get(record, key))) === orderedJson(comparable(key, value))),
  "This source reference already has different saved details. Keep the original and record the correction separately.");
}
export function touchDelivery(context: DeliveryContext, key: string): void {
  const alreadyTouched = context.batch.getEdits().some((edit) => edit.type === "updateObject"
    && edit.obj.$apiName === "HandoffWorkspace" && edit.obj.$primaryKey === context.workspace.workspaceId);
  if (!alreadyTouched) guardWorkspace(context.batch, context.workspace, key);
}
/** Searches cannot see an earlier edit in this batch. Repeated ingestion must not create another record. */
export function pendingDeliveryRecord(context: DeliveryContext, apiName: string, id: string, expected: object, timestampKeys: readonly RecordTimestampKey[] = []): boolean {
  const pending = context.batch.getEdits().find((edit) => edit.type === "createObject" && edit.obj.apiName === apiName
    && Reflect.get(edit.properties, edit.obj.primaryKeyApiName!) === id);
  if (!pending || pending.type !== "createObject") return false;
  sameRecord(pending.properties, expected, ["recordedAt", "updatedAt"], timestampKeys);
  return true;
}
/** A commitment or payment must use committed balances, not another helper's invisible in-flight edits. */
export function requireSavedFinancialState(context: DeliveryContext): void {
  const changed = context.batch.getEdits().some((edit) => {
    const apiName = edit.type === "createObject" ? edit.obj.apiName : edit.type === "updateObject" ? edit.obj.$apiName : "";
    return ["HandoffJob", "HandoffFunding", "HandoffPayment", "HandoffWorkPlan"].includes(apiName);
  });
  requireHandoff(!changed, "Save the earlier work or money change before making another commitment or payment.");
}

export async function recordQuote(context: DeliveryContext, input: unknown): Promise<string> {
  const shared = deliveryAccess(context), offer = validateQuoteOffer(input);
  const source = await requireDeliverySource(context, offer.sourceDocumentId, [offer.providerPartyId]);
  requireHandoff(source.kind === "Quote" && source.partyId === offer.providerPartyId,
    "The quote document must identify the provider making this offer.");
  const quoteId = sourceIdentity("quote", shared.workspaceId, offer);
  const props = { ...shared, quoteId, ...offer, lines: undefined, linesJson: orderedJson(offer.lines), status: "Offered", recordedAt: context.now };
  const { lines: _lines, ...saved } = props;
  if (pendingDeliveryRecord(context, "HandoffQuote", quoteId, saved, ["availableFrom", "validUntil"])) return quoteId;
  const prior = await one(context.client(HandoffQuote).where({ quoteId: { $eq: quoteId } }));
  if (prior) { inWorkspace(prior, context.workspace, context.caller); sameRecord(prior, saved, ["recordedAt", "status"], ["availableFrom", "validUntil"]); return quoteId; }
  context.batch.create(HandoffQuote, saved); touchDelivery(context, quoteId);
  return quoteId;
}

export async function recordExistingJob(context: DeliveryContext, input: ExistingJob): Promise<string> {
  const shared = deliveryAccess(context);
  const row = details(input, ["sourceSystem", "sourceRecordId", "sourceDocumentId", "title", "providerPartyId", "kind", "currency", "scope", "status", "startedAt", "summary"], ["committedCents"], "Existing work");
  const source = sourceRecord(row), lines = quoteLines(row.scope);
  requireHandoff(input.status === "Underway" || input.status === "Awaiting check" || input.status === "Complete", "Record the actual reported work state.");
  const startedAt = instant(input.startedAt);
  requireHandoff(startedAt <= instant(context.now), "Existing work cannot start in the future.");
  if (input.committedCents !== undefined) requireHandoff(money(input.committedCents) === sumQuotedCosts(lines), "The existing work's lines and cost disagree.");
  await requireDeliverySource(context, source.sourceDocumentId, [words(input.providerPartyId, "Provider", 160)]);
  const jobId = sourceIdentity("job", shared.workspaceId, source);
  const saved = { ...shared, ...source, jobId, title: words(input.title, "Job title", 200), providerPartyId: input.providerPartyId,
    kind: words(input.kind, "Service type", 100), currency: currencyCode(input.currency), scopeJson: orderedJson(lines),
    committedCents: input.committedCents, origin: "Existing", status: input.status === "Complete" ? "Awaiting check" : input.status,
    progressSummary: words(input.summary, "Reported progress", 3000), revision: "1", createdAt: startedAt, updatedAt: context.now };
  if (pendingDeliveryRecord(context, "HandoffJob", jobId, saved, ["createdAt"])) return jobId;
  const prior = await one(context.client(HandoffJob).where({ jobId: { $eq: jobId } }));
  if (prior) { inWorkspace(prior, context.workspace, context.caller); sameRecord(prior, saved, ["status", "revision", "updatedAt", "progressSummary"], ["createdAt"]); return jobId; }
  context.batch.create(HandoffJob, saved); touchDelivery(context, jobId);
  return jobId;
}

export async function recordInspection(context: DeliveryContext, input: InspectionReport): Promise<string> {
  const shared = deliveryAccess(context);
  const row = details(input, ["sourceSystem", "sourceRecordId", "sourceDocumentId", "title", "observerPartyId", "observedAt", "purpose", "findings"], ["jobId"], "Observation");
  const source = sourceRecord(row), observedAt = instant(input.observedAt), observed = findings(input.findings);
  requireHandoff(observedAt <= instant(context.now), "An observation cannot be dated in the future.");
  requireHandoff(input.purpose === "Condition report" || input.purpose === "Completion check", "Choose the purpose of the observation.");
  if (input.purpose === "Completion check") requireHandoff(input.jobId, "Identify the job being checked.");
  if (input.jobId) {
    const job = await deliveryJob(context, input.jobId), scope = jobScope(job);
    requireHandoff(observed.every((finding) => scope.some((line) => line.lineId === finding.lineId)), "The report contains findings outside this job.");
  }
  await requireDeliverySource(context, source.sourceDocumentId, [words(input.observerPartyId, "Observer", 160)]);
  const inspectionId = sourceIdentity("inspection", shared.workspaceId, source);
  const saved = { ...shared, ...source, inspectionId, title: words(input.title, "Observation title", 200), observerPartyId: input.observerPartyId,
    observedAt, purpose: input.purpose, jobId: input.jobId, findingsJson: orderedJson(observed), recordedAt: context.now };
  if (pendingDeliveryRecord(context, "HandoffInspection", inspectionId, saved, ["observedAt"])) return inspectionId;
  const prior = await one(context.client(HandoffInspection).where({ inspectionId: { $eq: inspectionId } }));
  if (prior) { inWorkspace(prior, context.workspace, context.caller); sameRecord(prior, saved, ["recordedAt"], ["observedAt"]); return inspectionId; }
  context.batch.create(HandoffInspection, saved); touchDelivery(context, inspectionId);
  return inspectionId;
}

export async function recordInvoice(context: DeliveryContext, input: SupplierInvoice): Promise<string> {
  const shared = deliveryAccess(context);
  const row = details(input, ["sourceSystem", "sourceRecordId", "sourceDocumentId", "title", "jobId", "providerPartyId", "payerPartyId", "currency", "lines", "totalCents", "issuedAt", "dueAt", "paymentTerms"], [], "Supplier invoice");
  const source = sourceRecord(row), lines = quoteLines(input.lines), totalCents = money(input.totalCents);
  requireHandoff(totalCents === sumQuotedCosts(lines), "The invoice lines do not match its stated total.");
  const issuedAt = instant(input.issuedAt), dueAt = instant(input.dueAt);
  requireHandoff(issuedAt <= instant(context.now) && dueAt >= issuedAt, "Check the invoice issue and due dates.");
  const job = await deliveryJob(context, input.jobId);
  requireHandoff(job.providerPartyId === input.providerPartyId, "The invoice issuer does not match the job's provider.");
  const document = await requireDeliverySource(context, source.sourceDocumentId, [input.providerPartyId, words(input.payerPartyId, "Payer", 160)]);
  requireHandoff(document.kind === "Invoice" && document.partyId === input.providerPartyId,
    "The invoice document must identify the supplier requesting payment.");
  const invoiceId = sourceIdentity("invoice", shared.workspaceId, { sourceSystem: source.sourceSystem,
    sourceRecordId: digest([input.providerPartyId, source.sourceRecordId]) });
  const status = invoiceMatchesJob(lines, jobScope(job).map(({ acceptedScope: _scope, ...line }) => line), input.currency, words(job.currency, "Job currency", 3)) ? "Received" : "Disputed";
  const saved = { workspaceId: shared.workspaceId, readerIds: shared.readerIds, handoffId: shared.handoffId, ...source, invoiceId,
    title: words(input.title, "Invoice title", 200), jobId: job.jobId, providerPartyId: input.providerPartyId, payerPartyId: input.payerPartyId,
    currency: currencyCode(input.currency), totalCents, linesJson: orderedJson(lines), issuedAt, dueAt,
    paymentTerms: words(input.paymentTerms, "Invoice terms", 3000), status, recordedAt: context.now };
  if (pendingDeliveryRecord(context, "HandoffInvoice", invoiceId, saved, ["issuedAt", "dueAt"])) return invoiceId;
  const prior = await one(context.client(HandoffInvoice).where({ invoiceId: { $eq: invoiceId } }));
  if (prior) { inWorkspace(prior, context.workspace, context.caller); sameRecord(prior, saved, ["status", "recordedAt"], ["issuedAt", "dueAt"]); return invoiceId; }
  context.batch.create(HandoffInvoice, saved); touchDelivery(context, invoiceId);
  return invoiceId;
}
