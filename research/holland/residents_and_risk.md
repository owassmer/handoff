# Holland resident evidence and settlement risk

Reconciled 2026-09-30. This replaces the interrupted 49-item narrative. The evidence supports specific settlement-process failures and investigation questions; it does not establish Holland's overall dispute rate, systematic illegality, or the merits of every charge. Current portfolio attribution uses `communities.json`; historical management is established only where the individual record supplies it.

## What the completed recovery establishes

`reviews.json` contains **60 selected source records**: 28 full BBB records, three full archived apartments.com reviews, and 29 residual search-index excerpts. Forty-three have an absolute publication-date prefix; 17 remain undated with an explicit explanation. Publication, move-out and archive-capture dates are separate concepts. Some absolute dates are approximate years rather than days.

The original dataset had 49 records. Recovery replaced 20 legacy records with fuller originals, including merging two excerpts of the same BBB complaint. Thirty-one original records were admitted, yielding 60 total. All 60 resident quotations and all response excerpts from full captures pass checks against saved text. Partial search excerpts remain identified as such; passing a quote check establishes transcription fidelity, not the truth of an allegation.

There are **44 records naming 24 of the current 61 communities**, three about named properties outside that list (two Fountain Plaza, one Overlook of Lakemont), two with uncertain current-property attribution, and 11 unidentified properties. The Flats attribution is inferred, and the masked Preserve could refer to either of two communities; neither enters the named-community count. The remaining 37 current communities have no admitted record in this sample, which says nothing about their performance.

**These are 60 source records, not 60 verified unique cases.** Names are intentionally omitted; household and cross-platform linkage cannot be established. Known snippet duplication has been removed. Two November 2023 Lydian BBB complaints have different narratives but very similar management replies: one concerns post-move-out collections, the other excess rent before move-out. The second reply's linkage is unresolved, so it is not counted as another collections allegation. See `reviews_summary.json` for reproducible counts and the row-level `case_identity`, `record_id` and attribution fields.

## The most useful evidence is in the full business replies

| Record | Resident's allegation | Business response and observed disposition | What can be concluded |
|---|---|---|---|
| [Unnamed property, December 2025](sources/reviews/bbb/complaint_1296_27031141_24230744.txt) | Painting invoice lacked a breakdown and depreciation detail; cleaning and hardware responsibility disputed. | Management acknowledged that the wear-and-tear allowance had been applied incorrectly, proposed an adjustment, then waived painting and cleaning. Consumer accepted the resolution. | A specific acknowledged calculation/treatment error and a documented resolution. The waiver alone does not decide the lawfulness of every original charge. |
| [Masked Preserve, June 2026](sources/reviews/bbb/complaint_1296_27031141_24959214.txt) | Portal demanded $6,782.66 despite a revised $973.66 balance after re-rental. | Management said its collector had apparently not received or updated the corrected amount. Consumer confirmed the payment site was updated and intended to pay. | A documented mismatch between the site's corrected account and collections/payment records. Exact property and state remain unresolved. |
| [Flats, February–April 2026](sources/reviews/bbb/complaint_1296_27031141_24562446.txt) | Collection contact resumed despite written zero-balance confirmation. | Management confirmed prior reversals and work with Central Billing, later asserted closure. Consumer continued requesting satisfactory closure documentation through April 24. | Central Billing coordination and proof of closure are distinct work. An asserted closed account is not a mutually accepted resolution in this record. Deposit amount remains disputed. |
| [Fountain Plaza, August 2025](sources/reviews/bbb/complaint_1296_27031141_23739658.txt) | No statement or refund received within the asserted deadline. | Management said the statement had been prepared and check mailed, but the statement was not emailed as intended. | An admitted delivery-process failure; whether legally sufficient delivery otherwise occurred requires the underlying delivery records and governing law. |
| [Unnamed Seattle property, March 2026](sources/reviews/bbb/complaint_1296_27031141_24622310.txt) | Cleaning/hardware charges disputed; portal allegedly prevented partial payment. | Management acknowledged the bathroom portion of the move-in inspection was missing and refunded the deposit while retaining disputed charges. | Missing baseline evidence is admitted. The record does not establish the ultimate legal validity of the retained charges or the technical portal behavior. |
| [Lydian, September 2024](sources/reviews/bbb/complaint_1296_27031141_22357176.txt) | Painting/damage deduction disputed as pre-existing condition. | Business described repainting after a year as typical even without visible damage and referred to natural wear. | The business's stated rationale deserves case-level examination against the applicable rule and evidence. This is not a finding about every Holland property. |
| [Lydian, March 2026](sources/reviews/bbb/review_1296_27031141_856292.txt) | Thin itemization, unanswered contact and collection referral. | Business asserted supporting documentation was provided, then waived cleaning as a courtesy. | Evidence sufficiency is disputed. Courtesy waiver proves the disposition, not that the original charge was indefensible. |

Replies expose named handoffs among on-site management, regional management, accounting/Central Billing and outside collectors. A third-party utility biller appears in older evidence. The Seattle resident names Bilt; that single report does not establish the entire portfolio's payment configuration.

## Descriptive themes, with the right denominator

Counts below are over all 60 selected records, including former and unidentified properties. Themes overlap and include positive references: JUXT's expected cleaning fee contributes to `cleaning_charge`. These are not complaint rates or counts of confirmed violations.

| Theme | Records |
|---|---:|
| Cleaning charge | 26 |
| Deposit withheld | 21 |
| Paint charge | 14 |
| Itemization/documentation | 10 |
| Collections/credit reporting | 9 |
| Lease-break/notice | 9 |
| Carpet charge | 8 |
| Refund delay | 7 |
| Recurring fees | 7 |
| Billing error | 6 |
| Final utility bill | 6 |
| Application/holding deposit | 5 |
| Statement timing | 5 |
| Positive move-out | 3 |

The full theme dictionary and counts restricted to named current communities are in `reviews_summary.json`. The archive recovery supplies an important counterexample: [Inspiration, December 2020](sources/reviews/wayback/inspiration__apartments.com_20251026101904.txt) reports return of the deposit in less than a week. JUXT reports a smooth exit with the expected cleaning fee, and Coen & Columbia reports seamless move-in/move-out. Positive records are retained without claiming that this purposive sample represents satisfaction.

Repeated topics justify examining condition baselines, charge responsibility, depreciation calculations, delivery evidence, corrected balances and closure documentation. We cannot infer that cleaning is automatically charged throughout Holland, that charges generally lack documentation, or that concessions and waivers establish illegality. We also cannot calculate move-out volume, internal dispute frequency, average deductions, recovery cost or staff time from these records. The prior estimate of public escalations as a fraction of move-outs is withdrawn: neither numerator coverage nor the denominator was established.

## Litigation and regulatory evidence

**Direct settlement/collections case.** The [Hollingsworth complaint](sources/courts/gov.uscourts.cod.209806.1.3.txt), D. Colo. 1:21-cv-02522, alleges a disputed Holland-managed lease balance collected and credit-reported by IQ Data International, with requested lease/accounting records not supplied. The [December 27, 2021 order](sources/courts/gov.uscourts.cod.209806.21.0.txt) dismisses without prejudice for failure to prosecute. It is evidence of allegations and procedural disposition, not a liability finding. IQ Data is historically tied to Holland in this primary filing; the current collection vendor is not established.

**Deposit accounting pleaded, outcome unrecovered.** The [Hrubec complaint](sources/courts/hrubec_complaint_or.txt), Multnomah 17CV55642, alleges Palladia habitability injuries and an ORS 90.300 accounting claim. The complaint is a primary pleading. No merits outcome has been recovered from the available free records or the targeted follow-up search; the unresolved outcome must not be described as an ongoing case merely because the complaint survives online.

**California screening enforcement.** The [California AG announcement of December 18, 2024](sources/cag_press.txt) and [complaint](sources/cag_complaint.txt) concern use of COVID-19 rental debt in tenant screening. The announcement attributes the $625,000 payment to RealPage and describes injunctive terms for both RealPage and Holland. It does not establish a $625,000 Holland fine or a deposit-return enforcement action. This supports a company-level compliance concern adjacent to Handoff's account data, not proof of settlement defects.

**California broker accusation.** [DRE Accusation H-12779 SF](sources/ca_dre_H12779_pleading.txt), filed October 24, 2025, alleges deficient trust-fund records, an unexplained $4,138.31 overage, deficient account designations and withdrawal/licensing controls. These are the regulator's allegations, not adjudicated findings. The [September 30, 2026 license-page refresh](sources/reviews/dre_status_refresh.txt) still lists the corporation as LICENSED and links the accusation; no final disciplinary order appears in that retrieved listing. That is a scoped observation, not proof no later document exists elsewhere.

**Other legal exposure.** The saved [Nicherie docket](sources/courts/nicherie-v-holland-partner-group-llc.txt) records dismissal upon settlement on November 4, 2025 in a disability-accommodation case; settlement is not a merits finding. Parkside explosion reporting, Alta Laguna litigation, employment cases and vendor-contract claims concern other operational risks. They are preserved in the original [research ledger](sources/residents_risk.ledger.json) as leads; their previously reported procedural states are not adopted as current outcomes here. They do not increase the settlement-case count.

Older Overlook of Lakemont review text names Preston Mitchell Company as a collector. That is an unverified historical resident account, not a confirmed current supplier relationship. Recent BBB replies establish use of a third-party collector without naming it. We do not infer a successor or present vendor from the historical IQ Data filing.

## Law and event dates

`law_period` is a chronology aid only. A 2026 complaint can concern a 2024 move-out, and the wrong event date changes the analysis. Three legislative dates remain as comparison markers; no finding of applicability or violation follows from being before or after one. Oregon and Arizona are marked unclassified, not as having no relevant law changes. Applicable provisions, effective-date branches and local layers belong in `law_map.json` and the subsequent jurisdiction derivation. This brief withdraws the former blanket claim that post-change examples were necessarily violations or near-violations.

## Retrieval coverage and residual limits

- **BBB:** public JSON API recovered 32 HPG complaints and six reviews, and searched 16 additional profiles. Twenty-eight relevant full records entered this dataset. Three older BBB items remain indexed excerpts outside the recovered full-record set. Website blocking did not prevent API recovery. BBB's rolling profile totals are time-dependent and cannot be annualized into an internal complaint rate.
- **Wayback:** saved interrupted work contained 28 parsed reviews; manual scope screening admitted three, replacing two existing snippets and adding one positive deposit account. Other recovered reviews concern general living/leasing and were excluded. Logs and partial resume state disagree because disk-full errors interrupted writes; no complete 61-property archive sweep is claimed. Fresh targeted CDX attempts for Yelp Lydian and ApartmentRatings 1111 Wilshire did not yield usable responses (saved under `sources/reviews/archive_*.txt`).
- **Reddit:** 19 saved RSS query responses predominantly contain irrelevant broad matches and advertisements. None was admitted as Holland settlement evidence. Targeted web search recovered a July 2023 Denver thread describing a transition from Holland to another manager; it was excluded from this settlement sample because the post concerns a move-in account adjustment under changed management, with attribution unresolved. A separate Seattle collections thread does not name Holland. Search hits and general commenters' speculation are not evidence of Holland's systems or liability.
- **Rent.com/ApartmentGuide:** public GraphQL answered for eight communities/13 listings with null review data, followed by an empty challenge response. This establishes no recovered text, not an absence of reviews. Google Maps supplied limited-view pages without review text; the review endpoint returned 403. Neither source family contributes records.
- **CourtListener/RECAP:** saved entity searches and the [refresh](sources/reviews/courtlistener_cfpb_refresh.txt) did not recover a new deposit class action. The refresh returned bankruptcy records for two deposit-keyword queries; subsequent queries failed. RECAP is incomplete, particularly for state small-claims cases and owner entities not searched by name. The result cannot establish that Holland has no such litigation.
- **CFPB:** earlier query/parser behavior and the latest 403 responses mean no usable Holland-linked narratives were recovered. The prior categorical assertion that the API no longer exposes narratives is withdrawn; failed requests do not establish the API's overall capabilities. A missing landlord-name result cannot identify its collectors or clear them.
- **Other public enforcement:** prior broad web searches did not recover a directly relevant HUD/FTC/city action; dedicated municipal enforcement portals and comprehensive state trial-court searches were not completed. This is an explicit coverage limit. It is not a finding that no action exists.

The original worker attempted direct pages, ordinary browser rendering, search-index copies, public APIs and archives; this recovery reused saved originals and made targeted public follow-ups. No login, contact, form submission, personal-browser access or human-check circumvention was used in this recovery. There are no new Browser MCP tabs to close.

## Implication for Handoff's existing objective

The strongest supported opportunity is continuity from physical evidence to a correct account and an accepted disposition: keep move-in condition available, distinguish repair cost from tenant responsibility, explain adjustments, prove statement delivery, propagate corrected balances to collectors and retain usable closure confirmation. The recovered material specifically supports these work requirements. Whether they materially reduce Holland's labor, dispute costs or elapsed time remains an empirical question; this public sample does not supply those economics.
