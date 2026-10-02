// @vitest-environment jsdom
import { StrictMode } from "react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import type { PublicOauthClient } from "@osdk/oauth";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import AuthCallback from "./AuthCallback";

const auth = vi.hoisted(() => ({ signIn: vi.fn<PublicOauthClient["signIn"]>(), signOut: vi.fn() }));
vi.mock("@/client", () => ({ auth }));
const result = { access_token: "test-session", expires_in: 3600, expires_at: 9999999999999 };
function open() {
  return render(
    <StrictMode>
      <MemoryRouter
        initialEntries={["/auth/callback"]}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <Routes>
          <Route path="/auth/callback" element={<AuthCallback />} />
          <Route path="/handoffs/garden-home" element={<h1>Your handoff</h1>} />
          <Route path="/" element={<h1>Active handoffs</h1>} />
        </Routes>
      </MemoryRouter>
    </StrictMode>,
  );
}
beforeEach(() => {
  auth.signIn.mockReset();
  auth.signOut.mockReset();
  sessionStorage.setItem("handoff.return", "/handoffs/garden-home");
});
afterEach(() => {
  cleanup();
  sessionStorage.clear();
});

it("finishes sign-in once under repeated effects and returns to the remembered handoff", async () => {
  let finish!: (value: typeof result) => void;
  auth.signIn.mockReturnValueOnce(
    new Promise((resolve) => {
      finish = resolve;
    }),
  );
  open();
  expect(screen.getByRole("status").textContent).toBe("Signing you in…");
  await waitFor(() => expect(auth.signIn).toHaveBeenCalledTimes(1));
  await act(async () => finish(result));
  await screen.findByRole("heading", { name: "Your handoff" });
  expect(sessionStorage.getItem("handoff.return")).toBeNull();
  expect(auth.signOut).not.toHaveBeenCalled();
  expect(screen.queryByRole("heading", { name: "Active handoffs" })).toBeNull();
});

it("gives a plain recovery route when callback completion fails, without retrying authorization", async () => {
  auth.signIn.mockRejectedValueOnce(new Error("private authorization response"));
  open();
  await screen.findByRole("heading", { name: "We couldn’t finish signing you in" });
  expect(document.body.textContent).not.toMatch(/private authorization response|password/);
  expect(sessionStorage.getItem("handoff.return")).toBe("/handoffs/garden-home");
  fireEvent.click(screen.getByRole("button", { name: "Return to Handoff" }));
  await screen.findByRole("heading", { name: "Your handoff" });
  expect(auth.signIn).toHaveBeenCalledTimes(1);
  expect(auth.signOut).not.toHaveBeenCalled();
});

it("does not follow an untrusted return address", async () => {
  sessionStorage.setItem("handoff.return", "//another.example/account");
  auth.signIn.mockResolvedValueOnce(result);
  open();
  await screen.findByRole("heading", { name: "Active handoffs" });
});

it("does not consume a return route after the callback has unmounted", async () => {
  let finish!: (value: typeof result) => void;
  auth.signIn.mockReturnValueOnce(
    new Promise((resolve) => {
      finish = resolve;
    }),
  );
  const view = open();
  await waitFor(() => expect(auth.signIn).toHaveBeenCalledTimes(1));
  view.unmount();
  await act(async () => finish(result));
  expect(sessionStorage.getItem("handoff.return")).toBe("/handoffs/garden-home");
});
