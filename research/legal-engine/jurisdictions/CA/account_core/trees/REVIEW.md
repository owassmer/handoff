# California account-core trees: review

October 3, 2026. Milestone step A2, for Owen's ruling. These are proposals; nothing here is accepted law for Handoff until you rule.

There are 34 trees, one JSON file per legal decision, in the format of `design/legal-trees.md`. Each one covers a California market-rate apartment move-out with 2026 event dates. All are layer `CA`, effective from January 1, 2026, the date the current (AB 414) text of Civil Code 1950.5 took effect.

Every leaf quotes the saved official text it rests on. `check_trees.py` fails if a quote is not verbatim in that text, if a quote cited to a subdivision is not inside that subdivision, or if a tree breaks the format; all 34 pass. `JEV_CHECK.json` holds the Jev fidelity check.

How to read a tree:
- **Leaf kinds:**
  - *determinate*: code settles it from records;
  - *semantic*: a narrow question over named evidence;
  - *discretionary*: someone decides; in these trees it is always the operator taking a side of a contested point.
- **Contested points** keep both readings with their authority. The exposure figure uses the reading least favorable to the operator.
- **Section numbers** are the Civil Code unless marked.

## How the main demonstration case runs through the trees

**Before move-out**
- The tenant's notice on October 12 triggers two written notices due that day: the offer of an initial inspection (`inspection-offer-notice`) and the right to an electronic refund (`electronic-refund-notice`), because rent was paid electronically.
- The tenant asks for an inspection. It may be held no earlier than October 27, with written notice 48 hours before, and the itemized list is handed over at the inspection on November 2.

**Rent and holdover**
- The lease ends November 10 and rent under the lease stops there (`rent-to-term-end`), provided no "rent" is accepted for days after November 10 while the tenant is still in the unit.
- November 11–16 is a holdover, charged at the schedule's daily rate (`holdover-charge`).

**Deductions**
- Each repair, cleaning and carpet line runs its deduction tree, which in turn checks the inspection list (`inspection-list-gate`).
- Water is deducted only with its final bill attached (`deduct-water`).

**Statement and refund**
- The statement is due December 7 (`statement-due`).
- The remainder goes back electronically to the account the tenant designated on the page (`refund-electronic`).
- That designation counts as a writing only because the page also collects a separate, optional agreement to deal electronically (`electronic-writing`).

## The trees

### DP3 — Rent through possession

- **`rent-to-term-end` (DP3.1).** Rent under a fixed-term lease stops on the last day of the term (Civ 1933). Two exceptions keep the tenancy going:
  - the tenant stays on and the landlord accepts rent for a period after expiry, which raises a presumption of renewal for a month at a time where rent is monthly (1945); the tree treats that presumption as rebuttable by the parties' evident intent;
  - the lease has an automatic-renewal clause that was triggered and is enforceable under 1945.5 (boldface rules).

  In practice: never take a payment described as rent for days after the lease end while the tenant is still in the unit; bill those days as holdover.
- **`month-to-month-end` (DP3.2).** A month-to-month tenancy ends on the date in the tenant's written notice if the notice was served in a 1946 manner and gave at least 30 days. A shorter notice works only if agreed when the tenancy began, and never under seven days. Rent is due to and including the termination date. This is where the renewed tenancy above leads. Owner-initiated endings (1946.1, just cause) are not compiled here.
- **`holdover-charge` (DP3.5).** For days after the tenancy ends, the landlord may charge the value of use (3334) when all of these hold:
  - the tenant stayed without permission;
  - no unlawful detainer court is assessing the damages;
  - the daily rate fits one of 3334's measures: within the reasonable rental value; within the benefit the tenant obtained, unless the stay was a mistake of fact; or a liquidated holdover amount in the lease that survives the 1671(d) penalty test.

  The amount is the number of days from the tenancy end to the return of possession, times the schedule's daily rate. That is six days in the demonstration.
- **`rent-after-abandonment` (DP3.3).** When a tenant breaches and abandons before the term ends, the lease terminates (1951.2). The same applies when the lease is deemed abandoned after a 1951.3 notice, or when the landlord ends possession for breach.
  - The landlord may recover unpaid rent earned to termination.
  - It may also recover rent lost since then, less re-letting income and any loss the tenant proves was avoidable.
  - The exception is a lease that keeps itself alive under 1951.4.
  - Rent after an award and the interest to award are litigation remedies, so they are left out of the deposit statement.

### DP4 — The pre-move-out inspection

- **`inspection-offer-notice` (DP4.1).** Once either side gives notice of termination, or as a fixed term nears its end, the landlord must tell the tenant in writing that they may request an initial inspection and be present. This duty, like all of subdivision (f), falls away when the tenancy ends under CCP 1161(2)–(4) ((f)(7)).
  - The law says "within a reasonable time". The operating date is the day notice is received, with the lease end as the outer limit.
  - Subdivision (f)(1) requires the abandoned-property statement in "written notice by the landlord" without saying which notice, so the tree puts it in both this notice and the 48-hour notice.
- **`initial-inspection` (DP4.1).** If the tenant requests an inspection and does not withdraw the request, the landlord must:
  - try to agree a time;
  - inspect no earlier than two weeks before the tenancy ends, and before any final inspection, whether or not the tenant is present;
  - hand over the itemized list of proposed repairs and cleanings, with the text of 1950.5(b)(1)–(4), or leave it inside.

  The tenant may cure until the tenancy ends. If the tenant never asks after a proper offer, the landlord's (f) duties are discharged.
- **`inspection-notice-48h` (DP4.1).** Written notice of the date and time at least 48 hours ahead, unless both sides sign a waiver or (f)(7) applies.
- **`inspection-list-gate` (DP4.2).** This tree decides whether the list bars a later deduction. A repair or cleaning that was not on the list is barred unless one of these applies:
  - the line is not a repair or cleaning at all;
  - the tenancy ended under CCP 1161(2)–(4);
  - no inspection was held because the tenant did not ask after a proper offer;
  - no inspection was held because the landlord skipped the offer or a requested inspection, which is contested (C9);
  - the tenant's belongings prevented identifying repairs at the inspection;
  - the item was listed and not cured;
  - it arose after the inspection;
  - belongings hid it.

  Every repair and cleaning tree requires this gate to pass.

### DP5 — What may be kept and charged

- **`deduct-unpaid-rent` (DP5.5).** Unpaid rent may be deducted (1950.5(b)(1)), up to the end date fixed by the DP3 trees.
  - A partial last period is prorated by the schedule's daily rate.
  - The 1942.4 bar is carried in full: it applies only if all five of its conditions hold, the first being an official written citation. It therefore drops out in an ordinary case.
- **`deduct-holdover` (DP5.5).** The holdover charge may come out of the security if either:
  - the lease makes holdover days rent, which puts it squarely in (b)(1); or
  - the "any purpose" reading of (b) applies (contested C6).

  Otherwise the holdover is billed separately.
- **`deduct-repair` (DP5.3).** A repair may be deducted when all of these hold:
  - the money is security;
  - the line repairs damage to the premises caused by the tenant or a guest;
  - the damage was not present at move-in;
  - it is beyond ordinary wear, which is broken into three questions: cause (accident, misuse or neglect against normal use or age), extent, and accumulated wear;
  - the inspection gate passes;
  - the work restores rather than upgrades;
  - the cost is reasonable.

  The amount is the cost times the tenant's share under the company schedule's useful lives. Documents and photographs are now a duty attached to the deduction, not a condition of it (see the Jev section).
- **`deduct-cleaning` (DP5.3).** Cleaning may be deducted when all of these hold:
  - the area was left less clean than at the start of the tenancy;
  - the soiling is not wear or accumulated wear;
  - the inspection gate passes;
  - the cost is reasonable;
  - for professional carpet cleaning or other professional services, the work was reasonably necessary to restore move-in condition ((e)(2)(C)).

  The inception standard applies only to tenancies that began after January 1, 2003. Older tenancies are outside this tree.
- **`deduct-personal-property` (DP5.1).** Keys, fobs, remotes and furnishings may be charged under (b)(4) when all of these hold:
  - the lease obliges the tenant to return or restore the item;
  - the lease authorizes using the deposit for it;
  - the tenant defaulted;
  - the loss or damage was not present at move-in and is not ordinary wear;
  - the cost is reasonable.

  A receipt is a duty attached to the deduction.
- **`water-final-bill` (PW3.3)** and **`deduct-water` (DP5.1).** These apply only where the submeter chapter does (1954.216).
  - The submeter is read within five days of the end of the tenancy if possible. If it cannot be, the final month is "based on" the previous month's bill (1954.207(b)).
  - The water bill may be deducted only if all of these hold: the bill carries only the charges 1954.205(a) allows, the admin fee is within its cap, no landlord penalties are passed through (1954.208), and the last bill is attached to the statement documents (1954.207(c)).
  - Following your decision, no tree estimates water or any other utility.
- **`deduct-other-charge` (DP5.2).** A lease debt outside the four listed purposes may be deducted only under the contested "any purpose" reading (C6). Examples are a gas or electric bill already issued, or a late fee. The debt must also:
  - be owed;
  - not be barred;
  - for master-metered gas or electricity, not exceed the utility's direct rate (PUC 739.5);
  - for a fixed sum such as a late fee, survive 1671(d).
- **`barred-charge` (DP5.3).** Charges barred whatever the lease says:
  - for physical-condition lines: preexisting conditions, ordinary wear, accumulated wear, unnecessary professional cleaning, and the part of any work that improves on move-in condition (AB 2801's stated intent);
  - for any line: anything resting on a "nonrefundable" clause, and fees for serving notices under CCP 1161 or Civ 1946.
- **`move-out-photographs` (PW3.3).** When possession returns on or after April 1, 2025 and repairs or cleanings will be deducted, the unit is photographed:
  - before that work starts, which is the hard limit;
  - again after it, with Handoff taking these at each job's completion check.

### DP6 — The statement and the refund

- **`statement-due` (DP6.1).** The deadline is 21 days after the tenant vacated, which is December 7 in the demonstration. Whether the tenant had vacated on the recorded date is a semantic question over keys, belongings and occupancy.
  - The statement shows the security received, its basis and disposition, and the remainder returned.
  - It may not go out before a termination notice, or earlier than 60 days before a fixed term ends.
  - The operating deadline is the nominal day 21. Both weekend and holiday extensions are computed as margin only (C5).
- **`repair-cleaning-documentation` (DP6.4).** For repair and cleaning deductions, the statement must carry:
  - for in-house work: a description, hours and a reasonable rate;
  - for vendor work: the invoice, with the vendor's name, address and phone;
  - for materials: receipts or a price list;
  - the (g) photographs with a written cost explanation.

  None of this is required if those deductions total $125 or less, or if the tenant signed a timely waiver that substantially includes the text of (h)(2).
- **`good-faith-estimate` (DP6.4).** A good-faith estimate may be deducted if an in-house repair cannot reasonably be finished by day 21, or if a provider's documents are not in hand by then. It must go out with the statement.
  - If documents are missing, the statement names the provider with address and phone.
  - Within 14 days of finishing the work or receiving the documents, the statement and documents are completed.
- **`estimate-true-up` (DP6.4).** When the final cost is at or below the estimate, keep the final cost and refund the difference within 14 days. Whether a cost above the estimate may be kept is contested (C7). Little security is usually left by then, so in practice the excess becomes a balance that, under your rule, comes back for acceptance.
- **`documentation-on-request` (DP6.4).** A tenant's request for documents within 14 days of receiving the statement must be met within 14 days of the request, even below $125. Whether a message is such a request is a semantic question over the message. Handoff does this without a decision.
- **`electronic-refund-notice`, `refund-electronic`, `refund-agreed-method`, `refund-check-to-all`, `refund-check-or-delivery` (DP6.5, DP6.6).** The AB 414 refund rules, as five small trees with one outcome each:
  - a written notice of the electronic-refund right, unless a written agreement already set another method or (f)(7)'s CCP 1161 grounds apply;
  - an electronic refund to the account designated in writing when the security or rent was paid electronically;
  - the method set by written agreement: the electronic payer's alternative, the all-tenant agreement, or a 1946.7 tenant's request;
  - one check payable to all adult tenants, with the statement mailed to one of them, when several adults reside and none of those agreements exists;
  - otherwise, personal delivery or a first-class check to the tenant.

  Where several adults paid electronically without an agreement, the statute is contested (C8). The statute gives no fallback if an electronic payer never designates an account; Handoff collects the designation on the tenant page.
- **`electronic-writing` (DP1.6).** This is the 1633.5(b) point. An electronic designation or agreement satisfies a requirement to be "in writing" only if the tenant agreed to deal electronically, in one of three ways:
  - a separate, optional agreement;
  - an agreement inside a lease that is itself electronic;
  - the tenant's own conduct, never inferred solely from paying electronically.

  The tenant must also not have refused. A clause in a paper form lease does not count. The tenant page therefore collects a separate, optional agreement before it collects the bank designation.
- **`statement-delivery` (DP6.5).** The statement may be emailed when all of these hold:
  - there is a mutual agreement and an email account the tenant provided;
  - the agreement is separate, or contained in an electronic lease (a paper-lease clause alone is contested, C14);
  - for several adults, the all-tenant agreement specifies email (contested, C8).

  Otherwise it goes by personal delivery or first-class mail.
- **`mailing-address` (DP6.5).** Mailings go to the address the tenant provided, or else to the vacated unit.

### DP7 — Consequences

- **`bad-faith-retention` (DP7.1).** A bad-faith failure to comply with subdivision (h) forfeits any claim to the security, so the whole deposit goes back ((h)(7)). Bad faith is a semantic question; no controlling definition was found, so its wording lists considerations rather than authority. What the forfeiture leaves claimable is C1.
- **`good-faith-noncompliance` (DP7.2).** After a good-faith failure, proven and reasonable damages remain recoverable by setoff or later claim, subject to equitable defenses (*Granberry*; the Senate Judiciary Committee analysis of AB 2801). This is the second half of C1.
- **`statutory-damages` (DP7.5).** A bad-faith claim or retention in violation of 1950.5 exposes the landlord to up to twice the security plus actual damages, which a court may award on its own motion; the landlord bears the burden on reasonableness. The figure shown is the maximum: 2 × $2,437.50 plus actual damages in the demonstration. Whether a procedural failure alone, with valid charges, triggers this is C2.

## Contested points

Each carries both readings with quoted authority. The evaluator reports every branch and computes exposure on the one marked.

| Point | Reading A | Reading B | What it means in practice | Exposure on |
|---|---|---|---|---|
| **C1** forfeiture scope (`bad-faith-retention`) | (h)(7) forfeits only the security. The charges can still be claimed separately. Authority: the text "claim any amount of the security"; (e)(2)(A), which says "against the tenant or the security" when it means both; the committee analysis ("forfeit their ability to claim any amount of the security deposit"); *Granberry* fn. 6 left bad faith open. | It bars any claim against the tenant for those items. Authority: the Legislative Counsel's Digest ("prohibit the landlord from making a claim against the tenant or the security"). | After a bad-faith failure, A lets the operator still pursue a balance; B ends it. | B |
| **C1** good-faith survival (`good-faith-noncompliance`) | *Granberry* survives AB 2801. Authority: its holding, the committee analysis's explicit statement on offset, and (h)(7)'s bad-faith condition. | The *Granberry* dissent: a late statement cuts off setoff. It is weak and has never been adopted. | Decides whether a late or defective statement sent in good faith still supports the charges. | B |
| **C2** (`statutory-damages`) | Keeping any security after a bad-faith (h) failure is a retention "in violation of this section", so up to 2× is available. Authority: (h)(7), (m), and the committee analysis ("for a bad faith violation of AB 2801's provisions"). | (m) reaches only amounts the landlord was not entitled to keep; (h)(7) forfeiture is the specific remedy. Authority: *Granberry*: "Courts will not impose penalties ... in addition to those that are provided expressly". | A missing photo set handled in bad faith costs the deposit under both readings; under A it can also cost up to 2× more. | A |
| **C5** (`statement-due`) | Civ 10/11 and CCP 12a extend a deadline that falls on a weekend or holiday. | "21 calendar days" fixes the day. | Already decided by you: Handoff works to day 21. | B |
| **C6** (`deduct-holdover`, `deduct-other-charge`) | "Any purpose, including, but not limited to" lets the deposit cover other lease debts. Authority: *Brooks v. Greystar* (S.D. Cal. 2025, nonbinding) on utilities. | (e)(1) limits claims to the four listed purposes. | Under B, holdover damages (unless the lease makes them rent), already-billed gas or electric, and late fees are billed separately, not deducted. | B |
| **C7** (`estimate-true-up`) | A final cost above the estimate may be kept from security still held. | Only the estimate may be kept; the excess is a separate balance. | Rarely matters, because the remainder has usually been refunded at day 21. | B |
| **C8** (refund trees, `statement-delivery`) | Several adults without an all-tenant agreement get one check payable to all, with the statement mailed to one of them. | The electronic duty and agreed email still apply, because (A)(ii) and (B)(ii) are not "subject to subparagraph (C)". | Avoid the question by getting the all-tenant agreement on the page. Exposure is set on A, because paying one tenant electronically risks paying twice. | A |
| **C9** (`inspection-list-gate`) | Skipping the offer notice or a requested inspection does not bar deductions; (f)(4) applies only "if an initial inspection is conducted". | Deductions an inspection would have caught are barred, given (f)(1)'s purpose of letting the tenant cure. | Only arises if the offer notice or inspection is missed; Handoff sends it on day one. | B |
| **C14** (`statement-delivery`; new, not in MAP) | A paper lease clause is enough "mutual agreement" to email the statement under (h)(1)(B)(ii). | 1633.5(b) says an agreement to deal electronically cannot sit in a paper standard-form contract except as a separate, optional agreement. | Handoff collects the separate agreement anyway, so the two readings agree in the demonstration. | B |

## The Jev fidelity check

For every leaf, Jev was asked one yes/no question: does the quoted text, read within its surrounding subdivision, establish this leaf as a condition of (or exception to) the tree's effect, in the place the tree gives it?
- One request per tree and cited subdivision.
- The shared state carries that subdivision's text, the tree's effects, and the whole condition structure, with each leaf labelled.
- Model `typesafe/jev-1.13`, pinned build `20260917`.
- 444 questions over three rounds: 194, then 180, then 70 re-asked after changes. The reported cost was about $0.013.
- Requests and answers are in `JEV_CHECK.json`, with every exchange cached by hash under `research/legal-engine/.cache/jev-tree-check/`.

**Round 1** described each leaf's place with a one-line role. That was wrong for nested groups: each of 1942.4's five joint conditions, for example, read as a bar on its own. Most of its low answers came from that, and I treated them as a flaw in the question. Round 2 put the full structure in the state. Of 180 answers, 18 remain below 0.5 in the final round.

**What I changed because of a low answer** (after re-reading the section):
1. **Documentation is a duty, not a condition of the deduction.** Round 1 scored the (h)(2) documentation leaves inside the repair, cleaning and property trees at 0.08–0.41. On re-reading:
   - (h)(2) says the landlord "shall also include" the documents; it does not make them a condition of deducting;
   - (h)(7) forfeits only on a bad-faith failure;
   - *Granberry* and the AB 2801 committee analysis say a good-faith failure still allows offset.

   The documents are now a duty effect on each deduction, linked to the documentation tree and to the bad-faith tree. This departs from the abridged example in `design/legal-trees.md`; the gateway can still refuse to send a deduction without its documents, as an operating rule.
2. **No useful-life condition** in `deduct-repair` (0.06). (e)(2)(A) does not make remaining useful life a condition. Proration stays in the amount through the schedule, which gives zero for an item past its life.
3. **Holdover rate rebuilt on 3334(b)** (0.25). The leaf capped the rate at rental value, but the statute measures value of use as the greater of rental value or the benefit obtained, and uses rental value alone only on a mistake of fact. All three measures are now alternatives.
4. **Owen's billing policy taken out of a law leaf** (0.06). `deduct-other-charge` had required the charge to be "billed before the statement". That is your policy, not law.
5. **Smaller fixes:**
   - the provider-contact requirement in `good-faith-estimate` became a duty, as with (h)(2);
   - `rent-default` and the property `cost-reasonable` statements were narrowed to what the text says;
   - the 48-hour notice's request leaf was re-sourced to the sentence actually about scheduling.

   Each change raised the answer on re-asking.

**What I kept, and why**
- **Seven contested-branch leaves (C1, C2, C7, C8, C9, C14).** Each quotes one reading's basis, so a low answer only restates that the point is contested.
- **Scope and link leaves.** Their quote states the scope of a rule, or they point to another tree, so the text says nothing about deposits as such:
  - the PUC 739.5 and 1671(c) scope alternatives;
  - "not a repair or cleaning" for the (f)(4) bar;
  - the link from the holdover deduction to the holdover charge;
  - the "final cost within the estimate" leaf.
- **"No inspection conducted" (0.23).** Jev read (f)(4) literally, so that no inspection means no bar at all. That literal reading is C9 branch A.
- **"The tenant owes this amount under the lease" (0.12).** The debt comes from the lease, not a statute; (e)(1) is the nearest text. Listed for you below.
- **The wear factors in `barred-charge` (about 0.3; 0.5–0.6 in `deduct-repair`).** 1950.5 does not define ordinary wear, and the factors come from the DRE guide, which the questions cite as their basis. Listed for you below.
- **The 1945 renewal-rebuttal leaf (0.32).** Rebuttal rests on the general law of presumptions in the Evidence Code, which is not saved. Listed for you below.
- **Two links in the DP7 trees** that rest on case law rather than the quoted statute.

Each leaf's answers by round and its disposition are in `JEV_CHECK.json` under `reviews`. Jev was not run on any case evidence.

**One change came from my own read-through, not Jev.** `barred-charge` would have asked the wear and preexisting-condition questions of every line, including rent and utilities, where they have no evidence. Those alternatives now apply only to repair, cleaning and restoration lines.

## Where MAP.md is wrong or incomplete

- **DP6.3, CCP 135.** MAP says CCP 135 excepts "days appointed by the Governor". The text excepts "any other day appointed by the President, but not by the Governor". This affects only the margin dates.
- **DP3.1, Civ 1945.** MAP says renewal is presumed "if rent is accepted after the term expires". The text also requires that the lessee "remains in possession", so accepting rent after the tenant has left does not renew.
- **Condition structures, item 8.** Like the format example, MAP makes the (h)(2) documents a condition of the charge. The text makes them a duty, with forfeiture only for bad faith. See change 1 above.
- **DP3.5, Civ 3334.** MAP omits (b)(2): on a mistake of fact the value of use is the rental value only.
- **The H8 estimate trigger.** MAP says "vendor documents". The text covers documents from anyone providing services, materials or supplies, including materials for in-house work.
- **Late-bill section, water.** MAP lists 1954.205(b) and 1954.212 (75% of a three-month average when a reading is unavailable) beside 1954.207(b) (the previous month's bill) without noting that they conflict for the final month. The trees follow 1954.207(b), which is specific to the end of a tenancy and matches your decision.
- **DP1.4.** MAP lists the CCP 1161(6) notice-fee bar but not its twin, Civ 1946(b), for 30- and 60-day notices.
- **C14 is new.** MAP treats the paper-lease email question as inference. The trees carry it as contested because both readings rest on text.

## Format additions (for the coordinator)

The checker enforces these, and an evaluator can ignore the optional fields it does not use. Accept them or strip them.
- **Question basis.** Semantic questions may carry `basis: [{citation, quote}]` for guidance behind a factor (the DRE guide, AB 2801 §1). It is checked verbatim.
- **Discretionary decisions.** Discretionary leaves carry `decision: {by, what}`.
- **Contested leaves.** A leaf decided by a contested point carries `contested: "C6"`.
- **Branch effects.** Each branch has an `id` and an `effect: {statement, sets: {leafId: true|false}}`, so every branch can be evaluated.
- **Effect fields.** Effects may carry a checked `source`, plus `margin` and `notBefore` date formulas.
- **Cross-tree references.** Formulas may use `holds("CA.tree")` and `amount("CA.tree", "effect-id")`.
- **Parameter units.** Also `hours`, `date` and `multiplier`.
- **Citations.** They are written so the checker can find the saved text: Civ, CCP, Gov or PUC plus section and subdivision, or a named source.
  - Contested authority may also cite the Granberry mirror, the AB 2801 bill text and the DRE guide.
  - It may also cite the authorities agent's committed captures (*Brooks* ECF 56 from GovInfo, and the Senate Judiciary analysis of AB 2801). I only read and cited those; they remain that agent's files.

## Points needing your ruling

1. **Documentation as a duty.** Confirm that (h)(2) documents are a duty attached to each deduction, with forfeiture only for bad faith (change 1). The gateway can still require documents before sending, as Handoff's own rule.
2. **Ordinary wear.** Confirm the factor rule:
   - a condition is beyond ordinary wear only if both its cause (accident, misuse or neglect) and its extent go beyond normal use, and it is not accumulated wear;
   - age counts only through the schedule's useful-life share.
3. **Water's final month.**
   - Confirm the five-day read runs from the day possession is returned, not the lease end. With a holdover, the lease end would leave the holdover days unread.
   - Choose whether "based on the bill amount for the previous month" is prorated by days for a partial final period. The trees prorate unless you rule otherwise.
4. **Holdover.**
   - Should the demonstration lease contain a clause making holdover days rent? That keeps the six days in (b)(1) and out of C6.
   - Confirm the schedule's holdover rate is the contract daily rent.
   - Choose the daily convention. In November, $2,735 × 6 / 30 = $547.00; on a 365-day year it is $539.51.
5. **Exposure branches.** Confirm C8's exposure branch A (a check payable to all). Confirm C14 is carried as contested, or rule on it.
6. **The 1945 renewal presumption.** Confirm it is treated as rebuttable, and the operating rule: no "rent" accepted for post-expiry days while the tenant is in possession.
7. **Bad faith.** No controlling definition was found. The question's considerations are inference: knowledge, practice, ignored requests, and an evidentiary basis. Accept them for now, or wait for the authorities agent's search.
8. **Smaller choices made conservatively:**
   - vendor services and machine carpet extraction are treated as "professional cleaning";
   - restoration lines count toward the $125 threshold;
   - tenancies begun before 2003 are outside the cleaning tree;
   - a lease debt's existence rests on the lease (the 0.12 leaf).
