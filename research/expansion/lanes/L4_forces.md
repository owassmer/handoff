# L4 — Forces and timing through ~2030: how Handoff should expand

Lane: external, structural shifts. Research date: 2026-09-28. All figures carry a source and date. Claims from model knowledge are marked [unverified]. Arithmetic done by this lane is labeled "lane calculation".

## 1. One-paragraph answer

The strongest force in this market through 2030 is regulation converging on exactly the moment Handoff owns: the end of a tenancy and the money that moves at that moment. Between 2024 and September 2026, California, Colorado, Michigan, South Dakota and Virginia enacted new deposit, fee or move-out rules, and the FTC opened a federal rulemaking on rental fees "from application to moveout" in March 2026 (details and sources in section 2.1).[1][3][9]
At the same time, AI rules are closing the doors that look most attractive to an AI company, rent pricing and applicant screening, while the market is in a low-turnover, oversupplied phase that ends around 2027–2028 as construction collapses.[15][23][31]
So Handoff should not expand sideways into more of the lease lifecycle. It should expand *along the end-of-tenancy event*: first make the settlement engine compliance-grade across several strict states, including the move-in condition record it depends on; then sell the same engine to new payers who touch that event: consolidators absorbing portfolios, deposit-alternative and lease-insurance providers who adjudicate move-out claims, and, as a proving ground the founders can reach, Charlottesville student housing. The window is roughly 2026–2028. It closes when property-management-software incumbents, which already run agentic AI on 9.4 million units, ship their own move-out agents.[45]
Confidence: medium on the direction, low on any single buyer, because no private operator data was available to this lane.

## 2. Findings

### 2.1 Regulation: the end of tenancy is becoming a compliance event (enacted, 2024–2026)

**Deposit law is tightening state by state, and the new rules are about evidence and process, not just caps.**
- California AB 2801 requires landlords, from April 1, 2025, to photograph the unit after the tenant returns possession and before repairs or cleaning, and from July 1, 2025 to photograph it at move-in.[1]
  The same bill restricts what can be deducted and requires invoices or receipts for deductions.[1]
- California AB 414 took effect in early 2026: a deposit paid electronically must be returned electronically unless the tenant agrees in writing to another method.[2]
  California also capped most deposits at one month's rent from July 1, 2024 (AB 12). [unverified in this lane's fetches; widely reported]
- Colorado HB25-1249 took effect January 1, 2026.[3]
  It widens "normal wear and tear," requires documentation on request, allows walk-through inspections on request, and presumes a retention unreasonable if it is 125% or more of actual damages.[3]
- Michigan Public Act 102 of 2026 took effect September 21, 2026, one week before this report.[4]
  It rewrites the itemized notice of damages and requires the landlord to deposit the balance owed to the tenant into the tenant's account within 10 days of mailing the notice.[4]
- South Dakota SB 4 (signed February 11, 2026) changed the return deadline from two weeks to 21 days and tightened the itemized-accounting duty.[5]
- New York City Council bill Int 0249-2026 would require landlords to give tenants documentation of damages within 21 days when they withhold any deposit.[6]
  It is proposed, not enacted.

**Federal consumer-protection enforcement has already reached move-out.**
- The FTC's 2024 case against Invitation Homes, the largest single-family landlord, included "unfairly withholding tenants' security deposits when they moved out"; the settlement was $48 million (September 24, 2024).[7]
- Greystar agreed to pay $24 million over hidden mandatory fees in advertised rent (December 2, 2025).[8]
- On March 12, 2026 the FTC opened an advance notice of proposed rulemaking on rental housing fee practices across the lease lifecycle, "from application to moveout," with security deposits named as a topic.[9]
  The notice cites a survey finding 83% of renters pay a deposit, median $795 in 2025.[10]
  The FTC had excluded rental housing from its general fees rule (published January 10, 2025), so this is a separate track.[71][10]
  An ANPRM is the first of several steps; a final rule before 2028 is unlikely. [unverified: timing based on typical FTC Magnuson-Moss rulemaking length]

**Fee-disclosure laws are spreading.**
- Colorado HB25-1090 (effective January 1, 2026) requires total-price disclosure and caps markups on pass-through services at 2% or $10 a month.[11]
- Virginia HB 2430 requires an itemized fee list on the first page of leases entered, extended or renewed after July 1, 2025.[13]
  Virginia's 2026 amendments (effective July 1, 2026) require landlords to accept checks and money orders, limit processing and maintenance-related fees, and extend the nonpayment notice to 14 days; a 90-day rent-increase notice follows on July 1, 2027.[12]
- The FTC notice lists 2021–2025 state fee laws and bills in at least 15 states, including Connecticut, Georgia, Illinois, Nevada, New Mexico, Oregon, Texas, Vermont and Virginia.[10]

**Rent regulation is expanding in the founders' two markets and in the West.**
- New York's Good Cause Eviction law (April 20, 2024) caps "reasonable" increases for covered market-rate units at inflation plus 5%, maximum 10%.[19]
- NYC's FARE Act (June 11, 2025) bars landlords from passing broker fees to tenants.[18]
- NYC's Rent Guidelines Board voted June 25, 2026 for a two-year freeze on about 1 million rent-stabilized apartments, for leases starting October 1, 2026 to September 30, 2027.[20]
- Washington's HB 1217 (2025) caps increases for existing tenants at 7% plus inflation or 10%, whichever is lower.[21]
- Implication: in NYC, owner revenue is frozen or capped while costs rise. That makes cost-cutting software easier to sell and turnover rarer. [lane inference]

### 2.2 AI-specific rules: pricing and screening are closing; coordination with human sign-off is not

- DOJ's proposed RealPage settlement (November 24, 2025) bars the software from using competitors' nonpublic data to set rents at runtime.[15]
  California AB 325 (signed October 6, 2025) extends antitrust law to "common pricing algorithms."[16]
  New York S7882 (signed) makes it unlawful to set rents or lease terms through an algorithm performing a "coordinating function."[17]
  Virginia is studying a follow-on algorithmic pricing bill in 2026 after its 2025 legislation.[14]
- Colorado repealed and replaced its AI Act with SB 26-189 (signed May 14, 2026). It regulates automated decision-making in "consequential decisions," including housing, from January 1, 2027.[22]
  California's CCPA automated decision-making (ADMT) rules require compliance by January 1, 2027 for "significant decisions" that include housing.[23]
- Federal pressure runs the other way. A December 11, 2025 executive order created a DOJ AI Litigation Task Force to challenge state AI laws.[24]
  HUD proposed in January 2026 to remove its disparate-impact regulations, and issued a supplemental proposal on August 10, 2026.[27]
  Both are proposals or directives, not settled law.
- Implication: an AI company moving into rent setting or screening would walk into active enforcement and a changing patchwork. Handoff's current design keeps the AI on coordination, with deterministic checks on money and a human accepting or changing each plan. That design fits the ADMT regimes better than an autonomous decision-maker does. Whether a deposit deduction counts as a "consequential decision" about housing is untested. [lane inference; no source found]

### 2.3 Macro: an oversupplied, low-mobility market now; tighter from ~2027–2028

- Rental vacancy was 7.3% in Q2 2026, level with Q1 and up from a 5.6–5.9% low in 2022.[30][28]
- Apartment starts fell to about 55,000 units in Q1 2026, 73% below the early-2022 peak and the lowest since 2011; units under construction fell to about 579,000, down more than 50% from peak.[31]
  RealPage expects about 312,000 deliveries over the next four quarters and 1.9% rent growth from Q3 2026 to Q2 2027.[33]
- Rents are flat to slightly up: apartment asking rents +0.9% year over year in August 2026 with 95.5% occupancy;[32] single-family rents +1.8% year over year in July 2026.[35]
- Mobility is at record lows. Residential mobility fell to 11.2% in 2024.[28]
  Apartment retention was near record in 2025.[34]
  Research finds mortgage lock-in cut mobility by about 16% in 2022–2024.[36]
  JCHS notes rental retention rates rose and new occupancies declined into early 2026.[29]
  JCHS reports household growth slowed to 1.1 million in 2025 and cost-burdened renter households hit 22.7 million in 2024.[28]
- Turnover at scale: Invitation Homes' 2025 turnover rate was 22.8%.[37]
  AMH's was 26.3% (27.8% in 2024).[39]
  Invitation Homes spent $39.65 million on "turnover, net" in 2025 across 76,819 same-store homes.[37]
  Lane calculation: about $516 per home per year, or about $2,260 per turn, net of resident recoveries. That is a rough ceiling on what a scaled single-family operator spends on a turn's direct costs, excluding vacancy days.
- Evictions are not rising nationally: 1.23 million filings in tracked areas in 2025 versus 1.26 million in 2024.[67]
- Charlottesville is unusually soft. HUD's 2026 market analysis puts apartment vacancy at 12.4% in Q4 2025, the highest since 2010. UVA enrolls 26,685 students, and student households are about 14% of renter households.[70]
- Implication: 2026–2027 is a buyer's market for operators. Fewer tenants leave, and every vacant day costs more against a high vacancy baseline. AppFolio's 2026 survey found 55% of property managers named elevated vacancy as the top threat.[46]
  Once deliveries fall through 2027–2028, rent growth should firm and the value of a faster turn (days vacant) rises. [lane inference from [31][33]]

### 2.4 Ownership: fragmented owners, consolidating managers

- Individual investors held 59.6% of single-family rental properties in 2024, down from 70.9% in 2021. LLC/LP structures rose to 20.6%; REITs and corporations held 1.8% (Census Rental Housing Finance Survey via CRE Daily).[40]
  GAO found institutional investors may have raised prices and rents after 2008, but their effect on tenants is unclear.[41]
- Executive Order 14376 (January 20, 2026) directs agencies to stop federal programs from facilitating single-family sales to large institutional investors.[25]
  It does not ban purchases and carves out build-to-rent communities.[26]
  Invitation Homes bought build-to-rent developer ResiBuilt in January 2026.[37]
  Implication: institutional single-family growth shifts to build-to-rent and to fee-based management of others' homes.
- Invitation Homes began third-party management in January 2024 with a 14,000-home agreement.[38]
  At year-end 2025 it managed 15,866 "managed-only" homes, plus 8,006 joint-venture homes.[37]
- Manager consolidation is active. Alpine Investors launched Oakline Properties in September 2025 to roll up property and association managers, starting with a 20,000-unit firm.[43]
  A sell-side adviser reports that private-equity platforms make most property-management acquisitions and that valuations run 6–12x EBITDA. This is a marketing source; treat the figures as indicative.[44]
  AvalonBay and Equity Residential completed their merger into Vivmark Residential in August 2026, with more than 180,000 apartments.[42]
- The trade is still fragmented. There were 460,400 property, real estate and community-association manager jobs in 2025, and 31% of those workers were self-employed.[68]
  Community associations are a large adjacent pool: 373,000 associations with 29.6 million housing units (2025).[69]
- Implication: each acquisition merges firms that run different software, vendors and move-out practices. The buyer needs one standard process fast. That is a buyer for a system that sits above whatever PMS each acquired firm uses. [lane inference]

### 2.5 Labor and trades: vendor capacity is the binding constraint

- Associated Builders and Contractors estimates construction must attract 349,000 net new workers in 2026 and 456,000 in 2027.[50]
- In AGC's 2025 survey, 28% of firms said immigration enforcement had affected them in the prior six months. More than 75% reported trouble hiring electricians, plumbers and other trades, and 92% said openings were as hard or harder to fill than a year earlier.[51]
- Implication: turn quality and speed depend on getting scarce vendors to show up, quote and finish. Paying vendors quickly and reliably becomes leverage for winning capacity. [lane inference]

### 2.6 Insurance: costs spiked, now splitting

- Minneapolis Fed survey: multifamily property premiums rose 14% (2021–22), 22% (2022–23) and 45% (2023–24).[52]
- By Q3 2026 property insurance had softened. Commercial property premiums fell for a fourth straight quarter in Q2 2026, the largest decrease in 16 years, while casualty lines stayed tight. Water damage remains a leading loss driver.[53]
- Deposit alternatives are scaling and being codified. LeaseLock reported $14 billion in leases insured and more than 2 million deposit-free leases (July 2025).[63]
  Florida statute 83.491 authorizes a fee in lieu of a deposit.[61]
  Oregon's SB 158 (2025) proposed a similar recurring charge; this lane did not verify whether it was enacted.[62]
  An older estimate put $45 billion in US deposit accounts (2022).[64]
- Implication: deposit alternatives move the loss from the tenant's deposit to an insurer or guarantor. That insurer then needs the same thing Handoff produces: an evidence-backed, itemized, lawful account of damage at move-out. [lane inference]

### 2.7 Technology: agent capability is cheap and incumbents are shipping it

- The cost of GPT-3.5-level inference fell more than 280-fold from November 2022 to October 2024.[54]
  AI agents' success on real-world terminal tasks rose from 20% to 77.3% in a year (AI Index 2026).[55]
  METR estimates the length of task frontier agents can complete has doubled roughly every 7 months.[56]
- Incumbents: AppFolio manages about 9.4 million units for 22,096 customers. It launched agentic "Realm-X Performers" for maintenance and leasing, and a resident-onboarding product with Second Nature (Q4 2025).[45]
  EliseAI raised $250 million in August 2025 and says it covers about 10% of the US apartment market.[48] 58% of real-estate management professionals used AI in 2026, up from 21% in 2023.[47]
  AppFolio reports that firms that broadly adopted AI expect 31% portfolio growth in 2026, against 12% for others. This is a self-reported vendor survey.[46]
- Incumbents have a history of restricting integrations: Yardi and Entrata settled an antitrust suit over alleged PMS monopolization on the eve of trial.[49]
  Current API openness at AppFolio, Yardi, Entrata and RealPage was not verified by this lane. [coverage gap]
- Payments: FedNow had more than 1,700 participating institutions by August 2026, and RTP processed 128 million transactions a quarter.[57]
  California's AB 414 now ties the deposit refund method to the payment method.[2]
  Virginia's 2026 law requires landlords to accept checks.[12]
  Payment rails are becoming compliance constraints, not only features.
- Implication: generic coordination is being commoditized inside the PMS. What is hard to commoditize: (a) working across several PMSs and parties; (b) taking responsibility for an outcome; (c) the deterministic, state-specific money and evidence rules around deposits. [lane inference]

### 2.8 Public and affordable housing

- HUD's NSPIRE inspection standard becomes mandatory for Housing Choice Vouchers on February 1, 2027.[58]
- HUD warned in February 2026 of large voucher funding shortfalls and suggested agencies stop issuing new vouchers.[59]
- The 2025 budget law (OBBBA) permanently raised 9% LIHTC allocations by 12% and cut the bond test for 4% credits to 25%, for bonds issued after 2025.[60]
  Implication: more LIHTC units come online in 2027–2030 with heavy compliance, but tight budgets and low recovery on tenant balances. NAA cites collection-agency recovery of 15–20% overall and sometimes below 10% in affordable housing (2018 data).[65]

### 2.9 Recovery and collections

- The CFPB's 2024 FDCPA report flagged rental-debt collection complaints, including ambiguous damage terms and collection of amounts tenants dispute.[66]
  NAA reported an average of $92 per apartment unit lost to collections each year (2018 survey), with collection agencies keeping 20–40% of what they recover.[65]
- Implication: most of the value in recovery is decided before the debt is written, by the quality of the itemization and evidence. Third-party collection itself is a regulated, low-margin business. [lane inference]

## 3. Expansion options (lane taxonomy)

Taxonomy: **Deepen** (same event, harder rules) · **New payers on the same event** · **New segments** · **New adjacent events** · **Business-model shifts** · **Avoid** (doors closing).

### Deepen

**O1. Compliance-grade move-out settlement across strict states (with the move-in baseline).**
- What: turn the settlement engine into a state-rule system: deadlines, allowed deductions, photo/receipt evidence, itemization formats, return method and walk-through rights. Start with CA, CO, MI, NY and VA; add WA and others. Add a move-in condition capture module, because CA already requires move-in photos and every dispute turns on the baseline.
- Who pays: property managers and owners, per move-out or per unit per month. The customer is a mid-size manager in a strict state, where one mishandled deposit can cost up to twice the deposit in statutory damages under California's 1950.5.[1]
- Why these founders: Owen builds quickly and can encode rules as deterministic checks. Handoff already separates AI reasoning from deterministic money checks. The founders can reach Virginia (Charlottesville) and New York operators, both jurisdictions with active 2025–2026 rule changes.[12][6]
- Evidence: California rules.[1][2]
  Colorado, Michigan and South Dakota rules.[3][4][5]
  Federal and fee rules.[9][11][12]
- Timing: now to 2028. Rules are enacted and in force. A federal FTC rule could arrive around 2028–2029 and would nationalize demand. [unverified timing]
- Key risks: PMS incumbents add state rule packs; managers treat compliance as "our lawyer's forms"; the state-by-state legal upkeep costs more than a two-person team can carry.
- Falsified if: in 10–20 operator interviews in strict states, deposit disputes, complaints or statutory-damage exposure rank low among their problems, or their PMS already produces compliant itemizations.
- Confidence: medium.

**O2. Lease-lifecycle charge audit ("is this charge lawful and disclosed?").**
- What: a ledger checker that tests every tenant charge against state fee laws and lease disclosures. Move-out is where charges pile up, so it starts there.
- Who pays: large operators and roll-ups facing FTC and state attorney-general exposure.
- Why these founders: it extends the deterministic "check money" core.
- Evidence: federal enforcement and rulemaking.[8][9][10]
  State fee laws.[11][12]
- Timing: 2027–2029; demand spikes if the FTC moves to a proposed rule.
- Key risks: federal rule stalls; law firms and PMS vendors fill it; it drifts toward rent and fee setting.
- Falsified if: the FTC withdraws the ANPRM, or large operators say their existing counsel covers it.
- Confidence: low–medium.

### New payers on the same event

**O3. Claims adjudication for deposit-alternative and lease-insurance providers.**
- What: at move-out, the provider (not the tenant's deposit) pays the landlord and then pursues the tenant. Handoff produces the evidence-backed, lawful damage claim and the tenant notice, for the provider or for the landlord filing to the provider.
- Who pays: the provider per claim, or the landlord as part of the claim.
- Why these founders: same engine, few buyers, high volume per buyer. Suits a two-person commercial team.
- Evidence: deposit alternatives are scaling.[63]
  Florida codified fee-in-lieu programs.[61]
  Regulators scrutinize rental debt claims.[66]
- Timing: 2026–2029, as fee-in-lieu laws and regulator attention grow.
- Key risks: providers already run in-house claims teams; incentives diverge (a provider may want a larger claim, the landlord a faster one); state insurance regulation.
- Falsified if: two or three providers say claim handling is not a meaningful cost or loss driver, or will not share claim data.
- Confidence: low–medium. (No source on provider claim costs was found.)

**O4. Portfolio transitions for consolidators.**
- What: when a roll-up buys a manager, or a manager takes over a portfolio, deposits, ledgers, condition records, vendor contracts and in-flight turns must move over. Handoff runs the transition and then standardizes move-outs across the acquired firms regardless of their PMS.
- Who pays: the acquirer (PE platform, REIT or third-party manager), per portfolio plus per unit.
- Why these founders: few buyers, large contracts, and it plays to the product's "gather lease, condition, owner, vendor information" step.
- Evidence: Invitation Homes' third-party management.[37][38]
  Consolidation deals and M&A.[42][43][44]
- Timing: 2026–2029, while consolidation stays active.
- Key risks: enterprise sales cycles; acquirers standardize on one PMS and use its tools; transitions are episodic.
- Falsified if: acquirers report that migration pain is in accounting and software, not move-outs or deposits, or they will not buy from a pre-revenue vendor.
- Confidence: low–medium.

**O5. Owner-side oversight for individually owned single-family rentals.**
- What: a view for the owner funding the turn: why this cost, whether this deduction is lawful, whether the vendor was paid.
- Who pays: owners, or third-party managers as a retention feature.
- Evidence: individuals own 59.6% of single-family rentals.[40]
- Key risks: owners rarely buy software; it may conflict with the manager, who is the core customer.
- Confidence: low. Better as a feature of O1 than as a separate line.

### New segments

**O6. Student housing turn season (Charlottesville first).**
- What: most units turn over in a few weeks each summer, with roommates, parents and guarantors on each account. It is the hardest coordination and settlement case in a compressed window.
- Who pays: student-housing operators and local managers near UVA.
- Why these founders: a Charlottesville connection plus a very soft local market (12.4% apartment vacancy) where operators need faster, cheaper turns.[70]
- Evidence: [70]
- Timing: a hard annual deadline; prepare by spring 2027 for the August 2027 turn.
- Key risks: seasonal revenue; national student operators have in-house systems and staff; the segment is small outside college towns.
- Falsified if: local operators say the August turn is already well handled, or will not pilot for one season.
- Confidence: low–medium as a business, medium as a proving ground.

**O7. Scattered-site single-family and build-to-rent.**
- What: the current product in the segment where vendor coordination is hardest: every house is a separate trip.
- Who pays: SFR operators, third-party managers, build-to-rent owners.
- Evidence: turnover rates of 22.8% and 26.3%.[37][39]
  About $2,260 net direct cost per turn at Invitation Homes (lane calculation).[37]
  The build-to-rent carve-out.[26]
  Trade scarcity.[51]
- Timing: 2026–2030.
- Key risks: the largest operators run turns in house; Lessen and similar firms sell outsourced turns. [unverified detail on Lessen's current scale]
- Confidence: medium as a target within O1. Low as a standalone wedge against incumbents.

**O8. Affordable, LIHTC and voucher properties.**
- What: move-outs and turns with NSPIRE-compliant condition evidence and compliance files.
- Who pays: affordable owners and managers.
- Evidence: voucher inspection and funding changes.[58][59]
  LIHTC expansion and low recovery.[60][65]
- Timing: 2027–2030.
- Key risks: thin budgets, low recovery, slow procurement, voucher funding shortfalls.
- Confidence: low for the next expansion; revisit after 2028.

### New adjacent events (same shape: multi-party, evidence, money, deadline)

**O9. Water-damage and insurance-claim coordination in rentals.**
- What: a leak triggers vendors, the insurer, possible tenant relocation, rent abatement and tenant charges. The shape matches a turn.
- Who pays: operators; possibly carriers.
- Evidence: water damage is a leading insurance loss driver.[53]
- Key risks: restoration firms and carriers own this workflow; mid-lease events carry more habitability exposure.
- Confidence: low.

### Business-model shifts

**O10. Outcome-priced managed service ("we own the turn").**
- What: charge per completed turn or per vacant day saved, and take responsibility for the result, as the brief describes, rather than selling seats.
- Who pays: operators, from their turn budget rather than a software budget.
- Evidence: turn budgets are real line items;[37] AI inference is cheap, so agent-run service margins can beat labor-heavy turn services.[54]
- Key risks: liability for vendor failures; cash-flow exposure if Handoff pays vendors; ops load on two founders.
- Confidence: medium as a pricing model for O1, O6 and O7.

**O11. Sell into, or be bought by, a PMS vendor or consolidator.**
- What: treat expansion as proving one high-value, compliance-heavy module, then distribute it through a PMS marketplace or sell the company.
- Evidence: AppFolio is moving into resident lifecycle products;[45] roll-ups pay for operational standardization.[43][44]
- Confidence: medium that this is the realistic end state if the founders do not raise significant capital. Depends on founder goals (unknown).

### Avoid (doors closing)

- **Rent pricing or revenue management:** DOJ, California and New York actions make this a legal minefield.[15][16][17]
- **Applicant screening:** the Colorado and California automated-decision rules start January 1, 2027.[22][23]
- **Third-party debt collection:** FDCPA scope and CFPB attention; low recovery.[65][66]
  Better to improve the itemization that happens before collection.
- **Vendor payment financing or money transmission as a product:** licensing burden. [unverified] Use licensed payment partners instead.
- **Community-association management:** large (29.6 million units) but a different workflow and buyer.[69]

## 4. Ranking and reasoning

1. **O1 + move-in baseline, priced as O10.** This is where enacted law, federal enforcement and the product's existing design (AI coordination, deterministic money checks, human sign-off) meet. The need is created by statute rather than by persuasion, and it is state-specific, which is hard for a horizontal PMS to serve well early. It also sets up everything below.
2. **O4 (consolidators and portfolio transitions).** Consolidation is the clearest ownership trend. Each deal creates a one-time, urgent, budgeted need, then an ongoing multi-PMS need.[42][43]
Few buyers suit a small team.
3. **O3 (deposit-alternative claims).** A new payer for the same engine, with volume per buyer. Ranked below O4 only because this lane found no evidence of the providers' pain.
4. **O6 (Charlottesville student turn season).** The best near-term proving ground the founders can reach, with a hard deadline that creates a clear test. Likely too small to be the business.
5. **O7 (SFR and build-to-rent)** as the segment focus within O1 rather than a separate line.
6. **O2 (charge audit)**: an option that switches on if the FTC proceeds to a proposed rule.
7. **O11** is not ranked as an "expansion" but is the default path if capital stays small.
8. **O5, O8, O9** later or never.

Reasoning on timing: 2026–2027 is soft (7.3% vacancy, near-record retention).[30][34]
Operators want cost control and legal safety more than speed. That favors O1 and O4 now. From 2027–2028, falling deliveries should restore rent growth and make vacant days expensive again, which favors speed-based pricing (O10) and SFR/BTR (O7).[31][33]
Trade shortages peak in the same window (456,000 workers needed in 2027), which raises the value of vendor coordination.[50]

## 5. Challenges to the premise

- **"Once both are built" may be the wrong order.** The settlement layer, not turn orchestration, is where regulation is converging and where incumbents look least specialized. Turn coordination is the part AppFolio's maintenance agents and outsourced-turn firms are closest to commoditizing.[45]
  Leading with settlement, and treating the turn as the evidence source, may be the stronger position.
- **Low turnover caps a per-turn business.** With turnover of about 23–26% in large SFR portfolios and record-low mobility, a 1,000-unit manager may produce only 200–450 move-outs a year.[37][39][28]
  Lane calculation. Revenue per customer is small unless price per turn is high or Handoff serves many customers. The shift to more parties (O3, O4) addresses this better than more workflows do.
- **"Expand" may mean "be acquired."** If the founders are not raising substantial capital, the rational plan may be to build one defensible module and exit to a PMS vendor or consolidator within the 2026–2028 window (O11). This depends on founder facts unknown to this lane.
- **Taking responsibility is a service business.** "Takes responsibility for a move-out" implies liability and operations, not software margins. That choice drives staffing, insurance, pricing and fundraising more than any expansion option does.
- **The founders' home markets cut both ways.** NYC's rent freeze and Good Cause push owners to cut costs, but also reduce turnover.[19][20]
  Charlottesville is soft now and student-heavy.[70]
  These are good places to learn, not necessarily to scale.

## 6. Founder-fact assumptions my conclusions depend on

- **Capital raised:** O4, O10 (if Handoff fronts vendor payments) and any roll-up path need capital. If the company is unfunded, rank O1 → O6 → O11.
- **Full-time status:** the state-rule upkeep in O1 and the claims volume in O3 need sustained engineering. Part-time founders should narrow to two or three states.
- **Legal capacity:** O1 assumes access to landlord-tenant counsel in each target state. No source tells us whether the founders have it.
- **Operating credibility:** O4 and O3 sell to enterprises that prefer vendors with an operating record. No prior property-management operating role is assumed.
- **Introductions:** O6 and early O1 assume the Charlottesville and NYC introductions turn into pilots. Network size is unknown.
- **Liability appetite:** O10 assumes willingness to carry responsibility for vendor outcomes.

## 7. Questions only private operator data can answer

1. Per 1,000 units: move-outs per year, and the share that end in a deduction, a dispute or a balance above the deposit.
2. Average deduction, amount recovered beyond the deposit, and cost to recover.
3. Days from move-out to itemized statement and to refund, compared with the statutory deadline in each state; count of late or defective notices.
4. Complaints, small-claims suits or attorney-general inquiries over deposits in the last three years, and their cost.
5. Days vacant attributable to vendor scheduling, quotes and approvals, versus physical work.
6. Current internal staff hours per turn and per settlement, and the loaded cost.
7. Which PMS each target uses, and whether its API exposes ledgers, charges, work orders and documents.
8. Share of leases on a deposit alternative, and how that provider's move-out claims are prepared and paid.
9. For consolidators: what broke in the last portfolio transition, and who paid to fix it.
10. For student operators: units turned in the August window, overtime and contractor premiums, and disputes with parents or guarantors.

## 8. Coverage gaps

- The Census RHFS figures come via CRE Daily, not the Census tables.[40]
  California AB 414 comes via a practitioner summary, not bill text.[2]
  The AB 12 deposit cap is not fetched.
- No primary multifamily turn-cost benchmark (NAA or NMHC) was fetched. The single-family figure is a lane calculation from Invitation Homes' filing.[37]
- No evidence was found on deposit-alternative providers' claim costs or processes (O3).
- PMS API openness was not verified; the date of the Yardi–Entrata settlement is not shown on the accessible page.[49]
- Oregon SB 158 enactment status and NYC Int 0249-2026's status beyond introduction were not verified.[62][6]
- FTC rulemaking timing is an estimate. HUD's disparate-impact change is a proposal, not a final rule.[27]
- International markets (for example UK deposit-protection schemes with adjudication) were not researched. They may be relevant as a model for neutral deposit adjudication. [unverified]
- Lessen's and other outsourced-turn providers' current scale and economics were not verified.
- Verification: `sources.py verify --strict` passed on 2026-09-28. 71 sources are cited, 30 of them with verbatim evidence quotes in the ledger. About 39% of prose sentences carry a citation; the rest are this lane's analysis, options and questions, marked as inference where they state facts.

## Sources

[1] https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2801 — California AB 2801 (2024) security deposits: photographs
[2] https://www.relisto.com/2026/01/12/alert-update-to-california-security-deposit-law-ab-414-now-in-effect — ReLISTO: California AB 414 deposit return method (Jan 2026)
[3] https://leg.colorado.gov/bills/HB25-1249 — Colorado HB25-1249 Tenant Security Deposit Protections
[4] https://legislature.mi.gov/documents/2025-2026/publicact/htm/2026-PA-0102.htm — Michigan Public Act 102 of 2026 (SB 22) security deposits
[5] https://mylrc.sdlegislature.gov/api/Documents/SessionLaw/300761.pdf?Year=2026 — South Dakota 2026 SB 4 security deposit return
[6] https://legistar.council.nyc.gov/LegislationDetail.aspx?GUID=25D112EA-7F83-49BE-BC52-DB70E8787550&ID=7862025 — NYC Council Int 0249-2026 security deposit damage documentation
[7] https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-takes-action-against-invitation-homes-deceiving-renters-charging-junk-fees-withholding-security — FTC v. Invitation Homes press release (Sept 24, 2024)
[8] https://www.ftc.gov/news-events/news/press-releases/2025/12/greystar-agrees-pay-24-million-stop-deceptive-advertising-practices-result-ftc-colorado-lawsuit — FTC: Greystar $24M settlement (Dec 2, 2025)
[9] https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-seeks-public-comment-proposed-rulemaking-regarding-unfair-or-deceptive-rental-housing-fee — FTC rental housing fee ANPRM press release (Mar 12, 2026)
[10] https://www.ftc.gov/system/files/ftc_gov/pdf/r207011rentalhousingfeesanprm.pdf — FTC ANPRM text: Rule on Unfair or Deceptive Rental Housing Fee Practices
[11] https://dre.colorado.gov/hb25-1090-summary — Colorado DRE: HB25-1090 deceptive pricing summary
[12] https://www.williamsmullen.com/insights/news/legal-news/virginia-enacts-new-laws-impacting-residential-landlords — Williams Mullen: Virginia enacts new landlord laws (2026)
[13] https://nlihc.org/resource/state-virginia-adopts-new-laws-addressing-rental-fees-while-also-requiring-written-notice — NLIHC: Virginia 2025 rental fee laws
[14] https://vhc.virginia.gov/7.21.26%20Algorithmic%20Summary.pdf — Virginia Housing Commission algorithmic pricing workgroup summary (Jul 21, 2026)
[15] https://www.justice.gov/opa/pr/justice-department-requires-realpage-end-sharing-competitively-sensitive-information-and — DOJ: RealPage proposed settlement (Nov 24, 2025)
[16] https://aguiar-curry.asmdc.org/press-releases/20251006-majority-leader-aguiar-currys-ab-325-signed-governor-newsom-protecting — California AB 325 signed (Oct 6, 2025)
[17] https://www.nysenate.gov/legislation/bills/2025/S7882 — New York S7882 algorithmic rent pricing (signed)
[18] https://www.nyc.gov/site/dca/news/018-25/dcwp-the-fare-act-now-effect — NYC DCWP: FARE Act in effect (Jun 11, 2025)
[19] https://www.nyc.gov/site/hpd/services-and-information/good-cause-eviction.page — NYC HPD: Good Cause Eviction
[20] https://gothamist.com/news/nyc-rent-guidelines-board-approves-2-year-rent-freeze-fulfilling-mamdani-campaign-pledge — Gothamist: NYC RGB 2-year rent freeze (Jun 25, 2026)
[21] https://governor.wa.gov/news/2025/governor-ferguson-signs-rent-stabilization-affordable-housing-bills — WA Governor: HB 1217 rent stabilization signed (2025)
[22] https://kofirm.com/colorado-ai-act-repealed-and-replaced-what-businesses-need-to-know — Colorado SB 26-189 replaces AI Act (Jun 2026)
[23] https://www.thompsoncoburn.com/insights/californias-admt-rules-under-the-ccpa-what-they-mean-for-significant-decisions-and-how-to-get-ahead-of-implementation — Thompson Coburn: California CCPA ADMT rules
[24] https://www.whitehouse.gov/fact-sheets/2025/12/fact-sheet-president-donald-j-trump-ensures-a-national-policy-framework-for-artificial-intelligence — White House fact sheet: national AI policy framework EO (Dec 11, 2025)
[25] https://www.whitehouse.gov/fact-sheets/2026/01/fact-sheet-president-donald-j-trump-stops-wall-street-from-competing-with-main-street-homebuyers — White House fact sheet: EO 14376 institutional SFR buyers (Jan 2026)
[26] https://www.housingwire.com/articles/trump-signs-executive-order-targeting-institutional-investors — HousingWire: EO targeting institutional investors
[27] https://www.federalregister.gov/documents/2026/08/10/2026-16228/huds-implementation-of-the-fair-housing-acts-disparate-impact-standard-amendments-to-huds-title-vi — Federal Register: HUD disparate impact supplemental NPRM (Aug 10, 2026)
[28] https://www.jchs.harvard.edu/sites/default/files/interactive-item/files/Harvard_JCHS_State_Nations_Housing_2026_Key_Facts_0.pdf — Harvard JCHS State of the Nation's Housing 2026 Key Facts
[29] https://www.jchs.harvard.edu/blog/ten-takeaways-2026-state-nations-housing — Harvard JCHS: Ten Takeaways 2026
[30] https://www.census.gov/housing/hvs/current — Census HVS Q2 2026 (Jul 28, 2026)
[31] https://www.costargroup.com/press-room/2026/apartmentscom-and-costar-release-multifamily-construction-activity-update-q1-2026 — CoStar multifamily construction update Q1 2026
[32] https://www.realpage.com/analytics/august-2026-us-data-update — RealPage August 2026 data update
[33] https://www.realpage.com/analytics/forecast-2q26 — RealPage apartment forecast 2Q 2026
[34] https://www.realpage.com/analytics/what-we-got-right-2025 — RealPage: What we got right and wrong in 2025
[35] https://www.cotality.com/press-releases/annual-single-family-rent-growth-returns-to-seasonal-norms — Cotality Single-Family Rent Index July 2026
[36] https://www.philadelphiafed.org/-/media/FRBP/Assets/working-papers/2026/wp26-33.pdf — Philadelphia Fed WP 26-33 mortgage lock-in (2026)
[37] https://www.sec.gov/Archives/edgar/data/1687229/000168722926000013/q42025supplemental.htm — Invitation Homes Q4 2025 earnings release and supplemental (SEC)
[38] https://www.nasdaq.com/press-release/invitation-homes-announces-next-evolution-providing-professional-management-services — Invitation Homes third-party management launch (Jan 10, 2024)
[39] https://www.sec.gov/Archives/edgar/data/1716558/000156240126000010/amh-20251231.htm — AMH 2025 Form 10-K (SEC)
[40] https://www.credaily.com/briefs/single-family-rental-ownership-remains-individual-led — CRE Daily on Census 2024 RHFS SFR ownership
[41] https://www.gao.gov/products/gao-24-106643 — GAO-24-106643 institutional investment in SFR (May 2024)
[42] https://www.multifamilydive.com/news/reit-merger-vivmark-equity-residential-avalonbay/827775 — Multifamily Dive: AvalonBay-Equity Residential merger completes (Aug 2026)
[43] https://www.businesswire.com/news/home/20250925164992/en/Alpine-Investors-Launches-Property-and-Association-Management-Platform-Oakline-Properties — Alpine Investors launches Oakline Properties (Sept 2025)
[44] https://parklandcp.com/guides/ma-trends-2026-property-management — Parkland Capital: 2026 property management M&A trends
[45] https://ir.appfolioinc.com/static-files/ec0754ac-fb05-4c68-aee8-71f4d56d7f1b — AppFolio Q4 2025 prepared remarks
[46] https://www.appfolio.com/newsroom/property-manager-benchmark-survey-2026 — AppFolio 2026 Property Management Benchmark Report release
[47] https://blog.irem.org/ai-use-is-growing-fast-in-property-management.-are-your-guardrails-keeping-up — IREM: 2026 IREM-AppFolio AI adoption survey
[48] https://www.businesswire.com/news/home/20250820023566/en/EliseAI-Secures-%24250M-Series-E-to-Automate-Healthcare-and-Housing-Hiring-Hundreds-to-Fuel-Expansion — EliseAI $250M Series E (Aug 2025)
[49] https://news.bloomberglaw.com/antitrust/yardi-entrata-settle-real-estate-antitrust-suit-on-eve-of-trial — Bloomberg Law: Yardi, Entrata settle antitrust suit
[50] https://www.abc.org/News-Media/News-Releases/abc-construction-industry-must-attract-349000-workers-in-2026-despite-macroeconomic-headwinds — ABC: construction must attract 349,000 workers in 2026
[51] https://www.enr.com/articles/61266-increased-ice-enforcement-adds-to-constructions-labor-shortage-woes-agc-survey-finds — ENR: AGC survey on ICE enforcement and labor (2025)
[52] https://www.minneapolisfed.org/article/2025/rising-property-insurance-costs-stress-multifamily-housing — Minneapolis Fed: property insurance costs stress multifamily (Mar 2025)
[53] https://imacorp.com/insights/real-estate-markets-in-focus-q3-2026 — IMA: Real estate insurance markets Q3 2026
[54] https://hai.stanford.edu/ai-index/2025-ai-index-report — Stanford AI Index 2025
[55] https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report — Stanford HAI: 12 takeaways from AI Index 2026
[56] https://metr.substack.com/p/2026-1-29-time-horizon-1-1 — METR Time Horizon 1.1 (Jan 2026)
[57] https://www.richmondfed.org/publications/research/economic_brief/2026/eb_26-28 — Richmond Fed Economic Brief 26-28 FedNow (Aug 2026)
[58] https://www.nahro.org/news/hud-publishes-new-nspire-for-vouchers-administrative-notice — NAHRO: NSPIRE for vouchers notice (Jul 22, 2026)
[59] https://www.nahro.org/news/hud-sends-letter-on-hcv-budget-management-expects-large-shortfalls-despite-99-hap-proration — NAHRO: HUD HCV shortfall letter (Feb 18, 2026)
[60] https://www.nixonpeabody.com/insights/alerts/2025/07/16/low-income-housing-and-community-development-tax-credits-in-the-big-beautiful-bill — Nixon Peabody: LIHTC in OBBBA (Jul 2025)
[61] https://flsenate.gov/laws/statutes/2025/83.491 — Florida Statutes 83.491 fee in lieu of security deposit
[62] https://apps.oregonlegislature.gov/liz/2025R1/Downloads/MeasureDocument/SB158 — Oregon SB 158 (2025) charge in lieu of deposit
[63] https://www.businesswire.com/news/home/20250708882331/en/LeaseLock-Surpasses-%2414-Billion-in-Leases-Insured-as-Renters-Nationwide-opt-for-Deposit-Free-Living — LeaseLock $14B leases insured (Jul 2025)
[64] https://www.axios.com/2022/05/25/security-deposit-replacement-rhino-leaselock-obligo — Axios: security deposit alternatives (2022)
[65] https://naahq.org/best-practices-debt-collections — NAA: Best practices multifamily debt collections
[66] https://files.consumerfinance.gov/f/documents/cfpb_fdcpa-2024-annual-report_2024-09.pdf — CFPB FDCPA Annual Report 2024 (rental debt)
[67] https://evictionlab.org/ets-report-2025 — Eviction Lab: 2025 filing patterns
[68] https://www.bls.gov/ooh/Management/Property-real-estate-and-community-association-managers.htm — BLS OOH: property, real estate and community association managers
[69] https://natlawreview.com/press-releases/us-surpasses-373000-community-associations-housing-model-reaches-new-heights — FCAR 2025 Statistical Review release (Apr 1, 2026)
[70] https://www.huduser.gov/portal/sites/default/files/publications/pdf/CharlottesvilleVA-CHMA-26.pdf — HUD CHMA Charlottesville VA (2026)
[71] https://www.federalregister.gov/documents/2025/01/10/2024-30293/trade-regulation-rule-on-unfair-or-deceptive-fees — Federal Register: FTC Rule on Unfair or Deceptive Fees (Jan 10, 2025)
