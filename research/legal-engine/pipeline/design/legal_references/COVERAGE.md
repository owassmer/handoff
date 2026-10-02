# Coverage reconciliation

Every declared boundary has explicit contract treatment and cases below. Counts overlap and are not independent observations. Case IDs refer to preserved bundles; d IDs span original and extra development, e IDs identify the retired candidate, f IDs identify fresh evaluation. Complete per-case accounting remains in each run’s evaluation.json.

| Boundary | Development examples | Fresh examples | Fresh agreement / answered / total | Treatment |
|---|---|---|---|---|
| Self and focus-size invariance | d001 d002 d011 d012 d042 | f001 f002 f008 f017 f018 | 4 / 5 / 5 | Same section anchor despite focus size; explicit number needs source identity. |
| Enclosing units | d003 d006 | f001 f004 f013 f021 | 3 / 4 / 4 | Read actual hierarchy and relevant scope/definitions. |
| Other sections and substantive headings | d004 d005 d010 d051 | f005 f009 f012 f014 f023 f028 f033 | 7 / 7 / 7 | Identify each pointer, target and version; no automatic effect finding. |
| Relative and subordinate units | d013 d014 | f007 f010 f022 f024 f030 | 3 / 5 / 5 | Resolve against hierarchy; f010 is subordinate relative to the section anchor, not whole-section self. |
| Ranges and multiple mentions | d004 d014 | f001 f007 f009 f024 | 3 / 4 / 4 | Presence does not expand targets or test range validity. |
| Named public authorities | d016 d017 d018 d019 d037 d038 d039 d040 | f014 f034 f035 f036 f037 f038 f039 f040 f041 | 9 / 9 / 9 | Named statutes, regulations, constitutions, treaties, court rules, decisions, orders and official legal guidance count; no authority ranking. |
| Generic law qualifications | d007 d027 d028 d041 | f042 | 1 / 1 / 1 | NO here still leaves agent research needs. |
| Ordinary/private/nonlegal contrasts | d008 d022 d023 d024 d025 d026 d043 d047 d048 d049 d050 | f006 f016 f026 f043 f044 f047 | 6 / 6 / 6 | Private or ordinary meaning controls; inspect private records separately. |
| Readable prose without a pointer | d009 d030 | f003 f011 f020 | 3 / 3 / 3 | Absence of a pointer is not absence of operative law. |
| Quoted references and adversarial instructions | d020 d021 | f046 f047 f048 | 3 / 3 / 3 | Quotes are data; keep errors and inspect the actual text. |
| Mixed passages | d004 d005 d006 d036 d044 | f001 f030 f045 | 3 / 3 / 3 | Any definite public pointer establishes YES; record every individual relationship. |
| Source labels, headings and metadata | d029 d046 d051 d052 | f003 f011 f015 f016 f019 f031 f032 f033 | 6 / 8 / 8 | Recognized locator versus substantive pointer versus unknown role; metadata is outside model state. |
| Damage, truncation and uncertainty | d031 d032 d033 d034 d044 d045 d049 d050 | f025 f026 f027 f028 f029 f030 f031 f048 | 6 / 8 / 8 | Retain uncertainty when presence is undecidable; definite public pointer wins; clear private target does not count. |
| Historical or inapplicable targets | d004 d035 | f017 f023 f034 | 3 / 3 / 3 | Detection does not require validity or applicability; date-qualified federal incorporation demonstrated in source follow-up. |

All 48 fresh cases are reconciled above; no case is excluded from totals. All 100 dev4 development cases are reconciled in the three development run files and independent failure reviews. The original 48-case dev2 run remains separate.

Missing/empty input, source mutation, wrong spans, stale reviews, duplicate IDs, changed frozen labels, and missing responses are preparation/accounting conditions tested in test_reference_experiment.py. They are not fabricated Jev answers.

Raw authored strata are preserved even where terminology predates a clarification: retired e029/e048 retain an old insufficient tag, and fresh f010 uses excerpt_self for a subsection pointer. Neither tag determines labels or the fixed-section relationship convention; this table uses that convention.

Explicit exclusions: general implicit dependency discovery, full target retrieval/interpretation, current-law verification, statewide coverage, production exclusion, non-English performance, representative OCR performance, and comparative productivity. These exceed this presence-contract goal and are not counted as completed. Private-document investigation remains agent work rather than being discarded. Named nonstatutory authorities are tested with authored examples, not claimed as real-source validation.

Per-source dependence is reported in fresh-evaluation-run/grouped.json: 16 real excerpts from six source files, including overlapping whole-section/excerpt cases; 32 authored contrasts. Source families are BPC/FIN/MVC, separate from all development families. Independently authored examples share task concepts by design; they are not statistically independent draws.
