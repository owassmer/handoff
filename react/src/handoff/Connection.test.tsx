// @vitest-environment jsdom
import { StrictMode } from "react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { type Client, createClient } from "@osdk/client";
import type { PublicOauthClient } from "@osdk/oauth";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { HandoffCasePage } from "./App";
import { HandoffConnectionPage } from "./Connection";
import type { HandoffGateway } from "./contracts";
import { exampleGateway } from "./examples.test-support";

const harness = vi.hoisted(() => {
  const events = new EventTarget();
  const auth = Object.assign(
    vi.fn(async () => "test-session"),
    {
      signIn: vi.fn<PublicOauthClient["signIn"]>(),
      signOut: vi.fn<PublicOauthClient["signOut"]>(),
      refresh: vi.fn<PublicOauthClient["refresh"]>(),
      getTokenOrUndefined: vi.fn<PublicOauthClient["getTokenOrUndefined"]>(),
      addEventListener: events.addEventListener.bind(events),
      removeEventListener: events.removeEventListener.bind(events),
    },
  );
  return {
    auth,
    events,
    client: undefined as Client | undefined,
    gateway: undefined as HandoffGateway | undefined,
  };
});
vi.mock("../client", () => ({ auth: harness.auth, ontologyRid: "test-ontology" }));
vi.mock("@osdk/react", () => ({ useOsdkClient: () => harness.client }));
vi.mock("./branchConfig", () => ({
  HANDOFF_BRANCH: "test-branch",
  handoffDeployment: { workspaceId: "test-workspace", functionVersion: "1.0.0" },
}));
vi.mock("./gateway", async (original) => ({
  ...(await original<typeof import("./gateway")>()),
  createHandoffGateway: () => harness.gateway,
}));

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (error: unknown) => void;
  const promise = new Promise<T>((yes, no) => {
    resolve = yes;
    reject = no;
  });
  return { promise, resolve, reject };
}
const response = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
const denied = () =>
  response(
    {
      errorCode: "PERMISSION_DENIED",
      errorName: "ApiUsageDenied",
      errorInstanceId: "private-error-reference",
      parameters: { privateDetail: "do-not-display" },
    },
    403,
  );
const signedOut = () => response({ errorCode: "UNAUTHORIZED", errorName: "Unauthorized" }, 401);
const transport = vi.fn<typeof fetch>();
function open() {
  render(
    <StrictMode>
      <MemoryRouter
        initialEntries={["/handoffs/garden-home"]}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <Routes>
          <Route element={<HandoffConnectionPage />}>
            <Route
              path="/handoffs/:handoffId"
              element={<HandoffCasePage handoffId="garden-home" />}
            />
          </Route>
        </Routes>
      </MemoryRouter>
    </StrictMode>,
  );
}
function expectBusy(message: string) {
  expect(screen.getByRole("status").textContent).toBe(message);
  expect((screen.getByRole("button", { name: "Sign in" }) as HTMLButtonElement).disabled).toBe(
    true,
  );
  expect((screen.getByRole("button", { name: "Try again" }) as HTMLButtonElement).disabled).toBe(
    true,
  );
}
function expectNoPrivateDetails() {
  expect(document.body.textContent).not.toMatch(
    /ApiUsageDenied|private-error-reference|do-not-display|test-session|test-ontology|password/i,
  );
}
beforeEach(() => {
  transport.mockReset();
  harness.auth.mockClear();
  harness.auth.signIn.mockReset();
  harness.auth.signOut.mockReset();
  harness.auth.getTokenOrUndefined.mockReset().mockReturnValue(undefined);
  harness.gateway = exampleGateway().gateway;
  // Real installed Platform SDK getCurrent, with an entirely local HTTP transport.
  harness.client = createClient(
    "https://handoff.test.invalid",
    "ri.ontology.main.ontology.00000000-0000-0000-0000-000000000000",
    harness.auth,
    undefined,
    transport,
  );
  window.history.replaceState({}, "", "/handoffs/garden-home");
});
afterEach(() => {
  cleanup();
  sessionStorage.clear();
});

it("starts sign-in from a real unauthenticated button click and shows a returned failure", async () => {
  transport.mockResolvedValueOnce(signedOut());
  const opening = deferred<Awaited<ReturnType<PublicOauthClient["signIn"]>>>();
  harness.auth.signIn.mockReturnValueOnce(opening.promise);
  open();
  await screen.findByText("Please sign in to return to your units.");
  fireEvent.click(screen.getByRole("button", { name: "Sign in" }));
  expectBusy("Opening sign-in…");
  fireEvent.click(screen.getByRole("button", { name: "Sign in" }));
  await waitFor(() => expect(harness.auth.signIn).toHaveBeenCalledTimes(1));
  expect(harness.auth.signOut).not.toHaveBeenCalled();
  expect(sessionStorage.getItem("handoff.return")).toBe("/handoffs/garden-home");
  await act(async () => opening.reject(new Error("do-not-display")));
  expect(screen.getByRole("alert").textContent).toContain("We couldn’t open sign-in.");
  expect((screen.getByRole("button", { name: "Sign in" }) as HTMLButtonElement).disabled).toBe(
    false,
  );
  expect(transport).toHaveBeenCalledTimes(1);
  expectNoPrivateDetails();
});

it("revokes an already signed-in grant before asking for fresh authorization", async () => {
  harness.auth.getTokenOrUndefined.mockReturnValue("test-session");
  transport.mockResolvedValueOnce(denied());
  const revoking = deferred<void>();
  const opening = deferred<Awaited<ReturnType<PublicOauthClient["signIn"]>>>();
  harness.auth.signOut.mockReturnValueOnce(revoking.promise);
  harness.auth.signIn.mockReturnValueOnce(opening.promise);
  open();
  await screen.findByRole("heading", { name: "Handoff needs access" });
  expect(screen.getByRole("alert").textContent).toContain("You’re signed in");
  fireEvent.click(screen.getByRole("button", { name: "Sign in" }));
  expectBusy("Opening sign-in…");
  await waitFor(() => expect(harness.auth.signOut).toHaveBeenCalledTimes(1));
  expect(harness.auth.signIn).not.toHaveBeenCalled();
  await act(async () => {
    harness.events.dispatchEvent(new Event("signOut"));
    revoking.resolve();
  });
  await waitFor(() => expect(harness.auth.signIn).toHaveBeenCalledTimes(1));
  expectBusy("Opening sign-in…");
  // Refresh/sign-in events during reauthorization must not start another identity read.
  await act(async () => {
    harness.events.dispatchEvent(new Event("refresh"));
    harness.events.dispatchEvent(new Event("signIn"));
  });
  expect(transport).toHaveBeenCalledTimes(1);
  await act(async () => opening.reject(new Error("Unable to redirect")));
  expect(screen.getByRole("alert").textContent).toContain("We couldn’t open sign-in.");
  expectNoPrivateDetails();
});

it("visibly retries the read-only identity check and reports missing app access, without a sign-in loop", async () => {
  harness.auth.getTokenOrUndefined.mockReturnValue("test-session");
  const retry = deferred<Response>();
  transport.mockResolvedValueOnce(denied()).mockReturnValueOnce(retry.promise);
  open();
  await screen.findByRole("heading", { name: "Handoff needs access" });
  fireEvent.click(screen.getByRole("button", { name: "Try again" }));
  expectBusy("Checking your access…");
  fireEvent.click(screen.getByRole("button", { name: "Try again" }));
  await waitFor(() => expect(transport).toHaveBeenCalledTimes(2));
  await act(async () => retry.resolve(denied()));
  expect(screen.getByRole("alert").textContent).toContain(
    "this app doesn’t have the access it needs",
  );
  expect((screen.getByRole("button", { name: "Try again" }) as HTMLButtonElement).disabled).toBe(
    false,
  );
  expect(harness.auth.signIn).not.toHaveBeenCalled();
  expect(harness.auth.signOut).not.toHaveBeenCalled();
  expect(harness.gateway!.list).not.toHaveBeenCalled();
  for (const [input, init] of transport.mock.calls) {
    const request = new Request(input, init);
    expect(new URL(request.url).pathname).toBe("/api/v2/admin/users/getCurrent");
    expect(request.method).toBe("GET");
    expect(request.body).toBeNull();
  }
  expectNoPrivateDetails();
});

it("opens the handoff only after a retry verifies the real current-user response", async () => {
  transport.mockResolvedValueOnce(denied()).mockResolvedValueOnce(response({ id: "morgan" }));
  open();
  await screen.findByRole("heading", { name: "Handoff needs access" });
  expect(screen.queryByRole("button", { name: "Change" })).toBeNull();
  fireEvent.click(screen.getByRole("button", { name: "Try again" }));
  await screen.findByRole("button", { name: "Change" });
  expect(transport).toHaveBeenCalledTimes(2);
  expect(harness.auth.signIn).not.toHaveBeenCalled();
});

it("reports a failed revocation rather than pretending a fresh sign-in began", async () => {
  harness.auth.getTokenOrUndefined.mockReturnValue("test-session");
  transport.mockResolvedValueOnce(denied());
  harness.auth.signOut.mockRejectedValueOnce(new Error("do-not-display"));
  open();
  await screen.findByRole("heading", { name: "Handoff needs access" });
  fireEvent.click(screen.getByRole("button", { name: "Sign in" }));
  await screen.findByText(/We couldn’t open sign-in/);
  expect(harness.auth.signIn).not.toHaveBeenCalled();
  expect((screen.getByRole("button", { name: "Try again" }) as HTMLButtonElement).disabled).toBe(
    false,
  );
  expectNoPrivateDetails();
});

it("reports a connection interruption separately from permission or password problems", async () => {
  transport.mockRejectedValueOnce(new TypeError("do-not-display"));
  open();
  await screen.findByText(/We couldn’t check your access/);
  expect(screen.queryByText(/You’re signed in/)).toBeNull();
  expectNoPrivateDetails();
});
