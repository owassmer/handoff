-- What the agent saw and did in each wake: the brief it was given, its reasoning messages and its tool calls.
-- Kept so an operator can always see why Handoff did something.
create table run_messages (
  run_id text not null references runs,
  seq integer not null,
  role text not null check (role in ('system', 'user', 'assistant', 'tool')),
  content jsonb not null,
  primary key (run_id, seq)
);
create trigger run_messages_kept before update or delete on run_messages for each row execute function refuse_change();
