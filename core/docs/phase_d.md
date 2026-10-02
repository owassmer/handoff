# Phase D — operating the simulated closeout lifecycle

## Boundary and known version

Phase D adds an explicit simulated lifecycle to the retained stored-case interface: immutable statement versions, exact-intent approvals, reserved requests, attempt history, raw simulated results, accepted results, and derived completion. It does not send statements, post to an external ledger, move real money, generate PDFs, or prove legal performance. Statement artifacts contain structured content and exact rendered text marked `SYNTHETIC - NOT LEGAL PERFORMANCE`.

The current surface is 30 named edit functions/Actions (15 case operations plus 15 lifecycle operations), three queries and eleven object types. `docs/phase_c.md` remains the guide to the retained case interface and its phase-specific acceptance record; its original feature boundary does not describe the additional v2 lifecycle. There is one native review and one shared persistence path, not a second money or deadline calculator.

Known validated logic: commit `b37873960e251e4c2aa644313d89e5a968475c75`, Function tag `1.2.0-branch-20260920-041008`, tagged CI passed. Native validation reported **959 passed**, with five unchanged template examples skipped. This identifies the tested runtime, not a later documentation tag or a Main deployment. Work remains on :resource[ri.branch..branch.d1812bd8-71a2-4ae6-8bf1-aac76c929aa2], in draft review; no merge or Main seed is asserted.

### Fixed constructed scope

- Company: `constructed-company-001`.
- Approved operator: `c47a52a0-0048-4607-931f-f4df283ae7c4`.
- Environment: `DC_PHASE_C_SYNTHETIC`. This is stable identity, not a cosmetic phase label to rename.
- Data origin: `CONSTRUCTED`; mode: `SIMULATED`.
- Rule release: `NC_SYNTHETIC_REVIEW_V1`; all legal review cards remain `PENDING`.

`depositComplete`, `overallCaseComplete` and `legalPerformanceConfirmed` remain **false**. The v2-only `simulatedDepositWorkflowComplete` and `simulatedOverallWorkflowComplete` are derived and may become true. Related work can still prevent simulated overall completion even when deposit workflow work is complete. Do not interpret either simulated flag as legal certification or transport confirmation.

## Read the correct contract

| Interface | Meaning |
| --- | --- |
| `reviewDepositCloseout(requestJson)` | Standalone read-only native review. Strict `ReviewRequest` 1.0.0 input; base `ReviewEnvelope` 1.1.0 returned as JSON text. |
| `getCloseoutReview(closeoutCase)` | Validated stored base review, with its recorded clock. The object parameter is policy-visible; it is not a caller-supplied authority grant. |
| `getCloseoutWorkflow(caseId)` | Server-loads the scalar primary key and returns the persisted `WorkflowReviewV2` JSON text. Requires explicit workflow initialization. |

All retain the base result fields `scopeRequirements`, `itemDecisions`, `account`, `missingInputs`, `actions`, and `outcomes`. The v2 review adds commitments, operation/approval/request/statement details and simulated outcomes. Its `metadata.workflowSchemaVersion` is `2.0.0`; its base `metadata.schemaVersion` is still `1.1.0`, not `2.0.0`. `metadata.codeVersion` remains native `phase-b.1`.

Initialized roots have `workflowVersion = "2"` and unchanged `projectionVersion = "1"`. A `DcReviewSnapshot` retains base `requestJson` and `reviewJson`, adding `workflowStateJson`, `workflowStateHash`, `workflowReviewJson` and `workflowReviewHash`. Full typed codec validation checks the complete workflow state, review, identities and references. Historical review equality is recomputed at the snapshot's recorded `createdAt`/authority time, not the current clock. A stored read is not a fresh authorization decision; subsequent commands always check current authority.

The existing case, review, execution-event, charge, evidence, money, party and requirement types remain in use. The three additions are:

| Type | Operational role |
| --- | --- |
| `DcStatementVersion` | Frozen structured content and rendered text, content/materiality hashes, source review and any superseded statement link; current/issued status is derived. |
| `DcApproval` | Immutable `APPROVED`, `REJECTED` or `REVOKED` decision for an exact intent. Current validity is a projection, not a rewrite of that decision. |
| `DcActionRequest` | Immutable scoped instruction and frozen route where applicable, with current request state/reservation derived from events. |

Command receipts produced by the current shared C/D persistence path use `DcExecutionEvent.eventCategory = COMMAND_RECEIPT`. D projections separately distinguish `REQUEST_LIFECYCLE`, `RAW_SIMULATED_RESULT` and `RESULT_ACCEPTED`. Do not count receipts as execution or raw results as accepted performance. Native request facts contain one derived current fact per request ID, rather than competing state rows appended for each transition.

## Command entry and identity

### Open and initialize

1. Prepare a strict base request for the constructed company and ending tenancy, at snapshot revision **1**. Use `caseIdFor(managementCompanyId, tenancyId)` in `typescript-functions/src/deposit_closeout/phase_c/types.ts`; identity includes the fixed environment. A tenancy label or invented UUID is not the composite case primary key.
2. Call the existing `openCloseoutCase` bootstrap Action with `requestJson` and a stable `commandId`. It creates the version-one root, snapshot, receipt and projections atomically; it does not initialize v2. The Action supplies the approved current actor. The standalone demo-input helper does not perform this bootstrap.
3. Read the resulting case/revision. As the trusted case administrator, call `initializeCloseoutWorkflow` with `payloadJson` equal to `"{}"`. Do this before any other lifecycle command. Initialization splits existing instructions conservatively; it does not turn missing route evidence into verification.
4. Read `getCloseoutWorkflow(caseId)`. Use its requirements and action details to decide what is admissible; never infer readiness from a single amount or status.

For all 15 D Actions, caller inputs are `caseId`, `commandId`, `expectedRevision` and strict kind-specific `payloadJson`. `expectedRevision` is a **numeric Long on the Action**; the TSv2 function receives the canonical decimal Long string. JSON amounts remain exact numeric cents, not Long strings. The platform injects `client`; the Action binds `actorId` through server `current_user_id`. Neither is an editable form parameter. Operation kind is fixed by the named wrapper; `payloadJson` is the payload object, not an arbitrary command envelope.

A minimal initialization Action parameter shape, after a fresh opening, is:

```json
{
  "caseId": "<caseId from caseIdFor>",
  "commandId": "constructed-init-001",
  "expectedRevision": 1,
  "payloadJson": "{}"
}
```

The placeholder must be replaced with the real case key and revision. Required nullable fields in other payloads must be explicit `null`; unknown fields are rejected. Do not insert actor, grants, hashes, target versions or replacement objects into a payload to bypass server derivation.

### Named lifecycle Actions

These are the registered function names backing the named Actions. Exact fields and validations are canonical in `typescript-functions/src/deposit_closeout/lifecycle/types.ts` (`LifecycleCommandPayloads`) and `codec.ts` (`parseLifecycleCommand`); this table is an operating index, not a second schema.

| Function | Fixed command kind | Purpose |
| --- | --- | --- |
| `initializeCloseoutWorkflow` | `INIT_WORKFLOW` | Add the explicit v2 sidecar. |
| `acceptCloseoutScopeFacts` | `ACCEPT_SCOPE_FACTS` | Accept evidenced scope facts, not a legal determination. |
| `qualifyCloseoutInterim` | `SET_INTERIM_QUALIFICATION` | Record a distinct interim qualification decision and evidence. |
| `upsertCloseoutRecipientParty` | `UPSERT_RECIPIENT_PARTY` | Add/update resident or signatory membership only; no principal or grant creation. |
| `setCloseoutStatementInstructions` | `SET_STATEMENT_INSTRUCTIONS` | Version the statement channel independently. |
| `setCloseoutRefundInstructions` | `SET_REFUND_INSTRUCTIONS` | Version the refund channel independently. |
| `prepareCloseoutStatement` | `PREPARE_STATEMENT` | Freeze `INTERIM`, `FINAL` or linked `CORRECTIVE` content. |
| `decideCloseoutApproval` | `DECIDE_APPROVAL` | Approve or reject the exact server-derived intent. |
| `revokeCloseoutApproval` | `REVOKE_APPROVAL` | Append withdrawal without erasing the earlier decision. |
| `requestCloseoutOperation` | `REQUEST_OPERATION` | Admit one approved instruction, reserving any financial commitment. |
| `claimCloseoutRequest` | `CLAIM_REQUEST` | Claim an admissible `READY` request and record its attempt. |
| `markCloseoutOutcomeUnknown` | `RECORD_OUTCOME_UNKNOWN` | Preserve uncertainty against the known attempt. |
| `simulateCloseoutResult` | `GENERATE_SIMULATED_RESULT` | Generate a raw synthetic observation; administrator-gated. |
| `ingestCloseoutResult` | `INGEST_RESULT` | Validate and accept a raw source event against the current case. |
| `cancelUnattemptedCloseoutRequest` | `CANCEL_UNATTEMPTED_REQUEST` | Withdraw only a still-unattempted `READY` request. |

Current actor-specific role, action scope and amount authority are checked at actual server time. Initialization and raw simulation require trusted administration. Case membership, a display role, an approval, or a future business clock is not by itself permission to operate. Recipient upsert requires `principalId = null`, resident/signatory roles and case evidence; it cannot overwrite operators, custodians or authority-bearing parties, nor alter access grants.

Retained C Actions continue to accept their existing contracts, including bootstrap, explicit charge choice, evidence/fact and authority operations, work assignment, recheck and demo-clock advance. Once v2 is initialized, their shared persistence path reconciles the workflow too. Work assignment can target v2 requirements derived by the trusted server; no payload override supplies arbitrary requirements. An explicit change through C's combined recipient command maps both channels; use the D split commands when changing only one channel. Do not reinterpret uninitialized C behavior as globally replaced by v2.

### Retry, concurrency and limits

For existing-case mutations the shared C `persistCase` path updates **the exact loaded root once**, and writes one new snapshot, command receipt and all projections in one edit batch. It does not refresh away a competing root version or rely on a process mutex. A successful new command advances one revision; exact authorized receipt replay returns no edits.

Retain the original command ID, expected revision and canonical payload for a retry of the same command. Authorization precedes replay. Reusing an ID with different intent conflicts. For a stale/concurrent failure, reload the root and inspect receipts and request history first: determine whether the original committed before proposing new intent with a new command ID. Do not blindly generate new IDs to bypass an uncertain result.

Command idempotency and economic idempotency are separate. A different command/approval for the same scoped instruction still resolves to the same request identity, not another reservation or payment. Such a semantic replay can produce its own command receipt/revision without another economic effect. Source-event and canonical transaction identity also suppress exact and semantically duplicate result effects; conflicting deliveries require reconciliation.

`requestCloseoutOperation` alone among D wrappers accepts optional `testDelayMilliseconds` from **0 through 3000**, for the constructed overlap test only. It is excluded from immutable intent and is not a lock or execution scheduler. Omit it for normal operation.

Stored-case JSON is at most **262,144 UTF-8 bytes**; workflow payload/state/review JSON must be **strictly below** that bound. Each projection family is capped at **1,000 rows**. Bounds fail closed; no truncation, history deletion or guessed-zero fallback is supported. Source timestamps require explicit UTC with exact microsecond precision; stored review clocks must be representable exactly at milliseconds or coarser. Actor/recording times are real server times; the synthetic business clock may be later but never determines authority. V2 rechecks do not rewind that business clock.

## Performing the simulated workflow

1. **Resolve the basis.** Use accepted case-local evidence, association, charge decision and explicit choice Actions. Unknown additional work is not zero. Accept scope and intended parties/instructions where needed. Invoice delay alone does not qualify an interim statement; it needs a separately evidenced, accepted condition supported by the synthetic rules.
2. **Prepare and inspect content.** Freeze a statement once its scope/trigger and final account, or distinct interim qualification, permit it. Inspect the exact text and sources. Preparation is not dispatch. Verified statement and refund routes are separate; a statement can proceed while the refund route is unconfirmed. Routes are synthetic `DEMO_OUTBOX` references, not actual addresses or payment destinations.
3. **Approve exact operations.** Select kind, positive cents for money operations (null for dispatch), disposition and applicable statement/replacement/reversal references. The server derives materiality and target versions. Approvals cover that exact intent, not an unrestricted case revision or a blanket permission to spend.
4. **Request, then claim.** Request from an approval ID; inspect the resulting current request and reservation. Claim only admissible `READY` work, with current authority, materiality and capacity checks. A claim is treated conservatively as potentially attempted; do not clear it merely because no outcome is visible.
5. **Generate, then ingest.** Use the known request and attempt plus a stable source-event identity to generate a simulated result. This creates a raw record, not performance. Ingest that source event explicitly at the latest observed revision. Validate the accepted event, native money/statement facts, remaining commitments and resulting review; an Action success reply alone is not the completion test.

`STATEMENT_DISPATCH`, `CHARGE_POSTING`, `DEPOSIT_APPLICATION` and `REFUND` are distinct instructions. A posting is noncash and does not apply held deposit funds. `CHARGE_POSTING_REVERSAL` and `DEPOSIT_APPLICATION_REVERSAL` use **positive** amounts and an explicit original canonical transaction; negative payments are not a correction mechanism. Zero refund needs no refund instruction or event, while statement/posting/application obligations can still exist.

### Materiality is not performance

Frozen content hashes include the exact structured artifact and rendered text. Approval-materiality hashes answer whether the decision basis still matches. Full review/state hashes validate snapshots. Financial identity binds scoped kind, amount, disposition, materiality, relevant recipient version and any replacement/reversal target; it deliberately excludes whole-case revision, command/approval identity, current paid/held balances and statement-only text/route. A statement link on a financial intent is a basis/display link, not its economic identity.

Normal reservations and accepted execution facts do not invalidate the approvals they implement. A material correction can invalidate an approval and supersede an **unattempted** `READY` request, without fabricating a replacement request. The immutable instruction, decision, content and event history remain. Mere inability to verify a basis is not evidence to release a reservation. Attempted or unknown requests remain for reconciliation even when authority or materiality changes.

### Cash and unknowns

New refund capacity is the smaller of:

- native unpaid refund liability less refund reservations; and
- verified held deposit cash less other refund reservations and deposit-application commitments.

Deposit applications are likewise constrained by their kind-specific uncommitted delta and the shared held-cash budget. Native refund liability still includes reservations; do not subtract them twice or equate it with `newlyRequestableRefundCents`. Existing-request checks may exclude that request's own commitment, but new-intent capacity must not. Pending cash-in reversals or returns do not fund new outflows until accepted. Unclassified pending ledger work or unknown outcomes can make finances unverifiable; display `null`, not zero. Approval does not bypass request/claim capacity gates.

## Recovery without rewriting business history

| Situation | Safe action and retained history |
| --- | --- |
| Request never attempted | Cancel only if still `READY`, or let a known material change/revocation supersede it. Cancellation and supersession are events, not deletion. |
| Approval withdrawn | Append a `REVOKED` decision. The earlier `APPROVED` record remains, with projected validity false; a qualifying `READY` request becomes `SUPERSEDED`. Withdrawal does not undo attempted performance. |
| Claimed/requested outcome unknown | Mark the existing attempt unknown. Preserve its reservation, block blind new commitment/cancellation, and ingest a later valid result for the **same instruction** when available. Do not assume failure or create a replacement to clear uncertainty. |
| Definitively failed instruction or verified returned refund | A separately approved replacement may explicitly reference the parent request, subject to remaining liability, existing replacements and cash. Unknown/attempted work is not replaceable merely because it is inconvenient. |
| Refund returned | Accept a distinct return tied to the original canonical settlement. Keep the settlement; gross paid, returned and net refunded are different values. A return does not erase the earlier payment. |
| Correction before statement attempt | A same-kind unissued/unattempted draft can be replaced with an explicit `supersedesId`. Preserve the prior content and any superseded request. |
| Correction after issue or possible attempt | Preserve the issued/potentially attempted statement and reconcile its dispatch. Use a linked `CORRECTIVE` version. Omission of a predecessor cannot bypass authoritative same-duty history; unchanged preparation may reuse the exact current artifact. A first FINAL following an INTERIM duty remains distinct. |
| Terminal failure contradicted by later success evidence | Keep both observations and the reconciliation requirement. Block new financial approval, admission, claim and first send, including a previously READY replacement. Do not release commitments or choose a winning fact automatically. Independent communications and fact ingestion are not globally disabled. |
| Lower deduction after application/refund | Recompute liability and actual held cash separately. Accept targeted positive application/posting reversals as needed; only returned held cash can fund an additional refund. Preserve both original and correction transactions. |

For a native reversal or return, `MoneyEvent.requestId` retains the **original canonical transaction chain's request identity** (and original charge-item association). The D accepted workflow event retains correlation to the actual new performing reversal request. This is intentional compatibility with native transaction validation: do not relabel the reversal as a new refund settlement or overwrite the original request to make the IDs look alike.

### Stop/rollback procedure

First **stop new claims and new commitments** if a discrepancy, access concern, unexpected version or inconsistent result appears. Retain all attempted instructions, reservations, raw/accepted results, approvals, issued content and command receipts. Inspect the persisted root/snapshot, current request facts and canonical transaction chain under the existing read policies. Reconcile late outcomes before considering replacements; do not delete rows, reset an unknown request to `READY`, downgrade a v2 root, or restore an older snapshot over accepted history. Any code-version rollback requires a reader/writer compatible with existing v2 state and an explicit reviewed deployment decision; rolling back code is not undoing business effects. Unattempted work can be withdrawn through the named Actions when its preconditions are met.

## Observed synthetic acceptance

These are results of the constructed branch checks for the known runtime, not universal guarantees or a new test run by this document. All **15 new D Actions** were exercised, including scope, party, interim qualification, revocation and cancellation. Selected inherited recheck/choice/evidence/charge-decision bridges were exercised; the retained C acceptance record is in `docs/phase_c.md`. This does not claim all 30 Actions were successfully retested under every D condition.

| Observed case or check | Result |
| --- | --- |
| Ordinary basis and performance | The initial unknown item stayed null. Accepting the additional $150 produced 40000 cents deductions / 160000 refund. Frozen statement and exact approvals supported simulated dispatch, posting 40000, application 40000 and refund 160000. No raw result prematurely counted as performance; expected effects did not invalidate approvals. |
| Return, replacement and uncertainty | A 160000 refund return was a separate event, with the old settlement retained. During replacement uncertainty, 160000 remained reserved and native finances were null, not zero. Cancellation and blind new approval were blocked; late acceptance of the same instruction resolved it. After replacement, gross paid 320000 minus returned 160000 equaled net refunded 160000. Exact and semantic replays added no economic effect. |
| Paid correction, ordinary case revision 58 | Lowering deductions from $400 to $350 left held cash 0 but an extra 5000 owed. A new positive refund request was actually blocked until acceptance of a 5000 application reversal restored cash; a 5000 posting reversal and additional refund followed. Old issued content stayed frozen, and a corrective version was issued. Endpoint: net posting/application 35000, net refunds 165000, held 0, owed 0; simulated deposit completion true, legal performance false. |
| Preperformance correction, revision 30 | Old `READY` intent was superseded without a fabricated replacement. An unissued `FINAL` was explicitly linked to its replacement: old $400/$1,600 content remained frozen, new content $350/$1,650. Statement dispatch succeeded with refund routing `UNCONFIRMED`; after routing was restored, settlement completed. |
| Zero refund, revision 19 | Held deposit 40000 and deductions 40000 implied refund 0. With refund routing `UNCONFIRMED`, no refund requests/events or zero-dollar payments were created. Statement, posting and application completed; simulated deposit completion true. |
| Interim, revision 11 | Invoice-delay-only preparation failed. A distinct stipulated qualification was explicitly accepted; the `INTERIM` statement was simulated-issued while the additional amount remained unknown and `interimMoneyPolicy` unresolved. No cash operation; final scope remained blocked and simulated completion false. This is not a legal finding on a 30/60-day test-date assumption. |
| Forced request overlap | Two 100000 requests both read revision 4 against 160000 capacity. Only contender B committed root revision 5: reserve 100000, available 60000. A encountered concurrent modification / `Actions:ObjectVersionChanged`, then stale-retry rejection; none of A's losing rows or receipt remained. Same instruction/different command did not double reserve; a fresh 100000 overcommit was rejected. |
| Withdrawal and recipient boundary, overlap case revision 16 | B's approval remained `APPROVED` but invalid, with a separate `REVOKED` decision; its `READY` request became `SUPERSEDED`. A was then admitted and cancelled while `READY`. No money moved even in the simulator. Joint recipient membership retained null principal/no grants; access was unchanged and statement/refund channels remained independent. The endpoint was a joint-recipient preview, not an issued statement; simulated completion false. |

The primary five-case checkpoint observed **7 statements, 22 approvals and 20 requests**: 17 `SUCCEEDED`, 2 `SUPERSEDED`, 1 `CANCELLED`, with 134 command receipts. A sixth deliberately conflicted case was then added for the audit regression. Its accepted FAILED result and later contradictory raw SUCCEEDED result remain distinct; a READY replacement retains its 160000-cent commitment and has no attempt. Actual ingestion, new approval and replacement claim were all rejected with unchanged root/hashes/counts and no failure receipts. Native accepted-fact arithmetic can remain known while v2 operational work is blocked: numerical capacity is not permission to pay.

The issued-lineage audit regression also used an actual preparation Action against the completed corrective case. `FINAL` with an omitted predecessor was rejected; the existing issued versions were not replaced. Both audit fixes are covered by the final 959-test suite and actual branch checks. A separate source-only Main query saw zero visible cases. These are scoped observations, not permanent inventory totals, proof that all Main data is absent, or a guarantee that branch fixture data would be copied during deployment.

Broader UTF-8, timestamp, exact-arithmetic, budget, partial-return, storage-contract and request variants are covered by native regressions; do not label every such matrix variant as an actual platform Action trial. The overlap result supports the tested loaded-root edit-batch path, not all storage configurations or alternate writers.

## Outstanding boundaries

- Contradictory terminal failure/success adjudication is deliberately not automated or resolved by a generic override. The case stays blocked with named reconciliation work and preserved evidence; further verified source correction is required before it can safely proceed. Do not mistake this safe exception boundary for a completed reconciliation.
- Production multi-principal access/isolation and legal certification have **not** been tested. Only the configured constructed operator was used; the Handoff project has broad Owner access within the organization. Whole-record policies, including JSON fields, do not make that a production access certification.
- These functions record and reconcile facts in the Ontology. They do not establish external transport, provider settlement, or provider exactly-once behavior.
- No UI, models, automations or live connectors are implemented. No Main seeding/merge or Phase E work is included.
- The canonical current configuration is `docs/tsv2_release_manifest.json`; payload authority remains in the typed code/codec. Do not weaken limits, invent defaults for unknown money, or remove accepted history to make a case appear complete.
