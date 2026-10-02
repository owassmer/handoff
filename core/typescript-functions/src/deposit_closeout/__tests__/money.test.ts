/** Independent money expectations and native BigInt/microsecond regressions.
 * Only this test scaffolding reads fixtures; production money has no I/O. */
import { readFileSync } from "node:fs";
import { beforeEach, describe, expect, it } from "vitest";
import { ContractError } from "../domain/codec.js";
import { _bounded, _Problems, _time, review_money } from "../domain/money.js";
import type { MoneyReview } from "../domain/money.js";
import type { CaseSnapshot, EvidenceInput, ItemDecision, MoneyEvent, RequestFact, ReviewRequest } from "../domain/types.js";
import { MAX_SAFE_INTEGER as MAX } from "../domain/vocabulary.js";

function when(day: number): string { return `2026-09-${String(day).padStart(2, "0")}T12:00:00Z`; }
interface EventOptions { day?: number; tx?: string; request?: string; target?: string; item?: string }
function event(key: string, kind: string, amount: number, o: EventOptions = {}): MoneyEvent {
  const statuses: Record<string, string> = { REFUND_INITIATED: "PENDING", REFUND_FAILED: "FAILED", REFUND_RETURNED: "RETURNED" };
  return { eventId: key, canonicalTransactionId: o.tx ?? key, sourceEventId: `source-${key}`, kind,
    status: statuses[kind] ?? "SETTLED", amountCents: amount, occurredAt: when(o.day ?? 5), learnedAt: when(15),
    sourceEvidenceId: "ev-money", requestId: o.request ?? null, reversesTransactionId: o.target ?? null, chargeItemId: o.item ?? null };
}
function request(key: string = "request-1", amount: number = 50000, state: string = "REQUESTED", fingerprint: string = "payload-1"): RequestFact {
  return { requestId: key, actionKind: "REQUEST_REFUND", targetVersionId: "review-1", payloadFingerprint: fingerprint,
    amountCents: amount, state, approvalIds: [], externalReference: null };
}
function blocked(result: MoneyReview, question?: string): void {
  expect(result.account.finalRefundCents).toBeNull(); expect(result.account.finalAccountReady).toBe(false);
  expect(result.moneyState).toBe("BLOCKED"); expect(result.questions.length).toBeGreaterThan(0);
  result.questions.forEach((q): void => { expect(q.resolverRole).toBe("ACCOUNTANT"); expect(q.neededRecord).toBeTruthy(); });
  if (question !== undefined) expect(result.questions.map((q): string => q.questionId)).toContain(question);
}
function permutations<T>(values: readonly T[]): T[][] {
  if (values.length === 0) return [[]];
  return values.flatMap((value: T, i: number): T[][] => permutations([...values.slice(0, i), ...values.slice(i + 1)]).map((rest: T[]): T[] => [value, ...rest]));
}

describe("native money review", (): void => {
  let snapshot: CaseSnapshot; let clock: string; let decisions: ItemDecision[]; let known: ItemDecision[]; let proof: EvidenceInput;
  beforeEach((): void => {
    const input = JSON.parse(readFileSync(new URL("./fixtures/base_request.json", import.meta.url), "utf8")) as ReviewRequest;
    snapshot = input.snapshot; clock = input.reviewClock;
    decisions = snapshot.charges.map((c): ItemDecision => ({ itemId: c.itemId, costVersionId: c.costVersionId,
      vendorCostCents: c.vendorCostCents, allocation: c.acceptedAllocation, allowability: c.allowabilityState,
      supportedAmountCents: c.supportedAmountCents, chosenAmountCents: c.chosenAmountCents, choiceState: c.choiceState,
      reason: c.reason, sourceReferences: [], ruleQuestionIds: [], missingInputIds: [...c.unresolvedQuestionIds],
      requiresReviewer: c.reviewRequired, fingerprint: c.itemId }));
    known = [...decisions];
    known[2] = { ...known[2]!, allocation: "TENANT", allowability: "SUPPORTED", vendorCostCents: 15000,
      supportedAmountCents: 15000, chosenAmountCents: 15000, choiceState: "CHOSEN", requiresReviewer: false, missingInputIds: [] };
    proof = { ...snapshot.evidence[2]!, evidenceId: "ev-money", recordKind: "SOURCE_EVENT", externalRecordId: "test-ledger", occurredAt: null, learnedAt: when(15) };
    snapshot = { ...snapshot, evidence: [...snapshot.evidence, proof] };
  });
  function review(events: MoneyEvent[] = [], requests: RequestFact[] = [], s: CaseSnapshot = snapshot, ds: ItemDecision[] = known, scope: boolean = true): MoneyReview {
    return review_money({ ...s, moneyEvents: events, priorRequests: requests }, ds, scope, clock);
  }
  function net(amount: number, included: string[], day: number = 8): CaseSnapshot {
    return { ...snapshot, depositBalance: { ...snapshot.depositBalance, amountCents: amount, asOf: when(day), includedTransactionIds: included, sourceEvidenceId: "ev-money" } };
  }
  it("preserves interface and empty-history amounts", (): void => {
    const r = review();
    expect(Object.keys(r).sort()).toEqual(["account", "hasReturn", "hasUnknownResult", "moneyReason", "moneyState", "questions"]);
    expect(r.account).toMatchObject({ recordedDepositCents: 200000, knownChosenDeductionsCents: 40000, totalDeductionsCents: 40000,
      finalRefundCents: 160000, proposedExcessReceivableCents: 0, postingDeltaCents: 40000, depositApplicationDeltaCents: 40000, finalAccountReady: true });
    expect(r.moneyState).toBe("READY"); expect(r.questions).toEqual([]);
  });
  it("unknown is not zero; known subtotal survives", (): void => {
    const r = review([], [], snapshot, decisions); blocked(r, "money:item:additional-item");
    expect(r.account).toMatchObject({ recordedDepositCents: 200000, knownChosenDeductionsCents: 25000, unresolvedItemIds: ["additional-item"], totalDeductionsCents: null, pendingReservedRefundCents: 0 });
    const ds = [...known]; ds[2] = { ...ds[2]!, allowability: "NOT_EVALUATED", supportedAmountCents: null, chosenAmountCents: 0 };
    blocked(review([], [], snapshot, ds)); expect(review([], [], snapshot, ds).account.knownChosenDeductionsCents).toBe(25000);
  });
  it("deliberate waiver zero does not erase unresolved review work", (): void => {
    const ds = [...decisions]; ds[2] = { ...ds[2]!, choiceState: "WAIVED", chosenAmountCents: 0, requiresReviewer: false, missingInputIds: [] };
    expect(review([], [], snapshot, ds).account).toMatchObject({ finalAccountReady: true, totalDeductionsCents: 25000, finalRefundCents: 175000 });
    blocked(review([], [], snapshot, [...ds.slice(0, 2), { ...ds[2]!, requiresReviewer: true }]));
    blocked(review([], [], snapshot, [...ds.slice(0, 2), { ...ds[2]!, missingInputIds: ["still-required"] }]));
  });
  it("owner costs are excluded, not interpreted as completed review", (): void => {
    const ds = [...known]; ds[1] = { ...ds[1]!, vendorCostCents: MAX };
    expect(review([], [], snapshot, ds).account.totalDeductionsCents).toBe(40000);
    ds[1] = { ...ds[1]!, chosenAmountCents: 80000 }; blocked(review([], [], snapshot, ds));
    ds[1] = { ...ds[1]!, chosenAmountCents: 0, requiresReviewer: true }; blocked(review([], [], snapshot, ds), "money:item:paint-800");
  });
  it("requires supported chosen amounts and consistent per-item decisions", (): void => {
    blocked(review([], [], snapshot, [{ ...known[0]!, chosenAmountCents: 25001 }, ...known.slice(1)]));
    blocked(review([], [], snapshot, known.slice(0, 2)));
    blocked(review([], [], snapshot, [...known, { ...known[0]!, chosenAmountCents: 1 }]));
    blocked(review([], [], snapshot, [...known, { ...known[0]!, itemId: "absent" }]));
    expect(review([], [], snapshot, [...known, known[0]!]).account.totalDeductionsCents).toBe(40000);
    blocked(review([], [], { ...snapshot, charges: [...snapshot.charges, { ...snapshot.charges[0]!, reason: "changed" }] }));
  });
  it("supported subtotal survives outstanding review", (): void => {
    const r = review([], [], snapshot, [{ ...known[0]!, requiresReviewer: true }, ...known.slice(1)]); blocked(r);
    expect(r.account.knownChosenDeductionsCents).toBe(40000);
  });
  it("charge posting is not custody or application", (): void => {
    expect(review([event("posting", "CHARGE_POSTING", 25000, { item: "repair-250" })]).account).toMatchObject({ recordedDepositCents: 200000,
      existingNetPostingCents: 25000, postingDeltaCents: 15000, depositApplicationDeltaCents: 40000, finalRefundCents: 160000 });
  });
  it("post-snapshot application/refund and net-snapshot anti-double-counting", (): void => {
    const es = [event("application", "DEPOSIT_APPLICATION", 25000), event("refund", "REFUND_SETTLED", 30000)];
    const expected = { recordedDepositCents: 145000, existingDepositApplicationsCents: 25000, priorNetRefundsCents: 30000,
      depositApplicationDeltaCents: 15000, finalRefundCents: 130000, proposedExcessReceivableCents: 0 };
    expect(review(es).account).toMatchObject(expected); expect(review(es, [], net(145000, ["application", "refund"])).account).toMatchObject(expected);
    expect(review([...es, event("later", "REFUND_SETTLED", 20000, { day: 10 })], [], net(145000, ["application", "refund"])).account)
      .toMatchObject({ recordedDepositCents: 125000, priorNetRefundsCents: 50000, finalRefundCents: 110000 });
  });
  it.each([["event"], [], ["canonical", "canonical"], ["absent"]])("requires canonical inclusion/history: %j", (...included: string[]): void => {
    blocked(review([event("event", "DEPOSIT_APPLICATION", 25000, { tx: "canonical" })], [], net(175000, included)), "money:balance-basis");
  });
  it("valid inclusion cannot reference future or only-pending effects", (): void => {
    expect(review([event("event", "DEPOSIT_APPLICATION", 25000, { tx: "canonical" })], [], net(175000, ["canonical"])).account.recordedDepositCents).toBe(175000);
    blocked(review([event("later", "REFUND_SETTLED", 10000, { day: 10 })], [], net(190000, ["later"])), "money:balance-basis");
    blocked(review([event("pending", "REFUND_INITIATED", 10000)], [], net(200000, ["pending"])), "money:balance-basis");
  });
  it("uncertain balance produces null ledger values and named questions", (): void => {
    for (const patch of [{ amountCents: null }, { basis: "UNRECONCILED" }, { reconciliationState: "CONFLICT" }, { asOf: when(17) }]) {
      const r = review([], [], { ...snapshot, depositBalance: { ...snapshot.depositBalance, ...patch } }); blocked(r, "money:balance-basis");
      expect(r.account.recordedDepositCents).toBeNull(); expect(r.account.existingNetPostingCents).toBeNull(); expect(r.account.pendingReservedRefundCents).toBeNull();
    }
    blocked(review([], [], { ...snapshot, currency: "EUR" }), "money:currency");
  });
  it("over-deposit receivable and signed reversal deltas are separate", (): void => {
    expect(review([], [], snapshot, [{ ...known[0]!, chosenAmountCents: 225000, supportedAmountCents: 225000, vendorCostCents: 225000 }, ...known.slice(1)]).account)
      .toMatchObject({ totalDeductionsCents: 240000, finalRefundCents: 0, proposedExcessReceivableCents: 40000, postingDeltaCents: 240000, depositApplicationDeltaCents: 200000 });
    expect(review([event("posting", "CHARGE_POSTING", 60000), event("application", "DEPOSIT_APPLICATION", 60000)]).account)
      .toMatchObject({ postingDeltaCents: -20000, depositApplicationDeltaCents: -20000, recordedDepositCents: 140000, finalRefundCents: 160000 });
  });
  it("negative holdings and overpayment block rather than round to zero", (): void => {
    blocked(review([event("too-much", "REFUND_SETTLED", 200001)]), "money:negative-funds");
    const r = review([event("overpaid", "REFUND_SETTLED", 170000)]); blocked(r, "money:overpayment");
    expect(r.account.recordedDepositCents).toBe(30000); expect(r.account.priorNetRefundsCents).toBeNull();
    blocked(review([event("prior", "REFUND_SETTLED", 1)], [], snapshot, [{ ...known[0]!, chosenAmountCents: 200000, supportedAmountCents: 200000 }, ...known.slice(1)]), "money:overpayment");
  });
  it("event/source aliases and repeated canonical settlement reports count once", (): void => {
    const e = event("refund", "REFUND_SETTLED", 30000);
    expect(review([e, e, { ...e, eventId: "copy" }]).account).toMatchObject({ priorNetRefundsCents: 30000, recordedDepositCents: 170000, finalRefundCents: 130000 });
    expect(review([event("r1", "REFUND_SETTLED", 30000, { tx: "refund" }), event("r2", "REFUND_SETTLED", 30000, { day: 6, tx: "refund" })]).account.priorNetRefundsCents).toBe(30000);
  });
  it("contradictory aliases never select an input row", (): void => {
    const e = event("refund", "REFUND_SETTLED", 30000);
    for (const other of [{ ...e, amountCents: 30001 }, { ...e, eventId: "copy", amountCents: 30001 }, { ...e, canonicalTransactionId: "other" }]) {
      const r = review([e, other]); blocked(r); expect(r.account.recordedDepositCents).toBeNull(); expect(r).toEqual(review([other, e]));
    }
  });
  it("request plus correlated initiation reserves once without settlement", (): void => {
    const q = request(); const e = event("initiated", "REFUND_INITIATED", 50000, { request: q.requestId });
    for (const es of [[], [e, e]]) {
      const r = review(es, [q, q]); expect(r.account).toMatchObject({ finalRefundCents: 160000, pendingReservedRefundCents: 50000, priorNetRefundsCents: 0, finalAccountReady: true }); expect(r.moneyState).toBe("PENDING");
    }
    expect(review([{ ...e, requestId: null }]).account.pendingReservedRefundCents).toBe(50000);
    expect(review([{ ...e, requestId: null }, event("second", "REFUND_INITIATED", 50000)]).account.pendingReservedRefundCents).toBe(100000);
  });
  it("settled/returned requests cease reserving even with stale request state", (): void => {
    const q = request(); const es = [event("initiated", "REFUND_INITIATED", 50000, { tx: "payment", request: q.requestId }), event("settled", "REFUND_SETTLED", 50000, { day: 6, tx: "payment", request: q.requestId })];
    expect(review(es, [q]).account).toMatchObject({ pendingReservedRefundCents: 0, priorNetRefundsCents: 50000, finalRefundCents: 110000 });
    const r = review([...es, event("returned", "REFUND_RETURNED", 50000, { day: 7, tx: "payment", request: q.requestId })], [{ ...q, state: "SUCCEEDED" }]);
    expect(r.account).toMatchObject({ pendingReservedRefundCents: 0, priorNetRefundsCents: 0, finalRefundCents: 160000 }); expect(r.hasReturn).toBe(true); expect(r.moneyState).toBe("REOPENED");
  });
  it.each(["FAILED", "CANCELLED", "SUPERSEDED"])("terminal %s releases reservation but contradicting payment blocks", (state: string): void => {
    const q = request("request-1", 50000, state); expect(review([], [q]).account.pendingReservedRefundCents).toBe(0);
    blocked(review([event("paid", "REFUND_SETTLED", 50000, { request: q.requestId })], [q])); blocked(review([event("pending", "REFUND_INITIATED", 50000, { request: q.requestId })], [q]));
  });
  it("failure releases reservations; unknown/unproved success do not prove settlement", (): void => {
    const q = request(); expect(review([event("failed", "REFUND_FAILED", 50000, { request: q.requestId })], [q]).account.pendingReservedRefundCents).toBe(0);
    const r = review([], [{ ...q, state: "OUTCOME_UNKNOWN" }]); blocked(r); expect(r.hasUnknownResult).toBe(true);
    blocked(review([], [{ ...q, state: "SUCCEEDED" }]));
    const unknown = review([{ ...event("unknown", "REFUND_SETTLED", 50000), status: "UNKNOWN" }]); blocked(unknown); expect(unknown.hasUnknownResult).toBe(true);
  });
  it("request row conflicts and active payload aliases are not ordered or totaled", (): void => {
    const q = request();
    for (const other of [{ ...q, amountCents: 40000 }, { ...q, payloadFingerprint: "changed" }, { ...q, state: "SUCCEEDED" }, { ...q, requestId: "second-key" }]) {
      const r = review([], [q, other]); blocked(r); expect(r).toEqual(review([], [other, q]));
    }
    blocked(review([], [{ ...q, externalReference: "external" }, { ...q, externalReference: "external", requestId: "other", payloadFingerprint: "other" }]));
    blocked(review([], [{ ...q, state: "UNSUPPORTED" }])); blocked(review([], [{ ...q, amountCents: null }]));
  });
  it("external identity aliases across terminal requests block before holdings certification", (): void => {
    const q = { ...request(), externalReference: "same-payment", state: "SUCCEEDED" }; const other = { ...q, requestId: "second", payloadFingerprint: "other" };
    const r = review([event("first", "REFUND_SETTLED", 50000, { request: q.requestId }), event("second", "REFUND_SETTLED", 50000, { request: other.requestId })], [q, other]);
    blocked(r, "money:duplicate-external-reference:request-1:second"); expect(r.account.recordedDepositCents).toBeNull(); expect(r.account.priorNetRefundsCents).toBeNull();
  });
  it("reservations cannot exceed remaining entitlement", (): void => {
    blocked(review([], [request("request-1", 160001)]), "money:overpayment"); blocked(review([event("prior", "REFUND_SETTLED", 50000)], [request("request-1", 120000)]), "money:overpayment");
  });
  it("request action/principal must match and only one payment identity may claim a refund request", (): void => {
    const e = event("payment", "REFUND_SETTLED", 50000, { request: "request-1" }); blocked(review([e]));
    blocked(review([e], [request("request-1", 50001)])); blocked(review([e], [{ ...request(), actionKind: "REQUEST_LEDGER_POSTING" }]));
    const r = review([e, event("second", "REFUND_SETTLED", 50000, { day: 6, request: "request-1" })], [request()]); blocked(r);
    // This conflict is discovered after independently certified custody.
    expect(r.account.recordedDepositCents).toBe(100000); expect(r.account.pendingReservedRefundCents).toBeNull();
  });
  it("same-canonical partial return has one net effect across snapshot cuts", (): void => {
    const es = [event("paid", "REFUND_SETTLED", 50000, { tx: "payment" }), event("returned", "REFUND_RETURNED", 20000, { day: 10, tx: "payment" })];
    for (const s of [snapshot, net(150000, ["payment"]), net(170000, ["payment"], 12)]) {
      const r = review(es, [], s); expect(r.account).toMatchObject({ priorNetRefundsCents: 30000, recordedDepositCents: 170000, finalRefundCents: 130000 }); expect(r.moneyState).toBe("REOPENED");
    }
    expect(review([es[0]!, { ...es[1]!, reversesTransactionId: "payment" }]).account.finalRefundCents).toBe(130000);
  });
  it("independent partial returns sum once with explicit target", (): void => {
    const es = [event("payment", "REFUND_SETTLED", 50000), event("return", "REFUND_RETURNED", 20000, { day: 7, target: "payment" })];
    const r = review(es); expect(r.account).toMatchObject({ priorNetRefundsCents: 30000, finalRefundCents: 130000 }); expect(r.hasReturn).toBe(true);
    expect(review(es, [], net(170000, ["payment", "return"])).account.finalRefundCents).toBe(130000);
    expect(review([...es, event("return2", "REFUND_RETURNED", 10000, { day: 8, target: "payment" })]).account.priorNetRefundsCents).toBe(20000);
  });
  it("orphan, over-principal and identity-inconsistent returns block", (): void => {
    const paid = event("payment", "REFUND_SETTLED", 50000); const returned = event("return", "REFUND_RETURNED", 20000, { day: 7, target: "payment" });
    blocked(review([returned])); blocked(review([paid, { ...returned, amountCents: 50001 }]));
    blocked(review([paid, returned, event("return2", "REFUND_RETURNED", 40000, { day: 8, target: "payment" })]));
    blocked(review([paid, { ...returned, requestId: "request-1" }], [request()]));
    blocked(review([paid, { ...returned, canonicalTransactionId: "payment", requestId: "request-1", reversesTransactionId: null }], [request()]));
    blocked(review([event("only-return", "REFUND_RETURNED", 20000)])); blocked(review([paid, { ...returned, reversesTransactionId: "return" }]));
  });
  it("in-transaction and independent reversals cannot both claim principal", (): void => {
    blocked(review([event("payment", "REFUND_SETTLED", 50000), event("r1", "REFUND_RETURNED", 10000, { day: 7, tx: "payment" }), event("r2", "REFUND_RETURNED", 10000, { day: 8, target: "payment" })]));
  });
  it("equal-time conflict, regression and changed repeated principal block", (): void => {
    const started = event("started", "REFUND_INITIATED", 50000, { tx: "payment" }); const paid = event("paid", "REFUND_SETTLED", 50000, { tx: "payment" });
    blocked(review([started, paid])); blocked(review([started, event("failed", "REFUND_FAILED", 50000, { day: 6, tx: "payment" }), { ...paid, occurredAt: when(7) }]));
    blocked(review([paid, { ...started, occurredAt: when(7) }])); blocked(review([started, { ...paid, amountCents: 30000, occurredAt: when(6) }]));
    blocked(review([paid, event("r1", "REFUND_RETURNED", 20000, { day: 7, tx: "payment" }), event("r2", "REFUND_RETURNED", 30000, { day: 8, tx: "payment" })]));
  });
  it("requires a supported kind/status/family", (): void => {
    const e = event("bad", "REFUND_SETTLED", 50000);
    for (const patch of [{ status: "RETURNED" }, { kind: "CORRECTION" }, { kind: "DEPOSIT_RECEIPT", status: "PENDING" }]) blocked(review([{ ...e, ...patch }]));
    blocked(review([e, { ...event("other", "CHARGE_POSTING", 50000, { day: 6 }), canonicalTransactionId: "bad" }]));
  });
  it("application and posting reversals preserve signed ledger effects", (): void => {
    const es = [event("app", "DEPOSIT_APPLICATION", 50000), event("post", "CHARGE_POSTING", 50000), event("ar", "DEPOSIT_APPLICATION_REVERSAL", 20000, { day: 7, target: "app" }), event("pr", "CHARGE_POSTING_REVERSAL", 10000, { day: 7, target: "post" })];
    expect(review(es).account).toMatchObject({ recordedDepositCents: 170000, existingDepositApplicationsCents: 30000, existingNetPostingCents: 40000, depositApplicationDeltaCents: 10000, postingDeltaCents: 0, finalRefundCents: 160000 });
  });
  it("full same-transaction reversal after snapshot restores held amount", (): void => {
    const posted = event("app", "DEPOSIT_APPLICATION", 50000); const reversed = { ...posted, eventId: "reverse", sourceEventId: "source-reverse", status: "REVERSED", occurredAt: when(10) };
    expect(review([posted, reversed], [], net(150000, ["app"])).account).toMatchObject({ recordedDepositCents: 200000, existingDepositApplicationsCents: 0, finalRefundCents: 160000 }); blocked(review([reversed]));
  });
  it("orphan, wrong-family, early, overamount and self-reversal block", (): void => {
    const app = event("app", "DEPOSIT_APPLICATION", 50000); const reverse = event("reverse", "DEPOSIT_APPLICATION_REVERSAL", 10000, { day: 7, target: "app" }); blocked(review([reverse]));
    for (const patch of [{ amountCents: 50001 }, { occurredAt: when(5) }, { kind: "CHARGE_POSTING_REVERSAL" }, { reversesTransactionId: "reverse" }, { reversesTransactionId: null }]) blocked(review([app, { ...reverse, ...patch }]));
  });
  it("receipts/transfers reconcile without implying applications", (): void => {
    const es = [event("receipt", "DEPOSIT_RECEIPT", 10000), event("in", "DEPOSIT_TRANSFER_IN", 20000), event("out", "DEPOSIT_TRANSFER_OUT", 5000)];
    for (const s of [snapshot, net(225000, ["receipt", "in", "out"])]) expect(review(es, [], s).account).toMatchObject({ recordedDepositCents: 225000, finalRefundCents: 185000 });
  });
  it("proof must exist, be accepted/known/consistent, and not be model-derived", (): void => {
    const e = event("paid", "REFUND_SETTLED", 50000); blocked(review([{ ...e, sourceEvidenceId: "absent" }]));
    for (const patch of [{ associationAccepted: false }, { learnedAt: when(17) }, { sourceClass: "MODEL_PROPOSAL" }, { recordKind: "MODEL_PROPOSAL" }, { occurredAt: when(16) }]) blocked(review([e], [], { ...snapshot, evidence: [...snapshot.evidence.slice(0, -1), { ...proof, ...patch }] }));
    blocked(review([e], [], { ...snapshot, evidence: [...snapshot.evidence, { ...proof, sourceVersion: "conflict" }] }));
    blocked(review([], [], { ...snapshot, depositBalance: { ...snapshot.depositBalance, sourceEvidenceId: "absent" } }), "money:balance-basis");
  });
  it("event proof/knowledge ordering and charge references are checked", (): void => {
    const e = event("paid", "REFUND_SETTLED", 50000);
    for (const patch of [{ learnedAt: when(17) }, { learnedAt: when(4) }, { chargeItemId: "absent" }, { chargeItemId: "repair-250" }]) blocked(review([{ ...e, ...patch }]));
    expect((): MoneyReview => review([{ ...e, occurredAt: "2026-09-05T12:00:00" }])).toThrow(ContractError);
    blocked(review([e], [], { ...snapshot, evidence: [...snapshot.evidence.slice(0, -1), { ...proof, learnedAt: when(4) }] }));
    blocked(review([{ ...e, learnedAt: when(6) }])); blocked(review([], [], { ...snapshot, depositBalance: { ...snapshot.depositBalance, asOf: when(8) } }), "money:balance-basis");
  });
  it("unrelated balances and missing route never become deductions; scope still blocks", (): void => {
    const s: CaseSnapshot = { ...snapshot, otherBalances: [
      { balanceId: "unrelated", description: "Other claim", amountCents: 90000, state: "KNOWN", sourceEvidenceId: "ev-balance", unresolvedQuestionIds: [] },
      { balanceId: "unknown-related", description: "Parent reviews", amountCents: null, state: "UNKNOWN", sourceEvidenceId: "ev-balance", unresolvedQuestionIds: ["related-question"] }],
      recipients: { ...snapshot.recipients, state: "MISSING", verifiedRouteReference: null } };
    expect(review([], [], s).account).toMatchObject({ finalRefundCents: 160000, finalAccountReady: true, otherBalanceIds: ["unknown-related", "unrelated"], recipientState: "MISSING" }); blocked(review([], [], s, known, false), "money:scope");
  });
  it("zero-work not-applicable differs from proved fulfillment without remaining ledger delta", (): void => {
    const s = { ...snapshot, charges: [], depositBalance: { ...snapshot.depositBalance, amountCents: 0 } };
    expect(review([], [], s, []).account.finalRefundCents).toBe(0); expect(review([], [], s, []).moneyState).toBe("NOT_APPLICABLE");
    const es = [event("app", "DEPOSIT_APPLICATION", 40000), event("post", "CHARGE_POSTING", 40000), event("paid", "REFUND_SETTLED", 160000)];
    const r = review(es); expect(r.account).toMatchObject({ recordedDepositCents: 0, finalRefundCents: 0, priorNetRefundsCents: 160000 }); expect(r.moneyState).toBe("FULFILLED"); expect(review([es[0]!, es[2]!]).moneyState).toBe("READY");
  });
  it.each([true, false, 1.5, "1", -1, MAX + 1, NaN, Infinity, undefined, 1n])("rejects invalid programmatic amount %s, without coercion/defaulting", (bad: unknown): void => {
    const invalid = bad as number;
    expect((): MoneyReview => review([{ ...event("paid", "REFUND_SETTLED", 1), amountCents: invalid }])).toThrow(ContractError);
    expect((): MoneyReview => review([], [], { ...snapshot, depositBalance: { ...snapshot.depositBalance, amountCents: invalid } })).toThrow(ContractError);
    expect((): MoneyReview => review([], [{ ...request("bad"), amountCents: invalid }])).toThrow(ContractError);
    expect((): MoneyReview => review([], [], snapshot, [{ ...known[0]!, chosenAmountCents: invalid }, ...known.slice(1)])).toThrow(ContractError);
  });
  it("rejects invalid scope, timestamp, identifier and bigint wire input", (): void => {
    expect((): MoneyReview => review_money(snapshot, known, "true" as unknown as boolean, clock)).toThrow("scope_supported: expected boolean");
    for (const value of ["2026-02-30T12:00:00Z", "2026-09-05T12:00:00+25:00", null]) expect((): string => _time(value, "clock")).toThrow(ContractError);
    expect((): MoneyReview => review([{ ...event("paid", "REFUND_SETTLED", 1), eventId: "" }])).toThrow(ContractError);
    expect((): number => _bounded(1n, "wire")).toThrow(ContractError);
  });
  it("bounds chosen totals, holdings and reconstructed gross deposit basis", (): void => {
    expect((): MoneyReview => review([], [], snapshot, [{ ...known[0]!, chosenAmountCents: MAX, supportedAmountCents: MAX }, ...known.slice(1)])).toThrow("knownChosenDeductionsCents");
    expect((): MoneyReview => review([event("app", "DEPOSIT_APPLICATION", 1)], [], net(MAX, ["app"]))).toThrow("gross deposit basis");
    const s = { ...snapshot, depositBalance: { ...snapshot.depositBalance, amountCents: MAX } };
    expect((): MoneyReview => review([event("receipt", "DEPOSIT_RECEIPT", 1)], [], s)).toThrow("actual current holdings"); expect(review([], [], s).account.finalRefundCents).toBe(MAX - 40000);
  });
  it.each(["CHARGE_POSTING", "DEPOSIT_APPLICATION", "REFUND_SETTLED"])("bounds aggregate %s", (kind: string): void => {
    expect((): MoneyReview => review([event("one", kind, MAX), event("two", kind, 1)])).toThrow(ContractError);
  });
  it("bounds reservation/reversal aggregates even after business conflicts", (): void => {
    expect((): MoneyReview => review([], [request("first", MAX), request("second", 1, "REQUESTED", "other")])).toThrow("pendingReservedRefundCents");
    expect((): MoneyReview => review([event("original", "REFUND_SETTLED", MAX), event("a", "REFUND_RETURNED", MAX, { day: 6, target: "original" }), event("b", "REFUND_RETURNED", 1, { day: 7, target: "original" })])).toThrow("reversal total:original");
  });
  it("later receipts cannot hide prior negative holdings", (): void => {
    blocked(review([event("overdraw", "REFUND_SETTLED", 250000), event("receipt", "DEPOSIT_RECEIPT", 100000, { day: 7 })]), "money:negative-funds");
  });
  it("bounds each historical cut, not only final holdings", (): void => {
    const s = { ...snapshot, depositBalance: { ...snapshot.depositBalance, amountCents: MAX } };
    expect((): MoneyReview => review([event("in", "DEPOSIT_RECEIPT", 1), event("out", "DEPOSIT_TRANSFER_OUT", 1, { day: 6 })], [], s)).toThrow("post-snapshot holdings");
  });
  it("BigInt preserves an exact one-cent net after transient sums greater than safe Number", (): void => {
    const s = { ...snapshot, charges: [], depositBalance: { ...snapshot.depositBalance, amountCents: 0 } };
    const es = [event("a", "DEPOSIT_RECEIPT", MAX), event("b", "DEPOSIT_RECEIPT", MAX), event("c", "DEPOSIT_RECEIPT", MAX), event("d", "DEPOSIT_RECEIPT", 1), event("e", "DEPOSIT_TRANSFER_OUT", MAX), event("f", "DEPOSIT_TRANSFER_OUT", MAX), event("g", "DEPOSIT_TRANSFER_OUT", MAX)];
    expect(review(es, [], s, []).account).toMatchObject({ recordedDepositCents: 1, finalRefundCents: 1, finalAccountReady: true }); expect(review([...es].reverse(), [], s, []).account.recordedDepositCents).toBe(1);
  });
  it("snapshot inclusion cancellation never rounds through an unsafe intermediate", (): void => {
    const es = [event("a", "DEPOSIT_RECEIPT", MAX), event("b", "DEPOSIT_RECEIPT", 2)]; const s = { ...net(1, ["a", "b"]), charges: [] };
    expect(review(es, [], s, []).account).toMatchObject({ recordedDepositCents: 1, finalRefundCents: 1, finalAccountReady: true });
  });
  it("microsecond ordering does not truncate to milliseconds", (): void => {
    const started = { ...event("started", "REFUND_INITIATED", 50000, { tx: "payment" }), occurredAt: "2026-09-05T12:00:00.000001Z" };
    const paid = { ...event("paid", "REFUND_SETTLED", 50000, { tx: "payment" }), occurredAt: "2026-09-05T12:00:00.000002Z" };
    expect(review([paid, started]).account).toMatchObject({ priorNetRefundsCents: 50000, finalRefundCents: 110000 }); blocked(review([started, { ...paid, occurredAt: started.occurredAt }]));
  });
  it("timestamp equivalence and source aliases compare instants rather than spellings", (): void => {
    const paid = event("paid", "REFUND_SETTLED", 50000); const copy = { ...paid, eventId: "copy", occurredAt: "2026-09-05T08:00:00-04:00", learnedAt: "2026-09-15T12:00:00.000000Z" };
    expect(review([paid, copy]).account.priorNetRefundsCents).toBe(50000);
    expect(review([paid], [], { ...snapshot, evidence: [...snapshot.evidence, { ...proof, learnedAt: "2026-09-15T08:00:00-04:00" }] }).account.priorNetRefundsCents).toBe(50000);
  });
  it("returned replacement moves from pending to proved fulfillment", (): void => {
    const q = request("request-1", 160000); const es = [event("app", "DEPOSIT_APPLICATION", 40000), event("post", "CHARGE_POSTING", 40000), event("paid", "REFUND_SETTLED", 160000, { day: 6, tx: "payment" }), event("returned", "REFUND_RETURNED", 160000, { day: 7, tx: "payment" })];
    const pending = review(es, [q]); expect(pending.hasReturn).toBe(true); expect(pending.moneyState).toBe("PENDING"); expect(pending.account.pendingReservedRefundCents).toBe(160000);
    const complete = review([...es, event("replacement", "REFUND_SETTLED", 160000, { day: 9, request: q.requestId })], [q]); expect(complete.hasReturn).toBe(true); expect(complete.moneyState).toBe("FULFILLED"); expect(complete.account).toMatchObject({ priorNetRefundsCents: 160000, finalRefundCents: 0, pendingReservedRefundCents: 0 });
  });
  it("fully-returned zero-net cash history still needs snapshot inclusion", (): void => {
    const es = [event("paid", "REFUND_SETTLED", 50000, { tx: "payment" }), event("returned", "REFUND_RETURNED", 50000, { day: 7, tx: "payment" })];
    expect(review(es, [], net(200000, ["payment"])).account).toMatchObject({ recordedDepositCents: 200000, priorNetRefundsCents: 0, finalRefundCents: 160000 }); blocked(review(es, [], net(200000, [])), "money:balance-basis");
  });
  it("no mutation and equivalence across all 120 event permutations", (): void => {
    const q = request(); const es = [event("started", "REFUND_INITIATED", 50000, { tx: "payment", request: q.requestId }), event("paid", "REFUND_SETTLED", 50000, { day: 6, tx: "payment", request: q.requestId }), event("returned", "REFUND_RETURNED", 20000, { day: 7, tx: "payment", request: q.requestId }), event("app", "DEPOSIT_APPLICATION", 25000), event("post", "CHARGE_POSTING", 40000)];
    const s = { ...snapshot, moneyEvents: es, priorRequests: [q, q] }; const before = structuredClone({ s, known }); const expected = review_money(s, known, true, clock); expect(expected.account.finalRefundCents).toBe(130000);
    permutations(es).forEach((permuted: MoneyEvent[]): void => { expect(review_money({ ...s, moneyEvents: permuted, evidence: [...s.evidence].reverse(), charges: [...s.charges].reverse() }, [...known].reverse(), true, clock)).toEqual(expected); }); expect({ s, known }).toEqual(before);
  });
  it("question keys, reasons and affected IDs use Unicode code-point ordering", (): void => {
    const p = new _Problems(); p.add("money:𐀀", "z", "record", { ledger: false, item: "𐀀" }); p.add("money:", "a", "record", { ledger: false, item: "" }); p.add("money:𐀀", "a", "record", { ledger: false, item: "" });
    expect(p.questions().map((q): string => q.questionId)).toEqual(["money:", "money:𐀀"]); expect(p.questions()[1]!.reason).toBe("a z"); expect(p.questions()[1]!.affectedItemIds).toEqual(["", "𐀀"]);
  });
});
