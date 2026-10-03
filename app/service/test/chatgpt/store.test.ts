import { mkdir, mkdtemp, readFile, readdir, rm, stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { exportAccount, importAccount, logout } from "../../src/llm/chatgpt/login.js";
import { type CredentialRecord, CredentialLocationError, CredentialStore } from "../../src/llm/chatgpt/store.js";
import { PlanNotEnabled, ReauthorizationRequired, StoredCredentials, TransientAuthError } from "../../src/llm/chatgpt/tokens.js";
import { FakeOpenAI, tempStore, tokenJson } from "./fakes.js";

let store: CredentialStore;
let cleanup: () => Promise<void>;
beforeEach(async () => ({ store, cleanup } = await tempStore()));
afterEach(() => cleanup());

const NOW = Date.parse("2026-10-03T12:00:00Z");

function record(over: Partial<CredentialRecord> = {}): CredentialRecord {
  return {
    label: "owner-abc123", email: "owner@example.com", issuer: "https://auth.openai.com", subject: "user-123", client_id: "oaiapp_abc123",
    ext_agent_host_id: "urn:uuid:11111111-1111-4111-8111-111111111111", id_token: "idt", access_token: "at-old", refresh_token: "rt-old",
    token_type: "Bearer", expires_in: 3600,
    scopes: ["chatgpt.tokens.use.direct", "email", "offline_access", "openid", "profile", "resource.invoke"],
    saved_at: new Date(NOW - 3_590_000).toISOString(), expires_at: new Date(NOW + 10_000).toISOString(), earliest_refresh_at: null, ...over,
  };
}

describe("where and how credentials are kept", () => {
  it("keeps folders and files owner-only and writes atomically", async () => {
    await store.write(record());
    expect((await stat(store.dir)).mode & 0o777).toBe(0o700);
    expect((await stat(join(store.dir, "accounts"))).mode & 0o777).toBe(0o700);
    expect((await stat(join(store.dir, "accounts", "owner-abc123.json"))).mode & 0o777).toBe(0o600);
    expect((await readdir(join(store.dir, "accounts"))).filter((f) => f.endsWith(".tmp"))).toEqual([]);
  });

  it("refuses a location inside a git repository", async () => {
    const repo = await mkdtemp(join(tmpdir(), "repo-"));
    await mkdir(join(repo, ".git"));
    await expect(new CredentialStore(join(repo, "creds")).write(record())).rejects.toThrow(CredentialLocationError);
    await rm(repo, { recursive: true, force: true });
    await expect(new CredentialStore("/home/user/handoff/app/.chatgpt").ensure()).rejects.toThrow(CredentialLocationError);
  });

  it("creates this host's id once, as a JWK thumbprint URI, and reuses it", async () => {
    const first = await store.hostIdentity();
    expect(first.ext_agent_host_id).toMatch(/^urn:ietf:params:oauth:jwk-thumbprint:sha-256:[A-Za-z0-9_-]{43}$/);
    expect((await new CredentialStore(store.dir).hostIdentity()).ext_agent_host_id).toBe(first.ext_agent_host_id);
    expect((await stat(join(store.dir, "host.json"))).mode & 0o777).toBe(0o600);
  });
});

describe("refresh", () => {
  it("uses a fresh token without refreshing, and refreshes near expiry with the documented request", async () => {
    await store.write(record({ expires_at: new Date(NOW + 3_000_000).toISOString() }));
    await store.setActive("owner-abc123");
    const api = new FakeOpenAI().on((r) => r.url.endsWith("/oauth/token"), () => tokenJson({ access_token: "at-new", refresh_token: "rt-new" }));
    expect(await new StoredCredentials(store, { fetch: api.fetch, now: () => NOW }).authorization()).toBe("Bearer at-old");
    expect(api.requests).toHaveLength(0);

    await store.write(record());
    expect(await new StoredCredentials(store, { fetch: api.fetch, now: () => NOW }).authorization()).toBe("Bearer at-new");
    expect(api.form(0)).toEqual({ grant_type: "refresh_token", client_id: "oaiapp_abc123", refresh_token: "rt-old", resource: "https://api.openai.com/v1" });
    const saved = (await store.read("owner-abc123"))!;
    expect(saved).toMatchObject({ access_token: "at-new", refresh_token: "rt-new", expires_in: 3600, client_id: "oaiapp_abc123" });
    expect(saved.expires_at).toBe(new Date(NOW + 3_600_000).toISOString());
  });

  it("serializes refreshes across processes so a rotating token is spent once", async () => {
    await store.write(record());
    let calls = 0;
    const api = new FakeOpenAI().on((r) => r.url.endsWith("/oauth/token"), async () => {
      calls++;
      await new Promise((r) => setTimeout(r, 50));
      return tokenJson({ access_token: `at-${calls}`, refresh_token: `rt-${calls}` });
    });
    // Two stores on one folder stand for two processes on one host.
    const a = new StoredCredentials(new CredentialStore(store.dir), { label: "owner-abc123", fetch: api.fetch, now: () => NOW });
    const b = new StoredCredentials(new CredentialStore(store.dir), { label: "owner-abc123", fetch: api.fetch, now: () => NOW });
    const tokens = await Promise.all([a.authorization(), b.authorization(), a.authorization(), b.authorization()]);
    expect(calls).toBe(1);
    expect(new Set(tokens)).toEqual(new Set(["Bearer at-1"]));
    expect(api.form(0).refresh_token).toBe("rt-old");
  });

  it("clears an unusable session but keeps the registration, and asks for sign-in again", async () => {
    await store.write(record());
    const api = new FakeOpenAI().on(() => true, () => Response.json({ error: "invalid_grant" }, { status: 400 }));
    await expect(new StoredCredentials(store, { label: "owner-abc123", fetch: api.fetch, now: () => NOW }).authorization()).rejects.toThrow(ReauthorizationRequired);
    expect(await store.read("owner-abc123")).toMatchObject({ access_token: null, refresh_token: null, client_id: "oaiapp_abc123", id_token: "idt", ext_agent_host_id: record().ext_agent_host_id });
  });

  it("keeps the credentials through a temporary failure", async () => {
    await store.write(record());
    const api = new FakeOpenAI().on(() => true, () => new Response("upstream", { status: 503 }));
    await expect(new StoredCredentials(store, { label: "owner-abc123", fetch: api.fetch, now: () => NOW }).authorization()).rejects.toThrow(TransientAuthError);
    expect(await store.read("owner-abc123")).toMatchObject({ refresh_token: "rt-old" });
  });

  it("refuses to serve a token for an account without plan permission", async () => {
    await store.write(record({ scopes: ["email", "offline_access", "openid", "profile", "resource.invoke"], expires_at: new Date(NOW + 3_000_000).toISOString() }));
    await expect(new StoredCredentials(store, { label: "owner-abc123", now: () => NOW }).authorization()).rejects.toThrow(PlanNotEnabled);
  });

  it("after a 401, obtains a different token once, or reports that it cannot", async () => {
    await store.write(record({ expires_at: new Date(NOW + 3_000_000).toISOString() }));
    const api = new FakeOpenAI().on(() => true, () => tokenJson({ access_token: "at-renewed", refresh_token: "rt-2" }));
    const src = new StoredCredentials(store, { label: "owner-abc123", fetch: api.fetch, now: () => NOW });
    expect(await src.renew("Bearer at-old")).toBe(true);
    expect(await src.authorization()).toBe("Bearer at-renewed");
  });
});

describe("moving a session and signing out", () => {
  it("imports onto another host without taking the copied host id", async () => {
    await store.write(record());
    const file = join(store.dir, "..", "transfer.json");
    await exportAccount(store, "owner-abc123", file);
    expect((await stat(file)).mode & 0o777).toBe(0o600);
    const vm = await tempStore();
    try {
      const vmHost = await vm.store.hostIdentity();
      const imported = await importAccount(vm.store, JSON.parse(await readFile(file, "utf8")));
      expect(imported.ext_agent_host_id).toBe(vmHost.ext_agent_host_id);
      expect(imported.imported_from_host).toBe(record().ext_agent_host_id);
      expect(imported).toMatchObject({ client_id: "oaiapp_abc123", refresh_token: "rt-old" });
      expect(await vm.store.active()).toBe("owner-abc123");
    } finally {
      await vm.cleanup();
    }
  });

  it("revokes the renewable session, then clears tokens but keeps the client id", async () => {
    await store.write(record());
    const api = new FakeOpenAI()
      .on((r) => r.url.endsWith("openid-configuration"), () => Response.json({ revocation_endpoint: "https://auth.openai.com/api/accounts/oauth/revoke" }))
      .on((r) => r.url.endsWith("/oauth/revoke"), () => new Response(null, { status: 200 }));
    expect(await logout(store, "owner-abc123", api.fetch)).toEqual({ revoked: true });
    expect(api.form(1)).toEqual({ token: "rt-old", token_type_hint: "refresh_token", client_id: "oaiapp_abc123" });
    expect(await store.read("owner-abc123")).toMatchObject({ access_token: null, refresh_token: null, id_token: null, client_id: "oaiapp_abc123" });
  });
});
