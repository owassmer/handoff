# Prepare the work before asking Jev

The founder corrected the prior experiment: source selection, task meaning and configuration belong to us. The old 41/48 result tested our combined preparation and question; attributing seven intrinsic model failures was not established. Historical inputs, expectations, responses and audits remain preserved. Goal 1 is now complete within its bounded research scope, supported by [independent review and broader evaluation](BROADER_REVIEW.md).

## Current method

1. Agent identifies the research or operating decision and selects its needed evidence. Source locators stay outside the judgment passage; real references in the operative text remain.
2. Agent selects the exact expression and its governing context. Keep other references and definition dependencies as separate work. Use enough context to interpret the expression, without automatically supplying a whole section.
3. Code checks source hashes and exact spans, accounts for inputs, and preserves the selected occurrence for target resolution.
4. Choose the question type and configuration for the task. The current statutory task uses native Noul: **Is “<selected expression>” a pointer to statutory text?** Its criteria distinguish a statute or unit of statutory text from something discussed in the text.
5. Batch independent questions sharing useful context. The agent resolves targets and follows dependencies; code handles exact identities and calculations. A reference judgment neither decides applicability nor closes research.

[Configuration guide](CONFIGURATION.md) covers Noul, Choice, Score, structured content, direct questions, batching and uncertainty. More structure or more context is not automatically better.

## Latest evidence

The [independent review and broader evaluation](BROADER_REVIEW.md) returned **36/36 agreement** on new prepared selections across CCP, BPC and FIN, using the unchanged final question. An independent reviewer fixed expectations before seeing author labels or model responses. An additional historical coverage review found all 15 explicit statutory-pointer occurrences accounted for in the earlier four complete bodies; its result exposure is disclosed.

The [earlier statutory pilot](STATUTORY_PILOT.md) preserves development corrections, the matched batching comparison and first-hop follow-up. Those results are not recombined into a perfect score. The latest run is a bounded, deliberately selected evaluation, not representative corpus-wide reliability or proof of end-to-end savings.

The agent previously retrieved 11 official dependencies and recorded what remains in [fresh.followup.json](fresh.followup.json). [Broader follow-up](broader.followup.json) retains a source-numbering discrepancy and actions for each new selection. No production routing or legal rule changed.

## To-do

- [x] Correct the old completion claim and preserve previous observations.
- [x] Audit other question contracts and record focused prototypes.
- [x] Implement exact selection and complete input accounting.
- [x] Test expression selection, native configuration, direct wording and governing context; preserve every attempt.
- [x] Compare equivalent separate and shared-context execution.
- [x] Perform bounded first-hop dependency follow-up and record what remains.
- [x] Independently review final preparation, fresh expectations and bounded candidate coverage.
- [x] Evaluate 36 broader fresh statutory selections with the final method.
- [ ] Evaluate other legal authority types and remaining tasks under Goal 5.
- [ ] Compare complete useful work against an agent-plus-code baseline.

The other tasks in `questions.json` remain prototypes requiring their own evaluation. Explicit hierarchy containment uses code after the agent establishes the scope.

## Earlier preparation accounting

The original 48 inputs yielded 35 ready passages. Seven required missing context or source-role recovery, two contained only locators, and four belonged to private-document work. Those 13 were preparation outcomes, not correct model negatives. Authored fixtures without recoverable sources remain explicitly unavailable. Twelve additional early selections came from CIV 1633.8 and 1785.26; they were not an independent representative benchmark. [RESULTS.md](RESULTS.md) preserves those attempts and links later work.

`prepare.py` verifies agent-selected spans; it is not an automatic semantic body extractor. `statutory.py` freezes and executes the bounded native-Noul experiments using the existing OpenRouter client, budget handling and shared question adapter. Credentials are not copied into artifacts. No universal confidence cutoff or mandatory duplicate full classification has been introduced.

Next sequential implementation item: **Goal 2 — main-client cache reliability**, tracked in [PLAN.md](../../../PLAN.md). The complete-process comparison remains Goal 6.
