import { HandoffDocument, HandoffMessage, HandoffParty } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import { createEditBatch } from "@osdk/functions";
import { addActivity, command, wasApplied } from "./activity.js";
import { currentCaller, guardWorkspace, inWorkspace, loadAgentWork, loadHandoff, one, type HandoffEdit } from "./records.js";
import { validateSupportingDocument } from "./supportingSources.js";
import { dateOnly, details, nextRevision, orderedJson, parseDetails, reference, requireHandoff, words } from "./values.js";
import { validateQuoteOffer } from "./quoteCosts.js";
import { wordList } from "./values.js";
import { sameRecord } from "./deliveryRecords.js";
import { associatedOriginal, associatedPrepared, configureSource, preparedDetails, sourceDetails } from "./sourceAccess.js";

export interface ReceivedDocument {
  sourceSystem: string; sourceRecordId: string; sourceVersion: string; title: string; kind: string; text: string;
  partyId: string; availableFrom: string; sourceKind: "Original" | "Prepared";
  associatedDocumentId?: string;
  detailsJson?: string; mediaSetRid?: string; mediaItemRid?: string; mimeType?: string; pageStart?: number; pageEnd?: number;
}
export function readReceivedDocument(json: string): ReceivedDocument {
  const row = details(parseDetails(json, "Incoming document", 140000),
    ["sourceSystem", "sourceRecordId", "sourceVersion", "title", "kind", "text", "partyId", "availableFrom", "sourceKind"],
    ["associatedDocumentId", "detailsJson", "mediaSetRid", "mediaItemRid", "mimeType", "pageStart", "pageEnd"], "Incoming document");
  requireHandoff(row.sourceKind === "Original" || row.sourceKind === "Prepared", "Identify original material or prepared supporting information.");
  requireHandoff((row.mediaSetRid === undefined) === (row.mediaItemRid === undefined), "Identify both the original collection and file.");
  requireHandoff(row.sourceKind !== "Original" || row.mediaItemRid !== undefined, "Keep the original file reference with source material.");
  if (row.pageStart !== undefined || row.pageEnd !== undefined) requireHandoff(typeof row.pageStart === "number" && Number.isSafeInteger(row.pageStart)
    && typeof row.pageEnd === "number" && Number.isSafeInteger(row.pageEnd) && row.pageStart > 0 && row.pageEnd >= row.pageStart,
  "Provide a valid inclusive page range.");
  requireHandoff(row.sourceKind !== "Prepared" || row.mediaItemRid === undefined, "Prepared information cannot assert an original file reference.");
  if (row.detailsJson !== undefined) {
    const body = parseDetails(words(row.detailsJson, "Supporting details", 100000), "Supporting details");
    requireHandoff(typeof body === "object" && body !== null && !Array.isArray(body) && !Object.hasOwn(body, "_preparation"), "Source preparation is recorded by the server.");
  }
  return { ...(row.associatedDocumentId === undefined ? {} : { associatedDocumentId: words(row.associatedDocumentId, "Associated original", 160) }), sourceSystem: words(row.sourceSystem, "Source system", 160), sourceRecordId: words(row.sourceRecordId, "Source reference", 200),
    sourceVersion: words(row.sourceVersion, "Source version", 160), title: words(row.title, "Document title", 200), kind: words(row.kind, "Document kind", 100),
    text: words(row.text, "Relevant document text", 24000), partyId: words(row.partyId, "Sender", 160), availableFrom: dateOnly(row.availableFrom, "Available date"), sourceKind: row.sourceKind,
    ...(row.detailsJson === undefined ? {} : { detailsJson: orderedJson(parseDetails(words(row.detailsJson, "Supporting details", 100000), "Supporting details")) }),
    ...(row.mediaSetRid === undefined ? {} : { mediaSetRid: words(row.mediaSetRid, "Source collection", 200), mediaItemRid: words(row.mediaItemRid, "Source file", 200) }),
    ...(row.mimeType === undefined ? {} : { mimeType: words(row.mimeType, "File type", 200) }),
    ...(row.pageStart === undefined ? {} : { pageStart: row.pageStart as number, pageEnd: row.pageEnd as number }) };
}
/** Incoming correspondence preserves originals; it cannot overwrite an accepted decision or a result. */
export async function receiveDocument(client: Client, handoffId: string, documentJson: string, commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  const input = readReceivedDocument(documentJson), caller = await currentCaller(client, currentUserId);
  const { handoff, workspace } = await loadHandoff(client, handoffId, caller, "work");
  // Source setup is distinct from ordinary operator messages and cannot be a work-user funding shortcut.
  configureSource(workspace, caller);
  const intent = command(workspace.workspaceId, handoffId, handoffId, commandId, caller.id, "Document received", { handoffId, document: input });
  if (await wasApplied(client, workspace, caller, intent)) return [];
  const associated = input.sourceKind === "Original"
    ? await associatedOriginal(client, workspace, caller, handoffId, words(input.associatedDocumentId, "Associated original", 160))
    : input.associatedDocumentId ? await associatedPrepared(client, workspace, caller, handoffId, input.associatedDocumentId) : undefined;
  const documentId = associated?.documentId ?? reference("document", workspace.workspaceId, input.sourceSystem, input.sourceRecordId, input.sourceVersion);
  const [sender, prior, work] = await Promise.all([
    one(client(HandoffParty).where({ partyId: { $eq: input.partyId } })),
    one(client(HandoffDocument).where({ documentId: { $eq: documentId } })), loadAgentWork(client, handoff, workspace, caller),
  ]);
  requireHandoff(sender, "The sender must be a known party."); inWorkspace(sender, workspace, caller);
  const { associatedDocumentId: _association, ...document } = input;
  if (associated) {
    const protectedFields = ["title", "kind", "text", "partyId", "sourceKind", "mediaSetRid", "mediaItemRid", "mimeType", "pageStart", "pageEnd"];
    requireHandoff(protectedFields.every((key) => Reflect.get(associated, key) === Reflect.get(document, key))
      && (associated.sourceVersion ?? "1") === document.sourceVersion
      && (associated.sourceSystem ?? "Received document") === document.sourceSystem
      && (associated.sourceRecordId ?? associated.documentId) === document.sourceRecordId
      && document.availableFrom === (associated.availableFrom ?? handoff.businessDate),
    "Keep the associated original text, identity, date, sender and page range unchanged.");
    if (document.kind === "Quote" && document.detailsJson) {
      const normalized = sourceDetails(document.detailsJson);
      const evidence = wordList(normalized.sourcePassages, "Quoted source passages", 16, 1, 4000);
      requireHandoff(evidence.every((passage) => associated.text?.includes(passage)), "Use actual passages from this original quote.");
      const offer = validateQuoteOffer({ ...(normalized.offer as object), sourceSystem: associated.sourceSystem ?? "Received document",
        sourceRecordId: associated.sourceRecordId ?? associated.documentId, sourceDocumentId: associated.documentId });
      requireHandoff(offer.providerPartyId === associated.partyId, "Normalize the original quote from its actual provider.");
      const quoted = evidence.join("\n");
      const priceAppears = (text: string, cents: string): boolean => {
        const units = BigInt(cents) / 100n, fraction = (BigInt(cents) % 100n).toString().padStart(2, "0");
        const decimal = fraction === "00" ? "(?:\\.00)?" : `\\.${fraction}`;
        return new RegExp(`(?:^|[^0-9.])${units}${decimal}(?![0-9]|\\.[0-9])`).test(text.replaceAll(",", ""));
      };
      requireHandoff(offer.lines.every((line) => evidence.some((passage) => passage.split(line.description).slice(1).some((suffix) => {
        // The same service can appear in the description before its priced entry. Check each
        // occurrence, but never substitute a later total or another charge for its first price.
        const firstPrice = suffix.split(/[;\n]/)[0]!.match(/[0-9]+(?:,[0-9]{3})*(?:\.[0-9]{1,2})?/u)?.[0];
        return firstPrice !== undefined && priceAppears(firstPrice, line.amountCents);
      }))) && priceAppears(quoted, offer.totalCents) && (offer.depositCents === "0" || priceAppears(quoted, offer.depositCents))
        && quoted.includes(offer.paymentTerms),
      "Each original quoted charge, total and payment terms need their actual verbatim source passages.");
    }
    requireHandoff(!associated.detailsJson || Object.keys(sourceDetails(associated.detailsJson)).length === 0 || orderedJson(sourceDetails(associated.detailsJson)) === orderedJson(sourceDetails(document.detailsJson ?? "{}")),
      "This original already has different supporting details. Keep the original and record the correction separately.");
  }
  validateSupportingDocument({ documentId, ...document });
  document.detailsJson = preparedDetails(document.detailsJson, caller, associated ? [associated.documentId] : []);
  const shared = { workspaceId: workspace.workspaceId, readerIds: [...workspace.readerIds!], handoffId };
  const saved = { ...shared, ...document, documentId };
  if (prior) {
    inWorkspace(prior, workspace, caller);
    if (!associated) {
      sameRecord(prior, saved, ["detailsJson"]);
      requireHandoff(orderedJson(sourceDetails(prior.detailsJson ?? "{}")) === orderedJson(sourceDetails(document.detailsJson)),
        "This source reference already has different saved details. Keep the original and record the correction separately.");
    }
  }
  const batch = createEditBatch<HandoffEdit>(client), now = new Date().toISOString(), revision = nextRevision(handoff.revision);
  const enriching = associated && (!associated.detailsJson || Object.keys(sourceDetails(associated.detailsJson)).length === 0
    || !Object.hasOwn(parseDetails(associated.detailsJson, "Supporting details") as object, "_preparation"));
  if (enriching) batch.update(associated, { detailsJson: document.detailsJson });
  if (prior && !enriching) {
    guardWorkspace(batch, workspace, commandId);
    addActivity(batch, intent, shared.readerIds, "Document received", "This source version was already saved.", handoff.revision!, now);
    return batch.getEdits();
  }
  if (!prior) {
    batch.create(HandoffDocument, saved);
    batch.create(HandoffMessage, { ...shared, messageId: reference("message", workspace.workspaceId, documentId),
      title: "Supporting material received", body: "New supporting material has been received for the handoff.", senderPartyId: sender.partyId,
      recipientPartyId: sender.partyId, purpose: "Document", direction: "Incoming", status: "Received", createdAt: now, externalReference: documentId });
  }
  batch.update(work, { status: "Ready to continue", nextStep: "Consider the new supporting material.", nextWakeAt: now, nextBusinessAt: undefined, updatedAt: now, operationKey: `document:${documentId}` });
  batch.update(handoff, { revision, nextStep: "Handoff will consider the new supporting material." });
  guardWorkspace(batch, workspace, commandId);
  addActivity(batch, intent, shared.readerIds, "Document received", "Supporting material was saved without changing accepted decisions or earlier results.", revision, now);
  return batch.getEdits();
}
