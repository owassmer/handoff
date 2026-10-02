/**
 * Frozen Phase D wire contract. Pure JSON DTOs: numbers are exact safe integer
 * cents, NOT Foundry Long strings. Nullable fields are required on the wire.
 * V2 is a sidecar; it never replaces the native request or v1 review envelope.
 */
import type {
  AccountResult, AvailableAction, CaseParty, ItemDecision, Outcomes,
  ReviewMetadata, ReviewResult, SourceReference,
} from "../domain/types.js";

export const WORKFLOW_SCHEMA_VERSION = "2.0.0";
export const WORKFLOW_VERSION = "2";
export const WORKFLOW_MODE = "SIMULATED";
// Intentionally the existing Phase C scope, not a new environment/backend.
export const WORKFLOW_ENVIRONMENT_ID = "DC_PHASE_C_SYNTHETIC";
export const WORKFLOW_COMPANY_ID = "constructed-company-001";
export const MAX_WORKFLOW_JSON_BYTES = 256 * 1024; // exclusive bound, no truncation
export const MAX_WORKFLOW_RECORDS = 1024;
export const SYNTHETIC_STATEMENT_BADGE = "SYNTHETIC - NOT LEGAL PERFORMANCE";

export const OPERATION_KINDS = ["STATEMENT_DISPATCH", "REFUND", "CHARGE_POSTING",
  "DEPOSIT_APPLICATION", "CHARGE_POSTING_REVERSAL", "DEPOSIT_APPLICATION_REVERSAL"] as const;
export type OperationKind = typeof OPERATION_KINDS[number];
export type OperationsKind = OperationKind;
export type FinancialOperationKind = Exclude<OperationKind, "STATEMENT_DISPATCH">;
export const STATEMENT_KINDS = ["INTERIM", "FINAL", "CORRECTIVE"] as const;
export type StatementKind = typeof STATEMENT_KINDS[number];
export const REQUEST_STATES = ["READY", "CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN",
  "SUCCEEDED", "FAILED", "CANCELLED", "SUPERSEDED"] as const;
export type CurrentRequestState = typeof REQUEST_STATES[number];
export type ApprovalDecision = "APPROVED" | "REJECTED" | "REVOKED";
export type FactAcceptanceState = "UNCONFIRMED" | "ACCEPTED" | "DISPUTED" | "NOT_APPLICABLE";
export type SimulatedResultKind = "SUCCEEDED" | "FAILED" | "RETURNED";

export interface WorkflowScope {
  caseId: string;
  managementCompanyId: string;
  environmentId: typeof WORKFLOW_ENVIRONMENT_ID;
}

/** Trusted adapter inputs, never read from a public command payload. */
export interface PureContext {
  actorId: string;
  serverNow: string;
  isAdministrator: boolean;
  commandId: string;
  basisReviewId: string;
}

export interface OperationInstructionsInput {
  partyIds: string[];
  state: "VERIFIED" | "UNCONFIRMED";
  method: "DEMO_OUTBOX" | null;
  /** Opaque synthetic reference only; never an address, URL, or real route. */
  routeReference: string | null;
  evidenceIds: string[];
}
export interface OperationInstructions extends OperationInstructionsInput {
  versionId: string;
}

/** User selects an intent; the reducer derives versions/hashes from trusted state. */
export interface OperationIntentSpec {
  kind: OperationKind;
  amountCents: number | null;
  dispositionKey: string;
  statementId: string | null;
  replacesRequestId: string | null;
  reversesTransactionId: string | null;
}

export interface FinancialIntent {
  kind: FinancialOperationKind;
  amountCents: number;
  currency: "USD";
  dispositionKey: string;
  /** Display/basis link only: not financial materiality or economic identity. */
  statementId: string | null;
  recipientVersionId: string | null;
  materialityHash: string;
  targetVersionId: string;
  replacesRequestId: string | null;
  reversesTransactionId: string | null;
}
export interface StatementDispatchIntent {
  kind: "STATEMENT_DISPATCH";
  amountCents: null;
  currency: "USD";
  dispositionKey: string;
  statementId: string;
  recipientVersionId: string;
  materialityHash: string;
  contentHash: string;
  targetVersionId: string;
  replacesRequestId: string | null;
  reversesTransactionId: null;
}
export type OperationIntent = FinancialIntent | StatementDispatchIntent;

export interface StatementPartyLabel {
  partyId: string;
  displayLabel: string;
}
export interface StatementDate {
  factKey: string;
  state: FactAcceptanceState;
  value: string | null;
}
export interface StatementLine {
  itemId: string;
  location: string;
  description: string;
  decision: ItemDecision;
}
/** No invented addresses; only labels, accepted facts, and native core amounts. */
export interface StatementContent {
  mode: "SIMULATED";
  syntheticBadge: typeof SYNTHETIC_STATEMENT_BADGE;
  title: string;
  parties: StatementPartyLabel[];
  dates: StatementDate[];
  items: StatementLine[];
  account: AccountResult;
  sourceReferences: SourceReference[];
}
export interface StatementVersionRecord extends WorkflowScope {
  statementId: string;
  kind: StatementKind;
  createdCommandId: string;
  createdBy: string;
  createdAt: string;
  businessCreatedAt: string;
  sourceReviewId: string;
  materialityHash: string;
  contentHash: string;
  recipientVersionId: string;
  content: StatementContent;
  renderedText: string;
  supersedesStatementId: string | null;
}

/** Append-only decisions; validity and revocation effects are projections. */
export interface ApprovalRecord extends WorkflowScope {
  approvalId: string;
  createdCommandId: string;
  actorId: string;
  actorPartyId: string;
  authorityVersion: string;
  scope: OperationKind;
  intent: OperationIntent;
  decision: ApprovalDecision;
  decidedAt: string;
  revokesApprovalId: string | null;
}

/** One immutable economic operation. Mutable RequestFacts belong in projections. */
export interface RequestInstruction extends WorkflowScope {
  requestId: string;
  instructionKey: string;
  createdCommandId: string;
  kind: OperationKind;
  intent: OperationIntent;
  /** Frozen route snapshot for dispatch/refund; null for ledger operations. */
  instructions: OperationInstructions | null;
  instructionHash: string;
  approvalIds: string[];
  createdBy: string;
  createdAt: string;
  businessCreatedAt: string;
  replacesRequestId: string | null;
  reversesTransactionId: string | null;
}

export interface RawSimulatedResult {
  requestId: string;
  attemptId: string;
  sourceEventId: string;
  kind: SimulatedResultKind;
  operationKind: OperationKind;
  instructionHash: string;
  amountCents: number | null;
  currency: "USD";
  recipientVersionId: string | null;
  canonicalTransactionId: string | null;
  returnOfCanonicalTransactionId: string | null;
}
export interface WorkflowEventBase {
  eventId: string;
  sequence: number;
  caseId: string;
  commandId: string;
  requestId: string | null;
  attemptId: string | null;
  sourceEventId: string | null;
  occurredAt: string;
  learnedAt: string;
  recordedAt: string;
  recordedBy: string;
  mode: "SIMULATED";
}
export interface InstructionEventPayload { instructionHash: string }
export interface ReasonEventPayload { reason: string }
export interface SupersededEventPayload extends ReasonEventPayload { replacementRequestId: string | null }
export interface AcceptedResultPayload {
  rawEventId: string;
  instructionHash: string;
  canonicalTransactionId: string | null;
  returnOfCanonicalTransactionId: string | null;
}
export type WorkflowEvent = WorkflowEventBase & (
  | { category: "REQUEST_LIFECYCLE"; kind: "REQUEST_CREATED" | "ATTEMPT_CLAIMED" | "REQUESTED" | "ACKNOWLEDGED"; payload: InstructionEventPayload }
  | { category: "REQUEST_LIFECYCLE"; kind: "OUTCOME_UNKNOWN" | "CANCELLED_BEFORE_ATTEMPT"; payload: ReasonEventPayload }
  | { category: "REQUEST_LIFECYCLE"; kind: "SUPERSEDED_BEFORE_ATTEMPT"; payload: SupersededEventPayload }
  | { category: "SIMULATED_RESULT"; kind: "RAW_SIMULATED_RESULT"; payload: RawSimulatedResult }
  | { category: "SIMULATED_RESULT"; kind: "RESULT_ACCEPTED"; payload: AcceptedResultPayload }
);
export type WorkflowEventKind = WorkflowEvent["kind"];

export interface WorkflowStateV2 extends WorkflowScope {
  schemaVersion: "2.0.0";
  mode: "SIMULATED";
  initializedBy: string;
  initializedAt: string;
  businessClock: string;
  statementInstructions: OperationInstructions;
  refundInstructions: OperationInstructions;
  statements: StatementVersionRecord[];
  approvals: ApprovalRecord[];
  requests: RequestInstruction[];
  events: WorkflowEvent[];
  currentStatementId: string | null;
}

/** Derived only. Never append competing mutable states for the same request. */
export interface CurrentRequest {
  requestId: string;
  kind: OperationKind;
  state: CurrentRequestState;
  amountCents: number | null;
  reservedAmountCents: number;
  attemptId: string | null;
  lastEventId: string | null;
  canonicalTransactionId: string | null;
  reconciliationRequired: boolean;
  reason: string;
}
export type ProposedCurrentRequest = CurrentRequest;
export interface ApprovalValidity { approvalId: string; valid: boolean; reason: string }
export interface StatementStatus {
  statementId: string;
  isCurrent: boolean;
  dispatchRequestIds: string[];
  issued: boolean;
}
export interface FinancialCommitment {
  kind: FinancialOperationKind;
  reservedCents: number;
  requestIds: string[];
}
export interface WorkflowAccount extends AccountResult {
  financialCommitments: FinancialCommitment[];
  /** Null when the account is unverified. Do not deduct reserves from finalRefundCents twice. */
  newlyRequestableRefundCents: number | null;
}
export interface WorkflowActionDetails {
  operationKind: OperationKind;
  intent: OperationIntent | null;
  approvalDetails: ApprovalValidity[];
  requestDetails: CurrentRequest[];
  statementDetails: StatementStatus[];
}
export interface WorkflowAction extends AvailableAction { workflow: WorkflowActionDetails | null }
export interface WorkflowOutcomes extends Outcomes {
  depositComplete: false;
  overallCaseComplete: false;
  simulatedDepositWorkflowComplete: boolean;
  simulatedOverallWorkflowComplete: boolean;
  completionMode: "SIMULATED";
  legalPerformanceConfirmed: false;
}
export interface WorkflowReviewMetadata extends ReviewMetadata {
  workflowSchemaVersion: "2.0.0";
  workflowStateHash: string;
  /** Recompute persisted equality at the snapshot's createdAt, not today's time. */
  authorityEvaluatedAt: string;
}
export interface WorkflowReviewResult extends ReviewResult {
  account: WorkflowAccount;
  actions: WorkflowAction[];
  outcomes: WorkflowOutcomes;
}
export interface WorkflowReviewV2 { metadata: WorkflowReviewMetadata; result: WorkflowReviewResult }
export interface WorkflowSnapshotExtras {
  workflowStateJson?: string;
  workflowStateHash?: string;
  workflowReviewJson?: string;
  workflowReviewHash?: string;
}
export interface ParsedWorkflowSnapshot { state: WorkflowStateV2; review: WorkflowReviewV2 }

export const LIFECYCLE_COMMAND_KINDS = ["INIT_WORKFLOW", "ACCEPT_SCOPE_FACTS", "SET_INTERIM_QUALIFICATION",
  "UPSERT_RECIPIENT_PARTY", "SET_STATEMENT_INSTRUCTIONS", "SET_REFUND_INSTRUCTIONS", "PREPARE_STATEMENT",
  "DECIDE_APPROVAL", "REVOKE_APPROVAL", "REQUEST_OPERATION", "CLAIM_REQUEST", "RECORD_OUTCOME_UNKNOWN",
  "GENERATE_SIMULATED_RESULT", "INGEST_RESULT", "CANCEL_UNATTEMPTED_REQUEST"] as const;
export type LifecycleCommandKind = typeof LIFECYCLE_COMMAND_KINDS[number];
export interface AcceptScopeFactsPayload {
  jurisdiction: string;
  tenancyRegime: string;
  tenancyEndsInFull: boolean | null;
  cashSecurityDeposit: boolean | null;
  evidenceIds: string[];
  reason: string;
}
export interface InterimQualificationPayload {
  state: FactAcceptanceState;
  evidenceIds: string[];
  reason: string;
}
export interface PrepareStatementPayload { kind: StatementKind; supersedesId: string | null; reason: string }
export interface DecideApprovalPayload { intent: OperationIntentSpec; decision: "APPROVED" | "REJECTED" }
export interface GenerateSimulatedResultPayload {
  requestId: string;
  attemptId: string;
  sourceEventId: string;
  outcome: SimulatedResultKind;
  amountCents: number | null;
  /** Required nullable. Null explicitly means the current business clock. */
  occurredAt: string | null;
}
export interface LifecycleCommandPayloads {
  INIT_WORKFLOW: Record<string, never>;
  ACCEPT_SCOPE_FACTS: AcceptScopeFactsPayload;
  SET_INTERIM_QUALIFICATION: InterimQualificationPayload;
  UPSERT_RECIPIENT_PARTY: { party: CaseParty };
  SET_STATEMENT_INSTRUCTIONS: OperationInstructionsInput;
  SET_REFUND_INSTRUCTIONS: OperationInstructionsInput;
  PREPARE_STATEMENT: PrepareStatementPayload;
  DECIDE_APPROVAL: DecideApprovalPayload;
  REVOKE_APPROVAL: { approvalId: string; reason: string };
  REQUEST_OPERATION: { approvalId: string };
  CLAIM_REQUEST: { requestId: string };
  RECORD_OUTCOME_UNKNOWN: { requestId: string; attemptId: string; reason: string };
  GENERATE_SIMULATED_RESULT: GenerateSimulatedResultPayload;
  INGEST_RESULT: { sourceEventId: string };
  CANCEL_UNATTEMPTED_REQUEST: { requestId: string; reason: string };
}
export type LifecycleCommand = {
  [K in LifecycleCommandKind]: { kind: K; payload: LifecycleCommandPayloads[K] }
}[LifecycleCommandKind];
