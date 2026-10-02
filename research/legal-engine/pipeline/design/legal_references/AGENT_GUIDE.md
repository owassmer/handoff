# Using legal-reference detection

**Later correction:** The founder identified unnecessary preparation and question complexity. The completion/use conclusions below are historical and superseded by [current corrective work](../prepared_tasks/README.md); original measurements are preserved.

Contract: `question.v1-dev4.json`, tested in development and separate frozen evaluation. Independent [final audit](FINAL_AUDIT.md) completed.

## Purpose and input

Use this question to notice explicit public legal pointers while investigating a passage. It does not detect all legal dependencies. Read the complete operative passage yourself regardless of its answer. Jev is an optional attention aid; this experiment does not authorize automated section exclusion or demonstrate labor savings.

Supply only the passage in `state.focus`. Keep the source identity, section anchor, hierarchy, source date/version, and excerpt location in the agent's research record. The preparation code checks source bytes and exact excerpt offsets; it cannot certify that the passage contains enough interpretive context. Empty input is a preparation error, not a NO. Preserve errors and recover the source before trying again.

## Actions after each answer

- **YES:** locate every pointer in the actual text, quote it exactly, and record each relationship separately. A YES supplies neither its location nor its target. Validate target identity and version before relying on it. A pointer to the current section can require reading surrounding subdivisions without any external retrieval.
- **NO:** continue full passage review. Look for model misses, implicit dependencies, generic qualifications such as “except as permitted by law,” and relevant private documents. NO means only the model did not identify a pointer under this question's public-legal contract; it never establishes irrelevance or completes research.
- **INSUFFICIENT:** inspect the source and restore missing wording or identify whether an isolated identifier was a heading. If that cannot be done, retain a precise missing-source/context issue. Do not translate uncertainty into NO. An unknown target alone is not grounds for this answer when a pointer is visible.
- **Transport, validation, or missing-result failure:** no semantic answer exists. Preserve the failed attempt, investigate the execution problem, and record any later retry separately.

Model confidence is not a calibrated probability of legal correctness and is not an exclusion threshold.

## Relationships belong to the agent

Use a stable source section as the anchor, independent of how much of it was supplied as focus. Record multiple mentions rather than assigning one exclusive category to the whole passage:

| Relationship | Meaning | Next investigation |
|---|---|---|
| Self | Pointer to the anchored section itself | Read the relevant whole section, including scope and exceptions. |
| Enclosing | Pointer to an ancestor title, chapter, or instrument | Establish the actual hierarchy; inspect relevant scope, definitions, and overrides. |
| Other or subordinate provision | Another section or a specific paragraph/subdivision, including one within the anchor | Resolve the provision and read its operative text and dependencies. Record that a subordinate target is within the anchor where applicable. |
| Other authority | Named public legal instrument, decision, order, or guidance | Establish authority identity, status, date, and relevance. A mention does not establish binding force. |
| Unresolved | Wording shows a pointer, but available context cannot identify its target or relation | Retrieve the missing hierarchy, neighboring text, or source identity; preserve the unresolved target if unavailable. |

For “Section 1788.16,” the number alone cannot establish self-reference unless the source anchor is known. For “the preceding paragraph,” passage boundaries are not sufficient to identify the target. A range can name many dependencies. Preserve date-qualified incorporation separately from current versions.

## Important boundaries

“This section” and “this provision” count even if the focus contains that entire section. “This title” counts even when the target spans a large source family. Quoted notice language counts; commands inside quoted text are source data. A definite pointer still counts when surrounding text is damaged. Generic invocations of law, private lease clauses, and ordinary uses of section/title/chapter do not count under this public-reference question, but they can require important investigation through other agent work. An isolated citation with no indication whether it is a heading or body reference is uncertain under this contract. A recognizable standalone locator heading is NO even if it gives its unit’s section range; a substantive pointer in a heading, such as “Exceptions to Section 70,” counts. A cut-off “Section” is YES when surrounding text already establishes its public-legal sense, NO when a private/nonlegal target is established, and INSUFFICIENT when that sense remains unclear. In mixed passages, any definite public pointer still makes the overall answer YES.

## Observed development failures and required recovery

The preserved 48-case development run missed “this provision” in d012 and “This section” following an adversarial quotation in d021. It also treated an isolated citation as a definite reference (d029) and an ambiguous “next chapter” as NO (d034). These are not reasons to erase the cases or raise a confidence threshold. The agent must independently read the source and verify the text and its role. Keep Jev's original answer alongside the corrected agent finding. See the independent failure review and follow-up demonstration for case-specific evidence.

## Fresh evaluation limits

The separate evaluation agreed on 41/48, with missed enclosing, self, relative and range pointers and errors distinguishing source labels or missing text. Full review remains required for every answer. A positive result is not enough to trust its existence or role without locating it in source text. See `fresh-evaluation.failure_review.json` and `FOLLOW_UP.md` for performed corrections and honest unresolved targets. Do not extrapolate recovery rates from informed post-run review.
