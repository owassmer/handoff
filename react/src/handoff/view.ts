import type { HandoffWorkspace, QuoteLine, WorkPlan, WorkSelection } from "./contracts";

type Workspace = HandoffWorkspace;
export type Quote = Workspace["quotes"][number];
export type Message = Workspace["messages"][number];

export function partyName(data: Workspace, id: string | null | undefined): string {
  return data.parties.find((p) => p.id === id)?.name ?? "Unknown party";
}

export function sumCents(values: readonly (string | null | undefined)[]): string {
  return values.reduce((total, value) => total + BigInt(value ?? "0"), 0n).toString();
}

export interface PlanLine {
  selection: WorkSelection;
  quote: Quote;
  line: QuoteLine;
}
export interface VendorGroup {
  providerPartyId: string;
  vendor: string;
  quote: Quote;
  lines: PlanLine[];
  subtotalCents: string;
}

/** Resolve each selected quote line to its quote; unknown references are dropped, never guessed. */
export function planLines(data: Workspace, selections: readonly WorkSelection[]): PlanLine[] {
  return selections.flatMap((selection) => {
    const quote = data.quotes.find((q) => q.id === selection.quoteId);
    const line = quote?.lines.find((l) => l.lineId === selection.quoteLineId);
    return quote && line ? [{ selection, quote, line }] : [];
  });
}

export function byVendor(data: Workspace, lines: readonly PlanLine[]): VendorGroup[] {
  const groups = new Map<string, VendorGroup>();
  lines.forEach((entry) => {
    const key = entry.quote.id;
    const group = groups.get(key) ?? {
      providerPartyId: entry.quote.providerPartyId,
      vendor: partyName(data, entry.quote.providerPartyId),
      quote: entry.quote,
      lines: [],
      subtotalCents: "0",
    };
    group.lines.push(entry);
    group.subtotalCents = sumCents([group.subtotalCents, entry.line.amountCents]);
    groups.set(key, group);
  });
  return [...groups.values()];
}

/** Quote lines received but not in the plan, available to add. */
export function unselectedLines(data: Workspace, selections: readonly WorkSelection[]) {
  return data.quotes
    .filter((q) => q.status === "Offered" || q.status === "Accepted")
    .flatMap((quote) =>
      quote.lines
        .filter(
          (line) =>
            !selections.some((s) => s.quoteId === quote.id && s.quoteLineId === line.lineId),
        )
        .map((line) => ({ quote, line })),
    );
}

export function needsDecision(data: Workspace): boolean {
  const plan = data.workPlan;
  return Boolean(
    plan &&
    !plan.acceptedDecisionId &&
    !["Accepted", "Superseded", "Withdrawn"].includes(plan.status),
  );
}

export function acceptedPlan(
  data: Workspace,
): { plan: WorkPlan; decision: Workspace["decisions"][number] } | undefined {
  const decision =
    data.decisions.find((d) => d.id === data.handoff.operativeDecisionId) ??
    data.decisions[data.decisions.length - 1];
  return decision ? { plan: decision.content, decision } : undefined;
}

/** Readiness steps shown on the unit header, mapped from the backend's physical progress. */
export const READINESS_STEPS = ["Assessing", "Plan ready", "Work underway", "Ready"] as const;
export function readinessStep(progress: string): number {
  const value = progress.toLowerCase();
  if (value === "ready") {
    return 3;
  }
  if (value.includes("arranging") || value.includes("provider") || value.includes("underway")) {
    return 2;
  }
  if (value === "plan ready") {
    return 1;
  }
  return 0;
}

/** The list only knows progress text; this matches the backend's "plan ready" wording and similar. */
export function awaitsDecision(progress: string): boolean {
  return /plan ready|your decision/i.test(progress);
}

/** Handoff's own state as the operator reads it. */
const AGENT_LABELS: Record<string, string> = {
  "Plan requested": "Preparing a plan",
  "Ready to continue": "Working",
  "Waiting for information": "Waiting for replies",
  "Waiting for provider": "Waiting on vendors",
  "Waiting for funding": "Waiting for owner funds",
  "Waiting for decision": "Needs your decision",
  "Needs attention": "Needs your attention",
  "Recommendation unavailable": "Needs your attention",
  Paused: "Paused",
};
export function agentLabel(status: string): string {
  return AGENT_LABELS[status] ?? statusLabel(status);
}

/** Activity written by Handoff's own turns, as opposed to operator commands. */
const AGENT_ACTIVITY = [
  "Handoff progressed",
  "Handoff next step",
  "Work plan ready",
  "Recommendation unavailable",
  "Work can't be ordered",
];
export interface ThreadEntry {
  id: string;
  who: "You" | "Handoff";
  at: string;
  body: string;
}
/** The operator's messages, each followed by the first thing Handoff did after it. Saved records, so replies stay. */
export function conversationThread(data: Workspace): ThreadEntry[] {
  const mine = data.messages
    .filter((m) => m.direction === "Operator")
    .sort((a, b) => a.createdAt.localeCompare(b.createdAt));
  const agent = data.activity
    .filter((a) => AGENT_ACTIVITY.includes(a.title) && a.detail)
    .sort((a, b) => a.at.localeCompare(b.at));
  return mine.flatMap((m, i) => {
    const next = mine[i + 1]?.createdAt;
    const entries: ThreadEntry[] = [{ id: m.id, who: "You", at: m.createdAt, body: m.body }];
    // Handoff's saved reply to this message; older messages fall back to its next recorded step.
    const saved = data.messages.find(
      (r) => r.direction === "Handoff" && r.replyToMessageId === m.id,
    );
    const reply = saved
      ? { id: saved.id, at: saved.createdAt, detail: saved.body }
      : agent.find((a) => a.at > m.createdAt && (!next || a.at < next));
    if (reply) {
      entries.push({ id: reply.id, who: "Handoff", at: reply.at, body: reply.detail });
    }
    return entries;
  });
}

/** A report line such as "Floors scratched: needs work", split into the condition and its result. */
export function conditionLines(observation: string): { text: string; result: string | null }[] {
  return observation
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const at = line.lastIndexOf(": ");
      return at > 0
        ? { text: line.slice(0, at), result: line.slice(at + 2) }
        : { text: line, result: null };
    });
}
const RESULT: Record<string, string> = {
  Deficient: "needs work",
  Satisfied: "satisfactory",
  "Not checked": "not checked",
};
/**
 * The conditions a report covers, each once. An assessment repeats its full condition list under each deliverable, so
 * the count comes from the conditions, not the report lines. A line without its own result takes the finding's.
 */
export function reportConditions(
  findings: readonly { result: string; observation: string }[],
): { text: string; result: string }[] {
  const seen = new Map<string, string>();
  findings.forEach((f) =>
    conditionLines(f.observation).forEach((line) => {
      if (!seen.has(line.text)) {
        seen.set(line.text, line.result ?? RESULT[f.result] ?? f.result.toLowerCase());
      }
    }),
  );
  return [...seen].map(([text, result]) => ({ text, result }));
}
/** Report lines that share the same observations are shown once. */
export function groupFindings<T extends { observation: string }>(
  findings: T[],
): { observation: string; findings: T[] }[] {
  const groups: { observation: string; findings: T[] }[] = [];
  findings.forEach((f) => {
    const group = groups.find((g) => g.observation === f.observation);
    if (group) {
      group.findings.push(f);
    } else {
      groups.push({ observation: f.observation, findings: [f] });
    }
  });
  return groups;
}

/** Backend statuses say "provider"; operators say "vendor". */
export function statusLabel(value: string): string {
  return value.replace(/provider/g, "vendor").replace(/Provider/g, "Vendor");
}

export type Tone = "attention" | "active" | "done" | "waiting" | "problem" | "neutral";
export function tone(status: string): Tone {
  const value = status.toLowerCase();
  if (/(decision|plan ready|attention)/.test(value)) {
    return "attention";
  }
  if (value === "needs work") {
    return "problem";
  }
  if (value === "satisfactory" || value === "done") {
    return "done";
  }
  if (value === "not checked" || value === "no access") {
    return "waiting";
  }
  if (/(unavailable|failed|returned|rejected|cancel|deficient)/.test(value)) {
    return "problem";
  }
  if (value === "satisfied") {
    return "done";
  }
  if (value === "not checked") {
    return "waiting";
  }
  if (/(complete|settled|paid|ready|accepted|received)$/.test(value)) {
    return "done";
  }
  if (/(underway|arranging|preparing|commissioned|continue|scheduled)/.test(value)) {
    return "active";
  }
  if (/(waiting|requested|confirming|queued|sent|offered)/.test(value)) {
    return "waiting";
  }
  return "neutral";
}

/** Outgoing requests without a reply yet, newest first. */
export function openRequests(data: Workspace): Message[] {
  return data.messages
    .filter(
      (m) =>
        m.direction === "Outgoing" &&
        // Orders for accepted work are followed in the vendor table, not as open questions.
        m.purpose !== "Appointment" &&
        !m.jobId &&
        !data.messages.some((r) => r.direction === "Incoming" && r.replyToMessageId === m.id),
    )
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt));
}

export function correspondenceByParty(data: Workspace) {
  const threads = new Map<string, Message[]>();
  data.messages
    .filter((m) => m.direction === "Outgoing" || m.direction === "Incoming")
    .forEach((m) => {
      const key = m.recipientPartyId ?? "unknown";
      threads.set(key, [...(threads.get(key) ?? []), m]);
    });
  return [...threads.entries()]
    .map(([partyId, messages]) => ({
      partyId,
      name: partyName(data, partyId),
      messages: messages.sort((a, b) => a.createdAt.localeCompare(b.createdAt)),
    }))
    .sort((a, b) =>
      (b.messages[b.messages.length - 1]?.createdAt ?? "").localeCompare(
        a.messages[a.messages.length - 1]?.createdAt ?? "",
      ),
    );
}

export interface MoneySummary {
  currency: string;
  setAsideCents: string | null;
  committedCents: string;
  invoicedCents: string;
  paidCents: string;
  availableCents: string | null;
}
export function moneySummary(data: Workspace): MoneySummary | undefined {
  const currency =
    data.funding[0]?.currency ?? data.invoices[0]?.currency ?? data.jobs[0]?.currency;
  if (!currency) {
    return undefined;
  }
  const funded = data.funding.filter((f) => f.currency === currency);
  return {
    currency,
    setAsideCents: funded.length ? sumCents(funded.map((f) => f.confirmedCents)) : null,
    committedCents: sumCents(
      data.jobs.filter((j) => j.currency === currency).map((j) => j.committedCents),
    ),
    invoicedCents: sumCents(
      data.invoices.filter((i) => i.currency === currency).map((i) => i.totalCents),
    ),
    paidCents: sumCents(
      data.payments
        .filter((p) => p.currency === currency && p.status === "Settled")
        .map((p) => p.amountCents),
    ),
    availableCents: funded.length ? sumCents(funded.map((f) => f.availableCents)) : null,
  };
}
