import { type Fetch, OAuthError, type TokenResponse, grantedScopes, planEnabled, refreshGrant } from "./oauth.js";
import { type CredentialRecord, CredentialStore } from "./store.js";

/** No usable authorization: no saved account, or no token supplied by the environment. */
export class NotAuthorized extends Error {}
/** Signed in, but without permission to use the ChatGPT plan. Inference must not proceed. */
export class PlanNotEnabled extends Error {}
/** The refresh token can no longer be used. The user must sign in again with the saved client id. */
export class ReauthorizationRequired extends Error {}
/** The token endpoint could not be reached or failed; credentials are kept for a later try. */
export class TransientAuthError extends Error {}
/** The client registration itself was rejected. */
export class ClientConfigError extends Error {}

/** Where a request's authorization comes from. */
export interface TokenSource {
  readonly kind: "stored" | "environment" | "injected";
  /** The Authorization header value, or null when the environment's credential proxy adds it. */
  authorization(): Promise<string | null>;
  /** After a 401, obtains a different token if this source can. False if it cannot renew. */
  renew(failedAuthorization: string | null): Promise<boolean>;
  describe(): string;
}

/** The durable, renewable flow: credentials saved by the login helper, refreshed near expiry under a lock. */
export class StoredCredentials implements TokenSource {
  readonly kind = "stored";

  constructor(
    private readonly store: CredentialStore,
    private readonly o: { label?: string; fetch?: Fetch; refreshSkewMs?: number; now?: () => number } = {},
  ) {}

  describe(): string {
    return `saved ChatGPT account ${this.o.label ?? "(active)"} in ${this.store.dir}`;
  }

  async authorization(): Promise<string | null> {
    return `Bearer ${await this.accessToken({ force: false })}`;
  }

  async renew(failedAuthorization: string | null): Promise<boolean> {
    const failed = failedAuthorization?.replace(/^Bearer /, "") ?? null;
    const token = await this.accessToken({ force: true, failed });
    return token !== failed;
  }

  private now(): number {
    return this.o.now?.() ?? Date.now();
  }

  private async label(): Promise<string> {
    const label = this.o.label ?? (await this.store.active());
    if (!label) throw new NotAuthorized("no ChatGPT account is signed in on this host; run `npm run chatgpt -- login`");
    return label;
  }

  private usable(r: CredentialRecord): boolean {
    if (!r.access_token || !r.expires_at) return false;
    return Date.parse(r.expires_at) - this.now() > (this.o.refreshSkewMs ?? 120_000);
  }

  private async accessToken(p: { force: boolean; failed?: string | null }): Promise<string> {
    const label = await this.label();
    const first = await this.store.read(label);
    if (!first) throw new NotAuthorized(`no saved ChatGPT account ${label}`);
    if (!planEnabled(first.scopes)) throw new PlanNotEnabled(`account ${label} is signed in without permission to use the ChatGPT plan`);
    if (!p.force && this.usable(first)) return first.access_token!;

    return this.store.withLock(label, async () => {
      // Another process may have refreshed while we waited for the lock.
      const r = await this.store.read(label);
      if (!r) throw new NotAuthorized(`no saved ChatGPT account ${label}`);
      if (this.usable(r) && (!p.force || r.access_token !== p.failed)) return r.access_token!;
      const notYet = r.earliest_refresh_at && Date.parse(r.earliest_refresh_at) > this.now();
      if (!p.force && notYet && r.access_token && r.expires_at && Date.parse(r.expires_at) > this.now()) return r.access_token;
      if (!r.refresh_token) throw new ReauthorizationRequired(`account ${label} has no renewable session; sign in again`);

      let t: TokenResponse;
      try {
        t = await refreshGrant(this.o.fetch ?? fetch, { clientId: r.client_id, refreshToken: r.refresh_token });
      } catch (e) {
        if (e instanceof OAuthError && e.unusableRefresh) {
          await this.store.write({ ...r, access_token: null, refresh_token: null, expires_at: null, earliest_refresh_at: null, saved_at: new Date(this.now()).toISOString() });
          throw new ReauthorizationRequired(`the session for ${label} ended (${e.code}); sign in again`);
        }
        if (e instanceof OAuthError && e.code === "invalid_client") throw new ClientConfigError(`the client registration for ${label} was rejected`);
        if (e instanceof OAuthError && e.transient) throw new TransientAuthError(e.message);
        throw e;
      }
      const next = withTokens(r, t, new Date(this.now()));
      await this.store.write(next);
      if (!planEnabled(next.scopes)) throw new PlanNotEnabled(`account ${label} no longer has permission to use the ChatGPT plan`);
      return next.access_token!;
    });
  }
}

/** A record with a token response applied: access token, rotating refresh token, expiry and scopes replaced together. */
export function withTokens(r: CredentialRecord, t: TokenResponse, savedAt: Date): CredentialRecord {
  return {
    ...r,
    access_token: t.access_token,
    refresh_token: t.refresh_token ?? r.refresh_token,
    id_token: t.id_token ?? r.id_token,
    token_type: t.token_type,
    expires_in: t.expires_in,
    scopes: t.scope ? grantedScopes(t.scope) : r.scopes,
    saved_at: savedAt.toISOString(),
    expires_at: new Date(savedAt.getTime() + t.expires_in * 1000).toISOString(),
    earliest_refresh_at: normalizeTime(t.earliest_refresh_at),
  };
}

function normalizeTime(v: number | string | undefined): string | null {
  if (v === undefined || v === null) return null;
  if (typeof v === "number") return new Date(v > 1e12 ? v : v * 1000).toISOString();
  const parsed = Date.parse(v);
  return Number.isNaN(parsed) ? null : new Date(parsed).toISOString();
}

/** An access token placed in the environment's settings. It cannot be renewed here; it lasts about an hour. */
export class EnvironmentToken implements TokenSource {
  readonly kind = "environment";

  constructor(private readonly variable = "HANDOFF_CHATGPT_ACCESS_TOKEN", private readonly env: NodeJS.ProcessEnv = process.env) {}

  describe(): string {
    return `access token from the environment variable ${this.variable}`;
  }

  async authorization(): Promise<string | null> {
    const token = this.env[this.variable];
    if (!token) throw new NotAuthorized(`${this.variable} is not set; add it in the environment's settings`);
    return `Bearer ${token}`;
  }

  async renew(): Promise<boolean> {
    return false;
  }
}

/** The environment's protected credential proxy adds the Authorization header; no token is ever held in this process. */
export class ProxyInjectedToken implements TokenSource {
  readonly kind = "injected";

  describe(): string {
    return "access token injected by the environment's credential proxy";
  }

  async authorization(): Promise<string | null> {
    return null;
  }

  async renew(): Promise<boolean> {
    return false;
  }
}

/** HANDOFF_CHATGPT_AUTH chooses the source: stored (default), environment, or injected. */
export function tokenSourceFromEnvironment(env: NodeJS.ProcessEnv = process.env, fetchImpl?: Fetch): TokenSource {
  const mode = env.HANDOFF_CHATGPT_AUTH ?? "stored";
  switch (mode) {
    case "stored":
      return new StoredCredentials(CredentialStore.fromEnvironment(env), { label: env.HANDOFF_CHATGPT_ACCOUNT, fetch: fetchImpl });
    case "environment":
      return new EnvironmentToken("HANDOFF_CHATGPT_ACCESS_TOKEN", env);
    case "injected":
      return new ProxyInjectedToken();
    default:
      throw new Error(`HANDOFF_CHATGPT_AUTH must be stored, environment or injected, not ${mode}`);
  }
}
