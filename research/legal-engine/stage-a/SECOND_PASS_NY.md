# NY second pass (2026-09-28)

Scope: New York State layer only (`stage-a/NY.json`). NYC items are the NYC worker's (`NYC:`); federal items belong to the federal worker (`US:`).
Result: 143 atoms became 172. 17 unknowns became 12: 6 closed and 1 new, narrower one opened. `python3 stage_a_check.py stage-a/NY.json` exits 0. With NYC.json, the cross-file check reports 0 errors; NYC.json's own 17 errors are missing `closable_by` fields in the sibling's file.

## The seam: stabilized or ETPA tenancy, lease or renewal entered before 2025-11-15

**Result: state statute sets no refund deadline, no itemized statement and no forfeiture for these tenancies.** Three readings establish this, and the Legislature confirms it.

- **7-108 excludes these units, both before and after 2019.** The pre-2019 7-108(1) excluded "any dwelling unit specifically referred to in section 7-107" (bracketed old text in L.2019 c.36 Part M s.25). HSTPA kept that exclusion and renamed the section "Deposits made by tenants of non-rent stabilized dwelling units". Atoms: `NY:GOL-7-108(1)`, `NY:GOL-7-108(1)-pre2019`.
- **Former 7-107 held only successor liability.** Its title and text covered grantee/assignee liability on conveyance, the receiver limit and the waiver bar. It had no cap, statement, deadline or forfeiture. The deleted text is in brackets in S952-B, the bill signed as L.2025 c.436. Atom: `NY:GOL-7-107-pre2025(1)-scope`. The existing pre2025 (2)(a), (2)(b) and (3) atoms now cite S952-B.
- **The sponsors say so.** The A6423-A memo's justification: "these protections do not extend to the hundreds of thousands of units that are rent stabilized, since the HSTPA included these protections in a Section of the General Obligations Law (7-108) that explicitly excludes rent stabilized dwelling units." The original S952 memo described the bill as removing 7-108's exclusion of stabilized units. Atom: `NY:L2025-c436-memo-gap`.
- **c.436 has not been amended.** It was signed with no approval memo, so no chapter amendment was agreed. The 7-107 text at nysenate.gov on 2026-09-28 matches the enacted bill word for word. c.436 s.2 turns on the date the lease or renewal was *entered into*, not the date its term starts.

**What governs these tenancies instead:**

- **Common law.** The deposit is returned at the end of the tenancy unless the landlord proves damage beyond wear and tear or applies it to unpaid rent. The landlord bears the burden. Atoms: `NY:COMMONLAW-deposit-return` (Gable v Cahill, App Term 2d Dept 2020), `NY:CASE-Gelbart-rent-offset`.
- **GOL 7-103.** Trust, bank notice and interest apply.
- **The 7-103 forfeiture (Appellate Division).** Commingling forfeits the deposit, and a missing bank notice lets a court infer commingling unless the landlord rebuts it. Rent claims survive the forfeiture. Atoms: `NY:CASE-Paterno-bank-notice-inference`, `NY:CASE-Paterno-commingling-forfeiture`, `NY:CASE-Paterno-rent-survives`. This is the only forfeiture that reaches these tenancies on current authority.
- **Rent regulation.** NYC:RSC-2525.4 in NYC (NYC worker); 9 NYCRR 2505.4 for ETPA units outside NYC.

**Conflict kept open.** One trial court (Karole, Civ Ct NY County 2022) applied the 7-108(1-a)(e) forfeiture and 2x punitive damages to a stabilized renewal lease. It relied on RSC 2525.4 ("owner otherwise complies with ... article 7") and did not address 7-108(1). This goes against the statute's text and the Legislature's account, but it is real litigation exposure. It is recorded as `NY:CASE-Karole-RS-via-RSC` and the new unknown `BU-NY-RS-pre2025-by-reference` (closable by counsel). No appellate decision either way was found. The affected group shrinks as tenants sign renewals entered on or after 2025-11-15.

## Unknowns closed

| Unknown | Closed by | Reason |
|---|---|---|
| BU-NY-07107-transition | NY:GOL-7-107-pre2025(1)-scope, NY:L2025-c436-memo-gap, NY:GOL-7-108(1)-pre2019, NY:COMMONLAW-deposit-return, NY:CASE-Paterno-commingling-forfeiture | Text, session laws and the sponsor memo agree: no statutory deadline, statement or forfeiture before 2025-11-15; common law and 7-103 govern. The residual exposure is split out as BU-NY-RS-pre2025-by-reference. |
| BU-NY-7108-prior-scope | NY:GOL-7-108(1)-pre2019, NY:COMMONLAW-deposit-return, NY:CASE-Bogom-Shanon-month-to-month, NY:CASE-Case-v-575Classon | Part M s.29 limits s.25 to leases entered on or after 2019-07-14, so the old 7-108(1) scope (written leases in 6+ unit buildings, plus rent control) still governs unrenewed older leases. The return rule is the common law. A month-to-month continuation counts as a new tenancy. |
| BU-NY-234-a-date | NY:L2021-c695-s6, NY:L2022-c162 | 234-a took effect 2021-12-21 (c.695, immediate). The co-op carve-out came from c.162, effective as of the same date. The statute voids "any agreement" with no lease-date limit. |
| BU-NY-unclaimed-refund | NY:ABP-1315(2), NY:OSC-MS11-refunds-due | ABP 1315: 3 years unclaimed, counted from when the tenant became entitled. The Comptroller classes it as "Refunds Due" under 1315, 3-year dormancy. |
| BU-NY-227-e-old-leases | NY:L2019-c36-PartM-s29, NY:RPL-227-e (effect updated) | Part M applies to actions commenced on or after 2019-06-14, whatever the lease date. |
| BU-NY-estimate | NY:CASE-Toporek-estimate | App Div 1st Dept: a timely statement itemizing each repair with its estimated cost complies with (e). Need and cost are tried later, with the burden on the landlord. NY has no follow-up statement; any shortfall is a separate claim. |

## Unknowns remaining (12)

**counsel (10): no controlling authority was found, so a legal opinion is needed.**
- **BU-NY-RS-pre2025-by-reference** (new): whether courts will import 7-108(1-a) into pre-2025 stabilized leases through RSC 2525.4(d) (Karole). The text says no.
- **BU-NY-forfeiture-vs-claims:** narrowed. Every decision read allows the separate claim on proof: Levine (App Term 1st Dept 2026), Masseroli, Pickens, and Paterno (App Div, by analogy under 7-103). There is no App Div holding on (1-a)(e) itself.
- **BU-NY-willful:** narrowed. Willfulness is a fact finding (Prando, App Term). Only open point: whether ignorance of the law negates it. Masseroli says yes; Bogom-Shanon and Karole say no.
- **BU-NY-provide-delivery:** narrowed. The statement must be written; letter, email or text qualify, oral does not (Bogom-Shanon). Open: whether the deadline is met on sending or on receipt, and what to do when there is no forwarding address or email.
- **BU-NY-multi-tenant-payee:** narrowed. An occupant is not a tenant and so not a payee (RPL 235-f, now atomized). Co-tenant split and payee rules are still open.
- **BU-NY-abandoned-belongings:** narrowed. Belongings may not be held for rent (Facey, trial level), and they can push back the "vacated" date (Urban, App Div). The disposal procedure is still open.
- **BU-NY-GBL-consumer-claim:** trial courts split (Lefferts 2026 against Kings & Queens 2017); no appellate decision.
- **BU-NY-7103-property:** narrowed. The test is the building, and mixed-use buildings count (Gihon, App Div). Multi-building complexes are still open.
- **BU-NY-NYC-tenant-monthly-notice:** no NYC statute or decision found. RPL 232-b applies outside NYC only.
- **BU-NY-late-fees-from-deposit:** no decision on point found.

**reading (1): readable text, not reached in this pass.**
- **BU-NY-ETPA-EHRCL-regs:** 9 NYCRR parts 2500-2510 and 2100-2111 beyond the deposit sections; the ETPA and EHRCL statutes.

**owner (1): a scoping choice for Owen.**
- **BU-NY-local-outside-NYC:** which municipalities outside NYC are in scope.

## Source replacements

- **Seasonal exception, 7-108(1-a)(a), (4), (5).** The first pass relied on a secondary source ("L.2021 c.428 per secondary source"). Now:
  - `NY_L2021_c428_A4587A.txt`: signed 2021-09-20, effective immediately.
  - `NY_L2022_c111_S7795.txt`: chapter amendment signed 2022-02-24, effective as of c.428. It deleted the state-registry option.
- **Co-op exception, 7-108(6).** The first pass said "L.2021 c.789 as amended; session laws not saved". Now:
  - `NY_L2021_c789_S5105C.txt`: signed 2021-12-22, effective immediately, for actions commenced on or after that date.
  - `NY_L2022_c93_S7735.txt`: signed 2022-02-24, effective as of c.789. It renumbered subdivision (4) to (6) and excluded purchase-price payments.
- **c.436 atoms.** These now cite `NY_L2025_c436_S952B.txt`, the Senate bill that was signed, instead of the Assembly same-as bill. The texts are identical; the mechanical diff shows only the effective-date clause at the tail. Also saved: the A6423-A memo (`NY_L2025_c436_A6423A_memo.txt`) and the nysenate S952 bill page with all three memo versions (`NY_L2025_S952_senate_page.txt`).
- **RPL 234-a.** Saved `NY_L2021_c695_S2014.txt` and `NY_L2022_c162_S7801.txt` (with the A8750 memo).
- **How the texts were obtained.** Session-law texts come from nyassembly.gov by curl, with HTML and bill line numbers stripped by script. Case texts come from the nycourts.gov reporter via web_extract cache files, except:
  - Levine: Fordham FLASH reprint (the nycourts URL returned 404);
  - Gelbart: CourtListener-derived reprint;
  - Gordon: FindLaw copy (saved, not atomized).

## Atoms changed because the first pass was wrong or incomplete

- `NY:GOL-7-108(1-a)(g)` and `NY:GOL-7-107(8)`: were typed RULE. They contain the standard "willfully", so they are now MIXED with that judgment term, and they depend on `NY:CASE-Prando-willful`.
- `NY:GOL-7-108(4)`, `NY:GOL-7-108(6)`, `NY:GOL-7-108(1-a)(a)`: effective dates rested on secondary sources and were vague ("2021-2022"). They now carry exact dates from the session laws, including the two chapter amendments that apply retroactively to the original effective dates.
- `NY:RPL-234-a`: said "enactment date not read". Now 2021-12-21, with the c.162 wording.
- `NY:L2025-c436-s2`, `NY:GOL-7-107(1)`, `NY:GOL-7-108(1)`: the pre-2025 branch had been left to "by inference". It is now stated in atoms, and the test is clarified as the date the lease or renewal was entered into.
- `NY:GOL-7-108(1-a)(e)-forfeiture`: the separate-claims position was updated with Levine and Paterno.
- `NY:CPLR-214-i`: now records the trial-level split.
- Case walks:
  - C1: the pre-2025 branch is now answered.
  - C5a: now fully resolved.
  - C7: estimates allowed.
  - C9: escheat path added.
  - C10: no unknowns.
  - C11 and C12: new atoms.
- Coverage families 1, 5, 8 and 9 were rewritten to match.

## Other findings and hand-offs

- **Cohen v Abruzzo (App Div 2d Dept 2024)** counts the 14 days with the vacating day excluded (vacated July 24, due August 7). This is appellate confirmation of the GCN 20 reading.
- **Urban v Zipper (App Div 1st Dept 2025).** The "vacated" date that starts the clock is a question of fact, and lease terms about belongings left behind shape it. It is typed as a judgment (MIXED), not a rule.
- **Federal atoms still in NY.json.** NY.json still holds the first pass's US: atoms (SCRA 3955, FDCPA 1692a, 24 CFR 982.313). The federal worker now owns them. Once US.json fixes its ids, they should become NY external references. No new US: references were declared, so that the cross-file check cannot fail on ids the federal worker has not chosen. Only `US:FDCPA-conduct` remains declared.
- **Unit-status programs** are declared as NY external references so NYC.json's citations resolve: `NY:ETPA`, `NY:LEHRCA`, `NY:RPTL-421-a`, `NY:PHFL-art8`. `NY:RPL-235-f` is now an atom.
- **Scratch scripts.** The rebuild script `ny_pass2_apply.py` (outside the repo) rebuilds NY.json from a saved copy of the first pass: `~/.hermes/profiles/ferro/cache/scratch/NY.pass1.json`.
