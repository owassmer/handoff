# Preparation correction: observations

Current status: [independent review and broader evaluation](BROADER_REVIEW.md) now complete bounded Goal 1. The checkpoints below retain their original results and limitations.

This work corrects our input/task design. It does not attribute the previous disagreements to intrinsic model limitations. Historical results remain unchanged. The old completion claim is superseded in PLAN.md and linked historical status documents.

## What changed

Agent-selected operative spans exclude source labels. Code verifies exact spans and accounts for every input. Missing context, locator-only material, and different document work remain separate preparation outcomes. Context needed to understand a phrase must survive selection; removing metadata does not mean removing all context.

The reference question is being narrowed to one selected expression in its passage. The expression is copied by exact character offsets; the model also receives the source kind. Source numbers, filenames, expected answers, and review notes do not enter its input. The question is simply: “Does the expression refer to a legal provision?”

Other task prototypes now use selected passages/claims. Definition sense, exceptions, deadlines, and claim support are separate questions. Explicit scope containment has a small checked code function after the agent establishes the scope. These additional prototypes are not yet evaluated or integrated into production.

## Whole-passage attempts retained

| Attempt | Requests answered | Reviewed agreement | Limit |
|---|---:|---:|---|
| “Does this passage contain a legal reference?” — revisited inputs | 35/35 | 27/35 | “Legal reference” did not reliably distinguish references from ordinary legal prose. |
| Same question — additional source selections | 12/12 | 9/12 | New selections from two related source sections; not a representative benchmark. |
| “Does this legal passage refer to a provision?” — development diagnostic | 44/44 | 30/40 unambiguous labels | Four labels flagged ambiguous before execution remain unscored: f034, f042, n001, n009. |

The first attempt used 35 of the original 48 inputs. Seven were incomplete/role-unknown, two contained only metadata, and four belonged to private-document work. The 13 are not model successes. The provision diagnostic separately excludes three authority-reference examples that do not fit its provision question; all three were correct in the preceding run, and their work remains with the agent. No old score is rewritten using the changed denominator.

A candidate phrased in terms of “legal text” was rejected before execution because contracts, pleadings, and notices also satisfy that wording. Merely shortening or substituting nouns did not solve the input-granularity problem. These observations led to selecting the actual expression to judge instead of asking one question about an entire provision.

Both executed whole-passage questions produced YES on straightforward operative prose without references. Some short local pointers were missed. This suggests confusion about the intended object of judgment, but these runs changed several inputs and are not a causal isolation experiment. The expression probe tests the practical correction without claiming to prove the model's internal mechanism.

## Expression probe

Executed after independent review of all 20 expression cases (11 positive, 9 negative). This is a deliberately selected development probe, including earlier difficult cases and negatives. It tests the prepared expression judgment, not automatic discovery of every expression in a legal corpus. Candidate discovery remains explicit agent preparation; no regex completeness or throughput gain is claimed.


| Configuration on the same 20 development cases | Agreement | Reported cost | Seconds |
|---|---:|---:|---:|
| Expression + passage + source kind, Choice | 16/20 | $0.000328230 | 4.1877 |
| Same wording/state, native Noul without criteria | 14/20 | $0.000281190 | 1.4569 |
| Expression beside question in structured instructions, “textual cross-reference”, Noul | 16/20 | $0.000286230 | 1.5481 |
| Same structured request with concise true/false criteria | 19/20 | $0.000316470 | 1.3027 |

All calls answered; no retries. Noul majority above/below .5 is a development comparison only. Native type alone did not fix meaning. The structured treatment changed wording and placement together, so it does not isolate their individual effects. Its labels were carried from the reviewed expression task, not independently re-reviewed for the changed wording. The criteria comparison kept that structured request fixed and added the distinction between identifying a unit of legal text and describing a thing/event/duration.

The final disagreement is xf016, “the contract”, answered .59. The intended public-provision target is not adequately expressed by “legal text”, which can include contracts. This is an unresolved task-definition boundary; the 19/20 result must not be promoted as cleared evaluation or production reliability. Other local-reference failures in the preceding run disappeared, but these cases have been used for development. Fresh representative evaluation and candidate discovery measurement remain necessary.

Exact requests, raw responses, evaluations and costs remain in `expression-run`, `expression-noul-run`, `expression-structured-noul-run`, and `expression-criteria-noul-run`. The unexecuted `cross-reference.question.json` Choice proposal is superseded by the recorded native structured diagnostics, not a separate successful experiment. See [configuration guidance](CONFIGURATION.md) for the pipeline-wide correction and limits.

## Statutory task and fresh follow-up

See [STATUTORY_PILOT.md](STATUTORY_PILOT.md) for the next configuration: 18/20 on reused development inputs, 25/27 on new selections, matched separate/batched execution, corrected occurrence preparation, and 11 official dependency retrievals. The two fresh false positives remain visible. These are bounded research observations, not completed Goal 1 or production reliability.

The pilot record now includes direct-expression, pointer-versus-subject, and governing-clause checks. Current observations are 60/61 development, 16/16 new selections, and 1/1 targeted context correction. The original 25/27 and all other prior results remain intact.
