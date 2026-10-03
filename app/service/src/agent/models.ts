import { BaseChatModel } from "@langchain/core/language_models/chat_models";
import type { BaseMessage } from "@langchain/core/messages";
import type { ChatResult } from "@langchain/core/outputs";
import { RunnableLambda } from "@langchain/core/runnables";
import { ChatOpenAI } from "@langchain/openai";
import { ChatGPTPlanModel } from "../llm/chatgpt/model.js";
import type { Fetch } from "../llm/chatgpt/oauth.js";
import { ChatGPTPlanError } from "../llm/chatgpt/responses.js";
import {
  ClientConfigError, NotAuthorized, PlanNotEnabled, ReauthorizationRequired, type TokenSource, TransientAuthError, tokenSourceFromEnvironment,
} from "../llm/chatgpt/tokens.js";

/**
 * Which provider serves each role, from the environment:
 * - HANDOFF_MODEL_PROVIDER: openai_chatgpt (default; billed to a ChatGPT plan) or openrouter (paid API).
 *   HANDOFF_<ROLE>_PROVIDER overrides it for one role.
 * - HANDOFF_<ROLE>_MODEL: the model for that role, e.g. HANDOFF_COORDINATOR_MODEL. Never set in code.
 * - HANDOFF_ALLOW_PAID_FALLBACK: "true" lets a failed ChatGPT plan request retry on OpenRouter with
 *   HANDOFF_<ROLE>_FALLBACK_MODEL. Anything else, including unset, means no failure ever reaches a paid provider.
 * Jev is not configured here; its access and billing are separate.
 */
export type Provider = "openai_chatgpt" | "openrouter";
export type Role = "coordinator" | "tenant" | "analyst";

export interface ModelSettings {
  role: Role;
  provider: Provider;
  model: string;
  allowPaidFallback: boolean;
  fallbackModel: string | null;
}

export function settingsFor(role: Role, env: NodeJS.ProcessEnv = process.env): ModelSettings {
  const ROLE = role.toUpperCase();
  const provider = (env[`HANDOFF_${ROLE}_PROVIDER`] ?? env.HANDOFF_MODEL_PROVIDER ?? "openai_chatgpt") as Provider;
  if (provider !== "openai_chatgpt" && provider !== "openrouter") throw new Error(`unknown model provider ${provider}; use openai_chatgpt or openrouter`);
  const model = env[`HANDOFF_${ROLE}_MODEL`];
  if (!model) throw new Error(`set HANDOFF_${ROLE}_MODEL to a model for the ${role}`);
  const allowPaidFallback = provider === "openai_chatgpt" && env.HANDOFF_ALLOW_PAID_FALLBACK === "true";
  const fallbackModel = allowPaidFallback ? env[`HANDOFF_${ROLE}_FALLBACK_MODEL`] ?? null : null;
  if (allowPaidFallback && !fallbackModel) throw new Error(`HANDOFF_ALLOW_PAID_FALLBACK is true but HANDOFF_${ROLE}_FALLBACK_MODEL is not set`);
  return { role, provider, model, allowPaidFallback, fallbackModel };
}

export interface ModelDependencies {
  env?: NodeJS.ProcessEnv;
  tokens?: TokenSource;
  fetch?: Fetch;
  /** Builds a paid model; defaults to OpenRouter. */
  paidModel?: (model: string) => BaseChatModel;
}

/** The chat model for a role. */
export function modelFor(role: Role, deps: ModelDependencies = {}): BaseChatModel {
  const env = deps.env ?? process.env;
  const s = settingsFor(role, env);
  const paid = deps.paidModel ?? ((m: string) => openRouterModel(m, {}, env));
  if (s.provider === "openrouter") return paid(s.model);
  const primary = new ChatGPTPlanModel({ model: s.model, tokens: deps.tokens ?? tokenSourceFromEnvironment(env, deps.fetch), fetch: deps.fetch });
  return s.allowPaidFallback ? new PaidFallbackModel(primary, () => paid(s.fallbackModel!)) : primary;
}

/** A model reached through OpenRouter's OpenAI-compatible API. Paid per token. */
export function openRouterModel(model: string, options: { maxTokens?: number } = {}, env: NodeJS.ProcessEnv = process.env): ChatOpenAI {
  const apiKey = env.OPENROUTER_API_KEY;
  if (!apiKey) throw new Error("OPENROUTER_API_KEY is not set");
  return new ChatOpenAI({ model, apiKey, maxTokens: options.maxTokens, configuration: { baseURL: env.OPENROUTER_BASE_URL ?? "https://openrouter.ai/api/v1" } });
}

/** Failures of the ChatGPT plan path that an explicit paid fallback may take over. Programming errors are not among them. */
export function isPlanFailure(e: unknown): boolean {
  return e instanceof ChatGPTPlanError || e instanceof NotAuthorized || e instanceof PlanNotEnabled ||
    e instanceof ReauthorizationRequired || e instanceof TransientAuthError || e instanceof ClientConfigError;
}

/** Used only when HANDOFF_ALLOW_PAID_FALLBACK is "true". The paid model is built only if it is needed. */
export class PaidFallbackModel extends BaseChatModel {
  private paidInstance: BaseChatModel | null = null;

  constructor(readonly primary: ChatGPTPlanModel, private readonly makePaid: () => BaseChatModel) {
    super({});
  }

  _llmType(): string {
    return "chatgpt-plan-with-paid-fallback";
  }

  private paid(): BaseChatModel {
    return (this.paidInstance ??= this.makePaid());
  }

  override bindTools(tools: any[], kwargs?: any): any {
    const primary = this.primary.bindTools(tools, kwargs);
    return RunnableLambda.from(async (input: BaseMessage[], config) => {
      try {
        return await primary.invoke(input, config);
      } catch (e) {
        if (!isPlanFailure(e)) throw e;
        return this.paid().bindTools!(tools, kwargs).invoke(input, config);
      }
    });
  }

  async _generate(messages: BaseMessage[], options: this["ParsedCallOptions"]): Promise<ChatResult> {
    try {
      return await this.primary._generate(messages, options);
    } catch (e) {
      if (!isPlanFailure(e)) throw e;
      return this.paid()._generate(messages, options);
    }
  }
}
