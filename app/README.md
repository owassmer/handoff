# Handoff app

The new Handoff build, separate from Foundry. Design: `design/DESIGN.md`. TypeScript on Node 22.

```
cd app && npm install
npm test          # all workspaces
npm run typecheck
```

## `service/`: the case runtime

The platform the agent runs inside (DESIGN.md §5.1). It holds the records, and code enforces authority, money and idempotency around everything the agent does.

| Piece | File | What it guarantees |
|---|---|---|
| Records | `migrations/001_core.sql` | Tenancy, parties, case. Events are append-only, decisions can't change once proposed, and action outcomes are final. The database enforces these with triggers, not only the code. |
| Inbox | `events.ts`, `inbound.ts` | Everything that happens to a case arrives as an event. Trust comes from the source: tenant and counterparty content can inform, never authorize. |
| Business clock | `clock.ts`, `wakeups.ts`, `timeline.ts` | Real time in production. A stored clock in a simulated world, moving only forward. Deadlines and follow-ups are wake-ups stored as data. |
| Decisions | `decisions.ts`, `principals.ts` | The agent proposes and an operator decides. Acceptance binds to the content hash the operator reviewed. A correction retires what it corrects only once it is accepted. Standing instructions need `configure`. |
| Action gateway | `gateway.ts`, `actions/` | Every effect checks authority (an accepted decision, a standing instruction or a stated routine) and runs further checks. Refusals are recorded. An effect happens at most once per key, and an unconfirmed effect is settled by asking the outside system, never by acting again blind. |
| Case runner | `runner.ts` | Each wake is a fresh turn rebuilt from the records, under a per-case lease. A failed turn leaves its events pending. The agent (LangGraph, next) plugs in as a `CaseTurn`. |
| Case records | `migrations/003_case_records.sql`, `records.ts` | Documents, inspections, conditions, neutral observations, responsibility findings (a new one supersedes, none are erased), work items linked to the conditions they fix, and the working account. Account entries are signed cents that are never edited: corrections are reversals, and the balance is their sum. |
| Decision content | `account/statement.ts`, `account/pursuit.ts`, `work/plan.ts` | The shapes of the account statement, the work plan, balance pursuit and balance correction. A refund is refused unless the accepted statement adds up. |
| Outside systems | `adapters/`, `actions/` | Mail, payments, ledger, utility biller, in-house maintenance, vendors, collector. Every effect is an action through the gateway. Ledger postings, collector placements and corrections take their amounts from the accepted decision, never from the request. Quotes and final utility reads are routine. Planned work needs the accepted plan and stays within its budget. |
| Imitations | `sim/`, `migrations/002_*`, `004_*` | Each outside system as a separate imitation with its own records in the `sim` schema, hidden scenarios (timeouts, declines, holidays, late invoices, a collector that lags corrections) and timers on the business clock. A world copy carries them. Agent tools never read the `sim` schema. |
| Simulated world | `world.ts` | Records, imitations and clock in one in-process Postgres (PGlite). `advanceTo` fires everything due, in time order. `copy()` branches the whole world at any moment. |

| Models | `agent/models.ts`, `llm/chatgpt/` | Each role's model comes from configuration. During development it runs on a ChatGPT plan through Sign in with ChatGPT. Paid providers are used only when chosen explicitly, never as a silent fallback. Setup: `service/CHATGPT_PLAN.md`. |

### Next

- The agent itself (DESIGN.md §6 step 2): the LangGraph coordinator as a `CaseTurn`, its read and prepare tools over these records, and the evidence analyst.
- The legal engine's evaluator is being built in `app/legal` (DESIGN.md §6 step 3).
