import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { HandoffNotFound, ReadNotice } from "./App";
import { MAX_STEPS, type StepRecord, type StopReason, runSteps } from "./caseSteps";
import { HandoffError } from "./contracts";
import { calendarDate } from "./format";
import { useHandoffRead, useHandoffStore } from "./hooks";
import { agentLabel, statusLabel } from "./view";

const REASONS: Record<StopReason, string> = {
  decision: "Stopped: a plan is ready for your decision.",
  attention: "Stopped: Handoff needs attention.",
  ready: "Stopped: the unit is ready.",
  unchanged: "Stopped: the last step changed nothing. Handoff is waiting for new information.",
  limit: `Stopped after ${MAX_STEPS} steps.`,
  stopped: "Stopped.",
  refused: "Stopped: the step was refused three times in a row.",
  stepped: "Step finished.",
};
const clock = (ms: number) =>
  new Date(ms).toLocaleTimeString(undefined, {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
  });

/** Admin-only page that runs Resume handoff back to back. Not linked from the app. */
export function CaseControlsPage({ handoffId }: { handoffId: string }) {
  const store = useHandoffStore();
  const resource = store.workspace(handoffId);
  const read = useHandoffRead(resource);
  const [running, setRunning] = useState<"once" | "run" | null>(null);
  const [log, setLog] = useState<StepRecord[]>([]);
  const [result, setResult] = useState<string>();
  const stop = useRef(false);
  useEffect(
    () => () => {
      stop.current = true;
    },
    [],
  );
  const data = read.data;
  if (!data) {
    return read.failed ? (
      <ReadNotice failureKind={read.failureKind} onRetry={() => void read.refresh()} />
    ) : (
      <div className="loading" role="status">
        Loading…
      </div>
    );
  }
  if (!data.permissions.canConfigure) {
    return <HandoffNotFound />;
  }
  const resume = store.gateway.resume?.bind(store.gateway);
  const start = async (mode: "once" | "run") => {
    if (!resume || running) {
      return;
    }
    stop.current = false;
    setRunning(mode);
    setResult(undefined);
    try {
      const outcome = await runSteps({
        once: mode === "once",
        step: () => resume(handoffId),
        read: async () => {
          await resource.fresh();
          const snapshot = resource.getSnapshot();
          if (snapshot.failed || !snapshot.data) {
            throw new HandoffError(snapshot.failureKind);
          }
          return snapshot.data;
        },
        onStep: (record) => setLog((prev) => [record, ...prev]),
        stopped: () => stop.current,
        sleep: (ms) => new Promise((resolve) => setTimeout(resolve, ms)),
        now: () => Date.now(),
      });
      setResult(
        outcome.reason === "refused"
          ? `${REASONS.refused} ${outcome.detail ?? ""}`
          : REASONS[outcome.reason],
      );
    } catch (error) {
      setResult(
        error instanceof HandoffError && error.kind === "permission"
          ? "Resume handoff isn't allowed for this app yet. Allow it in Developer Console."
          : `Stopped: ${error instanceof Error ? error.message : "the step failed"}.`,
      );
    } finally {
      setRunning(null);
    }
  };
  const today = data.handoff.businessDate;
  return (
    <>
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link to={`/handoffs/${encodeURIComponent(handoffId)}`}>{data.property.name}</Link>
        <span>/</span>
        <span>Case controls</span>
      </nav>
      <div className="list-head">
        <div>
          <h1>Case controls</h1>
          <p>Run Handoff&rsquo;s next step as soon as the last one finishes.</p>
        </div>
      </div>
      <section className="section" aria-label="Case">
        <dl className="money-grid controls-facts">
          <div>
            <dt>Case date</dt>
            <dd>{today ? calendarDate(today) : "—"}</dd>
          </div>
          <div>
            <dt>Unit</dt>
            <dd>{statusLabel(data.handoff.physicalProgress)}</dd>
          </div>
          <div>
            <dt>Handoff</dt>
            <dd>{agentLabel(data.agent.status)}</dd>
          </div>
        </dl>
        <p className="controls-next">{data.agent.nextStep}</p>
        <div className="actions controls-actions">
          <button
            type="button"
            className="btn"
            disabled={Boolean(running) || !resume}
            onClick={() => void start("once")}
          >
            {running === "once" ? "Running…" : "Next step"}
          </button>
          <button
            type="button"
            className="btn primary"
            disabled={Boolean(running) || !resume}
            onClick={() => void start("run")}
          >
            {running === "run" ? "Running…" : "Run until Handoff needs you"}
          </button>
          <button
            type="button"
            className="btn quiet"
            disabled={!running}
            onClick={() => {
              stop.current = true;
            }}
          >
            Stop
          </button>
        </div>
        {result && (
          <p className="notice" role="status">
            {result}
          </p>
        )}
      </section>
      {log.length > 0 && (
        <div className="table-card">
          <table className="rows" aria-label="Steps">
            <thead>
              <tr>
                <th>Step</th>
                <th>Started</th>
                <th className="num">Took</th>
                <th>Result</th>
                <th>Case date</th>
                <th>Next step</th>
              </tr>
            </thead>
            <tbody>
              {log.map((row, index) => (
                <tr key={`${row.at}-${index}`}>
                  <td>{row.n || "—"}</td>
                  <td>{clock(row.at)}</td>
                  <td className="num">{(row.ms / 1000).toFixed(1)} s</td>
                  <td>
                    {row.outcome === "changed"
                      ? agentLabel(row.status)
                      : row.outcome === "unchanged"
                        ? "No change"
                        : "Refused, retrying"}
                  </td>
                  <td>{row.caseDate ? calendarDate(row.caseDate) : ""}</td>
                  <td className="muted">{row.detail}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}

export function CaseControlsRoute() {
  const { handoffId } = useParams();
  return handoffId && handoffId.length <= 512 ? (
    <CaseControlsPage key={handoffId} handoffId={handoffId} />
  ) : (
    <HandoffNotFound />
  );
}
