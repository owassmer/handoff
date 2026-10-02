# Evaluation protocol before inference

This protocol implements the independent design review; it does not report capability acceptance.

## Fixed scope and sample floors

Six capabilities: definition_present, candidate_term_use, exception_to_requirement, changes_deadline, candidate_meaning, supports_claim. Development:24 per task (144), independently reviewed. Held-out:60 per task (360), at least20 statutory,20 regulatory,10 judicial and10 administrative-interpretation source clusters per task. Author labels and independent labels are separate. Where multiple tasks use one source, disclose cross-task dependence. More cases are required if a material contract branch is absent.

## Required challenge matrix

| Task | Positive branches | Consequential negatives and ambiguity controls |
|---|---|---|
| definition_present | express meaning; embedded meaning; adopted external meaning | ordinary use; illustration; reported unadopted proposal; heading-only selection repaired |
| candidate_term_use | direct use; qualified use; same sense with legal applicability denied | homonym; different actor/context; selected occurrence among repeated uses; missing definition recovered |
| exception_to_requirement | conditional exemption; narrowing duty; substitute expressly excusing original duty | independent duty; remedy; unchanged duty with alternative satisfaction; unresolved relative reference recovered |
| changes_deadline | duration; extension; tolling; holiday/service adjustment; changed trigger | other duty’s deadline; post-deadline remedy; unchanged temporal rule; historical context recovered |
| candidate_meaning | distinct competing meanings; varied correct-option position; no candidate fits | duplicate/overlapping alternatives resolved by agent before dispatch; missing use context recovered; genuine ambiguity investigated to completion |
| supports_claim | express support; necessary implication; accurately conditional proposition | missing condition; wrong modality/actor; reported argument vs adopted conclusion; historical vs present assertion; contradictory evidence |

Every case records its family, source cluster, edge case and downstream error consequence. Every cell needs inspected source-backed examples or a reasoned inapplicability finding. Missing input examples need a recovery record and completed reviewed judgment, not an INSUFFICIENT label counted as success.

## Configuration development

Start from contracts.json. Before final freeze, compare plain questions with concise native criteria on matched binary development cases; retain cases where criterion semantics materially distinguish labels. Compare a structured object only where it places selected objects more clearly than the state+question arrangement. Test independent shared-context questions against separate requests on a declared development subset. Choice uses mutually exclusive meaning descriptions; test option-order changes on development. Score is not justified by the current un-ordered task outputs.

Configuration selection follows task meaning, observed errors, latency and reported cost. Do not select a variant merely by aggregate agreement while consequential failures remain. Record exact alternatives, results and rationale. Any observed held-out failure becomes development evidence permanently; material changes require fresh affected-capability validation.

## Acceptance and reporting

Freeze final source preparation, questions, criteria, native serialization, SDK/model build and consumer policy before held-out inference. Independent expected answers must already exist. Record raw transport bytes, all attempts, usage, probabilities and failures. Report task/family/cluster results and conditional uncertainty calculations with purposive-sampling limits.

A diagnostic majority is not an authorization threshold. Each disagreement receives a documented investigation distinguishing preparation, expectation ambiguity, judgment and execution, with completed correction or demonstrated agent/code method. No task passes while material findings remain. Independent final review must inspect source coverage, code, actual results, corrections and usage instructions. Full-process value and routine integration remain Goals6/7.
