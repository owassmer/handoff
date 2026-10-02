# US federal overlays: resolution pass (2026-09-28)

All 18 questions in `stage-a/US.json` are now atoms, and `bounded_unknowns` is empty. `US.json` has 175 atoms: 35 new,
plus 24 existing atoms whose effects no longer point at open questions. `python3 stage_a_check.py stage-a/US.json`
exits 0. The joint check of NY, NYC, VA and US also exits 0, with no cross-file errors. `US.json` carries a
`resolved_questions` map, and each case walk lists its `resolved_by` atoms.

Forum key:
- **NY** means New York federal courts, bound by the Second Circuit.
- **VA** means Virginia federal courts, bound by the Fourth Circuit.

"Weight" means the rule other circuits and in-circuit district courts apply where the forum's circuit has not ruled.

| Former question | Resolving atoms | Controlling authority (NY / VA) | Adjudication |
|---|---|---|---|
| BU-US-default-date | `US:15USC1692a(6)(F)(iii)-default-meaning`, `US:15USC1692a(6)(F)(iii)-moveout-branches` | NY: *Alibrandi* (2d Cir. 2003), binding. VA: no Fourth Circuit ruling; *Yergovich* (E.D. Va. 2018) uses the same test; *Alibrandi* is the only appellate decision. | A move-out balance is not in default on its due date. It defaults when the lease's delinquency period runs, or earlier when the owner treats it as in default (referral to a self-identified debt collector, "collection begins", charge-off). |
| BU-US-manager-fiduciary | `US:15USC1692a(6)(F)(i)-manager-incidental`, `US:15USC1692a(6)(F)(i)-collection-only` | VA: *Wilson v. Draper & Goldberg* (4th Cir. 2006), binding; *Yergovich*. NY: no Second Circuit ruling; the weight is *Wilson*, *Harris* (11th Cir. 2012) and *Rowe* (9th Cir.), which all apply one test. | A manager's collection is excluded when it is incidental to (not central to, or the main purpose of) broad management duties. A collection-only engagement is not excluded. |
| BU-US-damage-charges-debt | `US:15USC1692a(5)-lease-charges`, `US:15USC1692a(5)-non-party-tort` | NY: *Romea* (2d Cir. 1998) and *Alibrandi*. VA: *Mabe* (4th Cir. 1994) test; *Galdamez* (E.D. Va. 2016). | Every obligation a tenant owes under the lease (rent, damage, cleaning, fees) arises from the housing transaction and is a "debt". A tort claim against a non-party to the lease is not that person's debt. |
| BU-US-state-exemption | `US:15USC1692o-NY-VA-none` | Both forums: the CFPB Regulation F final rule preamble (85 FR 76734); the FTC Maine exemption (60 FR 66972). | Maine is the only State ever exempted, so the FDCPA and Regulation F apply in full in New York and Virginia. |
| BU-US-ph-pha-exclusion | `US:15USC1692a(6)(C)-PHA-staff`, `US:15USC1692a(6)(C)-private-manager` | Both forums: 1692a(8); *NLRB v. Hawkins County* (U.S. 1971); Va. Code 36-4 and 36-19; N.Y. PHL 3, 30 and 402; *Liles* (S.D. Iowa 2001). | Housing authorities in both States are political subdivisions, so their staff are excluded. A private management company is not, and is judged by the ordinary manager tests. |
| BU-US-handoff-model | `US:HANDOFF-config-pre-default`, `-post-default`, `-owner-name-only`, `-principal-purpose`, `-owns-balance` | NY: *Alibrandi*, *Vincent* (2d Cir. 2013), *Maguire* (2d Cir. 1998), *Goldstein* (2d Cir. 2004). VA: the same weight, plus *Dickenson* (S.D. W. Va.) and *Ramsay* (D. Md.). Both: *Henson* (U.S. 2017); *Barbato* (3d Cir. 2019) as the weight on principal purpose. | See the Handoff configurations below. |
| BU-US-hcv-promptly | `US:24CFR982.313(d)-promptly` | Both forums: 982.313(c)-(d) and 983.259; the HUD-52641-A tenancy addendum para. 15; the HCV Guidebook (2025). | "Promptly" has no federal day count. It means without delay once charges are fixed, and never later than the State deadline (NY 14 days; VA 45 days). Meeting the State deadline satisfies it. |
| BU-US-special-claims-availability | `US:HUD-SpecialClaims-renewal`, `US:HUD-SpecialClaims-procedure` | Both forums: form HUD-9637 sec. 5; 880.608(f) and its parallels; the HUD Special Claims Processing Guide, ch. 1 and 5. | Renewal contracts carry the claim provisions forward. HUD requires three things before a claim: a certified demand letter, referral to a collection agency, and an itemized list. The claim must be filed within 180 days. |
| BU-US-scra-cotenants | `US:50USC3955(a)(1)-all-parties` | Both forums: 3955(a)(1) text; H.R. Rep. No. 108-683 (2004). No court decision was found. | The lease ends as to every party on the effective date. Non-dependent co-tenants owe nothing for later periods but remain liable for amounts that accrued earlier. |
| BU-US-scra-deposit-clock | `US:50USC3955-deposit-clock-NY`, `US:50USC3955-deposit-clock-VA` | NY: GOL 7-108(1-a)(e) and 7-107(6). VA: 55.1-1226(A). Both: 3955(d), (f) and (h). | New York's 14 days run from vacating. Virginia's 45 days run from the later of the effective termination date and vacating. Neither State allows holding the deposit for rent after termination. |
| BU-US-scra-distress-lien | `US:50USC3951-distress-VA`, `US:50USC3951-distress-NY`, `US:50USC3958-lien-enforcement` | VA: Va. Code 8.01-130.1 to 8.01-130.13 and 55.1-1254. NY: *Van Rensselaer v. Snyder* (N.Y. 1855), on the 1846 abolition of distress. Both: 3951 and 3958 text. | Virginia distress, and selling a servicemember's goods to apply the proceeds, both need a court order. Plain disposal of abandoned goods does not. New York has no distress remedy at all. |
| BU-US-ph-former-tenant-grievance | `US:24CFR966.53(f)-former-tenant`, `US:24CFR966.4(b)(4)-after-vacating` | Both forums: 966.53(f), 966.51(a)(1) and 966.4(e)(8); the HUD PHOG grievance chapter. | A person who has vacated is not a "tenant" and has no grievance right for charges first noticed after move-out. The two-week due-date rule and the statement of grounds still apply, and a grievance requested before vacating runs to completion. |
| BU-US-eiv-debts | `US:24CFR5.233-debts-owed-PHA`, `US:24CFR5.233-multifamily-no-debts` | Both forums: 24 CFR 5.233; Notice PIH 2018-18; HUD EIV FAQs; form HUD-52675; Handbook 4350.3 ch. 9. | PHAs must enter former participants' balances within 60 days, whether they pursue or write them off. Multifamily owners have no EIV debt-reporting step. |
| BU-US-assistance-animal-charges | `US:42USC3604(f)(3)(B)-animal-fees`, `US:24CFR5.303-animal-program-rules`, `US:42USC3604(f)(3)(B)-animal-damage` | Both forums: 3604(f)(3)(B); 24 CFR 100.204, 5.303 and 960.705; 7 CFR 3560.204(b)(4); the PHOG lease chapter; *Goldmark* (D.N.D. 2011). FHEO-2013-01 and FHEO-2020-01 were withdrawn effective 2025-09-17 (91 FR 17291). | Pet fees, pet deposits and pet-based deductions for an assistance animal must be waived when the accommodation is necessary and reasonable, and are barred outright in HUD and RD programs. Actual damage is chargeable like any tenant damage. |
| BU-US-880-anchor | `US:24CFR880.608(d)-anchor` | Both forums: 880.608(c)-(d); model lease para. 8d; Handbook para. 6-18 C (guidance). | The 30 days run from receipt of the vacated family's forwarding address, or from vacating if the address came earlier. The handbook's move-out date is never later, so meeting it meets both. New York's 14 days governs in NY; the federal 30 days governs in VA. |
| BU-US-model-lease-notice-condition | `US:HUD-90105a-8a-state-law` | Both forums: 880.608(d) ("subject to State and local law"); Handbook 4350.3 para. 6-4 E (follow the rule most beneficial to the tenant); GOL 7-108 and 7-103(3); Va. 55.1-1226(A), 55.1-1208 and 55.1-1201(A). | Para. 8a cannot forfeit the deposit. Only State-permitted deductions apply, including rent actually owed because of short notice. |
| BU-US-rd-unclaimed | `US:7CFR3560.204(f)-state-unclaimed` | Both forums: 7 CFR 3560.204(e)-(f); USDA HB-2-3560 para. 4.7; N.Y. ABP 1315(2); Va. 55.1-1226(B) and the Unclaimed Property Act. | (f) does not displace State unclaimed-property law. The funds go to the operating account, and the borrower still reports or pays the State when State law requires. Complying with both is possible, so nothing is preempted. |
| BU-US-deposit-setoff-bankruptcy | `US:11USC362(a)(7)-deposit-is-setoff`, `US:CASE-Strumpf-hold` | NY: *Sweet N Sour* (Bankr. S.D.N.Y. 2010); *Malinowski* (2d Cir. 1998), which confines recoupment narrowly. VA: no Fourth Circuit ruling; *In re Cole* (Bankr. D. Md. 1989). Both: *Strumpf* (U.S. 1995); 11 U.S.C. 553(a). | Applying a lease deposit is a stayed setoff, not recoupment, so it needs stay relief first. A temporary hold while the landlord promptly seeks relief is allowed. |

## Handoff configurations (BU-US-handoff-model)

Stage A states the law for each configuration. Which one Handoff adopts is Owen's operating choice, not a Stage A
question.

- **A. Engaged before default.** Handoff takes on the account at lease-up, notice or move-out. It is excluded by
  (F)(iii) for that account, whatever its principal purpose and in whatever name it writes.
- **B. Engaged after default.** Handoff is a debt collector if it collects for others regularly (the *Goldstein*
  factors), or if collection is its principal purpose. It must then write under its true name (1692e(14)).
- **C. Owner writes under Handoff's name, with no real collection work by Handoff.** The owner becomes a debt collector
  under the false-name clause, and Handoff is liable under 1692j (*Vincent*). This does not apply if Handoff in fact
  collects, or if the name was used from the start of the tenancy (*Maguire*, *Franceschi*).
- **D. Collection is the principal purpose of Handoff's business.** Handoff is covered for every account that (F)(iii)
  does not exclude (*Barbato*).
- **E. Handoff buys balances.** Handoff falls outside the "collects for another" clause (*Henson*), but not outside the
  principal-purpose clause.

## Existing atoms revised in the same pass

These atoms' effects no longer point at open questions:
- FDCPA: 1692a(5), 1692a(6)(C), 1692a(6)(F)(i), 1692a(6)(F)(iii), 1692a(6)-principal-purpose, 1692j(a), 1692o, and
  CASE-Romea-1998.
- SCRA: 3951(a)(1)(B), 3955(a)(2), 3955(f), 3958(a).
- HUD voucher programs: 982.313(d), 983.259(c)-(e).
- Public housing: 966.4(b)(4), 966.4(n)(1), 966.53.
- Project-based Section 8: 880.608(d), 880.608(f), HUD-4350.3-6-18C, HUD-90105a-8.
- Other: 7CFR3560.204(d)-(f), 42USC3604(f)(3)(B), 11USC362(a)(7).

Four case-walk notes were rewritten:
- `handoff_collects_for_owner`;
- `former_tenant_in_bankruptcy`;
- `servicemember_early_termination_VA`;
- `hud_voucher_tenant_moves_out_VA`.

## New sources (all mechanically saved under `sources/`)

State texts read for federal questions use the prefix `US_x`.

- **Cases:**
  - Alibrandi; Vincent; Maguire; Goldstein; Malinowski.
  - Wilson v. Draper & Goldberg; Mabe; Harris; Barbato.
  - Citizens Bank v. Strumpf; NLRB v. Hawkins County.
  - Franceschi; Sweet N Sour; Yergovich; Galdamez; Ramsay; In re Cole; Dickenson; Liles.
  - FH Dakotas v. Goldmark; Van Rensselaer v. Snyder.
- **Federal Register and agency documents:**
  - Regulation F 2020 final rule; FTC Maine exemption (1995); FTC FDCPA staff commentary (1988); HUD FHEO guidance
    withdrawal (2026).
  - Notice PIH 2018-18; EIV FAQs; form HUD-52675.
  - PHOG grievance and lease chapters.
  - Handbook 4350.3 ch. 1 and ch. 9; Special Claims Guide ch. 1 and ch. 5.
  - Forms HUD-9637 and HUD-52641-A; HCV Guidebook (2025).
  - USDA HB-2-3560 ch. 4, saved from the ahacpa.org mirror because rd.usda.gov returned HTTP 403.
  - H.R. Rep. No. 108-683; DOJ-hosted CRS SCRA explanation.
- **Statutes and rules:**
  - 11 U.S.C. 553.
  - 24 CFR 5.100, 5.233, 5.303, 880.606, 891.410, 960.705, 966.51, 982.308. US_24CFR_960.707.txt was re-fetched, and its
    text is unchanged.
  - Va. Code 8.01-130.1 et seq.; Va. Code 55.1 ch. 14 art. 4; Va. Code 36 ch. 1.
  - N.Y. Pub. Hous. Law 3, 30, 402.

## Retrieval notes

- **CourtListener:** the search API works without a key but allows 5 requests a minute. Opinion pages are bot-walled for
  curl; `web_extract` works, but results can arrive one call late, so match the returned URL before saving.
- **Truncated extracts:** the Wilson and Vincent extracts were cut off at about 50,000 characters. The quoted passages
  lie inside the saved text.
