# Graph- and workflow-based agent frameworks: evaluation for Handoff

Family: LangGraph (+ LangSmith Deployment), Google ADK (+ Agent Runtime, formerly Vertex AI Agent Engine), Microsoft Agent Framework (+ Foundry Agent Service), LlamaIndex Workflows. Brief: `CRITERIA.md`. All sources accessed 2026-10-03. Version numbers and dates come from PyPI/npm registry metadata pulled that day.

Ratings: S = strong, A = adequate, W = weak. "Documented" means the vendor docs describe it; "demonstrated" means public evidence of production use. Unless stated, everything below is documented only.

---

## 1. LangGraph + LangSmith Deployment

**Status.** MIT-licensed library. Python `langgraph` 1.2.12 (2026-09-21); JS `@langchain/langgraph` 1.4.18 (2026-09-25). 1.0 shipped 2025-10-22 with a no-breaking-changes policy until 2.0. 1.2 (May 2026) added `DeltaChannel` (beta), which stores incremental state deltas instead of full state per step. Postgres checkpointer: `langgraph-checkpoint-postgres` 3.1.2 (Py), 1.0.5 (JS). The hosted product is now called **LangSmith Deployment**, and its runtime is **Agent Server** (`langgraph-api` 0.15.1, **Elastic-2.0** licence, not OSI open source). LangChain's site names Uber, Lyft, Coinbase, Rippling, Harvey, Workday, Elastic and ServiceNow as production users. These are vendor claims.

| # | Fit | Mechanism / evidence |
|---|---|---|
| 1 Agent-led | **S** | Nodes can be agents. Routing can be decided at runtime by conditional edges or by a node returning `Command(goto=…)`, and `Send` fans out dynamically. Prebuilt agent loop, subgraphs, supervisor patterns. The graph can be as small as "agent + tools", so it does not force a fixed pipeline. |
| 2 Waking | **A** | One case = one `thread_id`. Every event becomes a new run on that thread: `Command(resume=…)` answers a pending `interrupt()`, otherwise the event is new input. Docs: "Graph waits indefinitely until you resume." The OSS library has **no timer primitive**. Agent Server has `after_seconds` delayed runs and cron jobs "interpreted in UTC". Both run on the wall clock, so a simulated clock means building your own deadline dispatcher. Agent Server `multitask_strategy` (reject/interrupt/rollback/enqueue) handles events that arrive while a run is busy. Without Agent Server you serialise those yourself. |
| 3 Operator authority | **A** (primitive only) | `interrupt()` and `HumanInTheLoopMiddleware` support approve, edit, reject and respond. The resume value is supplied by the client, and the docs leave authorization to the developer. Checking that an accepted decision matches the action, and defending against prompt injection, must happen in Handoff's own tool layer. |
| 4 Deterministic checks | **A** | Deterministic nodes are plain code. Two hazards: (a) on resume "the node restarts from the beginning… any code before the `interrupt()` runs again", and (b) replay "re-executes nodes… LLM calls, API requests… fire again". Side effects need idempotency keys. |
| 5 Owned records | **S** agent state / **A** audit | `PostgresSaver` writes checkpoints into **your** Postgres, which can be the same database as the case records. Checkpoints are serialized blobs, not a relational audit log, and docs advise retention policies because they grow. The library self-hosts anywhere for free. Self-hosting Agent Server needs a LangSmith licence key (Standalone) or the Enterprise plan (self-hosted control plane). Self-hosted LangSmith is Enterprise-only. |
| 6 Multi-provider | **S** | Provider-neutral chat-model packages (OpenAI, Anthropic, Google, OpenAI-compatible endpoints such as OpenRouter). Each node or agent can use a different model. |
| 7 Simulation / fork | **A→S** | Time travel: `get_state_history`, replay from a `checkpoint_id`, fork via `update_state`, which "creates a new checkpoint that branches". Agent Server `POST /threads/{id}/copy` copies the **full** checkpoint history. A May 2026 forum thread reports 12+ minute copies on large threads, and the suggested workaround is a shallow `threads.create(supersteps=…)`. Forks cover agent state only, not records or simulators, but because checkpoints can live in the app's database, one database snapshot gives a consistent fork of the whole world. LangSmith provides datasets, experiments and LLM judges. `openevals` provides `run_multiturn_simulation` and `create_llm_simulated_user`. |
| 8 Surfaces | **S** | Stream modes (values, updates, messages, custom), typed v2 streaming since 1.1. Agent Server streams over SSE with Redis pub/sub. JS `useStream` hook. Email is up to the app. |
| 9 Velocity | **S** | TypeScript and Python are both first-class. Largest docs and community in this family, and well known to AI coding agents. Risks: confusing layering (LangChain `create_agent` vs LangGraph vs Deep Agents) and churn in the surrounding packages. |
| 10 Lock-in / cost | **A** | The library is MIT. Code is shaped around LangGraph's API, so leaving means a moderate rewrite, but the state already sits in your Postgres. LangSmith: Developer $0 (5k base traces/mo), Plus $39/seat (10k), Enterprise custom (required for self-hosted/hybrid). Pricing moved to LCU/LSU units in July 2026. The production Agent Server is paid. |

**Weaknesses and risks.** No timers or business clock. Re-execution semantics on resume. Checkpoint tables grow. Thread copy is slow on large threads. `DeltaChannel` is still beta. Agent Server is source-available and requires a licence. Replay is re-execution, not deterministic playback.

**Verdict: strong.** Use the OSS library with a self-run `PostgresSaver` in Handoff's own Postgres, and own the event intake, deadline scheduler and authority gate. Agent Server is optional and can be added later.

Sources: https://docs.langchain.com/oss/python/langgraph/interrupts · https://docs.langchain.com/oss/python/langgraph/use-time-travel · https://docs.langchain.com/oss/python/langgraph/persistence · https://docs.langchain.com/oss/python/langchain/human-in-the-loop · https://docs.langchain.com/langsmith/deployments · https://docs.langchain.com/langsmith/deploy-standalone-server · https://docs.langchain.com/langsmith/cron-jobs · https://reference.langchain.com/python/langgraph-sdk/_async/runs/RunsClient/create · https://forum.langchain.com/t/langgraph-thread-copy-can-take-12-minutes-recommended-production-pattern/3763 · https://www.langchain.com/pricing · https://www.langchain.com/langgraph · https://docs.langchain.com/langsmith/multi-turn-simulation · https://github.com/langchain-ai/langgraph/releases · https://pypi.org/project/langgraph-api/ · https://usagepricing.com/blueprint/activity/langsmith-2026-07-21-price-change (secondary)

---

## 2. Google ADK + Agent Runtime (Gemini Enterprise Agent Platform)

**Status.** Apache-2.0. ADK 2.0 reached GA for Python on 2026-05-19, Go on 2026-06-30 and TypeScript on 2026-08-21. 2.0 adds a graph workflow runtime, "dynamic workflows" written in code, and a Task API for coordinator/sub-agent delegation. It also brings breaking changes: `BaseAgent` now subclasses `BaseNode`, and the event schema changed. Current versions: `google-adk` 2.11.0 (2026-10-02), `@google/adk` 2.2.0 (2026-09-30). In April 2026 Vertex AI became the **Gemini Enterprise Agent Platform**. Agent Engine was renamed **Agent Runtime**, and Sessions and Memory Bank became "Agent Platform Sessions/Memory Bank" (both GA since 2025-12-17). I found no independently documented production users of ADK 2.0.

| # | Fit | Mechanism / evidence |
|---|---|---|
| 1 Agent-led | **S** | An `LlmAgent` with sub-agents chooses transfers itself. Agents can be wrapped as tools (`AgentTool`), and the Task API supports a coordinator with sub-agents. Graph workflows route by explicit route values that nodes emit against a fixed edge set ("LLM agents do not autonomously choose the next node"), so steering should live in an agent node, or in a dynamic workflow, rather than in the graph. |
| 2 Waking | **A** | Human-in-the-loop uses `RequestInput` nodes, tool confirmation and long-running function tools, persisted as session events. Google's own pattern (blog, 2026-05-12): a webhook loads the session from storage and resumes. The blog describes no timer mechanism, and none exists, so Handoff must own the clock. `ResumabilityConfig` (Py ≥1.16) recovers after crashes. |
| 3 Operator authority | **A** (primitive only) | Tool confirmation flow. A `RequestInput` response schema "does not reformat… the reply must already be in that format", so validation is the app's job. GCP-managed "semantic governance policies" exist on Agent Gateway (VPC-SC support in Preview, 2026-09-25). They are managed-only and not self-hostable. |
| 4 Deterministic checks | **A** | Function nodes run plain code. Resume is **at-least-once**: "If your agent uses Tools where duplicate runs would have a negative impact, such as purchases, you should modify the Tool." |
| 5 Owned records | **A** | `DatabaseSessionService` stores events and state in Postgres, MySQL or SQLite. Python uses SQLAlchemy; TS uses MikroORM with a Postgres peer dependency. The event list works well as an append log. Caveat from the docs: "State updates, artifact updates, and event persistence are not performed in a single atomic transaction." ADK runs in any container. Agent Runtime, Sessions and Memory Bank are GCP-only. |
| 6 Multi-provider | **A** in Py / **W** in TS | Python supports Gemini and Claude natively, plus a LiteLLM connector that covers OpenRouter. LiteLLM had a PyPI supply-chain compromise on 2026-03-24 (1.82.7/1.82.8), so pin and audit it. TS `@google/adk` 2.2.0 ships only Gemini and Apigee model classes. Other providers need a custom `BaseLlm` or a third-party bridge such as `adk-llm-bridge`. |
| 7 Simulation / fork | **A** | Built-in evaluation: evalsets, tool-trajectory and rubric LLM judges, **user simulation**, `adk eval`, conformance tests, pytest. **No session copy or fork**, only rewind (Py ≥1.17), which "does not manage external dependencies". Whole-world forks would need a database snapshot, as with LangGraph. |
| 8 Surfaces | **A** | `adk web` dev UI and an API server with SSE. The assistant-ui adapter is at 0.0.33, i.e. early. |
| 9 Velocity | **A** | Python docs are good. TS 2.0 has only been GA since August. 2.0 introduced breaking changes, and docs lean toward Gemini and GCP. |
| 10 Lock-in / cost | **A** | ADK itself is portable. Agent Runtime pricing, as of 2026-09-01: Agent Storage $0.30/GiB-month; Agent Compute $0.085/vCPU-h, charged per 1M session writes or 3M reads. Adopting Memory Bank, Agent Gateway or governance pulls Handoff toward GCP. |

**Weaknesses and risks.** Gemini-first. No non-Gemini models in TS without extra work. No timers, no fork. At-least-once tool execution. API churn from 2.0. Managed safety features only exist inside GCP.

**Verdict: adequate.** A credible choice if Handoff picks Python and is comfortable leaning toward GCP. In TypeScript it is weaker than LangGraph on model neutrality and maturity.

Sources: https://adk.dev/2.0/ · https://adk.dev/graphs/ · https://adk.dev/graphs/human-input/index.md · https://adk.dev/runtime/resume/ · https://adk.dev/sessions/session/ · https://adk.dev/sessions/session/rewind/ · https://adk.dev/agents/models/ · https://adk.dev/evaluate/ · https://adk.dev/integrations/dbos/index.md · https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/ · https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes · https://cloud.google.com/vertex-ai/pricing · https://www.npmjs.com/package/@google/adk · https://github.com/google/adk-python · https://www.arthur.ai/column/litellm-supply-chain-attack-pypi-compromise-2026 (secondary)

---
## 3. Microsoft Agent Framework + Foundry Agent Service

**Status.** MIT. 1.0 went GA on 2026-04-03 for **.NET and Python**. A Go SDK entered public preview on 2026-07-10. **There is no TypeScript SDK.** Python `agent-framework` is at 1.20.0 (2026-10-02), but many integrations are still pre-release: `-anthropic` 1.0.0b, `-durabletask` 1.0.0b, `-azure-cosmos` 1.0.0b, and `-postgres` 1.0.0a (a pgvector store only). Agent Framework is the declared successor to Semantic Kernel and AutoGen. AutoGen has been in maintenance since October 2025, and Semantic Kernel now gets only critical fixes (secondary source). Foundry **Hosted Agents** went GA on 2026-07-09.

| # | Fit | Mechanism / evidence |
|---|---|---|
| 1 Agent-led | **A** | Workflows are built from executors with typed edges, switch-case edges and fan-out/fan-in, and agents can act as executors. The orchestrations add handoff (agents decide handoffs), group chat and **Magentic** (a manager agent plans dynamically). Microsoft's own docs reserve workflows for "fixed graph topologies" and point to orchestrations for imperative coordination. |
| 2 Waking | **A** | `ctx.request_info()` / `RequestPort` pauses a run. Pending requests are saved in checkpoints and "re-emitted" on restore, and a run resumes via `run(checkpoint_id=…, responses=…)`. Python checkpoint stores: in-memory, file and **Cosmos DB only**, so Postgres needs a custom `CheckpointStorage`. Durable timers and "waits that can last hours, days, or weeks" come from the Durable Task extension. Its portable SDKs use only the **Azure-managed Durable Task Scheduler** ("Azure connectivity required"; there is a local emulator). Timers run on orchestration wall-clock time, and entity state is capped at 1 MB. |
| 3 Operator authority | **A** (primitive only) | Tool approval (`function_approval_request`) and RequestPorts. Enforcement is up to the app. |
| 4 Deterministic checks | **A** | Executors are plain code run in supersteps. Durable orchestrations must be deterministic code, and Durable Task activities run at-least-once. |
| 5 Owned records | **W/A** | Checkpoints are pickled (behind a restricted unpickler) to file or Cosmos. The durable path relies on an Azure service. In-process workflows can be self-hosted. |
| 6 Multi-provider | **A** | Foundry, Azure OpenAI, OpenAI, Anthropic, Bedrock, Gemini and Ollama. OpenRouter works through the OpenAI-compatible client. The Python Anthropic package is still beta. |
| 7 Simulation / fork | **A** | A checkpoint can be rehydrated into a new workflow instance, which works as a fork, as long as the topology and executor IDs are identical. Since Python 1.13.0, entry checkpoints make "the complete workflow run replayable". Evaluations run through Foundry (Preview). I found no built-in user simulator. |
| 8 Surfaces | **A** | Streaming workflow events. AG-UI/CopilotKit adapters and DevUI are in Preview. |
| 9 Velocity | **W** | No TypeScript. Python integrations are pre-release, and checkpoint semantics changed in 1.13. |
| 10 Lock-in / cost | **A** | The core is MIT, but production storage and durability lean on Azure (Cosmos, Durable Task Scheduler, Foundry). Foundry prompt agents and workflows carry no charge; Hosted Agents are billed by container compute. |

**Verdict: weak to adequate.** The workflow engine is capable, but it has no TS SDK, Postgres is not a first-class store, and its durable timer path depends on Azure.

Sources: https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/ · https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints · https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop · https://learn.microsoft.com/en-us/agent-framework/workflows/ · https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-agents-microsoft-agent-framework · https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-storage-providers?pivots=durable-task-sdks · https://devblogs.microsoft.com/go/microsoft-agent-framework-for-go-public-preview/ · https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-july-august-2026/ · https://azure.microsoft.com/pricing/details/foundry-agent-service/ · https://pypi.org/project/agent-framework-postgres/ · https://atlan.com/know/ai-agent/what-is-autogen/ (secondary)

---

## 4. LlamaIndex Workflows (brief)

**Status.** MIT, Python. `llama-index-workflows` is at 2.25.0 (2026-09-25). The TS `@llamaindex/workflow-core` was last published at 1.3.4 on 2026-03-09, so it lags.

**Mechanisms.** Steps are event-driven: the type of event a step emits at runtime picks the next step, so routing is dynamic. `AgentWorkflow` supports handoffs. For human input, `InputRequiredEvent` and `HumanResponseEvent` (or `ctx.wait_for_event`) pause a run. To persist across restarts you store `ctx.to_dict()` yourself and restore with `Context.from_dict`. Alternatively, `llama-agents-dbos` journals each step completion to SQLite or Postgres and releases idle workflows after `idle_timeout`. Models are broadly provider-neutral. There is no timer primitive; DBOS added wall-clock delay scheduling in April 2026. There are no fork or simulation harnesses comparable to LangGraph's or ADK's.

**Ratings.** Requirements 1, 6 and 9 (Python only): A. Requirements 2 and 5: A, via DBOS on Postgres. Requirements 3 and 4: A, as primitives only. Requirements 7 and 8: W. Requirement 10: S (MIT, light footprint). **Verdict: weak to adequate.** A lightweight Python orchestrator with too little platform around it for Handoff.

Sources: https://pypi.org/project/llama-index-workflows/ · https://developers.llamaindex.ai/python/llamaagents/workflows/human_in_the_loop/ · https://developers.llamaindex.ai/python/llamaagents/workflows/dbos/ · https://www.dbos.dev/blog/dbos-new-features-april-2026

---

## Cross-cutting findings for Handoff

1. **No option provides a controllable clock.** Every timer that exists (LangGraph `after_seconds` and UTC cron, Durable Task timers, DBOS delays) runs on the wall clock. Handoff should keep a `deadlines` table in Postgres driven by its own business clock and deliver each wake-up as an ordinary event. This also keeps the 21-day statutory deadline logic deterministic and testable.
2. **No option enforces operator authority.** Resume and approval payloads come from the client. The framework pause should carry only a decision reference. A server-side tool gateway then checks the accepted decision in Postgres, including that its content matches, before committing money.
3. **Forking the whole world.** The frameworks fork agent state only. The practical route is to keep checkpoints or sessions in the same Postgres as the records and simulator state, then snapshot the database (template database or a per-case schema copy). That favours LangGraph `PostgresSaver` and ADK `DatabaseSessionService`. It counts against MAF (file, Cosmos or Durable Task Scheduler) and against managed sessions (Agent Runtime, Foundry, Agent Server copy).
4. **Re-execution is the norm.** LangGraph re-runs a node on resume, and ADK resume and Durable Task activities are at-least-once. Idempotency keys on every side effect are mandatory regardless of which option is chosen. Deterministic replay needs recorded model and tool responses in all four.

## Ranking for Handoff

1. **LangGraph** (OSS library + `PostgresSaver`, self-run; Agent Server optional). Fits best on steering, TS/Python parity, provider neutrality, Postgres-native state and fork/time-travel primitives.
2. **Google ADK** (Python). Best built-in evaluation and user simulation. Weaker on TS models and forking, and pulls toward GCP.
3. **Microsoft Agent Framework.** A solid workflow engine, but no TS, no first-class Postgres store, and durable timers tied to Azure.
4. **LlamaIndex Workflows.** Clean and lightweight, but too little platform for the requirements.

**Most important unknown.** I could not verify how LangGraph's Postgres checkpointer behaves for **weeks-long, event-heavy threads**: storage growth, `DeltaChannel` (still beta) correctness, resume latency and fork cost at hundreds or thousands of checkpoints per case. I found no public production evidence at that duration, only vendor customer logos and a forum report of 12-minute thread copies. Handoff should measure this in a spike before committing.
