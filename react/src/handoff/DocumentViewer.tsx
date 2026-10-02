import { useCallback, useEffect, useRef, useState } from "react";
import { documentKey } from "./contracts";
import type { HandoffGateway, HandoffWorkspace, SourceDocument } from "./contracts";
import { calendarDate, money } from "./format";
import { documentForm } from "./model";
import { conditionLines, groupFindings, partyName } from "./view";

function downloadName(document: SourceDocument, pdf: boolean, type: string): string {
  const base =
    document.title
      .replace(/\.(pdf|png|jpe?g|gif|webp)$/iu, "")
      .replace(/[^\p{L}\p{N} ,-]/gu, "")
      .slice(0, 80) || "Document";
  return `${base}.${pdf ? "pdf" : type.split("/")[1] || "file"}`;
}

/** Opens the protected original through the gateway; the object URL lives only while this view is open. */
function FileView({
  document,
  gateway,
  onInvalidated,
}: {
  document: SourceDocument;
  gateway: HandoffGateway;
  onInvalidated(): void;
}) {
  const [original, setOriginal] = useState<{ url: string; type: string }>();
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [revoked, setRevoked] = useState(false);
  // Keyed by the canonical document identity; equivalent polling reads must not revoke the open file.
  const source = useRef(document).current;
  const alive = useRef(true),
    permitted = useRef(true),
    generation = useRef(0),
    file = useRef<string>();
  useEffect(() => {
    alive.current = true;
    const lifetime = generation.current + 1;
    generation.current = lifetime;
    setOriginal(undefined);
    setLoading(false);
    const release = () => {
      if (file.current) {
        URL.revokeObjectURL(file.current);
        file.current = undefined;
      }
    };
    const stop = gateway.onDocumentInvalidated?.(source, () => {
      permitted.current = false;
      release();
      if (alive.current) {
        setOriginal(undefined);
        setRevoked(true);
        onInvalidated();
      }
    });
    return () => {
      alive.current = false;
      generation.current = lifetime + 1;
      stop?.();
      release();
    };
  }, [source, gateway, onInvalidated]);
  const openFile = useCallback(async () => {
    if (!permitted.current) {
      return;
    }
    const ticket = generation.current;
    setLoading(true);
    setFailed(false);
    try {
      const blob = await gateway.document(source);
      if (!alive.current || !permitted.current || ticket !== generation.current) {
        return;
      }
      file.current = URL.createObjectURL(blob);
      setOriginal({ url: file.current, type: blob.type });
    } catch {
      if (alive.current && ticket === generation.current) {
        setFailed(true);
      }
    } finally {
      if (alive.current && ticket === generation.current) {
        setLoading(false);
      }
    }
  }, [gateway, source]);
  useEffect(() => {
    void openFile();
  }, [openFile]);
  const pdf = original
    ? original.type === "application/pdf"
    : document.mimeType === "application/pdf";
  if (revoked) {
    return (
      <div role="alert" className="notice problem">
        This file is no longer available. Close it and refresh.
      </div>
    );
  }
  return (
    <>
      <div className="file-bar">
        {original && (
          <a
            className="btn"
            href={original.url}
            download={downloadName(document, pdf, original.type)}
          >
            Download
          </a>
        )}
        {loading && <span className="faint">Opening…</span>}
      </div>
      {failed && (
        <div role="alert" className="notice problem">
          <p>We couldn’t open this file.</p>
          <button type="button" className="btn" onClick={() => void openFile()}>
            Try again
          </button>
        </div>
      )}
      {original &&
        (pdf ? (
          <iframe
            src={`${original.url}#page=${document.pageStart ?? 1}`}
            title={document.title}
            className="pdf"
          />
        ) : (
          <img className="pdf" src={original.url} alt={document.title} />
        ))}
    </>
  );
}

/** An invoice, quote or report laid out as the document it stands for, from the saved record. */
function RenderedDocument({
  data,
  document,
}: {
  data: HandoffWorkspace;
  document: SourceDocument;
}) {
  const form = documentForm(data, document);
  const invoice = data.invoices.find((i) => i.sourceDocumentId === document.id);
  const quote = data.quotes.find((q) => q.sourceDocumentId === document.id);
  const report = data.inspections.find((i) => i.sourceDocumentId === document.id);
  const vendorId = invoice?.providerPartyId ?? quote?.providerPartyId ?? report?.observerPartyId;
  const vendor = partyName(data, vendorId);
  const paid =
    invoice &&
    data.payments.find(
      (p) => p.jobId === invoice.jobId && p.purpose !== "Advance" && p.status === "Settled",
    );
  // Everything settled on this job counts toward the invoice, the advance included.
  const paidCents = invoice
    ? data.payments
        .filter((p) => p.jobId === invoice.jobId && p.status === "Settled")
        .reduce((sum, p) => sum + BigInt(p.amountCents), 0n)
    : 0n;
  const dueCents = invoice ? BigInt(invoice.totalCents) - paidCents : 0n;
  const invoiceTerms = invoice
    ? data.quotes.find((q) => q.id === data.jobs.find((j) => j.id === invoice.jobId)?.quoteId)
        ?.paymentTerms
    : undefined;
  const lines = invoice?.lines ?? quote?.lines ?? [];
  const currency = invoice?.currency ?? quote?.currency ?? "USD";
  const title = form === "invoice" ? "Invoice" : form === "quote" ? "Quote" : "Report";
  return (
    <article className="paper" aria-label={`${title} from ${vendor}`}>
      <header className="paper-head">
        <div>
          <div className="paper-vendor">{vendor}</div>
        </div>
        <div className="paper-kind">
          <div className="paper-title">{title}</div>
          <div className="faint">
            {calendarDate(
              document.availableFrom ?? report?.observedAt ?? data.handoff.businessDate,
            )}
          </div>
          {paid && (
            <div className="paid-badge" aria-label="Paid">
              Paid {calendarDate(paid.observedAt ?? paid.requestedAt)}
            </div>
          )}
        </div>
      </header>
      {invoice && (
        <dl className="paper-meta">
          <div>
            <dt>Bill to</dt>
            <dd>{partyName(data, invoice.payerPartyId)}</dd>
          </div>
          <div>
            <dt>Service address</dt>
            <dd>{data.property.address}</dd>
          </div>
          <div>
            <dt>Due</dt>
            <dd>{calendarDate(invoice.dueAt)}</dd>
          </div>
        </dl>
      )}
      {quote && (
        <dl className="paper-meta">
          <div>
            <dt>For</dt>
            <dd>{quote.title}</dd>
          </div>
          <div>
            <dt>Earliest start</dt>
            <dd>{calendarDate(quote.availableFrom)}</dd>
          </div>
          <div>
            <dt>Valid until</dt>
            <dd>{calendarDate(quote.validUntil)}</dd>
          </div>
        </dl>
      )}
      {lines.length > 0 && (
        <table className="paper-lines">
          <thead>
            <tr>
              <th>Description</th>
              <th className="num">Amount</th>
            </tr>
          </thead>
          <tbody>
            {lines.map((line) => (
              <tr key={line.lineId}>
                <td>{line.description}</td>
                <td className="num">{money(line.amountCents, currency)}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            {quote && BigInt(quote.depositCents) > 0n && (
              <tr>
                <td>Advance on booking</td>
                <td className="num">{money(quote.depositCents, currency)}</td>
              </tr>
            )}
            <tr className="grand">
              <td>Total</td>
              <td className="num">
                {money(invoice?.totalCents ?? quote?.totalCents ?? "0", currency)}
              </td>
            </tr>
            {invoice && (
              <>
                <tr>
                  <td>Amount paid</td>
                  <td className="num">{money(paidCents.toString(), currency)}</td>
                </tr>
                <tr className="due">
                  <td>Amount due</td>
                  <td className="num">
                    {money((dueCents > 0n ? dueCents : 0n).toString(), currency)}
                  </td>
                </tr>
              </>
            )}
          </tfoot>
        </table>
      )}
      {invoiceTerms && (
        <div className="paper-terms">
          <p>{invoiceTerms}</p>
        </div>
      )}
      {quote && (
        <div className="paper-terms">
          <p>{quote.paymentTerms}</p>
          {quote.requirements.map((r) => (
            <p key={r}>{r}</p>
          ))}
        </div>
      )}
      {report && (
        <table className="paper-lines">
          <thead>
            <tr>
              <th>Condition</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody>
            {groupFindings(report.findings)
              .flatMap((g) =>
                conditionLines(g.observation).map((line) => ({
                  ...line,
                  result: line.result ?? g.findings[0]?.result ?? null,
                })),
              )
              .map((line, i) => (
                <tr key={i}>
                  <td>{line.text}</td>
                  <td>{line.result ?? ""}</td>
                </tr>
              ))}
          </tbody>
        </table>
      )}
      {report && report.findings[0]?.method && (
        <p className="paper-terms">
          Method: {[...new Set(report.findings.map((f) => f.method))].join(" ")}
        </p>
      )}
    </article>
  );
}

/** The selected document, shown in place on the Documents tab. Files are fetched only when shown. */
export function DocumentViewer({
  document,
  documents = [],
  data,
  gateway,
  onClose,
}: {
  document: SourceDocument;
  documents?: SourceDocument[];
  data?: HandoffWorkspace;
  gateway: HandoffGateway;
  onClose(): void;
}) {
  // A record backed by exactly one file opens on that file; its summary is one click back.
  const [selection, setSelection] = useState<{ id: string; key: string } | undefined>(() => {
    const files = (document.sourceDocumentIds ?? [])
      .map((id) =>
        documents.find(
          (d) => d.id === id && d.sourceKind === "Original" && d.mediaSetRid && d.mediaItemRid,
        ),
      )
      .filter((d): d is SourceDocument => Boolean(d));
    const only = files.length === 1 ? files[0] : undefined;
    return only ? { id: only.id, key: documentKey(only) } : undefined;
  });
  const [unavailable, setUnavailable] = useState(false);
  const invalidate = useCallback(() => setUnavailable(true), []);
  const selected = selection
    ? documents.find((d) => d.id === selection.id && documentKey(d) === selection.key)
    : undefined;
  const active = selected ?? document;
  const hasFile = Boolean(active.mediaSetRid && active.mediaItemRid);
  const rendered =
    !hasFile && data && ["invoice", "quote", "report"].includes(documentForm(data, active));
  const supports = (active.sourceDocumentIds ?? [])
    .map((id) =>
      documents.find(
        (d) => d.id === id && d.sourceKind === "Original" && d.mediaSetRid && d.mediaItemRid,
      ),
    )
    .filter((d): d is SourceDocument => Boolean(d));
  return (
    <section className="doc-viewer" aria-labelledby="doc-title">
      <div className="doc-head">
        <div>
          {selected && (
            <button type="button" className="link" onClick={() => setSelection(undefined)}>
              ← {document.title}
            </button>
          )}
          <h2 id="doc-title">{unavailable ? "Document unavailable" : active.title}</h2>
          <p>
            {active.kind}
            {active.availableFrom ? ` · ${calendarDate(active.availableFrom)}` : ""}
          </p>
        </div>
        <div className="doc-actions">
          {rendered && (
            <button type="button" className="btn" onClick={() => window.print()}>
              Print
            </button>
          )}
          <button type="button" className="btn quiet" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
      <div className="doc-body">
        {selection && !selected && (
          <div role="alert" className="notice problem">
            That file changed or is no longer available.
          </div>
        )}
        {hasFile ? (
          <FileView
            key={documentKey(active)}
            document={active}
            gateway={gateway}
            onInvalidated={invalidate}
          />
        ) : rendered && data ? (
          <RenderedDocument data={data} document={active} />
        ) : (
          <>
            <p className="doc-text">{active.text || "No text on file."}</p>
            {supports.length > 0 && (
              <div className="doc-files">
                <div className="subhead">Files</div>
                <ul className="file-list">
                  {supports.map((doc) => (
                    <li key={doc.id}>
                      <button
                        type="button"
                        className="link"
                        onClick={() => setSelection({ id: doc.id, key: documentKey(doc) })}
                      >
                        {doc.title}
                      </button>
                      <span className="kind">PDF</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
    </section>
  );
}
