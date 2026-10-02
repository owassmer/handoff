# Handoff backend integration

## Delivery boundary

The work is in the existing TypeScript v2 backend and uses its managed local SDK and `workReasoner` model alias. No additional service, user profession, model-backed CRUD endpoint, or second coordinator is introduced. `prepareHandoffWorkPlan` and `continueHandoff` enter `coordinateHandoff`; conversation wakes that same coordinator. Current deployment remains demonstration-only through the existing workspace authorization guard.

These files do **not** configure Actions or workers, publish a release, execute a business Action, seed Main, activate a live connection, or complete the tenant account. An edit-function preview returns proposed edits without saving them.

## Read contract

The complete client TypeScript contract is `contracts.ts`. `listHandoffs`, `getHandoffWorkspace`, and `getHandoffChange` retain their registered names and return JSON with `version: "2"`. Pin the release version and global data branch explicitly in the client. Do not use an old read pin with the new decoder.

The workspace retains its earlier fields and adds `jobs`, `quotes`, `inspections`, `invoices`, `funding`, and `payments`. The current proposal is `workPlan`; the mandate governing existing work is separately identified by `handoff.operativeDecisionId`. `decisions[].content` provides the exact accepted business content in a normalized view, including older version-one acceptances. It is not reconstructed from the current proposal. New proposals have `selections: { quoteId, quoteLineId, scope, reason }[]` and optional `fixedProviderPartyId` (represented as null when absent). The complete source/reason text is in its dedicated fields, not hidden in a case snapshot.

Amounts and revisions are decimal strings. Page numbers remain numbers. Optional read values are null, not empty strings. Document metadata includes `kind`, `sourceVersion`, `mimeType`, `availableFrom`, original media references and the existing inclusive page range. Source page extraction/search remains in the separate mechanical intake component; this backend does not edit that pipeline or its page index.

Read collections are explicitly bounded, not silently truncated. The current bound is 100 per growing collection; model conversation context is the most recent 24 messages and source reads are selected rather than an automatic full corpus prompt. Larger-scale paging is not implemented here.

## Function signatures and Action bindings

`Client` is injected by Foundry and is never an Action parameter. All edit functions return `Promise<HandoffEdit[]>`. `currentUserId` must be bound to the Action's `current_user_id`, not shown as a caller-editable parameter. `Long` is a canonical decimal string in the function/SDK contract.

```ts
receiveMoveOutNotice(client: Client, workspaceId: string, noticeJson: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]>
prepareHandoffWorkPlan(client: Client, handoffId: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]>
continueHandoff(client: Client, handoffId: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]>
changeHandoffWorkPlan(client: Client, workPlanId: string, expectedRevision: Long,
  commandId: string, currentUserId: string, budgetCents?: Long,
  changesJson?: string): Promise<HandoffEdit[]>
acceptHandoffWorkPlan(client: Client, workPlanId: string, expectedRevision: Long,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]>
sendHandoffMessage(client: Client, handoffId: string, message: string,
  commandId: string, currentUserId: string, expectedPlanRevision?: Long): Promise<HandoffEdit[]>
receiveHandoffDocument(client: Client, handoffId: string, documentJson: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]>
listHandoffs(client: Client, workspaceId: string): Promise<string>
getHandoffWorkspace(client: Client, handoffId: string): Promise<string>
getHandoffChange(client: Client, handoffId: string, commandId: string): Promise<string>
```

The budget Action's **argument order changed**, but existing parameter names remain. Its `budgetCents` parameter is now optional, as is the new `changesJson`; provide exactly one. The structured form is the `WorkPlanChange` interface in `contracts.ts`:

```ts
{
  budgetCents?: string;
  selections?: { quoteId: string; quoteLineId: string; scope: string; reason: string }[];
  fixedRequirements?: string[];
  fixedProviderPartyId?: string | null;
}
```

A precise edit recalculates quote costs and owned proposal fields without a compulsory model call. It must preserve the handoff's explicit requirements. A change to an accepted plan creates a current proposal without editing the old plan or decision. Broader conversation is saved immediately and reconsidered by the coordinator; a message is never an acceptance.

### Exact saved-command confirmation

Canonical hashing uses `orderedJson`/`digest` in `values.ts`: recursively sorted object keys, array order preserved, undefined properties omitted, SHA-256. Confirmation matches subject, command, actual actor, kind and canonical payload—not the present amount alone. Supported kinds and payloads:

- `Work budget changed`: `{ workPlanId, expectedRevision, budgetCents }`; subject is the reviewed plan ID.
- `Work plan changed`: `{ workPlanId, expectedRevision, changes }`; `changes` is the parsed structured form; subject is the reviewed plan ID even if the result is a new proposal.
- `Work plan accepted`: `{ workPlanId, expectedRevision }`; subject is the accepted plan ID. This confirmation remains valid after later proposals.
- `Message sent`: `{ handoffId, message, expectedPlanRevision }`; subject is the handoff ID.
- `Document received`: `{ handoffId, document }`; document is the parsed/canonical `ReceivedDocument`; subject is the handoff ID.

## Initial and incoming information

`MoveOutNotice` remains the narrow structured intake contract in `notice.ts`. Documents, agreements and obligations can be omitted, and there need not be a provider or quote. `tenancy.endDate` is optional. `endingKind` is `Tenancy ending`, `Occupant departure`, or `To confirm`; an occupant-only or unconfirmed ending cannot set a tenancy end date. Document inputs can include source version, available date, file type and bounded structured supporting details. Original media remains unchanged. A notice with prepared supporting documents requires configure permission; raw original media references cannot be introduced through a notice.

`receiveHandoffDocument` accepts `ReceivedDocument` in `documentIntake.ts`: source system, stable source reference, source version, title, kind, text, known sender, available date and `Original`/`Prepared` source kind. **This is authenticated demonstration source setup and requires configure permission**, not an unrestricted incoming-mail or financial-confirmation API. Work-only users use operator conversation; normal external ingestion still needs a verified adapter. Same source/version with changed content is rejected. Prepared input cannot assert original media references or server provenance. Original input is association-only: it must supply `associatedDocumentId` of an existing original in this exact handoff, with exactly the same reader audience and unchanged text, identity, date, sender and page range. The server fetches the actual original with public `MediaSets.MediaSets.readOriginal`; denied/unavailable originals fail closed. No new original audience or corpus association is created by this Action. This relies on the already-established association; it is not generic proof of every principal’s access to every media RID.

Only the workspace's same-reader audience can be used for a derived proposal or correspondence. Narrower or different reader scopes fail before their text reaches the model or a broader record; the code never declassifies a source. Source versions **and content**, business date, relevant facts and authority are checked after inference. Unrelated workspace revision/activity does not invalidate the result. Funding is checked independently at commitment/payment time; a funding confirmation does not rewrite the work mandate.

## Responsive counterpart source contracts

A test provider needs persistent, source-backed service information rather than an already-created offer or a prewritten activity feed. The full validators/types are in `supportingSources.ts`. Store this bounded information in a `Provider information` Document attributed to the actual provider. Its `detailsJson` is:

```ts
{ services: [{
  serviceId: string, title: string,
  kind: "Assessment" | "Repair" | "Cleaning" | "Verification",
  currency: string,
  lines: { lineId: string, description: string, amountCents: string }[],
  depositCents: string, paymentTerms: string, requirements: string[],
  availableFrom: string, validUntil: string,
  durationMinutes: number, responseMinutes: number,
  effects: { lineId: string, conditionIds: string[], method: string }[]
}] }
```

All timestamps are UTC ISO timestamps. A service line has one described physical effect/check. `requirements` states requirements this offer actually meets; it is not a list of system tasks. The initial agent tool request is `Inquiry { purpose: "Quote", recipientPartyId, question, providerDocumentId, serviceId }`—**no quote ID is needed**. Delivery/status requests for an existing offered job use the older `ProviderRequest` contract. Both use the same durable Message collection and coordinator.

A `Property condition` Document supplies attributed observations for the responsive counterpart, not an expected final answer:

```ts
{ conditions: [{
  conditionId: string, description: string,
  state: "Satisfied" | "Deficient" | "Not checked",
  repairable: boolean, accessible: boolean
}] }
```

Only commissioned service effects change corresponding conditions. An assessment records what it observes without repairing anything. Inaccessible/missing checks remain unchecked, and defects outside the service capability remain deficient. Results create a new prepared condition version linked to the prior document; originals remain untouched. A report, completion check and invoice are generated from the actual saved appointment, scope and resulting state. Final payment requires a checked complete job and matching invoice.

A configure-authorized `Owner funding` Document supplies an attributed funding allocation and payment-response behavior to the isolated demonstration interface. This is not a live-bank confirmation:

```ts
{
  ownerPartyId: string, currency: string, confirmedCents: string,
  confirmedAt: string,
  paymentBehavior: "Settle" | "Reject" | "Uncertain",
  responseMinutes: number
}
```

The document sender must match its funding owner. The funding owner need not be the tenancy landlord. Stable document source references distinguish allocations from versions of the same allocation. An additional independent allocation is recognized when needed, not inferred from an increased budget. Known commitments remain held during uncertain outcomes. The payment counterpart responds to the same saved instruction; `Uncertain` does not mean safe to resend. This is a stateful test payment interface, not a live bank connection.

Ordinary information questions go to known parties. Replies use material attributed to the respondent; absence remains an unanswered question, followed up on its own schedule. The operator is not required to act as the provider.

### Already existing business records

A received document can carry one typed `offer`, `job`, `report` or `invoice` envelope in `detailsJson` for Document kinds `Quote`, `Job record`, `Inspection` or `Invoice`, respectively. Bodies follow `QuoteOffer`, `ExistingJob`, `InspectionReport` and `SupplierInvoice` in `deliveryContracts.ts`, **omitting** `sourceSystem`, `sourceRecordId`, and `sourceDocumentId`; the source-record adapter binds those from the actual received document. It checks the ordinary business record validators before writing. Existing work does not get a fabricated Handoff instruction or approval. A reported-complete existing job still needs its completion evidence. Record amendments/corrections explicitly; reusing one business source identity with different issued content is not a retry.

Version-one acceptances remain immutable and readable. `recognizeAcceptedWork` in `acceptedWork.ts` recognizes the **original Handoff instruction**, once, from an explicitly prepared evidence mapping, its exact immutable Decision, whole accepted assessment/check scope, original source quote, and matching original outgoing request/acknowledgment pair. It creates a Handoff-origin Job retaining the old Decision/request identities; it does not create another order, Decision, formal version-two acceptance, or fictitious externally commissioned history. Repairs are excluded from this recognition. New repair recommendations remain separate proposals requiring acceptance. Missing or mismatched original correspondence fails closed.

## Coordinator and wake-up configuration

The release owner must wire the new function version into the existing Actions and the one shared continuation mechanism. Use a **new `commandId` per coordinator turn**. An initial successful `continue:<decision>` call cannot be reused forever; that receipt represents an already-completed invocation. Business instruction identities remain stable independently of turn IDs.

- Intake or a new operator message/document makes work ready immediately.
- Scheduled execution should resume work whose `nextWakeAt` is due, including waiting states, not only newly accepted plans.
- Execute the function-backed Action, not a plain Function effect that merely returns edits.
- The configured worker identity must have workspace work permission and the same protected source access. It is not the accepting user.
- Newly queued inquiries produce replies in later committed turns. Funding recognition, commissions, payment intent, observations and completion recognition are separated only where the next operation needs committed state.
- `businessTime` and `nextBusinessAt` are internal Agent work fields. The counterpart follows the handoff's business timeline, including historical quotes and observations; `nextWakeAt` remains real server time. Test waits are compressed to at most one minute, preserving their business-event ordering. Operator messages, decisions and activity retain their actual recording time. No clock-management button or source-date rewriting is required.

The current implementation does not prove a universal distributed transaction or serializable multi-object lock. It uses stable instruction IDs, exact captures, relevant guards and the existing touched-record mechanisms; actual concurrent Action/worker behavior still requires release-level verification. Do not activate a live effect adapter on the strength of unit tests alone.

## Information replies

The test correspondence interface answers an `Information` request from the recipient's own material only:

- A provider with `Provider information` answers from its published service terms: earliest visit, visit length, reply time, validity, payment terms and requirements. A visit time is agreed only after commissioning.
- Any other correspondent discloses its attributed documents, as before.
- A correspondent with nothing on file answers once and definitively (`unanswered: false`). No reminder follows; the unchanged question coalesces to the same request identity.
- `Funding` requests are unchanged: without owner funding material they stay open and receive one reminder.
- Replies saved as `unanswered: true` before this change keep their single reminder.

## Work requirements

- A proposal's `fixedRequirements` may contain only the handoff's requirements and those on the current plan, which the operator sets through Change work plan. A model draft that adds its own is rejected with validation code `requirements`; its advice belongs in the rationale.
- An accepted requirement that the vendor's offer does not state no longer blocks the order. The order lists it and asks the vendor to confirm it when booking. The vendor's first reply to that order confirms it (`confirmedRequirements` in the reply details) before any booking; it is not repeated later.
- When accepted work still cannot be ordered (offer no longer valid, owner funds short, case records changed) and reasoning proposes nothing new, the work is set to `Needs attention` and the next step states the reason. It waits for the operator instead of reading `Waiting for information`.

## Verification and release handoff

Tests are in `__tests__/coordinator.test.ts` and the existing delivery suites. They exercise the connected flow, successive assessment/repair decisions, discussion, incoming documents, existing work, exact receipts, narrowed source rejection, future-source exclusion, changed source/authority, unrelated activity, funding shortfall, rejected/uncertain payment, inaccessible/deficient work, independent physical completion, and historical business time. Test provider behavior is computed from source terms/conditions and persisted jobs; the model mock does not supply future invoices or results.

Run from `typescript-functions`: `npx tsc --noEmit -p src/tsconfig.json` and `npm test -- --maxWorkers=2`. Managed diagnostics discovers the functions. A release owner must then commit explicit file paths, run CI, publish, bind Actions, configure wakes, update the client version/contract, and exercise actual branch Actions. No new Function-target Eval run can evaluate these unpublished changes; targeting the prior tag would test the prior implementation.

The read-only branch preview verified the version-two workspace including the existing version-one acceptance. A real GPT-5.2 coordinator preview read relevant documents through a tool and returned proposed information requests without applying any edits. That confirms the model/tool route, not completed primary-case delivery, worker scheduling, UI comprehension or operator acceptance. The source-preparation/adapter setup for the full case, live branch integration and focused operator check remain with the release owner.


## Focused source preparation and original-work continuation

The wrapper signatures and frontend version-two DTO are unchanged. All changes below are inside bounded document JSON or private helpers. This review does not publish, commit, seed business objects, bind Actions, or run the worker. The release owner retains those steps.

### Intake contract and immutable association

Use `receiveHandoffDocument(client, handoffId, documentJson, commandId, currentUserId)` through the existing configure-authorized intake. Bind currentUserId to the authenticated actor. Never supply `_preparation`; the server writes it. Use a separate command per input and per coordinator turn.

```ts
{
  sourceSystem: string, sourceRecordId: string, sourceVersion: string,
  title: string, kind: string, text: string, partyId: string,
  availableFrom: "YYYY-MM-DD", sourceKind: "Prepared" | "Original",
  associatedDocumentId?: string,
  detailsJson: JSON.stringify(/* the bounded schema below */),
  // Original only: preserve existing mediaSetRid, mediaItemRid, mimeType, pageStart, pageEnd
}
```

For new Prepared documents, stable sourceSystem/sourceRecordId identify a business source; versions do not create additional funding allocations.

For enrichment, set associatedDocumentId to the **existing** document. Supply its unchanged sourceKind, title, kind, text, party and all existing optional media/page/mime fields. A Prepared document stays Prepared; it must have no media IDs. A prior `_preparation` is not required for legacy text: authenticated configure may attribute the new normalization now without pretending the old text was authored now. An Original must already be Original with actual media references. Its same protected audience is checked before `MediaSets.readOriginal` verifies access. Neither path creates a replacement document or copies it into a wider audience.

Existing source metadata must match exactly. If a legacy association lacks metadata, use these **input-only defaults**:

- sourceSystem: `"Received document"`
- sourceRecordId: the associated documentId
- sourceVersion: `"1"`
- availableFrom: current handoff businessDate when the original field is absent

Only `detailsJson` is updated. No fallback value is written into the original metadata. Existing nonempty supporting details cannot change; an identical legacy payload may receive server provenance, and an already attributed retry remains unchanged. These defaults are not evidence of an original publisher or historical issuance date.

### Normalize the same quote

Enrich the existing Quote with:

```ts
{
  offer: {
    title: string, providerPartyId: string,
    kind: "Assessment" | "Verification", currency: string,
    lines: [{ lineId: string, description: string, amountCents: string }],
    totalCents: string, depositCents: string, paymentTerms: string,
    requirements: string[], availableFrom: string, validUntil: string,
    durationMinutes: number, responseMinutes: number
  },
  sourcePassages: string[],
  providerDocumentId: string, serviceId: string, providerSourceVersion: string
}
```

Do **not** put sourceSystem/sourceRecordId/sourceDocumentId inside offer. `recognizeSourceRecord` binds those from the saved Quote document: system is its stored system or `"Received document"`; record identity is `(stored sourceRecordId or documentId) + ":" + (stored sourceVersion or "1")`. Quote identity is `sourceIdentity("quote", workspaceId, { sourceSystem, sourceRecordId })`.

Use every original priced charge exactly once, with its original line description and price; do not aggregate distinct charges into an invented line. All sourcePassages must be verbatim in the existing text. Each line description and its currency-unit price, total, any positive deposit, and the exact paymentTerms must occur in those passages. Keep the quotation's actual payment terms rather than paraphrasing them. The normalizer still relies on configure-authorized interpretation for semantic equivalence; numeric/text checks are not a general natural-language contract verifier. Preserve original requirements, currency, exclusions and accepted full scope.

Register the corresponding Provider information first, with its actual service schema from above. Its lines, kind, currency, advance, payment terms and confirmed requirements must cover this exact quote. `providerSourceVersion` is the provider document's sourceVersion (or digest(detailsJson) only when it lacks one). Optional service `invoiceDueMinutes` records the quoted payment period for the generated invoice; provide it for an associated quote rather than relying on the legacy one-day default. It belongs to the service, **not** the offer envelope. The report may arrive at visit completion; it does not assert a later contractual deadline was missed.

### Map many accepted prose terms to the priced lines

Register one configure-authored Prepared `Accepted work mapping` document:

```ts
{
  decisionId: string,
  quoteDocumentId: string,
  fundingId?: string,
  scope: [{
    quoteLineId: string,
    acceptedScopes: string[],
    reason: string,
    sourcePassage: string
  }]
}
```

Each acceptedScopes entry is an **exact** term from the unchanged original plan. A term may apply to multiple quote lines; a quoteLineId appears exactly once. Every quoted line and every accepted term must be covered. The mapping retains separate line charges and the accepted total/currency/requirements. `reason` explains the relation and sourcePassage is verbatim supporting quotation text. Bounds: 48 mapping rows; up to 48 exact terms per row, each up to 1,000 characters; reason 1,500; passage 4,000; total stored scope JSON 100,000. Legacy singular acceptedScope remains supported, but do not supply both fields in the same row.

The Job/frontend still uses `{lineId, description, amountCents, acceptedScope}`. For a multi-term line, acceptedScope is the complete terms joined with newline, bounded to 50,000 characters. No field was added to that DTO and no original acceptance was rewritten.

### Current funding is distinct from recognition of history

fundingId is optional. If specified, derive it as `sourceIdentity("funding", workspaceId, {sourceSystem, sourceRecordId})`, independent of document version. Omit it if unknown. Current configured Owner funding is normalized idempotently before recognition, on a separate committed turn, even when the old acceptance has no version-two quote selections. Legacy confirmations with missing source identity use `"Owner funding confirmation"` and their documentId, consistently across recognition and validation; these defaults do not change their source fields.

Recognition records the already-issued commitment with original decision/request references even if funds are unknown or insufficient. It does not fabricate historical cash and does not make a new purchase. Funding is bound in a later committed turn only when current confirmation, property, currency, existing holds and whole-cost coverage check out. Once bound it is not silently reassigned. If a mapping specifies a fundingId, that exact source must become available; otherwise the coordinator can choose a sufficient current allocation. Without it, Handoff asks a funding question, preserves the visible commitment, and requests no payment. A known new allocation/document wakes the same work; it is not another approval. Advance and invoice dispatch still require funding; invoice dispatch additionally requires supporting completion evidence.

### Appointment and meaningful report

The original outgoing instruction and acknowledgment remain byte-for-byte unchanged. A new **Appointment follow-up**, not a new work order, references the saved acknowledgment using previousReplyId and the recognized job. Its responseDueAt and job nextResponseAt are durable. The provider responds in a later committed turn. Old acknowledgments without sender/job/reply metadata are admitted only by their exact original request correlation and original work-plan/provider relationship. The coordinator waits for the saved response/report/payment time instead of asking for another work acceptance.

Prepare current Property condition as above, with honest accessibility and unknown states. For recognized prose scope, also describe each supported deliverable under the matching service effect:

```ts
effects: [{
  lineId: string, conditionIds: string[], method: string,
  deliverables: [{
    acceptedScope: string,        // exact term used for this line in the mapping
    observation: string,          // substantive report content, not "all done"
    method: string,
    sourceDocumentIds: string[],  // current permitted supporting documents
    conditionIds: string[]        // known conditions needed for this observation
  }]
}]
```

Every mapped term needs a matching supported deliverable before that line is satisfactory. Each observation must be verbatim in at least one named current document, all named sources must be available, and all its named conditions must exist, be accessible, and have known observations. The base service check must also be satisfactory. A missing deliverable, unavailable evidence, inaccessible area or unknown check is explicitly **Not checked**. Detailed accepted terms, observations and methods survive in the generated report and completion check; they are not collapsed into a blanket success. Assessment completion does not repair deficient conditions or imply property readiness. A deficient verification stays deficient.

Configure factual report evidence only where it is genuinely available in the demonstration world. A scope promise is not a photographic schedule, a quantity measurement, a comparison result or a budget note. Do not invent missing measurements, photographs, causation findings or liability conclusions merely to finish the scenario. If those outputs are not known, leave them not checked and provide the actual report later through the existing evidence intake/record path. These prepare-only sources are demo counterpart facts, not proof that a live supplier performed an inspection or a real bank settled funds.

### Verification boundaries

`acceptedWorkFlow.test.ts` uses unrelated structural examples: seven accepted prose terms, three separately priced lines, an existing Prepared quote without media/metadata/provenance, original two-message correspondence and a version-one capture. It exercises configure intake, quote/funds/job recognition in committed turns, explicit appointment follow-up, detailed report/check/invoice and funded settlement. It asserts the complete original plan, decision and two messages are identical, no second plan/Decision/order is created, and the frontend scope shape stays unchanged. Negative cases cover missing/full/new terms, duplicate/missing charges, unrelated evidence, currency/price/requirements, no/insufficient funding, unknown/access-limited checks and invalid enrichment.

No production case keys, monetary amounts or private document text belong in these tests or source files. Read-only scoped ontology checks informed the fix; actual branch Actions, protected-source preparation, worker scheduling/concurrency and primary-case progression remain for the release owner. Do not infer deployment or real-world fulfillment from local tests.

Focused-fix verification: TypeScript no-emit compilation passed; full suite with maxWorkers=2 passed 1,328 tests with 5 existing skips (221 Handoff tests); managed Functions diagnostics completed without errors; `./rune discover` exited successfully with `diagnostics: []`. No function business preview, Action, worker, model invocation, commit, publication or Main edit was performed.
