# Stage A source register: market-rate NYC tenancy settlement

Built 2026-09-30. The reviewed findings were applied the same day (`review/REGISTER_DISPOSITION.md`): every section now
carries a reviewer decision, and `check_register.py` runs strict by default. This register makes the universe of law for the chain finite by construction. It holds a closed
list of instruments. Every unit (article, title, part, chapter) of each instrument is either in scope or excluded
with a reason. Every section of every in-scope unit is saved verbatim and has exactly one status. Completeness is
now a script check: `python3 check_register.py` (it passes; output is at the end of this file).

Chain: from facts fixed at move-in and the notice that the tenancy is ending, to the account closed. That
includes collection, suit, judgment, enforcement and write-off, unclaimed funds, bankruptcy, death, military,
disability, domestic violence, coerced debt, tax and information reporting, data and privacy, credit reporting and
anti-discrimination. Scope: NY State, NYC and federal law for a market-rate unit in NYC. Out of aperture:
rent-stabilized and rent-controlled units, public, project-based or subsidized housing, Virginia, places outside
NYC and commercial tenancies.

## Files

| File | What it is |
|---|---|
| `instruments.json` | 63 instruments, each with `units_in_scope` (with headings and section counts), `units_out` (heading and a one-line reason), `toc_source_url` and per-status section counts. It also holds `non_code_sources` (the case law, guidance, forms, session laws and notices named by atoms that cite no code section), `atom_citations_in_out_of_scope_units`, `considered_not_added`, and the rule-file sha256 values. |
| `sections.jsonl` | 3,686 sections: `section_id`, `instrument`, `unit`, `heading`, `text_file`, `chars`, `repealed`. |
| `texts/<instrument>/<section>.txt` | Saved text of every section, each with a SOURCE / RETRIEVED header. All text was extracted mechanically; none was retyped. |
| `match.json` | Step 3 output: for each section, the atom ids that cite it, 4A/5A universe items and 5A gap findings; plus every atom's parsed citations. |
| `triage.jsonl` | For each section: status, reason, routing version, atom ids, universe citations, Jev answers (role, probabilities, confidence, chain_duty, returned model, cache key) or a hand reason. |
| `review_queue.json` | 2,496 sections grouped by instrument, highest P(DECIDES) first, each with its heading, reason and a 300-character excerpt. |
| `jev_questions.json` | The versioned Jev questions (Q1 Choice `role`, Q2 Noul `chain_duty`), global rules, and the chain and exclusion text sent as state. |
| `routing.json` | Routing thresholds v1 and v2 (current), with the reason for the change. |
| `calibration.md`, `calibration.json`, `calibration_negatives.json` | Gold sets, results for every version, the threshold sweep, and the 183 hand-checked negatives. |
| `jev_triage.py` | Jev client: typesafe_sdk through OpenRouter, $2.00 per-run spend cap, 12,000-attempt ceiling, cache and exchange log. |
| `jev_cache/`, `jev_exchanges.jsonl`, `jev_results.jsonl`, `jev_runs.jsonl` | Cached raw responses, every network exchange (the request without credentials plus the raw response), answers per section, and usage per run. |
| `fetch_gaps.json` | Sections without text (none) and instrument-level source limits, with the URLs attempted. |
| `check_register.py` | The completeness check and its self-tests. |
| `tools/` | Fetchers and builders: `nylaw.py`, `harvest_ny.py`, `fetch_ny.py`, `senate_archive.py`, `aml.py`, `usc.py`, `ecfr.py`, `nycrr.py`, `fetch_nycrr.py`, `scope.py` (scope decisions and reasons), `build.py`, `cites.py`, `match.py`, `negatives.py`, `route.py`, `calibrate.py`, `build_outputs.py`. |
| `toc/` | Harvested tables of contents (NY statutes, NYCRR). |

## Method

1. **Instrument register.** I seeded the register from every instrument named in the rule files' provisions and
   in the 4A and 5A universes, then added absent instruments that govern the chain, each with an `added_why`:
   - Debtor and Creditor Law: bankruptcy exemptions for the refund, cancellation of a judgment after discharge,
     setoff.
   - Not-for-Profit Corporation Law and Partnership Law: capacity of foreign landlords to sue.
   - Mental Hygiene Law art. 81: a guardian as payee or party.
   - 18 NYCRR 352: public assistance shelter rules.
   - Regulation E: implements EFTA, which is in scope.
   - 9 NYCRR 540: the ESRA regulations; STT 305 is stated.
   - 24 CFR 5 subpart L: VAWA protections in the voucher program.

   Units were scoped generously. A unit goes to section level unless its heading is plainly outside the chain.
   The RS/RC chapters and parts that decide whether a unit is market-rate are in scope; the rest of the RS/RC
   regimes and all subsidized-housing parts are out with an aperture reason. 12 instruments are registered only
   because rule files cite them for an out-of-aperture regime (24 CFR 966, 960, 880-886, 891, 983, 92; 7 CFR
   3560); all of their units are out. `considered_not_added` lists 11 instruments I weighed and left out, with
   the reason for each.
2. **Sections.** Each source was fetched mechanically. Nothing was retyped, and a saved file is never fetched
   again.

   | Source | Used for | How |
   |---|---|---|
   | newyork.public.law | NY statutes (mirror of nysenate.gov) | Page body extracted; the site's added "pragmatic" cross-reference labels removed so the enacted wording remains |
   | Internet Archive captures of nysenate.gov | NYC Civil Court Act and SCPA (not on public.law) | Each file records the capture URL and the page's "published on" date |
   | American Legal Publishing official bulk XML | NYC Admin. Code and RCNY | RCNY chapters assigned to titles by the XML's global record order |
   | uscode.house.gov USLM XML (release point 119-111) | USC and the FRBP (title 11 appendix) | Notes are dropped, except the PTFA note under 12 USC 5220 |
   | eCFR versioner API | CFR | Full-part XML, dated up-to-date-as-of |
   | Cornell LII | NYCRR | Westlaw's official NYCRR site now walls curl |

3. **Mechanical match** (`tools/cites.py`, `tools/match.py`; code only). Citations are normalized. Subdivisions
   are dropped, so 'GOL 7-108(1-a)(e)' becomes GOL 7-108. Bare numbers inherit the preceding prefix, so 'RPL
   440(1), 440-a' gives both sections. Integer ranges are expanded ('MDL 301-302'), and 'Admin. Code', 'HMC',
   'RSC', '6 RCNY', '11 U.S.C.' and FRBP forms are recognized. Source-file names such as
   `REVIEW5A_NY_GBL_349.txt` are parsed as citations too. A section with at least one atom is `stated`.
4. **Jev triage.** Jev triaged every section that is not stated and is 12,000 characters or shorter, after a
   calibration run. Jev only classifies; it does not state law. Routing is owned by code (`tools/route.py`,
   `routing.json` v2). A section goes to the review queue if any of these holds:
   - P(DECIDES) ≥ 0.15;
   - chain_duty ≥ 0.10;
   - Jev's confidence < 0.7;
   - it is LONG or unfetched;
   - it is a definition or applicability section in a unit with a stated rule;
   - a 4A/5A universe item cites it;
   - Jev returns EXCLUDED_REGIME outside an RS/RC routing unit.

   Otherwise the section is triaged_no_decision, or triaged_excluded (only inside a regime unit).
5. **Outputs and check.** `tools/build_outputs.py` writes the outputs; `check_register.py` verifies them.

## Counts

- **Instruments: 64.** 28 NY, 3 NYC (Admin. Code, RCNY, NYC Civil Court Act) and 33 federal. 52 have in-scope
  units; 12 are out-of-aperture only. The FTC Disposal Rule (16 CFR part 682) was added at adjudication.
- **Units: 291 in scope, 1,443 out**, each out unit with a reason. TILA part B (15 U.S.C. 1631-1651) moved in at
  adjudication.
- **Sections: 3,722**, of which 52 are repealed or reserved. All 3,722 texts are saved; none is unfetched. The 36
  sections added at adjudication (TILA part B, 16 CFR 682) have hand-routed triage rows (no Jev call).
- **Statuses:**

  | Status | Sections |
  |---|---|
  | stated | 312 |
  | review_queue | 2,532 |
  | triaged_no_decision | 878 |
  | triaged_excluded | 0 |
  | unfetched | 0 |

- **Why sections are in the review queue:**

  | Route | Sections |
  |---|---|
  | Jev thresholds | 2,328 |
  | LONG (not sent to Jev) | 108 |
  | Cited by a 4A/5A universe item | 21 |
  | Definition section in a stated unit | 21 |
  | Applicability section in a stated unit | 17 |
  | EXCLUDED_REGIME outside a regime unit | 1 |

- **Review queue by instrument:** CPLR 335; Admin. Code 246; RCNY 176; 11 USC 145; RPAPL 133; 22 NYCRR 102;
  GOL 100; CCA 100; SCPA 100; UCC 95; GBL 92; FRBP 71; RPL 69; 15 USC ch. 41 66; MDL 55; 24 CFR 982 51;
  EPTL 49; GCN 42; SSL 37; ABP 32; Military Law 32; 26 CFR 30; MHL 29; 9 NYCRR 29; SCRA 29; Judiciary Law 23;
  18 NYCRR 23; Reg E 19; 24 CFR 5 19; IRC info returns 17; 24 CFR 100 17; FHA 16; Reg V 16;
  Partnership Law 14; DCL 12; Executive Law 11; CFPA 11; 19 NYCRR 8; 16 NYCRR 7; 23 NYCRR 6; Reg F 6;
  LLC Law 5; N-PCL 5; BCL 4; STT 4; VAWA 3; E-SIGN 2; IRC 166 1; PTFA 1; 47 CFR 64 subpart L 1.
- **Reviewer decisions (every section, check 7):** batches 1-9 decide 3,410 sections (3,374 from batches 1-8, 36 new
  in batch 9; batch 9 also re-decides 26 U.S.C. 6050I, 6050W and 6045, keeping the batch 5 decision in
  `review_history`); the 312 sections stated by citation match carry `review_batch` 'match'. Totals: stated 398,
  partial 133, new_rule 467, no_decision 2,613, excluded_regime 111.
- **Rule-file atoms at build: 690** (after the register review was applied on 2026-09-30: 1,297; NY 694, NYC 244,
  US 359; see `review/REGISTER_DISPOSITION.md`). The figures below describe the build.
  - 531 cite at least one in-scope section.
  - 130 citations point to sections in out-of-aperture units: RSC and RC parts, subsidized-housing CFR parts,
    MDL art. 7-B. They are listed in `instruments.json`.
  - 76 atoms cite no code section. Their 47 instrument strings are classed in `non_code_sources`.

## Jev usage and spend

- **Model and requests.** `typesafe/jev-1.13` through `https://openrouter.ai/api`; every response returned
  `typesafe/jev-1.13-20260917`. There were 3,582 requests (3,582 physical attempts, no retries, no errors) over
  5 runs.
- **Spend.** $0.279 in total, against a $2.00 cap per run. The largest run, the full triage, cost $0.235.
- **Records.** 3,582 cache files and 3,582 logged exchanges.
- **Key handling.** The key is read at runtime from the environment or `/Users/owenwassmer/dev/Slope_Sparse_Events/.env`.
  I searched every register file for it and found none.

## Calibration (full detail in calibration.md)

- **Gold sets.** Positives: 315 (312 stated plus 3 cited only in 5A gap findings). Negatives: 183, hand-checked.
- **v1 thresholds (P(DECIDES) 0.15, chain_duty 0.30, confidence 0.7):** recall 301/315 (95.6%); negatives
  triaged away 152/183 (83.1%). calibration.md lists the 14 misses with their probabilities.
- **v2 (current):** recall **315/315**; negatives triaged away **127/183 (69.4%)**.
  - Changes: chain_duty threshold lowered to 0.10, plus the universe, applicability and EXCLUDED-outside-regime
    routes.
  - Jev-only recall under the v2 thresholds is 273/277.
- **Limits.** I chose the thresholds on the same gold set, so there is no held-out estimate.

## Rule-file hashes (sha256, verified unchanged by check_register.py)

Refreshed by `build/apply_register_6.py` after the register review was applied (2026-09-30):

- `stage-a/NY.json` 694 rules: `669e13cf98dc7467772ecf66dc658b8bb6c2ad20e626922211e1264270afd2e8`
- `stage-a/NYC.json` 244 rules: `b30841c4f6cb235c1c4a81c02724080fc225aab4943df3d1fb99b1eb2a139b9e`
- `stage-a/US.json` 359 rules: `e989ff5c34ca662ae958d1f20a8752c5118f6567278d45d237591b1b6e6e2b43`

## Known gaps and limits

- **Source currency** (see `fetch_gaps.json`):
  - The CCA and SCPA texts come from Internet Archive captures (2025-04 to 2026-01). nysenate.gov, its API,
    Justia, FindLaw and the Assembly LAWS site all refuse curl and the browser.
  - The NYCRR texts come from Cornell LII, which updates quarterly.
  - NY statutes come from the public.law mirror (last accessed 2026-09-26).
  - Future-effective text is not in the register: the SHIELD Rule amendments to 6 RCNY 5-76/5-77, effective
    2027-01-01, and pending bills.
- **Review queue size.** The queue holds 2,496 sections, 74% of the non-stated ones. This follows from generous
  unit scope, deliberately asymmetric routing and low Jev confidence. The sweep in calibration.md shows the
  trade-off: a 0.30 chain_duty threshold would queue 1,948 sections but miss 4 positives.
- **Not triaged by Jev.** 108 non-stated sections longer than 12,000 characters are in the queue as LONG.
- **Heuristic routes.** Definition and applicability sections are recognized by heading pattern.
- **Scope decisions are mine.** Out-unit reasons are specific for units adjacent to the chain and generic (the
  heading is quoted) for the rest. The RS/RC operative parts and all subsidized-housing parts are out by
  aperture, so the stated atoms on those parked regimes point outside in-scope units.
- **Case law is not enumerable.** Only code sections are in the register; case-law atoms appear only as
  non-code sources.
- **Rebuilding.** A rebuild uses the source caches under the profile scratch folder (XML zips, archive pages,
  raw HTML), which is pruned after 24 hours idle. Saved texts and every output stay in this folder.

## Surprising

The queue contains 56 sections that no rule states and neither review universe cites, which Jev scored
P(DECIDES) ≥ 0.9 and chain_duty ≥ 0.8. They are the first candidates for the next adjudication:
- Admin. Code 26-3402 (limitation of fees associated with vacating a premises);
- GOL 15-106 (death of a joint obligor) and GOL 5-519;
- RPL 227-b (termination by senior citizens) and RPL 231 (lease void for unlawful use);
- CPLR 5003 (interest upon judgment), CPLR 5230 and 5232;
- GBL 380-b and 380-l (NY Fair Credit Reporting Act);
- RPAPL 753 and 755 (stays of rent actions);
- 50 USC 3913 (protection of persons secondarily liable, such as guarantors), 3933 and 3934;
- 28 RCNY 12-02 and 12-08 (occupant duties for smoke and CO alarms).

A high Jev score is a routing signal, not a finding of law; each needs adjudication against its text.

## Reproduce

```
python3 tools/harvest_ny.py                    # NY tables of contents (public.law)
python3 tools/fetch_ny.py --budget 360         # NY section texts (rerun until 'complete')
python3 tools/senate_archive.py fetch CCA A1 A2 A3 A4 A8 A9 A14 A15 A16 A18 A18-A A19 A21
python3 tools/senate_archive.py fetch SCP A1 A7 A10 A11 A13 A16 A17 A17-A A18 A21
python3 tools/fetch_nycrr.py --budget 360
python3 tools/build.py                         # instruments + sections (NYC XML, USLM, eCFR texts saved here)
python3 tools/match.py                         # Step 3
python3 tools/negatives.py                     # gold negatives
.../scratch/jevenv/bin/python jev_triage.py run --set calibration
python3 tools/calibrate.py
.../scratch/jevenv/bin/python jev_triage.py run --set triage
python3 tools/build_outputs.py
python3 check_register.py
```

## check_register.py output (2026-09-30, after the register review was applied; strict mode)

```
Status counts:
  stated                 312
  review_queue           2532
  triaged_no_decision    878
  triaged_excluded       0
  unfetched              0
  total                  3722

Per instrument (sections: stated / review_queue / triaged_no_decision / triaged_excluded / unfetched):
  NY:ABP                    44:    6 /   32 /    6 /   0 /  0   units in 3, out 11
  NY:BCL                    21:    1 /    4 /   16 /   0 /  0   units in 1, out 17
  NY:CPLR                  395:   32 /  335 /   28 /   0 /  0   units in 25, out 48
  NY:DCL                    12:    0 /   12 /    0 /   0 /  0   units in 4, out 9
  NY:EPTL                   77:    0 /   49 /   28 /   0 /  0   units in 11, out 13
  NY:EXEC                   17:    2 /   11 /    4 /   0 /  0   units in 1, out 80
  NY:GBL                   273:   15 /   92 /  166 /   0 /  0   units in 8, out 139
  NY:GCN                    90:    9 /   42 /   39 /   0 /  0   units in 6, out 3
  NY:GOL                   145:   16 /  100 /   29 /   0 /  0   units in 22, out 15
  NY:JUD                    51:    3 /   23 /   25 /   0 /  0   units in 1, out 40
  NY:LLC                    27:    2 /    5 /   20 /   0 /  0   units in 2, out 11
  NY:MDL                    80:    7 /   55 /   18 /   0 /  0   units in 8, out 10
  NY:MHY                    44:    0 /   29 /   15 /   0 /  0   units in 1, out 23
  NY:MIL                    41:    6 /   32 /    3 /   0 /  0   units in 1, out 10
  NY:NPCL                   21:    0 /    5 /   16 /   0 /  0   units in 1, out 16
  NY:PTR                    82:    0 /   14 /   68 /   0 /  0   units in 2, out 9
  NY:RPAPL                 148:    8 /  133 /    7 /   0 /  0   units in 9, out 18
  NY:RPL                   145:   43 /   69 /   33 /   0 /  0   units in 5, out 21
  NY:SSL                    72:    1 /   37 /   34 /   0 /  0   units in 1, out 37
  NY:STT                     9:    3 /    4 /    2 /   0 /  0   units in 1, out 4
  NY:UCC                   104:    1 /   95 /    8 /   0 /  0   units in 11, out 12
  NY:CCA                   115:    7 /  100 /    8 /   0 /  0   units in 13, out 7
  NY:SCPA                  123:    4 /  100 /   19 /   0 /  0   units in 10, out 19
  NY:9NYCRR                 53:    8 /   29 /   16 /   0 /  0   units in 4, out 34
  NY:19NYCRR                29:    1 /    8 /   20 /   0 /  0   units in 1, out 7
  NY:22NYCRR               137:    1 /  102 /   34 /   0 /  0   units in 2, out 14
  NY:23NYCRR                 7:    1 /    6 /    0 /   0 /  0   units in 1, out 12
  NY:16NYCRR                 9:    1 /    7 /    1 /   0 /  0   units in 1, out 14
  NY:18NYCRR                39:    0 /   23 /   16 /   0 /  0   units in 1, out 11
  NYC:ADC                  325:   47 /  246 /   32 /   0 /  0   units in 36, out 364
  NYC:RCNY                 263:   10 /  176 /   77 /   0 /  0   units in 24, out 247
  US:11USC                 170:   13 /  145 /   12 /   0 /  0   units in 16, out 15
  US:FRBP                   74:    1 /   71 /    2 /   0 /  0   units in 4, out 6
  US:15USC-ch41            124:   16 /   97 /   11 /   0 /  0   units in 6, out 5
  US:15USC-ch96              6:    3 /    2 /    1 /   0 /  0   units in 1, out 2
  US:42USC-ch45             24:    2 /   16 /    6 /   0 /  0   units in 2, out 0
  US:50USC-ch50             44:   10 /   29 /    5 /   0 /  0   units in 7, out 2
  US:47USC227                1:    1 /    0 /    0 /   0 /  0   units in 1, out 1
  US:26USC-6041-6050        41:    3 /   17 /   21 /   0 /  0   units in 1, out 5
  US:26USC166                1:    0 /    1 /    0 /   0 /  0   units in 1, out 1
  US:12USC5481              18:    1 /   11 /    6 /   0 /  0   units in 3, out 5
  US:12USC5220note           1:    0 /    1 /    0 /   0 /  0   units in 1, out 0
  US:34USC-VAWA              6:    1 /    3 /    2 /   0 /  0   units in 1, out 1
  US:12CFR1006              19:   13 /    6 /    0 /   0 /  0   units in 4, out 0
  US:12CFR1005              24:    0 /   19 /    5 /   0 /  0   units in 2, out 1
  US:12CFR1022              26:    2 /   16 /    8 /   0 /  0   units in 5, out 6
  US:24CFR100               23:    4 /   17 /    2 /   0 /  0   units in 6, out 2
  US:24CFR982               58:    5 /   51 /    2 /   0 /  0   units in 7, out 5
  US:24CFR5                 21:    0 /   19 /    2 /   0 /  0   units in 3, out 10
  US:47CFR64L                5:    1 /    1 /    3 /   0 /  0   units in 1, out 29
  US:26CFR1-info            33:    1 /   30 /    2 /   0 /  0   units in 1, out 0
  US:24CFR966                0:    0 /    0 /    0 /   0 /  0   units in 0, out 2
  US:24CFR960                0:    0 /    0 /    0 /   0 /  0   units in 0, out 7
  US:24CFR880                0:    0 /    0 /    0 /   0 /  0   units in 0, out 4
  US:24CFR881                0:    0 /    0 /    0 /   0 /  0   units in 0, out 4
  US:24CFR882                0:    0 /    0 /    0 /   0 /  0   units in 0, out 4
  US:24CFR883                0:    0 /    0 /    0 /   0 /  0   units in 0, out 4
  US:24CFR884                0:    0 /    0 /    0 /   0 /  0   units in 0, out 2
  US:24CFR886                0:    0 /    0 /    0 /   0 /  0   units in 0, out 2
  US:24CFR891                0:    0 /    0 /    0 /   0 /  0   units in 0, out 6
  US:24CFR983                0:    0 /    0 /    0 /   0 /  0   units in 0, out 8
  US:24CFR92                 0:    0 /    0 /    0 /   0 /  0   units in 0, out 12
  US:7CFR3560                0:    0 /    0 /    0 /   0 /  0   units in 0, out 17
  US:16CFR682                5:    0 /    5 /    0 /   0 /  0   units in 1, out 0

Reviewer decisions (strict): excluded_regime 111, new_rule 467, no_decision 2613, partial 133, stated 398; batches 1-9 3410, match 312

Self-test planted unclassified section: caught (2 errors raised)
Self-test planted bad atom id:         caught (1 errors raised)
Self-test planted undecided section:   caught (strict check 7)

PASS: every section of every in-scope unit has a status and a reviewer decision; every atom id named exists; every triaged section carries a Jev record or hand reason; every instrument named in an atom provision is registered. (strict)
```
