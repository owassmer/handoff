// @vitest-environment jsdom
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { CaseControlsPage } from "./Controls";
import { exampleGateway, exampleWorkspace, memoryStorage } from "./examples.test-support";
import { HandoffContext } from "./hooks";
import { HandoffStore } from "./state";

const stores: HandoffStore[] = [];
afterEach(() => {
  cleanup();
  stores.forEach((s) => s.dispose());
  stores.length = 0;
});
function setup(admin: boolean) {
  const data = exampleWorkspace();
  data.permissions.canConfigure = admin;
  data.handoff.physicalProgress = "Arranging work";
  const { gateway, state } = exampleGateway(data);
  gateway.resume = vi.fn(async () => {
    state.data.handoff.revision = String(Number(state.data.handoff.revision) + 1);
    state.data.agent.nextStep = "Paid Hudson Floor Restoration's $2,000.00 advance.";
    return { kind: "done" as const };
  });
  const store = new HandoffStore(gateway, memoryStorage(), "controls", 0);
  stores.push(store);
  render(
    <MemoryRouter initialEntries={["/handoffs/garden-home/controls"]}>
      <HandoffContext.Provider value={store}>
        <Routes>
          <Route
            path="/handoffs/:id/controls"
            element={<CaseControlsPage handoffId="garden-home" />}
          />
        </Routes>
      </HandoffContext.Provider>
    </MemoryRouter>,
  );
  return { gateway };
}

describe("Case controls", () => {
  it("is not available to someone who isn't a workspace admin", async () => {
    const { gateway } = setup(false);
    expect(await screen.findByRole("heading", { name: "That unit isn’t available" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Next step" })).toBeNull();
    expect(gateway.resume).not.toHaveBeenCalled();
  });
  it("runs one step and logs what it changed", async () => {
    const { gateway } = setup(true);
    fireEvent.click(await screen.findByRole("button", { name: "Next step" }));
    await screen.findByText("Step finished.");
    expect(gateway.resume).toHaveBeenCalledExactlyOnceWith("garden-home");
    const steps = screen.getByRole("table", { name: "Steps" });
    expect(steps.textContent).toContain("Paid Hudson Floor Restoration's $2,000.00 advance.");
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "Next step" })).toHaveProperty("disabled", false),
    );
  });
});
