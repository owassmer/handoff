# How the legal map and Jev connect to Handoff

2026-09-29. Ferro's proposal for Owen. The authority is the intent notepad (§2, §3, §5, §9) and research/APERTURE.md.
Nothing here is authorized to build. "Today" facts were read on Core origin/master (b2b512b, 2026-09-28).

## 1. What Handoff has today, and what the law needs from it

Handoff runs outcome 1 (the unit ready) end to end: notice, work plan, operator acceptance, provider requests,
visits, inspection reports, invoices, owner funding and provider payment. Outcome 2 (the account) is phase C and
not started. The coordinator's model is told this turn "concerns physical work, not the outgoing account", and no
Handoff code evaluates any tenancy law. The old `deposit_closeout` module holds NC-only review cards and refuses
any other jurisdiction ("No NC fallback is applied"); intent §10 retires it.

What already exists that the market-rate rules consume:

| Handoff today | Law it feeds |
|---|---|
| Notice: `tenancy.startDate`, `endDate`, `noticeDate`, `endingKind` (Tenancy ending / Occupant departure / To confirm) | Which deposit regime (lease date), co-tenant clock (`NY:ADJ-cotenants-vacated`), when the tenancy ends (Step 3) |
| Notice: `agreements` with terms text | Lease clauses: auto-renewal (`NY:GOL-5-905`), lease-break sum (`NY:ADJ-lease-break-charge`), interest rate (`NY:CASE-NML-contract-rate`), notice terms |
| Notice: `parties` with email and phone | Where the 14-day statement goes (`NY:ADJ-provide-address-branches`); collection contact rules |
| `Property condition` document: conditions with `state` (Satisfied, Deficient, Not checked), `accessible`, `repairable` | The move-out condition record for each proposed charge |
| Provider services: `effects` mapping each quote line to the condition ids it fixes | The link from a charge line to the condition it charges for |
| `HandoffInspection` findings per line; `HandoffInvoice` lines that must sum exactly | Evidence and cost for each damage deduction (`NY:GOL-7-108(1-a)(b)-refundable`; `NY:CASE-Toporek-estimate`) |
| `clock.ts` case business time | The 14-day clock and its weekend and holiday rollover (`NY:GCN-20`, `NY:GCN-25-a(1)`) |
| Exact integer money (`quoteCosts.ts`, `values.ts`) | Every amount in the account |

What the law needs that Handoff does not record yet (phase C and its evidence contracts):
- Unit and building facts: building unit count, certificate of occupancy, HPD registration, open rent-impairing
  violations, stabilization status (Step 0).
- The move-in condition record signed under 7-108(1-a)(c), which bars any deduction for a condition it notes.
- Deposit facts: amount, date, bank and bank notice, interest earned, who paid which part.
- The vacate date as evidence (keys, belongings, the lease's definition), not a notice field.
- Fee disclosure signed before the lease (FARE Act), and the rent ledger with each charge's type.
- The account itself: charges, credits, deposit application, refund, balance, statement, payee (blueprint C.1).
- Tenant status signals: military orders, domestic-violence termination, bankruptcy filing, disputes.

A Deficient finding says the condition needs work. It does not say the tenant caused it. That gap is the
judgment in intent §3's repainting example, and it is exactly where Jev sits.

## 2. The division of labor

| Layer | Owns | Market-rate examples |
|---|---|---|
| Stage A rules | What the law says, dated and sourced | 201 NY, 185 NYC, 176 US atoms (after review 2) |
| Code (Stage B clocks, Stage C evaluators) | Every date, amount, cap, category and regime | Day 14 with rollover; one-month cap; interest less 1%; the four retention categories; 2% statutory interest; which payee after a bankruptcy filing |
| Jev typed judgments (Stage D joints) | One narrow judgment per question, built from a STANDARD or MIXED rule's judgment terms | Wear and tear or tenant damage for this line; noted at move-in; does this invoice line cover this condition; did the tenant vacate on this evidence; does this message report a bankruptcy filing |
| Agent (Handoff's reasoner) | Investigating, drafting, scheduling to meet the clock, reasoning about treatment and concessions | Asks the vendor for the photo before day 10; drafts the statement; recommends conceding a weak charge |
| Operator | Accepting or changing the account (intent §5) | One decision on the whole account, with every line's basis visible |

Rules that bind all layers: a Jev answer never sets an amount or a date; its confidence is not the odds of a court
outcome and never discounts a charge; nothing changes the account without the operator's acceptance; an unknown is
a typed state, never zero; a unit outside the market-rate scope is routed to the operator, never defaulted.

## 3. Where Jev sits in one move-out

1. Every inbound message and document: yes/no checks for facts that switch a code path (forwarding address or new
   channel; military orders; bankruptcy filing; domestic-violence termination; a dispute; a request to stop
   contact). Code routes each answer to the rules it triggers (`US:50USC3955*`, `US:11USC542-refund-payee`,
   `NY:RPL-227-c(5)(b)`, SHIELD cease rules).
2. The vacate date: a choice over what the evidence shows; code sets the date and day 14.
3. Each proposed charge line: wear and tear or tenant damage; noted at move-in; covered by this invoice line; which
   retention category or a fee; on the fee disclosure. The criteria text is quoted from the rule.
4. Drafts before they are sent: does each amount state its basis; does it demand a pre-filing balance; does it call a
   domestic-violence termination early; does it undercut the tenant's dispute rights.
5. The balance: a forecast of one party's decision (will the former tenant pay after a demand, or dispute), anchored
   on a sourced base rate (agency recovery 15-20%, NAA) and adjusted for the case; code computes net recovery after
   costs, 2% interest and time; the operator decides to pursue, hand off or write off.
6. Evidence priority before day 14: dollars at stake per line (code) times judgment ambiguity (Jev) times whether
   more evidence can settle it.
7. A contribution record: every Jev answer is marked used, prompted a second read, redirected work, overridden with
   a reason, or unused. Operator accept or change on each line is a labeled example for evaluation only; it never
   becomes a standing rule (intent §9).

Jev runs through OpenRouter, as in Slope. Slope's latest check: 36 of 39 hand-labeled boundary cases agreed, for
about a tenth of a cent in total; its weakest question (does this passage support the claim) agreed 4 of 6. That is
a sanity check, not an accuracy estimate, so each question used here is measured on labeled cases first.

## 4. What changes for the operator

Today, for this customer, a move-out settlement is a person remembering the law, chasing vendors for photos and
invoices, guessing whether paint is wear and tear, counting to day 14, and hoping. The cost of a miss is concrete:
in New York a missed 14-day statement forfeits the right to keep any of the deposit, and a willful violation adds
up to twice the deposit.

With the engine, on the day the notice arrives Handoff already knows:
- whether the unit is in scope, and whether rent can be recovered at all (certificate of occupancy, registration,
  rent-impairing violations), before any rent is billed;
- the exact day-14 deadline, and which statement channel is lawful for this tenant;
- which charges the lease and the law allow, and which are barred (fees, legal fees, repainting after ordinary use,
  anything on the move-in record, a lease-break penalty).

During the turn it schedules vendors and evidence to land before the deadline, because the legal clock is visible to
the same coordinator that books the work. By about day 10 the operator sees one account: every line shows the rule
it applies (with the quote), the evidence (move-in record, report, photo, invoice), the judgment and its criteria,
and the arithmetic. The operator accepts or changes it once. Handoff sends the statement and refund by a lawful
channel on time, reads every reply for facts that change the rules, answers disputes with the evidence already on
file, and brings a pursue-or-write-off recommendation with its numbers. The operator stops carrying the law in
their head, stops fearing forfeiture, and spends their time on the few decisions that are theirs.

This is what makes the accountable-service shape credible (APERTURE §3): Handoff can take responsibility for the
settlement because the law is compiled, the clock is enforced, and every judgment is typed and measured. It is also
what converts the service to software: each judgment step becomes a question with a measured record.

## 5. Order of work (proposed; each gate is Owen's)

Superseded in part (2026-09-30): Stage A now runs for Holland Partner Group's five states through the
jurisdiction-pipeline skill, and NYC is parked without acceptance, so steps 1-2 below no longer run on the NYC
market-rate set. Steps 3-5 apply to the first accepted Holland layer. Which layer carries the Jev tests is not yet
decided (APERTURE.md section 7).

1. Stage A for market-rate NYC: the building-and-owner sweep, a third review limited to it, Owen's acceptance.
2. Jev experiments on this set (approved, after step 1): the quote-supports-rule check against the two reviews'
   findings; then the typed judgment questions on reconstructed market-rate cases, Jev against Handoff's model.
3. Stage B clocks and Stage D evidence contracts for market-rate: for each rule, the facts it needs and which Handoff
   record supplies them. This produces the phase C data model (section 1's missing list), sized to the rules.
4. The four-way test on reconstructed market-rate cases: the current process; a capable model alone; the model with
   the compiled law; the model with the compiled law and Jev. If the plain model does as well at acceptable cost,
   the smaller mechanism wins.
5. Build into phase C. Because Handoff ports off Foundry soon, the clocks, evaluators and judgment layer are written
   as platform-free modules behind a storage interface, like `quoteCosts.ts` and `values.ts` today, so they move with
   the port unchanged.

Parallel and not a build: the operator walkthroughs (5-8 NYC and Virginia managers), which decide the second regime.
