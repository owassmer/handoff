# Calibration of Jev triage routing (Stage A source register)

2026-09-30. Data: `calibration.json` (every version evaluated, one row per gold section with Jev's answers),
`calibration_negatives.json` (hand-checked negatives), `routing.json` (every threshold version), `tools/calibrate.py`.
Jev: `typesafe/jev-1.13` through OpenRouter; every answer returned model `typesafe/jev-1.13-20260917`.

## Gold sets

- **Positives: 315 sections.** The 312 sections stated by at least one rule-file atom (provision or source_file),
  plus 3 sections cited only in a 5A gap finding: CPLR 1201, 26 USC 166, 26 CFR 1.6041-1. They are routed as if
  not stated. 277 were sent to Jev; 38 are longer than 12,000 characters and go to the review queue as LONG
  without a Jev call.
- **Negatives: 183 sections** from in-scope units of 17 instruments (GBL art. 26, 22 NYCRR 202, 6 RCNY ch. 6
  penalty schedules, IRC information returns, 26 CFR, 11 USC, FRBP Part IX, EFTA, FCRA, Fair Housing Act,
  SSL art. 5 title 1, EPTL art. 11, MHL art. 81, CPLR art. 45, Judiciary Law art. 15, Reg V appendices, SCRA).
  I checked each by hand: I read the heading against the chain, and I read the text where the heading did not
  settle it. Each has a one-line reason. None is stated by a rule or cited in a 5A gap finding, and all are
  12,000 characters or shorter.

## Versions

| Version | Q1 P(DECIDES) ≥ | Q2 chain_duty ≥ | Q1 confidence < | Other review-queue routes | Recall on positives | Negatives triaged away |
|---|---|---|---|---|---|---|
| v1 | 0.15 | 0.30 | 0.70 | LONG, unfetched, definition section in a unit with a stated rule | **301/315 (95.6%)** | 152/183 (83.1%) |
| v2 (current) | 0.15 | **0.10** | 0.70 | v1 routes, plus: an applicability section in a unit with a stated rule; any section cited by a 4A/5A universe item; EXCLUDED_REGIME outside a regime unit goes to the queue | **315/315 (100%)** | **127/183 (69.4%)** |

Under both versions, a section is triaged away only when Jev is confident on both questions: Q1 is NO_DECISION or
EXCLUDED_REGIME, confidence ≥ 0.7, P(DECIDES) below the threshold and chain_duty below the threshold.

### v1 misses (14), with Jev's answers

| Section | Route under v1 | Q1 | P(DECIDES) | conf | chain_duty | What v2 does |
|---|---|---|---|---|---|---|
| GCN 35 | triaged_no_decision | NO_DECISION | 0.01 | 0.98 | 0.11 | Q2 ≥ 0.10 |
| LLC Law 206 | triaged_no_decision | NO_DECISION | 0.01 | 0.98 | 0.05 | cited by U5A-147 |
| RPL 212 | triaged_no_decision | NO_DECISION | 0.07 | 0.90 | 0.15 | Q2 ≥ 0.10 |
| RPL 232-b | triaged_excluded | EXCLUDED_REGIME | 0.01 | 0.97 | 0.29 | EXCLUDED outside a regime unit → queue |
| RPL 441-c | triaged_no_decision | NO_DECISION | 0.09 | 0.87 | 0.22 | cited by U5A-063; Q2 |
| RPL 442 | triaged_no_decision | NO_DECISION | 0.07 | 0.90 | 0.10 | Q2 ≥ 0.10 |
| STT 305 | triaged_no_decision | NO_DECISION | 0.13 | 0.80 | 0.15 | cited by U083/U5A-112; Q2 |
| SCPA 1305 | triaged_no_decision | NO_DECISION | 0.11 | 0.83 | 0.29 | cited by U155; Q2 |
| SCPA 1802 | triaged_no_decision | NO_DECISION | 0.11 | 0.84 | 0.26 | cited by U156/U5A-138; Q2 |
| Admin. Code 26-414 | triaged_excluded | EXCLUDED_REGIME | 0.05 | 0.88 | 0.27 | Q2 ≥ 0.10 |
| Admin. Code 26-520 | triaged_excluded | EXCLUDED_REGIME | 0.02 | 0.91 | 0.27 | Q2 ≥ 0.10 |
| Admin. Code 27-2097 | triaged_no_decision | NO_DECISION | 0.10 | 0.84 | 0.17 | cited by U5A-260; Q2 |
| 28 RCNY 1-01 | triaged_no_decision | NO_DECISION | 0.00 | 0.98 | 0.07 | applicability section in a stated unit |
| 24 CFR 982.404 | triaged_excluded | EXCLUDED_REGIME | 0.00 | 0.99 | 0.28 | EXCLUDED outside a regime unit (the voucher program is inside the aperture) |

v2 has no misses.

### How much of the recall comes from Jev

- Under v2 the routing rules are applied in order, and 194 of the 315 positives reach the queue through the
  universe rule before Jev is consulted. For each positive sent to Jev, I also scored it with the v2 thresholds
  alone. **Jev-only recall is 273/277 (98.6%).** The four that Jev alone would triage away are LLC Law 206
  (chain_duty 0.05), RPL 440 (0.08), Admin. Code 20-699.20 (0.08) and 28 RCNY 1-01 (0.07). The universe,
  definitions and applicability routes catch all four.
- Jev's miss pattern: sections that fix capacity to sue, licensing or definitions that other rules depend on.
  Jev reads each of them as administrative or definitional.

### Threshold sweep

The structural routes of v2 are kept in every row. "Full queue" is the review queue over all 3,374 sections not
stated by a rule.

| Q2 ≥ | P(DECIDES) ≥ | Positives in queue | Negatives triaged | Full queue |
|---|---|---|---|---|
| 0.30 | 0.15 | 311/315 | 152/183 | 1,948 |
| 0.25 | 0.15 | 313/315 | 152/183 | 1,972 |
| 0.20 | 0.15 | 313/315 | 152/183 | 2,031 |
| 0.15 | 0.15 | 313/315 | 149/183 | 2,158 |
| **0.10** | **0.15** | **315/315** | **127/183** | **2,496** |
| 0.10 | 0.10 | 315/315 | 126/183 | 2,520 |

## Caveats

- I chose the thresholds on the same gold set they are scored on. There is no held-out estimate, so recall on
  sections unlike the positives is not measured.
- The positives cluster in the deposit, statement, collection and suit core. Corners the rules do not reach yet
  are the reason for the register, and they are under-represented in this measurement.
- On the full population, the queue is large (74% of non-stated sections). It is driven by low Jev confidence:
  1,130 queued sections have P(DECIDES) ≥ 0.15 together with confidence below 0.7. Units were scoped generously,
  and routing is deliberately asymmetric.
- No section was triaged_excluded under v2. EXCLUDED_REGIME triage is allowed only inside the RS/RC routing
  units, and the non-stated sections there all carry chain_duty ≥ 0.10.
