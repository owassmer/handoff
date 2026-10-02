import { describe, expect, it } from "vitest";
import { canonical_json } from "../domain/codec.js";
import { compare_timestamps } from "../domain/datetime.js";
import { nativeReview } from "../phase_c/validation.js";
import { parseWorkflowState, serializeWorkflowState } from "../lifecycle/codec.js";
import { applyRequestCommand, projectNativeFacts, projectRequests, reconcileRequestsAfterChange } from "../lifecycle/requests.js";
import { canonicalTransactionIdFor } from "../lifecycle/ids.js";
import { revokeApproval } from "../lifecycle/approvals.js";
import { remainingCanonicalPrincipal, verifiedNativeTransactions } from "../lifecycle/simulator.js";
import { versionedRoute } from "../lifecycle/materiality.js";
import { RequestHarness, refundSpec, requestContext, requestFixture, REQUEST_NOW } from "./phaseDRequestsSupport.js";

describe("Phase D pure request admission and immutable current facts", (): void => {
  it("fixed 2000 held / 400 deductions yields 1600 unpaid; a 600 reserve leaves 1000 newly requestable", (): void => {
    const h = new RequestHarness();
    expect(h.account().recordedDepositCents).toBe(2000);
    expect(h.account().totalDeductionsCents).toBe(400);
    expect(h.account().finalRefundCents).toBe(1600);
    h.admit();
    expect(h.account().finalRefundCents).toBe(1600);
    expect(h.account().pendingReservedRefundCents).toBe(600);
    expect(h.account().finalRefundCents! - h.account().pendingReservedRefundCents!).toBe(1000);
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
    expect(h.request.snapshot.revision).toBe(1);
  });
  it("different commands and approvals for one instruction reserve only once, before budget checks", (): void => {
    const h = new RequestHarness(); const id = h.admit(refundSpec(1600));
    const secondApproval = h.approve(refundSpec(1600));
    const result = h.run({ kind: "REQUEST_OPERATION", payload: { approvalId: secondApproval } });
    expect(result.summary).toEqual({ requestId: id, replayed: true });
    expect(h.workflow.requests).toHaveLength(1);
    expect(h.workflow.events.filter((event): boolean => event.kind === "REQUEST_CREATED")).toHaveLength(1);
    expect(h.account().pendingReservedRefundCents).toBe(1600);
  });
  it("admits partial instructions with distinct disposition identities, not overcommit", (): void => {
    const h = new RequestHarness(); h.admit(); h.admit(refundSpec(1000, "installment-2"));
    expect(h.account().pendingReservedRefundCents).toBe(1600);
    const approvalId = h.approve(refundSpec(1, "installment-3"));
    const before = canonical_json({ request: h.request, workflow: h.workflow });
    expect((): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } })).toThrow(/liability less/);
    expect(canonical_json({ request: h.request, workflow: h.workflow })).toBe(before);
  });
  it("projects one fact per D request without history, preserves external requests and evidence", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.claim(id);
    const current = h.request.snapshot.priorRequests[0]!;
    h.request.snapshot.priorRequests.push({ ...current, state: "READY" });
    h.request.snapshot.priorRequests.push({ ...current, requestId: "external-fact", actionKind: "REQUEST_STATEMENT_DISPATCH", amountCents: null });
    const before = canonical_json({ request: h.request, workflow: h.workflow });
    const result = projectNativeFacts(h.request, h.workflow);
    expect(result.snapshot.priorRequests.filter((fact): boolean => fact.requestId === id)).toHaveLength(1);
    expect(result.snapshot.priorRequests.find((fact): boolean => fact.requestId === id)?.state).toBe("CLAIMED");
    expect(result.snapshot.priorRequests.some((fact): boolean => fact.requestId === "external-fact")).toBe(true);
    expect(result.snapshot.evidence).toEqual(h.request.snapshot.evidence);
    expect(canonical_json({ request: h.request, workflow: h.workflow })).toBe(before);
  });
  it.each([0, -1, 0.5, Number.MAX_SAFE_INTEGER + 1])("rejects nonpositive or inexact amount %s", (amount): void => {
    const h = new RequestHarness(); expect((): unknown => h.approve(refundSpec(amount))).toThrow();
  });
  it("does not turn unknown native funds into zero", (): void => {
    const h = new RequestHarness(); h.request.snapshot.depositBalance.amountCents = null;
    expect(h.account().finalRefundCents).toBeNull();
    expect((): unknown => h.approve()).toThrow(/verified|unknown/);
  });
  it("checks actual-time authority: trusted administrator does not bypass an expired accountant", (): void => {
    const h = new RequestHarness(); const approvalId = h.approve();
    h.request.snapshot.authorityGrants.find((grant): boolean => grant.partyId === "demo-accountant")!.effectiveUntil = REQUEST_NOW;
    expect((): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } })).toThrow(/current accountant authority/);
  });
  it("does not grant authority from a future demo clock", (): void => {
    const h = new RequestHarness(); const approvalId = h.approve();
    h.request.snapshot.authorityGrants.find((grant): boolean => grant.partyId === "demo-accountant")!.effectiveFrom = "2026-09-19T00:00:00Z";
    h.workflow.businessClock = "2026-10-01T12:00:00Z";
    expect((): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } })).toThrow(/current accountant authority/);
  });
  it("rejects new stale approval after chosen deduction changes", (): void => {
    const h = new RequestHarness(); const approvalId = h.approve(); h.request.snapshot.charges[0]!.chosenAmountCents = 300;
    expect((): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } })).toThrow(/current approval|stale/);
  });
  it("cannot claim or send after refund route changed", (): void => {
    const h = new RequestHarness(); const id = h.admit();
    h.workflow.refundInstructions = versionedRoute(h.workflow, "REFUND", { ...h.workflow.refundInstructions, routeReference: "demo-new-route" });
    expect((): unknown => h.claim(id)).toThrow(/current approval|stale/);
  });
  it("READY cancellation releases reservation, but CLAIMED is already potentially attempted", (): void => {
    const h = new RequestHarness(); const first = h.admit();
    h.run({ kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId: first, reason: "Do not send." } });
    expect(h.workflow.events.at(-1)?.kind).toBe("CANCELLED_BEFORE_ATTEMPT");
    expect(projectRequests(h.workflow)[0]!.state).toBe("CANCELLED");
    expect(h.account().pendingReservedRefundCents).toBe(0);
    const second = h.admit(refundSpec(600, "second")); h.claim(second);
    expect((): unknown => h.run({ kind: "CANCEL_UNATTEMPTED_REQUEST", payload: { requestId: second, reason: "Too late." } })).toThrow(/unattempted/);
    expect(h.account().pendingReservedRefundCents).toBe(600);
  });
  it("CLAIM replay never invents another attempt", (): void => {
    const h = new RequestHarness(); const id = h.admit(); const attempt = h.claim(id);
    expect(h.claim(id)).toBe(attempt);
    expect(h.workflow.events.filter((event): boolean => event.kind === "ATTEMPT_CLAIMED")).toHaveLength(1);
  });
  it("stale reconciliation is READY-only, never releases attempted or unknown commitments", (): void => {
    const h = new RequestHarness(); const ready = h.admit(); const claimed = h.admit(refundSpec(500, "second")); h.claim(claimed);
    h.request.snapshot.charges[0]!.chosenAmountCents = 300;
    const result = reconcileRequestsAfterChange(h.request, h.workflow, requestContext("reconcile"));
    expect(projectRequests(result.workflow).find((entry): boolean => entry.requestId === claimed)?.state).toBe("CLAIMED");
    expect(projectRequests(result.workflow).find((entry): boolean => entry.requestId === ready)?.state).toBe("SUPERSEDED");
    expect(result.workflow.events.at(-1)).toMatchObject({ requestId: ready, kind: "SUPERSEDED_BEFORE_ATTEMPT",
      attemptId: null, payload: { replacementRequestId: null } });
    expect(result.workflow.events.some((event): boolean => event.kind === "CANCELLED_BEFORE_ATTEMPT")).toBe(false);
    expect(result.workflow.requests).toEqual(h.workflow.requests);
    expect(result.workflow.approvals).toEqual(h.workflow.approvals);
    expect(result.request.snapshot.priorRequests.find((entry): boolean => entry.requestId === ready)?.state).toBe("SUPERSEDED");
    expect(nativeReview(result.request).result.account.pendingReservedRefundCents).toBe(500);
    expect(projectRequests(h.workflow).find((entry): boolean => entry.requestId === ready)?.state).toBe("READY");
    const replay = reconcileRequestsAfterChange(result.request, result.workflow, requestContext("reconcile-again"));
    expect(replay.workflow.events).toEqual(result.workflow.events);
  });
  it.each(["CLAIMED", "REQUESTED", "OUTCOME_UNKNOWN", "SUCCEEDED"] as const)(
    "known changed basis never supersedes %s or releases its unresolved commitment", (state): void => {
      const h = new RequestHarness(); const id = h.admit(); const attemptId = h.claim(id);
      if (state !== "CLAIMED") h.raw(id, "attempt-result");
      if (state === "SUCCEEDED") h.ingest("attempt-result");
      if (state === "OUTCOME_UNKNOWN") h.run({ kind: "RECORD_OUTCOME_UNKNOWN",
        payload: { requestId: id, attemptId, reason: "No confirmed outcome." } });
      h.request.snapshot.charges[0]!.chosenAmountCents = 300;
      const result = reconcileRequestsAfterChange(h.request, h.workflow, requestContext("attempted-reconcile"));
      expect(result.workflow.events).toEqual(h.workflow.events);
      expect(projectRequests(result.workflow)[0]).toMatchObject({ state, attemptId,
        reservedAmountCents: state === "SUCCEEDED" ? 0 : 600 });
    });
  it("explicit approval revocation supersedes only its READY target without a replacement", (): void => {
    const h = new RequestHarness(); const first = h.admit(); const second = h.admit(refundSpec(500, "second"));
    const approvalId = h.workflow.requests[0]!.approvalIds[0]!;
    h.workflow.approvals.push(revokeApproval(h.request, h.workflow, approvalId, requestContext("revoke-first")));
    h.workflow = parseWorkflowState(serializeWorkflowState(h.workflow));
    const result = reconcileRequestsAfterChange(h.request, h.workflow, requestContext("reconcile-revocation"));
    expect(projectRequests(result.workflow).find((entry): boolean => entry.requestId === first)?.state).toBe("SUPERSEDED");
    expect(projectRequests(result.workflow).find((entry): boolean => entry.requestId === second)?.state).toBe("READY");
    expect(result.workflow.events.at(-1)).toMatchObject({ requestId: first, kind: "SUPERSEDED_BEFORE_ATTEMPT",
      payload: { replacementRequestId: null } });
    expect(result.workflow.requests).toEqual(h.workflow.requests);
    expect(result.workflow.approvals).toEqual(h.workflow.approvals);
    expect(nativeReview(result.request).result.account.pendingReservedRefundCents).toBe(500);
  });
  it.each(["REFUND", "STATEMENT_DISPATCH"] as const)("reconciles %s own-route change, not the other channel", (kind): void => {
    const h = new RequestHarness(); const statementId = kind === "STATEMENT_DISPATCH" ? h.prepare() : null;
    const id = h.admit(refundSpec(600, "own-channel", { kind, statementId,
      amountCents: kind === "STATEMENT_DISPATCH" ? null : 600 }));
    const otherChannel = kind === "REFUND" ? "STATEMENT" : "REFUND";
    const otherKey = kind === "REFUND" ? "statementInstructions" : "refundInstructions";
    h.workflow[otherKey] = versionedRoute(h.workflow, otherChannel,
      { ...h.workflow[otherKey], routeReference: "demo-other-channel-changed" });
    const unchanged = reconcileRequestsAfterChange(h.request, h.workflow, requestContext("other-route"));
    expect(unchanged.workflow.events).toEqual(h.workflow.events);
    const ownKey = kind === "REFUND" ? "refundInstructions" : "statementInstructions";
    h.workflow[ownKey] = versionedRoute(h.workflow, kind === "REFUND" ? "REFUND" : "STATEMENT",
      { ...h.workflow[ownKey], routeReference: "demo-own-channel-changed" });
    const result = reconcileRequestsAfterChange(h.request, h.workflow, requestContext("own-route"));
    expect(projectRequests(result.workflow)[0]).toMatchObject({ requestId: id, state: "SUPERSEDED", reservedAmountCents: 0 });
    expect(result.workflow.events.at(-1)).toMatchObject({ kind: "SUPERSEDED_BEFORE_ATTEMPT", payload: { replacementRequestId: null } });
    expect(result.workflow.requests).toEqual(h.workflow.requests);
    expect(result.workflow.approvals).toEqual(h.workflow.approvals);
  });
});

describe("Phase D separate simulator observation and trusted result ingestion", (): void => {
  it("raw source is not accepted proof and does not settle or release reservation", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.claim(id); h.raw(id, "source-1");
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
    expect(h.request.snapshot.evidence.some((entry): boolean => entry.evidenceId.startsWith("dc-simulator-proof:"))).toBe(false);
    expect(h.account().pendingReservedRefundCents).toBe(600);
    expect(projectRequests(h.workflow)[0]!.state).toBe("REQUESTED");
    h.ingest("source-1");
    expect(h.request.snapshot.moneyEvents).toHaveLength(1);
    expect(h.account().priorNetRefundsCents).toBe(600);
    expect(h.account().finalRefundCents).toBe(1000);
    expect(h.account().pendingReservedRefundCents).toBe(0);
  });
  it("lost response raw success -> unknown -> late ingestion retains money liability correctly", (): void => {
    const h = new RequestHarness(); const id = h.admit(); const attemptId = h.claim(id); h.raw(id, "lost-response");
    const approvalId = h.approve(refundSpec(200, "next"));
    h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: id, attemptId, reason: "Transport acknowledgement was lost." } });
    // Native account fails closed; the independently projected commitment remains.
    expect(h.account().pendingReservedRefundCents).toBeNull();
    expect(h.account().finalRefundCents).toBeNull();
    expect(projectRequests(h.workflow)[0]!.reservedAmountCents).toBe(600);
    expect(projectRequests(h.workflow)[0]!.state).toBe("OUTCOME_UNKNOWN");
    expect((): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } })).toThrow(/unknown|verified/);
    h.ingest("lost-response");
    expect(projectRequests(h.workflow)[0]!.state).toBe("SUCCEEDED");
    expect(h.account().priorNetRefundsCents).toBe(600);
    expect(h.account().finalRefundCents).toBe(1000);
  });
  it("CLAIMED may be marked unknown without inventing a failure or send", (): void => {
    const h = new RequestHarness(); const id = h.admit(); const attemptId = h.claim(id);
    h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: id, attemptId, reason: "Worker crashed after claim." } });
    expect(h.workflow.events.some((event): boolean => event.kind === "REQUESTED")).toBe(false);
    expect(h.account().pendingReservedRefundCents).toBeNull();
    expect(projectRequests(h.workflow)[0]!.reservedAmountCents).toBe(600);
    expect((): unknown => h.admit(refundSpec(600, "replacement", { replacesRequestId: id }))).toThrow();
  });
  it("same source replay with null occurrence retains original time, independent of actor and command", (): void => {
    const h = new RequestHarness(); const id = h.admit(); const attemptId = h.claim(id); h.raw(id, "source-1");
    const before = canonical_json(h.workflow); const events = h.workflow.events.length;
    h.run({ kind: "GENERATE_SIMULATED_RESULT", payload: { requestId: id, attemptId, sourceEventId: "source-1",
      outcome: "SUCCEEDED", amountCents: 600, occurredAt: null } }, { actorId: "another-admin" });
    expect(h.workflow.events).toHaveLength(events);
    expect(canonical_json(h.workflow)).toBe(before);
    h.ingest("source-1"); const count = h.workflow.events.length;
    h.ingest("source-1", { actorId: "another-recorder" });
    expect(h.workflow.events).toHaveLength(count);
    expect(h.request.snapshot.moneyEvents).toHaveLength(1);
  });
  it.each(["amount", "outcome", "time"])('conflicting same source %s is rejected, not last-row-wins', (change): void => {
    const h = new RequestHarness(); const id = h.admit(); const attemptId = h.claim(id); h.raw(id, "source-1");
    const before = canonical_json(h.workflow);
    expect((): unknown => h.run({ kind: "GENERATE_SIMULATED_RESULT", payload: { requestId: id, attemptId,
      sourceEventId: "source-1", outcome: change === "outcome" ? "FAILED" : "SUCCEEDED",
      amountCents: change === "amount" ? 500 : 600, occurredAt: change === "time" ? "2026-09-17T12:00:00Z" : null } })).toThrow();
    expect(canonical_json(h.workflow)).toBe(before);
  });
  it("different source delivery of the same canonical success corroborates without a second MoneyEvent", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id);
    h.raw(id, "second-delivery"); const result = h.ingest("second-delivery");
    expect(result.summary.economicDuplicate).toBe(true);
    expect(h.request.snapshot.moneyEvents).toHaveLength(1);
    expect(h.workflow.events.filter((event): boolean => event.kind === "RESULT_ACCEPTED")).toHaveLength(2);
  });
  it("late fact generation/ingestion needs no current approval after send", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.claim(id); h.raw(id, "first-delivery");
    h.request.snapshot.charges[0]!.chosenAmountCents = 200;
    h.request.snapshot.authorityGrants.forEach((grant): void => { grant.revoked = true; });
    h.raw(id, "late-delivery"); h.ingest("late-delivery", { actorId: "trusted-recorder", isAdministrator: false });
    expect(h.account().priorNetRefundsCents).toBe(600);
    expect(h.account().finalRefundCents).toBe(1200);
  });
  it("actual administrator controls simulation but cannot bypass first-send financial authority", (): void => {
    const h = new RequestHarness(); const id = h.admit(); const attemptId = h.claim(id);
    expect((): unknown => h.run({ kind: "GENERATE_SIMULATED_RESULT", payload: { requestId: id, attemptId, sourceEventId: "no-admin",
      outcome: "SUCCEEDED", amountCents: 600, occurredAt: null } }, { isAdministrator: false })).toThrow(/administrator/);
    h.request.snapshot.authorityGrants.find((grant): boolean => grant.partyId === "demo-accountant")!.revoked = true;
    expect((): unknown => h.raw(id, "admin-no-authority")).toThrow(/current accountant authority/);
  });
  it("failure after settlement is retained raw for reconciliation with no contradictory native write", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id); h.raw(id, "contradictory-failure", "FAILED");
    expect(projectRequests(h.workflow)[0]!.reconciliationRequired).toBe(true);
    expect((): unknown => h.ingest("contradictory-failure")).toThrow(/contradict/);
    expect(h.request.snapshot.moneyEvents).toHaveLength(1);
    expect(projectRequests(h.workflow)[0]!.state).toBe("SUCCEEDED");
  });
  it("definitive failed result releases reservation but replacement gets a fresh payment identity", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.claim(id); h.raw(id, "failed", "FAILED"); h.ingest("failed");
    expect(projectRequests(h.workflow)[0]!.state).toBe("FAILED"); expect(h.account().pendingReservedRefundCents).toBe(0);
    const replacement = h.admit(refundSpec(600, "replacement", { replacesRequestId: id }));
    expect(replacement).not.toBe(id);
    expect(canonicalTransactionIdFor(h.workflow, replacement)).not.toBe(canonicalTransactionIdFor(h.workflow, id));
    h.settle(replacement, "replacement-success"); expect(h.account().priorNetRefundsCents).toBe(600);
  });
  it("manual C money linked to a D request blocks claim and cannot trigger duplicate sending", (): void => {
    const h = new RequestHarness(); const id = h.admit();
    h.request.snapshot.moneyEvents.push({ eventId: "manual", canonicalTransactionId: "manual-tx", sourceEventId: "manual-source",
      kind: "REFUND_SETTLED", status: "SETTLED", amountCents: 600, occurredAt: h.workflow.businessClock,
      learnedAt: h.workflow.businessClock, sourceEvidenceId: "ev-balance", requestId: id, reversesTransactionId: null, chargeItemId: null });
    expect((): unknown => h.claim(id)).toThrow(/manual accounting fact/);
    expect(h.workflow.events).toHaveLength(1);
  });
  it("rejects forged economic identity on ingestion, while keeping original unaccepted raw", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.claim(id); h.raw(id, "forged");
    const raw = h.workflow.events.find((event): boolean => event.kind === "RAW_SIMULATED_RESULT")!;
    if (raw.kind !== "RAW_SIMULATED_RESULT") throw new Error("Test raw missing");
    raw.payload.canonicalTransactionId = "injected-arbitrary-id";
    expect((): unknown => h.ingest("forged")).toThrow(/economic identity/);
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
  });
  it("every returned state round trips codec with preceding claims and contiguous sequences", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id);
    expect(parseWorkflowState(serializeWorkflowState(h.workflow))).toEqual(h.workflow);
    expect(h.workflow.events.map((event): number => event.sequence)).toEqual([1, 2, 3, 4, 5]);
    expect(h.workflow.events.every((event): boolean => compare_timestamps(event.recordedAt, REQUEST_NOW) === 0)).toBe(true);
    expect(h.workflow.events.every((event): boolean => compare_timestamps(event.occurredAt, event.learnedAt) <= 0)).toBe(true);
    expect(h.request.reviewClock).toBe(h.workflow.businessClock);
  });
});

describe("Phase D returns, ledger kinds and statement separation", (): void => {
  it.each([200, 600])("%s returned reopens liability without falsely failing successful request", (amount): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id); h.raw(id, "return-1", "RETURNED", amount); h.ingest("return-1");
    expect(projectRequests(h.workflow)[0]!.state).toBe("SUCCEEDED");
    expect(h.account().reconciliationState).toBe("RECONCILED");
    expect(h.account().priorNetRefundsCents).toBe(600 - amount);
    expect(h.account().finalRefundCents).toBe(1000 + amount);
    expect(h.request.snapshot.moneyEvents[1]!.requestId).toBe(id);
    expect(h.request.snapshot.moneyEvents[1]!.reversesTransactionId).toBe(h.request.snapshot.moneyEvents[0]!.canonicalTransactionId);
    const replacement = h.admit(refundSpec(amount, "replacement", { replacesRequestId: id }));
    h.settle(replacement, "replacement-settlement", amount);
    expect(h.account().priorNetRefundsCents).toBe(600);
    expect(h.account().finalRefundCents).toBe(1000);
  });
  it("multiple partial returns have distinct canonical IDs and never exceed settled principal", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id);
    h.raw(id, "return-a", "RETURNED", 200); h.ingest("return-a");
    h.raw(id, "return-b", "RETURNED", 150); h.ingest("return-b");
    expect(new Set(h.request.snapshot.moneyEvents.map((event): string => event.canonicalTransactionId)).size).toBe(3);
    expect(h.account().priorNetRefundsCents).toBe(250); expect(h.account().finalRefundCents).toBe(1350);
    h.raw(id, "return-too-large", "RETURNED", 300);
    expect((): unknown => h.ingest("return-too-large")).toThrow(/remaining settled principal/);
    expect(h.request.snapshot.moneyEvents).toHaveLength(3);
  });
  it("return redelivery with same explicit occurrence is one economic return", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id); h.raw(id, "return-a", "RETURNED", 200); h.ingest("return-a");
    const occurred = h.request.snapshot.moneyEvents[1]!.occurredAt;
    h.raw(id, "return-delivery-b", "RETURNED", 200, occurred); h.ingest("return-delivery-b");
    expect(h.request.snapshot.moneyEvents).toHaveLength(2); expect(h.account().priorNetRefundsCents).toBe(400);
  });
  it("raw return may arrive before settlement acceptance but ingestion waits for evidence", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.claim(id); h.raw(id, "settlement"); h.raw(id, "return", "RETURNED", 200);
    expect((): unknown => h.ingest("return")).toThrow(/prior settlement/);
    h.ingest("settlement"); h.ingest("return"); expect(h.account().priorNetRefundsCents).toBe(400);
  });
  it("opposite economic states cannot share an allocated occurrence timestamp", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id); h.raw(id, "return", "RETURNED", 600); h.ingest("return");
    expect(compare_timestamps(h.request.snapshot.moneyEvents[0]!.occurredAt, h.request.snapshot.moneyEvents[1]!.occurredAt)).toBe(-1);
  });
  it("return before or exactly at settlement requires reconciliation, no native effect", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id);
    h.raw(id, "bad-return", "RETURNED", 100, h.request.snapshot.moneyEvents[0]!.occurredAt);
    expect((): unknown => h.ingest("bad-return")).toThrow(/strictly before/); expect(h.request.snapshot.moneyEvents).toHaveLength(1);
  });
  it("posting and application use independent native deltas and outstanding commitments", (): void => {
    const h = new RequestHarness();
    const posting = h.admit(refundSpec(250, "post", { kind: "CHARGE_POSTING" }));
    const approval = h.approve(refundSpec(200, "overpost", { kind: "CHARGE_POSTING" }));
    expect((): unknown => h.run({ kind: "REQUEST_OPERATION", payload: { approvalId: approval } })).toThrow(/kind-specific/);
    const application = h.admit(refundSpec(400, "application", { kind: "DEPOSIT_APPLICATION" }));
    h.settle(posting, "posted", 250);
    expect(h.account().existingNetPostingCents).toBe(250); expect(h.account().existingDepositApplicationsCents).toBe(0);
    expect(h.account().recordedDepositCents).toBe(2000); expect(h.account().finalRefundCents).toBe(1600);
    h.settle(application, "applied", 400);
    expect(h.account().existingDepositApplicationsCents).toBe(400); expect(h.account().recordedDepositCents).toBe(1600);
    expect(h.account().finalRefundCents).toBe(1600);
  });
  it.each(["CHARGE_POSTING", "DEPOSIT_APPLICATION"] as const)("%s reversal preserves original native request identity but workflow performing request is new", (kind): void => {
    const h = new RequestHarness(); const id = h.admit(refundSpec(400, "original", { kind })); h.settle(id, "original-success", 400);
    const original = h.request.snapshot.moneyEvents[0]!.canonicalTransactionId;
    h.request.snapshot.charges[0]!.chosenAmountCents = 100;
    const reversalKind = kind === "CHARGE_POSTING" ? "CHARGE_POSTING_REVERSAL" : "DEPOSIT_APPLICATION_REVERSAL";
    const reverseId = h.admit(refundSpec(300, "reversal", { kind: reversalKind, reversesTransactionId: original }));
    h.settle(reverseId, "reversed", 300);
    expect(h.request.snapshot.moneyEvents[1]!.requestId).toBe(id);
    expect(h.request.snapshot.moneyEvents[1]!.reversesTransactionId).toBe(original);
    expect(h.workflow.events.find((event): boolean => event.kind === "RESULT_ACCEPTED" && event.sourceEventId === "reversed")?.requestId).toBe(reverseId);
    expect(h.account().reconciliationState).toBe("RECONCILED");
    expect(remainingCanonicalPrincipal(verifiedNativeTransactions(h.request), original)).toBe(100);
    expect(kind === "CHARGE_POSTING" ? h.account().existingNetPostingCents : h.account().existingDepositApplicationsCents).toBe(100);
  });
  it("statement dispatch carries null amount and proof but never settles money", (): void => {
    const h = new RequestHarness(); const statementId = h.prepare();
    const id = h.admit(refundSpec(0, "dispatch", { kind: "STATEMENT_DISPATCH", amountCents: null, statementId }));
    h.settle(id, "dispatched", null);
    expect(projectRequests(h.workflow)[0]!.state).toBe("SUCCEEDED");
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
    expect(h.account().finalRefundCents).toBe(1600);
    expect(h.account().priorNetRefundsCents).toBe(0);
    expect(h.request.snapshot.priorRequests[0]!.actionKind).toBe("REQUEST_STATEMENT_DISPATCH");
  });
  it("late dispatch only issues its immutable old statement, never the current replacement", (): void => {
    const h = new RequestHarness(); const oldStatement = h.prepare();
    const id = h.admit(refundSpec(0, "dispatch", { kind: "STATEMENT_DISPATCH", amountCents: null, statementId: oldStatement }));
    h.claim(id); h.raw(id, "old-dispatch", "SUCCEEDED", null);
    h.request.snapshot.charges[0]!.chosenAmountCents = 300;
    const newStatement = h.prepare("CORRECTIVE", oldStatement); expect(newStatement).not.toBe(oldStatement);
    h.ingest("old-dispatch");
    expect(h.request.snapshot.priorStatements.find((fact): boolean => fact.versionId === oldStatement)?.issuedAt).not.toBeNull();
    expect(h.request.snapshot.priorStatements.find((fact): boolean => fact.versionId === newStatement)?.issuedAt).toBeNull();
    expect(h.request.snapshot.moneyEvents).toHaveLength(0);
  });
  it("same instruction replay after full settlement cannot start another operation", (): void => {
    const h = new RequestHarness(); const approvalId = h.approve(refundSpec(1600));
    const id = String(h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
    h.settle(id, "all-paid", 1600); expect(h.account().finalRefundCents).toBe(0);
    const result = h.run({ kind: "REQUEST_OPERATION", payload: { approvalId } });
    expect(result.summary.replayed).toBe(true); expect(h.workflow.requests).toHaveLength(1);
    expect(h.request.snapshot.moneyEvents).toHaveLength(1);
  });
  it("two same-amount partial returns need explicit distinct producer occurrences", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id);
    h.raw(id, "equal-return-a", "RETURNED", 100); h.ingest("equal-return-a");
    h.raw(id, "equal-return-b", "RETURNED", 100, "2026-09-17T12:00:00Z"); h.ingest("equal-return-b");
    expect(h.request.snapshot.moneyEvents).toHaveLength(3); expect(h.account().priorNetRefundsCents).toBe(400);
    expect((): unknown => h.raw(id, "ambiguous-delivery", "RETURNED", 100)).toThrow(/Ambiguous/);
  });
  it("a changed delivery ID and null occurrence cannot silently manufacture another equal return", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id);
    h.raw(id, "return-original", "RETURNED", 100); h.ingest("return-original");
    h.raw(id, "return-new-delivery", "RETURNED", 100); h.ingest("return-new-delivery");
    expect(h.request.snapshot.moneyEvents).toHaveLength(2); expect(h.account().priorNetRefundsCents).toBe(500);
  });
  it("uncertainty can be recorded after grant expiry without authorizing another payment", (): void => {
    const h = new RequestHarness(); const id = h.admit(); const attemptId = h.claim(id);
    h.request.snapshot.authorityGrants.forEach((grant): void => { grant.revoked = true; });
    h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId: id, attemptId, reason: "Late report of worker failure." } },
      { actorId: "trusted-recording-actor", isAdministrator: false });
    expect(projectRequests(h.workflow)[0]!.state).toBe("OUTCOME_UNKNOWN");
    expect(projectRequests(h.workflow)[0]!.reservedAmountCents).toBe(600);
  });
  it.each(["REFUND", "CHARGE_POSTING", "DEPOSIT_APPLICATION"] as const)(
    "unverifiable financial basis emits no event and retains READY %s commitment", (kind): void => {
      const h = new RequestHarness(); const amountCents = kind === "REFUND" ? 600 : 400;
      const id = h.admit(refundSpec(amountCents, "unknown-basis", { kind }));
      h.request.snapshot.depositBalance.amountCents = null;
      const result = reconcileRequestsAfterChange(h.request, h.workflow, requestContext("unknown-basis"));
      expect(projectRequests(result.workflow).find((entry): boolean => entry.requestId === id)?.state).toBe("READY");
      expect(projectRequests(result.workflow)[0]!.reservedAmountCents).toBe(amountCents);
      expect(result.workflow.events).toEqual(h.workflow.events);
      expect(result.workflow.requests).toEqual(h.workflow.requests);
      expect(result.workflow.approvals).toEqual(h.workflow.approvals);
      expect(nativeReview(result.request).result.account.finalRefundCents).toBeNull();
    });
  it("trusted simulator proof preserves business occurrence/knowledge separately from actual recording", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id);
    const money = h.request.snapshot.moneyEvents[0]!;
    const proof = h.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === money.sourceEvidenceId)!;
    expect(proof.sourceClass).toBe("TEST_ASSUMPTION"); expect(proof.recordKind).toBe("SOURCE_EVENT");
    expect(proof.associationAccepted).toBe(true); expect(proof.locator.startsWith("demo:")).toBe(true);
    expect(compare_timestamps(money.occurredAt, proof.learnedAt)).toBeLessThanOrEqual(0);
    expect(compare_timestamps(proof.learnedAt, money.learnedAt)).toBeLessThanOrEqual(0);
    expect(compare_timestamps(money.occurredAt, REQUEST_NOW)).toBe(-1);
    expect(h.workflow.events.every((event): boolean => compare_timestamps(event.recordedAt, REQUEST_NOW) === 0)).toBe(true);
  });
  it("no successful request can serve as native settlement proof without a MoneyEvent", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id); h.request.snapshot.moneyEvents = [];
    expect(h.account().finalRefundCents).toBeNull();
    expect(h.account().notFinalReasons.some((reason): boolean => reason.includes("not settlement proof"))).toBe(true);
  });
  it("a conflicting current replacement cannot create another commitment", (): void => {
    const h = new RequestHarness(); const id = h.admit(); h.settle(id); h.raw(id, "return", "RETURNED", 600); h.ingest("return");
    h.admit(refundSpec(300, "replace-part-a", { replacesRequestId: id }));
    expect((): unknown => h.admit(refundSpec(300, "replace-part-b", { replacesRequestId: id }))).toThrow(/conflicting replacement/);
  });
  it("pure input objects remain unchanged across command application", (): void => {
    const pair = requestFixture(); const before = canonical_json(pair);
    expect((): unknown => applyRequestCommand(pair.request, pair.workflow, { kind: "CLAIM_REQUEST", payload: { requestId: "missing" } }, requestContext("bad"))).toThrow();
    expect(canonical_json(pair)).toBe(before);
  });
});
