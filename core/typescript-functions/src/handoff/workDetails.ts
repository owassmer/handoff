import { HandoffProperty, HandoffTenancy, HandoffDocument, HandoffAgreement, HandoffObligation, HandoffParty } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import { bounded, inWorkspace, one, type Caller, type Handoff, type Workspace } from "./records.js";
import { requireHandoff, words } from "./values.js";
import { validateWorkContext, type WorkContext } from "./reasoner.js";
import { checkDocumentSources, isFileAssociation } from "./originals.js";

export interface HandoffDetails {
  property: Osdk.Instance<HandoffProperty>;
  tenancy: Osdk.Instance<HandoffTenancy>;
  documents: Osdk.Instance<HandoffDocument>[];
  originalTitles?: Map<string, string>;
  supportingFiles?: Osdk.Instance<HandoffDocument>[];
  agreements: Osdk.Instance<HandoffAgreement>[];
  obligations: Osdk.Instance<HandoffObligation>[];
  parties: Osdk.Instance<HandoffParty>[];
}

/** Read only the current handoff's documents, tenancy agreements and referenced parties. */
export async function loadDetails(client: Client, handoff: Handoff, workspace: Workspace, caller: Caller): Promise<HandoffDetails> {
  requireHandoff(handoff.propertyId && handoff.tenancyId, "The handoff needs a property and tenancy.");
  const [property, tenancy, handoffDocuments, agreements, obligations] = await Promise.all([
    one(client(HandoffProperty).where({ propertyId: { $eq: handoff.propertyId } })),
    one(client(HandoffTenancy).where({ tenancyId: { $eq: handoff.tenancyId } })),
    bounded(client(HandoffDocument).where({ handoffId: { $eq: handoff.handoffId }, workspaceId: { $eq: workspace.workspaceId } }), 100),
    bounded(client(HandoffAgreement).where({ tenancyId: { $eq: handoff.tenancyId }, workspaceId: { $eq: workspace.workspaceId } }), 16),
    bounded(client(HandoffObligation).where({ handoffId: { $eq: handoff.handoffId }, workspaceId: { $eq: workspace.workspaceId } }), 24),
  ]);
  requireHandoff(property && tenancy && tenancy.propertyId === property.propertyId, "The handoff's property and tenancy need to be checked.");
  [property, tenancy, ...handoffDocuments, ...agreements, ...obligations].forEach((record) => inWorkspace(record, workspace, caller));
  const agreementDocumentIds = [...new Set(agreements.map((agreement) => words(agreement.sourceDocumentId, "Agreement document reference", 160)))]
    .filter((id) => !handoffDocuments.some((document) => document.documentId === id));
  const agreementDocuments = agreementDocumentIds.length ? await bounded(client(HandoffDocument).where({
    workspaceId: { $eq: workspace.workspaceId }, documentId: { $in: agreementDocumentIds },
  }), 24) : [];
  agreementDocuments.forEach((document) => inWorkspace(document, workspace, caller));
  const documents = [...handoffDocuments, ...agreementDocuments].filter((doc) => !doc.availableFrom || doc.availableFrom <= handoff.businessDate!);
  requireHandoff(agreements.every((agreement) => documents.some((doc) => doc.documentId === agreement.sourceDocumentId))
    && obligations.every((obligation) => obligation.tenancyId === tenancy.tenancyId
      && (!obligation.basisAgreementId || agreements.some((agreement) => agreement.agreementId === obligation.basisAgreementId))
      && (!obligation.basisDocumentId || documents.some((doc) => doc.documentId === obligation.basisDocumentId))),
  "Some supporting agreements or documents are missing from this handoff.");
  const partyIds = [...new Set([words(tenancy.landlordPartyId, "Landlord reference", 160), ...(tenancy.tenantPartyIds ?? []),
    ...documents.flatMap((doc) => doc.partyId ? [doc.partyId] : []),
    ...obligations.flatMap((obligation) => [...(obligation.responsiblePartyIds ?? []), ...(obligation.beneficiaryPartyIds ?? [])])])];
  const parties = await bounded(client(HandoffParty).where({ partyId: { $in: partyIds }, workspaceId: { $eq: workspace.workspaceId } }), 32);
  parties.forEach((party) => inWorkspace(party, workspace, caller));
  requireHandoff(parties.length === partyIds.length, "Some parties are missing from this handoff.");
  const originalTitles = await checkDocumentSources(client, handoff, workspace, caller, documents);
  // Pointer-only attachments are available to the reader, not newly asserted facts for the coordinator.
  return { property, tenancy, documents: documents.filter((document) => !isFileAssociation(document)),
    supportingFiles: documents.filter(isFileAssociation), agreements, obligations, parties, originalTitles };
}

export function workContext(handoff: Handoff, workspace: Workspace, details: HandoffDetails): WorkContext {
  const providers = details.parties.filter((party) => details.documents.some((doc) => doc.kind === "Quote" && doc.partyId === party.partyId));
  requireHandoff(providers.length > 0, "Add a quote identifying the party offering the work before preparing a plan.");
  return validateWorkContext({
    title: handoff.title, goal: handoff.goal,
    property: `${details.property.name}. ${details.property.address}. ${details.property.description}`,
    tenancy: `${details.tenancy.title}. Starts ${details.tenancy.startDate}; ends ${details.tenancy.endDate}; notice received ${details.tenancy.noticeDate}. Business date ${handoff.businessDate}.`,
    agreements: details.agreements.map((agreement) => `${agreement.title}: ${agreement.termsText}`),
    obligations: details.obligations.map((obligation) => `${obligation.title}: ${obligation.description}. Status: ${obligation.status}.`),
    documents: details.documents.map((document) => ({ id: document.documentId, title: document.title,
      description: document.kind, kind: document.kind, body: document.text,
      ...(document.kind === "Quote" ? { providerPartyId: document.partyId } : {}) })),
    allowedProviderPartyIds: providers.map((party) => party.partyId),
    providers: providers.map((party) => ({ partyId: party.partyId, name: party.name, description: party.description })),
    currency: workspace.currency,
    // Obligations inform the recommendation; only conditions specified for the handoff are fixed.
    fixedRequirements: handoff.fixedRequirements ?? [],
  });
}
