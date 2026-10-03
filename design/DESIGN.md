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
1. Handoff recommends whether to pursue the balance, hand it to a collector or write it off, on expected net recovery: likely recovery, the collector's fee, time, and the risks under debt-collection and credit-reporting rules.
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
  - an evidence analyst compares move-in and move-out photos and records for each condition and reports findings with responsibility;
  - a legal reader answers a specific question from the compiled rules and the saved texts.

  The coordinator does the rest. Jev handles narrow judgments where measurement shows it helps.
- **Tools:**
  - read: the case, documents, photos, ledger, rules;
  - compute: deadlines, prorations, useful-life shares, totals;
  - prepare: the pre-move-out list, the work plan, the account, a settlement;
  - act: messages, scheduling, quotes, orders, ledger postings, refunds, collector hand-offs. Act tools go through the gateway.

### 5.3 The law inside the system

- California's compiled rules are loaded as data from the legal pipeline.
- Code evaluates the determinate rules:
  - the 21-day date and how it is computed;
  - the estimate-then-complete path for repairs and invoices not yet received, and whether it extends to a late final utility bill;
  - the $125 documentation threshold;
  - documentation requests within 14 days;
  - refund method and recipients, including several adult tenants;
  - the holdover proration.
- Standards such as ordinary wear and "reasonably necessary" go to the agent and the evidence analyst, with the rule text and the company schedule.
- Each account line carries its rule reference, its evidence links and its exposure (bad-faith forfeiture, up to twice the deposit).

### 5.4 Surfaces

- **Operator app:**
  - the units list;
  - the case view, with Unit and Account progress shown separately;
  - decision screens for the list, plan, account and revisions, with evidence and before/after comparison;
  - a conversation with Handoff;
  - money.
- **Tenant page:** a secure link plus an emailed code. It shows status and dates, and the account line by line with evidence. It collects the refund method and forwarding address in writing, lets the tenant question a line or pay a balance, and confirms closure.
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
3. The law: the account-core rules from the legal track, and their evaluators.
4. The account path and the operator decision screens.
5. The tenant page, the simulated tenant and the email rendering.
6. Scenarios, staged copies and evaluation, then the model comparison and the demo freeze.

## 7. Open points for Owen

- Neutral names for the property, owner, manager and tenant.
- The demo dates above: notice October 12, keys November 16, deadline December 7.
- Hosting and database provider, needed at first deployment.
