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
| Imitations | `sim/` | Mail and payments, with hidden scenarios (timeouts, declines) and their own timers. They live in the `sim` schema, so a world copy carries them. |
| Simulated world | `world.ts` | Records, imitations and clock in one in-process Postgres (PGlite). `advanceTo` fires everything due, in time order. `copy()` branches the whole world at any moment. |

### Next

- The remaining outside systems, as adapter interfaces plus imitations: ledger, utility biller, in-house maintenance, vendors, collector.
- Condition, work and account records.
- The agent itself (DESIGN.md §6 step 2).
