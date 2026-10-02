import type React from "react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import type { HandoffWorkspace } from "./contracts";
import { shortTime } from "./format";
import { useHandoffRead, useHandoffStore } from "./hooks";
import { type CalendarEvent, calendarEvents, caseToday, dayKey, eventDays } from "./model";

// US week, as Google Calendar and Outlook show it to US accounts: Sunday first, weekend at both edges.
const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const clock = (value: string) =>
  new Date(value).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
/** Google Calendar's compact time: "9am", "1:30pm". */
const compact = (value: string) => {
  const d = new Date(value);
  const h = d.getHours() % 12 || 12;
  const m = d.getMinutes();
  return `${h}${m ? `:${String(m).padStart(2, "0")}` : ""}${d.getHours() < 12 ? "am" : "pm"}`;
};
const when = (event: CalendarEvent) => {
  if (!event.end) {
    return shortTime(event.start);
  }
  return dayKey(event.start) === dayKey(event.end)
    ? `${shortTime(event.start)} – ${clock(event.end)}`
    : `${shortTime(event.start)} – ${shortTime(event.end)}`;
};
const sundayOf = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate() - d.getDay());

/** Days the bar still runs in this week row, from the given cell; its label may use that width. */
function cellsLeft(event: CalendarEvent, cell: Date): number {
  const days = eventDays(event);
  const from = days.indexOf(dayKey(cell));
  const toSaturday = 7 - cell.getDay();
  return Math.max(1, Math.min(days.length - from, toSaturday));
}

/** Where a multi-day event's bar sits on a given day, so consecutive days read as one bar. */
function spanOf(event: CalendarEvent, key: string): "single" | "start" | "middle" | "end" {
  const days = eventDays(event);
  if (days.length < 2) {
    return "single";
  }
  if (key === days[0]) {
    return "start";
  }
  return key === days[days.length - 1] ? "end" : "middle";
}

function EventSheet({
  event,
  workspaces,
  onClose,
}: {
  event: CalendarEvent;
  workspaces: HandoffWorkspace[];
  onClose(): void;
}) {
  const data = workspaces.find((w) => w.handoff.id === event.handoffId);
  const job = data?.jobs.find((j) => j.id === event.jobId);
  const access = data?.documents.find((d) => d.kind === "Access arrangements");
  const emails = data?.messages
    .filter(
      (m) =>
        job && m.jobId === job.id && (m.direction === "Outgoing" || m.direction === "Incoming"),
    )
    .sort((a, b) => a.createdAt.localeCompare(b.createdAt));
  return (
    <aside className="event-sheet" aria-label={event.title}>
      <div className="event-head">
        <div>
          <span className="pill" data-kind={event.kind}>
            {event.kind}
          </span>
          <h3>{event.title}</h3>
          <p className="muted">{when(event)}</p>
          <p className="faint">{event.unit}</p>
        </div>
        <button type="button" className="btn quiet" onClick={onClose}>
          Close
        </button>
      </div>
      <dl className="facts">
        <dt>Status</dt>
        <dd>{event.detail}</dd>
        {job && data && (
          <>
            <dt>Work</dt>
            <dd>
              <ul className="plain">
                {job.scope.map((line) => (
                  <li key={line.lineId}>{line.description}</li>
                ))}
              </ul>
            </dd>
          </>
        )}
        {job && access && (
          <>
            <dt>Access</dt>
            <dd className="muted">{access.text}</dd>
          </>
        )}
      </dl>
      {emails && emails.length > 0 && (
        <>
          <div className="subhead">Scheduling emails</div>
          {emails.map((m) => (
            <article
              className={`email compact${m.direction === "Incoming" ? " in" : ""}`}
              key={m.id}
            >
              <header>
                <strong>{m.title}</strong>
                <time dateTime={m.createdAt}>{shortTime(m.createdAt)}</time>
              </header>
              <div className="email-body">{m.body}</div>
            </article>
          ))}
        </>
      )}
      <Link className="btn" to={`/handoffs/${encodeURIComponent(event.handoffId)}?tab=messages`}>
        Open unit messages
      </Link>
    </aside>
  );
}

/** Month or week grid on the case's own clock. Multi-day work is one bar across its working days. */
export function CalendarView({
  events,
  workspaces,
  showUnit = false,
}: {
  events: CalendarEvent[];
  workspaces: HandoffWorkspace[];
  showUnit?: boolean;
}) {
  const today = workspaces
    .map(caseToday)
    .filter((v): v is string => Boolean(v))
    .sort()
    .pop();
  const anchor = new Date(today ?? events[0]?.start ?? Date.now());
  const [view, setView] = useState<"Month" | "Week">("Month");
  const [cursor, setCursor] = useState(anchor);
  const [selected, setSelected] = useState<CalendarEvent>();
  const byDay = new Map<string, CalendarEvent[]>();
  events.forEach((e) => eventDays(e).forEach((d) => byDay.set(d, [...(byDay.get(d) ?? []), e])));
  const todayKey = today ? dayKey(today) : "";
  const monthStart = new Date(cursor.getFullYear(), cursor.getMonth(), 1);
  const first = sundayOf(view === "Month" ? monthStart : cursor);
  const monthDays = new Date(cursor.getFullYear(), cursor.getMonth() + 1, 0).getDate();
  const weeks = Math.ceil((monthStart.getDay() + monthDays) / 7);
  const kinds = new Set(events.map((e) => e.kind));
  const cells = Array.from(
    { length: view === "Month" ? weeks * 7 : 7 },
    (_, i) => new Date(first.getFullYear(), first.getMonth(), first.getDate() + i),
  );
  const step = (n: number) =>
    setCursor(
      view === "Month"
        ? new Date(cursor.getFullYear(), cursor.getMonth() + n, 1)
        : new Date(cursor.getFullYear(), cursor.getMonth(), cursor.getDate() + 7 * n),
    );
  const title =
    view === "Month"
      ? monthStart.toLocaleDateString(undefined, { month: "long", year: "numeric" })
      : `Week of ${first.toLocaleDateString(undefined, { month: "long", day: "numeric", year: "numeric" })}`;
  return (
    <div className={`calendar${selected ? " with-sheet" : ""}`}>
      <div className="calendar-main">
        <div className="calendar-bar">
          <div className="calendar-nav">
            <button type="button" className="btn" onClick={() => setCursor(anchor)}>
              Today
            </button>
            <button
              type="button"
              className="btn quiet"
              aria-label="Previous"
              onClick={() => step(-1)}
            >
              ‹
            </button>
            <button type="button" className="btn quiet" aria-label="Next" onClick={() => step(1)}>
              ›
            </button>
            <h2>{title}</h2>
          </div>
          <div className="segmented" role="group" aria-label="Calendar view">
            {(["Month", "Week"] as const).map((v) => (
              <button type="button" key={v} aria-pressed={view === v} onClick={() => setView(v)}>
                {v}
              </button>
            ))}
          </div>
        </div>
        <div className="legend" aria-hidden="true">
          {(["Visit", "Invoice due", "Offer expires", "Lease end"] as const)
            .filter((k) => kinds.has(k))
            .map((k) => (
              <span data-kind={k} key={k}>
                {k === "Visit" ? "Visit or work" : k}
              </span>
            ))}
        </div>
        <div className={view === "Month" ? "month" : "month week"} role="grid" aria-label={title}>
          {WEEKDAYS.map((d) => (
            <div className="month-head" key={d} role="columnheader">
              {d}
            </div>
          ))}
          {cells.map((cell) => {
            const key = dayKey(cell);
            return (
              <div
                className="month-cell"
                key={key}
                role="gridcell"
                data-out={view === "Month" && cell.getMonth() !== monthStart.getMonth()}
                data-today={key === todayKey}
                data-weekend={cell.getDay() === 0 || cell.getDay() === 6}
              >
                <span className="month-date">
                  {view === "Week"
                    ? cell.toLocaleDateString(undefined, { day: "numeric", month: "short" })
                    : cell.getDate()}
                </span>
                {(byDay.get(key) ?? []).map((e) => {
                  const span = spanOf(e, key);
                  // Like Google Calendar, a bar is labelled where it starts and again at each new week row.
                  const labelled =
                    span === "single" || span === "start" || view === "Week" || cell.getDay() === 0;
                  return (
                    <button
                      type="button"
                      className="month-item"
                      data-kind={e.kind}
                      data-span={span}
                      data-selected={selected?.id === e.id ? "true" : undefined}
                      data-labelled={labelled && span !== "single" ? "true" : undefined}
                      style={
                        labelled && span !== "single"
                          ? ({ "--cells": cellsLeft(e, cell) } as React.CSSProperties)
                          : undefined
                      }
                      key={e.id}
                      title={e.title}
                      aria-label={e.title}
                      onClick={() => setSelected(e)}
                    >
                      {e.kind === "Visit" && labelled && span === "single" && (
                        <span className="item-time">{compact(e.start)}</span>
                      )}
                      {labelled ? (
                        <span className="item-label">
                          {showUnit ? `${e.title} · ${e.unit}` : e.title}
                        </span>
                      ) : (
                        " "
                      )}
                    </button>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>
      {selected && (
        <EventSheet
          event={selected}
          workspaces={workspaces}
          onClose={() => setSelected(undefined)}
        />
      )}
    </div>
  );
}

function UnitEvents({
  id,
  onData,
}: {
  id: string;
  onData(id: string, data: HandoffWorkspace): void;
}) {
  const store = useHandoffStore();
  const read = useHandoffRead(store.workspace(id));
  useEffect(() => {
    if (read.data) {
      onData(id, read.data);
    }
  }, [id, read.data, onData]);
  return null;
}

/** Calendar across every unit in the workspace. */
export function CalendarPage() {
  const store = useHandoffStore();
  const list = useHandoffRead(store.list);
  const [loaded, setLoaded] = useState<Record<string, HandoffWorkspace>>({});
  const [onData] = useState(
    () => (id: string, data: HandoffWorkspace) =>
      setLoaded((prev) => (prev[id] === data ? prev : { ...prev, [id]: data })),
  );
  const units = list.data?.handoffs ?? [];
  const workspaces = units
    .map((u) => loaded[u.id])
    .filter((w): w is HandoffWorkspace => Boolean(w));
  return (
    <>
      <div className="list-head">
        <div>
          <h1>Calendar</h1>
          <p>Visits, due dates and offers across your units</p>
        </div>
      </div>
      {units.map((u) => (
        <UnitEvents key={u.id} id={u.id} onData={onData} />
      ))}
      {!list.data && list.loading && (
        <div className="loading" role="status">
          Loading…
        </div>
      )}
      {list.data && (
        <div className="section calendar-card">
          <CalendarView
            events={workspaces.flatMap(calendarEvents)}
            workspaces={workspaces}
            showUnit
          />
        </div>
      )}
    </>
  );
}
