# Handoff 0-to-1 outcome paths: simulation report

2026-09-28. Model: `model.py`. Calibration: `calibrate.py` -> `calibration.json`. Run: `run.py` -> `results.json`.
Tables: `tables.py` -> `tables.md` (every number below comes from those files). Sources: `SIM.ledger.json` (S1-S9, each
with a verbatim quote) and the lane reports in `../lanes/` (cited as L1-L5 with section).

## What the model is

A monthly Monte Carlo from October 2026 (month 0) to October 2032 (month 72). Each simulated company:

1. Looks for its first paying customer. The monthly chance depends on the shape: selling an outcome, a software tool,
   an engine to platforms, or buying a management firm.
2. Adds customers from founder-led sales, and later from funded sales and referrals. It loses customers to churn and
   hits a market ceiling.
3. After 12 months with 3 or more customers, starts its expansion direction. The expansion grows revenue per customer
   for 36 months if it works; whether it works is drawn once per company.
4. Can have its wedge commoditized: an incumbent bundles it, point tools copy it, or a partner builds it in-house. That
   cuts new sales by 40% and new prices by 25%, and raises churn 30%.
5. Burns cash by funding level. It raises a pre-seed, a seed at $400k+ ARR, and a Series A at $2.5M+ ARR (S9).
   Out of cash, it survives small if gross profit covers its smallest team, otherwise it dies. With no paying customer
   by month 18, it stops.
6. Can be acquired, with the hazard rising by ARR band. Price is the private multiple for its ARR band (S4). Services
   are discounted, and an AI-native premium (S4) applies with a path-specific chance. Founders are paid after a
   1x non-participating preference.

The paths are shape plus direction:

| Path | Shape | Direction after the core |
|---|---|---|
| P1 | Software to managers | Tenancy depth: move-in baseline, turn, evidence-backed settlement |
| P2 | Software to managers | Occupied maintenance |
| P3 | Software to managers | Owner-funded projects (capex, casualty) |
| P4 | Accountable service, priced per outcome | Tenancy depth |
| P5 | Accountable service | Turns plus owner projects |
| P9 | Service first, converts to software once automation is proven | Tenancy depth |
| P6 | Engine sold to platforms and deposit insurers | Settlement and turn engine, revenue share |
| P7 | Engine sold to consolidators | Portfolio transitions |
| P8 | Own the operator | Buy a small management firm and run it on Handoff |

## Where the parameters come from

- Global constants: none of these is pinned by a source. They are calibrated so a generic B2B software company
  (ARPA $12k, 3% monthly churn) reproduces the sourced base rates:

| Base rate | Source | Target | Model |
|---|---|---|---|
| Reach $1M ARR within 3 years of first revenue | S1 ChartMogul | 13% | 13% |
| Reach $1M ARR within 5 years | S1 | 25% | 28% |
| Pre-seed companies that raise a seed | S3 | 45-55% | 41% |
| Seeded companies that raise a Series A within 24 months | S2 Carta | 20% | 19% |
| Seeded companies that fail | S5 PitchBook | ~33% (lifetime) | 11% (within the 6-year window) |

  The last row misses by design. PitchBook counts failures over a company's life; the model stops at month 72, and
  most seeded companies seed around month 30. Treat the model's death rates for funded companies as a floor.

- Client size and turn volume: a median client of 400 doors (L3 C1: 100-2,000), turning 28% a year (L2 §2.9:
  Invitation Homes 22.8%; L5 §2.12: apartments 46.8%). That is about 112 turns per client per year.
- Price per turn:
  - Software: $100-250. L1 shows a $150-400 turn product would take up to a small manager's whole profit; TurnOps
    sells at $19 per report (L5 §2.8).
  - Accountable service: $250-450. It replaces coordination labor that managers already buy: a property-management
    virtual assistant costs $1,800-2,400 a month (L3), and contractor management took 15 hours a week at an NAA
    case-study property (L1).
- Churn: SMB software 3-7% a month (S6). The software paths use 2-4.5%, because they sit inside a workflow. The
  service paths use 1.2-3%, because they are contracted outcomes.
- Gross margin:
  - Software: 65-82%, net of inference cost.
  - Service: 35-65%. Pilot reached 60%; traditional bookkeepers run 25-33% (L5 §2.4).
- Commoditization risk per year:
  - Software, tenancy: 15-35%. Obligo's deposit agent inside every major PMS, TurnOps, My AI Front Desk and AppFolio's
    agents (L2 §2.3-2.4).
  - Maintenance: 25-45%, the most crowded category (L2 §2.3, L0).
  - Accountable service: 8-22%. Incumbents sell tools, not accountability (L2 §2.3).
- Expansion upside and odds:
  - Tenancy depth: +25-70% a year, 50-80% chance it works (L5 §2.3, lifecycle expansion).
  - Maintenance: +40-120% a year but only a 20-45% chance (crowded; fee-manager economics negative, L0, L1).
  - Owner projects: +10-35% a year (capex $840 per unit per year, L1; rarer events).
- Engines:
  - First customer: 2.5-7% a month. Yardi requires two years and three clients before interface partnership, and
    Obligo built its own agent (L2 §2.2, §2.4).
  - Contract size: $60-350k.
  - Acquisition hazard: 1.5-3x the software rate, because partners buy their suppliers (Colleen went to Entrata,
    Zuma to Venn, L2 §2.7).
- Roll-up:
  - Operating economics: 6% margin and $1,809 revenue per door (NARPM via L1); 25% of owners leave a year (L1).
  - AI margin uplift to 12-28%, with a 35-65% chance: General Catalyst's "doubled EBITDA" claim, unproven (L5 §2.6).
  - Acquisition price $1,000-2,000 per door (S7). Licensing takes 3-9 months (unverified).
- Every range above is a judgment inside the evidence. The uncertainty run samples all of them.

## Results

See `tables.md` for the full tables. The headline:

1. **Revenue: the accountable-service shapes are the most likely to get paid.**
   - Chance of a paying customer within 12 months:
     - Service shapes (P4, P5, P9): 88-89%.
     - Software: 76%.
     - Engines: 46-50%.
     - Roll-up: 10%.
   - Across the 300 draws, a service shape ranks first on this goal every time.
2. **Funding: service first on tenancy close-out leads.**
   - $1M ARR by month 36: P9 42%, P4 41%, P1 26%, P2 19%, P6 14%.
   - Seed round: P9 52%, P4 51%, P1 36%.
   - P9 or P4 ranks first on both goals in about 90% of draws.
   - Why: each client pays about twice as much ($39k against $20k a year), churn is lower, and the first customer
     comes sooner. That outweighs the capacity limit of a service.
3. **Exit: a three-way tie, and every outcome is modest.**
   - Exit of $25M or more by month 72: P9 4.5%, P1 4.0%, P6 2.9%.
   - Founders taking home $5M or more: P9 6.9%, P1 6.4%, P6 4.8%.
   - Across the draws, P9, P6 and P1 each rank first on these goals 24-33% of the time.
   - Median exit value for the leading paths: $4-10M. The realistic exit inside six years is a tuck-in sale. That matches L2: point tools
     are absorbed by PMS vendors and platforms, and Venn paid $50M for Zuma.
4. **Direction: tenancy depth beats owner projects in both shapes, on every goal.**
   - Software: P1 beats P3. Service: P4 beats P5.
   - Occupied maintenance (P2) is a higher-variance bet. It reaches fewer milestones and dies more (72% against 63%
     for P1). But it has the fattest upside when the upsell works, so it ranks first on expected founder proceeds in
     27% of draws.
5. **Roll-up does not start without capital.**
   - The binding constraint is financing the first acquisition, not overhead: 10% get one within 12 months.
   - With founder or angel capital: 34%. Even then, exits inside six years are small (median $1.9M), because the value
     needs scale beyond the window. That matches the critics in L5 §2.6.
6. **Founder time outweighs any shape choice.**
   - Part-time until the first round roughly halves everything. For P9:
     - Paying customer within 12 months: 88% to 66%.
     - Seed: 52% to 21%.
     - Any exit: 19% to 8%.

## What decides the close contests

- **P9 against P1** (P9 wins 47% of draws on expected founder proceeds). Decided by:
  - whether the tenancy-depth expansion works (P9's growth);
  - what software alone can charge per turn (P1's ARPA);
  - P1's churn.
- **P6 against P1** (P6 wins 56%). Decided by whether platforms and insurers buy at all, and at what size (P6's
  contract size and buyer arrival rate).
- **P1 against P2** (50/50). Decided by how large the maintenance upsell really is, and maintenance churn.

Each of these is a question a small number of real conversations can answer (see the Next section in the reply).

## Limits

- The levels are calibrated on generic software base rates, not on property technology. Treat the rankings and
  gaps as the result, not the absolute probabilities.
- Every path parameter is a judgment range from the lane evidence. There is no operator data yet.
- Not modelled:
  - switching between paths, except P9's conversion;
  - an IPO;
  - the production platform's cost (Foundry or otherwise);
  - participating preferences, earn-outs and secondaries.
- Commoditization is a single event, not a gradual squeeze.
- Death rates for funded companies are right-censored (see the calibration section).
