# Reference flags for J1 researchers

The active input is `passage-preparation.json`. It partitions the complete operative §76.802 body into14 passages and CIV1950.5(f) into7. The grain follows paragraphs and subsections; governing introductions remain with dependent lists. Source paths, version notes and offsets are bookkeeping. Jev receives the passage and necessary context, with one fixed question: **Does this passage cite or refer to another document or provision?**

`pipeline.reference_discovery` prepares independent Noul questions together, one answer per passage. Researchers inspect those signals, find the cited texts and reconcile coverage. There is no citation-candidate list, relationship taxonomy, model-driven register mutation or negative-score completeness declaration in this helper.

Run from research/legal-engine:

```sh
.venv/bin/python -m pipeline.reference_discovery j1/references/passage-preparation.json j1/references/passage-run-2 --run --cap .10
```

Use a new output directory for each attempt. The actual October1 `passage-run-1` failed resolving OpenRouter on its first request; the second was not sent. That failed attempt remains saved. With restored network access, passage-run-2 answered all21 passages; followthrough.json records the actual target reconciliation. The cpuc/ directory applies the same question to29 coherent paragraphs/footnotes in the newly recovered modifying order. Scores support research and do not establish instrument completeness. The three focused tests establish partition/source isolation behavior, not semantic adequacy.

`fcc-preparation.json`, `fcc-run-1` and `ca-preparation.json` preserve the superseded citation-selection work. They are not inputs to this method.
