import { spawn } from "node:child_process";
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import type { JWTVerifyGetKey } from "jose";
import { CALLBACK_HOST, CALLBACK_PATH, DEFAULT_CALLBACK_PORT, OPENAI_AUTH } from "./config.js";
import {
  type Fetch, authorizationUrl, callbackUri, exchangeCode, grantedScopes, newAttempt, planEnabled, readCallback, redactedUrl,
  revokeRefreshToken, verifyIdToken,
} from "./oauth.js";
import { type CredentialRecord, CredentialStore, writeAtomic } from "./store.js";
import { withTokens } from "./tokens.js";

export interface LoginOptions {
  store: CredentialStore;
  /** A saved registration to sign in to again; omit to register a new one. */
  label?: string;
  port?: number;
  /** Ask again for permission to use the ChatGPT plan, e.g. after it was declined. */
  enablePlan?: boolean;
  fetch?: Fetch;
  jwks?: JWTVerifyGetKey;
  openBrowser?: (url: string) => Promise<void> | void;
  log?: (line: string) => void;
  timeoutMs?: number;
  now?: () => Date;
}

export interface LoginResult {
  record: CredentialRecord;
  newRegistration: boolean;
  planEnabled: boolean;
}

/**
 * Sign in with ChatGPT from this machine. The loopback callback reaches only the computer running the
 * browser, so run this where the browser is; a remote host imports the result (see exportAccount).
 */
export async function login(o: LoginOptions): Promise<LoginResult> {
  const log = o.log ?? ((l: string) => console.log(l));
  const host = await o.store.hostIdentity();
  const existing = o.label ? await o.store.read(o.label) : null;
  if (o.label && !existing) throw new Error(`no saved account ${o.label}`);

  const attempt = newAttempt();
  const listener = await listen(o.port ?? DEFAULT_CALLBACK_PORT);
  const redirectUri = callbackUri(listener.port);
  const url = authorizationUrl({
    clientId: existing?.client_id ?? null,
    hostId: host.ext_agent_host_id,
    redirectUri,
    attempt,
    idTokenHint: existing?.id_token,
    loginHint: existing?.email,
    requestConsent: o.enablePlan,
  });

  try {
    const arrival = listener.next(o.timeoutMs ?? 300_000);
    log("Continue with ChatGPT in your browser to connect Handoff.");
    try {
      await (o.openBrowser ?? openSystemBrowser)(url);
    } catch {
      // The hint is left out of a URL shown on screen; signing in still works without it.
      log(`Open this address in your browser:\n${existing?.id_token ? redactedUrl(url).replace(/&id_token_hint=[^&]*/, "") : url}`);
    }
    const { url: returned, respond } = await arrival;
    try {
      const cb = readCallback(returned, { attempt, clientId: existing?.client_id ?? null });
      const tokens = await exchangeCode(o.fetch ?? fetch, { clientId: cb.clientId, code: cb.code, verifier: attempt.verifier, redirectUri });
      if (!tokens.id_token) throw new Error("the token response carried no ID token");
      const identity = await verifyIdToken(tokens.id_token, { clientId: cb.clientId, nonce: attempt.nonce }, o.jwks);
      if (existing && identity.subject !== existing.subject) {
        throw new Error("the browser signed in to a different ChatGPT account than the one selected; nothing was replaced");
      }
      const now = o.now?.() ?? new Date();
      const base: CredentialRecord = existing ?? {
        label: labelFor(identity.email, cb.clientId),
        email: identity.email,
        issuer: OPENAI_AUTH.issuer,
        subject: identity.subject,
        client_id: cb.clientId,
        ext_agent_host_id: host.ext_agent_host_id,
        id_token: null, access_token: null, refresh_token: null, token_type: "Bearer", expires_in: null,
        scopes: [], saved_at: now.toISOString(), expires_at: null, earliest_refresh_at: null,
      };
      const record = withTokens(
        { ...base, email: identity.email ?? base.email, ext_agent_host_id: host.ext_agent_host_id, scopes: grantedScopes(tokens.scope ?? cb.scope) },
        { ...tokens, scope: tokens.scope ?? cb.scope ?? undefined },
        now,
      );
      await o.store.withLock(record.label, () => o.store.write(record));
      if (!existing || !(await o.store.active())) await o.store.setActive(record.label);
      const enabled = planEnabled(record.scopes);
      respond(200, enabled ? "Handoff is connected to your ChatGPT plan. You can close this tab." : "Signed in, but permission to use your ChatGPT plan was not granted. You can close this tab.");
      return { record, newRegistration: !existing, planEnabled: enabled };
    } catch (e) {
      respond(400, `Sign-in did not complete: ${e instanceof Error ? e.message : String(e)}`);
      throw e;
    }
  } finally {
    await listener.close();
  }
}

/** A stable, distinct local label for a registration: the email's local part and the end of the client id. */
export function labelFor(email: string | null, clientId: string): string {
  const who = (email?.split("@")[0] ?? "account").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40) || "account";
  return `${who}-${clientId.toLowerCase().replace(/[^a-z0-9]/g, "").slice(-6)}`;
}

interface Listener {
  port: number;
  next(timeoutMs: number): Promise<{ url: URL; respond: (status: number, text: string) => void }>;
  close(): Promise<void>;
}

/** The loopback listener, started before the browser opens. Falls back to any free port if the preferred one is busy. */
async function listen(preferred: number): Promise<Listener> {
  let pending: ((v: { url: URL; respond: (status: number, text: string) => void }) => void) | null = null;
  const server = createServer((req: IncomingMessage, res: ServerResponse) => {
    const url = new URL(req.url ?? "/", `http://${CALLBACK_HOST}`);
    if (req.method !== "GET" || url.pathname !== CALLBACK_PATH || !pending) {
      res.writeHead(404).end();
      return;
    }
    const deliver = pending;
    pending = null;
    deliver({
      url,
      respond: (status, text) => {
        res.writeHead(status, { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" });
        res.end(`<!doctype html><meta charset="utf-8"><title>Handoff</title><p style="font:16px system-ui;margin:3em">${escapeHtml(text)}</p>`);
      },
    });
  });
  const bind = (port: number) => new Promise<number>((resolve, reject) => {
    server.once("error", reject);
    server.listen(port, CALLBACK_HOST, () => {
      server.off("error", reject);
      resolve((server.address() as { port: number }).port);
    });
  });
  let port: number;
  try {
    port = await bind(preferred);
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code !== "EADDRINUSE") throw e;
    port = await bind(0);
  }
  return {
    port,
    next: (timeoutMs) => new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        pending = null;
        reject(new Error("timed out waiting for the browser to return"));
      }, timeoutMs);
      pending = (v) => {
        clearTimeout(timer);
        resolve(v);
      };
    }),
    close: () => new Promise((resolve) => server.close(() => resolve())),
  };
}

function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!);
}

function openSystemBrowser(url: string): Promise<void> {
  const [cmd, args] = process.platform === "darwin" ? ["open", [url]] : process.platform === "win32" ? ["cmd", ["/c", "start", "", url]] : ["xdg-open", [url]];
  return new Promise((resolve, reject) => {
    const child = spawn(cmd as string, args as string[], { stdio: "ignore", detached: true });
    child.once("error", reject);
    child.once("spawn", () => {
      child.unref();
      resolve();
    });
  });
}

// ---- Moving a session to a self-hosted VM, and signing out ---------------------------------------

/** Writes one registration's protected record for transfer over a secure channel such as SSH. */
export async function exportAccount(store: CredentialStore, label: string, path: string): Promise<void> {
  const r = await store.read(label);
  if (!r) throw new Error(`no saved account ${label}`);
  await writeAtomic(path, r);
}

/** Imports a transferred record. This host keeps its own host id; the copied one is noted, not used. */
export async function importAccount(store: CredentialStore, record: CredentialRecord): Promise<CredentialRecord> {
  const host = await store.hostIdentity();
  const existing = await store.read(record.label);
  if (existing && (existing.subject !== record.subject || existing.client_id !== record.client_id)) {
    throw new Error(`a different registration is already saved as ${record.label}; nothing was replaced`);
  }
  const imported: CredentialRecord = {
    ...record,
    ext_agent_host_id: host.ext_agent_host_id,
    imported_from_host: record.ext_agent_host_id !== host.ext_agent_host_id ? record.ext_agent_host_id : record.imported_from_host,
  };
  await store.withLock(imported.label, () => store.write(imported));
  if (!(await store.active())) await store.setActive(imported.label);
  return imported;
}

/**
 * Signs out: revokes the renewable session, then clears the tokens. The registration's client id and
 * this host's id are kept for a later sign-in. Returns whether revocation was confirmed.
 */
export async function logout(store: CredentialStore, label: string, f: Fetch = fetch): Promise<{ revoked: boolean }> {
  return store.withLock(label, async () => {
    const r = await store.read(label);
    if (!r) throw new Error(`no saved account ${label}`);
    let revoked = !r.refresh_token;
    for (let i = 0; r.refresh_token && i < 3 && !revoked; i++) {
      try {
        await revokeRefreshToken(f, { clientId: r.client_id, refreshToken: r.refresh_token });
        revoked = true;
      } catch {
        await new Promise((res) => setTimeout(res, 250 * 2 ** i));
      }
    }
    await store.write({ ...r, access_token: null, refresh_token: null, id_token: null, expires_at: null, earliest_refresh_at: null });
    return { revoked };
  });
}
