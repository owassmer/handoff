# NYC Stage A, second pass (2026-09-28)

File: `stage-a/NYC.json`. Check: `python3 stage_a_check.py stage-a/NYC.json` exits 0 (153 atoms, 0 errors).
Joint check with `NY.json` and `US.json`: 0 errors, cross-file 0 errors.

| | First pass | Second pass |
|---|---|---|
| Atoms | 128 | 153 (25 new; 5 more drafted this pass were dropped as duplicates of NY atoms; of the 128, 55 changed: 11 in quote, condition or effect, the rest in source, URL or dates only) |
| Bounded unknowns | 17 | 14 (6 closed, 3 new; 8 others re-routed or narrowed, 3 of them in substance: proviso-vs-caps, CPL-landlord-scope, overcharge-offset) |
| Atoms on unofficial Cornell text | 53 | 2 (flagged `source_authority: unofficial`) |

This is still Stage A only. Nothing here is a clock, parameter or model test.

## 1. The seam: stabilized tenancy whose lease or renewal predates 2025-11-15

**Result.** No city provision fixes the refund deadline, the itemization or the consequence.

- **Checked in full on the city side:**
  - RSC Parts 2520-2531 in official text, section by section;
  - RSL 26-501 ff. (first pass);
  - DHCR Fact Sheets #9 (11/2025) and #30 (11/2023), and DHCR's "Leases" page;
  - the NYC Rent Guidelines Board's Legal Assistance page and Security Deposits FAQ.
- **What RSC 2525.4 does.** It sets the cap, the interest-bearing account and the tenant's interest election. Paragraph (d) sends everything else back to GOL article 7.
- **What governs the return** is the state common-law rule for 7-103 trust deposits, which the NY worker holds as `NY:COMMONLAW-deposit-return` (Gable v Cahill, App Term 2020):
  - the deposit is due at the end of the tenancy;
  - the landlord must prove the damage and its reasonable cost;
  - there is no day count, no required itemized statement and no statutory forfeiture.
- **What the city side adds:**
  - `NYC:CASE-Pezzo-lease-return-term` (App Div 2d Dept 2016, a rent-stabilized unit): a lease return period (there, 60 days) is enforceable as a contract term. Keeping the keys past the lease's end did not defeat surrender (`NYC:CASE-Pezzo-surrender`).
  - `NYC:CASE-Middleton-stabilized-deposit` (Civ Ct 2010): RSC 2525.4 sends return to GOL art. 7. The deposit is the tenant's property, due at the end of the tenancy.
  - `NYC:RGB-14day-not-regulated` (city guidance): "the aforementioned 14-day requirement does not apply to rent regulated tenants". This is right for pre-2025-11-15 stabilized leases and for rent control. It is out of date for stabilized leases from 2025-11-15.
  - `NYC:DHCR-FS09-2025-change` (DHCR guidance) describes the 2025-11-15 change without the statute's lease-date condition (L.2025 c.436 s.2). The statute controls, so the guidance must not be read to reach older leases.
- **Remaining risk.** One trial court (Karole, Civ Ct 2022) read RSC 2525.4(d) as importing GOL 7-108(1-a)'s 14-day statement, forfeiture and double punitive damages. The text of 7-108(1) and the c.436 sponsor memo point the other way. The NY worker owns this question as `BU-NY-RS-pre2025-by-reference` (closable by counsel), with atoms `NY:CASE-Karole-RS-via-RSC` and `NY:L2025-c436-memo-gap`. My duplicate atoms for Gable, Karole and the memo were removed so that each fact has one owner.
- **Product note (Owen's decision, not law).** A written itemized statement within 14 days complies with every reading.
- **New seam edge:** `BU-NYC-holdover-renewal-2025` (closable by case law). Take a stabilized tenant who holds over without signing the offered renewal, across 2025-11-15. Has a renewal been "entered into" on or after that date?
  - RSC 2523.5(c)(2), in official text, deems a lease in effect only to fix rent in an overcharge proceeding.
  - Samson v Hubert (2d Dept 2012) bars holding the tenant to a deemed new term.

## 2. Unknowns closed (id -> atoms; reason)

| Unknown | Atoms | Reason |
|---|---|---|
| BU-NYC-RC-return-rule | NYC:RER-2205.5, NYC:RER-2205.5-GOL, NYC:CASE-Pezzo-lease-return-term, NYC:RGB-14day-not-regulated, NY:COMMONLAW-deposit-return | Parts 2200-2209 read in official text; 2205.5 is the only deposit provision. No NYC return rule exists, and 7-108(1-a) excludes controlled units, so 7-103 plus the common-law rule governs. |
| BU-NYC-RC-tenant-notice | NYC:RER-2204.1(d) | A statutory tenant must give 30 days' written notice by registered or certified mail. Otherwise the tenant owes the landlord's lost rent, up to one month. The first pass read 2204.1 and missed subdivision (d). |
| BU-NYC-voucher-claims | NYC:HRA-voucher-claim-window, NYC:HRA-voucher-proof, NYC:DSS-SOTA-voucher-claim | Voucher terms (HRA W-147N 05/2025; DSS SOTA DHS-10f): the claim is made after the tenant vacates and within 3 months, with sworn, notarized proof, capped at one month's rent. SOTA pays rent only after the first year. There is no cash deposit to refund. |
| BU-NYC-collection-procedures-trigger | NYC:SHIELD-5-76-procedures, NYC:DCWP-FAQ-procedures-trigger | DCWP's FAQ: collection procedures start when billing stops, suit is taken or threatened, or the full balance is demanded. A final statement that demands the balance starts them. |
| BU-NYC-SHIELD-status | NYC:SHIELD-effective-date, NYC:SHIELD-penalty-effective-date, NYC:DCWP-FAQ-validation-scope, NYC:SHIELD-5-77(b)(1)(iii)-frequency, NYC:SHIELD-5-77(b)(1)(iii)(D)(IX), NYC:SHIELD-5-77(b)(5)(i)(B), NYC:SHIELD-5-77(b)(4)-cease | City Record Notice of Change of Effective Date (2026-07-22): 2027-01-01. The penalty schedule has the same date (notice of 2026-08-20). rules.cityofnewyork.us lists the rule as Adopted, effective 2027-01-01. The communication limits, electronic consent and cease rules are now atomized. |
| BU-NYC-RSC-sections-unread | NYC:RSC-2523.5(c)(2), NYC:RSC-2526.1(e), NYC:RSC-2522.5(f)(2) | Every RSC section was fetched in official text and screened. The exceptions are 2520.1, 2520.2, 2523.2 and 2523.3, which were read on Cornell because Westlaw throttled; they are outside the chain. |

The seam itself was not a first-pass NYC unknown (it was the NY worker's `BU-NY-07107-transition`). The NYC reading is recorded in `closed_unknowns.BU-NYC-SEAM-pre2025-stabilized`.

## 3. Unknowns remaining, by `closable_by`

- **case_law (5)**
  - BU-NYC-holdover-renewal-2025 (new);
  - BU-NYC-fees-vs-damages;
  - BU-NYC-painting-allocation;
  - BU-NYC-overcharge-offset (narrowed: a departed stabilized tenant can enforce a DHCR penalty as a judgment, per RSC 2526.1(e); a rent-controlled tenant has a 2-year treble-damages action, per 2206.8);
  - BU-NYC-abandoned-property.
- **counsel (4)**
  - BU-NYC-RSC-proviso-vs-caps (narrowed to one group: pre-2025-11-15 leases of non-senior, non-disabled tenants with continuous occupancy who still hold more than one month. For leases or renewals from 2025-11-15, amended GOL 7-107(2) caps the deposit at one month and overrides the proviso);
  - BU-NYC-succession-deposit (FS #30 and RSC 2523.5(b) are silent);
  - BU-NYC-CPL-landlord-scope (narrowed: from 2027-01-01 only the 20-700 "consumer debt" question remains);
  - BU-NYC-FARE-undisclosed-fee (the DCWP FAQ covers only fees "to rent an apartment").
- **owner (1)**
  - BU-NYC-DCA-license-manager. Whether Handoff needs a DCWP licence turns first on how Handoff pursues balances: in whose name, with whose staff, and whether collection is its principal purpose.
- **event (2)**
  - BU-NYC-RSL-sunset (RSL expires 2027-04-01 unless extended);
  - BU-NYC-SHIELD-text-alignment (new; the rule aligning the in-text dates is still Proposed; nothing operative depends on it).
- **reading (2)**
  - BU-NYC-HPD-escrow-deductions (in the building's own HPD documents; a Stage D document);
  - BU-NYC-NYCRR-sections-unfetched (new: 9 NYCRR 2211.2-2211.8, the high-income decontrol procedure, is not read in any text).

## 4. Source replacements and wording differences

### Where the official text is

- **The official source.** govt.westlaw.com/nycrr is the online NYCRR that the Department of State provides.
  - It calls itself the "Unofficial New York Codes, Rules and Regulations".
  - Every 9 NYCRR section read there says "Current through September 15, 2021". It does not contain DHCR's amendments adopted in the NYS Register on 2023-11-08, effective 2023-11-08 (HCR-35-22-00007-A for the RSC; HCR-35-22-00004-A for the rent-control regulations).
- **The 2023 amendment text.** The NYS Register printed only summaries; the full text is on hcr.ny.gov.
  - hcr.ny.gov blocks curl, and the browser too (Cloudflare "you have been blocked").
  - web_extract returns at most about 50,000 characters, so DHCR's amendment text is saved only in part.
- **Saved official text:**
  - `sources/NYC_RSC_Part2520_NYCRR.txt` … `Part2531` and `sources/NYC_RER_Part2200_NYCRR.txt` … `Part2209`: 208 sections, one URL and "Current through" line per section;
  - the NYS Register notices (`NYC_NYSREG_*`);
  - the partial DHCR amendment text (`NYC_DHCR_RSC_2023_amendment_text_PARTIAL.txt`, `NYC_DHCR_RER_2023_amendment_text_PARTIAL.txt`, with PDF line numbers removed mechanically).

### The 53 first-pass atoms on Cornell text

The task said 56; a count of `source_url` containing cornell gives 53.

- **22 switched** to the official Part files. The quote is verbatim in the official text, and the section was not amended in 2023.
- **20 switched** to the official Part files. The section was amended in 2023, but the quoted words appear in both the 2021 official text and the post-2023 text. `effective_from` now says the words predate the amendment.
- **3 re-quoted** to words the amendment did not change, then switched:
  - `NYC:RSC-2528.4(a)`: the 2023 amendment deleted "on or after the base date" and the four-year lookback sentence;
  - `NYC:RER-2202.27`: the official text has a comma after "maximum rent";
  - `NYC:RER-2203.4`: the 2023 amendment dropped the 1962 date and added a physical-street-address duty.
- **7 moved to DHCR's own amendment text** (quote verbatim there; `effective_from` 2023-11-08):
  - NYC:RSC-2520.6(c) and NYC:RSC-2520.6(c)-fees (Cornell had "alease" and "aviolation"; DHCR reads "a lease" and "a violation");
  - NYC:RSC-2520.11(c) (DHCR text shows the deleted "[or]");
  - NYC:RSC-2520.11(r)(1) and NYC:RSC-2520.11(s)(1);
  - NYC:RER-2200.2(k);
  - NYC:RER-2200.14(a) (DHCR text shows the deleted "[either a rent bill or]").
- **1 kept on Cornell**, marked unofficial: NYC:RSC-2523.5(b)(2), on permanent vacating for succession.
  - The sentence was added in 2023 and is not in the saved part of DHCR's text.
  - It is corroborated by the NYS Register summary and by DHCR Fact Sheet #30.
- **One new atom on Cornell**, also marked unofficial: `NYC:RER-2202.27-fuel`, the 2023 ban on fuel pass-alongs in rent control. It is corroborated by the Register summary.

### Other differences found

These are in sections read, but not in any quote. They are Cornell artifacts or typos in the official 2021 text:

- "ETP A" (Cornell);
- "semien closed" (Cornell);
- "non primary" (Cornell);
- "beomce" (official 2021 text of 2200.2), which the 2023 amendment corrected to "became".

The full section-by-section diff is in the builder output (`source_report.json` in scratch).

## 5. Atoms changed because the first pass was wrong

- **`NYC:RSC-2525.4(d)`.** The first pass said the refund rules come from GOL 7-107, which implied the 14-day rule for every stabilized unit.
  - Corrected: the rule depends on the lease date.
  - Leases and renewals from 2025-11-15 fall under amended 7-107. Earlier ones fall under the common-law rule, plus any lease term. No city rule fills the gap.
- **Coverage, point-in-time.** The first pass said "DHCR FS #9 confirms" a 2025-11-15 switch.
  - Corrected: FS #9 omits the lease-date condition, so it does not confirm it.
  - New atom `NYC:DHCR-FS09-2025-change` records the gap.
- **`NYC:SHIELD-effective-date`.** It rested on a proposed rule; it now rests on the City Record Notice of Change of Effective Date.
- **`NYC:RSC-2525.4-proviso`.** It now states that for leases or renewals from 2025-11-15, amended 7-107(2) overrides the proviso.
- **2204.1(d) was missed.** The first pass read 9 NYCRR 2204.1 but missed subdivision (d), the rent-controlled tenant's notice and liability. Case walks C2 and C6 said this was open or that NYC adds nothing; both are corrected.
- **Six quotes came from unofficial post-2023 text.** NYC:RSC-2520.6(c) and (c)-fees, NYC:RSC-2520.11(c), NYC:RSC-2528.4(a), NYC:RER-2203.4 and NYC:RER-2200.14(a) quoted Cornell as if it were the section text. Two of them had Cornell typos. All are now fixed to official or DHCR-published text, with dates.
- **`effective_from` for 2023-amended sections.** It said "2023-11-08 (last amendment)" as if that were the date of the quoted words. It now says whether the quoted words predate the amendment or came from it.
- **Case walk C5b.** It said stabilized leases from 2019 to 2025 fall under "former 7-107". Former 7-107 held only successor liability. Corrected: the common-law rule governs them.

## 6. New atoms (25)

- **Case law (city regime):** Pezzo (lease return term; surrender), Middleton, Samson.
- **Guidance:**
  - RGB on the 14-day rule;
  - DHCR FS #9 on the 2025 change;
  - DHCR on excess-deposit jurisdiction;
  - DCWP SHIELD FAQ (trigger; validation scope);
  - DCWP FARE FAQ.
- **SHIELD rules:** penalty effective date; frequency cap; original-creditor exception; electronic consent; cease communication.
- **Vouchers:** HRA claim window; HRA proof; SOTA claim.
- **Rent-control regulations (official text):**
  - 2204.1(d) tenant notice;
  - 2202.24(a) retroactive rent due on vacating;
  - 2206.8 tenant overcharge action;
  - 2202.27 fuel ban (unofficial text).
- **RSC (official text):**
  - 2523.5(c)(2) deemed lease only for overcharge;
  - 2526.1(e) penalty enforceable as a judgment once the tenant is out;
  - 2522.5(f)(2) early vacancy. Paragraph (f) was amended in 2023; the amended wording was not obtained, as flagged in the atom.

## 7. Sources added (all `sources/NYC_*`)

- **Official 9 NYCRR, per Part:** RER Parts 2200-2209 and RSC Parts 2520-2531.
- **NYS Register:** 2023-11-08 adoptions and 2022-08-31 proposals, for both the RSC and the rent-control regulations.
- **DHCR amendment text:** partial, for both.
- **Cornell fallback:** unfetched sections only; no atom rests on it.
- **Case law:** Pezzo (2d Dept 2016), Samson (2d Dept 2012), Middleton (Civ Ct 2010).
- **City Record:** SHIELD notices of 2026-07-22 and 2026-08-20.
- **Other DCWP material:**
  - SHIELD rule status pages (rules.cityofnewyork.us);
  - DCWP SHIELD FAQ (08/04/2026);
  - DCWP FARE FAQ (08/12/2025);
  - DCWP debt collection licence page.
- **Vouchers:** HRA W-147N (05/07/2025) and DSS SOTA DHS-10f (06/28/2019).
- **Guidance:**
  - RGB Legal Assistance, The Basics and Security Deposits FAQ;
  - DHCR Leases page and Fact Sheet #30;
  - NYS AG "Recovering Rent Security".

## 8. Checks run

- `stage_a_check.py stage-a/NYC.json`: 0 errors.
- `stage_a_check.py stage-a/NY.json stage-a/NYC.json stage-a/US.json`: 0 errors; cross-file 0.
- **Mutation test.** Changing "30 days" to "14 days" in NYC:RER-2204.1(d), plus one word in a second quote, gives 2 errors. The check discriminates.
- **Cross-jurisdiction.** The quotes of NYC:RER-2204.1(d), NYC:RSC-2525.4, NYC:RSC-2523.5(c)(2), NYC:HRA-voucher-claim-window and NYC:SHIELD-effective-date appear in no NY_, VA_ or US_ source.
- **Closure.** Every case-walk atom and unknown id, and every closed-unknown atom id, exists. This was asserted in the builder.

## 9. Limits

- **2023 wording.** DHCR's full 2023 amendment text could not be saved whole. Three atoms therefore rest on unofficial or partial wording, and each is flagged in its atom: 2523.5(b)(2), 2202.27-fuel and 2522.5(f)(2).
- **Westlaw throttling.** Westlaw throttled document requests after 208 of 227 sections. 2211.2-2211.8 are unread (BU-NYC-NYCRR-sections-unfetched).
- **DHCR decisions.** DHCR orders and advisory opinions are not searchable online. The fees-versus-damages and succession questions stay with case law or counsel.
