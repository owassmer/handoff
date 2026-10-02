# Implementation and agent-follow-up review

2026-09-30. Targeted independent review using the code-review skill. No separately authored evaluation inputs, labels, or results were read. Only this report was written by the reviewer; fixes described below were made by the parent during review.

## Finding 1: stale independent labels could acquire new request identities — corrected

**P1, confirmed by execution.** In the initially reviewed `experiment.py:60–69`, `freeze()` joined review labels to current inputs solely through `case_id`, then assigned the current request hash to those old labels. Changing a passage or question while retaining IDs could silently freeze labels that were never independently established for the new task.

Temporary-directory reproduction: a review saying YES because the original passage was “This section applies.” successfully froze against the current text “The title of the novel.” The review even declared an older question version. Its stale YES received the current request hash. This demonstrated a provenance failure before model execution; request hashing after this point could not detect it.

The minimal correction is to make the reviewer record exact SHA-256 hashes of the cases and question files, and have `freeze()` verify both before assigning any labels. The parent implemented this in `experiment.py:62–65` using `review.reviewed_inputs`. Rechecked the implementation and the added parameterized regression covering changed case text and changed question instructions. Both fail safely without new review. Existing frozen development artifacts should remain unchanged; their historical input correspondence was separately checked in the failure review rather than retroactively claiming the new guard protected them.

## Finding 2: mixed-reference demonstration omitted a self-pointer — corrected

**P2, confirmed against saved CIV 1788.17.** `FOLLOW_UP.md:17` initially claimed completed target identification while omitting “this section” from the final sentence. The date-qualified incorporation also needed to distinguish federal targets from local self/enclosing pointers.

The parent added the self-pointer and now explicitly applies January 1, 2001 to the federal targets only. Rechecked the final paragraph against the saved source and previously reviewed d004 focus. The correction preserves all three relationship types and avoids attaching the federal historical qualification to the California section/title.

## Scope and checks

Read the complete `experiment.py`, its targeted tests, `AGENT_GUIDE.md`, and `FOLLOW_UP.md`. Read the shared runner's request/response validators and execution flow to understand interfaces. Reused the already inspected saved source contexts and development run, including the four adjudicated failures; did not inspect the new evaluation set. Git blame was unavailable because the workspace root is not a Git repository. Review targeted behavior and executable reproductions rather than style or linting.

Preparation permits only focus text into model state; labels, strata, source identities, and wrapper metadata remain outside it. Source hashes and exact Unicode-character spans are checked. Blank text, unattributed examples, duplicate IDs, and unresolved review flags are rejected. Request identity includes the question, focus, version, assembler version, and pinned build.

Evaluation checks frozen-file integrity, matches executed requests to the frozen requests, validates raw model answers/builds, and retains all frozen cases in the denominator even when results are missing. It derives actual answers from raw responses rather than trusting a redundant parsed field. No additional material identity or denominator defect was found in this scope. The evaluator does not itself certify independent review, chronological pre-run freezing, or semantic correctness; those remain evidence/procedure claims.

The guide correctly requires complete passage review regardless of Jev's answer, preserves generic-law and private-document investigation after NO, separates relation/target resolution from presence, and rejects confidence-based exclusion. The follow-up correctly distinguishes visible corrections in d012/d021 from unresolved context in d029/d034. It does not claim to have recovered missing source context for authored fixtures or to have completed legal applicability research. The described recovery remains a post-run worked demonstration with known failures, not an independently measured recovery rate or labor-saving result.

The pre-existing runner was read only as an integration dependency. A general audit of interrupted-call billing, provider behavior, durable crash recovery, and the main client is outside this focused change. The actual development run reported no transport/invalid/unanswered cases; this report does not extend that observation to failure paths or production.

## Verification and disposition

Ran the focused tests after the parent completed its correction:

```sh
cd research/legal-engine
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest pipeline/tests/test_reference_experiment.py -q -p no:cacheprovider
```

Result: **7 passed**. An earlier run overlapped the parent's code edit before fixture hashes were updated and yielded two fixture failures; the final run above resolves those failures. The review did not independently rerun the full suite or rehash all 58 historical artifacts; those are parent-reported checks for the final audit.

Both findings are corrected and rechecked. No unresolved material finding remains within this implementation/follow-up scope. Separate evaluation and the requirement-by-requirement completion audit remain necessary.

## Historical development input identity

Independently compared exact bytes, not only parsed JSON, after the correction. The current files are the same 48-case dataset and dev2 question reviewed before development execution. Both match their original frozen counterparts exactly:

| Reviewed file | Frozen counterpart | SHA-256 of both files |
| --- | --- | --- |
| `development.cases.json` | `development-frozen/cases.json` | `cbf72bcfa2b59b1b5c3115d951c582c40415026d62d8776b727d9ff84b859a45` |
| `question.v1-dev2.json` | `development-frozen/question.json` | `3e079a133d6de8fab5116d2fd7d4bebdd13ba0ec61f1d51e1b4b83be13b5951e` |

This supports the original development review's actual input correspondence despite the earlier missing automated guard. It does not retroactively add hash attestation to that review. No historical review or frozen file was changed.
