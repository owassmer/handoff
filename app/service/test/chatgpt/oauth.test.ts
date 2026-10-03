import { describe, expect, it } from "vitest";
import {
  CallbackError, authorizationUrl, callbackUri, exchangeCode, grantedScopes, newAttempt, pkceChallenge, planEnabled, readCallback,
  redactedUrl, refreshGrant, verifyIdToken,
} from "../../src/llm/chatgpt/oauth.js";
import { FakeOpenAI, testSigner, tokenJson } from "./fakes.js";

const HOST = "urn:ietf:params:oauth:jwk-thumbprint:sha-256:abc";

describe("authorization request", () => {
  it("registers a new client with the documented parameters", () => {
    const attempt = newAttempt();
    const url = new URL(authorizationUrl({ clientId: null, hostId: HOST, redirectUri: callbackUri(1455), attempt }));
    expect(url.origin + url.pathname).toBe("https://auth.openai.com/api/accounts/authorize");
    expect(Object.fromEntries(url.searchParams)).toEqual({
      client_id: "dynamic_agent_client",
      agent_name_hint: "Handoff",
      ext_agent_host_id: HOST,
      response_type: "code",
      redirect_uri: "http://127.0.0.1:1455/auth/callback",
      scope: "openid profile email offline_access resource.invoke chatgpt.tokens.use.direct",
      resource: "https://api.openai.com/v1",
      state: attempt.state,
      nonce: attempt.nonce,
      code_challenge_method: "S256",
      code_challenge: attempt.challenge,
    });
  });

  it("signs in again with the issued client, hints, and no name hint", () => {
    const url = new URL(authorizationUrl({ clientId: "oaiapp_123", hostId: HOST, redirectUri: callbackUri(54321), attempt: newAttempt(), idTokenHint: "old.id.token", loginHint: "owner@example.com" }));
    expect(url.searchParams.get("client_id")).toBe("oaiapp_123");
    expect(url.searchParams.has("agent_name_hint")).toBe(false);
    expect(url.searchParams.get("id_token_hint")).toBe("old.id.token");
    expect(url.searchParams.get("login_hint")).toBe("owner@example.com");
    expect(url.searchParams.get("redirect_uri")).toBe("http://127.0.0.1:54321/auth/callback");
    expect(redactedUrl(url.toString())).not.toContain("old.id.token");
  });

  it("uses fresh values every attempt and an S256 challenge without padding", () => {
    const a = newAttempt();
    const b = newAttempt();
    expect(new Set([a.state, a.nonce, a.verifier, b.state, b.nonce, b.verifier]).size).toBe(6);
    // RFC 7636 appendix B example.
    expect(pkceChallenge("dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk")).toBe("E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM");
  });
});

describe("callback", () => {
  const attempt = newAttempt();
  const cb = (q: Record<string, string>) => new URL(`http://127.0.0.1:1455/auth/callback?${new URLSearchParams(q)}`);

  it("returns the issued client id for a new registration", () => {
    expect(readCallback(cb({ code: "c1", state: attempt.state, client_id: "oaiapp_new", scope: "openid" }), { attempt, clientId: null }))
      .toEqual({ code: "c1", clientId: "oaiapp_new", scope: "openid" });
  });

  it("rejects the wrong state before anything else, a declined consent, and an incomplete registration", () => {
    expect(() => readCallback(cb({ code: "c1", state: "other", client_id: "oaiapp_new" }), { attempt, clientId: null })).toThrow(expect.objectContaining({ kind: "state_mismatch" }));
    expect(() => readCallback(cb({ error: "access_denied", state: attempt.state }), { attempt, clientId: null })).toThrow(expect.objectContaining({ kind: "access_denied" }));
    expect(() => readCallback(cb({ code: "c1", state: attempt.state }), { attempt, clientId: null })).toThrow(expect.objectContaining({ kind: "registration_incomplete" }));
    expect(() => readCallback(cb({ code: "c1", state: attempt.state, client_id: "dynamic_agent_client" }), { attempt, clientId: null })).toThrow(CallbackError);
  });

  it("keeps the saved client on reauthorization and refuses a different one", () => {
    expect(readCallback(cb({ code: "c2", state: attempt.state }), { attempt, clientId: "oaiapp_saved" }).clientId).toBe("oaiapp_saved");
    expect(() => readCallback(cb({ code: "c2", state: attempt.state, client_id: "oaiapp_other" }), { attempt, clientId: "oaiapp_saved" })).toThrow(expect.objectContaining({ kind: "client_mismatch" }));
  });
});

describe("token endpoint", () => {
  it("exchanges the code with the issued client, verifier, same redirect and resource, and no secret", async () => {
    const api = new FakeOpenAI().on((r) => r.url.endsWith("/oauth/token"), () => tokenJson());
    await exchangeCode(api.fetch, { clientId: "oaiapp_1", code: "c1", verifier: "v1", redirectUri: callbackUri(1455) });
    expect(api.requests[0]!.headers["content-type"]).toBe("application/x-www-form-urlencoded");
    expect(api.form(0)).toEqual({ grant_type: "authorization_code", client_id: "oaiapp_1", code: "c1", code_verifier: "v1", redirect_uri: "http://127.0.0.1:1455/auth/callback", resource: "https://api.openai.com/v1" });
  });

  it("refreshes with the issued client and resource, omitting scope", async () => {
    const api = new FakeOpenAI().on((r) => r.url.endsWith("/oauth/token"), () => tokenJson());
    await refreshGrant(api.fetch, { clientId: "oaiapp_1", refreshToken: "rt-0" });
    expect(api.form(0)).toEqual({ grant_type: "refresh_token", client_id: "oaiapp_1", refresh_token: "rt-0", resource: "https://api.openai.com/v1" });
  });

  it("reports an unusable refresh token by its code", async () => {
    const api = new FakeOpenAI().on(() => true, () => Response.json({ error: "refresh_token_reused" }, { status: 400 }));
    await expect(refreshGrant(api.fetch, { clientId: "c", refreshToken: "r" })).rejects.toMatchObject({ code: "refresh_token_reused", unusableRefresh: true });
  });
});

describe("ID token and plan permission", () => {
  it("accepts only a token signed by the key set, for this client, with this nonce, unexpired", async () => {
    const { jwks, idToken } = await testSigner();
    const ok = await idToken({ aud: "oaiapp_1", nonce: "n1" });
    expect(await verifyIdToken(ok, { clientId: "oaiapp_1", nonce: "n1" }, jwks)).toEqual({ subject: "user-123", email: "owner@example.com", issuer: "https://auth.openai.com" });
    await expect(verifyIdToken(ok, { clientId: "oaiapp_1", nonce: "other" }, jwks)).rejects.toThrow(/nonce/);
    await expect(verifyIdToken(ok, { clientId: "oaiapp_2", nonce: "n1" }, jwks)).rejects.toThrow();
    await expect(verifyIdToken(await idToken({ aud: "oaiapp_1", nonce: "n1", iss: "https://evil.example" }), { clientId: "oaiapp_1", nonce: "n1" }, jwks)).rejects.toThrow();
    await expect(verifyIdToken(await idToken({ aud: "oaiapp_1", nonce: "n1", expiresIn: "-1m" }), { clientId: "oaiapp_1", nonce: "n1" }, jwks)).rejects.toThrow();
    const other = await testSigner();
    await expect(verifyIdToken(await other.idToken({ aud: "oaiapp_1", nonce: "n1" }), { clientId: "oaiapp_1", nonce: "n1" }, jwks)).rejects.toThrow();
  });

  it("treats plan usage as enabled only with chatgpt.tokens.use.direct granted", () => {
    expect(planEnabled(grantedScopes("openid profile email offline_access resource.invoke chatgpt.tokens.use.direct"))).toBe(true);
    expect(planEnabled(grantedScopes("openid profile email offline_access resource.invoke"))).toBe(false);
  });
});
