# Research coverage tracking

Track the work needed to support an operating decision, including what remains to investigate. The source register remains the inventory of retrieved statutory sections. Coverage records connect that inventory, source versions, research questions, consequential dependencies, conclusions and independent reviews. No Jev answer or old route is converted into completed legal research.

## Working commands

Run from `research/legal-engine` with the existing `.venv/bin/python` (plain Python also works; this feature uses the standard library).

```sh
python -m pipeline coverage seed CA california-research --purpose 'Resolve physical work and the outgoing account under applicable California law' --author root
python -m pipeline coverage export CA california-research > /tmp/coverage-export.json
python -m pipeline coverage status CA california-research
python -m pipeline coverage followup CA california-research --file pipeline/design/prepared_tasks/fresh.followup.json --expected-revision 1 --author root
python -m pipeline coverage link-research CA california-research --file pipeline/design/collection_dependencies/RESOLUTION_VERIFICATION.json --expected-revision 2
```

The live California scope has already been initialized; do not repeat these mutations against revision zero. Export returns `revision` plus `document`. Edit the document, keeping its existing records, and save the **document object** as a separate JSON file:

```sh
python -m pipeline coverage save CA california-research --file /tmp/coverage-document.json --expected-revision 3
python -m pipeline coverage check CA california-research
```

`status` successfully reports open work; `check` exits nonzero until recorded coverage is complete. Both default to today's assessment date. `--as-of YYYY-MM-DD` supports an explicitly dated assessment; it does not turn old research into current law. `export --revision N` inspects history. `digest --kind item|boundary|scope --target ID` provides the exact content hash for an actual independent reviewer to bind in their record.

`pipeline check CODE` now also reports every declared research scope. Its full default check cannot succeed without complete recorded coverage, even if legacy retrieval/routing stages pass. Earlier `--upto` checks retain their narrow mechanical meaning and still print coverage separately. A completed small scope does not hide a larger open scope.

## Record contract

A scope declares its purpose, legal/research date, scope description, author and next action. Its four primary lists contain stable IDs:

- **Items:** recognizable sources and legal questions. Each has an affected operating decision, investigation status, next action, conclusion and supporting evidence. Open questions may identify a broad lead before a canonical source is known. A source also records immutable versions, the selected version, the legal date to which it is applied, currentness investigation and its next recheck. A different period can require another item/version; don't collapse January and February law into one current text.
- **Boundaries:** exact enumerated source IDs, the selection method and authoritative inventory evidence. The inventory is a saved JSON artifact with `source_ids`, `method` and `evidence`. A boundary review assesses enumeration; it is not an interpretation review. Registered-unit selectors reconcile both membership and complete row identity against the live register, including source-file/version changes.
- **Dependencies:** directed relationships with their actual consequence. Unknown targets remain questions; they do not disappear because retrieval failed. Required targets cannot be satisfied by excluded items. A dismissed dependency retains its reason/evidence and receives review through the affected item and scope. Cycles are allowed and traversed finitely; every member still needs substantive support and review.
- **Reviews:** append-only, ordered records identifying target kind/ID, exact target hash, independent reviewer, checked matters, result, unresolved findings and a retained report. Item hashes include the finite transitive dependency graph; scope hashes include all declared content. A later challenge supersedes an earlier pass for the same target. Reviews never hash themselves.

Evidence objects have root-relative `path`, exact `sha256`, and a precise `locator`. Use `coverage.artifact(path, locator)` to capture a reference. Pin the actual source material and operative analysis, not just a report filename. The checker verifies bytes and observes external register files again during assessment; a changed artifact or source binding requires reconciliation.

Source `versions` have ID, URL, retrieval observation, effective start/end where applicable, a textual temporal basis and evidence. The end is exclusive. Historical legislative analysis is not treated as an operative statute. `source.currentness_evidence` records the actual amendment/version investigation; a byte hash alone is not evidence that no later law exists. `checked_through` must cover the assessment date. An expired `recheck_on` blocks closure. Unknown dates remain explicit investigation problems rather than defaulting to today's law.

## Imports and prior work

`seed` reads current registered sections and all declared units, including unharvested units, pins the register/instrument files, and records pending source families, non-code sources and fetch gaps as open investigation. It leaves every source open. Legacy matches, `no_decision`, excluded routes and model scores cannot grant closure. Missing text remains visible.

`followup` imports the prepared-task follow-up contract. It preserves exact source occurrence, observation, targets and agent notes, including model negatives and broad nonstatutory leads. These become open questions and dependencies. The original evidence file remains unchanged and bound; a later change requires reconciliation.

`link-research` retains Goal 3's exact accepted finding/review pairs and original scope. It verifies those hashes against the saved independent review. This preserves completed research as available evidence without calling its conclusions unreviewed, or asserting that it completes the larger California source inventory. The agent decides how each conclusion applies to new work and records that reasoning with its own review.

## Durability and changes

Each jurisdiction stores new records in `coverage.sqlite3`. SQLite `BEGIN IMMEDIATE`, full synchronous commits and expected-revision checks make a committed revision the unit of update. A process killed before commit leaves the prior revision; after commit the new revision is authoritative. There is no manually recoverable lock file or snapshot pointer to guess from. SQLite's normal journal recovery releases a killed writer's lock. Storage hardware/filesystem guarantees still govern actual power-loss behavior; the demonstrated guarantee is process interruption.

Revisions retain a parent/content hash chain. Concurrent stale writers must reload and reconcile. Items, boundaries and dependency identities cannot disappear; retain explicit excluded/dismissed work. Source-version records and reviews are immutable. Scope/selector reduction requires an explanation and invalidates review. Imported research links remain present; a changed link requires an explicit reconciliation reason. No automatic rollback presents an older revision as current when integrity checks fail.

The checker validates recorded consistency and evidence identity. It cannot authenticate the real identity behind an author name, invent omitted sources, or prove a legal interpretation from a nonempty paragraph. Actual independent source/meaning review remains required. The fresh demonstration and adverse tests distinguish those tasks from mechanical checks.

## Evidence and status

See [goal and to-dos](GOAL.md), [initial independent challenge](INDEPENDENT_INITIAL.md), [implementation review](INDEPENDENT_IMPLEMENTATION.md), and [fresh research](fresh_research/FINDINGS.md). Fresh research and its tracker mapping have passed independent review. The fresh scope is complete at revision6 while the broader California scope remains open at revision4. See [acceptance audit](COMPLETION.md), [verification](VERIFICATION.json) and [resumption evidence](resume-evidence.json). Historical research and experiments remain untouched.

The fresh candidate references an immutable `coverage-inventory.<hash>.json`. Earlier `coverage_inventory.json` is retained for the first onboarding revision and is not the accepted final inventory. `build_demo.py` assembles demonstration records; it does not fabricate the chronological order of source discovery or insert review acceptance.
