import type { Client, Osdk } from "@osdk/client";
import { HandoffDocument } from "@ontology/sdk";
import { MediaSets } from "@osdk/foundry";
import { authorize, inWorkspace, one, type Caller, type Workspace } from "./records.js";
import { details, orderedJson, parseDetails, requireHandoff, words } from "./values.js";

export interface Preparation { actorId: string; purpose: "Demonstration configuration"; sourceDocumentIds: string[] }
/** Internal attribution is written by authenticated configuration, never accepted from model/input JSON. */
export function preparedDetails(value: string | undefined, caller: Caller, sourceDocumentIds: string[] = []): string {
  const body = value === undefined ? {} : sourceDetails(value);
  requireHandoff(!value || !Object.hasOwn(parseDetails(value, "Supporting details") as object, "_preparation"), "Source preparation is recorded by the server.");
  return orderedJson({ ...body, _preparation: { actorId: caller.id, purpose: "Demonstration configuration", sourceDocumentIds } });
}
export function sourceDetails(value: string): Record<string, unknown> {
  const parsed = parseDetails(value, "Supporting details");
  requireHandoff(typeof parsed === "object" && parsed !== null && !Array.isArray(parsed), "Supporting details need named fields.");
  const { _preparation: _internal, ...body } = parsed as Record<string, unknown>;
  return body;
}
export function preparation(document: { detailsJson?: string }): Preparation {
  const body = parseDetails(words(document.detailsJson, "Configured source", 140000), "Configured source") as Record<string, unknown>;
  const row = details(body._preparation, ["actorId", "purpose", "sourceDocumentIds"], [], "Source preparation");
  requireHandoff(row.purpose === "Demonstration configuration" && Array.isArray(row.sourceDocumentIds)
    && row.sourceDocumentIds.every((id) => typeof id === "string"), "This counterpart needs authenticated source configuration.");
  return { actorId: words(row.actorId, "Configuration author", 160), purpose: "Demonstration configuration", sourceDocumentIds: row.sourceDocumentIds as string[] };
}

/** Legacy Prepared text may be attributed now, but never relabelled as an original file. */
export async function associatedPrepared(client: Client, workspace: Workspace, caller: Caller, handoffId: string,
  documentId: string): Promise<Osdk.Instance<HandoffDocument>> {
  configureSource(workspace, caller);
  const document = await one(client(HandoffDocument).where({ documentId: { $eq: documentId } }));
  requireHandoff(document && document.handoffId === handoffId && document.sourceKind === "Prepared"
    && !document.mediaSetRid && !document.mediaItemRid, "Use Prepared text already associated with this handoff and its protected audience.");
  inWorkspace(document, workspace, caller);
  return document;
}
/** Association-only: caller access to a file is NOT proof that all workspace readers may see it. */
export async function associatedOriginal(client: Client, workspace: Workspace, caller: Caller, handoffId: string,
  documentId: string): Promise<Osdk.Instance<HandoffDocument>> {
  const document = await one(client(HandoffDocument).where({ documentId: { $eq: documentId } }));
  requireHandoff(document && document.handoffId === handoffId && document.sourceKind === "Original" && document.mediaSetRid && document.mediaItemRid,
    "Use an original already associated with this handoff and its protected audience.");
  inWorkspace(document, workspace, caller);
  // Supported public API verifies the reference actually remains available to this invocation.
  const original = await MediaSets.MediaSets.readOriginal(client, document.mediaSetRid, document.mediaItemRid);
  requireHandoff(original.ok, "The associated original is no longer available to this request.");
  await original.body?.cancel();
  return document;
}
export function configureSource(workspace: Workspace, caller: Caller): void {
  authorize(workspace, caller, "configure");
}
