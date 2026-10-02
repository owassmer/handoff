# Review 1, round 5: disposition of the independent reviews

2026-09-30. Findings: review/INDEPENDENT_REVIEW_5A.md (completeness: 41 gaps, 14 critical, 10 major, 17 minor; one
over-scope group) and review/INDEPENDENT_REVIEW_5B.md (correctness: 10 findings, 4 critical, 2 major, 4 minor).
ir5a_verify.py (344 quotes) and ir5b_verify.py (40 quotes) pass. Owen chose option a: apply, then build the source
register and classify every section, with Jev triaging.

Changes: build/apply_review5_1.py (5B), _2.py and _2b.py (5A critical), _3.py (5A major and minor), _4.py (walk).
New rules quote the reviewer's verified evidence by index from independent_review_5a.json (build/r5lib.py), and every
figure a rule states beyond its quote is asserted against the saved source at run time. Backups:
build/backups/*_pre_review5.json, NYC_MARKET_RATE_pre_review5.md.

## Rulings that differ from the reviewers

| Finding | Ruling | Why |
|---|---|---|
| R5A-01 E-SIGN consent (critical) | Modify | E-SIGN 7001(c) applies where a rule of law requires information "in writing". GOL 7-108(1-a)(e) requires an "itemized statement" with no writing words, unlike (1-a)(c) and (d); the writing requirement comes from Bogom-Shanon, which accepts email and text. New `NY:ADJ-statement-electronic` (statement by email or text needs no E-SIGN consent) and `US:15USC7001(c)-esign-consent` (applies to the (1-a)(d) inspection notices and other "in writing" notices; eviction and cure notices go on paper). |
| R5A-41 S450/A659 (minor) | No rule | Not passed by both houses in one year: Senate 2025-05-13, Assembly 2026-05-05, then referred to committee in the Senate on 2026-05-28. It concerns only 421-a units, which are stabilized and routed to Review 2. |

All other findings are accepted as stated.

## Correctness (5B)

| Finding | Change |
|---|---|
| R5B-01 vacate order, installment already paid (critical) | `NY:ADJ-vacate-order-rent` (Kennedy, Strasburger); walk 3.6, T-vacate: 10/31 of March earned, 21/31 refunded, damages claim |
| R5B-02 RPL 227 sudden casualty (critical) | `NY:RPL-227` (Suydam, Warrin); walk 2.6 |
| R5B-03 pre-sale rent is the seller's (critical) | `NY:RPL-223` (Getty Realty); walk 2.1, C10 |
| R5B-04 tenant's claims extended by 108(a) (critical) | `NY:ADJ-tenant-deposit-claim-limitations`; new `US:11USC108(a)-debtor-claims`; walk 7.6 |
| R5B-05 RPAPL 1305 limits (major) | `NY:RPAPL-1305-successor` |
| R5B-06 refund with only an email (major) | `NY:ADJ-provide-address-branches`; walk C3 |
| R5B-07 use and occupancy is not rent (minor) | `NY:HANDOFF-broker-config-collection-agency` |
| R5B-08 willfulness label (minor) | `NY:ADJ-willful-standard` judgment terms |
| R5B-09 detector reimbursement (minor) | `NYC:HMC-27-2045-detector-charge`; walk 5.5a, T-lead |
| R5B-10 new lease ends the old at market or agreed rate (minor) | Walk 3.3 |

## Completeness (5A)

| Findings | New rules | Walk |
|---|---|---|
| R5A-01 | `NY:ADJ-statement-electronic`, `US:15USC7001(c)-esign-consent` | 4.1, 6.4 |
| R5A-02 | `NY:GBL-349-unfair-abusive` | 5.10 |
| R5A-03 | `NY:JUD-489-champerty` | 8.1b |
| R5A-04 | `NY:SSL-143-b(5)-rent-bar` | 8.10 |
| R5A-05 | `NY:RPAPL-768-853-unlawful-eviction` | 3.7, 6.9 |
| R5A-06 | `US:47USC227-TCPA` | 8.3 |
| R5A-07 | `NY:GOL-15-104-105-cotenant-release` | 8.1b |
| R5A-08 | `NY:UCC-1-308-full-payment-check` | 8.1b |
| R5A-09 | `NY:16NYCRR96-submetering` | 5.5a |
| R5A-10 | `US:FRBP-3002(c)-claim-deadline` | 8.8 |
| R5A-11 | `NY:RPAPL-749(3)-after-proceeding` | 3.8 |
| R5A-12 | `NY:MDL-302-c-fuel-credit` | 5.5a |
| R5A-13 | `US:24CFR100.7-3617-liability` | 5.10 |
| R5A-14 | `NY:GBL-899-aa-breach-notice` | 6.10 |
| R5A-15 to R5A-24 | `NY:RPL-223-b-retaliation`, `NY:GOL-5-703-15-301-early-termination`, `NY:GOL-17-103-limitations-promise`, `NY:CPLR-321-JUD-495-appearance`, `NY:GBL-130-assumed-name`, `NY:CPLR-5020-satisfaction`, `NY:CPLR-5205-5231-enforcement-limits`, `NY:GBL-399-h-disposal`, `US:34USC12491-VAWA`, `US:15USC1681b-1681c-report-limits` | 3.3, 3.8, 6.10, 8.1b, 8.7, 8.10, 8.12, 0.6 |
| R5A-25 to R5A-40 | `NY:RPL-218-waiver-void`, `NY:RPL-441-c-licence-discipline`, `NY:RPAPL-744-dv-removal`, `NY:22NYCRR-208.42(g)-registration-plea`, `NY:MDL-51-c-tenant-lock`, `NY:CPLR-204-208-tolling`, `NY:CPLR-1203-1015-5208-parties`, `NY:CPLR-5003-a-settlement-payment`, `NY:GBL-399-ddd-604-a`, `NY:ABP-1400-1412-reporting`, `NY:MIL-306-309`, `NY:EXC-297(9)-remedies`, `NYC:ADC-26-3003-3006-data-sale`, `US:26CFR1.166-1(e)-bad-debt`, `NY:RPAPL-741(5-a)-231-c-notice`, `NY:GOL-5-702-plain-language` | 3.8, 5.5a, 5.10, 6.8, 6.10, 7.6, 8.6, 8.9, 8.10, 8.11 |
| Over-scope: 28 RCNY ch. 1 and HPD escrow rules | Deferred to Review 2; Article VIII buildings route out at 0.6 via `NYC:RCL-26-403(e)(1)(c)` | 0.6, 5.8 |

## Checks after the changes

stage_a_check.py: 0 errors across NY (291 rules), NYC (201), VA (277), US (198); cross-file 0.
check_review.py: 593 in scope, 490 cited, 103 deferred, 0 missing.

## Convergence record

| Round | Correctness findings (critical) | Completeness gaps (critical) | Blind-list overlap |
|---|---|---|---|
| 4 | 15 (3) | 34 (9) | - |
| 5 | 10 (4) | 41 (14) | 148 shared; 116 only in 5A, 27 only in 4A |

Correctness is converging. Completeness is not, because each reviewer draws the boundary. Next: the source register
(register/), in which every section of every in-scope instrument is classified, with Jev triaging sections that no
rule states.
