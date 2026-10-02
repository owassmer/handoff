# Independent initial implementation review — Goal 5

Reviewed `contracts.json`, `tasks.py`, `run.py`, `test_focused_tasks.py`, and the reused SDK/response-validation helpers. No inference run. No implementation file edited. **Not ready for consequential evaluation inference until the request-contract and evidence-binding defects below are repaired and independently rechecked.**

## Material findings

### P1: Truth contracts are not sent or bound

`prepare()` builds each question from only `primitive` and `instructions` (plus optional criteria). All six `truth_boundary` definitions are omitted from both the native request and request identity. The newly resolved distinctions therefore govern expected labels but not the instructions actually judged. In particular, incorporation as definition, excusing versus satisfying a duty, necessarily implied support, and quoted argument versus adopted rule are not communicated by the generic prompts.

Independent deterministic reproduction changed a task's truth boundary to the opposite YES definition while keeping its version unchanged: both request hash and expected wire object remained identical. The reproduction mocked only SDK construction; this omission occurs before SDK behavior.

Required correction: deliberately compile the task's tested truth convention into native instructions/criteria, and bind the full relevant contract/configuration content to the preparation identity or separately frozen manifest. A manual version string alone does not detect accidental edits under the same version. Verify the serialized request contains the selected convention without leaking expected labels. Test a truth-boundary change produces a meaningful request/configuration change.

### P1: Source hash and selected text can come from different reads

`prepare()` calls `digest(path)` then `path.read_text()`. A replacement between them validates old bytes but supplies new text. Independent reproduction replaced AAAA with BBBB after digest returned the old hash: preparation accepted BBBB with the AAAA source hash. This contradicts the exact-source-selection guarantee.

Read bytes once, hash those same bytes and decode/select from that snapshot using a declared encoding/newline convention. Retain enough source selection detail to revalidate the preparation later. The prepared request currently retains only an opaque `evidence_hash`, not the source references themselves; a separately frozen input-case manifest can retain them, but execution artifacts must bind that manifest unambiguously.

### P1: Selected term occurrence is not identifiable in semantic payload

Both same-sense and candidate-meaning contracts refer to one selected occurrence, but state contains only `term` plus passages; the contract explicitly keeps occurrence identity outside the payload. A passage may use the same word in different senses, including comparing or rejecting definitions. The model cannot identify which occurrence was selected from bookkeeping it never receives. Preparation also does not verify that the term occurs in the supplied passage.

Either require and validate that the supplied use passage unambiguously contains one selected occurrence, or provide an exact selected occurrence locator/marked representation meaningful to the model while preserving separately validated source text. Include a repeated-term/mixed-sense regression. Do not resolve this merely by storing another invisible offset.

### P2: Charged invalid responses disappear from cost totals

Runner stores raw response, invokes `diagnostic()` and only then reads/adds usage cost. A response with a wrong build, missing answer, invalid probability or other semantic-validation failure may still report a real charge. The exception path retains raw evidence but summary `reported_cost` omits that charge. Record trustworthy reported usage independently of semantic validity, retain invalid/missing usage distinctly and stop further dispatch when accounting is uncertain.

The $0.01 reservation is an estimate, not an enforced maximum: a single request can exceed the nominal cap before the post-response stop. Describe that property accurately or use a justified pre-dispatch upper bound/provider limit. Do not claim a hard spend ceiling from this check alone.

## Serialization and execution verification gaps

The request hook is a good implementation direction: it inspects the native transport body before sending and raises on unexpected body or repeated attempt. However, the three tests never execute this path. Before live inference, test the actual pinned SDK against a local/mock transport with a fake credential: accepted payload, SDK mutation rejected before network dispatch, zero/multiple attempts, Choice alternative serialization, invalid raw response with nonzero usage, and failure followed by retained not-sent rows. Confirm that exactly one verified transport attempt is required for an answered record, not merely that every hook invocation would be checked.

The stored `transport.body` is parsed JSON, not the exact serialized request bytes. Semantic JSON equality can be a defensible verification standard, but it must be named as such; if the promised artifact is the actual serialized request, retain the body bytes or UTF-8 body string/hash alongside parsed JSON, excluding credentials. Record/validate endpoint URL and method against the frozen identity as well as body content. Pin and record SDK/serializer versions in the frozen configuration. Verify `expected_wire` itself corresponds to the hashed identity before dispatch rather than treating an arbitrary supplied companion object as authority.

`requests.json` and incremental results are useful durable evidence. There is not yet a freeze/independent-label manifest enforcement path in these files. That is a required held-out gate, not an assertion that the runner must itself discover legal context. Connect execution to frozen case IDs, source selections, contract bytes, independent label hash, split designation and model/configuration before held-out testing. Reject duplicate case IDs to preserve unambiguous joins.

## Contract recheck

The new truth boundaries substantially resolve the initial semantic ambiguities: passage-level definition recognition, conditional exception relations separate from actual applicability, explicit temporal modifications, real NONE versus missing context, and atomic direct/necessary support are stated. They are acceptable development conventions once actually communicated and tested. Definition incorporation may yield YES before extracting its meaning, but the overall required work still needs completed retrieval and extraction; downstream instructions correctly prohibit treating this as a complete extracted definition.

Choice alternatives must be independently checked for overlap; exact-string duplicate rejection alone cannot establish semantic exclusivity. Disclosing and validating this agent preparation responsibility is appropriate. Test unknown/none cases and selected occurrence identity before treating a Choice distribution as usable evidence.

## Verification performed

- Read full implementation and shared response validator.
- Independently reproduced omitted truth-boundary binding and source-read race with temporary fixtures, without inference.
- Ran the three focused tests with the environment's `python3`: one passed and two failed because `typesafe_sdk` was not installed in that interpreter. This is an environment mismatch, not evidence that SDK behavior is broken. Requested the pinned interpreter used by the author for three passing tests; rerun with that environment when supplied.

No capability is accepted from this initial review. Repair and recheck the material findings, demonstrate transport behavior without paid inference, then proceed with independently labeled development cases. Broader evaluation tooling and held-out freeze/label gates still require their own final review.

## Immediate correction recheck and freeze review

Author identified the pinned interpreter: `.venv/bin/python`. All three focused tests pass there. Rechecked the new single-byte-snapshot source validation, contract-content hash in identity, and explicit use-expression selection validation. The first two repair the demonstrated source race and undetected contract-content changes. Concise native criteria communicating material truth distinctions are sufficient; the whole preparation policy need not be copied into instructions. Native communication and transport tests remain to recheck after author changes.

The new use expression makes occurrence selection visible, but a unique phrase may itself contain two occurrences of the term in different senses. Current validation checks that the phrase occurs once and contains the term, not that it selects one occurrence within the phrase. Require one term occurrence in the phrase or an explicit unambiguous occurrence locator and add a mixed-sense test.

`freeze.py` now preserves cases, review, contracts, requests and implementation hashes. It also reproduces the read/hash race at another boundary: cases/contracts are parsed first and later reread by `digest` for comparison with reviewed inputs. Parse and hash one snapshot per input. Ensure the copied frozen artifacts correspond to the exact accepted bytes or explicitly bind the deterministic transformed content. Otherwise review can validate newer file bytes while preparation used older content.

Freeze verifies label coverage and reasons, but reviewer identity/exposure disclosure is only mentioned in a note and execution accepts a requests file without verifying the freeze manifest. Prior to held-out execution, enforce the defined review metadata and bind execution to the frozen manifest/configuration/implementation. This cannot authenticate real independence, but it can reject absent disclosures and detect changed prepared artifacts. Source/label/contract freezing should not depend on an operator remembering a separate unverified file.

## Second correction recheck

All six focused tests pass independently under `.venv/bin/python`. Rechecked: selected use expression now contains the term exactly once; four native Noul criteria communicate the material truth conventions; source and freeze inputs are hashed and parsed from single captured byte snapshots; freeze copies the exact case/review/contract bytes; valid reported usage is counted before semantic validation. The actual SDK mock test demonstrates native body capture and charged-invalid stop behavior; a second test demonstrates body mismatch prevents dispatch. These repair the corresponding initial findings.

**Remaining material gate defect:** `read_frozen` verifies only whichever manifest members happen to be supplied. A manifest containing just `requests.json` and an empty implementation object is accepted; the new test explicitly demonstrates this acceptance. Thus CLI dispatch does not actually require the claimed case, independent-review, contract or implementation bindings. Enforce exact mandatory file and implementation membership (and reject missing members), validate required reviewer identity/exposure metadata, and add successful real freeze→read_frozen coverage as well as missing-member failures. The current freeze test exercises a deliberately invalid review, then substitutes a manually constructed minimal bundle; it does not test a successful complete freeze.

The request hook still retains parsed JSON rather than raw serialized content. Retain actual body bytes/text and hash, or accurately narrow the artifact claim to semantic JSON verification. The prior recommendation to assert exactly one verified attempt before marking an answer and record endpoint/method remains appropriate. These are bounded execution-evidence requirements; none requires adding expected labels to a semantic request or expanding into Goal 6.

Initial semantic/source defects are corrected. Final execution-gate acceptance awaits the missing-member repair and final transport evidence recheck; no inference or capability acceptance has occurred.

## Final pre-inference implementation acceptance

**Accepted for independently labeled development evaluation after corrections.** This section supersedes earlier pending repair checkpoints. All eight focused tests pass independently using `.venv/bin/python`; parent reports the complete suite passed with 196 tests. No live inference was performed by this reviewer, and this reviewer has not read preparation authors' labels or model responses.

Verified exact mandatory bundle and implementation membership, same-snapshot input freezing and exact source-byte validation, reviewer identity/exposure requirements, successful complete freeze roundtrip, frozen-input mutation rejection, explicit unique occurrence selection, concise native truth criteria, and actual SDK mock transport behavior. Transport records now retain serialized body text and SHA-256 alongside parsed JSON. Charged invalid responses remain charged in the summary and stop further dispatch. These address the material defects reported above.

Read the new evaluator. It rejects duplicate/missing case joins, recomputes diagnostic answers from raw responses, checks answered-request identity and single matching transport body, retains execution failures in the case ledger, and reports per-task and per-family counts separately. Source-cluster counts and any-disagreement counts are reported. The binomial upper bound is correctly described as a conditional independent-case reference calculation for a purposive clustered challenge set, not a deployment reliability guarantee or authorization threshold.

Minor evidence-hardening recommendations remain nonblocking for this controlled development run: validate retained body text/hash against parsed body during evaluation, record HTTP method with endpoint, record the pinned SDK version in final run evidence, and assert exactly one verified transport attempt in the runner as well as the evaluator. The verified SDK path and evaluator already establish the single captured body for evaluated answers; these recommendations do not reopen a demonstrated false-result defect. The reservation remains an estimate rather than an enforced provider spending limit and must be described accordingly.

Acceptance is limited to this prepared-task execution/evaluation implementation. Independent source preparation and labels, actual development results, configuration selection, fresh held-out coverage, all material finding investigations and any completing fallback method still require demonstrated review. No legal judgment capability is accepted as dependable solely from these unit and mock-transport tests.

Accepted file hashes:

- `contracts.json`: `2de55d706a2e91904fa67deaf26ad4889470038119cb67828f38d4ea6de8a208`.
- `tasks.py`: `3ae707c717e539078984c62071af1db254d390b865d7d7f9abbd38726ceec133`.
- `run.py`: `62e11b83b1ea96133962b7ae8a32084da72a9fc129b55a67fc1a9ce9c02ac3cb`.
- `freeze.py`: `5ecbd2784b79095c79029d2d5b57a5afe690b024628b5de88282e7188c0d6260`.
- `evaluate.py`: `a7ba610a888adfcdcb43a1f7dc2b171817dbdfe24dca1e600f12ecb760438ae4`.
- `test_focused_tasks.py`: `b6d1aaff22e54bacdd4edc18a122ffcc873ad33456b813a1eef005d4fb8d6d88`.

## Initial batching implementation challenge

Reviewed new `batching.py` and runner's multi-answer diagnostics mapping. Grouping only identical canonical semantic state with matching endpoint/model/build is a sound controlled comparison; no question consumes another question's result. This is JSON-content identity, not literally byte identity of original source serialization. Existing eight focused tests pass, but none exercises batching.

**Material comparison defect:** `compare()` validates batched raw answers but trusts the stored separate `diagnostic` field and does not verify either transport against frozen request content. It also silently overwrites duplicate separate-result/label IDs. Independent synthetic reproduction supplied separate raw answers of0.8 (YES) with stale stored diagnostic NO, batched raw0.2 (NO), and no transport records; compare emitted separate NO/batched NO for both questions. Thus the result can manufacture apparent matched agreement from inconsistent or absent evidence. No inference was used for the reproducer.

Required correction: pass the frozen separate requests into comparison, recompute separate diagnostics from validated raw, verify request identities and single serialized transport/body evidence on both sides using the same checks as the evaluator, and reject duplicate IDs in batches, separate requests/results and labels. Preserve failed/not-sent rows with their expected label and separate execution status, rather than presenting missing execution as a semantic comparison. Add reproducer-based tests before relying on the matched batching experiment. Source label blindness is independent of these code checks.

The prior single-question runner acceptance does not grant acceptance of this newly added comparison path.

## Batching correction recheck

Inspected the updated comparison: both sides now recompute diagnostics from validated raw, compare exact expected transport JSON, verify body text/hash, and reject duplicate result/label/batch IDs. Independently reran the substantive stale-diagnostic reproducer with correct transport evidence: separate raw0.8 now correctly appears as YES despite stale stored NO, while batched0.2 remains NO. Removing transport now raises `Comparison transport mismatch`. The previously demonstrated false-agreement defect is corrected. Targeted permanent regressions remain appropriate before final integration acceptance. Failed-batch rows still contain less comparison context than answered rows; preserve source expected labels and separate execution status in final reporting.

## Matched batching experiment acceptance

**Accepted for the bounded matched development experiment after correction.** All nine focused tests pass independently, including the new regression for stale separate diagnostics, duplicate records and missing transport. Re-read the CLI: it loads the verified parent freeze, requires the separate run's executed requests to match, creates an exclusive pre-inference plan with exact batch requests and module hash, executes through the verified runner and compares against independently prepared parent labels. Same-state grouping supplies no prior answers to another question. This supports the planned eighteen judgments in nine shared-state calls without a whole-process or routine-use reliability claim.

This does not turn batching agreement into semantic correctness: the original baseline disagreements and independently investigated relations remain attached to their cases. Any cross-question influence or changed answer must be investigated. The source-preparation refinements are separate new versions, not inputs silently substituted into the original matched experiment.

Current batching implementation SHA-256: `d1f16577d2cbb88d97fa2c52cc0d32a50ec0161122b0a36c7143b0cf742db77d`.
