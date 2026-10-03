# Stateful-agent platforms and application-level frameworks: evaluation for Handoff

All sources were accessed on 2026-10-03. Ratings: S = strong, A = adequate, W = weak.

**The main finding is about Letta.** The thing the brief describes, a Postgres-backed server that keeps agents as persistent entities, has been retired:
- The README was switched to the Letta Agent SDK on 2026-07-03.
- The repo was marked "archive the legacy server repository" on 2026-08-16.
- AGENTS.md now says the old server "is unsupported, receives no fixes or security updates" and forbids using it in production.

Every other option still needs Handoff to build its own case runtime: an event inbox, a business clock, decision binding and a world fork. None of them provides these.

---

## 1. Letta

**What it is now.** Letta Code is an agent harness with an App Server, a TypeScript Agent SDK and Letta Cloud. The `letta` package on PyPI is at 0.34.2 (2026-10-02). The legacy server's last release was v0.16.8.
- The App Server exposes "one bidirectional WebSocket at `/ws`".
- State lives either in Letta Cloud or in a "local" backend. The local backend is MemFS, "a git-tracked collection of Markdown files" under `~/.letta/lc-local-backend`. It does not use Postgres.
- The old Docker image "is no longer an actively maintained or supported Letta product surface".
- Pricing now redirects to Letta Code pricing. The API plan is $20/month plus $0.10 per active agent per month.

| Req | Mechanism | Fit |
|---|---|---|
| 1 Long-lived cases | Persistent agents with memory and subagents. Product focus is now coding and personal agents. | A |
| 2 Waking | Cloud cron schedules on the wall clock (`letta cron`); no event inbox, no controllable clock | W |
| 3 Operator authority | Tool approval documented in the SDK; binding approvals to decisions would be custom; state is outside your server | W |
| 4 Deterministic checks | Custom tools only | W |
| 5 Owned records | Git/Markdown files or Letta Cloud; no Postgres | W |
| 6 Multiple providers | BYOK, "model agnostic" | S |
| 7 Simulation/eval | "The Agent SDK does not currently expose AgentFile import or export"; conversation forking existed in legacy v0.16.7; no eval tooling | W |
| 8 Surfaces | WebSocket streaming; Slack/Telegram channels | A |
| 9 Team/velocity | Heavy churn (two architectures in 2026) | W |
| 10 Lock-in/cost | Apache-2.0, but tied to the harness and Cloud | W |

**Verdict: weak. Do not adopt.** Being a stateful agent server is no longer the product's focus.

Sources: https://github.com/letta-ai/letta , https://github.com/letta-ai/letta/commits/main , https://raw.githubusercontent.com/letta-ai/letta/main/AGENTS.md , https://docs.letta.com/self-hosting , https://docs.letta.com/self-hosting/app-server , https://docs.letta.com/v1-sdk/docker/index.md , https://docs.letta.com/reference/faq/index.md , https://docs.letta.com/letta-code/pricing , https://docs.letta.com/letta-code/scheduling

## 2. Mastra (TypeScript)

**Status.** @mastra/core is at 1.74.0 (2026-10-01). Version 1.0 was announced 2026-01-20, and releases come roughly weekly (1.63 on Aug 26 through 1.74 on Oct 1).
- Adoption: 28.5k stars and about 2.19M npm downloads a week.
- Production users named by Mastra: Replit, PayPal, Sanity, Marsh McLennan.
- License: Apache-2.0, except `ee/` directories (auth, agent-builder, editor), which carry an enterprise license.

| Req | Mechanism | Fit |
|---|---|---|
| 1 Long-lived cases | Agents with tools and subagents; graph workflows for fixed parts; "Harness" with durable agents, background tasks and AgentController | S |
| 2 Waking | Signals (`sendSignal`, `sendNotificationSignal`) "wake an idle thread", with a notification inbox in Postgres. Schedules are persisted crons. Workflows have `.sleep/.sleepUntil`. Signals and durable agents are labelled **Beta**. No injectable clock is documented. | A |
| 3 Operator authority | `requireApproval` per tool, or a `requireToolApproval` async function; suspended runs survive restarts with storage; `listSuspendedRuns()`; resume by `runId`/`toolCallId`. Checking that an action matches an accepted decision must be done in your tool code. | A |
| 4 Deterministic checks | Tools run your code. Concurrent `resume()` was fixed in 1.61 to claim the run atomically. But durable recovery "can reissue LLM calls … and re-execute tool calls", so you need your own idempotency keys. | A |
| 5 Owned records | `PostgresStore` holds memory, workflow snapshots, traces, scores, schedules, threadState and more. Composite storage can split domains across stores. Mastra owns the schema, and it is not append-only. | S |
| 6 Multiple providers | Model router ("212+ providers") including `openrouter/...` | S |
| 7 Simulation/eval | Datasets, experiments and scorers, with comparison in Studio. Workflow "time travel" re-runs a step inside the same run rather than forking it. No world fork. | A |
| 8 Surfaces | Server adapters (Express, Hono, Fastify, Koa); resumable streams via `observe(runId)`; Slack/Teams/Discord channels; no native email | S |
| 9 Team/velocity | TypeScript, good docs, large ecosystem; risk from fast-changing beta APIs | S |
| 10 Lock-in/cost | Self-hostable, data in your Postgres; moderate API lock-in to workflows and harness | A |

**Weaknesses.**
- The long-running pieces Handoff most needs (signals, durable agents) are beta, and breaking changes can land in minor versions.
- Crash recovery replays tool calls.
- Timers run on the wall clock.

**Verdict: adequate to strong.** It is the most complete option in this family for TypeScript.

Sources: https://github.com/mastra-ai/mastra/releases , https://mastra.ai/blog/announcing-mastra-1 , https://mastra.ai/docs/long-running-agents/durable-agents.md , https://mastra.ai/docs/harness/signals.md , https://mastra.ai/docs/harness/schedules.md , https://mastra.ai/docs/agents/agent-approval.md , https://mastra.ai/docs/storage.md , https://mastra.ai/docs/workflows/time-travel.md , https://mastra.ai/docs/evals/experiments.md , https://mastra.ai/models/gateways/openrouter , https://github.com/mastra-ai/mastra/blob/main/LICENSE.md , https://newreleases.io/project/github/mastra-ai/mastra/release/@mastra%2Fcore@1.61.0

## 3. Pydantic AI (Python)

**Status.** Version 2.53.0 (2026-10-02). v2 went stable on 2026-06-23, and v1 still gets security backports (1.107.7 on Sep 29).
- Release cadence is close to daily.
- 20.4k stars and about 1.34M PyPI downloads a week.
- License MIT; the core package is classified "Production/Stable".
- The first-party Pydantic AI Harness is 0.x and classified **Alpha**.
- No production users are documented in official sources.

| Req | Mechanism | Fit |
|---|---|---|
| 1 Long-lived cases | Agent loop with typed tools; delegation to subagents; pydantic-graph (its newer builder API is still labelled beta) | S |
| 2 Waking | No built-in inbox. Deferred tools end a run, and you resume it whenever the event arrives. `CallDeferred` covers results coming from outside systems. Durability comes from Temporal, DBOS, Prefect, Restate or Lambda. Temporal's test server can skip time; DBOS has durable sleep and cron, backed by Postgres. | A |
| 3 Operator authority | `requires_approval` or `ApprovalRequired` makes the run end with `DeferredToolRequests`. You resume later with message history plus `DeferredToolResults` (`ToolApproved`/`ToolDenied`, optional `override_args`), with no documented time limit. `args_validator` runs before approval. `ToolCallJudge` was added in v2.53. | S |
| 4 Deterministic checks | Pydantic-validated arguments; Harness StepPersistence keeps a ledger of tool effects; DBOS and Prefect step semantics help with idempotency | S |
| 5 Owned records | Message history serialises to your Postgres via `ModelMessagesTypeAdapter`; DBOS uses Postgres. StepPersistence has no Postgres store yet (SQLite, file, Mongo only). The Logfire server is closed-source, but output is plain OpenTelemetry. | S |
| 6 Multiple providers | Native providers plus `OpenRouterModel` | S |
| 7 Simulation/eval | pydantic-evals (Datasets, Cases, Evaluators, LLMJudge); StepPersistence `fork_run()`; DBOS `fork_workflow(start_step)`. These fork runs, not the whole world. | A |
| 8 Surfaces | You build the web layer. DBOS-wrapped streams are "buffered rather than delivered in real time". | A |
| 9 Team/velocity | Python, good docs, high velocity, lots of churn | S |
| 10 Lock-in/cost | MIT, low lock-in; Logfire optional (from $49/month, enterprise self-host on request) | S |

**Weaknesses.**
- It is a library, not a platform: the inbox, scheduling and UI are yours to build.
- Picking a durability engine adds a choice and infrastructure; Temporal is heavy.
- The Harness is alpha.
- `DBOSAgent` "will be removed in v3".

**Verdict: strong as the agent layer inside a case runtime you own.**

Sources: https://github.com/pydantic/pydantic-ai/releases , https://github.com/pydantic/pydantic-ai/releases/tag/v2.53.0 , https://pydantic.dev/docs/ai/project/changelog/ , https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/ , https://pydantic.dev/docs/ai/capabilities/durable_execution/overview/ , https://pydantic.dev/docs/ai/capabilities/durable_execution/dbos/ , https://pydantic.dev/docs/ai/harness/step-persistence/index.md , https://pydantic.dev/docs/ai/evals/evals/ , https://pydantic.dev/docs/ai/models/openrouter/ , https://docs.dbos.dev/python/tutorials/workflow-management , https://docs.temporal.io/develop/python/testing-suite , https://pydantic.dev/articles/logfire-pricing-change

## 4. Convex Agent and Workflow (TypeScript, reactive database)

**Status.**
- `@convex-dev/agent` 0.7.3 (2026-09-14), still pre-1.0, about 246k downloads a week. 0.6.0 required AI SDK v6 and 0.7.0 requires AI SDK v7.
- `@convex-dev/workflow` 0.4.8 (2026-09-15).
- The backend is licensed FSL-1.1-Apache-2.0: it is not open source until two years after each release, and competing uses are barred.
- Self-hosting is Docker on SQLite, Postgres or MySQL, and it "supports all the free-tier features" of the cloud.

| Req | Mechanism | Fit |
|---|---|---|
| 1 Long-lived cases | Persisted threads and messages; agents callable from any action | A |
| 2 Waking | Workflow `step.awaitEvent`/`sendEvent`, `step.sleep`, scheduler `runAt`. Wall clock only; fake timers exist only in the `convex-test` mock. | A |
| 3 Operator authority | `needsApproval`, `approveToolCall`, `denyToolCall` (since 0.6.0). But the changelog says it will "auto-deny unresolved approvals when new generation starts", which would collide with events arriving while an approval is pending. | W–A |
| 4 Deterministic checks | ACID, serializable mutations are good for exact money and idempotency keys. Workflows must be deterministic, with a 1 MB journal per step and an 8 MiB total limit. | S |
| 5 Owned records | Even when self-hosted on Postgres, data sits in Convex's internal serialized document store, not in tables you can query. Export is a backup zip or Fivetran/Airbyte. | W |
| 6 Multiple providers | AI SDK v7 providers | S |
| 7 Simulation/eval | Backup and restore of a whole deployment (beta) could in principle fork world state; not verified for component tables. Agent playground; no eval framework. | A |
| 8 Surfaces | Reactive queries give excellent live operator UIs; HTTP actions handle webhooks | S |
| 9 Team/velocity | Strong developer experience; agent component still churns | A |
| 10 Lock-in/cost | Proprietary programming model; leaving means rewriting the data layer | W |

**Verdict: adequate for a demo, weak for Handoff's requirements on owned records and lock-in.**

Sources: https://docs.convex.dev/agents , https://raw.githubusercontent.com/get-convex/agent/main/CHANGELOG.md , https://github.com/get-convex/workflow , https://github.com/get-convex/convex-backend , https://raw.githubusercontent.com/get-convex/convex-backend/main/LICENSE.md , https://raw.githubusercontent.com/get-convex/convex-backend/main/self-hosted/README.md , https://docs.convex.dev/database/import-export/ , https://docs.convex.dev/testing/convex-test , https://discord-questions.convex.dev/m/1364200522608939089

## 5. CrewAI (brief)

**Status.** Version 1.15.23 (2026-09-28), MIT, 59.3k stars, about 575k downloads a week. CrewAI AMP is a commercial control plane.

| Req | Mechanism | Fit |
|---|---|---|
| 1 Long-lived cases | Flows (`@listen`/`@router`) plus role-based Crews | A |
| 2 Waking | No external inbox | W |
| 3 Operator authority | `@human_feedback` with an async provider returns `HumanFeedbackPending`; state is persisted automatically and resumed with `resume_async()` | A |
| 4 Deterministic checks | Custom code | A |
| 5 Owned records | `@persist` defaults to SQLite; a custom FlowPersistence is needed for Postgres | W |
| 6 Multiple providers | Many providers | S |
| 7 Simulation/eval | `restore_from_state_id` forks flow state | A |
| 8 Surfaces | None built in | W |
| 9 Team/velocity | Python, popular | A |
| 10 Lock-in/cost | MIT core; AMP upsell | A |

**Verdict: weak.** The crew metaphor adds abstraction without solving durable cases.

Sources: https://github.com/crewAIInc/crewAI , https://docs.crewai.com/en/concepts/flows , https://docs.crewai.com/edge/en/learn/human-feedback-in-flows

## 6. Build our own (baseline)

**What the team would build.** A custom agent loop over provider APIs inside the company's own service:
- `cases`, `events` (an append-only inbox), `decisions`, `actions` (with idempotency keys) and `transcripts` tables in Postgres.
- A Postgres job queue (pg-boss or graphile-worker in TypeScript; DBOS or Procrastinate in Python). Jobs are keyed to a `business_clock` table, so simulated time comes for free.
- A per-case lock so events are processed one at a time.
- A provider adapter layer.
- Tool wrappers that check the action against an accepted decision before running it: matching content hash, the 21-day rule, integer money.
- Server-sent-events streaming to the operator app.
- World fork through Postgres itself (template databases or pg_dump/restore), because all state, including transcripts, lives there.

**What frameworks provide that the team would otherwise maintain:**
- Provider quirks: tool-call formats, reasoning tokens, caching, retries.
- Context compaction and memory.
- Subagent transcripts.
- Streaming protocols.
- Tracing UIs.
- Eval runners and judge tooling.
- Crash recovery mid-tool-call.

| Req | Fit |
|---|---|
| 2 Waking (inbox, controllable clock) | S, by construction |
| 3 Operator authority | S, by construction |
| 4 Deterministic checks | S, by construction |
| 5 Owned records | S, by construction |
| 7 Simulation/eval (world fork) | S, by construction |
| 1 Long-lived cases | A; quality depends on the team's context management |
| 6 Multiple providers | A |
| 8 Surfaces | A |
| 9 Team/velocity | A; more code, though AI coding agents lower the cost |
| 10 Lock-in/cost | S |

**Main risk:** subtle bugs in context management and recovery, plus slower feature work.

Sources: https://github.com/timgit/pg-boss , https://worker.graphile.org

---

## Ranking for Handoff (stateful/application-framework family)

1. **Pydantic AI, used as the agent and model layer inside an owned Postgres case runtime** (if the team picks Python). Its deferred-tool design, where a run ends, state stays as data and the run resumes on an event, fits weeks-long cases with approvals that wait days, and it keeps every record in Handoff's Postgres.
2. **Mastra** (if the team picks TypeScript). It covers the most out of the box: approvals, signals, schedules, evals, Postgres storage and streaming. Keep the inbox, the clock and decision binding in your own tables, and treat the beta harness APIs with caution.
3. **Pure build-our-own.** Best fit and least lock-in, but the most maintenance.
4. **Convex.** Excellent developer experience and transactions, but it conflicts with owned records and lock-in (requirements 5 and 10).
5. **CrewAI.**
6. **Letta.** Its server has been retired.

**Most important thing I couldn't verify:** none of these options documents a way to drive its persisted timers (Mastra schedules and sleep, Convex scheduler and Workflow sleep, DBOS sleep, Letta cron) from an injectable business clock in a running deployment. Only Temporal's test server documents time-skipping, and that is for tests. If none can do it, every option needs deadlines modelled as Handoff's own clock-driven jobs. I couldn't confirm either way.
