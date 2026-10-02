# Independent preparation review

Reviewed all 48 original revisit inputs and their preparation outcomes, all 35 dispatched revisit passages, all 12 new passages, the serializer, and the question. No old labels, model results, or later model outputs were read. No model was called. All 16 source-backed original spans, 15 dispatched revisit source spans, and 12 new source spans match their source files and recorded SHA-256 hashes. Every input hash and every ready selection matches the serialized passage.

The plain question, “Does this passage contain a legal reference?”, fits collecting research leads. Relative references such as “this section”, “this part”, and “this chapter” remain meaningful references. Generic legal qualifications are references even without exact locators; detecting them does not establish an applicable rule or complete the later research. Named judgments, court orders, and official legal guidance likewise supply legal research leads. The earlier candidate wording “refer to a legal provision” created an avoidable boundary for those last three kinds; the simpler reference wording removes it without a taxonomy.

All 35 ready revisit selections preserve the reference-bearing language and are suitable for this question. Removing the standalone section identifier from f001/f017/f019 appropriately separates source identification from the body. The real relative references in f001/f002/f004/f008/f010/f013/f017/f018/f021 remain intact. f019/f020 correctly retain only a substantive sentence without a reference. f033 retains a heading that actually refers to another section. f023 and f034 still contain references despite former/repealed status. f045 preserves both private-contract language and the separate Act reference. f046 retains the quoted instruction as text to classify. All 12 new passages are suitable; n001 and n009 contain generic legal leads, and n003/n006/n007/n008 state substantive requirements or describe notices without provision references. Nested numbering in n008–n011 does not prevent answering the reference question.

The 13 nondispatch decisions were reviewed individually:

| Input | Outcome | Assessment and practical effect |
|---|---|---|
| f015 | source_metadata | Real source hierarchy, not selected operative content. Retain the chapter locator and select the body. |
| f025 | needs_context | Truncated statutory sentence. It already reveals a legal pointer, but intact capture remains unfinished. No backing source was supplied to recover here. |
| f026 | different_task | Explicit private-contract fixture with truncated text. Route through the private-document workflow; do not interpret exclusion as a model inability to answer. |
| f027 | needs_context | Truncated, unprovenanced “Section” reference. Both source role and complete capture are unresolved. |
| f028 | needs_context | Section 934 already supplies a clear lead, but the statutory sentence is cut off. Recover intact capture before dispatch. |
| f029 | needs_context | Illegible target prevents determining the reference from the passage. Recover source text. |
| f030 | needs_context | “Preceding subsection” is already a clear lead; the illegible fee makes source preparation unfinished, not reference recognition impossible. |
| f031 | needs_context | Bare Section 934 has no established source role; recover whether this is a locator, a body reference, or private text. |
| f032 | source_metadata | Explicit fictional source heading; retain its locator and obtain body text. |
| f043 | different_task | Private rehearsal fixture expressly uses the Act title for a performance. Separate input workflow; it would be a useful negative control in a broader mixed-source experiment. |
| f044 | different_task | Clauses and Constitution name refer expressly to a private agreement. Separate private-document workflow. |
| f047 | different_task | Private workbook reference and embedded instruction. Separate rehearsal workflow; the instruction is not reviewer authority. |
| f048 | needs_context | Unfinished archivist quotation lacks an established target/source role. Recover intact text; the quoted answer instruction supplies no evidence. |

These outcomes are appropriate under the clarified preparation policy: repair capture before dispatch, retain source identifiers outside focus, and route private rehearsal/contract fixtures separately. The policy deliberately withholds some already-recognizable references and some answerable negative controls. Consequently, the 35 ready revisit cases cannot establish performance on all 48 original inputs; the 13 outcomes must remain visible as preparation results.

The serializer enforces identity, complete outcome coverage, nonempty selected spans, and attributed exact-source matching. It does not establish semantic completeness, select passages, or execute next actions; those remain agent responsibilities. Several stock reasons call annotations, headings, and commentary “operative text.” That wording is imprecise: their suitability follows from containing a coherent passage for reference detection, not from operative legal effect. The unsupported authored fragments cannot actually be recovered from available fixtures, so their next actions remain pending limitations rather than completed repairs.

The review JSON files bind the exact respective cases and question bytes. This is a review of input selection and expected reference detection, not legal applicability or a measurement of model performance. The earlier composite-design result must not be attributed to intrinsic model weakness on this revised task.
