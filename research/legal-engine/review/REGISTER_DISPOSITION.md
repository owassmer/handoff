# Register review applied: disposition (NYC market-rate)

2026-09-30. Owen approved applying the adjudicated register findings (register/work/ADJUDICATION_QUEUE.md) in one pass; NYC Stage A is now parked. Scripts: build/apply_register_1.py (sources) to _6.py (register status), each rerun-safe from build/backups/*_pre_register.* and build/backups/register_checkpoints/. This file is written by build/write_register_disposition.py.

## Counts

| File | Rules before | Rules after | Added | From queue proposals | From conditions (11 U.S.C. 362) | From scope additions (batch 9) | Existing rules changed |
|---|---|---|---|---|---|---|---|
| NY.json | 291 | 694 | 403 | 403 | 0 | 0 | 18 |
| NYC.json | 201 | 244 | 43 | 43 | 0 | 0 | 7 |
| US.json | 198 | 359 | 161 | 148 | 4 | 9 | 10 |
| VA.json | 277 | 277 | 0 | 0 | 0 | 0 | 0 |

Queue proposals (decisions_1-8): 596. Added as rules: 594. Merged into another proposal: 2. Proposals naming an existing rule ('amends'): 91; every one is kept as its own rule and linked both ways to the rule it amends (each states a different section from its target; the one sharing a cite, US:11USC105-discharge-contempt, rests on 105(a), a different power from 524(a)(2)). Where the adjudication ruled that the target itself was incomplete or wrong, the target was also edited (below).

## Merges

| Merged proposal | Into | Why |
|---|---|---|
| `NY:DCL-282-deposit-exemption-payee` (batch 1) | `US:11USC522-refund-exemption` (batch 5) | Same law: a New York debtor's exempt residential deposit is paid to the tenant once the exemption stands. The batch 5 rule is fuller (state or federal election, setoff, lien avoidance); the DCL 282, CPLR 5205(g) and 522(l) quotes are carried as construction. |
| `NY:CCA-305-venue-residence` (batch 2) | `NY:CCA-2101(g)-balance-venue-current` (batch 7) | Batches 7-8 condition 2: one venue rule set. The batch 7 rule states today's venue (a lease balance is not a consumer credit transaction, so any city county where a party resides); CCA 305's entity residence and assignee rule are merged into it, and `NY:S9760-venue` and it now point to each other (current rule until the pending act applies, then S9760). |

## Re-points

- `NY:NPCL-1309(b)-name-change-suspension`: dependency `NY:BCL-1312(a)-foreign-authority` -> `NY:NPCL-1313-foreign-authority` (batches 7-8 condition 1).
- `NY:PTR-121-1504-foreign-related-llp`: `NY:LLC-808(a)-foreign-authority` -> `NY:PTR-121-1502-foreign-llp` (same).
- `NY:PTR-121-1506-llp-process-address-suspension`: adds `NY:PTR-121-104-a-process-address-suspension`, keeps `NY:LLC-206-publication-suspension` for the construction its reasoning cites (same).
- Every dependency on a merged proposal is re-pointed to its merge target.
- `US:15USC1681s-2(b)(1)` and `US:12CFR1022.43(a)`: the unread `EXT:15USC1681i` -> `US:15USC1681i-furnisher-deadline`; the external reference is removed.

## Existing rules changed (each carries out a ruling)

| Rule | Ruling carried out |
|---|---|
| `NYC:SHIELD-5-77(e)(10)-credit-report-notice` | Table row 1: FCRA 1681t(b)(1)(F) preempts the pre-reporting notice; reverses R4A-11 for furnishing |
| `NY:GBL-604-bb-coerced-debt` | Table row 1: credit-bureau notice branch displaced by FCRA 1681t(b)(1)(F); collection duties stand |
| `NY:RPL-227-c(5)(b)` | Table row 1: credit-bureau branch displaced by FCRA 1681t(b)(1)(F); third-party branch stands |
| `NY:MIL-306-309` | Table row 2: 306 stays execution and attachments, mandatory on application; it does not stay the action |
| `NY:COMMONLAW-owner-death-agency` | Table row 3: rent accrued before death is the estate's personal property even for a specifically devised building |
| `US:11USC542-refund-payee` | Table row 4: exemption, abandonment, conversion and dismissal branches added |
| `NY:16NYCRR96-submetering` | Table row 5: rate cap (96.1(i)) and HEFPA protections (96.6) added |
| `NY:ADJ-tenant-death-payee` | Table row 6: co-tenant death, public administrator, foreign fiduciaries, small-estate certificates, SCPA 1806/1808/1810 deadlines and guardianship ending on death added |
| `NY:CASE-NML-contract-rate` | Table row 7: a rate stated without a period is yearly (GOL 5-1301) |
| `NY:ADJ-provide-written-dispatch` | Table row 8: the day is counted on New York time (GCN 53) |
| `NY:CPLR-5205-5231-enforcement-limits` | Table row 9: exemption amounts adjust every three years (CPLR 5253) |
| `NY:ADJ-tenant-deposit-claim-limitations` | Table row 10: CPLR 202 borrowing statute for non-resident plaintiffs |
| `NY:CPLR-213(2)` | Table row 10: CPLR 202 borrowing statute for non-resident plaintiffs |
| `NY:CPLR-321-JUD-495-appearance` | Table row 11: a corporation defending a small claim may appear by its officer or employee (CCA 1809(2)) |
| `NYC:HMC-27-2135(c)-receiver-rents` | Table row 12: the 27-2148 lien receiver reaches one- and two-family houses |
| `NY:ADJ-lease-break-charge` | Table row 13 (condition 2 met): NYC Admin. Code 26-3402 caps vacating charges on leases from 2022-06-22 |
| `NYC:HMC-27-2017.5-turnover` | Table row 14: owner pest and mold duty in every dwelling (27-2017.1) |
| `NYC:HMC-27-2013(a)` | Table row 14: a written lease may shift repair and painting in a one- or two-family house (27-2005(c)) |
| `NYC:PAINT-wear-and-tear` | Table row 14: written-lease allocation branch for one- and two-family houses |
| `NYC:HMC-27-2045-detector-charge` | Table row 15: class B buildings added |
| `US:24CFR92.253(b)(2)` | Table row 16: HRA HOME TBRA is in the aperture; moved out of the deferred list |
| `US:11USC524(a)(2)` | Table row 17: contempt sanction and 524(c), (e), (f) branches added |
| `US:FRBP-3002(c)-claim-deadline` | Table row 17: chapter 7 tardy claims paid in the third class (726(a)(3)) |
| `US:24CFR100.65-terms` | Table row 18: 3603(b) exemptions stated |
| `US:15USC7001(c)-esign-consent` | Table row 18: consent owed only to a consumer (7006(1)) |
| `US:50USC4042` | Table row 18: 4041 penalties and 4043 other remedies added |
| `NY:BCL-1312(a)-foreign-authority` | Batches 7-8: BCL 1301 statutory 'doing business' exclusions |
| `NY:LLC-808(a)-foreign-authority` | Batches 7-8: LLC Law 803 statutory 'doing business' exclusions |
| `NY:GBL-130-assumed-name` | Batches 7-8: BCL 1301(d) carve-out for a filed fictitious name |
| `NY:HANDOFF-broker-config-under-broker` | Batches 7-8: 19 NYCRR 175.21 supervision condition |
| `NYC:ADC-20-490` | Batches 7-8: 20-105 daily fine added |
| `US:15USC1681s-2(b)(1)` | Report 6 finding 4: the reinvestigation period stated (1681i) |
| `US:12CFR1022.43(a)` | Report 6 finding 4: dependency re-pointed from the unread EXT:15USC1681i to the 1681i rule |
| `US:26CFR1.166-1(e)-bad-debt` | Report 5: agent reporting of rents added |
| `NY:S9760-venue` | Batches 7-8 condition 2: reconciled with the current-venue rule NY:CCA-2101(g)-balance-venue-current |

New rules the conditions required (11 U.S.C. 362 in full; report 5 said the owner of 362 should state them): `NY:GCN-52-standard-time`, `US:11USC707(b)-abuse-motion`, `US:11USC362(c)-stay-ends`, `US:11USC362(c)(3)-(4)-repeat-filer`, `US:11USC362(e)-relief-deadline`, `US:11USC362(k)-willful-violation`.

## Changes made to proposals when applying them (each against its saved source)

- `NYC:ADC-26-3402-vacating-fee-cap` (condition 2): legislative history of L.L. 2021/169 (Int. 2312-A) saved from Legistar: the enacted local law, both committee reports, the stated-meeting report, the fiscal impact statement, hearing testimony and transcript. Construction: 227-e governs mitigated rent damages; every other vacating charge, including a lease-break sum fixed as liquidated damages, falls within the fair-market-cost ceiling (the reports name lease-break penalties and fees for vacating in slower months). The proposal had placed valid liquidated damages outside the ceiling; that branch is reversed on the committee reports. Applies only to leases entered into on or after 2022-06-22 (section 2). No decision construing the section was found (CourtListener search API for '26-3402', '26-3302', 'fair market cost necessary to prepare', 'fees associated with vacating'; web search).
- `NY:CCA-1808-preclusion`, `NY:CCA-1808-A-preclusion`: Simmons v Trans Express (Court of Appeals 2021) saved; it holds a small-claims judgment 'may' preclude under the pragmatic transactional test and expressly leaves the counterclaim question open, so the rules are MIXED with the test as judgment terms, and branch (d) rests on Henry Modell (Court of Appeals 1986, saved).
- `US:11USC523-landlord-exceptions`: In re Massa (2d Cir. 1999) does not hold the no-asset rule the proposal cited it for (it holds that an unscheduled creditor with actual knowledge that fails to act is discharged, and that knowledge of a chapter 13 filing is not knowledge of the converted chapter 7). Massa is now cited for what it holds; the no-asset branch rests on 523(a)(3)(A) and FRBP 3002(c)(5).
- `US:11USC507(a)(7)-deposit-priority`: Guarracino, River Village, Wise and Cimaglia saved and quoted; the reasoning now attributes Guarracino's holding to the legislative history (not the grammar argument). In re Miller (Bankr. S.D. Ala. 2019) was not found (CourtListener search API: three queries by name, court alsb and the 507(a)(7) text); its point (no priority for a landlord's claim for an unpaid deposit) rests on 507(a)(7)'s text, which gives the priority only to individuals who made the deposit, so no branch is dropped.
- `US:15USC1681t(b)(1)(F)-furnisher-preemption`: Macpherson v JPMorgan Chase (2d Cir. 2011) saved; preemption covers common-law claims, even malicious reporting. Applied consistently beyond the table: `NY:MIL-313-a-no-adverse-report` (its credit-bureau branch) and `NY:GBL-380-o-false-pretenses` (branch (b), knowingly false furnishing) no longer bind a furnisher; `US:15USC1681h(e)-furnisher-immunity` gains the Macpherson branch; the disposal branch cites 1681t(b)(5)(I).
- `NY:CPLR-3213-summary-judgment-in-lieu` and `NY:CPLR-4545-collateral-source` (condition 3): no round 6B follows (NYC is parked), so the controlling decisions were read now: Midda Realty v Ci-Tex and Big K Kosher Dairy v Gross (2d Dept) hold a lease is not an instrument for the payment of money only; Fisher v Qualico (Court of Appeals 2002) applies 4545 to property-damage claims and states its purpose.
- `NY:CPLR-202-borrowing`: Global Fin. v Triarc and Portfolio Recovery v King saved and quoted (accrual where the plaintiff resides; assignee takes the assignor's place; foreign tolling borrowed; choice-of-law clause irrelevant).
- `US:11USC105-discharge-contempt` (Taggart), `US:11USC550-transferee-liability` (Finley, Kumble), `US:11USC104-dollar-amounts` (90 FR 8941, 90 FR 10643, 87 FR 6625): quoted.
- `NY:GCN-52-standard-time` quotes 15 U.S.C. 260a (the Uniform Time Act's supersession of state changeover dates) and `US:11USC707(b)-abuse-motion` quotes FRBP 1017(e)(2) (condition 1).
- Process wording removed from four proposals (`NY:RPL-224-attornment-void`, `NYC:HMC-27-2004(48)-ending-harassment`, `NY:PTR-121-1504-foreign-related-llp`, `NY:PTR-121-201-lp-publication`); `NY:GOL-5-1301-rate-per-annum` no longer uses a figure in its example.

Every figure a new rule states (money, percentages, periods, dates) is traced to a saved source by the apply scripts (must()); the trace for 228 rules is build/register_figure_trace.json.

## Scope additions (ADJUDICATION_QUEUE 'Modifications')

- TILA part B (15 U.S.C. 1631-1651, 31 sections) is now an in-scope unit of US:15USC-ch41, and the FTC Disposal Rule (16 CFR part 682, 5 sections) a new instrument US:16CFR682; texts saved in the register format from the USLM XML (release 119-111) and the eCFR API. Batch 9 (register/work/batch_9.json, decisions_9.jsonl, reviewer ferro) decides all 36 plus the three tax sections the adjudication reclassified: 9 new rules (`US:15USC1631-plan-disclosure-duty`, `US:15USC1632-disclosure-form`, `US:15USC1638-closed-end-disclosures`, `US:15USC1640-tila-civil-liability`, `US:15USC1641-assignee-liability`, `US:16CFR682.3-disposal`, `US:26USC6050I-cash-over-10000`, `US:26USC6050W-card-network-settlement` (per Handoff configuration), `US:26USC6045(f)-attorney-payments`), 2 stated, 28 no_decision (mortgage, open-end, card and education-loan sections).
- `US:24CFR92.253(b)(2)`: HRA HOME tenant-based rental assistance is in the aperture (24 CFR 92.209(g) and 68 RCNY 9-06 quoted); moved out of the walk's deferred list.

## Authorities saved (sources/REGISTER_*)

| File | Source |
|---|---|
| REGISTER_NYC_LL2021-169_committee_report_2021-11-09.txt | https://legistar.council.nyc.gov/View.ashx?M=F&ID=9945781&GUID=D7F304E1-89C8-4596-BDB5-3D8BC016D3E7 |
| REGISTER_NYC_LL2021-169_committee_report_2021-11-22.txt | https://legistar.council.nyc.gov/View.ashx?M=F&ID=10223991&GUID=29ED3E63-A2B1-47D1-AED8-BAB8C0D5F123 |
| REGISTER_NYC_LL2021-169_committee_report_stated_meeting.txt | https://legistar.council.nyc.gov/View.ashx?M=F&ID=10245222&GUID=5B799C9B-0FC0-4E11-A83F-92F52CBE0617 |
| REGISTER_NYC_LL2021-169_fiscal_impact.txt | https://legistar.council.nyc.gov/View.ashx?M=F&ID=10223994&GUID=DB9A2EC9-8DDD-4D2A-A54D-D09DDEC3EEDE |
| REGISTER_NYC_LL2021-169_hearing_testimony_2021-11-09.txt | https://legistar.council.nyc.gov/View.ashx?M=F&ID=9966355&GUID=51B37429-8EF1-44B5-8F60-582E5E68EBA6 |
| REGISTER_NYC_LL2021-169_hearing_transcript_2021-11-09.txt | https://legistar.council.nyc.gov/View.ashx?M=F&ID=10316505&GUID=F36C3381-3073-40C3-95BE-6C8F3D84AA45 |
| REGISTER_NYC_LL2021-169_legistar_record.txt | https://legistar.council.nyc.gov/LegislationDetail.aspx?ID=4950996&GUID=68DDC6D7-24B5-4AD3-99FE-7F4924B38291&Options=ID|Text|&Search= |
| REGISTER_NYC_LL2021-169_local_law.txt | https://legistar.council.nyc.gov/View.ashx?M=F&ID=10412352&GUID=44524566-6694-4A0F-A255-0C0693363F0B |
| REGISTER_NYC_LL2021-169_summary_Int2312-A.txt | https://legistar.council.nyc.gov/View.ashx?M=F&ID=9968609&GUID=42A79212-4F7A-46DB-A4F8-48B180580E2E |
| REGISTER_NY_CASE_Big_K_Kosher_v_Gross_1993_2dDept.txt | https://static.case.law/ad2d/198/cases/0205-01.json |
| REGISTER_NY_CASE_Fisher_v_Qualico_2002_CoA.txt | https://static.case.law/ny-2d/98/cases/0534-01.json |
| REGISTER_NY_CASE_Global_Fin_v_Triarc_1999_CoA.txt | https://static.case.law/ny-2d/93/cases/0525-01.json |
| REGISTER_NY_CASE_Henry_Modell_v_Minister_Elders_1986_CoA.txt | https://static.case.law/ny-2d/68/cases/0456-01.json |
| REGISTER_NY_CASE_Midda_Realty_v_Ci-Tex_1975_2dDept.txt | https://static.case.law/ad2d/50/cases/0600-03.json |
| REGISTER_NY_CASE_Portfolio_Recovery_v_King_2010_CoA.txt | https://static.case.law/ny3d/14/cases/0410-01.json |
| REGISTER_NY_CASE_Simmons_v_Trans_Express_2021_CoA.txt | https://storage.courtlistener.com/pdf/2021/06/03/charlene_simmons_v._trans_express_inc.pdf |
| REGISTER_NY_PEN_190.40.txt | https://newyork.public.law/laws/n.y._penal_law_section_190.40 |
| REGISTER_US_15USC_260a.txt | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section260a&num=0&edition=prelim |
| REGISTER_US_15USC_261.txt | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section261&num=0&edition=prelim |
| REGISTER_US_16CFR_682.3.txt | https://www.ecfr.gov/current/title-16/section-682.3 |
| REGISTER_US_24CFR_92.209.txt | https://www.ecfr.gov/current/title-24/section-92.209 |
| REGISTER_US_26CFR_1.6045-5.txt | https://www.ecfr.gov/current/title-26/section-1.6045-5 |
| REGISTER_US_26CFR_1.6050I-1.txt | https://www.ecfr.gov/current/title-26/section-1.6050I-1 |
| REGISTER_US_26CFR_1.6050W-1.txt | https://www.ecfr.gov/current/title-26/section-1.6050W-1 |
| REGISTER_US_26CFR_301.6011-2.txt | https://www.ecfr.gov/current/title-26/section-301.6011-2 |
| REGISTER_US_26USC_1211.txt | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title26-section1211&num=0&edition=prelim |
| REGISTER_US_26USC_1441.txt | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title26-section1441&num=0&edition=prelim |
| REGISTER_US_26USC_61.txt | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title26-section61&num=0&edition=prelim |
| REGISTER_US_CASE_Commissioner_v_Glenshaw_Glass_1955_SCOTUS.txt | https://static.case.law/us/348/cases/0426-01.json |
| REGISTER_US_CASE_Finley_Kumble_Christy_v_Alexander_1997_2dCir.txt | https://static.case.law/f3d/130/cases/0052-01.json |
| REGISTER_US_CASE_Guarracino_v_Hoffman_2000_DMass.txt | https://static.case.law/br/246/cases/0130-01.json |
| REGISTER_US_CASE_In_re_Cimaglia_1985_BankrSDFla.txt | https://static.case.law/br/50/cases/0009-01.json |
| REGISTER_US_CASE_In_re_Massa_1999_2dCir.txt | https://static.case.law/f3d/187/cases/0292-01.json |
| REGISTER_US_CASE_In_re_River_Village_1993_BankrEDPa.txt | https://static.case.law/br/161/cases/0127-01.json |
| REGISTER_US_CASE_In_re_Wise_1990_BankrDAlaska.txt | https://static.case.law/br/120/cases/0537-01.json |
| REGISTER_US_CASE_Kawaauhau_v_Geiger_1998_SCOTUS.txt | https://static.case.law/us/523/cases/0057-01.json |
| REGISTER_US_CASE_Koons_Buick_v_Nigh_2004_SCOTUS.txt | https://static.case.law/us/543/cases/0050-01.json |
| REGISTER_US_CASE_Lamar_Archer_v_Appling_2018_SCOTUS.txt | https://www.supremecourt.gov/opinions/17pdf/16-1215_gdhk.pdf |
| REGISTER_US_CASE_Macpherson_v_JPMorgan_Chase_2011_2dCir.txt | https://static.case.law/f3d/665/cases/0045-01.json |
| REGISTER_US_CASE_Taggart_v_Lorenzen_2019_SCOTUS.txt | https://www.supremecourt.gov/opinions/18pdf/18-489_p8k0.pdf |
| REGISTER_US_FRBP_1017.txt | https://uscode.house.gov/view.xhtml?path=/prelim@title11/title11a&edition=prelim |
| REGISTER_US_FR_87FR6625_bankruptcy_dollar_amounts_2022.txt | https://www.govinfo.gov/content/pkg/FR-2022-02-04/pdf/2022-02299.pdf |
| REGISTER_US_FR_90FR10643_bankruptcy_dollar_amounts_2025_correction.txt | https://www.govinfo.gov/content/pkg/FR-2025-02-25/pdf/C1-2025-02207.pdf |
| REGISTER_US_FR_90FR8941_bankruptcy_dollar_amounts_2025.txt | https://www.govinfo.gov/content/pkg/FR-2025-02-04/pdf/2025-02207.pdf |

Already saved before this pass and used as is: 11 U.S.C. 362 in full (register/texts/US_11USC/362.txt, sources/US_11USC_362.txt). Not saved, with routes tried: In re Miller (Bankr. S.D. Ala. 2019), see above; the Int. 2312-A '(FINAL)' Legistar attachment returned a non-document body, and the enacted Local Law 169 text (saved) is identical. No branch rests on either.

## Register status

Every section in register/triage.jsonl carries a reviewer decision: review_decision, review_batch (1-9, or 'match' for the 312 sections the register marked stated by citation match, whose rules passed review rounds 1-5), review_reason, and atom_ids for stated, partial and new_rule. The three tax sections keep their batch 5 decision in review_history. check_register.py runs strict by default (check 7) and has a third self-test (a planted undecided section). check_decisions.py checks every batch file and accepts a proposal id in the rule files only as its applied atom (register/work/applied.json).

## Walk

review/NYC_MARKET_RATE.md cites every new rule at its step; procedure is grouped in Step 8.13 (court and venue, commencing and serving, answer and preclusion, proof, defaults, judgment and costs, enforcement); new sub-steps 1.9, 5.7a, 6.6a and 7.7; the sentences the rulings change are rewritten (0.5 owner death, 3.3 and 5.2 and 5.4 vacating charges, 3.4 227-c(5)(b), 3.8 Military Law 306, 4.1 E-SIGN consumer, 5.5a submetering, pests and class B detectors, 6.7 bankruptcy payee, 6.10 disposal, 7.6 borrowing, 8.1a coerced debt, 8.5 SHIELD notice, 8.6a broker supervision, 8.8 discharge and tardy claims, 8.10 appearance, venue and interest, 8.12 exemption adjustment, test case C6).

## Check output (final run)

```
$ stage_a_check.py stage-a/NY.json stage-a/NYC.json stage-a/VA.json stage-a/US.json
stage-a/NY.json: 694 atoms, 0 errors
stage-a/NYC.json: 244 atoms, 0 errors
stage-a/VA.json: 277 atoms, 0 errors
stage-a/US.json: 359 atoms, 0 errors
cross-file: 0 errors
(exit 0)
```
```
$ review/check_review.py review/NYC_MARKET_RATE.md
in scope 1200: cited 1098, deferred 102, not cited 0; also cited from outside scope 3
(exit 0)
```
```
$ register/work/check_decisions.py all
batch 1: 499/499 decided {'excluded_regime': 49, 'new_rule': 55, 'no_decision': 340, 'partial': 40, 'stated': 15}; 0 errors
batch 2: 560/560 decided {'excluded_regime': 1, 'new_rule': 193, 'no_decision': 341, 'partial': 23, 'stated': 2}; 0 errors
batch 3: 422/422 decided {'excluded_regime': 48, 'new_rule': 28, 'no_decision': 297, 'partial': 13, 'stated': 36}; 0 errors
batch 4: 496/496 decided {'excluded_regime': 0, 'new_rule': 48, 'no_decision': 402, 'partial': 32, 'stated': 14}; 0 errors
batch 5: 264/264 decided {'excluded_regime': 0, 'new_rule': 48, 'no_decision': 201, 'partial': 13, 'stated': 2}; 0 errors
batch 6: 257/257 decided {'excluded_regime': 3, 'new_rule': 78, 'no_decision': 158, 'partial': 6, 'stated': 12}; 0 errors
batch 7: 456/456 decided {'excluded_regime': 10, 'new_rule': 2, 'no_decision': 436, 'partial': 5, 'stated': 3}; 0 errors
batch 8: 420/420 decided {'excluded_regime': 0, 'new_rule': 6, 'no_decision': 413, 'partial': 1, 'stated': 0}; 0 errors
batch 9: 39/39 decided {'excluded_regime': 0, 'new_rule': 9, 'no_decision': 28, 'partial': 0, 'stated': 2}; 0 errors
(exit 0)
```
```
$ register/work/check_decisions.py --self-test
self-test: planted bad atom id, bad quote and undecided section caught = True
(exit 0)
```
```
$ register/check_register.py
Status counts:
  stated                 312
  review_queue           2532
  triaged_no_decision    878
  triaged_excluded       0
  unfetched              0
  total                  3722
  ...
Reviewer decisions (strict): excluded_regime 111, new_rule 467, no_decision 2613, partial 133, stated 398; batches 1-9 3410, match 312

Self-test planted unclassified section: caught (2 errors raised)
Self-test planted bad atom id:         caught (1 errors raised)
Self-test planted undecided section:   caught (strict check 7)

PASS: every section of every in-scope unit has a status and a reviewer decision; every atom id named exists; every triaged section carries a Jev record or hand reason; every instrument named in an atom provision is registered. (strict)
(exit 0)
```

## Appendix: proposals that named an existing rule, kept as their own rules and linked both ways

| Proposal (batch) | Existing rule |
|---|---|
| `NY:16NYCRR-96.6-submeter-charge-limits` (1) | `NY:16NYCRR96-submetering` |
| `NY:RPL-227-b(5)-(7)-senior-reinstatement` (1) | `NY:RPL-227-a(2)` |
| `NY:9NYCRR-466.14-association` (1) | `NY:EXEC-296(5)(a)(2)-terms` |
| `US:11USC522-refund-exemption` (1) (merged from `NY:DCL-282-deposit-exemption-payee`) | `US:11USC542-refund-payee` |
| `NY:GOL-5-1301-rate-per-annum` (1) | `NY:CASE-NML-contract-rate` |
| `NY:16NYCRR-96.1(i)-rate-cap` (1) | `NY:16NYCRR96-submetering` |
| `NY:GCN-62-type-size` (1) | `NY:CPLR-4544-small-print` |
| `NY:CCA-1811(d)-satisfaction-proof` (2) | `NY:CCA-1812-treble` |
| `NY:CPLR-215(7)-retaliation-one-year` (2) | `NY:RPL-223-b-retaliation` |
| `NY:CPLR-5003-judgment-interest` (2) | `NY:CPLR-5004(a)-consumer-2pct` |
| `NY:CPLR-5230-execution` (2) | `NY:CPLR-5205-5231-enforcement-limits` |
| `NY:CPLR-5232-levy` (2) | `NY:CPLR-5205-5231-enforcement-limits` |
| `NY:CCA-1402-default-on-endorsed-summons` (2) | `NY:CPLR-3215(g)(3)` |
| `NY:CCA-1815-relative-representative` (2) | `NY:CPLR-321-JUD-495-appearance` |
| `NY:CCA-412-interest-from-service` (2) | `NY:CPLR-5001(a)-(b)` |
| `NY:CPLR-1021-substitution-deadline` (2) | `NY:CPLR-1203-1015-5208-parties` |
| `NY:CPLR-1201-representation` (2) | `NY:CPLR-1203-1015-5208-parties` |
| `NY:CPLR-1205-no-costs-against-incapacitated` (2) | `NY:CPLR-1203-1015-5208-parties` |
| `NY:CPLR-201-agreed-shorter-period` (2) | `NY:ADJ-tenant-deposit-claim-limitations` |
| `NY:CPLR-5002-decision-to-judgment` (2) | `NY:CPLR-5001(a)-(b)` |
| `NY:CPLR-5021-entry-of-satisfaction` (2) | `NY:CPLR-5020-satisfaction` |
| `NY:CPLR-5201-reachable-property` (2) | `NY:CPLR-5205-5231-enforcement-limits` |
| `NY:CPLR-5206-homestead` (2) | `NY:CPLR-5205-5231-enforcement-limits` |
| `NY:CPLR-5253-exemption-adjustment` (2) | `NY:CPLR-5205-5231-enforcement-limits` |
| `NY:JUD-484-nonlawyer-preparation` (2) | `NY:CPLR-321-JUD-495-appearance` |
| `NY:CPLR-1202-guardian-ad-litem-motion` (2) | `NY:CPLR-1203-1015-5208-parties` |
| `NY:JUD-485-a-felony` (2) | `NY:CPLR-321-JUD-495-appearance` |
| `NY:JUD-490-champerty-exception` (2) | `NY:JUD-489-champerty` |
| `NY:CCA-110-housing-part-appearance` (2) | `NY:CPLR-321-JUD-495-appearance` |
| `NYC:HMC-27-2005(c)-1-2-family-allocation` (3) | `NYC:HMC-27-2013(a)` |
| `NYC:HMC-27-2017.1-pest-owner-duty` (3) | `NYC:HMC-27-2017.5-turnover` |
| `NYC:HMC-27-2148-lien-receiver-rents` (3) | `NYC:HMC-27-2135(c)-receiver-rents` |
| `NYC:RCNY28-12-03-classB-smoke` (3) | `NYC:HMC-27-2045-detector-charge` |
| `NYC:RCNY28-12-09-classB-CO` (3) | `NYC:HMC-27-2045-detector-charge` |
| `NYC:RCNY6-6-62-collection-penalties` (3) | `NYC:ADC-20-490` |
| `NYC:RCNY6-6-89-FARE-penalties` (3) | `NYC:FARE-20-699.23(c)` |
| `NYC:ADC-20-106-unlicensed-sanctions` (3) | `NYC:ADC-20-490` |
| `NYC:ADC-20-703-CPL-remedies` (3) | `NYC:CPL-20-700` |
| `NYC:ADC-27-2103-registration-extension` (3) | `NYC:ADC-27-2107(b)-rent-stay` |
| `NYC:RCNY6-6-47-CPL-penalties` (3) | `NYC:CPL-20-700` |
| `NY:MIL-302-guarantor-stay` (4) | `NY:MIL-306-309` |
| `NY:MIL-304-stay-on-application` (4) | `NY:MIL-306-309` |
| `NY:MIL-307-stay-terms` (4) | `NY:MIL-306-309` |
| `NY:18NYCRR-352.6(c)(2)-damage-verification` (4) | `NYC:HRA-voucher-proof` |
| `NY:EPTL-11-4.6-execution-leave` (4) | `NY:CPLR-1203-1015-5208-parties` |
| `NY:GBL-604-b-penalty-cure` (4) | `NY:GBL-601-a-family` |
| `NY:GBL-604-dd-lease-balance-not-secured` (4) | `NY:GBL-604-bb-coerced-debt` |
| `NY:MIL-316-a(2)-storage-lien` (4) | `US:50USC3958(a)` |
| `NY:MIL-318-no-waiver-request` (4) | `US:50USC3918` |
| `NY:SCPA-1803-claim-form` (4) | `NY:ADJ-tenant-death-payee` |
| `NY:SSL-137-assistance-exempt` (4) | `NY:CPLR-5205-5231-enforcement-limits` |
| `NY:SSL-137-a-wages-exempt` (4) | `NY:CPLR-5205-5231-enforcement-limits` |
| `NY:EPTL-11-1.1-fiduciary-powers` (4) | `NY:ADJ-tenant-death-payee` |
| `NY:EPTL-11-3.4-no-representative-of-representative` (4) | `NY:ADJ-tenant-death-payee` |
| `NY:EPTL-13-1.1-accrued-rent-leasehold` (4) | `NY:COMMONLAW-owner-death-agency` |
| `NY:EPTL-13-3.4-foreign-fiduciary` (4) | `NY:ADJ-tenant-death-payee` |
| `NY:GBL-349-c-elderly-penalty` (4) | `NY:GBL-349-unfair-abusive` |
| `NY:GBL-350-d-civil-penalty` (4) | `NY:GBL-349-unfair-abusive` |
| `NY:GBL-133-deceptive-name` (4) | `US:15USC1692a(6)-false-name` |
| `NY:GBL-399-zzz-paper-fee` (4) | `NY:RPL-235-g` |
| `NY:MHL-81.44-death-of-ward` (4) | `NY:ADJ-tenant-death-payee` |
| `NY:NPCL-1313-foreign-authority` (4) | `NY:BCL-1312(a)-foreign-authority` |
| `NY:LLC-802-foreign-publication-suspension` (4) | `NY:LLC-808(a)-foreign-authority` |
| `NY:SCPA-1115-pa-small-estate` (4) | `NY:ADJ-tenant-death-payee` |
| `NY:SCPA-1118-pa-before-letters` (4) | `NY:COMMONLAW-owner-death-agency` |
| `NY:SCPA-1302-va-personal-property-only` (4) | `NY:COMMONLAW-owner-death-agency` |
| `NY:SCPA-1309-foreign-small-estate` (4) | `NY:ADJ-tenant-death-payee` |
| `NY:SCPA-720-revoked-letters` (4) | `NY:ADJ-tenant-death-payee` |
| `NY:EXEC-296-a-payment-plan` (4) | `NY:EXEC-296(5)(a)(2)-terms` |
| `NY:UCC-3-116-cotenant-refund-check` (4) | `NY:ADJ-cotenants-payee` |
| `US:11USC506-deposit-secured-claim` (5) | `US:FRBP-3002(c)-claim-deadline` |
| `US:11USC507(a)(7)-deposit-priority` (5) | `US:11USC541-704-owner-chapter7` |
| `US:11USC726-ch7-distribution-order` (5) | `US:FRBP-3002(c)-claim-deadline` |
| `US:FRBP3001-claim-contents` (5) | `US:FRBP-3002(c)-claim-deadline` |
| `US:11USC105-discharge-contempt` (5) | `US:11USC524(a)(2)` |
| `US:26CFR1.6049-6-tenant-statement` (5) | `US:26USC6049-deposit-interest` |
| `US:26USC166-writeoff-deduction` (5) | `US:26CFR1.166-1(e)-bad-debt` |
| `US:11USC101(5)-charge-timing` (5) | `US:11USC362(a)(6)` |
| `US:26CFR1.6041-1-agent-reports-rent` (5) | `US:26CFR1.166-1(e)-bad-debt` |
| `US:26CFR1.6049-4-middleman-return` (5) | `US:26USC6049-deposit-interest` |
| `US:26CFR1.6050P-1-identifiable-events` (5) | `US:26USC6050P-no-1099C` |
| `US:26CFR1.6050P-2-debt-buyer` (5) | `US:26USC6050P-no-1099C` |
| `US:50USC4043-other-remedies` (6) | `US:50USC4042` |
| `US:15USC7006-esign-consumer` (6) | `US:15USC7001(c)-esign-consent` |
| `US:15USC1681i-furnisher-deadline` (6) | `US:15USC1681s-2(b)(1)` |
| `NY:19NYCRR-175.21-broker-supervision` (7) | `NY:HANDOFF-broker-config-under-broker` |
| `NY:BCL-1301-doing-business-and-fictitious-name` (7) | `NY:BCL-1312(a)-foreign-authority` |
| `NY:BCL-1309(c)-authority-suspension` (7) | `NY:BCL-1312(a)-foreign-authority` |
| `NY:CCA-2101(g)-balance-venue-current` (7) | `NY:ADJ-lease-balance-not-consumer-credit` |
| `NY:LLC-803-doing-business-exclusions` (7) | `NY:LLC-808(a)-foreign-authority` |
| `NYC:ADC-20-105-unlicensed-daily-fine` (8) | `NYC:ADC-20-490` |
