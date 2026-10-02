# Independent development findings — baseline 48

Reviewed the preserved baseline requests, transport evidence, raw responses and evaluation rows for d024 and d029, then reread the selected regulation and the CFPB official interpretation. This review occurred **after response exposure**. I still have not read author labels. The original pre-response independent labels and hashes remain untouched.

## Conclusion

The two disagreements reveal defects in preparation/contract precision that must be resolved before attributing them to Jev. Preserve baseline 46/48 diagnostic agreement and both original NO labels as historical evidence. Do not revise the old result to 48/48 or treat revised-case success as fresh held-out validation. My original acceptance of d024 missed a real overlap between the YES and NO conventions.

## d024: limiting investigation scope versus satisfying the duty

The selected sentence still combines prompt investigation with determining an error within ten business days. The candidate specifies conditional sufficiency of the institution's own-record review. Baseline Jev returned 0.71 YES against the original NO expectation. The request's YES criterion includes narrowing a requirement; its NO criterion includes a way of satisfying an unchanged requirement. Those categories can overlap here.

Official commentary treats own-record review as sufficient in the specified situation while still requiring relevant account information and a context-dependent investigation. This supports distinguishing the existence of a duty from the extent of work sufficient to discharge it. It does not support treating the candidate as permission to do no investigation. [CFPB official interpretation, 11(c)(4)-2 and -5](https://www.consumerfinance.gov/rules-policy/regulations/1005/Interp-11/).

The initial NO rationale is defensible only for a precisely selected proposition: the duty to investigate remains, and the candidate supplies a compliance standard. YES is defensible under the broader phrase “narrows the requirement” if it includes limiting the required investigation's extent. The single probability does not reveal which reading the model used. Therefore classify this as **expectation/contract ambiguity plus insufficiently atomic selection**, not an established intrinsic judgment error.

Required correction:

1. Select the exact source clause `A financial institution shall investigate promptly` as the occurrence being judged, retaining the complete paragraph as context. Do not conflate investigation performance with its determination deadline.
2. State the intended relation explicitly. Recommended question: “Does the candidate excuse performance of the selected duty in some circumstances?” Criteria can distinguish exclusion/exemption from a provision stating what conduct counts as satisfying that duty. Under that focused relation, expected NO remains source-supported.
3. Do not lose the scope issue by designing it away. Record a separate supported proposition: under the candidate's stated conditions, own-record review is sufficient to satisfy investigation requirements. An atomic support task can assess that proposition; the agent must also retain the commentary's qualifications. This preserves useful operating information without forcing performance exemption and scope specification into one ambiguous bit.
4. If the program wants a broader exception relation that includes reduced extent, explicitly adopt that broader convention and relabel a **new version** from source reasoning. The original case cannot be retroactively treated as an unambiguous positive or negative under both conventions.

The new performance-focused relation must be checked against all existing exception cases, especially scope exclusions and payment-condition exemptions. It does not automatically settle every narrowing relation promised by the broader capability; agent synthesis or a separate focused relation must complete those branches.

## d029: temporal rule versus resulting calendar date

The selected reporting rule is three business days after completion of investigation. The candidate substitutes twenty for ten business days for a different investigation period; it does not replace the reporting interval or the event from which that interval runs. The statutory distinction supports the original NO expectation for a direct rule-modification question. [CFPB regulation, §1005.11(c)(1) and (3)(i)](https://www.consumerfinance.gov/rules-policy/regulations/1005/11/).

But the wording “change the deadline” and “modifies when ... due” also permits a causal reading: an investigation that actually finishes later leads to a later reporting date under the unchanged rule. The candidate does not necessarily make it finish later; it permits additional time. Baseline 0.51 YES is a marginal diagnostic outcome and gives no explanation. Classify the observed disagreement as **ambiguous task wording**, not proof that the model failed to distinguish the numerical periods.

Recommended question: “Does the candidate modify the stated timing rule for the selected requirement?” Define YES as changing that requirement's duration, triggering event or applicable time-computation rule. Define NO to include a change to another task's allowed duration that can shift the factual occurrence of an unchanged trigger. Retain holiday adjustments, tolling, service additions and genuine trigger replacement as positive branches. Keep the selected three-day reporting sentence and current context. Expected NO remains unchanged for this clarified relation.

Do not hard-code numbers or this case into instructions. Test fresh cases involving unchanged dependent triggers, true trigger replacement, other-duty extensions and direct computation adjustments. Exact date propagation remains code work after agent-established dependencies.

## Corrective evaluation sequence

Keep the baseline bundle, original independent review, requests, results and evaluation immutable. Create revised case/configuration versions, state which factors changed, and independently establish labels before their new responses. The two observed cases are development cases permanently. First verify that the focused contracts retain the full promised semantic branches; then rerun affected development cases and validate on fresh material. Completing these source and contract findings does not itself establish Jev reliability.

Do not optimize exclusively to obtain NO on these two rows. A tighter performance question might miss a material restriction on duty extent; a narrow duration question might miss a changed trigger or holiday rule. Preserve those branches in the challenge matrix and the completing agent workflow.

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
