-- Imitations of the remaining outside systems: the property-management ledger, the utility billing
-- agent, the in-house maintenance system, vendors and the collector. Each keeps its own records the
-- way the real system would, and acts later through sim.timers on the business clock.

-- The ledger, the books of record. Positive amounts are charged to the resident, negative ones credited.
create table sim.ledger_transactions (
  ref text primary key,
  -- The order entries were posted, as the ledger lists them.
  seq bigint generated always as identity,
  idempotency_key text unique,
  tenancy_ref text not null,
  posted_on date not null,
  code text not null,
  description text not null,
  amount_cents bigint not null,
  posted_at timestamptz not null
);
create index ledger_tenancy on sim.ledger_transactions (tenancy_ref, posted_on, seq);

create table sim.utility_requests (
  ref text primary key,
  idempotency_key text not null unique,
  case_id text,
  tenancy_ref text not null,
  move_out_on date not null,
  requested_at timestamptz not null
);

create table sim.utility_bills (
  ref text primary key,
  case_id text,
  tenancy_ref text not null,
  utility text not null check (utility in ('water', 'sewer', 'trash', 'gas', 'electric')),
  period_start date not null,
  period_end date not null,
  amount_cents bigint not null check (amount_cents >= 0),
  read_type text not null check (read_type in ('actual', 'previous_month', 'estimated')),
  issued_on date not null
);

create table sim.work_orders (
  ref text primary key,
  idempotency_key text not null unique,
  case_id text,
  unit_ref text not null,
  category text not null,
  description text not null,
  status text not null check (status in ('open', 'scheduled', 'in_progress', 'completed', 'cancelled')),
  scheduled_for timestamptz,
  completed_at timestamptz,
  technician text,
  hours numeric(6, 2),
  hourly_rate_cents bigint,
  materials_cents bigint,
  created_at timestamptz not null
);

-- Quote requests and orders sent to vendors, as the vendor holds them.
create table sim.vendor_requests (
  ref text primary key,
  idempotency_key text not null unique,
  case_id text,
  vendor_party_id text not null,
  kind text not null check (kind in ('quote', 'order')),
  scope text not null,
  not_to_exceed_cents bigint,
  status text not null check (status in ('received', 'quoted', 'in_progress', 'completed', 'invoiced')),
  created_at timestamptz not null
);

create table sim.collector_placements (
  ref text primary key,
  idempotency_key text not null unique,
  case_id text,
  debtor_party_id text not null,
  creditor text not null,
  placed_at timestamptz not null
);

create table sim.collector_components (
  placement_ref text not null references sim.collector_placements,
  component_id text not null,
  description text not null,
  amount_cents bigint not null check (amount_cents >= 0),
  consumer_credit boolean not null,
  primary key (placement_ref, component_id)
);

-- Corrections sent to the collector. Until one is applied, the collector still carries the old amount.
create table sim.collector_adjustments (
  ref text primary key,
  idempotency_key text not null unique,
  placement_ref text not null references sim.collector_placements,
  component_id text not null,
  amount_cents bigint not null check (amount_cents >= 0),
  reason text not null,
  received_at timestamptz not null,
  applied_at timestamptz
);
