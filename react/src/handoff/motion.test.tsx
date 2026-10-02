// @vitest-environment jsdom
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { act, cleanup, render, renderHook, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HandoffCasePage } from "./App";
import {
  acceptWork,
  exampleGateway,
  exampleWorkspace,
  memoryStorage,
} from "./examples.test-support";
import { HandoffContext } from "./hooks";
import { pollDelay, replyExpected } from "./model";
import { ARRIVAL_MS, TRANSIENT_MS, useArrivals, useAutoDismiss } from "./motion";
import { HandoffStore, ReadResource } from "./state";

const NOW = Date.parse("2026-09-28T05:00:00Z");
const stores: HandoffStore[] = [];
afterEach(() => {
  cleanup();
  stores.forEach((s) => s.dispose());
  stores.length = 0;
  vi.useRealTimers();
});

describe("reading at the pace of the work", () => {
  it("reads every 2 s when a step is due or a reply is expected, 15 s while vendors work", () => {
    const data = acceptWork(exampleWorkspace());
    data.agent = { status: "Ready to continue", nextStep: "", updatedAt: "", nextWakeAt: null };
    expect(pollDelay(data, 7000, NOW)).toBe(2000);
    data.agent.nextWakeAt = new Date(NOW + 30_000).toISOString();
    expect(pollDelay(data, 7000, NOW)).toBe(2000);
    data.agent = {
      status: "Waiting for provider",
      nextStep: "",
      updatedAt: "",
      nextWakeAt: new Date(NOW + 3_600_000).toISOString(),
    };
    expect(pollDelay(data, 7000, NOW)).toBe(15_000);
    data.messages.push({
      id: "mine",
      title: "Owen to Handoff",
      body: "When is the next visit?",
      recipientPartyId: null,
      direction: "Operator",
      purpose: "Discussion",
      jobId: null,
      replyToMessageId: null,
      status: "Received",
      createdAt: "2030-01-01T00:00:00Z",
    });
    expect(replyExpected(data)).toBe(true);
    expect(pollDelay(data, 7000, NOW)).toBe(2000);
    expect(pollDelay(undefined, 7000, NOW)).toBe(7000);
  });
  it("follows the interval the data asks for and pauses while the tab is hidden", async () => {
    vi.useFakeTimers();
    const read = vi.fn(async () => "value");
    const resource = new ReadResource(read, undefined, () => 2000);
    const stop = resource.subscribe(() => {});
    await vi.advanceTimersByTimeAsync(0);
    expect(read).toHaveBeenCalledTimes(1);
    await vi.advanceTimersByTimeAsync(2000);
    expect(read).toHaveBeenCalledTimes(2);
    const visibility = vi.spyOn(document, "visibilityState", "get").mockReturnValue("hidden");
    await vi.advanceTimersByTimeAsync(10_000);
    expect(read).toHaveBeenCalledTimes(2);
    visibility.mockReturnValue("visible");
    document.dispatchEvent(new Event("visibilitychange"));
    await vi.advanceTimersByTimeAsync(0);
    expect(read).toHaveBeenCalledTimes(3);
    stop();
  });
});

describe("arrivals", () => {
  it("marks nothing on first load, then marks a new key until the highlight ends", async () => {
    vi.useFakeTimers();
    const { result, rerender } = renderHook(({ keys }) => useArrivals(keys), {
      initialProps: { keys: ["a", "b"] },
    });
    expect(result.current.size).toBe(0);
    rerender({ keys: ["a", "b", "c"] });
    expect([...result.current]).toEqual(["c"]);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(ARRIVAL_MS);
    });
    expect(result.current.size).toBe(0);
  });
});

function renderCase(data = acceptWork(exampleWorkspace())) {
  const { gateway, state } = exampleGateway(data);
  const store = new HandoffStore(gateway, memoryStorage(), "motion", 0);
  stores.push(store);
  render(
    <MemoryRouter initialEntries={["/handoffs/garden-home"]}>
      <HandoffContext.Provider value={store}>
        <Routes>
          <Route path="/handoffs/:id" element={<HandoffCasePage handoffId="garden-home" />} />
        </Routes>
      </HandoffContext.Provider>
    </MemoryRouter>,
  );
  return { store, state };
}

describe("live case page", () => {
  it("shows Handoff typing under a message it hasn't answered, then the saved reply", async () => {
    const data = acceptWork(exampleWorkspace());
    data.messages.push({
      id: "mine",
      title: "Owen to Handoff",
      body: "When is the next visit?",
      recipientPartyId: null,
      direction: "Operator",
      purpose: "Discussion",
      jobId: null,
      replyToMessageId: null,
      status: "Received",
      createdAt: "2030-01-01T00:00:00Z",
    });
    const { store, state } = renderCase(data);
    expect(await screen.findByText("Handoff is replying")).toBeTruthy();
    expect(screen.getByText(/· Sent/)).toBeTruthy();
    state.data.messages.push({
      id: "reply",
      title: "Handoff",
      body: "Oak Repairs visits on Monday.",
      recipientPartyId: null,
      direction: "Handoff",
      purpose: "Discussion",
      jobId: null,
      replyToMessageId: "mine",
      status: "Sent",
      createdAt: "2030-01-01T00:01:00Z",
    });
    await act(() => store.workspace("garden-home").fresh());
    expect(screen.getByText("Oak Repairs visits on Monday.")).toBeTruthy();
    expect(screen.queryByText("Handoff is replying")).toBeNull();
  });
  it("names a new step in a toast and marks the Timeline tab while you're elsewhere", async () => {
    const { store, state } = renderCase();
    await screen.findByText("Accepted plan");
    expect(screen.queryByText("Oak Repairs booked the visit for Monday, September 28.")).toBeNull();
    state.data.activity.push({
      id: "booked",
      title: "Handoff progressed",
      detail: "Oak Repairs booked the visit for Monday, September 28.",
      at: "2026-09-23T09:00:00Z",
    });
    await act(() => store.workspace("garden-home").fresh());
    expect(screen.getByText("Oak Repairs booked the visit for Monday, September 28.")).toBeTruthy();
    expect(screen.getByRole("tab", { name: /^Timeline/ }).querySelector(".tab-dot")).toBeTruthy();
  });
});

describe("transient messages", () => {
  it("close after the wait, not while held, and restart the wait when released", () => {
    vi.useFakeTimers();
    const onDismiss = vi.fn();
    const { result } = renderHook(() => useAutoDismiss("Your change was saved.", onDismiss));
    act(() => vi.advanceTimersByTime(TRANSIENT_MS - 1000));
    act(() => result.current.onMouseEnter());
    act(() => vi.advanceTimersByTime(TRANSIENT_MS * 2));
    expect(onDismiss).not.toHaveBeenCalled();
    act(() => result.current.onMouseLeave());
    act(() => vi.advanceTimersByTime(TRANSIENT_MS - 1));
    expect(onDismiss).not.toHaveBeenCalled();
    act(() => vi.advanceTimersByTime(1));
    expect(onDismiss).toHaveBeenCalledTimes(1);
    vi.useRealTimers();
  });
});
