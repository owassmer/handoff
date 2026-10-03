# Vendor and cloud agent platforms: evaluation for Handoff

Family: model-vendor and cloud agent platforms and SDKs. Sources accessed 2026-10-03. Ratings: strong / adequate / weak, per CRITERIA.md requirements 1–10.

**Summary.** The libraries in this family (the OpenAI Agents SDK, Strands, the Claude Agent SDK) can run inside Handoff's own service and write to Handoff's own Postgres. The hosted loops (Claude Managed Agents, the AgentCore harness, Foundry hosted agents) are quicker to demo, but each keeps the case transcript in the vendor's store. Two of the requirements count against the Claude options: the simulated tenant must run on a different provider (6), and records must be owned and self-hostable (5). No option here supplies a controllable business clock, a fork of the whole world state, or a decision object bound to its content. Handoff has to build those itself in any case.

---

## 1. OpenAI Agents SDK and OpenAI's platform

**Status.** `openai-agents` (Python) 0.23.1, released 2026-10-02. `@openai/agents` (TypeScript) 0.18.0, released 2026-09-10. Both are MIT-licensed. The SDK is still pre-1.0: the changelog lists breaking changes in minor versions 0.15 through 0.22. Sandbox Agents (persistent isolated workspaces with snapshots) have been in beta since 0.14 (April 2026).

On the platform side, Responses plus Conversations is now the supported path. The Assistants API shut down on 2026-08-26. On 2026-06-03 OpenAI announced that **Agent Builder, the Evals platform and the v1/prompts API** will shut down on **2026-11-30**, with evals going read-only on 10-31. ChatKit stays. The SDK docs name no production users.

| # | Mechanism | Fit |
|---|---|---|
| 1 | The model drives a loop over tools, handoffs and `Agent.as_tool`. Specialists sit under a coordinator. | strong |
| 2 | There is no event bus and no timer. Handoff persists the session and `RunState`, then calls `Runner.run` when an event arrives. The docs list durable integrations with Temporal, DBOS, Restate and Dapr. The clock belongs to Handoff, so it can be controlled. | adequate |
| 3 | A tool can set `needs_approval` (a boolean, or a per-call callable that fails closed). The run returns `interruptions`. `state.approve/reject` acts on one specific call ID. `RunState.to_json()` goes into Handoff's database and can be resumed days later. The docs say to keep the snapshot on the server (it is not authenticated), to consume each pending decision atomically, and to store a version marker. Checking the call against an accepted decision is Handoff's own code. | strong |
| 4 | Tool input and output guardrails run on every function-tool call, with an option to run input checks before approval. Integer money and idempotency are Handoff's code. | strong |
| 5 | Sessions can be stored in SQLAlchemy (Postgres), Redis, MongoDB, Dapr, SQLite, encrypted storage, or OpenAI Conversations. Tracing is **on by default and exports to OpenAI**; it can be turned off or replaced with custom processors, and it is unavailable under ZDR. The library runs anywhere, so self-hosting and VPC deployment are possible. | strong |
| 6 | OpenAI comes first. Other providers connect through OpenAI-compatible clients, a per-agent `Model`, or `MultiProvider` prefixes (the docs show an `openrouter/...` example). The LiteLLM and Any-LLM adapters are "best-effort, beta". Tool search, programmatic tool calling and hosted tools work only on Responses. A tenant on another provider can run in the same process. | adequate |
| 7 | `RunState` and session rows are JSON and can be copied, so a run can be forked at a point. There is no world snapshot and no deterministic replay. OpenAI is withdrawing its Evals platform and recommends Promptfoo instead. | adequate |
| 8 | `run_streamed` streams events, and ChatKit covers chat UI. The tenant page and email are Handoff's to build. | adequate |
| 9 | Python and TypeScript, extensive docs and examples, but fast-moving minor versions. | strong |
| 10 | No license or runtime fees; token costs only. SDK lock-in is low. The hosted platform has removed several products in 2026. | strong |

**Risks.**
- Pre-1.0 churn.
- Non-OpenAI paths are beta.
- Tracing exports to OpenAI by default.
- OpenAI's hosted agent products have a poor 2026 track record (Assistants, Agent Builder, Evals and prompts all retired).

**Verdict.** A good engine to embed in Handoff's own service. Do not build on OpenAI's hosted platform.

## 2. AWS Bedrock AgentCore and Strands Agents

**Status.**
- AgentCore went GA on 2025-10-13.
- Policy (Cedar) went GA 2026-03-03, and Evaluations went GA in March 2026.
- The managed harness entered preview in April 2026 and went GA on 2026-06-17.
- The Runtime **Instances** compute type arrived in August 2026: EC2 in the customer's account, with sessions of up to 14 days.
- Harness lifecycle hooks arrived in September 2026.
- `bedrock-agentcore` SDK 1.24.0 (2026-09-28; PyPI classifier "Alpha").
- Strands: 1.57.2 for Python (2026-10-01) and 1.19.0 for TypeScript; Apache-2.0; "Production/Stable".

Documented user: Swisscom (Runtime, Identity and Memory, with Strands).

| # | Mechanism | Fit |
|---|---|---|
| 1 | Runtime hosts any framework (LangGraph, OpenAI Agents SDK, ADK, Strands, custom code) in a microVM per session. The harness is a loop defined in configuration. Strands runs a model-driven loop and also offers Graph and Swarm. | strong |
| 2 | Work starts on invocation. The microVM stops after 15 idle minutes by default, or at its maximum lifetime (8 hours on microVMs, 14 days on Instances). The session resumes on a new microVM, with state restored from session storage, Memory or Handoff's database. There is no controllable timer: EventBridge and Step Functions run on wall-clock time. | adequate |
| 3 | **Gateway Policy (Cedar)** intercepts every agent-to-tool request and allows or denies it outside the agent's code. Harness hooks call a Lambda that returns allow or deny before each tool call. For human approval, Strands interrupts on `BeforeToolCallEvent` and persists the interrupt through the session manager so the answer can come later. Step Functions can also wrap the harness with an approval step. Nothing provides a decision object bound to its content. | adequate |
| 4 | Strands hooks (which can cancel a tool), Cedar policies and Lambda hooks. All are deterministic. | strong |
| 5 | Memory and Observability (CloudWatch, OTEL) are AWS-managed. Transcripts reach Handoff's Postgres only if Handoff writes them there (Strands supports a custom `Storage` or `SessionRepository`). Runtime supports VPC connectivity, PrivateLink and GovCloud, and Instances run in the customer's own account. AgentCore cannot be self-hosted; Strands can. | adequate |
| 6 | Runtime accepts any model. The harness supports Bedrock, OpenAI, Gemini, LiteLLM and OpenAI-compatible `apiBase` endpoints (which makes OpenRouter possible). Strands supports Bedrock, Anthropic, OpenAI, Google, Ollama and LiteLLM. | strong |
| 7 | Evaluations, batch evaluation, user simulation (May 2026) and A/B testing; Strands snapshot sessions. There is no fork of the world state. | adequate |
| 8 | Streaming invocations and WebSocket shells. The UI is Handoff's. | adequate |
| 9 | Strands has good Python and TypeScript docs. AgentCore is large (12 billable components) and needs a lot of IAM setup for two founders. | adequate |
| 10 | Runtime costs $0.0895 per vCPU-hour and $0.00945 per GB-hour, with no CPU charge during I/O wait. Memory and Gateway are billed per request. Lock-in is low if Runtime only hosts a portable framework, and high if Handoff builds on Memory, Gateway, Policy and the harness. | adequate |

**Risks.**
- Operational burden.
- Deep AWS coupling.
- The harness and Instances are new (both mid-2026).
- AgentCore SDK is still "Alpha" on PyPI.

**Verdict.** Strands as a library is a strong, model-neutral alternative to the OpenAI SDK. AgentCore Runtime or Instances is a credible later home when a customer requires an AWS VPC. Do not make AgentCore Memory the system of record.

## 3a. Claude Agent SDK

**Status.** TypeScript 0.3.288 (2026-10-02) and Python 0.2.163 (2026-09-30). PyPI marks it "Alpha" and the wrapper is MIT-licensed, but the docs say its use is governed by Anthropic's Commercial Terms. The SDK spawns the `claude` CLI as a subprocess. The docs name no third-party production users.

| # | Mechanism | Fit |
|---|---|---|
| 1 | Claude Code's loop, with subagents, skills, MCP and compaction. It is built for agents that work in a filesystem, so Handoff would disable the built-in tools. | strong |
| 2 | There is no event bus. Each active session is one subprocess. A session resumes by ID from the `SessionStore` on any host. The clock is Handoff's. | adequate |
| 3 | `PreToolUse` hooks return allow, deny, ask or **defer**, and can rewrite input with `updatedInput`. The `canUseTool` callback can wait, but only while the process stays alive. `defer` ends the turn with a `deferred_tool_use` and has no timeout. **Caveat:** `defer` is ignored when the model makes several tool calls in one turn, so the permission fallback has to deny by default. | adequate |
| 4 | Hooks run in Handoff's process, which makes them deterministic. | strong |
| 5 | Transcripts are JSONL on local disk, deleted after 30 days by default. A `SessionStore` adapter mirrors them to Postgres; a reference adapter ships with the SDK. The harness can be self-hosted. Inference can go through the Anthropic API, Bedrock, Vertex, Foundry or Claude Platform on AWS, which allows residency in a chosen cloud region. | strong |
| 6 | **Claude only.** The docs say Anthropic does not support routing to non-Claude models through any gateway. The tenant simulator and the OpenRouter service would need a different stack. | weak |
| 7 | `forkSession` rewrites IDs into a new session. This is a fork of the transcript only. | adequate |
| 8 | Messages stream. | adequate |
| 9 | Python and TypeScript, with very thorough docs and very frequent releases. | adequate |
| 10 | The library is free; tokens are the cost. Running one subprocess per session costs memory and operations work. Model lock-in is high. | weak |

**Verdict.** The best hook model in this family, but it locks the coordinator to Claude and the process model is heavy. It fits only if Handoff accepts a Claude-only coordinator and runs the other agents on a different library.

## 3b. Claude Managed Agents

**Status.** Public beta since 2026-04-08, with the `managed-agents-2026-04-01` header.
- Memory reached public beta on 04-23, and multiagent and outcomes followed in May.
- Webhooks arrived on 05-06 and self-hosted sandboxes on 05-19.
- The `auto` permission policy was added on 09-10.
- MCP tunnels and "dreams" are still research previews.

Launch customers: Notion, Rakuten, Asana and Sentry.

| # | Mechanism | Fit |
|---|---|---|
| 1 | Anthropic hosts the loop. A coordinator can call up to 20 roster agents, one level deep, in persistent threads. Outcomes use a rubric grader. | strong |
| 2 | An idle session waits for events, and its sandbox is checkpointed. Handoff can send `user.message`, `system.message` (privileged context) or results from its own tools. Webhooks are only hints: at most 3 attempts, unordered, and then dropped, so Handoff must reconcile. Scheduled deployments run on wall-clock cron, so Handoff owns the clock. Runtime is billed only while the session is running. | adequate |
| 3 | An `always_ask` tool pauses the session with `requires_action`. The approval is bound to the specific `tool_use` event and its input, and the session waits indefinitely. The docs say `auto` is "not a human checkpoint" and that it treats `user.message` as the operator's intent, so untrusted tenant text must not be relayed in a user message. Permission policies do not cover tools Handoff executes itself; that is where Handoff's own decision check belongs. | adequate |
| 4 | Server tools offer only allow, ask or deny. Deterministic checks are possible only inside tools or MCP servers that Handoff runs. | adequate |
| 5 | Anthropic stores the transcripts until they are deleted; Handoff can list the events and copy them. The service is **not eligible for ZDR or a HIPAA BAA**, and data at rest stays in the **US only** (the workspace geo). Self-hosted sandboxes move tool execution only: tool inputs and outputs still pass through Anthropic, and memory stores stay hosted. There is no self-hosted control plane. | weak |
| 6 | Claude only. | weak |
| 7 | No API to fork or snapshot a session. `initial_events` accepts only `user.message` and `define_outcome` events (50 at most), so a case cannot be recreated at a staged point. | weak |
| 8 | SSE streaming with event deltas. | strong |
| 9 | SDKs in eight languages plus a CLI. Fastest path to a demo. | strong |
| 10 | Token costs plus $0.08 per session-hour while running; idle time is free. Rate limits are 300 create and 1,200 read requests per minute. Lock-in is the highest in this family. | weak |

**Verdict.** An impressive hosted loop for a quick pilot, but it does not meet requirements 5, 6 and 7.

## 4. Azure and Google (brief)

**Azure: Foundry Agent Service.** Hosted Agents went GA on 2026-07-09 and run a team's own framework code. Thread storage can be brought into the customer's Cosmos DB, and the standard setup supports a virtual network. Claude has been GA in Foundry since June 2026, alongside Azure OpenAI. This is relevant only if an institutional customer requires Azure, and its storage is Cosmos DB rather than Postgres.

**Google.** Vertex AI is now "Gemini Enterprise Agent Platform", and Agent Engine is now "Agent Runtime". Sessions and Memory Bank went GA on 2025-12-17, and billing began on 2026-01-28. Another researcher covers Google in depth.

## Ranking for Handoff
1. **OpenAI Agents SDK, used as a library in Handoff's own service.** It has the most complete documentation for serializable approval and resume, and Postgres sessions. Non-OpenAI models are beta.
2. **Strands Agents, as a library.** It is the most model-neutral and its versioning is stable. AgentCore Runtime or Instances can host it later when a customer requires a VPC.
3. **Claude Agent SDK.** It has the best deterministic hooks and a Postgres session store, but only Claude can run on it.
4. **AgentCore managed services** (harness, Memory, Gateway, Policy). Cedar gives strong governance, but AWS holds the state.
5. **Claude Managed Agents.** It is beta, runs only Claude, and keeps state at Anthropic in the US, with no fork.
6. **Azure Foundry or Google**, only if a customer requires that cloud.

Whatever Handoff picks, it needs its own Postgres event log, decision records bound to their content, idempotency keys, a business clock it can control (for example Temporal with time skipping, or its own scheduler), and world snapshots.

## Biggest unknown
No vendor in this family shows production evidence or publishes an SLA for a single agent session that stays paused for weeks with an approval pending. Managed Agents documents that a session "waits indefinitely". The AgentCore harness resumes pending inline tool calls by `runtimeSessionId`. I could not confirm that either holds up after days of idleness and across beta API revisions.

## Sources (accessed 2026-10-03)
- OpenAI Agents SDK: [human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/), [models](https://openai.github.io/openai-agents-python/models/), [sessions](https://openai.github.io/openai-agents-python/sessions/), [guardrails](https://openai.github.io/openai-agents-python/guardrails/), [tracing](https://openai.github.io/openai-agents-python/tracing/), [running agents and durable integrations](https://openai.github.io/openai-agents-python/running_agents/), [changelog](https://openai.github.io/openai-agents-python/release/)
- OpenAI platform: [package (PyPI)](https://pypi.org/project/openai-agents/), [package (npm)](https://www.npmjs.com/package/@openai/agents), [deprecations](https://developers.openai.com/api/docs/deprecations), [conversation state](https://developers.openai.com/api/docs/guides/conversation-state), [data controls](https://developers.openai.com/api/docs/guides/your-data)
- AgentCore: [overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), [sessions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html), [lifecycle settings](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-lifecycle-settings.html), [harness hooks](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-lifecycle-hooks.html), [release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html), [Policy GA](https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available/), [harness GA](https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-harness-generally-available/), [pricing](https://aws.amazon.com/bedrock/agentcore/pricing/), [Swisscom case study](https://www.zenml.io/llmops-database/enterprise-agentic-ai-for-customer-support-and-sales-using-amazon-bedrock-agentcore)
- Strands: [interrupts](https://strandsagents.com/docs/user-guide/sdk/interrupts/index.md), [session management](https://strandsagents.com/docs/user-guide/sdk/agents/session-management/index.md), [index](https://strandsagents.com/llms.txt)
- Claude Agent SDK: [overview](https://code.claude.com/docs/en/agent-sdk/overview), [session storage](https://code.claude.com/docs/en/agent-sdk/session-storage), [sessions](https://code.claude.com/docs/en/agent-sdk/sessions), [hosting](https://code.claude.com/docs/en/agent-sdk/hosting), [hooks and `defer`](https://code.claude.com/docs/en/hooks), [LLM gateway](https://code.claude.com/docs/en/llm-gateway), [user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- Claude Managed Agents: [overview](https://platform.claude.com/docs/en/managed-agents/overview), [permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies), [webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks), [self-hosted sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes), [their security model](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security), [multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration), [events and streaming](https://platform.claude.com/docs/en/managed-agents/events-and-streaming), [reference and rate limits](https://platform.claude.com/docs/en/managed-agents/reference)
- Anthropic platform: [pricing](https://platform.claude.com/docs/en/about-claude/pricing), [data residency](https://platform.claude.com/docs/en/manage-claude/data-residency), [data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention), [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws), [release notes](https://platform.claude.com/docs/en/release-notes/overview), [launch coverage](https://itbrief.co.uk/story/anthropic-launches-claude-managed-agents-in-public-beta)
- Azure and Google: [Foundry June 2026](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-june-2026/), [Foundry July–August 2026](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-july-august-2026/), [Cosmos DB thread storage](https://devblogs.microsoft.com/cosmosdb/azure-ai-foundry-connection-for-azure-cosmos-db-and-byo-thread-storage-in-azure-ai-agent-service/), [Google agent release notes](https://docs.cloud.google.com/agent-builder/release-notes)
