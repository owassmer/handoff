import { afterEach, describe, expect, it } from "vitest";
import { coordinatorTurn } from "../../src/agent/turn.js";
import { stageNoticeWorld } from "../../src/demo/seed.js";
import { ChatGPTPlanModel } from "../../src/llm/chatgpt/model.js";
import { EnvironmentToken } from "../../src/llm/chatgpt/tokens.js";
import type { World } from "../../src/world.js";
import { FakeOpenAI, completed, fnCall, message, reasoning } from "./fakes.js";

let w: World;
afterEach(() => w.close());

describe("the coordinator on the ChatGPT plan transport", () => {
  it("runs a wake through LangGraph with tool names, call ids and results carried exactly", async () => {
    const api = new FakeOpenAI().respond(
      completed([reasoning("rs_1"), fnCall("call_ack", "message_send", { key: "ack-notice", toPartyId: "tenant-1", subject: "We received your notice", body: "Thank you.", purpose: "acknowledge" })]),
      completed([message("Acknowledged the notice.")], "resp_2"),
    );
    const model = new ChatGPTPlanModel({ model: "plan-model", tokens: new EnvironmentToken("T", { T: "at-1" }), fetch: api.fetch });
    w = await stageNoticeWorld(coordinatorTurn({ model }));
    await w.runner.runUntilQuiet();

    expect(await w.mail.inbox("tenant-1")).toHaveLength(1);
    const [first, second] = api.bodies("https://api.openai.com/v1/responses");
    const names = first!.tools[0].tools.map((t: { name: string }) => t.name);
    expect(first!.tools[0]).toMatchObject({ type: "namespace", name: "handoff" });
    expect(names).toEqual(expect.arrayContaining(["message_send", "payment_refund", "propose_decision", "schedule_wakeup", "record_finding"]));
    expect(first!.instructions).toMatch(/You are Handoff's coordinator/);
    expect(first!.input[0].content[0].text).toMatch(/UNTRUSTED/);
    const output = second!.input.find((i: { type: string }) => i.type === "function_call_output");
    expect(output.call_id).toBe("call_ack");
    expect(JSON.parse(output.output)).toMatchObject({ status: "succeeded" });
    expect(second!.input).toContainEqual(reasoning("rs_1"));
    const roles = (await w.db.query<{ role: string }>(`select role from run_messages order by seq`)).map((r) => r.role);
    expect(roles).toEqual(["system", "user", "assistant", "tool", "assistant"]);
  });
});
