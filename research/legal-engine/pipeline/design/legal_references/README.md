# Legal-reference presence experiment

**Later correction:** The founder identified unnecessary preparation and question complexity. The completion/use conclusions below are historical and superseded by [current corrective work](../prepared_tasks/README.md); original measurements are preserved.

Goal 1 establishes a usable detection contract and its limits. [GOAL.md](GOAL.md) defines the boundary and acceptance criteria. [AGENT_GUIDE.md](AGENT_GUIDE.md) explains use; [FOLLOW_UP.md](FOLLOW_UP.md) records source-reading demonstrations. Separate evaluation is complete (41/48 agreement), and the [final audit](FINAL_AUDIT.md) supports completion of this bounded goal.

## Fixed candidate contract

`question.v1-dev4.json` is the versioned question being evaluated. Its `dev4` suffix records its development history; it does not imply that the evaluation may modify it. The first draft is preserved in `question.v1-dev.json`. A public legal pointer counts whether it refers to the current section, enclosing unit, another provision, or a named public authority. Relationship classification, target resolution, and legal effect remain agent work. Every model answer requires source review.

Input is one `state.focus` string. Metadata, expected labels, reviewer reasons, and coverage strata never enter that model state. Saved-source examples include file hashes and exact Unicode spans; synthetic examples are explicitly authored. The task is English-only and concerns explicit public pointers, not every dependency or private document needed for a decision.

## Reproduction

Run from `research/legal-engine` using the existing virtual environment. The runner uses the existing credential loader and OpenRouter integration; do not put credentials in artifacts. Each execution output directory must be new. Re-running a model is a new observation, not a replacement for preserved responses.

```sh
.venv/bin/python -m pipeline.design.legal_references.experiment freeze \
  --cases pipeline/design/legal_references/fresh-evaluation.cases.json \
  --question pipeline/design/legal_references/question.v1-dev4.json \
  --review pipeline/design/legal_references/fresh-evaluation.review.json \
  --output pipeline/design/legal_references/fresh-evaluation-frozen

.venv/bin/python pipeline/design/agent_jev_code/run.py \
  --requests pipeline/design/legal_references/fresh-evaluation-frozen/requests.jsonl \
  --output pipeline/design/legal_references/fresh-evaluation-run

.venv/bin/python -m pipeline.design.legal_references.experiment evaluate \
  --bundle pipeline/design/legal_references/fresh-evaluation-frozen \
  --run pipeline/design/legal_references/fresh-evaluation-run

python3 -m pytest pipeline/tests -q
```

A review must bind the exact cases and question file SHA-256 values through `reviewed_inputs.cases` and `reviewed_inputs.question`. Changing either requires renewed review. Freeze rejects missing labels, unresolved material ambiguities, changed sources, and incorrect excerpts. Evaluation validates frozen file hashes, executed requests, result identities and pinned build; unanswered requests remain in the denominator. The freeze flag alone is not proof of chronology: inspect the review, frozen inputs, and run artifacts together.

The original development freeze predates the review-binding fix. Its preserved review and inputs are checked separately for exact equality by independent review; the historical bundle is not rewritten to claim the later validation existed earlier.

## Evidence interpretation

Development used 48 examples (10 exact saved-source passages and 38 authored). Jev answered all, agreeing on 44. Four model errors remain in the record. See `development.failure_review.json` for case-by-case adjudication and every authored adversarial example. Agreement is against independently reasoned task labels, not proof of law, calibrated confidence, or complete dependency recall. Reviewers are separate agents in the same model family, not independent human legal experts.

`prior_artifact_hashes.json` pins 58 pre-existing experiment artifacts. Goal 1 does not modify those pilots or repair the main production cache. Model invocation latency/cost excludes agent investigation and review. No throughput gain from adding this detector to mandatory source review has yet been demonstrated; the complete-process comparison remains a later goal.

## Preserved development progression

The first separately authored 48-case evaluation candidate exposed two wording gaps before model execution. Its isolated source heading and legal-context cutoff examples informed dev3; a private-context cutoff caution informed dev4. The entire candidate set is therefore retired to development. It is never reported as held-out evidence. Four additional authored controls test the clarified private-cutoff and heading boundaries. Original dev2 model results remain unchanged. A new author prepares fresh evaluation without reading these cases or outputs.
