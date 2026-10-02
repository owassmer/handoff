# Review 1, round 2: disposition of the independent review

2026-09-29. Findings: review/INDEPENDENT_REVIEW_2.md (13 findings, 27 confirmations; "accept after listed
corrections"). ir2_verify.py passes (39 quotes, 103 rule ids, self-test). Ferro read the source text behind every
critical and major finding and brought the adjudication to Owen before any edit; Owen approved it (option a).
Changes: build/apply_review2.py (backups build/backups/*_pre_review2.json, NYC_MARKET_RATE_pre_review2.md).

| Finding | Ruling | Verified against | Change |
|---|---|---|---|
| R2-01 certificate of occupancy (critical) | Accept; Ferro adds that keeping the deposit for barred rent is recovering it | MDL 4(7), 301(1), 302(1)(b); Caldwell (2d Dept); 49 Bleecker (1st Dept); Chazon (CoA); GOL 7-103(1) | New `NY:MDL-4(7)-multiple-dwelling`, `NY:MDL-301(1)`, `NY:MDL-302(1)(b)`; walk 0.5, 5.5, C4, C7, C14 |
| R2-02 pending three-year limit (critical) | Accept as a dated future change; current law six years | Assembly record: passed Senate 2026-06-02, Assembly 2026-06-03, no delivery to Governor; nysenate.gov status box stale | New `NY:CPLR-214-i-consumer-debt-S9760`; `NY:ADJ-lease-balance-not-consumer-credit` notes it; walk 8.1, C14 |
| R2-03 registration bar (major) | Accept | MDL 325(2) | New `NY:MDL-325(2)`; `NYC:ADC-27-2107(b)-rent-stay` limited to one- and two-family houses; walk 0.5, 8.10, C10 |
| R2-04 Good Cause exemptions (major) | Accept | RPL 214(1)-(15) | `NY:RPL-214` lists all fifteen; new `NY:RPL-214(15)-high-rent`; walk 3.1 |
| R2-05 willful (major) | Accept with reconciliation: two parts (deliberate failure; knowledge of law charged to professionals) | Karole (both lines); Prando | `NY:ADJ-willful-standard` effect, construction, reasoning; walk 7.5 |
| R2-06 lease-break charges (major) | Accept | JMD Holding (CoA); RPL 227-e | New `NY:ADJ-lease-break-charge`; walk 3.3, C6 |
| R2-07 rent after early move-out (major) | Accept | GOL 7-108(1-a); Kunik (App Term 2d) | New `NY:ADJ-early-departure-rent-retention`; walk 5.5, C6 |
| R2-08 RPL 232 (minor) | Accept; one point to settle first: whether a monthly rent term specifies duration | RPL 232 text | Assigned to the building-and-owner sweep |
| R2-09 ABP 1422 (minor) | Accept | ABP 1422 | New `NY:ABP-1422`; walk 6.8, C9 |
| R2-10 23 NYCRR Part 1 (minor) | Accept | 23 NYCRR 1.1(d) | New `NY:23NYCRR-1.1(d)-not-lease`; walk 8.1 |
| R2-11 small claims exception (minor) | Accept | CPLR 3215(g)(3)(iii) | `NY:CPLR-3215(g)(3)` effect, construction; walk 8.9 |
| R2-12 HPD source urls (minor) | Accept | Saved XML section ids | Both HPD rules repointed |
| R2-13 walk alignment (minor) | Accept | Walk text | Provenance sentence removed; Step 1 renumbered |
| F-01 rent-impairing violations (Ferro) | Add; missed by both reviews | MDL 302-a(3) text (saved sources/NY_MDL_302-A_nysenate.txt) | New `NY:MDL-302-a(3)`; walk 0.5, C7, C14 |

Round-one corrections: Ferro agrees with all 17 of the reviewer's verdicts (13 complete; R1-05, R1-06 and R1-13
completed by R2-03, R2-04 and R2-11; R1-10 over-corrected and fixed by R2-05).

Pattern: both rounds found gaps at the edge of the chain, not in its core. They cluster in one family the
deposit-outward discovery does not reach: facts about the building and owner that bar or condition rent recovery.
That family gets a targeted sweep, then a third review limited to the changes and the family.

Checks after the changes: stage_a_check.py 0 errors across NY, NYC, VA, US (NY.json 201 atoms, NYC.json 185);
check_review.py 465 in scope, 370 cited, 95 deferred, 0 missing.
