import { readFileSync } from "node:fs";
import { loadEnv } from "vite";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HANDOFF_BRANCH } from "./branchConfig";
import { isConnected } from "./gateway";

const expected = {
  VITE_HANDOFF_WORKSPACE_ID:
    "workspace:433cce6e773072edba75357c931ed5c14efe80c180dbefff8c7258217c3b13ac",
  VITE_HANDOFF_CHANGE_FUNCTION_RID:
    "ri.function-registry.main.function.5036147c-b612-4176-858e-c07d49905a26",
  VITE_HANDOFF_ACCEPT_FUNCTION_RID:
    "ri.function-registry.main.function.0a95a24a-6d0e-4934-b29c-edc850ed6e21",
  VITE_HANDOFF_MESSAGE_FUNCTION_RID:
    "ri.function-registry.main.function.7c599c2f-4dd3-432a-bf04-ed88b0dcb9f2",
};
afterEach(() => vi.unstubAllEnvs());

describe("Handoff deployment", () => {
  it.each(["development", "code-workspaces", "production"])(
    "binds %s to the case workspace with no version pins and message identity",
    async (mode) => {
      const env = loadEnv(mode, process.cwd());
      expect(env).toMatchObject(expected);
      expect(env.VITE_HANDOFF_FUNCTION_VERSION).toBeUndefined();
      expect(env.VITE_HANDOFF_ACTION_FUNCTION_VERSION).toBeUndefined();
      // Also check each file, not just Vite's combined environment.
      const file = readFileSync(`.env.${mode}`, "utf8");
      for (const [key, value] of Object.entries(expected)) {
        expect(file.split(/\r?\n/)).toContain(`${key}=${value}`);
        vi.stubEnv(key, value);
      }
      vi.resetModules();
      const { handoffDeployment } = await import("./branchConfig");
      expect(handoffDeployment).toEqual({
        workspaceId: expected.VITE_HANDOFF_WORKSPACE_ID,
        changeFunctionRid: expected.VITE_HANDOFF_CHANGE_FUNCTION_RID,
        acceptFunctionRid: expected.VITE_HANDOFF_ACCEPT_FUNCTION_RID,
        messageFunctionRid: expected.VITE_HANDOFF_MESSAGE_FUNCTION_RID,
      });
      expect(HANDOFF_BRANCH).toBeUndefined();
      expect(
        isConnected({
          ontologyRid: env.VITE_FOUNDRY_ONTOLOGY_RID,
          ...handoffDeployment,
        }),
      ).toBe(true);
      expect(env.VITE_FOUNDRY_API_URL).toBe("https://owenwassmer.usw-22.palantirfoundry.com");
      expect(env.VITE_FOUNDRY_CLIENT_ID).toBe("e1741d6da7d970a5abe5906a2251d9ec");
      expect(env.VITE_FOUNDRY_ONTOLOGY_RID).toBe(
        "ri.ontology.main.ontology.cfb1478a-5b0e-466a-aaff-b212870e8861",
      );
    },
  );
  it("wires a separately supplied message function identity without inventing a deployment value", async () => {
    vi.stubEnv("VITE_HANDOFF_MESSAGE_FUNCTION_RID", "published-message-function");
    vi.resetModules();
    const { handoffDeployment } = await import("./branchConfig");
    expect(handoffDeployment.messageFunctionRid).toBe("published-message-function");
  });
  it("preserves all registered sign-in redirect settings", () => {
    expect(loadEnv("production", process.cwd()).VITE_FOUNDRY_REDIRECT_URL).toBe(
      "https://handoff-ite67ixhgakg2t7f.apps.usw-22.palantirfoundry.com/auth/callback",
    );
    expect(loadEnv("development", process.cwd()).VITE_FOUNDRY_REDIRECT_URL).toBe(
      "http://localhost:8080/auth/callback",
    );
    expect(readFileSync(".env.code-workspaces", "utf8")).toContain(
      "VITE_FOUNDRY_REDIRECT_URL=https://${DEV_SERVER_DOMAIN}${DEV_SERVER_BASE_PATH}/auth/callback",
    );
  });
});
