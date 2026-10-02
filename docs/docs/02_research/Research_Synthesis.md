# Research synthesis and decision record

**Property-management business design | Research cutoff: 15 September 2026**

This document explains the evidence, assumptions, alternatives and tests behind the playbook. It provides an inspectable analytical record, not a raw internal reasoning transcript. The detailed source reviews, operating tables, raw public data and calculations accompany it.

## 1. The question and the research boundary

The question is not how much of today's property-manager job can be replaced. It is **which recurring property outcome a new company can improve enough to earn a sustainable fee, and what division of people, software, authority and physical work makes that possible**.

The work proceeded across the full operating model before narrowing the proposed first offer. It covers ownership and management mandates; marketing and occupancy; physical assets and work; money; obligations and disputes; people, vendors and systems; ordinary operation, changes, failures and exit. Residential, commercial, associations, affordable housing, student/shared housing and hospitality differences are explicit.

The quantitative depth is greatest in US residential rentals. UK commercial standards, English landlord data and US federal/state/local requirements provide useful comparisons and scope checks. This is a systematic broad research corpus, not a claim to have enumerated every supplier, jurisdiction or individual decision in world property markets. Local operating rules still require actual contracts, program details, buildings and current law.

### What was examined

- All three supplied attachments, including the complete 13-page strategy review and 12-page McKinsey PDF with exhibits; both linked articles in full.
- An inventory of 38 entries (37 current providers and one acquired product lineage), across PMSs, AI, maintenance, inspection, payments, accounting, deposits, compliance, commercial operations and associations, supported by 75 opened primary-source pages with access/pricing limits.
- Nine cross-industry primary research records with populations, methods, observed results and transfer limits; source tracing for the Forbes statistics.
- The 2024 Census Rental Housing Finance Survey public microdata: 4,425 property records, survey-weighted calculations, codebook, methodology and official verification controls.
- Current Census rental-market statistics, BLS labor context and operator-reported turnover/operating results. These measures retain their different populations and dates.
- A 115-decision inventory across 17 families, with explicit alternatives, authority, execution, dependencies and validation questions. Counts describe the work performed; they do not measure commercial importance.

No operator interviews, vendor quotes, authenticated PMS trials or live customer experiments were conducted. The attached playbook's private correspondence summaries were considered as supplied context, not independently authenticated as a complete case record. No customer demand or improvement is represented as observed.

## 2. What survives from the supplied material

The original playbook's strongest insight is that useful software can coexist with a fragmented experience. Its CBS examples distinguish a continuing household from a vacant-unit turn and show that one problem can cross maintenance, accounting, resident-controlled information and a utility. Those are useful distinctions. They do not show how frequently the same problem occurs elsewhere or who would pay to change it.

The strategy review adds commercial urgency but overstates what follows. It calls the selected experience representative, treats limited full-process adoption as a technical frontier, elevates deposit administration before comparing the full business, and supplies prices/margins/revenue milestones without operating measurements. The new playbook retains concurrent research, building and selling while removing those unsupported conclusions.

McKinsey's supplied paper supports connected workflows and explicit attention to who captures value. Its forecast covers real estate, construction and development, not a property-management software market. Its technical-potential diagrams are modeled combined-sector work hours. Its client improvement examples lack the disclosed cohorts and comparisons needed to forecast a new product's effect. Page 4 allows some judgment work to become controlled repeatable work; the simple steps-versus-thoughts slogan should not become a fixed design constraint.

Palantir provides a useful pattern: link relevant facts, evaluation methods, authorized action and the subsequent result. The central Onyx example is fictional. This supports a design principle rather than proof of a particular architecture's ROI. A small operation can apply the pattern with a modest database, calculations and reliable interfaces. [Palantir article](https://blog.palantir.com/connecting-agents-to-decisions-277dee8ddb40).

### Consequential source corrections

| Claim | What inspection established | Decision consequence |
|---|---|---|
| 8% of firms fully automated a process means a structural automation ceiling | It is a vendor survey adoption measure, alongside 58% reporting AI use; the combined 3,200+ research respondents include managers, owners and renters | Do not infer task capability, 92% addressability or a permanent services niche |
| 8.6% renewal uplift supports residential AI economics | The primary paper concerns willingness to renew in observational office-tenant data | Exclude from residential treatment-effect assumptions |
| 23% retention, 28% training, 85% investor expectation | The inspected source chains did not substantiate these as usable empirical estimates; training also changes measure/denominator between articles | Exclude from demand and savings calculations |
| Broad read/write API access is available from an AppFolio Plus subscription | Public pricing describes the customer API as read-only; partner access is a separate question | Validate exact operations before committing to a product design |
| A manager can simply place an outside service under its license | Authority and licensing/exemptions are action- and jurisdiction-specific | Do not turn a service contract into a claimed legal exemption |
| Colon v. Martin supports deposit remedies | The cited case concerns municipal pre-action examinations | Remove the erroneous case citation; establish applicable statutory rules directly |

Sources: [Buildium report](https://www.buildium.com/resource/2026-property-management-industry-report/), [Hu/Kok/Palacios](https://link.springer.com/article/10.1007/s11146-025-10043-6), [AppFolio pricing](https://www.appfolio.com/pricing), [Virginia exemptions](https://law.lis.virginia.gov/vacode/title54.1/chapter21/section54.1-2103/), [Colon v. Martin](https://www.nycourts.gov/reporter/3dseries/2020/2020_02681.htm). The full audit supplies each intermediary source and the remaining uncertainty.

These errors matter because they alter product selection and economics. A large penalty does not establish incidence, avoidability or willingness to pay. A cited percentage with a different population cannot be used as a shortcut to expected returns.

## 3. The operating model changes the unit of analysis

The appropriate unit is often an **obligation or outcome that joins several decisions**, not a message, work order, resident or building alone. A unit and an agreement do not have the same lifecycle; several residents can share one agreement, and a physical system can serve several units. One incident can generate several jobs and financial consequences. One job may satisfy only part of a resident's problem.

The detailed map makes seven concurrent lifecycles explicit and separates four flows: physical use/work, money, authority/obligations, and information/commitments. It includes takeover, normal service, renewals, disputes, casualty, insolvency, management change and residual duties after exit.

The decision register is organized around what managers actually choose. It does not assume managers personally hold every right. For each item it asks who may recommend, decide, act and verify; those may be different parties. Sources anchor operating and legal domains; the proposed automation modes are original hypotheses requiring validation.

### What changes across property segments

| Segment | What becomes central | Why a single generic workflow fails |
|---|---|---|
| Scattered homes | Travel, heterogeneous assets, many owners, outsourced trades | Building-level staffing and equipment assumptions do not hold |
| Conventional multifamily | Shared systems, onsite teams, frequent leases and service | A unit issue can affect common infrastructure and other occupants |
| Student/shared housing | Beds, guarantors, changing participants, synchronized dates | A household change is not necessarily a vacant-unit turn |
| Affordable/program housing | Eligibility, assistance, recertification, program inspections | Standard private-rental terms and decision rights may not apply |
| Office/retail/industrial | Negotiated obligations, expense recovery, service standards, tenant improvements | A residential rent/deposit model omits major commercial decisions |
| Associations/co-ops | Boards, voting, reserves, assessments and common property | The payer and decision-maker are collective; owner/tenant roles overlap |
| Hospitality/specialist use | Short stays, bookings, staffing, operator-specific services | Property and hospitality/care operations must be separated |

The map should remain broad even when the product is narrow. It reveals side effects and expansion possibilities; it does not require implementing every relationship in software.

## 4. Independent public-data analysis

### Method

The calculation uses the Census 2024 RHFS public CSV, `WEIGHT` for properties and `WEIGHT × NUMUNITS_R` for units. It reproduces official property-size and unit-size verification totals to the published rounding. The included script records the raw-file SHA-256, checks controls and produces the analysis tables.

The financial reference year is 2023. The frame excludes public/transient housing and newly built properties after late 2020. Public-use disclosure modifications affect the unit count; the public-file total is approximately 49.895 million versus 49.722 million in pre-disclosure controls. The former agrees with the public-file verification workbook. These are descriptive point estimates, without newly calculated sampling intervals. See [Census methodology](https://www.census.gov/programs-surveys/rhfs/technical-documentation/methodology.html), [public CSV](https://www2.census.gov/programs-surveys/rhfs/data/public-use-files/2024/rhfspuf2024.csv), and [verification file](https://www2.census.gov/programs-surveys/rhfs/technical-documentation/help-guides/2024/2024-RHFS-Microdata-Estm-4-User-Verification.xls).

### Market structure

| Property size | Share of represented properties | Share of public-file units |
|---|---:|---:|
| One unit | 82.9% | 31.5% |
| 2-4 units | 14.6% | 15.4% |
| 5-24 units | 1.7% | 8.2% |
| 25-49 units | 0.4% | 5.4% |
| 50+ units | 0.4% | 39.4% |

| Day-to-day manager | Share of represented properties | Share of public-file units |
|---|---:|---:|
| Owner or unpaid agent | 53.4% | 33.1% |
| Owner-employed manager | 14.7% | 22.0% |
| Management company | 21.6% | 35.3% |
| Other | 5.4% | 2.8% |
| Not reported | 4.9% | 6.7% |

These calculations show why property counts, unit counts and buying-company counts must stay separate. A manager can aggregate many scattered properties; a large property is not necessarily a large independent buyer. The management-company category does not establish whether the company is affiliated with the owner. Neither table provides a customer list, reachable budget or automatic TAM.

### Expenses and missing data

Among valid nonnegative maintenance-and-repair responses, the property-weighted median annual cost per unit is $1,600 and the unit-weighted median is approximately $1,175. Only 46.9% of the weighted property population has a valid response for that item. These are conditional descriptive figures, not industry-wide savings potential.

Management-company expense has a valid-response share of only 18.1%. The corresponding medians are $1,300 and $720 per unit annually. They cannot be treated as a general quoted management fee. Missing and not-applicable values are excluded separately, never converted to zero. Medians across expense categories have different response populations and cannot be summed into a cost waterfall.

**Business inference:** maintenance is a material expense and the payer structure is diverse. **Not established:** how much spending is avoidable, how often coordination causes it, or what Handoff could capture. The economic memo and workbook retain these distinctions alongside the raw data.

## 5. Current competitive reality

Core platforms and specialists now advertise execution, not just records. AppFolio, Yardi, RealPage, MRI and Entrata position agents across operations; EliseAI spans substantial resident and maintenance work. Maintenance specialists extend into cost checks, scheduling, procurement and physical service networks. Financial and deposit specialists cover other proposed entry points.

The inventory establishes **documented coverage**, not actual performance. Recent announcements are distinguished from verified availability. Published pricing is a dated snapshot; quote-only offerings remain quote-only. Supported integration must be checked at the operation and permission level.

This changes the hypothesis from “nobody has built the connective software” to “can we serve a specific customer's operating need better than its feasible alternatives?” The latter can support a business in a competitive category, but requires direct comparison.

Sources and granular observations are in the provider inventory and opened-page audit. Particularly important comparisons include [Property Meld cost support](https://propertymeld.com/truecost/), [LeadSimple workflows/pricing](https://www.leadsimple.com/pricing), [Lula](https://lula.life/property-managers), [Lessen](https://www.lessen.com/), and [EliseAI implementation requirements](https://support.meetelise.com/hc/en-us/articles/39887009308301-Getting-Started-with-MaintenanceAI). A properly configured existing product is a real competitor, not a control group we are allowed to keep artificially weak.

[Vendoroo](https://www.vendoroo.ai/) is an especially close service comparison because it uses the customer's vendors and markets human support and owner-approval handling. APM Help, OJO and Proper strengthen the financial-operations comparison. Conservice and Second Nature illustrate utility and resident-service alternatives. Their coverage does not prove that any particular deployment solves a customer's problem, but it removes easy claims of category novelty.

## 6. Why turn readiness is the lead test, and why it can lose

The broad company thesis is to operate a recurring property responsibility with AI and a smaller amount of necessary human coordination. The lead test is vacant-home readiness because it combines an understandable result, observable condition/date, a bounded cohort, several consequential choices and owner-level economic stakes.

It is not objectively established as the best lane. Occupied maintenance is more frequent; takeover projects may have stronger urgency and immediate budgets; financial operations have a recurring established buyer; commercial obligations may support larger fees. Expertise and competitive objections apply to **all** of these, including turns. Physical inspection, contractor management and habitability obligations are not trivial merely because a founder can build the software.

| Candidate | Condition that would make it beat turns | Measurement needed |
|---|---|---|
| Occupied maintenance | Frequent avoidable repeated visits/approval delays; turns mostly wait on demand | Eligible volume, preventable cost, completion quality and buyer capture |
| Takeover/onboarding | Partner grows through repeated acquisitions or management assignments | Event cadence, implementation cost, errors prevented and purchase budget |
| Month-end/financial operations | Controller owns painful recurring work and a capable finance partner is available | Reconciliation burden, error cost, close timing, trust controls and alternative quote |
| Commercial obligations | Accessible specialist/operator with collectible contractually supported value | Actual lease sample, repeatable obligations, cycle length and net recovery |
| Existing-stack implementation | Needed functions already work once configured; no ongoing delivery gap | Setup effort, useful transfer and whether recurring service is actually necessary |

The first discovery week therefore compares real work across domains before contracting a turn pilot. This preserves a clear lead hypothesis while allowing evidence to select another business.

### The strongest counterthesis

Turn coordination could be a low-volume service whose apparent value comes from rent gains that never materialize. Skilled trades, capital or rental demand may dominate the timeline. An existing coordinator with standing approvals may perform just as well. Native vendors and operated services may already cover the relevant segment at lower cost. If so, AI adds another layer of supervision rather than removes work.

The response is not a more elaborate system. Test the actual critical path, compare the best alternatives, and require enough practical control to improve the outcome. Do not guarantee a date while lacking access, vendors, funding or authority. A pilot can initially promise specific controllable service actions and report the complete outcome; any later performance guarantee should match demonstrated control and contractual allocation.

## 7. Economics that can falsify the recommendation

The live workbook uses one clearly labeled **illustrative turn scenario**. None of its savings or prices is an observed customer result.

| Input | Assumption |
|---|---:|
| Portfolio and turnover | 1,000 units; 35% annual turns; all eligible |
| Monthly case volume | 29.17 turns |
| Net manager time released | 60 minutes/turn at $45/hour |
| Cash realization of released time | 50% |
| Additional collected rent | 3 days/turn at $2,000 monthly rent, using 30 days |
| Avoided repair expense | $0 |
| Service price | $100/turn; no recurring base fee |
| Handoff human work | 35 minutes/turn, including assumed exceptions |
| Handoff labor and variable tools | $35/hour; $2/turn |
| Account support and setup allocation | $400/month plus $1,000 setup spread over 12 months |

| Monthly result | Integrated owner-operator | Third-party fee manager at 8% |
|---|---:|---:|
| Benefit captured before service price | $6,490 | $1,123 |
| Service price | $2,917 | $2,917 |
| Buyer net benefit | **$3,573** | **-$1,794** |

Handoff's modeled monthly delivery cost is $1,137 and contribution is $1,780, or 61.0%, before acquisition, central overhead and product development. The direct break-even price is $38.99 per turn; a 60% contribution target under these assumptions requires $97.47. These are algebraic thresholds, not market prices or validated margins.

**The crucial downside:** with no additional collected-rent days, the integrated buyer loses approximately **$2,260 a month** at the same price. With no repair savings, the integrated buyer needs about **1.16 genuinely additional paid days per turn** to break even. A fee manager capturing only 8% of incremental rent needs approximately **14.53 days** under the same assumptions. This strongly favors an owner-funded budget or a different source of manager value; it does not prove that an owner will buy.

The separate general maintenance-work illustration in the economic memo is deliberately a different population: 210 eligible items/month rather than 29 turns, different handling/pricing, and explicit hypothetical expense savings. It is a comparison of business mechanics, not a second estimate of the same service. The workbook and script use identical assumptions for the turn example.

### Frequency and measurement

Invitation Homes' 22.8% FY2025 same-store turnover implies 19 monthly turns per hypothetical 1,000 homes. AvalonBay's 37.2% annualized H1 2026 turnover implies 31. These portfolios differ; the figures are not a statistically estimated industry range. They show why a small company's short pilot may have too few turns. [Invitation Homes](https://www.businesswire.com/news/home/20260218809149/en/Invitation-Homes-Reports-Fourth-Quarter-and-Full-Year-2025-Results), [AvalonBay](https://investors.avalonbay.com/sec-filings/all-sec-filings/content/0000915912-26-000018/q22026ex-992.htm).

A sample of 20-40 cases is useful for discovering workflow and unit-cost issues. It cannot establish a stable small causal effect or rare-failure safety. As a mathematical illustration, detecting a two-day average change with five-day standard deviation at conventional 80% power and 5% two-sided significance requires about 98 cases per group before clustering or other complications. The field guide separates feasibility, economics and later causal evaluation.

## 8. Cross-domain lessons that earn their place

The research corpus includes customer support, consulting, product development, office work, software maintenance, economy-wide labor adoption, clinical reasoning and building analytics. Positive and negative results both matter; older model studies are not permanent capability ceilings.

| Transferable lesson | Application here | What is not justified |
|---|---|---|
| AI can spread useful operating knowledge and reduce novice ramp time | Reuse successful diagnosis questions and well-founded decisions | Importing support-center productivity percentages into PM staffing |
| Capabilities vary by task; human-plus-AI can fail | Test repair options, permissions, invoice matching and escalation separately | A universal approval checkbox as proof of safety |
| Individual time savings need not change organizational output | Redesign approvals, staffing and dependencies, not only drafting | Counting faster email as payroll savings |
| Better analysis can cross departmental boundaries | Prepare a combined cost, timing and resident-impact decision | Assuming the model has physical expertise or contractual authority |
| Physical-system savings require action and verification | Link observed conditions to feasible repair and outcome checks | Claiming sensor-based energy savings for homes without those systems |
| Selection and self-report can mislead | Include failures, refused cases, rework and actual clocks | A successful demo or enthusiastic survey as proof of impact |

The primary-study table in the corpus records methods and limitations. It supports these evaluation choices, not the financial inputs. The most useful inheritance from Owen's projects is disciplined comparison and execution: reliable calculations, explicit applicability, source-aware interpretation, practical integration, and testing with real cases. The company should not inherit their vocabulary or architectural scope.

## 9. Recommendation changes and remaining tests

| Question | Evidence or analysis | Resulting decision | What would change it |
|---|---|---|---|
| Is software missing? | Broad current provider coverage and implementation documentation | Compete against feasible existing execution, not absent technology | A repeatable task with no adequate supported product/service |
| Is the residual work inherently human? | Adoption does not establish capability; task-level experimental variation | Separate ability, permission, observability, cost and preference | Measured model limits in the selected operating context |
| Should deposits lead? | Prior ranking not based on broad comparison; legal/source errors and active competition | Reopen all lanes; deposits remain one candidate | Actual volume, costly preventable failures and funded delegation |
| Who should buy? | Owner/manager value split and live economics | Prefer owner-operator or explicit owner-funded budget | Verified staffing/capacity gain makes fee-manager purchase work |
| What should be sold? | Feature competition; need for actual completion | A bounded operating result, with software behind it | Customers already supply execution and only need a tool |
| Why turns first? | Understandable result, connected choices, measurable cohort | Provisional lead test with broad first-week comparison | Demand-limited vacancy, low volume, insufficient control or better adjacent economics |
| How much should be built? | Integration/authority can dominate implementation | Small working slice through real permitted actions | Repeated customer use establishes need for broader shared capability |
| How should it scale? | Exception cost and repeated setup threaten service economics | Reproduce delivery with a second partner before expansion | Service cannot repeat profitably; remain a priced project business or stop |

## 10. Evidence still missing

The highest-value next evidence is private operating evidence obtained with permission: a consecutive case history, actual approval limits, installed modules and configuration, required read/write permissions, staff time, contractor performance, readiness and collection dates, and a real purchasing decision.

Public research cannot determine those facts. Specifically unresolved are: target customer willingness to delegate and pay; actual preventable delay; local supplier availability; integration costs and commercial access; role-specific labor costs; callbacks and quality; founder/operator execution capability; and customer acquisition cost. The operating map identifies what to ask for without presuming the answer.
