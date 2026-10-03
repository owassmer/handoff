import type { BaseChatModel } from "@langchain/core/language_models/chat_models";
import { type BaseMessage, HumanMessage } from "@langchain/core/messages";
import type { Queryable } from "../db.js";
import type { CaseTurn } from "../runner.js";
import { buildBrief } from "./brief.js";
import { coordinatorGraph } from "./graph.js";
import { COORDINATOR_PROMPT } from "./prompt.js";
import { coordinatorTools } from "./tools.js";

export interface CoordinatorOptions {
  model: BaseChatModel;
  /** Most model and tool steps in one wake before it is stopped. */
  maxSteps?: number;
  system?: string;
}

/** The coordinator as a case turn: brief, reason and act, record the transcript, summarize. */
export function coordinatorTurn(o: CoordinatorOptions): CaseTurn {
  const system = o.system ?? COORDINATOR_PROMPT;
  return async (ctx) => {
    const brief = await buildBrief(ctx);
    const graph = coordinatorGraph(o.model, coordinatorTools(ctx), system);
    let messages: BaseMessage[] = [new HumanMessage(brief)];
    try {
      for await (const state of await graph.stream({ messages }, { streamMode: "values", recursionLimit: o.maxSteps ?? 60 })) {
        messages = state.messages;
      }
    } finally {
      await saveTranscript(ctx.db, ctx.runId, system, messages);
    }
    const last = messages.at(-1);
    const summary = last?.getType() === "ai" ? textOf(last) : "";
    if (summary) await ctx.note("wake.summary", { text: summary });
  };
}

function textOf(m: BaseMessage): string {
  return typeof m.content === "string" ? m.content : m.content.map((p) => ("text" in p && typeof p.text === "string" ? p.text : "")).join("");
}

async function saveTranscript(q: Queryable, runId: string, system: string, messages: BaseMessage[]): Promise<void> {
  const rows: Array<{ role: string; content: unknown }> = [{ role: "system", content: { text: system } }];
  for (const m of messages) {
    const type = m.getType();
    if (type === "human") rows.push({ role: "user", content: { text: textOf(m) } });
    else if (type === "ai") rows.push({ role: "assistant", content: { text: textOf(m), toolCalls: (m as { tool_calls?: unknown[] }).tool_calls ?? [] } });
    else if (type === "tool") rows.push({ role: "tool", content: { name: (m as { name?: string }).name, toolCallId: (m as { tool_call_id?: string }).tool_call_id, text: textOf(m) } });
  }
  for (const [seq, r] of rows.entries()) {
    await q.query(`insert into run_messages (run_id, seq, role, content) values ($1, $2, $3, $4)`, [runId, seq, r.role, r.content]);
  }
}
