import { describe, expect, it } from "vitest";
import { canonical_json } from "../domain/codec.js";
import type { ReviewRequest } from "../domain/types.js";
import type { WorkAssignment } from "../phase_c/change_types.js";
import { nativeReview } from "../phase_c/validation.js";
import { applyLifecycleCommand, authorizeLifecycleCommand, reconcileWorkflowAfterCaseChange } from "../lifecycle/commands.js";
import { hashWorkflowReview, parseWorkflowReview, parseWorkflowState } from "../lifecycle/codec.js";
import { reviewWorkflow } from "../lifecycle/review.js";
import { checkedCents, sumCents, unreservedCents } from "../lifecycle/performance.js";
import { projectRequests } from "../lifecycle/requests.js";
import { approvalValidity } from "../lifecycle/approvals.js";
import type { LifecycleCommand, OperationIntentSpec, OperationKind, PureContext, WorkflowStateV2 } from "../lifecycle/types.js";
import { requestContext, requestFixture, REQUEST_NOW } from "./phaseDRequestsSupport.js";

class LifecycleHarness {
  request: ReviewRequest = requestFixture().request;
  workflow: WorkflowStateV2 | null = null;
  assignments: WorkAssignment[] = [];
  private serial = 0;
  constructor() { this.run({ kind: "INIT_WORKFLOW", payload: {} }); }
  ctx(extra: Partial<PureContext> = {}): PureContext { return requestContext(`orchestrator-${++this.serial}`, extra); }
  run(command: LifecycleCommand, extra: Partial<PureContext> = {}): ReturnType<typeof applyLifecycleCommand> {
    const result = applyLifecycleCommand(this.request, this.assignments, this.workflow, command, this.ctx(extra));
    this.request = result.request; this.workflow = result.workflow;
    return result;
  }
  change(next: ReviewRequest): void {
    const result = reconcileWorkflowAfterCaseChange(this.request, next, this.assignments, this.workflow!, this.ctx());
    this.request = result.request; this.workflow = result.workflow;
  }
  review(at: string = REQUEST_NOW): ReturnType<typeof reviewWorkflow> {
    return reviewWorkflow(this.request, nativeReview(this.request), this.workflow!, this.assignments, at);
  }
  prepare(): string {
    return String(this.run({ kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "Pure synthetic preparation" } }).summary.statementId);
  }
  approve(kind: OperationKind, amountCents: number | null, extra: Partial<OperationIntentSpec> = {}): string {
    return String(this.run({ kind: "DECIDE_APPROVAL", payload: { decision: "APPROVED", intent: { kind, amountCents,
      statementId: kind === "STATEMENT_DISPATCH" ? this.workflow!.currentStatementId : null,
      dispositionKey: `${kind}-${++this.serial}`, replacesRequestId: null, reversesTransactionId: null, ...extra } } }).summary.approvalId);
  }
  requestOp(kind: OperationKind, amount: number | null, extra: Partial<OperationIntentSpec> = {}): string {
    const approvalId = this.approve(kind, amount, extra);
    return String(this.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
  }
  claim(id: string): string { return String(this.run({ kind: "CLAIM_REQUEST", payload: { requestId: id } }).summary.attemptId); }
  raw(id: string, outcome: "SUCCEEDED" | "FAILED" | "RETURNED" = "SUCCEEDED", amount?: number): string {
    const instruction = this.workflow!.requests.find((entry): boolean => entry.requestId === id)!;
    const attemptId = projectRequests(this.workflow!).find((entry): boolean => entry.requestId === id)!.attemptId!;
    const sourceEventId = `orchestrator-source-${++this.serial}`;
    this.run({ kind: "GENERATE_SIMULATED_RESULT", payload: { requestId: id, attemptId, sourceEventId,
      outcome, amountCents: amount ?? instruction.intent.amountCents, occurredAt: null } });
    return sourceEventId;
  }
  ingest(sourceEventId: string, extra: Partial<PureContext> = {}): void { this.run({ kind: "INGEST_RESULT", payload: { sourceEventId } }, extra); }
  perform(kind: OperationKind, amount: number | null, extra: Partial<OperationIntentSpec> = {}): string {
    const id = this.requestOp(kind, amount, extra); this.claim(id); this.ingest(this.raw(id)); return id;
  }
  complete(deduction: number = 400, refund: number = 1600): void {
    this.prepare(); this.perform("STATEMENT_DISPATCH", null);
    if (deduction > 0) { this.perform("CHARGE_POSTING", deduction); this.perform("DEPOSIT_APPLICATION", deduction); }
    if (refund > 0) this.perform("REFUND", refund);
  }
}

function completeFlag(h: LifecycleHarness): boolean { return h.review().result.outcomes.simulatedDepositWorkflowComplete; }
function requestState(h: LifecycleHarness, id: string): string { return projectRequests(h.workflow!).find((entry): boolean => entry.requestId === id)!.state; }

describe("Phase D connected pure lifecycle (not persistence/runtime proof)", (): void => {
  it("ordinary 400/1600 actually finishes all five simulation tracks without changing v1 completion", (): void => {
    const h = new LifecycleHarness(); const revision = h.request.snapshot.revision;
    expect(completeFlag(h)).toBe(false);
    h.complete();
    const result = h.review();
    expect(result.result.account).toMatchObject({ finalRefundCents: 0, postingDeltaCents: 0, depositApplicationDeltaCents: 0,
      newlyRequestableRefundCents: 0, pendingReservedRefundCents: 0 });
    expect(result.result.outcomes).toMatchObject({ simulatedDepositWorkflowComplete: true, simulatedOverallWorkflowComplete: true,
      depositComplete: false, overallCaseComplete: false, legalPerformanceConfirmed: false, completionMode: "SIMULATED" });
    expect(h.request.snapshot.revision).toBe(revision);
    expect(nativeReview(h.request).result.outcomes.depositComplete).toBe(false);
    expect(parseWorkflowState(canonical_json(h.workflow))).toEqual(h.workflow);
    expect(parseWorkflowReview(canonical_json(result))).toEqual(result);
    expect(new Set(h.request.snapshot.priorRequests.map((entry): string => entry.requestId)).size).toBe(4);
  });
  it("350/1650 changes reuse native math and complete", (): void => {
    const h = new LifecycleHarness(); const next = structuredClone(h.request);
    next.snapshot.charges[0]!.chosenAmountCents = 350;
    h.change(next); expect(h.review().result.account.finalRefundCents).toBe(1650);
    h.complete(350, 1650); expect(completeFlag(h)).toBe(true);
  });
  it("preparation, approval, request, claim and raw observations are individually not performance", (): void => {
    const h = new LifecycleHarness(); h.prepare(); expect(completeFlag(h)).toBe(false);
    const approvalId = h.approve("STATEMENT_DISPATCH", null); expect(completeFlag(h)).toBe(false);
    const id = String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
    h.claim(id); const source = h.raw(id);
    expect(h.review().result.actions.find((entry): boolean => entry.actionKey === "request:dispatch")!.workflow!.statementDetails[0]!.issued).toBe(false);
    h.ingest(source);
    expect(h.review().result.outcomes.tracks.find((entry): boolean => entry.track === "COMMUNICATIONS")!.state).toBe("FULFILLED");
    expect(completeFlag(h)).toBe(false);
  });
  it("reserve is subtracted once from native unpaid liability", (): void => {
    const h = new LifecycleHarness(); h.requestOp("REFUND", 600);
    expect(h.review().result.account).toMatchObject({ finalRefundCents: 1600, pendingReservedRefundCents: 600, newlyRequestableRefundCents: 1000 });
    expect(h.review().result.account.financialCommitments.find((entry): boolean => entry.kind === "REFUND")!.reservedCents).toBe(600);
  });
  it("unknown account remains null, never zero or payment permission", (): void => {
    const h = new LifecycleHarness(); const next = structuredClone(h.request); next.snapshot.depositBalance.reconciliationState = "UNRECONCILED"; h.change(next);
    expect(h.review().result.account.newlyRequestableRefundCents).toBeNull();
    expect(h.review().result.actions.find((entry): boolean => entry.actionKey === "request:refund")!.availability).toBe("BLOCKED");
  });
  it("a missing refund channel cannot block independent statement duty", (): void => {
    const h = new LifecycleHarness(); h.run({ kind: "SET_REFUND_INSTRUCTIONS", payload: { partyIds: [], state: "UNCONFIRMED", method: null, routeReference: null, evidenceIds: [] } });
    h.prepare(); h.perform("STATEMENT_DISPATCH", null);
    const r = h.review(); expect(r.result.outcomes.tracks.find((entry): boolean => entry.track === "COMMUNICATIONS")!.state).toBe("FULFILLED");
    expect(r.result.actions.find((entry): boolean => entry.actionKey === "request:refund")!.availability).toBe("BLOCKED");
    expect(completeFlag(h)).toBe(false);
  });
  it("verified zero refund needs no refund route/request, but still requires statement and ledger work", (): void => {
    const h = new LifecycleHarness(); const next = structuredClone(h.request); next.snapshot.depositBalance.amountCents = 400; h.change(next);
    h.run({ kind: "SET_REFUND_INSTRUCTIONS", payload: { partyIds: [], state: "UNCONFIRMED", method: null, routeReference: null, evidenceIds: [] } });
    expect(h.review().result.actions.find((entry): boolean => entry.actionKey === "request:refund")!.availability).toBe("NOT_APPLICABLE");
    h.complete(400, 0); expect(completeFlag(h)).toBe(true);
  });
  it("frozen statements and instructions survive split channel changes", (): void => {
    const h = new LifecycleHarness(); h.prepare(); const id = h.requestOp("STATEMENT_DISPATCH", null);
    const oldStatement = structuredClone(h.workflow!.statements[0]); const instruction = structuredClone(h.workflow!.requests[0]);
    const statementVersion = h.workflow!.statementInstructions.versionId;
    const { versionId: _version, ...route } = h.workflow!.refundInstructions;
    h.run({ kind: "SET_REFUND_INSTRUCTIONS", payload: { ...route, routeReference: "demo-refund-new" } });
    expect(h.workflow!.statementInstructions.versionId).toBe(statementVersion);
    expect(h.workflow!.statements[0]).toEqual(oldStatement); expect(h.workflow!.requests[0]).toEqual(instruction);
    expect(requestState(h, id)).toBe("READY");
  });
  it("unknown attempt keeps its reserve, accepts late proof after revocation, then return/replacement finishes", (): void => {
    const h = new LifecycleHarness(); h.prepare(); h.perform("STATEMENT_DISPATCH", null);
    h.perform("CHARGE_POSTING", 400); h.perform("DEPOSIT_APPLICATION", 400);
    const id = h.requestOp("REFUND", 1600); const attemptId = h.claim(id);
    h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: id, attemptId, reason: "Simulated ambiguous send" } });
    expect(h.review().result.account.pendingReservedRefundCents).toBeNull();
    expect(h.review().result.account.financialCommitments.find((entry): boolean => entry.kind === "REFUND")!.reservedCents).toBe(1600);
    expect(h.review().result.account.newlyRequestableRefundCents).toBeNull();
    expect(completeFlag(h)).toBe(false);
    const approvalId = h.workflow!.requests.find((entry): boolean => entry.requestId === id)!.approvalIds[0]!;
    h.run({ kind: "REVOKE_APPROVAL", payload: { approvalId, reason: "No new work may use this approval" } });
    expect(requestState(h, id)).toBe("OUTCOME_UNKNOWN");
    h.ingest(h.raw(id)); expect(completeFlag(h)).toBe(true);
    h.ingest(h.raw(id, "RETURNED")); expect(completeFlag(h)).toBe(false);
    expect(h.review().result.account.finalRefundCents).toBe(1600);
    h.perform("REFUND", 1600, { replacesRequestId: id });
    expect(completeFlag(h)).toBe(true);
    expect(h.request.snapshot.moneyEvents.filter((entry): boolean => entry.kind === "REFUND_RETURNED")).toHaveLength(1);
  });
  it("later revocation and expiry do not unperform completed history", (): void => {
    const h = new LifecycleHarness(); h.complete();
    const ids = h.workflow!.approvals.filter((entry): boolean => entry.decision === "APPROVED").map((entry): string => entry.approvalId);
    ids.forEach((approvalId): void => { h.run({ kind: "REVOKE_APPROVAL", payload: { approvalId, reason: "Withdraw all future permissions" } }); });
    const next = structuredClone(h.request); next.snapshot.authorityGrants.forEach((grant): void => { grant.revoked = true; }); h.change(next);
    expect(completeFlag(h)).toBe(true);
    expect(h.review().result.outcomes.tracks.find((entry): boolean => entry.track === "APPROVALS")!.state).toBe("FULFILLED");
  });
  // The longest lifecycle in this suite (about 5 s on CI's two workers); its own limit keeps it from failing unrelated releases.
  it("post-performance reduction requires separate reversals, additional refund and corrective dispatch", (): void => {
    const h = new LifecycleHarness(); h.complete(); const oldStatement = h.workflow!.currentStatementId!;
    const next = structuredClone(h.request); next.snapshot.charges[0]!.chosenAmountCents = 350; h.change(next);
    expect(completeFlag(h)).toBe(false);
    expect(h.review().result.account).toMatchObject({ postingDeltaCents: -50, depositApplicationDeltaCents: -50, finalRefundCents: 50 });
    const posting = h.request.snapshot.moneyEvents.find((entry): boolean => entry.kind === "CHARGE_POSTING")!.canonicalTransactionId;
    const application = h.request.snapshot.moneyEvents.find((entry): boolean => entry.kind === "DEPOSIT_APPLICATION")!.canonicalTransactionId;
    h.perform("CHARGE_POSTING_REVERSAL", 50, { reversesTransactionId: posting });
    h.perform("DEPOSIT_APPLICATION_REVERSAL", 50, { reversesTransactionId: application });
    h.perform("REFUND", 50);
    expect(h.review().result.outcomes.tracks.find((entry): boolean => entry.track === "MONEY")!.state).toBe("FULFILLED");
    expect(completeFlag(h)).toBe(false);
    h.run({ kind: "PREPARE_STATEMENT", payload: { kind: "CORRECTIVE", supersedesId: oldStatement, reason: "Changed chosen amount" } });
    h.perform("STATEMENT_DISPATCH", null); expect(completeFlag(h)).toBe(true);
    expect(h.workflow!.statements[0]!.content.account.totalDeductionsCents).toBe(400);
  }, 20_000);
  it("assignment, clock and expected performance preserve approval materiality", (): void => {
    const h = new LifecycleHarness(); h.prepare(); const approvalId = h.approve("REFUND", 1600);
    const approval = structuredClone(h.workflow!.approvals.find((entry): boolean => entry.approvalId === approvalId)!);
    h.assignments = [{ requirementKey: "NC:ordinary-account", assigneePartyId: "demo-manager", internalTargetAt: "2026-10-01T12:00:00Z",
      reason: "Internal follow-up", assignedBy: h.ctx().actorId, assignedAt: REQUEST_NOW }];
    const next = structuredClone(h.request); next.reviewClock = "2026-09-19T12:00:00Z"; h.change(next);
    expect(h.review().result.scopeRequirements.requirements.find((entry): boolean => entry.requirementKey === "NC:ordinary-account")!.internalTargetAt).toBe("2026-10-01T12:00:00Z");
    h.perform("CHARGE_POSTING", 400); h.perform("DEPOSIT_APPLICATION", 400);
    expect(approvalValidity(h.request, nativeReview(h.request), h.workflow!, approval, REQUEST_NOW).valid).toBe(true);
  });
  it("C recheck cannot rewind committed v2 event time behind a future demo clock", (): void => {
    const h = new LifecycleHarness(); const future = structuredClone(h.request); future.reviewClock = "2027-01-01T00:00:00Z"; h.change(future);
    h.requestOp("REFUND", 600); const committed = h.workflow!.businessClock;
    const recheck = structuredClone(h.request); recheck.reviewClock = REQUEST_NOW; h.change(recheck);
    expect(h.request.reviewClock).toBe(committed); expect(h.workflow!.businessClock).toBe(committed);
    expect(h.workflow!.events.every((entry): boolean => entry.learnedAt <= committed)).toBe(true);
  });
  it("C combined recipient compatibility maps BOTH channels with stable content IDs", (): void => {
    const h = new LifecycleHarness(); const { versionId: _version, ...input } = h.workflow!.refundInstructions;
    h.run({ kind: "SET_REFUND_INSTRUCTIONS", payload: { ...input, routeReference: "demo-only-refund" } });
    const split = structuredClone(h.workflow!);
    const noContentChange = structuredClone(h.request); noContentChange.snapshot.recipients.versionId = "legacy-new-label"; h.change(noContentChange);
    expect(h.workflow!.statementInstructions).toEqual(split.statementInstructions); expect(h.workflow!.refundInstructions).toEqual(split.refundInstructions);
    const combined = structuredClone(h.request); Object.assign(combined.snapshot.recipients, { state: "VERIFIED", verifiedRouteReference: "demo-combined-change" }); h.change(combined);
    expect(h.workflow!.statementInstructions.routeReference).toBe("demo-combined-change");
    expect(h.workflow!.refundInstructions.routeReference).toBe("demo-combined-change");
    const versions = [h.workflow!.statementInstructions.versionId, h.workflow!.refundInstructions.versionId];
    expect(versions[0]).not.toBe(versions[1]);
    const old = structuredClone(h.request); old.snapshot.recipients.versionId = "another-legacy-version"; h.change(old);
    expect([h.workflow!.statementInstructions.versionId, h.workflow!.refundInstructions.versionId]).toEqual(versions);
  });
  it("all C changes reconcile stale READY only, preserving claimed/unknown records and old instructions", (): void => {
    const h = new LifecycleHarness(); const ready = h.requestOp("REFUND", 600); const claimed = h.requestOp("REFUND", 600); h.claim(claimed);
    const oldInstructions = structuredClone(h.workflow!.requests); const oldMoney = structuredClone(h.request.snapshot.moneyEvents);
    const next = structuredClone(h.request); next.snapshot.charges[0]!.chosenAmountCents = 350; h.change(next);
    expect(requestState(h, ready)).toBe("SUPERSEDED"); expect(requestState(h, claimed)).toBe("CLAIMED");
    const event = h.workflow!.events.find((entry): boolean => entry.kind === "SUPERSEDED_BEFORE_ATTEMPT")!;
    expect(event.kind === "SUPERSEDED_BEFORE_ATTEMPT" && event.payload.replacementRequestId).toBeNull();
    expect(h.workflow!.requests).toEqual(oldInstructions); expect(h.request.snapshot.moneyEvents).toEqual(oldMoney);
    expect(h.review().result.account.pendingReservedRefundCents).toBe(600);
  });
  it("old dispatch does not fulfill a new route/version; unrelated refund changes do not reopen communication", (): void => {
    const h = new LifecycleHarness(); h.complete();
    const { versionId: _version, ...refund } = h.workflow!.refundInstructions;
    h.run({ kind: "SET_REFUND_INSTRUCTIONS", payload: { ...refund, routeReference: "demo-replacement-refund-route" } });
    expect(completeFlag(h)).toBe(true);
    const { versionId: _statementVersion, ...statement } = h.workflow!.statementInstructions;
    h.run({ kind: "SET_STATEMENT_INSTRUCTIONS", payload: { ...statement, routeReference: "demo-new-statement-route" } });
    expect(completeFlag(h)).toBe(false);
    expect(h.review().result.outcomes.tracks.find((entry): boolean => entry.track === "MONEY")!.state).toBe("FULFILLED");
    h.run({ kind: "PREPARE_STATEMENT", payload: { kind: "CORRECTIVE", supersedesId: h.workflow!.currentStatementId, reason: "Explicit correction of the issued statement's delivery route." } });
    expect(completeFlag(h)).toBe(false); h.perform("STATEMENT_DISPATCH", null); expect(completeFlag(h)).toBe(true);
  });
  it("related fulfillment only closes its own scope, and related open work only blocks overall", (): void => {
    const h = new LifecycleHarness(); const next = structuredClone(h.request);
    next.snapshot.relatedTasks.push({ taskId: "owner-related", description: "Separate owner follow-up", state: "OPEN", responsibleRole: "MANAGER", completionEvidenceIds: [] });
    h.change(next); h.complete();
    expect(h.review().result.outcomes).toMatchObject({ simulatedDepositWorkflowComplete: true, simulatedOverallWorkflowComplete: false });
    const done = structuredClone(h.request); Object.assign(done.snapshot.relatedTasks[0]!, { state: "FULFILLED", completionEvidenceIds: ["ev-repair"] }); h.change(done);
    expect(h.review().result.outcomes.simulatedOverallWorkflowComplete).toBe(true);
    const change = structuredClone(h.request); change.snapshot.charges[0]!.chosenAmountCents = 350; h.change(change);
    expect(completeFlag(h)).toBe(false);
  });
  it("stored review equality uses recorded authority time and is stable despite a later read", (): void => {
    const h = new LifecycleHarness(); const next = structuredClone(h.request);
    next.snapshot.authorityGrants.forEach((grant): void => { grant.effectiveUntil = "2026-09-19T00:00:00Z"; }); h.change(next);
    h.prepare(); h.approve("REFUND", 1600);
    const saved = h.review(REQUEST_NOW); const hash = hashWorkflowReview(saved);
    const later = h.review("2026-09-20T12:00:00Z"); expect(hashWorkflowReview(later)).not.toBe(hash);
    expect(hashWorkflowReview(h.review(saved.metadata.authorityEvaluatedAt))).toBe(hash);
    expect(parseWorkflowReview(canonical_json(saved))).toEqual(saved);
  });
  it("authorization before replay checks current role/amount but not changed applicability", (): void => {
    const h = new LifecycleHarness(); const id = h.approve("REFUND", 600); const next = structuredClone(h.request);
    next.snapshot.tenancyEndsInFull = false;
    const command: LifecycleCommand = { kind: "REQUEST_OPERATION", payload: { approvalId: id } };
    expect((): void => authorizeLifecycleCommand(next, h.workflow, command, h.ctx())).not.toThrow();
    expect((): void => authorizeLifecycleCommand(next, h.workflow, command, h.ctx({ actorId: "not-a-case-operator" }))).toThrow(/authority/i);
    next.snapshot.authorityGrants.forEach((grant): void => { grant.amountLimitCents = 500; });
    expect((): void => authorizeLifecycleCommand(next, h.workflow, command, h.ctx())).toThrow(/authority/i);
  });
  it("future business time never activates future approval authority", (): void => {
    const h = new LifecycleHarness(); const next = structuredClone(h.request); next.reviewClock = "2027-01-01T00:00:00Z";
    next.snapshot.authorityGrants.forEach((grant): void => { grant.effectiveFrom = "2026-10-01T00:00:00Z"; }); h.change(next);
    expect((): void => { h.approve("REFUND", 600); }).toThrow(/authority|grant/i);
    expect(h.review().result.actions.find((entry): boolean => entry.actionKey === "approve:refund")!.availability).toBe("BLOCKED");
  });
  it("result ingestion needs reconciliation role, not still-valid financial approval", (): void => {
    const h = new LifecycleHarness(); const id = h.requestOp("REFUND", 600); h.claim(id); const source = h.raw(id);
    expect((): void => authorizeLifecycleCommand(h.request, h.workflow, { kind: "INGEST_RESULT", payload: { sourceEventId: source } }, h.ctx({ actorId: "unknown" }))).toThrow(/authority/i);
    const approvalId = h.workflow!.requests[0]!.approvalIds[0]!; h.run({ kind: "REVOKE_APPROVAL", payload: { approvalId, reason: "Withdrawal" } });
    h.ingest(source); expect(requestState(h, id)).toBe("SUCCEEDED");
  });
  it("has no mutation side effects and retains the complete native account fields", (): void => {
    const h = new LifecycleHarness(); const original = structuredClone({ request: h.request, workflow: h.workflow, assignments: h.assignments });
    const base = nativeReview(h.request); const originalBase = structuredClone(base); const review = h.review();
    const { financialCommitments: _commitments, newlyRequestableRefundCents: _newly, ...account } = review.result.account;
    expect(account).toEqual(base.result.account); expect(review.result.itemDecisions).toEqual(base.result.itemDecisions);
    expect(base).toEqual(originalBase); expect({ request: h.request, workflow: h.workflow, assignments: h.assignments }).toEqual(original);
    expect(h.request.snapshot.moneyEvents).toEqual([]); expect(h.request.snapshot.executionEvents).toEqual([]);
    expect(review.result.actions.every((entry): boolean => Object.hasOwn(entry, "workflow"))).toBe(true);
  });
  it("explicit user questions are never discarded by placeholder substitution", (): void => {
    const h = new LifecycleHarness(); const next = structuredClone(h.request);
    next.snapshot.questions.push({ questionId: "recipient:instructions", question: "Real unresolved recipient exception", reason: "Review the supplied exception",
      resolverRole: "REVIEWER", resolverPartyId: null, neededRecord: null, affectedItemIds: [], affectedActionKinds: [] });
    h.change(next); expect(h.review().result.missingInputs.some((entry): boolean => entry.questionId === "recipient:instructions")).toBe(true);
    h.complete(); expect(completeFlag(h)).toBe(false);
  });
  it("inactive cancelled work is not performed and supplies no fictitious financial facts", (): void => {
    const h = new LifecycleHarness(); const id = h.requestOp("REFUND", 600);
    h.run({ kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId: id, reason: "Cancel prior to any attempt" } });
    expect(requestState(h, id)).toBe("CANCELLED");
    expect(h.review().result.account).toMatchObject({ finalRefundCents: 1600, pendingReservedRefundCents: 0 });
    expect(h.request.snapshot.moneyEvents).toEqual([]); expect(completeFlag(h)).toBe(false);
  });
  it("missing invoices do not infer interim qualification; accepted interim keeps unresolved money policy", (): void => {
    const h = new LifecycleHarness(); const next = structuredClone(h.request);
    Object.assign(next.snapshot.charges[0]!, { costState: "UNKNOWN", vendorCostCents: null, supportedAmountCents: null,
      choiceState: "NOT_DECIDED", chosenAmountCents: null, reviewRequired: true }); h.change(next);
    expect((): void => { h.run({ kind: "PREPARE_STATEMENT", payload: { kind: "INTERIM", supersedesId: null, reason: "Invoice late" } }); }).toThrow();
    h.run({ kind: "SET_INTERIM_QUALIFICATION", payload: { state: "ACCEPTED", evidenceIds: ["ev-repair"], reason: "Separate supported synthetic qualification" } });
    h.run({ kind: "PREPARE_STATEMENT", payload: { kind: "INTERIM", supersedesId: null, reason: "Accepted qualifying facts" } });
    h.perform("STATEMENT_DISPATCH", null);
    const review = h.review(); expect(review.result.missingInputs.some((entry): boolean => entry.questionId === "policy:INTERIM_MONEY")).toBe(true);
    expect(review.result.account.newlyRequestableRefundCents).toBeNull(); expect(completeFlag(h)).toBe(false);
  });
  it("new relevant source versions reopen only affected decision/statement bases", (): void => {
    const h = new LifecycleHarness(); h.prepare(); const statementApproval = h.approve("STATEMENT_DISPATCH", null); const refundApproval = h.approve("REFUND", 600);
    const source = structuredClone(h.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-repair")!);
    const unrelated = structuredClone(h.request); unrelated.snapshot.evidence.push({ ...source, evidenceId: "unrelated-source", externalRecordId: "unrelated-record",
      recordKind: "SERVICE_REQUEST", proposedItemIds: [], sourceVersion: "unrelated-v1", excerpt: "Separate owner scheduling note" }); h.change(unrelated);
    const validity = (id: string): boolean => approvalValidity(h.request, nativeReview(h.request), h.workflow!,
      h.workflow!.approvals.find((entry): boolean => entry.approvalId === id)!, REQUEST_NOW).valid;
    expect(validity(statementApproval)).toBe(true); expect(validity(refundApproval)).toBe(true);
    const updated = structuredClone(h.request); updated.snapshot.evidence.push({ ...source, evidenceId: "changed-repair-source", externalRecordId: "updated-repair",
      sourceVersion: "v2", supersedesEvidenceId: "ev-repair", excerpt: "Revised source needs specific review", associationAccepted: true }); h.change(updated);
    expect(validity(statementApproval)).toBe(false); expect(validity(refundApproval)).toBe(false);
    expect(completeFlag(h)).toBe(false);
  });
  it("pure reducers do not mutate caller inputs even on rejected commands", (): void => {
    const h = new LifecycleHarness(); const original = structuredClone({ request: h.request, workflow: h.workflow, assignments: h.assignments });
    applyLifecycleCommand(h.request, h.assignments, h.workflow, { kind: "PREPARE_STATEMENT", payload: { kind: "FINAL", supersedesId: null, reason: "Detached result" } }, h.ctx());
    expect({ request: h.request, workflow: h.workflow, assignments: h.assignments }).toEqual(original);
    expect((): void => { applyLifecycleCommand(h.request, h.assignments, h.workflow,
      { kind: "DECIDE_APPROVAL", payload: { decision: "APPROVED", intent: { kind: "REFUND", amountCents: 2001,
        dispositionKey: "over-budget", statementId: null, replacesRequestId: null, reversesTransactionId: null } } }, h.ctx()); }).toThrow();
    expect({ request: h.request, workflow: h.workflow, assignments: h.assignments }).toEqual(original);
  });
  it("withdrawal authorization allows the immutable record owner or trusted administrator despite grant expiry", (): void => {
    const h = new LifecycleHarness(); const id = h.requestOp("REFUND", 600); const approvalId = h.workflow!.requests[0]!.approvalIds[0]!;
    const next = structuredClone(h.request); next.snapshot.authorityGrants.forEach((grant): void => { grant.revoked = true; });
    expect((): void => authorizeLifecycleCommand(next, h.workflow, { kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId: id, reason: "Withdraw" } }, h.ctx({ isAdministrator: false }))).not.toThrow();
    expect((): void => authorizeLifecycleCommand(next, h.workflow, { kind: "REVOKE_APPROVAL", payload: { approvalId, reason: "Withdraw" } }, h.ctx({ isAdministrator: false }))).not.toThrow();
    expect((): void => authorizeLifecycleCommand(next, h.workflow, { kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId: id, reason: "Withdraw" } }, h.ctx({ actorId: "trusted-admin", isAdministrator: true }))).not.toThrow();
    expect((): void => authorizeLifecycleCommand(next, h.workflow, { kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId: id, reason: "Withdraw" } }, h.ctx({ actorId: "untrusted", isAdministrator: false }))).toThrow();
  });
  it("all new arithmetic is exact and rejects overflow rather than truncating", (): void => {
    expect(sumCents([Number.MAX_SAFE_INTEGER - 1, 1])).toBe(Number.MAX_SAFE_INTEGER);
    expect((): number => sumCents([Number.MAX_SAFE_INTEGER, 1])).toThrow(/range/);
    expect((): number => sumCents([0.5])).toThrow(/exact/);
    expect((): number => checkedCents(-1n)).toThrow(/range/);
    expect(unreservedCents(Number.MAX_SAFE_INTEGER, Number.MAX_SAFE_INTEGER - 1)).toBe(1);
    expect(unreservedCents(10, 11)).toBe(0);
  });
  it("deadline open and overdue explanations do not alter legal dates", (): void => {
    const h = new LifecycleHarness(); const first = h.review().result.scopeRequirements.requirements.find((entry): boolean => entry.requirementKey === "NC:ordinary-account")!;
    const future = structuredClone(h.request); future.reviewClock = "2027-01-01T00:00:00Z"; h.change(future);
    const overdue = h.review().result.scopeRequirements.requirements.find((entry): boolean => entry.requirementKey === "NC:ordinary-account")!;
    expect(overdue.legalDueDate).toBe(first.legalDueDate); expect(overdue.reason).toContain("Overdue"); expect(overdue.state).not.toBe("FULFILLED");
  });
});
