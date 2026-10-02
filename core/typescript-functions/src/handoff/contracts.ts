import type { WorkSelection } from "./proposal.js";
import type { Finding, QuoteLine, ScopeLine } from "./deliveryContracts.js";
/** Application contracts. Money and revision values are canonical decimal strings. */
export interface HandoffList {
  version: "2";
  workspace: { id: string; name: string; mode: string };
  handoffs: Array<{ id: string; title: string; propertyName: string; physicalProgress: string;
    financialProgress: string; nextStep: string; revision: string }>;
}
export interface WorkPlanView {
  id: string; revision: string; title: string; status: string; summary: string;
  desiredOutcome: string; scope: string[]; estimatedCostCents: string; budgetCents: string;
  currency: string; fixedRequirements: string[]; rationale: string; sourceDocumentIds: string[];
  providerPartyId: string; acceptedDecisionId: string | null;
  selections: WorkSelection[]; fixedProviderPartyId: string | null;
}
export interface HandoffWorkspaceView {
  version: "2";
  workspace: { id: string; name: string; mode: string };
  handoff: { id: string; title: string; goal: string; businessDate: string; physicalProgress: string;
    financialProgress: string; nextStep: string; revision: string; operativeDecisionId: string | null };
  property: { id: string; name: string; address: string; description: string };
  tenancy: { id: string; title: string; startDate: string; endDate: string | null; endingKind: string };
  parties: Array<{ id: string; name: string; kind: string; description: string }>;
  agreements: Array<{ id: string; title: string; termsText: string; sourceDocumentId: string }>;
  obligations: Array<{ id: string; title: string; description: string; status: string }>;
  documents: Array<{ id: string; title: string; text: string; kind: string; sourceVersion: string;
    mimeType: string | null; availableFrom: string | null; mediaSetRid: string | null; mediaItemRid: string | null;
    pageStart: number | null; pageEnd: number | null;
    sourceKind?: "Original" | "Prepared"; sourceDocumentIds?: string[] }>;
  workPlan: WorkPlanView | null;
  decisions: Array<{ id: string; title: string; workPlanId: string; revision: string; by: string; at: string;
    budgetCents: string; currency: string; content: WorkPlanView }>;
  messages: Array<{ id: string; title: string; body: string; recipientPartyId: string | null; direction: string;
    status: string; createdAt: string; purpose: string; jobId: string | null; replyToMessageId: string | null;
    senderPartyId: string | null; attachmentDocumentIds: string[] }>;
  activity: Array<{ id: string; title: string; detail: string; at: string }>;
  agent: { status: string; nextStep: string; updatedAt: string; nextWakeAt: string | null };
  permissions: { canWork: boolean; canDecide: boolean; canConfigure: boolean };
  jobs: Array<{ id: string; title: string; kind: string; status: string; origin: string; providerPartyId: string;
    workPlanId: string | null; decisionId: string | null; quoteId: string | null; scope: ScopeLine[];
    committedCents: string | null; currency: string; appointmentAt: string | null; appointmentEndsAt: string | null;
    progressSummary: string; verificationInspectionId: string | null }>;
  quotes: Array<{ id: string; title: string; providerPartyId: string; kind: string; status: string;
    currency: string; lines: QuoteLine[]; totalCents: string; depositCents: string; paymentTerms: string;
    requirements: string[]; availableFrom: string; validUntil: string; sourceDocumentId: string }>;
  inspections: Array<{ id: string; title: string; jobId: string | null; observerPartyId: string;
    purpose: string; observedAt: string; findings: Finding[]; sourceDocumentId: string }>;
  invoices: Array<{ id: string; title: string; jobId: string; providerPartyId: string; payerPartyId: string;
    status: string; lines: QuoteLine[]; totalCents: string; currency: string; dueAt: string; sourceDocumentId: string }>;
  funding: Array<{ id: string; title: string; ownerPartyId: string; currency: string;
    confirmedCents: string; committedOrSpentCents: string; availableCents: string; sourceDocumentId: string }>;
  payments: Array<{ id: string; title: string; jobId: string; purpose: string; status: string;
    amountCents: string; currency: string; requestedAt: string; observedAt: string | null }>;
}
/** Checked edits and conversation both address the same proposal. Omitted fields remain unchanged. */
export interface WorkPlanChange {
  budgetCents?: string;
  selections?: WorkSelection[];
  fixedRequirements?: string[];
  fixedProviderPartyId?: string | null;
}
