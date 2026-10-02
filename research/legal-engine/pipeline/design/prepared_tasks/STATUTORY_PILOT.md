# Statutory-reference preparation and follow-up

Current status: [independent review and broader evaluation](BROADER_REVIEW.md) now complete bounded Goal 1. The checkpoints below retain their original results and limitations.

September 30, 2026. This is a bounded continuation of Goal 1, not its completion.

## Initial decision

The current task asks: **Does this expression refer to a statute or part of a statute?** Native Noul, structured instructions containing the exact selected expression, and two concise criteria distinguish statutory text from other referents. The surrounding statutory body is shared state. This replaces the ambiguous “legal text” wording for this statutory task; it does not silently classify court decisions, regulations, private documents or generic references to law as irrelevant to the overall research.

The development set returned 18/20. The prior contract-text disagreement was corrected, but two ordinary-expression false positives remained (xf011, xn007). That result is preserved in `statutory-development-run`. Wording and criteria changed together; no isolated causal claim is made.

## Fresh sections and matched batching

Before dispatch, the preparing agent read the complete operative bodies of CIV 1942, 1942.1, 1942.2 and 1942.6, selected 27 expressions, and froze YES/NO expectations with reasons. These selections were absent from the earlier experiment datasets; the underlying statutes already belonged to the saved California corpus. They are four related sections, not a representative jurisdiction-wide benchmark or independently reviewed heldout set.

| Execution | Questions | HTTP requests | Agreement | Reported cost | Elapsed seconds |
|---|---:|---:|---:|---:|---:|
| Separate | 27 | 27 | 25/27 | $0.000647934 | 2.0899 |
| Shared section context | 27 | 4 | 25/27 | $0.000160944 | 0.6947 |

All calls used the pinned OpenRouter build, no retries, and the same conservative $0.25 experiment cap. The first request was isolated, followed by concurrency four. These are single-run observations, not a latency benchmark. Batching reduced reported cost by about 75% in this comparison. Majority classifications were identical; probabilities were not all identical. Code verifies that every per-question instruction, criteria and context is identical across the two arrangements.

All 15 selected statutory references received YES. Ten of 12 negative selections received NO. The two false positives were “Any agreement” in CIV 1942.1 and “the 30th day following notice” in CIV 1942, with batched values .57 and .60. A .5 split was used only to report development agreement. No production cutoff was selected, and no intrinsic model-failure explanation was established. The agent recorded the former as private-document work and the latter as a timing condition, rather than attempting nonexistent statutory retrievals.

## Preparation correction discovered in follow-up

One selection of “subdivision (a)” picked its earlier occurrence inside the external Section 1962 pointer instead of its intended occurrence in CIV 1942(c). Both are statutory references, so the Boolean expectation remained YES; their targets differ. The corrected span is in `statutory-fresh-corrected-frozen`. A regression test checks its surrounding clause.

`fresh-preparation-correction.json` explains the change. Exact model requests and hashes are identical because the selected string and entire context are identical; original answers can be used for that Boolean question without a new inference run. Original frozen inputs and results remain intact. Their original local-target label reason should be read with this correction. The corrected occurrence is used in `fresh.followup.json`. This is why reference presence, occurrence selection and target resolution must be checked separately. No independent candidate-recall claim is made.

## Actual follow-up

The agent recorded targets or investigation actions for all 27 expressions, using exact source spans. Nine named utility-payment provisions were retrieved from the official California site: PUC 777, 777.1, 10009, 10009.1, 12822, 12822.1, 16481 and 16481.1, plus GOV 60371. CIV 1929 and CCP 1280 were also retrieved: 11 official source snapshots total. HTML, extracted text, URLs, retrieval times and hashes are retained in `dependency-sources/manifest.json`.

CIV 1942.2's utility-payment route requires investigation of provider type, metering, customer status, bundled rent charges and actual payments. The statutory pointer leads to these conditions; it does not establish a tenant's deduction from a ledger alone. See the retrieved [PUC 777](dependency-sources/PUC-777.txt), [PUC 777.1](dependency-sources/PUC-777.1.txt) and [GOV 60371](dependency-sources/GOV-60371.txt).

Repair responsibilities also require the tenant-contribution rules in [CIV 1941.2](../../../jurisdictions/CA/texts/CA_CIV/1941.2.txt) and the ordinary-care duty in [CIV 1929](dependency-sources/CIV-1929.txt). These affect investigation and proposed account treatment; causation and entitlement remain case-dependent agent work.

Local pointers resolve against the selected source. “That section” in CIV 1942.2 depends on the applicable payment route; choosing the closest printed citation would be wrong. A reference to the arbitration title does not become complete by retrieving only its starting definitions. The section-range and chapter references remain broader investigation tasks.

Three broad references were retained outside the specific-statute question: two occurrences of “existing law” in CIV 1942.6 and “other applicable statutory or common law” in CIV 1942(d). They remain open research leads, not model negatives. Newly retrieved statutes also identify language, housing-type, legal-services, judgment-recording, utility-rule and local-law dependencies. `fresh.followup.json` names these next actions explicitly. This first-hop pilot does not close them or complete California mapping.

## Final task wording and preparation check

The direct-expression variant inserted the selected phrase into the question instead of placing it in a separate instruction field. It returned 26/27 on the four-section set, correcting the private-agreement false positive. A further 14 selections from CIV 1942.8 and 1942.9 returned 13/14: a submitted declaration defined by statute was mistaken for a statutory pointer. This exposed the difference between a text pointer and a subject whose meaning is supplied by law.

The current question is **Is “<selected expression>” a pointer to statutory text?** Its native Noul criteria are **It names a statute or a unit of statutory text** and **It names something discussed in the text**. No self-reference exception or list of case-specific exclusions is added. `statutory-pointer.question.json` records this version.

| Subsequent experiment | Agreement | Interpretation |
|---|---:|---|
| Direct expression, earlier statutory wording, four-section set | 26/27 | Development reuse; remaining date-expression false positive. |
| Same direct variant, 14 new selections from two sections | 13/14 | Submitted declaration false positive. |
| Pointer-versus-subject wording on all 61 accumulated examples | 60/61 | All are development material now; declaration still disagreed. |
| Frozen pointer question, 16 new CIV 1950.9 selections | 16/16 | Includes defined actors/documents, time expressions, local pointers, state/federal citations; one additional section, preparing-agent labels. |
| Same pointer question, declaration's governing clause | 1/1 | Targeted preparation correction, not fresh confirmation or a new aggregate score. |

The last check changed only selected context: from the whole section to the exact clause “who has submitted a declaration of COVID-19-related financial distress.” That clause identifies the expression as the object submitted. The adjacent definition citation remains a separate source-backed candidate; it was not removed from research coverage. Code verifies the clause against the original source and verifies that both Section 1179.02 selections remain in the parent set. Original whole-section input and failed response are retained.

This supports a concrete preparation rule: select the governing context needed to judge the expression, and keep adjacent dependencies as separate work. It does not prove a universal shortest-context policy or a model-internal explanation. Context selection is an agent judgment verified by exact spans, not a regex deletion rule. In particular, identifying the declaration's legal meaning still requires following its statutory definition.

The commercial section tests text-pointer recognition separately from residential applicability. Recognizing its references does not bring its commercial rules into Handoff's residential engine. Selected fresh examples are not a complete recall audit of that additional section.

All current observed false-positive patterns have a demonstrated correction on their development examples; the old results are not rewritten into a synthetic perfect score. The current fresh confirmation is 16/16, and the final clause correction has only its one targeted observation. Broad reliability remains unestablished.

## What remains

- Independently review candidate coverage, labels and the final preparation method before wider adoption. This turn used preparing-agent labels.
- Evaluate a broader source mix and the final context-selection method on additional unseen work; other legal authority types are separate tasks.
- Measure complete work against an agent-plus-code baseline. The matched batching experiment demonstrates a request-level improvement, not net benefit after agent preparation and investigation.
- Continue the explicitly recorded substantive dependencies under their planned research work; this pilot has only followed the first hop.

103 tests pass, including exact source/span checks, equivalent batch content, required answer IDs, model-build checks, invalid Noul values, corrected occurrence selection, direct question content and preservation of the adjacent definition references. No production routing or legal rules changed.
