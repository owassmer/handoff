# Phase E.1 — backend workspace query and compact queue

## Scope

`getCloseoutWorkspace(client: Client, caseId: string, intentSpecJson?: string): Promise<string>`
exposes the public query API name `getCloseoutWorkspace`. `client` is injected, not a public parameter.
This remains the only new Function. The three existing query interfaces/outputs, thirty edit Function
interfaces and eleven-object edit union are retained. A private pure queue projection adds eight optional
root properties to the same single root create/update in the existing shared edit batch. Native scope,
financial math, lifecycle reducers and actor admission are unchanged. No separate writer, new object type,
UI implementation, Main seed, administrator Function, egress, permission expansion or legal activation is
included. Constructed branch-only data was created through actual Actions for the acceptance record below.

As of 2026-09-20, the user-approved scope is **backend first**: the E.1 query and queue are implemented,
published on the branch and backend-accepted; **Main remains on 1.2**. The user merges the backend-only
proposal before UI SDK/query integration resumes. The existing approval to continue the full UI work
remains in force after merge confirmation; no additional GO is required. No automatic merge or Main data
writes are authorized, and no frontend changes belong in this backend proposal.

The existing local SDK (`@ontology/sdk`) is generated against the Phase E global branch after environment
preparation with `./rune sdk generate --sdk-package-name ontology --branch-rid <global-branch-rid>`.
`resources.json` is unchanged; the imports inspection tool does not enumerate this local resource-file
format correctly. The file and Rune both resolve eleven objects and eleven configured links.
The repository's AGENTS.md, README query configuration and generated local SDK declarations govern usage.

## CloseoutWorkspaceV1 transport

A canonical JSON string, schema `1.0.0`, with **exactly** these six fields:

- `metadata`: case/company/environment/home/tenancy identity; `caseRevision`, `currentReviewId`, input,
  effective-review, assignments and workflow-state hashes; explicit input/review/code/rule/projection/
  workflow versions; `reviewClock`, `snapshotCreatedAt`, `authorityEvaluatedAt`, `authorityEvaluationBasis`
  and `readAt`; explicit case-wide action-availability and preview-semantics labels.
- `request`: accepted native `ReviewRequest`, unchanged.
- `workAssignments`: complete validated assignments, including retained inactive/historical assignments.
- `workflow`: complete `WorkflowStateV2`, or explicit `null` for a known uninitialized legacy case.
- `review`: `{ kind: "WORKFLOW_V2", value: WorkflowReviewV2 }` when initialized, otherwise
  `{ kind: "LEGACY_BASE", value: ReviewEnvelope }`. Never both and never a v2-to-native cast.
- `intentPreview`: the discriminated result described below.

The authoritative exact fields and decoder are in `src/deposit_closeout/workspace/types.ts` and
`codec.ts`. Known legacy projection/workflow versions absent or `"0"` are normalized to `"0"` in the DTO;
unknown versions and partial/mismatched sidecars reject rather than fall back.

### Numbers and clocks

`metadata.caseRevision` is the SDK Long's canonical decimal **string**. The accepted native
`request.snapshot.revision` remains a positive **safe integer JSON number**. Existing `checkedLong`
rejects unsafe conversion, rather than rounding. Amounts remain exact native safe-integer cents.

Timestamps use existing exact UTC normalization (no fraction for whole seconds, otherwise six fractional
digits). `reviewClock` is business time. Workflow authority is the persisted snapshot's authority clock,
not re-evaluated at read time. Legacy base authority is evaluated at its native review clock, explicitly
labelled `LEGACY_REVIEW_CLOCK`; the query does not mislabel snapshot creation as legacy authority time.
`readAt` is actual server time sampled after loading/constructing the workspace, before output validation
and the final root check. It is not an authorization clock or the time the response arrives at the client.

### Intent preview

Omit `intentSpecJson` for `{ status: "NOT_REQUESTED" }`. Otherwise supply the exact six-field
`OperationIntentSpec`; all nullable fields are required:

```json
{"kind":"REFUND","amountCents":600,"dispositionKey":"installment-1","statementId":null,"replacesRequestId":null,"reversesTransactionId":null}
```

The existing lifecycle command decoder validates this shape without executing any command. The existing
pure `buildIntent(request, storedBaseReview, workflow, spec)` constructs the exact target. Results:

- `{ status: "CONSTRUCTED", spec, intent }` — business target construction only.
- `{ status: "BLOCKED", spec, reason: { code: "WORKFLOW_NOT_INITIALIZED", message } }`.
- `{ status: "BLOCKED", spec, reason: { code: "INTENT_CONSTRUCTION_BLOCKED", message } }`.

A well-formed but inapplicable spec does not prevent viewing the workspace. Invalid JSON, duplicate or
unknown keys, omitted nullables, illegal combinations, unsafe numbers and excessive input bytes reject
the entire call with `Closeout workspace [INVALID_INTENT_SPEC]`. A constructed target does **not** mean
actor authorization, current authority, request readiness, approval, held cash admission, or reservation.
There is no actor parameter. Existing case-wide action availability is not a current-user permission map.
Existing Actions must still bind the actor and recheck authority, revision and request admission.

### Validation, bounds and consistency

The query reads the policy-visible root by PK, calls `loadCurrentReview` (now also validating a present
queue against the exact accepted generation), validates the complete output, then re-reads the root.
A changed revision, pointer, scope, versions, clocks, access fields or any of the eight queue fields rejects
with `Closeout workspace [GENERATION_CHANGED]`; this is the only new error marked `retryable = true` in
code. Retry the **whole** query and discard the old target. This detects observed generation changes; it
is not a transaction snapshot, lock or proof that a case cannot change after the final read. SDK policy,
not-found and transport failures propagate; they are never treated as legacy or empty data.

The output codec composes existing request, work-assignment and workflow codecs and reuses the native
and workflow reviews. It validates exact fields, nested contracts, hashes, known versions, scopes and
recorded clocks. No second financial or lifecycle implementation exists. Serialization failures are
`Closeout workspace [INVALID_WORKSPACE]`. Existing stored-data contract failures retain their existing
user-facing errors. `code`/`retryable` are server error-class fields; clients must not assume arbitrary
custom fields survive Foundry error serialization. The stable message prefix identifies the new errors.

Bounds are inclusive **4 KiB UTF-8** for intent input and **1 MiB UTF-8** for the aggregate workspace.
Existing request/review/assignment **256 KiB inclusive** and workflow **256 KiB exclusive** limits are
retained. Oversize content rejects, never truncates. There are only three object lookups: root, current
snapshot, root; no child projection scans, event overfetching or pagination of JSON arrays.

## Compact root queue (schema 1.0.0)

`workspace/queue.ts` is a private pure display projection, not a registered Function or business engine.
It consumes the accepted request, effective v2 review (otherwise the known legacy base review),
assignments and the exact `currentReviewId` returned by `appendReviewAndReceipt`. All thirty existing
edit Functions share this persistence path. Opening creates the root once; every accepted new command,
including a semantic no-op, updates the loaded root once in the same batch as the review, receipt and
existing projections. Exact authorized replay still returns no edits; a losing/stale command cannot
refresh just the queue. Exceptions, including oversize output, abort the whole returned command batch.

Eight optional root properties, under the existing case reader policy:

| API name | Storage / meaning |
| --- | --- |
| `queueSummaryVersion` | Long, canonical SDK string `"1"`; separate from unchanged `projectionVersion="1"` and `workflowVersion="2"` |
| `queueAttentionKind` | One fixed category below; organizational display, not authorization |
| `queueNearestLegalDueDate` | Date copied from a review-provided, applicable unfulfilled LEGAL requirement |
| `queueNearestInternalTargetAtIso` | String `YYYY-MM-DDTHH:mm:ss.ffffffZ`, always six digits, for indexed exact ordering |
| `queueNextRequirementKey` | Selected next requirement, if that work has a requirement |
| `queueNextResponsibleRole` | Selected next work's role; not an access grant |
| `queueNextAssigneePartyId` | Assignment of that selected requirement only; not any/all work assigned to this party |
| `queueSummaryJson` | Nonindexed canonical compact JSON, inclusive 32 KiB UTF-8 maximum |

Every write supplies **all eight keys**. Inapplicable optional root values are explicitly `undefined`
in `batch.update`, which the SDK translates into property clears, never omitted patches retaining an
old due date, assignee or requirement. Preview serialization also shows explicit `null` clears on root
creation. JSON nullable values are always explicit `null`; known zero cents remains `0`, never unknown.

### Compact JSON fields

- `schemaVersion`: `"1.0.0"`.
- `metadata`: case/company/environment/home/tenancy scope, decimal-string `caseRevision`, exact
  `currentReviewId`, `reviewClock`, `inputHash`, `effectiveReviewHash`, `workAssignmentsHash` and
  `effectiveReviewKind` (`LEGACY_BASE` or `WORKFLOW_V2`).
- `scopeState`; `attention` (`kind`, fixed display `label`, machine `reasonCode`).
- `nearestLegalDue`: requirement key, copied date, `dueKind`, `ruleQuestionId`, `triggerFactKeys`, or null.
- `nearestInternalTarget`: requirement key and fixed-six-digit `atIso`, or null.
- `nextWork`: `workKey`, nullable `requirementKey`, question, responsible role, nullable assignee/action
  key and `selectionBasis`; or null. Action keys come from the effective review. Initialization has
  `workKey="workflow:initialize"`, no invented review action or requirement, and no inferred assignee.
- `availableActionKeys`: unique currently available non-maintenance action IDs, so an unresolved money
  issue never hides independent communications/preparation work. `reconciliationRequestIds` are unique.
- `account`: copied currency, recorded deposit, chosen/total deductions, existing posting/application,
  their separate deltas, prior refunds, reserved refund, final refund, excess receivable, newly requestable
  refund, final-account readiness and reconciliation state. No balance, reservation or refund recalculation.
  `newlyRequestableRefundCents` is null without v2, never guessed from the base amounts.
- `tracks`: each authoritative track and state separately. `completion` copies the two simulated flags;
  real deposit/overall completion and legal-performance confirmation remain false, mode `SIMULATED`.

No evidence bodies, full workflow, event history, statement text or cached wall-clock overdue flag is
stored here. `reviewClock` is the as-of clock; use the existing explicit recheck/clock command to refresh.
The workspace DTO retains its exact six top-level fields and metadata contract, without a second queue
payload. Queue readers use the root fields; the workspace read validates their generation.

### Deterministic display priorities

Attention uses only machine states/keys and validated review details, never matching English reasons:

1. `RECONCILIATION`: any deduplicated request flagged for reconciliation/unknown outcome, a legacy
   unknown request, non-reconciled account or named `money:` missing input.
2. `UNSUPPORTED_SCOPE`: unsupported or interpretation-required scope.
3. `NEEDS_FACTS_OR_DECISION`: missing inputs, reviewer-required items or missing scope facts.
4. `LEGACY_INITIALIZATION`: known uninitialized workflow, after higher-priority issues above.
5. `SIMULATED_COMPLETE`: the authoritative simulated **overall** workflow flag, not only deposit completion.
6. `READY_WORK`: available non-maintenance work.
7. `WAITING`: remaining prerequisites/results.

Repeated v2 request details across actions are deduplicated by request ID; conflicting copies reject.
No repeated amounts are summed. Reconciliation attention and legal-date selection are independent.
Legal dates exclude `FULFILLED`/`NOT_APPLICABLE` requirements and select date then requirement key.
Only existing review dates are used: no new deadline rule or legal certification.
Internal targets use assignments (including explicit null clears), falling back to the review only when
no assignment exists. Inactive/fulfilled work is excluded. Ordering uses existing exact
`compare_timestamps`/microsecond logic, then requirement key; whole seconds serialize with `.000000Z`.
There is no milliseconds truncation, lexical error from omitted fractions or legal/internal conflation.

Next work first targets reconciliation or unsupported scope, then initialization when it is the
attention category. Otherwise it prefers an available action (reconcile, claim, request, approve,
statement preparation, other; lexical action key ties), followed by missing-input/open requirements.
Requirements sort by legal date, then exact internal target, then key, null dates/targets last.
Approval actions associate with the approval requirement; financial work with money; dispatch/preparation
with the earliest open communications requirement. `selectionBasis` explains this **navigation suggestion**,
not actor authority or proof that a displayed blocked action is runnable. Other available work remains
visible in `availableActionKeys`. An “assigned to me” filter means **next work assigned to me**, never
all assigned work or a row-level security rule.

### Legacy and corruption handling

Only all eight queue properties absent is known pre-E state. Reads do not repair/backfill it. The next
ordinary accepted command writes version 1 atomically. A present version must be exactly `"1"`, with
all values matching the pure expected summary recomputed from that accepted review, assignments and
pointer. Partial/all-nil versioned summaries, unknown versions, invalid JSON, stale indexed properties,
foreign scope and mixed equal-clock generations fail closed. No fallback to a legacy or zero summary.
The workspace's final root check includes all eight properties as well as existing generation fields.

## Backend verification and acceptance — 2026-09-20

### Logic validation

Strict compilation and the full normal-concurrency Vitest suite pass: **1,107 passed, five unchanged
template skips** (959 inherited + 90 workspace + 58 queue). New fixtures cache setup then isolate each
store; no old timeout increase, skipped regression or relaxed business assertion. The inherited exact
root-key expectation now includes the eight required queue keys, and the workspace test's manually
constructed historical-assignment snapshot now also supplies its coherent queue hash.

Queue coverage includes open/C choice/operational/D persistence, one-root batch, semantic no-op/replay
and stale revision, every queue field's corruption/final-read race, all-absent legacy and unknown/partial
versions, exact/equal microseconds, assignment clearing, zero/unknown/interim values, fulfilled deadline
clearing, independent routes, actual simulator settlement/correction/conflict, repeated details and UTF-8
bounds. The complete existing suite continues exercising the thirty shared command routes and native math.

Rune discovers **34 Functions, zero diagnostics** (four queries, thirty edit Functions; unchanged
11-object edit union). A branch-only Rune preview of `openCloseoutCase` returned 22 edits, including all
eight queue fields and explicit null clears, without applying any object edits. That earlier preview is
not counted as an Action submission. No standalone ESLint task exists; new-file formatting checks use
the installed Prettier.

### Accepted runtime and branch configuration

The exact tested logic commit is `159fcf1fee43264fd2014d1d72977dfe1c0d3649`, published as
`1.3.0-branch-20260920-213828`; **tag CI passed**. The documentation closeout does not change runtime logic
or require another Function publication. This tag is a branch prerelease, not a Main release.

- Backend repository: :resource[ri.stemma.main.repository.40ca55f8-0251-478b-95fc-0b2e5126641e]{globalBranchRid="ri.branch..branch.065df81c-5f66-41a3-bf2e-3c0c214715de"}.
- Global branch: :resource[ri.branch..branch.065df81c-5f66-41a3-bf2e-3c0c214715de].
- Ontology branch: :resource[ri.ontology.main.branch.267d57c9-763c-4ab9-a959-d2444f03a194].
- Code branch: `ai-fde/owassmer1/deposit-closeout-phase-e-iZqyfb`.

All **30 branch Action rules** now select `>=1.3.0-0 <1.3.1-0`. Server binding to `current_user_id`, the
positive approved-principal admission and the eleven-object edit union were verified unchanged. The ten
existing child object types were initialized on the E branch by identical complete definition get/put
with `importMainEdits=false`; their 178 existing properties and policies are unchanged. These are branch
initialization entries, not ten new types or permission changes. The only semantic object-schema change
is the eight optional queue properties on the case root.

### Actual Action acceptance, not mock or preview writes

Acceptance ran **after** the Action rebinding and child-type branch initialization. All **15 actual Action
submissions** explicitly targeted the E ontology branch with `appliesToMain=no`: **13 new commands applied,
one exact replay returned zero edits, and one stale command rejected without a receipt**. This is a
selected integration sequence, not a claim that all thirty Actions or every native matrix variant were
submitted on-platform in Phase E.

Two constructed cases were used; IDs below are object primary keys, not additional resources:

| Case | Case primary key | Final revision | Final current review primary key |
| --- | --- | --- | --- |
| A | `dc-case:84a3ec2a7fe98158abc3d9779a95bac99ffb434180a4596881669c5bd04dc80b` | 9 | `dc-review:c0e5ab68c9b12087a82764280f1e66e0c0810bdd9d4765ea1fa2f3ecd3dc5010` |
| B | `dc-case:f8b3f5a3f4b235627a74d395935c8bd9a31f3bfab4a6541b848bb57ebb3d2e40` | 4 | `dc-review:1f57ef171b8e32d3e8ac830bacf7023c955fb60ea9311df0ea43a9022d7000d4` |

**Case A — queue persistence, unknown amounts, exact timestamps, replay and clearing**

1. Opening produced revision 1; explicit workflow initialization produced revision 2. A retained case
   charge-choice command selected **20,000 cents** at revision 3. Another item remained unknown, so queue
   total deductions, unpaid liability and newly requestable refund remained **null**, not guessed totals.
2. Assignment at revision 4 stored `2026-09-25T15:30:00.123456Z` exactly on the root, requirement and queue
   JSON. Clearing that internal target at revision 5 yielded SQL `NULL` on both root and requirement and
   JSON `null`; assignee `demo-accountant` and legal date `2026-10-02` were retained. Internal-target
   clearing did not erase a legal deadline or the work assignment.
3. Recheck produced revision 6. Exact replay reused the same command and original expected revision 5:
   zero edits, no extra receipt/review, and unchanged queue, hashes, pointer and counts at revision 6.
4. Evidence addition and association produced revisions 7 and 8. Accepting constructed unsupported
   jurisdiction `ZZ` at revision 9 cleared the old `2026-10-02` root legal date to SQL `NULL`, made queue
   `nearestLegalDue` null, and cleared the next assignee. The old NC requirement became `isCurrent=false`,
   **not complete**. No legal completion was asserted.
5. Command `phase-e-20260920-accept-a-stale`, expected revision 8 against actual revision 9, rejected on
   the exact accepted runtime above. There was no failed-command receipt and no partial queue write.

**Case B — statement preparation independent of refund routing**

The complete `NC-A-002` case-request fixture was opened at revision 1 and initialized at revision 2.
Refund instructions were set to `UNCONFIRMED` at revision 3. An actual statement `PREPARE` command still
succeeded at revision 4, despite the missing refund route. The current-basis statement is **NOT_ISSUED**:
`dc-statement:f10450d3dd5588c6a6cb52c09e91ac07daf44ed12fbde5c0daa0ac8432196358`.
No approval, operation request, dispatch or money effect was created by this sequence.

**Generation and write-isolation checks**

All 13 command receipts link to their matching reviews (A: nine; B: four), with **zero orphan receipts**.
For every accepted generation, the queue/root/snapshot revision, input hash, work-assignment hash,
effective-review hash and review pointer matched. The final E-branch counts were:

| Type | Count |
| --- | ---: |
| Case | 2 |
| Review snapshot | 13 |
| Execution event / command receipt | 13 |
| Case party | 8 |
| Evidence record | 18 |
| Charge item | 6 |
| Requirement | 10 |
| Statement version | 1 |
| Approval | 0 |
| Action request | 0 |
| Money event | 0 |

**All eleven Main object-type counts were zero before and after this acceptance.** No Main seeding or
Phase E merge occurred. No financial execution, external effect, real/legal completion or automatic
backfill is represented by these observations.

### Stored query checks and the remaining consumer gate

Positive `function_preview` reads used actual stored branch data: A in legacy mode at revision 1, A in
v2 mode at revision 9 with the clears above, and B in v2 mode at revision 4. B's exact-intent preview was
`CONSTRUCTED` with the matching statement hash, and returned no edits. The unchanged `getCloseoutReview`
base 1.1 envelope was confirmed on A at revision 1 and B at revision 4, retaining all six result fields.
Supplemental Rune execution explicitly on E confirmed canonical JSON with exactly six top-level fields;
metadata revision `"9"` was a Long string while native request revision `9` was a JSON number.

These are **backend stored reads and authoring/Rune previews**, not browser acceptance or a successful
published-query HTTP call. They do not certify multi-principal permissions, contention or UI routing.
Separate frontend work has 81 passing mock protocol/component tests and three skips with CI passed, but
those remain mocked/read-only diagnostic evidence and are **excluded from the backend proposal**. Its
current SDK 0.4 exposes only `getCloseoutWorkflow` 1.2; the workspace branch import failed with a generic
SDK-generation error, and the user confirmed `getCloseoutWorkspace` is not visible in Developer Console.
No consumer gate is marked passed on that basis.

The approved handoff is the backend query-and-queue scope only. After the user confirms the backend
merge, verify the Main 1.3 release and new query schema, regenerate the frontend SDK from **Main
definitions**, and continue the already-approved full UI validation on a **fresh validation global
branch** without Main seeding. Merge confirmation is the remaining prerequisite, not another GO request.
Main is still 1.2 at this record; neither merge nor frontend integration/acceptance is claimed here.
