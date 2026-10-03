# Durable-execution engines and actor runtimes for Handoff

Researcher: durable-execution family. All sources accessed 2026-10-03. Package versions and dates come from the npm and PyPI registries on that date.

## Findings that apply to every option

- **These are substrates, not agents.** None of them reasons. They make an agent loop that you write, or one from a framework they integrate with, survive crashes, sleep and wake up.
- **Reasoning freedom and determinism can coexist.** In the replay-based engines (Temporal, Restate, DBOS, Inngest, Vercel Workflow), each LLM call runs as an activity or step, and its output is journaled. On replay the same decision comes back, so only the orchestration code around the calls has to be deterministic. The real cost is code evolution. A case that lives for weeks spans many deploys, so each engine needs a versioning plan:
  - Temporal: patching or Worker Versioning.
  - Restate: pins each invocation to the deployment it started on.
  - DBOS: recovers a workflow only on its original application version, or through `DBOS.patch()`.
- **No engine delivers a payment exactly once.** Activities and steps are at-least-once everywhere. You get stable IDs to use as idempotency keys with the payment rail. DBOS alone also gives exactly-once writes to your own Postgres, in the same transaction as its checkpoint.
- **Operator authority (req 3) and prompt-injection defence are application code in all of them.** An engine can wait durably for a decision. It does not check that the decision's content matches the action. The money-moving activity has to re-check an accepted decision record in Postgres.
- **Controllable time is weak across the family.** Only Temporal ships time skipping, and only in its test server. An accelerated demo clock needs an app-level business clock in every option: deadlines stored in business time, and a clock service that emits tick events the case waits on.
- **Whole-world fork is not a product feature anywhere.** No option snapshots engine state, app records and simulated counterparties together.

## 1. Temporal (OSS server and Temporal Cloud)

**Status.**
- Funding: Series D, $300M at a $5B valuation (Feb 17, 2026).
- Named AI customers: OpenAI (Codex on the web), Replit, Lovable, Abridge.
- SDK versions: Python `temporalio` 1.34.0 (Sep 30, 2026) and TS `@temporalio/workflow` 1.24.0 (Sep 15, 2026).
- Replay 2026 (May): OpenAI Agents SDK integration declared **GA for Python** with sandbox support. Workflow Streams in Public Preview. Worker Versioning and Priority/Fairness GA. Serverless Workers (Lambda) in pre-release.
- Other integrations: TS OpenAI Agents integration is **Pre-release**, and AI SDK by Vercel (TS) is in **Public Preview** (announced Jan 20, 2026). The docs also list Google ADK, LangGraph, Pydantic AI, Mastra, Strands and Deep Agents.

**By requirement.**
1. **Agent-led cases: strong.** The integration runs "the agent loop, tool selection, and handoffs" inside the Workflow and model calls as Activities. Specialists can be child workflows. The documented "entity workflow" pattern makes one workflow per case. A history limit of 51,200 events or 50 MB means the case has to Continue-As-New periodically, carrying its state forward.
2. **Waking on events: adequate.** Signals, Updates and durable timers are mature. Time skipping exists only in `TestWorkflowEnvironment`. It is global to the environment, and it is not available on the dev or production server. A demo clock must be built at app level.
3. **Operator authority: adequate.** Approvals wait on a signal or update for days at no compute cost. Update validators can reject malformed decisions before they reach history. Python agent tools can pause for approval inside the workflow. The TS integration documents that "nested approval interruptions are not supported". Checking that the decision content matches the action is app code.
4. **Deterministic checks: adequate.** Activities are at-least-once. Workflow ID plus activity ID gives a natural idempotency key. Integer-money and statutory checks belong in deterministic workflow code or in activities.
5. **Owned records: adequate.** Event histories live in Temporal's persistence layer, which can be Postgres when self-hosted, but separate from the app's records. In Cloud they sit with the vendor. Transcripts can be inspected as workflow histories. The server is MIT-licensed and fully self-hostable.
6. **Multiple providers: strong.** The AI SDK plugin takes any `modelProvider`. The Python OpenAI Agents docs show only OpenAI.
7. **Simulation and fork: adequate.** Deterministic replay of a history (`Replayer`) and Reset to a workflow-task event are real strengths. Reset terminates the run and restarts under the **same** workflow ID. There is no fork to a new ID and no app-database snapshot.
8. **Surfaces: adequate.** Workflow Streams (preview) stream tokens and tool progress to external consumers. Queries serve status.
9. **Team and velocity: strong.** It is the most mature option with the deepest documentation, and it publishes a Temporal skill for coding agents (preview, Mar 2026). The learning curve and determinism rules are steep for two founders.
10. **Lock-in and cost: adequate.**
    - Cloud lists pay-as-you-go pricing at $50 per million actions, falling to $25. Active storage costs $0.042/GB-hr. New accounts get a $150 credit.
    - Self-hosting means running the frontend, history, matching and worker services plus a database. That is the heaviest operational load in this family.

**Weaknesses.** Heavy operations. Long-lived workflows force versioning discipline. Payload limits push large LLM transcripts to External Storage, which is still in preview. The TS agent integrations lag Python.

**Verdict.** The most proven choice. Weakest on records living in your own Postgres and on forking.

## 2. Restate

**Status.**
- Server v1.7.12 (Sep 22, 2026). v1.6 (Jan 30, 2026) added pause/resume and "restart from journal prefix". v1.7 (Jun 18, 2026) added flow control and UI 1.0.
- SDKs: TS SDK 1.17.2 and Python SDK 1.0.5 (Sep 2026).
- Series A: $20M, announced Sep 30, 2026. Named customers: Replit, DOSS and an unnamed Fortune 500 bank.
- Agent integrations: Vercel AI SDK, OpenAI Agents SDK (Jan 15, 2026), Google ADK (Jan 12, 2026), Pydantic AI (Apr 2, 2026), LangChain, or any SDK through `ctx.run()`.

**By requirement.**
1. **Agent-led cases: strong.** A **Virtual Object keyed by case ID** is a first-class long-lived entity: it holds K/V state, allows one writer per key, and queues concurrent messages. Caveat: the docs say a Virtual Object "will be blocked while waiting on the awakeable". A case handler that awaits a days-long approval stops every other message to that case. You have to design short per-event handlers, or move the waits into a Workflow.
2. **Waking on events: adequate.** Durable timers and delayed sends exist. The testcontainers harness documents no time control.
3. **Operator authority: adequate.** Awakeables (durable promises) suspend the handler at zero compute cost, with timeouts that survive restarts. Authority checks are app code.
4. **Deterministic checks: adequate.** `ctx.run` results are journaled. The docs concede that external side effects "may still need idempotency protection".
5. **Owned records: adequate.** State lives in Restate's own log and RocksDB store, with snapshots to S3, GCS or Azure, not in Postgres. The journal is visible in the UI. It is self-hostable as one binary, or available as Cloud or managed BYOC.
6. **Multiple providers: strong.**
7. **Simulation and fork: weak.** Restart-as-new copies a journal prefix into a **new invocation ID**, but only from completed invocations. Virtual Object state is not forked.
8. **Surfaces: adequate.** No browser-streaming primitive was found; the app has to add SSE.
9. **Team and velocity: adequate.** Docs are good. The ecosystem is smaller than Temporal's.
10. **Lock-in and cost: adequate.** The server is **BSL 1.1**: own-use production is allowed, offering it as a public service is not, and each release converts to Apache 2.0 after four years. Operations are light. The Cloud free tier is reported at 50k actions/month, from a third-party pricing page because the official page did not render.

**Verdict.** Has the cleanest per-case entity model. Its data store is not your Postgres, and the license and vendor are less established.

## 3. DBOS (Transact library and Conductor)

**Status.**
- Libraries: Python `dbos` 3.2.0 (Sep 29, 2026; 3.0 brought schema changes for scale) and TS `@dbos-inc/dbos-sdk` 5.2.11 (Sep 29, 2026). Transact is **MIT**.
- Integrations: Pydantic AI (`DBOSDurability`), OpenAI Agents (`dbos-openai-agents`), LlamaIndex (Apr 2026), Google ADK (Jun 2026), and Vercel AI SDK through `@dbos-inc/vercel-ai` 0.5.4 (Jul 2026).
- Named users: Walmart's internal agent framework, Yutori, Dosu, Goblins.

**By requirement.**
1. **Agent-led cases: adequate.** It has no entity primitive. A case is a workflow that loops on `DBOS.recv()`, or a series of per-event workflows with state in your tables. Waiting workflows live in the process and are recovered on restart. The memory cost of thousands of week-long waiting workflows is not documented.
2. **Waking on events: adequate.** `send`/`recv`, events, durable `DBOS.sleep` ("days, weeks, or months"), delayed scheduling (Apr 2026), and enqueue or send straight from SQL. No time control.
3. **Operator authority: adequate.** Approvals arrive through `recv` with a timeout. Authority checks are app code.
4. **Deterministic checks: strong.** A transactional step "writes the step checkpoint in the same database transaction as the application's updates". That makes ledger and decision writes exactly-once, and an outbox to the payment rail straightforward.
5. **Owned records: strong.** All durable state sits in **your** Postgres, which an institutional security review can audit directly. Conductor has a metadata-only mode and can be self-hosted at Enterprise tier, with HA support added in Jul 2026.
6. **Multiple providers: strong.** Pydantic AI uses a pre-registered `models` dict.
7. **Simulation and fork: adequate.** This is the best fit in the family. `fork_workflow` restarts from a step under a new ID and can use a different code version. Because engine state and app records share one Postgres, a database snapshot or branch should capture both together. That is my inference; it is not a documented feature.
8. **Surfaces: adequate.** Durable streams have used LISTEN/NOTIFY since Jun 2026.
9. **Team and velocity: strong.** It is a library inside the app, with no extra server. The ecosystem and vendor are smaller.
10. **Lock-in and cost: strong.** MIT, and the data is yours. Conductor is optional: Pro $99/month, Teams $499/month, then $40–50 per million extra checkpoints.

**Weaknesses.** No first-class long-lived entity. Version-pinned recovery needs old code versions running. Python is ahead of TS on integrations. The pydantic-ai integration "takes no per-tool config".

**Verdict.** The best fit for records-first, Postgres-centric Handoff.

## 4. Inngest (and AgentKit)

**Status.**
- Server is SSPL with delayed Apache 2.0 publication. SDKs are Apache 2.0.
- TS SDK `inngest` 4.21.1 (Oct 1, 2026). Python SDK still 0.5.19.
- **AgentKit looks stalled**: the last npm release was 0.13.2 on Nov 13, 2025, and the last commit was Apr 29, 2026.

**By requirement.**
1. **Agent-led cases: adequate.** Event-driven functions. Limits of **1,000 steps** and 32 MiB of state per run mean a weeks-long agent has to be split into one run per wake.
2. **Waking on events: adequate.** `waitForEvent` with CEL matching. The documented gotcha: "A matching event sent earlier will not resume this wait". Maximum wait depends on plan: 30 days (Free), 90 days (Pro), 366 days (Business). `@inngest/test` mocks sleeps but cannot advance a clock.
3. **Operator authority: adequate.**
4. **Deterministic checks: adequate.** Steps are memoized by ID and run at-least-once.
5. **Owned records: adequate.** Self-hosting with Postgres and Redis has been supported since 1.0, but "support team does not guarantee direct support for self-hosted", and old rows are not pruned automatically.
6. **Multiple providers: strong.** `step.ai.infer` covers OpenAI, Anthropic, Gemini, Grok and Azure.
7. **Simulation and fork: weak.** Rerun-from-step creates a new run with earlier steps memoized, and "repeats every side effect from the selected starting point".
8. **Surfaces: adequate.**
9. **Team and velocity: adequate.** Strong DX in TS.
10. **Lock-in and cost: adequate.** Free $0 with 50k executions; Pro from $99; Business from $499. Every step counts as an execution.

**Verdict.** Good for event plumbing. A weak home for a weeks-long agent.

## 5. Cloudflare Agents SDK

**Status.**
- npm `agents` 0.26.0 (Oct 2, 2026). Still pre-1.0, with very fast churn: v0.7 in March and v0.20 in July.
- Recent additions: fibers (durable execution), background sub-agents (v0.17, Jun 2026), and agent tracing (Aug 2026).

**By requirement.**
1. **Agent-led cases: strong.** Each Agent is a Durable Object addressed by name, such as a case ID, with SQLite, state and schedules: a true long-lived entity.
2. **Waking on events: adequate.** `this.schedule` runs on DO alarms. Workflows `waitForEvent` lasts up to 365 days. Tests can fire alarms with `runDurableObjectAlarm`, but there is no business clock.
3. **Operator authority: adequate.** `waitForApproval()` is backed by Workflows and documented to hold "for months or longer".
4. **Deterministic checks: weak.** Fiber recovery is checkpoint-based ("the original lambda is gone"), and v0.17 promises "exactly-once-on-the-happy-path".
5. **Owned records: weak.** State lives in Cloudflare-hosted DOs. `workerd` stores DOs in memory or on local disk ("experimental") and "is not a hardened sandbox". There is no credible VPC deployment. Postgres is reachable only over the network.
6. **Multiple providers: strong.**
7. **Simulation and fork: weak.**
8. **Surfaces: strong.** WebSockets, state synced to the `useAgent` React hook, and email.
9. **Team and velocity: adequate.** TS only.
10. **Lock-in and cost: weak.** High platform lock-in.

**Verdict.** The best developer experience for a live agent entity. It fails the self-hosting requirement.

## 6. Vercel Workflow DevKit / AI SDK WorkflowAgent (brief)

**Status.**
- Vercel Workflows reached GA in mid-April 2026. npm `workflow` 5.0.1 (Oct 1, 2026).
- `@ai-sdk/workflow` `WorkflowAgent` 2.0.58 (Oct 1, 2026) "handles tool schema serialization, workflow step boundaries, and built-in tool approval flows".

**By requirement.**
- `"use workflow"` and `"use step"` directives, with `sleep`, hooks and webhooks.
- Any AI SDK provider. Streaming from steps to the UI.
- It has no entity primitive and no documented clock control or fork.
- Self-hosting relies on a **community-maintained** Postgres "World" of unstated maturity. In practice it pulls toward Vercel hosting.
- TS only.

**Verdict.** Adequate for a Next.js-centric team. Unproven off Vercel.

## Fit summary (S = strong, A = adequate, W = weak)

| Req | Temporal | Restate | DBOS | Inngest | Cloudflare | Vercel WF |
|---|---|---|---|---|---|---|
| 1 Agent-led cases | S | S | A | A | S | A |
| 2 Waking and controllable clock | A | A | A | A | A | A |
| 3 Operator authority | A | A | A | A | A | A |
| 4 Deterministic checks and idempotency | A | A | S | A | W | A |
| 5 Owned records and self-hosting | A | A | S | A | W | A |
| 6 Multiple providers | S | S | S | S | S | S |
| 7 Simulation, fork and replay | A | W | A | W | W | W |
| 8 Surfaces | A | A | A | A | S | S |
| 9 Team and velocity | S | A | S | A | A | A |
| 10 Lock-in and cost | A | A | S | A | W | A |

## Ranking for Handoff

1. **DBOS.** Engine state and the ledger share your Postgres. It has exactly-once database writes, `fork_workflow` and an MIT license, with the lowest operational load. The per-case entity and clock have to be built by hand.
2. **Temporal.** The most proven option, with the best test time-skipping and replay and a Python OpenAI Agents integration that is GA. Costs: heavy operations, history held outside your database, and versioning burden.
3. **Restate.** The best per-case entity model, but awakeables block the object, the license is BSL and state lives in its own store.
4. **Inngest.** Step and run limits fit poorly with week-long agents, and AgentKit appears stalled.
5. **Vercel Workflow.**
6. **Cloudflare Agents.** Excellent entity and UI model, but it cannot meet self-hosting or VPC requirements.

## Most important unknown

I could not verify whether **any** option can take a consistent fork of a whole case at a staged moment: engine state, app Postgres records and simulated counterparties, with pending timers, queued messages and in-flight steps. I also could not verify that such a fork resumes without double-firing side effects. DBOS (one Postgres database) is the most plausible route, but it is undocumented and undemonstrated. It needs a prototype spike before committing.

## Sources (accessed 2026-10-03)

- Temporal OpenAI Agents (Python): https://docs.temporal.io/develop/python/integrations/openai-agents
- Temporal OpenAI Agents (TS): https://docs.temporal.io/develop/typescript/integrations/openai-agents
- Temporal AI SDK (TS): https://docs.temporal.io/develop/typescript/integrations/ai-sdk
- Temporal integrations list: https://docs.temporal.io/develop/integrations
- Temporal Replay 2026 announcements: https://temporal.io/blog/replay-2026-product-announcements
- Temporal Python SDK changelog: https://temporal.io/changelog/product-area/python-sdk
- Temporal AI SDK by Vercel changelog: https://temporal.io/changelog/ai-sdk-vercel-integration
- Temporal TS testing suite: https://docs.temporal.io/develop/typescript/testing-suite
- Temporal Python testing suite: https://docs.temporal.io/develop/python/testing-suite
- Temporal Reset: https://docs.temporal.io/workflow-execution/event#reset
- Temporal long-running workflows: https://temporal.io/blog/very-long-running-workflows
- Temporal pricing: https://temporal.io/pricing
- Temporal Series D: https://temporal.io/news/temporal-raises-300M-to-make-agentic-ai-real-for-companies
- Restate server changelog: https://docs.restate.dev/changelog/server.md
- Restate license: https://github.com/restatedev/restate/blob/main/LICENSE
- Restate AI docs: https://docs.restate.dev/ai
- Restate sessions pattern: https://docs.restate.dev/ai/patterns/sessions
- Restate human-in-the-loop pattern: https://docs.restate.dev/ai/patterns/human-in-the-loop
- Restate awakeables (TS): https://docs.restate.dev/develop/ts/awakeables
- Restate TS testing: https://docs.restate.dev/develop/ts/testing
- Restate restart-as-new: https://docs.restate.dev/admin-api/invocation/restart-as-new-invocation
- Restate versioning: https://docs.restate.dev/services/versioning
- What is an agent runtime (Restate): https://restate.dev/what-is-an-agent-runtime
- Restate Series A: https://restate.dev/blog/announcing-series-a
- Restate pricing (third-party): https://devtune.ai/verticals/workflow-orchestration-and-durable-execution/restate/pricing
- DBOS AI quickstart: https://docs.dbos.dev/ai/ai-quickstart
- DBOS OpenAI Agents integration: https://docs.dbos.dev/integrations/openai-agents
- Pydantic AI with DBOS: https://pydantic.dev/docs/ai/integrations/durable_execution/dbos/
- DBOS outbox example: https://docs.dbos.dev/python/examples/outbox
- DBOS workflow communication: https://docs.dbos.dev/python/tutorials/workflow-communication
- DBOS upgrading workflows: https://docs.dbos.dev/python/tutorials/upgrading-workflows
- DBOS April 2026 features: https://www.dbos.dev/blog/dbos-new-features-april-2026
- DBOS June 2026 features: https://dbos.dev/blog/new-in-dbos-june-2026
- DBOS July 2026 features: https://dbos.dev/blog/new-in-dbos-july-2026
- DBOS pricing: https://www.dbos.dev/dbos-pricing
- DBOS customer stories: https://www.dbos.dev/customer-stories
- Inngest self-hosting: https://www.inngest.com/docs/self-hosting
- Inngest usage limits: https://www.inngest.com/docs/usage-limits/inngest
- Inngest wait for event: https://www.inngest.com/docs/features/inngest-functions/steps-workflows/wait-for-event
- Inngest rerun function runs: https://www.inngest.com/docs/platform/manage/rerun-function-runs
- Inngest AI orchestration: https://www.inngest.com/docs/features/inngest-functions/steps-workflows/step-ai-orchestration
- Inngest pricing: https://www.inngest.com/pricing
- Inngest server repository: https://github.com/inngest/inngest
- AgentKit repository: https://github.com/inngest/agent-kit
- Cloudflare Agents docs: https://developers.cloudflare.com/agents/
- Cloudflare durable execution: https://developers.cloudflare.com/agents/runtime/execution/durable-execution/
- Cloudflare scheduling: https://developers.cloudflare.com/agents/runtime/execution/schedule-tasks/
- Cloudflare human-in-the-loop: https://developers.cloudflare.com/agents/concepts/human-in-the-loop/
- Cloudflare Agents changelog: https://developers.cloudflare.com/changelog/product/agents/
- Cloudflare Workflows limits: https://developers.cloudflare.com/workflows/reference/limits/
- Cloudflare Workers test APIs: https://developers.cloudflare.com/workers/testing/vitest-integration/test-apis/
- workerd repository: https://github.com/cloudflare/workerd
- Vercel Workflow deploying: https://workflow-sdk.dev/docs/deploying
- Vercel Workflow AI docs: https://workflow-sdk.dev/docs/ai
- AI SDK Workflow reference: https://ai-sdk.dev/docs/reference/ai-sdk-workflow
- Vercel Workflows GA notice: https://community.vercel.com/t/vercel-weekly-2026-04-20/38580
