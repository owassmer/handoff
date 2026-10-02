/**
 * Versioned wire contracts for the read-only Deposit Closeout core.
 * camelCase and required-but-nullable fields are intentional versioned wire names.
 * Core numbers are exact safe JSON integers, NOT @osdk/functions.Long (a string).
 * This module is pure domain code; the published JSON-string boundary is separate.
 */
export interface SourceReference {
  evidenceId: string;
  sourceClass: string;
  sourceVersion: string;
  locator: string;
  page: number | null;
  quote: string | null;
}
export interface EvidenceInput {
  evidenceId: string;
  recordKind: string;
  sourceClass: string;
  externalRecordId: string;
  sourceVersion: string;
  locator: string;
  occurredAt: string | null;
  learnedAt: string;
  supersedesEvidenceId: string | null;
  proposedItemIds: string[];
  associationAccepted: boolean;
  excerpt: string | null;
}
export interface DateFact {
  factKey: string;
  state: string;
  value: string | null;
  evidenceIds: string[];
  acceptedBy: string | null;
  reason: string;
}
export interface CaseParty {
  partyId: string;
  displayLabel: string;
  roles: string[];
  effectiveFrom: string | null;
  effectiveUntil: string | null;
  principalId: string | null;
  evidenceIds: string[];
}
export interface AuthorityGrant {
  grantId: string;
  partyId: string;
  authorityVersion: string;
  allowedActionKinds: string[];
  amountLimitCents: number | null;
  effectiveFrom: string;
  effectiveUntil: string | null;
  revoked: boolean;
  evidenceIds: string[];
}
export interface RecipientInstructions {
  versionId: string;
  statementPartyIds: string[];
  refundPartyIds: string[];
  state: string;
  statementMethod: string;
  refundMethod: string;
  verifiedRouteReference: string | null;
  evidenceIds: string[];
}
export interface OpenQuestion {
  questionId: string;
  question: string;
  reason: string;
  resolverRole: string;
  resolverPartyId: string | null;
  neededRecord: string | null;
  affectedItemIds: string[];
  affectedActionKinds: string[];
}
export interface ChargeInput {
  itemId: string;
  location: string;
  description: string;
  category: string;
  costState: string;
  vendorCostCents: number | null;
  costVersionId: string | null;
  proposedAllocation: string;
  acceptedAllocation: string;
  allowabilityState: string;
  supportedAmountCents: number | null;
  choiceState: string;
  chosenAmountCents: number | null;
  reason: string;
  evidenceIds: string[];
  unresolvedQuestionIds: string[];
  reviewRequired: boolean;
}
export interface BalanceSnapshot {
  balanceId: string;
  amountCents: number | null;
  asOf: string;
  custodianPartyId: string | null;
  sourceEvidenceId: string;
  basis: string;
  includedTransactionIds: string[];
  reconciliationState: string;
}
export interface MoneyEvent {
  eventId: string;
  canonicalTransactionId: string;
  sourceEventId: string;
  kind: string;
  status: string;
  amountCents: number;
  occurredAt: string;
  learnedAt: string;
  sourceEvidenceId: string;
  requestId: string | null;
  reversesTransactionId: string | null;
  chargeItemId: string | null;
}
export interface OtherBalance {
  balanceId: string;
  description: string;
  amountCents: number | null;
  state: string;
  sourceEvidenceId: string;
  unresolvedQuestionIds: string[];
}
export interface StatementFact {
  versionId: string;
  kind: string;
  reviewId: string;
  contentHash: string;
  recipientInstructionsVersion: string;
  issuedAt: string | null;
  issuanceEvidenceIds: string[];
}
export interface ApprovalFact {
  approvalId: string;
  decision: string;
  actionKind: string;
  targetVersionId: string;
  payloadFingerprint: string;
  authorityVersion: string;
  actorPartyId: string;
  decidedAt: string;
  revokedApprovalId: string | null;
}
export interface RequestFact {
  requestId: string;
  actionKind: string;
  targetVersionId: string;
  payloadFingerprint: string;
  amountCents: number | null;
  state: string;
  approvalIds: string[];
  externalReference: string | null;
}
export interface ExecutionFact {
  eventId: string;
  kind: string;
  requestId: string | null;
  attemptId: string | null;
  occurredAt: string;
  learnedAt: string;
  resultCode: string;
  evidenceIds: string[];
}
export interface RelatedTaskFact {
  taskId: string;
  description: string;
  state: string;
  responsibleRole: string;
  completionEvidenceIds: string[];
}
export interface CaseSnapshot {
  schemaVersion: string;
  caseId: string;
  managementCompanyId: string;
  homeId: string;
  tenancyId: string;
  revision: number;
  origin: string;
  jurisdiction: string;
  tenancyRegime: string;
  tenancyEndsInFull: boolean | null;
  cashSecurityDeposit: boolean | null;
  currency: string;
  agreementEvidenceIds: string[];
  dates: DateFact[];
  parties: CaseParty[];
  authorityGrants: AuthorityGrant[];
  recipients: RecipientInstructions;
  evidence: EvidenceInput[];
  charges: ChargeInput[];
  depositBalance: BalanceSnapshot;
  moneyEvents: MoneyEvent[];
  otherBalances: OtherBalance[];
  questions: OpenQuestion[];
  specialCircumstances: string[];
  interimConditionState: string;
  interimConditionEvidenceIds: string[];
  interimConditionReason: string;
  priorStatements: StatementFact[];
  priorApprovals: ApprovalFact[];
  priorRequests: RequestFact[];
  executionEvents: ExecutionFact[];
  relatedTasks: RelatedTaskFact[];
}
export interface ReviewRequest {
  snapshot: CaseSnapshot;
  ruleReleaseId: string;
  reviewClock: string;
}
export interface RequirementResult {
  requirementKey: string;
  question: string;
  ruleQuestionId: string | null;
  track: string;
  dueKind: string;
  legalDueDate: string | null;
  internalTargetAt: string | null;
  triggerFactKeys: string[];
  state: string;
  responsibleRole: string;
  prerequisiteIds: string[];
  completionCondition: string;
  completionEvidenceIds: string[];
  reason: string;
}
export interface ScopeRequirements {
  scopeState: string;
  jurisdiction: string;
  regime: string;
  ruleReleaseId: string;
  ruleStatus: string;
  appliedQuestionIds: string[];
  limitations: string[];
  requirements: RequirementResult[];
}
export interface ItemDecision {
  itemId: string;
  costVersionId: string | null;
  vendorCostCents: number | null;
  allocation: string;
  allowability: string;
  supportedAmountCents: number | null;
  chosenAmountCents: number | null;
  choiceState: string;
  reason: string;
  sourceReferences: SourceReference[];
  ruleQuestionIds: string[];
  missingInputIds: string[];
  requiresReviewer: boolean;
  fingerprint: string;
}
export interface AccountResult {
  currency: string;
  recordedDepositCents: number | null;
  balanceSourceEvidenceId: string;
  balanceAsOf: string;
  reconciliationState: string;
  knownChosenDeductionsCents: number;
  totalDeductionsCents: number | null;
  existingNetPostingCents: number | null;
  postingDeltaCents: number | null;
  existingDepositApplicationsCents: number | null;
  depositApplicationDeltaCents: number | null;
  priorNetRefundsCents: number | null;
  pendingReservedRefundCents: number | null;
  finalRefundCents: number | null;
  proposedExcessReceivableCents: number | null;
  unresolvedItemIds: string[];
  otherBalanceIds: string[];
  finalAccountReady: boolean;
  notFinalReasons: string[];
  recipientInstructionsVersion: string;
  recipientState: string;
}
export interface AvailableAction {
  actionKey: string;
  actionKind: string;
  availability: string;
  responsibleRole: string;
  targetVersionId: string | null;
  payloadFingerprint: string | null;
  amountCents: number | null;
  prerequisiteIds: string[];
  requiredApprovalScopes: string[];
  reason: string;
  fallbackDescription: string | null;
}
export interface TrackOutcome {
  track: string;
  state: string;
  openRequirementKeys: string[];
  completionEvidenceIds: string[];
  reason: string;
}
export interface Outcomes {
  tracks: TrackOutcome[];
  depositComplete: boolean;
  overallCaseComplete: boolean;
  summary: string;
}
export interface ReviewResult {
  scopeRequirements: ScopeRequirements;
  itemDecisions: ItemDecision[];
  account: AccountResult;
  missingInputs: OpenQuestion[];
  actions: AvailableAction[];
  outcomes: Outcomes;
}
export interface ReviewMetadata {
  schemaVersion: string;
  baseCaseRevision: number;
  inputHash: string;
  ruleReleaseId: string;
  codeVersion: string;
  reviewClock: string;
}
export interface ReviewEnvelope {
  metadata: ReviewMetadata;
  result: ReviewResult;
}
export interface SyntheticAssumptions {
  ordinaryPeriodDays: number;
  finalPeriodDays: number;
  periodBasis: string;
  triggerAcceptance: string;
  scopeBasis: string;
  interimQualification: string;
  interimMoneyHandling: string;
  missingAddressHandling: string;
  missingInvoiceTreatment: string;
}
export interface SyntheticRuleManifest {
  schemaVersion: string;
  ruleReleaseId: string;
  status: string;
  implementationStatus: string;
  legalReviewStatus: string;
  legalReviewedBy: string | null;
  legalEffectiveFrom: string | null;
  legalEffectiveUntil: string | null;
  allowedOrigins: string[];
  jurisdiction: string;
  tenancyRegime: string;
  currency: string;
  allowLiveUse: boolean;
  questionIds: string[];
  sourceReferences: SourceReference[];
  syntheticAssumptions: SyntheticAssumptions;
  warnings: string[];
}
export interface SafetyProfile {
  schemaVersion: string;
  phase: string;
  syntheticOnly: boolean;
  allowOntologyWrites: boolean;
  allowExternalEffects: boolean;
  allowModelAssistance: boolean;
  allowRuleActivation: boolean;
}
