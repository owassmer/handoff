# California pipeline work — updated October 1, 2026

## Current position: J0 complete; J1 next — October 1

The [intake review](J0_INTAKE.md) records the substantive completion basis. CA, CA-OC and CA-HB profiles now contain court/appeal relationships, issue-specific authority rules, applicability facts and their evidence, scope and actual unit-record status. Huntington Beach inherits through Orange County; county applicability remains provision-specific. No rule atoms were changed. Known demonstration facts and missing unit records are explicit; no missing fact narrows jurisdiction research. No customer roster has been supplied.

Next: close J1 instrument registration. Court-authority research for each substantive decision remains J5 work; the court map itself is now filled. Jev redesign/diagnostics are paused. The entries below describe earlier work and do not override this stage position.


## Collection pilot and source reconciliation — September 30, 2026

[Overall plan and to-do list](../../PLAN.md). [Pilot report](../../pipeline/design/agent_jev_code/pilots/ca_collection/REPORT.md): 43 frozen requests over 18 saved sections; one missing-context request returned to the agent before dispatch; 42 answers and 40 frozen-label agreements. Post-run review separates one clear missed title reference from one self-reference question ambiguity. No prompt tuning on the pilot. Source enumeration independently found and recovered four absent sections; California now has 166 registered sections, with all 22 sections of Title 1.6C reconciled to four captured official articles. Original source bodies remain unchanged; substantive rules, currentness, and authority research remain open. Tests: 83 passed.

## OpenRouter development run completed — September 30, 2026

The refreshed environment restored provider access. [The frozen 22-example run](../../pipeline/design/agent_jev_code/REVIEW.md) completed in 2.0068 seconds at $0.001095066 reported cost, with all returned builds matching the pin. Jev agreed with 20/22 reviewed development labels. Both missing-context controls incorrectly returned YES; agent recovery restored the omitted source context, preserving the original misses. This is not held-out reliability, calibrated confidence, or full-process performance. No production routes or legal rules changed. The earlier DNS failure below is historical.

## Atomic-task review and OpenRouter attempt — September 30, 2026

[Two blind development-review passes](../../pipeline/design/agent_jev_code/REVIEW.md) identified and corrected the difference between candidate term matching and establishing technical meaning. Draft 2 now has 22 reviewed examples across five task contracts, including four additional edge cases. The complete regression suite passes 80 tests. A real SDK request through the existing OpenRouter configuration failed DNS resolution before any response; the batch stopped after one attempt, leaving all 22 examples unanswered. No model accuracy or throughput result exists, and no active rules or production routes changed. Reviewed inputs, separate labels, exact request hashes, runner, and failure record are saved for resumption.

## Agent, Jev, and code design — September 30, 2026

The user clarified that the pipeline is agent-led investigation with rapid atomic Jev judgments and code for structured I/O and computation. [The worked flow](../../pipeline/design/agent_jev_code/README.md) now specifies that collaboration against California property-left-behind and document-request examples, with five draft task contracts, 18 development cases, exact source selections, and a runnable input preparer. Expected answers remain separate from model inputs. These are author-labelled development examples, not independent calibration; no new model answers, routing changes, or active legal rules result from this work.

The existing 481/483 score below measures combined routing with existing source-register research context. It is neither standalone Jev accuracy nor initial-discovery validation for California. The existing heading checks do not establish semantic dependencies, and the current Jev triage prompt expressly treats definitions-only sections as NO_DECISION. The worked design addresses this question/coverage mismatch without claiming it has already been solved in production.

California now has an active section register in the general pipeline. The statewide inventory remains open; these files do not represent completed California coverage or runtime legal answers.

## Work completed in this pass

- Imported 162 complete saved section texts across CIV, CCP, BPC, FIN, GOV and MVC, with source links, retrieval headers, hashes and links back to their original captures. This includes 92 sections from the saved hiring-of-real-property chapter and 13 from the abandoned-property chapter. Dedicated section captures take precedence over chapter slices where both exist.
- Verified every imported body against its original source, and every input against the intake manifest's hash. Chapter splitting distinguishes actual headings from bare cross-reference numbers; section 1941's bracketed heading is retained.
- Created an explicit discovery record for all 27 legal functions in the shared chain map. Candidate sources are research leads, not assertions that the function is fully covered.
- Ran matching and cached-only triage: all 162 sections remain in review, 153 without model scores and nine longer than the Jev limit. No California model answers were obtained. No section was excluded.
- Established the CA-HB child layer and a US reference placeholder pointing to the existing federal work. Federal rules have not been migrated or presumed applicable. Parent reuse/currentness review remains necessary before relying on active-layer matching.
- Recovered all 12 sections of Huntington Beach's nuisance chapter and completed its independent first review: 11 sections propose legal branches and one gives a specific reason for no account/work decision. The 56 proposals pass the decision-file checker and quote tests. They remain proposals pending incorporated-law, effective-date and wider authority work; they have not been copied into active rules. See the [review report](../CA-HB/decisions/report_1.md).
- Corrected shared calibration to retain each pooled example's source-register context. The corrected v2 result is 481/483 answered positives retained, with two remaining misses. This is a corrected measurement of the existing routing, not a new routing version or California validation.

## What remains

1. Finish source enumeration: code tables of contents and whole relevant units, regulations, court rules, agency sources, cross-references and session-end amendments. `discovery.json` gives the source families for every function. The instrument checker now explicitly fails an inventory whose discovery status is open.
2. Verify currentness of saved sections against final enacted changes. A retrieval date is not proof of coverage through that date. Historical source versions and effective dates must remain separate from a contemporary demonstration's dates.
3. Complete the Huntington Beach and applicable county/program review, then the other California local layers relevant to the Holland scope. Local publisher pages can have different update states: the code landing page reported incorporation through Ordinance 4349, while the retrieved chapter 5.16 page still displayed Ordinance 4346 as pending incorporation. Do not apply the landing-page cutoff to every retrieved page.
4. The J0 court map is now complete. At J5, review controlling decisions and subsequent treatment for each substantive issue. The preliminary Granberry/current-amendment and Rosenthal transaction questions remain open research. The new profiles intentionally have no invented court-search completion.
5. Repair and independently validate the remaining routing weaknesses; create California positive and negative labels and obtain model answers. The existing low-priority routes still require section review.
6. Review and propose complete legal branches, evaluate them against varied cases, and connect approved results to physical commitments and account actions. No new active rules have been applied in this pass.

## Breakwater application

The [CMFA Special Finance Agency VII audited 2024 financial statements](https://www.cmfa-ca.com/wp-content/uploads/2025/02/CMFA-Special-Finance-Agency-VII-6.30.24-Issued-FS.pdf), note 1, identify the agency's 2021 bond financing of the 400-unit Breakwater property at 16761 Viewpoint Lane. Public ownership/program documents are therefore a concrete applicability dependency. The audit does not establish the particular resident's income restrictions, lease terms or governing regulatory agreement.

Continue using the case for realism. Recover the relevant agreement and program terms, or expressly author a coherent different demonstration setting. Neither route permits treating the historical case as proven unrestricted market-rate housing. Preserve the historical 2023 account separately from any contemporary adaptation.

The operating questions remain: what work is necessary, which commitments and prices are justified, what may be recovered, which evidence and actions protect that recovery, and when correction or settlement is economically appropriate. The source inventory extends beyond this case.

## Reproduction

`build/start_california.py` records the original mechanical intake and refuses to overwrite later research. Do not rerun it to reset decisions. Run normal pipeline commands from `research/legal-engine` for subsequent work. The initial `match` and `triage --cached-only` outputs are reflected in the register; cached-only triage returns nonzero because 153 expected answers are absent. An empty active rule set produces zero matches, not a finding that the sections impose no duties.

Validation: pipeline regression suite 64 passed; original Holland map quote/header checker passed unchanged (271 entries); every California imported body and input hash matched; CA-HB batch checker returned 12/12 decisions and zero errors, with negative self-tests passing. Open-inventory checks intentionally fail for CA and CA-HB. No live model calibration, California case evaluation or runtime integration has been completed.
