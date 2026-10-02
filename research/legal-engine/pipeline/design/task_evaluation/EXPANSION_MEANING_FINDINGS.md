# Independent adjudication: expansion meaning disagreements

Reviewer `/root/reference_final_audit`, 2026-10-01. **Correct judgments remain exp018 NO, exp032 NO, and exp038 B.** Do not replace those judgments to improve agreement. Preserve all original labels, requests and responses. [Completed corrected input recommendations](EXPANSION_MEANING_CORRECTED_INPUTS.json) contain exact source-backed context, precise occurrence selection, and these judgments; they have not been executed and are development material.

Exposure: this adjudication began with the parent disclosing the three disagreements. I subsequently inspected their frozen expectations and actual serialized requests/responses. It is therefore **response-exposed adjudication**, not a new blind labeling round. The earlier 48-case independent review's before-response disclosure remains historically accurate and was not altered.

## exp018: genuinely different business-day meanings

The supplied definition uses the creditor-office business-functions test. The selected occurrence in the official commentary expressly uses the calendar-day test excluding Sundays and enumerated federal holidays. The tests can classify the same date differently: an ordinary Saturday on which a creditor is closed still counts under the latter test. Conversely, merely being open does not override the latter's excluded holidays. Shared vocabulary and overlapping dates do not establish semantic identity.

The full operative 12 CFR 1026.2(a)(6), inspected immediately above the captured commentary, explicitly introduces the alternate definition with “However.” The commentary's final July 3 example confirms that observed closure is not the calendar test. **NO is a meaning judgment, not just a conclusion that a definition from another provision lacks legal force.** The v2 permission to recognize a meaning despite denied applicability does not turn different definitions into the same meaning. [Primary regulation and official interpretation](https://www.consumerfinance.gov/rules-policy/regulations/1026/2/).

The actual response gave Noul `0.8`, diagnostic YES. The original use passage already spells out the alternate meaning; this is a supported judgment disagreement, not a missing-definition excuse. The corrected recommendation additionally supplies the complete operative two-branch definition as `context` so the comparison no longer relies on the clipped candidate's position. It retains the original narrow candidate meaning and selected occurrence. The completed answer is still **NO**.

## exp032: recover the Washington definition before attributing the failure

The Oregon candidate is the special branch of ORS 90.100(14): when the person rents only the site/moorage rather than the manufactured dwelling, vehicle or floating home, the term denotes the rented space, not the home. It is not Oregon's preceding general structure definition. Replacing it with that preceding sentence would change the tested candidate and must not be described as correcting the same judgment.

The Washington use is RCW 59.18.085(1)'s prohibition on renting a condemned or unlawful dwelling unit. The original payload did not include RCW 59.18.030(10), even though the complete saved Washington source contains it. I recovered that exact definition: the chapter uses the term for a residential structure or part of a structure, expressly including mobile homes. The official live page contains both until-2027 and future versions; I checked the **effective-until-January-1-2027** text rather than relying on the search/page title's future-version label. [Primary Washington definition](https://app.leg.wa.gov/RCW/default.aspx?cite=59.18.030).

**NO** follows from the two meanings' referents, not merely Oregon-versus-Washington jurisdiction. The general Washington structure sense is different from the supplied Oregon separately rented-site sense. Condemnation is not a fact proving that the tenant rented a site without renting a home. Actual same-sense uses across jurisdictions can still be YES under this contract.

The actual response gave Noul `0.56`, diagnostic YES. Preserve the disagreement, but do not call it a clean isolated model-judgment failure: preparation omitted the governing definition needed to make this legal use's exact sense secure. The ordinary phrase suggests a structure, but suggestion is weaker than completed legal preparation. The corrected input adds the exact Washington definition as `context`, with file hash and offsets, and retains the candidate and original use. That completed prepared comparison is **NO**. A later evaluation must report whether that repaired input succeeds; this review supplies no such observed result.

## exp038: explicit exclusion does not reverse the term's meaning

The complete commentary identifies live representative/agent assistance, excludes automated-only means, and retains transactions combining live assistance with automation. The selected occurrence is the grammatical subject of the negative exclusion sentence. Its meaning is **B**, the live representative or agent, not **A**, the automated means being excluded. The candidates are distinct here; NONE is unnecessary because B fits. [Primary official interpretation of 1026.10(e), comment 3](https://www.consumerfinance.gov/rules-policy/regulations/1026/10/).

The actual Choice response selected A with probabilities `{A:0.97,B:0.02,NONE:0.01}`. A is inconsistent with the supplied source and the designated term. Neither exclusion nor the presence of the words “automated means” within the selection makes that object the meaning of the subject. This remains a consequential judgment disagreement: using A downstream could incorrectly classify automated-only payment service as representative assistance for a fee exception.

There is nevertheless a fixable interface weakness. The instruction asks for the meaning of the whole `use_expression`, while the preparation contract intends the selected occurrence of `term` within that locating expression. The original long anchor contains both the target and its excluded alternative. I do not infer from this alone that the wording caused the response, or that A becomes legally defensible. The corrected exact unique anchor is `A customer service representative`; the complete passage and all alternatives remain unchanged. The completed answer remains **B**. This preserves the negative-context challenge rather than deleting the exclusion or rewriting it as a positive paraphrase.

## Concrete contract and preparation corrections

Use `use_expression` only to locate one occurrence; explicitly ask about the **selected occurrence of the term within use_expression**, not the meaning of an entire sentence or clause. Suggested binary instruction: “Does the selected occurrence of the term within use_expression convey the meaning given by definition_passage?” Suggested Choice instruction: “Which candidate meaning fits the selected occurrence of the term within use_expression?” Preserve the distinction between semantic meaning and legal applicability. Clarify that common labels, subject matter or some shared instances do not by themselves establish the same meaning.

Code should continue verifying a unique anchor and one target-term occurrence. The agent must recover governing definition/context where it determines a use's sense. These are preparation and question-design recommendations, not proof of a reliable model correction. A native criteria comparison may clarify semantic identity, but the report does not assume one will work. Repaired repeats are development diagnostics; validate any selected correction on fresh material covering alternate-calendar meanings, structure versus site, different-jurisdiction same-sense positives, and exclusion sentences with minimal and longer anchors. Do not replace the original disagreements with corrected-run scores.

## Verification and evidence binding

All original selected spans for these cases matched their frozen source-file hashes and character ranges. Both added context spans are exact substrings of those already captured primary-source files. Every corrected occurrence anchor is unique and contains its term exactly once. Original frozen case/contract/review and run artifacts were read only; no original or historical artifact was edited.

| Artifact | SHA256 |
|---|---|
| bundles/expansion-96-v2/cases.json | `16eb5c0437e620460df20c4f9f1c2cf14f18ef2a0d9ef52587ac3586ca821057` |
| bundles/expansion-96-v2/contracts.json | `93b2ad6fbb6b4ba2438960c8f15527ad2906374f8bc6eee6f51ba6577d7cd86f` |
| bundles/expansion-96-v2/review.json | `859ad10feff5f26a376668cdf71423750426e6c1ae9465baa0b02fc9df46b195` |
| runs/expansion-96-v2/results.json | `d2b9e8520c441f0a77fb11d1702f29201f772f0ff2b6f3b4c2317df17a38b388` |
| EXPANSION_MEANING_CORRECTED_INPUTS.json | `1e46bdbc27a8c8fae3143ca7e5fd0f13f43077e5e503bea49cc6e87d0c2505cd` |

The corrected-input artifact contains the precise original source identities, offsets, complete added text, proposed instructions, and final judgments. It is a review recommendation artifact rather than a frozen executable bundle. No inference was performed during this adjudication.

## Proposed v3 question review

After completing the source judgments above, I inspected `configurations/proposed-v3.json` at SHA256 `22bf043cce6ac92f1cbfe72a09cd2e34713c4a1bee9b2c0575a22a0b3a8d2a87`. Its actual meaning questions are “Does the term have the defined meaning in the selected use expression?” and “What does the term mean in the selected use expression?” Both resolve the term-versus-whole-expression weakness without changing the substantive meaning task; I accept them for the next development comparison. With the exact prepared changes specified above, expectations remain **NO / NO / B**. This does not establish model performance.

The full v3 configuration also changes the deadline question and its true criterion. Those changes are outside this targeted meaning review; this acceptance must not be cited as independent approval of the complete v3 configuration. The full expansion v3 case file is owned by the parent/author and was not modified here.
