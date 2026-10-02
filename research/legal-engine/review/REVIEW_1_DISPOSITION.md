# Review 1: disposition of the independent review

2026-09-28. Findings: review/INDEPENDENT_REVIEW_1.md (17 findings, 30 confirmations; judgment "accept after listed
corrections"). The reviewer's evidence check (review/ir1_verify.py) passes: 47 quotes, 0 failures. Ferro read the
source text behind each critical and major finding before applying it. All 17 are accepted and applied. Rule changes
are in build/apply_review1.py (backups in build/backups/*_pre_review1.json and NYC_MARKET_RATE_pre_review1.md).

| Finding | Severity | Verified against | Change |
|---|---|---|---|
| R1-01 interest on the balance | critical | CPLR 5004(a)-(b) text; L.2021 c.831 s.7; Allen v Whidbee; CPLR 5001; NML Capital (Court of Appeals) on contract rates | New `NY:CPLR-5001(a)-(b)`, `NY:CPLR-5004(a)-consumer-2pct`, `NY:CASE-NML-contract-rate`, `NY:ADJ-lease-interest-on-rent`; review 8.10, C7, C14 |
| R1-02 automatic renewal | critical | GOL 5-905 text | New `NY:GOL-5-905`; review 3.1, C6 |
| R1-03 co-tenant payee | critical | Holmes majority and dissent; GOL 7-103(1); Lasky (words of severance) | `NY:ADJ-cotenants-payee` rewritten in two branches; review 6.6, C8; NY case walk C8 |
| R1-04 refund payee after bankruptcy | critical | 11 U.S.C. 541(a)(1), 542(b), 542(c), 1306(b) | New `US:11USC542-refund-payee`; `US:CASE-Strumpf-hold` repointed; review 6.7, C15; US case walk |
| R1-05 HPD registration | major | Admin. Code 27-2097(b)(1), (3); 27-2107(b) | New `NYC:ADC-27-2097-registration`, `NYC:ADC-27-2107(b)-rent-stay`; review 1.8, 8.10, C4, C7, C14 |
| R1-06 Good Cause Eviction | major | RPL 212, 214, 215, 216(1); RPL 211(3) (Justia; nysenate.gov returns "not found") | New `NY:RPL-212`, `NY:RPL-211(3)-small-landlord`, `NY:RPL-214`, `NY:RPL-215`; review 3.1 |
| R1-07 painting outside multiple dwellings | minor | Admin. Code 27-2013(a) | New `NYC:HMC-27-2013(a)`; `NYC:PAINT-wear-and-tear` extended; review 1.5, 5.3 |
| R1-08 RPL 236 silence | minor | RPL 236 text | Review 2.5 |
| R1-09 advance rent | minor | GOL 7-108(1-a)(a); Attorney General guide | `NY:GOL-7-108(1-a)(a)` effect, construction, reasoning; review 1.1 |
| R1-10 willfulness wording | minor | Bogom-Shanon; Masseroli; the rule's own text | Review 7.5 |
| R1-11 C3 refund method | minor | GOL 7-108(1-a)(e) "return" | Review C3 |
| R1-12 phone limb | minor | Bogom-Shanon ("text"); Pickens | `NY:ADJ-provide-address-branches` effect, construction, reasoning; review 6.5 |
| R1-13 default-judgment mailing | minor | CPLR 3215(g)(3) (Justia; nysenate.gov returns "not found") | New `NY:CPLR-3215(g)(3)`; review 8.9 |
| R1-14 small and commercial claims | minor | CCA 1809(1), 1801-A(b), 1803-A(b) | New `NY:CCA-1809(1)`, `NY:CCA-1801-A(b)`, `NY:CCA-1803-A(b)`; review 8.10 |
| R1-15 over-scope in the walk | minor | GBL 600(1); Van Rensselaer; ABP 1310 text | 17 rules moved to the review's deferred list; one sentence kept for each point |
| R1-16 weight warnings | minor | Owen's standing ruling | "Lighter authority" section and "No appellate court" sentence removed; 8.1 states the controlling authority |
| R1-17 unofficial sources | minor | Official copies saved and quotes re-verified | Gelbart (nycourts.gov), RPL 235-b and GCN 35 (nysenate.gov), Mabe and Van Rensselaer (CourtListener); 9 references repointed |

Also applied from the confirmed list: Srinivasan v Silvi (Appellate Term, Second Department) added as an authority
for `NY:COMMONLAW-NYC-monthly-tenant-surrender`, so the rule rests on both Appellate Terms.

Two sources remain on an unofficial compilation because the official site does not serve them: RPL 211 and CPLR 3215
(both Justia). Each rule's instrument field says so.

Checks after the changes:
- stage_a_check.py across NY, NYC, VA and US: 0 errors, cross-file 0 errors.
- review/check_review.py: 454 rules in scope, 359 cited, 95 deferred, 0 missing.
