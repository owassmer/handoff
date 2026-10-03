import type { Queryable } from "./db.js";

export type EventSource = "operator" | "tenant" | "counterparty" | "outside_system" | "clock" | "handoff";

/** Tenants and counterparties can inform a case but never authorize anything in it. */
export const TRUSTED_SOURCES: ReadonlySet<EventSource> = new Set(["operator", "outside_system", "clock", "handoff"]);

export interface CaseEvent {
  id: number;
  caseId: string;
  kind: string;
  source: EventSource;
  trusted: boolean;
  payload: Record<string, unknown>;
  occurredAt: Date;
  recordedAt: Date;
  processedAt: Date | null;
}

interface EventRow {
  id: string | number;
  case_id: string;
  kind: string;
  source: EventSource;
  trusted: boolean;
  payload: Record<string, unknown>;
  occurred_at: Date;
  recorded_at: Date;
  processed_at: Date | null;
}

const columns = `id, case_id, kind, source, trusted, payload, occurred_at, recorded_at, processed_at`;

function toEvent(r: EventRow): CaseEvent {
  return {
    id: Number(r.id),
    caseId: r.case_id,
    kind: r.kind,
    source: r.source,
    trusted: r.trusted,
    payload: r.payload,
    occurredAt: new Date(r.occurred_at),
    recordedAt: new Date(r.recorded_at),
    processedAt: r.processed_at ? new Date(r.processed_at) : null,
  };
}

export interface NewEvent {
  caseId: string;
  kind: string;
  source: EventSource;
  payload: Record<string, unknown>;
  occurredAt: Date;
  /** False for a record that should not wake the case, such as Handoff noting its own work. Default true. */
  wakes?: boolean;
}

export async function appendEvent(q: Queryable, e: NewEvent): Promise<CaseEvent> {
  const [row] = await q.query<EventRow>(
    `insert into events (case_id, kind, source, trusted, payload, occurred_at, processed_at)
     values ($1, $2, $3, $4, $5, $6, case when $7 then null else now() end)
     returning ${columns}`,
    [e.caseId, e.kind, e.source, TRUSTED_SOURCES.has(e.source), e.payload, e.occurredAt, e.wakes ?? true],
  );
  return toEvent(row!);
}

export async function unprocessedEvents(q: Queryable, caseId: string): Promise<CaseEvent[]> {
  const rows = await q.query<EventRow>(
    `select ${columns} from events where case_id = $1 and processed_at is null order by id`,
    [caseId],
  );
  return rows.map(toEvent);
}

export async function caseEvents(q: Queryable, caseId: string): Promise<CaseEvent[]> {
  const rows = await q.query<EventRow>(`select ${columns} from events where case_id = $1 order by id`, [caseId]);
  return rows.map(toEvent);
}

export async function markProcessed(q: Queryable, ids: number[]): Promise<void> {
  if (ids.length === 0) return;
  await q.query(`update events set processed_at = now() where id = any($1::bigint[]) and processed_at is null`, [ids]);
}

export async function casesWithWork(q: Queryable): Promise<string[]> {
  const rows = await q.query<{ case_id: string }>(
    `select case_id from events where processed_at is null group by case_id order by min(id)`,
  );
  return rows.map((r) => r.case_id);
}
