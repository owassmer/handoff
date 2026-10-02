import type { HandoffWorkspace, SourceDocument } from "./contracts";
import { money } from "./format";
import { type Message, type Tone, partyName, sumCents } from "./view";

type Workspace = HandoffWorkspace;
export type Job = Workspace["jobs"][number];
type Payment = Workspace["payments"][number];

const lastOf = <T>(items: readonly T[]): T | undefined => items[items.length - 1];
const latest = (values: readonly (string | null | undefined)[]): string | null =>
  lastOf(values.filter((v): v is string => Boolean(v)).sort()) ?? null;
const earliest = (values: readonly (string | null | undefined)[]): string | null =>
  values.filter((v): v is string => Boolean(v)).sort()[0] ?? null;

/* ---------- One lifecycle stage per job ---------- */

export interface StageStep {
  name: "Ordered" | "Advance" | "Visit" | "Report" | "Paid";
  date: string | null;
  done: boolean;
  /** No advance on this job; the slot stays so every rail lines up. */
  skipped?: boolean;
}
export interface JobStage {
  label: string;
  tone: Tone;
  steps: StageStep[];
  closed: boolean;
}
const settled = (payments: Payment[]) => payments.find((p) => p.status === "Settled");
const failed = (p: Payment | undefined) => Boolean(p && /fail|reject|return/i.test(p.status));

/** The whole vendor lifecycle in one status. "Complete" means checked and paid, never only "work done". */
export function jobStage(data: Workspace, job: Job): JobStage {
  const payments = data.payments.filter((p) => p.jobId === job.id);
  const advances = payments.filter((p) => p.purpose === "Advance");
  const settlement = payments.filter((p) => p.purpose !== "Advance");
  const invoice = data.invoices.find((i) => i.jobId === job.id);
  const report = data.inspections.find((i) => i.jobId === job.id);
  const quote = data.quotes.find((q) => q.id === job.quoteId);
  const needsAdvance = BigInt(quote?.depositCents ?? "0") > 0n || advances.length > 0;
  const ordered = earliest(
    data.messages
      .filter((m) => m.jobId === job.id && m.direction === "Outgoing")
      .map((m) => m.createdAt),
  );
  const advancePaid = settled(advances);
  const visited = ["Complete", "Awaiting check", "Needs attention"].includes(job.status);
  const paid = settled(settlement);
  const steps: StageStep[] = [
    { name: "Ordered", date: ordered, done: true },
    needsAdvance
      ? { name: "Advance", date: advancePaid?.observedAt ?? null, done: Boolean(advancePaid) }
      : { name: "Advance", date: null, done: false, skipped: true },
    { name: "Visit", date: job.appointmentAt, done: visited },
    { name: "Report", date: report?.observedAt ?? null, done: Boolean(report) },
    { name: "Paid", date: paid?.observedAt ?? null, done: Boolean(paid) },
  ];
  const stage = (label: string, tone: Tone, closed = false): JobStage => ({
    label,
    tone,
    steps,
    closed,
  });
  if (job.status === "Cancelled") {
    return stage("Cancelled", "problem", true);
  }
  if (job.status === "Needs attention") {
    return stage("Needs attention", "attention");
  }
  if (paid && job.status === "Complete") {
    return stage("Complete · paid", "done", true);
  }
  const invoicePayment = settlement[0];
  if (failed(invoicePayment)) {
    return stage("Invoice payment failed", "problem");
  }
  if (invoicePayment) {
    return stage("Paying invoice", "waiting");
  }
  if (invoice && job.status === "Complete") {
    return stage("Invoice to pay", "waiting");
  }
  if (report && !paid) {
    return stage("Checking report", "active");
  }
  if (job.appointmentAt && !visited) {
    return stage("Visit booked", "active");
  }
  const advance = lastOf(advances);
  if (failed(advance)) {
    return stage("Advance payment failed", "problem");
  }
  if (advance && !advancePaid) {
    return stage("Paying advance", "waiting");
  }
  if (needsAdvance && !advancePaid) {
    return stage("Advance needed", "waiting");
  }
  return stage(advancePaid ? "Booking visit" : "Ordered", "waiting");
}

/** When a job started, for ordering jobs as they happened. */
export function jobStart(data: Workspace, job: Job): string {
  return jobStage(data, job).steps[0]?.date ?? job.appointmentAt ?? "";
}

/** The next booked visit when every open job has one; the Now line names it instead of "waiting on". */
export function nextVisit(data: Workspace): { vendor: string; job: string; at: string } | null {
  const open = data.jobs.filter((job) => !jobStage(data, job).closed);
  if (!open.length || !open.every((job) => jobStage(data, job).label === "Visit booked")) {
    return null;
  }
  const job = [...open].sort((a, b) => a.appointmentAt!.localeCompare(b.appointmentAt!))[0]!;
  return { vendor: partyName(data, job.providerPartyId), job: job.title, at: job.appointmentAt! };
}

/** Vendors whose jobs are waiting on them. */
export function waitingOn(data: Workspace): string[] {
  const names = data.jobs
    .filter((job) => {
      const s = jobStage(data, job);
      return !s.closed && ["Ordered", "Booking visit", "Visit booked"].includes(s.label);
    })
    .map((job) => partyName(data, job.providerPartyId));
  return [...new Set(names)];
}

/* ---------- Case clock ---------- */

/** The case's own today: the latest dated event, not the server's clock. */
export function caseToday(data: Workspace): string | null {
  return latest([
    ...data.activity.map((a) => a.at),
    ...data.messages.map((m) => m.createdAt),
    ...data.decisions.map((d) => d.at),
  ]);
}

/* ---------- Calendar ---------- */

export interface CalendarEvent {
  id: string;
  kind: "Visit" | "Invoice due" | "Offer expires" | "Lease end";
  title: string;
  start: string;
  end: string | null;
  unit: string;
  handoffId: string;
  jobId?: string;
  detail: string;
}
export function calendarEvents(data: Workspace): CalendarEvent[] {
  const unit = data.property.name,
    handoffId = data.handoff.id;
  const events: CalendarEvent[] = [];
  data.jobs.forEach((job) => {
    if (job.appointmentAt) {
      events.push({
        id: `visit-${job.id}`,
        kind: "Visit",
        title: `${partyName(data, job.providerPartyId)}: ${job.title}`,
        start: job.appointmentAt,
        end: job.appointmentEndsAt,
        unit,
        handoffId,
        jobId: job.id,
        detail: jobStage(data, job).label,
      });
    }
  });
  data.invoices.forEach((invoice) => {
    const paid = data.payments.some(
      (p) => p.jobId === invoice.jobId && p.purpose !== "Advance" && p.status === "Settled",
    );
    if (!paid) {
      events.push({
        id: `invoice-${invoice.id}`,
        kind: "Invoice due",
        title: `${partyName(data, invoice.providerPartyId)} invoice ${money(invoice.totalCents, invoice.currency)}`,
        start: invoice.dueAt,
        end: null,
        unit,
        handoffId,
        jobId: invoice.jobId,
        detail: "Payment due",
      });
    }
  });
  const ordered = new Set(data.jobs.map((j) => j.quoteId));
  data.quotes
    .filter((q) => q.status === "Offered" && !ordered.has(q.id))
    .forEach((q) =>
      events.push({
        id: `offer-${q.id}`,
        kind: "Offer expires",
        title: `${partyName(data, q.providerPartyId)} offer: ${q.title}`,
        start: q.validUntil,
        end: null,
        unit,
        handoffId,
        detail: money(q.totalCents, q.currency),
      }),
    );
  if (data.tenancy.endDate) {
    events.push({
      id: `lease-${data.tenancy.id}`,
      kind: "Lease end",
      title: "Lease ended",
      start: `${data.tenancy.endDate.slice(0, 10)}T12:00:00Z`,
      end: null,
      unit,
      handoffId,
      detail: data.tenancy.title,
    });
  }
  return events.sort((a, b) => a.start.localeCompare(b.start));
}
/** Local date key (YYYY-MM-DD) for grouping, in the same zone the app shows times in. */
export function dayKey(value: string | Date): string {
  const d = typeof value === "string" ? new Date(value) : value;
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
/** Every local day an event covers, so multi-day work draws as one continuous bar. */
export function eventDays(event: CalendarEvent): string[] {
  const start = new Date(event.start);
  const end = event.end ? new Date(event.end) : start;
  const days: string[] = [];
  const cursor = new Date(start.getFullYear(), start.getMonth(), start.getDate());
  const last = new Date(end.getFullYear(), end.getMonth(), end.getDate());
  for (let n = 0; cursor <= last && n < 62; n += 1) {
    days.push(dayKey(cursor));
    cursor.setDate(cursor.getDate() + 1);
  }
  return days;
}

/* ---------- Timeline ---------- */

/** Intake bookkeeping that is not a business event. */
const HIDDEN_TITLES = ["Source file associated"];
const AGENT_TITLES = [
  "Handoff progressed",
  "Handoff next step",
  "Work plan ready",
  "Recommendation unavailable",
  "Work can't be ordered",
];
export interface TimelineEntry {
  id: string;
  at: string;
  who: string;
  text: string;
  more: string[];
  parties: string[];
}
/** Handoff's steps and the operator's actions, newest first; a burst of steps within minutes is one entry. */
export function timeline(data: Workspace): TimelineEntry[] {
  const names = data.parties.map((p) => p.name);
  const mine = data.messages.filter((m) => m.direction === "Operator");
  const rows = [...data.activity]
    .filter((row) => !HIDDEN_TITLES.includes(row.title))
    .sort((a, b) => a.at.localeCompare(b.at));
  const entries: TimelineEntry[] = [];
  rows.forEach((row) => {
    const agent = AGENT_TITLES.includes(row.title);
    let text = agent ? row.detail : row.title;
    let who = agent ? "Handoff" : "You";
    if (row.title === "Message received") {
      const sent = mine.find(
        (m) => Math.abs(Date.parse(m.createdAt) - Date.parse(row.at)) < 120000,
      );
      text = sent ? `“${sent.body}”` : "Sent Handoff a message.";
    } else if (row.title === "Move-out notice received") {
      who = "Handoff";
      text = "Received the move-out notice and the unit file.";
    }
    if (!text) {
      return;
    }
    // A vendor's or the owner's own act is theirs, not Handoff's.
    const actor = agent ? names.find((n) => text.startsWith(n)) : undefined;
    if (actor) {
      who = actor;
    }
    const parties = names.filter((n) => text.includes(n));
    const previous = lastOf(entries);
    const close =
      previous &&
      previous.who === who &&
      agent &&
      Date.parse(row.at) - Date.parse(previous.at) <= 5 * 60000 &&
      previous.more.length < 12;
    if (close) {
      if (text !== previous.text && !previous.more.includes(text)) {
        previous.more.push(text);
      }
      previous.parties = [...new Set([...previous.parties, ...parties])];
      previous.at = row.at;
    } else {
      entries.push({ id: row.id, at: row.at, who, text, more: [], parties });
    }
  });
  return entries.reverse();
}

/* ---------- Inbox ---------- */

export interface InboxThread {
  partyId: string;
  name: string;
  subject: string;
  last: Message;
  messages: Message[];
  awaitingReply: boolean;
}
export function inbox(data: Workspace): InboxThread[] {
  const threads = new Map<string, Message[]>();
  data.messages
    .filter((m) => m.direction === "Outgoing" || m.direction === "Incoming")
    .forEach((m) => {
      const key =
        (m.direction === "Incoming" ? m.senderPartyId : null) ?? m.recipientPartyId ?? "unknown";
      threads.set(key, [...(threads.get(key) ?? []), m]);
    });
  return [...threads.entries()]
    .map(([partyId, messages]) => {
      const sorted = [...messages].sort((a, b) => a.createdAt.localeCompare(b.createdAt));
      const last = lastOf(sorted)!;
      return {
        partyId,
        name: partyName(data, partyId),
        subject: last.title.replace(/^Re:\s*/i, ""),
        last,
        messages: sorted,
        awaitingReply:
          last.direction === "Outgoing" &&
          !data.messages.some((r) => r.direction === "Incoming" && r.replyToMessageId === last.id),
      };
    })
    .sort((a, b) => b.last.createdAt.localeCompare(a.last.createdAt));
}
/** What Handoff recorded from an incoming email, from the records it links to. */
export function recordedFrom(data: Workspace, message: Message): string[] {
  const facts: string[] = [];
  (message.attachmentDocumentIds ?? []).forEach((id) => {
    const quote = data.quotes.find((q) => q.sourceDocumentId === id);
    if (quote) {
      facts.push(`Quote ${money(quote.totalCents, quote.currency)}`);
    }
    const invoice = data.invoices.find((i) => i.sourceDocumentId === id);
    if (invoice) {
      facts.push(`Invoice ${money(invoice.totalCents, invoice.currency)}`);
    }
    const report = data.inspections.find((i) => i.sourceDocumentId === id);
    if (report) {
      facts.push("Report");
    }
  });
  if (message.direction === "Incoming" && /Confirmed requirements:/.test(message.body)) {
    facts.push("Requirements confirmed");
  }
  const job = data.jobs.find((j) => j.id === message.jobId);
  if (
    message.direction === "Incoming" &&
    job?.appointmentAt &&
    /start on|booked/i.test(message.body)
  ) {
    facts.push(
      `Visit ${new Date(job.appointmentAt).toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" })}`,
    );
  }
  return [...new Set(facts)];
}
export function attachments(data: Workspace, message: Message): SourceDocument[] {
  return (message.attachmentDocumentIds ?? [])
    .map((id) => data.documents.find((d) => d.id === id))
    .filter((d): d is SourceDocument => Boolean(d));
}

/* ---------- Documents ---------- */

export type DocumentForm = "file" | "quote" | "invoice" | "report" | "text";
export function documentForm(data: Workspace, doc: SourceDocument): DocumentForm {
  if (doc.mediaSetRid && doc.mediaItemRid) {
    return "file";
  }
  if (data.quotes.some((q) => q.sourceDocumentId === doc.id)) {
    return "quote";
  }
  if (data.invoices.some((i) => i.sourceDocumentId === doc.id)) {
    return "invoice";
  }
  if (data.inspections.some((i) => i.sourceDocumentId === doc.id)) {
    return "report";
  }
  if ((doc.sourceDocumentIds ?? []).length) {
    return "file";
  }
  return "text";
}

/* ---------- Money ---------- */

export interface VendorLedger {
  partyId: string;
  name: string;
  committedCents: string;
  invoicedCents: string;
  paidCents: string;
  requestedCents: string;
  currency: string;
}
/** A payment asked for but not settled, failed or withdrawn. It is owed, never counted as paid. */
export function outstanding(status: string): boolean {
  return status !== "Settled" && !/fail|cancel|reject|void|withdrawn/i.test(status);
}

export function ledger(data: Workspace): VendorLedger[] {
  const byVendor = new Map<string, Job[]>();
  data.jobs.forEach((job) =>
    byVendor.set(job.providerPartyId, [...(byVendor.get(job.providerPartyId) ?? []), job]),
  );
  return [...byVendor.entries()].map(([partyId, jobs]) => {
    const ids = new Set(jobs.map((j) => j.id));
    const payments = data.payments.filter((p) => ids.has(p.jobId));
    return {
      partyId,
      name: partyName(data, partyId),
      currency: jobs[0]!.currency,
      committedCents: sumCents(jobs.map((j) => j.committedCents)),
      invoicedCents: sumCents(
        data.invoices.filter((i) => ids.has(i.jobId)).map((i) => i.totalCents),
      ),
      paidCents: sumCents(payments.filter((p) => p.status === "Settled").map((p) => p.amountCents)),
      requestedCents: sumCents(
        payments.filter((p) => outstanding(p.status)).map((p) => p.amountCents),
      ),
    };
  });
}

/* ---------- Live state ---------- */

const DUE = ["Ready to continue", "Plan requested"];
/** A reply to the operator's last message is still to come. */
export function replyExpected(data: Workspace): boolean {
  const mine = data.messages
    .filter((m) => m.direction === "Operator")
    .sort((a, b) => a.createdAt.localeCompare(b.createdAt));
  const last = lastOf(mine);
  return Boolean(
    last &&
    !data.messages.some((r) => r.direction === "Handoff" && r.replyToMessageId === last.id) &&
    !data.activity.some((a) => a.at > last.createdAt && a.title !== "Message received"),
  );
}
/** How soon Handoff's next step is due, in ms from now; null if nothing is scheduled. */
export function dueIn(data: Workspace, now = Date.now()): number | null {
  if (DUE.includes(data.agent.status) && !data.agent.nextWakeAt) {
    return 0;
  }
  if (!data.agent.nextWakeAt) {
    return null;
  }
  return Math.max(0, Date.parse(data.agent.nextWakeAt) - now);
}
/** Read every 2 s while a step or reply is due soon, every 15 s while vendors work, else the base rate. */
export function pollDelay(data: Workspace | undefined, base: number, now = Date.now()): number {
  if (!data) {
    return base;
  }
  const due = dueIn(data, now);
  if ((due !== null && due < 60_000) || replyExpected(data)) {
    return 2000;
  }
  if (/^Waiting for (provider|information)$/.test(data.agent.status)) {
    return 15_000;
  }
  return base;
}

/** Quotes and invoices are money records: they open from the Money tab, not Documents. */
export function moneyDocumentIds(data: Workspace): Set<string> {
  return new Set(
    [...data.quotes, ...data.invoices]
      .map((r) => r.sourceDocumentId)
      .filter((id): id is string => Boolean(id)),
  );
}

export type LineState = "Ordered" | "Approved" | "In proposed plan" | "Not ordered";
export const LINE_STATES: LineState[] = ["Ordered", "Approved", "In proposed plan", "Not ordered"];

/**
 * Where one quoted line stands: ordered on a job; approved in the accepted plan and waiting for its order; selected in
 * the plan awaiting a decision; or not ordered.
 */
export function lineState(data: Workspace, quoteId: string, lineId: string): LineState {
  if (data.jobs.some((j) => j.quoteId === quoteId && j.scope.some((s) => s.lineId === lineId))) {
    return "Ordered";
  }
  const plan = data.workPlan;
  if (!plan?.selections.some((s) => s.quoteId === quoteId && s.quoteLineId === lineId)) {
    return "Not ordered";
  }
  return plan.status === "Accepted"
    ? "Approved"
    : plan.status === "Ready"
      ? "In proposed plan"
      : "Not ordered";
}
