# Queue review, batches 1-6: Ferro's adjudication

2026-09-30. Inputs: register/work/decisions_1-6.jsonl and report_1-6.md. check_decisions.py passes on all six
(2,498/2,498 decided, 0 errors, no proposed-id collisions). No rule file has been edited.

## Counts

| Decision | Sections |
|---|---|
| no_decision | 1,739 |
| new_rule | 450 |
| partial | 127 |
| excluded_regime | 101 |
| stated | 81 |

Proposed rules: 582 (106 critical, 263 major, 213 minor); 85 amend an existing rule.

## Rulings

Accept all 582 as proposed, subject to the conditions and modifications below. Ferro read the effect of every
critical rule and the saved text behind each finding that changes an existing rule.

### Conditions before applying

1. Authorities named but not saved under sources/ must be saved and quoted, or the branch that rests on them is
   dropped: Simmons v Trans Express (NY 2021; CCA 1808/1808-A claim preclusion); Global Fin. v Triarc (NY 1999) and
   Portfolio Recovery v King (NY 2010) (CPLR 202); Taggart v Lorenzen (US 2019), Guarracino, River Village, Appling,
   Geiger, Massa, Finley Kumble (bankruptcy); 90 FR 8941 (2025 dollar adjustments); 11 USC 362(c), (e), (k);
   FRBP 1017(e); 15 USC 260a (Uniform Time Act, for GCN 52); controlling Second Circuit authority on FCRA 1681t(b)(1)(F).
2. NYC:ADC-26-3402-vacating-fee-cap: text verified. Its reach (whether 'any amount' spares rent owed under the RPL
   227-e mitigation rule) rests on a Council summary not saved. Save the legislative history of L.L. 2021/169 and any
   decision construing 26-3402, then state the rule with that construction.
3. NY:CPLR-3213 and NY:CPLR-4545 rules rest on statutory reading only; round 6B checks them first.

### Modifications

- NY:UCC-3-802-check-suspends-obligation: keep. Text verified: a drawer's check suspends the obligation until
  presentment and on dishonor the obligation is enforceable. The consequence 'a dishonored refund check not replaced
  within the 14 days is a missed deadline' is stated as the adjudicated consequence with that reasoning.
- Batch 5 scope: 26 USC 6050I (cash over $10,000), 6050W (payment settlement entity, if Handoff settles payments for
  several owners) and 6045(f) (payments to a tenant's attorney) were decided no_decision under Ferro's brief, which
  limited tax to three events. That brief was narrower than the general test. They are reclassified as in scope and
  get rules in the apply step.
- Batch 6 register scope: TILA Part B (15 USC 1631-1651) and the FTC disposal rule (16 CFR 682) are added to the
  register as in-scope units.

### Findings that change existing rules (verified against saved text)

| Existing rule | Finding | Ruling |
|---|---|---|
| NYC:SHIELD-5-77(e)(10)-credit-report-notice; NY:GBL-604-bb-coerced-debt (credit-bureau notice); NY:RPL-227-c(5)(b) as to credit bureaus | FCRA 1681t(b)(1)(F) preempts state and city requirements on any subject matter regulated under 1681s-2; the only exceptions are two named Massachusetts and California provisions (text verified) | Accept. Reverses the round-4 R4A-11 rule for furnishing; the rules stay for collectors' other conduct |
| NY:MIL-306-309 | Section 306 stays execution of judgments and attachments or garnishments, mandatory on application unless ability to comply is not materially affected; it does not stay the action (text verified) | Accept |
| NY:COMMONLAW-owner-death-agency | Rent accrued before an owner's death is personal property of the estate, even where the building is specifically devised (EPTL 13-1.1(a)(6), text verified) | Accept |
| US:11USC542-refund-payee | Missing exemption (DCL 282, CPLR 5205(g), 11 USC 522), abandonment, conversion and dismissal branches | Accept |
| NY:16NYCRR96-submetering | Missing the rate cap and HEFPA protections (16 NYCRR 96.1(i), 96.6) | Accept |
| NY:ADJ-tenant-death-payee | Missing co-tenant death (GOL 15-106), public administrator, foreign fiduciaries and small-estate certificates, SCPA 1806/1808/1810 deadlines, guardianship ending on death | Accept |
| NY:CASE-NML-contract-rate | A rate stated without a period is yearly (GOL 5-1301) | Accept |
| NY:ADJ-provide-written-dispatch | The day is counted on New York time (GCN 53) | Accept, after 15 USC 260a is saved |
| NY:CPLR-5205-5231-enforcement-limits | Exemption amounts adjust every three years (CPLR 5253) | Accept |
| NY:ADJ-tenant-deposit-claim-limitations; NY:CPLR-213(2) | CPLR 202 borrowing statute for non-resident plaintiffs | Accept, after sources in condition 1 |
| NY:CPLR-321-JUD-495-appearance | Tenant suing a corporate owner in small claims: owner may appear by its officer or employee (CCA 1809(2)) | Accept |
| NYC:HMC-27-2135(c)-receiver-rents | The 27-2148 lien receiver reaches one- and two-family houses | Accept |
| NY:ADJ-lease-break-charge; walk 3.3, 5.2, 5.4 | NYC Admin. Code 26-3402 caps vacating charges | Accept, subject to condition 2 |
| NYC:HMC-27-2017.5-turnover; NYC:HMC-27-2013(a); NYC:PAINT-wear-and-tear | Owner pest duty in every dwelling (27-2017.1); written-lease repair shift in one- and two-family houses (27-2005(c)) | Accept |
| NYC:HMC-27-2045-detector-charge | Class B buildings | Accept |
| US:24CFR92.253(b)(2) deferral | HRA HOME tenant-based rental assistance in a private unit is in the aperture, like CityFHEPS | Accept; move out of the deferred list |
| US:11USC524(a)(2); US:FRBP-3002(c)-claim-deadline | Contempt sanction; 524(c), (e), (f) branches; chapter 7 tardy claims paid third | Accept |
| US:24CFR100.65-terms; US:15USC7001(c)-esign-consent; US:50USC4042 | 3603(b) exemptions; consent owed only to a consumer; 4041 penalties and 4043 | Accept |

## Jev on sections it was not tuned on

| Tier | Decides something | Does not |
|---|---|---|
| strong | 44 | 19 |
| likely | 359 | 359 |
| possible | 152 | 739 |
| low-confidence only | 62 | 656 |
| long or unscored | 41 | 67 |

Five deciding sections had scores that would have set them aside had Jev been confident (RPL 442-C, 15 USC 7006,
STT 302, Admin. Code 26-3001, 27-2017): 5 of 49 queued sections with set-aside-like scores. So the 876 set-aside
sections are reviewed too (batches 7-8, register/work/batch_7.json, batch_8.json). Jev's score orders the work well
but does not by itself close completeness.

## Next

1. Batches 7-8 report; adjudicate their proposals the same way.
2. On Owen's go: save the authorities in condition 1; apply all accepted rules by script with backups
   (build/apply_register_*.py); integrate into the walk; set every register section's status from the decisions;
   check_register.py fails on any section without a reviewer decision.
3. Round 6: 6A reviews the register's instrument list and a sample of no_decision rulings; 6B reviews correctness of
   every rule added or changed since round 5.

## Batches 7-8: the 876 sections Jev set aside (2026-09-30)

check_decisions.py all: 3,374/3,374 sections decided across batches 1-8, 0 errors, no id collisions.
14 set-aside sections decide something (1.6%): 7 in batch 7, 7 in batch 8. Every one had Jev P(DECIDES) <= 0.05,
and 11 of 14 are entity-capacity law (whether an owner entity may sue, or winds up). Proposed rules: 14 (1 critical:
NY:PTR-121-201-lp-publication, text verified in register/texts/NY_PTR/121-201.txt).

Ruling: accept all 14, with two conditions at apply time.
1. Rules whose dependencies were listed as existing equivalents because the checker accepts only existing ids
   (batch 8 on NY:NPCL-1313-foreign-authority, NY:PTR-121-1502-foreign-llp, NY:PTR-121-104-a-process-address-
   suspension) are re-pointed to the accepted queue proposals.
2. NY:CCA-2101(g)-balance-venue-current states today's Civil Court venue for a balance suit, which the queue proposal
   NY:CCA-305-venue-residence assumed; the two are reconciled into one venue rule set (current, and from S9760's
   effective date).
Existing-rule findings: NY:BCL-1312(a)-foreign-authority and NY:LLC-808(a)-foreign-authority gain the statutory
'doing business' exclusions (BCL 1301, LLC 803); NY:GBL-130-assumed-name gains the BCL 1301(d) carve-out;
NY:HANDOFF-broker-config-under-broker gains the 19 NYCRR 175.21 supervision condition; NYC:ADC-20-490 gains the
20-105 daily fine. Close calls decided no_decision (Partnership Law 121-303, 121-403, RPL 442-A, SCPA 2108,
6 RCNY 5-42) stand.

Jev result on untuned sections: its set-aside list was 98.4% right, but its misses cluster in one family (entity
capacity), so a set-aside list is reviewed, not accepted, in every future register.
