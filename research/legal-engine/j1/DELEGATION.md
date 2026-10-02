# J1 coordination

Current instruction: Owen has authorized implementation delegation and requested a trim to reduce memory use while root continues orchestrating and reasoning. J1 is active and remains incomplete. Under the current explicit goal, at most four workers run concurrently, rotated through concrete remaining source dependencies. The original six lane artifacts below remain retained; they are not six simultaneous assignments. Root steers scope, integrates shared changes and assesses substantive completeness.

## Shared basis

Read HANDOFF_CONTEXT.md, research/expansion/context/intent_notepad.md, research/legal-engine/PLAN.md, jurisdictions/CA/J0_INTAKE.md and /Users/owenwassmer/.codex/skills/jurisdiction-pipeline/SKILL.md. Paths without a leading slash are relative to the workspace; jurisdiction paths below are relative to research/legal-engine. The latest user clarifications in HANDOFF_CONTEXT.md take precedence over conflicting historical method assumptions. The current conversation, including the user's repeated corrections, supplies their meaning.

The purpose is an engine that enables complete residential physical work and outgoing-account resolution, avoiding unnecessary expense and litigation while preserving justified recovery. This is a repeatable jurisdiction method, not a Breakwater-derived legal checklist. Current layers are US, CA, Orange County and Huntington Beach. Conditional housing regimes remain within the agreed aperture. Existing draft selections are proposals to examine, not authority.

J1 supplies instruments, reasoned unit selections/exclusions, current and adopted future changes, and concrete TOC/acquisition paths. Whole-text harvest is J2; semantic compilation and controlling-case work have later stages. Follow a dependency far enough to decide the present source selection; exercise judgment about how much text that requires. Counts and passing checks do not decide substantive completeness.

## Responsibilities

| Lane | Responsibility | Existing starting material |
|---|---|---|
| California codes | State code units and exclusions against the operating/legal functions | build_register.py, refine_civil.py, code_root_census.json, CA register |
| California enactments | Enacted and both-house-passed statutory changes, session coverage and status | bill_candidates.json, early-2026 lists, collect_bill_headings.py, saved official action indexes |
| Federal and programs | Federal parent scope, regulations, assisted-housing/program documents, adopted future rules | US register, additional_sources.py, supplemental_sources.py, program captures |
| Local and agency | OC/HB codes and uncodified actions, emergencies, local/program and regional agency requirements, CA regulatory currentness | CA/CA-OC/CA-HB registers, saved agency and local indexes |
| Acquisition | Whether selected units lead to actual source acquisition through the existing adapters; concrete corrections | pipeline/adapters, pipeline/harvest.py, four registers |
| Courts | Operative and adopted future court rules, procedural orders and forms for the registered forums | Four registers, court-source captures and official publication indexes |

Each source lane owns j1/lanes/<lane>/ for proposals and source additions. Shared canonical registers and generation scripts are integrated by the coordinator to avoid concurrent overwrites. The acquisition lane additionally owns narrowly necessary changes to pipeline/adapters/, harvest.py, reused USC/eCFR parsing helpers and relevant tests. Agents coordinate source identities and acquisition needs directly. The coordinator retains cross-lane operating coverage and integration, including the shared decision map. Reviewed instrument replacements are retained in register_updates.json and applied after the baseline build so regeneration preserves them.

A useful return explains the substantive scope decision, supporting source location, concrete proposed change and remaining dependency, with enough context to evaluate it. Prefer concise results linked to detailed evidence over raw browser output. Choose research routes and subdivision methods to fit the material; raise overlaps early. The coordinator handles cross-lane reconciliation and reasons through the complete operator aperture before declaring J1 done.

## Grounding findings to carry forward

- Codes: relate retained separate-industry Civil Code units to actual operating decisions; reconsider the generic exclusion of Education Code general provisions; refine whole-tax-code selection against the agreed aperture.
- Enactments: 797 announcements and 177 earlier bill IDs are distinct but do not establish a reconciled session. SB895 appears in a prose announcement and escaped the bullet parser. No bill_scope.json or individual bill integration exists. Use official session/action histories to establish coverage; matching a total is not the substantive bar.
- Federal/programs: eight supplemental additions remain unmaterialized; unspecified Treasury sections, HCD award-vintage guidelines and CalHFA documents need concrete identities. CTCAC's linked manual says April 2023 despite its 2026 upload path. NSPIRE transitions need program-specific interpretation.
- Local/agency: complete post-codification action coverage; distinguish captured URLs from actually read minutes. 68805.pdf is the 2017 CoC PSH guide, incorrectly assigned to FSS. Check HB Title 13's complete headings before sustaining the blanket exclusion. Reconcile operative state regulatory changes and local emergency instruments.
- Acquisition: code root indexes and generic document directories are not interchangeable with section-enumerating adapter inputs. Resolve concrete targets and adapter contracts before whole-text acquisition.

These are research findings from the grounding pass, not accepted legal interpretations or a claim that this list exhausts J1. The resumed lanes are resolving them and any material dependencies they uncover.

## Jev during source review

Use Jev to flag whether each coherent source passage cites or refers to another document or provision. Cover the complete operative source with paragraph/subsection spans, retain governing introductions with their lists and necessary enclosing context, and keep source labels outside the judged text. Each passage receives its own answer, including when independent questions share a call. Researchers then inspect flagged passages, locate the cited texts, recover them and reconcile their coverage. Do not preselect citations as a prerequisite or turn this aid into relationship extraction. A broad positive passage may need subdivision. Root maintains `pipeline/reference_discovery.py`; `j1/references/passage-preparation.json` is the first actual prepared input. Live screening now runs with restored network access: passage-run-2 answered21 passages, and cpuc/run-2 answered29 newly recovered order paragraphs/footnotes. Source followthrough is recorded next to each run; the earlier network failure is historical.
