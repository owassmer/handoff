import type React from "react";
import type { HandoffWorkspace, SourceDocument } from "./contracts";
import { calendarDate, money } from "./format";
import { type Job, jobStage, jobStart, ledger, outstanding } from "./model";
import { useArrivals } from "./motion";
import { moneySummary, partyName, reportConditions, sumCents, unselectedLines } from "./view";

function StageRail({ data, job }: { data: HandoffWorkspace; job: Job }) {
  const stage = jobStage(data, job);
  return (
    <ol className="rail" aria-label={`${job.title} progress`}>
      {stage.steps.map((step) => (
        <li key={step.name} data-done={step.done} data-skipped={step.skipped ? "true" : undefined}>
          <span className="dot" aria-hidden="true" />
          <span className="rail-name">{step.name}</span>
          <span className="rail-date">
            {step.skipped ? "None" : step.date ? calendarDate(step.date) : ""}
          </span>
        </li>
      ))}
    </ol>
  );
}

/** One line per report, counted by condition like an inspection summary; anything not checked is named, never hidden. */
function FindingsLine({
  findings,
  onOpen,
}: {
  findings: { result: string; observation: string }[];
  onOpen(): void;
}) {
  const conditions = reportConditions(findings);
  const needs = conditions.filter((c) => c.result === "needs work").length;
  const unchecked = conditions.filter((c) => c.result === "not checked");
  const parts = [
    `${conditions.length} ${conditions.length === 1 ? "condition" : "conditions"}`,
    needs ? `${needs} ${needs === 1 ? "needs" : "need"} work` : "",
    unchecked.length ? `${unchecked.length} not checked` : "",
  ].filter(Boolean);
  return (
    <div className="job-findings">
      <button type="button" className="link muted" onClick={onOpen}>
        Report: {parts.join(" · ")}
      </button>
      {unchecked.length > 0 && (
        <ul className="job-limits" aria-label="Not checked">
          {unchecked.map((c) => (
            <li key={c.text}>{c.text}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export function WorkSection({
  data,
  readDocument,
}: {
  data: HandoffWorkspace;
  readDocument(document: SourceDocument): void;
}) {
  // Quoted work not yet planned or ordered; once everything is ordered this list disappears.
  const others = unselectedLines(data, data.workPlan?.selections ?? []).filter(
    ({ quote, line }) =>
      !data.jobs.some(
        (job) => job.quoteId === quote.id && job.scope.some((s) => s.lineId === line.lineId),
      ),
  );
  const changedJobs = useArrivals(data.jobs.map((job) => `${job.id}:${jobStage(data, job).label}`));
  if (!data.jobs.length && !others.length) {
    return null;
  }
  const open = (id: string | undefined) => {
    const doc = id ? data.documents.find((d) => d.id === id) : undefined;
    if (doc) {
      readDocument(doc);
    }
  };
  const when = (job: Job) => job.appointmentAt ?? jobStart(data, job);
  const jobs = [...data.jobs].sort((a, b) => when(a).localeCompare(when(b)));
  const closed = jobs.filter((job) => jobStage(data, job).closed).length;
  return (
    <section className="section" aria-labelledby="work-title">
      <header>
        <h2 id="work-title">Work</h2>
        {jobs.length > 0 && (
          <span className="faint">
            {jobs.length} {jobs.length === 1 ? "job" : "jobs"} · {closed} complete
          </span>
        )}
      </header>
      <div className="section-body">
        {data.jobs.length > 0 && (
          <ul className="jobs">
            {jobs.map((job) => {
              const stage = jobStage(data, job);
              const quote = data.quotes.find((q) => q.id === job.quoteId);
              const report = data.inspections.find((i) => i.jobId === job.id);
              const invoice = data.invoices.find((i) => i.jobId === job.id);
              return (
                <li
                  className={`job${changedJobs.has(`${job.id}:${stage.label}`) ? " arrive" : ""}`}
                  key={job.id}
                  style={
                    {
                      "--i": [...changedJobs].findIndex((k) => k.startsWith(`${job.id}:`)),
                    } as React.CSSProperties
                  }
                >
                  <div className="job-main">
                    <div className="job-who">
                      <strong>{partyName(data, job.providerPartyId)}</strong>
                      <span className="muted">{job.title}</span>
                    </div>
                    <span className="status stage" data-tone={stage.tone} key={stage.label}>
                      {stage.label}
                    </span>
                    <span className="num">
                      {job.committedCents ? money(job.committedCents, job.currency) : "—"}
                    </span>
                  </div>
                  <StageRail data={data} job={job} />

                  {data.payments
                    .filter((p) => p.jobId === job.id && outstanding(p.status))
                    .map((p) => (
                      <p className="job-findings muted" key={p.id}>
                        {p.status === "Uncertain"
                          ? "Payment not yet confirmed"
                          : `Payment requested ${calendarDate(p.requestedAt)}`}
                        {" · "}
                        {money(p.amountCents, p.currency)}
                      </p>
                    ))}
                  <div className="job-links">
                    {quote && (
                      <button
                        type="button"
                        className="link"
                        onClick={() => open(quote.sourceDocumentId)}
                      >
                        Quote
                      </button>
                    )}
                    {report && (
                      <FindingsLine
                        findings={report.findings}
                        onOpen={() => open(report.sourceDocumentId)}
                      />
                    )}
                    {invoice && (
                      <button
                        type="button"
                        className="link"
                        onClick={() => open(invoice.sourceDocumentId)}
                      >
                        Invoice
                      </button>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        )}
        {others.length > 0 && (
          <>
            <div className="subhead">Quoted, not ordered</div>
            <table className="rows">
              <tbody>
                {others.map(({ quote, line }) => (
                  <tr key={`${quote.id}-${line.lineId}`}>
                    <td>
                      <strong>{partyName(data, quote.providerPartyId)}</strong>
                      <div className="sub-line">
                        <button
                          type="button"
                          className="link"
                          onClick={() => open(quote.sourceDocumentId)}
                        >
                          {line.description}
                        </button>
                      </div>
                    </td>
                    <td className="muted hide-sm">valid to {calendarDate(quote.validUntil)}</td>
                    <td className="num">{money(line.amountCents, quote.currency)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </div>
    </section>
  );
}

/** Overview keeps one line of owner funds; the detail lives on the Money tab. */
export function FundsLine({ data, onOpen }: { data: HandoffWorkspace; onOpen(): void }) {
  const summary = moneySummary(data);
  const changed = useArrivals(
    summary
      ? [`c:${summary.committedCents}`, `p:${summary.paidCents}`, `a:${summary.availableCents}`]
      : [],
  );
  if (!summary) {
    return null;
  }
  const item = (label: string, key: string, cents: string | null) => (
    <div className={changed.has(`${key}:${cents}`) ? "arrive" : undefined}>
      <dt>{label}</dt>
      <dd>{cents === null ? "\u2014" : money(cents, summary.currency)}</dd>
    </div>
  );
  return (
    <section className="section funds-line" aria-labelledby="funds-line-title">
      <h2 id="funds-line-title">Owner funds</h2>
      <dl>
        {item("Set aside", "s", summary.setAsideCents)}
        {item("Committed", "c", summary.committedCents)}
        {item("Paid", "p", summary.paidCents)}
        {item("Available", "a", summary.availableCents)}
      </dl>
      <button type="button" className="btn" onClick={onOpen}>
        Open Money
      </button>
    </section>
  );
}

export function MoneySection({ data }: { data: HandoffWorkspace }) {
  const summary = moneySummary(data);
  const requestedNow = sumCents(ledger(data).map((v) => v.requestedCents));
  const changed = useArrivals(
    summary
      ? [
          `Set aside:${summary.setAsideCents}`,
          `Committed:${summary.committedCents}`,
          `Paid:${summary.paidCents}`,
          `Requested:${requestedNow}`,
          `Available:${summary.availableCents}`,
        ]
      : [],
  );
  if (!summary) {
    return null;
  }
  const order = [...data.jobs]
    .sort((a, b) =>
      (a.appointmentAt ?? jobStart(data, a)).localeCompare(b.appointmentAt ?? jobStart(data, b)),
    )
    .map((j) => j.providerPartyId);
  const vendors = ledger(data).sort((a, b) => order.indexOf(a.partyId) - order.indexOf(b.partyId));
  const requested = sumCents(vendors.map((v) => v.requestedCents));
  const cell = (label: string, cents: string | null) => (
    <div className={changed.has(`${label.split(",")[0]}:${cents}`) ? "arrive" : undefined}>
      <dt>{label}</dt>
      <dd>{cents === null ? "—" : money(cents, summary.currency)}</dd>
    </div>
  );
  return (
    <section className="section" aria-labelledby="money-title">
      <header>
        <h2 id="money-title">Owner funds</h2>
      </header>
      <dl className="money-grid">
        {cell("Set aside", summary.setAsideCents)}
        {cell("Committed", summary.committedCents)}
        {cell("Paid", summary.paidCents)}
        {cell("Requested, not yet paid", requested)}
        {cell("Available", summary.availableCents)}
      </dl>
      {vendors.length > 0 && (
        <table className="rows ledger">
          <thead>
            <tr>
              <th>Vendor</th>
              <th className="num">Committed</th>
              <th className="num hide-sm">Invoiced</th>
              <th className="num">Paid</th>
            </tr>
          </thead>
          <tbody>
            {vendors.map((v) => (
              <tr key={v.partyId}>
                <td>{v.name}</td>
                <td className="num">{money(v.committedCents, v.currency)}</td>
                <td className="num hide-sm">{money(v.invoicedCents, v.currency)}</td>
                <td className="num">{money(v.paidCents, v.currency)}</td>
              </tr>
            ))}
          </tbody>
          {vendors.length > 1 && (
            <tfoot>
              <tr>
                <td>Total</td>
                <td className="num">
                  {money(sumCents(vendors.map((v) => v.committedCents)), summary.currency)}
                </td>
                <td className="num hide-sm">
                  {money(sumCents(vendors.map((v) => v.invoicedCents)), summary.currency)}
                </td>
                <td className="num">
                  {money(sumCents(vendors.map((v) => v.paidCents)), summary.currency)}
                </td>
              </tr>
            </tfoot>
          )}
        </table>
      )}
    </section>
  );
}
