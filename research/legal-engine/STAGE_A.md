# Stage A: legal meaning for the departing tenancy's financial settlement

Current scope (Owen, 2026-09-30): every state in Holland Partner Group's portfolio (CA, WA, CO, OR, AZ) with its local
layers, each built through the jurisdiction-pipeline skill under `jurisdictions/<CODE>/`. NY, NYC, VA and US are
compiled and parked; NYC's register review is applied (see the 2026-09-30 entries under "Status after the resolution
pass"). The Jurisdictions section below is the 2026-09-28/29 record and is superseded where it differs.

Owner of Stage A scope, method and closure state for this chain. `slice.py` is an earlier sample and is not Stage A.

## Chain (aperture)

Set by the intent notepad (Handoff resolves the departing tenancy's financial relationship) and Owen's 2026-09-28
choice (a). The chain runs from the notice of an ending tenancy, or the tenant vacating, to the account closed:
- the deposit, including any interest owed on it;
- each charge and credit;
- the itemized statement, the refund method and the payee;
- the balance owed, and the decision to pursue it, hand it off or write it off.

The aperture includes every provision that constrains that chain, wherever it sits in time:
- move-in records;
- the pre-move-out inspection;
- notice and delivery;
- applicability and exemptions;
- time computation;
- transfer to a successor landlord;
- trust and interest duties;
- local law for the unit's location;
- federal overlays.

Other actors (collectors, courts, insurers) enter only where their law changes the landlord's or manager's
decision in this chain.

## Jurisdictions (Owen, 2026-09-28)

- New York State and New York City first. NYC's local layer includes rent stabilization, rent control and city rules.
- Virginia second. It has no local layer (55.1-1201(E)).
- California is out for now. A California unit is out of scope, not answered. (Superseded 2026-09-30: California,
  Washington, Colorado, Oregon and Arizona are in scope; NYC and Virginia are parked.)
- Review and first test cases: NYC market-rate units (GOL 7-108) first; rent-stabilized and rent-controlled units
  next. Both stay fully compiled (Owen, 2026-09-28, (a)).
- Current focus (Owen, 2026-09-29): NYC market-rate units only. Rent-stabilized, rent-controlled and Virginia work is
  parked, not expanded. Conditions that keep the narrowing from becoming an omission:
  1. Scope gate: Step 0 classifies the unit; a stabilized, controlled or undetermined unit is a typed "outside this
     engine" state routed to the operator, never defaulted to GOL 7-108.
  2. Parked, not discarded: VA.json and the stabilized/controlled atoms stay in the files (resolution pass done, no
     independent review yet). Resuming either costs one independent review plus adjudication.
  3. The first paying operator's footprint decides the next regime; the operator walkthroughs are not a build and
     can run now.

Output: one file per jurisdiction in `stage-a/`, checked by `stage_a_check.py`. The check covers required fields,
verbatim quotes against saved sources, dependency closure, and bounded unknowns that name what they block and how
to close them.

## Discovery method (a source list does not define the forest)

Each state is read through every family below. Cross-references alone miss families 2-9.

1. Outbound cross-references from each operative section, followed recursively.
2. The whole enclosing chapter or article, not the section. VA: Code 55.1 ch. 12 (VRLTA). NY: GOL art. 7 title 1,
   RPL art. 7. CA: Civ. Code div. 3 pt. 4 title 5 ch. 2 (1940 onward).
3. Applicability, exemptions and definitions.
4. General provisions: time computation, notice and delivery, electronic records and signatures.
5. Point-in-time versions: enacted-but-future text and session laws (e.g. VA 55.1-1202 has a version effective
   2027-07-01; CA 1950.5 amended by AB 414, effective 2026-01-01).
6. The local layer for the unit's location, or a verified preemption.
7. Regulatory status that routes a unit to different provisions (NY rent stabilization and rent control).
8. Federal overlays that control where inconsistent (HUD for public housing; debt-collection law at hand-off).
9. Interpretive authority, only where it fixes the operative meaning of an atom (e.g. "willful", "bad faith",
   whether a statute applies to leases signed before its effective date).
10. Preconditions to recovery: facts about the building, owner and collecting agent that bar or condition rent
   recovery or decide who may collect (NY: certificate of occupancy MDL 301-302, registration MDL 325(2),
   rent-impairing violations MDL 302-a, agent licensing). Reading outward from the deposit statute never reaches
   this family; both independent reviews of the NYC market-rate walk found gaps here. Sweep it on purpose.

## Exit (CORDON Stage A)

The decision-reachable legal forest resolves:
- from controlling authority down to operational descendants;
- and back from materially different real cases.

Bounded unknowns are explicit, and Owen accepts. Cases test and instantiate the law; they do not define it. Cases to
test against, at minimum:
- NYC rent-stabilized unit; NYC rent-controlled unit; NYC market-rate unit in a building with 6 or more units;
- NYC unit in a building with fewer than 6 units;
- a lease signed before the 2019 HSTPA changes, and one signed after;
- early termination; damage above the deposit that needs a contractor;
- VA utility withholding; a VA tenant who paid damage insurance instead of a deposit;
- multiple tenants with one leaving; no forwarding address;
- the building sold mid-tenancy; abandoned property;
- a statement due on a weekend or holiday.

## First discovery pass (2026-09-28): what it changed

Each finding below either falsifies the slice or fills one of its gaps. Sources are saved in `sources/`, or noted
where the site blocked saving.

| # | Finding | Source | Effect on the slice |
|---|---|---|---|
| 1 | NY 7-108(1) routes NYC rent-stabilized and ETPA units to **7-107**. CORRECTED by the Stage A pass: 7-107's 14-day statement and forfeiture come from L.2025 c.436 and apply only to leases and renewals entered on or after 2025-11-15 (bill s.2). Before that, 7-107 held only successor liability. Stabilized tenancies on earlier leases are an open seam between NY.json and NYC.json (BU-NY-07107-transition). 7-108(1-a) separately excludes units under the city rent and rehabilitation law and the emergency housing rent control law. | NY GOL 7-108(1), 7-107(1) (nysenate.gov) | Routing error. The slice treated both groups as one "excluded" set. Rent-controlled units need the rent-control regime, which is not yet read. |
| 2 | NY deposits are held in trust and not commingled. Buildings with 6 or more units must use an interest-bearing account. The tenant is owed the interest less a 1%-a-year administration fee, paid at termination as collectable. | NY GOL 7-103(1), (2), (2-a), (2-b) (nysenate.gov; saving blocked) | Amount error. "Return any remaining portion" includes accrued interest. The slice had no interest term. |
| 3 | Time computation is statutory, not an unknown. NY: the event day is excluded (GCN 20); a period ending on a weekend or public holiday moves to the next business day (GCN 25-a). CA: exclude the first day, include the last; a holiday, including any Saturday, extends to the next non-holiday (Civ. 10; CCP 12a). VA: the event day is not counted (1-210(A)); an act due on a weekend or holiday may be done on the next business day (1-210(E)). | NY GCN 20, 25-a; CA_CIV_10.txt, CA_CCP_12a.txt; VA_1-210.txt | Closes the slice's first bounded unknown. Adds a rollover rule to Stage B. Holiday calendars become Stage D inputs. |
| 4 | Virginia's local layer is preempted: the chapter supersedes all other local ordinances on landlord-tenant relations. Where HUD regulations are inconsistent for public housing, they control. | VA_55.1-1201.txt (A), (E) | Closes the local-law unknown for VA. Adds a federal overlay. |
| 5 | VA applicability: named tenancies are not residential tenancies (e.g. a tenant who pays no rent; an employee occupancy conditioned on employment; transient lodging under 90 days). | VA_55.1-1201.txt (C), (D) | Missing applicability branch. |
| 6 | VA move-in report: the landlord itemizes existing damage within 5 days of occupancy. The report is deemed correct unless objected to within 5 days of receipt. | VA_55.1-1214.txt (A)-(C) | Missing cross-time evidence atom. The slice said only that the move-out report is evidence. |
| 7 | VA "Notice" is written notice by mail or hand delivery, with the sender keeping a certificate of service. Electronic notice is allowed if the lease provides for it, and the tenant may elect paper. 55.1-1202 has a new version effective 2027-07-01. | VA_55.1-1200.txt, VA_55.1-1202.txt | Delivery rules resolved for VA. Adds versioning. |
| 8 | Operative parts of the three core sections that the slice skipped. VA 55.1-1226 (B): multiple tenants get one check; unclaimed property goes to the State Treasurer after one year. (C): utility withholding needs 15 days' prior notice, and the balance is refunded within 10 days of confirmation. (D): expedited fee. (F): records kept 2 years. CA 1950.5 (b) permitted uses; (c) caps (1 month; 2 months for small natural-person landlords; service members); (e) limits; (h)(1)(A)-(C) refund method, including electronic return where the tenant paid electronically, and the multi-tenant rules; (i)-(k) successor landlord; (n) no "nonrefundable"; (p) proof. | VA_55.1-1226.txt; CA_CIV_1950.5.txt | The slice held 20 atoms from 3 sections. The core sections alone carry several times that, before families 2-9. |
| 9 | CA 1950.5(f)(1) requires notice text about reclaiming abandoned property. That links the chain to Civ. 1980 onward. | CA_CIV_1950.5.txt | New outbound dependency, not yet read. |

## Status after the resolution pass (2026-09-28, current)

- Candidates for Owen's review: stage-a/NY.json (177 atoms), NYC.json (182), VA.json (277), US.json (175); 811
  atoms (541 RULE, 234 MIXED, 36 STANDARD), 90 of them interpretive with verbatim construction quotes and reasoning.
- Zero open questions. The joint check passes, including cross-file references; a changed quote fails it.
- Each former question maps to its atoms in stage-a/RESOLUTION_{NY,NYC,VA,US}.md.
- Parent fixes after the workers: removed the hedge in NY:CASE-Gelbart-rent-offset; resolved US:15USC1602(f)
  (a payment plan for a balance is credit) and branched NYC:RCNY6-5-77(f)(1)-landlord-not-TILA-creditor on
  1602(g) (a landlord regularly offering installment plans of more than four payments becomes a TILA creditor).
- Builder scripts and backups copied out of scratch to build/ and build/backups/.
- Review order (Owen, (a)): NYC market-rate chain, then rent-stabilized and rent-controlled, then Virginia.
- Independent review of Review 1 (review/INDEPENDENT_REVIEW_1.md): 17 findings, all verified and applied
  (review/REVIEW_1_DISPOSITION.md). NY.json now 190 atoms, NYC.json 185, US.json 176.
- Independent review round 2 (review/INDEPENDENT_REVIEW_2.md): 13 findings plus one Ferro addition (MDL 302-a),
  adjudicated, approved by Owen and applied (review/REVIEW_2_DISPOSITION.md). NY.json now 201 atoms. R2-08 (RPL 232)
  and discovery family 10 go to a targeted sweep (review/SWEEP_BUILDING_OWNER.md), then a third review limited to
  the changes and that family. The sweep finished 2026-09-29 (review/SWEEP_BUILDING_OWNER.md: 34 atoms; RPL 232 runs a
  no-term agreement to October 1 per Stauber; collecting rent for a fee needs a broker licence per RPL 440). Its walk
  text is folded into review/NYC_MARKET_RATE.md (499 in scope, 0 missing).
- Independent review round 3 (review/INDEPENDENT_REVIEW_3.md): 14 findings, all applied (review/REVIEW_3_DISPOSITION.md);
  RPL 232 reversed (a bare monthly rent is month to month, Gerolemou). NY.json 233 atoms; walk 507 in scope, 0 missing.
- Round 4 (Owen, option c: "the applicable law isn't something we can afford not having the full and precisely correct
  universe of"): split into 4A, a blind enumeration of the applicable-law universe diffed against the files, and 4B,
  a correctness review of every in-scope rule. 49 findings (12 critical), all applied (review/REVIEW_4_DISPOSITION.md):
  NY 258 rules, NYC 200, US 190; walk 551 in scope, 0 missing.
- Round 5 (Owen, option c: "this is designed so that if you get it right the first time, convergence has to happen at
  some point"): same two-part design; 5A also compares its blind universe with 4A's to measure convergence. 51 findings
  applied (review/REVIEW_5_DISPOSITION.md): NY 291 rules, NYC 201, US 198; walk 593 in scope, 0 missing. Correctness
  converged (15 -> 10 findings, core rules held); completeness did not (41 new gaps; the two blind lists share 148 items).
- Completeness by construction (Owen, option a, "the perfect place to use Jev"): register/ holds the closed list of
  instruments and every section of each in-scope unit, each classified as stated by a rule, changes no decision, or
  outside the aperture; Jev (typesafe/jev-1.13 via OpenRouter) triages unstated sections after a calibration run, with
  code-owned asymmetric routing so a possible rule goes to review. Jev never states law. Built 2026-09-30
  (register/README.md): 63 instruments, 289 units in scope, 3,686 sections; 312 stated, 2,496 in the review queue,
  878 triaged as deciding nothing; calibration recall 315/315 at routing v2; 3,582 Jev requests, $0.28.
  check_register.py passes. Queue tiers by Jev score: 63 strong, 718 likely, 891 possible, 716 low-confidence
  only, 108 long or unscored.
- Queue review (Owen, option a: every queued section gets a reviewer decision): six reviewers by instrument family
  (register/work/batch_1-6.json, 2,498 sections incl. MDL 9 and RPL 442-C pulled back from Jev's set-aside list).
  Each writes register/work/decisions_N.jsonl (stated | partial | new_rule | no_decision | excluded_regime), checked
  by register/work/check_decisions.py (verbatim quotes, existing ids, no hedging, no undecided section). Proposed rules
  come to Owen with Ferro's adjudication before any rule-file edit. Done 2026-09-30: 2,498/2,498 decided, 582 rules
  proposed (106 critical), adjudication in register/work/ADJUDICATION_QUEUE.md. Five deciding sections carried
  set-aside-level Jev scores, so the 876 set-aside sections are reviewed too (batches 7-8, done 2026-09-30: 14 more rules
  proposed).
- Scope change (Owen, 2026-09-30): the first prospect is Holland Partner Group, managing 61 communities in CA (21),
  WA (19), CO (12), OR (8) and AZ (1) (research/holland/communities.json). NYC: finish the set-aside review, apply the
  adjudicated findings, then park until an NYC customer. Stage A then covers every Holland state and its local layers,
  after the Holland research (research/holland/) sets the cities and building ages.
- Register review applied (2026-09-30, Owen's go): the 596 queue proposals became 594 rules (2 merged into fuller
  ones), plus 4 rules for 11 U.S.C. 362 and 9 from the adjudication's scope additions (TILA part B, 16 CFR 682,
  26 U.S.C. 6050I, 6050W, 6045(f)); 35 existing rules changed by the rulings; every named authority saved and quoted
  (sources/REGISTER_*) except In re Miller (not found; its point rests on 507(a)(7)'s text). NY.json 694 rules, NYC.json 244, US.json 359 (VA.json 277, unchanged). Walk 1,200 in scope,
  0 not cited. Every register section carries a reviewer decision (check_register.py strict passes). Disposition:
  review/REGISTER_DISPOSITION.md. NYC Stage A is now parked; work moves to the Holland states.
- Review 1 (market-rate NYC) is ready at review/NYC_MARKET_RATE.md. review/show.py prints any rule with its quote
  and sources. review/check_review.py confirms every cited id exists and every in-scope rule is cited or deferred.

## Status after the second pass (2026-09-28, superseded)

- Candidate files: stage-a/NY.json (161 atoms), NYC.json (153), VA.json (251), US.json (140). The joint check passes,
  including cross-file references. Nothing is accepted.
- One owner per fact: the 11 federal atoms that NY.json held were removed and now point to US.json ids (backup in
  profile scratch, NY_pre_dedupe.json).
- The pre-2025 rent-stabilized gap is resolved as law. State law sets no refund deadline, statement or forfeiture for
  a stabilized tenancy whose lease or renewal predates 2025-11-15 (the A6423-A sponsor memo states the gap). What
  governs is the common-law return rule, the 7-103 trust and interest duties, and RSC 2525.4. The open risk is one
  trial court (Karole, 2022) that applied 7-108(1-a) through RSC 2525.4: BU-NY-RS-pre2025-by-reference (counsel).
- Open questions: 57, listed in stage-a/OPEN_QUESTIONS.md (generated). Owner 5, counsel 28, case law 13, reading 9,
  event 2.
- Per-file second-pass reports: stage-a/SECOND_PASS_NY.md, SECOND_PASS_NYC.md, SECOND_PASS_VA.md.

## Still open after the first pass (historical; see OPEN_QUESTIONS.md for current state)

- NY RPL art. 7 and any other NY provision that governs charges beyond the deposit. NY rent control.
- NYC local law: Rent Stabilization Code; the NYC Administrative Code as it bears on this chain.
- California: out of scope for now (Owen, 2026-09-28). The CA findings above are kept for when it re-enters.
- VA 55.1-1227 and 55.1-1251 (tenant obligations and damages for breach, which feed permitted deductions), plus the
  rest of ch. 12.
- Charges beyond the deposit in all three states (rent, late fees, utilities, fees): what may be charged, and how a
  balance owed may be stated and pursued. At hand-off, federal FDCPA and state collection law, only where they
  change the manager's decision.
- Interpretive authority for the standards (reasonable, wear and tear, willful, bad faith), and for how each amended
  rule applies to existing leases.
