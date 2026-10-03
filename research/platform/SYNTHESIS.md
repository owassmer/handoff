# Agent platform: synthesis of the four evaluations

October 3, 2026. Sources are the four evaluations in this folder, all checked against vendor documentation on that date. **Owen decided the same day: LangGraph is the agent layer** (see HANDOFF_CONTEXT.md). The recommendation below was the coordinator's before that decision.

## What every evaluation found

1. **Nothing on the market supplies the three things our agreements make central.**
   - A business clock that can be driven in a running deployment. Only Temporal can skip time, and only in its test server.
   - Server-side binding of an action to the exact content of an accepted decision.
   - A copy of the whole world at a staged moment: agent state, Handoff's records and the imitated outside systems together.

   Handoff builds these whatever it chooses.
2. **Executions paused inside an engine for weeks are fragile when code changes.** LangGraph checkpoints, ADK sessions, Microsoft workflow checkpoints, Temporal histories, Restate journals and DBOS workflows all carry versioning constraints. Our cases pause for weeks while code ships daily.
3. **Side effects run at least once everywhere.** Payments need our own idempotency keys. Only DBOS writes its checkpoint in the same Postgres transaction as the application's records.
4. **Hosted vendor agent platforms are weak on owned records, data residency and forking, and they churn.**
   - OpenAI retired Assistants, Agent Builder and Evals within 15 months.
   - Letta retired its agent server.
   - Claude Managed Agents is in beta, keeps transcripts with Anthropic, and cannot fork or import a session.

## The architecture this implies

- **Handoff's case runtime is the platform, built around the agent.** It holds:
  - an append-only event inbox per case;
  - the business clock;
  - the world records (tenancy, condition, work, money, account);
  - decisions bound to their content;
  - the imitated outside systems;
  - the operator app, tenant page and email.
- **Each wake is a short agent run rebuilt from those records.** Long waits live as data: pending decisions and clock-driven wake-ups. Code can change between wakes, which avoids finding 2.
- **Inside a run, an agent library supplies the moving parts:** the loop, typed tools, approvals as deferred calls, the provider abstraction, streaming and evaluation. A durable-step layer protects money effects.
- **Whole-world copies come from the database.** When transcripts, step state and records share one Postgres, a database branch captures everything. This is plausible but unproven; prototype it first.

## Finalists for the agent layer

| Option | For | Against |
|---|---|---|
| **Pydantic AI** (Python, MIT, v2 stable June 2026) | Deferred tools end a run with pending approvals or outside results; state stays as data; the run resumes when they arrive. That is the per-wake design. Typed tools. Native multi-provider support, including OpenRouter. Evaluation library. | Almost daily releases. No production users documented in official sources. We build the web layer and streaming. |
| **LangGraph** (Python or TypeScript, MIT library; LangSmith platform optional) | Largest ecosystem and most production evidence. The agent steers within a graph of coordinator and specialists. Interrupts. Postgres checkpointer in our database. Multi-provider. | Resume re-runs code before an interrupt, and replay repeats calls. Checkpoints grow. Survival across code changes is undocumented. Checkpoint durability is partly redundant under per-wake runs. Full LangSmith features are SaaS or Enterprise. |
| **Mastra** (TypeScript, Apache-2.0 core) | Most complete in TypeScript: approvals, signals to wake idle threads, schedules, evaluations, Postgres storage, streaming, server adapters. Same language as the screens. | The long-running pieces are beta. Crash recovery replays tool calls. Mastra owns the schema. |
| **OpenAI Agents SDK** (Python or TypeScript, library only) | Best-documented durable approval (a serialized run state approved per call). Guardrails on every tool call. Generally available with Temporal for Python. | Pre-1.0 churn. Non-OpenAI providers are "best-effort, beta". OpenAI-first defaults. The vendor's record of retiring hosted products. |
| **Our own loop** | Exact fit, no lock-in. | We maintain provider quirks, compaction, streaming and evaluation tooling ourselves. |

**Durable steps:**
- **DBOS** is first. It is a library in our own Postgres, with exactly-once writes alongside our records, `fork_workflow`, an MIT licence and no extra server.
- **Temporal** is second. It is the most proven, but heavier, keeps its history outside our database, and needs versioning work.

**Eliminated:**

| Option | Reason |
|---|---|
| Claude Managed Agents | Claude-only. Transcripts held by Anthropic, US-only at rest, not eligible for zero data retention. Cannot fork or import. |
| Claude Agent SDK | Claude-only, so no model comparison. One command-line subprocess per session. |
| Letta | Its agent server is retired. |
| Convex | Keeps data in its own store even when self-hosted. Proprietary programming model. |
| Cloudflare Agents | No credible self-hosted or VPC deployment. |
| Inngest | Step and run limits; its agent kit has stalled. |
| Microsoft Agent Framework | No TypeScript, no Postgres checkpoint store, durability tied to Azure. |
| Google ADK | The TypeScript version ships only Google's models. The Python version is credible but no better than the finalists. |
| CrewAI | No durable cases. |
| AWS AgentCore | A later VPC target if a customer requires AWS. Its Strands library is model-neutral and worth remembering. |

## Coordinator's recommendation

**A Python service: Pydantic AI, DBOS, and our own case runtime on Postgres. The operator app and tenant page stay in TypeScript and React, against the service's typed API.**

- Pydantic AI's deferred-tool model is the per-wake design.
- Typed tools fit exact money and business records.
- It is model-neutral, including OpenRouter.
- Python matches the legal pipeline and Jev's SDK, so rules and evaluators live in the same language as the agent's tools.
- DBOS keeps money effects exactly-once inside our Postgres and gives a path to whole-world copies.

LangGraph is the close alternative, with more production evidence. A TypeScript-only constraint would point to Mastra or LangGraph JS. A customer mandating AWS would point to Strands on AgentCore.

**Before committing, prototype the same thin slice in Pydantic AI and LangGraph on the same case runtime, taking 2–3 days:**
1. A tenant disputes a charge by email. The case wakes and the agent defends the charge with its evidence.
2. The agent proposes a correction. The operator accepts it a business day later on the simulated clock. The refund is checked against the decision's content and posted exactly once.
3. The whole world is copied at the pending decision, reopened twice, and checked for duplicate effects.
4. The coordinator model is swapped between providers, with the tenant on a different provider.

Compare the code each framework needs, how clear it is, how it behaves on failure, and how much the framework resists per-wake runs.
