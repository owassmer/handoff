# Development review and OpenRouter execution — September 30, 2026

The refreshed environment restored OpenRouter access. The frozen draft-2 run completed with **22/22 valid answers and 20/22 agreements** against the reviewed development labels. The pinned model build matched every response. This is a development result, not held-out reliability or an end-to-end cost-benefit finding.

## Completed run after environment refresh

The [evaluation](runs/openrouter-draft-2-refreshed-20260930/evaluation.json) joins each response to its frozen request and reviewer label by case ID and exact request hash. All returned builds and answer structures passed validation. The SDK batch took 2.0068 seconds; median request latency was 0.2074 seconds; summed provider-reported cost was $0.001095066. This excludes agent investigation, source retrieval, preparation, and review time.

| Atomic task | Agreements / examples |
|---|---:|
| Definition presence | 4 / 4 |
| Explicit reference presence | 5 / 5 |
| Candidate term use | 4 / 4 |
| Express scope includes use | 2 / 4 |
| Whether/when document requirement changes | 5 / 5 |

Both disagreements were intentional missing-context controls. In dev13, the use's chapter was withheld; in dev14, the express scope sentence was withheld. Reviewed answer: INSUFFICIENT. Jev answered YES in both, with confidence 0.27 and 0.44 respectively. These are failures to respect the input boundary. Low confidence does not turn an incorrect answer into a correct one; the fully supplied positive dev11 also had confidence 0.44. This set cannot justify a confidence threshold.

The agent then recovered the missing hierarchy and introductory sentence from the pinned source material. [Recovery records](runs/openrouter-draft-2-refreshed-20260930/agent_recovery.json) retain the original failures. Each corrected payload is identical to the already answered dev11, so no duplicate model request was needed. The full input supports textual chapter inclusion; it still does not establish case applicability or incorporation of every technical condition.

Practical consequence: retain agent responsibility for obtaining and checking context. Code can reject a null required hierarchy field; it cannot establish semantic context completeness by shape validation. A Jev YES must not stand in for absent source material. Keep scope judgment in experimental agent-assistance use. The other four task results are encouraging development observations, not proof of reliable discovery in new chapters.

## Review and corrections

The reviewer received frozen request payloads and the six complete saved source texts. Author labels, explanations, follow-up actions, and the design narrative were withheld. Expected answers were judged from the supplied request; the full sources were used separately to detect context omissions. This is a separate agent pass in the same model family, not human review or independent-model evidence.

The [first review](blind_review.json) found one material question/label ambiguity: dev09's grammatical correspondence did not establish the definition's technical meaning. The author's YES was defensible only as candidate recognition; the reviewer preferred INSUFFICIENT under the broader wording. We changed the question before obtaining model results, instead of counting a plausible answer as model error.

Changes in draft 2:

- Renamed `term_use` to `candidate_term_use`, expressly testing an expression or grammatical variant concerning the same kind of subject. A YES proposes a connection for the agent to investigate; it does not establish incorporation of a definition's special conditions.
- Corrected the documentation question's claim that all referenced context was supplied. The selected range omits paragraph (h)(1), which is unnecessary for these narrow relationship questions but would matter for a complete timeline.
- Removed a destination-specific instruction that closely cued the sole negative. The question now consistently asks only whether or when the document requirement must be fulfilled.
- Added four cases: real-property ownership contrasted with personal-property ownership, definition adoption by reference, a second no-reference negative, and a separate damages consequence that does not change the document requirement.

There are now five question contracts and 22 development examples. The [second review](blind_review_v2.json) assessed the revised questions and new examples: 12 YES, eight NO, and two INSUFFICIENT, agreeing with all 22 revised author labels. [Reviewed labels](reviewed_expectations.jsonl) are frozen by exact request hash. Prior exposure to the first draft is recorded; these remain development examples, not a holdout. The first draft's inputs and author labels remain under [review/draft-1](review/draft-1/questions.json).

These corrections illustrate the intended pipeline: the agent identified what each result should establish, the reviewer exposed an overbroad semantic claim, and code pinned the revised questions and inputs. These changes preceded the completed Jev run reported above.

## Earlier failed execution, before environment refresh

The runner uses the installed TypeSafe SDK, the same OpenRouter base URL and credential source as the existing integration, and its configured model/build:

- Base URL: `https://openrouter.ai/api`.
- Model: `typesafe/jev-1.13`.
- Expected returned build: `typesafe/jev-1.13-20260917`.
- First request isolated; subsequent concurrency four; no retries.
- Local spending threshold $0.25 using the existing project reservation estimate; not a provider-enforced billing limit.

The [frozen request copy](runs/openrouter-draft-2-20260930/requests.json), [results](runs/openrouter-draft-2-20260930/results.json), and [run summary](runs/openrouter-draft-2-20260930/summary.json) preserve the attempt. Result:

```text
TypeSafeAPIConnectionError: Connection error: [Errno 8] nodename nor servname provided, or not known
```

The direct DNS check also failed for `openrouter.ai`. The configured provider was OpenRouter throughout. That sandboxed attempt could not reach the provider. The subsequent refreshed-environment run above succeeded using the same integration, without changing the provider, endpoint, model, or frozen inputs.

Of 22 requested examples, one has an execution error and 21 were not sent after the first failure. All 22 remained unanswered in that failed attempt. Its accuracy field is null. The zero accounted spending field is local runner accounting, not a verified provider billing statement.

## Verification and remaining work

The full pipeline test suite passes **80 tests**. New tests cover separation of labels from model input, changed source files, invalid source spans, missing/unexpected input fields, changed request identities, wrong returned model builds, missing/unknown answers, and malformed probabilities. Preparation verifies all six source hashes and 21 selected source spans. This establishes mechanical behavior, not legal or model correctness.

The independent draft-2 labels should be joined to returned model answers only by matching case ID and request hash. Missing or invalid answers remain separate from semantic errors. The refreshed run and recorded agent follow-up complete that development experiment. Additional held-out examples, context-assembly checks, and full-process comparisons remain necessary before claiming general reliability or a throughput benefit.
