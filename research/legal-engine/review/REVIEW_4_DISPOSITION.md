# Review 1, round 4: disposition of the independent reviews

2026-09-29. Findings: review/INDEPENDENT_REVIEW_4A.md (completeness: 34 gaps, 9 critical, 15 major, 10 minor; 1
over-scope group) and review/INDEPENDENT_REVIEW_4B.md (correctness: 15 findings, 3 critical, 3 major, 9 minor).
ir4a_verify.py (237 quotes) and ir4b_verify.py (43 quotes) pass. Ferro read the source text behind every critical
finding. Owen chose option c: apply all findings, then a full two-part fifth review.

Changes: build/apply_review4_1.py (existing rules), _2.py (new state rules), _3.py (new federal and city rules),
_4.py (walk), _5.py (remaining weight labels). Shared helpers: build/r4lib.py. Every statement a new rule makes beyond
its quote is asserted against the saved source at run time (must()). Backups: build/backups/*_pre_review4.json,
NYC_MARKET_RATE_pre_review4.md.

## Correctness (4B)

| Finding | Ruling | Change |
|---|---|---|
| R4B-01 owner bankruptcy, tracing (critical) | Accept | `US:11USC541-704-owner-chapter7`, `US:11USC1107-1306-owner-reorganization` (Trafalgar); walk 0.5 |
| R4B-02 co-op/condo conversion (critical) | Accept | Walk 0.1 |
| R4B-03 willfulness (critical) | Accept; reverses Ferro's round-3 R3-10 rewording | `NY:ADJ-willful-standard`, `NY:ADJ-provide-address-branches`, NY case walk C9; walk 6.5, 7.5 |
| R4B-04 LLC publication (major) | Accept | `NY:LLC-206-publication-not-bar` replaced by `NY:LLC-206-publication-suspension` (Small Step, 2d Dept); walk 8.10 |
| R4B-05 commercial claims eligibility (major) | Accept | New `NY:CCA-1801-A(a)-eligibility`; `NY:CCA-1809(1)`, `NY:CCA-1803-A(b)`; walk 8.10 |
| R4B-06 temporary CO; combined apartments (major) | Accept | `NY:MDL-301(1)`, `NY:MDL-302(1)(b)`; walk 0.5 |
| R4B-07 voluntary payment while unregistered | Accept | `NY:MDL-325(2)`; walk 0.5 |
| R4B-08 city stay reaches multiple dwellings | Accept; reverses round-2 limit | `NYC:ADC-27-2107(b)-rent-stay`, `NYC:ADC-27-2097-registration`, `NY:MDL-325(2)` |
| R4B-09 common-area violation | Accept | Walk 0.5 |
| R4B-10 SHIELD 60-day channel | Accept | Walk 8.5 |
| R4B-11 T-vacate apportionment | Accept; unsupported day count removed | `NY:ADJ-vacate-order-rent`; walk T-vacate. Whether rent paid for the days after the order is refunded goes to review 5B for adjudication with authority. |
| R4B-12 C10 building type | Accept | Walk C10 |
| R4B-13 S9760 status | Accept | Walk 8.1 |
| R4B-14 421-a route | Accept | Walk 0.1 |
| R4B-15 hedges and weight labels | Accept | Walk 0.4, 8.3; `NYC:ADC-20-489(a)`, `US:15USC1692g(b)`, `US:15USC1692a(5)`, `US:15USC1692n`, `NYC:CASE-Middleton-stabilized-deposit`; instrument labels stripped |

## Completeness (4A)

| Finding | Ruling | New or changed rules |
|---|---|---|
| R4A-01 FARE landlord's agent (critical) | Accept | New `NYC:FARE-20-699.21-agent-fee-ban`; `NYC:FARE-moveout-service-fee` limited to the landlord's own fees; walk 5.4 |
| R4A-02 coerced debt (critical) | Accept | New `NY:GBL-604-bb-coerced-debt`, `NY:GBL-604-cc-coerced-defense`; walk 8.1a |
| R4A-03 tenant's death (critical) | Accept | New `NY:ADJ-tenant-death-payee`, `NY:CPLR-210-death`; walk 2.5 |
| R4A-04 tolling (critical) | Accept | New `US:50USC3936-tolling`, `US:11USC108(c)-extension`, `NY:GOL-17-101-acknowledgment`; walk 8.10 |
| R4A-05 tenant's time to sue (critical) | Accept | New `NY:ADJ-tenant-deposit-claim-limitations`; walk 7.6 |
| R4A-06 chapter 13 co-debtor stay (critical) | Accept | New `US:11USC1301-codebtor-stay`; walk 8.8 |
| R4A-07 lessor claim cap (critical) | Accept | New `US:11USC502(b)(6)-lessor-cap`; walk 8.8 |
| R4A-08 6% servicemember cap (critical) | Accept | New `US:50USC3937-6pct`, `NY:MIL-323-a-6pct`; walk 8.10 |
| R4A-09 surrender by operation of law (critical) | Accept | New `NY:CASE-Riverside-surrender-by-operation`; walk 3.3 |
| R4A-10 GBL 601 via 6 RCNY 5-77 | Accept; narrows round-1 deferral | New `NYC:RCNY6-5-77(d)(17)-GBL601`, `NYC:RCNY6-5-77(e)(8)-GBL601`; walk 8.4; deferred-list note |
| R4A-11 SHIELD credit-report notice | Accept | New `NYC:SHIELD-5-77(e)(10)-credit-report-notice`; walk 8.5 |
| R4A-12 Avila | Accept | New `US:CASE-Avila-accruing-balance`; walk 8.3 |
| R4A-13 CPLR 3215(j) | Accept | New `NY:CPLR-3215(j)-sol-affidavit`; walk 8.9 |
| R4A-14 CPLR 4544 | Accept | New `NY:CPLR-4544-small-print`; walk 5.2 |
| R4A-15 broker escrow | Accept | New `NY:19NYCRR-175.1-broker-escrow`; walk 1.2 |
| R4A-16 RPL 238-a(1) | Accept | New `NY:RPL-238-a(1)-no-move-in-fees`; walk 1.4 |
| R4A-17 guarantor | Accept | New `NY:GOL-5-701(a)(2)-guaranty`; walk 8.1 |
| R4A-18 anti-discrimination | Accept | New `US:24CFR100.65-terms`, `NY:EXEC-296(5)(a)(2)-terms`, `NYC:ADC-8-107(5)(a)-terms`, `NY:RPL-227-d-dv-status`; walk 5.10 |
| R4A-19 1099-INT | Accept | New `US:26USC6049-deposit-interest`; walk 5.6 |
| R4A-20 smart-access data | Accept | New `NYC:ADC-26-3002(c)-moveout-data`; walk 6.10. It binds the owner and a third party running the system, not every holder of tenant records. |
| R4A-21 licensed agency rules | Accept | New `NYC:RCNY6-2-192-payment-plan`, `NYC:RCNY6-2-193-records`; walk 8.6 |
| R4A-22 foreclosure successor | Accept, narrowed: the reviewer's rule that rent paid to the former landlord's representative before notice is no default is not in the saved text and is omitted | New `NY:RPAPL-1305-successor`; walk 0.5 |
| R4A-23 S947 pending | Accept | New `NY:S947-ach-fee-ban`; walk 1.8 |
| R4A-24 chapter 7 deemed rejection | Accept | New `US:11USC365(d)(1)-ch7-rejection`; walk 8.8 |
| R4A-25 owner tax | Accept | New `US:IRS-Pub527-deposit-income`, `US:26USC6050P-no-1099C`; walk 8.11 |
| R4A-26 CCA 1812 | Accept | New `NY:CCA-1812-treble`; walk 7.6 |
| R4A-27 tenant small claims | Accept | New `NY:CCA-1801-tenant-claim`; walk 7.6 |
| R4A-28 LeRoy | Accept | `NY:CASE-Paterno-commingling-forfeiture`; walk 7.3 |
| R4A-29 Graham Court | Accept | `NY:RPL-234`; walk 5.2 |
| R4A-30 GBL 601-a | Accept | New `NY:GBL-601-a-family`; walk 8.4 |
| R4A-31 TR04 | Accept | New `NY:OSC-TR04-broker-escrow`; walk 6.8 |
| R4A-32 data security | Accept | New `NY:GBL-899-bb-safeguards`; walk 6.10 |
| R4A-33 RPL 235-bb | Accept | New `NY:RPL-235-bb-co-notice`; walk 0.5 |
| R4A-34 Military Law 303(3) | Accept | New `NY:MIL-303(3)`; walk 8.9 |
| Over-scope: project-based voucher rules | Accept | Walk 5.7 line removed; three rules moved to the later-review deferred list |

## Checks after the changes

stage_a_check.py: 0 errors across NY (258 rules), NYC (200), VA (277), US (190); cross-file 0.
check_review.py: 551 in scope, 453 cited, 98 deferred, 0 missing.

## Convergence record

| Round | Scope | Findings | Critical | New law found |
|---|---|---|---|---|
| 1 | whole walk | 17 | 4 | - |
| 2 | whole walk | 13 | 2 | building/owner family |
| 3 | round-2 changes + sweep | 14 | 6 | 3 major |
| 4 | blind universe (176 items) + whole walk | 49 | 12 | 34 gaps |

Round 5 repeats round 4's design. It measures convergence directly: 5A compares its own blind universe with 4A's
176 items only after saving it, and reports items neither 4A nor the files contain.
