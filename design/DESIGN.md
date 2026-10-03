# Handoff product design

October 3, 2026. The coordinator's design for Owen's review. It rests on Owen's October 2–3 decisions in `HANDOFF_CONTEXT.md`. The California law it relies on is being mapped in `research/legal-engine/jurisdictions/CA/account_core/`.

Handoff takes a move-out from notice through two outcomes that finish independently:
- the unit is ready for the next resident;
- the departing tenant's account is resolved.

One agent per case does the investigating, recommending and follow-through. The operator decides at a few defined points. Code enforces authority, money and the law around everything the agent does.

## 1. The demonstration case

The case is adapted from Laura Seigel's tenancy at Breakwater (`research/california-case/RECORD.md`) as a private, market-rate apartment. Names are neutral and still to be chosen.

| | Adapted case |
|---|---|
| Property | A large professionally managed apartment community in Huntington Beach, CA, built in the 1970s and renovated. Owned by a private institutional owner and run by a third-party manager. |
| Unit | 3 bedrooms, 2 baths, 1,028 sq ft |
| Tenant | One adult tenant who paid rent electronically |
| Lease | November 11, 2025 to November 10, 2026. Move-in photos exist, as California requires for tenancies starting after July 1, 2025. |
| Rent, deposit | $2,735 a month; deposit $2,437.50 (both from the historical record) |
| What happens | Notice at lease end; keys returned November 16, 2026, six days after the lease ends (as historically) |
| What was found historically | Closet needing rebuild or repair, walls needing paint, carpet needing cleaning, unit needing cleaning, and a final utility bill |
| Legal deadline | Statement and refund due by Monday, December 7, 2026 (21 days after November 16) |

Handoff decides every amount from the evidence, the lease, the company charge schedule and the law. The historical charges are context, not answers.

## 2. The case from start to finish

| When (2026) | What happens | What Handoff does | What you decide |
|---|---|---|---|
| Oct 12 | The tenant confirms leaving at lease end. | Opens the case. Reads the lease, the ledger, the move-in record and photos, and the unit's work history. Emails the tenant a secure link to their move-out page with: the offer of a pre-move-out inspection, their right to an electronic refund, and requests for a forwarding address and written agreement to email delivery. Asks on-site maintenance for inspection times. | — |
| Oct 14 | The tenant asks for the inspection and designates a bank account on the page. | Books the inspection (at least 48 hours' written notice, no earlier than two weeks before the lease ends). | — |
| Nov 2 | The pre-move-out inspection. A maintenance technician walks the unit and photographs it. | Drafts the list of problems from the technician's findings, compared against the move-in record, and makes it as complete as possible. | **The pre-move-out list**, reviewed in minutes on your phone. It is then handed to the tenant at the inspection. |
| Nov 10–16 | The lease ends. The tenant stays six more days and returns the keys on the 16th. | Records the holdover. Photographs the unit before any work, as the law requires. Runs the move-out inspection. For each condition, records what was found and who is responsible: tenant damage, ordinary wear, or present at move-in. | — |
| Nov 17 | The turn needs a plan. | Gets a vendor quote for the closet (repair against rebuild) and for carpet cleaning, and in-house time and rates for paint and cleaning. Proposes the work plan and budget. | **The work plan and budget** |
| Nov 18 – Dec 1 | The work is done. Thanksgiving week affects scheduling. | Schedules in-house work orders and vendors, follows up, takes after-photos, checks completion, records hours and invoices. | — |
| ~Nov 30 | The account is due before December 7. | Builds the account. Holdover rent for six days. A tenant share of each charge, from the company schedule and the evidence. Carpet cleaning only if it was needed to restore move-in condition. Actual cleaning hours. Final utilities handled as the law allows, because the biller has not billed yet. Whether that means estimating now or billing later is a question for the legal map. Applies the deposit and shows the refund or balance due. Each line shows its evidence, its rule and its exposure. | **The account**, with method and recipients |
| Dec 1 | The account goes out. | Emails the statement with invoices, work-order hours and a link to the photos. Sends the refund electronically to the designated account. Posts to the ledger. Updates the tenant's page. | — |
| Dec 3 | **Live moment:** the tenant questions the closet charge on the page. | Answers with the move-in and move-out photos, the invoice and the rule. No decision needed from you. | — |
| Dec 4 | The tenant either produces a move-in photo of a damaged closet, or threatens small claims. | Brings one recommendation. For new evidence, a correction. For rising stakes, hold or settle at a specific amount, with the likely small-claims result, the cost of appearing and the twice-the-deposit exposure. | **Hold, correct or settle** |
| Dec 10 | The final utility bill arrives, after day 21. | Completes the utility charge the way the account set out. Where an estimate was used and the bill is at or below it, finishes within 14 days and refunds the difference under the same acceptance. If the bill is above, brings it back to you. | Only if the bill exceeds what was accepted |
| By mid-Dec | Closure | Settles any correction or settlement, reconciles the ledger, and sends the tenant a closure confirmation. The account is resolved. The unit was ready once its work passed completion checks; the two outcomes finish independently. | — |

## 3. The balance-owed variation

This uses the same code with a different starting state. The tenant leaves owing rent beyond the deposit.
1. Handoff recommends whether to pursue the balance, hand it to a collector or write it off, on expected net recovery. That weighs likely recovery, the collector's fee, time, the risks under debt-collection and credit-reporting rules, and small-claims limits: no one may file more than two claims over $2,500 a year statewide, and an entity's claim limit is $6,250.
2. Once you accept, Handoff hands the balance to the collector on the accepted terms.
3. Later the tenant disputes a line and Handoff corrects it.
4. The account is not resolved until the collector's balance matches the correction and Handoff has confirmation. Holland's own complaint record shows this exact failure.

## 4. Your decisions, in one place

| Decision | How often | What it binds |
|---|---|---|
| Company charge schedule (useful lives, rates, holdover, chargeable lease fees) | Once, changeable | Every account, until you change it |
| Pre-move-out list | Each move-out, in minutes | What may later be deducted |
| Work plan and budget | Each move-out | Result, scope, budget, explicit requirements |
| Account | Each move-out | Every line, deposit applied, refund or balance, method, recipients |
| Increase, correction, settlement, balance pursuit | When it arises | That change only |

Everything else Handoff does on its own: notices, scheduling, follow-up, defending charges, legal duties such as sending documentation within 14 days of a request, and completing within an accepted estimate.

## 5. How the system is built

TypeScript throughout. Postgres for all records. The LangGraph library for the agent. Claude for the coordinator, compared against other models before the demo is frozen.

### 5.1 The case runtime (Handoff's own platform)

- **Records:**
  - property, unit, tenancy, parties;
  - condition records (move-in, pre-move-out, move-out) with photos;
  - findings per condition;
  - quotes, work orders (in-house, with hours and rate), vendor jobs and invoices;
  - the account and its lines, each with evidence, rule and exposure;
  - decisions, actions, messages and documents.

  Financial entries are append-only and in exact cents.
- **Event inbox:** every input becomes an event on its case:
  - operator decisions and messages;
  - tenant emails and page actions;
  - results from outside systems;
  - deadlines and wake-ups coming due.

  A case handles its events one at a time.
- **Business clock:** real time in production, and a controllable clock per simulated world. Deadlines and wake-ups are rows keyed to it.
- **Decisions:** each one is bound to the exact content you reviewed.
- **Action gateway:** every tool that changes the world passes through it. Before acting it checks four things:
  - authority: there is a matching accepted decision or standing instruction, and the agent cannot grant itself authority;
  - the law: deadlines, evidence required, allowed charges, refund method;
  - money: exact arithmetic and available funds;
  - idempotency: a key that prevents duplicate payments or postings.

  It then records the result. Text from tenants and vendors is untrusted and can never carry authority.
- **Adapters:** one interface per outside system: ledger, payments, utility biller, maintenance, vendors, collector, email. The demo uses imitations; real systems plug in at the same interfaces.

### 5.2 The agent

- One LangGraph thread per case. Each wake is a fresh run:
  1. Build the case brief from the records: the situation, deadlines, open commitments, new events and a summary of earlier history.
  2. The coordinator reasons and uses tools.
  3. The run ends once it has acted or is waiting on something. Waiting is stored as data, not as a paused run, so code can change between wakes.
- **Specialists:**
  - an evidence analyst, on a model that can read images, records neutral observations of each condition from the move-in, inspection and move-out photos and notes: what is visible, where, and how extensive. These are observations, not legal conclusions;
  - a legal reader answers a specific question from the compiled rules and the saved texts.

  The coordinator does the rest. Jev handles narrow judgments where measurement shows it helps.
- **Tools:**
  - read: the case, documents, photos, ledger, rules;
  - compute: deadlines, prorations, useful-life shares, totals;
  - prepare: the pre-move-out list, the work plan, the account, a settlement;
  - act: messages, scheduling, quotes, orders, ledger postings, refunds, collector hand-offs. Act tools go through the gateway.

### 5.3 The legal engine inside Handoff

The thesis is from Nay's *Law Informs Code*: law turns goals into directives that can be stated in advance (rules) or applied to situations nobody listed (standards). Handoff compiles the rules, breaks the standards into answerable questions, and binds both to the evidence the turn produces. Jev is the sensor at each joint between a piece of evidence and a legal condition. Code evaluates the logic. The agent investigates whatever is still unresolved. The same compiled law also limits what Handoff's own agent may do.

**What the legal track compiles.** For each decision point, using CORDON's stages:
1. **Legal meaning as logic trees.** Each provision becomes conditions joined by *all*, *any* and *not*, plus:
   - exceptions ("unless") and requirements ("only if");
   - effects: a permission, a prohibition or a duty, with its amount or date formula.

   Every node carries its verbatim source quote, its effective dates and, where the law is genuinely contested, both branches with their authority.
2. **Clocks and parameters:** the 21-day deadline, 14-day completion, 48 hours' notice, the two-week inspection window, the $125 threshold, twice the deposit, the photo dates, holiday rules.
3. **Evaluators.** Code evaluates a tree over facts that are true, false or unknown, and returns effects plus a full trace. Unknown is a recorded state, never zero or false.
4. **Evidence contracts.** For each condition: the records that settle it (photos taken before and after the work, an invoice with the vendor's name, address and phone, or hours and rate), or the Jev question that settles it and the exact inputs that question needs.
5. **Actions.** Legal effects become duties on the clock (send the statement by December 7), checks at the action gateway (no deduction unless its contract is met), and required text in notices.

Jev helps compile the trees as well as apply them. Under the section-semantics method, focused questions break each section into its conditions, exceptions, timing and effects, and reviewers and Owen adjudicate the result before it becomes a tree. Compilation and runtime use the same question discipline: one useful determination per question, enough context to answer it, and a defined consumer for every answer.

**Three kinds of condition in a tree.**
- **Determinate**, which code computes from records: dates, amounts, whether move-in photos exist, whether an initial inspection took place, the payment method, the number of adult tenants.
- **Semantic**, which Jev answers. These are narrow, typed questions with a defined consumer:
  - a yes/no probability (Noul);
  - a choice among alternatives (Choice);
  - a position on a defined scale (Score).

  Standards are broken into the factors the authority uses. "Beyond ordinary wear" becomes questions about cause (accident, abuse or neglect versus normal use), extent, and age against useful life, each asked separately over the move-in and move-out evidence.
- **Discretionary or contested**, which stays with the agent and the operator: whether to pursue a permitted charge, settlement, and which side of a genuine legal disagreement to take. The tree supplies both branches and their consequences.

**Worked example: may the closet charge be deducted, and for how much?** It is allowed, up to the reasonable cost, when all of these hold:
- The deposit is security under the lease. *(record)*
- The damage was caused by the tenant or a guest. *(Jev, over the move-out evidence and the tenancy record)*
- It was not present at move-in. *(The move-in photos exist for this tenancy: record. Jev answers whether they or the move-in record show it.)*
- It goes beyond ordinary wear. *(Jev, factor by factor: cause, extent, and the closet's age against its useful life, with age from the unit's records.)*
- It was on the pre-move-out list, **or** the tenant's belongings hid it at that inspection, **or** it happened after the inspection. *(List membership: record. Hidden or later: Jev, over the inspection photos and notes.)*
- The amount does not exceed the reasonable cost of restoring move-in condition. *(Code, from the invoice or the hours and rate, and the company schedule's share. Jev answers whether the work restores rather than improves.)*
- The statement includes photos after possession returned but before the repair, photos after it, and the invoice or hours and rate. The exception is when repair and cleaning deductions total $125 or less and the tenant has not asked for documentation. *(record)*
- It goes out by day 21, or as a good-faith estimate completed within 14 days. *(clock)*

**Effect and exposure.**
- If every condition is satisfied: the deduction is allowed at the computed amount, with its evidence bundle.
- If a condition is unresolved: Handoff investigates before recommending, for example by getting the technician's note, closer photos, or the closet's install date.
- Exposure comes from the consequence branch: a bad-faith claim forfeits the whole deposit and can add up to twice the deposit.

**One judgment layer, more than one provider.** Every semantic question is registered once: its wording, type, required inputs, decision policy and log. The layer sends it to the provider that measures best for that question.
- Questions over photos go to OpenAI's Decisions API, which is multimodal and in limited preview, once Handoff has access.
- Text questions go where they measure best, which is Jev today. Jev reads text only, and the service calls its HTTP API directly because its official SDK is Python-only.
- A frontier vision model answering the same questions is the baseline.

Provider choice per question is a measured decision on labelled sets (accuracy, calibration, cost), not a fixed allegiance.

The evidence analyst's neutral, per-condition observations ("a 6-inch split in the closet door track") stay separate from legal conclusions. The statement, the tenant page and a small-claims judge read them, and text-only judgments use them. A disputed photo can be re-observed without redoing the law.

**How Jev runs at a wake.**
1. Code checks each question's evidence contract before asking it. Missing inputs become an investigation task, never a question. This guards against Jev answering yes on too little context, a failure seen in testing.
2. Independent questions that share evidence go out as one batch, and Jev returns probabilities.
3. A per-question policy, measured on labelled cases, maps each probability to established, negated or unresolved.
4. The evaluator recomputes the tree.
5. Each answer is logged with its inputs, the answer, and what it caused (used, prompted investigation, overridden with a reason). That log is the audit record and the next round's evaluation data.

**Jev also reads every inbound message for facts that change the law's path:**
- which account line a message disputes;
- a documentation request within 14 days;
- a new forwarding address;
- bankruptcy, military orders or domestic-violence termination.

Code routes each answer to the tree it switches.

**Consistency at scale.** The same questions, the same company schedule and the same trees run on every unit. That is "one standard for every unit" made real, and it is the strongest defense against pattern claims. A free-form agent judging each case afresh cannot promise it.

**The agent's place.**
- The coordinator chooses which trees apply, gathers the evidence their contracts require, resolves unknowns by investigating, and writes the recommendation with each line's trace.
- It cannot override a determinate prohibition; the gateway enforces it.
- The legal reader specialist answers questions the compiled trees don't cover, and logs each one as a gap for the legal track.

**Change.**
- Trees are versioned by effective date. Each case is evaluated under the law in force on its event dates.
- A change in law re-evaluates only the open cases it affects.
- A changed fact re-evaluates only the nodes that depend on it.
- Jev answers are reused only when the request is exactly the same.

**Proving it earns its place.** Each Jev question has a labelled set: cases built from the scenarios and from reviewed real material. The scenario library runs a four-way comparison:
1. today's process;
2. a capable model with the same records;
3. that model with the compiled trees;
4. that model with the trees and Jev.

They are compared on charges that are lawful and defensible, deadlines met, recovery, operator effort and cost. A component that doesn't improve the result is removed.

### 5.4 Surfaces

- **Operator app:**
  - the units list;
  - the case view, with Unit and Account progress shown separately;
  - decision screens for the list, plan, account and revisions, with evidence and before/after comparison;
  - a conversation with Handoff;
  - money.
- **Tenant page:** a secure link plus an emailed code. It shows status and dates, and the account line by line with evidence. It collects in writing the refund method and the forwarding address. It also collects a separate, optional agreement to receive the statement and refund electronically, because California's electronic-transactions law (Civ 1633.5(b)) won't let that agreement sit inside a paper form lease. It lets the tenant question a line or pay a balance, and confirms closure.
- **Email:** an imitated transport in the demo, stored and rendered; a real provider later.

### 5.5 The simulated world and evaluation

- **Imitations:** ledger, payments, utility biller, in-house maintenance, vendors and collector. Each has its own records, an interface shaped like the real system's, and a hidden scenario on the business clock.
- **Simulated tenant:** a model on a different provider with a hidden brief. It acts through the same emails and page.
- **Scenarios:** a starting state plus a scenario script. Main path, balance owed, returned refund, several adult tenants.
- **Staged copies:** the whole database is copied at a moment and reopened fresh. The mechanism depends on the hosting choice: a database branch, or a dump and restore.
- **Evaluation:** scenarios are scored on:
  - decision quality: lawful, defensible charges and deadlines met;
  - completion;
  - operator effort;
  - cost.

  The model comparison runs here before the demo is frozen.

## 6. Build order

1. The case runtime core: records, inbox, clock, decisions, gateway, adapter interfaces and the imitations.
2. The agent: the coordinator, its tools and the evidence analyst. Physical work first, so the loop runs end to end.
3. The legal engine: logic trees for the account decisions from the legal track, the tree evaluator, evidence contracts, the provider-neutral judgment layer (Jev and, once available, the Decisions API), and labelled sets for each question.
4. The account path and the operator decision screens.
5. The tenant page, the simulated tenant and the email rendering.
6. Scenarios, staged copies and evaluation, then the model comparison and the demo freeze.

## 7. Open points for Owen

- How unbilled final utilities are handled (see the legal map's utility section): the statutory final-month method for submetered water, plus either separate billing or a contested good-faith estimate for other utilities.
- Neutral names for the property, owner, manager and tenant.
- The demo dates above: notice October 12, keys November 16, deadline December 7.
- Hosting and database provider, needed at first deployment.
