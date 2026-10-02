# Handoff supporting files

## Additive workspace v2 contract

`getHandoffWorkspace` keeps `version: "2"`. Each document may additionally contain:

```ts
sourceKind?: "Original" | "Prepared";
sourceDocumentIds?: string[];
```

Absent fields remain valid for older clients/records. A nonempty `sourceDocumentIds` is at most 32 distinct IDs, each resolving to a separate `sourceKind: "Original"` entry in **the same returned workspace and handoff**. The summary stays Prepared, retains its title/text, and has no media references of its own. Each attached file has its own media references and stored source version. Its `kind` retains the configured classification; Original means an actual file, not an authenticated historical exhibit. No extracted source text is copied into the document record: the pointer's text is `Open the attached file.` The displayed filename is loaded live after checking file access, not persisted with workspace-wide permissions.

The read fails closed if an Original is missing, outside the handoff/audience, not yet available, unreadable/revoked, or (for these associations) has a changed media logical timestamp. There is no partial response containing dependent Prepared text or dangling references. This check uses the **current invocation's** public `MediaSets.readOriginal` and `MediaSets.info` APIs, not the configurator's token or a saved media read token. Existing readerIds and workspace authority checks remain in force. Clients must still honor their original-file availability checks, because access can be revoked after the workspace read. Include `sourceKind` and `sourceDocumentIds` in the frontend document/cache key; never substitute the summary for a missing original.

## Configure-only association

Function: `associateHandoffOriginal`. Parameters, all strings:

- `handoffId`
- `preparedDocumentId` — an existing Prepared document in that handoff, without media references
- `sourceJson` — exactly `{ mediaSetRid, mediaItemRid, kind }`
- `expectedRevision` — current handoff revision, canonical nonnegative decimal string
- `commandId` — request identity
- `currentUserId` — **bound by the Action rule to current_user_id**, not an action form parameter

`kind` is one of: `Reconstructed material`, `Contextual material`, `Archival material`, `Published source text`, `Unclassified material`. It is an explicit configuration classification, not a verification of document assertions. The supplied source must be a readable PDF. File version and MIME type come from the supported public media API. Titles, source bodies, extracted text, actors, readers, timestamps, page selections and provenance are not accepted from the client.

The function independently resolves the signed-in user using `Admin.Users.getCurrent`, requires configure authority and an exact workspace audience, and rechecks authority/target state before returning edits. It creates one stable file identity per workspace/handoff/media-set/media-item, appends that identity to the summary's protected `sourceDocumentIds`, and records the existing standard command receipt plus revisions. Exact replay is empty after rechecking current source rights. A changed command payload, stale revision or changed source identity/classification is rejected. Re-associating the same file with a new current request is a no-op; the same file may support multiple Prepared documents without duplicate originals.

No document intake, notice or conversation path can bootstrap this association. Their existing validation remains unchanged. No media bytes, permissions, party statements, funding, accepted work, decisions, messages, agent schedules or external effects are changed. Pointer-only attachments are returned in the reader contract but excluded from planning inputs and source materiality: attaching a file does not assert a new fact or invalidate an accepted mandate. Association alone establishes neither factual accuracy nor resident liability.

## Release boundary

Only schema/code/Action metadata is staged on the feature branch. No case association is executed, no Main user edits are imported into the branch, and no Main publication/merge is performed. Live Main records must remain untouched until separately authorized configuration. The branch's Document index does not contain Main edit-only documents, so a business association preview against those Main IDs correctly refuses the missing Prepared target. Positive edit-array behavior is covered by unit tests; live media access and metadata reads were verified separately. Platform concurrent-Action conflict behavior still requires release-owner validation; the local test store is not an Action conflict simulator.
