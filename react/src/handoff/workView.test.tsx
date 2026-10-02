// @vitest-environment jsdom
import { MemoryRouter } from "react-router-dom";
import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HandoffCasePage } from "./App";
import { HandoffError } from "./contracts";
import { deferred, exampleGateway, memoryStorage } from "./examples.test-support";
import { HandoffContext } from "./hooks";
import { HandoffStore } from "./state";
import { workExample } from "./work.test-support";

const stores: HandoffStore[] = [];
afterEach(() => {
  cleanup();
  stores.forEach((s) => s.dispose());
  stores.length = 0;
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});
function setup(data = workExample()) {
  const mock = exampleGateway(data),
    store = new HandoffStore(mock.gateway, memoryStorage(), "view", 0);
  stores.push(store);
  const view = render(
    <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <HandoffContext.Provider value={store}>
        <HandoffCasePage handoffId={data.handoff.id} />
      </HandoffContext.Provider>
    </MemoryRouter>,
  );
  return { ...mock, store, ...view };
}
async function loaded() {
  await screen.findByRole("heading", { name: "Repair the kitchen wall and door handle" });
}
const button = (name: string | RegExp) => screen.getByRole("button", { name }) as HTMLButtonElement;
const checkbox = (name: string | RegExp) =>
  screen.getByRole("checkbox", { name }) as HTMLInputElement;

describe("Work, money and the plan decision", () => {
  it("keeps the accepted assessment, the new proposal, delivery facts and accounting distinct", async () => {
    const { gateway, container } = setup();
    await loaded();
    expect(screen.getByText("Accepted plan")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Assess the wall and handle" })).toBeTruthy();
    const work = screen.getByRole("region", { name: "Work" });
    expect(work.textContent).toContain("Condition assessment");
    expect(within(work).getByText("Concealed pipework not examined")).toBeTruthy();
    expect(work.textContent).toContain("not checked");
    expect(work.textContent).not.toContain("payer");
    expect(work.textContent).toMatch(/£80\.00.*Payment (requested|not yet confirmed)/);
    expect(work.textContent).not.toMatch(/Paid £80/);
    const money = screen.getByRole("region", { name: "Owner funds" });
    expect(money.textContent).toContain("£1,000.00");
    expect(money.textContent).toContain("£920.00");
    expect(container.querySelector(".tracks")?.textContent).not.toContain(
      "Tenant account remains open",
    );
    expect(button(/^Accept plan/).disabled).toBe(false);
    expect(gateway.apply).not.toHaveBeenCalled();
    expect(container.textContent).not.toMatch(
      /decision-saved|assessment-job|offer-oak|quoteLineId|commandId|payloadHash/,
    );
  });
  it("sends removed work and an added requirement as one plan change", async () => {
    const { state, gateway, recordChange } = setup();
    await loaded();
    fireEvent.click(button("Change"));
    fireEvent.click(checkbox(/Refit handle/));
    fireEvent.change(screen.getByLabelText("New requirement"), {
      target: { value: "Protect the floor" },
    });
    fireEvent.click(button("Add"));
    expect(screen.getByText("Work total £800.00")).toBeTruthy();
    vi.mocked(gateway.apply).mockImplementationOnce(async (change) => {
      if (change.kind !== "plan") {
        throw new Error("Expected plan change");
      }
      Object.assign(state.data.workPlan!, change.changes, {
        revision: "2",
        estimatedCostCents: "80000",
      });
      await recordChange(change);
      return "saved";
    });
    fireEvent.click(button("Save changes"));
    await screen.findByText("Your change was saved.");
    expect(vi.mocked(gateway.apply).mock.calls[0][0]).toMatchObject({
      kind: "plan",
      workPlanId: "repair-proposal",
      expectedRevision: "1",
      changes: {
        budgetCents: "100000",
        fixedRequirements: [
          "Retain the existing fittings where they are sound",
          "Protect the floor",
        ],
        selections: [{ quoteId: "offer-oak", quoteLineId: "wall" }],
      },
    });
    expect(state.data.workPlan!.acceptedDecisionId).toBeNull();
    expect(state.data.decisions[0].content.scope).toEqual(["Inspect the wall and handle"]);
  });
  it("keeps a tracked budget in step with the selected work", async () => {
    const data = workExample();
    data.workPlan!.budgetCents = data.workPlan!.estimatedCostCents;
    setup(data);
    await loaded();
    fireEvent.click(button("Change"));
    fireEvent.click(checkbox(/Refit handle/));
    expect((screen.getByLabelText("Budget (GBP)") as HTMLInputElement).value).toBe("800.00");
  });
  it("asks for another look when the plan changes during an edit", async () => {
    const { state, store, gateway } = setup();
    await loaded();
    fireEvent.click(button("Change"));
    fireEvent.click(checkbox(/Refit handle/));
    state.data.workPlan!.revision = "2";
    await act(async () => {
      await store.workspace(state.data.handoff.id).fresh();
    });
    expect(button("Save changes").disabled).toBe(true);
    expect(screen.queryByRole("button", { name: /^Accept plan/ })).toBeNull();
    expect(checkbox(/Refit handle/).checked).toBe(false);
    fireEvent.click(button("I’ve reviewed the updated plan"));
    expect(button("Save changes").disabled).toBe(false);
    expect(gateway.apply).not.toHaveBeenCalled();
  });
  it("keeps an unsaved edit visible, and blocks saving, when a new plan replaces the old one", async () => {
    const { state, store, gateway } = setup();
    await loaded();
    fireEvent.click(button("Change"));
    fireEvent.click(checkbox(/Refit handle/));
    state.data.workPlan = { ...state.data.workPlan!, id: "replacement-proposal" };
    await act(async () => {
      await store.workspace(state.data.handoff.id).fresh();
    });
    expect(checkbox(/Refit handle/).checked).toBe(false);
    expect(button("Save changes").disabled).toBe(true);
    expect(gateway.apply).not.toHaveBeenCalled();
  });
  it("cancels an edit without saving anything", async () => {
    const { gateway } = setup();
    await loaded();
    fireEvent.click(button("Change"));
    fireEvent.click(button("Cancel"));
    expect(screen.queryByLabelText("Budget (GBP)")).toBeNull();
    expect(button(/^Accept plan/)).toBeTruthy();
    expect(gateway.apply).not.toHaveBeenCalled();
  });
});

describe("Opening files", () => {
  function fileHandles() {
    const create = vi.fn(() => "blob:original"),
      revoke = vi.fn();
    vi.stubGlobal(
      "URL",
      class extends URL {
        static createObjectURL = create;
        static revokeObjectURL = revoke;
      },
    );
    return { create, revoke };
  }
  async function openQuote() {
    fireEvent.click(screen.getByRole("tab", { name: /^Money/ }));
    fireEvent.click(
      within(screen.getByRole("region", { name: /^Quotes/ })).getByRole("button", {
        name: /^Oak Repairs quote/,
      }),
    );
    return screen.findByRole("region", { name: "Oak Repairs quote" });
  }
  it.each(["removed", "replaced", "denied"])(
    "releases an open file when its source is %s",
    async (kind) => {
      const { revoke } = fileHandles();
      const { state, store, gateway } = setup();
      await loaded();
      const dialog = await openQuote();
      await within(dialog).findByTitle("Oak Repairs quote");
      if (kind === "denied") {
        vi.mocked(gateway.workspace).mockRejectedValueOnce(new HandoffError("permission"));
      } else if (kind === "removed") {
        state.data.documents = state.data.documents.filter((d) => d.id !== "quote");
      } else {
        state.data.documents.find((d) => d.id === "quote")!.sourceVersion = "2";
      }
      await act(async () => {
        await store.workspace(state.data.handoff.id).fresh();
      });
      await waitFor(() =>
        expect(screen.queryByRole("region", { name: "Oak Repairs quote" })).toBeNull(),
      );
      expect(revoke).toHaveBeenCalledWith("blob:original");
    },
  );
  it("discards a slow file after the viewer closes", async () => {
    const { create } = fileHandles();
    const { gateway } = setup();
    await loaded();
    const pending = deferred<Blob>();
    vi.mocked(gateway.document).mockReturnValueOnce(pending.promise);
    const dialog = await openQuote();
    fireEvent.click(within(dialog).getByRole("button", { name: "Close" }));
    await waitFor(() =>
      expect(screen.queryByRole("region", { name: "Oak Repairs quote" })).toBeNull(),
    );
    await act(async () => {
      pending.resolve(new Blob(["%PDF-1.7"], { type: "application/pdf" }));
    });
    expect(create).not.toHaveBeenCalled();
  });
  it("opens a PDF at its first source page and an image as an image", async () => {
    fileHandles();
    const data = workExample();
    data.documents[1].pageStart = 3;
    data.documents[1].pageEnd = 5;
    setup(data);
    await loaded();
    const dialog = await openQuote();
    expect((await within(dialog).findByTitle("Oak Repairs quote")).getAttribute("src")).toBe(
      "blob:original#page=3",
    );
    cleanup();
    const plan = workExample();
    Object.assign(plan.documents[1], {
      title: "Original floorplan",
      mimeType: "image/png",
      pageStart: null,
      pageEnd: null,
      kind: "Agreement",
    });
    const { gateway } = setup(plan);
    vi.mocked(gateway.document).mockResolvedValue(new Blob(["image"], { type: "image/png" }));
    await loaded();
    fireEvent.click(screen.getByRole("tab", { name: /^Money/ }));
    fireEvent.click(
      within(screen.getByRole("region", { name: /^Quotes/ })).getByRole("button", {
        name: /Original floorplan/,
      }),
    );
    const image = await screen.findByRole("img", { name: "Original floorplan" });
    expect(image.closest("section")?.querySelector("iframe")).toBeNull();
  });
  it("hides file names and text after a failed refresh, without losing an edit", async () => {
    const { gateway, store, state } = setup();
    await loaded();
    fireEvent.click(button("Change"));
    fireEvent.change(screen.getByLabelText("Budget (GBP)"), { target: { value: "1200" } });
    vi.mocked(gateway.workspace).mockRejectedValueOnce(new HandoffError());
    await act(() => store.workspace(state.data.handoff.id).fresh());
    fireEvent.click(screen.getByRole("tab", { name: /^Documents/ }));
    expect(screen.queryByText("Oak Repairs quote")).toBeNull();
    fireEvent.click(screen.getByRole("tab", { name: /^Overview/ }));
    expect((screen.getByLabelText("Budget (GBP)") as HTMLInputElement).value).toBe("1200");
    expect(gateway.apply).not.toHaveBeenCalled();
  });
  it("folds each quote's and invoice's lines by default, and opens them per row or all at once", async () => {
    setup();
    await loaded();
    fireEvent.click(screen.getByRole("tab", { name: /^Money/ }));
    const quotes = within(screen.getByRole("region", { name: /^Quotes/ }));
    expect(quotes.queryByText("Local wall repair")).toBeNull();
    expect(quotes.getByText("In proposed plan", { selector: ".status" })).toBeTruthy();
    fireEvent.click(quotes.getByRole("button", { name: "Show lines of Quoted repair visit" }));
    expect(quotes.getByText("Local wall repair")).toBeTruthy();
    expect(quotes.getByText("Refit handle")).toBeTruthy();
    expect(
      quotes
        .getByRole("button", { name: "Hide lines of Quoted repair visit" })
        .getAttribute("aria-expanded"),
    ).toBe("true");
    fireEvent.click(quotes.getByRole("button", { name: "Collapse all" }));
    expect(quotes.queryByText("Local wall repair")).toBeNull();
    const invoices = within(screen.getByRole("region", { name: /^Invoices/ }));
    const lineRows = () =>
      invoices.getAllByRole("row").filter((r) => r.classList.contains("line-row"));
    expect(lineRows()).toHaveLength(0);
    fireEvent.click(invoices.getByRole("button", { name: "Expand all" }));
    expect(lineRows().length).toBeGreaterThan(0);
  });
  it("keeps quotes and invoices in Money, opens them in a drawer, and closes it with Escape", async () => {
    fileHandles();
    setup();
    await loaded();
    fireEvent.click(screen.getByRole("tab", { name: /^Documents/ }));
    expect(screen.queryByRole("button", { name: /Oak Repairs quote/ })).toBeNull();
    expect(screen.queryByRole("heading", { name: /^Invoices/ })).toBeNull();
    fireEvent.click(screen.getByRole("tab", { name: /^Money/ }));
    const invoices = screen.getByRole("region", { name: /^Invoices/ });
    expect(invoices.textContent).toContain("£80.00");
    expect(screen.getByRole("region", { name: /^Quotes/ }).textContent).toContain(
      "Oak Repairs quote",
    );
    fireEvent.click(
      within(screen.getByRole("region", { name: /^Quotes/ })).getByRole("button", {
        name: /^Oak Repairs quote/,
      }),
    );
    expect(await screen.findByRole("dialog")).toBeTruthy();
    fireEvent.keyDown(document, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
    fireEvent.click(screen.getByRole("tab", { name: /^Overview/ }));
    fireEvent.click(screen.getByRole("button", { name: "Open Money" }));
    expect(screen.getByRole("tab", { name: /^Money/ }).getAttribute("aria-selected")).toBe("true");
  });
});
