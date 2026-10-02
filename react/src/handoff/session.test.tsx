// @vitest-environment jsdom
import { useSyncExternalStore } from "react";
import { MemoryRouter } from "react-router-dom";
import type { PublicOauthClient } from "@osdk/oauth";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import { HandoffCasePage } from "./App";
import { exampleGateway, memoryStorage } from "./examples.test-support";
import { HandoffContext } from "./hooks";
import { takeReturnRoute } from "./returnRoute";
import { HandoffSession } from "./session";
import { HandoffStore } from "./state";

const stores: HandoffStore[] = [];
afterEach(() => {
  cleanup();
  stores.forEach((store) => store.dispose());
  stores.length = 0;
  sessionStorage.clear();
});
function TestSession({ session }: { session: HandoffSession }) {
  const state = useSyncExternalStore(session.subscribe, session.getSnapshot);
  return state.store ? (
    <HandoffContext.Provider value={state.store}>
      <HandoffCasePage handoffId="garden-home" />
    </HandoffContext.Provider>
  ) : (
    <p role="status">Opening your work…</p>
  );
}
function setup() {
  const events = new EventTarget();
  const auth = Object.assign(async () => "token", {
    addEventListener: events.addEventListener.bind(events),
    removeEventListener: events.removeEventListener.bind(events),
    getTokenOrUndefined: () => "token",
    signIn: vi.fn(),
    signOut: vi.fn(),
    refresh: vi.fn(),
  }) as PublicOauthClient;
  const currentUser = vi.fn(async () => "morgan");
  const storage = memoryStorage();
  const { gateway } = exampleGateway();
  const create = vi.fn((user: string) => {
    const store = new HandoffStore(gateway, storage, `changes:${user}`, 0);
    stores.push(store);
    return store;
  });
  const session = new HandoffSession(auth, currentUser, create);
  render(
    <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <TestSession session={session} />
    </MemoryRouter>,
  );
  return { auth, events, currentUser, session, create, storage, gateway };
}
it("preserves an operator’s visible budget draft across a normal OAuth refresh", async () => {
  const { events, currentUser, create } = setup();
  await screen.findByRole("button", { name: "Change" });
  fireEvent.click(screen.getByRole("button", { name: "Change" }));
  fireEvent.change(screen.getByLabelText("Budget (GBP)"), { target: { value: "1120.55" } });
  await act(async () => {
    events.dispatchEvent(new Event("refresh"));
  });
  await waitFor(() => expect(currentUser).toHaveBeenCalledTimes(2));
  expect(create).toHaveBeenCalledTimes(1);
  expect((screen.getByLabelText("Budget (GBP)") as HTMLInputElement).value).toBe("1120.55");
});
it("isolates local work when the signed-in person changes", async () => {
  const { events, currentUser, create } = setup();
  await screen.findByRole("button", { name: "Change" });
  fireEvent.click(screen.getByRole("button", { name: "Change" }));
  fireEvent.change(screen.getByLabelText("Budget (GBP)"), { target: { value: "1120.55" } });
  currentUser.mockResolvedValue("jules");
  await act(async () => {
    events.dispatchEvent(new Event("signIn"));
  });
  await screen.findByRole("button", { name: "Change" });
  expect(create).toHaveBeenCalledTimes(2);
  expect(screen.queryByLabelText("Budget (GBP)")).toBeNull();
});
it("keeps only recovery references on sign-out and isolates them from the next person", async () => {
  const { events, currentUser, session, gateway, storage } = setup();
  await screen.findByRole("button", { name: "Change" });
  const first = session.getSnapshot().store!;
  const data = first.workspace("garden-home").getSnapshot().data!;
  vi.mocked(gateway.apply).mockRejectedValueOnce(new Error("response lost"));
  await act(async () => {
    await first.submit(data, "accept");
  });
  const reference = first.pending("garden-home")!.reference;
  const saved = storage.getItem("changes:morgan");
  await act(async () => {
    events.dispatchEvent(new Event("signOut"));
  });
  expect(first.pending("garden-home")).toBeUndefined();
  expect(storage.getItem("changes:morgan")).toBe(saved);
  currentUser.mockResolvedValue("jules");
  await act(async () => {
    events.dispatchEvent(new Event("signIn"));
  });
  await screen.findByRole("button", { name: "Change" });
  expect(session.getSnapshot().store!.pending("garden-home")).toBeUndefined();
  currentUser.mockResolvedValue("morgan");
  await act(async () => {
    events.dispatchEvent(new Event("signIn"));
  });
  await screen.findByText("Checking your change");
  const recovered = session.getSnapshot().store!.pending("garden-home")!;
  expect(recovered.reference).toEqual(reference);
  expect(recovered.change).toBeUndefined();
  expect(gateway.apply).toHaveBeenCalledTimes(1);
});
it("retains only scoped recovery references when an explicit fresh sign-in fails", async () => {
  const { auth, session, gateway, storage, currentUser } = setup();
  await screen.findByRole("button", { name: "Change" });
  const first = session.getSnapshot().store!;
  const data = first.workspace("garden-home").getSnapshot().data!;
  vi.mocked(gateway.apply).mockRejectedValueOnce(new Error("response lost"));
  await act(async () => {
    await first.submit(data, "accept");
  });
  const reference = first.pending("garden-home")!.reference;
  const saved = storage.getItem("changes:morgan");
  vi.mocked(auth.signIn).mockRejectedValueOnce(new Error("Unable to redirect"));
  await act(async () => {
    await session.signIn();
  });
  expect(session.getSnapshot().failure).toBe("sign-in-failed");
  expect(session.getSnapshot().store).toBeUndefined();
  expect(first.pending("garden-home")).toBeUndefined();
  expect(storage.getItem("changes:morgan")).toBe(saved);
  currentUser.mockResolvedValue("jules");
  await act(async () => {
    await session.verify();
  });
  expect(session.getSnapshot().store!.pending("garden-home")).toBeUndefined();
  currentUser.mockResolvedValue("morgan");
  await act(async () => {
    await session.verify();
  });
  const recovered = session.getSnapshot().store!.pending("garden-home")!;
  expect(recovered.reference).toEqual(reference);
  expect(recovered.change).toBeUndefined();
  expect(gateway.apply).toHaveBeenCalledTimes(1);
});
it("ignores a late identity response after sign-out and another person’s sign-in", async () => {
  const { events, currentUser, session, create } = setup();
  await screen.findByRole("button", { name: "Change" });
  let finish!: (user: string) => void;
  currentUser.mockReturnValueOnce(
    new Promise((resolve) => {
      finish = resolve;
    }),
  );
  let earlier!: Promise<void>;
  await act(async () => {
    earlier = session.verify();
  });
  await act(async () => {
    events.dispatchEvent(new Event("signOut"));
    currentUser.mockResolvedValue("jules");
    events.dispatchEvent(new Event("signIn"));
  });
  await screen.findByRole("button", { name: "Change" });
  const second = session.getSnapshot().store;
  await act(async () => {
    finish("morgan");
    await earlier;
  });
  expect(session.getSnapshot().store).toBe(second);
  expect(create.mock.calls.map(([user]) => user)).toEqual(["morgan", "jules"]);
});
it("returns to a handoff after sign-in but never follows an external return address", () => {
  sessionStorage.setItem("handoff.return", "/handoffs/garden-home");
  expect(takeReturnRoute()).toBe("/handoffs/garden-home");
  expect(takeReturnRoute()).toBe("/");
  sessionStorage.setItem("handoff.return", "//other.example");
  expect(takeReturnRoute()).toBe("/");
});
