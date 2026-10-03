import { BaseChatModel } from "@langchain/core/language_models/chat_models";
import { AIMessage, type BaseMessage } from "@langchain/core/messages";
import type { ChatResult } from "@langchain/core/outputs";

type Step = AIMessage | ((messages: BaseMessage[]) => AIMessage);

/** A model that plays a fixed script, one reply per call, and remembers what it was shown. */
export class ScriptedModel extends BaseChatModel {
  readonly seen: BaseMessage[][] = [];
  toolNames: string[] = [];

  constructor(private readonly script: Step[]) {
    super({});
  }

  _llmType(): string {
    return "scripted";
  }

  override bindTools(tools: Array<{ name: string }>): any {
    this.toolNames = tools.map((t) => t.name);
    return this;
  }

  async _generate(messages: BaseMessage[]): Promise<ChatResult> {
    this.seen.push(messages);
    const step = this.script.shift();
    if (!step) throw new Error("the script ran out");
    const message = typeof step === "function" ? step(messages) : step;
    return { generations: [{ text: typeof message.content === "string" ? message.content : "", message }] };
  }
}

let n = 0;
export function calls(...c: Array<[name: string, args: Record<string, unknown>]>): AIMessage {
  return new AIMessage({ content: "", tool_calls: c.map(([name, args]) => ({ name, args, id: `call_${++n}`, type: "tool_call" as const })) });
}

export function say(text: string): AIMessage {
  return new AIMessage(text);
}
