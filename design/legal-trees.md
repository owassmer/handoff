# Legal tree format

October 3, 2026. This is the shared format between the legal track, which compiles trees, and the Handoff service, which evaluates them in TypeScript. The approach is set out in `DESIGN.md` §5.3. Trees live as JSON files under `research/legal-engine/jurisdictions/<CODE>/account_core/trees/`, one file per legal decision, for example `deduct-repair.json`.

## A tree

| Field | Meaning |
|---|---|
| `id` | Stable identifier, e.g. `CA.deduct-repair` |
| `title` | Plain question it answers, e.g. "May this repair be deducted from the deposit, and for how much?" |
| `decisionPoint` | Chain-map id, e.g. `DP5.2` |
| `layer` | `US`, `CA`, `CA-OC` or `CA-HB` |
| `effective` | `{from, to}` dates. A case is evaluated under the version in force on its event date. |
| `inputs` | The case facts and records the tree reads, by name: `moveOutDate`, `conditionFinding`, `invoice`, `photos.afterPossession` |
| `parameters` | Named values with sources, e.g. `{id: "statementDays", value: 21, unit: "calendarDays", source: {...}}` |
| `root` | The condition structure (below) |
| `effects` | What follows when the root holds, or when it fails |
| `contested` | Genuinely contested points, with each branch and its authority (below) |

## Condition nodes

- **`all`**: `{type: "all", children: [...]}`. True if every child is true, false if any is false, otherwise unknown.
- **`any`**: `{type: "any", children: [...]}`. True if any child is true, false if every child is false, otherwise unknown.
- **`not`**: `{type: "not", child: ...}`. True and false swap; unknown stays unknown.
- **`condition`**: a leaf, with:
  - `id` and `statement`: one plain sentence, e.g. "The damage was not present at move-in."
  - `source`: `{citation, quote}`, where the quote is verbatim from a saved official text and checked by script.
  - `kind`: `determinate`, `semantic` or `discretionary`.
  - For **determinate** leaves, `compute`: the named record field or calculation that settles it, e.g. `photos.afterPossession.exists`, or `sum(deductions.repairAndCleaning) <= parameters.documentationThreshold`.
  - For **semantic** leaves, `question`: `{type: "yesno" | "choice" | "score", wording, options?, inputs: [...]}`. The `inputs` list is the evidence contract. Code refuses to ask the question if any input is missing, and the leaf stays unknown. The judgment layer picks the provider. Each question's decision policy (thresholds for established, negated or unresolved) is set from labelled cases, not written here.
  - For **discretionary** leaves: who decides (`agent` or `operator`) and what they are deciding.
- **Exceptions and requirements:**
  - `{type: "unless", rule: ..., exception: ...}` is true when the rule is true and the exception is false. It is false when the exception is true, and unknown when the exception is unknown and the rule is true.
  - A requirement is simply a child of an `all`.

Unknown is never treated as false. An unknown that changes the outcome becomes an investigation task for the agent: whatever input or evidence would settle it.

## Effects

`{id, kind: "permission" | "prohibition" | "duty", statement, when: "holds" | "fails", amount?, due?, consequence?}`

- `amount` is a named formula evaluated by code in integer cents, e.g. `min(reasonableCost, invoice.total) * schedule.tenantShare(item, age)`.
- `due` is a date formula in calendar days from an anchor, e.g. `moveOutDate + 21`. Operating deadlines use the nominal day; the weekend and holiday extensions are recorded only as margin.
- `consequence` links to the tree that states what follows from breaching this duty, e.g. `CA.bad-faith-retention`.

## Contested points

`{issue: "C1", question, branches: [{reading, authority: [{citation, quote}], effect}], exposureBranch}`

The evaluator reports every branch. Exposure is computed on the branch least favorable to the operator (`exposureBranch`). The agent explains the disagreement, and the operator decides where a choice is needed.

## Additions adopted from the first compilation

Adopted October 3, 2026, from the California account-core trees. The checker enforces them, and the evaluator ignores any optional field it does not use.

- **Branch effects.** Each contested branch has an `id` and an `effect: {statement, sets: {leafId: true | false}}`, so the evaluator can run the tree under every branch.
- **Contested leaves.** A leaf that a contested point decides carries `contested: "C6"`.
- **Discretionary leaves** carry `decision: {by: "agent" | "operator", what}`.
- **Question basis.** A semantic question may carry `basis: [{citation, quote}]`: guidance behind a factor, such as the DRE guide or a bill's stated intent. It is checked verbatim like any source.
- **Effect fields.** An effect may carry a checked `source`. It may also carry `margin` and `notBefore` date formulas: the latest lawful date where an extension applies, and the earliest permitted date.
- **Cross-tree references.** Formulas may use `holds("CA.tree")` and `amount("CA.tree", "effect-id")`.
- **Parameter units.** In addition to `calendarDays` and `cents`: `hours`, `date` and `multiplier`.
- **Citations.** These follow the forms `Civ 1950.5(h)(2)`, `CCP 1161`, `Gov …` and `PUC …`, or a named source the checker maps to its saved text, such as a case mirror, a bill analysis or the DRE guide.

## Example (abridged): may the closet repair be deducted?

```json
{
  "id": "CA.deduct-repair",
  "title": "May this repair be deducted from the deposit, and for how much?",
  "decisionPoint": "DP5.2",
  "layer": "CA",
  "effective": {"from": "2026-01-01", "to": null},
  "root": {"type": "all", "children": [
    {"type": "condition", "id": "is-security", "kind": "determinate",
     "statement": "The deposit is security under the lease.",
     "compute": "tenancy.deposit.isSecurity",
     "source": {"citation": "Civ 1950.5(b)", "quote": "..."}},
    {"type": "condition", "id": "caused-by-tenant", "kind": "semantic",
     "statement": "The damage was caused by the tenant or a guest or licensee of the tenant.",
     "question": {"type": "yesno", "wording": "...", "inputs": ["observation.moveOut", "tenancy.record"]},
     "source": {"citation": "Civ 1950.5(b)(2)", "quote": "..."}},
    {"type": "condition", "id": "not-preexisting", "kind": "semantic",
     "statement": "The damage was not present at move-in.",
     "question": {"type": "yesno", "wording": "...", "inputs": ["observation.moveIn", "observation.moveOut"]},
     "source": {"citation": "Civ 1950.5(e)(2)(A)", "quote": "..."}},
    {"type": "all", "children": [
      {"type": "condition", "id": "cause-not-normal-use", "kind": "semantic", "...": "..."},
      {"type": "condition", "id": "beyond-age-and-use", "kind": "semantic", "...": "..."}]},
    {"type": "any", "children": [
      {"type": "condition", "id": "on-premoveout-list", "kind": "determinate", "...": "..."},
      {"type": "condition", "id": "hidden-by-belongings", "kind": "semantic", "...": "..."},
      {"type": "condition", "id": "after-inspection", "kind": "semantic", "...": "..."},
      {"type": "condition", "id": "no-initial-inspection", "kind": "determinate", "...": "..."}]},
    {"type": "condition", "id": "restores-not-improves", "kind": "semantic", "...": "..."},
    {"type": "any", "children": [
      {"type": "condition", "id": "documents-complete", "kind": "determinate",
       "statement": "The statement includes the invoice or hours and rate, and photos before and after the repair.",
       "compute": "statement.documents.repairComplete", "source": {"citation": "Civ 1950.5(h)(2)", "quote": "..."}},
      {"type": "condition", "id": "under-documentation-threshold", "kind": "determinate",
       "statement": "Repair and cleaning deductions together do not exceed $125.",
       "compute": "sum(deductions.repairAndCleaning) <= parameters.documentationThreshold",
       "source": {"citation": "Civ 1950.5(h)(4)(A)", "quote": "..."}}]}
  ]},
  "effects": [
    {"id": "may-deduct", "kind": "permission", "when": "holds",
     "statement": "The repair may be deducted.",
     "amount": "min(reasonableCost, actualCost) * schedule.tenantShare(item, age)"},
    {"id": "must-not-deduct", "kind": "prohibition", "when": "fails",
     "statement": "The repair may not be deducted.", "consequence": "CA.bad-faith-retention"}
  ]
}
```

Below the $125 threshold the documents need not go with the statement, but a tenant who asks within 14 days must receive them within 14 days (Civ 1950.5(h)(5)). That obligation is its own tree, `CA.documentation-on-request`: a duty with a `due` date, triggered by the request event. The `unless` node is used where a statute states an exception to a rule, for example the inspection-notice duties not applying when the tenancy ends under CCP 1161(2)–(4).
