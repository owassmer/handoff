# Phase C — stored case workflow

## Delivered boundary

One native TS review, eight linked object types, fifteen named case Actions and one guarded persistence path. All input remains constructed and all runtime tests were executed on the Phase C branch. There is no statement/approval/outbox/payment/ledger-execution workflow, model, UI or automation in this phase. Recording an accounting observation does not execute the observed operation.

The Action server binds the actor using `current_user_id`. A case ID is resolved on the server; caller-supplied object properties, role labels and grant booleans do not grant access. Current case scope, readership and applicable accepted authority are checked at actual server time. The test profile remains restricted to `constructed-company-001` and the approved operator; it is not a production multi-user security certification.

## How a command works

1. Resolve the actual case and accepted current snapshot; validate identities, hashes, projection version and current authority.
2. Decode only the fixed operation's contract and compare its stable command receipt. Identical authorized replay returns no edits; different intent under the same command ID is rejected before reapplying state.
3. Check the expected revision, source evidence, operation applicability and exact numeric bounds.
4. Change a copy of accepted state and call the unchanged native review.
5. In one batch, update the loaded case root once and write the new review, receipt and current projections. Do not read the execution's own pending edits.

Required-work assignment is a validated snapshot sidecar and survives unrelated changes. Disappeared requirements become inactive, not falsely performed. Statement and financial histories are not rewritten.

## Action surface

Open case; add evidence; associate evidence; accept/correct a date fact; record a charge decision; choose a supported amount; waive a supported charge; set recipient instructions; record a money fact; reconcile a balance; update case authority; assign work; record a related-task result; recheck at server time; advance the synthetic demonstration clock.

Most Actions take `caseId`, `commandId`, `expectedRevision` and a fixed-contract `payloadJson`. Open takes a structured request; choice has explicit item/amount/reason parameters; recheck has no fact payload. Only the synthetic overlap tests use the bounded optional delay. A command ID must be retained across retries. An Action's successful reply does not imply a statement was sent or money moved; inspect its receipt and current case state.

## Verification performed

### Native and platform build checks

- 475 native tests pass; five unchanged template examples are skipped.
- Strict TypeScript compilation and Function discovery pass.
- The branch Function release used for platform acceptance, `1.1.0-branch-20260918-023934`, passed tagged CI.
- Existing Action definitions were refreshed after the edit union grew from four to eight types. Updating a version range alone did not refresh their cached editable-type declarations.

### Actual stored-case results

- Opened and reloaded a case; full projection initialization and a fresh version-one opening both succeeded.
- The original unknown additional item stayed unknown, not zero.
- Added and explicitly associated final evidence, then accepted and explicitly chose the additional $150: $400 deductions / $1,600 proposed refund.
- Changed only the selected repair deduction from $250 to $200: $350 deductions / $1,650 proposed refund. The $800 owner repainting remained excluded.
- Tested waiver and restoration through Actions, without any cash movement.
- An explicit source-date correction did not move the separately accepted accounting trigger or the test legal due date.
- Stored recipient instructions v2, an accounting observation, a reconciled balance and an evidenced related-task result. The recorded CHARGE_POSTING35000 removed the additional posting delta but did not reduce held funds or imply deposit application.
- Assigned ordinary accounting work to the manager with internal target2026-09-25; the test legal due date remained2026-10-02. Assignment survived subsequent changes and recheck.
- Revoked manager authority, observed a real charge-change rejection, then restored authority through the administrator operation.
- Rejected an owner-cost deduction, conflicting reuse of a command ID and an association to evidence that existed only in another case.
- Exact command replay after later revisions returned no edits and did not roll back the restored choice, assignment or demo clock.
- Advanced the demo clock to2026-10-03. Arithmetic remained35000/165000; the ordinary requirement's state remainedOPEN and its explanation marked it overdue. This preserves the existing separation between operational state and timeliness. Recheck uses actual server time, so it is a different operation from holding a future demonstration clock.

### Actual concurrency evidence

Two forced-overlap checks, not just unit simulations:
- Initial charge contenders both logged revision2. One committed; the other encountered `Actions:ObjectVersionChanged`, was retried by the platform, and failed the explicit stale-revision check. No losing review or receipt was present.
- With the completed eight-type implementation, two rechecks of a fresh case both logged revision1. One committed to revision2; the other again encountered `Actions:ObjectVersionChanged` and then stale-revision rejection. The case has two reviews/two receipts: opening and the winner only.

These results support the tested normal Action/edit-batch path; they do not certify every deployment configuration, storage engine or future alternate writer. Every future command must retain the same loaded-root update discipline, actor checks and transaction boundary. Do not replace it with an application-only revision comparison or a process mutex.

The separate late stale-request trial was not counted as forced-overlap proof.

### Branch fixture endpoints

The full demonstration ending tenancy is `constructed-tenancy-001`, currently revision26, with26 review snapshots and26 command receipts. Its proposed refund is165000 cents, recorded posting35000 and additional posting delta0. Both completion flags are false. The fresh-opening/concurrency tenancy is `constructed-tenancy-c-opening`, currently revision2, with two reviews and two receipts. These are branch test records, not customer records or Main data.

## Limits and further acceptance

- Main merge is not performed by these tests. Code/schema review and a later deployment remain separate from branched object edits; do not assume fixture data is copied to Main.
- Only the configured test principal was used. Current-authority revocation was tested at runtime; a separate-principal data-access campaign and production project hardening remain necessary before real deployment.
- JSON payloads/snapshots are bounded at256KiB; each projection family is bounded at1000 rows. Exceeding a bound fails closed.
- Review clocks must be exactly representable in milliseconds. Source timestamps retain microseconds in canonical JSON/ISO projection fields. UTC input is required.
- Phase C uses the existing synthetic legal release. Neither completed work records nor successful Actions establish legal compliance or financial settlement.
- No generic patch endpoint, administrative cleanup Function, alternate backend or external authentication workaround is retained.

## Developer setup

Use the existing local SDK and supported imports. For branch-only schemas, follow environment preparation with:

```sh
./rune sdk generate --sdk-package-name ontology --branch-rid <the-global-branch-rid>
```

`rune env prepare` alone may regenerate against Main. Use generated declarations, not guessed object APIs. When a function's edited-type union changes, refresh the corresponding Action definition as well as publishing the function. Server actor binding must not be replaced by a hidden, caller-settable field.
