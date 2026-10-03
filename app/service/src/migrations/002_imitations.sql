-- Imitated outside systems for simulated worlds. They live in their own schema so that a world copy
-- carries them with the records, and so production roles and agent tools can be denied access.

create schema sim;

-- Hidden scenario settings per system, e.g. a payment that times out after it has gone through.
create table sim.scenarios (
  system text not null,
  name text not null,
  config jsonb not null,
  primary key (system, name)
);

-- Things an imitated system will do later on the business clock (a payment settling, a vendor replying).
create table sim.timers (
  id bigint generated always as identity primary key,
  system text not null,
  kind text not null,
  due_at timestamptz not null,
  payload jsonb not null,
  fired_at timestamptz
);
create index timers_pending on sim.timers (due_at) where fired_at is null;

-- Messages that left Handoff, as the recipient's mailbox would see them.
create table sim.outbox (
  id text primary key,
  idempotency_key text not null unique,
  case_id text,
  to_party_id text not null,
  to_address text not null,
  subject text not null,
  body text not null,
  attachments jsonb not null default '[]',
  sent_at timestamptz not null
);

-- Payments as the bank or payment processor holds them.
create table sim.payments (
  id text primary key,
  idempotency_key text not null unique,
  case_id text,
  payee_party_id text not null,
  amount_cents bigint not null check (amount_cents > 0),
  method text not null,
  memo text not null,
  status text not null check (status in ('submitted', 'settled', 'returned')),
  submitted_at timestamptz not null,
  settled_at timestamptz
);
