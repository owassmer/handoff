# Legal-reference contract and bounded use

**Later correction:** The founder rejected the preparation and question design underlying this completion claim. These results remain historical observations; they do not isolate intrinsic model limitations. Current corrective work is in [prepared_tasks](../prepared_tasks/README.md).

Status: Goal 1 completed within its declared boundary. The independent [final audit](FINAL_AUDIT.md) verified every acceptance criterion; closing status updates are recorded in [ACCEPTANCE.md](ACCEPTANCE.md).

## What the question promises

Detect whether the supplied English passage contains an explicit public legal pointer. Self, enclosing, subordinate, other-section, and named-authority pointers count. The agent identifies individual mentions, their relationships to a stable section anchor, exact targets, versions, and legal effect. One passage may contain several relationships. Presence remains one atomic YES/NO/INSUFFICIENT question.

The final candidate is `question.v1-dev4.json`; earlier versions remain intact. Known source-locator headings are not body references. An isolated identifier with unresolved role remains uncertain. A truncated expression counts when public legal meaning is already established; private meaning does not count; unclear meaning remains uncertain. Generic invocations of law and private agreements are outside this detector's public-pointer boundary but remain important research inputs.

## Development and corrections

The independently reviewed initial 48-case dev2 run agreed on 44. Its four failures were model errors: two missed self-pointers, an isolated citation treated as definite, and ambiguous chapter language treated as negative. The first new 48-case evaluation candidate exposed two contract gaps before any model execution. It was retired in full to development. Dev3 clarified headings and cutoffs; dev4 clarified private cutoffs. Four additional controls exercised those boundaries. No evaluation result was used to revise a question while retaining a held-out claim.

Independent code review also found that the original freeze helper joined reviews by case ID without binding exact reviewed bytes. The fix requires case-file and question-file hashes before assigning reviewed labels to requests. Two regression tests reject changed text or question wording with stale review. The original development freeze remains unchanged and its exact equality with reviewed inputs was independently verified after the fix.

| Run | Role | Cases | Answered | Agreement | Unanswered | Provider cost | Invocation elapsed |
|---|---|---:|---:|---:|---:|---:|---:|
| development-run | Original dev2 development | 48 | 48 | 44 | 0 | $0.001621872 | 4.8436 s |
| development-v4-run | Same original cases, revised contract | 48 | 48 | 43 | 0 | $0.001821456 | 4.2063 s |
| retired-v4-run | Retired candidate, development | 48 | 48 | 44 | 0 | $0.001821414 | 5.1724 s |
| extra-v4-run | Added development controls | 4 | 4 | 4 | 0 | $0.000149394 | 0.7023 s |
| fresh-evaluation-run | Separate frozen dev4 evaluation | 48 | 48 | 41 | 0 | $0.001870260 | 3.4807 s |

All listed runs used OpenRouter, pinned build `typesafe/jev-1.13-20260917`, with zero retries. Two dev4 runs overlapped in wall time; elapsed values are individual invocation measurements and cannot be summed as complete process duration. Costs are runner-reported provider usage; they exclude agent preparation, review, investigation, and correction. No comparative productivity claim follows.

Dev4 development retains nine model errors across 100 cases: d011/d012/d021 miss visible self-pointers; d029/e027 mistake isolated identifiers for established pointers; d034/e031 collapse uncertainty into NO; e011 incorrectly finds a pointer in a generic council-resolution mechanism; e014 misses a subordinate clause. The added controls pass. These are deliberately selected, related examples, not independent samples of legal text. Repeated runs on the original cases are not additional source diversity.

## Separate frozen evaluation

A fresh author who did not read development material prepared 48 cases after dev4 was fixed: 16 exact excerpts from six BPC/FIN/MVC source files and 32 authored contrasts. A separate reviewer independently labeled all 48 without author labels or model outputs; expectations agreed on all cases, and no material ambiguity remained. The review binds exact question/cases bytes. The frozen requests contain only focus text and task instructions, with no labels or reasons. No question change followed execution.

All 48 requests returned valid answers on the pinned build. Agreement was 41/48: 14/16 real-source excerpts and 27/32 authored cases. Source excerpts are related within six files; full-unit f001 overlaps f002/f003. The grouped results are in `fresh-evaluation-run/grouped.json`, and overlapping per-boundary counts plus every fresh case are reconciled in `COVERAGE.md`. These are selected task examples, not a population accuracy estimate.

The seven errors are f004 (missed enclosing “this part”), f008 (missed “this section”), f019 (source label treated as pointer), f022 (missed following paragraph), f024 (missed clause range), f029 (illegible potential pointer treated as absent), and f031 (isolated identifier treated as definite). All remain in the original totals. The three quoted-adversarial cases f046–f048 matched their labels; the failed development quote d021 remains a known counterexample, so general resistance is not established.

Across this goal's five invocations there were 196 requests and answers, zero retries, and $0.007284396 in reported provider usage. This includes repeated development cases and must not become a pooled accuracy score. None of the older pilots are included or rewritten.

## Demonstrated agent handling and limitations

`FOLLOW_UP.md` records actual source reading for self, enclosing, mixed and historical pointers, correct NO cases requiring further research, model misses, and unresolved context. Independent reviews preserve exact evidence and original model answers. The GOV 12955 missed clause was located in its saved target. The federal incorporation example identifies a historical version requirement without claiming that historical federal research is complete.

For authored damaged or ambiguous fixtures, no underlying recoverable source exists. The demonstrated outcome is retaining the missing context honestly, not inventing a successful recovery. This is deliberate coverage of uncertainty; production retrieval reliability is outside this goal.

`AGENT_GUIDE.md` requires full passage review for every answer. The detector is not reliable enough for unattended exclusion or research closure. Its optional advisory use has a concrete handling boundary, but this experiment has not shown that adding it saves effort or improves completed decisions. That comparison remains a separate goal. Same-model-family independent agents provided review; this is not independent human legal validation or confidence calibration.

## Evidence and reproducibility

`README.md` supplies freeze/run/evaluate commands. Frozen bundles preserve cases, questions, labels, reviews, request hashes and manifests. Run folders preserve requests, raw responses, counts, per-stratum results, cost and elapsed time. Preparation tests cover label separation, source identity, exact spans, missing results, immutable frozen labels, stale review rejection, and unresolved-review rejection. Old experiment files are checked against the 58-file `prior_artifact_hashes.json` baseline.

Main cache repair, broad integration, full legal dependency resolution, statewide coverage, legal applicability, and operator execution remain separate goals. No California rule set or production integration is activated by this experiment.
