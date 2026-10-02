// @vitest-environment jsdom
import { afterEach, expect, it, vi } from "vitest";

const createPublicOauthClient = vi.hoisted(() => vi.fn(() => vi.fn()));
const createClient = vi.hoisted(() => vi.fn());
vi.mock("@osdk/oauth", () => ({ createPublicOauthClient }));
vi.mock("@osdk/client", () => ({ createClient }));
afterEach(() => {
  document.head.innerHTML = "";
});

it("requests only the restricted public operation scopes while retaining the configured client and redirect", async () => {
  for (const [name, value] of Object.entries({
    foundryUrl: "https://foundry.test.invalid",
    clientId: "existing-client",
    redirectUrl: "https://handoff.test.invalid/auth/callback",
    ontologyRid: "existing-ontology",
  })) {
    const tag = document.createElement("meta");
    tag.name = `osdk-${name}`;
    tag.content = value;
    document.head.appendChild(tag);
  }
  await import("./client");
  expect(createPublicOauthClient).toHaveBeenCalledWith(
    "existing-client",
    "https://foundry.test.invalid",
    "https://handoff.test.invalid/auth/callback",
    {
      scopes: [
        "api:use-ontologies-read",
        "api:use-ontologies-write",
        "api:use-admin-read",
        "api:use-mediasets-read",
        "api:use-language-models-execute",
      ],
    },
  );
  expect(createClient).toHaveBeenCalledWith(
    "https://foundry.test.invalid",
    "existing-ontology",
    expect.any(Function),
    { UNSTABLE_DO_NOT_USE_BRANCH: undefined },
  );
});
