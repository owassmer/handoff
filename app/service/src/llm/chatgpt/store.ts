import { randomUUID } from "node:crypto";
import { constants } from "node:fs";
import { access, chmod, mkdir, open, readFile, readdir, rename, stat, unlink } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { type JWK, calculateJwkThumbprintUri, exportJWK, generateKeyPair } from "jose";

/** This machine's identity as an agent host. Opaque; not a credential and not proof of identity. */
export interface HostIdentity {
  ext_agent_host_id: string;
  created_at: string;
  public_jwk: JWK;
  private_jwk: JWK;
}

/**
 * One registration: an issued client id bound to one ChatGPT account and workspace, with its tokens.
 * The fields follow OpenAI's example credential record, plus derived expiry times.
 */
export interface CredentialRecord {
  label: string;
  email: string | null;
  issuer: string;
  subject: string;
  client_id: string;
  ext_agent_host_id: string;
  id_token: string | null;
  access_token: string | null;
  refresh_token: string | null;
  token_type: string;
  expires_in: number | null;
  scopes: string[];
  saved_at: string;
  /** saved_at plus expires_in. */
  expires_at: string | null;
  earliest_refresh_at: string | null;
  /** Set when the record was copied from another host; this host keeps its own id. */
  imported_from_host?: string;
}

export class CredentialLocationError extends Error {}

/**
 * Credentials on disk, outside any repository: `HANDOFF_CHATGPT_HOME`, or ~/.config/handoff/chatgpt.
 * Directories are owner-only (0700), files owner-only (0600), and every write is atomic.
 */
export class CredentialStore {
  private readonly inProcess = new Map<string, Promise<unknown>>();

  constructor(readonly dir: string) {}

  static fromEnvironment(env: NodeJS.ProcessEnv = process.env): CredentialStore {
    return new CredentialStore(resolve(env.HANDOFF_CHATGPT_HOME ?? join(homedir(), ".config", "handoff", "chatgpt")));
  }

  private get accountsDir(): string {
    return join(this.dir, "accounts");
  }

  async ensure(): Promise<void> {
    await assertOutsideRepository(this.dir);
    await mkdir(this.accountsDir, { recursive: true, mode: 0o700 });
    await chmod(this.dir, 0o700);
    await chmod(this.accountsDir, 0o700);
  }

  /** This host's id, created once before its first sign-in and reused for every later one. */
  async hostIdentity(): Promise<HostIdentity> {
    await this.ensure();
    const path = join(this.dir, "host.json");
    const existing = await readJson<HostIdentity>(path);
    if (existing) return existing;
    const { publicKey, privateKey } = await generateKeyPair("EdDSA", { crv: "Ed25519", extractable: true });
    const public_jwk = await exportJWK(publicKey);
    const identity: HostIdentity = {
      ext_agent_host_id: await calculateJwkThumbprintUri(public_jwk, "sha256"),
      created_at: new Date().toISOString(),
      public_jwk,
      private_jwk: await exportJWK(privateKey),
    };
    // Exclusive create: if another process made one first, use theirs.
    try {
      await writeAtomic(path, identity, { exclusive: true });
      return identity;
    } catch (e) {
      if ((e as NodeJS.ErrnoException).code !== "EEXIST") throw e;
      return (await readJson<HostIdentity>(path))!;
    }
  }

  private accountPath(label: string): string {
    if (!/^[a-z0-9][a-z0-9._-]{0,80}$/.test(label)) throw new Error(`invalid account label ${label}`);
    return join(this.accountsDir, `${label}.json`);
  }

  async read(label: string): Promise<CredentialRecord | null> {
    return readJson<CredentialRecord>(this.accountPath(label));
  }

  async write(record: CredentialRecord): Promise<void> {
    await this.ensure();
    await writeAtomic(this.accountPath(record.label), record);
  }

  async list(): Promise<CredentialRecord[]> {
    await this.ensure();
    const names = (await readdir(this.accountsDir)).filter((n) => n.endsWith(".json")).sort();
    const out: CredentialRecord[] = [];
    for (const n of names) {
      const r = await readJson<CredentialRecord>(join(this.accountsDir, n));
      if (r) out.push(r);
    }
    return out;
  }

  async active(): Promise<string | null> {
    return (await readJson<{ label: string }>(join(this.dir, "active.json")))?.label ?? null;
  }

  async setActive(label: string): Promise<void> {
    await this.ensure();
    await writeAtomic(join(this.dir, "active.json"), { label });
  }

  /**
   * Runs `work` while holding this account's lock, so two processes never race a rotating refresh token.
   * Within one process calls queue; across processes a lock file is created exclusively.
   */
  async withLock<T>(label: string, work: () => Promise<T>, o: { timeoutMs?: number; staleMs?: number } = {}): Promise<T> {
    const prior = this.inProcess.get(label) ?? Promise.resolve();
    const run = prior.catch(() => undefined).then(() => this.withFileLock(label, work, o));
    this.inProcess.set(label, run);
    try {
      return await run;
    } finally {
      if (this.inProcess.get(label) === run) this.inProcess.delete(label);
    }
  }

  private async withFileLock<T>(label: string, work: () => Promise<T>, o: { timeoutMs?: number; staleMs?: number }): Promise<T> {
    await this.ensure();
    const lock = `${this.accountPath(label)}.lock`;
    const deadline = Date.now() + (o.timeoutMs ?? 60_000);
    const staleMs = o.staleMs ?? 45_000;
    for (;;) {
      try {
        const fh = await open(lock, "wx", 0o600);
        await fh.writeFile(JSON.stringify({ pid: process.pid, at: Date.now() }));
        await fh.close();
        break;
      } catch (e) {
        if ((e as NodeJS.ErrnoException).code !== "EEXIST") throw e;
        const held = await stat(lock).catch(() => null);
        if (held && Date.now() - held.mtimeMs > staleMs) {
          await unlink(lock).catch(() => undefined);
          continue;
        }
        if (Date.now() > deadline) throw new Error(`timed out waiting for the credential lock for ${label}`);
        await new Promise((r) => setTimeout(r, 25 + Math.random() * 75));
      }
    }
    try {
      return await work();
    } finally {
      await unlink(lock).catch(() => undefined);
    }
  }
}

/** Refuses a credential location inside a git working tree, so credentials can never be committed. */
export async function assertOutsideRepository(dir: string): Promise<void> {
  let current = resolve(dir);
  for (;;) {
    if (await exists(join(current, ".git"))) throw new CredentialLocationError(`refusing to keep credentials inside the repository at ${current}`);
    const parent = dirname(current);
    if (parent === current) return;
    current = parent;
  }
}

async function exists(path: string): Promise<boolean> {
  return access(path, constants.F_OK).then(() => true, () => false);
}

async function readJson<T>(path: string): Promise<T | null> {
  try {
    return JSON.parse(await readFile(path, "utf8")) as T;
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === "ENOENT") return null;
    throw e;
  }
}

/** Writes a temporary owner-only file, flushes it, then renames it over the target. */
export async function writeAtomic(path: string, value: unknown, o: { exclusive?: boolean } = {}): Promise<void> {
  const tmp = `${path}.${randomUUID()}.tmp`;
  const fh = await open(tmp, "wx", 0o600);
  try {
    await fh.writeFile(`${JSON.stringify(value, null, 2)}\n`);
    await fh.sync();
  } finally {
    await fh.close();
  }
  if (o.exclusive && (await exists(path))) {
    await unlink(tmp);
    const err = new Error(`${path} already exists`) as NodeJS.ErrnoException;
    err.code = "EEXIST";
    throw err;
  }
  await rename(tmp, path);
}
