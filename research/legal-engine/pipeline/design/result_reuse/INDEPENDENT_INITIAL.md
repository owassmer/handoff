# Independent initial review: Goal 2 result reuse

October 1, 2026. Read HANDOFF_CONTEXT.md, PLAN.md, the main Jev client, triage/calibration, routing, batching, register checks, legacy import/export, relevant main CLI/read/write paths, and the standalone register execution/routing chain. Applied the code-review skill. This reviewer did not implement changes. Offline reproductions used temporary files and patched in-memory dependencies; no network/model calls or historical artifact edits were made.

The required outcome is compatible result reuse with accurate original attribution and explicit rejection of malformed or incompatible evidence. Fixing the filename hash alone will not establish that outcome: embedded answers currently bypass lookup, and current consumers can route or prioritize from them.

## Confirmed consequential defects

1. **Cache identity omits the pinned build and endpoint; hits bypass response checks.** `pipeline/jev.py:156–171, 204–212` hashes model alias, built question specifications and state. It omits `pinned_build` and `base_url`. A cache hit simply parses JSON and projects fields. A file at the expected name need not prove its stored request identity or contain complete answers. Live responses check the exact build at lines 239–241, but cached responses do not.

   Offline reproduction: saved an old-build response with empty answers under the current key. `cached_answers()` returned it as a result. Changing pin, endpoint, and registry to `999` still hit the same file; the returned result asserted registry `999`. This simultaneously demonstrates incompatible reuse and fabricated current attribution.

2. **Live answer shape is not validated before acceptance.** `record_from_raw()` at lines 113–119 substitutes empty dictionaries and missing fields. The live path checks the build, then caches the raw response and returns a projected record. `route.py:70–88` defaults an absent DECIDES probability to zero and trusts numeric fields. I passed matching-build raw data with NO_DECISION, an incomplete probability map, and NaN confidence/duty through that projection: routing returned `triaged_no_decision`. Non-numeric values can instead crash routing. Neither outcome is a valid semantic result.

   Installed SDK `_schemas/models.py` documents required Choice type/choice/confidence/probabilities and Noul type/noul, with finite probability semantics in [0,1] and approximately unit-sum distributions. The permissive custom Raw response model bypasses these checks. Validation should also state a policy for choice/distribution inconsistency, including ties and rounding, rather than silently changing the answer.

3. **Embedded and in-memory records bypass any future cache fix.** `triage.py:49` falls back to the row's existing `jev`; line 70 excludes truthy embedded results from targets; lines 79–80 count them as answered after an unsuccessful rerun. `reroute()` accepts supplied answer dictionaries without binding them to current source/profile/question identity. Offline reproduction: an embedded record with `model='wrong'` and an unverified key produced `triaged_no_decision` when answers was empty. A changed passage or contract can therefore leave stale routing active even when no compatible lookup succeeds.

4. **Batching and register checks permit indirect reuse.** `batch.py:70–86` trusts saved tier, route reason and embedded scores without rerunning triage. Clearing only `jev` while retaining a Jev-derived tier can still preserve stale priority. `registercheck.py:102–128` checks only set-aside rows without hand reasons, accepts a model substring, checks cache-file existence rather than contents, and recomputes from the same unverified projection. Corrupt/wrong-request files and incompatible records on other routes can escape the gate. The J4 gate delegates to this checker.

5. **Historical attribution is too weak.** `record_from_raw()` assigns the current registry to cache-origin data. `jev.py:246–249` preserves only the latest result per section, while exchange entries omit the expected pin and origin registry. `triage.jev_subset()` further strips origin information. `own_label_recall()` calls current mutable routes the routing actually used, although rerouting can change those routes after review. New reuse must distinguish originating inference, current compatibility assessment, and current routing. An old record must not gain a new origin version or become an unqualified current answer merely because it can be parsed.

6. **Legacy import creates another current-consumer entry point.** `legacy_import.py:228–255` copies projected old Jev values into active `jev`, calculates tiers from them, and copies unverifiable old cache envelopes into the main cache directory. The destination is a separate imported tree, but it is explicitly usable by the main pipeline. Import must preserve original records and review decisions while making their current compatibility status explicit. An incomplete legacy envelope cannot be upgraded by attaching today's request or pin.

## Paths and scope

| Path | Required disposition |
|---|---|
| Main live `_run`, ordinary cache hit, `cached_answers` | Shared current-request identity and raw-answer validation; invalid entries produce explicit rejected/missing evidence, never an answer. |
| `reroute`, triage skip/fallback/missing accounting, calibrate answer maps | Validate the exact expected item before use, including caller-supplied dictionaries. Invalid old records must not count as current answers or conceal a failed refresh. |
| `batch.plan`, saved route/tier/score fields, main register/J4 checks | Prevent stale derived values from affecting current ordering or passing current validity checks when triage was not rerun first. Preserve reviewer decisions separately. |
| Main `jev/results.jsonl` | Currently a latest-per-section output, not a main answer-input path. Do not silently treat it as reusable input. New records need traceable original identity; preserve older observations in attributable evidence before replacement. |
| `legacy_import` | In scope because imported rows feed the main pipeline. Preserve originals; admit only provably compatible evidence, otherwise retain it as historical and unverified for current use. |
| `export-data`, exported gold labels | Explicit historical snapshot. Main calibration takes reviewer labels and source text from this export and does **not** reuse its embedded Jev scores. Keep historic model, registry and cache/request attribution; do not rewrite scores as current predictions. The snapshot manifest supplies provenance but does not certify current compatibility. |
| Main match/apply/diff/core readers | They preserve or inspect rows but do not independently infer from Jev scores. They must not erase the provenance needed by the real consumer checks. `core.triage()` itself is a raw JSONL loader today. |
| Standalone `register/jev_triage.py`, `tools/calibrate.py`, `tools/build_outputs.py`, old checker | Separate legacy execution/results/routing chain, not imported by the main CLI. It has the same weak cache checks and additional substring-only live build checks. Its outputs can enter through import/export, so those boundaries matter. Do not claim repository-wide reuse safety while this remains runnable unchanged. |
| Frozen design experiments and prepared-task runs | Historical observations, not main routing inputs. Preserve all bytes. Their runners share some main helpers, so existing regression behavior must remain compatible; no retrospective revalidation or relabeling of their old results. |

For standalone tooling, a clear historical-only boundary plus guarded main import is sufficient for a **main-pipeline** claim. If new legacy execution is still intended, it also needs shared validation. Otherwise a clear guard directing new execution to the main pipeline is preferable to silent redirection, which would change the legacy NYC task's scope. Historical read/reproduction tools may remain available with explicit historical attribution. Do not disable or rewrite old evidence merely to simplify checking.

## Acceptance criteria and adversarial cases

1. **One declared identity policy.** Bind the requested model alias, exact expected build, endpoint/provider context, complete actual question configuration and state, and relevant contract/assembly version. Inspect SDK serialization so native type, optional criteria, structured instructions, and defaults are represented consistently. Declare whether metadata-only version changes permit equivalent-request reuse; if they do, retain the original version instead of relabeling it. Unrelated registry entries need not invalidate an unchanged request.

2. **Validated result envelope.** Store enough original request identity, returned build, original timestamp, response and origin version to reproduce acceptance. Verify the envelope against its own identity and the current expected request, not merely its filename. Reject wrong/missing pin, wrong request, mismatched raw/projection, absent answers, unexpected IDs, wrong primitive/value, invalid probabilities/confidence, nonfinite values and boolean-as-number. Do not normalize malformed evidence into validity. Define error treatment for invalid JSON, non-object JSON and missing envelope fields.

3. **Positive compatible reuse proof.** A legitimate live result must be accepted, saved, then reused without a second model request through both ordinary and cached-only paths. Compatible embedded/in-memory reuse should also work under the chosen contract; no test suite consisting solely of rejection cases establishes useful caching. Reordering JSON object keys should not change identity; material list ordering and actual semantic changes should.

4. **Invalidation matrix.** Independently vary pin, endpoint, alias, instructions, criteria, primitive, question IDs, body text, heading, instrument identity/name, scope, chain description and exclusions. Also vary question/registry/assembly versions under the declared policy. Every changed effective request must miss/reject; an unchanged effective request should not acquire invented historical metadata.

5. **Consumer closure.** Exercise ordinary triage, `--rerun`, `--cached-only`, limited triage, calibration with pooled profiles, direct `reroute`, batching without prior triage, and register/J4 checks. Include stale results on review-queue and stated rows as well as set-aside rows. Test stale source metadata, changed source files, duplicate/conflicting section IDs, and missing source files. No invalid result may satisfy completion accounting or influence current Jev-derived route/tier/priority. Retain independent structural routing and reviewer decisions.

6. **Failure behavior and replacement.** Test corrupt files, unsuccessful live refresh, wrong-build live output, malformed live output, missing/invalid usage values, and interrupted/partial writes. Preserve raw failures and rejected legacy entries with explicit reasons. A failed attempt cannot silently fall back to incompatible old data. Cached-only mode must perform no network work and honestly report unavailable answers. Define cache replacement/write behavior so valid evidence is not destroyed by an unsuccessful update.

7. **Legacy provenance, not synthetic migration.** Either reject insufficiently attributable legacy entries, or reconstruct compatibility only from exact matching original exchange/request/response evidence with the limitations disclosed. Same filename, marker or embedded scores are not enough. Preserve original registry, returned model, origin time and source record reference. Test that the original legacy files and frozen experiments remain unchanged.

8. **Historical/current distinction.** Keep inference history, compatibility decisions and routing history distinguishable. If old routing-at-review attribution was never captured, report that absence; do not reconstruct it from today's route. Calibration reports must bind the actual request population/configuration used, and rejected/missing answers must remain visible rather than improving reported recall through silent removal.

9. **Independent closeout.** Review implementation and end-to-end fixtures against the path table, run meaningful focused and full existing tests, verify preserved-artifact hashes, and document any deliberately unsupported legacy execution path. Current workspaces without cached answers do not test the migration/rejection boundary; fixtures must include both valid and invalid real-shaped records. No external model call is necessary to prove these mechanical properties.

These are implementation and evidence-handling defects, not evidence about the model's legal capability. The work should remain focused on trustworthy reuse and attribution, without changing legal question semantics, routing policy thresholds, or earlier experiment conclusions.

## Initial code identities

SHA-256 at initial inspection, before implementation:

- `pipeline/jev.py`: `0cc29232d9acd18e1dfb7e2296c5cd1ec123cbdc91c0bf75ddc1dc1f7ad0a59b`
- `pipeline/triage.py`: `96a7249980bbfc51e8413ccd299dcdd4fe0b5074c09ad140c810dd78f33940b5`
- `pipeline/batch.py`: `9d61c38de085c72912b61642cebe9a2b410ee5518bff3b19627b17a378dc1392`
- `pipeline/registercheck.py`: `32f2a0e45e1723a675befa58b5ddc6c963820c97556f67d39a6971980aee91e7`
- `pipeline/legacy_import.py`: `2814b25c8d1b58782e541eba83bfc1820995535143ea7b8ab54577330bc1253d`
- `pipeline/export.py`: `8d16e5c85d0ebd46be0aaa93459862c95f00c561aee02a8786195484ab538374`
