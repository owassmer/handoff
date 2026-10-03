import { AIMessage, HumanMessage, SystemMessage, ToolMessage } from "@langchain/core/messages";
import { tool } from "@langchain/core/tools";
import { describe, expect, it } from "vitest";
import { z } from "zod";
import { ChatGPTPlanModel } from "../../src/llm/chatgpt/model.js";
import { ChatGPTPlanError, UNSUPPORTED_FIELDS, buildResponsesRequest, toFunctionTool } from "../../src/llm/chatgpt/responses.js";
import { EnvironmentToken, ProxyInjectedToken, type TokenSource } from "../../src/llm/chatgpt/tokens.js";
import { FakeOpenAI, completed, fnCall, message, reasoning, sse } from "./fakes.js";

const URL_RESPONSES = "https://api.openai.com/v1/responses";
const sendMessage = tool(async () => "ok", {
  name: "message_send",
  description: "Email a party.",
  schema: z.object({ key: z.string(), toPartyId: z.string(), body: z.string(), purpose: z.string().optional() }),
});
const token = (t = "at-1") => new EnvironmentToken("TOKEN", { TOKEN: t });

describe("the outgoing request", () => {
  it("follows the plan route's rules: instructions, full history, namespaced tools, store false, stream true", () => {
    const priorItems = [reasoning("rs_1"), fnCall("call_1", "message_send", { key: "ack", toPartyId: "tenant-1", body: "Hi" })];
    const body = buildResponsesRequest([
      new SystemMessage("You are Handoff's coordinator."),
      new HumanMessage({ content: [
        { type: "text", text: "Here is the case." },
        { type: "image_url", image_url: { url: "https://example.test/closet.jpg", detail: "high" } },
        { type: "image", data: "aGVsbG8=", mimeType: "image/jpeg" },
        { type: "file", url: "https://example.test/lease.pdf", mimeType: "application/pdf", filename: "lease.pdf" },
      ] }),
      new AIMessage({ content: "", tool_calls: [{ id: "call_1", name: "message_send", args: { key: "ack", toPartyId: "tenant-1", body: "Hi" } }], additional_kwargs: { response_items: priorItems } }),
      new ToolMessage({ tool_call_id: "call_1", content: '{"status":"succeeded"}' }),
    ], { model: "plan-model", tools: [toFunctionTool(sendMessage)] });

    expect(body).toEqual({
      model: "plan-model",
      instructions: "You are Handoff's coordinator.",
      input: [
        { type: "message", role: "user", content: [
          { type: "input_text", text: "Here is the case." },
          { type: "input_image", image_url: "https://example.test/closet.jpg", detail: "high" },
          { type: "input_image", image_url: "data:image/jpeg;base64,aGVsbG8=", detail: "auto" },
          { type: "input_file", file_url: "https://example.test/lease.pdf", filename: "lease.pdf" },
        ] },
        ...priorItems,
        { type: "function_call_output", call_id: "call_1", output: '{"status":"succeeded"}' },
      ],
      tools: [{
        type: "namespace", name: "handoff", description: "Handoff's tools for working one move-out case.",
        tools: [{ type: "function", name: "message_send", description: "Email a party.", strict: false, parameters: expect.objectContaining({ type: "object", required: ["key", "toPartyId", "body"] }) }],
      }],
      tool_choice: "auto",
      parallel_tool_calls: true,
      store: false,
      stream: true,
      include: ["reasoning.encrypted_content"],
    });
    for (const field of UNSUPPORTED_FIELDS) expect(body).not.toHaveProperty(field);
    expect(JSON.stringify(body.input)).not.toContain('"role":"system"');
  });

  it("rebuilds an assistant turn that did not come from this API, keeping tool names and call ids", () => {
    const body = buildResponsesRequest([new AIMessage({ content: "Checking.", tool_calls: [{ id: "call_9", name: "note", args: { kind: "k", text: "t" } }] })], { model: "m" });
    expect(body.input).toEqual([
      { type: "message", role: "assistant", content: [{ type: "output_text", text: "Checking." }] },
      { type: "function_call", call_id: "call_9", name: "note", namespace: "handoff", arguments: '{"kind":"k","text":"t"}' },
    ]);
  });

  it("refuses input the route does not support", () => {
    expect(() => buildResponsesRequest([new HumanMessage({ content: [{ type: "audio", data: "x", mimeType: "audio/wav" } as never] })], { model: "m" })).toThrow(/not supported/);
  });
});

describe("the model over the wire", () => {
  it("sends the bearer token and reads the stream into a complete assistant message", async () => {
    const api = new FakeOpenAI().respond(completed([reasoning("rs_1"), fnCall("call_1", "message_send", { key: "ack", toPartyId: "tenant-1", body: "Hi" }), message("Sending now.")]));
    const model = new ChatGPTPlanModel({ model: "plan-model", tokens: token(), fetch: api.fetch });
    const reply = (await model.bindTools([sendMessage]).invoke([new SystemMessage("sys"), new HumanMessage("go")])) as AIMessage;

    const req = api.requests[0]!;
    expect(req.url).toBe(URL_RESPONSES);
    expect(req.method).toBe("POST");
    expect(req.headers).toMatchObject({ authorization: "Bearer at-1", "content-type": "application/json", accept: "text/event-stream" });
    expect(reply.tool_calls).toEqual([{ id: "call_1", name: "message_send", args: { key: "ack", toPartyId: "tenant-1", body: "Hi" }, type: "tool_call" }]);
    expect(reply.content).toBe("Sending now.");
    expect((reply.additional_kwargs.response_items as unknown[]).length).toBe(3);
    expect(reply.usage_metadata).toEqual({ input_tokens: 100, output_tokens: 20, total_tokens: 120 });

    // The next request replays the whole response, reasoning included, and answers the call by its id.
    api.respond(completed([message("Done.")], "resp_2"));
    await model.bindTools([sendMessage]).invoke([new SystemMessage("sys"), new HumanMessage("go"), reply, new ToolMessage({ tool_call_id: "call_1", content: "sent" })]);
    const second = api.bodies(URL_RESPONSES)[1]!;
    expect(second.input.slice(1)).toEqual([
      reasoning("rs_1"),
      fnCall("call_1", "message_send", { key: "ack", toPartyId: "tenant-1", body: "Hi" }),
      message("Sending now."),
      { type: "function_call_output", call_id: "call_1", output: "sent" },
    ]);
  });

  it("sends no Authorization header when the environment's proxy injects it", async () => {
    const api = new FakeOpenAI().respond(completed([message("ok")]));
    await new ChatGPTPlanModel({ model: "m", tokens: new ProxyInjectedToken(), fetch: api.fetch }).invoke([new HumanMessage("hi")]);
    expect(api.requests[0]!.headers).not.toHaveProperty("authorization");
  });

  it("after a 401 asks for a different token once, then retries once", async () => {
    let renewed = false;
    const tokens: TokenSource = {
      kind: "stored",
      describe: () => "test",
      authorization: async () => (renewed ? "Bearer at-2" : "Bearer at-1"),
      renew: async () => ((renewed = true), true),
    };
    const api = new FakeOpenAI().respond(Response.json({ error: { message: "expired", code: null } }, { status: 401 }), completed([message("ok")]));
    await new ChatGPTPlanModel({ model: "m", tokens, fetch: api.fetch }).invoke([new HumanMessage("hi")]);
    expect(api.requests.map((r) => r.headers.authorization)).toEqual(["Bearer at-1", "Bearer at-2"]);
  });
});

describe("failures stop inference and say why", () => {
  const run = (answer: string | Response) => new ChatGPTPlanModel({ model: "m", tokens: token(), fetch: new FakeOpenAI().respond(answer).fetch }).invoke([new HumanMessage("hi")]);

  it("classifies admission failures that carry only a detail message", async () => {
    const err = await run(new Response(JSON.stringify({ detail: "region not permitted" }), { status: 403, headers: { "x-request-id": "req_9" } })).catch((e) => e);
    expect(err).toBeInstanceOf(ChatGPTPlanError);
    expect(err).toMatchObject({ kind: "forbidden", detail: { status: 403, message: "region not permitted", requestId: "req_9" }, retryable: false });
  });

  it("classifies structured errors by code", async () => {
    const limit = await run(Response.json({ error: { code: "subscription_sharing_usage_limit_exceeded", message: "limit", param: null } }, { status: 429 })).catch((e) => e);
    expect(limit).toMatchObject({ kind: "usage_limit", retryable: false });
    expect(limit.message).toContain("chatgpt.com/settings/usage");
    const unsupported = await run(Response.json({ error: { code: "subscription_sharing_unsupported_capability", param: "tools[0]" } }, { status: 400 })).catch((e) => e);
    expect(unsupported).toMatchObject({ kind: "unsupported_capability", detail: { param: "tools[0]" } });
    expect(await run(Response.json({ error: { code: "subscription_sharing_user_not_eligible" } }, { status: 403 })).catch((e) => e)).toMatchObject({ kind: "not_eligible" });
    expect(await run(Response.json({ error: { code: "subscription_sharing_usage_unavailable" } }, { status: 503 })).catch((e) => e)).toMatchObject({ kind: "usage_unavailable", retryable: true });
  });

  it("treats a usage limit that arrives after streaming began as a failure", async () => {
    const stream = sse([
      { type: "response.created", response: { id: "r", output: [] } },
      { type: "response.output_text.delta", delta: "Partial" },
      { type: "response.failed", response: { error: { code: "subscription_sharing_usage_limit_exceeded", message: "limit reached" } } },
    ]);
    expect(await run(stream).catch((e) => e)).toMatchObject({ kind: "usage_limit" });
  });

  it("succeeds only on response.completed", async () => {
    const cut = sse([{ type: "response.created", response: { id: "r", output: [] } }, { type: "response.output_item.done", output_index: 0, item: message("half") }]);
    expect(await run(cut).catch((e) => e)).toMatchObject({ kind: "stream_interrupted", retryable: true });
    const incomplete = sse([{ type: "response.incomplete", response: { incomplete_details: { reason: "max_output_tokens" } } }]);
    expect(await run(incomplete).catch((e) => e)).toMatchObject({ kind: "incomplete" });
  });
});
