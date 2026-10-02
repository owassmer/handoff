import { type PublicOauthClient, createPublicOauthClient } from "@osdk/oauth";
import { webcrypto } from "node:crypto";
import { afterEach, expect, it, vi } from "vitest";
import { memoryStorage } from "./examples.test-support";
import { restartSignIn } from "./signIn";

afterEach(() => {
  vi.clearAllTimers();
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

it("uses the installed public OAuth client to revoke a cached grant and redirect afresh, including completed callback state", async () => {
  vi.useFakeTimers();
  vi.stubGlobal("crypto", webcrypto);
  // The SDK owns its storage and all PKCE handling. The test never reads or clears its keys.
  vi.stubGlobal("sessionStorage", memoryStorage());
  const location = {
    href: "https://handoff.test.invalid/handoffs/garden-home",
    get pathname() {
      return new URL(this.href).pathname;
    },
    toString() {
      return this.href;
    },
    assign: vi.fn(),
  };
  vi.stubGlobal("window", {
    location,
    history: {
      replaceState: (_state: unknown, _unused: string, href: string) => {
        location.href = href;
      },
    },
  });
  const requests: string[] = [];
  const fetchFn: typeof fetch = async (input, init) => {
    const path = new URL(new Request(input, init).url).pathname;
    requests.push(path);
    if (path.endsWith("/oauth2/token")) {
      return new Response(
        JSON.stringify({ token_type: "Bearer", access_token: "test-session", expires_in: 3600 }),
        {
          status: 200,
          headers: { "Content-Type": "application/json" },
        },
      );
    }
    if (path.endsWith("/oauth2/revoke_token")) {
      return new Response(null, { status: 200 });
    }
    throw new Error("Unexpected test request");
  };
  const auth = createPublicOauthClient(
    "test-client",
    "https://foundry.test.invalid",
    "https://handoff.test.invalid/auth/callback",
    {
      scopes: ["api:use-admin-read"],
      fetchFn,
    },
  );
  const initial = auth.signIn().catch((error: unknown) => error);
  await vi.waitFor(() => expect(location.assign).toHaveBeenCalledTimes(1));
  await vi.advanceTimersByTimeAsync(1100);
  expect(await initial).toBeInstanceOf(Error); // No actual navigation in the test browser.
  const authorize = new URL(location.assign.mock.calls[0][0] as string);
  expect(authorize.searchParams.get("scope")).toContain("api:use-admin-read");
  location.href = `https://handoff.test.invalid/auth/callback?code=test-code&state=${authorize.searchParams.get("state")}`;
  await auth.signIn();
  expect(location.pathname).toBe("/handoffs/garden-home");
  expect(Boolean(auth.getTokenOrUndefined())).toBe(true);
  const fresh = restartSignIn(auth).catch((error: unknown) => error);
  await vi.waitFor(() => expect(location.assign).toHaveBeenCalledTimes(2));
  await vi.advanceTimersByTimeAsync(1100);
  expect(await fresh).toBeInstanceOf(Error); // Failed navigation reaches the caller for feedback.
  expect(auth.getTokenOrUndefined()).toBeUndefined();
  expect(requests).toEqual(["/multipass/api/oauth2/token", "/multipass/api/oauth2/revoke_token"]);
});

it("revokes a session restored by the SDK instead of treating a refresh as fresh authorization", async () => {
  const order: string[] = [];
  const auth = {
    getTokenOrUndefined: () => undefined,
    signIn: vi.fn(async () => {
      order.push("sign-in");
    }),
    signOut: vi.fn(async () => {
      order.push("sign-out");
    }),
  } as unknown as PublicOauthClient;
  await restartSignIn(auth);
  expect(order).toEqual(["sign-in", "sign-out", "sign-in"]);
});

it("does not silently retry arbitrary authorization or network failures", async () => {
  const failure = new Error("Sign-in was declined");
  const auth = {
    getTokenOrUndefined: () => undefined,
    signIn: vi.fn().mockRejectedValue(failure),
    signOut: vi.fn(),
  } as unknown as PublicOauthClient;
  await expect(restartSignIn(auth)).rejects.toBe(failure);
  expect(auth.signIn).toHaveBeenCalledTimes(1);
  expect(auth.signOut).not.toHaveBeenCalled();
});
