import {
  HandoffWorkspace, HandoffProperty, HandoffParty, HandoffTenancy, HandoffAgreement,
  HandoffDocument, HandoffObligation, HandoffCase, HandoffAgentWork,
} from "@ontology/sdk";
import type { Client } from "@osdk/client";
import { Aliases, createEditBatch } from "@osdk/functions";
import { command, addActivity, wasApplied } from "./activity.js";
import { currentCaller, authorize, bounded, guardWorkspace, inWorkspace, loadWorkspace, one,
  type Caller, type HandoffEdit, type Workspace } from "./records.js";
import { configureSource, preparedDetails } from "./sourceAccess.js";
import { validateSupportingDocument } from "./supportingSources.js";
import { readMoveOutNotice } from "./notice.js";
import { digest, orderedJson, reference, requireHandoff, words } from "./values.js";

/** A new workspace grants its creator access; no existing workspace grants are changed. */
export async function openWorkspace(client: Client, name: string, commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  words(name, "Workspace name", 200);
  words(commandId, "Request reference", 160);
  const caller = await currentCaller(client, currentUserId);
  const workspaceId = reference("workspace", caller.id, commandId);
  const intent = command(workspaceId, workspaceId, undefined, commandId, caller.id, "Workspace created", { name });
  const existing = await one(client(HandoffWorkspace).where({ workspaceId: { $eq: workspaceId } }));
  if (existing) {
    authorize(existing, caller, "configure");
    requireHandoff(await wasApplied(client, existing, caller, intent), "This workspace already exists. Open it to continue.");
    return [];
  }
  const batch = createEditBatch<HandoffEdit>(client);
  batch.create(HandoffWorkspace, {
    workspaceId, name, readerIds: [caller.id], workUserIds: [caller.id], decideUserIds: [caller.id],
    adminUserIds: [caller.id], modelRid: Aliases.model("workReasoner").rid, mode: "demo", currency: "USD",
    lastCommandId: commandId, revision: "1",
  });
  addActivity(batch, intent, [caller.id], "Workspace opened", "The workspace is ready to receive a move-out notice.", "1", new Date().toISOString());
  return batch.getEdits();
}

/** Shared source facts are retained only when every supplied business field agrees. */
function keepExisting(existing: { workspaceId?: string; readerIds?: string[] } | undefined,
  proposed: object, workspace: Workspace, caller: Caller): boolean {
  if (!existing) return false;
  inWorkspace(existing, workspace, caller);
  requireHandoff(Object.entries(proposed).filter(([key]) => key !== "readerIds")
    .every(([key, value]) => orderedJson(Reflect.get(existing, key)) === orderedJson(value)),
  "A source record already has different details. Check the original notice before continuing.");
  return true;
}

/** Resolve all notice references, then return one atomic batch of business records and the next work step. */
export async function receiveNotice(client: Client, workspaceId: string, noticeJson: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  const notice = readMoveOutNotice(noticeJson);
  const caller = await currentCaller(client, currentUserId);
  const workspace = await loadWorkspace(client, workspaceId, caller, "work");
  if (notice.documents.length) configureSource(workspace, caller);
  requireHandoff(notice.documents.every((doc) => !doc.mediaSetRid && !doc.mediaItemRid && doc.sourceKind !== "Original"),
    "Associate protected originals through the source intake, not a move-out notice.");
  const source = (kind: string, id: string): string => reference(kind, workspaceId, notice.sourceSystem, id);
  const handoffId = source("handoff", notice.sourceRecordId);
  // Empty requirements keep the intent of notices received before this optional field was added.
  const payload = { ...notice, tenancy: { ...notice.tenancy, endingKind: notice.tenancy.endingKind === "Tenancy ending" ? undefined : notice.tenancy.endingKind }, fixedRequirements: notice.fixedRequirements?.length ? notice.fixedRequirements : undefined };
  const intent = command(workspaceId, handoffId, handoffId, commandId, caller.id, "Notice received", payload);
  if (await wasApplied(client, workspace, caller, intent)) return [];
  const existingHandoff = await one(client(HandoffCase).where({ handoffId: { $eq: handoffId } }));
  requireHandoff(!existingHandoff, "This move-out notice has already been received. Open its handoff to continue.");
  const common = { workspaceId, readerIds: [...workspace.readerIds!] };
  const property = { ...common, propertyId: source("property", notice.property.sourceId),
    name: notice.property.name, address: notice.property.address, description: notice.property.description };
  const parties = notice.parties.map(({ sourceId, ...party }) => ({ ...common, partyId: source("party", sourceId), ...party }));
  const tenancy = { ...common, tenancyId: source("tenancy", notice.tenancy.sourceId), propertyId: property.propertyId,
    title: notice.tenancy.title, landlordPartyId: source("party", notice.tenancy.landlordPartySourceId),
    tenantPartyIds: notice.tenancy.tenantPartySourceIds.map((id) => source("party", id)),
    startDate: notice.tenancy.startDate, endingKind: notice.tenancy.endingKind, endDate: notice.tenancy.endDate, noticeDate: notice.tenancy.noticeDate };
  const documents = notice.documents.map(({ sourceId, partySourceId, ...document }) => ({
    ...common, handoffId, documentId: source("document", sourceId), sourceSystem: notice.sourceSystem, sourceRecordId: sourceId, ...document, sourceVersion: document.sourceVersion ?? digest({ text: document.text, detailsJson: document.detailsJson, mediaSetRid: document.mediaSetRid, mediaItemRid: document.mediaItemRid }),
    partyId: partySourceId === undefined ? undefined : source("party", partySourceId),
  }));
  documents.forEach(validateSupportingDocument);
  documents.forEach((document) => { document.detailsJson = preparedDetails(document.detailsJson, caller); });
  const agreements = notice.agreements.map(({ sourceId, sourceDocumentSourceId, ...agreement }) => ({
    ...common, agreementId: source("agreement", sourceId), tenancyId: tenancy.tenancyId, ...agreement,
    sourceDocumentId: source("document", sourceDocumentSourceId),
  }));
  const obligations = notice.obligations.map(({ sourceId, responsiblePartySourceIds, beneficiaryPartySourceIds,
    basisAgreementSourceId, basisDocumentSourceId, ...obligation }) => ({
    ...common, handoffId, tenancyId: tenancy.tenancyId, obligationId: source("obligation", sourceId), ...obligation,
    responsiblePartyIds: responsiblePartySourceIds.map((id) => source("party", id)),
    beneficiaryPartyIds: beneficiaryPartySourceIds.map((id) => source("party", id)),
    basisAgreementId: basisAgreementSourceId === undefined ? undefined : source("agreement", basisAgreementSourceId),
    basisDocumentId: basisDocumentSourceId === undefined ? undefined : source("document", basisDocumentSourceId),
  }));
  const [savedProperty, savedTenancy, savedParties, savedDocuments, savedAgreements, savedObligations] = await Promise.all([
    one(client(HandoffProperty).where({ propertyId: { $eq: property.propertyId } })),
    one(client(HandoffTenancy).where({ tenancyId: { $eq: tenancy.tenancyId } })),
    bounded(client(HandoffParty).where({ partyId: { $in: parties.map((party) => party.partyId) } })),
    documents.length ? bounded(client(HandoffDocument).where({ documentId: { $in: documents.map((document) => document.documentId) } })) : Promise.resolve([]),
    agreements.length ? bounded(client(HandoffAgreement).where({ agreementId: { $in: agreements.map((agreement) => agreement.agreementId) } })) : Promise.resolve([]),
    obligations.length ? bounded(client(HandoffObligation).where({ obligationId: { $in: obligations.map((obligation) => obligation.obligationId) } })) : Promise.resolve([]),
  ]);
  const batch = createEditBatch<HandoffEdit>(client);
  if (!keepExisting(savedProperty, property, workspace, caller)) batch.create(HandoffProperty, property);
  if (!keepExisting(savedTenancy, tenancy, workspace, caller)) batch.create(HandoffTenancy, tenancy);
  parties.forEach((party) => {
    if (!keepExisting(savedParties.find((saved) => saved.partyId === party.partyId), party, workspace, caller)) batch.create(HandoffParty, party);
  });
  documents.forEach((document) => {
    if (!keepExisting(savedDocuments.find((saved) => saved.documentId === document.documentId), document, workspace, caller)) batch.create(HandoffDocument, document);
  });
  agreements.forEach((agreement) => {
    if (!keepExisting(savedAgreements.find((saved) => saved.agreementId === agreement.agreementId), agreement, workspace, caller)) batch.create(HandoffAgreement, agreement);
  });
  obligations.forEach((obligation) => {
    if (!keepExisting(savedObligations.find((saved) => saved.obligationId === obligation.obligationId), obligation, workspace, caller)) batch.create(HandoffObligation, obligation);
  });
  const now = new Date().toISOString();
  batch.create(HandoffCase, { ...common, handoffId, propertyId: property.propertyId, tenancyId: tenancy.tenancyId,
    title: notice.title, goal: notice.goal, fixedRequirements: notice.fixedRequirements ?? [],
    businessDate: notice.businessDate, revision: "1", status: "Open",
    physicalProgress: "Preparing plan", financialProgress: "Not started", nextStep: "Read the handoff documents and propose the work." });
  batch.create(HandoffAgentWork, { ...common, workId: reference("work", workspaceId, handoffId), handoffId,
    title: "Prepare the work plan", status: "Plan requested", nextStep: "Read the handoff documents and propose the work.",
    operationKey: `prepare:${handoffId}`, nextWakeAt: now, updatedAt: now });
  guardWorkspace(batch, workspace, commandId);
  addActivity(batch, intent, common.readerIds, "Move-out notice received", "Received the move-out notice and the unit file. Handoff is reviewing them.", "1", now);
  return batch.getEdits();
}
