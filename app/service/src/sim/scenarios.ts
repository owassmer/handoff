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

/** A standing setting for how an imitated system behaves, e.g. how long a vendor takes to quote. */
export async function readScenario<T = Record<string, unknown>>(q: Queryable, system: string, name: string): Promise<T | null> {
  const [row] = await q.query<{ config: T }>(`select config from sim.scenarios where system = $1 and name = $2`, [system, name]);
  return row?.config ?? null;
}

/**
 * The faults a test or staged demo can inject into one call: a timeout before the system acts,
 * or a timeout after it acted. Call `before()` first and `after()` once the effect is recorded.
 */
export async function faultFor(q: Queryable, system: string, call: string): Promise<{ before(): void; after(): void; config: Record<string, unknown> | null }> {
  const config = await useScenario(q, system, call);
  return {
    config,
    before() {
      if (config?.mode === "timeout-before-send") throw new Error(`${system} did not respond`);
    },
    after() {
      if (config?.mode === "timeout-after-send") throw new Error(`${system} did not respond`);
    },
  };
}
