# Review 1, round 3: disposition of the independent review

2026-09-29. Findings: review/INDEPENDENT_REVIEW_3.md (14 findings: 6 critical, 3 major, 5 minor; 26 confirmations).
ir3_verify.py passes (49 quotes). Ferro read the source text behind every critical finding and the RPL 232 conflict.
Owen approved applying all 14, then a full fourth review including a new search for missing law (option c).
Changes: build/apply_review3.py (backups build/backups/*_pre_review3.json, NYC_MARKET_RATE_pre_review3.md).

| Finding | Ruling | Verified against | Change |
|---|---|---|---|
| R3-01 RPL 232 (critical) | Accept; reverses the sweep's ruling | Spies ("If nothing had been said concerning the term ... a tenancy for a month only"); Gerolemou (App Term 2d); Stauber did not decide it | `NY:ADJ-RPL-232-monthly-letting` now the bare-monthly-rent presumption (Gerolemou base); `NY:ADJ-RPL-232-indefinite-term` limited to a contemplated longer stay (Spies base); `NY:RPL-232` condition; walk 3.2a, T-232; NY case walks C4, C6 |
| R3-02 MDL 301 exceptions (critical) | Accept | MDL 301(1)(a)-(b), 301(2) | `NY:MDL-301(1)`, `NY:MDL-302(1)(b)`; walk 0.5, C4, C7 |
| R3-03 registration is a suspension (critical) | Accept | 9 Montague Terrace (App Term 2d) | `NY:MDL-325(2)`, `NYC:ADC-27-2107(b)-rent-stay`; walk 0.5, 8.10, C4, C7 |
| R3-04 MDL 302-a exceptions (critical) | Accept | MDL 302-a(3)(c)-(e) | `NY:MDL-302-a(3)` now MIXED with the exceptions; walk 0.5 |
| R3-05 C14 broker licence (critical) | Accept | RPL 440, 442-f | Walk C14 |
| R3-06 unlicensed collection cost (critical) | Accept | G.C. Fortune (3d Dept); RPL 442-e | `NY:RPL-442-d-442-e-unlicensed` (MIXED, dominant-feature test); `NY:HANDOFF-broker-config-collects-rent` |
| R3-07 S9760 procedure (major) | Accept as dated future atoms | Bill ss. 2, 8-10, 12, 13, 15, 17; Assembly actions (last 2026-06-03, returned to senate) | New `NY:S9760-pleading-service`, `-notice-mailings`, `-venue`, `-default-judgment`; walk C14 |
| R3-08 foreign owner capacity (major) | Accept | LLC Law 808; BCL 1312; S. Garson (2d Dept 2026); 1700 First Ave (App Term 1st) | New `NY:LLC-808(a)-foreign-authority`, `NY:BCL-1312(a)-foreign-authority`, `NY:LLC-206-publication-not-bar`; walk 8.10 |
| R3-09 loft-law routing (major) | Accept | MDL 285(1) | New `NY:MDL-285(1)-loft-law`; walk 0.5 |
| R3-10 willful and the missing address (minor) | Accept, reworded: a manager's deliberate wait is willful; Prando stays an individual-owner finding | Prando; Karole | `NY:ADJ-willful-standard`, `NY:ADJ-provide-address-branches`; walk 6.5, 7.5; NY case walk C9 |
| R3-11 vacate order partial month (minor) | Accept | Younger v Campbell | `NY:ADJ-vacate-order-rent`; walk T-vacate |
| R3-12 detectors battery-only (minor) | Accept | Admin. Code 27-2045 | `NYC:HMC-27-2045-detector-charge`; walk 5.5a |
| R3-13 ABP 1422 cost (minor) | Accept | ABP 1422(4) | `NY:ABP-1422`; walk 6.8 |
| R3-14 provenance (minor) | Accept | Saved pages | 23 NYCRR source_url; Farmers' Loan re-saved from CourtListener and repointed |

Earlier rounds: Ferro agrees with the reviewer. R2-08's premise was wrong (source of the RPL 232 error); R2-03's C4
wording overstated registration; the loft-law exception proposed in round 2 had been dropped and is now restored.

Checks after the changes: stage_a_check.py 0 errors across NY (233 atoms), NYC (192), VA (277), US (179), cross-file 0;
check_review.py 507 in scope, 412 cited, 95 deferred, 0 missing.

Next: full fourth review (Owen, option c), split into a blind enumeration of the applicable-law universe and a fidelity
review of every in-scope rule.
