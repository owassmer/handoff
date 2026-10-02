# The property business as it actually operates

**Purpose.** This is an original operating and decision model, informed by the primary sources listed in `operating_sources.csv`. It is a broad working map for discovering a business, not a claim that one process fits every property. The companion `decision_inventory.csv` contains 115 distinct decision prompts across 17 families, with triggers, inputs, choices, authority, execution, outcomes, constraints, automation hypotheses, dependencies, and questions for operator validation.

**Coverage boundary.** It covers conventional rental housing, scattered homes, multifamily, student and affordable housing, associations, commercial space, and hospitality variants, including normal operation, stress, and exit. A locally exhaustive implementation also needs the actual management agreement, leases, physical systems, loan documents, insurance, program rules, governing documents, and applicable current law. The inventory is not a measured distribution of time, case frequency, avoidable cost, or automation feasibility. Its source IDs identify supporting operating domains; they do not imply that a source endorses our product hypotheses.

## 1. What the business is for

People and businesses need useful space. Somebody owns that space and must pay to preserve it. Other parties supply labor, capital, utilities, protection, and rules. Property management makes the resulting promises work day after day: people can use what they were promised; problems are resolved; the right money reaches the right party; the property remains usable; the owner can make informed choices.

There are **three different businesses** that often appear in one software account:

| Business | Economic purpose | Typical decision owner | What must not be conflated |
|---|---|---|---|
| Property ownership/investment | Provide useful space and earn an acceptable return within obligations | Owner, investor, asset manager, board | Property value and collected rent are not management-company revenue |
| Property management | Deliver agreed operations profitably and retain clients | Management principal, regional manager, site manager | Owner savings do not automatically become manager savings or willingness to pay |
| Occupant's household or business | Live, work, trade, produce, receive care, or stay temporarily | Household members, tenant company, guest, specialist operator | Occupants are people with rights and purposes, not merely sources of rent or service demand |

A vertically integrated owner-manager can align some tradeoffs internally. A third-party manager must negotiate them. An association manager serves collective governance; the board and members retain decisions defined by law and governing documents. A building manager, investment asset manager, facilities contractor, hotel operator, and licensed healthcare operator do not hold interchangeable authority.

California's official property-management reference confirms the breadth of the role: agency agreements, owner and tenant duties, leasing, maintenance, accounting, staffing, purchasing, and reporting. It is used here as a scope check, not a source for current prices or a universal legal rule. [O01 — DRE](https://www.dre.ca.gov/files/pdf/refbook/ref22.pdf)

## 2. All the parties and what connects them

One person or firm can fill multiple rows; a row cannot disappear merely because roles share an employer.

| Party | What it supplies or receives | Decisions/rights it usually holds | Main connection to the manager |
|---|---|---|---|
| Beneficial owner; property-owning entity; investor; fund | Equity, objective, risk capital; distributions and property value | Investment strategy and reserved approvals | Mandate, budgets, approvals, funding, reporting |
| Asset manager; owner representative; family office | Portfolio direction and capital allocation | Delegated owner decisions | Operating plan, exceptions, forecasts, transaction preparation |
| Association/co-op board; committees; voting members | Collective authority, assessments, shared-property decisions | Reserved votes, budgets, rules, capital decisions | Meeting materials, approvals, enforcement, reserves, records |
| Management-company principal; licensed broker where applicable | Contractual operating service and supervision | Client acceptance, staffing, delegated actions | Scope, economics, supervision, escalation, liability |
| Regional/site/property manager | Day-to-day coordination and decisions | Authority granted by mandate, policy, law | Owns execution across people and systems |
| Leasing/brokerage; marketing; reservations staff | Demand, tours, negotiation, booking | Delegated offers and representations | Availability, pricing, approved terms, qualification |
| Bookkeeper; controller; treasury; payroll; CPA | Accurate books, client funds, payments, filings | Financial controls and approved releases | Bill/receipt matching, cash availability, distributions, close |
| Prospective occupant; applicant; tenant; resident; guest | Demand, payment, information; receives use and service | Application, agreement, notice, complaint, lawful remedies | Inquiry through move-out and later disputes |
| Roommates; household members; guarantor; emergency contact; representative | Shared use, guarantee, consent, emergency support | Rights differ from named payer or leaseholder | Occupancy, access, changes, lawful disclosure |
| Housing authority; subsidy administrator; tax-credit allocator; service coordinator | Assistance, eligibility rules, monitoring, resident support | Program approval and oversight within program | Certification, assistance payment, inspection, transfer, reporting |
| Maintenance employee; building engineer; cleaner; concierge; security | Physical service and observations | Role-specific operational and technical authority | Work, access, condition, safety, shift coverage |
| Trade contractor; general contractor; subcontractor; supplier | Skilled work, parts, capacity, warranties | Methods within qualification and contract | Scope, bid, dispatch, progress, change, completion, invoice |
| Architect; engineer; surveyor; inspector; environmental specialist | Qualified assessment or certification | Professional conclusions within scope | Design, safety, condition, permits, reserve studies |
| Utility; telecom; waste; meter provider; district service | Essential infrastructure and measured usage | Service/network control and tariff administration | Account transfer, interruption, repair, billing, capacity |
| Bank; payment processor; card network; escrow provider | Settlement, account custody, payment events | Payment controls, returns, holds | Receipts, releases, reconciliations, fraud responses |
| Lender; servicer; lender's inspector | Debt and restricted reserves | Covenants, consents, draws, cash management | Reporting, reserve release, repairs, insurance, default |
| Insurance broker; insurer; adjuster; restoration firm | Risk transfer, claims determination, recovery | Policy coverage and claim approval | Risk changes, renewals, incident notice, mitigation, payment |
| Lawyer; mediator; court; enforcement officer; receiver; trustee | Advice, dispute resolution, enforceable orders | Legal representation, adjudication, lawful enforcement/control | Notices, claims, possession, insolvency, transfer of authority |
| Building/fire/health/environment/rental regulator; tax authority | Public standards, permits, inspections, taxes | Enforcement and statutory approvals | Registration, filings, inspections, correction, appeals |
| Emergency responders; neighboring owners; adjacent occupants | Immediate response and shared exposure | Emergency powers; independent rights | Hazards, access, common systems, incident communication |
| PMS; CRM; access-control; accounting; screening; communications; AI vendors | Records, calculations, workflows, interfaces | Only permissions delegated to software/provider | Data, actions, audit history, outages, export, switching |
| Buyer; seller; developer; outgoing/incoming manager | Asset or responsibility transfer | Transaction-specific rights | Diligence, assignments, opening balances, keys, unfinished obligations |

The important separation is **who wants the result, who pays, who can authorize it, who does it, and who can verify it**. These are often five different parties. A better recommendation alone does not join them.

## 3. Four flows run through every operation

| Flow | Ordinary path | Typical break | Product implication |
|---|---|---|---|
| Physical use and work | Space becomes usable; occupant takes possession; equipment is serviced; defects repaired; space returned | Access denied; diagnosis wrong; part absent; contractor unavailable; work marked complete prematurely | Digital progress must correspond to a real change in the property |
| Money | Occupant/subsidy pays; bank settles; ledger allocates; operating bills and debt paid; required reserves retained; owner receives available cash; manager earns agreed fees | Returned payment; wrong owner ledger; restricted cash mistaken for spendable cash; duplicate invoice; unapproved cost | The account with cash is not necessarily the party entitled to spend it |
| Authority and obligations | Law and contracts establish rights; owner/board delegates; PM approves; qualified parties execute; regulator/court may supersede | Owner absent; unclear scope; unsigned amendment; expired power; court hold; contradictory instruction | Action rights need actual scope, limit, effective date, and change handling |
| Information and commitments | A report enters; facts are checked; a decision made; someone commits; updates and completion return | Multiple inboxes; stale status; silent waiting; disputed facts; undocumented promise | Track who will do what by when and whether the promised result happened |

**The sequence is not always linear.** Emergency mitigation can precede cost allocation. A vendor can complete work before an invoice arrives. A lease can be signed before the unit is ready. A payment can appear before it finally settles. A property can sell while a claim remains open. The model must allow these combinations rather than overwrite them with a single status.

For example, California's trust reference distinguishes bank records from beneficiary records; reconciling them is essential to knowing whose money is present. That distinction is the useful design lesson. It is not an instruction to apply California's precise rules everywhere. [O02 — DRE trust funds](https://www.dre.ca.gov/files/pdf/refbook/ref21.pdf)

## 4. Concurrent lifecycles and their states

These lifecycles coexist. A building does not move from leasing to maintenance and stop doing the other work.

| Lifecycle | Main states | Exit or recurrence | Important simultaneous condition |
|---|---|---|---|
| Ownership and management mandate | Prospect; diligence; agreement pending; signed; takeover; active; changed scope; termination pending; handover; residual obligations; archived | Renew, sell, change manager, restructure, dissolve | Legal owner, operating authority, and bank signer may change on different dates |
| Physical property and equipment | Planned/acquired; delivery/commissioning; usable; degraded; restricted; failed; temporary remedy; repair; verified usable; renovation; decommissioned | Repeated operation and renewal; redevelopment; demolition | Occupied space can be partly unusable; usable space can be unavailable to lease |
| Demand and occupancy rights | Available/coming available; prospect; tour; application; waitlist; offered; accepted; signed; pre-possession; occupied; amended; renewal; notice; holdover/disputed possession; returned; final account; residual claim | Renew or relet; cancellation; transfer; lawful termination | Marketing availability, legal possession, and physical readiness are distinct |
| Service request or planned work | Reported/due; identity located; urgency assessed; facts missing; scoped; responsibility identified; authorized; funded; assigned; scheduled; in progress; blocked; completion claimed; verified; billed; paid; reopened/closed | Callback; warranty; recurring service; capital escalation | One incident can require multiple jobs; one job can serve multiple units |
| Money and accounting | Obligation estimated; charge/invoice issued; disputed; approved; payment initiated; pending settlement; settled; allocated; reconciled; reported; refunded/adjusted/written off | Recurring rent, service invoices, assessments, taxes | Cash, receivable, expense, deposit liability, and owner distribution are different things |
| Complaint, legal matter, claim, or emergency | Detected; protected/contained; assessed; notified; investigated; remedy proposed; contested; approved/ordered; carried out; recovery/settlement; appeal/reopened; retained | Recurrent condition, further loss, new claim | Ordinary collection or access workflows may be suspended while essential service continues |
| People, vendors, systems and capacity | Needed; selected; verified; granted access; trained; active; reassigned; unavailable; suspended; replaced; access revoked | Renewal, hiring, turnover, outage recovery | A valid contract does not mean capacity is available today |

**Do not infer a finished result from an intermediate state.** “Notice received” is not “possession returned.” “Paid” is not “settled.” “Invoice approved” is not “work verified.” “Vendor assigned” is not “appointment confirmed.” “Manager offboarded” is not “all duties extinguished.”

## 5. Transitions, exceptions, and reversals

The table identifies consequential joins. It does not prescribe a universal order for every jurisdiction.

| Transition | Conditions to establish | Exception or reversal | Consequence for connected work |
|---|---|---|---|
| Agreement signed → active management | Effective mandate; owner identity; funding; access; emergency contacts | Closing slips; authority contested; essential records absent | Conditional takeover; preserve emergency coverage; do not assume all powers started |
| Old manager → new manager | Funds/liabilities reconcile; records and keys received; open matters assigned | Missing deposits; disputed invoices; old credentials active | Separate unknown opening balances; revoke access; assign surviving duties |
| Future vacancy → marketable offer | Forecast date and permitted marketing; truthful attributes | Notice withdrawn; holdover; works delayed | Update prospects, commitments, staffing, and financial forecast |
| Applicant → accepted tenant | Permitted screening; actual decision authority; program fit | Report error; accommodation; queue priority; adverse action | Correct decision, provide applicable notice, preserve dispute path |
| Accepted → signed → possession | Operative agreement; required disclosures; funds conditions; safe readiness; legal availability | Signature fails; payment returns; current occupant remains; unit unsafe | Delay/alternative/credit as lawful; do not issue misleading access or readiness |
| Report → repair response | Correct location; severity; safe next step | Emergency; duplicate report; ambiguous unit; multiple affected systems | Immediate protection; merge facts without losing distinct affected occupants |
| Scope → approved/funded work | Correct responsibility; sufficient authority and cash | Owner silent; estimate exceeds cap; mandatory urgent duty | Defined emergency process; specific approval; owner funding; lawful mitigation |
| Assigned → attended → repaired | Confirmed provider; parts; lawful access; adequate diagnosis | No-show; no access; hidden damage; parts unavailable | Replan with named blocker and next commitment; update occupant |
| Completion claimed → verified | Original problem tested; competent assessment; unresolved issues recorded | Callback; resident disagreement; new defect | Reopen linked work; preserve history; avoid duplicate-charge assumptions |
| Invoice → payment | Approved scope; delivered work; payee verified; correct entity and funds | Duplicate; changed bank details; disputed scope; lien issue | Hold appropriate payment; verify independently; pay undisputed amount only when authorized |
| Receipt → settled available cash | Bank confirmation; allocation; reserves and restrictions recognized | Return; chargeback; wrong payer; unidentified receipt | Reverse correct entry; reassess arrears and distributions; no silent overwrite |
| Arrears → enforcement | Accurate debt; required notices; authority; no applicable hold | Repair dispute; assistance; bankruptcy; protected circumstance | Pause prohibited actions; counsel; settlement; corrected balance; essential repairs continue |
| Notice → possession returned | Actual surrender or lawful enforcement; belongings/access addressed | Abandonment uncertain; death/probate; holdover | Counsel and authorized process; delay turn and incoming possession |
| Vacant → ready → occupied | Sequenced work; inspection; utilities; legally usable space | Failed final check; damage after inspection; new tenant cancels | Reopen readiness; revise availability and commercial commitments |
| Inspection → compliant | Specific deficiency remedied; required acceptance/certification | Finding contested; remedial work insufficient; deadline missed | Appeal/correction as available; exposure remains until resolved |
| Casualty → safe reoccupation | Qualified safety finding; restoration; service; required permission | Hidden damage; claim denied; funding insufficient; tenant displacement | Separate recovery negotiation from urgent safety; alternative accommodation and funding plan |
| Solvent owner → receiver/bankruptcy control | Court order; debtor identity; authority; restricted funds | Changing orders; partial asset coverage; stay relief | Replace approval path; hold affected collection/payments; continue permitted essential operation |
| Operating asset → sale/redevelopment | Transaction; assignment; notices; cash/deposits; tenant rights; work continuity | Sale fails; loan consent absent; possession schedule infeasible | Continue current obligations; reverse provisional changes; retain verified records |
| Case closed → reopened | New fact; reversal; recurrence; dispute; appeal | Prior record deleted or overwritten | Preserve old decision, record correction and downstream changes |

These reversals are not rare technical edge cases to append later. Whether they are frequent enough to justify a product must be measured, but they belong in the operating model from the start.

## 6. How the property manager makes a decision

A useful decision description asks: **What changed? What do we actually know? What needs to happen? Who can decide? Who will do it? What will count as done? What happens if the plan fails?**

The manager does not personally decide everything. They can originate a recommendation, exercise delegated choice, request someone else's approval, coordinate execution, and verify the result. The same person may switch among these roles in a single incident. A viable product must know which role it is replacing or supporting.

| Decision family | Inventory IDs | Main dependency |
|---|---|---|
| Management mandate | D001–D007 | Staff capacity; vendor coverage; available records |
| Takeover and operational setup | D008–D014 | Mandate; funding; access |
| Portfolio planning and resource allocation | D015–D020 | Budget; leasing; capital |
| Demand and leasing pipeline | D021–D026 | Turn plan; rent approval; inspections |
| Applications and eligibility | D027–D032 | Published criteria; source access |
| Lease and move-in | D033–D037 | Screening; pricing; readiness |
| Occupied-property service | D038–D044 | Occupancy identity; responsibility map |
| Rent; receivables; arrears | D045–D050 | Lease terms; meter; resident change |
| Reactive repairs and incidents | D051–D061 | Access; contacts; property equipment |
| Preventive work; capital; energy | D062–D068 | Asset inventory; access; vendor availability |
| Procurement and vendor relationships | D069–D073 | Needed trade; service geography |
| Accounting; cash; reporting | D074–D081 | Contract; service completion; property identity |
| Renewal; vacancy; turn | D082–D088 | Pricing; resident issues; unit plans |
| Legal; insurance; casualty; continuity | D089–D094 | Repairs; resident history; legal hold |
| Management-company people; systems; commercial health | D095–D100 | Staff capacity; risk; client scope |
| Asset sale; refinancing; redevelopment; exit | D101–D104 | Closed books; physical backlog; legal matters |
| Segment-specific additional decisions | D105–D115 | Mandate; budget; reserve plan |

The CSV's `what_to_validate_with_operator` column is important: it converts a desk-research map into a fieldwork instrument. Ask an operator to walk through completed, delayed, reopened, and disputed examples. Count omissions and rewrite the map around the actual work.

## 7. Segment differences that change the business

| Segment | Operating distinctions | Buyer/authority differences | Product consequence |
|---|---|---|---|
| Self-managed small landlord | Few properties; owner does leasing, approval, bookkeeping and vendor selection; sporadic work | User, payer and owner often one person | Simple low-cost or event-based service; less coordination volume per account |
| Third-party scattered single-family/small multifamily | Travel; different owners and standards; vendor coverage; separate reserves; heterogeneous homes | PM buys tools but owner may get most property-level benefit | Owner authority and client-level economics can dominate software sophistication |
| Large institutional single-family | Geographic clusters; centralized staff; standardized policies; remote field execution | More consistent delegated authority and procurement | Route density, repeatable service and integration can improve economics |
| Conventional multifamily | Shared systems; on-site team; many residents affected by one incident; continuous leasing | Owner/AM and regional/site teams divide rights | Building-wide cause and impact matter alongside unit tickets |
| Student/shared housing/co-living | Bed and room can be separate saleable units; guarantors; roommates; concentrated turns | Student/household/guarantor rights differ; operator policies matter | Lease identity is not room occupancy; seasonal capacity and allocation are central |
| Affordable/subsidized/restricted housing | Program eligibility; waitlists; recertification; rent/subsidy split; inspections; agency contact | PHA/contract administrator/allocator may hold key decisions | Program-specific state and dates; never one generic affordable-housing rule set |
| HOA/condominium/co-op | Common property; assessments; reserves; votes; rule enforcement; architectural requests | Board/member governance; manager implements delegated authority | Approval validity and common/private responsibility matter more than lease funnel |
| Office | Tenant buildouts; lease abstracts; shared services; after-hours HVAC; expense recoveries | Tenant companies and brokers; negotiated long leases | Clause-specific charges, operating hours and fit-out delivery |
| Retail | Co-tenancy; permitted use; exclusivity; sales reporting; percentage rent; shared customer areas | Anchor and other tenants' rights interact | One tenant's condition can trigger another lease's economics |
| Industrial/logistics | Loading; power; fire systems; permitted processes; environmental exposure; roof/slab responsibility | Tenant operates its own production/logistics business | Technical scope, downtime and responsibility split; standard residential repair triage insufficient |
| Mixed-use | Residential, commercial and common elements share systems | Multiple contracts and governance layers | Allocate physical impact and cost across distinct legal rights |
| Hospitality/short-stay | Nightly inventory; channels; housekeeping; guest recovery; lodging taxes; brand/OTA conditions | Operator may control guest service and pricing; owner retains capital | Different tempo, inventory granularity and payment/tenancy rules; separate initial market |
| Manufactured housing; parking; storage | Land/site/space rights may differ from building ownership; vehicles or goods rather than a household unit | Specialized occupancy and lien/possession rules | Same operating families with different objects and legal consequences |
| Senior housing; healthcare; data centers; specialist industrial | Building operations coexist with care, clinical, critical-IT or process operations | Licensed/qualified operators hold specialized responsibilities | Distinguish real-estate service from regulated operating business; partner for specialization |

Affordable-housing and association cases demonstrate why “all property managers” is not one implementable customer segment. The HUD handbook shows the program-specific selection structure; it is historical and must be supplemented with current program rules before deployment. Florida's condominium statute joins qualified physical reserve assessment to funding and governance. [O07 — HUD](https://archives.hud.gov/offices/adm/hudclips/handbooks/hsgh/43503c4HSGH.PDF); [O15 — Florida](https://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0718/Sections/0718.112.html)

Commercial service charges similarly depend on what individual leases permit, how services are procured and allocated, and how actual expenditure is reconciled. RICS is a useful commercial operating reference; its standard is not a statement of US law. [O12 — RICS](https://www.rics.org/content/dam/ricsglobal/documents/standards/Service-Charges-in-Commercial-Property-2nd-edition.pdf)

## 8. Representative legal and institutional constraints change the design

The implication is not “legal work cannot be automated.” It is that automation needs the actual rule, relevant facts, valid authority, and a correction path.

| Example | Source-supported fact | General operating/design lesson |
|---|---|---|
| US tenant screening | A condition such as extra deposit or co-signer can be adverse action when a consumer report contributes to it; notices are not only for outright rejection | Preserve actual decision inputs and trigger the right downstream action; a score alone is insufficient [O03](https://www.ftc.gov/business-guidance/resources/using-consumer-reports-what-landlords-need-know) |
| Lead disclosure | Most pre-1978 housing requires specified information before lease signing | Building facts and action order matter; a later document upload may not cure a missed step [O05](https://www.epa.gov/lead/real-estate-disclosures-about-potential-lead-hazards) |
| NYC essential services | Heat obligations depend on season/time/temperature; hot-water obligations apply year-round | Urgency cannot be determined by generic keyword alone; property and live conditions matter [O08](https://www.nyc.gov/site/hpd/services-and-information/heat-and-hot-water-information.page) |
| California possession and deposits | Official guidance prohibits self-help lockout and distinguishes lawful deductions from ordinary wear | Payment status cannot directly trigger lock changes; restoring space and allocating repair cost are separate decisions [O13](https://oag.ca.gov/tenants) |
| US algorithmic rental pricing | DOJ's 2025 announcement addresses sharing of competitively sensitive information in a proposed RealPage settlement | Do not assume data pooling or coordinated optimization is permissible merely because technically feasible; examine actual data and market conduct [O04](https://www.justice.gov/opa/pr/justice-department-requires-realpage-end-sharing-competitively-sensitive-information-and) |
| Bankruptcy | Automatic stay and cash-collateral restrictions can change permissible collection and spending; exceptions and orders matter | Authority must change when circumstances change; old automated instructions must be interruptible [O10](https://www.uscourts.gov/court-programs/bankruptcy/bankruptcy-basics/chapter-11-bankruptcy-basics) |
| Hazardous-energy maintenance | OSHA's standard regulates energy isolation during covered servicing | A digital agent can coordinate work; qualified physical safety procedures still have to occur [O09](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147) |
| Fair housing | Protected rights apply across housing transactions, not only initial applications | Pricing, service, access, renewal and enforcement all need appropriate treatment; changing the interface does not remove the obligation [O14](https://www.justice.gov/crt/fair-housing-act-1) |

These are architectural examples, not a legal product specification. Laws, regulations, court orders, agency guidance, professional standards, contracts, and owner preferences have different force. They should not be merged into an undifferentiated “policy” without identifying the source and who may change it.

## 9. What this map suggests about opportunities

The following are **inferences to test**, not market facts established by the sources.

1. **Waiting can be more expensive than doing.** Many jobs stall between a known need and authorized, funded, scheduled, physically completed action. Measure elapsed time and its cause as well as staff minutes. A language model that writes faster does not solve lack of a plumber or an owner refusing funds.
2. **The most valuable unit may be an outcome across several tasks.** “Ready for the promised move-in date,” “repair actually works,” or “correct owner funds available after close” can align product scope with what operators already recognize. It need not require replacing their systems.
3. **Information can change the process rather than decorate it.** Good diagnosis can eliminate a visit; permission can be agreed in advance; a vendor can receive the right parts before dispatch; jobs can be combined geographically; responsibility can be resolved without withholding urgent service.
4. **Authority is often a redesign opportunity.** A human approval may exist because nobody has written the owner's allowable choices clearly. Pre-authorized classes, spending limits, and escalation conditions can remove delay. This is different from assuming every approval is legally mandatory or all approvals are waste.
5. **Physical observations deserve attention.** The first reliable condition check can prevent downstream disagreement in repair, turnover, billing, and claims. Its value must exceed collection burden; indiscriminate photography and forms are not a product advantage.
6. **Financial benefit follows the contract.** Lower property vacancy may benefit an owner much more than a percentage-fee manager. The paying customer must capture enough value, or the commercial arrangement must change.
7. **Exception handling is not inherently forever-human.** Some exceptions are missing facts, bad records, or unstated policy. Others require technical expertise, negotiation, physical work, or reserved authority. Classify the actual reason, then test whether it can be removed, standardized, delegated, or supported.
8. **Recurrence creates learning only if outcome and cause are known.** A callback may indicate poor work, wrong diagnosis, occupant behavior, or a new defect. Counting “tickets closed” can reward premature closure; learning requires enough attribution to improve future choices.
9. **Human service can be the right delivery model.** A company can sell reliable completion and use software internally before selling a standalone product. The service must still earn sustainable margins and avoid becoming bespoke coordination for every client.
10. **Breadth is a discovery tool, not an implementation commitment.** The map identifies possible markets. A first business should specify one paying customer, one consequential result, one operating setting, one authority model, and a credible way to verify delivery.

DOE's operations guidance supports treating maintenance as a system of interacting functions that affects reliability and efficiency. It does not establish a particular savings percentage for private rental properties or prove any proposed company will capture it. [O06 — DOE](https://www.energy.gov/cmei/femp/operations-and-maintenance-challenges-and-solutions)

## 10. How to validate completeness with an operator

Use actual cases, not only interviews about preferred workflows. For each candidate customer obtain, with permission, a small set spanning ordinary work, delayed work, disputed work, repeat failure, emergency, takeover and exit. Reconstruct timestamps and actions from their existing records; distinguish what the records prove from what staff remember.

For every case ask: Who wanted what? Who was entitled to decide? What was missing? What changed physically? What money moved? Who waited for whom? What did completion mean? What later reversed it? What did the manager earn or lose? What did the occupant experience?

Map each observation to the decision register. Add missing decision variants; delete inapplicable ones from the customer-specific version; keep the broad market map intact. If the work cannot be sampled, outcomes cannot be verified, authority cannot be granted, or the beneficiary will not pay, that is a business finding—not an invitation to build a more elaborate architecture.
