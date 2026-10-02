# Independent design review: legal-reference detection

2026-09-30. Development review; no held-out labels created. Read `HANDOFF_CONTEXT.md`, the existing five-question contract, the California collection disagreement review, the agent/Jev/code design, and saved CIV 1983. Applied the Handoff engine-development skill. This reviews a text task, not the current legal meaning or validity of any provision.

## Useful atomic boundary

Ask whether the supplied focus contains at least one explicit pointer to an identifiable kind of public legal source or legal unit. Include the current provision itself, its enclosing units, subordinate provisions, other provisions, named enactments, and specific rules or regulations. Detection does not establish an exact target, target availability, legal effect, incorporation, applicability, currentness, or operational relevance.

“Explicit” should mean that the words point to a legal source/unit, rather than that code can resolve the target. “The preceding paragraph,” “this title,” “Section 12,” and a named statute can be explicit even when retrieval requires more context. An absent target is not a damaged reference expression.

Minimal first task: `YES / NO / INSUFFICIENT`, with YES meaning at least one qualifying expression is visible. Remove “another” from the lead question. The existing question conflicts with itself at a whole-section self-reference. Its uncertainty is a contract problem, not missing source text. Preserve the old 40/42 frozen agreement and both mismatches; collection16 is a known contract ambiguity, collection36 a clear enclosing-title miss under that contract. Neither is fresh evaluation evidence.

A negative means only “no explicit legal-source pointer detected in this focus.” It cannot exclude the provision, private agreements, implicit dependencies, or generic legal standards from agent investigation. Agent work after a positive is to inspect the expression and decide what context to retrieve; after insufficiency, recover the damaged expression. The agent also retains responsibility for important dependencies outside this detector's scope.

## Distinctions without a misleading section label

Presence and relation are different propositions. A passage can contain self, enclosing-unit, and cross-references together. Do not force a mutually exclusive passage classification. Keep presence as the baseline atomic question. If relation information demonstrably helps the agent, use separate predicates or classify individual reference expressions with an exact quotation and supplied source identity.

For a relation task, fix an anchor independently of excerpt size. A workable initial convention is the statutory section containing the expression:

| Relation | Meaning relative to the supplied anchor section |
| --- | --- |
| Self | The target is the anchor section itself, including “this section” and its explicit number when identity is supplied. |
| Enclosing | The target is an ancestor such as the containing article, chapter, title, or code. |
| Cross-reference | Another section, a subordinate or sibling unit, or another public legal source. This includes a subsection of the anchor section. |
| Unresolved relation | A legal pointer is present, but supplied identity/hierarchy cannot establish the relation. |

The fixed section anchor is a design convention, not a claim about legal ontology. For example, “this subsection” is a subordinate-unit pointer under this convention; it is not an enclosing-section pointer merely because the focus is one sentence. If the intended labels instead anchor on the current subsection, specify that unit explicitly and test it separately. Do not infer hierarchy from filenames or confuse changes in focus size with changes in legal target.

“Ordinary lookalike language” is a negative distinction, not a reference relation. “Section of carpet,” “title to property,” “paragraph of a tenant's letter,” and “chapter of a novel” need their local context. Capitalization or the token “section” alone is not sufficient.

## Boundaries to settle in the contract

| Boundary | Recommended treatment and reason |
| --- | --- |
| Generic legal language | “As required by law,” “under applicable law,” and “other legal remedies” do not identify a source or unit. NO for this task, but potentially important agent research leads. “Under California law” alone remains a general body of law; “under the California Civil Code” names an identifiable source and counts. |
| Private documents | “Section 4 of the lease,” an invoice, a letter, or house rules are not public legal-source references. NO unless a separate qualifying public legal reference is present. Do not infer public authority from mandatory wording. A defined private “Act” must be read in context. |
| Headings and metadata | Define focus as the source body selected for scanning. Source URLs, retrieval dates, navigation, current-section labels, and amendment-history annotations belong outside it. Their citations must not make the body positive. A substantive legal pointer in a deliberately included heading can count, but heading coverage must be explicit and consistent. Source capture problems are preparation issues. |
| Quoted notices | An actual legal reference inside prescribed notice text counts as a visible reference. Quotation does not erase it. A private notice or letter mentioned without a legal pointer does not count. Whether quoted material states operative law is a later question. |
| Ranges and lists | “Sections 10 through 14,” “subdivisions (a) and (c),” and “Chapter 3 (commencing with Section 100)” count. Detection does not require expansion, enumeration, endpoint validation, or deciding whether the range is legally coherent. |
| Truncation | Distinguish recognizable reference with incomplete target from uncertain reference presence. “Pursuant to Section 19…” can be YES if the context visibly identifies a legal unit despite the unfinished identifier. A cut at “pursuant to…” cannot establish presence. A clipped “section” whose legal/private/ordinary sense is unavailable can be INSUFFICIENT. |
| Mixed passages | One complete qualifying pointer makes presence YES even if another expression is damaged or ordinary. Do not let global insufficiency erase an established existential answer. Record capture defects separately. With no qualifying pointer and a damaged plausible reference, use INSUFFICIENT rather than NO. |

An unrestricted notion of “legal source” could also include case citations, constitutional provisions, orders, treaties, or agency materials. State the intended set before freezing. Prefer including unmistakable public legal-authority citations rather than silently excluding a dependency because it is not statutory. Do not expand the first experiment into authority-ranking or citation-resolution work.

## Necessary development and fresh evaluation coverage

Use matched sentence-focus and whole-section-focus development cases for “this section,” plus “this chapter/title.” Require invariant presence answers. Add a mixed passage containing all three relations, a subordinate-unit reference, an explicit-number self-reference with identity supplied, and one legal reference whose relation cannot be resolved from supplied hierarchy.

Cover each boundary above with affirmative and near-negative examples: public versus private “Section 4”; property title versus statutory title; generic law versus a named enactment; body text versus wrapper-only citation; a citation within prescribed notice text; ranges and lists; recognizable incomplete targets versus genuinely cut-off reference expressions; and mixed complete/damaged passages. Saved CIV 1983 is a development illustration of a chapter pointer plus a different-section pointer, while its SOURCE line and amendment note illustrate why wrapper policy matters.

Keep copied clauses, alternate excerpt sizes, and related source families together when separating development and evaluation. Freeze contract, focus policy, actual inputs, model build, and label reasons before Jev execution. A reviewer should see the required source context but neither model answers nor author labels when independently labeling fresh examples. Report task disagreement separately from inadequate preparation and unresolved contract boundaries. No single pooled accuracy number establishes dependency-investigation quality; inspect false negatives and the resulting agent work.

Avoid adding target resolution, applicability, legal-force classification, dependency graphs, or automatic routing to make this small test look complete. The useful deliverable is a clear detection promise, known blind spots, frozen evidence, and an agent that can inspect and follow the resulting leads.
