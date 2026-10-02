/** Cash admission uses native custody, not unpaid liability or anticipated cash-in.
 * Pure constructed fixtures only: no runtime actions, external sends, or permissions changes.
 */
import { describe, expect, it } from "vitest";
import { canonical_json } from "../domain/codec.js";
import type { MoneyEvent } from "../domain/types.js";
import { nativeReview } from "../phase_c/validation.js";
import { approvalValidity, buildIntent } from "../lifecycle/approvals.js";
import { appendWorkflowEvent, nextBusinessInstant } from "../lifecycle/events.js";
import { projectNativeFacts, projectRequests } from "../lifecycle/requests.js";
import type { FinancialOperationKind } from "../lifecycle/types.js";
import { RequestHarness, refundSpec, REQUEST_NOW } from "./phaseDRequestsSupport.js";

const CASH_ERROR = /verified held deposit cash/;

function unchangedOnFailure(h: RequestHarness, operation: () => unknown, message: RegExp): void {
  const before = canonical_json({ request: h.request, workflow: h.workflow });
  expect(operation).toThrow(message);
  expect(canonical_json({ request: h.request, workflow: h.workflow })).toBe(before);
}

/** Native, evidence-backed observation independent of any D request. */
function addNativeMoney(h: RequestHarness, key: string, kind: string, amountCents: number,
  status: string = "SETTLED"): void {
  const at = nextBusinessInstant(h.workflow);
  h.workflow.businessClock = at;
  h.request.reviewClock = at;
  const sourceEvidenceId = `cash-proof-${key}`;
  const proof = h.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-dates")!;
  h.request.snapshot.evidence.push({ ...proof, evidenceId: sourceEvidenceId, recordKind: "SOURCE_EVENT",
    externalRecordId: key, locator: `fixture:cash-${key}`, occurredAt: at, learnedAt: at,
    excerpt: "Constructed independent native money observation for cash commitment tests." });
  const event: MoneyEvent = { eventId: `cash-event-${key}`, canonicalTransactionId: `cash-tx-${key}`,
    sourceEventId: `cash-source-${key}`, kind, status, amountCents, occurredAt: at, learnedAt: at,
    sourceEvidenceId, requestId: null, reversesTransactionId: null, chargeItemId: null };
  h.request.snapshot.moneyEvents.push(event);
}

function addExternalRefund(h: RequestHarness, source: "request" | "pending-event", amountCents: number): void {
  if (source === "pending-event") {
    addNativeMoney(h, "external-refund", "REFUND_INITIATED", amountCents, "PENDING");
    return;
  }
  h.request.snapshot.priorRequests.push({ requestId: "external-refund", actionKind: "REQUEST_REFUND",
    targetVersionId: "external-refund-target", payloadFingerprint: "external-refund-payload", amountCents,
    state: "REQUESTED", approvalIds: [], externalReference: null });
}

function settleMoney(h: RequestHarness, kind: FinancialOperationKind, amount: number, key: string): string {
  const requestId = h.admit(refundSpec(amount, key, { kind }));
  h.settle(requestId, `${key}-settled`, amount);
  return requestId;
}

function spentThenReduced(): { h: RequestHarness; applicationId: string; refundId: string } {
  const h = new RequestHarness();
  const applicationId = settleMoney(h, "DEPOSIT_APPLICATION", 400, "original-application");
  const refundId = settleMoney(h, "REFUND", 1600, "original-refund");
  h.request.snapshot.charges[0]!.chosenAmountCents = 350;
  expect(h.account()).toMatchObject({ finalAccountReady: true, reconciliationState: "RECONCILED",
    recordedDepositCents: 0, finalRefundCents: 50, depositApplicationDeltaCents: -50 });
  return { h, applicationId, refundId };
}

function expectCurrentApproval(h: RequestHarness, requestId: string): void {
  const instruction = h.workflow.requests.find((entry): boolean => entry.requestId === requestId)!;
  const approval = h.workflow.approvals.find((entry): boolean => instruction.approvalIds.includes(entry.approvalId))!;
  const projected = projectNativeFacts(h.request, h.workflow);
  const review = nativeReview(projected);
  expect(approvalValidity(projected, review, h.workflow, approval, REQUEST_NOW).valid).toBe(true);
  expect(buildIntent(projected, review, h.workflow, refundSpec(instruction.intent.amountCents!, instruction.intent.dispositionKey,
    { kind: instruction.kind }))).toEqual(instruction.intent);
}

describe("Phase D verified custody and cross-kind commitments", (): void => {
  it.each(["application-first", "refund-first"] as const)("exact combined commitments fit (%s), including own-reserve claim/send rechecks", (order): void => {
    const h = new RequestHarness();
    const application = refundSpec(400, "application", { kind: "DEPOSIT_APPLICATION" });
    const refund = refundSpec(1600, "refund");
    const first = h.admit(order === "application-first" ? application : refund);
    const second = h.admit(order === "application-first" ? refund : application);
    expect(h.account()).toMatchObject({ recordedDepositCents: 2000, pendingReservedRefundCents: 1600, finalRefundCents: 1600 });
    expect(projectRequests(h.workflow).map((entry): number => entry.reservedAmountCents).sort((a, b): number => a - b)).toEqual([400, 1600]);
    h.claim(first); h.claim(second);
    const firstAmount = order === "application-first" ? 400 : 1600;
    const secondAmount = order === "application-first" ? 1600 : 400;
    h.raw(first, "first-success", "SUCCEEDED", firstAmount);
    h.raw(second, "second-success", "SUCCEEDED", secondAmount);
    expect(h.account().recordedDepositCents).toBe(2000);
    h.ingest("first-success"); h.ingest("second-success");
    expect(h.account()).toMatchObject({ recordedDepositCents: 0, pendingReservedRefundCents: 0,
      finalRefundCents: 0, depositApplicationDeltaCents: 0 });
  });

  it.each(["READY", "CLAIMED", "REQUESTED", "ACKNOWLEDGED"] as const)("does not spend cash promised to an %s application after deductions shrink", (state): void => {
    const h = new RequestHarness();
    const application = h.admit(refundSpec(400, "committed-application", { kind: "DEPOSIT_APPLICATION" }));
    if (state !== "READY") h.claim(application);
    if (state === "REQUESTED" || state === "ACKNOWLEDGED") h.raw(application, "unaccepted-application", "SUCCEEDED", 400);
    if (state === "ACKNOWLEDGED") appendWorkflowEvent(h.workflow, h.ctx(), application,
      projectRequests(h.workflow)[0]!.attemptId, null, { category: "REQUEST_LIFECYCLE", kind: "ACKNOWLEDGED",
        payload: { instructionHash: h.workflow.requests[0]!.instructionHash } });
    h.request.snapshot.charges[0]!.chosenAmountCents = 350;
    expect(h.account()).toMatchObject({ finalAccountReady: true, finalRefundCents: 1650, recordedDepositCents: 2000 });
    const approvalId = h.approve(refundSpec(1650, "unfunded-refund"));
    unchangedOnFailure(h, (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }), CASH_ERROR);
    // The original 400 obligation survives; 1600, not 1650, is cash-available.
    const funded = h.admit(refundSpec(1600, "funded-refund"));
    h.claim(funded);
    h.raw(funded, "funded-refund-success", "SUCCEEDED", 1600);
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === application)?.reservedAmountCents).toBe(400);
  });

  it("unknown application outcomes keep their reserve and retain the prior no-new-commitment guard", (): void => {
    const h = new RequestHarness();
    const id = h.admit(refundSpec(400, "application", { kind: "DEPOSIT_APPLICATION" }));
    const attemptId = h.claim(id);
    h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: id, attemptId, reason: "No accepted outcome." } });
    expect(projectRequests(h.workflow)[0]!.reservedAmountCents).toBe(400);
    unchangedOnFailure(h, (): unknown => h.admit(refundSpec(1600, "not-new-authority")), /verified|unknown/);
  });

  it.each(["request", "pending-event"] as const)("includes external %s refunds alongside D application commitments, without counting D refunds twice", (source): void => {
    const h = new RequestHarness();
    h.admit(refundSpec(400, "application", { kind: "DEPOSIT_APPLICATION" }));
    h.request.snapshot.charges[0]!.chosenAmountCents = 350;
    addExternalRefund(h, source, 1000);
    const refund = h.admit(refundSpec(600, "d-refund"));
    expect(h.account()).toMatchObject({ recordedDepositCents: 2000, finalRefundCents: 1650, pendingReservedRefundCents: 1600 });
    const approvalId = h.approve(refundSpec(1, "one-cent-too-many"));
    unchangedOnFailure(h, (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }), CASH_ERROR);
    h.claim(refund); h.raw(refund, "funded", "SUCCEEDED", 600); h.ingest("funded");
    expect(h.account()).toMatchObject({ recordedDepositCents: 1400, pendingReservedRefundCents: 1000, finalRefundCents: 1050 });
  });

  it("positive application cannot consume cash reserved for refund even when the earlier native guard blocks first", (): void => {
    const h = new RequestHarness();
    addExternalRefund(h, "request", 1600);
    const application = h.admit(refundSpec(400, "exact-application", { kind: "DEPOSIT_APPLICATION" }));
    h.claim(application); h.raw(application, "not-yet-applied", "SUCCEEDED", 400);
    // Raising chosen deductions cannot manufacture extra available cash. Native
    // refund over-reservation now blocks buildIntent before requireBudget runs.
    Object.assign(h.request.snapshot.charges[0]!, { vendorCostCents: 450, supportedAmountCents: 450, chosenAmountCents: 450 });
    expect(h.account()).toMatchObject({ finalAccountReady: false, reconciliationState: "CONFLICT", finalRefundCents: null });
    unchangedOnFailure(h, (): unknown => h.approve(refundSpec(50, "extra-application", { kind: "DEPOSIT_APPLICATION" })), /verified|unknown/);
    expect(projectRequests(h.workflow)[0]!.reservedAmountCents).toBe(400);
  });

  it("held zero / unpaid 50 after a performed 400 application and 1600 refund cannot admit another refund", (): void => {
    const { h } = spentThenReduced();
    // Approvals may express future intent; admission is the custody gate.
    const approvalId = h.approve(refundSpec(50, "additional-refund"));
    unchangedOnFailure(h, (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }), CASH_ERROR);
    expect(h.account().finalRefundCents).toBe(50);
    expect(h.workflow.requests).toHaveLength(2);
  });

  it.each(["claim", "send"] as const)("rechecks held cash at %s with a still-exact approval and preserves the existing reservation", (stage): void => {
    const h = new RequestHarness();
    h.request.snapshot.charges[0]!.chosenAmountCents = 350;
    settleMoney(h, "DEPOSIT_APPLICATION", 350, "application");
    settleMoney(h, "REFUND", 1600, "refund");
    const requestId = h.admit(refundSpec(50, "remaining-refund"));
    if (stage === "send") h.claim(requestId);
    // A verified independent application is learned after admission/claim.
    // Gross entitlement is unchanged, but custody has fallen to zero.
    addNativeMoney(h, "late-extra-application", "DEPOSIT_APPLICATION", 50);
    expect(h.account()).toMatchObject({ finalAccountReady: true, recordedDepositCents: 0, finalRefundCents: 50,
      pendingReservedRefundCents: 50, depositApplicationDeltaCents: -50 });
    expectCurrentApproval(h, requestId);
    unchangedOnFailure(h, (): unknown => stage === "claim" ? h.claim(requestId)
      : h.raw(requestId, "must-not-send", "SUCCEEDED", 50), CASH_ERROR);
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === requestId)).toMatchObject({
      state: stage === "claim" ? "READY" : "CLAIMED", reservedAmountCents: 50 });
  });

  it("only accepted positive application reversal settlement restores cash for the additional refund", (): void => {
    const { h, applicationId } = spentThenReduced();
    const refundApproval = h.approve(refundSpec(50, "additional-refund"));
    const original = projectRequests(h.workflow).find((entry): boolean => entry.requestId === applicationId)!.canonicalTransactionId!;
    const reversal = h.admit(refundSpec(50, "application-reversal", { kind: "DEPOSIT_APPLICATION_REVERSAL", reversesTransactionId: original }));
    const rejectRefund = (): void => unchangedOnFailure(h,
      (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId: refundApproval } }), CASH_ERROR);
    rejectRefund();
    h.claim(reversal); rejectRefund();
    h.raw(reversal, "reversed", "SUCCEEDED", 50); rejectRefund();
    expect(h.account()).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 50, depositApplicationDeltaCents: -50 });
    expect(h.request.snapshot.moneyEvents).toHaveLength(2);
    h.ingest("reversed");
    expect(h.account()).toMatchObject({ recordedDepositCents: 50, finalRefundCents: 50, depositApplicationDeltaCents: 0 });
    const refundId = String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId: refundApproval } }).summary.requestId);
    h.settle(refundId, "additional-refund-paid", 50);
    expect(h.account()).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 0,
      existingDepositApplicationsCents: 350, priorNetRefundsCents: 1650 });
  });

  it("a pending refund return is not cash; accepted return proof restores only its verified amount", (): void => {
    const { h, refundId } = spentThenReduced();
    const approvalId = h.approve(refundSpec(50, "extra-refund"));
    h.raw(refundId, "returned-fifty", "RETURNED", 50);
    expect(h.account()).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 50 });
    unchangedOnFailure(h, (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }), CASH_ERROR);
    h.ingest("returned-fifty");
    expect(h.account()).toMatchObject({ recordedDepositCents: 50, finalRefundCents: 100 });
    const id = String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
    h.settle(id, "fifty-paid", 50);
    expect(h.account()).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 50 });
    const nextApproval = h.approve(refundSpec(50, "still-unfunded"));
    unchangedOnFailure(h, (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId: nextApproval } }), CASH_ERROR);
  });

  it("posting remains noncash when held cash is zero", (): void => {
    const { h } = spentThenReduced();
    settleMoney(h, "CHARGE_POSTING", 350, "noncash-posting");
    expect(h.account()).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 50, postingDeltaCents: 0 });
  });

  it("posting reversal is not blocked by zero held cash and still uses kind-specific principal", (): void => {
    const h = new RequestHarness();
    const posting = settleMoney(h, "CHARGE_POSTING", 400, "original-posting");
    settleMoney(h, "DEPOSIT_APPLICATION", 400, "application");
    settleMoney(h, "REFUND", 1600, "refund");
    h.request.snapshot.charges[0]!.chosenAmountCents = 350;
    const original = projectRequests(h.workflow).find((entry): boolean => entry.requestId === posting)!.canonicalTransactionId!;
    const spec = refundSpec(50, "noncash-reversal", { kind: "CHARGE_POSTING_REVERSAL", reversesTransactionId: original });
    const reversal = h.admit(spec);
    const otherApproval = h.approve({ ...spec, dispositionKey: "double-reversal" });
    unchangedOnFailure(h, (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId: otherApproval } }), /kind-specific/);
    h.settle(reversal, "posting-reversed", 50);
    expect(h.account()).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 50, postingDeltaCents: 0 });
  });

  it.each(["REFUND", "DEPOSIT_APPLICATION"] as const)("unknown held cash is not zero or new %s authority", (kind): void => {
    const h = new RequestHarness();
    const spec = refundSpec(400, "known-before", { kind });
    const approvalId = h.approve(spec);
    h.request.snapshot.depositBalance.amountCents = null;
    expect(h.account()).toMatchObject({ recordedDepositCents: null, pendingReservedRefundCents: null, finalRefundCents: null });
    unchangedOnFailure(h, (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }), /approval|verified|unknown/);
    unchangedOnFailure(h, (): unknown => h.approve(spec), /verified|unknown/);
  });

  it.each(["claim", "send"] as const)("unknown native custody blocks %s without releasing its reserve", (stage): void => {
    const h = new RequestHarness();
    const id = h.admit(refundSpec(1600, "refund"));
    if (stage === "send") h.claim(id);
    h.request.snapshot.depositBalance.amountCents = null;
    expect(h.account().recordedDepositCents).toBeNull();
    unchangedOnFailure(h, (): unknown => stage === "claim" ? h.claim(id) : h.raw(id, "not-sent", "SUCCEEDED", 1600), /approval|verified|unknown/);
    expect(projectRequests(h.workflow)[0]!.reservedAmountCents).toBe(1600);
  });

  it("zero refund remains no instruction rather than a zero-valued cash operation", (): void => {
    const h = new RequestHarness();
    h.request.snapshot.depositBalance.amountCents = 400;
    expect(h.account()).toMatchObject({ recordedDepositCents: 400, finalRefundCents: 0 });
    unchangedOnFailure(h, (): unknown => h.admit(refundSpec(0, "zero-refund")), /positive/);
    expect(h.workflow.requests).toHaveLength(0);
    settleMoney(h, "DEPOSIT_APPLICATION", 400, "only-application");
    expect(h.account()).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 0 });
    expect(h.workflow.requests.every((entry): boolean => entry.kind !== "REFUND")).toBe(true);
  });

  it("exact combined commitments at the native safe-integer boundary are neither rounded nor double counted", (): void => {
    const h = new RequestHarness();
    const max = Number.MAX_SAFE_INTEGER;
    h.request.snapshot.depositBalance.amountCents = max;
    h.request.snapshot.charges[0]!.chosenAmountCents = 1;
    h.request.snapshot.authorityGrants.forEach((grant): void => { grant.amountLimitCents = max; });
    const application = h.admit(refundSpec(1, "one-cent-application", { kind: "DEPOSIT_APPLICATION" }));
    const refund = h.admit(refundSpec(max - 1, "large-refund"));
    h.claim(application); h.claim(refund);
    h.raw(application, "one-cent", "SUCCEEDED", 1);
    h.raw(refund, "large", "SUCCEEDED", max - 1);
    expect(h.account()).toMatchObject({ recordedDepositCents: max, pendingReservedRefundCents: max - 1 });
  });

  it("large cross-kind commitments cannot overflow or round into available cash", (): void => {
    const h = new RequestHarness();
    const max = Number.MAX_SAFE_INTEGER;
    h.request.snapshot.depositBalance.amountCents = max;
    Object.assign(h.request.snapshot.charges[0]!, { vendorCostCents: max, supportedAmountCents: max, chosenAmountCents: max });
    h.request.snapshot.authorityGrants.forEach((grant): void => { grant.amountLimitCents = max; });
    const application = h.admit(refundSpec(max, "large-application", { kind: "DEPOSIT_APPLICATION" }));
    h.claim(application);
    h.request.snapshot.charges[0]!.chosenAmountCents = 1;
    const approvalId = h.approve(refundSpec(max - 1, "cannot-reuse-promised-cash"));
    unchangedOnFailure(h, (): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }), CASH_ERROR);
    expect(projectRequests(h.workflow)[0]!.reservedAmountCents).toBe(max);
  });
});
