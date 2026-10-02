> Superseded by the founder correction: do not replace these capabilities with agent-completed judgments before evaluating decomposition into focused Jev jobs. Preserve the source findings and distinct relations below as inputs to that design. The agent-replacement recommendation is withdrawn.

# Complete a focused legal relation

Version: agent-relations-1. This method is under development validation, not accepted yet.

The input is one source-bound case in the existing focused-task format. The output is a completed relation record. Do not inspect expected labels or model answers while producing an independently evaluated record.

1. Read the selected evidence and the complete governing unit. Identify the exact term occurrence or actor/action. Separate the target from neighboring duties and conditions. Retain those other effects as connected records when they materially qualify the answer.
2. Retrieve any necessary definition, incorporated provision, qualification or authoritative interpretation. Capture it with an exact source selection. Do not treat missing text as NO or finish with a deferral. Resolve interpretation from the sources before completing the record.
3. For meaning, state the candidate definition and the meaning governing this occurrence. Compare their actual inclusion/exclusion tests. Record material differences even when both meanings share an ordinary-language category. Decide same operative meaning separately from legal applicability.
4. For an exception, state the base obligation and its already-stated conditions. State the candidate conditions and identify whether the candidate removes the duty, reduces its required scope, adds a means of unchanged satisfaction, supplies a distinct branch, adds another duty/remedy, or has no relevant effect. Explain the effect; categories alone do not complete the work.
5. For timing, identify actor, action, duration/unit or qualitative time rule, triggering event and conditions. Determine whether the candidate changes a duration, defines the legal trigger/date, adjusts computation, tolls a clock, creates a waiver/alternative branch, concerns a different clock, or has no temporal effect. Distinguish a changed legal rule from a later actual event governed by the same rule. Keep effective credit dates separate from posting dates. Record coexisting rules separately.
6. Write each material relation as an atomic proposition, its conditions, exact supporting/qualifying evidence and the permitted downstream conclusion. Consider the strongest plausible contrary reading and explain why the evidence supports or defeats it. Preserve legitimate alternative branches; do not force a single category when several effects coexist.
7. Complete every dependency needed for these propositions. Record the resolved question and source evidence. Do not assert factual conditions of a live tenancy unless that is the supplied question and evidence supports them. Missing live-case facts may be named as conditions; missing legal context must be recovered.
8. Submit the record for independent source review. The reviewer checks meaning, missing effects, preparation and evidence, with expected conclusions established independently before comparing answers where this is an evaluation. Correct material findings and recheck the changed record. Code validates identity, structure, exact source bytes and the binding of acceptance to the completed record; it does not certify legal truth.

Jev atomic claim support may corroborate a completed proposition and a meaningful counterclaim. Save those outputs separately. A rejected claim does not prove its negation. This optional assistance does not replace the agent's completed relation or independently reviewed evidence.

No date or amount is calculated by this method. Once interpretation and case facts are established, code can compute the result. Goals6/7 own complete-process comparison and routine integration.

## Output fields

Record: `case_id`, `task`, `input_sha256` (canonical SHA256 of the entire prepared case), `method_version:"agent-relations-1"`, `analysis`, `relations`, `dependencies`, `contrary_reading`, `conclusion`, `downstream_use`, `unresolved:[]`.

Analysis for candidate_term_use: `candidate_meaning`, `use_meaning`, `material_differences` (list), `same_meaning` (boolean), `applicability` (explanation separate from sense).

Analysis for exception_to_requirement: `base_obligation`, `base_conditions` (list), `candidate_conditions` (list).

Analysis for changes_deadline: `actor`, `action`, `duration`, `unit`, `trigger`, `conditions` (list). Use a faithful qualitative duration/unit if the source is qualitative; do not fabricate a number.

Relations: nonempty list of `{id,kind,proposition,conditions:[],consequence,evidence:[]}`. Kinds: `same_meaning`, `different_meaning`, `removes_duty`, `reduces_scope`, `unchanged_satisfaction`, `independent_duty`, `independent_remedy`, `no_relation`, `duration_change`, `legal_trigger_definition`, `computation_adjustment`, `tolling`, `waiver_or_alternative_branch`, `other_clock`, `no_temporal_effect`.

Each evidence item is `{path,sha256,start,end,quote,role}` using exact UTF8-decoded character offsets; role is `supports`, `qualifies`, or `contrary_considered`. Source metadata remains bookkeeping. Each resolved dependency is `{question,resolution,evidence:[]}`. An empty dependency list is allowed only when the selected source context already completes the judgment.

`contrary_reading` is `{reading,resolution,evidence:[]}`. Name a material alternative reading, not a fabricated objection. Record multiple relations when necessary—for emergency entry, default notice, emergency branch and post-entry notice remain distinguishable.

The independent review supplies `reviewer`, `method_sha256`, `cases_sha256`, `records_sha256`, `material_findings:[]`, and `cases:[{id,accepted:true,reason}]`. Approval binds exact method, inputs and outputs. This record is a reusable completed judgment, not authorization for an operating action.
