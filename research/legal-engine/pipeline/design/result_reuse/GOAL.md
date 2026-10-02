# Goal 2 — result reuse

October 1, 2026. Status: complete. Purpose: previous semantic judgments may inform current research only when they answer the current prepared question on the current evidence with the required model build. Rejection is unavailable evidence, never a semantic NO. This goal changes result handling, not legal conclusions, thresholds, or the agent/Jev/code division of work.

## Coverage boundary

In scope: main-client cached-only reads, live-path cache hits and misses, live response validation/writes, in-memory prepared-question reuse, triage embedded-result skip/fallback, calibration, batch scores/tiers, register validation, persisted result/exchange/history attribution, and legacy-cache treatment. Trace historical import/export and standalone register execution explicitly so neither can silently assert that old values are current. Include native supported question configurations and actual prepared context in identity. Preserve old experiments and saved legal sources.

Historical experiment bundles are immutable evidence, not caches feeding the main client. Their existing exact-request validators remain accounted dependencies; changing their recorded results is excluded. Source-download caches and legal-rule applicability are separate mechanisms, excluded because they do not reuse Jev judgments. Production runtime integration, new task calibration and legal mapping remain later goals.

## Observable acceptance criteria

1. Inventory every result producer/reader and identify its trust boundary; reconcile each to a change, demonstrated safe path, or justified historical-only exclusion.
2. Identity binds endpoint, requested model, pinned returned build, active question content/primitive/criteria and material list ordering (JSON object order is immaterial), question/registry versions, and complete prepared state. Different effective inputs cannot hit the same reusable entry. Current attribution never replaces unknown/old origin metadata.
3. Live and cached responses pass the same strict build, answer-ID and typed-value checks, including finite/ranged probabilities and required routing values. Malformed JSON/envelopes and unsupported shapes cannot be returned as valid answers.
4. Valid compatible entries reuse without an inference call. Legacy entries require demonstrable identity before adoption; incomplete evidence yields an explicit rejection and preserved historical record. Changing questions/build/state invalidates reuse.
5. Existing embedded triage results cannot bypass validation. Failed/limited refresh cannot fall back to stale values or count them as answered. Current batch/validation/output paths do not trust stale scores. Historical import/export retains origin and clearly marks historical values.
6. Persistence retains the raw response and origin request, and does not destroy prior experiment/history records. Interrupted/corrupt writes are not valid answers. Failed requests, invalid cache entries and unanswered inputs are separately countable.
7. Demonstrate the behavior with adversarial cases and actual current corpus/cache inspection; independently review consequential implementation and correct findings. Tests alone do not establish that all consumers were covered.

## Initial findings

The old key omits endpoint and pinned build; cache reads validate nothing. Live responses check the build only. Embedded triage results bypass the cache and survive failed reruns; batch uses embedded scores. Results are projected under the currently supplied registry version even when raw origin is unknown. The current workspace has no main-client jurisdiction caches and no embedded Jev values in CA/CA-HB, but the historical register contains 3,582 cache files and its exchange log. These existing historical files must remain intact.

## To-do

- [x] Read current plan, Goal 1 evidence, registry, client and initial consumers.
- [x] Complete independent path/acceptance review (`INDEPENDENT_INITIAL.md`).
- [x] Implement full identity, response validation, origin records and explicit legacy behavior.
- [x] Close embedded-result and downstream reuse bypasses.
- [x] Exercise valid reuse, invalidation, corruption, live failures, limits and historical preservation.
- [x] Independently review implementation; correct and recheck material findings.
- [x] Audit each acceptance criterion against final evidence and update PLAN.md.

## Implementation progress — October 1

Request-bound envelopes and shared response validation are implemented, with canonical object keys and material list ordering. Triage and batch recompute from validated current cache evidence; displaced embedded values retain their original fields in history. Register checks compare embedded records against current validated evidence, including stated/review-queue rows. Legacy import retains original judgments/routes under `legacy`, computes current routes without those unverified scores, and preserves reviewer decisions. Historical export marks scores historical; standalone legacy inference now directs new execution to the main client.

Nineteen new isolated-cache checks pass for compatible reuse, identity changes, malformed entries, embedded override rejection and register rejection. The combined suite found an old importer assertion requiring current routes to equal historical routes; that assertion has been corrected to require preservation of historical routes and absence of unverified active scores. Combined rerun and live-path/failure tests remain pending. No completion claim yet.

## Final acceptance

All seven criteria are reconciled in [COMPLETION.md](COMPLETION.md). The final SDK-enabled suite passes 159 tests with no skips. The independent reviewer re-ran the suite, verified all 7,962 protected hashes and implementation hashes, reproduced the corpus findings, and reported no remaining material finding. Two review findings were corrected and independently rechecked. Historical experiments remain unchanged. Provider availability and legal/model-quality conclusions are not implied by mechanical reuse verification.
