# An agentic legal engine for the end of the tenancy

2026-09-28. This is research and reasoning for a direction decision, not an approved scope. The evidence slice is
`slice.py` / `slice.json`: 20 atoms of the deposit-settlement chain in NY, CA and VA. Each atom carries a verbatim
statute quote; a check fails when a quote is altered (tested). Statute texts were retrieved today and saved under
`sources/`.

**Correction (same day).** The 20-atom slice and the comparison table in section 2 are drawn from three sections
only. They are not the applicable law. The first Stage A discovery pass (`STAGE_A.md`) found the following:
- NYC rent-stabilized units follow GOL 7-107, not 7-108.
- NY deposits carry trust and interest duties (GOL 7-103) that change the amount returned.
- Holiday rollover is fixed by statute in all three states.
- Virginia preempts local ordinances and requires a move-in damage report within 5 days.
- Several operative subsections of each core section are missing.

Treat section 2 as an illustration of the method, not as meaning.

## 1. The idea, stated precisely

Four bodies of work, one architecture:

| Source | What it contributes |
|---|---|
| Nay, *Law Informs Code* (2023) | **Why.** Law turns vague human goals into legible directives. Rules can be specified in advance; standards ("reasonable", "wear and tear", "bad faith") generalize to situations nobody enumerated. AI has moved from rule-following ("AI-contract") to standard-applying ("AI-standards") capability. The agent's own behavior can be specified through legal concepts. |
| CORDON | **How to compile law without corrupting it.** Staged derivation: A legal meaning, B clocks and parameters, C deterministic evaluators, D evidence contracts, E actions, F nouns, G platform. One fact has one owner. Checks must be able to fail. The aperture is set by the decision chain. Bounded unknowns are named, never filled. Built and accepted for real EU/Italian/Puglia law: 426 provision versions, 126 clocks, 171 parameters, 902 dispositions. |
| Jev (Slope Sparse Events) | **The semantic interface.** A fast, typed judgment (Choice, Score, yes/no) at the joint between evidence and a predicate. Authority is asymmetric: a Jev answer never sets an amount or a date, and it enters the record only through the agent's acceptance and code validation. Every answer is logged with what it caused. "Unknown is a typed state, never zero." |
| Handoff | **The operating substrate.** It runs the physical work that produces the legal evidence: quotes, invoices, photos, visit reports, notices. It owns the action plane (orders, payments, correspondence), the operator's accept/change decision, and point-in-time records. |

Together: **the law's operative meaning is compiled into atoms. Code evaluates what is determinate. A typed semantic
sensor binds real evidence to each predicate and breaks standards down into checkable questions. An agent
investigates, drafts and schedules the physical work to meet legal clocks. The operator makes the judgments that law
or the owner reserves.** The same atoms also bound what Handoff's own agent may do. That is Nay's thesis applied
literally: law informs the code of the agent itself.

## 2. What the three statutes show (from the slice)

Each state has the same obligation: account for the deposit after move-out. Every atomic component differs:

| Component | New York GOL 7-108(1-a) | California Civ. 1950.5 | Virginia 55.1-1226 |
|---|---|---|---|
| Clock anchor | tenant vacated | tenant vacated (not before notice / 60 days before term end) | later of termination or vacating |
| Window | 14 days | 21 calendar days | 45 days |
| Extension | none stated | good-faith estimate, then documents within 14 days of completion | +15 days if contractor notice given within 45 |
| Miss the deadline | forfeit any right to retain, no intent element | forfeit only on bad faith; up to 2x for bad-faith retention | willful: return deposit, damages, attorney fees |
| Move-in dependency | conditions noted in the move-in agreement can never be deducted | move-in photos required for tenancies from 2025-07-01; repair/cleaning deductions must attach them | move-out report is evidence |
| Pre-move-out | inspection 1-2 weeks before end, 48 h notice, cure | initial inspection on request, cure, itemized list binds | tenant may attend inspection within 72 h of possession |
| Burden | landlord proves reasonableness | landlord proves reasonableness (bad-faith actions) | not stated in section |

Of the 20 atoms, 10 are pure rules (code decides), 5 are standards (judgment), and 5 mix both. That split is Nay's
point made concrete. The value is not a deadline table. It sits at the joints:

1. **Legal clocks drive the physical schedule.** In California, a repair not finished within 21 days turns the
   statement into an estimate with a second 14-day clock. In New York there is no estimate mechanism in the text,
   and a miss forfeits everything. So the vendor schedule, the invoice and the photos must land inside 14 days, or
   the statement has to deal with work not yet invoiced (a bounded unknown in the slice). Handoff's coordinator
   already schedules vendors; today it does so without knowing the legal clock.
2. **The physical work produces the legal evidence.** California requires the vendor's bill, name, address and phone
   number, plus before-and-after photos, with each repair deduction. Handoff's turn already produces those records.
   The evidence contract (CORDON Stage D) is satisfied by the work Handoff runs.
3. **Obligations cross time.** The move-in record governs what can be deducted at move-out, in both New York and
   California. A move-out product cannot recover a missing move-in photo. Handoff's own adjudication addendum said
   this in September; the statute text confirms it.
4. **Failure is asymmetric.** New York punishes lateness regardless of intent. California and Virginia punish bad
   faith or willfulness, which are standards. So the same late statement is fatal in New York and defensible in
   California if the record shows good faith. The engine's job is different in each: prevent the miss in New York;
   document good faith in California.

## 3. Broader implications

**a. It is the defensible core of the accountable-service path.** The simulation's leading path (P9, service first,
then software) wins on revenue and funding because an outcome is worth more than a tool. Taking responsibility for a
landlord's money at move-out is only credible if the settlement is legally right, on time, and backed by evidence.
The legal engine is what makes that responsibility safe to take. It is also what converts service to software: the
judgment-heavy part becomes automatable only when its rules are compiled and its standards are decomposed and
measured.

**b. The regulatory uptick turns rule maintenance into recurring value.** California added photo mandates in 2025.
Colorado presumes a retention unreasonable at 125% or more of actual damages (2026). Michigan's act took effect
September 21, 2026. The FTC opened a rental-fee rulemaking on March 12, 2026 covering "application to moveout"
(L4 §findings). Each change is a versioned atom with effective dates, evaluated point-in-time against open cases.
That is CORDON's reopening discipline, and it is work a property manager cannot do per state. Competitors sell
deadline tracking (TurnOps, Obligo's agent). What they don't visibly sell is faithful point-in-time meaning bound to
the evidence and the physical work.

**c. The direction becomes "obligations across the tenancy", for the same buyer.** Each step reuses A-D and the
physical loop. From move-out settlement to:
- the move-in baseline (legally required in California);
- renewal and rent-change notices (NY RPL 226-c; Virginia requires 90 days' notice of rent increases from July 1,
  2027, per the L4 ledger);
- fee compliance (Colorado HB25-1090, FTC);
- repair and habitability clocks.

This is the "tenancy depth" direction, sharpened: expansion along legal families that share one buyer, one evidence
base and one action plane.

**d. The abstract engine generalizes. The product should not, yet.** The staged pattern is domain-independent:
- CORDON: plant-health removal orders.
- Slope: litigation and covenant effects on credit.
- Handoff: tenancy obligations.

The pattern in each is an authority's decision chain, then atoms, clocks, evaluators, evidence and actions. Selling
that as a horizontal legal engine now would compete with Norm Ai (regulatory AI agents and legal engineering) and
with open rule languages (Catala, OpenFisca). There is no demonstrated buyer for a horizontal compiler, and
Handoff's own adjudication deferred it. First principles give the split: **build the method horizontally as internal
infrastructure; sell it vertically where the value is measurable.** Revisit a horizontal product when repeated demand
appears, for example a PMS vendor or deposit insurer asking to license the settlement layer (simulation path P6).

**e. Founder fit is real, and the jurisdiction choice needs one correction.**
- Owen has built and had accepted a staged legal compilation of real law (CORDON A-C) and a typed judgment plane
  (Slope/Jev). Few founders in property technology have done that.
- California, Virginia and New York are where the founders are from or live, which gives access.
- The adjudication addendum's rule still holds: choose jurisdictions from customers' footprints, not founder
  residence. Here both point the same way on merit: the strictest consequences (New York forfeiture, California
  photo mandates and 2x damages) are where an engine prevents the most loss.
- Difficulty is uneven:
  - New York City needs unit-status facts, because 7-108(1-a) excludes units under the named rent laws, and local
    law adds more.
  - California cities add ordinances.
  - Virginia (Charlottesville) is the cleanest first test.

## 4. Division of labor

| Work | Owner | Examples |
|---|---|---|
| Applicability, clocks, thresholds, forfeiture conditions, amounts | Code (A-C compiled) | 14/21/45-day deadlines; $125 documentation threshold; VA later-of anchor; 2025-07-01 photo applicability |
| Evidence-to-predicate binding and standard decomposition | Jev-style typed judgments, logged with disposition | Does this photo show the deducted item? (yes/no). Is this condition ordinary wear and tear, damage, or prior-tenant damage, given the move-in record? (Choice). Does this invoice line cover the deducted condition? Does the notice include the required statutory text? |
| Investigation, drafting, scheduling to meet clocks, reconciliation | Agent | Draft the itemized statement; move a vendor visit to land before day 14; ask for the missing move-in record |
| Reserved judgment | Operator (and owner instructions) | Whether to pursue a permitted charge; concessions; accepting the statement |
| Standards themselves | Stay standards | The engine never turns "reasonable" or "bad faith" into a number. It shows the evidence that bears on them. |

## 5. Limits and risks

- **A frontier model can read these statutes.** The engine's value is point-in-time faithfulness, deterministic
  clocks, evidence binding and auditability, and it must be proven. Use the adjudication addendum's three-way test:
  the existing process, against a capable model with the same documents, against the model with the compiled
  representation. If the representation does not beat the plain model on decision quality at acceptable cost,
  don't build it.
- **Liability** [unverified; needs counsel]:
  - Computing a landlord's own obligations resembles compliance or tax software.
  - Sending statements for landlords is closer to agency.
  - Recovering balances raises debt-collection and licensing questions.
- **Maintenance:** every state and many cities. CORDON's aperture rule limits scope to one decision chain, with
  states added as customers require.
- **Bounded unknowns already visible:**
  - holiday rollover statutes;
  - New York's missing estimate mechanism;
  - New York's exclusions;
  - local law;
  - what counts as delivery.

  A generic tool would silently guess these.

## 6. What would test it cheaply

1. **Walkthroughs.** Reconstruct each operator's last 10 move-outs against the statutory clock: days to statement,
   evidence present (move-in photos, invoices), disputes, forfeitures, estimates.
2. **Stage A closure** for the settlement chain in NY, CA and VA, including the bounded unknowns above.
3. **The three-way evaluation** on about 20 reconstructed cases before any build into Handoff's tenant-account phase.
