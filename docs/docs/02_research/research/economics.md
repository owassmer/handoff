# Property-management economics: what the public data supports

Research date: 15 September 2026. This note separates published observations, independent descriptive calculations, and hypothetical business cases. It is a decision rationale and reproducible analysis, not a transcript of private reasoning.

## Findings that should change the company thesis

1. **A property manager is not always the economic beneficiary.** Preventing a repair, recovering rent, or reducing vacancy primarily benefits the owner. A third-party manager normally receives only the contractual share of additional revenue; expense savings may produce no immediate manager revenue. A product can have excellent property-level economics and still be hard to sell to the manager.
2. **“Number of properties” is an especially bad proxy for sales opportunity.** Our calculation from the Census public file finds that one-unit properties constitute approximately 83% of properties but 31% of units. Owners, management companies, properties, buildings, units, leases and households are separate populations. No credible customer count follows merely by dividing units by an invented average portfolio.
3. **Vacant-unit work has an observable outcome but relatively low frequency.** At published large-operator turnover rates, 1,000 units generate roughly 19–31 turnover cases a month, before eligibility exclusions. A repair coordination business and a turn coordination business have different throughput, staffing and prices.
4. **The hard economic question is whether a better decision changes a real outcome.** Earlier readiness is not automatically earlier rent. Fewer calls are not automatically fewer paid hours. A lower invoice is not a saving if repair quality falls or the work simply occurs next month.
5. **AI adoption reports identify demand and an implementation gap, not technical limits.** Current full-process automation rates say little about what can be achieved after changing authority, contracts, process and information collection. They also do not prove that any new product will succeed.

## The market denominators

| Measure | Current anchor | Correct use | Incorrect inference |
|---|---:|---|---|
| US renter-occupied units | 46.827m, Q2 2026; 90% margin of error ±0.580m | Scale of occupied rental housing | Number of professionally managed homes, customers or properties |
| US rental vacancy rate | 7.3%, Q2 2026; 90% margin of error ±0.2 percentage points | Macro context | A target portfolio's controllable vacancy or potential product impact |
| Median asking rent for vacant units | $1,531/month, Q2 2026 | Asking-rent context for vacant stock | Average rent actually collected from all occupied units |
| BLS broad manager occupation | 460,400 jobs in 2025; median wage $69,990/year or $33.65/hour | Labor-market anchor | PM-company count or wage of every worker involved in a workflow |

Sources: [Census Q2 2026 HVS release](https://www.census.gov/housing/hvs/files/currenthvspress.pdf), [BLS occupation profile](https://www.bls.gov/ooh/management/property-real-estate-and-community-association-managers.htm), updated August 27, 2026. The BLS employment count includes residential, commercial and community-association work and self-employed workers; its wage estimate excludes self-employment income. Employer benefits and overhead are additional; use actual role costs in a pilot. The $45/hour model input is an assumption, not a BLS observation.

The HVS release gives rental vacancy rates of 5.9% Northeast, 6.9% Midwest, 9.5% South and 5.3% West. These broad differences support geographic segmentation, not choosing a market by vacancy alone. Local demand, rent levels, vendor density, authority, product competition, landlord obligations and customer access jointly determine suitability.

The US anchors are an initial measurement choice, not the product boundary. For example, England's 2024 official landlord survey reports 45% of its direct-landlord respondents own one property, while the 17% with five or more own 49% of tenancies. The report explicitly excludes agent-registered landlords from its weighted findings; it should not be promoted to a full market estimate. This is the same distribution problem in a different operating and legal setting. [English Private Landlord Survey](https://www.gov.uk/government/statistics/english-private-landlord-survey-2024-main-report/english-private-landlord-survey-2024-main-report).

Commercial, mixed-use, community associations, social housing, student housing, senior housing and short stays need separate denominators. Residential-unit counts cannot price an office building's equipment management or an association's common-area work. The [EIA commercial-building dataset](https://www.eia.gov/consumption/commercial/data/2018/index.php) is a relevant source for building systems/energy segmentation; its historical counts were not combined with residential units here.

## Independent Census microdata analysis

### Inputs and verification

Downloaded the [2024 RHFS public CSV](https://www2.census.gov/programs-surveys/rhfs/data/public-use-files/2024/rhfspuf2024.csv) and [codebook](https://www2.census.gov/programs-surveys/rhfs/data/public-use-files/2024/Codebook-Version-1.pdf). The 4,425 property records are weighted with `WEIGHT`; unit counts use `WEIGHT × NUMUNITS_R`. All five property-size and unit-size totals reproduce the Census [microdata verification workbook](https://www2.census.gov/programs-surveys/rhfs/technical-documentation/help-guides/2024/2024-RHFS-Microdata-Estm-4-User-Verification.xls) to its reported rounding. The script performs these assertions on every run.

Limits that matter:

- The survey was collected in 2024; financial questions concern calendar 2023. Its frame excludes public and transient housing and lacks newly built properties after late 2020. These are structural observations, not a fresh census of the September 2026 market. [Census methodology](https://www.census.gov/programs-surveys/rhfs/technical-documentation/methodology.html).
- `NUMUNITS_R` uses disclosure-modified components. The public file totals 49.895m units, while the published pre-disclosure unit controls total 49.722m. The public-file result agrees with Census's verification workbook; neither is silently substituted for the other. [Topcoding documentation](https://www2.census.gov/programs-surveys/rhfs/technical-documentation/help-guides/2024/2024-RHFS-Microdata-Topcoding).
- The codebook's introductory record count says 6,424, but the downloaded data, verification workbook and current methodology agree on 4,425. We use the verified file, not that introductory statement.
- These are descriptive weighted point estimates. No sampling confidence intervals have been estimated in this analysis; do not infer statistically significant differences from small gaps. Replicate weights are retained in the raw file for subsequent formal inference. Missingness and disclosure modification are additional limitations that confidence intervals would not fix.
- Census corrected occupancy-rate processing in March 2026. This analysis does not use those occupancy variables. [Correction notice](https://www.census.gov/programs-surveys/rhfs/news-and-updates/updates/2024-PUFs-and-tablCreator.html).

### Who manages the properties?

| Day-to-day manager | Weighted properties | Share of properties | Weighted units in public file | Share of units |
|---|---:|---:|---:|---:|
| Owner or unpaid agent | 10.13m | 53.4% | 16.51m | 33.1% |
| Manager directly employed by owner | 2.79m | 14.7% | 11.00m | 22.0% |
| Management company | 4.09m | 21.6% | 17.61m | 35.3% |
| Other | 1.02m | 5.4% | 1.41m | 2.8% |
| Not reported | 0.93m | 4.9% | 3.36m | 6.7% |

Source: our weighted calculation from the [RHFS public file](https://www2.census.gov/programs-surveys/rhfs/data/public-use-files/2024/rhfspuf2024.csv), category definitions from codebook p.59. “Management company” does not prove independence from the owner; the survey does not establish the commercial contract or ultimate affiliation. The 4.09m figure counts managed properties, **not management companies**.

For 50+ unit properties, management companies account for approximately 52% of public-file units and directly employed managers for another 32%. For one-unit properties, the corresponding figures are 22% and 16%. This supports different distribution approaches: direct sales to owner-operators; sales to fee managers with demonstrated manager-level savings; or a product distributed through managers but economically purchased by owners.

### Expense data: why the denominator must travel with the headline

| Annual cost per unit, 2023 | Median with property weights | Median with unit weights | Valid-response records | Weighted share of all properties with a valid response |
|---|---:|---:|---:|---:|
| Maintenance and repair | $1,600 | $1,175 | 1,495 | 46.9% |
| Management-company expense | $1,300 | $720 | 989 | 18.1% |
| Insurance | $1,000 | $760 | 1,501 | 48.2% |
| Payroll | $0 | $963 | 1,016 | 16.9% |
| Operating expenses excluding tax | $4,328 | $4,467 | 1,724 | 56.9% |

Source: independent calculation from the same [RHFS public file](https://www2.census.gov/programs-surveys/rhfs/data/public-use-files/2024/rhfspuf2024.csv); variables `OPREP`, `OPMNG`, `OPINSUR`, `OPPAY`, `OPEX_R`. Each row uses only nonnegative responses for that item; “not applicable” and “not reported” are excluded, never treated as zero. Medians of per-unit property expenses are weighted first by property, then separately by units. These are different questions. They are not a cost waterfall: medians have different valid-response sets and cannot be added. Total OPEX is a Census recode and should not be treated as proof that every expense component was supplied.

**Interpretation:** maintenance is financially material, but the data does not estimate avoidable maintenance, coordination labor, repair frequency, or AI savings. The property-weighted zero payroll median is not evidence that the operating work is free: owner effort, external managers and contractors may perform it. The low reporting fraction for management expenses makes “average fee” extrapolation especially unsafe.

## Observed operator data and the turn-frequency constraint

| Operator and period | Published observation | Implication for a hypothetical 1,000-unit portfolio |
|---|---|---|
| Invitation Homes, FY2025 | 22.8% annual same-store turnover; 76,819 same-store homes; 96.8% average occupancy | 228 annual turns, or 19/month if spread evenly |
| AvalonBay, H1 2026 | 37.2% annualized same-store turnover; Q1 annualized 31.7%, Q2 annualized 42.6% | 372 annualized turns, or 31/month at that half-year run rate |

Sources: [Invitation Homes release](https://www.businesswire.com/news/home/20260218809149/en/Invitation-Homes-Reports-Fourth-Quarter-and-Full-Year-2025-Results), [AvalonBay filing, Attachment 3](https://investors.avalonbay.com/sec-filings/all-sec-filings/content/0000915912-26-000018/q22026ex-992.htm). AvalonBay's metric excludes third-party-managed communities. These are specific portfolios with different geography, building types and operating models; they do not establish an industry range. Seasonality makes evenly spread monthly counts a planning approximation.

The constraint is practical. A 30-day test at a 200-unit customer might observe only a handful of turns. It can test integration, approval and coordination, but cannot credibly establish a stable rent-recovery effect from such a sample. Either combine several properties, extend the period, or use more frequent maintenance decisions for the first test.

AvalonBay reports FY2025 same-store residential revenue of $2.712bn and operating expenses of $851.659m, implying a 68.6% NOI margin before excluded corporate, financing and other items. That is not owner cash profit. Its definitions also use a 2.5% management-fee assumption for disposition underwriting. That specific institutional convention is not an observed small-manager fee. [AvalonBay FY2025 release and definitions](https://investors.avalonbay.com/news-events/press-releases/detail/434/avalonbay-communities-inc-announces-2025-operating-results-1-7-dividend-increase-and-initial-2026-outlook).

This is why rent-dollar graphics and property EBITDA should not be mixed: NOI, debt service, capital spending, distributions and PM-company profit measure different things. An AI company must identify the spending pool it can reduce and the customer entitled to that reduction.

## Explicitly hypothetical economics

These inputs illustrate which variables matter; they are not recommended pricing, observed demand or validated product returns.

### General work-item case

Assume 1,000 units, 0.30 incoming items/unit/month and 70% eligibility: 210 eligible items/month. Net PM time saved is 20 minutes/item; loaded labor is $45/hour; 50% turns into realizable economic value. Assume $20 owner expense saving and $10 incremental collected rent per item; neither effect is yet proven. The PM fee is 8% of the rent increase only. The illustrative price is $1,000/month + $5/item = $2,050/month.

| Monthly outcome | Third-party manager pays | Integrated owner-operator pays |
|---|---:|---:|
| PM capacity value before realization | $3,150 | $3,150 |
| Realizable labor value | $1,575 | $1,575 |
| Gross owner operating benefit | $6,300 | $6,300 |
| Benefit captured by buyer, before price | $1,743 | $7,875 |
| Product price | $2,050 | $2,050 |
| Buyer net benefit | **−$307** | **$5,825** |

The third-party manager captures only $168 of the owner revenue uplift; it captures none of the assumed expense savings. The integrated buyer captures all of the operating effect, with internal fees cancelling. If the owner savings are not demonstrated, the integrated case also becomes negative: $1,575−$2,050=−$475/month.

This does not imply that integrated ownership is required. A fee manager can sell the service to owners, charge an agreed coordination fee, share verified savings, or buy based on demonstrable staffing capacity. Those are different commercial arrangements and must be validated in actual agreements. Do not present the owner's benefit as the manager's ROI.

### Provider costs and the exception tail

Assume provider labor at $35/hour; 3 routine human minutes/item; 15% of items need 20 additional minutes; model/comms cost $0.50/item; support costs $400/month; and 20 implementation hours at $50/hour are amortized over 12 months.

- Average human handling is 6 minutes/item; total monthly delivery cost is $1,323; contribution is $727, or 35.4% of revenue, **before sales, general overhead and product development**.
- At 40% exceptions needing 40 extra minutes, average handling rises to 19 minutes and contribution becomes −$866/month.
- At this price and volume, reaching 60% contribution after the modeled support/implementation charges requires average human handling below about 1.9 minutes/item. That is a mathematical threshold under these assumptions, not a desired safety limit.

Cheap model tokens do not make an operations business cheap. Count founder time, on-call interruptions, customer-specific exceptions, vendor follow-up and failures. If the economics work at 35% contribution with repeatable operations, it may still be a worthwhile service company; there is no need to pretend it is immediately high-margin software.

### Turn-only case

This is the active scenario in the companion workbook; the higher-volume general work-item scenarios above remain separate contrasts. Assume 35% annual turnover: 29.17 turns/month per 1,000 units, with every turn eligible. Save 60 PM minutes/turn at $45/hour with 50% realization. Recover 3 actual paid-rent days at $2,000/month and a 30-day convention: $200 owner revenue/turn. No repair-cost saving is assumed. A **$100/turn test quote with no monthly base** produces $2,916.67/month revenue. This is a price hypothesis to test, not an observed market quote or recommended price.

| Monthly outcome | Third-party manager pays | Integrated owner-operator pays |
|---|---:|---:|
| Realizable PM labor value | $656.25 | $656.25 |
| Buyer operating benefit before price | $1,122.92 | $6,489.58 |
| Product price | $2,916.67 | $2,916.67 |
| Buyer net benefit | **−$1,793.75** | **$3,572.92** |
| Buyer benefit / price | 0.385× | 2.225× |

Provider handling is 20 routine minutes/turn plus 25% of turns needing 60 extra minutes: 35 minutes/turn on average. Provider labor is $35/hour; model/comms cost $2/turn; monthly support is $400; implementation is 20 hours at $50/hour spread over 12 months. Total delivery cost is **$1,137.15/month**, leaving **$1,779.51 contribution, or 61.01%**, before sales, company overhead and product development. Variable delivery cost is $22.42/turn; the allocated total at this volume is $38.99/turn.

The conditional price bounds matter more than the test quote. Under these assumptions, the provider breaks even at $38.99/turn and earns 60% contribution at $97.47/turn. The third-party PM captures only $38.50/turn before price, while an integrated buyer captures $222.50/turn. There is effectively no economic room for a third-party PM buyer under this assumed delivery model without a different fee arrangement, materially lower service cost, or additional demonstrated benefit. The integrated case has room only if the assumed value occurs.

At the $100/turn quote, an integrated buyer needs **1.1625 additional collected-rent days per turn** to break even after the assumed labor benefit. If faster readiness does not advance paid occupancy, buyer net value is **−$2,260.42/month**. Three days of faster work followed by three extra days waiting for a tenant create no recovered rent. “Rent-ready” time is a useful operational measure; economic value must be measured through occupancy and collected rent while adjusting for concessions and quality. Do not price from these ceilings before validating both benefit and delivery cost.

## What the adoption research does and does not establish

Buildium's public report page says AI use rose from 20% to 58% between its 2024 and 2025 surveys, while 8% of companies fully automated any process. Its blog reports 75% planned growth versus 55% who grew, 56% of owners hiring managers for maintenance help, and maintenance/responsiveness featuring in renters' stated renewal preferences. [Report page](https://www.buildium.com/resource/2026-property-management-industry-report/), [survey discussion](https://www.buildium.com/blog/2026-property-management-industry-trends/).

Use these as hypotheses for customer discovery. This is vendor-sponsored, self-reported research; the public pages do not establish a probability-sample estimate, causal retention lift, or willingness to pay for this product. Stated intention to renew is not an observed renewal. The “8%” finding is not evidence that 92% of processes are technically impossible to automate, nor that there is a 92% market waiting to buy.

## How to measure the first deployment

1. **Specify the decision and population.** Define an eligible item before seeing its outcome. Keep emergency exclusions, declined cases, cancellations and incomplete cases in the denominator; report each separately.
2. **Separate effort from elapsed time.** Collect actual staff touch time, number of follow-ups, approval wait, vendor wait, parts wait, access wait and physical work. A quicker AI answer may leave the critical delay untouched.
3. **Use a concurrent counterfactual.** Randomly allocate eligible cases where practical; otherwise stagger rollout across comparable properties. Control for property, season, issue severity, vendor, lease status and scope. Do not compare one unusually bad pre-period with a cleaner pilot month and call the whole difference impact.
4. **Measure total cost through recurrence.** Include quoted and final invoice amounts, repeat visits, reopened work, related follow-on repairs, temporary accommodation, concessions, overtime and product fees. Track 30/60-day recurrence as appropriate to the job; long-lived equipment needs longer follow-up.
5. **Measure residents' outcomes.** Time without essential service, missed visits, disruption, unresolved complaints, accessibility needs and repeat contact matter alongside owner dollars. An unanswered request quietly closed is a failure, not saved workload.
6. **Measure actual authority.** Log what the product proposed, what could be done under delegated limits, what needed approval, what was changed, what happened and whether the result met the agreed standard. This is ordinary operational accountability; no special document ceremony is needed.
7. **Measure the provider too.** Record all human minutes, model/comms cost, implementation labor, support time, failed integrations and recovery. Retained intervention categories should guide the next product iteration.
8. **Predefine success and failure.** Agree on a minimum worthwhile effect relative to the customer's baseline and economics; inspect uncertainty, not only averages. Stop or redesign if the work merely moves to a different employee, reductions depend on deferred necessary maintenance, or the proposed buyer cannot capture enough value.

Simple illustrative sample-size check: if cycle-time standard deviation is 5 days and the minimum effect of interest is 2 days, a conventional two-group 80%-power/5%-two-sided calculation gives roughly 98 cases per group: `2×(1.96+0.84)^2×5^2/2^2`. This is an approximation before clustering, skewness or repeated-property effects, which may increase the requirement. A 20-case pilot is suitable for operational learning, not a precise causal claim.

## The next evidence to obtain

Public data establishes scale and segmentation; it does not settle the product. The most decision-useful new corpus is a bounded, consented export from candidate customers: recent maintenance requests and turns, contracts/approval limits, timestamps, scope/quotes/invoices, staff effort, outcomes and recurrence. Inspect a representative sample including difficult cases before designing integrations. Ask who owns the budget and whether the proposed charge is permissible under their owner agreements.

Compare at least three candidate improvements against the same baseline: automate today's follow-ups, change approval/delegation rules, and redesign the service itself. The best answer may be a smaller amount of AI plus a better approval rule, or a fully managed service with software underneath. Do not force every improvement into a SaaS feature.

Files: `economic_calculations.py` reproduces `economic_outputs.json` and `public_data.csv` from `rhfspuf2024.csv`. `rhfs_verification.xls` and `Codebook-Version-1.pdf` support audit. Raw data SHA-256 is stored in the JSON. None of the modeled savings is an observed AI treatment effect.
