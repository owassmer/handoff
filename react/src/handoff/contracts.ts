/** Narrow public read contracts. Money and revisions remain lossless decimal strings. */
export interface WorkspaceIdentity {
  id: string;
  name: string;
  mode: string;
}
export interface HandoffSummary {
  id: string;
  title: string;
  propertyName: string;
  physicalProgress: string;
  financialProgress: string;
  nextStep: string;
  revision: string;
}
export interface HandoffList {
  version: "2";
  workspace: WorkspaceIdentity;
  handoffs: HandoffSummary[];
}
export interface SourceDocument {
  id: string;
  title: string;
  text: string;
  kind: string;
  sourceVersion: string;
  sourceKind?: "Original" | "Prepared";
  sourceDocumentIds?: string[];
  mimeType: string | null;
  availableFrom: string | null;
  mediaSetRid: string | null;
  mediaItemRid: string | null;
  pageStart: number | null;
  pageEnd: number | null;
  /** Optional original-file integrity value, when supplied by intake. */
  sha256?: string;
}
export interface WorkSelection {
  quoteId: string;
  quoteLineId: string;
  scope: string;
  reason: string;
}
export interface WorkPlanChange {
  budgetCents?: string;
  selections?: WorkSelection[];
  fixedRequirements?: string[];
  fixedProviderPartyId?: string | null;
}
export interface WorkPlan {
  id: string;
  revision: string;
  title: string;
  status: string;
  summary: string;
  desiredOutcome: string;
  scope: string[];
  estimatedCostCents: string;
  budgetCents: string;
  currency: string;
  fixedRequirements: string[];
  rationale: string;
  sourceDocumentIds: string[];
  providerPartyId: string;
  acceptedDecisionId: string | null;
  selections: WorkSelection[];
  fixedProviderPartyId: string | null;
}
export interface Decision {
  id: string;
  title: string;
  workPlanId: string;
  revision: string;
  by: string;
  at: string;
  budgetCents: string;
  currency: string;
  content: WorkPlan;
}
export interface QuoteLine {
  lineId: string;
  description: string;
  amountCents: string;
}
export interface ScopeLine extends QuoteLine {
  acceptedScope: string;
}
export interface Finding {
  lineId: string;
  result: "Satisfied" | "Deficient" | "Not checked";
  observation: string;
  method: string;
}
export interface HandoffWorkspace {
  version: "2";
  workspace: WorkspaceIdentity;
  handoff: {
    id: string;
    title: string;
    goal: string;
    businessDate: string;
    physicalProgress: string;
    financialProgress: string;
    nextStep: string;
    revision: string;
    operativeDecisionId: string | null;
  };
  property: { id: string; name: string; address: string; description: string };
  tenancy: {
    id: string;
    title: string;
    startDate: string;
    endDate: string | null;
    endingKind: string;
  };
  parties: { id: string; name: string; kind: string; description: string }[];
  agreements: { id: string; title: string; termsText: string; sourceDocumentId: string }[];
  obligations: { id: string; title: string; description: string; status: string }[];
  documents: SourceDocument[];
  workPlan: WorkPlan | null;
  decisions: Decision[];
  messages: {
    id: string;
    title: string;
    body: string;
    recipientPartyId: string | null;
    direction: string;
    status: string;
    createdAt: string;
    purpose: string;
    jobId: string | null;
    replyToMessageId: string | null;
    /** Newer backends: who sent an incoming message, and the documents attached to it. */
    senderPartyId?: string | null;
    attachmentDocumentIds?: string[];
  }[];
  activity: { id: string; title: string; detail: string; at: string }[];
  agent: { status: string; nextStep: string; updatedAt: string; nextWakeAt: string | null };
  permissions: { canWork: boolean; canDecide: boolean; canConfigure: boolean };
  jobs: {
    id: string;
    title: string;
    kind: string;
    status: string;
    origin: string;
    providerPartyId: string;
    workPlanId: string | null;
    decisionId: string | null;
    quoteId: string | null;
    scope: ScopeLine[];
    committedCents: string | null;
    currency: string;
    appointmentAt: string | null;
    appointmentEndsAt: string | null;
    progressSummary: string;
    verificationInspectionId: string | null;
  }[];
  quotes: {
    id: string;
    title: string;
    providerPartyId: string;
    kind: string;
    status: string;
    currency: string;
    lines: QuoteLine[];
    totalCents: string;
    depositCents: string;
    paymentTerms: string;
    requirements: string[];
    availableFrom: string;
    validUntil: string;
    sourceDocumentId: string;
  }[];
  inspections: {
    id: string;
    title: string;
    jobId: string | null;
    observerPartyId: string;
    purpose: string;
    observedAt: string;
    findings: Finding[];
    sourceDocumentId: string;
  }[];
  invoices: {
    id: string;
    title: string;
    jobId: string;
    providerPartyId: string;
    payerPartyId: string;
    status: string;
    lines: QuoteLine[];
    totalCents: string;
    currency: string;
    dueAt: string;
    sourceDocumentId: string;
  }[];
  funding: {
    id: string;
    title: string;
    ownerPartyId: string;
    currency: string;
    confirmedCents: string;
    committedOrSpentCents: string;
    availableCents: string;
    sourceDocumentId: string;
  }[];
  payments: {
    id: string;
    title: string;
    jobId: string;
    purpose: string;
    status: string;
    amountCents: string;
    currency: string;
    requestedAt: string;
    observedAt: string | null;
  }[];
}
export type PlanCommand = Readonly<{
  kind: "budget" | "accept";
  handoffId: string;
  workPlanId: string;
  expectedRevision: string;
  budgetCents: string;
  commandId: string;
}>;
export type ProposalCommand = Readonly<{
  kind: "plan";
  handoffId: string;
  workPlanId: string;
  expectedRevision: string;
  budgetCents: string;
  changes: WorkPlanChange;
  commandId: string;
}>;
export type MessageCommand = Readonly<{
  kind: "message";
  handoffId: string;
  message: string;
  expectedPlanRevision?: string;
  commandId: string;
}>;
export type Change = PlanCommand | ProposalCommand | MessageCommand;
export interface HandoffChange {
  version: "2";
  commandId: string;
  status: "Saved" | "Not found";
  subjectId: string | null;
  kind: string | null;
  payloadHash: string | null;
  resultRevision: string | null;
  at: string | null;
}
export type ApplyResult = "saved" | "rejected";
/** One Resume handoff call: it ran, or the server refused it (e.g. an automation ran the same step first). */
export type StepResult = { kind: "done" } | { kind: "refused"; message: string };
export interface HandoffGateway {
  /** Admin case controls only; the operator surface never calls it. */
  resume?(handoffId: string): Promise<StepResult>;
  list(): Promise<HandoffList>;
  workspace(handoffId: string): Promise<HandoffWorkspace>;
  receipt(handoffId: string, commandId: string): Promise<HandoffChange>;
  apply(change: Change): Promise<ApplyResult>;
  document(document: SourceDocument): Promise<Blob>;
  clearDocuments?(): void;
  onDocumentInvalidated?(document: SourceDocument, invalidate: () => void): () => void;
}
export class HandoffError extends Error {
  constructor(
    public readonly kind: "unavailable" | "access" | "permission" | "read" | "document" = "read",
  ) {
    super(
      kind === "unavailable"
        ? "Handoff can't connect right now. Please try again."
        : kind === "permission"
          ? "Handoff needs access. Ask your team for help."
          : kind === "access"
            ? "Please sign in to continue."
            : "We couldn't load this handoff. Please try again.",
    );
  }
}

type Check = (value: unknown) => boolean;
const record = (v: unknown): v is Record<string, unknown> =>
  typeof v === "object" && v !== null && !Array.isArray(v);
const text: Check = (v) => typeof v === "string";
const numberString: Check = (v) =>
  typeof v === "string" && /^(0|[1-9]\d*)$/.test(v) && v.length <= 19;
const money: Check = (v) => numberString(v) && BigInt(v as string) <= 9223372036854775807n;
const currency: Check = (v) => typeof v === "string" && /^[A-Z]{3}$/.test(v);
const nullable =
  (check: Check): Check =>
  (v) =>
    v === null || check(v);
const array =
  (check: Check): Check =>
  (v) =>
    Array.isArray(v) && v.length <= 100 && v.every(check);
const shape =
  (checks: Record<string, Check>): Check =>
  (v) =>
    record(v) && Object.entries(checks).every(([k, check]) => check(v[k]));
const fields = (...names: string[]): Record<string, Check> =>
  Object.fromEntries(names.map((name) => [name, text]));
const identity = shape(fields("id", "name", "mode"));
const page = nullable((v) => typeof v === "number" && Number.isInteger(v) && v >= 1);
const documentCheck = shape({
  ...fields("id", "title", "text", "kind", "sourceVersion"),
  sourceKind: (v) => v === undefined || v === "Original" || v === "Prepared",
  sourceDocumentIds: (v) =>
    v === undefined ||
    (Array.isArray(v) &&
      v.length <= 32 &&
      v.every((id) => typeof id === "string" && Boolean(id.trim())) &&
      new Set(v).size === v.length),
  mimeType: nullable(text),
  availableFrom: nullable(text),
  mediaSetRid: nullable(text),
  mediaItemRid: nullable(text),
  pageStart: page,
  pageEnd: page,
  sha256: (v) => v === undefined || (typeof v === "string" && /^[a-f0-9]{64}$/.test(v)),
});
const selectionCheck = shape(fields("quoteId", "quoteLineId", "scope", "reason"));
const planCheck = shape({
  ...fields("id", "title", "status", "summary", "desiredOutcome", "rationale", "providerPartyId"),
  revision: numberString,
  scope: array(text),
  estimatedCostCents: money,
  budgetCents: money,
  currency,
  fixedRequirements: array(text),
  sourceDocumentIds: array(text),
  acceptedDecisionId: nullable(text),
  selections: array(selectionCheck),
  fixedProviderPartyId: nullable(text),
});
const lineCheck = shape({ ...fields("lineId", "description"), amountCents: money });
const commonSummary = {
  ...fields("id", "title", "physicalProgress", "financialProgress", "nextStep"),
  revision: numberString,
};
const listCheck = shape({
  version: (v) => v === "2",
  workspace: identity,
  handoffs: array(shape({ ...commonSummary, propertyName: text })),
});
const workspaceCheck = shape({
  version: (v) => v === "2",
  workspace: identity,
  handoff: shape({
    ...commonSummary,
    goal: text,
    businessDate: text,
    operativeDecisionId: nullable(text),
  }),
  property: shape(fields("id", "name", "address", "description")),
  tenancy: shape({
    ...fields("id", "title", "startDate"),
    endDate: nullable(text),
    endingKind: (v) => ["Tenancy ending", "Occupant departure", "To confirm"].includes(String(v)),
  }),
  parties: array(shape(fields("id", "name", "kind", "description"))),
  agreements: array(shape(fields("id", "title", "termsText", "sourceDocumentId"))),
  obligations: array(shape(fields("id", "title", "description", "status"))),
  documents: array(documentCheck),
  workPlan: nullable(planCheck),
  decisions: array(
    shape({
      ...fields("id", "title", "workPlanId", "by", "at"),
      currency,
      revision: numberString,
      budgetCents: money,
      content: planCheck,
    }),
  ),
  messages: array(
    shape({
      ...fields("id", "title", "body", "direction", "status", "createdAt", "purpose"),
      recipientPartyId: nullable(text),
      jobId: nullable(text),
      replyToMessageId: nullable(text),
      senderPartyId: (v) => v === undefined || v === null || text(v),
      attachmentDocumentIds: (v) =>
        v === undefined || (Array.isArray(v) && v.length <= 20 && v.every((item) => text(item))),
    }),
  ),
  activity: array(shape(fields("id", "title", "detail", "at"))),
  agent: shape({ ...fields("status", "nextStep", "updatedAt"), nextWakeAt: nullable(text) }),
  permissions: shape({
    canWork: (v) => typeof v === "boolean",
    canDecide: (v) => typeof v === "boolean",
    canConfigure: (v) => typeof v === "boolean",
  }),
  jobs: array(
    shape({
      ...fields("id", "title", "kind", "status", "origin", "providerPartyId", "progressSummary"),
      currency,
      workPlanId: nullable(text),
      decisionId: nullable(text),
      quoteId: nullable(text),
      scope: array((v) => lineCheck(v) && record(v) && text(v.acceptedScope)),
      committedCents: nullable(money),
      appointmentAt: nullable(text),
      appointmentEndsAt: nullable(text),
      verificationInspectionId: nullable(text),
    }),
  ),
  quotes: array(
    shape({
      ...fields(
        "id",
        "title",
        "providerPartyId",
        "kind",
        "status",
        "paymentTerms",
        "availableFrom",
        "validUntil",
        "sourceDocumentId",
      ),
      currency,
      lines: array(lineCheck),
      totalCents: money,
      depositCents: money,
      requirements: array(text),
    }),
  ),
  inspections: array(
    shape({
      ...fields("id", "title", "observerPartyId", "purpose", "observedAt", "sourceDocumentId"),
      jobId: nullable(text),
      findings: array(
        shape({
          ...fields("lineId", "observation", "method"),
          result: (v) => ["Satisfied", "Deficient", "Not checked"].includes(String(v)),
        }),
      ),
    }),
  ),
  invoices: array(
    shape({
      ...fields(
        "id",
        "title",
        "jobId",
        "providerPartyId",
        "payerPartyId",
        "status",
        "dueAt",
        "sourceDocumentId",
      ),
      currency,
      lines: array(lineCheck),
      totalCents: money,
    }),
  ),
  funding: array(
    shape({
      ...fields("id", "title", "ownerPartyId", "sourceDocumentId"),
      currency,
      confirmedCents: money,
      committedOrSpentCents: money,
      availableCents: money,
    }),
  ),
  payments: array(
    shape({
      ...fields("id", "title", "jobId", "purpose", "status", "requestedAt"),
      currency,
      amountCents: money,
      observedAt: nullable(text),
    }),
  ),
});
function readJson<T>(value: unknown, check: Check): T {
  try {
    if (typeof value !== "string") {
      throw new HandoffError();
    }
    const parsed: unknown = JSON.parse(value);
    if (!check(parsed)) {
      throw new HandoffError();
    }
    return parsed as T;
  } catch {
    throw new HandoffError();
  }
}
export const receiptKinds = {
  budget: "Work budget changed",
  plan: "Work plan changed",
  accept: "Work plan accepted",
  message: "Message sent",
} as const;
export function readChange(value: unknown, commandId: string): HandoffChange {
  const result = readJson<HandoffChange>(
    value,
    shape({
      version: (v) => v === "2",
      commandId: (v) => v === commandId,
      status: (v) => v === "Saved" || v === "Not found",
      subjectId: nullable(text),
      kind: nullable(text),
      payloadHash: nullable(text),
      resultRevision: nullable(numberString),
      at: nullable(text),
    }),
  );
  const details = [
    result.subjectId,
    result.kind,
    result.payloadHash,
    result.resultRevision,
    result.at,
  ];
  if (
    result.status === "Not found"
      ? details.some((v) => v !== null)
      : details.some((v) => !v) ||
        ![...Object.values(receiptKinds), "Document received"].includes(result.kind!) ||
        !/^[a-f0-9]{64}$/.test(result.payloadHash!) ||
        Number.isNaN(Date.parse(result.at!))
  ) {
    throw new HandoffError();
  }
  return result;
}
export function readList(value: unknown, workspaceId: string): HandoffList {
  const result = readJson<HandoffList>(value, listCheck);
  if (
    result.workspace.id !== workspaceId ||
    new Set(result.handoffs.map((h) => h.id)).size !== result.handoffs.length
  ) {
    throw new HandoffError();
  }
  return result;
}
export function readWorkspace(
  value: unknown,
  workspaceId: string,
  handoffId: string,
): HandoffWorkspace {
  const result = readJson<HandoffWorkspace>(value, workspaceCheck);
  if (result.workspace.id !== workspaceId || result.handoff.id !== handoffId) {
    throw new HandoffError();
  }
  for (const rows of [
    result.documents,
    result.parties,
    result.decisions,
    result.messages,
    result.activity,
    result.jobs,
    result.quotes,
    result.inspections,
    result.invoices,
    result.funding,
    result.payments,
  ]) {
    if (new Set(rows.map((r) => r.id)).size !== rows.length) {
      throw new HandoffError();
    }
  }
  if (result.tenancy.endingKind !== "Tenancy ending" && result.tenancy.endDate !== null) {
    throw new HandoffError();
  }
  for (const doc of result.documents) {
    if (
      (doc.mediaSetRid === null) !== (doc.mediaItemRid === null) ||
      (doc.pageEnd !== null && (doc.pageStart === null || doc.pageEnd < doc.pageStart)) ||
      (doc.sourceKind === "Prepared" && doc.mediaSetRid !== null) ||
      (doc.sourceKind === "Original" &&
        (!doc.mediaSetRid ||
          !doc.mediaItemRid ||
          !doc.mimeType ||
          Boolean(doc.sourceDocumentIds?.length))) ||
      (Boolean(doc.sourceDocumentIds?.length) && doc.sourceKind !== "Prepared") ||
      doc.sourceDocumentIds?.some(
        (id) =>
          id === doc.id ||
          !result.documents.some(
            (source) =>
              source.id === id &&
              source.sourceKind === "Original" &&
              source.mediaSetRid &&
              source.mediaItemRid,
          ),
      )
    ) {
      throw new HandoffError();
    }
  }
  for (const decision of result.decisions) {
    const content = decision.content;
    if (
      content.id !== decision.workPlanId ||
      content.revision !== decision.revision ||
      content.acceptedDecisionId !== decision.id ||
      content.status !== "Accepted" ||
      content.budgetCents !== decision.budgetCents ||
      content.currency !== decision.currency
    ) {
      throw new HandoffError();
    }
  }
  for (const id of [result.handoff.operativeDecisionId, result.workPlan?.acceptedDecisionId]) {
    if (id && !result.decisions.some((d) => d.id === id)) {
      throw new HandoffError();
    }
  }
  if (result.workPlan?.acceptedDecisionId) {
    const accepted = result.decisions.find(
      (d) => d.id === result.workPlan!.acceptedDecisionId,
    )!.content;
    if (
      Object.keys(accepted).some(
        (key) =>
          JSON.stringify(Reflect.get(accepted, key)) !==
          JSON.stringify(Reflect.get(result.workPlan!, key)),
      )
    ) {
      throw new HandoffError();
    }
  }
  return result;
}
/** Any source change closes an already-open original, including changed text/access context. */
export function documentKey(document: SourceDocument): string {
  return JSON.stringify(document);
}
