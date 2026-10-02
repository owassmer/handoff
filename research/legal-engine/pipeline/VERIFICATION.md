# Interrupted pipeline work: verified state

**Subsequent correction, September 30:** pooled calibration previously omitted source-register structural context for examples outside the target jurisdiction. `triage.calibration_contexts` now uses the corresponding source register without turning gold labels into routing evidence. Five of the seven v2 misses below are recovered by existing structural routes. Two remain: NYC ADC 20-105 and 26-2402. Corrected recall is 481/483 (99.59%), with 56 long positives still reported separately and 128/183 answered negatives set aside. Thresholds, cached model answers and historical routing are unchanged. This is not held-out California validation. The full regression suite passes 64 tests. [Corrected output](verification/calibration_source_context_NY.txt) and [JSON](verification/calibration_source_context_NY.json) preserve the new evaluator version; the original outputs remain intact.

Verified 2026-09-30 at 22:06 UTC. Scope: recover the interrupted implementation's actual state, rerun existing checks, and retain the result. No new jurisdiction harvest, live migration, model call, threshold change, or legal acceptance occurred.

## Implementation and legacy preservation

| Check | Verified result |
|---|---|
| Regression suite | 61 passed in 11.81 seconds |
| Existing Stage A checker | NY 694, NYC 244, VA 277, US 359 rules; zero errors, including cross-file check |
| NYC market-rate review walk | 1,200 in scope: 1,098 cited, 102 explicitly deferred, zero uncited; three additional outside-scope citations |
| Strict legacy register | 3,722 sections pass the register consistency check |
| Export snapshot | All 22 recorded input hashes match live inputs |
| Protected files | All four Stage A files, both routing files and legacy triage output unchanged before/after verification |

The importer tests exercise isolated copies. The exported data and importer are implemented; the live legacy corpus remains in its existing layout. Passing equivalence is not a new acceptance decision. In particular, equivalence uses the legacy hedge vocabulary: the stricter new checker intentionally identifies `VA:business-day-meaning` for the phrase “persuasive only.” That test passes because it expects the finding, not because the finding has been resolved.

## Calibration gate remains open

Cached NY calibration uses 539 positive examples and 183 negative examples. Of the positives, 483 have cached model answers and 56 exceed the model limit and are sent directly to review. There are no other unanswered positives in this run.

| Routing version | Answered positives retained | Answered negatives set aside |
|---|---:|---:|
| v1 | 450/483 (93.17%) | 147/183 |
| v2, current | 476/483 (98.55%) | 128/183 |

The command correctly exits 1. Seven current-v2 misses remain:

- NYC:ADC 20-105
- NYC:ADC 20-699.20
- NYC:ADC 26-2402
- NYC:ADC 26-3001
- NYC:ADC 27-2017
- NYC:RCNY 28 1-01
- US:15 USC 7006

This population differs from the original 315-positive calibration on which v2's thresholds were selected. The old 315/315 result is historical and was not held-out evidence. The expanded result does not undo the subsequent manual register review; it shows that current automated routing is insufficient as a completeness gate.

A separate output measures the **historical routing actually used against NY reviewer labels**: 438 deciding sections, 421 routed to review and 17 set aside. These 17 are not the seven expanded-calibration misses. The expanded positive population combines NY stated rules with function-relevant deciding rows from other jurisdictions; it is not every NY reviewer-positive row.

Next pipeline work must correct routing in a new version, retain these populations separately, and test generalization without treating threshold selection as validation. That is a subsequent stage; no thresholds were altered in this reconciliation.

## Reproduction and retained evidence

Run from `research/legal-engine`:

```sh
python3 -m pytest pipeline/tests -q -p no:cacheprovider
python3 stage_a_check.py stage-a/NY.json stage-a/NYC.json stage-a/VA.json stage-a/US.json
python3 review/check_review.py review/NYC_MARKET_RATE.md
python3 register/check_register.py --strict
PIPELINE_ROOT=/Users/owenwassmer/.hermes/profiles/ferro/cache/scratch/pipeline_import_test python3 -m pipeline calibrate NY --cached-only
```

The last command depends on the saved scratch import and its cached answers, writes its report there, and performs no network call. Durable copies of its text and JSON output are retained in [verification/](verification/). [results.json](verification/results.json) records commands, exit codes, timestamps and hashes. Adapter live reachability was not revalidated in this pass; saved adapter fixtures were tested.
