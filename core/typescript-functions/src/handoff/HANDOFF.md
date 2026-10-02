# Handoff

## Business flow

1. **Create a workspace** for the signed-in person, with separate work, decision and configuration grants.
2. **Receive a move-out notice** containing the property, parties, tenancy, documents, agreements and obligations. This requests a work plan; it does not provide a saved recommendation.
3. **Prepare the work plan** by reading the current documents through the configured model and checking the quoted costs with exact integer addition. The model proposes the scope and budget. Quotes are not spending permission.
4. **Change the work budget**, if needed, without rerunning the model or changing the scope and fixed requirements.
5. **Accept the work plan** at the revision reviewed. The decision preserves the complete proposal, budget, requirements, provider and source references.
6. **Continue the handoff** by recording a request to the accepted provider. The correspondence service acknowledges receipt and waits for scheduling confirmation. It does not report repairs complete or perform financial work.

The application displays the workspace's `mode` as one Demo indicator. The only supported mode is `demo`; no function falls back to an external delivery service.

## Functions

The platform supplies `client: Client`. Editing functions return `Promise<HandoffEdit[]>` and apply no edits in preview. They must be used through Actions.

| Function | Remaining parameters, in order |
| --- | --- |
| `createHandoffWorkspace` | `name: string, commandId: string, currentUserId: string` |
| `receiveMoveOutNotice` | `workspaceId: string, noticeJson: string, commandId: string, currentUserId: string` |
| `prepareHandoffWorkPlan` | `handoffId: string, commandId: string, currentUserId: string` |
| `changeHandoffWorkPlan` | `workPlanId: string, expectedRevision: Long, budgetCents: Long, commandId: string, currentUserId: string` |
| `acceptHandoffWorkPlan` | `workPlanId: string, expectedRevision: Long, commandId: string, currentUserId: string` |
| `continueHandoff` | `handoffId: string, commandId: string, currentUserId: string` |

Action configuration must bind `currentUserId` to the platform's current-user value, never a user-editable field. The functions also compare it to `Admin.Users.getCurrent(client)`. There are no embedded user identities or profession-based grants. A workspace creator receives all three grants only on their newly created workspace. No function changes existing grants.

Read functions have their matching API names and return `Promise<string>`:

- `listHandoffs(client: Client, workspaceId: string)` returns the first 25 handoffs in stable-reference order.
- `getHandoffWorkspace(client: Client, handoffId: string)` returns the current handoff view.
- `recommendPropertyWork(client: Client, contextJson: string)` remains a read-only recommendation helper. It cannot accept a plan, persist records or arrange work.

Read identity comes from the platform, not a caller parameter. `contracts.ts` defines the application-facing list and workspace JSON. Money and revisions are decimal strings; dates are ISO dates. Technical references occupy dedicated fields. Activity summaries exclude command comparison hashes and model execution details. Decision makers are shown by the signed-in person's display name or as a workspace decision maker, not an operator identifier.

## Move-out notices

`notice.ts` defines and validates `MoveOutNotice`. `noticeJson` is its JSON representation. Required top-level fields are:

- `sourceSystem`, `sourceRecordId`, `title`, `goal`, `businessDate`
- `property`: source reference, name, address and description
- `parties`: source reference, name, kind and description; optional email and phone
- `tenancy`: source reference, title, landlord and tenant source references, start, end and notice dates
- `documents`: source reference, title, text, business kind and source kind; optional supplying party and source file/page references
- `agreements`: source reference, title, kind, terms, supporting document source reference and effective date
- `obligations`: source reference, title, description, responsible and benefiting party references and status; optional agreement/document basis and due date

`fixedRequirements` is optional: up to 24 distinct, nonempty strings of at most 1,000 characters each, containing conditions specified for this handoff. It defaults to `[]` and is stored on the handoff. The work context uses only this explicit value for fixed requirements; obligations, agreements and documents remain evidence for choosing the scope and budget, not a list of fixed instructions. Existing handoffs without the field also use `[]`. Omitting it and supplying an empty list have the same notice intent, including for earlier request receipts.

Unknown fields are rejected at every level. All references must resolve within the notice. Dates and source page ranges are checked. Limits include 32 parties, 24 documents, 16 agreements, 24 obligations, 24,000 characters per document and 180,000 characters of document text combined. Source file references are identifiers only; receiving a notice does not retrieve a file or contact its source.

`Quote` documents must identify the provider through `partySourceId`. The stored document's `partyId`, not a party profession or kind, determines available providers. `sourceKind` is `Source` or `Prepared`; it is separate from the document's business kind.

Source keys produce stable workspace-qualified object references. Existing source records can be reused only if all supplied business fields agree. These functions never overwrite source facts. Receiving the same command again returns no edits; changed intent under the same command reference is rejected. A new command for an already received notice does not duplicate the handoff.

## Work recommendations

The current handoff and its tenancy agreements select the source documents. Source documents linked through an agreement are included; unrelated handoff records are not supplied. The model must read every supplied document and call `sumMoney` before returning a proposal. The result must cite the selected provider's quote and retain explicit fixed requirements. The acceptance of evidence-based meaning remains subject to human review; structural checks are not a legal or semantic proof.

`WorkContext.budgetLimitCents` is optional and means an actual owner ceiling when supplied. It is not a proposed budget. The notice contains no numeric spending grant, so the record-based recommendation does not invent one. The model must respect explicit owner ceilings and approval requirements in source documents. The proposed budget must cover the checked estimate; if a numeric ceiling is supplied it must not be exceeded. The available model is resolved through the managed default alias, and the workspace's model reference must match it.

The actual model draft is stored as a work plan. Activity stores only a bounded execution record: model reference, documents read, tool count and duration. No prompt, private deliberation or authentication value is stored there.

## Authority and repeated requests

- Current reader access and the appropriate work or decision grant are checked before interpreting old command receipts.
- A budget change and acceptance require the exact plan revision and its matching handoff basis revision. Budget changes increment both. Acceptance records the reviewed content revision without changing that content.
- Activity receipts bind workspace, command reference, actor, operation, subject and a canonical payload hash. Exact old repeats remain effect-free even after later commands.
- Related records must have the same reader set as their workspace. A change to workspace readers alone cannot broaden a recommendation derived from more restricted sources. Coordinated access maintenance is outside these functions.
- Work, case and plan updates use loaded SDK instances. Every changing command also updates the loaded workspace authority record in its single edit batch. Model preparation rechecks authority and its handoff/work records after the model returns. Read views recheck their workspace/handoff anchors before returning.
- These measures do **not** establish serializable reads across the entire Ontology. Concurrent Action behavior, create collisions, revoked grants and retry behavior still need deployed Action verification. The unit store does not simulate Foundry conflict admission. Sources must remain immutable through the supported command surface.

## Correspondence and scheduled work

A received notice creates `HandoffAgentWork` with `status = "Plan requested"` and `operationKey = "prepare:" + handoffId`.

Acceptance updates that work to `status = "Ready to continue"` and `operationKey = "continue:" + decisionId`. An automation can call the corresponding normal Action as an authorized execution identity. The Action's current-user binding must stay server-owned.

Continuation verifies the current plan against the immutable decision. Deterministic outgoing and incoming message references use the decision operation, not the triggering command reference. The demo correspondence service records the request and its receipt acknowledgement in the same batch, then sets `Waiting for provider` with a next wake time 24 hours later. A later command with the same accepted decision validates the existing correspondence and returns no edits. The waiting timestamp does not manufacture an appointment or complete repairs. The scheduled delivery owner should enable only the supported queued statuses; future waiting work needs an actual provider update capability.

The parent delivery task owns Action creation, publishing, deployment verification, data loading and automation setup. No Action, data or automation is created by these source files themselves.
