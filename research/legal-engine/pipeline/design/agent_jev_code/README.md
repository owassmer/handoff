# Agent-led legal investigation with Jev and code

Working design, September 30, 2026. Implements the user's agreed division of work as an instructed research flow and reproducible development inputs. The five question contracts and 22 examples are development material. A reviewer with author labels withheld reviewed the original inputs and the corrected second draft. After an initial DNS failure, the refreshed environment completed the OpenRouter run: 20/22 agreements, with both missing-context controls failing. See the [review and execution report](REVIEW.md). Existing routing, active rules, and runtime behavior are unchanged.

## Purpose and responsibility

Handoff must establish what work and account treatment are justified, perform the full operating flow, preserve legitimate recovery, and avoid unnecessary expense and litigation. Legal mapping supplies the reusable reasoning underneath those decisions. These examples address dependency discovery within that larger pipeline; they do not replace source enumeration, currentness research, controlling-authority research, or legal synthesis.

The **agent** reasons and orchestrates along the instructed flow: understands the operating question, inspects source structure, chooses useful questions, obtains the necessary material, evaluates results, follows dependencies, and synthesizes the law. It can decide a straightforward relationship directly without adding a Jev call. Agent conclusions remain inspectable against source material and independently reviewed where the research procedure calls for it.

**Jev** supplies rapid, parallel, atomic semantic judgments. Each answer establishes one limited proposition over a specified input. The agent uses that speed to examine more material and test more candidate relationships. A positive does not establish complete legal relevance; a negative does not close a section. Use a task only where the investigation benefits from many comparable judgments or measured quality/cost improvement.

**Code** retains and validates structured sources, assembles the specified inputs, dispatches work, associates results with their exact inputs, tracks coverage and dependencies, and computes determinate outputs. Code can establish an exact citation's identity without judging its legal effect. Schema validity and quotation equality are mechanical checks, not proof of meaning.

Atomicity concerns the proposition, not an arbitrarily small text window. A single semantic judgment can require a complete subsection, introductory language, exceptions, or another provision. A request can eventually contain several independent typed questions over the same context if evaluation shows that does not degrade their answers. Start with one question per request to establish the baseline; batch requests concurrently for throughput.

## Instructed flow

| Step | Agent work | Jev work | Code work and retained result |
|---|---|---|---|
| 1. Frame the investigation | Identify operating decisions, jurisdictional layers, source dates, and facts that may alter applicability. Separate unknown case facts from unresolved law. | None required. | Record the investigation scope and initial knowledge snapshot. Existing research is an explicit starting input when used. |
| 2. Inspect and enumerate | Examine official source hierarchy and representative bodies. Establish what a section/subsection means in this source; investigate capture defects. Enumerate whole relevant units and dependencies beyond them. | Optional atomic scans of ambiguous material, after a task is specified. | Preserve immutable captures, source locations, hierarchy, dates, and missing-source records. Check enumeration independently of model results. |
| 3. Prepare broad scans | Select useful scan questions and context rules. Inspect long or mixed sections before deciding boundaries. | Across prepared passages, identify explicit definitions and explicit references as separate propositions. Other needs receive separately defined tasks, not an expanded catch-all relevance question. | Retain each passage's parent, exact offsets, and source hash. For a complete scan, check that focus spans cover the entire operative body; record every gap and every unanswered request. No silent truncation. |
| 4. Form candidates | Read positive/uncertain passages; identify terms, scopes, target references, exceptions, and implicit dependencies. Inspect negatives sufficiently to test the scan's blind spots; maintain section review coverage. | Narrow repeated comparisons where useful, such as one candidate term use against one definition. | Resolve unambiguous citations, preserve subsection paths, validate agent-selected text spans, deduplicate candidates, and track unresolved targets. A parser miss is not evidence of absence. |
| 5. Assemble necessary context | Retrieve the target provision and governing scope, exceptions, or version evidence. Decide what must be supplied for the next question. | Answer a bounded relationship question only when the specified input contract can be met; explicit insufficiency can request further investigation. | Validate structural completeness and source identity. Save the actual request. Structural completeness cannot certify that the agent selected enough legal context. |
| 6. Interpret and follow | Combine findings, investigate disagreements, and follow new dependencies. Agent can correct a Jev result against the source and records why. Seek governing interpretations when textual analysis is insufficient. | Parallel additional atomic checks chosen by the agent. | Maintain links between affected provisions, requests, agent findings, and remaining work. Deduplicate cycles without suppressing a genuinely different question or version. |
| 7. Synthesize and test | State the complete legal branch with its scope, conditions, exceptions, authority, and source version; test its consequence for work and account decisions. | Optional atomic checks of specific claims, separately evaluated from discovery tasks. | Validate source quotes, typed facts, branches, and exact calculations. A missing fact is not false or zero. Feed results into existing review/rule workflows. |
| 8. Reconcile completion | Explain how each relevant section and dependency was handled; close only after unresolved material questions are investigated. Keep unrelated operating work progressing. | No model result itself closes the investigation. | Report source coverage, open dependencies, unreviewed sections, changed sources, and missing/invalid answers separately. |

A failed fetch, malformed output, insufficient-context answer, low-confidence result, or unsupported target creates specific agent work. It does not become a negative. Completion depends on reconciled investigation and review, not convergence of Jev scores. Absence of an explicit reference does not settle the presence of an implicit definition, general rule, or controlling interpretation.

## Worked investigation A: property remaining after move-out

Operating question: what investigation, notice, storage, release, or disposal is justified before clearing a unit, and what protects the operator from avoidable claims?

The saved [CIV 1983](../../../jurisdictions/CA/texts/CA_CIV/1983.txt) supplies notice provisions. The agent examines its enclosing chapter and reads [1980](../../../jurisdictions/CA/texts/CA_CIV/1980.txt), [1981](../../../jurisdictions/CA/texts/CA_CIV/1981.txt), and referenced provisions. It does not wait for a model to discover every evident relationship. These are frozen source examples, not a new conclusion that this chapter applies to every case.

1. A definition scan finds meanings in 1980 despite the empty heading in its register record. Code's heading regex cannot establish that finding. A NO on the delivery language in 1983(c) only means that passage does not explicitly define a term; its delivery duties remain important.
2. The agent identifies the full definition of “reasonable belief,” including its investigation exception, and the phrase “reasonably believes” in 1983(a). Jev's `candidate_term_use` task tests that one candidate connection. It does not establish incorporation of the definition's detailed investigation standard. A literal word-match-only search can miss the grammatical variation.
3. A separate `scope_includes_use` task receives the introductory “As used in this chapter” language and the actual hierarchy of both provisions. Its YES establishes textual reach, not case applicability or temporal validity. With the introductory sentence or necessary hierarchy withheld, the intended answer is INSUFFICIENT. No section-number guessing.
4. The agent combines these findings and investigates what they mean for locating property owners. It also investigates 1981's exclusions. Treating 1980's defined “owner” as the building owner would produce the wrong inquiry.
5. An explicit-reference scan of 1983(b) points toward a reference the agent/code must resolve to 1989. The agent follows 1989's release/disposal conditions and its further references. It must not turn a liability-protection reference into unconditional permission to discard property.
6. Only after the applicable path, facts, and time rules are established does code compute dates or amounts. The broader chapter review, authority work, and case-fact investigation are still required before operational use.

Development cases dev01, dev03–05, dev07–14 exercise pieces of this loop. Their expected answers concern the supplied passages, not complete legal advice.

## Worked investigation B: a request for refund documentation

Operating question: how should Handoff answer a disputed charge/document request, obtain missing material, and preserve a justified recovery without unnecessary work or exposure?

The saved [CIV 1950.5](../../../jurisdictions/CA/texts/CA_CIV/1950.5.txt) has 26,437 body characters in the register and currently routes as LONG without a Jev answer. Its operative content includes embedded definitions and interdependent paragraphs. This exercise uses the saved version whose history names the 2025 amendment effective January 1, 2026. It does not apply that version retroactively to the 2023 Breakwater account or establish session-end currentness.

1. The agent reads the whole section and identifies the document-requirement group in subdivision (h). Code retains exact source spans, the containing subdivision identity, and links back to the complete capture. For a full-section scan, every remaining provision also needs a focus span or an explicit agent review; these examples alone do not achieve that coverage.
2. Jev can independently test whether paragraph (4) changes whether/when paragraph (2)'s documents must be provided, and whether paragraph (5) does so. The input includes paragraphs (2) through (7), rather than isolated fragments stripped of their references. Both development answers are YES, with different consequences that the agent must read and explain.
3. The agent synthesizes the exception and the request-driven restoration together. Jev's YES does not establish that a waiver is valid, the request is timely, the deduction is lawful, or an amount is recoverable.
4. Paragraph (6)'s mailing destination is a deliberate negative for this **specific** question about whether/when documents must be supplied. It remains a separate operating requirement. Paragraph (3)'s estimate and later-completion mechanism is a positive.
5. The agent establishes the source version, deductions, invoices, work completion, request/receipt dates, delivery facts, and any agreement. It follows the section's other limits and relevant authorities. Code computes only the dates and amounts whose governing inputs have been established; missing invoices or dates create concrete investigation tasks.

Development cases dev02, dev06, and dev15–18 show the inputs and expected atomic answers. They do not conclude how the real dispute must be settled.

## Initial Jev contracts

Exact instructions, choices, and required fields are in [questions.json](questions.json). All five use the integration's existing Choice concept with YES / NO / INSUFFICIENT. INSUFFICIENT represents a substantive input/meaning limitation; a provider timeout or invalid response is an execution error, recorded separately. Model scores, if returned, require empirical evaluation and do not erase either distinction.

| Task | One proposition | Essential input | Agent use |
|---|---|---|---|
| `definition_present` | This focus passage explicitly assigns meaning to a term. | Complete focus passage for the local scan. | Locate and read full candidate definitions, including scope and exceptions. |
| `reference_present` | This focus passage explicitly refers to a legal provision or enclosing unit. | Complete focus passage. | Resolve candidate targets and retrieve their text; continue implicit-dependency work independently. |
| `candidate_term_use` | This expression or grammatical variant refers to the same kind of subject, identifying a candidate connection only. | One complete defining clause, the term, and the use with enough surrounding text. | Test a candidate connection, allowing grammatical variation; establish scope separately. |
| `scope_includes_use` | The express textual reach includes this use's location. | Actual scope language, both legal locations, and the use. | Confirm or reject this textual reach; investigate absent/ambiguous scope. |
| `qualifies_requirement` | This candidate changes whether/when these documents must be provided. | One requirement, one candidate, and enclosing/referenced context. | Investigate and synthesize the condition or restoration; preserve separate duties. |

The fifth question is intentionally specific to the worked documentation requirement. Do not silently reuse it for all legal qualifications. New tasks or broader wording require their own examples and evaluation. These five are a small initial toolset; the agent should not force all legal investigation through them.

## Input discipline and runnable preparation

[examples.json](examples.json) holds 22 agent-authored cases with expected answers, reasons, and follow-up actions. [sources.json](sources.json) pins six saved source files and 21 exact selected spans. Every selector refers to a real captured passage; omitted-context controls deliberately remove context rather than fabricate statutory text.

Run from the repository root:

```sh
python3 research/legal-engine/pipeline/design/agent_jev_code/prepare.py --output-dir /tmp/handoff-dependency-inputs
```

[prepare.py](prepare.py) validates source hashes and exact Unicode character offsets, rejects unexpected state fields, and emits:

- `requests.jsonl`: neutral case ID, request identity, pinned build, task version, and the exact model/question/state payload. It excludes expected answers, review explanations, strata, and proposed agent actions.
- `expectations.jsonl`: separate author labels and reasons, joined only by case ID and request hash.

Only `payload` is model input. `primitive`, `instructions`, and `criteria` follow the existing internal question-spec shape; a live runner must construct the SDK Choice object, not assume this JSON is a provider wire API. The request identity includes the pinned build, assembled question, complete input, and assembler/task versions. Source-location fields within passages provide traceability; hierarchy needed to answer a scope question is supplied explicitly, so a missing-hierarchy control cannot recover it from an extra metadata field.

This preparer is a small executable specification, not a dispatcher, a statutory segmenter, a semantic validator, or a substitute for agent work. It performs no model calls and changes no source, rule, or routing record. Hash/span equality proves the excerpt was copied correctly; it does not prove context sufficiency or legal interpretation. An agent-authored span and expected label still require review.

## Calibration and comparison plan

1. **Review the development tasks before measuring accuracy.** Read complete sources and inspect each question/input/expected-answer combination. Correct ambiguous criteria rather than rewarding an answer to a different question. The 22 examples are development material, including deliberately similar cases; they cannot serve as independent holdout evidence.
2. **Freeze the actual starting state.** For initial discovery, no finished rule matches or later review citations enter the agent's or Jev's inputs. For incremental research, explicitly provide only research available at that checkpoint. Evaluate those two modes separately. The previous 481/483 result used existing research context and measures combined routing, not standalone Jev accuracy or discovery from an empty register.
3. **Establish reference answers independently.** Have a reviewer reason from the full source and governing context without seeing Jev outputs or the author's expected answers. Distinguish a task's answer from whether the whole input assembly was adequate. Resolve disagreements before using labels as truth. A same-model-family reviewer performed the label-withheld development review here. This is not human or independent-model review and is not a held-out evaluation.
4. **Construct a held-out set by source family.** Keep related chapters, repeated clauses, and alternate versions of the same provision together so variants cannot straddle development and holdout. Include headingless and mixed sections, long provisions, scope limitations, grammatical variants, generic words in different senses, relative references, ranges, missing targets, historical versions, and exceptions to exceptions. Determine sample sizes from desired error bounds and expected task prevalence; do not claim reliability from these 22 cases.
5. **Measure three distinct layers.** (a) Discovery and assembly: were the needed passages/candidates found and supplied? (b) Atomic judgment: correctness by task and stratum, including insufficiency and false negatives. (c) Completed investigation: consequential dependencies/branches found, operating decision quality, agent corrections, and work remaining. Include all unanswered and invalid requests in completion reporting; do not hide them behind accuracy over answered cases.
6. **Compare complete processes with equivalent starting material.** Compare the existing research/routing process, a competent agent with source tools and code, and that same process with Jev assistance. Use separate runs without shared completed findings. Measure elapsed time, request/token volume, cost, agent effort, and decision errors. Jev earns its place through useful throughput or quality improvement, not raw call speed.
7. **Tune only on development data.** Freeze prompts, segmentation/context policy, model build, and routing policy before held-out evaluation. Calibrate thresholds per task if probabilities improve decisions; no unmeasured reuse of old relevance thresholds. Report uncertainty and sample sizes. A consequential miss triggers investigation of retrieval, framing, context, judgment, or synthesis—not automatic threshold lowering.
8. **Introduce through shadow use.** Agent continues full section review while measuring suggestions. Promote only the tasks whose benefit is demonstrated; retain investigation paths for uncertainty, missing material, and detected blind spots. No automatic legal exclusions follow from these draft questions.

## Supporting implementation sequence

Already executable here: frozen source selections, five task contracts, 22 development inputs, label-separated assembly, and failure checks for corrupted sources/spans or contaminated input fields.

Next implementation work follows the reviewed flow:

1. Add agent-facing work records for scope, source coverage, candidate dependencies, exact requests, results, agent findings, and outstanding retrieval. Reuse existing section/source identities and reviewer outputs. Keep proposed links distinct from confirmed findings without making the operator manage research metadata.
2. Add reusable passage preparation that preserves the source hierarchy and records complete scan coverage. The agent chooses legally coherent context; code verifies offsets, bounds, coverage, and source versions. Oversized input returns a preparation task; do not silently truncate or equate atomicity with arbitrary text length.
3. The development [runner](run.py) now uses the installed SDK and existing OpenRouter configuration, with a first-request check, bounded concurrent batches, no retries, pinned-build and answer validation, frozen request copies, and separate execution errors. It has no response cache. Integrating successful tasks into the main client remains future work. Existing code verifies the pinned build on live responses but does not recheck it on cache hits; cache keys also currently use the model alias without the pinned build. Fix both before cross-build comparison. Reuse its bounded concurrency, request logging, and spending controls after checking their behavior for the new inputs.
4. Run independently reviewed development inputs, inspect failures, and then run the frozen comparison/holdout. Integrate successful tasks into the agent loop rather than replacing the agent with a fixed classifier chain.

No new universal framework or standalone all-pairs dependency service is required. Start with these two real investigation loops and generalize only the repeated mechanisms.

## Verification and execution

The complete regression suite now includes input preparation and response validation tests. [verification.json](verification.json) records counts and hashes; [REVIEW.md](REVIEW.md) records the blind review, corrections, and OpenRouter execution results. Mechanical checks do not establish model accuracy.

After preparing inputs with the command above, run from the repository root using a fresh output directory:

```sh
research/legal-engine/.venv/bin/python research/legal-engine/pipeline/design/agent_jev_code/run.py --requests /tmp/handoff-dependency-inputs/requests.jsonl --output /tmp/handoff-dependency-jev-run
```

The runner reads the existing credential at runtime and never writes it. It sends only frozen request payloads, not author expectations or review notes. Default concurrency after the first request is four, retries are disabled, and the local spending threshold is $0.25 using the existing project's reservation estimate. This is not a provider-enforced billing cap. A failed first request stops the batch. Results retain execution failure separately from YES, NO, and INSUFFICIENT. No production routing or legal rules are changed.
