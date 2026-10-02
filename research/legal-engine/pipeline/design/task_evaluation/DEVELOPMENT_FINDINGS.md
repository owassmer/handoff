# Independent development findings — baseline 48

Reviewed the preserved baseline requests, transport evidence, raw responses and evaluation rows for d024 and d029, then reread the selected regulation and the CFPB official interpretation. This review occurred **after response exposure**. I still have not read author labels. The original pre-response independent labels and hashes remain untouched.

## Conclusion

The two disagreements reveal resolved source/contract findings: d024 requires a YES expectation under the agreed narrowing relation, while d029 remains NO for modification of the stated timing rule. Corrected versions still need validation; neither baseline result establishes an intrinsic model failure. Preserve baseline 46/48 diagnostic agreement and both original NO labels as historical evidence. Do not revise the old result to 48/48 or treat revised-case success as fresh held-out validation. My original acceptance of d024 missed a real overlap between the YES and NO conventions.

## d024: limiting investigation scope versus satisfying the duty

The selected sentence still combines prompt investigation with determining an error within ten business days. The candidate specifies conditional sufficiency of the institution's own-record review. Baseline Jev returned 0.71 YES against the original NO expectation. The request's YES criterion includes narrowing a requirement; its NO criterion includes a way of satisfying an unchanged requirement. Those categories can overlap here.

Official commentary treats own-record review as sufficient in the specified situation while still requiring relevant account information and a context-dependent investigation. This supports distinguishing the existence of a duty from the extent of work sufficient to discharge it. It does not support treating the candidate as permission to do no investigation. [CFPB official interpretation, 11(c)(4)-2 and -5](https://www.consumerfinance.gov/rules-policy/regulations/1005/Interp-11/).

The initial NO rationale was defensible only for a different, more narrowly selected proposition: the duty to investigate remains, and the candidate supplies a compliance standard. YES is defensible under the broader phrase “narrows the requirement” if it includes limiting the required investigation's extent. The single probability does not reveal which reading the model used. Therefore classify the baseline as **expectation/contract ambiguity plus insufficiently atomic selection**, not an established intrinsic judgment error. The final adjudication below resolves it under the agreed broader task.

### Completed relation adjudication

The agreed capability expressly includes narrowing, not just complete exemption. Under that scope, the correct revised expectation is **YES** for the investigation-duty target. The candidate limits the investigation's necessary extent in its specified circumstances; satisfying the remaining duty is compatible with narrowing its required scope. Treating every provision using satisfaction language as NO was an overbroad rule in my original expectation. This is an **independent expectation defect**, exposed alongside a compound target, rather than a demonstrated model error. Do not retroactively replace the preserved baseline gold or erase the original disagreement.

Use the exact atomic target `A financial institution shall investigate promptly`, with the complete source paragraph as context. Keep candidate (c)(4), including its section1005.14 carveout and both third-party conditions. Add the relevant official commentary as context for interpreting investigation extent. Expected YES means a conditional scope limitation on the investigation duty; it does not mean permission to omit investigation, ignore relevant records, or miss a determination deadline.

Recommended general question: “Does the candidate excuse or reduce what is required by the selected duty in some circumstances?” YES includes removing a duty, excluding circumstances or reducing its required extent. NO includes an additional duty, remedy, or another compliance option that does not reduce the required substance or extent. Evaluate the actual legal effect, not whether the source happens to use the word satisfies. Keep alternatives that expressly excuse the original duty positive. Recheck other exception cases, including electronic delivery, against this distinction instead of carrying their old labels automatically.

This preserves the agreed task's scope. My initially suggested performance-only question would have changed that scope and is **not the adopted correction**. A separate question about whether all investigation is excused would legitimately be NO, but is a different relation and cannot stand in for this narrowing capability.

## d029: temporal rule versus resulting calendar date

The selected reporting rule is three business days after completion of investigation. The candidate substitutes twenty for ten business days for a different investigation period; it does not replace the reporting interval or the event from which that interval runs. The statutory distinction supports the original NO expectation for a direct rule-modification question. [CFPB regulation, §1005.11(c)(1) and (3)(i)](https://www.consumerfinance.gov/rules-policy/regulations/1005/11/).

But the wording “change the deadline” and “modifies when ... due” also permits a causal reading: an investigation that actually finishes later leads to a later reporting date under the unchanged rule. The candidate does not necessarily make it finish later; it permits additional time. Baseline 0.51 YES is a marginal diagnostic outcome and gives no explanation. Classify the observed disagreement as **ambiguous task wording**, not proof that the model failed to distinguish the numerical periods.

Recommended question: “Does the candidate modify the stated timing rule for the selected requirement?” Define YES as changing that requirement's duration, triggering event or applicable time-computation rule. Define NO to include a change to another task's allowed duration that can shift the factual occurrence of an unchanged trigger. Retain holiday adjustments, tolling, service additions and genuine trigger replacement as positive branches. Keep the selected three-day reporting sentence and current context. Expected NO remains unchanged for this clarified relation.

Do not hard-code numbers or this case into instructions. Test fresh cases involving unchanged dependent triggers, true trigger replacement, other-duty extensions and direct computation adjustments. Exact date propagation remains code work after agent-established dependencies.

## Corrective evaluation sequence

Keep the baseline bundle, original independent review, requests, results and evaluation immutable. Create revised case/configuration versions, state which factors changed, and independently establish labels before their new responses. The two observed cases are development cases permanently. First verify that the focused contracts retain the full promised semantic branches; then rerun affected development cases and validate on fresh material. Completing these source and contract findings does not itself establish Jev reliability.

Do not optimize exclusively to obtain NO on these two rows. A performance-only question would miss the material restriction on duty extent and is rejected here; a narrow duration question might miss a changed trigger or holiday rule. Preserve those branches in the challenge matrix and the completing agent workflow.

## Matched plain configuration

Read configurations/PLAN.md and compared contracts with configurations/plain.json. The only per-task differences remove optional binary criteria for definition, exception, deadline and support; same-sense and Choice remain unchanged. This is a legitimate controlled development comparison of configuration, with no need to duplicate unchanged tasks.

However, d024 and d029 are now known contract-boundary challenges. A plain-versus-criteria agreement table must retain their investigated ambiguity and cannot use either result as automatic proof of the preferred semantic interpretation. Prefer completing the clarified contract first, then comparing concise variants on the same prepared meaning. If running the historical variant to investigate the original ambiguity, label it an exploratory diagnostic comparison and retain the open interpretation finding in its evaluation.

I have now inspected baseline responses. A newly authored plain-configuration review cannot truthfully assert `model_responses_seen:false`. The original independent expectations genuinely predate responses and can be reused by exact hash, with a new configuration-review record disclosing later response exposure. The current freeze gate requires false exposure on the review; do not satisfy it by mislabeling this later review. Either obtain a genuinely unexposed reviewer for new labels, or explicitly support reuse of an immutable pre-response expectation artifact plus a separate transparent configuration review. No historical exposure metadata should be edited.

## Evidence identities

- `development.independent_review.json`: `b90fb41e21264c84c74b68c945ecd97944d1bc13a5a206dfb1fae167c2568a0b`.
- `configurations/plain.json`: `ec7e1b868f0f2c60adfc804223e78ceb1e0dfc0bedb0dcd39c07cea36d9df19e`.
- `runs/development-48-v1/results.json`: `5ce124c06fe0429550dbbc1bed8c01bd3b14e28a82cac3cb14fa280aa841786c`.
- `runs/development-48-v1/evaluation.json`: `9ec9223e781215a5fd25d7203dbc6f0b1751a892e3ec4f4f5d4640603fb92190`.
- `contracts.json`: `2de55d706a2e91904fa67deaf26ad4889470038119cb67828f38d4ea6de8a208`.

## Saved official source recovery

Saved the official CFPB commentary web-tool capture in `independent_sources/CFPB_1005_11_commentary.web.json`, SHA-256 `c7391efd7596351ea1ccfbeae52c98cafa8706c18f714d6fb0fcef58608cdd90`. Verified the capture contains comments 11(c)(4)-2 and -5, including scope and relevant-record qualifications. This is a retained web-tool primary-page capture, not a claim of an independently downloaded original HTML file.

## Proposed v2 configuration review

Reviewed `configurations/proposed-v2.json` independently against the resolved source relations. **Accept the revised conventions for corrected development testing.** Exception criteria now include reduced required scope while distinguishing an added option that leaves that scope unchanged; this preserves the agreed narrowing capability and supports the source-adjudicated YES for the corrected d024 target. Deadline instructions explicitly ask about the stated timing rule and distinguish an unchanged trigger occurring later; this supports NO for d029 without excluding true trigger, tolling or holiday modifications. The per-task changes are confined to these relation definitions.

This accepts the source-grounded contract clarification, not a predicted model result. Corrected case preparation and all affected expectations require a separate reviewer who has not seen responses, as the parent proposes. I cannot provide that blindness after the present investigation. Historical expectations and results remain immutable. Reassess all affected cases, especially compliance alternatives, rather than changing only the failed row.

Proposed v2 configuration SHA-256: `93b2ad6fbb6b4ba2438960c8f15527ad2906374f8bc6eee6f51ba6577d7cd86f`.

## Corrected v2 and matched plain runs: d032 and d008

Inspected preserved v2 d032 (0.60 YES), matched plain d032 (0.52 YES), and d008 with criteria (0.40 YES/diagnostic NO) versus plain (0.75 YES). These are development observations, not evidence for changing a threshold. Optional criteria helped distinguish a reported argument from an adopted definition in this one matched d008 example; one observation does not establish a general benefit. Both original versions remain preserved.

**d032 source adjudication remains NO.** The tenant's section1965(a)(1) request condition runs eighteen days from vacating. Subdivision(e)(1) supplies damages and surrender-related timing, including references to tender/pickup conditions; it does not amend that tenant-request interval or trigger. Subdivisions(e)(2)/(3) concern bad-faith awards and fee/cost remedies. Their existence does not change the selected request clock. This follows the saved full CIV1965 text, not the model response.

The supplied candidate aggregates several remedies, and context contains other actors' clocks. This does not make the eighteen-day proposition legally ambiguous, but it is avoidable preparation complexity for a focused relation. We cannot infer the model's internal cause from the returned probability. Record an observed task disagreement with a preparation refinement to test, rather than asserting that the model intrinsically cannot reason about deadlines or that a smaller threshold would solve the task.

Recommended faithful preparation:

- Requirement: exact tenant-request clause through `the surrender of the personal` + source newline + `property`, retaining actor, eighteen-day period and vacating trigger. Omit mailing-address/description detail from the selected object while preserving full source context if needed.
- Candidate: retain the subdivision(e) liability lead-in and complete(e)(1). Do not strip the governing wrongful-retention condition or the tender/pickup cross-references.
- Context: retain the surrender-duty lead-in and the referenced(a)(3)/(4) when necessary to interpret(e)(1). Keep source spans exact. Context omitted from the semantic request must remain available in the source-selection record.
- Selected-object placement: a simple question such as “Does the candidate change this timing rule?” followed directly by the exact selected tenant-request clause makes the referent explicit. Structured native instructions are justified if they put that object beside the question. This is a configuration experiment, not a new legal meaning or a prompt containing the expected answer.
- Keep(e)(2)/(3) in the agent's source/dependency inventory and review them as separate remedies. If evaluating their relation to the request clock, create separate atomic candidates and preserve their negative relations; do not treat their omission from one request as a finding that they are legally irrelevant.

Expected NO is unchanged for the revised selected rule and(e)(1) relation. Independently review revised spans and configuration before dispatch. Change one factor at a time where practical (candidate narrowing versus selected-object placement), disclose combined changes otherwise, and retain results for all attempts. Fresh validation must include both actual temporal modifiers and cross-actor remedy clocks. A successful rerun of d032 would remain development evidence.

Read the source requirement and remedies from the retained [CIV1965 capture](../coverage_tracking/fresh_research/sources/CIV_1965.txt). The overall capability still must account for its operative clocks and remedy dependencies through agent preparation and focused judgments.
