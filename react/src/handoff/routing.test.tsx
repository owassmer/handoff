// @vitest-environment jsdom
import type { ReactNode } from "react";
import { RouterProvider } from "react-router-dom";
import { cleanup, render, screen } from "@testing-library/react";
import { afterAll, afterEach, expect, it, vi } from "vitest";

vi.mock("../client", () => ({
  default: {},
  ontologyRid: "test-ontology",
  auth: { signIn: vi.fn() },
}));
vi.mock("@osdk/react", () => ({
  OsdkProvider: ({ children }: { children: ReactNode }) => children,
  useOsdkClient: () => ({}),
}));
vi.stubEnv("VITE_HANDOFF_WORKSPACE_ID", "");
vi.stubEnv("VITE_HANDOFF_FUNCTION_VERSION", "");
const { router } = await import("../router");
afterEach(() => cleanup());
afterAll(() => {
  router.dispose();
  vi.unstubAllEnvs();
});

it("opens Handoff at the root without substituting sample work when the connection is missing", () => {
  render(<RouterProvider router={router} future={{ v7_startTransition: true }} />);
  expect(screen.getByRole("link", { name: "Handoff" })).toBeTruthy();
  expect(screen.getByRole("heading", { name: "Handoff isn’t available yet" })).toBeTruthy();
  expect(screen.queryByText("Demo")).toBeNull();
  expect(screen.queryByRole("button", { name: /^Accept/ })).toBeNull();
});
it("registers only the new work routes and the existing sign-in callback", () => {
  expect(router.routes[0].children?.map((route) => route.path)).toEqual([
    "/",
    "/handoffs/:handoffId",
    "/handoffs/:handoffId/controls",
    "/calendar",
    "*",
  ]);
  expect(router.routes[1].path).toBe("/auth/callback");
  expect(router.routes).toHaveLength(2);
});
