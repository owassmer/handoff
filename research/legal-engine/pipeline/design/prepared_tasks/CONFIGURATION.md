# Configure Jev for the work

Founder direction, September 30, 2026: use Jev's available configuration where it improves the task throughout the durable pipeline. The existing runner must not determine the task's question shape. This carries forward the typed semantic interface described in [Ferro's synthesis](../../../SYNTHESIS.md) and [workflow connection](../../../HANDOFF_CONNECTION.md).

## Preparation and configuration are one design decision

For each task, record the operating/research decision, selected evidence, exact object being judged, primitive, instructions, criteria when useful, shared context, downstream use, and evaluation version. Inspect the actual serialized request. Source identifiers belong in bookkeeping unless their meaning is necessary for that judgment. Question IDs are bookkeeping, not model context.

| Work | Mechanism and configuration |
|---|---|
| Does a selected passage define a term? Does a selected expression identify legal text? | Noul for one proposition; selected object directly in instructions when helpful, surrounding passage in state. Optional concise true/false criteria clarify the intended distinction. |
| Does a use have the defined sense? Does an exception modify this requirement? Does evidence support this claim? | Separate Nouls, with the selected pair and necessary scope/context. Do not combine independent conditions into one answer. |
| Which candidate meaning, evidence item, or category fits? | Choice with meaningful alternatives and structured descriptions where needed. Include none/unknown only when those are real outcomes. Nonexclusive categories instead need independent questions. |
| A useful judgment along ordered descriptive levels | Score with an evaluated rubric. No current reference task requires it. Its position is not an exact quantity, severity fact, or legal outcome probability. |
| Money, dates, known hierarchy containment, identity | Code after the agent establishes the meaning and inputs. |
| Missing context, candidate discovery, conflicting interpretation, investigation and synthesis | Agent; code checks records and exact spans. Jev does not repair unavailable evidence by returning NO. |

Use strings when clear. Structured instructions can place the candidate directly beside its question; structured option descriptions or levels can preserve relevant records without an overloaded prose prompt. More fields are not automatically better. Include enough context to interpret the object, then exclude irrelevant material.

Batch independent questions sharing the same evidence into one request where useful. Keep question-specific objects in their own instructions. Multiple concurrent HTTP requests are a different optimization. Retrieve or resolve prerequisites before asking dependent questions; do not pretend questions in a batch can consume each other's answers.

Keep returned distributions and uncertainty. A Noul value is not degree of satisfaction; a Choice distribution is relative to its offered alternatives; a Score is an expected position on descriptive levels. Do not carry thresholds across primitives, question versions or models without evaluation. Ambiguous judgment, missing evidence, invalid response and execution failure require distinct handling. Consequential follow-up depends on the consumer's error costs and demonstrated performance, not a universal cutoff.

## Implementation and verification

`pipeline.jev.sdk_questions` now explicitly constructs Noul, Choice and Score and rejects unknown primitives. It preserves structured instructions and criteria; Noul criteria may be omitted. `built_questions` fills scope recursively without flattening those structures. Legacy registry requests remain identical in a regression check. The existing triage result consumer remains specific to role/chain-duty; this adapter change does not turn that consumer into a general task runner.

Before adopting a task, freeze the exact prepared input and configuration, review expected meaning, execute, inspect disagreements, and test on fresh representative material. Compare configuration changes on fixed inputs where possible; record when multiple factors change. Include preparation/candidate discovery and useful follow-up in whole-process measurement. Preserve failures. A development score is not production calibration.

Pinned model, full instructions/criteria/state, source versions, assembly version, answer schema and downstream policy must be traceable. Current research runs retain exact requests and raw responses. Production cache validation and broader runtime integration remain separate unfinished plan items.

## Current limits and follow-through

The other task questions in `questions.json` remain prototypes. Their primitive/preparation choices above are design guidance, not demonstrated reliability. A [matched four-section pilot](STATUTORY_PILOT.md) now records 27 separate calls versus four shared-context calls with identical majority classifications and about 75% lower reported cost. This single-run result does not establish broader latency or end-to-end workflow benefit. Score construction is tested, but no production Score task is justified yet. Reference candidate discovery recall remains unmeasured.

Primary documentation consulted: [structured instructions and criteria](https://docs.typesafe.ai/primitives/advanced), [Noul](https://docs.typesafe.ai/primitives/noul), [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score), [fan-out](https://docs.typesafe.ai/patterns/fan-out), and [Jev 1.13 behavior](https://docs.typesafe.ai/model-jaggedness/jev-1.13). Check current documentation when extending the integration; use features because they fit the work.

The statutory pilot also tests configuration simplicity: placing the literal expression directly in a short question improved one development case. The final task distinguishes a pointer to statutory text from a subject discussed by that text; the governing clause can be sufficient context when a whole section adds competing references. Preserve those other dependencies as separate candidates. Do not assume structured objects or larger shared contexts always perform better.
