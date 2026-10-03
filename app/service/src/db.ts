import { PGlite } from "@electric-sql/pglite";
import { readFile, readdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

/** The queries the runtime needs. Production Postgres and in-process PGlite both satisfy it. */
export interface Queryable {
  query<T>(sql: string, params?: unknown[]): Promise<T[]>;
}

export interface Db extends Queryable {
  /** Several statements at once, no parameters. Used for schema migrations. */
  exec(sql: string): Promise<void>;
  transaction<T>(work: (tx: Queryable) => Promise<T>): Promise<T>;
  close(): Promise<void>;
}

export class PgliteDb implements Db {
  constructor(private readonly pg: PGlite) {}

  async query<T>(sql: string, params: unknown[] = []): Promise<T[]> {
    return (await this.pg.query<T>(sql, params)).rows;
  }

  async exec(sql: string): Promise<void> {
    await this.pg.exec(sql);
  }

  transaction<T>(work: (tx: Queryable) => Promise<T>): Promise<T> {
    return this.pg.transaction((tx) =>
      work({ query: async <R>(sql: string, params: unknown[] = []) => (await tx.query<R>(sql, params)).rows }),
    );
  }

  close(): Promise<void> {
    return this.pg.close();
  }

  /** The whole world as one archive: records, imitated systems and clock together. */
  dump(): Promise<Blob | File> {
    return this.pg.dumpDataDir("gzip");
  }
}

const migrationsDir = join(dirname(fileURLToPath(import.meta.url)), "migrations");

export async function migrate(db: Db): Promise<void> {
  await db.query(`create table if not exists schema_migrations (name text primary key, applied_at timestamptz not null default now())`);
  const applied = new Set((await db.query<{ name: string }>(`select name from schema_migrations`)).map((r) => r.name));
  for (const name of (await readdir(migrationsDir)).filter((f) => f.endsWith(".sql")).sort()) {
    if (applied.has(name)) continue;
    if (!/^[\w.-]+$/.test(name)) throw new Error(`unexpected migration name ${name}`);
    // Each file applies whole or not at all.
    try {
      await db.exec(`begin;\n${await readFile(join(migrationsDir, name), "utf8")}\ninsert into schema_migrations (name) values ('${name}');\ncommit;`);
    } catch (e) {
      await db.exec("rollback;");
      throw e;
    }
  }
}

/** An in-process database: a whole simulated world, or a test. */
export async function openMemoryDb(): Promise<PgliteDb> {
  const db = new PgliteDb(await PGlite.create());
  await migrate(db);
  return db;
}

/** Reopen a saved world as an independent copy. */
export async function openDbFromDump(dump: Blob | File): Promise<PgliteDb> {
  return new PgliteDb(await PGlite.create({ loadDataDir: dump }));
}
