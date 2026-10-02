import { type ReactNode, useEffect, useRef, useState } from "react";
import type { HandoffWorkspace, SourceDocument } from "./contracts";
import { calendarDate, money, shortTime } from "./format";
import {
  attachments,
  dayKey,
  documentForm,
  inbox,
  moneyDocumentIds,
  recordedFrom,
  timeline,
} from "./model";
import { useArrivals, useFlip } from "./motion";

/* ---------- Messages: an email client (conversation list, then the thread) ---------- */

export function MessagesTab({
  data,
  readDocument,
}: {
  data: HandoffWorkspace;
  readDocument(document: SourceDocument): void;
}) {
  const threads = inbox(data);
  const [open, setOpen] = useState<string | undefined>(() => threads[0]?.partyId);
  const list = useRef<HTMLUListElement>(null);
  useFlip(list, threads.map((t) => t.partyId).join(","));
  const thread = threads.find((t) => t.partyId === open) ?? threads[0];
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const arrived = useArrivals([
    ...threads.map((t) => `thread:${t.partyId}:${t.last.id}`),
    ...threads.flatMap((t) => t.messages.map((m) => `email:${m.id}`)),
  ]);
  const us = data.workspace.name;
  if (!threads.length) {
    return (
      <div className="tab-empty">
        <p className="faint">No messages yet.</p>
      </div>
    );
  }
  return (
    <div className="inbox-pane">
      <ul className="inbox" aria-label="Conversations" ref={list}>
        {threads.map((t) => (
          <li
            key={t.partyId}
            data-flip={t.partyId}
            className={arrived.has(`thread:${t.partyId}:${t.last.id}`) ? "arrive" : undefined}
          >
            <button
              type="button"
              aria-current={t.partyId === thread?.partyId ? "true" : undefined}
              onClick={() => setOpen(t.partyId)}
            >
              <span className="inbox-top">
                <strong>{t.name}</strong>
                <time dateTime={t.last.createdAt}>{shortTime(t.last.createdAt)}</time>
              </span>
              <span className="inbox-subject">{t.subject}</span>
              <span className="inbox-snippet">
                {t.last.body.replace(/^(Hi|Hello)[^\n]*\n+/, "")}
              </span>
              {t.awaitingReply && <span className="pill">Awaiting reply</span>}
            </button>
          </li>
        ))}
      </ul>
      {thread && (
        <div className="thread-pane">
          <h3 className="thread-title">{thread.name}</h3>
          {thread.messages.map((m, index) => {
            const incoming = m.direction === "Incoming";
            const latest = index === thread.messages.length - 1;
            const show = latest || expanded.has(m.id);
            const files = attachments(data, m);
            const facts = recordedFrom(data, m);
            return (
              <article
                className={`email${incoming ? " in" : ""}${show ? "" : " collapsed"}${arrived.has(`email:${m.id}`) ? " arrive" : ""}`}
                key={m.id}
              >
                <header>
                  <button
                    type="button"
                    className="email-from"
                    aria-expanded={show}
                    disabled={latest}
                    onClick={() =>
                      setExpanded((prev) => {
                        const next = new Set(prev);
                        if (next.has(m.id)) {
                          next.delete(m.id);
                        } else {
                          next.add(m.id);
                        }
                        return next;
                      })
                    }
                  >
                    <strong>{incoming ? thread.name : us}</strong>
                    {show ? (
                      <span className="faint"> to {incoming ? us : thread.name}</span>
                    ) : (
                      <span className="faint email-preview">{m.title}</span>
                    )}
                  </button>
                  <time dateTime={m.createdAt}>{shortTime(m.createdAt)}</time>
                </header>
                {show && (
                  <>
                    <div className="email-subject">{m.title}</div>
                    <div className="email-body">{m.body}</div>
                    {files.length > 0 && (
                      <div className="chips">
                        {files.map((doc) => (
                          <button
                            type="button"
                            className="chip"
                            key={doc.id}
                            onClick={() => readDocument(doc)}
                          >
                            <span className="chip-icon" aria-hidden="true">
                              {documentForm(data, doc) === "file" ? "PDF" : "DOC"}
                            </span>
                            {doc.title}
                          </button>
                        ))}
                      </div>
                    )}
                    {facts.length > 0 && (
                      <p className="recorded">
                        <span>Recorded by Handoff</span> {facts.join(" · ")}
                      </p>
                    )}
                  </>
                )}
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}

/* ---------- Timeline: what Handoff did and why ---------- */

function seenKey(id: string): string {
  return `handoff.seen.${id}`;
}
export function TimelineTab({ data }: { data: HandoffWorkspace }) {
  const entries = timeline(data);
  const [lane, setLane] = useState<string>();
  // A burst that grows keeps its id; its size is part of the key so the added step reads as an arrival.
  const arrived = useArrivals(entries.map((e) => `${e.id}:${e.more.length}`));
  const [seen] = useState(() => {
    try {
      return localStorage.getItem(seenKey(data.handoff.id)) ?? "";
    } catch {
      return "";
    }
  });
  const newest = entries[0]?.at ?? "";
  useEffect(
    () => () => {
      try {
        if (newest) {
          localStorage.setItem(seenKey(data.handoff.id), newest);
        }
      } catch {
        /* Marking what's new is optional. */
      }
    },
    [data.handoff.id, newest],
  );
  const vendors = new Set(
    data.jobs.map((j) => data.parties.find((p) => p.id === j.providerPartyId)?.name ?? ""),
  );
  const lanes = [...new Set(entries.flatMap((e) => e.parties))].sort(
    (a, b) => Number(vendors.has(b)) - Number(vendors.has(a)) || a.localeCompare(b),
  );
  const shown = lane ? entries.filter((e) => e.parties.includes(lane)) : entries;
  const firstOld = seen ? shown.findIndex((e) => e.at <= seen) : -1;
  if (!entries.length) {
    return (
      <div className="tab-empty">
        <p className="faint">Nothing has happened on this unit yet.</p>
      </div>
    );
  }
  return (
    <div className="timeline-pane">
      {lanes.length > 1 && (
        <div className="filter-chips" role="group" aria-label="Show steps for">
          <button type="button" aria-pressed={!lane} onClick={() => setLane(undefined)}>
            All
          </button>
          {lanes.map((name) => (
            <button
              type="button"
              key={name}
              aria-pressed={lane === name}
              onClick={() => setLane(name)}
            >
              {name}
            </button>
          ))}
        </div>
      )}
      <ol className="timeline">
        {shown.map((e, index) => (
          <li
            key={e.id}
            className={arrived.has(`${e.id}:${e.more.length}`) ? "arrive" : undefined}
            data-who={
              e.who === "Handoff" || e.who === "You"
                ? e.who
                : vendors.has(e.who)
                  ? "Vendor"
                  : "Person"
            }
          >
            {(index === 0 || dayKey(e.at) !== dayKey(shown[index - 1]!.at)) && (
              <div className="day-divider">
                {new Date(e.at).toLocaleDateString(undefined, {
                  weekday: "long",
                  month: "long",
                  day: "numeric",
                })}
              </div>
            )}
            {index === firstOld && index > 0 && (
              <div className="seen-divider">
                <span>Earlier</span>
              </div>
            )}
            <span className="tl-icon" aria-hidden="true" />
            <div className="tl-body">
              <div className="tl-meta">
                <span className="who">{e.who}</span>
                <time dateTime={e.at}>
                  {new Date(e.at).toLocaleTimeString(undefined, {
                    hour: "numeric",
                    minute: "2-digit",
                  })}
                </time>
              </div>
              <p>{e.text}</p>
              {e.more.length === 1 && <p>{e.more[0]}</p>}
              {e.more.length > 1 && (
                <details>
                  <summary>
                    {e.more.length} more {e.more.length === 1 ? "step" : "steps"}
                  </summary>
                  <ul>
                    {e.more.map((text, i) => (
                      <li key={i}>{text}</li>
                    ))}
                  </ul>
                </details>
              )}
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}

/* ---------- Documents: grouped list and the selected document ---------- */

export function DocumentsTab({
  data,
  selectedId,
  readDocument,
  viewer,
}: {
  data: HandoffWorkspace;
  selectedId?: string;
  readDocument(document: SourceDocument): void;
  viewer: ReactNode;
}) {
  const arrivedDocs = useArrivals(data.documents.map((d) => d.id));
  const moneyRecords = moneyDocumentIds(data);
  const shown = data.documents.filter(
    (d) =>
      !moneyRecords.has(d.id) &&
      !(
        d.sourceKind === "Original" &&
        data.documents.some((p) => p.sourceDocumentIds?.includes(d.id))
      ),
  );
  const form = (d: SourceDocument) => documentForm(data, d);
  const byDate = (a: SourceDocument, b: SourceDocument) =>
    (a.availableFrom ?? "").localeCompare(b.availableFrom ?? "");
  /** Inside a group the group name says what it is: "Invoice for Floor restoration" reads "Floor restoration". */
  const label = (d: SourceDocument) => {
    const vendorOf = (partyId: string | undefined) =>
      data.parties.find((p) => p.id === partyId)?.name.replace(/ (LLC|PLLC|Inc\.?)$/, "");
    const quote = data.quotes.find((q) => q.sourceDocumentId === d.id);
    const invoice = data.invoices.find((i) => i.sourceDocumentId === d.id);
    const report = data.inspections.find((i) => i.sourceDocumentId === d.id);
    const vendor = vendorOf(
      quote?.providerPartyId ?? invoice?.providerPartyId ?? report?.observerPartyId,
    );
    const title = d.title.replace(/^Invoice for /, "").replace(/ — report$/, "");
    return vendor && !title.includes(vendor) ? `${vendor}\u00a0· ${title}` : title;
  };
  const detail = (d: SourceDocument) => {
    const quote = data.quotes.find((q) => q.sourceDocumentId === d.id);
    const invoice = data.invoices.find((i) => i.sourceDocumentId === d.id);
    if (quote) {
      return money(quote.totalCents, quote.currency);
    }
    if (invoice) {
      const settledOnJob = data.payments.some(
        (p) => p.jobId === invoice.jobId && p.purpose !== "Advance" && p.status === "Settled",
      );
      return `${money(invoice.totalCents, invoice.currency)}${settledOnJob ? " · paid" : ""}`;
    }
    if (form(d) === "file") {
      return "PDF";
    }
    return d.availableFrom ? calendarDate(d.availableFrom).replace(/, \d{4}$/, "") : "";
  };
  const records = shown.filter(
    (d) => !["quote", "invoice", "report"].includes(form(d)) && d.kind !== "Provider information",
  );
  const groups: [string, SourceDocument[]][] = [
    ["Lease & records", [...records].sort(byDate)],
    ["Reports", shown.filter((d) => form(d) === "report").sort(byDate)],
    ["Vendor terms", shown.filter((d) => d.kind === "Provider information")],
  ];
  return (
    <div className="docs-pane">
      <nav className="doc-list" aria-label="Documents">
        {groups
          .filter(([, docs]) => docs.length)
          .map(([title, docs]) => (
            <div className="file-group" key={title}>
              <h3>
                {title} <span className="faint">{docs.length}</span>
              </h3>
              <ul className="file-list">
                {docs.map((d) => (
                  <li
                    key={d.id}
                    className={arrivedDocs.has(d.id) ? "arrive" : undefined}
                    aria-current={d.id === selectedId ? "true" : undefined}
                  >
                    <button type="button" className="doc-item" onClick={() => readDocument(d)}>
                      <span className="doc-name">{label(d)}</span>
                      <span className="kind">{detail(d)}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        <div className="file-group">
          <h3>
            People <span className="faint">{data.parties.length}</span>
          </h3>
          <ul className="file-list">
            {[...data.parties]
              .sort((a, b) => a.kind.localeCompare(b.kind) || a.name.localeCompare(b.name))
              .map((p) => (
                <li key={p.id} title={p.description}>
                  <span>{p.name}</span>
                  <span className="kind">{p.kind === "Organization" ? "Company" : "Person"}</span>
                </li>
              ))}
          </ul>
        </div>
      </nav>
      <div className="doc-pane">
        {viewer ?? <p className="faint doc-placeholder">Select a document to view it here.</p>}
      </div>
    </div>
  );
}
