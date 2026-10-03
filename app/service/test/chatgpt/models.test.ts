import { HumanMessage } from "@langchain/core/messages";
import { describe, expect, it, vi } from "vitest";
import { PaidFallbackModel, modelFor, settingsFor } from "../../src/agent/models.js";
import { ChatGPTPlanModel } from "../../src/llm/chatgpt/model.js";
import { EnvironmentToken, NotAuthorized, StoredCredentials } from "../../src/llm/chatgpt/tokens.js";
import { ScriptedModel, say } from "../scriptedModel.js";
import { FakeOpenAI, completed, message, tempStore } from "./fakes.js";

const usageLimit = () => Response.json({ error: { code: "subscription_sharing_usage_limit_exceeded" } }, { status: 429 });

describe("choosing the provider", () => {
  it("defaults to the ChatGPT plan, with the model from configuration", () => {
    const env = { HANDOFF_COORDINATOR_MODEL: "plan-model", HANDOFF_CHATGPT_AUTH: "environment", HANDOFF_CHATGPT_ACCESS_TOKEN: "t" };
    const m = modelFor("coordinator", { env });
    expect(m).toBeInstanceOf(ChatGPTPlanModel);
    expect((m as ChatGPTPlanModel).model).toBe("plan-model");
    expect(settingsFor("coordinator", env)).toMatchObject({ provider: "openai_chatgpt", allowPaidFallback: false, fallbackModel: null });
  });

  it("uses stored credentials unless told otherwise, and per-role settings", () => {
    const env = { HANDOFF_MODEL_PROVIDER: "openai_chatgpt", HANDOFF_COORDINATOR_MODEL: "a", HANDOFF_TENANT_MODEL: "b", HANDOFF_TENANT_PROVIDER: "openrouter", HANDOFF_CHATGPT_HOME: "/tmp/handoff-test-creds" };
    expect((modelFor("coordinator", { env }) as ChatGPTPlanModel).tokens).toBeInstanceOf(StoredCredentials);
    const paid = vi.fn(() => new ScriptedModel([]));
    modelFor("tenant", { env, paidModel: paid });
    expect(paid).toHaveBeenCalledWith("b");
  });

  it("needs a model for the role and a known provider", () => {
    expect(() => settingsFor("coordinator", {})).toThrow(/HANDOFF_COORDINATOR_MODEL/);
    expect(() => settingsFor("coordinator", { HANDOFF_MODEL_PROVIDER: "other", HANDOFF_COORDINATOR_MODEL: "x" })).toThrow(/unknown model provider/);
  });
});

describe("no paid fallback unless explicitly allowed", () => {
  const env = { HANDOFF_COORDINATOR_MODEL: "plan-model", HANDOFF_CHATGPT_AUTH: "environment", HANDOFF_CHATGPT_ACCESS_TOKEN: "t", HANDOFF_COORDINATOR_FALLBACK_MODEL: "paid-model" };

  it("lets a usage limit, ineligibility or missing authorization stop the request when fallback is off", async () => {
    const paid = vi.fn(() => new ScriptedModel([say("paid answer")]));
    for (const flag of [undefined, "false", "TRUE", "1"]) {
      const api = new FakeOpenAI().respond(usageLimit());
      const m = modelFor("coordinator", { env: { ...env, HANDOFF_ALLOW_PAID_FALLBACK: flag }, fetch: api.fetch, paidModel: paid });
      await expect(m.invoke([new HumanMessage("hi")])).rejects.toMatchObject({ kind: "usage_limit" });
    }
    const noToken = modelFor("coordinator", { env: { ...env, HANDOFF_CHATGPT_ACCESS_TOKEN: undefined }, paidModel: paid });
    await expect(noToken.invoke([new HumanMessage("hi")])).rejects.toThrow(NotAuthorized);
    const { store, cleanup } = await tempStore();
    try {
      const noAccount = modelFor("coordinator", { env: { ...env, HANDOFF_CHATGPT_AUTH: "stored", HANDOFF_CHATGPT_HOME: store.dir }, paidModel: paid });
      await expect(noAccount.invoke([new HumanMessage("hi")])).rejects.toThrow(NotAuthorized);
    } finally {
      await cleanup();
    }
    expect(paid).not.toHaveBeenCalled();
  });

  it("falls back only when allowed, only on plan failures, and needs a named paid model", async () => {
    expect(() => modelFor("coordinator", { env: { ...env, HANDOFF_ALLOW_PAID_FALLBACK: "true", HANDOFF_COORDINATOR_FALLBACK_MODEL: undefined } })).toThrow(/FALLBACK_MODEL/);
    const paid = vi.fn(() => new ScriptedModel([say("paid answer")]));
    const api = new FakeOpenAI().respond(usageLimit());
    const m = modelFor("coordinator", { env: { ...env, HANDOFF_ALLOW_PAID_FALLBACK: "true" }, fetch: api.fetch, paidModel: paid });
    expect(m).toBeInstanceOf(PaidFallbackModel);
    expect((await m.bindTools!([]).invoke([new HumanMessage("hi")])).content).toBe("paid answer");
    expect(paid).toHaveBeenCalledWith("paid-model");

    const healthy = modelFor("coordinator", { env: { ...env, HANDOFF_ALLOW_PAID_FALLBACK: "true" }, fetch: new FakeOpenAI().respond(completed([message("plan answer")])).fetch, paidModel: paid });
    expect((await healthy.bindTools!([]).invoke([new HumanMessage("hi")])).content).toBe("plan answer");
    expect(paid).toHaveBeenCalledTimes(1);
  });

  it("does not hide a programming error behind a paid model", async () => {
    const paid = vi.fn(() => new ScriptedModel([say("paid")]));
    const broken = new PaidFallbackModel(new ChatGPTPlanModel({ model: "m", tokens: new EnvironmentToken("T", { T: "t" }), fetch: async () => { throw new TypeError("bug"); } }), paid);
    await expect(broken.bindTools([]).invoke([new HumanMessage("hi")])).rejects.toThrow(TypeError);
    expect(paid).not.toHaveBeenCalled();
  });
});
