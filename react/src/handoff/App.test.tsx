// @vitest-environment jsdom
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HandoffCasePage, HandoffLayout, HandoffListPage } from "./App";
import { type ApplyResult, HandoffError, type HandoffWorkspace } from "./contracts";
import {
  acceptWork,
  deferred,
  exampleGateway,
  exampleWorkspace,
  memoryStorage,
  savedChange,
} from "./examples.test-support";
import { HandoffContext } from "./hooks";
import { HandoffStore } from "./state";

const stores: HandoffStore[] = [];
afterEach(() => {
  cleanup();
  stores.forEach((s) => s.dispose());
  stores.length = 0;
  vi.restoreAllMocks();
});
function setup({ list = false, data = exampleWorkspace(), interval = 0 } = {}) {
  const { gateway, state, recordChange } = exampleGateway(data);
  const storage = memoryStorage();
  const store = new HandoffStore(gateway, storage, "test", interval);
  stores.push(store);
  const view = renderApp(store, list);
  return { gateway, state, store, storage, recordChange, ...view };
}
function renderApp(store: HandoffStore, list = false) {
  return render(
    <MemoryRouter
      initialEntries={[list ? "/" : "/handoffs/garden-home"]}
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <HandoffContext.Provider value={store}>
        <Routes>
          <Route element={<HandoffLayout />}>
            <Route path="/" element={<HandoffListPage />} />
            <Route path="/handoffs/:id" element={<HandoffCasePage handoffId="garden-home" />} />
          </Route>
        </Routes>
      </HandoffContext.Provider>
    </MemoryRouter>,
  );
}
const button = (name: string | RegExp) => screen.getByRole("button", { name }) as HTMLButtonElement;
const acceptButton = () => button(/^Accept(ing| plan)/);
async function loaded() {
  await screen.findByRole("heading", { name: "Repair the kitchen wall and door handle" });
}

describe("Units list and unit page", () => {
  it.each([
    { list: true, kind: "unavailable" as const },
    { list: false, kind: "unavailable" as const },
    { list: true, kind: "permission" as const },
    { list: false, kind: "permission" as const },
  ])("distinguishes $kind on the read notice with list=$list", async ({ list, kind }) => {
    const { gateway } = exampleGateway();
    vi.mocked(gateway.list).mockRejectedValue(new HandoffError(kind));
    vi.mocked(gateway.workspace).mockRejectedValue(new HandoffError(kind));
    const store = new HandoffStore(gateway, memoryStorage(), "read-notice", 0);
    stores.push(store);
    renderApp(store, list);
    const notice = await screen.findByRole("alert");
    expect(notice.textContent).toContain(
      kind === "unavailable" ? "Handoff can’t connect right now" : "You don’t have access",
    );
    if (kind === "unavailable") {
      expect(notice.textContent).not.toMatch(/access|permission|sign in/i);
    }
    expect(notice.textContent).not.toMatch(/QueryNotFound|QueryVersionNotFound|apiName|token/);
    vi.mocked(gateway.list).mockResolvedValue({
      version: "2",
      workspace: exampleWorkspace().workspace,
      handoffs: [],
    });
    vi.mocked(gateway.workspace).mockResolvedValue(exampleWorkspace());
    fireEvent.click(within(notice).getByRole("button", { name: "Try again" }));
    await waitFor(() => expect(screen.queryByRole("alert")).toBeNull());
  });
  it("lists units that need a decision first, with readiness and what's next", async () => {
    const { container } = setup({ list: true });
    const link = await screen.findByRole("link", { name: "Garden home" });
    expect(screen.getByText("1 unit needs your decision")).toBeTruthy();
    const row = link.closest("tr")!;
    expect(row.textContent).toContain("Ready for your decision");
    expect(row.textContent).not.toContain("Final settlement not yet prepared");
    expect(row.textContent).toContain("Review the work plan");
    expect(screen.queryByText(/demo/i)).toBeNull();
    expect(container.textContent).not.toMatch(
      /phase|prototype|fixture|constructed|bootstrap|simulat|revision|commandId|work-garden|media-set/i,
    );
    fireEvent.click(link);
    await loaded();
  });
  it("opens on the decision with values, and keeps reasons and background closed", async () => {
    const data = exampleWorkspace();
    data.property.description = "DESCRIPTION_NARRATIVE";
    const { container, gateway } = setup({ data });
    await loaded();
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("Garden home");
    expect(screen.getByText("Needs your decision")).toBeTruthy();
    const tracks = container.querySelector(".tracks")!;
    expect(tracks.textContent).toContain("Ready for your decision");
    expect(tracks.textContent).not.toContain("Final settlement");
    expect(screen.getByText("Work total").closest("tr")?.textContent).toContain("£875.00");
    expect(screen.getByText("Budget for this plan").closest("tr")?.textContent).toContain(
      "£1,000.00",
    );
    expect(
      screen.getByText("Retain the existing fittings where they are sound").closest("li"),
    ).toBeTruthy();
    expect(screen.getByText("Why this plan").closest("details")?.open).toBe(false);
    expect(screen.queryByText("DESCRIPTION_NARRATIVE")).toBeNull();
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(gateway.apply).not.toHaveBeenCalled();
    expect(gateway.document).not.toHaveBeenCalled();
  });
  it("validates a budget change, saves it, then accepts without extra dialogs", async () => {
    const { gateway, state, recordChange } = setup();
    await loaded();
    fireEvent.click(button("Change"));
    const input = screen.getByLabelText("Budget (GBP)") as HTMLInputElement;
    expect(input.value).toBe("1000.00");
    expect(screen.queryByRole("button", { name: /^Accept plan/ })).toBeNull();
    fireEvent.change(input, { target: { value: "800" } });
    expect(screen.getByRole("alert").textContent).toBe("The budget must cover the work.");
    expect(button("Save changes").disabled).toBe(true);
    fireEvent.change(input, { target: { value: "1000000.01" } });
    expect(screen.getByRole("alert").textContent).toBe("Enter a budget of £1,000,000.00 or less.");
    expect(button("Save changes").disabled).toBe(true);
    fireEvent.change(input, { target: { value: "1100.50" } });
    expect(button("Save changes").disabled).toBe(false);
    vi.mocked(gateway.apply).mockImplementationOnce(async (change) => {
      if (change.kind !== "budget") {
        throw new Error("Expected budget change");
      }
      state.data.workPlan!.budgetCents = change.budgetCents;
      state.data.workPlan!.revision = "3";
      await recordChange(change);
      return "saved";
    });
    fireEvent.click(button("Save changes"));
    await screen.findByText("Your change was saved.");
    expect(vi.mocked(gateway.apply).mock.calls[0][0]).toMatchObject({
      kind: "budget",
      workPlanId: "work-garden",
      expectedRevision: "2",
      budgetCents: "110050",
    });
    expect(screen.queryByLabelText("Budget (GBP)")).toBeNull();
    await waitFor(() => expect(acceptButton().disabled).toBe(false));
    expect(acceptButton().textContent).toContain("£1,100.50");
    vi.mocked(gateway.apply).mockImplementationOnce(async (change) => {
      state.data = acceptWork(state.data);
      await recordChange(change);
      return "saved";
    });
    fireEvent.click(acceptButton());
    await screen.findByText("Accepted plan");
    expect(screen.getByText(/Accepted by Morgan Lee/).textContent).toContain("£1,100.50");
    expect(gateway.apply).toHaveBeenCalledTimes(2);
    expect(screen.queryByRole("dialog")).toBeNull();
  });
  it("does not show acceptance before the confirming read, and blocks double clicks", async () => {
    const { gateway, state } = setup();
    await loaded();
    const sent = deferred<ApplyResult>();
    const result = deferred<HandoffWorkspace>();
    vi.mocked(gateway.apply).mockImplementationOnce(async (change) => {
      const response = await sent.promise;
      state.receipts.set(change.commandId, await savedChange(change, acceptWork(state.data)));
      return response;
    });
    fireEvent.click(acceptButton());
    fireEvent.click(acceptButton());
    expect(acceptButton().disabled).toBe(true);
    await waitFor(() => expect(gateway.apply).toHaveBeenCalledTimes(1));
    vi.mocked(gateway.workspace).mockReturnValueOnce(result.promise);
    await act(async () => {
      sent.resolve("saved");
    });
    expect(await screen.findByText("Checking your change")).toBeTruthy();
    expect(screen.queryByText("Accepted plan")).toBeNull();
    await act(async () => {
      state.data = acceptWork(state.data);
      result.resolve(state.data);
    });
    await screen.findByText("Accepted plan");
  });
  it("keeps an uncertain change across reload and checks instead of sending again", async () => {
    const { gateway, state, store, storage, recordChange, unmount } = setup();
    await loaded();
    vi.mocked(gateway.apply).mockRejectedValueOnce(new Error("connection lost"));
    fireEvent.click(acceptButton());
    await screen.findByText("Checking your change");
    const original = store.pending("garden-home")!.change!;
    unmount();
    store.dispose();
    const restored = new HandoffStore(gateway, storage, "test", 0);
    stores.push(restored);
    renderApp(restored);
    await loaded();
    expect(restored.pending("garden-home")?.reference.commandId).toBe(original.commandId);
    expect(acceptButton().disabled).toBe(true);
    state.data = acceptWork(state.data);
    await recordChange(original);
    fireEvent.click(button("Check again"));
    await screen.findByText("Accepted plan");
    expect(gateway.apply).toHaveBeenCalledTimes(1);
  });
  it.each([new Error("query name and private details"), new HandoffError("unavailable")])(
    "keeps a budget edit on read failure (%s) and asks for review when the plan changes",
    async (error) => {
      const { gateway, state, store } = setup();
      await loaded();
      fireEvent.click(button("Change"));
      fireEvent.change(screen.getByLabelText("Budget (GBP)"), { target: { value: "1095.25" } });
      vi.mocked(gateway.workspace).mockRejectedValueOnce(error);
      await act(async () => {
        await store.workspace("garden-home").fresh();
      });
      const notice = screen
        .getAllByRole("alert")
        .find((a) => a.textContent?.includes("edits are kept"));
      expect(notice?.textContent).not.toContain("private details");
      expect((screen.getByLabelText("Budget (GBP)") as HTMLInputElement).value).toBe("1095.25");
      expect(button("Save changes").disabled).toBe(true);
      state.data.workPlan!.revision = "3";
      await act(async () => {
        await store.workspace("garden-home").fresh();
      });
      expect(screen.getByText(/plan changed while you were editing/)).toBeTruthy();
      expect(button("Save changes").disabled).toBe(true);
      fireEvent.click(button("I’ve reviewed the updated plan"));
      expect(button("Save changes").disabled).toBe(false);
      expect(gateway.apply).not.toHaveBeenCalled();
    },
  );
  it("keeps controls steady during a background refresh; the saved revision still guards the change", async () => {
    const { gateway, store, state } = setup();
    await loaded();
    fireEvent.click(button("Change"));
    fireEvent.change(screen.getByLabelText("Budget (GBP)"), { target: { value: "1200.50" } });
    const read = deferred<HandoffWorkspace>();
    vi.mocked(gateway.workspace).mockReturnValueOnce(read.promise);
    let refresh!: Promise<void>;
    act(() => {
      refresh = store.workspace(state.data.handoff.id).fresh();
    });
    // A refresh does not grey out or disable anything the operator can use.
    expect(button("Save changes").disabled).toBe(false);
    fireEvent.click(button("Save changes"));
    await waitFor(() => expect(gateway.apply).toHaveBeenCalledTimes(1));
    expect(vi.mocked(gateway.apply).mock.calls[0]![0]).toMatchObject({
      expectedRevision: state.data.workPlan!.revision,
    });
    await act(async () => {
      read.resolve(structuredClone(state.data));
      await refresh;
    });
  });
  it("handles loading, a plan still being prepared, and no units, without invented amounts", async () => {
    const { gateway } = exampleGateway();
    const loading = deferred<HandoffWorkspace>();
    vi.mocked(gateway.workspace).mockReturnValue(loading.promise);
    const store = new HandoffStore(gateway, memoryStorage(), "loading", 0);
    stores.push(store);
    renderApp(store);
    expect(await screen.findByText("Loading…")).toBeTruthy();
    expect(screen.queryByText(/£0/)).toBeNull();
    const data = exampleWorkspace();
    data.workPlan = null;
    data.handoff.physicalProgress = "Preparing plan";
    data.agent.status = "Reviewing the survey";
    await act(async () => {
      loading.resolve(data);
    });
    expect(await screen.findByText("Reviewing the survey")).toBeTruthy();
    expect(screen.queryByRole("button", { name: /^Accept plan/ })).toBeNull();
    expect(screen.queryByText(/£0/)).toBeNull();
    cleanup();
    const empty = exampleGateway();
    vi.mocked(empty.gateway.list).mockResolvedValue({
      version: "2",
      workspace: data.workspace,
      handoffs: [],
    });
    const emptyStore = new HandoffStore(empty.gateway, memoryStorage(), "empty", 0);
    stores.push(emptyStore);
    renderApp(emptyStore, true);
    expect(await screen.findByRole("heading", { name: "No move-outs in progress" })).toBeTruthy();
  });
  it("shows saved messages and activity as background reads arrive", async () => {
    const { state, gateway } = setup({ data: acceptWork(exampleWorkspace()), interval: 35 });
    await screen.findByText("Accepted plan");
    fireEvent.click(screen.getByRole("tab", { name: /^Messages/ }));
    expect(screen.getByText("No messages yet.")).toBeTruthy();
    state.data.messages.push({
      id: "message-saved",
      title: "Visit requested",
      body: "Please suggest a time for the approved repairs.",
      recipientPartyId: "provider",
      direction: "Outgoing",
      purpose: "Correspondence",
      jobId: null,
      replyToMessageId: null,
      status: "Sent",
      createdAt: "2026-09-22T11:00:00Z",
    });
    state.data.activity.push({
      id: "activity-saved",
      title: "Vendor contacted",
      detail: "Oak Repairs has received the request.",
      at: "2026-09-22T11:00:00Z",
    });
    expect(
      (await screen.findAllByText("Please suggest a time for the approved repairs.")).length,
    ).toBeGreaterThan(0);
    expect(screen.getByRole("heading", { name: "Oak Repairs" })).toBeTruthy();
    fireEvent.click(screen.getByRole("tab", { name: /^Timeline/ }));
    expect(await screen.findByText("Vendor contacted")).toBeTruthy();
    expect(gateway.apply).not.toHaveBeenCalled();
  });
  it("lets a work user message Handoff without decision access or implying acceptance", async () => {
    const data = exampleWorkspace();
    data.permissions.canDecide = false;
    const { gateway, state, recordChange } = setup({ data });
    await loaded();
    expect(screen.queryByRole("button", { name: /^Accept plan/ })).toBeNull();
    expect(screen.queryByRole("button", { name: "Change" })).toBeNull();
    expect(screen.getByText("Someone with approval access decides this plan.")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("Message Handoff"), {
      target: { value: "Can we preserve the door finish?" },
    });
    vi.mocked(gateway.apply).mockImplementationOnce(async (change) => {
      if (change.kind !== "message") {
        throw new Error("Expected message");
      }
      state.data.handoff.revision = "9";
      state.data.messages.push({
        id: "discussion",
        title: "Morgan to Handoff",
        body: change.message,
        direction: "Operator",
        purpose: "Discussion",
        status: "Received",
        createdAt: "2026-09-22T13:00:00Z",
        recipientPartyId: null,
        replyToMessageId: null,
        jobId: null,
      });
      await recordChange(change);
      return "saved";
    });
    fireEvent.click(button("Send"));
    await screen.findByText(
      "Your message is saved. Handoff will consider it with the current work.",
    );
    expect(screen.getByText("Can we preserve the door finish?")).toBeTruthy();
    expect((screen.getByLabelText("Message Handoff") as HTMLTextAreaElement).value).toBe("");
    expect(state.data.workPlan?.acceptedDecisionId).toBeNull();
  });
  it("does not send a message written for an older plan without review", async () => {
    const { gateway, state, store } = setup();
    await loaded();
    fireEvent.change(screen.getByLabelText("Message Handoff"), {
      target: { value: "Use the same materials" },
    });
    state.data.workPlan!.revision = "3";
    await act(async () => {
      await store.workspace(state.data.handoff.id).fresh();
    });
    expect(screen.queryByRole("button", { name: "Send" })).toBeNull();
    fireEvent.click(button("I’ve reviewed it"));
    expect(button("Send").disabled).toBe(false);
    expect(gateway.apply).not.toHaveBeenCalled();
  });
  it("shows decision controls to a decision maker without work permission", async () => {
    const data = exampleWorkspace();
    data.permissions.canWork = false;
    setup({ data });
    await loaded();
    expect(button("Change")).toBeTruthy();
    expect(acceptButton().disabled).toBe(false);
  });
  it("does not expose a sign-in identifier as a person's name", async () => {
    const data = acceptWork(exampleWorkspace());
    const actor = "123e4567-e89b-12d3-a456-426614174000";
    data.decisions[0].by = actor;
    const { container } = setup({ data });
    await screen.findByText("Accepted plan");
    expect(container.textContent).not.toContain(actor);
    expect(screen.getByText(/Accepted by A team member/)).toBeTruthy();
  });
});
