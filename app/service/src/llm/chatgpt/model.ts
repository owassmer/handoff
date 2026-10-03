import type { BaseChatModelCallOptions } from "@langchain/core/language_models/chat_models";
import { BaseChatModel } from "@langchain/core/language_models/chat_models";
import type { BaseMessage } from "@langchain/core/messages";
import type { ChatResult } from "@langchain/core/outputs";
import { API_RESOURCE } from "./config.js";
import type { Fetch } from "./oauth.js";
import { type FunctionTool, type RequestOptions, buildResponsesRequest, collectResponse, errorFromHttp, readServerSentEvents, toAIMessage, toFunctionTool } from "./responses.js";
import type { TokenSource } from "./tokens.js";

export interface ChatGPTPlanCallOptions extends BaseChatModelCallOptions {
  responsesTools?: FunctionTool[];
}

export interface ChatGPTPlanFields {
  /** A model slug available to the signed-in account, from GET /v1/models. */
  model: string;
  tokens: TokenSource;
  fetch?: Fetch;
  baseUrl?: string;
  reasoningEffort?: RequestOptions["reasoningEffort"];
}

/** A chat model billed to the user's ChatGPT plan through Sign in with ChatGPT. No fallback lives here. */
export class ChatGPTPlanModel extends BaseChatModel<ChatGPTPlanCallOptions> {
  readonly model: string;
  readonly tokens: TokenSource;
  private readonly fetchImpl: Fetch;
  private readonly baseUrl: string;
  private readonly reasoningEffort: RequestOptions["reasoningEffort"];

  constructor(fields: ChatGPTPlanFields) {
    super({});
    this.model = fields.model;
    this.tokens = fields.tokens;
    this.fetchImpl = fields.fetch ?? ((...a) => fetch(...a));
    this.baseUrl = fields.baseUrl ?? API_RESOURCE;
    this.reasoningEffort = fields.reasoningEffort;
  }

  _llmType(): string {
    return "openai-chatgpt-plan";
  }

  override bindTools(tools: Array<{ name: string; description?: string; schema?: unknown }>, kwargs?: Partial<ChatGPTPlanCallOptions>): any {
    return this.withConfig({ ...kwargs, responsesTools: tools.map(toFunctionTool) } as Partial<ChatGPTPlanCallOptions>);
  }

  async _generate(messages: BaseMessage[], options: this["ParsedCallOptions"]): Promise<ChatResult> {
    const body = buildResponsesRequest(messages, { model: this.model, tools: options.responsesTools, reasoningEffort: this.reasoningEffort });
    const message = toAIMessage(await this.send(body, options.signal));
    return { generations: [{ text: typeof message.content === "string" ? message.content : "", message }] };
  }

  /** Posts once; after a 401 asks the token source for a different token and tries exactly once more. */
  private async send(body: Record<string, unknown>, signal?: AbortSignal) {
    let authorization = await this.tokens.authorization();
    for (let attempt = 0; ; attempt++) {
      const headers: Record<string, string> = { "Content-Type": "application/json", Accept: "text/event-stream" };
      if (authorization) headers.Authorization = authorization;
      const res = await this.fetchImpl(`${this.baseUrl}/responses`, { method: "POST", headers, body: JSON.stringify(body), signal });
      if (res.status === 401 && attempt === 0 && (await this.tokens.renew(authorization))) {
        await res.body?.cancel();
        authorization = await this.tokens.authorization();
        continue;
      }
      if (!res.ok) throw await errorFromHttp(res);
      if (!res.body) throw new Error("the Responses API returned no stream");
      return collectResponse(readServerSentEvents(res.body), res.headers.get("x-request-id"));
    }
  }
}
