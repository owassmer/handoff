import type { BaseChatModel } from "@langchain/core/language_models/chat_models";
import { SystemMessage } from "@langchain/core/messages";
import type { StructuredToolInterface } from "@langchain/core/tools";
import { END, MessagesAnnotation, START, StateGraph } from "@langchain/langgraph";
import { ToolNode, toolsCondition } from "@langchain/langgraph/prebuilt";

/**
 * One wake of the coordinator: it reasons, calls tools, reads their results, and goes on until it
 * answers without a tool call. A tool error goes back to it as a result to reason about, not a crash.
 */
export function coordinatorGraph(model: BaseChatModel, tools: StructuredToolInterface[], system: string) {
  if (!model.bindTools) throw new Error("the coordinator's model must support tool calling");
  const bound = model.bindTools(tools);
  return new StateGraph(MessagesAnnotation)
    .addNode("coordinator", async (state) => ({ messages: [await bound.invoke([new SystemMessage(system), ...state.messages])] }))
    .addNode("tools", new ToolNode(tools, { handleToolErrors: true }))
    .addEdge(START, "coordinator")
    .addConditionalEdges("coordinator", toolsCondition, ["tools", END])
    .addEdge("tools", "coordinator")
    .compile();
}
