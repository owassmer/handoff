import { Fragment, type ReactNode, useEffect, useRef, useState } from "react";
import { MoneySection } from "./Work";
import type { HandoffWorkspace, SourceDocument } from "./contracts";
import { calendarDate, money } from "./format";
import { LINE_STATES, lineState, outstanding } from "./model";
import { useArrivals } from "./motion";
import { partyName, sumCents } from "./view";

type Workspace = HandoffWorkspace;

function DocButton({
  data,
  id,
  fallback,
  onOpen,
}: {
  data: Workspace;
  id: string | null | undefined;
  fallback: string;
  onOpen(doc: SourceDocument): void;
}) {
  const doc = id ? data.documents.find((d) => d.id === id) : undefined;
  if (!doc) {
    return <span>{fallback}</span>;
  }
  return (
    <button type="button" className="link" onClick={() => onOpen(doc)}>
      {doc.title.replace(/^Invoice for /, "")}
    </button>
  );
}

const TONE: Record<string, string | undefined> = {
  Ordered: "done",
  "Partly ordered": "done",
  Approved: "done",
  "In proposed plan": "waiting",
};

/** Which documents have their lines unfolded. Lines start folded; each row and the whole section toggle. */
function useLines() {
  const [opened, setOpened] = useState<ReadonlySet<string>>(new Set());
  return {
    opened,
    toggle: (id: string) =>
      setOpened((prev) => {
        const next = new Set(prev);
        if (!next.delete(id)) {
          next.add(id);
        }
        return next;
      }),
    set: (ids: string[]) => setOpened(new Set(ids)),
  };
}

function Disclose({ open, label, onToggle }: { open: boolean; label: string; onToggle(): void }) {
  return (
    <button
      type="button"
      className="disclose"
      aria-expanded={open}
      aria-label={`${open ? "Hide" : "Show"} lines of ${label}`}
      onClick={onToggle}
    >
      <svg aria-hidden="true" viewBox="0 0 16 16" width="14" height="14" data-open={open}>
        <path d="M6 4l4 4-4 4" fill="none" stroke="currentColor" strokeWidth="1.6" />
      </svg>
    </button>
  );
}

function AllToggle({ state, ids }: { state: ReturnType<typeof useLines>; ids: string[] }) {
  const allOpen = ids.every((id) => state.opened.has(id));
  return (
    <button
      type="button"
      className="btn quiet all-lines"
      onClick={() => state.set(allOpen ? [] : ids)}
    >
      {allOpen ? "Collapse all" : "Expand all"}
    </button>
  );
}

/**
 * Money for this unit in one place (Ramp / Bill.com pattern): the funds summary and vendor ledger, then
 * invoices, quotes and payments as tables. A row's document opens in a drawer over the tab.
 */
export function MoneyTab({
  data,
  readDocument,
  openId,
}: {
  data: Workspace;
  readDocument(doc: SourceDocument): void;
  openId?: string;
}) {
  const arrived = useArrivals([
    ...data.invoices.map((i) => `invoice:${i.id}`),
    ...data.quotes.map((q) => `quote:${q.id}:${q.status}`),
    ...data.payments.map((p) => `payment:${p.id}:${p.status}`),
  ]);
  const settledFor = (jobId: string) =>
    data.payments.find(
      (p) => p.jobId === jobId && p.purpose !== "Advance" && p.status === "Settled",
    );
  const requestedFor = (jobId: string) =>
    data.payments.find(
      (p) => p.jobId === jobId && p.purpose !== "Advance" && outstanding(p.status),
    );
  const docDate = (id: string | null | undefined) =>
    data.documents.find((d) => d.id === id)?.availableFrom ?? "";
  const invoices = [...data.invoices].sort((a, b) =>
    docDate(b.sourceDocumentId).localeCompare(docDate(a.sourceDocumentId)),
  );
  const quotes = [...data.quotes].sort((a, b) =>
    docDate(b.sourceDocumentId).localeCompare(docDate(a.sourceDocumentId)),
  );
  const payments = [...data.payments].sort((a, b) =>
    (b.observedAt ?? b.requestedAt).localeCompare(a.observedAt ?? a.requestedAt),
  );
  const row = (key: string, id: string | null | undefined, extra = "") =>
    [extra, arrived.has(key) ? "arrive" : "", id && id === openId ? "selected" : ""]
      .filter(Boolean)
      .join(" ") || undefined;
  const invoiceLines = useLines();
  const quoteLines = useLines();
  return (
    <div className="main-col money-tab">
      <MoneySection data={data} />
      <section className="section" aria-labelledby="invoices-title">
        <header>
          <h2 id="invoices-title">Invoices</h2>
          <span className="faint">{invoices.length}</span>
          {invoices.length > 0 && (
            <AllToggle state={invoiceLines} ids={invoices.map((i) => i.id)} />
          )}
        </header>
        {invoices.length ? (
          <table className="rows ledger lined docs">
            <colgroup>
              <col className="col-name" />
              <col />
              <col className="col-date hide-sm" />
              <col className="col-status" />
              <col className="col-amount" />
            </colgroup>
            <thead>
              <tr>
                <th>Vendor</th>
                <th>For</th>
                <th className="hide-sm">Date</th>
                <th>Status</th>
                <th className="num">Amount</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((i) => {
                const paid = settledFor(i.jobId);
                const requested = requestedFor(i.jobId);
                const open = invoiceLines.opened.has(i.id);
                const title = i.title.replace(/^Invoice for /, "");
                return (
                  <Fragment key={i.id}>
                    <tr className={row(`invoice:${i.id}`, i.sourceDocumentId, "group-head")}>
                      <td title={partyName(data, i.providerPartyId)}>
                        <Disclose
                          open={open}
                          label={title}
                          onToggle={() => invoiceLines.toggle(i.id)}
                        />
                        {partyName(data, i.providerPartyId)}
                      </td>
                      <td>
                        <DocButton
                          data={data}
                          id={i.sourceDocumentId}
                          fallback={title}
                          onOpen={readDocument}
                        />
                      </td>
                      <td className="muted hide-sm">
                        {docDate(i.sourceDocumentId)
                          ? calendarDate(docDate(i.sourceDocumentId))
                          : ""}
                      </td>
                      <td>
                        <span
                          className="status"
                          data-tone={paid ? "done" : requested ? "waiting" : "attention"}
                        >
                          {paid
                            ? `Paid ${calendarDate(paid.observedAt ?? paid.requestedAt)}`
                            : requested
                              ? "Payment requested"
                              : `Due ${calendarDate(i.dueAt)}`}
                        </span>
                      </td>
                      <td className="num strong">{money(i.totalCents, i.currency)}</td>
                    </tr>
                    {open &&
                      i.lines.map((line, n) => (
                        <tr
                          key={line.lineId}
                          className={`line-row${n === i.lines.length - 1 ? " last" : ""}`}
                          id={n === 0 ? `lines-${i.id}` : undefined}
                        >
                          <td />
                          <td colSpan={3}>{line.description}</td>
                          <td className="num">
                            {i.lines.length > 1 ? money(line.amountCents, i.currency) : ""}
                          </td>
                        </tr>
                      ))}
                  </Fragment>
                );
              })}
            </tbody>
            {invoices.length > 1 && (
              <tfoot>
                <tr>
                  <td colSpan={4}>Total invoiced</td>
                  <td className="num">
                    {money(sumCents(invoices.map((i) => i.totalCents)), invoices[0]!.currency)}
                  </td>
                </tr>
              </tfoot>
            )}
          </table>
        ) : (
          <p className="faint section-empty">No invoices yet.</p>
        )}
      </section>
      <section className="section" aria-labelledby="quotes-title">
        <header>
          <h2 id="quotes-title">Quotes</h2>
          <span className="faint">{quotes.length}</span>
          {quotes.length > 0 && <AllToggle state={quoteLines} ids={quotes.map((q) => q.id)} />}
        </header>
        {quotes.length ? (
          <table className="rows ledger lined docs">
            <colgroup>
              <col className="col-name" />
              <col />
              <col className="col-date hide-sm" />
              <col className="col-status" />
              <col className="col-amount" />
            </colgroup>
            <thead>
              <tr>
                <th>Vendor</th>
                <th>For</th>
                <th className="hide-sm">Valid until</th>
                <th>Status</th>
                <th className="num">Amount</th>
              </tr>
            </thead>
            <tbody>
              {quotes.map((q) => {
                const states = q.lines.map((line) => lineState(data, q.id, line.lineId));
                const quoteState = states.every((x) => x === "Ordered")
                  ? "Ordered"
                  : states.includes("Ordered")
                    ? "Partly ordered"
                    : states.includes("Approved")
                      ? "Approved"
                      : states.includes("In proposed plan")
                        ? "In proposed plan"
                        : q.status;
                const open = quoteLines.opened.has(q.id);
                return (
                  <Fragment key={q.id}>
                    <tr
                      className={row(`quote:${q.id}:${q.status}`, q.sourceDocumentId, "group-head")}
                    >
                      <td title={partyName(data, q.providerPartyId)}>
                        <Disclose
                          open={open}
                          label={q.title}
                          onToggle={() => quoteLines.toggle(q.id)}
                        />
                        {partyName(data, q.providerPartyId)}
                      </td>
                      <td>
                        <DocButton
                          data={data}
                          id={q.sourceDocumentId}
                          fallback={q.title}
                          onOpen={readDocument}
                        />
                      </td>
                      <td className="muted hide-sm">{calendarDate(q.validUntil)}</td>
                      <td>
                        <span className="status" data-tone={TONE[quoteState]}>
                          {quoteState}
                        </span>
                      </td>
                      <td className="num strong">{money(q.totalCents, q.currency)}</td>
                    </tr>
                    {open &&
                      q.lines.map((line, n) => (
                        <tr
                          key={line.lineId}
                          className={`line-row${n === q.lines.length - 1 ? " last" : ""}`}
                          id={n === 0 ? `lines-${q.id}` : undefined}
                        >
                          <td />
                          <td colSpan={new Set(states).size > 1 ? 2 : 3}>{line.description}</td>
                          {new Set(states).size > 1 && (
                            <td>
                              <span className="status" data-tone={TONE[states[n]!]}>
                                {states[n]}
                              </span>
                            </td>
                          )}
                          <td className="num">
                            {q.lines.length > 1 ? money(line.amountCents, q.currency) : ""}
                          </td>
                        </tr>
                      ))}
                  </Fragment>
                );
              })}
            </tbody>
            <tfoot>
              {(() => {
                const byState = LINE_STATES.map((state) => ({
                  state,
                  cents: quotes.flatMap((q) =>
                    q.lines
                      .filter((line) => lineState(data, q.id, line.lineId) === state)
                      .map((line) => line.amountCents),
                  ),
                })).filter((row) => row.cents.length);
                const currency = quotes[0]!.currency;
                return [
                  ...byState.map((row) => (
                    <tr key={row.state}>
                      <td colSpan={4}>{row.state}</td>
                      <td className="num">{money(sumCents(row.cents), currency)}</td>
                    </tr>
                  )),
                  byState.length > 1 && (
                    <tr key="total" className="grand">
                      <td colSpan={4}>Total quoted</td>
                      <td className="num">
                        {money(sumCents(quotes.map((q) => q.totalCents)), currency)}
                      </td>
                    </tr>
                  ),
                ];
              })()}
            </tfoot>
          </table>
        ) : (
          <p className="faint section-empty">No quotes yet.</p>
        )}
      </section>
      {payments.length > 0 && (
        <section className="section" aria-labelledby="payments-title">
          <header>
            <h2 id="payments-title">Payments</h2>
            <span className="faint">{payments.length}</span>
          </header>
          <table className="rows ledger docs">
            <colgroup>
              <col className="col-name" />
              <col />
              <col className="col-date hide-sm" />
              <col className="col-status" />
              <col className="col-amount" />
            </colgroup>
            <thead>
              <tr>
                <th>Vendor</th>
                <th>For</th>
                <th className="hide-sm">Date</th>
                <th>Status</th>
                <th className="num">Amount</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((p) => {
                const job = data.jobs.find((j) => j.id === p.jobId);
                return (
                  <tr key={p.id} className={row(`payment:${p.id}:${p.status}`, null)}>
                    <td title={job ? partyName(data, job.providerPartyId) : undefined}>
                      {job ? partyName(data, job.providerPartyId) : ""}
                    </td>
                    <td>
                      {p.purpose === "Advance"
                        ? "Advance"
                        : data.payments.some(
                              (a) =>
                                a.jobId === p.jobId &&
                                a.purpose === "Advance" &&
                                a.status === "Settled",
                            )
                          ? "Balance after advance"
                          : "Invoice"}
                      {job ? ` · ${job.title}` : ""}
                    </td>
                    <td className="muted hide-sm">{calendarDate(p.observedAt ?? p.requestedAt)}</td>
                    <td>
                      <span
                        className="status"
                        data-tone={
                          p.status === "Settled"
                            ? "done"
                            : outstanding(p.status)
                              ? "waiting"
                              : "problem"
                        }
                      >
                        {p.status === "Settled"
                          ? "Paid"
                          : p.status === "Uncertain"
                            ? "Not yet confirmed"
                            : outstanding(p.status)
                              ? "Requested"
                              : p.status}
                      </span>
                    </td>
                    <td className="num">{money(p.amountCents, p.currency)}</td>
                  </tr>
                );
              })}
            </tbody>
            {payments.length > 1 && (
              <tfoot>
                <tr>
                  <td colSpan={4}>Total paid</td>
                  <td className="num">
                    {money(
                      sumCents(
                        payments.filter((p) => p.status === "Settled").map((p) => p.amountCents),
                      ),
                      payments[0]!.currency,
                    )}
                  </td>
                </tr>
              </tfoot>
            )}
          </table>
        </section>
      )}
    </div>
  );
}

/**
 * A document opened from a money table, in a right-hand drawer (Stripe / Ramp detail drawer). The drawer is the
 * only thing that scrolls while it's open: the page behind is locked, Escape and the backdrop close it, and focus
 * moves into it.
 */
export function MoneyDrawer({ onClose, children }: { onClose(): void; children: ReactNode }) {
  const panel = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    panel.current?.focus();
    const key = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    document.addEventListener("keydown", key);
    return () => {
      document.body.style.overflow = previous;
      document.removeEventListener("keydown", key);
    };
  }, [onClose]);
  return (
    <div className="drawer-layer">
      <div className="drawer-backdrop" aria-hidden="true" onClick={onClose} />
      <div
        className="drawer"
        role="dialog"
        aria-modal="true"
        aria-labelledby="doc-title"
        ref={panel}
        tabIndex={-1}
      >
        {children}
      </div>
    </div>
  );
}
