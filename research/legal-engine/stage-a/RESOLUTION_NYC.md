# Resolution pass, New York City (2026-09-28)

`stage-a/NYC.json` now holds 182 atoms and `bounded_unknowns: []`. `python3 stage_a_check.py stage-a/NYC.json` exits 0.
The joint check with NY, VA and US reports 0 cross-file errors. NY also passes on its own. VA (14 errors) and US (18 errors)
still fail on their own open items; those files belong to the sibling workers.

- New authorities are saved under `sources/NYC_*`. Every quote and construction quote is checked verbatim.
  - Mutation test: changing one word in a construction quote (Bogom-Shanon) and one in a primary quote (SHIELD notice of adoption), and adding "arguably" to a reasoning field, gives 3 errors.
  - Cross-jurisdiction test: new quotes sourced to NYC files do not appear in NY, VA or US sources. The one exception is the Marshals Handbook sentence, which Facey (an NY source) quotes. The 20-489(a)(7)(ii) quote was lengthened so that it is not the FDCPA's identical clause.
- Backup of the pre-pass file: profile scratch `NYC_pre_resolution.json`. The builder is `build_nyc_resolution.py` with `nyc_res_atoms.py` in the same directory.

## Former question -> atoms, controlling authority, adjudication

| Former id | Resolving atoms | Controlling authority | Adjudication |
|---|---|---|---|
| BU-NYC-holdover-renewal-2025 | NYC:RS-HOLDOVER-signed-renewal, NYC:RS-HOLDOVER-rent-accepted, NYC:RS-HOLDOVER-no-rent-accepted | Samson v Hubert (2d Dept 2012); Case v 575 Classon (App Term 2d Dept 2024); Bogom-Shanon v Altman (Civ Ct NY County 2025); RSC 2523.5(a), (c)(2)-(3); L.2025 c.436 s.2 | RPL 232-c governs a stabilized holdover (Samson). Rent accepted after expiry creates a renewal tenancy "entered into" (Case), and each month is a new leasehold (Bogom-Shanon). So rent accepted into a month beginning on or after 2025-11-15 brings amended GOL 7-107; with no rent accepted, the last signed lease governs. |
| BU-NYC-fees-vs-damages | NYC:RS-FEE-vs-DAMAGES | RSC 2520.6(c) as amended 2023 (definition of rent); DHCR Fact Sheet #44; Gable (App Term 2d Dept) | A lease-imposed charge "for, or in connection with, the use or occupation" is rent, so above the legal rent it is an overcharge. Compensation for proven damage beyond wear and tear is not consideration for occupancy and is recoverable. The Code and FS #44 agree. |
| BU-NYC-painting-allocation | NYC:PAINT-wear-and-tear | HMC 27-2013(b)(2); RSC 2520.6(r)(1); DHCR FS #28; Bohl v Poffenbarger and Blansett v Zambrana (App Term 2d Dept); Gable | Repainting after ordinary occupancy is wear and tear and the owner's three-year duty. The tenant pays only the proven extra cost of damage beyond wear and tear. A bare painting and spackling bill proves nothing. |
| BU-NYC-overcharge-offset | NYC:RS-OVERCHARGE-court-counterclaim, NYC:RS-OVERCHARGE-final-account-credit, NYC:RSC-2526.7(i)(7) (edits NYC:RSC-2526.1(e)) | Admin. Code 26-516(a), (a)(2); Rockaway One v Wiggins (2d Dept 2006); RSC 2526.7 (added 2023); NYS Register 2023 (concurrent jurisdiction, tenant's choice of forum) | The tenant may raise the overcharge in the owner's action at any time, and the court nets it (Rockaway One). The owner may credit an overcharge on the final statement itself. A pre-complaint refund can count on willfulness; a post-complaint refund cannot (26-516(a)). |
| BU-NYC-abandoned-property | NYC:ABANDONED-city-layer (refs NY:COMMONLAW-belongings-owner-keeps, NY:COMMONLAW-belongings-abandonment) | DOI Marshals Handbook ch. IV s. 6-4; the Admin. Code and RCNY, searched in full; NY file for the state rule | No NYC rule governs belongings left after a voluntary move-out, since the marshals' rules reach only evictions. The statewide rule in the NY file governs. |
| BU-NYC-RSC-proviso-vs-caps | NYC:RS-PROVISO-survives-HSTPA | RSC 2525.4 proviso (not amended in the 2023 re-promulgation); GOL 7-108(1); amended GOL 7-107(2) with c.436 s.2; RSC 2527.11 | The HSTPA cap sits in 7-108, which excludes stabilized units, and DHCR kept the proviso when it implemented HSTPA in 2023. So the regulation prevails over Fact Sheet #9 until a lease, renewal or monthly leasehold entered into from 2025-11-15 brings the 7-107(2) one-month cap. |
| BU-NYC-succession-deposit | NYC:RS-SUCCESSION-tenancy-continues, NYC:RS-SUCCESSION-claim-fails | RSC 2523.5(b)(1)-(2); RSC 2522.5(f)(1) (renumbered 2023); GOL 7-103(1); GOL 7-107(6) | Succession continues the tenancy on the same terms. The deposit therefore stays as security, and no settlement runs until the successor tenancy ends. The refund belongs to the depositor unless assigned. If succession fails, the tenant of record's settlement runs when the owner regains possession. |
| BU-NYC-CPL-landlord-scope | NYC:CPL-tenant-balance-consumer-debt, NYC:RCNY6-5-77(f)(1)-landlord-not-TILA-creditor | Admin. Code 20-701(c); 6 RCNY 5-76 "debt"; Romea (2d Cir 1998); Allen v Whidbee (2025); NY:ADJ-lease-balance-not-consumer-credit | Consumer debts are defined by household purpose, so a former tenant's balance is one, and DCWP's rules reach whoever collects it. The current 5-77(f)(1) validation binds only Truth in Lending Act creditors, and a landlord is not one. |
| BU-NYC-FARE-undisclosed-fee | NYC:FARE-20-699.20-fee, NYC:FARE-moveout-service-fee, NYC:FARE-damages-rent-not-fees | Admin. Code 20-699.20 ("fee"), 20-699.22(b), 20-699.23(c), 20-699.24; Charter 1041(5)(b)(ii) on the weight of the DCWP FAQ | A lease charge for a move-out service is a fee "in connection with" the rental. It must be on the signed pre-lease disclosure; otherwise it is subject to restitution and compensatory recovery. Rent and damages are not fees. The statute's words govern the FAQ's narrower "to rent an apartment". |
| BU-NYC-HPD-escrow-deductions | NYC:HPD-ESCROW-no-owner-draw, NYC:HPD-ESCROW-regulatory-agreement | 28 RCNY 1-12(b), (f); HPD publishes no separate escrow procedure (searched) | Escrowed deposits are released only to the tenant, on the owner's certification. The owner has no draw and pursues arrears and damages against the tenant, unless a 1-12(f) regulatory agreement provides a procedure. |
| BU-NYC-NYCRR-sections-unfetched | NYC:RER-2211.8(a) | DHCR full amendment text for the NYC Rent and Eviction Regulations (eff. 2023-11-08) | 2211.2-2211.7 were repealed on 2023-11-08. 2211.8 now ends high-income decontrol from 2019-06-14 and keeps earlier lawful deregulations. That is a routing rule; nothing in Part 2211 bears on the settlement (coverage family 2). |
| BU-NYC-DCA-license-manager | NYC:DCA-owner-own-staff, NYC:DCA-affiliate-collector, NYC:DCA-manager-for-owners, NYC:DCA-handoff-principal-purpose, NYC:DCA-handoff-incidental, NYC:DCA-debt-buyer, NYC:DCA-originated-exclusion-scope | Admin. Code 20-489(a), (a)(1), (a)(3), (a)(7), 20-490; Citibank v Yanling Wu (2d Dept 2021); Goldstein (2d Cir 2004) for the contrast with the FDCPA; DCWP licence page | A licence is needed only where the business's principal purpose is regularly collecting others' debts, or where it buys delinquent debt. The owner's own staff, affiliates, managers whose business is management, and Handoff collecting incidentally as the owner's fiduciary need none. Handoff whose principal business is collection needs one, whichever name it uses. The originated-debt exclusion reaches only the lessor. Which configuration applies is Owen's operating choice. |
| BU-NYC-RSL-sunset | NYC:RSL-26-520 (effective_to 2027-03-31); 67 stabilization atoms carry effective_to 2027-03-31; NYC:RCL-26-401-duration | Admin. Code 26-520 as enacted through L.L. 2026/110 (last extension L.L. 2024/047); 26-401(a) | No extension had been enacted by the compilation date, so the RSL and the RSC made under it run through 2027-03-31. Rent control has no fixed end date. |
| BU-NYC-SHIELD-text-alignment | NYC:SHIELD-operative-date | City Record Notice of Change of Effective Date (2026-07-22); SHIELD notice of adoption ("the effective date of this rule"); Charter 1043(f)(1), 1045(b), 1041(5); certified Compilation (amlegal 5-76, 2026-09-28); DCWP FAQ | 1043(f) sets a floor, not a mandatory start date. DCWP moved the date by City Record notice before it arrived, and the rule defines its in-text dates as its effective date. The certified Compilation still holds the old rules. So the operative date is 2027-01-01 and the in-text dates read as that date. The pending amendment only conforms the words. |

## Source replacements and corrections

- DHCR's full 2023 amendment texts are now saved whole:
  - `NYC_DHCR_RSC_2023_amendment_text_FULL.txt` and `NYC_DHCR_RER_2023_amendment_text_FULL.txt`.
  - Route: Internet Archive `id_` captures of `hcr.ny.gov` (`rsc-rule-text-10.23.23.pdf`; the RER page URL serves a PDF).
  - Seven atoms moved from the partial copies to the full text.
- The two Cornell atoms moved to official DHCR text with identical wording: NYC:RSC-2523.5(b)(2) and NYC:RER-2202.27-fuel. No atom now rests on Cornell.
- Corrections the full text forced:
  - RSC 2522.5(f), on vacancy before the lease term ends, was repealed on 2023-11-08. NYC:RSC-2522.5(f)(2) now carries effective_to 2023-11-07, and case walk C6 says so.
  - RSC 2526.1 now governs only proceedings commenced before 2019-06-14. The new NYC:RSC-2526.7(i)(7) carries the same credit and judgment remedy for later proceedings.
- Pointer text that named former questions now names the resolving atoms, in 21 atoms.
- Case walks carry the new atoms and have empty `unknowns`. The NY seam points to NY:ADJ-RS-pre2025-7108-inapplicable, which rejects Karole.

## Configuration branches handed to later stages (law stated, choice not made)

- The licensing configuration (the NYC:DCA-* atoms) is Owen's operating choice. Each branch states its rule.
- Holdover facts are Stage D inputs:
  - whether rent was accepted after expiry;
  - the date a renewal was executed.
- Other Stage D inputs:
  - succession facts;
  - the escrow directive and any regulatory agreement for HPD article VIII buildings;
  - the FARE disclosure signed at lease-up.
