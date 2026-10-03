import type { Queryable } from "./db.js";
import { newId } from "./ids.js";

// ---- Documents ---------------------------------------------------------------------------------

export type DocumentKind =
  | "lease" | "photo" | "video" | "invoice" | "receipt" | "quote" | "utility_bill"
  | "statement" | "notice" | "agreement" | "correspondence" | "other";

export interface NewDocument {
  caseId: string | null;
  kind: DocumentKind;
  title: string;
  mediaType: string;
  storageRef: string;
  sha256: string;
  source: "operator" | "tenant" | "counterparty" | "outside_system" | "handoff";
  capturedAt?: Date;
  receivedAt: Date;
  metadata?: Record<string, unknown>;
}

export async function addDocument(q: Queryable, d: NewDocument): Promise<string> {
  const id = newId("doc");
  await q.query(
    `insert into documents (id, case_id, kind, title, media_type, storage_ref, sha256, source, captured_at, received_at, metadata)
     values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)`,
    [id, d.caseId, d.kind, d.title, d.mediaType, d.storageRef, d.sha256, d.source, d.capturedAt ?? null, d.receivedAt, d.metadata ?? {}],
  );
  return id;
}

// ---- Inspections, conditions, observations, findings -------------------------------------------

export type InspectionKind = "move_in" | "pre_move_out" | "move_out" | "completion";

export async function addInspection(
  q: Queryable,
  i: { caseId: string; kind: InspectionKind; conductedAt: Date; conductedBy: string; tenantPresent?: boolean; notes?: string; photos?: Array<{ documentId: string; area?: string }> },
): Promise<string> {
  const id = newId("insp");
  await q.query(
    `insert into inspections (id, case_id, kind, conducted_at, conducted_by, tenant_present, notes) values ($1, $2, $3, $4, $5, $6, $7)`,
    [id, i.caseId, i.kind, i.conductedAt, i.conductedBy, i.tenantPresent ?? null, i.notes ?? ""],
  );
  for (const p of i.photos ?? []) {
    await q.query(`insert into inspection_documents (inspection_id, document_id, area) values ($1, $2, $3)`, [id, p.documentId, p.area ?? null]);
  }
  return id;
}

export async function addCondition(
  q: Queryable,
  c: { caseId: string; area: string; item: string; summary: string; identifiedAt: Date; identifiedIn?: string },
): Promise<string> {
  const id = newId("cond");
  await q.query(
    `insert into conditions (id, case_id, area, item, summary, identified_at, identified_in) values ($1, $2, $3, $4, $5, $6, $7)`,
    [id, c.caseId, c.area, c.item, c.summary, c.identifiedAt, c.identifiedIn ?? null],
  );
  return id;
}

export async function addObservation(
  q: Queryable,
  o: { conditionId: string; inspectionId?: string; observedBy: string; observedAt: Date; text: string; documentIds?: string[] },
): Promise<number> {
  const [r] = await q.query<{ id: string }>(
    `insert into observations (condition_id, inspection_id, observed_by, observed_at, text, document_ids) values ($1, $2, $3, $4, $5, $6) returning id`,
    [o.conditionId, o.inspectionId ?? null, o.observedBy, o.observedAt, o.text, o.documentIds ?? []],
  );
  return Number(r!.id);
}

export type Responsibility = "tenant_damage" | "ordinary_wear" | "present_at_move_in" | "undetermined";

export interface Finding {
  id: string;
  conditionId: string;
  responsibility: Responsibility;
  reasoning: string;
  basis: Record<string, unknown>;
  foundBy: string;
  foundAt: Date;
  supersedes: string | null;
}

/** Records a finding. Any earlier finding on the condition is superseded by this one, not erased. */
export async function addFinding(
  q: Queryable,
  f: { conditionId: string; responsibility: Responsibility; reasoning: string; basis?: Record<string, unknown>; foundBy: string; foundAt: Date },
): Promise<Finding> {
  const prior = await currentFinding(q, f.conditionId);
  const id = newId("find");
  await q.query(
    `insert into findings (id, condition_id, responsibility, reasoning, basis, found_by, found_at, supersedes) values ($1, $2, $3, $4, $5, $6, $7, $8)`,
    [id, f.conditionId, f.responsibility, f.reasoning, f.basis ?? {}, f.foundBy, f.foundAt, prior?.id ?? null],
  );
  return { id, conditionId: f.conditionId, responsibility: f.responsibility, reasoning: f.reasoning, basis: f.basis ?? {}, foundBy: f.foundBy, foundAt: f.foundAt, supersedes: prior?.id ?? null };
}

/** The finding nothing has superseded. */
export async function currentFinding(q: Queryable, conditionId: string): Promise<Finding | null> {
  const [r] = await q.query<{ id: string; condition_id: string; responsibility: Responsibility; reasoning: string; basis: Record<string, unknown>; found_by: string; found_at: Date; supersedes: string | null }>(
    `select f.* from findings f where f.condition_id = $1 and not exists (select 1 from findings g where g.supersedes = f.id)`,
    [conditionId],
  );
  return r ? { id: r.id, conditionId: r.condition_id, responsibility: r.responsibility, reasoning: r.reasoning, basis: r.basis, foundBy: r.found_by, foundAt: new Date(r.found_at), supersedes: r.supersedes } : null;
}

// ---- Work --------------------------------------------------------------------------------------

export type WorkStatus = "planned" | "ordered" | "scheduled" | "in_progress" | "completed" | "cancelled";

export interface WorkItem {
  id: string;
  caseId: string;
  performer: "in_house" | "vendor";
  vendorPartyId: string | null;
  description: string;
  externalRef: string | null;
  status: WorkStatus;
  scheduledFor: Date | null;
  completedAt: Date | null;
  hours: number | null;
  hourlyRateCents: number | null;
  materialsCents: number | null;
  estimateCents: number | null;
  finalCostCents: number | null;
  quoteDocumentId: string | null;
  invoiceDocumentId: string | null;
  conditionIds: string[];
}

export async function addWorkItem(
  q: Queryable,
  w: { caseId: string; performer: "in_house" | "vendor"; vendorPartyId?: string; description: string; conditionIds: string[]; estimateCents?: number },
): Promise<string> {
  const id = newId("work");
  await q.query(
    `insert into work_items (id, case_id, performer, vendor_party_id, description, status, estimate_cents) values ($1, $2, $3, $4, $5, 'planned', $6)`,
    [id, w.caseId, w.performer, w.vendorPartyId ?? null, w.description, w.estimateCents ?? null],
  );
  for (const c of w.conditionIds) await q.query(`insert into work_item_conditions (work_item_id, condition_id) values ($1, $2)`, [id, c]);
  return id;
}

/** Applies what the system doing the work reports. Only the fields given change. */
export async function updateWorkItem(
  q: Queryable,
  id: string,
  u: Partial<Pick<WorkItem, "externalRef" | "status" | "scheduledFor" | "completedAt" | "hours" | "hourlyRateCents" | "materialsCents" | "estimateCents" | "finalCostCents" | "quoteDocumentId" | "invoiceDocumentId">>,
): Promise<void> {
  const columns: Record<string, string> = {
    externalRef: "external_ref", status: "status", scheduledFor: "scheduled_for", completedAt: "completed_at", hours: "hours",
    hourlyRateCents: "hourly_rate_cents", materialsCents: "materials_cents", estimateCents: "estimate_cents",
    finalCostCents: "final_cost_cents", quoteDocumentId: "quote_document_id", invoiceDocumentId: "invoice_document_id",
  };
  const sets: string[] = [];
  const values: unknown[] = [id];
  for (const [k, v] of Object.entries(u)) {
    if (v === undefined) continue;
    const column = columns[k];
    if (!column) throw new Error(`work item has no field ${k}`);
    values.push(v);
    sets.push(`${column} = $${values.length}`);
  }
  if (sets.length === 0) return;
  const rows = await q.query(`update work_items set ${sets.join(", ")} where id = $1 returning id`, values);
  if (rows.length === 0) throw new Error(`no work item ${id}`);
}

export async function caseWorkItems(q: Queryable, caseId: string): Promise<WorkItem[]> {
  const rows = await q.query<Record<string, unknown>>(
    `select w.*, coalesce(array_agg(c.condition_id order by c.condition_id) filter (where c.condition_id is not null), '{}') as condition_ids
     from work_items w left join work_item_conditions c on c.work_item_id = w.id
     where w.case_id = $1 group by w.id order by w.id`,
    [caseId],
  );
  const num = (v: unknown) => (v === null || v === undefined ? null : Number(v));
  const date = (v: unknown) => (v ? new Date(v as string) : null);
  return rows.map((r) => ({
    id: r.id as string,
    caseId: r.case_id as string,
    performer: r.performer as WorkItem["performer"],
    vendorPartyId: r.vendor_party_id as string | null,
    description: r.description as string,
    externalRef: r.external_ref as string | null,
    status: r.status as WorkStatus,
    scheduledFor: date(r.scheduled_for),
    completedAt: date(r.completed_at),
    hours: num(r.hours),
    hourlyRateCents: num(r.hourly_rate_cents),
    materialsCents: num(r.materials_cents),
    estimateCents: num(r.estimate_cents),
    finalCostCents: num(r.final_cost_cents),
    quoteDocumentId: r.quote_document_id as string | null,
    invoiceDocumentId: r.invoice_document_id as string | null,
    conditionIds: r.condition_ids as string[],
  }));
}

// ---- Account -----------------------------------------------------------------------------------

export type EntryKind = "deposit_held" | "rent_due" | "charge" | "credit" | "payment_received" | "refund_paid" | "write_off" | "reversal";

export interface AccountEntry {
  id: number;
  caseId: string;
  kind: EntryKind;
  lineKey: string | null;
  description: string;
  amountCents: number;
  effectiveOn: string;
  conditionId: string | null;
  workItemId: string | null;
  rule: string | null;
  documentIds: string[];
  decisionId: string | null;
  source: "ledger" | "handoff";
  ledgerRef: string | null;
  reverses: number | null;
}

/** Which way each kind moves the balance. Positive means the tenant owes more. */
const SIGN: Record<Exclude<EntryKind, "reversal">, 1 | -1> = {
  deposit_held: -1, rent_due: 1, charge: 1, credit: -1, payment_received: -1, refund_paid: 1, write_off: -1,
};

export interface NewEntry {
  caseId: string;
  kind: Exclude<EntryKind, "reversal">;
  lineKey?: string;
  description: string;
  /** Always positive; the kind decides the direction. */
  amountCents: number;
  effectiveOn: string;
  conditionId?: string;
  workItemId?: string;
  rule?: string;
  documentIds?: string[];
  decisionId?: string;
  source: "ledger" | "handoff";
  ledgerRef?: string;
  recordedAt: Date;
}

export async function addEntry(q: Queryable, e: NewEntry): Promise<number> {
  if (!Number.isSafeInteger(e.amountCents) || e.amountCents <= 0) throw new Error(`entry amount must be a positive whole number of cents, got ${e.amountCents}`);
  const [r] = await q.query<{ id: string }>(
    `insert into account_entries (case_id, kind, line_key, description, amount_cents, effective_on, condition_id, work_item_id, rule,
       document_ids, decision_id, source, ledger_ref, recorded_at)
     values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14) returning id`,
    [e.caseId, e.kind, e.lineKey ?? null, e.description, SIGN[e.kind] * e.amountCents, e.effectiveOn, e.conditionId ?? null, e.workItemId ?? null,
     e.rule ?? null, e.documentIds ?? [], e.decisionId ?? null, e.source, e.ledgerRef ?? null, e.recordedAt],
  );
  return Number(r!.id);
}

/** Cancels an entry with an equal and opposite one. An entry can be reversed once. */
export async function reverseEntry(
  q: Queryable,
  entryId: number,
  r: { description: string; effectiveOn: string; decisionId?: string; source: "ledger" | "handoff"; ledgerRef?: string; recordedAt: Date },
): Promise<number> {
  const [orig] = await q.query<{ case_id: string; kind: EntryKind; line_key: string | null; amount_cents: string }>(
    `select case_id, kind, line_key, amount_cents from account_entries where id = $1`,
    [entryId],
  );
  if (!orig) throw new Error(`no entry ${entryId}`);
  if (orig.kind === "reversal") throw new Error("a reversal cannot itself be reversed; post a new entry instead");
  const [row] = await q.query<{ id: string }>(
    `insert into account_entries (case_id, kind, line_key, description, amount_cents, effective_on, decision_id, source, ledger_ref, reverses, recorded_at)
     values ($1, 'reversal', $2, $3, $4, $5, $6, $7, $8, $9, $10) returning id`,
    [orig.case_id, orig.line_key, r.description, -Number(orig.amount_cents), r.effectiveOn, r.decisionId ?? null, r.source, r.ledgerRef ?? null, entryId, r.recordedAt],
  );
  return Number(row!.id);
}

export async function accountEntries(q: Queryable, caseId: string): Promise<AccountEntry[]> {
  const rows = await q.query<Record<string, unknown>>(`select * from account_entries where case_id = $1 order by id`, [caseId]);
  return rows.map((r) => ({
    id: Number(r.id),
    caseId: r.case_id as string,
    kind: r.kind as EntryKind,
    lineKey: r.line_key as string | null,
    description: r.description as string,
    amountCents: Number(r.amount_cents),
    effectiveOn: typeof r.effective_on === "string" ? r.effective_on : (r.effective_on as Date).toISOString().slice(0, 10),
    conditionId: r.condition_id as string | null,
    workItemId: r.work_item_id as string | null,
    rule: r.rule as string | null,
    documentIds: r.document_ids as string[],
    decisionId: r.decision_id as string | null,
    source: r.source as AccountEntry["source"],
    ledgerRef: r.ledger_ref as string | null,
    reverses: r.reverses === null ? null : Number(r.reverses),
  }));
}

/** Above zero the tenant owes; below zero the operator owes the tenant. */
export async function accountBalance(q: Queryable, caseId: string): Promise<number> {
  const [r] = await q.query<{ balance: string }>(`select coalesce(sum(amount_cents), 0) as balance from account_entries where case_id = $1`, [caseId]);
  return Number(r!.balance);
}
