# Handoff decks

September 2026. Four decks about the product, each as an editable PPTX and a PDF of the same slides. Both formats
come from one content module (`src/content.py`) and one builder (`src/build_decks.py`). Each number on a slide has
a public source in its source line, or is labelled "Handoff analysis" of named public sources. The PPTX speaker
notes repeat each slide's source line.

| File | Purpose | Slides |
|---|---|---|
| `Handoff_Pitch` | Pitch for investors and design partners. | 15 |
| `Market_Research` | The market for move-out work and settlement: the customer, the money, competitors, regulation, risks. | 17 |
| `Business_Model_Scenarios` | The paths a company in this market can take, and the modelled odds of revenue, funding and exit. | 12 |
| `Settling_a_NYC_Move_Out` | What New York City law requires of a manager at move-out, step by step, and how Handoff handles each step. | 18 |

The earlier `Outcome_Simulation` and `Legal_Engine` files were replaced by `Business_Model_Scenarios` and
`Settling_a_NYC_Move_Out` and have been removed. The file `~$Outcome_Simulation.pptx` is a PowerPoint lock file
from an open window. It is not a deck.

## Build

From `research/decks/src`:

```
uv run --with python-pptx python build_decks.py                      # all four decks
uv run --with python-pptx python build_decks.py Handoff_Pitch        # one deck
uv run --with python-pptx python build_decks.py --check              # fit check only, reports every failing slide
```

- Each slide is laid out once, in inches, as shapes and text boxes. The same layout renders to PPTX (python-pptx)
  and to HTML (`src/html/`). Headless Chrome prints the HTML to PDF.
- Text is measured against the Georgia and Arial font files, with the same line breaks the renderers use (spaces,
  hyphens and en dashes). If any text does not fit its box, the build stops and names the slide.
- Headlines and callouts wrap to balanced lines. A non-breaking space keeps the last two words of a paragraph
  together, and keeps each number with its unit, date or section sign. The tie is dropped where it would not fit.

## Design system

- **Type.** Georgia for display text: titles, headlines, section titles, names and panel heads. Arial for text,
  labels and numbers. Both fonts ship with macOS, Windows and Office, so the PPTX uses the same fonts and metrics
  as the PDF. Georgia has old-style figures, so big numbers and chart values are set in Arial Bold.
- **Scale (pt).** Title 60, section title 46, closing headline 38, headline 30, big number 54 to 110, lede and
  callout 20, body 18 to 20. Labels are 12 pt uppercase with 0.12 em tracking. Source lines and page numbers are
  10 pt. Body text is never below 18 pt. Only labels, legends, axis ticks, source lines and small in-chart tags
  are smaller.
- **Color.** One accent, burnt orange `#C2410C` (lightened to `#F08A5D` on dark slides), marks the thing to look
  at: the highlighted figure, bar, row, step or decision. The rest is a neutral scale: ink `#15202B`, secondary
  text `#46505C`, muted `#7B8591`, rules `#D9DDE2`, panels `#F1F3F5`, neutral bars `#B4BCC6`. Title, section and
  closing slides use navy `#101C2B`.
- **Grid.** 13.333 × 7.5 in slides, 0.75 in side margins, a 12-column grid, a fixed headline position, and a fixed
  source line at the foot of each slide.
- **Slide types.** Title, section divider, numbered findings, big-number stats, a single big figure with notes,
  columns, panels, a flow with arrows, stacked layers, a timeline, tables, horizontal bar charts (simple, range,
  paired, and shared-label multi-measure), a decision diagram, a month calendar, worked examples, an
  account-line diagram, team, and a dark closing slide. Every chart is drawn from shapes, so it is editable in
  PowerPoint and identical in the PDF. There are no images.

### Design references

- Material Design 3, *Type scale tokens*. Type roles (display, headline, title, body, label), with a brand face for
  large styles and a plain face for small ones. https://m3.material.io/styles/typography/type-scale-tokens
- IBM Carbon Design System, *Data visualization*. Simple, grouped and floating (range) bars. Numeric axes start at
  zero, and values are labelled directly. https://carbondesignsystem.com/data-visualization/chart-types/ and
  https://carbondesignsystem.com/data-visualization/axes-and-labels/
- Matthew Butterick, *Practical Typography: Presentations*. Keep one base size, use color with restraint, soften
  pure black on white, drop needless bullets, and keep the layout consistent. https://practicaltypography.com/presentations.html
  Butterick advises against Arial. It is kept here as the text face because it is the one sans that renders the
  same in PowerPoint on any machine.
- Kevin Hale, Y Combinator, *How to Design a Better Pitch Deck*. Legible, simple and obvious: one idea per slide,
  and the product shown as a short sequence of steps. https://www.ycombinator.com/blog/how-to-design-a-better-pitch-deck
- Pitch order: Sequoia Capital, *Writing a Business Plan* (https://sequoiacap.com/article/writing-a-business-plan)
  and Y Combinator, *The YC Seed Deck Template* (https://www.ycombinator.com/blog/intro-to-the-yc-seed-deck).

## Slide lists

### Handoff_Pitch

1. Title: Handoff takes responsibility for a residential move-out: the unit ready and the account settled.
2. Problem: a move-out is two jobs, and the manager runs both by phone and email.
3. Who feels it: third-party managers of small buildings and scattered homes. Who signs, who uses, who pays.
4. Solution: how a move-out runs. What runs today, what the pilot delivers, and the two manager decisions.
5. Why the settlement matters: New York's 14-day itemized statement, forfeiture, and up to twice the deposit.
6. How it works: code, the judgment model, the coordinator, and the manager.
7. What changes for the manager: notice day, during the turn, about day 10, day 14 and after.
8. Market: about $5.7 billion in deposits settled at move-out each year.
9. Why now: tightening rules in NY, VA, CO and MI, the FTC's 2026 rulemaking, and models that apply standards.
10. Business model and pilot.
11. Why sell an outcome: modelled odds for service first against software only (Handoff analysis).
12. Competition.
13. Traction and plan: product milestones.
14. Team: names and product roles.
15. The ask.

For a meeting with a property manager, show 1, 2, 4, 7, 5, 10, 13 and 15.

### Market_Research

1. Title. 2. Summary. 3. Section: the customer. 4. Where the units are. 5. How managers operate. 6. Manager
economics. 7. Section: the money. 8. Frequency and cost of move-outs. 9. Annual flows (turn spend, vacancy,
deposits, bad debt). 10. Where the value sits: turn against settlement. 11. Recovery: a dollar settled at move-out
against a dollar chased later. 12. Section: the competition. 13. Competitors. 14. How point tools end. 15. Section:
regulation and risks. 16. Regulation timeline. 17. Six risks to the thesis.

### Business_Model_Scenarios

1. Title. 2. Summary. 3. The nine paths. 4. The model, with a one-line note on calibration. 5. Assumptions by shape.
6. Section: results. 7. Revenue. 8. Funding. 9. Exit. 10. Direction. 11. What would change the
ranking. 12. What to take from it, with the limits in one line. The founder-time sensitivity is not in the deck; it
stays in research/expansion/sim/REPORT.md.

### Settling_a_NYC_Move_Out

1. Title. 2. The six steps. 3. Which rules apply (unit status and lease date). 4. Section: the law, step by step.
5. Step 1: can rent be recovered at all. 6. Step 2: the deposit and its interest. 7. Step 3: what may be kept.
8. Step 4: the 14-day statement and where it goes. 9. Step 5: what a miss costs. 10. Step 6: collecting a balance
and who may collect it. 11. Section: worked examples. 12. The day-14 holiday rollover (vacated Friday 2026-12-11,
due Monday 2026-12-28). 13. A repainting charge. 14. A co-tenant refund. 15. Section: how Handoff handles it.
16. Division of work. 17. What the manager sees on one account line. 18. What runs today and what the pilot adds.

## Public sources used

Market and pitch figures:
- U.S. Census Bureau, Housing Vacancy Survey, Q2 2026 (46.8M renter-occupied homes). https://www.census.gov/housing/hvs/files/currenthvspress.pdf
- NMHC, *Impact of new development on renter mobility* (2025): 18.3% of renter households moved in 2024. https://www.nmhc.org/research-insight/research-notes/2025/impact-of-new-development-on-renter-mobility-in-a-changing-housing-market
- HUD/Census, 2021 Rental Housing Finance Survey findings: 46% of units in 1–4 unit properties, 22% of small
  properties professionally managed, 70% of properties owned by individuals. https://archives.hud.gov/news/2022/pr22-242.cfm
- Terner Center, *Ownership and Management of Small Multifamily Rental Properties* (2024): 8.2M units, 17%. https://ternercenter.berkeley.edu/wp-content/uploads/2024/01/Ownership-and-Management-of-Small-Multifamily-Rental-Properties-January-2024-Final.pdf
- FTC, Rental Housing Fees ANPRM (83% of renters pay a deposit, median $795 in 2025). https://www.ftc.gov/system/files/ftc_gov/pdf/r207011rentalhousingfeesanprm.pdf
  Press release, March 12, 2026: https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-seeks-public-comment-proposed-rulemaking-regarding-unfair-or-deceptive-rental-housing-fee
- FTC v. Invitation Homes, September 24, 2024 ($48M). https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-takes-action-against-invitation-homes-deceiving-renters-charging-junk-fees-withholding-security
- NAA, *Apartment Turnover* (2025): $1,800 per move-out, seven working days, contractor-management hours. https://naahq.org/sites/default/files/2025-03/01a.%20Apartment%20Turnover%202025.pdf
- NAA, *Multifamily Debt Collections* (2019): agencies recover 15–20% and charge 20–40%. https://www.naahq.org/sites/default/files/2022-07/01.%20Multifamily%20Debt%20Collections.pdf
- NAA and AppFolio, *2025 Top Challenges Report* (n=1,984). https://naahq.org/sites/default/files/2026-01/NAA%20and%20AppFolio%202025%20Top%20Challenges%20Report%20-%20FINAL%20FINAL.pdf
- NAA, Income/Expense IQ 2024 (repairs, bad debt). https://naahq.org/news/momentum-management-navigating-elevated-costs-constrained-operating-environment
- NARPM, *Financial Benchmarks Guide* (2019, 2017 data): 6% margin, $1,809 revenue per unit, 25% owner churn. https://www.narpm.org/indexed/doc4-financialbenchmarksguide-pdf
- Buildium, 2026 Rental Owners' Survey (84% approve large repairs; 57% switch over communication). https://www.buildium.com/blog/how-rental-owners-evaluate-a-property-managers-performance
- Roost, 2021 security deposit survey (52% took no move-in photos; a vendor survey). https://www.joinroost.com/post/security-deposits-what-roost-members-say-2021-survey-results
- Belong, 232 Bay Area turnovers (2026, $957 per turn). https://belonghome.com/blog/cost-of-resident-turnover-in-the-sf-bay-area-what-232-turnovers-show
- Invitation Homes, Q4 2025 supplemental (turn cost, 22.8% turnover). https://www.sec.gov/Archives/edgar/data/1687229/000168722926000013/q42025supplemental.htm
- MAA, FY2025 results ($1,687 average rent). https://ir.maac.com/news-events/press-releases/news-details/2026/MAA-REPORTS-FOURTH-QUARTER-AND-FULL-YEAR-2025-RESULTS/default.aspx
- Manager quote: r/Landlord, May 2026. https://www.reddit.com/r/Landlord/comments/1tiq4q3/property_manager_ustx_buildium_users_whats_the
- Competitors: Obligo (https://www.prnewswire.com/news-releases/obligo-introduces-the-first-ai-agent-for-security-deposits-302800451.html),
  AppFolio (https://www.appfolio.com/newsroom/appfolio-ai-agents, https://www.appfolio.com/newsroom/appfolio-unveils-foliospace),
  Entrata (https://www.entrata.com/press/ai-powered-maintenance, https://www.entrata.com/press/entrata-acquires-colleen-ai),
  TurnOps (https://turnops.app), My AI Front Desk (https://www.myaifrontdesk.com/multifamily/ai-move-out-assistant),
  Vendoroo (https://vendoroo.ai/home-page-vendoroo), RealPage–Knock (https://www.multifamilydive.com/news/realpage-acquires-knock-crm/633287),
  Property Meld–Mezo (https://www.prnewswire.com/news-releases/property-meld-acquires-mezo-advancing-ai-driven-property-maintenance-operations-302350847.html),
  Venn–Zuma (https://www.globenewswire.com/news-release/2026/09/22/3366532/0/en/venn-acquires-a16z-backed-zuma-for-50-million-as-its-platform-closes-in-on-one-million-homes.html).
- Regulation: Colorado HB25-1249 (https://leg.colorado.gov/bills/HB25-1249); Michigan Public Act 102 of 2026
  (https://legislature.mi.gov/documents/2025-2026/publicact/htm/2026-PA-0102.htm); Virginia 2025–26 landlord laws
  (https://nlihc.org/resource/state-virginia-adopts-new-laws-addressing-rental-fees-while-also-requiring-written-notice,
  https://www.williamsmullen.com/insights/news/legal-news/virginia-enacts-new-laws-impacting-residential-landlords);
  N.Y. Laws 2019, ch. 36, Part M; NYC DCWP debt-collection rule, effective 2027-01-01
  (https://rules.cityofnewyork.us/wp-content/uploads/2026/02/DCWP-NOA-Rules-Relating-to-Debt-Collectors.pdf).
- Models applying legal standards: Katz, Bommarito, Gao and Arredondo, *GPT-4 passes the bar exam*, Phil. Trans. R.
  Soc. A 382 (2024). https://doi.org/10.1098/rsta.2023.0254

Scenario model base rates (Business_Model_Scenarios and pitch slide 11): ChartMogul SaaS growth report (2025),
https://chartmogul.com/reports/saas-growth-the-odds-of-making-it; Carta data via PMF Show (Q3 2025),
https://www.pmf.show/blog/series-a-fundraising-data-carta-q3-2025; Incisive Ventures graduation rates (2025),
https://incisive.vc/2025/06/10/update-on-venture-graduation-rates; PitchBook seed outcomes via Causo (2025),
https://hub.causo.ai/guides/startup-shutdowns-and-runway-data-2026; 733Park ARR multiples (2026),
https://www.733park.com/guides/saas-valuation-multiples-2026; ChurnTools SMB churn (2026),
https://churntools.com/churn-rate-by-size/smb; CRV's Series A range via Startupik (2026),
https://startupik.com/real-odds-of-raising-a-series-a-2026. Every result on those slides is Handoff analysis:
a monthly company model, 30,000 runs per path, calibrated to these base rates, with 300 parameter draws.

Law (Settling_a_NYC_Move_Out): N.Y. General Obligations Law §§ 7-103, 7-105, 7-107, 7-108; N.Y. General
Construction Law §§ 20, 24, 25-a, 35; N.Y. Multiple Dwelling Law §§ 4(7), 301, 302, 302-a, 325; N.Y. Real Property
Law §§ 232-c, 234-a, 238-a, 440; N.Y. CPLR §§ 213, 5001, 5004; NYC Admin. Code §§ 20-489, 20-699.22, 20-699.23,
26-504, 27-2013; 15 U.S.C. § 1692a; 6 RCNY 5-76 and 5-77. State statutes are at
https://www.nysenate.gov/legislation/laws/ and the NYC code at https://codelibrary.amlegal.com/codes/newyorkcity/.
Decisions: Paterno v Carroll, 75 AD3d 625 (2d Dept 2010); 14 E. 4th St. Unit 509 LLC v Toporek, 203 AD3d 17 (1st
Dept 2022); Cohen v Abruzzo, 228 AD3d 724 (2d Dept 2024); Pickens v Lane, 2023 NY Slip Op 50384(U); Prando v Kelly,
2021 NY Slip Op 51241(U) (App Term 2d Dept); Levine v Xu-Kehrli, 2026 NY Slip Op 50528(U). The co-tenant example
is labelled as Handoff's reading of GOL §§ 7-103(1) and 7-108(1-a)(e) with GCL § 35. Amounts in the worked
examples are illustrative and labelled that way.

## Handoff analysis (computed from public figures)

- 8.6M moves a year: 46.8M renter households × 18.3% (Census HVS, NMHC).
- $5.7B settled a year: deposit incidence and median (FTC ANPRM) applied to annual moves.
- 31M units in 1–49 unit buildings: 22.8M (RHFS 2021) + 8.2M (Terner Center 2024). The 37% share for 50+ units is
  the remainder of 46% and 17%.
- About $9 profit per unit a month: 6% × $1,809 a year ÷ 12 (NARPM). The earlier decks said "about $10".
- $45 to $120 a year for a turn tool: $150–400 per turn × 30% turnover.
- Annual pools: turns × $957–4,480 (Belong, Invitation Homes); 7–25 vacant days at MAA's rent; bad debt at
  $75–92 per unit (NAA). The ranges are wide because no national turn-cost series exists.
- $9–16 left of $100: 15–20% recovered, less a 20–40% fee (NAA).
- Price, churn and margin ranges for the scenarios are Handoff planning assumptions from the sources above.

## Dropped for lack of a public source, or as internal context

- Rule counts, review rounds and findings, the staged-compilation method, discovery families, and the judgment
  model's internal agreement check. These describe how the work was done, not the product or the law.
- Figures from other projects and any founder history beyond names and product roles.
- The claim that most units in the segment are market-rate.
- The bill that would cut the time to sue on a consumer debt to three years. It is not law yet.
- A total addressable market, or a count of third-party management firms. No reliable public count was found.
- Any turn-speed, staff-hour or recovery result for Handoff. No manager has paid for a move-out yet.
- The ROI example of $708 a turn and the $117-a-day vacancy example. Both are illustrations, not measurements.
- NYC move-out seasonality.
- Competitor results: TurnOps' $2,400 per unit and APTS' $1,150 per turn. Both are marketing claims.
- The share of renters who dispute a deposit (40%, from a 2021 vendor survey).
- A round size, use of funds or valuation.

## Checks

- Each PDF page was rendered with `pdftoppm -png -r 60` and inspected in 2×2 contact sheets. Defects found were
  fixed and the pages checked again: orphans, uneven rows, arrows, chart scales, table margins and legend
  placement.
- A script scanned each slide's text and speaker notes, and each PDF's text, for these terms: Stage A, atom, lane,
  L0–L5, review round, adjudicat, CORDON, Slope, Jev, Nay, Foundry, Ferro, .md, .py, .json, sim/, legal-engine/,
  expansion/, APERTURE, SYNTHESIS, Playbook, 0-to-1, independent review, sweep, checker. It found 0 hits. The
  founders' names appear only on the team slide.
- The PPTX files were checked by structure: slide counts, fonts and sizes, and speaker notes. They were not opened
  in PowerPoint during this pass.
