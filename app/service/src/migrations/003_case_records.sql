-- The records a move-out builds: documents, inspections, conditions and what was seen of them,
-- who is responsible, the work that fixes them, and the account in exact cents.

create function refuse_change() returns trigger language plpgsql as $$
begin
  raise exception '% are kept as recorded', tg_table_name;
end $$;

-- Photos, invoices, quotes, bills, notices, agreements. The bytes live in storage; the record fixes their hash.
create table documents (
  id text primary key,
  case_id text references cases,
  kind text not null check (kind in ('lease', 'photo', 'video', 'invoice', 'receipt', 'quote', 'utility_bill',
                                     'statement', 'notice', 'agreement', 'correspondence', 'other')),
  title text not null,
  media_type text not null,
  storage_ref text not null,
  sha256 text not null,
  source text not null check (source in ('operator', 'tenant', 'counterparty', 'outside_system', 'handoff')),
  -- When a photo was taken, as distinct from when Handoff received it. The law cares about the first.
  captured_at timestamptz,
  received_at timestamptz not null,
  metadata jsonb not null default '{}'
);
create index documents_case on documents (case_id, kind);
create trigger documents_kept before update or delete on documents for each row execute function refuse_change();

create table inspections (
  id text primary key,
  case_id text not null references cases,
  kind text not null check (kind in ('move_in', 'pre_move_out', 'move_out', 'completion')),
  conducted_at timestamptz not null,
  conducted_by text not null,
  tenant_present boolean,
  notes text not null default ''
);
create index inspections_case on inspections (case_id, kind);

create table inspection_documents (
  inspection_id text not null references inspections,
  document_id text not null references documents,
  area text,
  primary key (inspection_id, document_id)
);

-- Something in the unit that may need work or lead to a charge, e.g. the bedroom 2 closet door.
create table conditions (
  id text primary key,
  case_id text not null references cases,
  area text not null,
  item text not null,
  summary text not null,
  identified_at timestamptz not null,
  identified_in text references inspections
);
create index conditions_case on conditions (case_id);

-- What someone saw, in neutral terms: what is visible, where, how extensive. Not a legal conclusion.
create table observations (
  id bigint generated always as identity primary key,
  condition_id text not null references conditions,
  inspection_id text references inspections,
  observed_by text not null,
  observed_at timestamptz not null,
  text text not null,
  document_ids text[] not null default '{}'
);
create trigger observations_kept before update or delete on observations for each row execute function refuse_change();

-- Who is responsible for a condition. A later finding supersedes an earlier one; none are erased.
create table findings (
  id text primary key,
  condition_id text not null references conditions,
  responsibility text not null check (responsibility in ('tenant_damage', 'ordinary_wear', 'present_at_move_in', 'undetermined')),
  reasoning text not null,
  -- The observations, documents and tree results the finding rests on.
  basis jsonb not null default '{}',
  found_by text not null,
  found_at timestamptz not null,
  supersedes text references findings
);
create index findings_condition on findings (condition_id, found_at);
create trigger findings_kept before update or delete on findings for each row execute function refuse_change();

-- Work that fixes one or more conditions: an in-house work order or a vendor job. Its state mirrors
-- the system that does the work; the events that changed it are in the case inbox.
create table work_items (
  id text primary key,
  case_id text not null references cases,
  performer text not null check (performer in ('in_house', 'vendor')),
  vendor_party_id text references parties,
  description text not null,
  external_ref text,
  status text not null check (status in ('planned', 'ordered', 'scheduled', 'in_progress', 'completed', 'cancelled')),
  scheduled_for timestamptz,
  completed_at timestamptz,
  hours numeric(6, 2),
  hourly_rate_cents bigint,
  materials_cents bigint,
  estimate_cents bigint,
  final_cost_cents bigint,
  quote_document_id text references documents,
  invoice_document_id text references documents,
  check ((performer = 'vendor') = (vendor_party_id is not null))
);
create index work_items_case on work_items (case_id, status);

create table work_item_conditions (
  work_item_id text not null references work_items,
  condition_id text not null references conditions,
  primary key (work_item_id, condition_id)
);

-- The working account for the tenancy. Every entry is exact cents and never edited; a correction
-- reverses an earlier entry. Positive amounts are owed by the tenant, negative ones are owed to the
-- tenant, so the sum is the balance: above zero the tenant owes, below zero a refund is due.
create table account_entries (
  id bigint generated always as identity primary key,
  case_id text not null references cases,
  kind text not null check (kind in ('deposit_held', 'rent_due', 'charge', 'credit', 'payment_received',
                                     'refund_paid', 'write_off', 'reversal')),
  -- A stable name for a statement line, e.g. 'closet-repair', so corrections can find it.
  line_key text,
  description text not null,
  amount_cents bigint not null,
  effective_on date not null,
  condition_id text references conditions,
  work_item_id text references work_items,
  -- The tree and effect the line rests on, e.g. 'CA.deduct-repair#may-deduct'.
  rule text,
  document_ids text[] not null default '{}',
  decision_id text references decisions,
  -- Entries read from the ledger mirror it; entries Handoff makes are posted to it.
  source text not null check (source in ('ledger', 'handoff')),
  ledger_ref text,
  reverses bigint references account_entries,
  recorded_at timestamptz not null,
  check ((kind = 'reversal') = (reverses is not null))
);
create index account_entries_case on account_entries (case_id, id);
create unique index account_entries_reversed_once on account_entries (reverses) where reverses is not null;
create trigger account_entries_kept before update or delete on account_entries for each row execute function refuse_change();
