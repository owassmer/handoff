# Independent implementation review: Goal 2

October 1, 2026. Separate reviewer, using the code-review skill. Read current `jev_results.py`, `jev.py`, `triage.py`, `batch.py`, `registercheck.py`, `legacy_import.py`, `export.py`, the legacy execution guard, new tests, and relevant installed SDK models/serialization. No implementation files or historical artifacts were modified; reproductions used temporary roots and no network calls. The coordinator was making corrections during review; dispositions below distinguish rechecked fixes from pending work.

**Disposition: the principal current-use bypasses are closed. Both consequential findings below were corrected and independently rechecked; no unresolved material finding remains in this implementation scope. This is an implementation review, not the final completion audit.**

## Findings

### R1 — Calibration destroyed its previous report and incompletely attributed selected responses — corrected and rechecked

`pipeline/triage.py:calibrate_main` writes `calibration.json` with `core.write_json`, then writes it again when own-reviewer statistics exist. Neither write preserves the prior report. The new cached-only usage outcomes name section ID and request hash but omit the originating response timestamp, response identity/hash and selected result values. A request hash identifies the question/input, not which response to a repeated inference produced a historical measurement.

Executed reproduction: in a temporary jurisdiction, created a legitimate compatible cached answer and an existing calibration report containing a unique historical marker; ran the real `calibrate_main(..., cached_only=True)` with one isolated positive. The old report was replaced and **zero copies of its exact bytes** remained anywhere in the temporary root. The new report contained only jurisdiction/time, usage/outcomes, counts, evaluation version/context policy and aggregate evaluations. Its cache-hit outcome had section ID, status, cache key and reason. No origin timestamp or response attribution was recorded.

This does not permit stale answers to route today. It fails the distinct requirement to preserve and accurately attribute historical measurements. Later recovery or re-inference can validly replace the answer for an identical request, so joining an old report solely to today's cache key is insufficient.

The coordinator now preserves exact previous calibration bytes under `calibration-history` before atomic replacement. Reports include `selected_answers` with actual values, originating timestamp, request key, response hash and origin configuration. Envelopes require and verify the response hash.

Independent recheck used two different valid responses to the same request in a temporary root. Two cached-only calibrations preserved both the original historical marker report and the complete first measured report byte-for-byte. The selected records retained the same request key, different response hashes, and their respective Noul values of 0 and 0.5. This directly proves the distinction that the original implementation lacked. No model call occurred. R1 is closed.

### R2 — Score response validation disagreed with the native schema — corrected and rechecked

The initially inspected `jev_results.validate` required 2–10 Score levels but ignored `legend`. The main preparation path permits additional questions alongside required role/chain-duty questions, so this branch was reachable. Independent `.venv` reproduction showed:

- Installed SDK `Score` accepts one and eleven criteria; the new validator rejected both.
- A two-level answer with no legend was accepted.
- A two-level answer with reversed legend text was accepted.

The coordinator removed the unsupported count bound and now checks a nonempty ordered rubric and exact legend correspondence. Re-read the corrected branch and new tests. Missing/mismatched legend is rejected; one, three and eleven levels are exercised. The full suite passed after these changes. No remaining R2 blocker.

## Consumer and identity assessment

| Area | Finding |
|---|---|
| Request identity | Endpoint, requested alias, expected returned build, registry/question versions, full question specs, prepared state and assembly format are bound. Canonical object order does not erase list order. Registry version changes deliberately invalidate rather than relabel old origin. |
| SDK configuration | Inspected installed native Noul/Choice/Score constructors and serializer. The internal `primitive` maps to the native `type`; instructions and criteria remain structured; optional None fields are omitted on the wire. The mocked live lifecycle test inspects native serialized role/chain-duty questions and supplied state. Shared question reuse now keys the entire built spec. No source-only or profile-fragment key remains in that cache. |
| Live and disk answers | Shared validation checks exact build, answer IDs, primitive type, required routing values, probabilities, confidence and finite/ranged values. Envelope identity is checked against both current request and stored request. Origin timestamps and reported costs are now validated. Invalid entries remain unavailable, not negative answers. |
| Compatible reuse | The real client lifecycle, with only provider I/O replaced, writes a valid envelope; subsequent ordinary and cached-only reads preserve origin and perform no second inference. Credentials are not loaded for a fully reusable run. |
| Embedded/in-memory bypass | `reroute` deliberately ignores supplied answer projections and reloads request-bound cache evidence. `current_rows` recomputes current routing. Old embedded values cannot establish compatibility; displaced values retain original fields in history. |
| Triage failure/limit behavior | Failed refresh drops stale current projection while preserving review decision/history. Cached-only outcomes are surfaced. Limited triage explicitly identifies deferred work and returns incomplete. Actual source length is checked in preparation, in addition to stored length. |
| Calibration | Fresh answers come through validated client/cache paths. Missing source inputs are retained in the requested population; unanswered negatives now fail the completeness check. Current own-label routing is explicitly described as current, not the historical route used at review. R1’s selected-response attribution and snapshot preservation are now rechecked. |
| Batching | `batch.plan` uses recomputed current rows for all tier/score ordering. `batch.main` preserves original stored rows while assigning batch membership; this is not a score-reuse bypass because score consumers reload current evidence. Historical rows should not be described as refreshed merely because a batch was created. |
| Register/J4 check | Embedded values on every route, including stated/review-queue, are compared with current validated cache projections. Set-aside routing uses validated evidence. This closes the original substring/file-existence acceptance path for actual Jev records. The checker does not independently certify every saved tier/reason field; batching recalculates those before using them. |
| Import/export | Import retains original Jev/route metadata under historical legacy fields, leaves active Jev empty, and recomputes current routing without unverified scores. Export keeps historical model/version/key attribution and marks scores historical-only; main gold construction does not use those scores as predictions. |
| Standalone register | New legacy inference is explicitly blocked with a direction to the main pipeline. Old read/reproduction tooling remains historical. No claim that every standalone historical script now implements current validation is justified or needed. |
| Persistence | Cache writes use temporary files and atomic replacement. Rejected prior cache bytes and previous result snapshots are retained; result history distinguishes observation from origin. Failed attempts preserve response/outcome evidence. Calibration now also preserves prior reports and selected-response attribution. |

## Executed checks and limits

Ran the full suite independently using the installed SDK environment:

```sh
cd research/legal-engine
.venv/bin/python -m pytest pipeline/tests -q
```

**155 passed in 13.51s** after the final R1 correction. An earlier installed-environment run passed 148 tests before the final history/JSON checks were added. An earlier system-Python run during concurrent additions produced 124 passed / 10 skipped; the installed-environment run covers the SDK-dependent tests and supersedes that limited run. One initial invocation used an incorrect importer-test filename and ran no tests; it is not counted as validation.

Inspected tests for compatible live-to-cache reuse, exact origin retention, corrupt-cache recovery and byte preservation, wrong build/shape/cost/transport rejection, budget refusal, atomic replacement failure, legacy rejection, prepared-input changes, embedded override rejection, failed rerun and limited triage. These use actual preparation, hashing, cache reads/writes and consumers with a mocked provider, rather than making model calls.

Additional temporary reproduction confirmed a stale derived tier/reason with no embedded Jev is not independently rejected by the register checker. This is recorded as the checker’s scope limit, not a new current-reuse defect: current batch and own-label score consumers recompute from validated evidence, and the field does not become an answer. Source/contract compatibility is not legal correctness, current-law verification, or model calibration.

Final closeout still needs preserved-artifact/current-corpus evidence and a requirement-by-requirement acceptance reconciliation. No historical experiment result should be rewritten to satisfy the new cache format.

## Final evidence and delta recheck

Independently rechecked the subsequent serialization, duplicate-ID, marker-removal and limit-accounting changes. The redacted serialized cache envelope is validated against the original request before it can replace a file or become an answer. The old substring check no longer competes with exact-build validation. Triage rejects duplicate or unequal ID populations. Limited calibration retains original positive/negative population sizes, records deferred inputs separately, and returns incomplete when any were deferred. Inspected the added batching, missing-source, legacy-guard and limit regressions. No new material finding.

Independently recomputed **all 7,962 hashes** in `historical-baseline.json`: zero changed or missing files. Every implementation hash in `VERIFICATION.json` matches the final inspected bytes. Independently repeated the corpus inspection: all **3,582** legacy cache envelopes lack complete request identity and report the historical pinned build; 3,581 pass typed-answer shape checks, while one has the recorded choice/distribution inconsistency. None is thereby admitted as compatible current evidence, and all original files remain unchanged.

The current corpus independently reproduces the recorded counts: CA has 166 sections/rows, 157 cache misses and nine source-length preparation errors; CA-HB has 12 sections/rows and 12 misses; US has zero sections. No compatible current answers exist in this corpus. Successful reuse is therefore demonstrated by the isolated lifecycle fixtures, not overstated as an observed migration of real current answers.

Final independent installed-environment suite: **159 passed in 12.76s**. This independently corroborates `TESTS.txt` (159 passed in 11.83s) and the final verification evidence. Both review findings remain closed; no material implementation or preservation blocker remains. The coordinator can complete the final acceptance/status reconciliation using this evidence, without extending the claim to legal correctness, task accuracy, or production deployment.
