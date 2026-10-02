# Huntington Beach batch 1 reviewer report

Reviewed 2026-09-30 by `ca_hb_review`. Report and proposals only; no accepted rule, profile, source or walk was changed.

## Scope and result

Read every word of the 12 saved HBMC 17.10 sections (18,150 section characters), the CA-HB profile, chain decision points, empty CA/US parent rule files, and the saved AB 1418 enactment extract. Also reopened the municipal chapter and enacted bill through the web tool to check the cited source identity. The chapter page identifies sections 17.10.100–17.10.190 as repealed by Ordinance 3398-7/98; they are not silently omitted live sections of this retrieved chapter.

- 12/12 section decisions: **11 new_rule, 1 no_decision**, zero stated, partial or excluded_regime.
- **56 proposed rules:** 49 critical, 6 major, 1 minor.
- The one no_decision is 17.10.080: a discretionary City graffiti reward, one reward per incident, does not determine a tenancy account or required turnover work. The decision records that actual reason, rather than labeling the entire nuisance chapter irrelevant.
- All sections were unscored because no Jev record exists. There are no low-scored sections to report and no negative Jev judgments to rely on.
- No accepted CA, CA-HB or US atoms existed when reviewed. `show 'CA:*'` returned no such rule; direct inspection confirmed empty atom arrays. There is consequently no existing atom to call complete, amend or cite as covering this material. Older Holland map entries are not silently treated as accepted pipeline atoms.

**This is complete section review of one retrieved chapter, not completed Huntington Beach discovery, dependency resolution, adjudication, historical reconstruction or California coverage.** The surrounding source inventory remains open.

## Operating consequences

The nuisance chapter connects physical work to financial protection: identify required abatement, distinguish necessary repair from optional scope, preserve an owner's opportunity to challenge an order, and avoid notice failures and City-cost recovery. It does not itself turn every owner expense into a tenant obligation.

- 17.10.030 ties responsibility to causing, maintaining or permitting the nuisance; owner, tenant, manager and corporate officer status are examples, not an automatic rule assigning every charge to the tenant. Negligent or willful minor conduct has a separate custodial-parent/guardian imputation and joint-and-several penalty/cost branch.
- Each of 17.10.050's 30 lettered designations has its own proposal, preserving internal alternatives and qualifiers. The commercial/industrial exterior-debris branch is retained conditionally, since shared or mixed premises have not been excluded. It is not applied to residential premises by default.
- 17.10.051 allows City-funded graffiti removal subject to owner consent and a release/waiver. The owner pays for an expanded painting/repair area only when agreeing to that expanded cost. If consent cannot be obtained, owner-funded removal follows the specified written-notice procedure and 72-hour period. These distinctions can change the recommended work and owner expense.
- 17.10.052–.053 specify the owner appeal, City response and hearing-notice clocks, permitted grounds, documents and Council decision. No automatic stay of the 72-hour removal duty is invented; the chapter does not expressly provide one.
- 17.10.054 distinguishes the Council's post-hearing order, verified record, owner expense, parcel assessment and independent civil recovery. It does not make those City collection rights the landlord's tenant chargeback rights.
- 17.10.060 supplies misdemeanor classifications, not a new administrative fine amount, deposit deduction, eviction procedure or rent-forfeiture rule.
- .020 and .070 overlap on alternative proceedings. Both section decisions retain the actor-specific text for adjudication; merging their overlap is possible without losing the City Attorney branch.

## Dependencies and limits requiring investigation before application

1. **Superior-law control of conduct-based enforcement.** The E, F, H, V, W and X designation proposals include mechanically copied construction from saved AB 1418, Government Code 53165.1(b)–(c). These local clauses cannot independently justify a local requirement/encouragement to evict or penalize for alleged unlawful conduct, arrest, association with a household member having police contact or a conviction, or a penalty solely for law-enforcement contact. The enactment preserves otherwise state-law-consistent local rules. This review does not declare the whole chapter void or erase independent lawful state nuisance remedies. The saved source is an enactment extract, not a verified current full code section; exceptions, subsequent amendments, related protections and controlling interpretation must be reconciled by the wider review. The general superior-law gate applies to all proposals, not just those six highlighted branches.
2. **Historical dates.** Every proposal deliberately has blank effective_from/effective_to plus an express event-date gate. Ordinance annotations show amendment identifiers/months, not established legal commencement dates or all intervening versions. Current capture cannot alone prove what governed the March 2023 Breakwater departure. AB 1418's January 2024 operation cannot be retroactively used to decide that 2023 event. Event-specific effective dates must be proved before any proposal becomes an executable rule.
3. **Incorporated law.** 17.10.050(A) invokes Civil Code 3479/3480 and other state/local nuisance declarations; (B) incorporates eight adopted/amended code families; (C) broadly invokes municipal, zoning and adopted codes; (D) invokes Title 5 and certificate-of-occupancy requirements; (F) invokes Penal Code 186.22; (V)/(X) depend on state offense definitions; (Y) invokes HBMC 8.40; and (DD) invokes Health and Safety Code 17920.3. Their complete operative text, reach, amendments and construction were not investigated in this assigned batch. The proposals preserve the incorporation, not falsely claim those predicates are fully resolved. In particular, (DD)'s displayed text refers to “following listed conditions” but does not itself supply a list; do not invent one or replace the section by an unexamined building-code list.
4. **Licence and rent recovery.** .050(D)'s title-5/certificate nuisance designation is not a rule automatically wiping out rent or prohibiting all claims. Establish the relevant licence/occupancy duty, violation, applicable statutory consequence and controlling authority separately. Neither a nuisance label nor this chapter supplies that conclusion.
5. **Tenant account and repair allocation.** Connect the state repair, tenant duty, habitability, ordinary-wear, deposit and contract rules to established facts before allocating expense or deducting security. Graffiti, existing damage and City charges require their own cause/condition records and lawful allocation. This chapter's duty to abate is not an answer to who owes the landlord money.
6. **Enforcement dependencies.** Government Code 38773.5 assessment procedures, any additional notice/hearing prerequisites, general municipal penalty/procedure provisions, day-counting rules, appeal-stay law and judicial-review remedies remain outside this batch's completed research. Council finality is described as finality within the local process, not elimination of court review. No assumption is made that an owner has only 72 hours to appeal, or that the 10-day appeal deadline automatically suspends abatement.
7. **Source currentness and property scope.** The live code page displayed a separate New Laws link; this batch did not reconcile pending codification or the full ordinance ledger. Property-specific assistance/affordability covenants, building facts, program terms and applicability remain unestablished. No market-rate-only exclusion was applied.

These are real limits on legal application, not sections disguised as irrelevant or assertions that law has been conclusively settled. Unsaved or not-investigated authority is named above but is not cited as a saved supporting quote. Proposal `dependencies` arrays do not pretend that these missing incorporated-law atoms already exist; adjudication must resolve and link them.

## Quote handling and validation

All primary quotations were extracted by script from the saved per-section text; the .050 designations and .060 branches use their exact saved branch text. Definitions are extracted by exact source delimiters. The AB 1418 construction quote is extracted from the saved enactment file. None was retyped. Procedural proposals sometimes quote their full short section to preserve every exception supporting the extracted branch.

Validation from `research/legal-engine`:

```text
python3 -m pipeline check-decisions CA-HB 1
CA-HB batch 1: 12/12 decided {'excluded_regime': 0, 'new_rule': 11, 'no_decision': 1, 'partial': 0, 'stated': 0}; 0 errors

python3 -m pipeline check-decisions CA-HB --self-test
check-decisions self-test: planted bad atom id, bad quote, hedging, wrong prefix and undecided section caught = True
```

These checks establish file coverage, required proposal fields and quotation fidelity; they do not establish legal correctness, temporal completeness or resolved dependencies.
