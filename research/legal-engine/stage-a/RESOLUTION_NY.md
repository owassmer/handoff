# Resolution pass, New York State (2026-09-28)

`stage-a/NY.json` now holds 177 atoms and `bounded_unknowns: []`. `python3 stage_a_check.py stage-a/NY.json` exits 0.
The joint check with NYC, VA and US reports 0 cross-file errors. Those three files still fail on their own open items; they are in progress.

- Aperture: units in New York City and the state law that governs them (Owen, 2026-09-28).
- New authorities are saved under `sources/NY_*`. Every quote is checked verbatim by the checker. Mutating one word in a construction quote makes it fail, which was tested.
- The pre-pass file is backed up in profile scratch as `NY_pre_resolution.json`. The transformation script is `resolve_ny.py` in the same directory.

## Former question -> atoms, controlling authority, adjudication

| Former id | Resolving atoms | Controlling authority | Adjudication |
|---|---|---|---|
| BU-NY-RS-pre2025-by-reference | NY:ADJ-RS-pre2025-7108-inapplicable; edits NY:CASE-Karole-RS-via-RSC | GOL 7-108(1) text; RSC 2525.4(d) text; A6423-A sponsor memo; Walsh (CoA 2019); Lefkowitz v Parker (1st Dept 1971) | 7-108(1) excludes every 7-107 unit, and RSC 2525.4(d) requires compliance only with the article 7 sections that reach the unit. So Karole (Civ Ct 2022) and Sheridan One (Civ Ct 2026, in passing) are rejected. A stabilized tenancy on a pre-2025-11-15 lease has no statutory 14-day statement, forfeiture or double damages. |
| BU-NY-forfeiture-vs-claims | NY:ADJ-forfeiture-claims-survive; edits to (1-a)(e)-forfeiture, Levine, Paterno, Case | Levine (App Term 1st Dept 2026); Paterno (2d Dept 2010); statute text; Artibee (CoA 2017, derogation read strictly) | The statute forfeits only the right to retain the deposit. Rent and damage claims survive and are pursued separately or by counterclaim, with the landlord bearing the burden. Case v 575 Classon (App Term 2d) did not reach the question, and no decision holds otherwise. |
| BU-NY-willful | NY:ADJ-willful-standard (STANDARD); edits to (1-a)(g), Prando, Karole-willful, Bogom-Shanon, Masseroli | App Div construction of "willful": Nash, Central City Roofing, TPK (knew or should have known; experience); Prando and Case (App Term: fact finding, record support) | The Appellate Division's should-have-known test prevails over Masseroli (Sup Ct 2024), whose unawareness reasoning is rejected. Karole and Bogom-Shanon follow the test. Masseroli's result still fits for an inexperienced individual owner. |
| BU-NY-provide-delivery | NY:ADJ-provide-written-dispatch; NY:ADJ-provide-address-branches | Cohen (2d Dept 2024) and Urban (1st Dept 2025): timeliness is measured by the date sent; Freeland (1st Dept 2026): email suffices where the statute prescribes no form; Bogom-Shanon: writing required; Pickens; Prando | The statement must be in writing and is timely if sent within 14 days by a channel directed to the tenant; receipt is not required. A known email or phone must be used rather than the vacated unit. With no other channel, the landlord sends to the vacated unit, and waiting for an address forfeits. |
| BU-NY-multi-tenant-payee | NY:ADJ-cotenants-vacated; NY:ADJ-cotenants-payee; edit NY:RPL-235-f | GCN 35 via GCN 110; GOL 7-103(1); Holmes v Worthen (App Term 2d 2008); Lasky v Lissik; Freedman v Montague | "The tenant" means all the tenants, so the clock starts when the last tenant vacates. The refund is a joint obligation, and payment to one co-tenant who made the deposit discharges the landlord. The statement goes to every co-tenant. The Holmes dissent (split by contribution) is the losing view. |
| BU-NY-abandoned-belongings | NY:COMMONLAW-belongings-owner-keeps; NY:COMMONLAW-belongings-abandonment (STANDARD); edit NY:CASE-Facey-belongings | 8902 Corp. v Helmsley-Spear (1st Dept 2005); Cretaro (4th Dept 2022, applying Foulke, CoA 1920); Henryka (App Term 2d 2012) | Belongings stay the tenant's until abandoned. The landlord may not hold them for rent, must allow retrieval, and owes no bailee duty without an agreement; Facey's bailee description yields to the First Department. Disposal is lawful only on proof of abandonment. The UCC 7-206 borrowing (Wilson) is not the rule. |
| BU-NY-GBL-consumer-claim | NY:ADJ-lease-balance-not-consumer-credit; edits GBL-600(1), 600(3), CPLR-214-i, Lefferts | Text of GBL 600(1) and CPLR 105(f) ("credit ... extended"); Romea (2d Cir 1998); Lefferts (Civ Ct 2026); Walsh | A lease balance comes from breach, not credit. So GBL 601 does not govern the landlord or its agent, and the limitations period is six years under CPLR 213(2). Kings & Queens (Civ Ct 2017) misread Romea and is rejected. |
| BU-NY-7103-property | NY:ADJ-7103-2a-building-count; edits NY:GOL-7-103(2-a), Gihon | Gihon (2d Dept 2013); Governor's approval memo L.1970 c.1009 (in State v Parker); Holmes; AG Informal Op. 2014-2; Lefkowitz v Parker | Units are counted per building, and an owner's separate buildings are not combined even on one lot or in one complex. The AG's reference to "large residential landlords" states the purpose, not an aggregation rule. |
| BU-NY-NYC-tenant-monthly-notice | NY:COMMONLAW-NYC-monthly-tenant-surrender; NY:ADJ-NYC-monthly-agreed-notice; edits RPL-232-a, 232-b | T.I.B. Corp. v Repetto (App Term 1st Dept 1940, affd 261 App Div 813, lv denied 261 App Div 943); Adams v City of Cohoes (CoA 1891); RPL 232-b text; Colon (CoA 2020, McKinney's Statutes 240) | A NYC month-to-month tenant may surrender at the end of any month without notice unless an agreement requires notice. 232-a binds only landlords, and 232-b's tenant notice applies only outside NYC. Where an agreement requires notice, it governs, subject to 227-e mitigation. |
| BU-NY-late-fees-from-deposit | NY:ADJ-no-fee-retention; NY:ADJ-fee-retention-commonlaw; edits (1-a)(b)-refundable, 7-107(3)-refundable | 7-108(1-a)(b) closed list; Colon (expressio unius; one act read as a whole); RPAPL 702 (same L.2019 Part M: fees are not rent, "notwithstanding any language to the contrary in any lease"); 7-108(3); Freeland | Under 7-108(1-a) and amended 7-107, fees cannot be retained from the deposit, even if the lease labels them "additional rent"; lawful fees are pursued separately. Under the common-law regime, the deposit secures the lease (7-103(1)) and may be applied to a fee that is lawful under RPL 238-a. |
| BU-NY-ETPA-EHRCL-regs | none (coverage family 7) | Owen, 2026-09-28: focus on NYC | Outside the aperture. ETPA and state rent control outside NYC are not answered. The two deposit atoms already read (9 NYCRR 2505.4, 2105.5) are kept but not relied on for NYC units. |
| BU-NY-local-outside-NYC | none (coverage family 6) | Owen, 2026-09-28: focus on NYC | Outside the aperture. Municipalities outside NYC are not surveyed. |

## Other changes in this pass

- New atom NY:RPL-235-b (warranty of habitability offsets rent owed), read to close a "not read" note in coverage family 2.
- Hedges removed from atom text. The BU pointers in effect fields are replaced by the resolving atoms, and the "by inference" wording on former 7-107 is replaced by the s.2 lease-date rule. Toporek's (c)/(d) notes now state the forfeiture-only-for-(e) holding plainly.
- Case walks C1-C12 carry the resolving atoms and have empty `unknowns`.

## Ids the NYC file can reference

- NY:ADJ-RS-pre2025-7108-inapplicable (Karole seam)
- NY:COMMONLAW-belongings-owner-keeps, NY:COMMONLAW-belongings-abandonment (the statewide rule behind BU-NYC-abandoned-property)
- NY:ADJ-no-fee-retention, NY:ADJ-fee-retention-commonlaw (fees vs deposit)
- NY:ADJ-lease-balance-not-consumer-credit (GBL/CPLR)
- NY:ADJ-cotenants-vacated, NY:ADJ-cotenants-payee
- NY:ADJ-provide-written-dispatch, NY:ADJ-provide-address-branches
- NY:ADJ-willful-standard, NY:ADJ-forfeiture-claims-survive

Existing ids referenced by NYC.json are unchanged.
