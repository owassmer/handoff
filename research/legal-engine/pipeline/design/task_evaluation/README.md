# Focused legal judgments — Goal 5

Status: development implementation; no task is yet accepted for routine use. See [objective](OBJECTIVE.txt), [plan](GOAL.md), [contracts](contracts.json) and [independent design review](DESIGN_REVIEW.md).

Use the legal-engine `.venv/bin/python` interpreter; it contains the native TypeSafe SDK. Provider configuration comes from `pipeline/jev_questions.json`: OpenRouter, Jev1.13 and its pinned response build. Credentials use the existing `pipeline.jev.api_key()` loader. No credential enters saved evidence.

## Prepare and review

Cases contain `id`, `task`, `family`, `source_cluster`, `state`, and `sources`. State contains exactly the task's declared fields plus optional `context` when needed. Each source field has a root-relative path, SHA256 of the UTF8 source file, and start/end character offsets into its decoded text. Exact source text is required. Metadata stays outside state. Term tasks require a uniquely occurring `use_expression` containing the term once. Choice alternatives live in `criteria`.

The agent supplies enough context to make the judgment well-posed. Code validates selected bytes and structure; those checks do not prove semantic completeness. When context is missing, retrieve it, complete preparation and independently review the resulting judgment. Preserve the initial defect and recovery record.

An independent reviewer reads cases and authoritative surrounding material without author labels or responses. Save `cases_sha256`, `contracts_sha256`, `reviewer`, `author_labels_seen:false`, `model_responses_seen:false`, `material_findings:[]`, and `cases:[{id,expected,reason}]`. Resolve material preparation or expectation disputes before freezing. Disclosure fields document the process; they cannot mechanically prove independence.

From the legal-engine root:

```sh
.venv/bin/python -m pipeline.design.task_evaluation.freeze CASES.json REVIEW.json BUNDLE
.venv/bin/python -m pipeline.design.task_evaluation.run BUNDLE OUTPUT --cap 1
.venv/bin/python -m pipeline.design.task_evaluation.evaluate BUNDLE OUTPUT EVALUATION.json
```

Freeze copies exact case, review and contract snapshots, prepares native requests, and hashes the required implementation. The runner rejects changed or incomplete bundles. Each HTTP attempt records actual serialized body text/hash and its parsed body before transmission, and checks it against the frozen request. Retries are disabled; failures stop subsequent dispatch and remain explicit records. The cost cap uses a $0.01 reservation per request; actual reported overshoot stops subsequent dispatch. This reservation is a stop policy, not a provider-enforced hard billing cap.

## Read the results

`evaluate.evaluate(cases, labels, requests, results)` validates response identities, raw transport capture and typed answers before comparing independently expected judgments. It preserves errors and unsent work. Noul majority and Choice argmax are diagnostic only; ties remain undecided. Probabilities are retained, with no inherited authorization threshold.

Report task and family outcomes, source clusters, execution gaps and every investigated disagreement. The binomial upper bound is an explicitly conditional reference calculation; purposive clustered challenge cases do not establish population error rates. No agreement score authorizes a payment, legal conclusion or research closure.

Development configuration comparisons, held-out evaluation, corrective fresh rounds and capability-specific usage acceptance remain pending. Goals 6 and 7 own complete-process comparison and routine integration.
