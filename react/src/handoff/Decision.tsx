import { useState } from "react";
import type { HandoffWorkspace, SourceDocument, WorkPlan, WorkSelection } from "./contracts";
import { calendarDate, money, readablePerson } from "./format";
import { useHandoffStore } from "./hooks";
import { useArrivals } from "./motion";
import { MAX_WORK_BUDGET_CENTS, budgetInput, parseBudget } from "./state";
import {
  type PlanLine,
  acceptedPlan,
  byVendor,
  planLines,
  sumCents,
  unselectedLines,
} from "./view";

const key = (quoteId: string, lineId: string) => `${quoteId}\n${lineId}`;

function LineTable({
  data,
  plan,
  lines,
  readDocument,
  totals,
}: {
  data: HandoffWorkspace;
  plan: WorkPlan;
  lines: PlanLine[];
  readDocument(document: SourceDocument): void;
  totals: [string, string][];
}) {
  const currency = plan.currency;
  const groups = byVendor(data, lines);
  return (
    <table className="lines">
      <thead>
        <tr>
          <th>Work</th>
          <th className="num">Amount</th>
        </tr>
      </thead>
      {groups.length === 0 && (
        // Plans saved before quoted-line selections existed carry their scope as text only.
        <tbody>
          {plan.scope.map((scope, index) => (
            <tr
              key={scope}
              className={`line-row${index === plan.scope.length - 1 ? " last-row" : ""}`}
            >
              <td>{scope}</td>
              <td />
            </tr>
          ))}
        </tbody>
      )}
      {groups.map((group) => {
        const source = data.documents.find((d) => d.id === group.quote.sourceDocumentId);
        return (
          <tbody key={group.quote.id}>
            <tr className="vendor-row">
              <td>
                <span className="vendor">{group.vendor}</span>
                {source && (
                  <button
                    type="button"
                    className="link quote-link"
                    onClick={() => readDocument(source)}
                  >
                    View quote
                  </button>
                )}
                <div className="terms">
                  {group.lines.length < group.quote.lines.length
                    ? `${group.lines.length} of ${group.quote.lines.length} quoted items · `
                    : ""}
                  {group.quote.paymentTerms}
                </div>
              </td>
              <td />
            </tr>
            {group.lines.map((entry, index) => (
              <tr
                key={entry.line.lineId}
                className={`line-row${index === group.lines.length - 1 ? " last-row" : ""}`}
              >
                <td>
                  <details className="line-desc">
                    <summary>{entry.line.description}</summary>
                    <p className="scope">{entry.selection.scope}</p>
                    {entry.selection.reason && <p className="reason">{entry.selection.reason}</p>}
                  </details>
                </td>
                <td className="num muted">{money(entry.line.amountCents, currency)}</td>
              </tr>
            ))}
          </tbody>
        );
      })}
      <tfoot>
        {totals.map(([label, cents], index) => (
          <tr key={label} className={index === totals.length - 1 ? "grand" : ""}>
            <td className="total-label">{label}</td>
            <td className="num">{money(cents, currency)}</td>
          </tr>
        ))}
      </tfoot>
    </table>
  );
}

/** Edits live in the store's draft, so they survive refreshes and are re-checked against the latest plan. */
function ChangeEditor({
  data,
  plan,
  stale,
  onAsk,
}: {
  data: HandoffWorkspace;
  plan: WorkPlan;
  stale: boolean;
  onAsk(): void;
}) {
  const store = useHandoffStore();
  const [requirement, setRequirement] = useState("");
  const draft = store.draft(plan)!;
  const selections: WorkSelection[] = draft.changes?.selections ?? plan.selections;
  const requirements = draft.changes?.fixedRequirements ?? plan.fixedRequirements;
  const chosen = new Set(selections.map((s) => key(s.quoteId, s.quoteLineId)));
  const offered = [
    ...planLines(data, plan.selections).map(({ quote, line }) => ({ quote, line })),
    ...unselectedLines(data, plan.selections),
  ];
  const quotes = data.quotes.filter((q) => offered.some((o) => o.quote.id === q.id));
  const selectionsChanged =
    selections.length !== plan.selections.length ||
    selections.some(
      (s) =>
        !plan.selections.some((p) => p.quoteId === s.quoteId && p.quoteLineId === s.quoteLineId),
    );
  const requirementsChanged =
    requirements.length !== plan.fixedRequirements.length ||
    requirements.some((r, i) => r !== plan.fixedRequirements[i]);
  const workCents = selectionsChanged
    ? sumCents(planLines(data, selections).map((l) => l.line.amountCents))
    : plan.estimatedCostCents;
  const budgetCents = parseBudget(draft.value);
  const outdated = draft.revision !== plan.revision || draft.reviewedPlanId !== plan.id;
  const busy = store.isSending(data.handoff.id) || Boolean(store.pending(data.handoff.id));
  const problem =
    budgetCents === undefined
      ? "Enter the budget as an amount, for example 2700.00."
      : BigInt(budgetCents) > MAX_WORK_BUDGET_CENTS
        ? `Enter a budget of ${money(MAX_WORK_BUDGET_CENTS.toString(), plan.currency)} or less.`
        : plan.selections.length > 0 && selections.length === 0
          ? "Keep at least one item of work."
          : BigInt(budgetCents) < BigInt(workCents)
            ? "The budget must cover the work."
            : undefined;
  const changed = selectionsChanged || requirementsChanged || budgetCents !== plan.budgetCents;

  function setChanges(next: { selections?: WorkSelection[]; fixedRequirements?: string[] }) {
    const nextSelections = next.selections ?? selections;
    // A budget that was tracking the work total keeps tracking it; a typed budget stays as typed.
    const tracking = budgetCents === workCents;
    store.editProposal(plan, {
      selections: nextSelections,
      fixedRequirements: next.fixedRequirements ?? requirements,
    });
    if (tracking && next.selections) {
      store.edit(
        plan,
        budgetInput(sumCents(planLines(data, nextSelections).map((l) => l.line.amountCents))),
      );
    }
  }
  function toggle(quoteId: string, lineId: string, description: string) {
    const k = key(quoteId, lineId);
    const existing = plan.selections.find((s) => key(s.quoteId, s.quoteLineId) === k);
    setChanges({
      selections: chosen.has(k)
        ? selections.filter((s) => key(s.quoteId, s.quoteLineId) !== k)
        : [
            ...selections,
            existing ?? {
              quoteId,
              quoteLineId: lineId,
              scope: description,
              reason: "Added during review.",
            },
          ],
    });
  }
  async function save() {
    if (problem || !budgetCents || outdated) {
      return;
    }
    if (!selectionsChanged && !requirementsChanged) {
      await store.submit(data, "budget", budgetCents);
    } else {
      await store.submit(data, "plan", undefined, {
        budgetCents,
        ...(selectionsChanged ? { selections } : {}),
        ...(requirementsChanged ? { fixedRequirements: requirements } : {}),
      });
    }
  }

  return (
    <div className="editor">
      {outdated && (
        <div className="notice" role="status">
          <p>The plan changed while you were editing. Review it before saving.</p>
          <button type="button" className="btn" onClick={() => store.reviewLatest(plan)}>
            I’ve reviewed the updated plan
          </button>
        </div>
      )}
      {quotes.length > 0 && (
        <fieldset className="field">
          <legend className="label">Work</legend>
          {quotes.map((quote) => (
            <div className="pick-group" key={quote.id}>
              <div className="pick-vendor">
                {data.parties.find((p) => p.id === quote.providerPartyId)?.name}
              </div>
              {quote.lines
                .filter((line) =>
                  offered.some((o) => o.quote.id === quote.id && o.line.lineId === line.lineId),
                )
                .map((line) => (
                  <label className="pick" key={line.lineId}>
                    <input
                      type="checkbox"
                      checked={chosen.has(key(quote.id, line.lineId))}
                      onChange={() => toggle(quote.id, line.lineId, line.description)}
                    />
                    <span>{line.description}</span>
                    <span className="num">{money(line.amountCents, quote.currency)}</span>
                  </label>
                ))}
            </div>
          ))}
        </fieldset>
      )}
      <div className="field">
        <label className="label" htmlFor="budget">
          Budget ({plan.currency})
        </label>
        <input
          id="budget"
          className="input money"
          inputMode="decimal"
          value={draft.value}
          onChange={(e) => store.edit(plan, e.target.value)}
        />
        <p className="hint">
          {problem ? (
            <span role="alert">{problem}</span>
          ) : (
            `Work total ${money(workCents, plan.currency)}`
          )}
        </p>
      </div>
      <div className="field">
        <span className="label">Requirements</span>
        <ul className="file-list">
          {requirements.map((r) => (
            <li key={r}>
              <span>{r}</span>
              {!plan.fixedRequirements.includes(r) && (
                <button
                  type="button"
                  className="link"
                  onClick={() =>
                    setChanges({ fixedRequirements: requirements.filter((x) => x !== r) })
                  }
                >
                  Remove
                </button>
              )}
            </li>
          ))}
        </ul>
        <div className="req-edit">
          <input
            className="input"
            placeholder="Add a requirement"
            aria-label="New requirement"
            value={requirement}
            onChange={(e) => setRequirement(e.target.value)}
          />
          <button
            type="button"
            className="btn"
            disabled={!requirement.trim() || requirements.includes(requirement.trim())}
            onClick={() => {
              setChanges({ fixedRequirements: [...requirements, requirement.trim()] });
              setRequirement("");
            }}
          >
            Add
          </button>
        </div>
      </div>
      <div className="decision-actions" style={{ padding: "0 0 18px" }}>
        <button
          type="button"
          className="btn primary"
          disabled={Boolean(problem) || !changed || outdated || busy || stale || store.blocked()}
          onClick={() => void save()}
        >
          Save changes
        </button>
        <button type="button" className="btn" disabled={busy} onClick={() => store.discard(plan)}>
          Cancel
        </button>
        <span className="spacer" />
        <button type="button" className="link" onClick={onAsk}>
          Or describe the change to Handoff
        </button>
      </div>
    </div>
  );
}

export function DecisionSheet({
  data,
  stale,
  readDocument,
  onAsk,
}: {
  data: HandoffWorkspace;
  stale: boolean;
  readDocument(document: SourceDocument): void;
  onAsk(): void;
}) {
  const store = useHandoffStore();
  const plan = data.workPlan!;
  const id = data.handoff.id;
  const draft = store.draft(plan);
  const pending = store.pending(id);
  const busy = store.isSending(id) || Boolean(pending);
  const blocked = stale || store.blocked() || busy;
  return (
    <section className="section decision" aria-labelledby="decision-title">
      <div className="decision-top">
        <div className="eyebrow">Needs your decision</div>
        <h2 id="decision-title">{plan.title}</h2>
        <p>{plan.summary}</p>
      </div>
      {draft && data.permissions.canDecide ? (
        <ChangeEditor data={data} plan={plan} stale={stale} onAsk={onAsk} />
      ) : (
        <>
          <LineTable
            data={data}
            plan={plan}
            lines={planLines(data, plan.selections)}
            readDocument={readDocument}
            totals={
              plan.budgetCents === plan.estimatedCostCents
                ? [["Total", plan.budgetCents]]
                : [
                    ["Work total", plan.estimatedCostCents],
                    ["Budget for this plan", plan.budgetCents],
                  ]
            }
          />
          {plan.fixedRequirements.length > 0 && (
            <div className="reqs">
              <h3>Requirements</h3>
              <ul>
                {plan.fixedRequirements.map((r) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
            </div>
          )}
          <details className="why">
            <summary>Why this plan</summary>
            <p>{plan.rationale}</p>
          </details>
          <div className="decision-actions">
            {data.permissions.canDecide ? (
              <>
                <button
                  type="button"
                  className="btn primary"
                  disabled={blocked}
                  onClick={() => void store.submit(data, "accept")}
                >
                  {busy && pending?.reference.kind === "accept"
                    ? "Accepting…"
                    : `Accept plan · ${money(plan.budgetCents, plan.currency)}`}
                </button>
                <button
                  type="button"
                  className="btn"
                  disabled={blocked}
                  onClick={() => store.edit(plan, budgetInput(plan.budgetCents))}
                >
                  Change
                </button>
              </>
            ) : (
              <span className="faint">Someone with approval access decides this plan.</span>
            )}
          </div>
        </>
      )}
    </section>
  );
}

export function AcceptedPlan({
  data,
  readDocument,
}: {
  data: HandoffWorkspace;
  readDocument(document: SourceDocument): void;
}) {
  const [open, setOpen] = useState(false);
  const accepted = acceptedPlan(data);
  // The decision card gives way to this line when a plan is accepted; it unfolds in place.
  const fresh = useArrivals(accepted ? [accepted.decision.id] : []);
  if (!accepted) {
    return null;
  }
  const { plan, decision } = accepted;
  return (
    <section
      className={`section${fresh.has(decision.id) ? " unfold" : ""}`}
      aria-labelledby="accepted-title"
    >
      <div className="accepted">
        <div>
          <div className="eyebrow">Accepted plan</div>
          <h2 id="accepted-title">{plan.title}</h2>
          <p className="muted">
            Accepted by {readablePerson(decision.by)} on {calendarDate(decision.at)} ·{" "}
            {money(plan.estimatedCostCents, decision.currency)} of{" "}
            {money(decision.budgetCents, decision.currency)} budget
            {data.decisions.length > 1 ? ` · ${data.decisions.length} plans accepted` : ""}
          </p>
        </div>
        <button type="button" className="btn" onClick={() => setOpen(!open)} aria-expanded={open}>
          {open ? "Hide plan" : "View plan"}
        </button>
      </div>
      {open && (
        <LineTable
          data={data}
          plan={plan}
          lines={planLines(data, plan.selections)}
          readDocument={readDocument}
          totals={[["Budget", decision.budgetCents]]}
        />
      )}
    </section>
  );
}
