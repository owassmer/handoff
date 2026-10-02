"""Content for the four Handoff decks. One module, read by build_decks.py for both PPTX and PDF.

Every number on a slide carries a public source in its `src` line, or is labelled as Handoff analysis of named
public sources. '**text**' marks bold. The `src` line is also written to the PPTX speaker notes.
"""

DATE = "September 2026"

# ====================================================================== 1. Pitch

PITCH = dict(short="Handoff", slides=[
    dict(kind="title", kicker="Company overview", name="Handoff",
         line="Handoff takes responsibility for a residential move-out: the unit ready for the next tenant, "
              "and the departing tenant's account settled.",
         meta=f"For property managers, investors and design partners · {DATE}"),

    dict(kind="columns", kicker="Problem",
         title="A move-out is two jobs, and the manager runs both by phone and email",
         pgap=4,
         cols=[
             dict(label="The turn", head="Get the unit ready",
                  body=["Walk-through and scope of work.", "Quotes from each trade, in order.",
                        "Owner approval of the budget.", "Vendor visits, reports and invoices.",
                        "Paying vendors from owner funds."]),
             dict(label="The account", head="Settle with the departing tenant", hl=True,
                  body=["The deposit and any interest owed.", "Charges and credits, each with evidence.",
                        "**An itemized statement within 14 days.**", "A refund, or a balance to collect."]),
         ],
         note="At one 300-unit property in an NAA case study, staff spent up to 15 hours a week managing "
              "contractors by email, text and phone.",
         src="NAA, Apartment Turnover (2025); N.Y. General Obligations Law § 7-108(1-a)(e)."),

    dict(kind="columns", kicker="Who feels it",
         title="Third-party managers of small buildings and scattered homes feel it most",
         cols=[
             dict(label="The customer",
                  body=["Manages NYC walk-ups, small multifamily buildings and scattered single-family homes "
                        "for owners.", "No on-site staff. Vendors, phone and email do the work."]),
             dict(label="Who signs, who uses",
                  body=["The operations lead or the owner signs.",
                        "The property manager and the super use it every day."]),
             dict(label="Who pays",
                  body=["The owner funds the turn. 84% of owners want to approve large repairs.",
                        "A manager keeps about $9 a unit a month, so the owner pays, or recovered charges do."]),
         ],
         note="“It's all happening in spreadsheets and texts outside the platform.” "
              "A manager of about 100 units, May 2026",
         src="Buildium, 2026 Rental Owners' Survey; Handoff analysis of NARPM Financial Benchmarks Guide (2019): "
             "6% margin on $1,809 revenue per unit a year; quote: r/Landlord."),

    dict(kind="flow", kicker="Solution",
         title="Handoff runs the move-out. The manager approves the plan and accepts the account",
         row_gap=0.3, arrow=0.52,
         rows=[
             dict(label="The unit ready for the next tenant", style="today", steps=[
                 dict(t="Notice and plan"), dict(t="Vendor quotes"), dict(t="Manager approves", gate=True),
                 dict(t="Visits and invoices"), dict(t="Owner funds, vendor paid"),
             ]),
             dict(label="The departing tenant's account settled", style="pilot", steps=[
                 dict(t="Evidence from the turn"), dict(t="Account drafted"), dict(t="Manager accepts", gate=True),
                 dict(t="Statement by day 14"), dict(t="Refund or balance"),
             ]),
         ],
         legend=[("today", "Runs today"), ("pilot", "Delivered in the pilot"), ("gate", "Manager decision")],
         note="The turn produces the evidence behind each charge on the account."),

    dict(kind="bignum", kicker="Why the settlement matters",
         title="In New York, a statement sent one day late forfeits the deposit",
         big="14", caption="days after the tenant vacates to send an itemized statement and return the rest.",
         items=[
             "**Forfeiture.** Miss the deadline and the landlord loses any right to keep the deposit. Intent does "
                            "not matter.",
             "**Penalty.** A willful violation adds damages of up to twice the deposit.",
             "**Burden.** The landlord must prove each charge is reasonable. Nothing noted at move-in can be "
                        "charged.",
             "**Late recovery.** Collection agencies recover 15–20% of former-tenant debt.",
         ],
         src="N.Y. General Obligations Law § 7-108(1-a)(c), (e)–(g); NAA, Multifamily Debt Collections (2019)."),

    dict(kind="layers", kicker="How it works",
         title="Code sets every date and amount. A narrow judgment model answers the judgment questions",
         bands=[
             dict(name="Code", text="Deadlines, caps, interest, barred charges and every amount."),
             dict(name="Judgment model", text="Narrow questions: wear and tear or tenant damage? Noted at move-in?"),
             dict(name="Coordinator", text="Schedules vendors so the evidence lands before the deadline."),
             dict(name="Manager", style="gate", text="Sees each line's basis and accepts the account once."),
         ],
         note="A judgment never sets an amount or a date. Unknown facts go to the manager."),

    dict(kind="timeline", kicker="What changes for the manager",
         title="By about day 10 the manager sees one account, and decides once",
         points=[
             dict(when="Notice day", what="Handoff knows whether rent can be recovered, the day-14 deadline, the "
                                          "lawful way to send the statement, and which charges are barred."),
             dict(when="During the turn", what="Vendor visits, photos and invoices are scheduled to land before "
                                               "the deadline."),
             dict(when="About day 10", style="hl", what="One account. Each line shows its rule, evidence, "
                                                        "judgment and arithmetic."),
             dict(when="Day 14 and after", what="Handoff sends the statement and refund on time, answers disputes "
                                                "with the evidence on file, and recommends whether to pursue a "
                                                "balance."),
         ],
         note="This is the settlement half, which the pilot delivers."),

    dict(kind="stats", kicker="Market",
         title="About $5.7 billion in deposits is settled at US move-outs each year",
         stats=[
             dict(num="46.8M", label="renter-occupied homes in the US, Q2 2026"),
             dict(num="8.6M", label="renter moves a year"),
             dict(num="31M", label="rental units in buildings of 1 to 49 units"),
             dict(num="$5.7B", label="in deposits settled at move-out each year", hl=True),
         ],
         note="83% of renters pay a deposit. The median deposit was $795 in 2025.",
         src="Census Housing Vacancy Survey, Q2 2026; NMHC (2025); HUD/Census Rental Housing Finance Survey 2021; "
             "Terner Center (2024); FTC rental-fee notice (2026). 8.6M and $5.7B are Handoff analysis of these."),

    dict(kind="timeline", kicker="Why now",
         title="Move-out rules are tightening, and models can now apply standards like wear and tear",
         points=[
             dict(when="2019", what="New York: an itemized statement within 14 days, or the deposit is "
                                    "forfeited."),
             dict(when="2024", what="FTC: a $48M settlement with Invitation Homes, including deposits withheld at "
                                    "move-out."),
             dict(when="2025–26", what="Virginia, Colorado and Michigan tighten fee, deposit and move-out rules."),
             dict(when="March 2026", style="hl", what="The FTC opens a rulemaking on rental fees “from application "
                                                      "to moveout.”"),
         ],
         note="GPT-4 passed the Uniform Bar Exam in a 2024 study. A narrow model can now apply a standard; code "
              "keeps the dates and amounts.",
         src="N.Y. Laws 2019, ch. 36, Part M; FTC press releases (Sept 2024, Mar 2026); Colorado HB25-1249; "
             "Michigan Public Act 102 of 2026; Virginia 2025–26 landlord laws; Katz et al., Phil. Trans. R. Soc. A "
             "(2024)."),

    dict(kind="columns", kicker="Business model",
         title="Handoff sells a completed move-out, priced per outcome, starting with a paid pilot",
         cols=[
             dict(label="Price",
                  body=["Per completed move-out.", "Planning range $250–450, against $100–250 for a software "
                                                   "tool."]),
             dict(label="Who pays",
                  body=["Billed to the owner, or covered by charges recovered from the departing tenant.",
                        "Not paid from the manager's margin."]),
             dict(label="Pilot", hl=True,
                  body=["One manager, the next 20 move-outs, a $1,000 fixed fee.",
                        "The manager approves every charge. The manager's own payment provider moves the money."]),
         ],
         note="As each judgment step is measured, more of the service runs as software.",
         src="Source: Handoff planning ranges based on published tool prices (TurnOps) and NAA and NARPM "
             "benchmarks."),

    dict(kind="bars", kicker="Why sell an outcome",
         title="Selling a completed move-out gets a paying customer sooner than selling software",
         legend=["Service first, then software", "Software only"],
         panels=[dict(max=100, grid=[0, 25, 50, 75, 100], rows=[
             dict(label="Paying customer in 12 months", a=88, b=76),
             dict(label="$1M revenue by month 36", a=42, b=26),
             dict(label="A seed round", a=52, b=36),
         ])],
         label_w=4.4,
         note="Modeled odds, not forecasts. On either path, the likely exit is a sale to a platform.",
         src="Source: Handoff analysis, a monthly company model with 30,000 runs per path, calibrated to public "
             "software base rates (ChartMogul, Carta, PitchBook)."),

    dict(kind="table", kicker="Competition",
         title="Others sell tools for parts of the move-out. Handoff takes responsibility for both outcomes",
         head=["Company", "What it sells", "Where it runs"], widths=[2.5, 6.0, 3.3],
         hl_rows=[5],
         rows=[
             ["Obligo", "An AI agent for deposit charges, refunds and disputes", "Inside the major systems"],
             ["AppFolio, Entrata", "AI maintenance agents and make-ready boards", "Their own systems"],
             ["TurnOps", "AI damage documentation for unit turns", "Standalone"],
             ["My AI Front Desk", "A move-out assistant from notice to final ledger", "Beside the major systems"],
             ["Vendoroo", "AI maintenance coordination with a human expert", "Standalone"],
             ["Handoff", "The result: the unit ready and the account settled", "With your vendors"],
         ],
         src="Obligo (PR Newswire, June 2026); AppFolio newsroom (June 2025); Entrata press (June 2025); TurnOps, "
             "My AI Front Desk and Vendoroo websites (2026)."),

    dict(kind="timeline", kicker="Traction and plan",
         title="The turn runs today. The pilot adds the settlement for New York City units",
         points=[
             dict(when="Today", what="The turn runs end to end, from the notice to paying the vendor."),
             dict(when="Next", style="open", what="Walkthroughs of recent move-outs with five to eight managers."),
             dict(when="Pilot", style="open", what="The next 20 move-outs for a $1,000 fixed fee, with the "
                                                   "settlement for NYC market-rate units."),
             dict(when="Measured", style="open", what="Days to rent-ready, staff hours per turn, days to "
                                                      "statement, charges kept and disputes."),
         ],
         note="No paying manager yet. The pilot produces the first measured results."),

    dict(kind="team", kicker="Team",
         title="Two founders: one builds the product, one runs the manager relationships",
         people=[dict(name="Owen Wassmer", role="Product and engineering",
                      text="Builds the move-out workflow, the settlement engine and the manager's account view."),
                 dict(name="Connor McPhail", role="Operators and partnerships",
                      text="Runs manager walkthroughs, pilots and partner introductions.")]),

    dict(kind="closing", kicker="The ask",
         title="We are looking for managers who will show us their recent move-outs",
         cols=[
             dict(label="Property managers",
                  body=["Walk us through your recent move-outs.",
                        "Run your next 20 through a $1,000 fixed-fee pilot. You approve every charge."]),
             dict(label="Investors and advisors",
                  body=["Introduce us to third-party managers of NYC walk-ups and small multifamily buildings."]),
         ],
         question="Which move-outs in the next two months could we run with you?"),
])

# ====================================================================== 2. Market research

MARKET = dict(short="The move-out market", slides=[
    dict(kind="title", kicker="Market research", name="The move-out market",
         line="Who runs move-outs for small rental buildings, how much money moves through them, and who else "
              "sells into them.",
         meta=f"Handoff · {DATE}"),

    dict(kind="findings", kicker="Summary",
         title="Move-outs are frequent, costly and more regulated each year, and small managers run them by hand",
         items=[
             ("The customer", "Third-party managers of small buildings and scattered homes. No on-site staff; "
                              "vendors, phone and email do the work."),
             ("The money", "About 8.6M renter moves a year. Direct turn spend is $8–38B; about $5.7B in "
                           "deposits is settled."),
             ("The competition", "Platforms and new AI tools each sell a part of the move-out. The manager still "
                                 "owns the result."),
             ("The rules", "Deposit and move-out rules are tightening in several states, and the FTC opened a "
                           "rental-fee rulemaking in 2026."),
         ],
         src="Source: Handoff analysis of the public sources named on the following slides."),

    dict(kind="divider", num="01", title="The customer",
         line="Who runs move-outs in small rental buildings, and how they work."),

    dict(kind="bars", kicker="Where the units are",
         title="Almost two thirds of US rental units are in buildings of fewer than 50 units",
         panels=[
             dict(title="Share of US rental units, by size of property", max=60, grid=[0, 20, 40, 60],
                  rows=[
                      dict(label="1 to 4 units", v=46, hl=True),
                      dict(label="5 to 49 units", v=17, hl=True),
                      dict(label="50 or more units", v=37),
                  ]),
         ],
         label_w=3.0,
         note="Only 22% of 1–4 unit properties are managed professionally, against 84% of those with 150+ units.",
         src="HUD/Census Rental Housing Finance Survey 2021; Terner Center, Small Multifamily Rental Properties "
             "(2024); the 50+ share is Handoff analysis of both."),

    dict(kind="columns", kicker="How they operate",
         title="The manager coordinates the move-out; the owner approves and pays",
         cols=[
             dict(label="No on-site staff",
                  body=["Vendors, phone and email do the work.",
                        "At one 300-unit property, managing contractors took up to 15 staff hours a week."]),
             dict(label="Errors are common",
                  body=["48% of operators are completely confident that turn best practices are always "
                        "followed.", "About half find costly errors daily or weekly."]),
             dict(label="The owner decides",
                  body=["84% of owners want to approve large repairs first.",
                        "Poor communication is the top reason owners switch managers (57%)."]),
         ],
         note="“It's all happening in spreadsheets and texts outside the platform.” A manager of about 100 "
              "units",
         src="NAA, Apartment Turnover (2025); NAA and AppFolio, 2025 Top Challenges Report (n=1,984); Buildium, "
             "2026 Rental Owners' Survey; quote: r/Landlord (May 2026)."),

    dict(kind="stats", kicker="Manager economics",
         title="A manager earns about $9 a unit a month, so the owner pays for the move-out",
         stats=[
             dict(num="6%", label="average adjusted profit margin of a management firm"),
             dict(num="$1,809", label="revenue per managed unit a year"),
             dict(num="~$9", label="profit per unit a month", hl=True),
             dict(num="25%", label="of owners leave their manager each year"),
         ],
         note="A $150–400 turn tool at 30% turnover costs $45 to $120 per unit a year: up to a manager's whole profit.",
         src="NARPM Financial Benchmarks Guide (2019, 2017 data). The $9 profit and the tool cost are Handoff "
             "analysis."),

    dict(kind="divider", num="02", title="The money",
         line="How often units turn over, what a turn costs, and what moves at the settlement."),

    dict(kind="stats", kicker="Frequency and cost",
         title="About 8.6 million renter households move each year, and a move-out costs about $1,800",
         stats=[
             dict(num="46.8M", label="renter-occupied homes, Q2 2026"),
             dict(num="18.3%", label="of renter households moved in 2024"),
             dict(num="8.6M", label="renter moves a year", hl=True),
             dict(num="$1,800", label="NAA's conservative cost of one move-out"),
         ],
         note="NAA reports seven working days as a typical make-ready guideline, with targets of three to five.",
         src="Census Housing Vacancy Survey, Q2 2026; NMHC (2025); NAA, Apartment Turnover (2025). 8.6M is Handoff "
             "analysis."),

    dict(kind="bars", kicker="Annual flows",
         title="Turn spend is the largest pool. Deposits are smaller, but settle on a legal clock",
         label_w=3.6,
         panels=[dict(title="US annual pools, $ billions", max=40, grid=[0, 10, 20, 30, 40],
                      gfmt=lambda g: f"${g:g}B", rows=[
                          dict(label="Direct spend on unit turns", lo=8, hi=38, text="$8–38B"),
                          dict(label="Rent lost while units sit vacant", lo=3, hi=12, text="$3–12B"),
                          dict(label="Deposits settled at move-out", v=5.7, hl=True, text="$5.7B"),
                          dict(label="Bad debt written off", lo=3.5, hi=4.3, text="$3.5–4.3B"),
                      ])],
         note="No one publishes a national turn-cost series, so the turn ranges are wide.",
         src="Handoff analysis of Census HVS, NMHC, NAA Income/Expense IQ 2024, NAA Apartment Turnover, Invitation "
             "Homes and MAA 2025 results, Belong (2026) and the FTC rental-fee notice (2026)."),

    dict(kind="compare", kicker="Where the value sits",
         title="The turn is the larger spend. The settlement is where deadlines and evidence decide the money",
         sides=[
             dict(label="The turn", head="Larger and crowded", items=[
                 "**Cost.** $957 to $4,480 of direct cost per turn.",
                 "**Value.** Vacant days saved: about $55 a day at a $1,687 rent.",
                 "**Competition.** Platforms ship make-ready boards and maintenance agents.",
             ]),
             dict(label="The settlement", head="Smaller, with hard rules", hl=True, items=[
                 "**Deadline.** 14 days in New York, with forfeiture on a miss.",
                 "**Evidence.** 52% of renters took no move-in photos (2021 vendor survey).",
                 "**Recovery.** Agencies recover 15–20% of what is owed and keep 20–40% of that.",
             ]),
         ],
         src="Belong (2026); Handoff analysis of Invitation Homes and MAA 2025 results; N.Y. Gen. Oblig. Law "
             "§ 7-108(1-a)(e); Roost renter survey (2021); NAA, Multifamily Debt Collections (2019)."),

    dict(kind="bars", kicker="Recovery",
         title="A dollar settled at move-out is worth several dollars chased later",
         label_w=4.2,
         panels=[dict(title="Of $100 owed by a former tenant", max=100, grid=[0, 25, 50, 75, 100],
                      gfmt=lambda g: f"${g:g}", rows=[
                          dict(label="Owed at move-out", v=100, text="$100"),
                          dict(label="Recovered by a collection agency", lo=15, hi=20, text="$15–20"),
                          dict(label="Left after the agency's fee", lo=9, hi=16, text="$9–16", hl=True),
                      ])],
         note="NAA advises sending balances to collection within 30 days of move-out.",
         src="NAA, Multifamily Debt Collections (2019); the net range is Handoff analysis."),

    dict(kind="divider", num="03", title="The competition",
         line="Who sells into the move-out today, and how those companies end."),

    dict(kind="table", kicker="Competitors",
         title="Platforms and new AI tools each sell a part of the move-out",
         head=["Company", "What it sells", "Part"], widths=[2.5, 7.4, 1.9],
         rows=[
             ["Obligo", "Deposit Agent inside Yardi, RealPage, AppFolio and Buildium (2026)", "Settlement"],
             ["AppFolio", "Realm-X agents for leasing and maintenance (June 2025)", "Turn"],
             ["Entrata", "Make-ready boards (2025); Colleen AI for former-resident debt (2024)", "Turn, balance"],
             ["TurnOps", "AI damage documentation for unit turns", "Turn"],
             ["My AI Front Desk", "A move-out assistant from notice to final ledger", "Settlement"],
             ["Vendoroo", "An AI maintenance coordinator backed by a human expert", "Maintenance"],
         ],
         src="Obligo (PR Newswire, June 2026); AppFolio newsroom (2025); Entrata press (2024, 2025); TurnOps, My AI "
             "Front Desk and Vendoroo websites (2026)."),

    dict(kind="timeline", kicker="How point tools end",
         title="Point tools in this market end up inside a larger platform",
         points=[
             dict(when="2022", what="RealPage buys Knock, a leasing CRM."),
             dict(when="2024", what="Entrata buys Colleen AI, and AppFolio buys LiveEasy."),
             dict(when="2025", what="Property Meld buys Mezo, a maintenance AI."),
             dict(when="2026", style="hl", what="Venn buys Zuma, an AI leasing agent, for $50M."),
         ],
         note="Venn says it gives the software away and charges for “agentic outcomes.”",
         src="Multifamily Dive (Oct 2022); Entrata press (June 2024); AppFolio newsroom (Oct 2024); PR Newswire "
             "(Jan 2025); GlobeNewswire (Sept 2026)."),

    dict(kind="divider", num="04", title="Regulation and risks",
         line="How the rules around move-outs are changing, and what could break the thesis."),

    dict(kind="table", kicker="Regulation",
         title="Deposit and move-out rules are tightening at the state, city and federal level",
         head=["When", "Where", "What changed"], widths=[1.5, 2.3, 8.0],
         rows=[
             ["Jul 2019", "New York", "14-day itemized statement, or the deposit is forfeited"],
             ["Sep 2024", "FTC", "$48M Invitation Homes settlement, including withheld deposits"],
             ["Jan 2026", "Colorado", "Keeping 125% of actual damages or more presumed unreasonable"],
             ["Mar 2026", "FTC", "Rulemaking on rental fees “from application to moveout.”"],
             ["Jul 2026", "Virginia", "Limits on processing and maintenance fees"],
             ["Sep 2026", "Michigan", "Refund paid into the tenant's account within 10 days"],
             ["Jan 2027", "New York City", "Debt-collection rules reach landlords' own collection"],
         ],
         src="N.Y. Laws 2019, ch. 36, Part M; FTC (2024, 2026); Colorado HB25-1249; Virginia 2026 amendments; "
             "Michigan Public Act 102 of 2026; NYC DCWP debt-collection rule (2026)."),

    dict(kind="list", kicker="Risks",
         title="Six risks could break the thesis",
         ncol=2,
         items=[
             "**The settlement is contested.** Obligo's deposit agent already runs inside the major "
                                             "property-management systems.",
             "**Per-event dollars are small.** The median deposit is $795, so the price must come from the owner "
                                             "or from recovered charges.",
             "**Collection carries legal weight.** Recovering a balance brings debt-collection and licensing "
                                                 "rules.",
             "**Managers may resist transparency.** An itemized account can expose markups on vendor work.",
             "**Nothing is measured yet.** No manager has paid for a completed move-out, so price and results "
             "are untested.",
             "**Maintenance has more volume.** Repairs in occupied units happen more often than move-outs, and "
                                             "tools there are crowded.",
         ],
         note="The paid pilot is the first test: whether managers pay per move-out, and how much.",
         src="Obligo (PR Newswire, June 2026); FTC rental-fee notice (2026)."),
])

# ====================================================================== 3. Business model scenarios

SIM = dict(short="Business model scenarios", slides=[
    dict(kind="title", kicker="Scenario analysis", name="Business model scenarios",
         line="Nine ways a company can build in the move-out market, and the modelled odds of revenue, funding "
              "and exit for each, 2026 to 2032.",
         meta=f"Handoff · {DATE}"),

    dict(kind="findings", kicker="Summary",
         title="Selling a completed move-out gives the best odds of revenue and funding",
         items=[
             ("Revenue", "Service paths get a paying customer within 12 months 88–89% of the time, against 76% "
                         "for software."),
             ("Funding", "Service first, then software, leads: 42% reach $1M in annual revenue by month 36, and "
                         "52% raise a seed round."),
             ("Exit", "Exits are modest on every path. The likely exit is a sale to a larger platform."),
             ("Direction", "Growing deeper into the tenancy beats adding owner projects or maintenance."),
         ],
         src="Source: Handoff analysis, a monthly company model with 30,000 runs per path and 300 parameter draws."),

    dict(kind="columns", kicker="The paths",
         title="Nine paths combine a business shape with a direction for growth",
         panel=True, gap=0.22, pgap=9,
         cols=[
             dict(head="Software",
                  body=["Tenancy depth", "Maintenance", "Owner projects"]),
             dict(head="Service",
                  body=["Tenancy depth, priced per move-out", "Turns and owner projects"]),
             dict(head="Service first", hl=True,
                  body=["Tenancy depth, then software as the work is automated"]),
             dict(head="Engine",
                  body=["Platforms and deposit insurers", "Consolidators"]),
             dict(head="Operator",
                  body=["Buy a small management firm and run it on Handoff"]),
         ],
         note="Tenancy depth: the move-in record, the turn and the settlement for the same manager."),

    dict(kind="flow", kicker="The model",
         title="Each simulated company runs month by month from October 2026 to October 2032",
         arrow=0.4, minh=0.75,
         rows=[dict(style="today", steps=[
             dict(t="First sale", sub="Monthly odds depend on the shape. None by month 18 ends the run."),
             dict(t="Growth", sub="Sales and referrals add customers; some churn."),
             dict(t="Expansion", sub="Starts after 12 months with three customers or more."),
             dict(t="Bundling", sub="A platform copies the product: sales fall 40%, prices 25%."),
             dict(t="Funding", sub="Seed at $400k in revenue, Series A at $2.5M."),
             dict(t="Exit", sub="A sale at the private multiple for its size."),
         ])],
         note="Calibrated so a generic software company reproduces public odds of reaching $1M in revenue and "
              "raising each round.",
         src="Sources: Handoff analysis; base rates: ChartMogul (2025), Carta (Q3 2025), Incisive Ventures (2025), PitchBook "
             "via Causo (2025), CRV via Startupik (2026); multiples: 733Park (2026)."),

    dict(kind="table", kicker="Assumptions",
         title="Service earns more per move-out and churns less. Software keeps more of each dollar",
         head=["Assumption", "Software", "Service"], widths=[6.4, 2.7, 2.7], accent_col=2,
         rows=[
             ["Price per move-out", "$100–250", "$250–450"],
             ["Monthly churn", "2–4.5%", "1.2–3%"],
             ["Gross margin", "65–82%", "35–65%"],
             ["Yearly chance a platform bundles the product", "15–35%", "8–22%"],
         ],
         note="A median client manages 400 homes turning 28% a year: about 112 move-outs.",
         src="Source: Handoff assumptions, drawn from TurnOps pricing, NARPM and NAA benchmarks, ChurnTools SMB churn data "
             "(2026) and Invitation Homes 2025 turnover."),

    dict(kind="divider", num="Results", title="What the odds say",
         line="Revenue, funding and exit for each path, and what moves them."),

    dict(kind="bars", kicker="Revenue",
         title="Service paths are the most likely to get a paying customer within 12 months",
         label_w=4.6,
         panels=[dict(max=100, grid=[0, 25, 50, 75], rows=[
             dict(label="Service paths (three)", v=89, text="88–89%", hl=True),
             dict(label="Software for managers", v=76),
             dict(label="Engines for platforms or consolidators", v=50, text="46–50%"),
             dict(label="Buying a management firm", v=10),
         ])],
         note="A service path ranks first on this measure in all 300 parameter draws.",
         src="Source: Handoff analysis, 30,000 runs per path."),

    dict(kind="bars2", kicker="Funding",
         title="Service first, then software, leads on revenue and on raising a seed round",
         panels=[
             dict(title="$1M in annual revenue by month 36", max=60, grid=[0, 20, 40, 60], rows=[
                 dict(label="Service, then software", v=42, hl=True),
                 dict(label="Service", v=41),
                 dict(label="Software, tenancy", v=26),
                 dict(label="Software, maintenance", v=19),
                 dict(label="Engine for platforms", v=14),
             ]),
             dict(title="A seed round", max=60, grid=[0, 20, 40, 60], rows=[
                 dict(label="Service, then software", v=52, hl=True),
                 dict(label="Service", v=51),
                 dict(label="Software, tenancy", v=36),
                 dict(label="Software, maintenance", v=30),
                 dict(label="Engine for platforms", v=24),
             ]),
         ],
         label_w=3.2,
         note="A service client pays about twice as much a year ($39k against $20k) and churns less.",
         src="Source: Handoff analysis, 30,000 runs per path."),

    dict(kind="bars2", kicker="Exit",
         title="Exit odds are close across the leading paths, and every exit is modest",
         panels=[
             dict(title="An exit of $25M or more by month 72", max=10, grid=[0, 5, 10], rows=[
                 dict(label="Service, then software", v=4.5, hl=True),
                 dict(label="Software, tenancy", v=4.0),
                 dict(label="Engine for platforms", v=2.9),
             ]),
             dict(title="Founders take home $5M or more", max=10, grid=[0, 5, 10], rows=[
                 dict(label="Service, then software", v=6.9, hl=True),
                 dict(label="Software, tenancy", v=6.4),
                 dict(label="Engine for platforms", v=4.8),
             ]),
         ],
         note="Median exits for these paths are $4–10M. Venn paid $50M for Zuma in 2026.",
         src="Sources: Handoff analysis, 30,000 runs per path; Venn (GlobeNewswire, Sept 2026)."),

    dict(kind="bars2", kicker="Direction",
         title="Growing deeper into the tenancy beats adding owner projects or maintenance",
         panels=[
             dict(title="$1M in annual revenue by month 36", max=100, rows=[
                 dict(label="Service, depth", v=41, hl=True),
                 dict(label="Service, projects", v=30),
                 dict(label="Software, depth", v=26, hl=True),
                 dict(label="Software, projects", v=19),
                 dict(label="Software, maintenance", v=19),
             ]),
             dict(title="The company fails by month 72", max=100, grid=[0, 50, 100], rows=[
                 dict(label="Service, depth", v=53, hl=True),
                 dict(label="Service, projects", v=74),
                 dict(label="Software, depth", v=63, hl=True),
                 dict(label="Software, projects", v=69),
                 dict(label="Software, maintenance", v=72),
             ]),
         ],
         label_w=3.2,
         note="Maintenance has the largest upside if its upsell works: first on founder proceeds in 27% of draws.",
         src="Source: Handoff analysis, 30,000 runs per path and 300 parameter draws."),

    dict(kind="table", kicker="What would change the ranking",
         title="Three close contests turn on facts that a pilot and a few sales calls can measure",
         head=["Contest", "First wins", "What decides it"], widths=[4.4, 1.8, 5.6], accent_col=1,
         rows=[
             ["Service first against software only", "47%", "Whether tenancy depth works; what software alone "
                                                             "can charge per move-out"],
             ["Engine against software only", "56%", "Whether platforms and deposit insurers buy, and at what "
                                                     "contract size"],
             ["Tenancy depth against maintenance", "50%", "How large the maintenance upsell is, and its churn"],
         ],
         note="Wins are the share of 300 parameter draws in which the first path has higher expected founder "
              "proceeds.",
         src="Source: Handoff analysis, rank correlations across 300 parameter draws."),

    dict(kind="list", kicker="What to take from it",
         title="Lead with a completed move-out, sold per outcome, and convert to software as it is measured",
         items=[
             "**Sell the outcome first.** It gets a paying customer soonest and leads on revenue and funding.",
             "**Grow deeper, not wider.** The move-in record, the turn and the settlement beat owner projects "
                                        "and maintenance.",
             "**Plan for a modest exit.** The likely end is a sale to a larger platform, at $4–10M in the median "
                                        "case.",
         ],
         note="Limits: the odds rest on generic software base rates and judgment ranges, not operator data. Read "
              "the rankings, not the levels.",
         src="Source: Handoff analysis."),
])

# ====================================================================== 4. Settling a NYC move-out

RAIL = 6

LEGAL = dict(short="Settling a NYC move-out", slides=[
    dict(kind="title", kicker="The settlement engine", name="Settling a New York City move-out",
         line="What the law requires of a manager when a market-rate tenant leaves, and how Handoff handles "
              "each step.",
         meta=f"Handoff · {DATE}"),

    dict(kind="journey", kicker="Overview",
         title="A move-out settlement in New York City runs in six steps",
         steps=[
             ("Rent", "Can rent be recovered at all?"),
             ("Deposit", "What is held, and what interest is owed?"),
             ("Charges", "What may be kept, and what never?"),
             ("Statement", "What is due by day 14, and where it goes."),
             ("A miss", "What missing day 14 costs."),
             ("Balance", "Who may collect what is still owed."),
         ],
         note="Handoff's settlement applies every deadline, cap and barred charge for a New York City market-rate "
              "unit, each tied to the statute or decision it comes from."),

    dict(kind="decision", kicker="Which rules apply",
         title="The rules depend on the unit's status and the lease date",
         questions=[
             dict(q="Is the unit rent-stabilized, or under rent control?", exit_style="dark",
                  exit="Different rules apply. Handoff routes the unit to the manager."),
             dict(q="Was the lease signed, renewed or continued on or after July 14, 2019?", exit_style="gate",
                  exit="General Obligations Law § 7-108(1-a): one-month cap, inspections, the 14-day statement, "
                       "forfeiture."),
         ],
         final="The common-law rule and the lease's own return terms.",
         src="NYC Admin. Code § 26-504; N.Y. Gen. Oblig. Law §§ 7-107, 7-108(1), (1-a); N.Y. Laws 2019, ch. 36, "
             "Part M, § 29; N.Y. Real Prop. Law § 232-c."),

    dict(kind="divider", num="Part 1", title="The law, step by step",
         line="What a manager must do at each step, and what Handoff does."),

    dict(kind="lawstep", kicker="Step 1 · Rent", rail=(1, RAIL),
         title="Three building facts decide whether rent can be recovered at all",
         items=[
             "**Certificate of occupancy.** A building built or converted for three or more families after 1929 "
                                          "needs a certificate for that use. Without one, the owner recovers no "
                                          "rent for the period, by suit, setoff or keeping the deposit.",
             "**Registration.** An owner that has not registered with HPD recovers no rent until it does; "
                              "then the rent that built up is owed.",
             "**Rent-impairing violations.** No rent while such a violation stays uncorrected six months after "
                                           "notice, unless the tenant caused it or refused access.",
         ],
         handoff=["Reads the building's certificate, HPD registration and violation record before any rent goes "
                  "on the account.", "A missing fact goes to the manager."],
         src="N.Y. Multiple Dwelling Law §§ 4(7), 301(1), 302(1)(b), 302-a(3), 325(2)."),

    dict(kind="lawstep", kicker="Step 2 · Deposit", rail=(2, RAIL),
         title="The deposit is the tenant's money, held in trust, and often earns interest",
         items=[
             "**Cap.** The deposit plus any advance rent may not exceed one month's rent.",
             "**Trust.** The deposit may not be mixed with the landlord's money. Mixing it forfeits the deposit.",
             "**Interest.** In a building of six or more units, it sits in an interest-bearing New York bank "
                          "account. The landlord may keep 1% a year.",
             "**Move-in record.** If the tenant accepts a joint move-in inspection, nothing on the signed record "
                                "can be charged later.",
         ],
         handoff=["Records the deposit, the bank, who paid which part, and the signed move-in record.",
                  "Code computes the interest owed at the end date."],
         src="N.Y. Gen. Oblig. Law §§ 7-103(1), (2), (2-a), (2-b), 7-108(1-a)(a), (c); Paterno v Carroll, 75 AD3d "
             "625 (2d Dept 2010)."),

    dict(kind="split", kicker="Step 3 · Charges", rail=(3, RAIL),
         title="The deposit may be kept for four things, and never for wear and tear",
         widths=[1, 1.6],
         sides=[
             dict(label="May be kept", items=[
                 "Unpaid rent already due",
                 "Damage beyond normal wear and tear",
                 "Utility charges owed under the lease",
                 "Moving and storing the tenant's belongings",
             ]),
             dict(label="May not be kept", ncol=2, items=[
                 "Wear and tear, or a prior tenant's damage",
                 "Anything noted on the move-in record",
                 "Late fees and other fees",
                 "Legal fees without a court order",
                 "A lease-break sum",
                 "Any fee charged by the agent who leased the unit",
             ]),
         ],
         note="Code bars what the law excludes. The judgment model decides wear and tear or damage.",
         src="N.Y. Gen. Oblig. Law § 7-108(1-a)(b), (c); N.Y. Real Prop. Law §§ 234-a, 238-a; NYC Admin. Code "
             "§§ 20-699.21, 20-699.22 (FARE Act, from June 11, 2025)."),

    dict(kind="lawstep", kicker="Step 4 · Statement", rail=(4, RAIL),
         title="The itemized statement is due 14 days after the tenant vacates, by a channel that reaches them",
         items=[
             "**Counting.** Calendar days, not counting the move-out day. Day 14 on a weekend or public holiday moves "
                          "to the next business day.",
             "**Form.** In writing: a letter, email or text. A phone call does not count.",
             "**Channel.** Use the forwarding address, email or phone on file. Mail to the vacated unit only if "
                         "there is no other channel.",
             "**Estimates.** Allowed if each item is itemized. There is no second statement.",
         ],
         handoff=["Computes the due date from the vacate evidence.",
                  "Sends the statement and refund by a lawful channel and keeps proof of sending."],
         src="N.Y. General Construction Law §§ 20, 25-a; N.Y. Gen. Oblig. Law § 7-108(1-a)(e); Cohen v Abruzzo, 228 AD3d "
             "724 (2024); 14 E. 4th St. v Toporek, 203 AD3d 17 (2022); Pickens v Lane (2023)."),

    dict(kind="bignum", kicker="Step 5 · A miss", rail=(5, RAIL),
         title="A missed deadline forfeits the deposit, and a willful one costs up to twice it",
         big="2×", caption="the deposit, at most, in damages for a willful violation, on top of returning it.",
         items=[
             "**Forfeiture.** A missed statement loses any right to keep the deposit. Intent does not matter.",
             "**Burden.** In a dispute, the landlord proves each amount kept was reasonable.",
             "**Willful.** A court finds it on the record. A manager is held to know the rule; an honest "
                         "process error is not willful.",
             "**The debt survives.** Proven rent and damage can still be claimed separately.",
         ],
         note="Handoff keeps the day-14 clock in front of the coordinator that books the vendor work.",
         src="N.Y. Gen. Oblig. Law § 7-108(1-a)(e)–(g); Prando v Kelly (App Term 2d Dept 2021); Levine v "
             "Xu-Kehrli (2026)."),

    dict(kind="lawstep", kicker="Step 6 · Balance", rail=(6, RAIL),
         title="A balance beyond the deposit is a lease claim, and who collects it decides the rules",
         items=[
             "**Time and interest.** Six years to sue today. Interest runs at 2% a year when the tenant is a "
                                   "person, 9% for a company.",
             "**The owner collecting.** Not a federal debt collector. City rules limit its staff's contacts once "
                                      "collection begins, and tighten in 2027.",
             "**A third party collecting.** Federal debt-collection rules apply after default. An agency needs a "
                                          "city license. Collecting rent for another for a fee needs a broker's "
                                          "license.",
         ],
         handoff=["Recommends whether to pursue, hand off or write off a balance, and shows the net recovery.",
                  "The owner or licensed manager sends the demand and receives the payment."],
         src="N.Y. CPLR §§ 213(2), 5001, 5004; 15 U.S.C. § 1692a(6); NYC Admin. Code § 20-489; N.Y. Real Prop. "
             "Law § 440(1); NYC DCWP debt-collection rule (6 RCNY 5-76, 5-77)."),

    dict(kind="divider", num="Part 2", title="Worked examples",
         line="Three move-outs, and what the law and Handoff do with each."),

    dict(kind="calendar", kicker="Example 1 · The deadline",
         title="Vacated Friday, December 11, 2026: the statement is due Monday, December 28",
         month=(2026, 12),
         marks={11: "vacated", **{d: "count" for d in range(12, 25)}, 25: "skip", 26: "skip", 27: "skip",
                28: "due"},
         counts={d: f"day {d - 11}" for d in range(12, 26)},
         legend=[("vacated", "Vacated"), ("count", "Counted"), ("skip", "Holiday or weekend"), ("due", "Due")],
         items=[
             "**Day 0.** The tenant vacates on Friday, December 11. The move-out day is not counted.",
             "**Day 14.** Friday, December 25, a public holiday. Saturday and Sunday follow.",
             "**Due.** Monday, December 28, the next business day.",
             "**Handoff.** Sets the date in code and schedules vendor evidence to land by about day 10.",
         ],
         src="N.Y. General Construction Law §§ 20, 24, 25-a; N.Y. Gen. Oblig. Law § 7-108(1-a)(e)."),

    dict(kind="example", kicker="Example 2 · A repainting charge",
         title="A painting invoice is not proof of damage",
         cols=[
             dict(label="The move-out", body=["A tenant leaves a walk-up after three years.",
                                              "The painter bills $1,400 to repaint the unit.",
                                              "The tenant painted one bedroom dark red. It needs two extra "
                                              "coats."]),
             dict(label="The law", body=["In a multiple dwelling, the owner repaints every three years.",
                                         "Repainting after ordinary use is wear and tear.",
                                         "Only damage beyond that is charged, at the cost of the extra work."]),
             dict(label="The account", body=["Charged: two extra coats in one bedroom, $220, with the invoice "
                                              "line and photos.",
                                              "Not charged: the $1,400 repaint.",
                                              "The manager sees the basis on the line."]),
         ],
         src="Sources: illustrative amounts; NYC Admin. Code § 27-2013(a), (b)(2); N.Y. Gen. Oblig. Law § 7-108(1-a)(b)."),

    dict(kind="example", kicker="Example 3 · Co-tenants",
         title="Two co-tenants: one statement each, and the refund follows who paid",
         cols=[
             dict(label="The move-out", body=["Two co-tenants paid a $3,000 deposit, $1,500 each, as the "
                                              "landlord's records show.",
                                              "One leaves in month 8. The other leaves at lease end.",
                                              "Lawful deductions: $400."]),
             dict(label="The law", body=["The 14-day clock starts when the last co-tenant leaves.",
                                         "Each co-tenant gets a statement.",
                                         "With records of who paid what, the rest is split in proportion. "
                                         "Without them, the refund is joint."]),
             dict(label="The account", body=["No statement in month 8.",
                                              "Within 14 days of the second move-out: a statement and $1,300 to "
                                              "each.",
                                              "Paying all $2,600 to one would not release the landlord toward "
                                              "the other."]),
         ],
         src="Sources: illustrative amounts; Handoff reading of N.Y. Gen. Oblig. Law §§ 7-103(1), 7-108(1-a)(e) and N.Y. "
             "General Construction Law § 35."),

    dict(kind="divider", num="Part 3", title="How Handoff handles it",
         line="Who sets what in a settlement, and what the manager sees."),

    dict(kind="layers", kicker="Division of work",
         title="Code sets the dates and amounts. A narrow model answers judgment questions. The manager decides",
         bands=[
             dict(name="Code", text="Day 14 with rollover, the deposit cap, interest, barred charges."),
             dict(name="Judgment model", text="Wear and tear or damage? Noted at move-in? Does the invoice cover it?"),
             dict(name="Coordinator", text="Gathers evidence, books vendors before day 14, drafts the statement."),
             dict(name="Manager", style="gate", text="Accepts or changes the whole account once."),
         ],
         note="A judgment never sets an amount or a date, and never discounts a charge."),

    dict(kind="account", kicker="What the manager sees",
         title="Every line on the account shows its rule, evidence, judgment and arithmetic",
         line="Bedroom repaint, two extra coats", amount="$220",
         parts=[
             ("Rule", "Damage beyond normal wear and tear. Gen. Oblig. Law § 7-108(1-a)(b)."),
             ("Evidence", "Move-in record: walls white. Move-out photos. Invoice line 3."),
             ("Judgment", "Tenant damage: a color that needs extra coats."),
             ("Arithmetic", "Two coats at $110 each: $220, kept from a $2,800 deposit."),
         ],
         src="Source: illustrative amounts."),

    dict(kind="compare", kicker="Today and in the pilot",
         title="The turn runs today. The pilot adds the settlement for New York City market-rate units",
         sides=[
             dict(label="Runs today", head="The turn", items=[
                 "**Work.** Notice, plan, vendor quotes, approval, visits, reports, invoices and payment.",
                 "**Records.** Parties, dates, unit condition, invoices and exact amounts.",
             ]),
             dict(label="Delivered in the pilot", head="The settlement", hl=True, items=[
                 "**Checks.** The building facts, the deposit and its interest, and the barred charges.",
                 "**Account.** The account, the statement and refund by day 14, and advice on any balance.",
             ]),
         ],
         note="Stabilized and rent-controlled units go to the manager."),
])

DECKS = {
    "Handoff_Pitch": PITCH,
    "Market_Research": MARKET,
    "Business_Model_Scenarios": SIM,
    "Settling_a_NYC_Move_Out": LEGAL,
}
