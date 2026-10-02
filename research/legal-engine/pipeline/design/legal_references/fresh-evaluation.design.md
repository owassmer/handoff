# Fresh independently authored task evaluation

Prepared September 30, 2026 against `question.v1-dev4.json`. This is a fresh task evaluation, not a representative benchmark or human legal review. It cannot establish legal applicability, comprehensive dependency recall, calibrated probabilities, production exclusion safety, or statewide coverage.

## Independence and preparation

The author read only the permitted question, GOAL.md, experiment.py, and saved source text files discovered under research/legal-engine. No development cases, earlier evaluation cases, reviewer reports, AGENT_GUIDE, FOLLOW_UP, or previous pilot contents were read. No model calls were made. Only the three fresh-evaluation files were written. Author labels are provisional and must remain separate from a blind reviewer until the reviewer has independently labeled all cases. These artifacts are not frozen execution inputs yet.

There are 48 cases: 16 exact saved-source excerpts and 32 newly authored contrasts. Provisional author counts are 31 YES, 13 NO, and 4 INSUFFICIENT. The composition deliberately emphasizes difficult boundaries and is not prevalence weighted. The authored cases explicitly mark invented statutes, public authorities, contracts, and quotations as fictional where applicable. Neutral damaged fragments and isolated identifiers do not purport to identify real authorities.

The real passage families are CA_BPC, CA_FIN, and CA_MVC. No CIV Title 1.6C, CIV Title 5, CCP, GOV, or CA-HB source passage was used. No chosen excerpt happens to contain a pointer into those excluded families either, but that is not a requirement for source-family independence. The BPC Securities Exchange Act passage preserves an actual cross-instrument pointer. Discovery displayed the permitted BPC/FIN/MVC source files in full, including some unselected references into other codes; those targets are not additional evaluation source families.

Each saved excerpt records the relative path, SHA-256 of raw file bytes, and half-open Unicode character offsets. Construction checked all 16 hashes and slices against the current files. Newlines and typographic Unicode inside selected spans remain exact. Source URLs, retrieval dates, file names, and surrounding omitted statutory text are outside focus and cannot supply a positive answer.

## Dependence groups

Saved excerpts from the same original file are a related group, not independent observations:

- `jurisdictions/CA/texts/CA_MVC/409.3.txt`: f001, f002, f003
- `jurisdictions/CA/texts/CA_BPC/10131.txt`: f004, f015
- `jurisdictions/CA/texts/CA_BPC/10133.txt`: f005, f006
- `jurisdictions/CA/texts/CA_BPC/10145.txt`: f007, f008, f014, f016
- `jurisdictions/CA/texts/CA_FIN/100000.5.txt`: f009, f010
- `jurisdictions/CA/texts/CA_FIN/100002.txt`: f011, f012, f013

The complete MVC section in f001 overlaps f002 and f003. This intentional relationship tests what changes when a complete unit, a self-referencing excerpt, or a reference-free excerpt is focused. Whole-unit f001 has additional enclosing and cross-pointers, so it does not isolate self-reference on its own. Authored f017–f020 supplies the isolating four-way comparison: complete unit with self-pointer, excerpt with self-pointer, complete unit without body pointer, excerpt without pointer.

The other source groups similarly exercise distinct spans of a shared source. BPC 10145 contains excerpt-self, relative range, named public statute, and private-document-negative spans. FIN 100002 contrasts a definition with no pointer, a numbered cross-pointer, and an enclosing-chapter pointer. The apparent increase in case count is not an increase in independent source diversity. Report grouped results alongside per-case and overlapping-stratum counts.

## New authored contrast groups

- f017–f020: complete statutory unit and excerpt, with and without self-reference.
- f021–f024: enclosing title, unresolved relative provision, expressly inapplicable former provision, and subdivision range.
- f025–f030: established public cut-off, established private cut-off, unresolved cut-off, recognizable completed citation before truncation, sole possible pointer lost to damage, and surviving pointer despite damage.
- f031–f033: isolated identifier, source-heading range, and substantive exception heading.
- f034–f041: fictional named statute, constitution, treaty, court rule, decision, court order, official legal guidance, and regulation.
- f042–f045: generic law/order invocations, ordinary performance title, private instrument with legal-sounding names and range, and mixed public/private references.
- f046–f048: quoted adversarial classification commands paired with a definite public pointer, a definite nonlegal target, and an ambiguous cut-off. The quoted commands must be treated only as data.

## Review attention and limitations

The author found no necessary contract revision, but asks the blind reviewer to examine these demanding applications explicitly after independently labeling:

- f019: whether a complete fictional section identifier followed by its body is recognizably a source label, rather than an isolated identifier. The provisional label treats it as a source label and checks the body for a pointer.
- f029: whether missing text occupying the only possible pointer location justifies INSUFFICIENT. The provisional label does not infer that the erased words actually named a provision.
- f042: generic court orders and binding regulations are intentionally unnamed, with no specific legal unit. The named order in f039 is its positive contrast.
- f043–f044: legal-looking names are explicitly assigned to performances/private instruments; the surrounding target definition controls.
- f048: an instruction embedded in a quote cannot resolve an otherwise ambiguous public/private cut-off.

These are review attention points, not permission to silently change labels after observing model output. Record any reviewer disagreement and adjudicate against the frozen question before executing evaluation. Retire inputs to development if they cause a question revision.

Unresolved relative targets are intentionally not researched: detection does not require target resolution. Legal authenticity of fictional authorities is intentionally irrelevant. Real sources are restricted to a few saved California statutory files; named nonstatutory authorities are represented only by authored cases. There is no multilingual, OCR-corpus, very-long-context, retrieval, live-validity, or human-user study. Metadata separation is tested through negative excerpts whose saved source files establish statutory context outside focus; no extra metadata is serialized into focus by these cases.

## Preparation identities

- Question raw-file SHA-256: `923ca7aa07af9bb2e07e171e98b9756645567850be0d37805dc6d1bb8735edee`
- Cases raw-file SHA-256: `50ccc119819aa5acf98c39fcc9287e89465aa289ac23d1b4b5c49c33ac2f257c`

The author-label file is a plain array of `{case_id, expected, reason}`. The cases file is a plain array containing only focus text, strata, identity, and either exact source attribution or `authored: true`. No expected label is embedded in the text or case metadata. No frozen request, reviewer label, model output, or adjudication is produced here.
