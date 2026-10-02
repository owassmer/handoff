# California collection pilot — September 30, 2026

The agent-led pilot produced two kinds of progress: a new-family Jev experiment using unchanged questions, and actual source-inventory/dependency work. They are measured separately. The next broad work remains in the [overall plan](../../../../../PLAN.md).

## Frozen experiment

Selected all 18 previously saved sections of Civil Code Title 1.6C. Each definition/reference scan received the entire saved operative body, excluding page headings and enactment history. Source hashes and exact ranges are retained in [sources.json](sources.json) and [coverage.json](coverage.json). Seven further requests tested candidate term use and scope, yielding 43 requests. No question was tuned on this family. The documentation-specific question was not repurposed for collection law.

The [blind reviewer](blind_review.json) labelled all 43 requests before model execution, with no author labels, case-intent notes, or model outputs supplied. Same-model-family and prior task exposure limitations remain. This is a small new-family pilot, not a representative held-out benchmark; it shares the California Civil Code and prior general project research with earlier work.

Mechanical preparation returned one deliberately incomplete request, collection43, to the agent because its use-location hierarchy was null. That is **not** a model abstention or a correct model answer. The remaining 42 requests went through the existing OpenRouter integration. All returned the pinned build and passed response validation. [Evaluation](evaluation.json):

| Task | Frozen-label agreements / answers |
|---|---:|
| Definition presence | 18 / 18 |
| Explicit reference presence | 16 / 18 |
| Candidate term use | 3 / 3 |
| Textual scope inclusion | 3 / 3 |
| Total | 40 / 42 |

Batch duration: 4.1899 seconds. Provider-reported cost: $0.001754172. These exclude agent/source/reviewer work and establish no end-to-end savings.

The [post-run review](disagreement_review.json) distinguishes the disagreements:

- **Collection16, CIV 1788.16:** the question says “another legal provision,” while its criteria include an enclosing unit. With the entire section as focus, “provisions of this section” exposes ambiguity over self-reference. Preserve the frozen YES/NO disagreement, but do not call it an unambiguous model error. Clarify this boundary in a future development version before another evaluation.
- **Collection36, CIV 1788.33:** “provisions of this title” explicitly refers to an enclosing unit. The NO is a clear reference-detection miss. Agent review retains that link and the provision; the model negative does not close the section.

The agent recovered collection43's hierarchy from the saved source headings. Its completed payload is identical to already answered collection40, so no duplicate model call was needed. [Recovery record](context_recovery.json). The general preparation check also intentionally leaves semantically incomplete but structurally valid inputs unresolved: it cannot certify that a supplied passage really contains the needed scope sentence.

## Source enumeration produced a separate finding

Two title-level URL attempts returned navigation without substantive content. Rather than count that as an empty title, the agent followed the official section page's hierarchy to the four article-level pages. The captured official articles contain **22 sections**, exposing four absent from the initial 18-section set:

- 1788: short title.
- 1788.14.5: information and documentary requirements concerning assigned delinquent debt, with conditions, definitions, dates, and cross-references requiring further review.
- 1788.185: hospital-debt litigation provisions, to be reviewed for the actual scope decision rather than silently absent.
- 1788.31: severability.

See [official article inventory](live_inventory.json), [comparison with frozen inputs](inventory_gaps.json), and [1788.14.5 source](1788.14.5_recovered.txt). One direct section retrieval failed; 1788.185 was recovered completely from the official article capture. The scan experiment stayed frozen at 18 sections, so these discoveries are not retrospectively counted as Jev findings or added to its denominator.

The idempotent [inventory importer](../../../../../build/import_collection_inventory.py) added all four captures and corrected the enclosing article metadata for the 18 existing records. California now contains **166 registered sections**. Title 1.6C's 22 section identities are reconciled across its four captured articles. Prior 162 source-body hashes remain unchanged; all 166 source hashes, inventory memberships, and triage identities were verified. Initial backups and a [source manifest](../../../../../jurisdictions/CA/collection_inventory_manifest.json) are retained. Statewide discovery, session-end currentness, authorities, and substantive section review remain open. No legal rule was accepted or applied.

## Agent investigation and remaining dependencies

The following findings come from reading complete source text and following its relationships, not from interpreting a Jev YES as a legal conclusion.

| Operating question | Source relationship found | Next substantive work |
|---|---|---|
| Does collection law reach this outgoing account and this participant? | 1788.2 defines debt collection, debt collector, consumer credit, and covered debt. Definitions and transaction facts must be considered together. | Resolve tenancy-credit authorities and the collector/transaction facts. Do not presume every tenant balance is covered or that using an outside collector is the only trigger. |
| How should an identity-theft dispute change collection work? | The general debtor definition points to 1788.18; that section supplies a local definition, required submissions, review steps, and conditions for further collection. | Synthesize the full branch and establish the actual submissions, reporting history, and review facts. Candidate expression matching alone does not select the governing definition. |
| Which federal requirements are incorporated? | 1788.17 specifies federal sections and exceptions, with federal references fixed as of January 1, 2001; 1788.18(d) links back through that incorporation. | Retrieve the appropriate historical federal text, resolve exact subsections and exclusions, and distinguish incorporation from independently applicable current federal law. |
| What documents must be available or supplied in a collection flow? | Newly recovered 1788.14.5 contains assignment, delinquency, documentary, timing, and other conditions, plus a debt-buyer compliance cross-reference. | Read alongside 1788.50/1788.52 and transaction dates; decide which conditions reach the workflow before generating communications or computing deadlines. |
| What limits collection charges or communications? | 1788.14 contains several branches, including other-law and federal-reporting references, and an embedded definition. | Follow the relevant authority and account facts; keep the permissible charge, collection conduct, and reporting questions separate. |
| What are the consequences, corrections, and limits? | 1788.30 includes remedies, cure/defense provisions, and timing; 1788.33 concerns waiver. | Research controlling interpretation and facts before determining exposure, cure, settlement, or a deadline. |

[Blind review dependency findings](blind_review.json) retain further details. These are concrete follow-up tasks, not a completed California legal opinion or a production operating decision.

## Implementation and verification

The small [context-preparation function](../../context.py) validates request identity and returns known missing scope-location fields as agent work. It does not modify frozen payloads, manufacture negative answers, infer hierarchy from section numbers, or certify semantic context sufficiency. The pilot used its ready-input output for actual dispatch. No confidence threshold was introduced.

Full pipeline suite: **83 tests passed**. Additional checks verified original source preservation, all current source hashes, inventory/triage agreement, exact input hashes, returned build/answer validity, and coverage of the 18 selected saved operative bodies. [Verification](verification.json).

Next: refine the ambiguous self-reference contract in development, complete the newly exposed legal dependencies, and compare complete agent-led work with and without Jev from equivalent starting states. This pilot is evidence that source discovery and agent interpretation must be measured alongside model judgments; it does not yet establish which complete process is faster or more reliable.
