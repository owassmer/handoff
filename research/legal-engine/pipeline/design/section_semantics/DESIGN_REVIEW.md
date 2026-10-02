# Independent design challenge

Reviewed OBJECTIVE.txt, PLAN.md and DESIGN.md. **Direction accepted; implement after specifying the concrete contracts below.** The agent-replacement proposal is withdrawn. This review does not revive it: agents discover, prepare, recover context and orchestrate; focused Jev judgments establish semantic outputs; code composes only licensed meaning. No inference was run for this design review.

## Requirements before implementation

### 1. Completeness must have a reviewable unit and denominator

Name the complete operative section/version and incorporated provisions in each work unit. Retain the source occurrence inventory, candidate jobs, unassigned spans and a reason for any omitted or excluded candidate. Compare against independently prepared whole-unit expectations, including negative candidates and easy-to-miss simultaneous effects. Counting only submitted questions rewards omission.

A semantic NO rejects the selected proposition, not the entire passage. A cross-reference, definition dependency or unresolved exception must remain tracked even when one candidate relation is rejected. Discovery completeness cannot be established by a Jev “nothing else matters” gate. Existing coverage records can track these open items; a new coverage framework is unnecessary.

Require a concrete completion check: every expected duty, permission, prohibition, condition, temporal component and consequence is either represented with its relationships or has a reviewed, source-supported exclusion. Candidate generation itself must be evaluated on new sections; feeding an independently completed gold inventory to the preparer would not demonstrate discovery repeatability.

### 2. A job must license exact fields, not a nearby record

For each job define selected occurrences, proposition/alternatives, allowed outputs and the exact fields or edges each answer licenses. Distinguish literal source-span copying from semantic interpretation of that span. Code can preserve the characters “24 hours”; a job must establish that this is a minimum advance-notice interval for the selected actor/action, rather than post-entry notice, a presumption or a remedy.

Bind the accepted field to source version/span, job/configuration version, actual serialized request, validated raw result and decision-policy version. Choice output must map through stable option identities and meanings, not list position. Never promote an entire candidate record from one broad “is this a duty?” answer. A rejected candidate cannot silently promote its alternative unless the frozen contract establishes exhaustive exclusive alternatives and the validated answer actually selects one.

The entry example's numbered items are still descriptions of several judgments each. Before implementation, show at least one full decomposition table: actor, action, object, modality, condition grouping, temporal interval/anchor, and required notice contents, with per-field licenses and dependencies. Some genuinely atomic relations may share one question; do not fragment mechanically into meaningless word checks.

### 3. Conditions are semantic work

A preparer may propose an all/any/not structure, but code must not accept that structure merely because the agent authored it. Focused jobs must establish the condition-to-action links and material logical grouping, including exceptions to exceptions, quantifiers, negation, temporal order and actor-specific qualifiers.

Do not infer a converse: permission in an emergency does not by itself prove prohibition in every non-emergency. Do not convert a presumption into a fixed deadline or a necessary condition into a sufficient one. Treat “only,” “unless,” “except,” and scope phrases as relationships to establish with evidence, not keyword parsing rules. The default-entry, emergency-entry and absent-tenant post-entry duties remain distinct conditional records; simultaneous obligations must survive composition.

Facts and legal conditions stay separate. The downstream case consumer must receive known/unknown/disputed factual values, not silently treat absent facts as false. If applying a legal condition to facts requires another semantic judgment, prepare a focused job using the established legal record and case evidence. That is new work; it is not permission to reread and reconstruct the original statute.

### 4. Semantic relationships can cycle; executable jobs cannot depend circularly

An execution DAG is appropriate. The legal/source graph may contain reciprocal definitions, overlapping exceptions and cross-references. Distinguish these graphs explicitly. First establish source/entity identity and candidate links, recover the relevant passages, then schedule judgments whose evidence is available. Do not reject a legitimate legal cycle or invent a conclusion to break a scheduling cycle.

A dependent question must bind the actual predecessor output used to assemble its request. A stale predecessor, changed definition or recovered source version invalidates affected descendants and composed fields. Independent questions sharing state cannot consume one another's unreturned answers. A runtime dependency may require a new job after retrieval; add it durably without treating the old unanswered branch as NO.

### 5. Preserve uncertainty and conflicts through composition

Specify states for proposed, answered, accepted under evaluated policy, uncertain, failed, not sent, superseded and conditionally inapplicable. Not-applicable needs its establishing predecessor and reason. Preserve distributions and ties; a majority answer alone is not an authorization rule for a consequential charge or deadline.

A composed record must show which fields are established and which remain open. Missing actor, unresolved exception, conflicting sources or an uncertain anchor cannot yield an apparently complete obligation. Do not silently choose the highest-probability conflicting claim. Prepare the source hierarchy, temporal applicability or interpretive conflict as the next focused work and resolve it. Keep both earlier answers and the new resolution so correction does not erase evidence.

The goal requires completed recovery and judgments, not a permanent list of unresolved flags. These states govern execution while work is pending; they do not weaken the final completion bar.

### 6. Resumption and native transport need concrete guarantees

Reuse the existing validated runner, source snapshots, immutable coverage history and transport checks where they fit. Support multiple job IDs per unit, exact expected answer-ID coverage and field-level dependencies. Persist raw responses and costs even when semantic validation fails. A restart must distinguish a completed accepted result, a known failed dispatch and an uncertain in-flight attempt; never infer a semantic negative or secretly replace a prior answer on retry.

Freeze and record model/build, question/criteria, option mapping, evidence selections, serializer and composition policy. Verify actual transmitted bytes. Batch only independent jobs with compatible shared context; compare batched and separate results on the same prepared meanings. Multiple requests in flight are a different optimization. Structured instructions should identify the selected object and relation, not wrap generic questions cosmetically.

### 7. Actual consumer integration must reject old information loss

For triage/route: queue unresolved source components and recovered dependencies from semantic records. No broad relevance or role probability may suppress an unjudged component.

For batch/review assembly: supply identified records, source links and unresolved findings. Reviewers may audit meaning, but the normal next step must not require rebuilding actor/action/condition relations from raw sections because the output omitted them.

For rule assembly and one operating-case consumer: accept a versioned semantic-record input with required-field and dependency checks. Demonstrate ordinary entry, emergency entry and absent-tenant post-entry notice from the same records across changed case facts. The consumer should obtain all applicable duties, timing inputs and notices without re-reading the section. A permission to enter must not suppress the post-entry duty. Money/date computation runs only with complete interpreted inputs.

Document exactly which existing commands/readers change and reject or explicitly segregate legacy broad-score records. An unused parallel store or JSON exporter does not satisfy integration. A useful integration test makes the raw section unavailable to the downstream consumer after production of the semantic records, while retaining source links for audit. Compare its outputs to independent case expectations; instrument tool access rather than merely declaring “no reread.”

### 8. Evaluation must test the connected output

Preserve the historical task experiments and their failures. Freeze new preparation, configurations, field licenses, scheduling, composition and consumer contracts before unseen testing. Independent expectations must include complete components/relations and case outcomes, not only one binary label per section. Independently establish them before responses; disclose prior exposure and source reuse.

Report component correctness, omitted components, relation correctness, conditional/temporal composition, unresolved execution and downstream completion separately. Use section/instrument clusters for whole-output uncertainty; dozens of jobs over one provision are not dozens of independent sections. Include multiple jurisdictions and statutory, regulatory, judicial and administrative families, recovered context, conflicts, overlapping effects and facts that activate different branches. Old unused definition/support selections can contribute atom evidence, but cannot become full-unit coverage by renaming them.

Require meaningful adversarial regressions: one answer attempts to populate unlicensed fields; a dependent job runs before its predecessor; a source revision leaves stale descendants; an omitted post-entry duty creates false completion; an unknown case fact is treated as false; a negated condition loses its scope; a partial batch response is scored as a negative; and a lower-probability but material competing interpretation disappears.

## Bounded implementation sequence

Start with the complete entry-notice work unit and a contrasting definition/temporal unit. Write their exact candidate inventories, job-to-field licenses, dependency schedules and consumer inputs/outputs before building broad machinery. Implement the small shared record/job contract in the existing pipeline, run these end to end, and independently inspect whether every semantic field actually comes from the specified focused judgments. Then expand using the same instructed preparation method to unseen source families and jurisdictions. Do not specialize the schema or prompts around the Oregon wording.

This is a connected multi-job redesign, not a collection of agent-authored final records with Jev as a ceremonial checker. Source selection necessarily proposes alternatives; final semantic promotion must remain attributable to the evaluated Jev jobs and deterministic composition. Any alternative method still requires the evidence and verified implementation specified by the user, rather than being adopted because generic questions were difficult.

## Review scope

No implementation or capability acceptance is granted by this design review. The requirements above sharpen the proposed design without adding a separate platform or framework. They cover the concrete failure modes exposed by prior work while preserving all six requested revisions and the founder's operating objective.

Reviewed input hashes:

- `OBJECTIVE.txt`: `840770453ae7269e9ed7df437a56dc1fe8dce6e6aaf28001b813d0df3a13d704`.
- `PLAN.md`: `a171e6dc34aaf5124687b904c2987652c1ad19c834f25cc5143563357d585f84`.
- `DESIGN.md`: `86db0aa833f6632070814dca2db8a5b7d69afab9885155b49c8e853ff2bf8f6c`.
