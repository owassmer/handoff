/** Read-only cash availability must agree with admission; no runtime/persistence operations. */
import { describe, expect, it } from "vitest";
import { canonical_json } from "../domain/codec.js";
import type { AccountResult } from "../domain/types.js";
import { financialAvailability } from "../lifecycle/availability.js";
import { appendWorkflowEvent, nextBusinessInstant } from "../lifecycle/events.js";
import { nativeReview } from "../phase_c/validation.js";
import { hashWorkflowReview, parseWorkflowReview } from "../lifecycle/codec.js";
import { projectNativeFacts, projectRequests } from "../lifecycle/requests.js";
import { reviewWorkflow } from "../lifecycle/review.js";
import type { FinancialOperationKind, WorkflowReviewV2 } from "../lifecycle/types.js";
import { RequestHarness, refundSpec, REQUEST_NOW } from "./phaseDRequestsSupport.js";

function view(h: RequestHarness): WorkflowReviewV2 {
  const projected = projectNativeFacts(h.request, h.workflow);
  return reviewWorkflow(projected, nativeReview(projected), h.workflow, [], REQUEST_NOW);
}
function perform(h: RequestHarness, kind: FinancialOperationKind, amount: number, key: string): string {
  const id = h.admit(refundSpec(amount, key, { kind }));
  h.settle(id, `${key}-settled`, amount);
  return id;
}

function reducedAfterPerformance(scale: number = 1): { h: RequestHarness; application: string; refund: string } {
  const h = new RequestHarness();
  h.request.snapshot.depositBalance.amountCents = 2000 * scale;
  Object.assign(h.request.snapshot.charges[0]!, { vendorCostCents: 400 * scale,
    supportedAmountCents: 400 * scale, chosenAmountCents: 400 * scale });
  const application = perform(h, "DEPOSIT_APPLICATION", 400 * scale, "performed-application");
  const refund = perform(h, "REFUND", 1600 * scale, "performed-refund");
  h.request.snapshot.charges[0]!.chosenAmountCents = 350 * scale;
  return { h, application, refund };
}
function independentApplication(h: RequestHarness, amountCents: number): void {
  const at = nextBusinessInstant(h.workflow);
  h.workflow.businessClock = at; h.request.reviewClock = at;
  const proof = h.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-dates")!;
  h.request.snapshot.evidence.push({ ...proof, evidenceId: "cash-view-independent-proof", recordKind: "SOURCE_EVENT",
    externalRecordId: "cash-view-independent", locator: "fixture:cash-view-independent", occurredAt: at, learnedAt: at,
    excerpt: "Constructed verified application learned after an instruction was admitted." });
  h.request.snapshot.moneyEvents.push({ eventId: "cash-view-independent-event", canonicalTransactionId: "cash-view-independent-tx",
    sourceEventId: "cash-view-independent-source", kind: "DEPOSIT_APPLICATION", status: "SETTLED", amountCents,
    occurredAt: at, learnedAt: at, sourceEvidenceId: "cash-view-independent-proof", requestId: null,
    reversesTransactionId: null, chargeItemId: null });
}

describe("Phase D shared cash availability", (): void => {
  it.each([1, 100])("unfunded correction keeps unpaid 50 * %i but offers no refund until accepted reversal", (scale): void => {
    const { h, application } = reducedAfterPerformance(scale);
    const amount = 50 * scale;
    const approvalId = h.approve(refundSpec(amount, "corrective-refund"));
    const assertUnfunded = (): void => {
      const r = view(h);
      const { financialCommitments: _commitments, newlyRequestableRefundCents, ...baseAccount } = r.result.account;
      expect(baseAccount).toEqual(h.account()); // Native unpaid liability is never rewritten to available cash.
      expect(baseAccount).toMatchObject({ recordedDepositCents: 0, finalRefundCents: amount, finalAccountReady: true });
      expect(newlyRequestableRefundCents).toBe(0);
      expect(r.result.actions.find((entry): boolean => entry.actionKey === "request:refund")!.availability).toBe("BLOCKED");
      expect(r.result.actions.find((entry): boolean => entry.actionKey === "approve:refund")!.availability).toBe("BLOCKED");
      expect((): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } })).toThrow(/verified held deposit cash/);
    };
    assertUnfunded();
    const original = projectRequests(h.workflow).find((entry): boolean => entry.requestId === application)!.canonicalTransactionId!;
    const reversal = h.admit(refundSpec(amount, "corrective-reversal", { kind: "DEPOSIT_APPLICATION_REVERSAL", reversesTransactionId: original }));
    assertUnfunded();
    h.claim(reversal); assertUnfunded();
    h.raw(reversal, "verified-reversal", "SUCCEEDED", amount); assertUnfunded();
    h.ingest("verified-reversal");
    const funded = view(h);
    expect(funded.result.account).toMatchObject({ recordedDepositCents: amount, finalRefundCents: amount,
      newlyRequestableRefundCents: amount });
    expect(funded.result.actions.find((entry): boolean => entry.actionKey === "request:refund")!.availability).toBe("AVAILABLE");
    const refund = String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
    const reserved = view(h);
    expect(reserved.result.account).toMatchObject({ finalRefundCents: amount, pendingReservedRefundCents: amount,
      newlyRequestableRefundCents: 0 });
    expect(reserved.result.actions.find((entry): boolean => entry.actionKey === `claim:${refund}`)!.availability).toBe("AVAILABLE");
    h.claim(refund); // Admission excludes only this existing intent; the NEW-intent readout above does not.
  });

  it.each(["READY", "CLAIMED", "REQUESTED", "ACKNOWLEDGED"] as const)("caps the NEW refund at cash left after an %s application commitment", (state): void => {
    const h = new RequestHarness();
    const application = h.admit(refundSpec(400, "active-application", { kind: "DEPOSIT_APPLICATION" }));
    if (state !== "READY") h.claim(application);
    if (state === "REQUESTED" || state === "ACKNOWLEDGED") h.raw(application, "unaccepted-application", "SUCCEEDED", 400);
    if (state === "ACKNOWLEDGED") appendWorkflowEvent(h.workflow, h.ctx(), application, projectRequests(h.workflow)[0]!.attemptId,
      null, { category: "REQUEST_LIFECYCLE", kind: "ACKNOWLEDGED", payload: { instructionHash: h.workflow.requests[0]!.instructionHash } });
    h.request.snapshot.charges[0]!.chosenAmountCents = 350;
    const r = view(h);
    expect(r.result.account).toMatchObject({ finalRefundCents: 1650, recordedDepositCents: 2000, newlyRequestableRefundCents: 1600 });
    expect(r.result.actions.find((entry): boolean => entry.actionKey === "approve:refund")!.amountCents).toBe(1600);
    const refund = h.admit(refundSpec(1600, "funded-only"));
    expect(view(h).result.account.newlyRequestableRefundCents).toBe(0);
    expect(view(h).result.actions.find((entry): boolean => entry.actionKey === `claim:${refund}`)!.availability).toBe("AVAILABLE");
    h.claim(refund);
  });

  it("counts external and D refunds exactly once alongside D applications, preserving own claim capacity", (): void => {
    const h = new RequestHarness();
    const application = h.admit(refundSpec(400, "application", { kind: "DEPOSIT_APPLICATION" }));
    h.request.snapshot.priorRequests.push({ requestId: "external-refund", actionKind: "REQUEST_REFUND", amountCents: 1000,
      state: "REQUESTED", targetVersionId: "external-target", payloadFingerprint: "external-payload", approvalIds: [], externalReference: null });
    expect(view(h).result.account.newlyRequestableRefundCents).toBe(600);
    const refund = h.admit(refundSpec(600, "refund"));
    const r = view(h);
    expect(r.result.account).toMatchObject({ finalRefundCents: 1600, pendingReservedRefundCents: 1600, newlyRequestableRefundCents: 0 });
    [application, refund].forEach((id): void => {
      expect(r.result.actions.find((entry): boolean => entry.actionKey === `claim:${id}`)!.availability).toBe("AVAILABLE");
      h.claim(id);
    });
  });

  it("blocks a still-exact READY refund claim when newly learned application leaves no held cash", (): void => {
    const h = new RequestHarness();
    h.request.snapshot.charges[0]!.chosenAmountCents = 350;
    perform(h, "DEPOSIT_APPLICATION", 350, "application"); perform(h, "REFUND", 1600, "refund");
    const id = h.admit(refundSpec(50, "last-refund"));
    expect(view(h).result.actions.find((entry): boolean => entry.actionKey === `claim:${id}`)!.availability).toBe("AVAILABLE");
    independentApplication(h, 50);
    const r = view(h);
    expect(r.result.account).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 50,
      pendingReservedRefundCents: 50, newlyRequestableRefundCents: 0 });
    const action = r.result.actions.find((entry): boolean => entry.actionKey === `claim:${id}`)!;
    expect(action.workflow!.approvalDetails.every((entry): boolean => entry.valid)).toBe(true);
    expect(action.availability).toBe("BLOCKED");
    expect(action.prerequisiteIds).toContain("insufficient-current-kind-specific-budget");
    expect((): string => h.claim(id)).toThrow(/verified held deposit cash/);
  });

  it("does not advertise pending return cash and advertises only the accepted amount", (): void => {
    const { h, refund } = reducedAfterPerformance();
    h.raw(refund, "partial-return", "RETURNED", 50);
    expect(view(h).result.account).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 50, newlyRequestableRefundCents: 0 });
    h.ingest("partial-return");
    expect(view(h).result.account).toMatchObject({ recordedDepositCents: 50, finalRefundCents: 100, newlyRequestableRefundCents: 50 });
  });

  it("posting remains actionable at held zero; its availability is not a cash budget", (): void => {
    const { h } = reducedAfterPerformance();
    const approvalId = h.approve(refundSpec(350, "noncash", { kind: "CHARGE_POSTING" }));
    expect(view(h).result.actions.find((entry): boolean => entry.actionKey === "request:charge_posting")!.availability).toBe("AVAILABLE");
    const id = String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
    h.settle(id, "posted", 350);
    expect(view(h).result.account).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 50, newlyRequestableRefundCents: 0, postingDeltaCents: 0 });
  });

  it("unknown application outcome preserves its commitment but never advertises a number as cash permission", (): void => {
    const h = new RequestHarness();
    const id = h.admit(refundSpec(400, "application", { kind: "DEPOSIT_APPLICATION" }));
    const attemptId = h.claim(id);
    h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: id, attemptId, reason: "No accepted result." } });
    const r = view(h);
    expect(r.result.account.newlyRequestableRefundCents).toBeNull();
    expect(r.result.account.financialCommitments.find((entry): boolean => entry.kind === "DEPOSIT_APPLICATION")!.reservedCents).toBe(400);
    expect(r.result.actions.find((entry): boolean => entry.actionKey === "request:refund")!.availability).toBe("BLOCKED");
  });

  it.each(["REFUND", "DEPOSIT_APPLICATION"] as const)("unclassified external pending ledger work fails closed for %s, without inventing cash purpose", (kind): void => {
    const h = new RequestHarness();
    h.request.snapshot.priorRequests.push({ requestId: "external-unclassified", actionKind: "REQUEST_LEDGER_POSTING", amountCents: 100,
      state: "REQUESTED", targetVersionId: "external-target", payloadFingerprint: "external-payload", approvalIds: [], externalReference: null });
    expect(h.account().finalAccountReady).toBe(true);
    const r = view(h);
    expect(r.result.account.newlyRequestableRefundCents).toBeNull();
    expect(r.result.actions.find((entry): boolean => entry.actionKey === `request:${kind.toLowerCase()}`)!.availability).toBe("BLOCKED");
    expect((): string => h.admit(refundSpec(100, "ambiguous-custody", { kind }))).toThrow(/unclassified ledger/);
    // This is a cash-only fail-closed capacity boundary, not a blanket posting gate.
    const posting = h.admit(refundSpec(400, "independent-posting", { kind: "CHARGE_POSTING" }));
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === posting)!.state).toBe("READY");
  });

  it.each(["recordedDepositCents", "pendingReservedRefundCents", "finalRefundCents"] as const)("unknown %s stays null rather than zero", (field): void => {
    const h = new RequestHarness();
    const account = { ...h.account(), [field]: null };
    expect(financialAvailability(account, [], [], "REFUND").availableCents).toBeNull();
  });

  it("validates all native monetary inputs before BigInt and rejects over-range commitment totals", (): void => {
    const h = new RequestHarness();
    const account = h.account();
    const fields: (keyof Pick<AccountResult, "recordedDepositCents" | "finalRefundCents" | "pendingReservedRefundCents">)[] = [
      "recordedDepositCents", "finalRefundCents", "pendingReservedRefundCents"];
    fields.forEach((field): void => {
      [0.5, -1, Number.MAX_SAFE_INTEGER + 1, Number.NaN, Number.POSITIVE_INFINITY].forEach((value): void => {
        expect((): unknown => financialAvailability({ ...account, [field]: value }, [], [], "REFUND")).toThrow(/exact/);
      });
    });
    h.admit(refundSpec(400, "application", { kind: "DEPOSIT_APPLICATION" }));
    const current = projectRequests(h.workflow)[0]!;
    expect((): unknown => financialAvailability(account, [{ ...current, reservedAmountCents: Number.MAX_SAFE_INTEGER },
      { ...current, requestId: "different-request", reservedAmountCents: 1 }], [], "REFUND")).toThrow(/range/);
  });

  it("is exact at MAX_SAFE_INTEGER, floors a cash deficit at zero and rejects a missing own native reserve", (): void => {
    const h = new RequestHarness();
    h.admit(refundSpec(1, "small-application", { kind: "DEPOSIT_APPLICATION" }));
    const current = projectRequests(h.workflow);
    const max = Number.MAX_SAFE_INTEGER;
    const account = { ...h.account(), recordedDepositCents: max, finalRefundCents: max - 1, pendingReservedRefundCents: max - 2 };
    expect(financialAvailability(account, current, [], "REFUND").availableCents).toBe(1);
    const oversizedApplication = [{ ...current[0]!, reservedAmountCents: max }];
    expect(financialAvailability(account, oversizedApplication, [], "REFUND").availableCents).toBe(0);
    const ownRefund = [{ ...current[0]!, kind: "REFUND" as const, reservedAmountCents: max }];
    expect((): unknown => financialAvailability(account, ownRefund, [], "REFUND", ownRefund[0]!.requestId)).toThrow(/own commitment/);
  });
});

describe("Phase D cash availability compatibility", (): void => {
  it("keeps full canonical v2 reviews unchanged for ordinary new, reserved, ready and completed cases", (): void => {
    const h = new RequestHarness();
    // Baselines captured before the shared-availability refactor, not regenerated
    // from new output. A canonical hash covers every field, action and reason.
    const hashes = [hashWorkflowReview(view(h))];
    const refund = h.admit(refundSpec(1600, "ordinary-refund"));
    hashes.push(hashWorkflowReview(view(h)));
    const application = h.admit(refundSpec(400, "ordinary-application", { kind: "DEPOSIT_APPLICATION" }));
    hashes.push(hashWorkflowReview(view(h)));
    h.settle(application, "ordinary-applied", 400);
    h.settle(refund, "ordinary-refunded", 1600);
    perform(h, "CHARGE_POSTING", 400, "ordinary-posting");
    h.prepare();
    const dispatch = h.admit(refundSpec(1, "ordinary-dispatch", { kind: "STATEMENT_DISPATCH", amountCents: null,
      statementId: h.workflow.currentStatementId }));
    h.settle(dispatch, "ordinary-dispatched", null);
    // Pure revision-36 fixture, not a claim to have read any live stored case.
    h.request.snapshot.revision = 36;
    const completed = view(h);
    expect(completed.result.account).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 0,
      newlyRequestableRefundCents: 0, postingDeltaCents: 0, depositApplicationDeltaCents: 0 });
    expect(completed.result.outcomes.simulatedDepositWorkflowComplete).toBe(true);
    expect(parseWorkflowReview(canonical_json(completed))).toEqual(completed);
    hashes.push(hashWorkflowReview(completed));
    expect(hashes).toMatchInlineSnapshot(`
      [
        "3d6b66d96a92e13f7c6c52c48049c424cf965eea774b225e1b2b5d75f6698fda",
        "3063694dd61ca0d000be07684d394ed0bb192e91ee185b360bf071c64eb05122",
        "3c7c5012f8cdb4f48de7a4c515c7b904031ee302316c4b1446537c3c4534588c",
        "df530102686cb2708ec0284c1c4c4fbc061fcc48b52f7c2aee9e1f129bda862f",
      ]
    `);
  });
});
