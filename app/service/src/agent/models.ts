import { ChatOpenAI } from "@langchain/openai";

/**
 * A chat model reached through OpenRouter's OpenAI-compatible API, so any provider's model can play any
 * role. Model ids come from configuration, never from code, so models can be compared and swapped.
 */
export function openRouterModel(model: string, options: { temperature?: number; maxTokens?: number } = {}): ChatOpenAI {
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) throw new Error("OPENROUTER_API_KEY is not set");
  return new ChatOpenAI({
    model,
    apiKey,
    temperature: options.temperature,
    maxTokens: options.maxTokens,
    configuration: { baseURL: process.env.OPENROUTER_BASE_URL ?? "https://openrouter.ai/api/v1" },
  });
}

/** The model for a role, from an environment variable such as HANDOFF_COORDINATOR_MODEL. */
export function modelFor(role: "coordinator" | "tenant" | "analyst"): ChatOpenAI {
  const variable = `HANDOFF_${role.toUpperCase()}_MODEL`;
  const id = process.env[variable];
  if (!id) throw new Error(`set ${variable} to an OpenRouter model id`);
  return openRouterModel(id);
}
