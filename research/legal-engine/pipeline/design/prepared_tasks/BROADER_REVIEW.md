# Independent review and broader evaluation

September 30, 2026. **Goal 1 is complete within its bounded research scope:** prepare coherent atomic questions and inputs, account for retained work, evaluate the statutory-pointer task, and audit other task prototypes. This does not establish production reliability, complete legal mapping, or benefit over the complete agent-plus-code process.

## Evidence

The independent historical coverage review verified all 27 selections against four complete source bodies: all 15 explicit statutory-pointer occurrences were represented, no exact candidate was duplicated, and three broad-law lead occurrences remained separately accounted. The declaration's governing clause was judged sufficient for its pointer-versus-subject question while preserving the adjacent definition dependency. The historical review was independent but not fully blind: the requested follow-up record exposed saved model values. That exposure is explicitly recorded in `coverage-independent-review.json`.

A separate author prepared 36 new source-backed selections from CCP 337/339, BPC 10176 and FIN 100001. The author read complete bodies and selected governing contexts before inference. The independent reviewer formed all expectations from the cases, unchanged question and source text before reading the author's design; author labels and model responses were withheld. Both independently arrived at 21 YES and 15 NO, with no material context or label ambiguities. Exact source hashes and passage/expression spans were verified. The reviewer subsequently reconciled 57 distinct statutory locator components in the complete bounded inventory; undispatched components and broader research leads remain recorded.

The source sections were absent from previous prepared-task frozen sets. Some had been encountered in earlier research and a different reference task. These are fresh prepared selections across three code families, not random sampling, a representative jurisdiction-wide benchmark, or an assertion of entirely unseen legal sources.

## Frozen execution

The configuration was unchanged from `statutory-pointer.question.json`: native Noul, literal expression in the direct question, two criteria distinguishing statutory text from its subject, and meaning-selected source context. Independent questions with identical contexts were batched. No wording or context changed after inspecting these responses.

| Measure | Result |
|---|---:|
| Independently reviewed questions | 36 |
| Positive expectations | 21 |
| Negative expectations | 15 |
| Agreement | 36/36 |
| Failed, missing or undecided answers | 0 |
| Requests / physical attempts | 19 / 19 |
| Retries | 0 |
| Reported cost | $0.000366030 |
| Model execution elapsed time | 2.2378 seconds |

Each response matched the pinned build and exact question IDs and contained valid Noul values. The .5 split reports evaluation agreement only; it is not a selected production routing threshold. Agent preparation/review time and cost were not included in the execution measurement. No net workflow-speed claim follows from it.

`statutory-broader-frozen` binds exact cases, configuration, reviewed labels, review, and both request arrangements. `statutory-broader-run` retains exact executed requests, raw responses and evaluation. Earlier runs remain unchanged; all 11 earlier prepared-task frozen bundle manifests were verified intact before this run.

## What the result enables

The prepared statutory-pointer task now has independent coverage/context review and a broader independently labeled result. It can inform the subsequent research-integration work. The agent still determines needed context, preserves exact occurrence identity, investigates targets and decides applicability. Code verifies the selected spans and typed execution. Jev supplies the narrow judgment.

One concrete unresolved target illustrates the boundary: CCP339 cites “subdivision 2” of CCP337, whose saved version uses letters. The expression clearly points to statutory text; resolving it requires source/history investigation, not replacing 2 with (b) by assumption. `broader.followup.json` preserves this issue and follow-up actions for every evaluated expression. A negative pointer judgment does not discard the contract, defined subject, date or other evidence from research.

Other atomic tasks were audited into focused prototypes and their configuration choices documented; they still require their own evaluation under Goal 5. Source-universe coverage is Goal 4. The full comparison against agent plus code is Goal 6. None is closed by this result.

## Implementation verification and next step

The freeze helper now accepts independent reviews only when their hashes match the current cases and question and no material ambiguity remains. The evaluator rejects duplicate/unknown result identities and preserves execution failures or exact .5 answers separately from semantic disagreement. The prototype catalog points to the current configuration instead of repeating the superseded wording.

**105 tests pass.** Existing raw experiments and production routing remain unchanged.

The next sequential item is **Goal 2: main-client cache reliability**—bind reuse to the correct model build and full request identity, validate cached responses, and test compatible reuse versus rejection. Broader reliability and operating benefit remain required before production integration.
