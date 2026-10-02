# Independent implementation challenge — coverage tracker

2026-10-01. Read-only implementation review, with temporary isolated runtime reproductions. Scope: `pipeline/coverage.py`, coverage CLI, aggregate `check.py` integration, and `tests/test_coverage.py`. Applied code-review methods; report location follows the explicit assignment. No author implementation/source edits. This is an intermediate review: follow-up integration and the fresh substantive demonstration are still under development.

## Reproduced findings

### P1 — Reordering old reviews could erase a later challenge: corrected and rechecked

Original `review_errors` used the last matching review in list order. `save` enforced review identity/content immutability but allowed reordering the list. Starting with a complete fixture, I appended and saved a `changes_required` review of the unchanged source target: assessment became incomplete. Moving that same challenge before the old passing review and saving made assessment complete again, without a new review. This violated the stated later-challenge supersession contract.

Requested fix: enforce the prior review list as an exact ordered prefix, or persist an immutable sequence used for precedence. Parent implemented the ordered-prefix check in `save`. Independent recheck now rejects the reorder with `reviews are immutable and ordered; append new reviews after the existing prefix`. No unresolved issue remains from this reproducer.

### P1 — Current register could point to a new source while old review stayed complete: corrected and rechecked

Original register reconciliation compared section IDs only. I bound a reviewed boundary selecting section A, with its saved `source.txt`, then changed the current register's A row to point to `replacement.txt` containing different legal text. The old source remained on disk. Assessment stayed complete, so neither saved-byte checks nor membership equality detected the current-source replacement.

Requested fix: bind complete selected register-row identity and require explicit source/version reconciliation when that identity changes. Parent added `register_record_sha256` and comparison against the current selected rows, plus duplicate-ID detection. Independent recheck: the correctly bound original register completes; changing only its `text_file` now makes assessment incomplete with `current register source/version differs: A`. Parent additionally binds seed imports to complete sections/instruments files so new units outside initial selectors remain visible.

### P2 — Save accepted a source record that status could not assess: correction pending recheck

`validate` originally used `source.get("versions", [])`, accepting an omitted versions field, while `assess` indexed `source["versions"]`. I removed that field from a source, saved revision 1 successfully, loaded it and called assessment: unhandled `KeyError: 'versions'`. Honest unfinished investigation may have zero known versions, but persisted valid records must remain assessable.

Requested fix: require the structural versions key/list at validation, or consistently interpret its absence as empty/open in assessment. Apply the same structural discipline to new imports and nested lists; do not store a malformed document and later fail with a raw implementation exception. This finding does not claim false closure, but breaks the intended durable resume/status workflow.

## Integration concern to address

New complete-register import bindings are useful. Preserve and validate their identities too: dropping the whole-register import can remove discovery-change detection for newly added units outside existing selectors. A fresh scope review invalidates old acceptance, but removal should also require an explicit reconciliation/scope-change reason, rather than silently discarding the upstream link. Imported follow-up observations retain source evidence on each work item; whole-register discovery evidence must receive equivalent deliberate treatment.

## Verification and positive findings

- Ran `python3 -m pytest pipeline/tests/test_coverage.py -q`: 17 tests passed at initial review. These tests did not catch the two P1 reproducers above.
- Independently exercised truly simultaneous writers in two processes, both expecting revision 1: one saved revision 2, the other received the explicit stale-update error; latest revision remained 2. This supplements the existing sequential CAS test.
- Existing process-death test passed: an uncommitted database change rolls back and a subsequent writer resumes. SQLite transactions with `BEGIN IMMEDIATE` simplify the originally proposed snapshot-pointer protocol and avoid a separately recoverable stale lock file.
- Content-only transitive graph binding terminates with cycles and invalidates ancestors when a dependent conclusion changes. Unknown and required-but-excluded dependencies remain blockers. Reviews do not recursively hash review records.
- Scope-wide review binds all non-review document content. Enumeration comparison uses exact membership, verifies the inventory artifact and its authority evidence, and blocks missing expected sources. Agent statements remain substantive evidence to review, not truths certified by code.
- Source/currentness/finding/review/inventory changes are checked through retained hashes. The checker distinguishes legal applicability dates from research currentness; a later assessment date cannot simply reuse an earlier checked-through date.
- The default aggregate J8 check now fails when declared research coverage is open/untracked and prints coverage separately from legacy stages. Earlier-stage checks remain earlier-stage checks. No automatic grant comes from legacy routing or model negatives.
- The follow-up importer retains model observations, exact prior row content, target strings and broad leads as open questions and required dependencies. It does not promote successful retrieval or a model-negative to closure. Full demonstration of actual imports remains pending.

## Reviewed intermediate identities

The code is being corrected concurrently. These identify the intermediate snapshot after the two P1 repairs, not a final release acceptance:

- `coverage.py`: `b4ccb8c7dbc6ae9033206361c3194fadd5d4fc8beedfa5c63f8d6ef94c137b8c`
- `__main__.py`: `9425060699b235ead55f6eb28f02875c165e2f4cd2fe553b031d0824b3eb6060`
- `check.py`: `913017403d0df8bc9b4720d67052d0a2175359ff1b812e8954542073b5c7bdd9`
- `tests/test_coverage.py`: `9e64b26ab119a7425b4d17c1148933f78abea1dd4172e1009648a0a8580ad94d`

Conclusion: two material false-closure defects found, fixed and independently reproduced as blocked. One malformed-record finding and import-retention concern await recheck. No final implementation or Goal 4 acceptance yet; the fresh source boundary, legal conclusion, interrupted/resumed demonstration and final regressions require separate final inspection.

## Second implementation pass

Rechecked the expanded adapters, README, record retention, transaction validation and actual live state. All 21 coverage tests pass. The earlier P2 is corrected: omitted source versions are rejected before persistence. Imported and completed-research identities are now validated and retained, with explicit reconciliation required for changed links. Save validates the full revision chain inside its write transaction. Assessment caches verified artifact bytes, parses the inventory from those bytes, and detects external changes before returning.

The live `CA/california-research` scope at revision 3 contains 166 source items, 71 questions and 9 prior accepted-report links, and remains open. The `timely-property-recovery` scope at revision 2 also remains open before substantive independent acceptance. Read `resume-evidence.json`: an actual killed uncommitted writer preserved the same revision 1/document hash; resumed work saved revision 2 with additional dependencies. The report correctly distinguishes this persistence demonstration from a reconstructed legal-research chronology.

### P1 — Seed could bind a newer inventory than the rows it imported: awaiting correction

`seed` read `core.sections(code)` and constructed its items before hashing the complete register for its import receipt. A concurrent addition in a new unit between those operations caused the receipt to bind the newer file even though the items and selectors came from the older file. The newer unit was outside every old selector, so subsequent assessment found no register/import discrepancy.

Independent deterministic reproduction patched `core.sections` to read A, then write A plus B in a new unit before returning A. Result: seeded items `[A]`, live register `[A,B]`, import evidence valid, and no register/import mismatch in assessment. The scope remained open for unrelated initial investigation, but its supposedly complete register accounting had lost the change that should require reconciliation.

Requested fix: read/hash/parse exactly the same bytes when constructing the seed. If the register later changes, the stored receipt must retain the old byte hash so assessment exposes the change. Apply the same exact-byte principle to the completed-research verification import, rather than parsing one read and hashing a later read. Final implementation acceptance remains pending this recheck and the final demonstration review.

## Seed race correction recheck

Parent changed seed to read/hash/parse one byte snapshot of each register file and changed completed-research verification parsing to use `evidence_bytes(ref)`. Independently injected a registry addition immediately after seed read the original bytes: seeded items remained A, live registry became A/B, and assessment now reported `changed evidence: jurisdictions/T/sections.jsonl`. The old snapshot is preserved and the change cannot silently disappear. All previously reported implementation findings are now corrected. The 21-test suite still passes at this checkpoint; additional final regressions and substantive-demo acceptance remain to bind.

## Final code and integration recheck checkpoint

The latest 25 coverage tests pass, including the added seed-read race, historical-version change, completed-research link retention/change and broader-open-scope regressions. The corrected implementation has no outstanding defect from this independent challenge. The earlier simultaneous-writer test remains applicable; no subsequent concurrency mechanism change invalidated its result.

Read the separate fresh legal review. It documents a consequential omitted-source defect (CIV 1965/CCP 1174), corrected research and independent recheck, with 25 selected and five additional retained captures. This reviewer does not substitute the code review for that substantive judgment. The actual tracker at fresh revision 4 had 31 items and zero review records: exactly 33 missing-review blockers remained (31 items, boundary and scope), while other consistency checks passed. That is evidence the tracker did not grant closure from authored conclusions alone. Final reviewed-revision observation and code hash binding follow when saved.

## Implementation acceptance binding

**Implementation accepted after correction** for the reviewed coverage storage, validation, integration and command behavior. No reported implementation defect remains open. This acceptance does not certify the later tracker review records or whole-goal completion; final fresh-scope closure and historical-preservation verification remain the parent’s final integration step.

Accepted implementation byte hashes:

- `coverage.py`: `568afc40ea108bdd9df772776e1dc02e0c980dacf33301a3ef6fc6e6d7d1ac9c`.
- `__main__.py`: `9425060699b235ead55f6eb28f02875c165e2f4cd2fe553b031d0824b3eb6060`.
- `check.py`: `913017403d0df8bc9b4720d67052d0a2175359ff1b812e8954542073b5c7bdd9`.
- `tests/test_coverage.py`: `997ffff562fa033085c370f5e5330f23fefda2c3d4387e13086540220f020490`.

## Final independent acceptance — October 1, 2026

**Accepted after corrections.** This final section supersedes the earlier pending integration checkpoints. Rechecked the final seed additions for empty declared units, pending source families and retrieval gaps, and the final malformed-record validation. These preserve unresolved work rather than losing it during import. Independently ran all 29 coverage tests successfully. Parent separately reports the complete suite passed: 188 tests in 12.37 seconds, exit 0. The earlier independent simultaneous-writer and seed-race reproductions remain applicable. No material implementation finding from this review remains unresolved.

Read the separate substantive review and its final TRACKER_REVIEW mapping acceptance. Loaded actual fresh scope revision 6, recomputed assessment and checked that every one of its 33 review target hashes appears in that exact independent review report. There are 31 items (30 source records and one operating question), 33 reviews (all items, boundary and scope), and zero unresolved checks. Closure is computed true for this bounded storage-fee research scope. Review evidence is a distinct agent's actual accepted report, not an authored conclusion or fabricated review receipt. This implementation review does not independently substitute for that separate legal analysis or certify future law, new facts or whole-jurisdiction coverage.

Loaded broad California revision 4: 166 source records, 78 open research questions (71 prepared questions plus seven discovery questions), and nine retained Goal 3 accepted-report links. Assessment remains open with 1,101 unresolved checks. Aggregate jurisdiction coverage remains false even though the narrower fresh scope is complete. Imported historical legal reports do not silently close broader research.

Re-read the actual process-interruption receipt and loaded historical fresh revisions 1 and 2. Their document hashes exactly match the preserved-before/after and resumed hashes in that receipt. Full revision-chain checks pass on both live scopes. This verifies retained history alongside the previously exercised killed-writer rollback; it does not invent a research chronology.

Final accepted code and evidence SHA-256 bindings:

- `coverage.py`: `9f6cbcc0b8fd57a36025da4e29cb8098631c9dcfb8cfbbf0900a3be1c9d6bba1`.
- `__main__.py`: `9425060699b235ead55f6eb28f02875c165e2f4cd2fe553b031d0824b3eb6060`.
- `check.py`: `913017403d0df8bc9b4720d67052d0a2175359ff1b812e8954542073b5c7bdd9`.
- `tests/test_coverage.py`: `686b13377e4b1f160d9be5cc06ce4e9879e8b9660323705579501370b8e298d2`.
- Fresh scope revision 6 canonical document: `65bd881dd723384807cee6aedd3206bcdce3141901324055a489066fbe3eafd4`.
- Broad scope revision 4 canonical document: `d0d61a719879bad7375c97e2c66fc3278c34f389ece26c87e2cf9abbbaa5a380`.
- `fresh_research/TRACKER_REVIEW.md`: `1a13207b90c774299ee9e3b42c2719a7232244ee3c667a0e1017b45807e999e4`.
- `resume-evidence.json`: `9bbe8ee5a675f82dcec96295af892b51887272a5f29ea93f64cc860d48001872`.

Acceptance is limited to the reviewed implementation and demonstrated integration. Software verifies identity, completeness relative to declared boundaries, history and required review bindings; it cannot authenticate human independence or establish legal sufficiency merely from a pass field. Independent source enumeration and substantive challenge remain necessary work. No author code or primary-source files were edited by this reviewer.
