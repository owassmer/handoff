# Independent evaluation design — legal-reference-presence-1-dev2

Prepared against the fixed `question.v1-dev2.json`, `GOAL.md`, and the serialization/source checks in `experiment.py`. The author did not inspect development examples, their labels, reviews, model outputs, prior pilot examples, or AGENT_GUIDE. No model calls were made. This is a deliberately constructed boundary evaluation, not a representative sample of legal passages or a calibration study.

## Artifacts and separation

`evaluation.cases.json` contains 48 cases: 14 exact saved-source excerpts and 34 explicitly authored examples. `evaluation.author_labels.json` separately contains author expectations and reasons. It is not an independent second-review result or final adjudication. Give the second reviewer only the fixed question, goal, and cases; reconcile author/reviewer disagreements before freeze and model execution. Expected answers must never enter state.focus or other Jev input.

Only these three evaluation files were written by this author. Cases are numbered e001–e048. Source excerpts were verified against raw-file SHA-256 and decoded UTF-8 Unicode character offsets: `full[start:end] == text`. Offsets are not byte offsets. Source headings and retrieval wrappers are excluded from each real-source focus. No assertions of present legal validity, applicability, successful remote retrieval, or authoritative completeness follow from the saved excerpts.

## Saved-source families

Nine files supply fourteen excerpts:

| Family | Files | Cases |
| --- | --- | --- |
| California Code of Civil Procedure | 12, 116.110, 116.220, 339, 685.010 | e001–e008 |
| Huntington Beach Municipal Code, Chapter 17.10 | 17.10.010, 17.10.070, 17.10.080 | e009–e011 |
| California Government Code | 12955 | e012–e014 |

All paths live under `jurisdictions/CA/texts/CA_CCP/`, `jurisdictions/CA/texts/CA_GOV/`, or `jurisdictions/CA-HB/texts/CA-HB_HBMC/`. These source families differ from the declared development families CIV Title 1.6C and CIV Title 5. The saved CA-HB text itself names the Civil Code and Penal Code, but its source family remains the municipal ordinance. Textual target-name overlap is intentional detection coverage, not source-family reuse. The author cannot certify exact textual nonoverlap with unseen development material; the freeze owner should compare identities mechanically if needed without exposing development labels to the author/reviewer.

The real-source cases retain line breaks, curly quotation marks, list markers, and original wording. Multiple excerpts from CCP 116.220 and GOV 12955 are correlated and must not be treated as independent observations. e002, e009, and e011 supply complete substantive section bodies (excluding source headings and history notes); e011 exercises a complete legal section with no internal legal pointer. The real-source definition in e008 does not gain a pointer from its excluded statutory heading.

## Authored groups

Every e015–e048 case carries `authored: true`. These are constructed passages, not assertions about real law. Named instruments, courts, citations, events, and quoted notices are invented or illustrative; no existence or effect is asserted, including the realistic C.F.R. citation. Authored examples intentionally distinguish presence from validity and target resolution.

| Contrast group | Cases | Distinction exercised |
| --- | --- | --- |
| Focused provision versus manual | e015–e016 | Whole-section self-reference and nonlegal use of section/provision |
| Enclosing title versus chart title | e017–e018 | Legal unit versus ordinary heading |
| Act and preceding subsection versus ordinary act | e019–e020 | Enclosing/relative pointers and conduct homonym |
| Quoted notices | e021–e022 | Explicit legal pointer versus generic legal qualification inside quotation |
| Private lease and mixed incorporation | e023–e024 | Private-only reference versus private passage also naming a public legal unit |
| Generic law, range, isolated citation, body reference | e025–e028 | Identified units, unresolved targets, and heading ambiguity |
| Truncation and unreadable remainder | e029–e033 | Incomplete undecidable text, readable no-pointer control, and definite-pointer precedence |
| Unknown document and two completions | e034–e036 | Ambiguous legal/private sense versus explicit ordinance or warranty context |
| Named public authorities | e037–e043 | Regulation, constitution, treaty, court rule, judicial decision, judicial order, official legal guidance |
| Guidance provenance | e043–e044 | Official legal guidance versus landlord internal policy guidance |
| Invalidity/applicability wording | e045 | Named statute explicitly described as repealed and inapplicable |
| Quoted instruction attempts | e046–e047 | Quoted instructions treated as data, with/without an actual pointer |
| Isolated unit heading with range | e048 | Unit identifier cannot establish a body reference by itself |

## Boundary coverage and limits

- Self and focused whole-section: e006, e012, e015. Enclosing chapter/title/Act/part: e002, e006, e009, e012, e017, e019, e021.
- Other/subordinate/relative provisions: e003, e005, e010, e014, e019, e021, e024, e026, e028. Targets absent or unresolved: e003, e026, e028, e038. Ranges: e005, e026, e048.
- Definitions versus definition pointers: e006, e008, e009. Exceptions and scope language: e003, e005, e019. Multiple simultaneous references: e006, e010, e012; the single presence answer does not classify these into exclusive relationship types.
- Mixed private/public or complete/incomplete content: e024, e030, e033. Ordinary words and private/nonlegal documents: e001, e007, e016, e018, e020, e023, e036, e044.
- Generic legal qualifications: e001, e004, e011, e022, e025. Readable legal language without a pointer: e007, e008, e013, e032.
- Quoted notice/content and instruction-like content: e021–e022, e046–e047. Target validity and legal applicability must not change presence: e019, e037–e045.
- Source metadata outside focus: e001, e008, e011, e013. A source identity can be known to the harness while remaining unavailable to the classifier. Isolated identifiers inside focus: e027, e048. Genuine uncertainty: e029, e031, e034 in addition to the isolated identifiers.

Empty, absent, non-string, or whitespace-only focus cannot be valid benchmark cases because `make_requests` rejects them before model execution. They require preparation/transport regression tests outside this semantic evaluation; they must not be mislabeled as model INSUFFICIENT answers. This set does not test retrieval, target version resolution, legal interpretation, next-action execution, or production exclusion routing. Those requirements need separate workflow evidence. A negative presence classification cannot terminate broader research.

## Review edges retained before freeze

The author considers the fixed contract sufficient to label the set, but retains hard cases for independent adjudication rather than smoothing them away:

1. e029 has explicit statutory context but ends with the word Section and no complement. The contract specifically discusses bare cut-off words when their public-legal sense cannot be established; here that sense is clear while the unit pointer itself remains incomplete. The reviewer should decide whether the general incompleteness rule resolves this or whether it is a material uncovered distinction.
2. e031 has an explicitly unreadable remainder and no visible pointer, whereas e032 completes the sentence without a pointer and e033 has a definite pointer before damage. The reviewer should apply the wording about damage preventing a decision without inventing a hidden reference.
3. e034 explicitly states that the document identity is missing, making public/private nature uncertain; e028 is a conventional numbered legal body reference with an unresolved code. The distinction is uncertainty about legal nature versus uncertainty about target resolution.
4. e048 looks like a source heading. The fixed contract expressly assigns uncertainty to isolated identifiers lacking body-reference wording; this should be assessed against that rule rather than inferred source provenance.

Any material unresolved ambiguity blocks freezing that case under `experiment.freeze`. If evaluation content informs a subsequent question/input-policy revision, this evaluation must be retired to development and replaced, as GOAL requires. Keep disagreements and failed/unanswered executions in historical accounting. Overlapping strata are useful boundary diagnostics but do not support independent sample counts or broad accuracy claims.
