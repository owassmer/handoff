# Gaps: California account-core map

October 3, 2026. Three groups: provisions the map needs but that were not retrieved or read; needed sources missing from the J1 register; and items outside this milestone, one line each.

## 1. Needed but not retrieved or not read

**Regulations** (both units are in the J1 register; neither text was attempted, because the CCR is hosted by Westlaw)
- 10 CCR 2832 — broker trust-fund handling of deposits. DP1.2: matters when the manager, not the owner, holds the deposit.
- 2 CCR 12185 et seq. — FEHA rules on assistance animals and reasonable accommodation. DP5.9: the state basis for "no pet deposit or fee for an assistance animal".

**Statutes not fetched** (all inside register units)
- Civ 1633.5 — UETA's requirement that parties agree to transact electronically. DP1.6 and the E-SIGN question in federal.md.
- Civ 1995.010 et seq. — assignment and sublet (DP2.2).
- Civ 2787 et seq. — guarantors (DP2.3).
- Civ 51 — Unruh Act (DP5.10).
- HSC 17975.1–17975.10 — relocation amounts and procedure (DP2.6, DP3.6).
- CCP 683.020, 704.x and 724.030 — enforcing and satisfying a judgment; exemptions (DP8.11).
- CCP 703.140 — the bankruptcy exemption election (federal.md).

**Dated values**
- Prob 890 adjusted small-estate threshold for Prob 13100: the Judicial Council table, which updates the statutory $166,250.
- Water-submeter fee cap 1954.205(a)(3): the current CPI-adjusted figure.

**Holder notice for unclaimed refunds**
- CCP 1513.5 covers banks only. The notice duty for non-bank business holders is in State Controller holder guidance (registered as CA:SCO-HOLDER, DUE-DILIGENCE). Not read.

**2026 acts**
- Holiday acts AB 1841, AB 2017, SB 1394 and AB 2294 are read (`sources/bills/`). Still open: their exact operative date, and how the double-jointing among them resolves. The presumption is Jan 1, 2027, under Gov 9600 (not read).
- Already read, with no effect on the account:
  - AB 395 (Education and Government Code meeting provisions; it adds no GOV 6700 holiday);
  - AB 2025 (disclosure of digitally altered images in rental advertising; leasing);
  - SB 1072 (housing-program and Gov 65863.10 amendments);
  - SB 1296 (pet-policy disclosure before tenancy, and refund of application fees; operative Apr 1, 2027).

**Case law (J5)**
CourtListener is blocked. The official courts.ca.gov archive holds only recent opinions. *Granberry* was read from the Stanford mirror. Not read:
- any appellate decision after AB 2801 on (h)(7) or (m);
- a California definition of "bad faith" under 1950.5;
- *Orozco v. Casimiro* (2004) 121 Cal.App.4th Supp. 7 (late fees);
- *Green v. Superior Court* (1974) 10 Cal.3d 616 (habitability);
- *Leaser v. Prime Ascot*, cited in Brooks ECF 56 (manager restitution);
- Ninth Circuit authority for re-grounding the FDCPA atoms (federal.md section 2).

**Brooks v. Greystar**
- ECF 48 is saved as text in `research/california-case/sources/`.
- ECF 56 (Aug 7, 2025) is saved as a PDF (`brooks-greystar-2025-08-07.pdf`). Its utility passage (pp. 13–14) was read and quoted this session.

**Huntington Beach**
- No eCode360 search for deposit, rent, collection or utility-billing rules for tenants was run this session. The conclusion that HB has no account rules rests on the J0 profile, RESEARCH.md and the absence of HB rent or tenant ordinances in prior work.
- HB water and sewer rules (registered as CA-HB:MUNICIPAL Title 14, water rates 2026, master fee schedule) matter only if units have individual city water accounts.

**Orange County Housing Authority**
- The HCV Administrative Plan (registered as CA-OC:OCHA-ADMIN) and owner notices (CA-OC:OCHA-OWNER) may add owner duties at move-out for the voucher template: HAP for the move-out month, notices, and any damage-claim policy. Not read.

**Currency of the earlier captures**
- Only a subset of the 166 sections captured on September 30 was re-fetched on October 3; the results are in `currency_recheck_2026-10-03.json`.
- The full re-check failed on proxy and leginfo throttling. The rest remain "saved September 30".

## 2. Needed but absent from the J1 register

- Every California code section the map uses falls within a unit marked in scope in `jurisdictions/CA/instruments.json` (checked read-only by heading range). No register gap for statutes.
- **Absent:** the DRE *California Tenants* guide (2026 edition). It is official agency guidance and the only official source of factors for wear and tear, cleaning and the useful-life proration. Saved here at `sources/DRE_2026_Landlord_Tenant_Guide.txt`. Propose registering it as guidance, labeled not law.
- **Absent:** AB 2801's uncodified intent section (Stats. 2024 ch. 280 §1). The act is listed among prior enactments, so check the entry keeps §1.
- **Absent:** the Judicial Council Prob 890 adjustment table, if the register does not already hold it under Judicial Council publications.
- **Federal, outside this register:** 15 U.S.C. 1681t(b)(1)(F) was captured this session at `research/legal-engine/sources/US_15USC_1681t.txt`. The US register should hold it.

## 3. Outside this milestone (later variation; not mapped)

- **Public-agency owner:**
  - Government Claims Act presentation for deposit claims (Gov 905, 911.2, 945.4);
  - immunity from punitive-type damages (Gov 818) against the 1950.5(m) statutory damages;
  - small claims against a public entity;
  - public-entity unclaimed-property handling.
- **Income-restricted units:**
  - regulatory agreement and tax-credit (CTCAC) compliance;
  - restricted-unit exemptions from just cause and the rent cap (1946.2(e)(9), 1947.12(d)(1));
  - LIHTC good-cause nonrenewal (AB 2689, 2026).
- **Prevailing wage on turn work** at a public-owned property (Lab 1720(a)(1), 1771) and its effect on the "reasonable" chargeable cost.
- **Federal and state program units:**
  - project-based vouchers (24 CFR 983);
  - project-based Section 8, 202 and 811 (24 CFR 880–891, HUD Handbook 4350.3, HUD-90105a, special claims);
  - HOME (24 CFR 92);
  - USDA Rural Development (7 CFR 3560);
  - HCD, CalHFA and CTCAC program instruments.
- **Public housing** (24 CFR 966, 960; PHA reporting of debts owed).
- **Junk-fee rules:** CLRA drip pricing (Civ 1770(a)(29), SB 478) and whether it reaches residential leases. Not researched; flat fees are already excluded by Owen's posture.
- **Leasing and marketing:** screening-fee limits (1950.6), tenant screening and rental advertising (AB 2025), the pet-policy disclosure (SB 1296).
- **Physical work (PW1, PW2):** permits, contractor licensing, lead and hazard rules. These do not change the account, except through PW3.4.
