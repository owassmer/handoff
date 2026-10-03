-- Handoff case runtime: core records.
-- Money is integer cents. Times are business time unless named recorded_at.

-- One row. In a simulated world the business clock is set here; in production it follows real time.
create table clock (
  only_row boolean primary key default true check (only_row),
  mode text not null check (mode in ('real', 'simulated')),
  now timestamptz not null
);

-- People who use Handoff. Permissions, not job titles.
create table users (
  id text primary key,
  name text not null,
  email text not null unique,
  permissions text[] not null check (permissions <@ array['view', 'work', 'decide', 'configure'])
);

create table parties (
  id text primary key,
  kind text not null check (kind in ('person', 'organization')),
  name text not null,
  email text,
  phone text
);

create table properties (
  id text primary key,
  name text not null,
  address text not null,
  -- Legal layers that apply, e.g. {US, CA, CA-OC, CA-HB}. Chosen from the legal place, not the postal city.
  legal_layers text[] not null
);

create table units (
  id text primary key,
  property_id text not null references properties,
  label text not null,
  bedrooms integer,
  bathrooms numeric(3, 1),
  square_feet integer
);

create table tenancies (
  id text primary key,
  unit_id text not null references units,
  starts_on date not null,
  ends_on date,
  rent_cents bigint not null check (rent_cents >= 0),
  deposit_cents bigint not null check (deposit_cents >= 0)
);

-- Real business relationships, not application roles.
create table tenancy_parties (
  tenancy_id text not null references tenancies,
  party_id text not null references parties,
  relationship text not null check (relationship in ('tenant', 'owner', 'manager')),
  primary key (tenancy_id, party_id, relationship)
);

-- One move-out. The unit and the account finish independently.
create table cases (
  id text primary key,
  tenancy_id text not null references tenancies,
  opened_at timestamptz not null,
  unit_outcome text not null default 'open' check (unit_outcome in ('open', 'ready')),
  account_outcome text not null default 'open' check (account_outcome in ('open', 'resolved')),
  -- A case handles its events one at a time. A run holds a lease while it works.
  run_lease_owner text,
  run_lease_until timestamptz
);

-- Everything that happens to a case arrives here. Append-only: only processed_at may be set, once.
create table events (
  id bigint generated always as identity primary key,
  case_id text not null references cases,
  kind text not null,
  source text not null check (source in ('operator', 'tenant', 'counterparty', 'outside_system', 'clock', 'handoff')),
  -- Tenant and counterparty content is untrusted: it can inform, never authorize.
  trusted boolean not null,
  payload jsonb not null,
  occurred_at timestamptz not null,
  recorded_at timestamptz not null default now(),
  processed_at timestamptz,
  check (trusted = (source in ('operator', 'outside_system', 'clock', 'handoff')))
);
create index events_unprocessed on events (case_id, id) where processed_at is null;

create function events_append_only() returns trigger language plpgsql as $$
begin
  if tg_op = 'DELETE' then
    raise exception 'events are append-only';
  end if;
  if old.processed_at is not null
     or new.case_id <> old.case_id or new.kind <> old.kind or new.source <> old.source
     or new.trusted <> old.trusted or new.payload <> old.payload or new.occurred_at <> old.occurred_at
     or new.recorded_at <> old.recorded_at then
    raise exception 'events are append-only';
  end if;
  return new;
end $$;
create trigger events_append_only before update or delete on events
  for each row execute function events_append_only();

-- Deadlines and scheduled wake-ups, on the business clock.
create table wakeups (
  id bigint generated always as identity primary key,
  case_id text not null references cases,
  due_at timestamptz not null,
  reason text not null,
  payload jsonb not null default '{}',
  -- Optional caller key, so rescheduling the same deadline doesn't duplicate it.
  key text,
  fired_at timestamptz,
  cancelled_at timestamptz,
  unique (case_id, key)
);
create index wakeups_pending on wakeups (due_at) where fired_at is null and cancelled_at is null;

-- What Handoff proposes and the operator decides. Content is fixed once proposed;
-- acceptance binds to the exact content hash the operator reviewed.
create table decisions (
  id text primary key,
  case_id text references cases, -- null for company-wide standing instructions
  kind text not null,
  content jsonb not null,
  content_hash text not null,
  status text not null check (status in ('proposed', 'accepted', 'declined', 'superseded')),
  proposed_by text not null,
  proposed_at timestamptz not null,
  decided_by text references users,
  decided_at timestamptz,
  note text,
  supersedes text references decisions
);
create index decisions_case on decisions (case_id, kind, status);

create function decisions_fixed_content() returns trigger language plpgsql as $$
begin
  if tg_op = 'DELETE' then
    raise exception 'decisions are kept';
  end if;
  if new.content <> old.content or new.content_hash <> old.content_hash or new.kind <> old.kind
     or new.case_id is distinct from old.case_id or new.proposed_at <> old.proposed_at then
    raise exception 'decision content cannot change; propose a new decision';
  end if;
  -- Once decided, the only change allowed is an accepted decision being superseded by a later accepted one.
  if old.status <> 'proposed' and (
       not (new.status = old.status or (old.status = 'accepted' and new.status = 'superseded'))
       or new.decided_by is distinct from old.decided_by or new.decided_at is distinct from old.decided_at
       or new.note is distinct from old.note) then
    raise exception 'a decided decision cannot change';
  end if;
  return new;
end $$;
create trigger decisions_fixed_content before update or delete on decisions
  for each row execute function decisions_fixed_content();

-- One wake of a case: the events it was given and how it ended.
create table runs (
  id text primary key,
  case_id text not null references cases,
  owner text not null,
  event_ids bigint[] not null,
  business_time timestamptz not null,
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  status text not null check (status in ('running', 'completed', 'failed')),
  error text
);
create index runs_case on runs (case_id, started_at);

-- Every action that changes the world goes through the gateway and is recorded here, including refusals.
-- The idempotency key makes a repeated request return the first outcome instead of acting twice.
-- A refusal does not hold the key, so the same action can go through once it is authorized.
create table actions (
  id bigint generated always as identity primary key,
  case_id text references cases,
  kind text not null,
  idempotency_key text not null,
  requested_by text not null,
  authority_decision_id text references decisions,
  authority_basis text,
  request jsonb not null,
  status text not null check (status in ('refused', 'pending', 'succeeded', 'failed', 'uncertain')),
  reason text,
  result jsonb,
  attempts integer not null default 0,
  requested_at timestamptz not null,
  completed_at timestamptz
);
create unique index actions_key on actions (idempotency_key) where status <> 'refused';
create index actions_case on actions (case_id, kind);

create function actions_outcome_once() returns trigger language plpgsql as $$
begin
  if tg_op = 'DELETE' then
    raise exception 'actions are kept';
  end if;
  if new.request <> old.request or new.kind <> old.kind or new.idempotency_key <> old.idempotency_key
     or new.case_id is distinct from old.case_id or new.authority_decision_id is distinct from old.authority_decision_id then
    raise exception 'an action request cannot change';
  end if;
  -- Pending and uncertain actions may still settle; the rest are final.
  if old.status in ('refused', 'succeeded', 'failed') and (new.status <> old.status or new.result is distinct from old.result) then
    raise exception 'action outcome is final';
  end if;
  return new;
end $$;
create trigger actions_outcome_once before update or delete on actions
  for each row execute function actions_outcome_once();
