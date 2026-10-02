import { HandoffActivity, HandoffCase, HandoffDocument, HandoffWorkspace } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import { MediaSets } from "@osdk/foundry";
import { createEditBatch, type Edits } from "@osdk/functions";
import { addActivity, command, wasApplied } from "./activity.js";
import { associatedPrepared, preparedDetails } from "./sourceAccess.js";
import { bounded, currentCaller, guardWorkspace, handoffUnchanged, inWorkspace, loadHandoff, workspaceUnchanged,
  type Caller, type Handoff, type Workspace } from "./records.js";
import { details, nextRevision, orderedJson, parseDetails, reference, requireHandoff, whole, wordList, words } from "./values.js";

export type OriginalAssociationEdit = Edits.Object<HandoffDocument> | Edits.Object<HandoffCase>
  | Edits.Object<HandoffWorkspace> | Edits.Object<HandoffActivity>;

const SOURCE_SYSTEM = "Handoff source file";
const SOURCE_KINDS = ["Reconstructed material", "Contextual material", "Archival material", "Published source text", "Unclassified material"] as const;
interface OriginalInput { mediaSetRid: string; mediaItemRid: string; kind: string }

function readOriginalInput(json: string): OriginalInput {
  const row = details(parseDetails(json, "Source file", 2000), ["mediaSetRid", "mediaItemRid", "kind"], [], "Source file");
  const mediaSetRid = words(row.mediaSetRid, "Source collection", 200), mediaItemRid = words(row.mediaItemRid, "Source file", 200);
  requireHandoff(/^ri\.mio\.[^.]+\.media-set\.[a-f0-9-]{36}$/.test(mediaSetRid)
    && /^ri\.mio\.[^.]+\.media-item\.[a-f0-9-]{36}$/.test(mediaItemRid), "Choose a valid source collection and file.");
  const kind = words(row.kind, "Source classification", 100);
  requireHandoff(SOURCE_KINDS.some((value) => value === kind), "Choose the source's classification.");
  return { mediaSetRid, mediaItemRid, kind };
}

/** A file association carries no business facts and must not become a new planning input. */
export function isFileAssociation(document: { sourceKind?: string; sourceSystem?: string }): boolean {
  return document.sourceKind === "Original" && document.sourceSystem === SOURCE_SYSTEM;
}

export function supportingOriginalIds(document: { sourceDocumentIds?: ReadonlyArray<string> }): string[] {
  return wordList(document.sourceDocumentIds ?? [], "Supporting files", 32);
}

/** Checks original-file permission under the invocation's own token; no read tokens are copied or stored. */
export async function checkOriginalAccess(client: Client, mediaSetRid: string, mediaItemRid: string): Promise<void> {
  const response = await MediaSets.MediaSets.readOriginal(client, mediaSetRid, mediaItemRid);
  await response.body?.cancel();
  requireHandoff(response.ok, "A supporting file is unavailable. Check source access before continuing.");
}

/** All references must resolve inside this returned, date-scoped handoff. Fail closed, including prepared text. */
export async function checkDocumentSources(client: Client, handoff: Handoff, workspace: Workspace, caller: Caller,
  documents: Osdk.Instance<HandoffDocument>[]): Promise<Map<string, string>> {
  const titles = new Map<string, string>();
  const originals = documents.filter((document) => document.sourceKind === "Original");
  documents.forEach((document) => {
    inWorkspace(document, workspace, caller);
    const ids = supportingOriginalIds(document);
    requireHandoff(!ids.length || (document.sourceKind === "Prepared" && document.handoffId === handoff.handoffId),
      "Only prepared documents in this handoff can reference supporting files.");
    requireHandoff(ids.every((id) => originals.some((source) => source.documentId === id
      && source.handoffId === handoff.handoffId && source.workspaceId === workspace.workspaceId)),
    "A supporting file is missing from this handoff.");
    requireHandoff(document.sourceKind === "Original" || (!document.mediaSetRid && !document.mediaItemRid),
      "Prepared text cannot stand in for an original file.");
  });
  await Promise.all(originals.map(async (document) => {
    requireHandoff(document.handoffId === handoff.handoffId && document.mediaSetRid && document.mediaItemRid,
      "An original file needs its own reference in this handoff.");
    await checkOriginalAccess(client, document.mediaSetRid, document.mediaItemRid);
    const info = await MediaSets.MediaSets.info(client, document.mediaSetRid, document.mediaItemRid);
    if (document.sourceSystem === SOURCE_SYSTEM) requireHandoff(document.sourceVersion === String(info.logicalTimestamp),
      "A supporting file has changed. Ask the workspace owner to check its association.");
    if (info.path) titles.set(document.documentId, info.path.split("/").at(-1)!.slice(0, 200));
  }));
  return titles;
}

/**
 * Attach one file to an existing prepared document without importing text or accepting business facts.
 * @param client Platform-injected client; source reads use the current caller's permissions.
 * @param handoffId Handoff being configured.
 * @param preparedDocumentId Existing Prepared document in that handoff.
 * @param sourceJson Only mediaSetRid, mediaItemRid and kind; no titles, extracted text, readers or provenance.
 * @param expectedRevision Revision observed before configuration.
 * @param commandId Idempotency key for this exact association.
 * @param currentUserId Server-bound action actor, independently checked against Admin.Users.getCurrent.
 */
export async function associateOriginal(client: Client, handoffId: string, preparedDocumentId: string, sourceJson: string,
  expectedRevision: string, commandId: string, currentUserId: string): Promise<OriginalAssociationEdit[]> {
  const input = readOriginalInput(sourceJson), revision = whole(expectedRevision, "Handoff revision");
  const caller = await currentCaller(client, currentUserId);
  const { handoff, workspace } = await loadHandoff(client, handoffId, caller, "configure");
  const prepared = await associatedPrepared(client, workspace, caller, handoffId, preparedDocumentId);
  requireHandoff(!prepared.availableFrom || prepared.availableFrom <= handoff.businessDate!, "This document is not yet available in the handoff.");
  const intent = command(workspace.workspaceId, preparedDocumentId, handoffId, commandId, caller.id, "Source file associated",
    { handoffId, preparedDocumentId, input, expectedRevision: revision });
  // Check current source rights even for replay; access once granted is not a reusable capability.
  await checkOriginalAccess(client, input.mediaSetRid, input.mediaItemRid);
  const info = await MediaSets.MediaSets.info(client, input.mediaSetRid, input.mediaItemRid);
  const sourceVersion = words(String(info.logicalTimestamp), "Source version", 160);
  requireHandoff(/^[0-9]+$/.test(sourceVersion), "The source file needs a valid stored version.");
  const mimeType = info.originallyUploadedFileMimeType ?? info.mimeType;
  requireHandoff(mimeType === "application/pdf", "Choose a PDF source file.");
  const documentId = reference("original", workspace.workspaceId, handoffId, input.mediaSetRid, input.mediaItemRid);
  const documents = await bounded(client(HandoffDocument).where({ handoffId: { $eq: handoffId }, workspaceId: { $eq: workspace.workspaceId } }), 100);
  const prior = documents.find((doc) => doc.documentId === documentId);
  const ids = supportingOriginalIds(prepared);
  await checkDocumentSources(client, handoff, workspace, caller, documents.filter((doc) => !doc.availableFrom || doc.availableFrom <= handoff.businessDate!));
  if (prior) {
    inWorkspace(prior, workspace, caller);
    requireHandoff(prior.sourceKind === "Original" && prior.mediaSetRid === input.mediaSetRid && prior.mediaItemRid === input.mediaItemRid
      && prior.sourceVersion === sourceVersion && prior.kind === input.kind && prior.sourceSystem === SOURCE_SYSTEM,
    "This file already has a different association. Keep its recorded identity and classification.");
  }
  const replay = await wasApplied(client, workspace, caller, intent);
  if (replay) {
    requireHandoff(prior && ids.includes(documentId), "The saved source association is no longer present. Refresh the handoff.");
    return [];
  }
  requireHandoff(whole(handoff.revision, "Handoff revision") === revision, "The handoff changed. Refresh it before associating a file.");
  if (prior && ids.includes(documentId)) return [];
  requireHandoff(ids.length < 32 && (prior || documents.length < 100), "This handoff has reached its supporting file limit.");
  const latest = await loadHandoff(client, handoffId, caller, "configure");
  const latestPrepared = await associatedPrepared(client, latest.workspace, caller, handoffId, preparedDocumentId);
  requireHandoff(handoffUnchanged(handoff, latest.handoff) && workspaceUnchanged(workspace, latest.workspace)
    && orderedJson(prepared) === orderedJson(latestPrepared), "The handoff changed while the source was checked. Refresh it to continue.");
  const batch = createEditBatch<OriginalAssociationEdit>(client), now = new Date().toISOString();
  const readerIds = [...workspace.readerIds!], resultRevision = nextRevision(handoff.revision);
  if (!prior) batch.create(HandoffDocument, {
    documentId, workspaceId: workspace.workspaceId, handoffId, readerIds, sourceKind: "Original",
    // Do not copy protected filenames, source bodies or extracted text into workspace-readable records.
    title: input.kind, kind: input.kind, text: "Open the attached file.", mediaSetRid: input.mediaSetRid, mediaItemRid: input.mediaItemRid,
    mimeType, sourceSystem: SOURCE_SYSTEM, sourceRecordId: `${input.mediaSetRid}/${input.mediaItemRid}`, sourceVersion,
    availableFrom: handoff.businessDate, detailsJson: preparedDetails(undefined, caller),
  });
  batch.update(prepared, { sourceDocumentIds: [...ids, documentId].sort() });
  batch.update(handoff, { revision: resultRevision });
  guardWorkspace(batch, workspace, commandId);
  addActivity(batch, intent, readerIds, "Source file associated", "A supporting file was associated with a document.", resultRevision, now);
  return batch.getEdits();
}
