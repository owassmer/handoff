import type { Queryable } from "../db.js";

/**
 * Hidden settings that make an imitated system misbehave the way real ones do. The agent never
 * sees them; a staged demo or a test sets them.
 */
export async function setScenario(q: Queryable, system: string, name: string, config: Record<string, unknown>): Promise<void> {
  await q.query(
    `insert into sim.scenarios (system, name, config) values ($1, $2, $3)
     on conflict (system, name) do update set config = excluded.config`,
    [system, name, config],
  );
}

/** Takes one use of a scenario that applies a set number of times, if any uses remain. */
export async function useScenario(q: Queryable, system: string, name: string): Promise<Record<string, unknown> | null> {
  const [row] = await q.query<{ config: Record<string, unknown> }>(
    `update sim.scenarios set config = jsonb_set(config, '{remaining}', to_jsonb((config->>'remaining')::int - 1))
     where system = $1 and name = $2 and (config->>'remaining')::int > 0 returning config`,
    [system, name],
  );
  return row?.config ?? null;
}
