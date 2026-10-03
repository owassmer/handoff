import { AIMessage, type BaseMessage } from "@langchain/core/messages";
import { toJsonSchema } from "@langchain/core/utils/json_schema";

/**
 * The Responses API as ChatGPT plan usage requires it (preview limitations, October 2026):
 * - every request sets store: false and stream: true, and carries its whole history in `input`;
 * - system text goes in `instructions`, never as a system message item;
 * - function tools are grouped in a namespace;
 * - omitted: background, conversation, max_output_tokens, max_tool_calls, metadata, moderation,
 *   multi_agent, prompt, prompt_cache_retention, safety_identifier, temperature, top_logprobs,
 *   top_p, truncation, user, previous_response_id.
 * Reasoning is carried between steps as encrypted content, since nothing is stored server-side.
 */

export interface FunctionTool {
  type: "function";
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  strict: boolean;
}

export const TOOL_NAMESPACE = { name: "handoff", description: "Handoff's tools for working one move-out case." } as const;

export const UNSUPPORTED_FIELDS = [
  "background", "conversation", "max_output_tokens", "max_tool_calls", "metadata", "moderation", "multi_agent", "prompt",
  "prompt_cache_retention", "safety_identifier", "temperature", "top_logprobs", "top_p", "truncation", "user", "previous_response_id",
] as const;

export function toFunctionTool(t: { name: string; description?: string; schema?: unknown }): FunctionTool {
  const schema: Record<string, unknown> = t.schema ? { ...(toJsonSchema(t.schema as never) as Record<string, unknown>) } : { type: "object", properties: {} };
  delete schema.$schema;
  return { type: "function", name: t.name, description: t.description ?? "", parameters: schema, strict: false };
}

export interface RequestOptions {
  model: string;
  tools?: FunctionTool[];
  reasoningEffort?: "none" | "minimal" | "low" | "medium" | "high" | "xhigh";
  toolChoice?: "auto" | "required" | "none";
}

type Item = Record<string, unknown>;

export function buildResponsesRequest(messages: BaseMessage[], o: RequestOptions): Record<string, unknown> {
  const instructions: string[] = [];
  const input: Item[] = [];
  for (const m of messages) {
    const type = m.getType();
    if (type === "system") instructions.push(textOnly(m.content, "system message"));
    else if (type === "human") input.push({ type: "message", role: "user", content: inputContent(m.content) });
    else if (type === "ai") input.push(...assistantItems(m as AIMessage));
    else if (type === "tool") input.push(toolOutput(m));
    else throw new Error(`cannot send a ${type} message to the Responses API`);
  }
  const body: Record<string, unknown> = {
    model: o.model,
    input,
    store: false,
    stream: true,
    include: ["reasoning.encrypted_content"],
  };
  if (instructions.length > 0) body.instructions = instructions.join("\n\n");
  if (o.tools && o.tools.length > 0) {
    body.tools = [{ type: "namespace", name: TOOL_NAMESPACE.name, description: TOOL_NAMESPACE.description, tools: o.tools }];
    body.tool_choice = o.toolChoice ?? "auto";
    body.parallel_tool_calls = true;
  }
  if (o.reasoningEffort) body.reasoning = { effort: o.reasoningEffort };
  return body;
}

function textOnly(content: BaseMessage["content"], what: string): string {
  if (typeof content === "string") return content;
  return content.map((p) => {
    if (p.type === "text" && typeof (p as { text?: unknown }).text === "string") return (p as { text: string }).text;
    throw new Error(`a ${what} may contain only text`);
  }).join("");
}

/** User content: text, images and files. Audio and video are not supported on this route. */
function inputContent(content: BaseMessage["content"]): Item[] {
  if (typeof content === "string") return [{ type: "input_text", text: content }];
  return content.map((raw) => {
    const p = raw as Record<string, any>;
    switch (p.type) {
      case "text":
        return { type: "input_text", text: p.text };
      case "image_url": {
        const url = typeof p.image_url === "string" ? p.image_url : p.image_url?.url;
        return { type: "input_image", image_url: url, detail: (typeof p.image_url === "object" && p.image_url?.detail) || "auto" };
      }
      case "image": {
        const mime = p.mimeType ?? p.mime_type ?? "image/png";
        const url = p.url ?? (p.data ? `data:${mime};base64,${p.data}` : undefined);
        if (!url) throw new Error("an image block needs a url or base64 data");
        return { type: "input_image", image_url: url, detail: p.detail ?? "auto" };
      }
      case "file": {
        const mime = p.mimeType ?? p.mime_type ?? "application/pdf";
        const filename = p.filename ?? p.metadata?.filename ?? "document";
        if (p.url) return { type: "input_file", file_url: p.url, filename };
        if (p.data) return { type: "input_file", file_data: `data:${mime};base64,${p.data}`, filename };
        throw new Error("a file block needs a url or base64 data");
      }
      default:
        throw new Error(`content of type ${p.type} is not supported by ChatGPT plan usage`);
    }
  });
}

/**
 * An assistant turn. If it came from this API, its output items are replayed exactly as returned:
 * reasoning with its encrypted content, messages, and function calls with their call ids.
 */
function assistantItems(m: AIMessage): Item[] {
  const replay = m.additional_kwargs?.response_items;
  if (Array.isArray(replay) && replay.length > 0) return replay as Item[];
  const items: Item[] = [];
  const text = typeof m.content === "string" ? m.content : textOnly(m.content, "assistant message");
  if (text) items.push({ type: "message", role: "assistant", content: [{ type: "output_text", text }] });
  for (const c of m.tool_calls ?? []) {
    if (!c.id) throw new Error(`tool call ${c.name} has no id`);
    items.push({ type: "function_call", call_id: c.id, name: c.name, namespace: TOOL_NAMESPACE.name, arguments: JSON.stringify(c.args ?? {}) });
  }
  return items;
}

function toolOutput(m: BaseMessage): Item {
  const callId = (m as { tool_call_id?: string }).tool_call_id;
  if (!callId) throw new Error("a tool result has no tool_call_id");
  const output = typeof m.content === "string" ? m.content : inputContent(m.content);
  return { type: "function_call_output", call_id: callId, output };
}

// ---- Errors ------------------------------------------------------------------------------------

export type PlanErrorKind =
  | "not_eligible" | "usage_limit" | "usage_unavailable" | "unsupported_capability" | "route_not_supported" | "invalid_user"
  | "scope_not_authorized" | "user_unavailable" | "unauthorized" | "forbidden" | "unavailable" | "incomplete"
  | "stream_interrupted" | "failed" | "http_error";

const KIND_BY_CODE: Record<string, PlanErrorKind> = {
  subscription_sharing_user_not_eligible: "not_eligible",
  subscription_sharing_usage_limit_exceeded: "usage_limit",
  subscription_sharing_usage_unavailable: "usage_unavailable",
  subscription_sharing_unsupported_capability: "unsupported_capability",
  subscription_sharing_route_not_supported: "route_not_supported",
  subscription_sharing_invalid_user: "invalid_user",
  chatpass_v2_scope_not_authorized: "scope_not_authorized",
  chatpass_v2_invalid_authorization_context: "scope_not_authorized",
  subscription_sharing_user_unavailable: "user_unavailable",
};

const RECOVERY: Partial<Record<PlanErrorKind, string>> = {
  not_eligible: "ChatGPT plan usage is unavailable for this user, workspace or policy. Do not repeat the request.",
  usage_limit: "Plan usage limit reached. Pause requests; see https://chatgpt.com/settings/usage.",
  usage_unavailable: "Usage availability could not be checked. Retry later with bounded backoff.",
  unsupported_capability: "Remove the unsupported input, tool, feature, model or service tier named in param. Do not retry the same body.",
  route_not_supported: "Check the method and endpoint: POST /v1/responses.",
  invalid_user: "The subscriber context could not be validated. Sign in again if the session was revoked.",
  scope_not_authorized: "The signed permission does not authorize this. Check the client and grant.",
  user_unavailable: "Account information is temporarily unavailable. Retry later with bounded backoff.",
  unauthorized: "The identity or plan permission was not accepted. Check the selected account and granted scopes.",
  forbidden: "A policy or permission check prevented admission, such as the serving region.",
  unavailable: "Direct routing is unavailable. Keep credentials and retry later with bounded backoff.",
};

const RETRYABLE = new Set<PlanErrorKind>(["usage_unavailable", "user_unavailable", "unavailable", "stream_interrupted"]);

/** A ChatGPT plan request that did not complete. It stops inference; nothing switches to another billing path. */
export class ChatGPTPlanError extends Error {
  readonly retryable: boolean;

  constructor(
    readonly kind: PlanErrorKind,
    readonly detail: { status?: number; code?: string | null; param?: string | null; message?: string | null; requestId?: string | null } = {},
  ) {
    super(`ChatGPT plan request ${kind}${detail.status ? ` (HTTP ${detail.status})` : ""}${detail.code ? ` ${detail.code}` : ""}` +
      `${detail.param ? ` param=${detail.param}` : ""}${detail.message ? `: ${detail.message}` : ""}${detail.requestId ? ` [request ${detail.requestId}]` : ""}` +
      `${RECOVERY[kind] ? ` — ${RECOVERY[kind]}` : ""}`);
    this.retryable = RETRYABLE.has(kind);
  }
}

/** Classifies a non-2xx answer before a stream opened. The body may be a standard error object or just {"detail": "..."}. */
export async function errorFromHttp(res: Response): Promise<ChatGPTPlanError> {
  const requestId = res.headers.get("x-request-id");
  const text = await res.text();
  let body: Record<string, any> | null = null;
  try {
    body = JSON.parse(text);
  } catch {
    body = null;
  }
  const code: string | null = body?.error?.code ?? null;
  const message: string | null = body?.error?.message ?? (typeof body?.detail === "string" ? body.detail : null) ?? (body ? null : text.slice(0, 300) || null);
  const param: string | null = body?.error?.param ?? null;
  const kind: PlanErrorKind = (code && KIND_BY_CODE[code]) || (res.status === 401 ? "unauthorized" : res.status === 403 ? "forbidden" : res.status === 503 ? "unavailable" : "http_error");
  return new ChatGPTPlanError(kind, { status: res.status, code, param, message, requestId });
}

// ---- Streaming ---------------------------------------------------------------------------------

export interface ServerSentEvent {
  event: string | null;
  data: string;
}

export async function* readServerSentEvents(body: ReadableStream<Uint8Array>): AsyncGenerator<ServerSentEvent> {
  const decoder = new TextDecoder();
  let buffer = "";
  let event: string | null = null;
  let data: string[] = [];
  const flush = () => {
    const out = data.length > 0 ? { event, data: data.join("\n") } : null;
    event = null;
    data = [];
    return out;
  };
  for await (const chunk of body as unknown as AsyncIterable<Uint8Array>) {
    buffer += decoder.decode(chunk, { stream: true });
    let nl: number;
    while ((nl = buffer.indexOf("\n")) >= 0) {
      const line = buffer.slice(0, nl).replace(/\r$/, "");
      buffer = buffer.slice(nl + 1);
      if (line === "") {
        const e = flush();
        if (e) yield e;
      } else if (line.startsWith(":")) {
        continue;
      } else if (line.startsWith("event:")) {
        event = line.slice(6).trim();
      } else if (line.startsWith("data:")) {
        data.push(line.slice(5).replace(/^ /, ""));
      }
    }
  }
  buffer += decoder.decode();
  if (buffer.trim()) {
    for (const line of buffer.split(/\r?\n/)) if (line.startsWith("data:")) data.push(line.slice(5).replace(/^ /, ""));
  }
  const last = flush();
  if (last) yield last;
}

export interface CompletedResponse {
  id: string;
  model: string;
  status: string;
  output: Item[];
  usage: Record<string, any> | null;
}

/** Reads the stream through its terminal event. Only response.completed is success. */
export async function collectResponse(events: AsyncIterable<ServerSentEvent>, requestId: string | null = null): Promise<CompletedResponse> {
  const items: Item[] = [];
  for await (const e of events) {
    let data: Record<string, any>;
    try {
      data = JSON.parse(e.data);
    } catch {
      continue;
    }
    switch (data.type) {
      case "response.output_item.done":
        items[data.output_index ?? items.length] = data.item;
        break;
      case "response.completed": {
        const r = data.response ?? {};
        const output = Array.isArray(r.output) && r.output.length > 0 ? r.output : items.filter(Boolean);
        return { id: r.id ?? "", model: r.model ?? "", status: r.status ?? "completed", output, usage: r.usage ?? null };
      }
      case "response.failed": {
        const err = data.response?.error ?? {};
        throw new ChatGPTPlanError((err.code && KIND_BY_CODE[err.code]) || "failed", { code: err.code ?? null, message: err.message ?? null, requestId });
      }
      case "response.incomplete":
        throw new ChatGPTPlanError("incomplete", { message: data.response?.incomplete_details?.reason ?? null, requestId });
      case "error":
        throw new ChatGPTPlanError((data.code && KIND_BY_CODE[data.code]) || "failed", { code: data.code ?? null, param: data.param ?? null, message: data.message ?? null, requestId });
      default:
        break;
    }
  }
  throw new ChatGPTPlanError("stream_interrupted", { message: "the stream ended without response.completed", requestId });
}

/** The completed response as one assistant message, keeping every output item for exact replay. */
export function toAIMessage(r: CompletedResponse): AIMessage {
  let text = "";
  const toolCalls: Array<{ id: string; name: string; args: Record<string, unknown>; type: "tool_call" }> = [];
  const invalid: Array<{ id: string; name: string; args: string; error: string; type: "invalid_tool_call" }> = [];
  for (const item of r.output) {
    if (item.type === "message") {
      for (const part of (item.content as Item[] | undefined) ?? []) {
        if (part.type === "output_text") text += String(part.text ?? "");
        else if (part.type === "refusal") text += String(part.refusal ?? "");
      }
    } else if (item.type === "function_call") {
      const name = String(item.name).replace(new RegExp(`^${TOOL_NAMESPACE.name}[.:/]`), "");
      const id = String(item.call_id);
      try {
        toolCalls.push({ id, name, args: JSON.parse(String(item.arguments || "{}")), type: "tool_call" });
      } catch (e) {
        invalid.push({ id, name, args: String(item.arguments), error: e instanceof Error ? e.message : String(e), type: "invalid_tool_call" });
      }
    }
  }
  const u = r.usage;
  return new AIMessage({
    content: text,
    tool_calls: toolCalls,
    invalid_tool_calls: invalid,
    additional_kwargs: { response_items: r.output },
    response_metadata: { id: r.id, model: r.model, status: r.status, usage: u },
    usage_metadata: u ? { input_tokens: u.input_tokens ?? 0, output_tokens: u.output_tokens ?? 0, total_tokens: u.total_tokens ?? 0 } : undefined,
  });
}
