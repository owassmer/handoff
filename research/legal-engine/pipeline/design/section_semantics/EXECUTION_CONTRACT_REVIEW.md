# Independent execution-contract review

**Changes required before implementation/inference acceptance.** Read both next preparations, concrete native operation proposals and YES licenses, typed interfaces, adaptation note, current consumer/requirement selection, and relevant captured primary sections. No inference was run and no preparation/runtime file was edited. Diagnostic originals remain unchanged. The interfaces improve on generic relationship labels, but several mappings presently omit legal effects or necessary machine inputs.

## Material findings

### E1 — Repeat termination loses common notice content and incorrectly inherits cure

Affected jobs: `or_entry.j451`, `or_entry.j452`, `or_entry.j453`.

j452 blocks termination for curable+timely cure without excluding qualifying repeat; j451 excludes the entire ordinary cause-notice bundle in that repeat branch, although not every notice-content requirement disappears.

Required correction: Judge and apply repeat exclusion to cure blocker; separate always-required acts/omissions content from ordinary/repeat timing and conditional cure content. Do not replace this with two competing whole notices.

Verification case: Qualifying repeat with same noticed violation within six months and attempted cure; repeat notice must still identify violation and keep its proper date.

### E2 — Specified repair times attached unconditionally

Affected jobs: `or_entry.j095`, `or_entry.j376`, `or_entry.j377`.

j095 attaches specified allowable-time action to the default reasonable-time record; j376 attaches it to repair entry without a when guard.

Required correction: Make specified-times and no-specified-times branches explicit, scoped to same repair authorization. Remove unconditional attachment to default branch; preserve the accepted choice of branch and its case classification.

Verification case: Written repair request contains no allowable times: consumer should require reasonable timing, not nonexistent specified hours.

### E3 — Payment-condition waiver does not zero monetary assessment

Affected jobs: `ca_return.j069`, `ca_return.j207`, `ca_return.j208`.

Ordinary return sets storage_paid true while storage filter/rate operations remain available. Pre-sale has a component waiver; ordinary return lacks equivalent monetary effect.

Required correction: License both removal/satisfaction of the payment prerequisite and zero storage assessment/prohibition on requiring storage under the qualifying waiver. Preserve actual payment facts; separate effective prerequisite satisfaction from factual payment. Define waiver precedence over rates/filtering.

Verification case: Qualifying two-day return, actual storage ledger100: release prerequisite satisfied by waiver and assessed storage0, not paid100 or a later positive charge.

### E4 — Any-person duplicate rule can erase the same claimants unpaid bill

Affected jobs: `ca_return.j201`, `ca_return.j202`, `ca_return.j203`.

parameters already_charged_to:any_person does not distinguish another person from the present claimant, or charged from paid.

Required correction: Track stable incurred-cost identity, assessment identity, charged person and paid/unpaid state separately. Apply same-cost multiple-person restriction without erasing an existing unpaid assessment to this claimant; disallow duplicate addition to ledger separately.

Verification case: An unpaid storage invoice already issued to the reclaiming former tenant remains part of the unpaid storage base; an identical incurred cost charged to another person must not also be allocated here.

### E5 — Method selectors omit required logical and applicability links

Affected jobs: `or_entry.j335`, `or_entry.j378`, `or_entry.j379`, `or_entry.j380`, `or_entry.j421`.

Selecting records.actual_notice_methods or records.written_notice_methods does not inherently select separate conditions.* trees, email_notice_conditions fields, or classified sender/recipient/service branch. Terms such as compliant addendum still require assembled legal content.

Required correction: Enumerate typed method alternatives with all conjunctive components and required field/condition selectors. Bind email addendum requirements, dual-service termination branch, written-method supplements, permitted locations and service timing to each applicable method. Keep actual-notice service date distinct from written-notice compliance-period extension.

Verification case: Termination email alone cannot satisfy mail+email branch; a supplement cannot replace required service; ordinary first-class and mail+attachment must not receive indiscriminately identical clock treatment.

### E6 — Scope declarations lack an executable record-membership contract

Affected jobs: `or_entry.j476`, `or_entry.j482`, `or_entry.j483`, `ca_return.j149`, `ca_return.j163`, `ca_return.j181`.

unit_scope uses all_primary_section_records and exceptions; present consumer does not execute these directives. Blocking one root does not suppress independently emitted waiver/postnotice/immunity records or define exceptions to scope.

Required correction: Bind source/unit membership and independently sourced exceptions to exact affected record IDs; execute inherited scope before every branch/output, with unknown preserved. Specify priority of express scope exceptions such as the retained immunity record.

Verification case: An excluded Oregon facility must not leak an OR90.322 standalone waiver or post-entry duty while entry permission is blocked; independent other-section obligations remain separately scoped.

### E7 — Whole-record selection requires complete field sets

Root corrected requirements.select so prefix-only selections remain unresolved. Proposals still supply record prefixes without required field contracts.

Required correction: Supply independently reviewed target_required_fields and per-item required_fields including necessary conditions, relationships and exact content/timing/method fields. A nonempty prefix is not completeness; rejected/missing fields must remain blockers.

Verification case: Actor-only notice record must not yield resolved complete notice.

### E8 — Conditional expiration lacks temporal state-transition semantics

Affected jobs: `or_entry.j107`.

Proposal says permission ends at expiry unless continuation holds, but does not specify evaluation time, later completion/loss of reasonable effort, or whether expired authority can revive.

Required correction: Bind request instance, evaluation instant and event history. Preserve until-repairs-completed limit; classify in-progress and reasonable-effort at relevant times. Establish source-grounded transition rules before implementation; do not latch one day-seven answer forever or silently revive an expired request.

Verification case: Repairs underway at day7 then completed day8: no day9 permission based only on day7 continuation.

### E9 — Calendar and money operations lack complete determinate input schemas

Affected jobs: `or_entry.j395`, `or_entry.j396`, `ca_return.j198`, `ca_return.j204`.

Anchor phrases and cost parameters such as storage_term/fair_rental_value remain conceptual; runtime template only licenses satisfied/not-satisfied/insufficient predicates, not timestamp or amount values.

Required correction: Define bound case-event identities, timestamp precision/timezone, service/entry distinction, selected calendar/version, cost currency/rate units/periods/rounding and classified allocation inputs. Supply value-selection/extraction jobs or verified structured business records, with exact licenses. Do not parse accepted prose into numbers or dates.

Verification case: Emergency notice clock anchored to actual entry with mailing service separately assessed; fair rental storage rate has a stated unit and duration before any total.

## Source-grounded qualifications

ORS90.392 retains general cause-notice content, differentiates ordinary/repeat periods, and denies a cure right for the qualifying repeat. ORS90.322(c) differentiates specified and reasonable repair times and limits requested-repair authority through completion/expiry. Review is against the captured2025 edition; the official chapter page flags2026 enactments, so this is not an independent current-law/version closure. [Oregon official chapter90](https://www.oregonlegislature.gov/bills_laws/ors/ors090.html).

CIV1990 separately addresses unpaid tenant costs, another owner's property interest, charging more than one person for the same cost, onsite rate and the two-day no-cost branch. A payment-condition override alone cannot implement these money effects. [Official CIV1990](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1990.).

The proposed low-value `waive_duty` is directionally correct: remove mandatory sale while preserving optional conduct. Keep the underlying unreleased-property, reasonable-belief and chapter-procedure conditions. Choosing sale still invokes the applicable sale notice/proceeds requirements; absence of a sale mandate is not approval of every method of disposition. Preserve the standalone low-value permission and actual election as distinct records.

The cure operations' constraint form is preferable to declaring a missing prerequisite true. The tenant-cure blocker must remain scoped to the corresponding termination route; it must not erase independent damages/injunctions. The new1965 initiated/completed predicates and ANY group address the stated Chapter5-disposition exclusion, but all remaining1965 prerequisites and occupancy exclusion still must be present in the alternate-route record.

## Contract completeness standard

Each operation needs its required legal fields, condition/link dependencies, factual inputs, output effects, unknown/conflict behavior and precedence/composition rule. In particular: waived storage is not a paid invoice; specified time and default time are conditional alternatives; method alternatives may themselves contain AND requirements; waiver of a duty does not prohibit optional performance; inherited scope applies to outputs as well as entry conditions.

A case-classification job may apply already-established legal meaning to new facts. It must receive the complete assembled meaning. Passing an action label or a predicate containing “compliant” without its linked legal requirements makes that job reconstruct the source semantics and violates the consumer contract. Required-field sets are therefore substantive preparation, not merely extra schema metadata.

Root repaired prefix-only selection during this review. I reread the correction: an explicit exact field can resolve, while a prefix without required_fields cannot; absent required fields now block. This is a useful guard, not completion of the actual notice/money/time contracts. The preparations still need reviewed complete field sets and focused Jev licenses for any new relationships/logic.

## Review/implementation gate

Correct the named operation candidates and their answer licenses together; freeze new versions without rewriting diagnostics. Independently review changed scope/conditions and complete field sets. Implement only the typed operations whose inputs and legal effect are settled, with unknown propagation and evidence traces. Run the concrete counterexamples above plus positive counterparts. Demonstrate notices, timing and money outputs from accepted records and bound case facts with raw legal source unavailable to the consumer. No operation is accepted merely because its JSON can be serialized or a relation question returns YES.

Input hashes are retained in EXECUTION_CONTRACT_REVIEW.json. This is review of the proposed execution contracts, not certification of all894 semantic jobs, complete jurisdiction mapping or live operating authority.
