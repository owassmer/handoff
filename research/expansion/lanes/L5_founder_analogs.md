# L5 — Founder-first principles and cross-industry analogs for expansion

Lane: external, independent. Scope: how a two-person, AI-native team with a working first product should choose and sequence expansion, tested against companies in operations-heavy industries, then applied to Handoff.
Date: 2026-09-28. Evidence ledger: `L5.ledger.json` (58 sources, each with at least one verbatim quote attached).

---

## 1. Answer in one paragraph

Handoff should not expand yet, and when it does, the first expansion should deepen the product for the same buyer. The analogs are consistent on this. Companies that expanded well already had retained customers. They kept the customer the same and changed one thing at a time, usually by moving into that customer's money flows. ServiceTitan reported gross dollar retention above 95% before its IPO [15]. Toast and AppFolio now earn roughly three-quarters of revenue from payments and other value-added services [14][5]. Companies that expanded before the core worked, or that bet their balance sheet or labour costs on automation that had not yet arrived, failed. Homejoy, Olive and Bench expanded or automated ahead of a working core [30][9][12]. Atrium, Zillow Offers and Katerra bet on efficiency or forecasts they could not deliver [11][8][29]. So the order for these founders is as follows. (1) Prove the core with a few operators in one dense area, running move-outs as a priced service and measuring results. (2) Close the vacancy loop: move-in baseline, pre-move-out inspection, move-out, settlement, make-ready. Lead with settlement where the law makes deadlines costly (New York takes away the landlord's right to keep any part of the deposit after 14 days).[34] (3) Earn money on the funds that already pass through the workflow, through partners rather than by building payment rails. (4) Choose deliberately among three different company shapes: a software vendor to property managers, an AI-run operator of turnovers (up to buying a property manager), or an engine sold to platforms and deposit insurers. Moving the same capability into other industries (HOA, short-term rental, commercial lease exits) should wait. EliseAI crossed industries only after passing $100M ARR, and Olive died of spreading too wide.[6][9] The main risk to the premise is that move-out coordination is becoming crowded. AppFolio ships its own maintenance agents, and point tools already cover the path from notice to final ledger.[39][53] The durable asset may therefore be accountable settlement and money handling, not the coordination itself.

---

## 2. Findings: analog cases and the patterns they support or refute

### 2.1 Pattern A — Expansion follows a working, retained core. Expanding before it fails.

- **Startup Genome (2011).** In a dataset of more than 3,200 high-growth startups, premature scaling was the main cause of failure. 70% of the dataset showed it. Startups that scaled properly grew about 20 times faster.[44] Caveat: the data is self-reported and old.
- **Homejoy (home cleaning, 2015).** Only about 15–20% of customers booked again within a month, against more than 35% at rival Handy. Homejoy still opened 30 cities in six months after raising $38M. A former employee asked: "if your core business doesn't work here, why expand in new markets?"[30] This is the clearest home-services example of geographic expansion ahead of retention.
- **Olive AI (healthcare operations, 2023).** It was once valued at $4B and raised a $400M round in 2021. It cut about 450 staff in July 2022. The CEO cited "fast-paced growth and lack of focus". Olive then sold "the heart of" the business (clearinghouse and patient access) and shut down the rest.[9]
- **Eisenmann (HBR, 2021)** names "speed traps": a startup saturates its first market, broadens to new segments with different needs, and costs rise. He also says a lack of industry experience makes missteps more likely.[41]
- **Bain (Zook & Allen).** Seventy-five percent of growth initiatives fail. The winners expand a strong core into related markets with a "repeatability formula" that changes one variable at a time.[55][56]
- **Supporting counter-case.** ServiceTitan lands with a Core product and expands into Pro products and FinTech. It reported gross dollar retention above 95% and net dollar retention above 110% for ten quarters in a row.[15] Expansion there rode on retention that was already proven.

- **Flexport (logistics, 2023)** cut about 20% of staff. CEO Ryan Petersen tied the path to profitability to the quality of core services: on-time execution and quote-to-invoice accuracy.[48]

**Implication for Handoff:** there are no paying customers yet. The expansion question comes second to one prior question: which one or two things make the first 5–10 operators keep paying?

### 2.2 Pattern B — The best-paid expansions follow the same customer's money.

- **Toast.** FY2020 revenue was $823.1M. Of that, $644.4M (78%) came from financial technology solutions and $101.4M from subscriptions. Hardware lost money: $64.0M of revenue against $85.0M of cost.[14]
- **AppFolio (property management software).** FY2024 revenue was $794.2M. Value Added Services were $605.0M (76%) and core software $180.6M, across 8.7M units under management.[5] That works out to about $91 of total revenue per unit per year (computed from [5]).
- **ServiceTitan.** In the six months to July 2024, usage revenue (mostly FinTech) was $84.5M of $363.3M total (23%). Gross transaction volume was $62.0B over the trailing 12 months.[15]
- **a16z (Strange, January 2020):** "nearly every company will derive a significant portion of its revenue from financial services". Shopify and Mindbody each earned nearly 50% that way.[18]

**Survivorship check.** Every company in this pattern had thousands of customers before financial products paid off: about 48,000 Toast locations,[14] and 8.7M AppFolio units.[5] Fintech attach is a scale effect. It is not an early strategy. Small vendors that tried it early and failed do not appear in public filings. That is a coverage gap.

**Implication:** Handoff already touches money: vendor payments from owner funds, the deposit, tenant charges and credits, recovery and write-off. That is the right direction for revenue. But property-management software incumbents already own the rails and distribute deposit products. Obligo credits its growth to partnerships with AppFolio, Buildium and Yardi.[32] Rhino bundles deposit insurance, cash deposit management, renters insurance and guarantor coverage across a partner network of six million homes.[31] A two-person team should earn on money flows through partners, not by building rails.

### 2.3 Pattern C — Expanding along the same workflow for the same buyer compounds. Crossing industries early does not.

- **EvenUp (legal AI).** Founded 2019. Its newest products account for "nearly 90% of new sales". It serves more than 2,000 firms, and ARR doubles year over year. It expanded along the case lifecycle for the same personal-injury firms.[40]
- **EliseAI.** It moved from housing into healthcare front-desk work only after passing $100M ARR and reaching 10% of the US apartment market.[6]
- **Olive** spread across revenue-cycle, population-health, 340B and payer products, then divested them and shut down.[9]
- **Palich, Cardinal & Miller (2000), a meta-analysis of 55 studies:** "moderate levels of diversification yield higher levels of performance than either limited or extensive diversification". Moving from a single business to related diversification helps. Moving on to unrelated diversification hurts.[20] Caveat: these are large firms, not startups.
- **Parker Conrad's "compound startup"** is the counter-thesis. He argues for building several integrated products in parallel on one system of record, because "product number two" is hard for a one-product company.[17] It is only a partial counter. His model still keeps one buyer and one data model. It argues for breadth *within* the workflow, not across industries.

**Implication:** the natural second product is the rest of the vacancy (move-in, pre-move-out inspection, make-ready) and the settlement. The same buyer and data model are reused. Other industries come later.

### 2.4 Pattern D — Services-plus-software works only when automation is real and measured. Otherwise it dies on labour cost.

This pattern has the most failures, and it is the most relevant, because Handoff "takes responsibility" for an outcome.

- **Atrium (legal, 2020).** It raised $75.5M and shut down. Kan: full-stack firms "did not figure out how to make a dent in operational efficiency". Its pivot to pure software for outside lawyers also stalled.[11]
- **Bench (bookkeeping, 2024).** It had more than 35,000 US customers by its own claim and had raised $113M.[10] Former staff said AI tools "didn't work properly". "Overreliance on these tools, sometimes at the expense of human bookkeepers, caused delays", and some customers' 2023 books were still unfinished in September 2024.[12] Its founder was removed in 2021 after disagreeing with the board on strategy.[13]
- **Pilot (bookkeeping).** Sacra estimates $43M ARR at 60% gross margin, against 25–33% for traditional bookkeepers. It cross-sells tax, R&D credits and fractional CFO work.[36] This is the success case for the same model.
- **Lessen (property services: turns, renovation, maintenance).** In January 2023 it bought SMS Assist for $950M, raising about $500M of debt and equity, with AMH among its investors. It served about 250,000 properties.[2] Its headcount then fell 28.7%, from 1,131 in 2023 to 806 in March 2026.[4] This is the closest analog to Handoff's turnover scope. It is not a clear win.
- **Latchel (maintenance coordination for single-family property managers).** It reached 100,000 homes in July 2022.[1] In 2026 it reports "112,000+ doors" and markets itself as an "AI front office".[3] That is slow unit growth, with a change of positioning.
- **Mynd (tech-enabled single-family property management)** merged into Roofstock in May 2024.[46] It is another property-services consolidation without a clear standalone outcome.
- **Foundation Capital (July 2025):** in services-as-software, "How you integrate, embed, and operate becomes the moat". Pricing is moving to outcomes.[23]

**What separated Pilot from Bench and Atrium:** automation that measurably lowered cost per unit of output before the company scaled, and humans kept in the loop where quality mattered. Handoff's design (agent coordinates, deterministic code checks money and identity, people decide) is the right shape. Its expansion should stay behind measured automation rates.

### 2.5 Pattern E — Balance-sheet and vertical-integration bets fail on forecasting risk.

- **Zillow Offers (2021)** was wound down with about a 25% workforce cut. "We have been unable to accurately forecast future home prices." Unit economics swung by about 1,200 basis points.[8]
- **Katerra (construction, 2021)** raised more than $2B to vertically integrate apartment building. It shut down and walked away from dozens of projects.[29]
- **Blend (mortgage software).** In 2021 it bought 90% of Title365, a services business, for $422M. Rising rates then "curtail[ed] demand". Blend lost $763.8M in 2022, cut 1,400 workers, and later took $150M to pay off the debt.[47]
- **Convoy (freight, 2023)** raised $260M at a $3.8B valuation, then closed with about 500 staff, down from a peak of 1,500. The cause was "a massive freight recession and a contraction in the capital markets".[28]
- **Vacasa (tech-enabled vacation-rental management)** was sold to Casago for $47.4M after 1,242 days as a public company.[7]

**Implication:** Handoff's design already keeps it off the balance sheet ("works within the owner's funds"). Expansion options that hold funds, guarantee deposits, underwrite recoveries or buy operators with debt would bring this risk back. Deposit insurance and underwriting belong with partners.

### 2.6 Pattern F — Owning the operator ("AI roll-up") is a real, new shape. It is unproven.

- **Dwelly (UK lettings, 2026).** Its founders came from Uber and Gett, and the CEO had earlier scaled a tech-enabled rental agency in Russia to 10,000 apartments. Dwelly has bought 10 agencies and raised £69M (£32M equity, £37M debt). It says the UK market is about 20,000 lettings firms managing 5.5M rentals, with the top 100 holding under 30%.[25] General Catalyst says Dwelly doubled EBITDA margins where its technology was fully deployed and cut repair wait times by 40%.[24]
- **Long Lake (US)** started by buying HOA management firms and has acquired 30 businesses. It then agreed to take Amex GBT private for $6.3B.[37] General Catalyst runs a $1.5B fund for this "Creation" strategy.[37]
- **Critics:** "the maths doesn't make sense" for venture returns, and founders must run two businesses at once.[26] "Services businesses aren't inefficient by accident"; clients pay for flexibility and "someone to blame". Concentrix still trades at low single-digit EV/EBITDA despite AI.[27]

**Survivorship check:** the roll-ups are one to three years old. No exit data exists yet. Vacasa is the older tech-enabled property-management consolidator, and it ended badly.[7]

### 2.7 Pattern G — Founder-market fit predicts success, but outsiders can learn it fast.

- **Azoulay, Jones, Kim & Miranda (US Census data):** prior work in the same industry "predicts a vastly higher probability of an upper-tail growth outcome or successful exit". Success rates rise up to 125%.[21]
- **ServiceTitan's founders** are "sons of trades business owners".[15]
- **Toast's founders were outsiders.** Their "first attempt at solving this problem failed miserably". They then went door-to-door to restaurant operators.[14]
- **Camuffo et al. (a randomised trial with 116 startups):** founders who test hypotheses like scientists perform better and pivot more.[22]
- **Paul Graham:** early on, "focus on a deliberately narrow market", or act as a consultant to a single user.[45]

**Implication for these founders:** their edge is building speed and quantitative evaluation (Owen), plus introductions and follow-through (Connor). Operating depth in property management is not listed. Compensate with a narrow, dense start and one or two deep operator partners, and use Owen's evaluation strength to run expansion as a sequence of priced experiments.

### 2.8 Pattern H — The move-out lane is filling quickly. Incumbents are building agents.

- **AppFolio Realm-X Performers (June 2025):** a Maintenance Performer that "self-sufficiently diagnoses and prioritizes resident maintenance requests", plus a Leasing Performer.[39]
- **Frontdesk** already markets "notice acknowledgment, move-out inspection scheduling, security-deposit walkthrough, forwarding-address capture, turn-vendor coordination, and final ledger close" across Yardi, RealPage, Entrata, AppFolio, Buildium and ResMan.[53]
- **TurnOps** sells AI move-out inspections, dispositions and deadline tracking for $19 per report.[52]
- **Stripe (February 2025 letter)** says AI is following SaaS from horizontal to vertical, with a growing number of industry-specific tools.[58][57]

These are vendor claims. Their traction is unverified. Still, the direction matters: coordination and inspection are being commoditised. The harder parts are accountability for the money, legally correct settlement, and running the work end to end inside the owner's funds.

### 2.9 Pattern I — Rules and geography shape how expansion can happen.

- **New York:** HSTPA (2019) caps the deposit for any apartment at one month's rent.[38] Under GOL §7-107 (rent-stabilised units), the landlord must return the deposit with an itemised statement within fourteen days of move-out, or "forfeit any right to retain any portion of the deposit". There is also an optional pre-move-out inspection with a right to cure.[34]
- **Virginia:** the cap is two months' rent, with itemisation due within 45 days.[35]
- **Regulators are active on tenant charges and pooled data.** The FTC and Colorado made Greystar pay $24M for "tacking on hidden fees".[50] The DOJ sued RealPage over landlords sharing "nonpublic, competitively sensitive information" to train pricing software.[49]

**Implication:** each new state is a new rules pack for the deterministic layer. Strict states (NY-style forfeiture) make settlement worth more. Charging tenants and pooling operators' data both carry legal exposure.

### 2.10 Pattern J — Platform dependency becomes a strategy constraint at scale.

- **Veeva** built its CRM on Salesforce. Its contract expired in September 2025 and it chose not to renew. It moved customers to its own Vault platform, with a wind-down running to 2030.[43]

**Implication:** Handoff's demo runs on Palantir Foundry, and production is undecided. The per-operator cost and deployment model of the production platform will limit which segments are economic: many small property managers, or a few institutions. Decide this before expanding across segments.

### 2.11 Multi-party networks

- **Procore** charges no per-seat fee. In 2020 each customer invited more than 160 project participants on average, including non-paying collaborators.[16]

Handoff already corresponds with vendors, owners and tenants. The vendor network is local. It compounds with density in one geography, not with breadth.

### 2.12 Market arithmetic relevant to any expansion

- The US has about 304,000 property management businesses, 238,000 of them residential. This is an aggregator figure, not primary data.[33]
- Turnover rates: apartments averaged 46.8% in NAA's 2019 survey, with about $1,800 per move-out.[54] Invitation Homes, a single-family operator, had 22.6% same-store turnover in FY2024 on 76,601 homes.[42] That is about 17,300 move-outs a year at one operator (computed).
- Illustration (my assumption, not sourced): at $150 per turn and 25–47% turnover, Handoff would earn about $38–70 per unit per year. AppFolio's total revenue is about $91 per unit per year.[5] So a per-turn fee can matter relative to the property-management software budget. But turnover happens rarely per unit, so revenue per customer is capped unless the scope widens.

---

## 3. Expansion options (my taxonomy)

The axes: what changes and what stays fixed. **Depth** keeps the buyer and changes the workflow. **Monetisation** keeps the workflow and changes who pays or which money flow. **Reach** keeps the product and changes segment or geography. **Shape** changes what kind of company this is.

### O1. Close the vacancy loop (Depth)
- **What:** extend from move-out and settlement to the whole vacancy. Capture the move-in condition baseline, which becomes evidence for the next move-out. Add the pre-move-out inspection and cure window, make-ready, and a ready-unit handoff to leasing.
- **Who pays:** the property manager, per turn or per unit. Owners may pay as a pass-through.
- **Why these founders:** same data model and agent. Adding it is mostly build speed, which is Owen's strength. It creates the evidence chain that settlement needs.
- **Evidence:** EvenUp's lifecycle expansion [40]; ServiceTitan Core to Pro [15]; Bain's one-variable adjacency [55].
- NY's pre-move-out inspection and right to cure give a built-in step [34].
- **Key risks:** crowded (Frontdesk, TurnOps, AppFolio agents).[53][52][39] Turnover is episodic.
- **What would falsify it:** design partners will not pay for the loop beyond move-out, or measured days vacant, turn cost against budget, and deposit disputes do not improve against their baseline.
- **Confidence:** high, as the first expansion.

### O2. Settlement-first in strict-deadline jurisdictions (Depth + Reach)
- **What:** make tenant-account settlement a lead product where deadlines carry forfeiture: New York first.[34][38] Offer defensible itemisation, on-time disposition, dispute handling and write-off recommendations.
- **Who pays:** the property manager or owner. It replaces the risk of forfeiture and staff time.
- **Why these founders:** the deterministic money, identity and permissions layer fits rules-heavy work. Both founders have renter experience and intros in NYC.
- **Evidence:** a statute that sets a hard penalty is rare, direct evidence of value. Regulators are scrutinising tenant charges.[50]
- **Context:** a record 22.4 million renter households were cost-burdened in 2022, so charges and deductions are sensitive.[51]
- **Key risks:** liability if the settlement is wrong. Consumer-protection exposure on charges. Debt-collection licensing if recovery is pursued [unverified].
- **What would falsify it:** property managers in NY already hit deadlines cheaply with staff or PMS tools, or will not delegate settlement to an agent.
- **Confidence:** medium-high.

### O3. Money flows through partners (Monetisation)
- **What:** earn on money that already moves: vendor payouts from owner funds, packaging deposit claims for deposit insurers and alternatives (Rhino, Obligo), and recovery of tenant balances through licensed partners. Do not build rails or hold risk.
- **Who pays:** partners (revenue share) and property managers. Tenants only through partner products.
- **Why these founders:** Connor's partner follow-through. The settlement engine produces exactly the itemised, evidenced claim a deposit insurer needs.
- **Evidence:** Toast 78%, AppFolio 76%, ServiceTitan 23% from money flows [14][5][15].
- Deposit products are distributed through the incumbents [32][31].
- **Key risks:** incumbents control payments. Revenue share is thin at low volume. Regulation [50].
- **What would falsify it:** no deposit insurer or payments partner will share economics at design-partner volumes.
- **Confidence:** medium on value. Low that the startup captures it directly.

### O4. Owner-funded project orchestration (Depth, adjacent workflow)
- **What:** apply the same quote → plan → budget → approve → order → pay loop to renovations between tenancies, capital projects and insurance-damage repairs.
- **Who pays:** owners (percentage of project) or property managers.
- **Why these founders:** reuses the quote and budget engine, which is Handoff's distinct capability versus triage tools.
- **Evidence:** Lessen bundles "renovation, turn, and maintenance".[2] Its contraction warns against a field-labour-heavy version.[4]
- **Key risks:** project management needs field presence. Scope creep.
- **What would falsify it:** projects need on-site supervision that email coordination cannot replace.
- **Confidence:** medium-low for now.

### O5. Density-first segment ladder (Reach)
- **What:** small and mid third-party property managers in Charlottesville and NYC, then regional firms, then institutional single-family and build-to-rent operators. Charlottesville student housing is a seasonal stress test; its August turnover peak is [unverified].
- **Who pays:** property managers, and later institutional operators.
- **Why these founders:** Connor's intros are local. Vendor networks compound locally.[16]
- **Evidence:** Homejoy's 30-city failure [30]; Paul Graham's narrow-market advice [45]; Dwelly staying UK-only before France [25].
- Bessemer's vertical-AI principles include "Target niche and underserved markets" [19].
- **Key risks:** small markets cap early revenue. Institutions such as AMH already back Lessen.[2]
- **What would falsify it:** there are not enough move-outs per month within the intro network to reach statistical learning in six months.
- **Confidence:** medium-high as a sequencing rule.

### O6. Become (or ally with) the operator (Shape)
- **Lite version:** run turnovers end to end for one or two property managers under an outcome contract.
- **Full version:** buy or partner with a small property manager in Charlottesville and run it on Handoff, AI roll-up style.
- **Who pays:** owners, through management and turnover fees.
- **Why these founders:** it avoids the hardest thing they lack, which is selling software to many reluctant small firms (Atrium's software pivot stalled).[11] It produces proprietary volume and data.
- **Evidence:** Dwelly and Long Lake [25][37]; General Catalyst's margin claims [24].
- Against: critiques on venture math and "someone to blame" [26][27]; Vacasa's outcome [7].
- **Key risks:** capital. Property-management licensing, since Virginia and New York generally require a real estate broker licence for third-party management [unverified]. Operating burden on two people. Founder operating experience is unknown.
- **What would falsify it:** no operator will hand over turn responsibility, or turn margins after Handoff do not beat the operator's current cost.
- **Confidence:** medium for the lite version. Low for the acquisition version unless capital and licensing are confirmed.

### O7. Engine-as-supplier (Shape)
- **What:** license the settlement and turn engine to PMS vendors, deposit insurers, or institutional operators' in-house teams.
- **Who pays:** platforms and institutions.
- **Why these founders:** fast building, few salespeople needed. It is also a realistic exit path.
- **Evidence:** PolyAI stayed software and partnered with BPOs, reaching a valuation above $500M.[27] Obligo grew through PMS partnerships.[32]
- **Key risks:** dependence on the partner, pricing power, and being copied (AppFolio builds agents in-house).[39]
- **What would falsify it:** platforms prefer to build. No partner signs a paid pilot.
- **Confidence:** medium as a channel or exit hedge.

### O8. Close-out engine for other industries (Shape, later)
- **What:** apply the same "end of a contract → evidence → vendor work → money settlement" pattern to HOA management transitions, short-term-rental turnovers, commercial lease exits, equipment-lease returns and insurance restoration.
- **Who pays:** operators in those industries.
- **Why these founders:** it reuses the architecture.
- **Evidence:** EliseAI crossed industries after passing $100M ARR [6]; Olive failed crossing early [9].
- The meta-analysis shows related diversification helps and unrelated hurts [20]. Long Lake entered through HOA [37].
- **Key risks:** loss of focus.
- **What would falsify it:** the core does not reach retention, so there is nothing to transfer.
- **Confidence:** low now. Medium in 2–3 years if the core works.

### O9. New paying parties (Reach)
- **What:** self-managing landlords, tenants (deposit-return help) or vendors as payers.
- **Evidence:** the landlord price point is about $19 per inspection;[52] a tenant-side product conflicts with the operator-side one; vendors are better treated as unpaid collaborators.[16]
- **Confidence:** low.

### O10. Turn-cost and vendor-price data products (Monetisation)
- **What:** benchmarks from pooled operators.
- **Risks:** needs volume. The antitrust theory in the DOJ's RealPage suit shows the legal risk of pooled operator data.[49]
- **Confidence:** low.

---

## 4. Ranking and reasoning

1. **Prove the core as a priced service, then O1 + O2 (vacancy loop, settlement-first where deadlines bite).** Every success in the set expanded from retention. Every early-expansion failure did not [44][30][9]. This keeps the buyer and data model fixed and changes one variable [55]. It aims at the part that is least commoditised and most legally consequential [34][53].
2. **O5 density-first as the sequencing rule.** It matches the founders' local introductions and the local nature of vendor networks.[30][45]
3. **O6-lite: run turns end to end for one or two operators on outcome terms.** This is the cheapest way to get real volume and learn operations. It tests whether "taking responsibility" is the product.[45][14] Decide later whether it grows into an operator or roll-up; that depends on capital and licensing.
4. **O3 through partners.** This is where long-run revenue per unit lives [14][5], but only after volume exists. Deposit-insurer claims are the most natural first link [31][32].
5. **O7 engine-as-supplier.** A hedge and a likely exit path if the incumbents keep building agents.[39][27]
6. **O4 owner-funded projects.** A logical adjacency, but it pulls toward Lessen-style field operations.[2][4]
7. **O8 other industries.** Only after the core retains.[6][9][20]
8. **O9 and O10.** Low value or high risk for this team.

Why not rank the roll-up (full O6) higher? It is the only option that fixes distribution outright. But it depends on three facts not in evidence: capital, licensing, and operating experience. The venture economics are disputed.[26][27]

---

## 5. Challenges to the premise

1. **"Once built" is not "once working".** With zero customers, the expansion question is premature. The test for expanding is retention and measured automation, not feature completeness.[44][12]
2. **The product may be a service, not software.** "Takes responsibility for the move-out" is an outcome promise. The analogs split sharply on that model: Pilot succeeded, while Bench and Atrium failed.[36][12][11] Choose between vendor, operator and engine before choosing expansions. Each shape implies a different next step.
3. **The wedge may be too episodic and too crowded.** Turnover happens once every two to four years per unit (22.6–46.8% a year) [42][54]. Incumbents and AI point tools are converging on it [39][53][52]. The defensible part may be settlement plus money accountability, not coordination.
4. **Expansion might not be the goal.** A focused, profitable per-turn service in a few metros may be a good business even if it is not venture-scale. Whether that is acceptable depends on the founders' goals and capital, which are not known.
5. **The platform decision is itself an expansion constraint.** Veeva shows how costly a foundation layer becomes at scale.[43] Foundry costs and deployment limits could decide which segments are reachable.
6. **An exit may be the best "expansion".** Selling the engine to a PMS or deposit insurer is a legitimate outcome if agents become a feature of the incumbents.[39][32]

---

## 6. Founder-fact assumptions my conclusions depend on

| Assumption | If false, what changes |
|---|---|
| Capital is modest (pre-seed scale) [unknown] | If large, the full O6 roll-up and a faster O3 become viable. If very small, stay on O1/O2 plus O6-lite only. |
| At least one founder works full-time [unknown] | If neither does, anything operator-shaped (O6) or on-call is out. Stay software/engine (O7). |
| No prior property-management operating role [unknown] | If one exists, O6 moves up. Industry experience predicts success.[21] |
| Intro network covers several operators with steady move-outs in Charlottesville and NYC [unknown size] | If thin, density-first fails. Channel partners (O7) or O3 partners become the distribution. |
| Owen's building speed keeps the loop (O1) cheap | If building is slower in production than in the demo, pick fewer surfaces and go settlement-first (O2). |
| Founders want venture scale | If not, a focused per-turn service is a complete answer. |
| Founders can hold the licences needed to manage or collect [unverified] | If not, O6-full and direct recovery are off. Use partners. |

---

## 7. Questions only private data can answer

1. How did demo viewers react? Who asked for pricing, and at what number?
2. For each introduced operator: units, move-outs per month, current cost and days per turn, deposit disputes and forfeitures, which PMS they use, and whether they would give email, vendor and payment authority.
3. What share of a demo move-out would run without a human today? What is the measured error rate on money?
4. What does Foundry cost per operator in production, and what are its licensing limits?
5. What are the capital runway and full-time status, and what outcome do the founders want (venture scale or not)?
6. Do the founders hold, or could they obtain, a real estate broker licence in Virginia and New York?
7. Would any deposit insurer or PMS vendor share economics or data at pilot volume?
8. Has any operator offered to let Handoff run its turns outright (the O6-lite signal)?

---

## Coverage gaps

- No systematic dataset on vertical-software expansion outcomes. The analogs are case-based and skewed toward companies that became public or famous.
- The academic evidence is mostly on large firms[20] or is dated and self-reported.[44]
- Latchel, Lessen, TurnOps and Frontdesk figures are company claims. Their private financials are unknown.
- Licensing (property management, collections, money transmission) is not verified. It needs a lawyer.
- Metropolis/SP+, Opendoor and Belong were identified but not read. They are not relied on.
- There is no primary data on what property managers will pay for move-out or settlement.
- About two-thirds of prose sentences carry no citation. They are this lane's own inference and implications, drawn from the cited findings above them. Treat them as reasoning, not sourced fact.

---

## Sources

[1] https://www.geekwire.com/2022/seattle-startup-making-it-easier-to-manage-single-family-rental-properties-raises-16-7m — GeekWire: Latchel raises $16.7M (2022)
    > "The company says its service is now used in more than 100,000 homes nationwide"
[2] https://www.lessen.com/resources/lessen-acquires-sms-assist — Lessen acquires SMS Assist (Jan 2023)
    > "approximately 250,000 residential and commercial properties"
[3] https://latchel.com — Latchel homepage (AI front office for property managers)
    > "deflect 50% of after-hours calls"
[4] https://www.reveliolabs.com/companies/lessen/employees — Revelio Labs: Lessen headcount
    > "Lessen’s total headcount has declined28.7% from 1,131 employees in 2023 to 806 in 2026"
[5] https://app.edgar.tools/filing/1433195/0001433195-25-000013 — AppFolio 10-K FY2024
    > "Value Added Services605,011"
[6] https://www.businesswire.com/news/home/20250820023566/en/EliseAI-Secures-%24250M-Series-E-to-Automate-Healthcare-and-Housing-Hiring-Hundreds-to-Fuel-Expansion — BusinessWire: EliseAI $250M Series E (Aug 2025)
    > "The company surpassed $100 million in Annual Recurring Revenue (ARR) earlier this year"
[7] https://skift.com/2025/05/01/vacasa-is-now-a-casago-company-after-acquisition-closes — Skift: Vacasa now a Casago company (May 2025)
    > "acquisition of the property management company became official"
[8] https://www.sec.gov/Archives/edgar/data/1617640/000161764021000085/exhibit993.htm — Zillow Group Q3 2021 shareholder letter
    > "we have been unable to accurately forecast future home prices"
[9] https://www.healthcaredive.com/news/olive-ai-shuts-down/698455 — Healthcare Dive: Olive AI to shut down (Oct 2023)
    > "fast-paced growth and lack of focus"
[10] https://techcrunch.com/2024/12/27/bench-shuts-down-leaving-thousands-of-businesses-without-access-to-accounting-and-tax-docs — TechCrunch: Bench shuts down (Dec 2024)
    > "Bench touted having more than 35,000 U.S. customers"
[11] https://techcrunch.com/2020/03/03/atrium-shuts-down — TechCrunch: Atrium shuts down (Mar 2020)
    > "did not figure out how to make a dent in operational efficiency"
[12] https://techcrunch.com/2025/01/03/inside-the-wild-fall-and-last-minute-revival-of-bench-the-vc-backed-accounting-startup-that-imploded-over-the-holidays — TechCrunch: Inside the fall of Bench (Jan 2025)
    > "Overreliance on these tools, sometimes at the expense of human bookkeepers, caused delays"
[13] https://threadreaderapp.com/thread/1872724231999381790.html — Ian Crosby thread on Bench shutdown (Dec 2024)
    > "I wanted to continue with what was working"
[14] https://www.sec.gov/Archives/edgar/data/1650164/000119312521258447/d166297ds1.htm — Toast S-1 (Sept 2021)
    > "Our first attempt at solving this problem failed miserably"
[15] https://www.sec.gov/Archives/edgar/data/1638826/000119312524260611/d577298ds1.htm — ServiceTitan S-1 (Nov 2024)
    > "Our founders, Ara Mahdessian and Vahe Kuzoyan, are the sons of trades business owners"
[16] https://www.sec.gov/Archives/edgar/data/1611052/000119312521065779/d564161ds1a.htm — Procore S-1/A (2021)
    > "In 2020, on average, each customer invited over 160 project participants"
[17] https://cloud.substack.com/p/why-the-first-rule-you-know-about — Cloud Weekly: Parker Conrad theory of compound startup
    > "figuring out how to get to product number two when your entire company is oriented around having just one product"
[18] https://a16z.com/every-company-will-be-a-fintech-company — a16z: Every Company Will Be a Fintech Company (Strange, 2019)
    > "make nearly 50 percent of their revenue through financial services"
[19] https://www.bvp.com/atlas/part-iv-ten-principles-for-building-strong-vertical-ai-businesses — Bessemer: Ten principles for vertical AI (Part IV)
    > "Target niche and underserved markets"
[20] https://ideas.repec.org/a/bla/stratm/v21y2000i2p155-174.html — Palich, Cardinal, Miller (2000) SMJ: Curvilinearity in diversification-performance
    > "moderate levels of diversification yield higher levels of performance than either limited or extensive diversification"
[21] https://www.nber.org/system/files/working%5Fpapers/w24489/w24489.pdf — Azoulay, Jones, Kim, Miranda (2018/2020): Age and High-Growth Entrepreneurship
    > "prior employment in the specific sector predicts a vastly higher probability of an upper-tail growth outcome or successful exit"
[22] https://cepr.org/publications/dp12421 — Camuffo et al.: Scientific approach to entrepreneurial decision-making (RCT)
    > "entrepreneurs who behave like scientists perform better, pivot to a greater extent to a different idea"
[23] https://foundationcapital.com/ideas/the-4-6t-services-as-software-opportunity-lessons-from-the-first-year — Foundation Capital: $4.6T Services-as-Software, lessons from first year
    > "How you integrate, embed, and operate becomes the moat"
[24] https://www.generalcatalyst.com/stories/the-future-of-services — General Catalyst: The Future of Services (AI-enabled roll-ups)
    > "They have acquired 6 agencies so far, doubling the EBITDA margins among agencies where their technology is fully deployed"
[25] https://fortune.com/2026/02/25/dwelly-ai-roll-up-uk-lettings-agencies-real-estate-brokerages-93-million-new-venture-captial-funding-to-fuel-expansion — Fortune: Dwelly AI roll-up raises $93M (Feb 2026)
    > "The company, which has already acquired 10 real estate agencies"
[26] https://pitchbook.com/news/articles/the-math-doesnt-make-sense-ai-rollup-hype-tests-the-limits-of-vc-economics — PitchBook: AI rollup hype tests limits of VC economics
    > "the maths doesn’t make sense"
[27] https://fortune.com/2025/06/27/ai-rollup-investment-strategy — Fortune: Why the AI rollup strategy is flawed (Jun 2025)
    > "Services businesses aren’t inefficient by accident"
[28] https://www.geekwire.com/2023/convoy-collapse-read-ceos-memo-detailing-sudden-shutdown-of-seattle-trucking-startup — GeekWire: Convoy CEO memo on shutdown (Oct 2023)
    > "we are in the middle of a massive freight recession and a contraction in the capital markets"
[29] https://www.housingwire.com/articles/rip-katerra-a-bold-power-play-that-failed-to-get-a-real-world-footing — HousingWire: RIP Katerra (2021)
    > "had raised more than $2 billion"
[30] https://www.forbes.com/sites/ellenhuet/2015/07/23/what-really-killed-homejoy-it-couldnt-hold-onto-its-customers — Forbes: What really killed Homejoy (Jul 2015)
    > "Only about 15% to 20% of customers booked again within a month"
[31] https://www.prnewswire.com/news-releases/rhinos-new-deposit-management-platform-launches-in-over-500-000-rental-units-302175530.html — PRNewswire: Rhino deposit management platform in 500,000 units (Jun 2024)
    > "secured 500,000 committed units to Rhino Integrated"
[32] https://www.obligo.com/blog/obligo-raises-35m-to-expand-its-security-deposit-solutions-across-millions-of-u-s-homes — Obligo raises $35M (2024)
    > "property management software companies"
[33] https://ipropertymanagement.com/research/property-management-industry-statistics — iPropertyManagement: Property management industry statistics
    > "are residential property management companies"
[34] https://newyork.public.law/laws/n.y.%5Fgeneral%5Fobligations%5Flaw%5Fsection%5F7-107 — NY General Obligations Law 7-108/7-107 (security deposits)
    > "If a landlord fails to provide the tenant with the statement and deposit within fourteen days, the landlord shall forfeit any right to retain any portion of the deposit"
[35] https://law.lis.virginia.gov/vacode/title55.1/chapter12/section55.1-1226 — Code of Virginia § 55.1-1226 Security deposits
    > "within 45 days after the termination date of the tenancy"
[36] https://sacra.com/research/pilot-mechanical-bookkeeper — Sacra: Pilot, the $43M/yr mechanical bookkeeper
    > "has hit 60% gross margins"
[37] https://pitchbook.com/news/articles/general-catalysts-6-3b-amex-deal-puts-its-ai-roll-up-strategy-on-display — PitchBook: Long Lake / GC $6.3B Amex GBT deal (2026)
    > "Long Lake has acquired 30 businesses since its founding"
[38] https://hcr.ny.gov/fact-sheet-9 — NY HCR Fact Sheet #9: Security deposits
    > "limits the amount of a security"
[39] https://www.appfolio.com/newsroom/appfolio-ai-agents — AppFolio: Realm-X Performers AI agents (Jun 2025)
    > "self-sufficiently diagnoses and prioritizes resident maintenance requests"
[40] https://www.evenuplaw.com/blog/evenup-2b-valuation — EvenUp: $150M Series E at $2B+ (Oct 2025)
    > "now account for nearly 90% of new sales"
[41] https://hbr.org/2021/05/why-start-ups-fail?ab=hero-main-text — Eisenmann, HBR: Why Start-ups Fail (2021)
    > "The start-up eventually saturates its original target market"
[42] https://www.sec.gov/Archives/edgar/data/1687229/000168722925000005/q42024supplemental.htm — Invitation Homes Q4 2024 supplemental
    > "Same Store Portfolio of 76,601 homes"
[43] https://www.fool.com/investing/2022/12/08/salesforce-and-veeva-systems-are-set-to-sever-ties — Motley Fool: Salesforce and Veeva set to sever ties (Dec 2022)
    > "its current contract with Salesforce expires in September 2025, and it does not plan to renew"
[44] https://startupgenome.com/insights/premature-scaling-a-deep-dive — Startup Genome: Premature Scaling deep dive (2011)
    > "the primary cause of failure is premature scaling, an affliction that 70% of startups in our dataset possess"
[45] https://www.paulgraham.com/ds.html — Paul Graham: Do Things that Don't Scale (2013)
    > "focus on a deliberately narrow market"
[46] https://www.globenewswire.com/en/news-release/2024/05/16/2883650/0/en/Roofstock-and-Mynd-Merge-to-Power-the-Next-Chapter-of-Growth-in-Single-Family-Rental-Investing.html — GlobeNewswire: Roofstock and Mynd merge (May 2024)
    > "Mynd will merge into the Roofstock corporate entity"
[47] https://www.inman.com/2024/04/30/mortgage-tech-provider-blend-gets-150m-private-equity-cash-injection — Inman: Blend gets $150M cash injection (Apr 2024)
    > "only to see rising mortgage rates suddenly curtail demand for its services"
[48] https://www.flexport.com/blog/flexport-ceos-note-to-employees — Flexport CEO's note to employees (Petersen)
    > "reduce the size of our global team by approximately 20%"
[49] https://www.justice.gov/archives/opa/pr/justice-department-sues-realpage-algorithmic-pricing-scheme-harms-millions-american-renters — DOJ: Justice Department sues RealPage (Aug 2024)
    > "share with RealPage nonpublic, competitively sensitive information"
[50] https://www.ftc.gov/news-events/news/press-releases/2025/12/greystar-agrees-pay-24-million-stop-deceptive-advertising-practices-result-ftc-colorado-lawsuit — FTC: Greystar agrees to pay $24M (Dec 2025)
    > "tacking on hidden fees on top of advertised prices"
[51] https://www.jchs.harvard.edu/sites/default/files/interactive-item/files/Harvard_JCHS_Americas_Rental_Housing_2024_Press_Release.pdf — Harvard JCHS: America's Rental Housing 2024 press release
    > "record high of 22.4 million"
[52] https://turnops.app — TurnOps: AI move-out inspection platform
    > "$19 per inspection report"
[53] https://www.myaifrontdesk.com/multifamily/ai-move-out-assistant — Frontdesk: AI move-out & turnover assistant
    > "turn-vendor coordination, and final ledger close"
[54] https://www.naahq.org/sites/default/files/2022-07/01a.%20Apartment%20Turnover%20%281%29.pdf — NAA: Apartment Turnover (2019 survey of operating income & expenses)
    > "the turnover rate across apartment rentals averaged 46.8 percent last year"
[55] https://www.bain.com/insights/growth-outside-core — Bain (Zook & Allen): Growth outside the core (HBR 2003)
    > "Seventy-five percent of growth initiatives fail"
[56] https://www.bain.com/insights/books/beyond-the-core — Bain: Beyond the Core (Zook) book page
    > "only one in five growth initiatives succeed"
[57] https://stripe.com/annual-updates/2024 — Stripe 2024 annual letter
    > "2024 was a good year for the internet economy"
[58] https://assets.stripeassets.com/fzn2n1nzq965/2pt3yIHthraqR1KwXgr98U/cbec59afdec826fb322271a56626aa9a/Stripe-annual-letter-2024-en-gb.pdf — Stripe 2024 annual letter (PDF, Feb 2025)
    > "Much as SaaS started horizontal and then went vertical"
