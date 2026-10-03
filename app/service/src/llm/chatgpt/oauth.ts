import { createHash, randomBytes } from "node:crypto";
import { createRemoteJWKSet, type JWTVerifyGetKey, jwtVerify } from "jose";
import { API_RESOURCE, AGENT_NAME, CALLBACK_HOST, CALLBACK_PATH, DYNAMIC_CLIENT, OPENAI_AUTH, PLAN_SCOPE, REQUESTED_SCOPES, UNUSABLE_REFRESH_CODES } from "./config.js";

export type Fetch = typeof fetch;

const b64url = (b: Buffer) => b.toString("base64url");

/** Fresh state, nonce and PKCE values for one authorization attempt. */
export interface Attempt {
  state: string;
  nonce: string;
  verifier: string;
  challenge: string;
}

export function newAttempt(): Attempt {
  const verifier = b64url(randomBytes(32));
  return { state: b64url(randomBytes(32)), nonce: b64url(randomBytes(32)), verifier, challenge: pkceChallenge(verifier) };
}

/** Base64url SHA-256 of the verifier, without padding. */
export function pkceChallenge(verifier: string): string {
  return b64url(createHash("sha256").update(verifier).digest());
}

export function callbackUri(port: number): string {
  return `http://${CALLBACK_HOST}:${port}${CALLBACK_PATH}`;
}

export interface AuthorizationRequest {
  /** The saved issued client id, or null to register a new client. */
  clientId: string | null;
  hostId: string;
  redirectUri: string;
  attempt: Attempt;
  idTokenHint?: string | null;
  loginHint?: string | null;
  /** Re-request consent, e.g. to enable plan usage after an earlier decline. Not for ordinary sign-ins. */
  requestConsent?: boolean;
}

export function authorizationUrl(r: AuthorizationRequest): string {
  const p = new URLSearchParams();
  p.set("client_id", r.clientId ?? DYNAMIC_CLIENT);
  if (r.clientId === null) p.set("agent_name_hint", AGENT_NAME);
  p.set("ext_agent_host_id", r.hostId);
  if (r.clientId !== null && r.idTokenHint) p.set("id_token_hint", r.idTokenHint);
  if (r.clientId !== null && r.loginHint) p.set("login_hint", r.loginHint);
  p.set("response_type", "code");
  p.set("redirect_uri", r.redirectUri);
  p.set("scope", REQUESTED_SCOPES.join(" "));
  p.set("resource", API_RESOURCE);
  p.set("state", r.attempt.state);
  p.set("nonce", r.attempt.nonce);
  p.set("code_challenge_method", "S256");
  p.set("code_challenge", r.attempt.challenge);
  if (r.requestConsent) p.set("prompt", "consent");
  return `${OPENAI_AUTH.authorizeEndpoint}?${p.toString()}`;
}

/** An authorization URL safe to log: the ID-token hint is removed. */
export function redactedUrl(url: string): string {
  const u = new URL(url);
  if (u.searchParams.has("id_token_hint")) u.searchParams.set("id_token_hint", "[redacted]");
  return u.toString();
}

export type CallbackFailure = "state_mismatch" | "access_denied" | "oauth_error" | "missing_code" | "registration_incomplete" | "client_mismatch";

export class CallbackError extends Error {
  constructor(readonly kind: CallbackFailure, message: string) {
    super(message);
  }
}

/**
 * Reads the browser's return to the loopback callback. State is checked before anything else is used.
 * A new registration must carry the issued client id; a reauthorization keeps the one it started with.
 */
export function readCallback(url: URL, pending: { attempt: Attempt; clientId: string | null }): { code: string; clientId: string; scope: string | null } {
  const q = url.searchParams;
  if (q.get("state") !== pending.attempt.state) throw new CallbackError("state_mismatch", "the sign-in response does not belong to this attempt");
  const error = q.get("error");
  if (error === "access_denied") throw new CallbackError("access_denied", "permission was declined in the browser");
  if (error) throw new CallbackError("oauth_error", `sign-in failed: ${error}${q.get("error_description") ? ` (${q.get("error_description")})` : ""}`);
  const code = q.get("code");
  if (!code) throw new CallbackError("missing_code", "the sign-in response carried no authorization code");
  const returned = q.get("client_id");
  let clientId: string;
  if (pending.clientId === null) {
    if (!returned || returned === DYNAMIC_CLIENT) throw new CallbackError("registration_incomplete", "registration did not return an issued client id");
    clientId = returned;
  } else {
    if (returned && returned !== pending.clientId) throw new CallbackError("client_mismatch", "the sign-in returned a different client than the selected account's");
    clientId = pending.clientId;
  }
  return { code, clientId, scope: q.get("scope") };
}

export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  id_token?: string;
  token_type: string;
  expires_in: number;
  scope?: string;
  earliest_refresh_at?: number | string;
}

/** An error from the token or revocation endpoint, by its machine-readable code. */
export class OAuthError extends Error {
  constructor(readonly status: number, readonly code: string | null, readonly description: string | null) {
    super(`token endpoint returned ${status}${code ? ` ${code}` : ""}${description ? `: ${description}` : ""}`);
  }

  /** The refresh token can no longer be used; the user must sign in again. */
  get unusableRefresh(): boolean {
    return this.code !== null && UNUSABLE_REFRESH_CODES.has(this.code);
  }

  /** A network-level or server failure: keep the credentials and try later. */
  get transient(): boolean {
    return this.status === 0 || this.status >= 500;
  }
}

async function postForm(f: Fetch, url: string, form: Record<string, string>): Promise<Response> {
  try {
    return await f(url, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded", Accept: "application/json" }, body: new URLSearchParams(form).toString() });
  } catch (e) {
    throw new OAuthError(0, null, `network error: ${e instanceof Error ? e.message : String(e)}`);
  }
}

async function tokenRequest(f: Fetch, form: Record<string, string>): Promise<TokenResponse> {
  const res = await postForm(f, OPENAI_AUTH.tokenEndpoint, form);
  const text = await res.text();
  let body: Record<string, unknown> = {};
  try {
    body = JSON.parse(text) as Record<string, unknown>;
  } catch {
    // Not JSON; the status says what happened.
  }
  if (!res.ok) {
    const nested = body.error && typeof body.error === "object" ? (body.error as Record<string, unknown>) : null;
    const code = typeof body.error === "string" ? body.error : typeof nested?.code === "string" ? nested.code : null;
    const description = typeof body.error_description === "string" ? body.error_description : typeof nested?.message === "string" ? nested.message : null;
    throw new OAuthError(res.status, code, description);
  }
  if (typeof body.access_token !== "string") throw new OAuthError(res.status, "invalid_response", "the token response had no access token");
  return body as unknown as TokenResponse;
}

/** Authorization-code exchange: the issued client id, the same redirect URI and resource, and the PKCE verifier. No secret. */
export function exchangeCode(f: Fetch, p: { clientId: string; code: string; verifier: string; redirectUri: string }): Promise<TokenResponse> {
  return tokenRequest(f, { grant_type: "authorization_code", client_id: p.clientId, code: p.code, code_verifier: p.verifier, redirect_uri: p.redirectUri, resource: API_RESOURCE });
}

/** Refresh with the issued client id. Scope is omitted so the grant is retained. */
export function refreshGrant(f: Fetch, p: { clientId: string; refreshToken: string }): Promise<TokenResponse> {
  return tokenRequest(f, { grant_type: "refresh_token", client_id: p.clientId, refresh_token: p.refreshToken, resource: API_RESOURCE });
}

/** Ends the renewable session. An empty 200 is success, including for a token already invalid. */
export async function revokeRefreshToken(f: Fetch, p: { clientId: string; refreshToken: string }): Promise<void> {
  const discovery = await f(OPENAI_AUTH.discovery).then((r) => r.json() as Promise<{ revocation_endpoint?: string }>);
  if (!discovery.revocation_endpoint) throw new OAuthError(0, null, "the discovery document names no revocation endpoint");
  const res = await postForm(f, discovery.revocation_endpoint, { token: p.refreshToken, token_type_hint: "refresh_token", client_id: p.clientId });
  if (!res.ok) throw new OAuthError(res.status, null, await res.text());
}

export function remoteJwks(): JWTVerifyGetKey {
  return createRemoteJWKSet(new URL(OPENAI_AUTH.jwksUri));
}

export interface VerifiedIdentity {
  subject: string;
  email: string | null;
  issuer: string;
}

/** Verifies the ID token's signature against OpenAI's keys, then issuer, audience (the issued client id), expiry and nonce. */
export async function verifyIdToken(idToken: string, p: { clientId: string; nonce: string }, keys: JWTVerifyGetKey = remoteJwks()): Promise<VerifiedIdentity> {
  const { payload } = await jwtVerify(idToken, keys, {
    issuer: OPENAI_AUTH.issuer,
    audience: p.clientId,
    requiredClaims: ["sub", "exp", "iat"],
    clockTolerance: 5,
  });
  if (payload.nonce !== p.nonce) throw new Error("the ID token nonce did not match this attempt");
  if (typeof payload.sub !== "string" || !payload.sub) throw new Error("the ID token has no subject");
  return { subject: payload.sub, email: typeof payload.email === "string" ? payload.email : null, issuer: OPENAI_AUTH.issuer };
}

export function grantedScopes(scope: string | null | undefined): string[] {
  return (scope ?? "").split(/\s+/).filter(Boolean).sort();
}

export function planEnabled(scopes: readonly string[]): boolean {
  return scopes.includes(PLAN_SCOPE);
}
