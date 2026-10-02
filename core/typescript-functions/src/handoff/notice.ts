import { dateOnly, details, entries, parseDetails, requireHandoff, wordList, words } from "./values.js";

export interface MoveOutNotice {
  sourceSystem: string; sourceRecordId: string; title: string; goal: string; businessDate: string;
  fixedRequirements?: string[];
  property: { sourceId: string; name: string; address: string; description: string };
  parties: Array<{ sourceId: string; name: string; kind: string; email?: string; phone?: string; description: string }>;
  tenancy: {
    sourceId: string; title: string; landlordPartySourceId: string; tenantPartySourceIds: string[];
    startDate: string; endDate?: string; noticeDate: string; endingKind?: "Tenancy ending" | "Occupant departure" | "To confirm";
  };
  documents: Array<{
    sourceId: string; title: string; text: string; kind: string; partySourceId?: string; sourceKind: string;
    mediaSetRid?: string; mediaItemRid?: string; pageStart?: number; pageEnd?: number;
    sourceVersion?: string; detailsJson?: string; availableFrom?: string; mimeType?: string;
  }>;
  agreements: Array<{
    sourceId: string; title: string; kind: string; termsText: string; sourceDocumentSourceId: string; effectiveFrom: string;
  }>;
  obligations: Array<{
    sourceId: string; title: string; description: string; responsiblePartySourceIds: string[];
    beneficiaryPartySourceIds: string[]; basisAgreementSourceId?: string; basisDocumentSourceId?: string;
    dueDate?: string; status: string;
  }>;
}

function optionalText(value: unknown, label: string, max = 160): string | undefined {
  return value === undefined ? undefined : words(value, label, max);
}
function page(value: unknown): number | undefined {
  if (value === undefined) return undefined;
  requireHandoff(typeof value === "number" && Number.isInteger(value) && value >= 1 && value <= 100000,
    "Source pages must be positive whole numbers.");
  return value;
}
function unique(records: { sourceId: string }[], label: string): Set<string> {
  const ids = new Set(records.map((entry) => entry.sourceId));
  requireHandoff(ids.size === records.length, `${label} must have different source references.`);
  return ids;
}

/** A notice creates named business facts, never a caller-selected field patch. */
export function readMoveOutNotice(noticeJson: string): MoveOutNotice {
  const input = details(parseDetails(noticeJson, "Move-out notice"),
    ["sourceSystem", "sourceRecordId", "title", "goal", "businessDate", "property", "parties", "tenancy"], ["fixedRequirements", "documents", "agreements", "obligations"], "Move-out notice");
  const property = details(input.property, ["sourceId", "name", "address", "description"], [], "Property");
  const tenancy = details(input.tenancy, ["sourceId", "title", "landlordPartySourceId", "tenantPartySourceIds", "startDate", "noticeDate"], ["endDate", "endingKind"], "Tenancy");
  const result: MoveOutNotice = {
    sourceSystem: words(input.sourceSystem, "Source name", 160),
    sourceRecordId: words(input.sourceRecordId, "Notice reference", 160),
    title: words(input.title, "Handoff title", 200), goal: words(input.goal, "Handoff goal"),
    businessDate: dateOnly(input.businessDate, "Business date"),
    fixedRequirements: input.fixedRequirements === undefined ? [] : wordList(input.fixedRequirements, "Requirements", 24, 0, 1000),
    property: { sourceId: words(property.sourceId, "Property reference", 160), name: words(property.name, "Property name", 200),
      address: words(property.address, "Property address", 500), description: words(property.description, "Property description", 2000) },
    parties: entries(input.parties, "Parties", 32, 2).map((entry) => {
      const party = details(entry, ["sourceId", "name", "kind", "description"], ["email", "phone"], "Party");
      const email = optionalText(party.email, "Email address", 320);
      requireHandoff(email === undefined || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email), "Check the email address.");
      return { sourceId: words(party.sourceId, "Party reference", 160), name: words(party.name, "Party name", 200),
        kind: words(party.kind, "Party kind", 100), description: words(party.description, "Party description", 2000),
        email, phone: optionalText(party.phone, "Phone number", 80) };
    }),
    tenancy: { sourceId: words(tenancy.sourceId, "Tenancy reference", 160), title: words(tenancy.title, "Tenancy title", 200),
      landlordPartySourceId: words(tenancy.landlordPartySourceId, "Landlord reference", 160),
      tenantPartySourceIds: wordList(tenancy.tenantPartySourceIds, "Tenants", 16, 1),
      startDate: dateOnly(tenancy.startDate, "Tenancy start date"), endDate: tenancy.endDate === undefined ? undefined : dateOnly(tenancy.endDate, "Tenancy end date"),
      endingKind: tenancy.endingKind === undefined ? (tenancy.endDate ? "Tenancy ending" : "To confirm") : words(tenancy.endingKind, "Notice meaning", 100) as MoveOutNotice["tenancy"]["endingKind"],
      noticeDate: dateOnly(tenancy.noticeDate, "Notice date") },
    documents: entries(input.documents ?? [], "Documents", 80, 0).map((entry) => {
      const doc = details(entry, ["sourceId", "title", "text", "kind", "sourceKind"],
        ["partySourceId", "mediaSetRid", "mediaItemRid", "pageStart", "pageEnd", "sourceVersion", "detailsJson", "availableFrom", "mimeType"], "Document");
      const sourceKind = words(doc.sourceKind, "Document origin", 100);
      requireHandoff(["Source", "Prepared"].includes(sourceKind), "Document origin must be Source or Prepared.");
      const mediaSetRid = optionalText(doc.mediaSetRid, "Source collection reference", 200);
      const mediaItemRid = optionalText(doc.mediaItemRid, "Source file reference", 200);
      requireHandoff((mediaSetRid === undefined) === (mediaItemRid === undefined), "Provide both source file references together.");
      const pageStart = page(doc.pageStart), pageEnd = page(doc.pageEnd);
      requireHandoff((pageStart === undefined) === (pageEnd === undefined)
        && (pageStart === undefined || (mediaSetRid !== undefined && pageEnd! >= pageStart)),
      "Provide an ordered source page range with its source file.");
      const kind = words(doc.kind, "Document kind", 100);
      const partySourceId = optionalText(doc.partySourceId, "Document provider reference");
      requireHandoff(kind !== "Quote" || partySourceId !== undefined, "A quote needs the party offering the work.");
      return { sourceId: words(doc.sourceId, "Document reference", 160), title: words(doc.title, "Document title", 200),
        text: words(doc.text, "Document text", 24000), kind, partySourceId, sourceKind, mediaSetRid, mediaItemRid, pageStart, pageEnd,
        sourceVersion: optionalText(doc.sourceVersion, "Source version", 160), detailsJson: optionalText(doc.detailsJson, "Supporting details", 100000),
        availableFrom: doc.availableFrom === undefined ? undefined : dateOnly(doc.availableFrom, "Available from"), mimeType: optionalText(doc.mimeType, "File type", 200) };
    }),
    agreements: entries(input.agreements ?? [], "Agreements", 16).map((entry) => {
      const agreement = details(entry, ["sourceId", "title", "kind", "termsText", "sourceDocumentSourceId", "effectiveFrom"], [], "Agreement");
      return { sourceId: words(agreement.sourceId, "Agreement reference", 160), title: words(agreement.title, "Agreement title", 200),
        kind: words(agreement.kind, "Agreement kind", 100), termsText: words(agreement.termsText, "Agreement terms"),
        sourceDocumentSourceId: words(agreement.sourceDocumentSourceId, "Agreement document reference", 160),
        effectiveFrom: dateOnly(agreement.effectiveFrom, "Agreement start date") };
    }),
    obligations: entries(input.obligations ?? [], "Obligations", 24).map((entry) => {
      const obligation = details(entry, ["sourceId", "title", "description", "responsiblePartySourceIds", "beneficiaryPartySourceIds", "status"],
        ["basisAgreementSourceId", "basisDocumentSourceId", "dueDate"], "Obligation");
      return { sourceId: words(obligation.sourceId, "Obligation reference", 160), title: words(obligation.title, "Obligation title", 200),
        description: words(obligation.description, "Obligation description", 1000),
        responsiblePartySourceIds: wordList(obligation.responsiblePartySourceIds, "Responsible parties", 16, 1),
        beneficiaryPartySourceIds: wordList(obligation.beneficiaryPartySourceIds, "Benefiting parties", 16, 1),
        basisAgreementSourceId: optionalText(obligation.basisAgreementSourceId, "Supporting agreement reference"),
        basisDocumentSourceId: optionalText(obligation.basisDocumentSourceId, "Supporting document reference"),
        dueDate: obligation.dueDate === undefined ? undefined : dateOnly(obligation.dueDate, "Due date"),
        status: words(obligation.status, "Obligation status", 100) };
    }),
  };
  requireHandoff(["Tenancy ending", "Occupant departure", "To confirm"].includes(result.tenancy.endingKind!), "Identify whether this notice ends the tenancy or concerns an occupant.");
  requireHandoff(result.tenancy.endingKind === "Tenancy ending" || !result.tenancy.endDate, "Do not record a tenancy end date for an unconfirmed ending or an occupant departure.");
  requireHandoff(!result.tenancy.endDate || result.tenancy.endDate >= result.tenancy.startDate, "The tenancy end date must follow its start date.");
  requireHandoff(result.tenancy.noticeDate <= result.businessDate, "The notice date cannot follow the business date.");
  requireHandoff(result.documents.reduce((sum, doc) => sum + doc.text.length, 0) <= 180000,
    "Choose a smaller set of relevant documents.");
  const parties = unique(result.parties, "Parties"), documents = unique(result.documents, "Documents");
  const agreements = unique(result.agreements, "Agreements");
  unique(result.obligations, "Obligations");
  requireHandoff(parties.has(result.tenancy.landlordPartySourceId)
    && result.tenancy.tenantPartySourceIds.every((id) => parties.has(id))
    && result.documents.every((doc) => doc.partySourceId === undefined || parties.has(doc.partySourceId))
    && result.agreements.every((agreement) => documents.has(agreement.sourceDocumentSourceId))
    && result.obligations.every((obligation) => [...obligation.responsiblePartySourceIds, ...obligation.beneficiaryPartySourceIds].every((id) => parties.has(id))
      && (obligation.basisAgreementSourceId === undefined || agreements.has(obligation.basisAgreementSourceId))
      && (obligation.basisDocumentSourceId === undefined || documents.has(obligation.basisDocumentSourceId))),
  "Every referenced party, document and agreement must be included in the notice.");
  return result;
}
