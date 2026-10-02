# Deposit closeout: build specification

**Design date:** 16 September 2026  
**Purpose:** Translate the operating model, public evidence, and prospect research into one working application.  
**Status:** Proposed design. This document is not an implemented application, completed evaluation, or approved production legal ruleset.

## 1. The application

Build a workspace for the property manager and accounting team handling the end of a tenancy. It takes the records of that tenancy, determines the current deposit disposition and required work, and keeps both up to date as information arrives and actions happen.

At any moment it should answer:

- What can be charged, what should be refunded, and what is not yet decided?
- What must happen next, by when, and who can do it?
- What has actually happened, and what is still unfinished?

The three previous demonstrations are tests of this one application. Do not build three separate demonstration scripts or products.

### First working scope

Use a conventional North Carolina residential tenancy ending in full, with a cash security deposit and confirmed property, tenancy, parties, and management authority. This is the first implementation example because Red Door and Henderson provide two prospective operating arrangements in the same state. It is not a promise to support their entire portfolios, a legal certification, or a requirement that the first customer be in North Carolina.

The same core records must support other jurisdictions, but their substantive decisions remain unavailable until the relevant rules are implemented and evaluated. Keep the Texas and Colorado operational patterns as general tests; never silently use North Carolina law to answer those cases.

Begin with ordinary damage deductions and refunds. Track other balances supplied by accounting without automatically treating them as allowable deposit deductions. Identify unfamiliar charge categories and special tenancy circumstances explicitly; do not silently mark the entire account settled while an unresolved item remains.

Do not implement renewal notices, eviction, a new maintenance-dispatch system, a resident portal, autonomous litigation, custody of money, or general utility account administration in version one.

### Source of the design

| Research observation | Required product behavior |
|---|---|
| Turnover work and tenant charges can be wrongly conflated. | Keep the vendor's cost, proposed allocation, approved charge, and ledger posting separate. |
| A recorded condition does not necessarily create a maintenance request. | Compare observations with actual service records. Do not invent intervening repairs. |
| Deadlines can arrive before all costs are known. | Determine what work is required now rather than waiting for a final invoice. |
| Possession, recurring rent collection, and deposit accounting can finish separately. | Track each outcome separately; never infer one from another. |
| Existing operators already use portals, inspections, and accounting software. | Add decisions and completion tracking to those systems, not a competing copy of their entire records. |

## 2. The unit of work

**One case belongs to one ending tenancy, not merely to one address or one resident.**

The home persists through several tenancies. Observations about its physical condition can remain useful across tenancies, but deposit balances, charge responsibility, and refund recipients must remain tied to the correct agreement and parties.

A case starts when a move-out notice or other supplied record identifies an ending tenancy. It may also be opened after move-out. Notice date, intended departure, agreement end, actual vacancy, key return, and legally relevant delivery of possession are distinct. Store the source events and the accepted date used by a decision; do not assume they coincide.

Before the applicable legal triggers are established, show preparation tasks and the missing triggering fact. Do not publish a definitive deadline based on an unconfirmed event. Preparation can include locating move-in records, arranging the existing inspection process, and establishing refund instructions.

### Records to store

These are record groups, not separate services or a general-purpose model of the whole property business.

| Record group | Minimum contents |
|---|---|
| Home and tenancy | Internal IDs; external system IDs; exact unit; jurisdiction; agreement and amendments; start/end events; linked people with their roles and effective dates. |
| People and authority | Management company; owning entity; assigned manager; accounting role; residents and signatories; approved recipient instructions; permitted actions and approval limits. Being an owner does not by itself establish every action permission. |
| Deposit and money records | Actual recorded deposit balance; custodian; source and date of the balance; existing applications/refunds; transaction references; pending or reversed payments; separate amounts claimed beyond the deposit. Do not use the lease's nominal deposit amount as proof of funds held. |
| Condition and work | Dated observations by location/item; move-in and move-out evidence; actual service requests; work completion records; estimates and invoices; source revisions. A single invoice can cover several items and allocations. |
| Charge decisions | Item; proposed owner/tenant/unresolved allocation; current decision; reason; facts and rule used; chosen amount; reviewer when required. Permitted does not mean the owner must charge the full amount. |
| Accounting versions | Interim or final statement; included item versions; calculated totals; recipients; delivery method; approval; what was actually issued. A later change creates a new version rather than rewriting a sent statement. |
| Required work and actions | What is owed or required; why; trigger; due date; responsible role; task; required approval; action attempt; result; failure or retry. Keep a legal due date separate from an internal work target. |
| Documents and changes | Original records; source locations for important facts; date of the real-world event; date learned; corrections and conflicts; changes to decisions and actions. Retain only what serves the case, evaluation, or maintenance. |

Money calculations use exact cents. Existing ledger entries and proposed entries are not added twice. A return or reversal changes the outstanding amount; it does not erase the first payment attempt. An amount above the deposit is a separate proposed receivable, not a negative refund or permission to debit a resident.

### Keep separate progress tracks

Track decision readiness, required communications, approvals, money, and related account tasks independently.

A case might correctly read: "Interim statement sent; final costs outstanding; refund not yet finalized; recurring draft cancellation confirmed."

The case summary is calculated from these tracks. A user cannot make obligations disappear by dragging the case to "Complete."

Legal performance and financial settlement are also different. The applicable rule determines when a legal notice or refund step is performed. The product separately records whether money is pending, settled, returned, or lawfully held. Do not claim that check clearance is always necessary to meet a legal deadline.

A unit can be ready for its next tenant while the prior deposit remains open. Deposit completion does not assert that repairs, contractor payment, unrelated utilities, and all other property work are complete.

## 3. The decisions the application makes

Every review of a case returns the same six outputs: applicable requirements, proposed charges, proposed account, missing decisions or facts, available actions, and completion status.

| Decision | Inputs | Output and resulting work |
|---|---|---|
| Is this a supported case, and which requirements apply? | Location; tenancy type; operative agreement; relevant dates; rule versions; any supplied special circumstances. | Applicable requirements, or the specific missing/special circumstance. Continue useful preparation without claiming an unsupported legal conclusion. |
| What part of each cost belongs to this tenant? | Before/after condition; intervening repairs; cause; actual cost; applicable rule and agreement. | Supported charge, owner cost, another allocation, or a specific unresolved question. A document marked "invoice" never becomes a tenant charge automatically. |
| Can the account be finalized? | All relevant items; actual deposit transactions; current decisions; known missing costs; applicability of any interim route. | Final account when ready, otherwise the permitted interim work and precise remaining questions. Unknown is not zero. |
| Who should receive the account and refund? | Tenancy membership; operative recipient instructions; law and agreement; verified contact/payment route. | Intended recipients and method. Last payer and most recently emailed person are not automatic defaults. |
| Who may approve and carry out each action? | Management authority; company roles; transaction and document version; action type; recipient and amount. | Ready action or a named required approval. Approval does not make a prohibited charge allowable. |
| What is finished and what happens next? | Actual action results; remaining obligations; time; current decisions. | Completed work, next useful action, and any failed or reopened work. A generated document is not a sent document. |

### What a written rule becomes

A rule becomes a decision with a defined question, circumstances, inputs, possible answers, resulting work, and completion condition. It does not become a paragraph placed in every model prompt.

For the initial North Carolina accounting example, use G.S. 42-52 as the source for the ordinary and conditional interim/final routes. Store the triggering events and the condition for using the interim route explicitly. A missing invoice alone does not automatically establish that condition. Missing address handling is a distinct branch, not a reason to declare completion or guess a recipient. [S1]

The implementation of a rule should record:

| Field | Purpose |
|---|---|
| Question and scope | What it decides and which cases it covers. |
| Source and applicable version | Which legal provision, agreement, or operating instruction establishes it; when it applies. |
| Required facts | Specific case facts, not a generic request for more documents. |
| Possible answers | Including a specific missing fact or unresolved interpretation when necessary. |
| Consequences | Calculations, required work, permissible choices, and restrictions. |
| Completion condition | What actually satisfies the particular requirement. |
| Reconsider when | Changes that can alter this answer or its pending actions. |
| Evaluation cases | Ordinary success, relevant variation, and known failure patterns. |

Law, agreement, company procedure, and case facts remain separate. A company webpage is evidence of its stated workflow, not automatically the governing law or the terms of a particular lease. A source conflict becomes a visible question; do not universally choose the strictest text or the most recent file.

A published rule change is reviewed for its actual effective scope. Do not apply today's rule automatically to a historical case. Preserve what was issued previously and apply any required correction as new work.

## 4. What the operator sees

### Screen one: open cases

One table, with filters for assigned person and work type:

- Home and ending tenancy.
- Nearest applicable deadline and the requirement behind it.
- Current issue, such as "Invoice needs itemization," "Approve refund," or "Payment returned."
- Deposit/account summary, with incomplete amounts clearly identified.
- Person responsible for the next step.
- A direct button for that step.

Order primarily by overdue/due work and blocked actions, not an unexplained risk score. Show whether a deadline is legally required or an internal target.

### Screen two: the case

**Top:** current recommendation, nearest deadline, and next available action.

**Charge review:** item; relevant condition; cost; proposed allocation; reason; reviewer decision. Open the supporting record alongside a questioned item. Allow the manager to correct a fact, revise an allocation, or waive a supported charge with a recorded reason. These are different operations.

**Account preview:** actual deposit balance, current deductions, unresolved items, proposed refund or separate receivable, recipients, and the exact statement awaiting approval. If the account is incomplete, do not display a supposedly final refund.

**Remaining work:** required statements, decisions, refund actions, recording, and separately applicable account tasks. Each task names its owner, due date, missing prerequisite, and completion result.

**History and source records:** available on demand, including what changed and why a previously approved action is no longer current. Sources are not the main screen.

The manager and accountant use the same case, with different permissions and filters. Version one does not need an owner dashboard or resident chatbot.

## 5. What happens when something changes

Whenever a record arrives, a person corrects a fact, a decision is approved, an action returns a result, or a deadline approaches:

1. Store the new information against the correct case.
2. Re-run the case's decision questions.
3. Compare the new answer with the prior answer.
4. Update required work and cancel or replace obsolete pending work.
5. Ask for fresh approval only where an approved amount, recipient, content, or relevant assumption changed.
6. Execute only actions allowed by current authority and approval.
7. Record the result and review the case again.

A small version can re-check the entire case after a change. It does not need an elaborate dependency system. Keep a simple record of the inputs to each decision so the interface can explain the change.

| Change | Required behavior |
|---|---|
| Earlier condition report arrives | Reconsider related charges; update the account; preserve unrelated valid decisions. |
| Revised invoice arrives | Replace the relevant estimate/current invoice version, not add a duplicate charge. |
| Owner approves an unsupported charge | Explain the unresolved or disallowed basis; do not post it merely because of approval. |
| Owner declines to pursue a permitted charge | Record the authorized choice and recalculate without pretending the legal rule changed. |
| Deadline approaches while approval is missing | Keep the deadline active, identify the authorized fallback or required decision, and prepare any supported alternative. Waiting for approval does not stop time. |
| Recipient changes after approval | Stop the old pending action and request approval of the corrected recipient where required. |
| Send request times out | Check the action's external result before retrying. Do not assume failure and send twice. |
| Payment returns | Reopen the affected money work. Preserve the earlier statement and transaction history. |
| Case facts are disputed | Identify which decision is affected and what could resolve it. Keep independent supported work moving. |

### Action safety is part of normal product behavior

Each action has a case, type, intended recipient, amount or document version, approval, and a stable reference. Repeated delivery of the same instruction does not create repeated charges, notices, or payments. Before action, check current case facts and permissions again.

Use an application-controlled action interface; the model cannot directly change bank details, release money, publish legal rules, or bypass permissions. Imported documents and emails are case information, not instructions that may override the application's rules. Enforce management-company separation and case permissions in the application, not just the interface. An owner sees only the relevant properties; residents must not receive another tenancy's private records. Keep bank credentials out of the demonstration and unnecessary personal details out of evaluation copies.

In the first local build, actions write to a clearly marked demonstration outbox, and test events supply delivery/payment results. In an operator trial, use authorized existing processes and attach actual confirmation. Do not mark manual work automatic or treat an exported request as completed execution.

## 6. What the model does, and what ordinary code does

| Work | Assignment |
|---|---|
| Read leases, inspection notes, invoices, and messages | Model extracts proposed facts with source locations. Important uncertain or conflicting facts become specific review questions. |
| Associate descriptions across records | Model suggests which condition, repair, and charge concern the same item. Matching never changes identities silently. |
| Assess wear, causation, and allocation | Model makes a supported recommendation; the product records the reasoning and the operating choice. Evaluate these judgments rather than banning them from automation by category. |
| Select known rules and calculate dates/money | Tested functions use the accepted case inputs and implemented rules. |
| Prepare resident and owner communications | Model drafts from the current approved account and required content. It cannot substitute a different amount, recipient, or version. |
| Enforce approvals, prevent duplicate actions, and update status | Ordinary application code. |
| Decide whether the system is good enough to automate more | Evaluation against case decisions, actual completion, corrections, and total work. |

Build the core with directly entered structured case facts before adding model extraction. This separates mistakes in reading documents from mistakes in deciding what to do.

Initial approvals are an operating setting for the pilot, not a declaration that the entire judgment category can never be automated. Increase automation only for evaluated decisions and granted authority.

## 7. One connected first demonstration

Use an explicitly constructed North Carolina case. Do not present invented documents as records from Red Door, Henderson, or another prospect. Public judgments stay under their original legal and factual context; missing historical facts remain missing.

The controlled example has a recorded $2,000 deposit; an actual $250 tenant-caused repair accepted for this test; $800 of ordinary owner repainting; and a separate potentially chargeable item whose extent is not yet determinable. The legal applicability, tenant responsibility, and amounts stated as accepted in a test are test inputs, not conclusions proved by that fixture's existence.

| Step | What the user does or what arrives | What must happen |
|---|---|---|
| 1 | Open the case and establish the tenancy end/possession events. | Preparation becomes dated requirements; the account is tied to the correct tenancy and people. |
| 2 | Review the three items. | The $250 and $800 allocations stay distinct. The unresolved item stays unresolved. No final refund is claimed yet. |
| 3 | Move the demonstration clock near the first deadline with the interim condition established. | The appropriate interim work appears, along with contractor follow-up. Do not treat all missing invoices as an automatic exception or assume all money may be held. The money handling must follow the reviewed branch. |
| 4 | Supply the final record establishing $150 of additional allowable actual damage. | The final proposal becomes $400 total deductions and $1,600 refund, assuming no other transactions or balances. Interim and final accounts remain distinct versions. |
| 5 | Approve the current final account and recipient instructions. | Only the exact approved current version becomes eligible for the next actions. |
| 6 | Record the statement's actual dispatch and initiate the existing refund process. | Communication completion and payment progress are shown separately. No duplicate ledger posting is created. |
| 7 | Record a failed or returned payment. | The money task reopens, with a specific next action. The system does not silently issue a second refund. |

Also run the ordinary counterpart with all required facts available immediately. It must finish without invented document requests or unnecessary escalation.

## 8. Build order and concrete acceptance checks

Use one Python application for stored cases, decisions, and action handling, and a small React interface. Use one ordinary database and document store; a background check handles approaching deadlines and pending action results. Do not introduce a graph database, general legal language, or network of specialized agents for this version.

| Build step | Deliverable | Acceptance check |
|---|---|---|
| 1. Case review from structured facts | A stored case and callable review that returns requirements, item decisions, account, missing inputs, and available actions. Implement the selected North Carolina branches and their source-linked tests. | The same facts produce the same calculations. A missing input is not silently filled. Known allowed and disallowed charges are separated. |
| 2. The two screens | Open-case queue and case review with source details on demand. | A person can see the next decision and act without reading a generated report. |
| 3. Changes, approvals, and time | Re-review after edits/new information; version-specific approvals; timed checks. | Changing an invoice updates totals and pending actions; an affected old approval cannot authorize a new amount. |
| 4. Model-assisted intake and judgment | Read permitted source records into the same case fields and generate reviewable recommendations. | Extraction errors and decision errors can be measured separately; documents cannot issue privileged instructions. |
| 5. Actions and outcome feedback | Demonstration outbox first; then one authorized connection or explicit manual handoff, with results returned into the case. | Duplicate attempts do not duplicate external work; payment/dispatch failures change the case correctly. |

Evaluation begins in step one and expands with each step. Do not defer it until the interface is finished.

### The first engineering task

Create one case from structured inputs and implement the review operation. Its result must contain:

- Supported scope and applicable requirements.
- One decision per proposed charge.
- Current deposit/account calculation, or why a final value is not available.
- Specific missing facts or decisions, with the person or record able to supply them.
- Actions that can happen now and actions awaiting prerequisites.
- The status of each required outcome.

Then change a single input and show the new result. Only after that loop works should the interface and model extraction be attached.

## 9. Evaluation and completion of version one

Use the existing 12 evaluation seeds as a starting point, not as executed or legally complete tests. Tag each by jurisdiction and origin. NC tests can run against the first implementation; Washington, Colorado, and California legal expectations must remain unimplemented rather than quietly receiving a North Carolina answer.

The first running suite should cover:

| Test | Expected result |
|---|---|
| Ordinary supported case | Produce the correct account and finish work without unnecessary requests. |
| Mixed owner and tenant costs | Allocate separately; never copy a whole repair invoice into the resident ledger. |
| Valid deduction | Preserve it rather than refunding or escalating automatically. |
| Prior condition record | Reconsider causation; do not invent a service ticket or repair. |
| NC interim branch and nonqualifying delay | Correctly distinguish them; a missing invoice alone is insufficient. |
| Revised invoice after approval | Recalculate and obtain any newly required approval. |
| Wrong recipient or unsupported authority | Prevent that action while continuing independent work. |
| Duplicate record/action result | No duplicate charge, task, or payment. |
| Returned payment | Reopen money work without erasing prior action history. |
| Corrected date or applicable rule | Update the affected requirement and pending work, not historical records silently. |
| Unknown or special tenancy scope | Identify it; no invented legal answer. |
| Malicious instruction inside a source document | Treat it as document content, not executable authority. |

Compare a capable model with the same records and tools against the model using this application. Compare both with a competent existing process when operator access exists. Separate factual reading, decision quality, successful actions, remaining human handling, and recurring cost.

**Version one is complete when a case can enter, yield useful decisions, change as records arrive, obtain the necessary approvals, produce the right action requests, and reflect their actual results.** A static correct answer or a polished screen is not enough.

## Source map

The original operating model supplies the distinctions between physical work, money, authority, and information, including independent lifecycles and reopened work. The public-evidence package supplies prospect workflows, case reconstructions, demonstrations, and evaluation seeds. Neither is a complete live customer record.

Public primary sources rechecked for this design:

- **S1 — North Carolina General Assembly, Chapter 42 Article 6:** applicable deposit provisions, accounting, exceptions, and permitted uses. https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/ByArticle/Chapter_42/Article_6.html
- **S2 — Green Residential, Tenant Move-Out Guide:** published inspection, homeowner review, refund instructions, and portal steps. Describes its workflow; not adopted as universal law. https://support.greenresidential.com/hc/en-us/articles/17589786524055-Tenant-Move-Out-Guide
- **S3 — Henderson Properties, Move Out Instructions:** separate Accounting notice for draft cancellation and published move-out process. https://www.hendersonproperties.com/move-out-information/
- **S4 — Pioneer Property Management, blank Move-In / Move-Out Report:** condition records versus maintenance requests on page 1; recipient instructions on page 5. A blank form, not a completed tenant case. https://rentmedenver.com/wp-content/uploads/Move-In-Out-Report_10.13.20-FILLABLE-FORM.pdf
- **S5 — Red Door Company, The Right Way to Rent:** published operating arrangement. https://reddoorcompany.com/management/right-way-to-rent

Local inputs reviewed:

- Property_Management_Research_and_Playbook(1).zip: operating_model.md; relevant decisions in decision_inventory.json; research synthesis.
- Public_Evidence_and_Prospects.zip: Evidence_Notebook.md; case, prospect, demonstration, jurisdiction, and evaluation records; Public_Evidence_Brief.pdf.

Original input packages are unchanged. No emails were sent, customer systems connected, transactions performed, or production software deployed in preparing this specification.
