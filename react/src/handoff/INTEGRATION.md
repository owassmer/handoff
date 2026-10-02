# Handoff frontend: integration notes

Internal implementation notes. Nothing here appears in the product.

## Screens

- **Units** (`App.tsx`, `HandoffListPage`): one row per move-out. Units whose work plan awaits a decision sort first
  and say so in the Now column. Readiness and move-out accounting are separate statuses.
- **Unit** (`HandoffCasePage`): header with address, lease end and the two tracks. Main column, in order:
  - `DecisionSheet` (`Decision.tsx`) when the current plan is not accepted: line items grouped by vendor with
    "View quote", totals, requirements, "Why this plan" (closed), Accept and Change.
  - Otherwise one line with the agent's current status and next step.
  - `AcceptedPlan`: the operative decision's immutable content, collapsed.
  - `WorkSection` (`Work.tsx`): jobs with visit, inspection findings (including Not checked), invoice with payer,
    and payment state. A requested or uncertain payment never reads as paid. Open questions and received quotes.
  - `MoneySection`: set aside, committed, invoiced, paid, available. Unknown is a dash, never zero.
- **Side panel** (`SidePanel.tsx`): Ask Handoff (operator thread and composer), Messages (correspondence grouped by
  party, original wording), Unit file (lease, records, vendor information, quotes, people, obligations),
  Activity.
- **Document viewer** (`DocumentDialog.tsx`): native `<dialog>`. Text records show their text and their files;
  a file opens only when the operator selects it. Object URLs are released on close, source change or lost access.

## Behaviour kept from the store (`state.ts`)

- Plan edits are store drafts (`edit`, `editProposal`, `discard`, `reviewLatest`), so they survive refreshes and
  are blocked when the plan's revision or identity changes until the operator reviews it.
- A budget-only change sends `budget`; any line or requirement change sends one `plan` change with the budget.
- Every change is confirmed by its receipt and a fresh read before the page shows it. An uncertain send is kept
  across reload and checked, never resent under a new identity.
- `canDecide` shows Accept and Change; `canWork` enables messages. The server decides both.

## Design system

`handoff.css`: light workspace, warm greys, one accent (#1f3a93) reserved for "needs your decision", hairline
dividers, tabular right-aligned money, status as a dot plus text. Breakpoints at 1100 px (side panel below) and
720 px (stacked rows, fewer table columns).

## Action contracts and confirmations

Use the installed public Platform SDK on Main, omitting `branch`. Never include `currentUserId` or an execution version in caller parameters.

| Action | Caller parameters | Receipt |
| --- | --- | --- |
| `change-handoff-work-plan`, budget | `workPlanId`, `expectedRevision`, `commandId`, `budgetCents` | `Work budget changed`; plan subject; payload `{ workPlanId, expectedRevision, budgetCents }` |
| `change-handoff-work-plan`, structured | `workPlanId`, `expectedRevision`, `commandId`, `changesJson` | `Work plan changed`; plan subject, including a fork; payload `{ workPlanId, expectedRevision, changes }` |
| `accept-handoff-work-plan` | `workPlanId`, `expectedRevision`, `commandId` | `Work plan accepted`; accepted plan subject; payload `{ workPlanId, expectedRevision }` |
| `send-handoff-message` | `handoffId`, `message`, `commandId`, optional `expectedPlanRevision` | `Message sent`; Handoff subject; payload `{ handoffId, message, expectedPlanRevision }`, omitting absent version |

Exactly one of budget or structured change is sent. `changesJson` contains the typed `WorkPlanChange`: optional budget, quoted selections (`quoteId`, `quoteLineId`, `scope`, `reason`), requirements and nullable fixed provider. Normalize whitespace before constructing and hashing the command, not after dispatch. Metadata checks require the known required/optional Long/JSON fields and reject extra inputs, including an exposed actor.

`state.ts` uses the existing one-request-per-Handoff journal. Recursively sorted JSON and SHA-256 must match the service. Confirmation requires command, subject, kind and payload hash plus a later coherent read. Old exact acceptance stays confirmable after a new proposal; a fork does not rewrite its original Decision. Matching current values alone proves nothing about a particular command.

Draft text, scope and exact retry payloads remain in memory. Browser storage contains only bounded recovery identifiers/hashes (32 entries / 64 KiB). Reload can check but cannot invent an exact retry. Plan identity as well as revision binds a draft. No optimistic acceptance, settlement or provider completion is shown.

`VITE_HANDOFF_ACTION_FUNCTION_VERSION` selects **only definitive-error recognition**. It must match the corresponding Function RID and exact runtime with the structured rejection envelope. Reads use their own exact pin. Tests retain distinct historical pins to reject read-runtime errors when a different Action runtime is configured. The current `1.6.0` deployment rejects stale `1.5.0`/`1.5.1`, future `1.6.1`, unrelated functions and malformed errors as definitive outcomes.

## Supporting-file integration — Main1.6.0

The user merged the protected source proposal; deployment succeeded. Stable Main1.6.0 at commit55be1fb383650177004d3e3d2660adfb601d3f01 was independently verified for all12affected Functions, including3reads,8existing mutations and the new association function. The prior prerelease lookup limitation does not apply to this stable release. All3frontend environments now pin1.6.0 queries and Action-error recognition; their separation and negative-version tests remain.

The additive v2 document fields are optional sourceKind (Prepared|Original) and sourceDocumentIds. References must be unique, bounded to32 and resolve to separate Original records in the same returned case. Prepared summaries cannot carry media pointers. documentKey includes these fields. File names and references come only from the protected read.

The server-bound/configure-authorized association Action checks live source rights/version and stores pointers, not protected filenames or source bodies. Reads recheck access. Pointer-only attachments do not enter planning/materiality. Nine existing Actions use the1.6.0family so the active coordinator has the same behavior. No work-plan acceptance is implied by an association.

Available condition/maintenance supporting PDFs are court-derived/reconstructed, not native email/photo exhibits. Keep the truthful classification at the file. Actual Main associations, receipt/replay outcomes and native browser access are recorded separately in the project checkpoint, not inferred from code publication.

## Source boundary

`gateway.ts`, `sources.ts` and `DocumentDialog.tsx` read only original references supplied by current protected workspace data. PDFs use inclusive page ranges. Supported original images are viewed as images, not inferred dimensions/findings. MIME/signature checks admit PDF, PNG, JPEG, GIF and WebP, not HTML/SVG. Optional checksums are enforced if supplied; current backend DTOs do not supply one.

Fresh reads replace source grants. Removed/replaced sources, failed fresh reads and access/identity invalidation clear grants and release blob URLs. Late source responses are discarded. Permission loss clears sensitive drafts and retry bodies; same-person OAuth refresh preserves them. Files already downloaded outside this app cannot be revoked.

The current persistent Demo contains prepared source records without original media references. Earlier extraction of22PDFs/60pages is not evidence of their association with this case. The dedicated configure-authorized association capability is now on Main1.6.0; ordinary notice/document/conversation paths remain unable to bootstrap arbitrary original references. Actual association and file-view verification are separate from the successful promotion. Never relabel prepared text, invent media IDs, patch raw objects or weaken source controls.

## Verification and remaining B evidence

Run `VERIFY_ENV_PRODUCTION=true npm test`, `npm run typecheck`, `npm run lint`, `npm run build`, and `git diff --check`. The earlier 911 passes / 3 existing skips are historical baseline evidence, not a claim that this release was tested. Record the current execution result in the release report.

Deployment tests check each environment, actual exported configuration, unchanged redirects, no branch parameter, exact query POST paths and separate Action rejection matching. Work-contract/gateway/state/view tests cover structured changes, messages, immutable acceptance, source invalidation and saved-only progress. Identity invalidation during metadata preflight prevents dispatch; an already-dispatched uncertain operation retains only its bounded recovery reference.

Publication requires explicit-file commit, successful exact-commit CI, the supported application publication tool and successful tag CI. Preserve unrelated `.vscode/settings.json`. Local mock/JSDOM tests and registry metadata do not establish restricted-app OAuth access, hosted rendering, native PDF behavior, worker timing, distributed concurrency or autonomous provider delivery.

Use safe read-only service checks and existing authorized isolated engineering records for actual mutation/receipt tests. Do not change the primary budget, send test conversation or accept its proposal merely to complete a release test. Earlier isolated engineering records are not currently returned by available Main/merged-branch reads; do not silently reconstruct them or write to a merged branch.

B still needs coherent source/world completion, substantive provider progress/change, reports/checks, invoices/final payments and continuation through waits, plus a focused operator check. Recovered scheduling or a published UI is not that evidence. The user's judgment remains theirs; C/D and live activation are separate scope.
