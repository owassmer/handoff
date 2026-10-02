import { describe, expect, it } from "vitest";
import { canonical_json, from_wire } from "../domain/codec.js";
import type { ReviewRequest } from "../domain/types.js";
import { baseRequest, loadReviewRelease } from "./fixtures/helpers.js";
import { caseIdFor } from "../phase_c/types.js";
import { nativeReview } from "../phase_c/validation.js";
import { approvalValidity, buildIntent } from "../lifecycle/approvals.js";
import { parseWorkflowState } from "../lifecycle/codec.js";
import { canonicalTransactionIdFor, instructionHashFor, instructionKeyFor, requestIdFor } from "../lifecycle/ids.js";
import { financialMaterialityHash, nativeGross } from "../lifecycle/materiality.js";
import { applyDecisionCommand, initializeWorkflow } from "../lifecycle/prerequisites.js";
import { renderCents, statementBasisCurrent } from "../lifecycle/statements.js";
import { SYNTHETIC_STATEMENT_BADGE } from "../lifecycle/types.js";
import type { ApprovalRecord, LifecycleCommand, OperationIntentSpec, PureContext, RequestInstruction, WorkflowStateV2 } from "../lifecycle/types.js";

const ACTOR = "c47a52a0-0048-4607-931f-f4df283ae7c4";
const NOW = "2026-09-18T12:00:00Z";
const context = (commandId: string, extra: Partial<PureContext> = {}): PureContext => ({ actorId: ACTOR, serverNow: NOW,
  isAdministrator: true, commandId, basisReviewId: "decision-review", ...extra });

function fixture(final: boolean = true, chosen: number = 15000): ReviewRequest {
  const request = structuredClone(baseRequest());
  request.ruleReleaseId = loadReviewRelease().ruleReleaseId;
  request.snapshot.caseId = caseIdFor(request.snapshot.managementCompanyId, request.snapshot.tenancyId);
  request.snapshot.parties.forEach((party): void => {
    if (party.roles.some((role): boolean => ["MANAGER", "ACCOUNTANT"].includes(role))) party.principalId = ACTOR;
  });
  if (final) {
    Object.assign(request.snapshot.charges.find((item): boolean => item.itemId === "additional-item")!, {
      costState: "KNOWN", vendorCostCents: 15000, costVersionId: "ev-extent", acceptedAllocation: "TENANT",
      allowabilityState: "SUPPORTED", supportedAmountCents: 15000, chosenAmountCents: chosen,
      choiceState: "CHOSEN", reviewRequired: false, unresolvedQuestionIds: [], reason: "Accepted final synthetic cost and chosen amount",
    });
    request.snapshot.questions = [];
  }
  return from_wire("ReviewRequest", request);
}
interface TestState { request: ReviewRequest; workflow: WorkflowStateV2 }
function initialized(request: ReviewRequest = fixture()): TestState {
  return applyDecisionCommand(request, null, { kind: "INIT_WORKFLOW", payload: {} }, context("init"));
}
function run(state: TestState, command: LifecycleCommand, id: string, extra: Partial<PureContext> = {}): TestState {
  return applyDecisionCommand(state.request, state.workflow, command, context(id, extra));
}
function prepared(request: ReviewRequest = fixture()): TestState {
  return run(initialized(request), { kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "Prepare only" } }, "prepare");
}
function spec(kind: OperationIntentSpec["kind"], amountCents: number | null, statementId: string | null = null): OperationIntentSpec {
  return { kind, amountCents, statementId, dispositionKey: "first-installment", replacesRequestId: null, reversesTransactionId: null };
}
function approve(state: TestState, intent: OperationIntentSpec, id: string = "approve"): TestState {
  return run(state, { kind: "DECIDE_APPROVAL", payload: { intent, decision: "APPROVED" } }, id);
}
function valid(state: TestState, approval: ApprovalRecord): boolean {
  return approvalValidity(state.request, nativeReview(state.request), state.workflow, approval, NOW).valid;
}
function latestApproval(state: TestState): ApprovalRecord { return state.workflow.approvals.at(-1)!; }

/** Handcrafted native inputs only: this is not a request/results reducer test. */
function addOperationFixture(state: TestState, approval: ApprovalRecord, status: "READY" | "OUTCOME_UNKNOWN" | "SUCCEEDED"): RequestInstruction {
  const intent = approval.intent;
  const instructions = intent.kind === "REFUND" ? structuredClone(state.workflow.refundInstructions)
    : intent.kind === "STATEMENT_DISPATCH" ? structuredClone(state.workflow.statementInstructions) : null;
  const request: RequestInstruction = { caseId: state.workflow.caseId, managementCompanyId: state.workflow.managementCompanyId,
    environmentId: state.workflow.environmentId, requestId: requestIdFor(state.workflow, intent), instructionKey: instructionKeyFor(state.workflow, intent),
    createdCommandId: "request-fixture", kind: intent.kind, intent: structuredClone(intent), instructions,
    instructionHash: instructionHashFor(state.workflow, intent, instructions), approvalIds: [approval.approvalId],
    createdBy: ACTOR, createdAt: NOW, businessCreatedAt: NOW, replacesRequestId: null, reversesTransactionId: intent.reversesTransactionId };
  state.workflow.requests.push(request);
  state.request.snapshot.priorRequests.push({ requestId: request.requestId,
    actionKind: intent.kind === "REFUND" ? "REQUEST_REFUND" : "REQUEST_LEDGER_POSTING", targetVersionId: intent.targetVersionId,
    payloadFingerprint: intent.materialityHash, amountCents: intent.amountCents, state: status, approvalIds: [approval.approvalId], externalReference: null });
  if (status === "SUCCEEDED") {
    const transaction = canonicalTransactionIdFor(state.workflow, request.requestId);
    const proofId = `proof-${intent.kind}`;
    const effectTime = intent.reversesTransactionId === null ? NOW : "2026-09-18T12:00:01Z";
    // The native contract requires reversal events to retain the ORIGINAL
    // request association and follow its settlement, independent of D's request.
    const nativeRequestId = intent.reversesTransactionId === null ? request.requestId
      : state.request.snapshot.moneyEvents.find((entry): boolean => entry.canonicalTransactionId === intent.reversesTransactionId)!.requestId;
    state.request.reviewClock = effectTime;
    state.workflow.businessClock = effectTime;
    state.request.snapshot.evidence.push({ ...state.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-balance")!,
      evidenceId: proofId, occurredAt: effectTime, learnedAt: effectTime, externalRecordId: `record-${intent.kind}` });
    state.request.snapshot.moneyEvents.push({ eventId: `event-${intent.kind}`, canonicalTransactionId: transaction,
      sourceEventId: `source-${intent.kind}`, kind: intent.kind === "REFUND" ? "REFUND_SETTLED" : intent.kind, status: "SETTLED", amountCents: intent.amountCents!,
      occurredAt: effectTime, learnedAt: effectTime, sourceEvidenceId: proofId, requestId: nativeRequestId,
      reversesTransactionId: intent.reversesTransactionId, chargeItemId: null });
  }
  return request;
}

describe("Phase D pure statements and prerequisites", (): void => {
  it("initializes split channels preserving verification, no money or revision edits", (): void => {
    const request = fixture();
    const original = structuredClone(request);
    const result = initialized(request);
    expect(request).toEqual(original);
    expect(result.request.snapshot.revision).toBe(request.snapshot.revision);
    expect(result.workflow.businessClock).toBe(NOW);
    expect(result.workflow.statementInstructions.state).toBe("VERIFIED");
    expect(result.workflow.refundInstructions.state).toBe("VERIFIED");
    expect(result.workflow.statementInstructions.versionId).not.toBe(result.workflow.refundInstructions.versionId);
    expect(result.workflow.requests).toEqual([]);
    expect(result.request.snapshot.moneyEvents).toEqual([]);
    expect(parseWorkflowState(canonical_json(result.workflow))).toEqual(result.workflow);
  });
  it("takes the exact microsecond max without business time authorizing a future grant", (): void => {
    const request = fixture();
    request.reviewClock = "2027-01-01T00:00:00.000002Z";
    const state = initialized(request);
    expect(state.workflow.businessClock).toBe(request.reviewClock);
    state.request.snapshot.authorityGrants[0]!.effectiveFrom = "2026-10-01T00:00:00Z";
    expect(() => run(state, { kind: "SET_INTERIM_QUALIFICATION", payload: { state: "ACCEPTED", evidenceIds: ["ev-extent"], reason: "Explicit condition" } }, "interim")).toThrow(/authority/);
  });
  it("requires admin init and rejects nondecision commands clearly", (): void => {
    expect(() => initializeWorkflow(fixture(), context("init", { isAdministrator: false }))).toThrow(/administrator/);
    expect(() => run(initialized(), { kind: "CLAIM_REQUEST", payload: { requestId: "x" } }, "claim")).toThrow(/does not support/);
  });
  it.each([[15000, 40000, 160000, "$400.00 USD", "$1,600.00 USD"], [10000, 35000, 165000, "$350.00 USD", "$1,650.00 USD"]] as const)(
    "freezes deductions and refund for chosen additional %i", (chosen, deductions, refund, deductionsText, refundText): void => {
      const state = prepared(fixture(true, chosen));
      const statement = state.workflow.statements[0]!;
      expect(statement.content.account.totalDeductionsCents).toBe(deductions);
      expect(statement.content.account.finalRefundCents).toBe(refund);
      expect(statement.renderedText).toContain(`Total deductions: ${deductionsText}`);
      expect(statement.renderedText).toContain(`Unpaid final refund: ${refundText}`);
      expect(statement.renderedText).toContain(SYNTHETIC_STATEMENT_BADGE);
      expect(statement.renderedText).toMatchSnapshot();
      const paint = statement.content.items.find((item): boolean => item.itemId === "paint-800")!;
      expect(paint.decision.chosenAmountCents).toBe(0);
      expect(paint.decision.allocation).toBe("OWNER");
      expect(parseWorkflowState(canonical_json(state.workflow))).toEqual(state.workflow);
    });
  it("unknown is not zero; only a native accepted proven interim condition permits interim", (): void => {
    let state = initialized(fixture(false));
    expect(() => run(state, { kind: "PREPARE_STATEMENT", payload: { kind: "INTERIM", supersedesId: null, reason: "Delayed invoice" } }, "bad")).toThrow(/qualification/);
    state = run(state, { kind: "SET_INTERIM_QUALIFICATION", payload: { state: "ACCEPTED", evidenceIds: ["ev-extent"], reason: "Separate synthetic qualifying condition accepted, not an invoice-delay inference" } }, "qualify");
    state = run(state, { kind: "PREPARE_STATEMENT", payload: { kind: "INTERIM", supersedesId: null, reason: "Prepare qualified interim" } }, "interim");
    const statement = state.workflow.statements[0]!;
    expect(statement.content.account.totalDeductionsCents).toBeNull();
    expect(statement.content.account.finalRefundCents).toBeNull();
    expect(statement.renderedText).toContain("Total deductions: UNKNOWN");
    expect(statement.content.items.find((item): boolean => item.itemId === "additional-item")!.decision.chosenAmountCents).toBeNull();
    expect(() => run(state, { kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "Still unknown" } }, "final")).toThrow();
  });
  it("zero-ready final account remains zero and cannot approve a zero payment", (): void => {
    const request = fixture();
    request.snapshot.depositBalance.amountCents = 0;
    request.snapshot.charges = [];
    const state = prepared(request);
    expect(state.workflow.statements[0]!.content.account.finalRefundCents).toBe(0);
    expect(renderCents(0)).toBe("$0.00 USD");
    expect(() => approve(state, spec("REFUND", 0))).toThrow(/positive/);
  });
  it("reuses unchanged statement before new time/review metadata enters content", (): void => {
    const state = prepared();
    const copy = structuredClone(state);
    const repeated = run(state, { kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "Recheck" } }, "later", { serverNow: "2026-09-19T12:00:00Z", basisReviewId: "new-review" });
    expect(repeated.workflow.statements).toEqual(state.workflow.statements);
    expect(state).toEqual(copy);
    expect(repeated.workflow.currentStatementId).toBe(state.workflow.currentStatementId);
  });
  it("prepares without a refund route, never makes combined C state falsely verified", (): void => {
    let state = initialized();
    state = run(state, { kind: "SET_REFUND_INSTRUCTIONS", payload: { partyIds: ["demo-resident"], state: "UNCONFIRMED", method: null, routeReference: null, evidenceIds: [] } }, "missing-refund");
    expect(state.request.snapshot.recipients.state).toBe("MISSING");
    state = run(state, { kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "Independent statement" } }, "prepare");
    expect(state.workflow.statements[0]!.content.account.recipientState).toBe("VERIFIED");
    expect(() => approve(state, spec("STATEMENT_DISPATCH", null, state.workflow.currentStatementId))).not.toThrow();
    expect(() => approve(state, spec("REFUND", 160000))).toThrow(/refund channel/);
  });
  it("unconfirmed statement delivery may prepare but cannot approve dispatch", (): void => {
    let state = initialized();
    state = run(state, { kind: "SET_STATEMENT_INSTRUCTIONS", payload: { partyIds: ["demo-resident"], state: "UNCONFIRMED", method: null, routeReference: null, evidenceIds: [] } }, "route");
    state = run(state, { kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "Intended party known" } }, "prepare");
    expect(state.workflow.statements[0]!.content.parties[0]!.displayLabel).toBe("Synthetic Resident A");
    expect(() => approve(state, spec("STATEMENT_DISPATCH", null, state.workflow.currentStatementId))).toThrow(/delivery channel/);
  });
  it("scope correction is whitelisted and unsupported scope stops definitive content", (): void => {
    const state = prepared();
    const corrected = run(state, { kind: "ACCEPT_SCOPE_FACTS", payload: { jurisdiction: "CA", tenancyRegime: "CONVENTIONAL_RESIDENTIAL",
      tenancyEndsInFull: true, cashSecurityDeposit: true, evidenceIds: ["ev-agreement"], reason: "Corrected source" } }, "scope");
    expect(corrected.request.snapshot.homeId).toBe(state.request.snapshot.homeId);
    expect(corrected.request.snapshot.tenancyId).toBe(state.request.snapshot.tenancyId);
    expect(nativeReview(corrected.request).result.scopeRequirements.scopeState).toBe("UNSUPPORTED");
    expect(statementBasisCurrent(corrected.request, nativeReview(corrected.request), corrected.workflow, state.workflow.statements[0]!)).toBe(false);
    expect(() => run(corrected, { kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "No fallback" } }, "prepare-2")).toThrow();
  });
  it.each(["MODEL_PROPOSAL", "FUTURE", "UNASSOCIATED"])("rejects %s source as prerequisite proof", (mode): void => {
    const state = initialized();
    const evidence = state.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-extent")!;
    if (mode === "MODEL_PROPOSAL") evidence.sourceClass = "MODEL_PROPOSAL";
    if (mode === "FUTURE") evidence.learnedAt = "2027-01-01T00:00:00Z";
    if (mode === "UNASSOCIATED") evidence.associationAccepted = false;
    expect(() => run(state, { kind: "SET_INTERIM_QUALIFICATION", payload: { state: "ACCEPTED", evidenceIds: ["ev-extent"], reason: "Explicit claim" } }, "qualify")).toThrow(/proof/);
  });
  it.each(["demo-manager", "demo-accountant", "demo-custodian"])("recipient upsert cannot overwrite %s", (partyId): void => {
    const state = initialized();
    const party = { ...state.request.snapshot.parties.find((p): boolean => p.partyId === "demo-resident")!, partyId };
    expect(() => run(state, { kind: "UPSERT_RECIPIENT_PARTY", payload: { party } }, "replace")).toThrow(/cannot overwrite/);
  });
  it("new recipient creates no operator authority or grants; old statement labels stay frozen", (): void => {
    const state = prepared();
    const resident = state.request.snapshot.parties.find((p): boolean => p.partyId === "demo-resident")!;
    const updated = run(state, { kind: "UPSERT_RECIPIENT_PARTY", payload: { party: { ...resident, displayLabel: "Corrected synthetic name" } } }, "rename");
    expect(updated.workflow.statements).toEqual(state.workflow.statements);
    expect(updated.workflow.statements[0]!.content.parties[0]!.displayLabel).toBe("Synthetic Resident A");
    expect(statementBasisCurrent(updated.request, nativeReview(updated.request), updated.workflow, updated.workflow.statements[0]!)).toBe(false);
    const additional = run(updated, { kind: "UPSERT_RECIPIENT_PARTY", payload: { party: { ...resident, partyId: "resident-b" } } }, "new-party");
    expect(additional.request.snapshot.authorityGrants).toEqual(state.request.snapshot.authorityGrants);
    expect(additional.request.snapshot.parties.at(-1)!.principalId).toBeNull();
    expect(() => run(state, { kind: "UPSERT_RECIPIENT_PARTY", payload: { party: { ...resident, principalId: ACTOR, roles: ["MANAGER"] } } }, "operator")).toThrow(/only resident/);
  });
  it("corrective version links old statement without mutating it", (): void => {
    const state = prepared();
    const old = structuredClone(state.workflow.statements[0]!);
    state.request.snapshot.charges.find((item): boolean => item.itemId === "additional-item")!.chosenAmountCents = 10000;
    const corrected = run(state, { kind: "PREPARE_STATEMENT", payload: { kind: "CORRECTIVE", supersedesId: old.statementId, reason: "Reduced choice" } }, "correct");
    expect(corrected.workflow.statements[0]).toEqual(old);
    expect(corrected.workflow.statements[1]!.supersedesStatementId).toBe(old.statementId);
    expect(corrected.workflow.statements[1]!.content.account.finalRefundCents).toBe(165000);
    expect(parseWorkflowState(canonical_json(corrected.workflow))).toEqual(corrected.workflow);
    expect(() => run(state, { kind: "PREPARE_STATEMENT", payload: { kind: "CORRECTIVE", supersedesId: "absent", reason: "Bad reference" } }, "bad")).toThrow(/earlier/);
  });
});

describe("Phase D materiality and actor-specific exact approvals", (): void => {
  it("stores actual manager vs accountant grant attribution and no automatic requests", (): void => {
    let state = prepared();
    state = approve(state, spec("STATEMENT_DISPATCH", null, state.workflow.currentStatementId), "statement-approval");
    state = approve(state, spec("REFUND", 160000), "refund-approval");
    expect(state.workflow.approvals.map((entry): string => entry.actorPartyId)).toEqual(["demo-manager", "demo-accountant"]);
    expect(state.workflow.approvals.every((entry): boolean => entry.actorId === ACTOR && entry.authorityVersion === "demo-authority-v1")).toBe(true);
    expect(state.workflow.requests).toEqual([]);
    expect(state.workflow.approvals.every((entry): boolean => valid(state, entry))).toBe(true);
    expect(parseWorkflowState(canonical_json(state.workflow))).toEqual(state.workflow);
  });
  it.each(["revoked", "expired", "limit", "principal", "role", "future-proof", "grant-version"])("invalidates current authority after %s, preserves history", (change): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const record = structuredClone(latestApproval(state));
    const grant = state.request.snapshot.authorityGrants.find((entry): boolean => entry.partyId === "demo-accountant")!;
    const party = state.request.snapshot.parties.find((entry): boolean => entry.partyId === "demo-accountant")!;
    if (change === "revoked") grant.revoked = true;
    if (change === "expired") grant.effectiveUntil = NOW;
    if (change === "limit") grant.amountLimitCents = 159999;
    if (change === "principal") party.principalId = "another-principal";
    if (change === "role") party.roles = ["OWNER"];
    if (change === "grant-version") grant.authorityVersion = "new-authority-v2";
    if (change === "future-proof") state.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-authority")!.learnedAt = "2027-01-01T00:00:00Z";
    expect(valid(state, record)).toBe(false);
    expect(state.workflow.approvals[0]).toEqual(record);
    if (change !== "grant-version") expect(() => approve(state, spec("REFUND", 160000), "another")).toThrow(/authority/);
  });
  it("role label without the trusted actor principal is never approval authority", (): void => {
    const state = prepared();
    expect(() => run(state, { kind: "DECIDE_APPROVAL", payload: { intent: spec("REFUND", 160000), decision: "APPROVED" } }, "impostor", { actorId: "some-manager", isAdministrator: false })).toThrow(/authority/);
  });
  it("immutable rejection grants nothing; own actor can append revocation even after grant revoked", (): void => {
    let state = approve(prepared(), spec("REFUND", 160000));
    const original = structuredClone(latestApproval(state));
    const rejected = run(state, { kind: "DECIDE_APPROVAL", payload: { intent: spec("REFUND", 160000), decision: "REJECTED" } }, "reject");
    expect(valid(rejected, latestApproval(rejected))).toBe(false);
    state.request.snapshot.authorityGrants.find((grant): boolean => grant.partyId === "demo-accountant")!.revoked = true;
    state = run(state, { kind: "REVOKE_APPROVAL", payload: { approvalId: original.approvalId, reason: "Stop new use" } }, "revoke", { isAdministrator: false });
    expect(state.workflow.approvals[0]).toEqual(original);
    expect(state.workflow.approvals[1]!.revokesApprovalId).toBe(original.approvalId);
    expect(valid(state, original)).toBe(false);
    expect(() => run(state, { kind: "REVOKE_APPROVAL", payload: { approvalId: original.approvalId, reason: "Unauthorized" } }, "wrong", { actorId: "outsider", isAdministrator: false })).toThrow(/original approver/);
  });
  it("unrelated work, revision, inputHash, recheck and unrelated evidence never change approval identity", (): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const original = structuredClone(latestApproval(state));
    state.request.snapshot.revision += 20;
    state.request.reviewClock = "2026-09-19T12:00:00Z";
    state.workflow.businessClock = state.request.reviewClock;
    state.request.snapshot.relatedTasks.push({ taskId: "independent", description: "Independent work", state: "OPEN", responsibleRole: "MANAGER", completionEvidenceIds: [] });
    state.request.snapshot.evidence.push({ ...state.request.snapshot.evidence[0]!, evidenceId: "unrelated-proof", externalRecordId: "unrelated", recordKind: "FACT_ASSERTION", proposedItemIds: [], excerpt: "Unrelated work proof" });
    expect(valid(state, original)).toBe(true);
  });
  it.each(["choice", "source", "new-evidence", "scope"])("changed %s invalidates the affected approval without modifying it", (change): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const record = structuredClone(latestApproval(state));
    if (change === "choice") state.request.snapshot.charges.find((item): boolean => item.itemId === "additional-item")!.chosenAmountCents = 10000;
    if (change === "source") state.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-repair")!.sourceVersion = "2";
    if (change === "new-evidence") state.request.snapshot.evidence.push({ ...state.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-repair")!, evidenceId: "new-repair", sourceVersion: "2", supersedesEvidenceId: "ev-repair", associationAccepted: false });
    if (change === "scope") state.request.snapshot.cashSecurityDeposit = false;
    expect(valid(state, record)).toBe(false);
    expect(state.workflow.approvals[0]).toEqual(record);
  });
  it("statement-route changes affect dispatch only; refund-route changes affect refund only", (): void => {
    let state = prepared();
    state = approve(state, spec("STATEMENT_DISPATCH", null, state.workflow.currentStatementId), "dispatch");
    state = approve(state, spec("REFUND", 160000), "refund");
    state = approve(state, spec("CHARGE_POSTING", 40000), "posting");
    const [dispatch, refund, posting] = state.workflow.approvals;
    const { versionId: _statementVersion, ...statementInput } = state.workflow.statementInstructions;
    const statementChanged = run(state, { kind: "SET_STATEMENT_INSTRUCTIONS", payload: { ...statementInput, routeReference: "demo-statement-2" } }, "route");
    expect(valid(statementChanged, dispatch!)).toBe(false);
    expect(valid(statementChanged, refund!)).toBe(true);
    expect(valid(statementChanged, posting!)).toBe(true);
    const { versionId: _version, ...refundInput } = state.workflow.refundInstructions;
    const refundChanged = run(state, { kind: "SET_REFUND_INSTRUCTIONS", payload: { ...refundInput, routeReference: "demo-refund-2" } }, "refund-route");
    expect(valid(refundChanged, dispatch!)).toBe(true);
    expect(valid(refundChanged, refund!)).toBe(false);
    expect(valid(refundChanged, posting!)).toBe(true);
  });
  it("statement-only descriptive text invalidates dispatch but not ledger or refund", (): void => {
    let state = prepared();
    state = approve(state, spec("STATEMENT_DISPATCH", null, state.workflow.currentStatementId), "dispatch");
    state = approve(state, spec("REFUND", 160000), "refund");
    state = approve(state, spec("CHARGE_POSTING", 40000), "ledger");
    state.request.snapshot.charges[0]!.description = "Corrected display text only";
    expect(state.workflow.approvals.map((entry): boolean => valid(state, entry))).toEqual([false, true, true]);
  });
  it("an unverified account projects current invalidity without rewriting an approved record", (): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const old = structuredClone(latestApproval(state));
    state.request.snapshot.depositBalance.amountCents = null;
    const projected = approvalValidity(state.request, nativeReview(state.request), state.workflow, old, NOW);
    expect(projected.valid).toBe(false);
    expect(projected.reason).toContain("currently unverifiable");
    expect(state.workflow.approvals[0]).toEqual(old);
  });
  it("original actor may revoke after its principal mapping is removed", (): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const old = latestApproval(state);
    state.request.snapshot.parties.find((party): boolean => party.partyId === old.actorPartyId)!.principalId = null;
    const revoked = run(state, { kind: "REVOKE_APPROVAL", payload: { approvalId: old.approvalId, reason: "Withdraw own historical approval" } }, "revoke", { isAdministrator: false });
    expect(revoked.workflow.approvals.at(-1)!.revokesApprovalId).toBe(old.approvalId);
  });
  it("recording/learning times with unchanged usable evidence do not change identity", (): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const old = latestApproval(state);
    const proof = state.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-repair")!;
    proof.learnedAt = "2026-09-05T12:00:00Z";
    expect(valid(state, old)).toBe(true);
  });
  it("financial display statement link is outside economic identity", (): void => {
    const state = prepared();
    const a = buildIntent(state.request, nativeReview(state.request), state.workflow, spec("REFUND", 160000));
    const b = buildIntent(state.request, nativeReview(state.request), state.workflow, spec("REFUND", 160000, state.workflow.currentStatementId));
    expect(a.targetVersionId).toBe(b.targetVersionId);
    expect(requestIdFor(state.workflow, a)).toBe(requestIdFor(state.workflow, b));
  });
  it("own pending reservation preserves basis and permits approval up to unpaid liability, not double availability", (): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const approval = latestApproval(state);
    addOperationFixture(state, approval, "READY");
    const account = nativeReview(state.request).result.account;
    expect(account.pendingReservedRefundCents).toBe(160000);
    expect(account.finalRefundCents).toBe(160000);
    expect(valid(state, approval)).toBe(true);
    expect(buildIntent(state.request, nativeReview(state.request), state.workflow, spec("REFUND", 160000)).targetVersionId).toBe(approval.intent.targetVersionId);
  });
  it("expected posting, application and refund preserve original gross basis, statement and every approval", (): void => {
    let state = prepared();
    state = approve(state, spec("STATEMENT_DISPATCH", null, state.workflow.currentStatementId), "dispatch");
    state = approve(state, spec("CHARGE_POSTING", 40000), "posting");
    state = approve(state, spec("DEPOSIT_APPLICATION", 40000), "application");
    state = approve(state, spec("REFUND", 160000), "refund");
    const old = structuredClone(state.workflow.approvals);
    old.filter((approval): boolean => approval.scope !== "STATEMENT_DISPATCH").forEach((approval): void => { addOperationFixture(state, approval, "SUCCEEDED"); });
    const base = nativeReview(state.request);
    expect(base.result.account.finalRefundCents).toBe(0);
    expect(base.result.account.postingDeltaCents).toBe(0);
    expect(base.result.account.depositApplicationDeltaCents).toBe(0);
    expect(nativeGross(base.result.account)).toBe(200000);
    expect(old.every((approval): boolean => valid(state, approval))).toBe(true);
    expect(state.workflow.approvals).toEqual(old);
    expect(statementBasisCurrent(state.request, base, state.workflow, state.workflow.statements[0]!)).toBe(true);
    expect(() => buildIntent(state.request, base, state.workflow, spec("REFUND", 160000))).toThrow(/exceeds/);
  });
  it("external unknown is not stripped and blocks new approvals", (): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const approval = latestApproval(state);
    state.request.snapshot.priorRequests.push({ requestId: "external-unknown", actionKind: "REQUEST_REFUND", targetVersionId: "external-target", payloadFingerprint: "external", amountCents: 5000, state: "OUTCOME_UNKNOWN", approvalIds: [], externalReference: null });
    expect(financialMaterialityHash(state.request, state.workflow, "REFUND")).toBeNull();
    expect(valid(state, approval)).toBe(false);
    expect(() => approve(state, spec("REFUND", 10000), "new")).toThrow(/full verified/);
  });
  it("own unknown control does not erase history, but full native admission still blocks", (): void => {
    const state = approve(prepared(), spec("REFUND", 160000));
    const approval = latestApproval(state);
    addOperationFixture(state, approval, "OUTCOME_UNKNOWN");
    expect(valid(state, approval)).toBe(true);
    expect(() => approve(state, spec("REFUND", 10000), "new")).toThrow(/full verified/);
  });
  it("settling both positive reversal operations preserves their changed decision basis", (): void => {
    let state = prepared();
    state = approve(state, spec("CHARGE_POSTING", 40000), "post");
    state = approve(state, spec("DEPOSIT_APPLICATION", 40000), "apply");
    const posting = addOperationFixture(state, state.workflow.approvals[0]!, "SUCCEEDED");
    const application = addOperationFixture(state, state.workflow.approvals[1]!, "SUCCEEDED");
    state.request.snapshot.charges.find((entry): boolean => entry.itemId === "additional-item")!.chosenAmountCents = 10000;
    state = approve(state, { ...spec("CHARGE_POSTING_REVERSAL", 5000), reversesTransactionId: canonicalTransactionIdFor(state.workflow, posting.requestId) }, "reverse-post");
    state = approve(state, { ...spec("DEPOSIT_APPLICATION_REVERSAL", 5000), reversesTransactionId: canonicalTransactionIdFor(state.workflow, application.requestId) }, "reverse-apply");
    const approvals = state.workflow.approvals.slice(-2);
    approvals.forEach((approval): void => { addOperationFixture(state, approval, "SUCCEEDED"); });
    const base = nativeReview(state.request);
    expect(base.result.account.postingDeltaCents).toBe(0);
    expect(base.result.account.depositApplicationDeltaCents).toBe(0);
    expect(base.result.account.finalRefundCents).toBe(165000);
    expect(approvals.every((approval): boolean => valid(state, approval))).toBe(true);
  });
  it("missing canonical original makes reversal approval unverifiable", (): void => {
    let state = prepared();
    state = approve(state, spec("CHARGE_POSTING", 40000), "post");
    const posting = addOperationFixture(state, latestApproval(state), "SUCCEEDED");
    state.request.snapshot.charges.find((entry): boolean => entry.itemId === "additional-item")!.chosenAmountCents = 10000;
    state = approve(state, { ...spec("CHARGE_POSTING_REVERSAL", 5000), reversesTransactionId: canonicalTransactionIdFor(state.workflow, posting.requestId) }, "reverse");
    state.request.snapshot.moneyEvents[0]!.canonicalTransactionId = "a-different-original";
    expect(valid(state, latestApproval(state))).toBe(false);
  });
  it("negative ledger adjustment needs positive explicit reversal with canonical original", (): void => {
    let state = prepared();
    state = approve(state, spec("CHARGE_POSTING", 40000), "post");
    state = approve(state, spec("DEPOSIT_APPLICATION", 40000), "apply");
    const posting = addOperationFixture(state, state.workflow.approvals[0]!, "SUCCEEDED");
    const application = addOperationFixture(state, state.workflow.approvals[1]!, "SUCCEEDED");
    state.request.snapshot.charges.find((entry): boolean => entry.itemId === "additional-item")!.chosenAmountCents = 10000;
    const base = nativeReview(state.request);
    expect(base.result.account.postingDeltaCents).toBe(-5000);
    expect(() => buildIntent(state.request, base, state.workflow, spec("CHARGE_POSTING", -5000))).toThrow();
    const reversal = buildIntent(state.request, base, state.workflow, { ...spec("CHARGE_POSTING_REVERSAL", 5000), reversesTransactionId: canonicalTransactionIdFor(state.workflow, posting.requestId) });
    expect(reversal.amountCents).toBe(5000);
    expect(() => buildIntent(state.request, base, state.workflow, { ...spec("CHARGE_POSTING_REVERSAL", 5000), reversesTransactionId: canonicalTransactionIdFor(state.workflow, application.requestId) })).toThrow(/canonical original/);
  });
});
