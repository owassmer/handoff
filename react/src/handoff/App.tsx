import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { Link, NavLink, Outlet, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { CalendarView } from "./Calendar";
import { ChatDock } from "./ChatDock";
import { AcceptedPlan, DecisionSheet } from "./Decision";
import { DocumentViewer } from "./DocumentViewer";
import { MoneyDrawer, MoneyTab } from "./Money";
import { DocumentsTab, MessagesTab, TimelineTab } from "./UnitTabs";
import { UpdateToast } from "./UpdateToast";
import { FundsLine, WorkSection } from "./Work";
import { documentKey } from "./contracts";
import type { HandoffError, HandoffWorkspace, SourceDocument } from "./contracts";
import { calendarDate, shortTime } from "./format";
import "./handoff.css";
import { useHandoffRead, useHandoffStore } from "./hooks";
import {
  calendarEvents,
  caseToday,
  dueIn,
  inbox,
  moneyDocumentIds,
  nextVisit,
  waitingOn,
} from "./model";
import { countdown, useAutoDismiss, useNow } from "./motion";
import { useUpdates } from "./updates";
import {
  READINESS_STEPS,
  agentLabel,
  awaitsDecision,
  needsDecision,
  readinessStep,
  statusLabel,
  tone,
} from "./view";

export function HandoffHeader({ name, decisions = 0 }: { name?: string; decisions?: number }) {
  return (
    <header className="topbar">
      <div className="topbar-inner">
        <Link to="/" className="brand">
          Handoff
        </Link>
        <nav aria-label="Main">
          <NavLink to="/" end={false} className={({ isActive }) => (isActive ? "active" : "")}>
            Units
            {decisions > 0 && (
              <span className="count" aria-label={`${decisions} need your decision`}>
                {decisions}
              </span>
            )}
          </NavLink>
          <NavLink to="/calendar">Calendar</NavLink>
        </nav>
        <span className="spacer" />
        {name && <span className="org">{name}</span>}
      </div>
    </header>
  );
}

export function HandoffLayout() {
  const store = useHandoffStore();
  const { data } = useHandoffRead(store.list);
  const decisions = (data?.handoffs ?? []).filter((u) => awaitsDecision(u.physicalProgress)).length;
  return (
    <div className="handoff-app">
      <a className="skip" href="#main">
        Skip to content
      </a>
      <HandoffHeader name={data?.workspace.name} decisions={decisions} />
      <main className="page" id="main">
        <Outlet />
      </main>
    </div>
  );
}

export function ReadNotice({
  onRetry,
  hasData = false,
  failureKind,
}: {
  onRetry(): void;
  hasData?: boolean;
  failureKind?: HandoffError["kind"];
}) {
  const title =
    failureKind === "permission"
      ? "You don’t have access to this workspace yet"
      : failureKind === "access"
        ? "Please sign in to continue"
        : failureKind === "unavailable"
          ? "Handoff can’t connect right now"
          : hasData
            ? "Couldn’t refresh"
            : "Couldn’t load this page";
  const help =
    failureKind === "permission"
      ? "Ask a workspace admin to add you, then try again."
      : failureKind === "access"
        ? "Your sign-in needs to be renewed."
        : hasData
          ? "You’re seeing the last saved information. Your edits are kept; try again before saving."
          : "Try again in a moment.";
  return (
    <div className="notice problem" role="alert">
      <div>
        <strong>{title}</strong>
        <p>{help}</p>
      </div>
      <button type="button" className="btn" onClick={onRetry}>
        Try again
      </button>
    </div>
  );
}

export function HandoffNotFound() {
  return (
    <div className="empty">
      <h1>That unit isn’t available</h1>
      <div className="actions">
        <Link className="btn" to="/">
          Back to units
        </Link>
      </div>
    </div>
  );
}

function Status({ value }: { value: string }) {
  return (
    <span className="status" data-tone={tone(value)}>
      {statusLabel(value) || "Not recorded"}
    </span>
  );
}

export function HandoffListPage() {
  const store = useHandoffStore();
  const read = useHandoffRead(store.list);
  const navigate = useNavigate();
  const units = [...(read.data?.handoffs ?? [])].sort(
    (a, b) =>
      Number(awaitsDecision(b.physicalProgress)) - Number(awaitsDecision(a.physicalProgress)),
  );
  const waiting = units.filter((u) => awaitsDecision(u.physicalProgress)).length;
  return (
    <>
      <div className="list-head">
        <div>
          <h1>Units</h1>
          {read.data && (
            <p>
              {waiting
                ? `${waiting} ${waiting === 1 ? "unit needs" : "units need"} your decision`
                : "Nothing needs you right now"}
            </p>
          )}
        </div>
      </div>
      {read.failed && (
        <ReadNotice
          failureKind={read.failureKind}
          hasData={Boolean(read.data)}
          onRetry={() => void read.refresh()}
        />
      )}
      {!read.data && read.loading && (
        <div className="loading" role="status">
          Loading units…
        </div>
      )}
      {read.data && units.length === 0 && (
        <div className="empty">
          <h2>No move-outs in progress</h2>
        </div>
      )}
      {units.length > 0 && (
        <div className="table-card">
          <table className="units">
            <thead>
              <tr>
                <th>Unit</th>
                <th>Readiness</th>
                <th>Latest</th>
              </tr>
            </thead>
            <tbody>
              {units.map((u) => {
                const href = `/handoffs/${encodeURIComponent(u.id)}`;
                const decide = awaitsDecision(u.physicalProgress);
                return (
                  <tr key={u.id} onClick={() => navigate(href)}>
                    <td className="unit-name">
                      <Link to={href} onClick={(e) => e.stopPropagation()}>
                        {u.propertyName}
                      </Link>
                      {!u.title.startsWith(u.propertyName.split(",")[0]) && <div>{u.title}</div>}
                    </td>
                    <td>
                      <Status value={u.physicalProgress} />
                    </td>
                    <td>
                      {decide ? (
                        <span className="status" data-tone="attention">
                          Review the work plan
                        </span>
                      ) : (
                        <span className="now-cell clamp">{u.nextStep}</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}

const STEP_NAMES = ["Assess", "Plan", "Work", "Ready"];

function UnitHeader({ data }: { data: HandoffWorkspace }) {
  const step = readinessStep(data.handoff.physicalProgress);
  const today = caseToday(data);
  return (
    <div className="unit-head">
      <div>
        <h1>{data.property.name}</h1>
        <p className="sub">
          {data.property.address.startsWith(data.property.name.split(",")[0]!)
            ? data.property.address
                .slice(data.property.name.split(",")[0]!.length)
                .replace(/^,\s*/, "")
            : data.property.address}
          {data.tenancy.endDate ? ` · lease ended ${calendarDate(data.tenancy.endDate)}` : ""}
        </p>
      </div>
      <dl className="tracks">
        <div className="track">
          <dt>Readiness</dt>
          <dd>
            <ol className="stepper" aria-label={`Readiness: ${data.handoff.physicalProgress}`}>
              {READINESS_STEPS.map((name, index) => (
                <li
                  key={name}
                  data-state={index < step ? "done" : index === step ? "current" : "todo"}
                  aria-current={index === step ? "step" : undefined}
                >
                  {STEP_NAMES[index]}
                </li>
              ))}
            </ol>
            <span className="step-note">{statusLabel(data.handoff.physicalProgress)}</span>
          </dd>
        </div>
        {today && (
          <div className="track">
            <dt>Today</dt>
            <dd className="today">
              {new Date(today).toLocaleDateString(undefined, {
                weekday: "short",
                month: "short",
                day: "numeric",
              })}
            </dd>
          </div>
        )}
      </dl>
    </div>
  );
}

/** Who is acting now, and on what. One line, above the plan and the work. */
function NowStrip({ data }: { data: HandoffWorkspace }) {
  const vendors = waitingOn(data);
  const visit = nextVisit(data);
  // Shown on the case clock, like every message and record on the page.
  const at = caseToday(data) ?? data.agent.updatedAt;
  const when = visit
    ? new Date(visit.at).toLocaleString(undefined, {
        weekday: "long",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      })
    : "";
  return (
    <div className="now-strip">
      <span className="now-label">Now</span>
      <span className="status" data-tone={visit ? "active" : tone(agentLabel(data.agent.status))}>
        {visit ? "Visits booked" : agentLabel(data.agent.status)}
      </span>
      <p className="now-text">
        {visit ? (
          `Next: ${visit.vendor}, ${visit.job.charAt(0).toLowerCase()}${visit.job.slice(1)}, ${when}.`
        ) : (
          <>
            {data.agent.nextStep}
            {vendors.length > 0 && !/^Waiting on /.test(data.agent.nextStep) && (
              <span className="faint"> Waiting on {vendors.join(", ")}.</span>
            )}
          </>
        )}
      </p>
      <div className="now-meta">
        <LiveState data={data} />
        <time className="faint" dateTime={at}>
          {shortTime(at)}
        </time>
      </div>
    </div>
  );
}

/**
 * Whether Handoff has a step due now, soon, or is waiting (GitHub Actions / Vercel live-status pattern). Edits save
 * only when a step ends, so "working" means a step is due, not that one is visibly mid-run.
 */
function LiveState({ data }: { data: HandoffWorkspace }) {
  const now = useNow(1000);
  const due = dueIn(data, now);
  const status = data.agent.status;
  const state =
    status === "Complete" || data.handoff.physicalProgress === "Ready"
      ? "done"
      : /decision|attention|unavailable/i.test(status)
        ? "you"
        : due !== null && due <= 3000
          ? "working"
          : due !== null && due < 10 * 60_000
            ? "scheduled"
            : "waiting";
  const text =
    state === "working"
      ? "Working on the next step"
      : state === "scheduled" && due !== null
        ? `Next step ${countdown(due)}`
        : state === "you"
          ? "Waiting on you"
          : state === "done"
            ? "Done"
            : "No step due";
  return (
    <span className="live" data-state={state}>
      <span className="live-dot" aria-hidden="true" />
      <span className="live-text">{text}</span>
    </span>
  );
}

/** Underline that slides to the selected tab (Linear, Stripe). */
function useTabInk(tab: string) {
  const list = useRef<HTMLDivElement>(null);
  const [ink, setInk] = useState<{ left: number; width: number }>();
  useLayoutEffect(() => {
    const measure = () => {
      const active = list.current?.querySelector<HTMLElement>('[aria-selected="true"]');
      if (active) {
        setInk({ left: active.offsetLeft, width: active.offsetWidth });
      }
    };
    measure();
    window.addEventListener("resize", measure);
    return () => window.removeEventListener("resize", measure);
  }, [tab]);
  return { list, ink };
}

/**
 * A banner about the operator's own change. A confirmation closes itself (useAutoDismiss); a problem stays until
 * closed. Only the unrecoverable-journal warning has no close, since it describes a state that stays true.
 */
function Notice({ text, ok, onClose }: { text: string; ok: boolean; onClose?: () => void }) {
  const hold = useAutoDismiss(ok && onClose ? text : undefined, () => onClose?.());
  return (
    <div className={`notice${ok ? " ok" : ""}`} role="status" {...hold}>
      <p>{text}</p>
      {onClose && (
        <button
          type="button"
          className="toast-close notice-close"
          aria-label="Dismiss"
          onClick={onClose}
        >
          ×
        </button>
      )}
    </div>
  );
}

const TABS = [
  ["overview", "Overview"],
  ["money", "Money"],
  ["messages", "Messages"],
  ["timeline", "Timeline"],
  ["calendar", "Calendar"],
  ["documents", "Documents"],
] as const;
type TabId = (typeof TABS)[number][0];
const DOCK_KEY = "handoff.dock";

export function HandoffCasePage({ handoffId }: { handoffId: string }) {
  const store = useHandoffStore();
  const read = useHandoffRead(store.workspace(handoffId));
  const [params, setParams] = useSearchParams();
  const tab: TabId = TABS.some(([id]) => id === params.get("tab"))
    ? (params.get("tab") as TabId)
    : "overview";
  const [document, setDocument] = useState<SourceDocument>();
  const [focus, setFocus] = useState(0);
  const [collapsed, setCollapsed] = useState(() => {
    try {
      return localStorage.getItem(DOCK_KEY) === "hidden";
    } catch {
      return false;
    }
  });
  const saved = read.data;
  const data = saved && read.failed ? { ...saved, documents: [] } : saved;
  // A background refresh keeps every control as it was; only a failed read (or no data yet) holds actions back.
  const stale = read.failed || !read.data;
  const visibleDocument =
    document &&
    !read.failed &&
    data?.documents.find((d) => documentKey(d) === documentKey(document));
  useEffect(() => {
    if (document && !visibleDocument) {
      setDocument(undefined);
    }
  }, [document, visibleDocument]);
  const updates = useUpdates(data, tab);
  const moneyIds = data ? moneyDocumentIds(data) : new Set<string>();
  const moneyDocument =
    visibleDocument && moneyIds.has(visibleDocument.id) ? visibleDocument : undefined;
  const recordDocument = visibleDocument && !moneyDocument ? visibleDocument : undefined;
  const tabs = useTabInk(data ? tab : "");
  const notice = store.notice(handoffId);
  const pending = store.pending(handoffId);
  const go = (next: TabId) =>
    setParams(
      (prev) => {
        const p = new URLSearchParams(prev);
        if (next === "overview") {
          p.delete("tab");
        } else {
          p.set("tab", next);
        }
        return p;
      },
      { replace: false },
    );
  const toggleDock = () =>
    setCollapsed((c) => {
      try {
        localStorage.setItem(DOCK_KEY, c ? "shown" : "hidden");
      } catch {
        /* Remembering the dock is optional. */
      }
      return !c;
    });
  const ask = () => {
    if (collapsed) {
      toggleDock();
    }
    setFocus((n) => n + 1);
  };
  // Quotes and invoices open over the Money tab; every other document opens in Documents.
  const readDocument = (doc: SourceDocument) => {
    setDocument(doc);
    go(data && moneyDocumentIds(data).has(doc.id) ? "money" : "documents");
  };
  const count = (id: TabId) =>
    !data
      ? 0
      : id === "messages"
        ? inbox(data).length
        : id === "documents"
          ? data.documents.filter((d) => d.sourceKind !== "Original" && !moneyIds.has(d.id)).length
          : 0;
  return (
    <>
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link to="/">Units</Link>
        <span>/</span>
        <span>{data?.property.name ?? "Unit"}</span>
      </nav>
      {read.failed && (
        <ReadNotice
          failureKind={read.failureKind}
          hasData={Boolean(data)}
          onRetry={() => void read.refresh()}
        />
      )}
      {!data && read.loading && (
        <div className="loading skeleton" role="status">
          <span className="sr-only">Loading…</span>
          <span className="sk sk-title" aria-hidden="true" />
          <span className="sk sk-line" aria-hidden="true" />
          <span className="sk sk-card" aria-hidden="true" />
          <span className="sk sk-card" aria-hidden="true" />
        </div>
      )}
      {data && (
        <>
          <UnitHeader data={data} />
          <div className="unit-tabs" role="tablist" aria-label="Unit" ref={tabs.list}>
            {TABS.map(([id, label]) => (
              <button
                key={id}
                type="button"
                role="tab"
                aria-selected={tab === id}
                onClick={() => go(id)}
              >
                {label}
                {count(id) > 0 && <span className="tab-count">{count(id)}</span>}
                {id !== "overview" && updates.unseen[id] && (
                  <span className="tab-dot" aria-label="New" />
                )}
              </button>
            ))}
            {tabs.ink && (
              <span
                className="tab-ink"
                aria-hidden="true"
                style={{ width: tabs.ink.width, transform: `translateX(${tabs.ink.left}px)` }}
              />
            )}
          </div>
          <UpdateToast
            toast={updates.toast}
            onView={(next) => {
              updates.dismiss();
              go(next);
            }}
            onDismiss={updates.dismiss}
          />
          {notice && (
            <Notice
              text={notice}
              ok={/saved|received/i.test(notice)}
              onClose={store.blocked() ? undefined : () => store.dismissNotice(handoffId)}
            />
          )}
          {pending && !store.isSending(handoffId) && (
            <div className="notice" role="status">
              <p>Checking your change</p>
              <button type="button" className="btn" onClick={() => void store.replay(handoffId)}>
                Check again
              </button>
            </div>
          )}
          <div className={`unit-body${collapsed ? " dock-hidden" : ""}`}>
            <div
              className="tab-panel"
              role="tabpanel"
              aria-label={TABS.find(([id]) => id === tab)![1]}
            >
              {tab === "overview" && (
                <div className="main-col">
                  {needsDecision(data) ? (
                    <DecisionSheet
                      data={data}
                      stale={stale}
                      readDocument={readDocument}
                      onAsk={ask}
                    />
                  ) : (
                    <NowStrip data={data} />
                  )}
                  <AcceptedPlan data={data} readDocument={readDocument} />
                  <WorkSection data={data} readDocument={readDocument} />
                  <FundsLine data={data} onOpen={() => go("money")} />
                </div>
              )}
              {tab === "money" && (
                <MoneyTab data={data} readDocument={readDocument} openId={moneyDocument?.id} />
              )}
              {tab === "messages" && <MessagesTab data={data} readDocument={readDocument} />}
              {tab === "timeline" && <TimelineTab data={data} />}
              {tab === "calendar" && (
                <div className="section calendar-card">
                  <CalendarView events={calendarEvents(data)} workspaces={[data]} />
                </div>
              )}
              {tab === "documents" && (
                <DocumentsTab
                  data={data}
                  selectedId={recordDocument ? recordDocument.id : undefined}
                  readDocument={readDocument}
                  viewer={
                    recordDocument ? (
                      <DocumentViewer
                        key={documentKey(recordDocument)}
                        document={recordDocument}
                        documents={data.documents}
                        data={data}
                        gateway={store.gateway}
                        onClose={() => setDocument(undefined)}
                      />
                    ) : null
                  }
                />
              )}
            </div>
            {tab === "money" && moneyDocument && (
              <MoneyDrawer onClose={() => setDocument(undefined)}>
                <DocumentViewer
                  key={documentKey(moneyDocument)}
                  document={moneyDocument}
                  documents={data.documents}
                  data={data}
                  gateway={store.gateway}
                  onClose={() => setDocument(undefined)}
                />
              </MoneyDrawer>
            )}
            <ChatDock
              data={data}
              stale={stale}
              focus={focus}
              collapsed={collapsed}
              onToggle={toggleDock}
            />
          </div>
        </>
      )}
    </>
  );
}

export function HandoffCaseRoute() {
  const { handoffId } = useParams();
  return handoffId && handoffId.length <= 512 ? (
    <HandoffCasePage key={handoffId} handoffId={handoffId} />
  ) : (
    <HandoffNotFound />
  );
}
