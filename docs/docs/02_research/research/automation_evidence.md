# Automation evidence, source audit, and transfer to property operations

Research date: 15 September 2026. This is a decision record and source critique, not a forecast of model capability. The quantitative studies below support mechanisms and evaluation choices; their effect sizes are not property-management business-case assumptions.

## 1. What survives scrutiny in the supplied argument

There is a credible business opportunity in moving work from an incoming request to an actual result. There is not yet evidence in the supplied articles that a particular proportion of the property manager's job is inherently human, that a platform must model the whole business before helping, or that a new vendor can charge for every dollar of property value it creates.

Three distinctions matter:

1. **Capability:** Can a person, software, a model, or a combination correctly perform this particular decision?
2. **Authority:** Who can legally and contractually commit the action, spend the money, enter the home, change the ledger, or bind another party?
3. **Economics:** Does the new arrangement produce a better result after review, integration, support, and recovery costs—and does the buyer capture enough of the gain to pay?

These are separate questions. A task can require professional authority without requiring that professional to perform every calculation or communication. A technically automatable task can remain uneconomic. A task described as relationship work may contain a great deal of automatable fact gathering, option generation, negotiation within agreed limits, and follow-up.

## 2. Forbes claims audit

The full Forbes article was read. This audit follows its cited numbers to the underlying studies or intermediary publications and records what each source can actually support.

Source: [Donati, Forbes, 8 July 2026](https://www.forbes.com/sites/angelicakrystledonati/2026/07/08/the-property-managers-job-is-changing-not-disappearing/).

| Claim carried by the article | What the cited source actually establishes | Treatment in the business case |
|---|---|---|
| Only 8% have fully automated a process | Buildium's own 2026 report landing page says this, alongside 58% using AI. The research blog says its combined survey covered more than 3,200 PM professionals, owners, and renters. That is not a denominator of 3,200 PM companies. Public pages do not establish sampling weights or the exact process-automation question. | Useful evidence of reported deployment difficulty. Not evidence that 92% are a reachable market or that only 8% of tasks can be automated. |
| Smart buildings have 23% better tenant retention | Wiss publishes the number, but supplies no study, sample, model, or source link attached to that claim. | Exclude from financial projections. Treat as an unverified marketing statistic. |
| Satisfaction improvement means 8.6% higher renewal likelihood | The primary Hu/Kok/Palacios paper says **greater willingness to renew** in an office-tenant observational study. Actual move-out is a separate outcome. | Do not convert into residential renewal lift or AI ROI. |
| 28% of professionals trained | Propmodo instead claims 28% of firms have a formal technology-training program. Its linked Deloitte report does not substantiate that statistic in the inspected text. | Both a measure/denominator mismatch and an unverified source chain. Exclude. |
| 52% see AI as a collaborator | The linked EliseAI report surveys 280 director-level-or-above executives at operators with at least 200 employees. The 52% assertion was not located in retrieved text; relevant AVIF charts were not accessible here. | Do not generalize to all property managers. Verify exact chart/question before retaining number. |
| 85% of institutional investors expect AI | Smartdev repeats this and attributes it to a CBRE 2024 Global Investor Survey without a direct source. Targeted CBRE search did not recover support. | Unverified. Do not use to establish mandatory adoption or demand. |
| A chatbot can resolve 70%, leaving 30% for people | No measured population accompanies the illustration. | Replace with observed eligible-case completion and escalation rates in the pilot. |

Primary-source links and cautions:

- [Buildium report](https://www.buildium.com/resource/2026-property-management-industry-report/) and [research-method summary](https://www.buildium.com/blog/2026-rental-market-predictions/). Vendor-sponsored self-report. The adoption change is between survey years, not proof of a controlled panel of identical firms. A reporting year of 2026 includes 2025 responses.
- [Wiss article](https://wiss.com/proptech-and-its-impact-on-the-real-estate-market/). Its 23% statement is about smart access/visitor/parking technologies, not an agent independently running property management.
- [Hu, Kok, Palacios, published January 2026](https://link.springer.com/article/10.1007/s11146-025-10043-6). Office surveys and building data; controlled observational associations. Abstract confirms the willingness/actual-outcome distinction. Publisher notes acknowledge sample selection and potential confounding. Actual occupancy labels partly use CoStar, company websites, and Google Maps; move-out timing is partly inferred from survey cessation. Raw data and code are available on request, not directly reproduced here. The freely accessible [2023 conference draft](https://eres.architexturez.net/system/files/P_20230221195520_2606.pdf) has different sample sizes and estimates; do not mix editions.
- [Propmodo](https://propmodo.com/ai-is-changing-property-management-faster-than-most-teams-can-keep-up/) links this [Deloitte 2023 outlook](https://www2.deloitte.com/content/dam/insights/articles/us175539_cfs_fsi-outlook-commercial-real-estate/DI_CFS_FSI-Outlook-Commercial-real-estate.pdf). Searched training/formal/28% and inspected workforce/technology sections. Training-program prevalence is not established by that linked report.
- [EliseAI survey](https://eliseai.com/resources/the-state-of-ai-in-multifamily). Methodology: 138 property-management, 68 operations, 74 marketing executives; all director level or higher, large employers. Its claimed expense and conversion improvements are respondents' reported outcomes without a randomized comparison. Strong willingness to buy in this sample does not establish small-operator budgets. Industry-wide claims of an enduring competitive moat exceed the survey design.
- [Smartdev](https://smartdev.com/ai-use-cases-in-commercial-real-estate/). Third-party software-service marketing, not the claimed CBRE primary survey. The same article mixes maintenance, due diligence, leasing, and predictive systems. Those are separate interventions.

The article's sharp division between routine steps and human thoughts should not become a product boundary. The supplied McKinsey PDF is more qualified: some formerly judgment-heavy work can become controlled, repeatable work. Its occupation-group and construction/real-estate hour estimates are modeled potential, not measured hours saved by an individual property manager. See `attachment_review.md` for the complete attachment audit.

## 3. Palantir: the transferable mechanism and the boundary

[Connecting Agents to Decisions](https://blog.palantir.com/connecting-agents-to-decisions-277dee8ddb40), 28 April 2026, was read in full. It connects decision-relevant data, calculation, execution, and permission; it also emphasizes actual system updates and learning from outcomes. Its detailed Onyx manufacturer example is explicitly fictional. It is a vendor architecture argument, not a causal evaluation of deployment benefits.

For a property business, the useful application is modest: know the home or building, affected people, current obligation, available choices, who may authorize them, and whether the result actually happened. A maintenance request cannot be evaluated apart from access, safety, owner limits, contractor capability, and prior failed repairs. This does not require buying Palantir or building a comprehensive enterprise ontology. Start with the minimum reliable records and actions necessary to complete one valuable responsibility. Expand shared representations when several useful workflows require the same facts.

Do not assume recording an action creates trustworthy learning. A manager's approval can reflect time pressure; a contractor's completion flag can be wrong; unpaid invoices may distort apparent repair cost. Outcome labels require independent checks.

## 4. Cross-industry evidence: what transfers, and what does not

Each row is a concise study record. These findings concern the tools and populations studied, not a fixed ceiling for 2026 models.

| Study and primary source | Population, method, observed result | Practical implication and limit |
|---|---|---|
| **Customer support:** [Brynjolfsson, Li, Raymond, QJE 2025](https://danielle.li/assets/docs/GenerativeAIatWork.pdf) | Staggered rollout to 5,172 customer-support agents, analyzed using rollout timing. AI suggestions increased resolved issues/hour by 15% on average. Gains varied; inexperienced workers benefited more, while experienced/high-skilled workers had small speed gains and small quality declines. | Retrieval and response support can spread operating knowledge and improve onboarding. This was assisted chat at one company, not autonomous physical service. It supports testing training/ramp benefits separately from staff elimination. Use the published 5,172/15% figures; earlier drafts used 5,179/14%. |
| **Consulting:** [Dell'Acqua et al., final 2026 paper](https://www.hbs.edu/ris/Publication%20Files/dell-acqua-et-al-2026-navigating-the-jagged-technological-frontier_5c589c8c-fbb5-458f-b285-c944746cd717.pdf) | Preregistered randomization of 758 BCG consultants. On 18 tasks suited to the tested GPT-4, AI users completed 12.2% more tasks, about 25.1% faster. On the chosen task outside capability, correctness fell by roughly 19 percentage points. | The same UI can help one decision and harm the next. Evaluate distinct decisions and exceptions, not a single global accuracy score. One deliberately difficult outside-capability task does not establish that all strategic decisions must stay human. Final quality-effect estimates differ from popular 2023 summaries; do not casually repeat the old 40% headline. |
| **Product development:** [The Cybernetic Teammate, final June 2026 paper](https://pubsonline.informs.org/doi/10.1287/orsc.2025.20702) | P&G one-day workshops, 791 randomized participants; 776 completed post-task data. Individuals/teams, with/without GPT-4. AI-assisted individuals produced idea quality comparable to two-person teams without AI; proposals crossed technical/commercial boundaries more readily. | Property managers might prepare a repair-versus-replace or renewal proposal without serially consulting several departments for preliminary analysis. This is evidence on generating and developing ideas; not proof of successful product launches, autonomous judgment, or replacing ongoing teams. |
| **Office work:** [Dillon et al., 2025 field experiment](https://www.hbs.edu/ris/Publication%20Files/w33795_dd1e2857-d195-4333-86ba-6a8953119ed4.pdf) | Six months, 7,137 workers in 66 firms, randomized M365 Copilot access. Email time fell 1.3 hours/week on intent-to-treat; the estimate for intensive users was 3.6 hours. No significant meeting-time change. Telemetry did not assess work content. Some authors worked for Microsoft. | Improving individual drafting does not automatically remove handoffs or meetings. To sell operational completion, change who waits on whom and what can proceed under standing authority. Do not label the 3.6-hour estimate a saving for every licensed worker or a cash saving. |
| **Software maintenance:** [METR July 2025 experiment](https://arxiv.org/abs/2507.09089) | Sixteen experienced open-source developers, 246 real tasks randomized to AI permitted or prohibited. Early-2025 tools increased time by 19%, despite participants believing they were faster. | Measure review/rework and finished output, not perceived productivity. An expert PM with deep local knowledge may spend more time correcting a generic assistant than doing the task. Small, selected sample and old tools prevent generalization to all developers or current models. |
| **Changing capabilities:** [METR February 2026 update](https://metr.org/blog/2026-02-24-uplift-update/) | Later study involved 57 developers and 800+ tasks. Authors judged the estimated current productivity effect unreliable because developers/tasks selectively opted out of no-AI conditions, pay changed, and concurrent agents complicated time accounting. | Do not freeze the 2025 slowdown as a permanent fact. Also do not rebrand biased later estimates as a reliable speedup. A pilot needs inclusion rules, visibility into refused/abandoned cases, and person-time plus elapsed-time measures. |
| **Economy-wide adoption:** [Humlum and Vestergaard, July 2025 version](https://www.andershumlum.com/s/chatbots_july25.pdf) | Two Danish survey rounds, about 25,000 workers per round and 7,000 workplaces across 11 exposed occupations; linked administrative data and difference-in-differences. Aggregate earnings/hours effects near zero over the observed horizon; reported average time savings about 3%. | Adoption can change tasks without immediately changing payroll or revenue. Build a buyer-specific capture plan. This is early-period, nonrandom chatbot adoption, not a verdict on later integrated agents or a PM-specific labor-demand estimate. |
| **Clinical reasoning:** [Goh et al., JAMA 2024](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2825395) | Fifty physicians randomized to GPT-4 access plus conventional resources or conventional resources alone; up to six clinical vignettes in an hour. Median reasoning scores 76% vs 74%; adjusted difference not significant. Standalone-model exploratory analysis scored higher. | Human-plus-AI is not automatically superior to either component. Test how reviewers actually respond to suggestions, not simply whether a review checkbox exists. Vignettes are not patient outcomes, and this is not a medical capability claim for today's models. |
| **Building systems:** [Berkeley Lab, October 2020](https://bies.lbl.gov/publications/proving-business-case-building) | Smart Energy Analytics Campaign: 104 organizations, about 6,500 buildings. Documented median annual energy savings of 3% for energy-information systems and 9% for fault detection/diagnostics; two-year simple payback. Observational adoption campaign plus commissioning practices, not randomized LLM deployment. | Physical operations can yield measured value through sensing, prioritization, corrective action, and verification. A model need not do everything. Where equipment/telemetry are missing, do not import this saving into scattered-home budgets. A fault alert is valuable only if someone can repair it. |

## 5. Assumptions to challenge through operating design

The following are our deductions and proposed tests, not conclusions proved by the studies above.

| Inherited assumption | Better question | Product consequence |
|---|---|---|
| Relationships cannot be automated | Which part is reliable availability, remembered commitments, clear explanation, discretionary negotiation, physical presence, or personal trust? | Automate remembering and following through; experimentally test bounded negotiation. Keep an accessible accountable person. Do not confuse warm wording with resolved problems. |
| A human must approve every consequential action | What authority can be agreed in advance, with which exclusions and limits? | Preauthorize ordinary actions where lawful and contractually permitted; escalate changed scope, conflicting facts, exceptions, and material commitments. Requiring approval on every message can destroy the benefit. |
| Owner approval is always needed above a fixed amount | Is the delay caused by an unavoidable right, a negotiable contract, cash availability, or habit? | A business might sell improved management arrangements alongside software: budgets, reserves, repair classes, emergency rules, preferred replacements. Changing a contract can create more value than better prompting. |
| The workflow is a fixed sequence | Which steps actually depend on each other, and which exist because systems or authority are fragmented? | Collect access preferences, check warranty, solicit available contractor windows, and prepare an owner choice in parallel when appropriate. Never fabricate agreement by another party. |
| Better triage solves maintenance | What constrains completion: diagnosis, contractor supply, funding, access, parts, capacity, quality, or coordination? | Select a product promise matching the controllable bottleneck. If contractor capacity dominates, software alone may disappoint; a service or supplier partnership may be the right business. |
| Judgment means an LLM must decide | Is this comparison, arithmetic, estimation, optimization, policy, or an open question? | Use exact calculations for balances and dates, policy checks for authority, optimization for scheduling, and models for interpretation or proposals. No architecture earns credit merely for being agentic. |
| More data is always better | What missing fact would change this decision? | Ask for one discriminating photo or question before ingesting a whole portfolio. Keep source time and uncertainty visible where they matter. |
| Automation percentage is the goal | What service result, at what total cost, is better? | Optimize completed work, avoided delay, fewer repeat visits, correct charges, or resident outcomes. A low-volume complex decision can be valuable; a high-volume automated notification can be worthless. |
| Current legal/process boundaries are permanent | Which constraints come from law, contract, policy, supplier capability, or custom? | Label each separately. Product innovation can change contracts, staffing, channel design, and delegated authority; it cannot simply ignore legal duties. |
| A comprehensive operating map is a comprehensive product specification | Which connected facts and actions are indispensable to one paid responsibility? | Use the broad map to select scope and discover side effects. Implement only the required slice, with clear interfaces to the rest. |

## 6. Practical design criteria without an oversized platform

For each chosen responsibility, the product must answer eight ordinary questions:

1. What has happened, and which property, person, asset, and commitment does it concern?
2. What result do we owe, by when, and what would count as completion?
3. What information is missing or contradictory?
4. What choices are available, and what do they cost in money, delay, and risk?
5. Who may choose, and what has already been authorized?
6. What action actually changes the situation?
7. How do we know the action succeeded, and what do we do if it did not?
8. What does the next responsible person need to know?

The minimum supporting implementation is correspondingly small: current records; pending obligations; explicit permissions; a few reliable actions; a visible history; and a way to resume or hand off unfinished work. Introduce additional modeling only when a real exception or second workflow needs it.

Do not equate an API success response with an operational result. A vendor may receive a dispatch and never accept. A payment request may be created and later fail. A resident may acknowledge an update while the leak continues. The useful state belongs to the underlying obligation, not only to a software task.

Security has a practical business meaning: one owner cannot read another owner's private information; a contractor receives necessary access details rather than the entire tenant history; a resident's email cannot instruct the assistant to alter owner policies; a mistaken retry cannot pay an invoice twice. These are design requirements, not a reason to build a generalized compliance product before solving the work.

## 7. Independent quantitative checks to put into the pilot

These are mathematical illustrations, not empirical estimates of property-management performance.

- **Serial reliability:** If twelve required actions independently succeed with probability 99% each, complete-chain success is `0.99^12 = 88.64%`. At 95% per action it is `0.95^12 = 54.04%`. Independence is only an illustration; shared outages and correlated interpretation errors change the result. Measure finished-case performance directly and build recovery.
- **Rare failures:** Zero critical failures in 200 independent representative cases leaves a one-sided 95% upper failure-rate bound of `1 - 0.05^(1/200) = 1.49%`. A short pilot cannot establish safety for rare emergencies. Use targeted tests of severe scenarios and an operating fallback; do not describe a zero-incident pilot as proof of universal reliability.
- **Time is not payroll:** A 10-minute reduction on 300 monthly cases is 50 hours of capacity. It becomes cash only if overtime, outsourced work, staffing needs, or another paid input actually fall; otherwise quantify redeployment and improved service separately.
- **Coordination versus total delay:** Removing 30 minutes of staff handling from a five-day contractor wait may be valuable labor relief and barely change resident resolution time. Conversely, a two-minute follow-up that prevents a missed appointment may produce substantial elapsed-time value. Record both.
- **Provider contribution per case:** `service revenue - model/tool cost - provider human review - provider exception handling - provider integration/support allocation - provider expected remediation cost`. Buyer value is not the provider's revenue. A wrong action with a 1% chance of a $1,000 recovery cost contributes $10/case to whichever party bears that cost, before any service harm. Do not use tiny inference cost as the total unit-cost estimate.
- **Buyer net value per case:** `benefit captured by buyer - service price - buyer internal residual cost`. Compare with the same baseline; do not subtract human work twice if the benefit already uses net labor savings. Property-owner gains that the PM cannot retain or charge for are not PM benefit captured.
- **Joint surplus per case:** `incremental value across affected parties - incremental real resource and loss costs across those parties`. Transfers such as the service price cancel when both payer and recipient are included. Count any owner or resident benefit separately and only once; joint value does not establish the buyer's budget or willingness to pay.

Recommended measurement fields: case type, property/segment, incoming channel, inclusion/exclusion reason, severity, current authority, start time, all human minutes, all vendor waits, needed facts, assistant proposals, rejected proposals and reason, actions attempted, actions acknowledged, objective completion, reopened work, financial outcome, resident complaint, and fully loaded operating cost. Log absent or abandoned cases, not just successes.

Compare against both today's practice and a simpler alternative such as existing software configuration, templates, standing owner approvals, or better staffing. Randomize comparable low-risk cases when feasible; otherwise use matched properties or a staged rollout and clearly state causal limits. An initial test can establish feasibility and unit economics without pretending to prove seasonal retention effects.

## 8. Business thesis implications

The best first product is unlikely to be selected by asking what percentage of a property manager's job AI can do. Select it by finding a recurring responsibility for which the current division of work causes expensive delay, repeated chasing, inconsistent choices, or avoidable mistakes—and for which a new company can reliably own more of the result.

Three ways to deliver value through the partnership remain live until customer work resolves them:

- **Software:** The buyer can supply competent staff, authority, clean-enough records, and contractor capacity; the missing piece is execution support.
- **Managed operation:** Customers want a completed responsibility and will pay for a mix of software and exception-handling staff. The company must price the real human workload and avoid unlimited bespoke service.
- **Redesign the partner's operation:** Work with the existing property-management partner to improve owner agreements, service promises, staffing, delegated authority, and supplier arrangements where these cause the bottleneck. The partner retains its management business and accountable role; changes to obligations and authority require its agreement and appropriate legal review. Evaluate the resulting economics for both parties before expanding the service.

No source here establishes which is best for Owen. The evidence supports a method of choosing: broad operating map, specific bottleneck, observed responsibility, measured alternative, clear buyer benefit, and a small paid test. The public research should widen the possibilities and sharpen the tests; it should not appoint the product.
