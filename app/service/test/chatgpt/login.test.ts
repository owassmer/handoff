import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { login } from "../../src/llm/chatgpt/login.js";
import { type CredentialStore } from "../../src/llm/chatgpt/store.js";
import { FakeOpenAI, tempStore, testSigner, tokenJson } from "./fakes.js";

const PLAN_SCOPES = "chatgpt.tokens.use.direct email offline_access openid profile resource.invoke";
let store: CredentialStore;
let cleanup: () => Promise<void>;
beforeEach(async () => ({ store, cleanup } = await tempStore()));
afterEach(() => cleanup());

/**
 * Plays the user's browser: reads the authorization request, then returns to the loopback callback the
 * way OpenAI would. It does not wait for the page, just as a browser would not block the app.
 */
function browser(reply: (authorize: URL) => Record<string, string>) {
  const seen: { authorize?: URL; page?: Promise<string> } = {};
  const open = (url: string) => {
    const authorize = new URL(url);
    seen.authorize = authorize;
    const back = new URL(authorize.searchParams.get("redirect_uri")!);
    for (const [k, v] of Object.entries(reply(authorize))) back.searchParams.set(k, v);
    seen.page = fetch(back).then((r) => r.text());
  };
  return { open, seen };
}

async function signer(clientId: string, sub = "user-123") {
  const { jwks, idToken } = await testSigner();
  return { jwks, token: (nonce: string) => idToken({ aud: clientId, nonce, sub }) };
}

describe("signing in from the computer with the browser", () => {
  it("registers a new client, validates it, and saves only what was validated", async () => {
    const s = await signer("oaiapp_new123");
    let nonce = "";
    const b = browser((a) => {
      nonce = a.searchParams.get("nonce")!;
      return { code: "code-1", state: a.searchParams.get("state")!, client_id: "oaiapp_new123", scope: PLAN_SCOPES };
    });
    const api = new FakeOpenAI().on((r) => r.url.endsWith("/oauth/token"), async () => tokenJson({ id_token: await s.token(nonce) }));
    const result = await login({ store, port: 0, fetch: api.fetch, jwks: s.jwks, openBrowser: b.open, log: () => {} });

    const host = await store.hostIdentity();
    expect(b.seen.authorize!.searchParams.get("client_id")).toBe("dynamic_agent_client");
    expect(b.seen.authorize!.searchParams.get("ext_agent_host_id")).toBe(host.ext_agent_host_id);
    const redirect = b.seen.authorize!.searchParams.get("redirect_uri")!;
    expect(redirect).toMatch(/^http:\/\/127\.0\.0\.1:\d+\/auth\/callback$/);
    expect(api.form(0)).toMatchObject({ grant_type: "authorization_code", client_id: "oaiapp_new123", code: "code-1", redirect_uri: redirect });
    expect(result).toMatchObject({ newRegistration: true, planEnabled: true });
    expect(await store.read(result.record.label)).toMatchObject({
      client_id: "oaiapp_new123", subject: "user-123", email: "owner@example.com", ext_agent_host_id: host.ext_agent_host_id,
      access_token: "at-1", refresh_token: "rt-1", token_type: "Bearer", expires_in: 3600,
    });
    expect(await store.active()).toBe(result.record.label);
    expect(await b.seen.page).toMatch(/connected to your ChatGPT plan/);
  });

  it("signs in again with the saved client and refuses a different account", async () => {
    const first = await signer("oaiapp_saved1");
    let nonce = "";
    const reg = browser((a) => ((nonce = a.searchParams.get("nonce")!), { code: "c1", state: a.searchParams.get("state")!, client_id: "oaiapp_saved1", scope: PLAN_SCOPES }));
    const api1 = new FakeOpenAI().on(() => true, async () => tokenJson({ id_token: await first.token(nonce) }));
    const { record } = await login({ store, port: 0, fetch: api1.fetch, jwks: first.jwks, openBrowser: reg.open, log: () => {} });

    // Same person: the callback may omit client_id; the saved one is used.
    const again = browser((a) => ((nonce = a.searchParams.get("nonce")!), { code: "c2", state: a.searchParams.get("state")! }));
    const api2 = new FakeOpenAI().on(() => true, async () => tokenJson({ id_token: await first.token(nonce), access_token: "at-2" }));
    await login({ store, label: record.label, port: 0, fetch: api2.fetch, jwks: first.jwks, openBrowser: again.open, log: () => {} });
    expect(again.seen.authorize!.searchParams.get("client_id")).toBe("oaiapp_saved1");
    expect(again.seen.authorize!.searchParams.has("agent_name_hint")).toBe(false);
    expect(again.seen.authorize!.searchParams.get("id_token_hint")).toBeTruthy();
    expect((await store.read(record.label))!.access_token).toBe("at-2");

    // Someone else in the browser: nothing is replaced.
    const other = await signer("oaiapp_saved1", "someone-else");
    const wrong = browser((a) => ((nonce = a.searchParams.get("nonce")!), { code: "c3", state: a.searchParams.get("state")! }));
    const api3 = new FakeOpenAI().on(() => true, async () => tokenJson({ id_token: await other.token(nonce), access_token: "at-3" }));
    await expect(login({ store, label: record.label, port: 0, fetch: api3.fetch, jwks: other.jwks, openBrowser: wrong.open, log: () => {} })).rejects.toThrow(/different ChatGPT account/);
    expect((await store.read(record.label))!.access_token).toBe("at-2");
    expect(await wrong.seen.page).toMatch(/did not complete/);
  });

  it("stops without exchanging a code when permission is declined", async () => {
    const b = browser((a) => ({ error: "access_denied", state: a.searchParams.get("state")! }));
    const api = new FakeOpenAI();
    await expect(login({ store, port: 0, fetch: api.fetch, openBrowser: b.open, log: () => {} })).rejects.toMatchObject({ kind: "access_denied" });
    expect(api.requests).toHaveLength(0);
    expect(await store.list()).toEqual([]);
  });

  it("keeps the sign-in but marks plan usage disabled when that permission is not granted", async () => {
    const s = await signer("oaiapp_noplan");
    let nonce = "";
    const b = browser((a) => ((nonce = a.searchParams.get("nonce")!), { code: "c1", state: a.searchParams.get("state")!, client_id: "oaiapp_noplan" }));
    const api = new FakeOpenAI().on(() => true, async () => tokenJson({ id_token: await s.token(nonce), scope: "email offline_access openid profile resource.invoke" }));
    const result = await login({ store, port: 0, fetch: api.fetch, jwks: s.jwks, openBrowser: b.open, log: () => {} });
    expect(result.planEnabled).toBe(false);
    expect(await b.seen.page).toMatch(/was not granted/);
  });
});
