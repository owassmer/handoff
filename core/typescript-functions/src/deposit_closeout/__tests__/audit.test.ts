/** Independent audit counterexamples for the read-only review core.
 * Input scaffolding intentionally does not use generated engine output as expectations.
 */
import { describe, expect, it } from "vitest";
import type { CaseSnapshot, OpenQuestion, ReviewRequest, ReviewResult } from "../domain/types.js";
import { action, applyFixturePatch, baseRequest, item, questionIds, requireElement, resultFor, track } from "./fixtures/helpers.js";

function ordinaryRequest(): ReviewRequest {
  const raw = baseRequest(); const snapshot = raw.snapshot;
  Object.assign(requireElement(snapshot.charges, 2), {
    costState: "KNOWN", vendorCostCents: 15000, costVersionId: "audit-additional",
    acceptedAllocation: "TENANT", allowabilityState: "SUPPORTED", supportedAmountCents: 15000,
    chosenAmountCents: 15000, choiceState: "CHOSEN", reviewRequired: false,
    evidenceIds: ["ev-extent", "audit-additional"], unresolvedQuestionIds: [],
  });
  snapshot.evidence.push({ ...requireElement(snapshot.evidence, 3), evidenceId: "audit-additional", externalRecordId: "audit-additional", locator: "fixture:audit-additional", proposedItemIds: ["additional-item"] });
  snapshot.questions = [];
  return raw;
}
function review(raw: ReviewRequest): ReviewResult { return resultFor(raw).result; }
function openQuestion(key: string, itemIds: string[]): OpenQuestion {
  return {
    questionId: key, question: "Which current record resolves the disputed decision?",
    reason: "An explicit unresolved decision, not an instruction to the reviewer.",
    resolverRole: "MANAGER", resolverPartyId: "demo-manager", neededRecord: "Accepted current decision",
    affectedItemIds: itemIds, affectedActionKinds: ["PREPARE_STATEMENT", "REQUEST_REFUND"],
  };
}
function addProof(snapshot: CaseSnapshot, key: string): void {
  snapshot.evidence.push({ ...requireElement(snapshot.evidence, 3), evidenceId: key, externalRecordId: key, recordKind: "SOURCE_EVENT", occurredAt: "2026-09-10T12:00:00Z", learnedAt: "2026-09-10T12:00:00Z", proposedItemIds: [] });
}

describe("original Phase B independent audit assertions", (): void => {
  it("control: ordinary work and deposit arithmetic progress independently", (): void => {
    const raw = ordinaryRequest(); const result = review(raw);
    expect(result.account.finalRefundCents).toBe(160000);
    expect(result.missingInputs).toEqual([]);
    expect(result.account.finalAccountReady).toBe(true);
    expect(result.actions.filter((a): boolean => a.actionKind.startsWith("REQUEST_")).every((a): boolean => a.availability === "BLOCKED")).toBe(true);
    expect(result.outcomes.depositComplete).toBe(false);
    expect(result.outcomes.overallCaseComplete).toBe(false);
    raw.snapshot.recipients.state = "MISSING"; raw.snapshot.recipients.verifiedRouteReference = null;
    expect(review(raw).account.finalRefundCents).toBe(160000);
  });
  it.each([
    ["/snapshot/jurisdiction", "UNKNOWN"], ["/snapshot/jurisdiction", "UNCONFIRMED"],
    ["/snapshot/tenancyRegime", "UNKNOWN"], ["/snapshot/tenancyEndsInFull", null],
  ] as const)("control: unknown scope has no NC fallback: %s=%s", (path, value): void => {
    const raw = ordinaryRequest(); applyFixturePatch(raw, { op: "replace", path, value });
    const result = review(raw);
    expect(result.scopeRequirements.scopeState).toBe("MISSING_FACTS");
    expect(result.scopeRequirements.appliedQuestionIds).toEqual([]);
    expect(result.account.finalRefundCents).toBeNull();
    expect(result.scopeRequirements.requirements.every((r): boolean => r.legalDueDate === null)).toBe(true);
  });
  it("waived item explicit review must block finality", (): void => {
    const raw = ordinaryRequest(); Object.assign(requireElement(raw.snapshot.charges, 0), { choiceState: "WAIVED", chosenAmountCents: 0, reviewRequired: true });
    const result = review(raw);
    expect(item(result).requiresReviewer).toBe(true);
    expect(track(result, "DECISIONS").state).toBe("BLOCKED");
    expect(result.account.finalAccountReady).toBe(false);
  });
  it("owner exclusion unresolved reference must block finality", (): void => {
    const raw = ordinaryRequest();
    requireElement(raw.snapshot.charges, 1).unresolvedQuestionIds = ["audit-owner-basis"];
    raw.snapshot.questions = [openQuestion("audit-owner-basis", ["paint-800"])];
    const result = review(raw);
    expect(item(result, "paint-800").requiresReviewer).toBe(true);
    expect(result.account.finalAccountReady).toBe(false);
  });
  it("explicit open-question item reference is never silently ignored", (): void => {
    const raw = ordinaryRequest(); raw.snapshot.questions = [openQuestion("audit-cost-dispute", ["repair-250"])];
    const result = review(raw);
    expect(questionIds(result)).toContain("audit-cost-dispute");
    expect(item(result).requiresReviewer).toBe(true);
  });
  it("future invoice occurrence cannot certify a current charge", (): void => {
    const raw = ordinaryRequest();
    const proof = raw.snapshot.evidence.find((e): boolean => e.evidenceId === "ev-repair");
    if (proof === undefined) throw new Error("Missing fixture evidence");
    proof.occurredAt = "2026-09-18T12:00:00Z";
    expect(review(raw).account.finalAccountReady).toBe(false);
  });
  it("future occurrence cannot establish the current trigger", (): void => {
    const raw = ordinaryRequest();
    const proof = raw.snapshot.evidence.find((e): boolean => e.evidenceId === "ev-dates");
    if (proof === undefined) throw new Error("Missing fixture evidence");
    proof.occurredAt = "2026-09-18T12:00:00Z";
    expect(review(raw).scopeRequirements.requirements.filter((r): boolean => r.legalDueDate !== null)).toEqual([]);
  });
  it("explicit supersession without repeated item IDs still requires review", (): void => {
    const raw = ordinaryRequest();
    raw.snapshot.evidence.push({ ...requireElement(raw.snapshot.evidence, 3), evidenceId: "audit-revised-repair", sourceVersion: "2", supersedesEvidenceId: "ev-repair", learnedAt: "2026-09-10T12:00:00Z", proposedItemIds: [] });
    expect(item(review(raw)).requiresReviewer).toBe(true);
  });
  it("accepted superseding evidence does not reopen superseded history", (): void => {
    const raw = ordinaryRequest();
    raw.snapshot.evidence.push({ ...requireElement(raw.snapshot.evidence, 3), evidenceId: "audit-revised-repair", sourceVersion: "2", supersedesEvidenceId: "ev-repair", learnedAt: "2026-09-10T12:00:00Z" });
    Object.assign(requireElement(raw.snapshot.charges, 0), { costVersionId: "audit-revised-repair", evidenceIds: ["audit-revised-repair"], vendorCostCents: 20000, supportedAmountCents: 20000, chosenAmountCents: 20000 });
    expect(review(raw).account.finalRefundCents).toBe(165000);
  });
  it("a shared external payment reference cannot prove two settlements", (): void => {
    const raw = ordinaryRequest(); const snapshot = raw.snapshot;
    [1, 2].forEach((index): void => {
      const key = `audit-payment-${index}`; addProof(snapshot, key);
      snapshot.priorRequests.push({ requestId: key, actionKind: "REQUEST_REFUND", targetVersionId: `target-${index}`, payloadFingerprint: `payload-${index}`, amountCents: 50000, state: "SUCCEEDED", approvalIds: [], externalReference: "same-external-payment" });
      snapshot.moneyEvents.push({ eventId: key, canonicalTransactionId: key, sourceEventId: key, kind: "REFUND_SETTLED", status: "SETTLED", amountCents: 50000, occurredAt: "2026-09-10T12:00:00Z", learnedAt: "2026-09-10T12:00:00Z", sourceEvidenceId: key, requestId: key, reversesTransactionId: null, chargeItemId: null });
    });
    expect(review(raw).account.finalAccountReady).toBe(false);
  });
  it("conflicting party records cannot select authority by input order", (): void => {
    const raw = ordinaryRequest(); raw.snapshot.parties.push({ ...requireElement(raw.snapshot.parties, 0), roles: ["OWNER"] });
    const first = review(raw); raw.snapshot.parties.reverse(); const second = review(raw);
    expect(action(first, "prepare:correct-facts").availability).toBe(action(second, "prepare:correct-facts").availability);
  });
  it("known zero related balance cannot hide its explicitly unresolved question", (): void => {
    const raw = ordinaryRequest(); raw.snapshot.otherBalances = [{ balanceId: "audit-related", description: "Unresolved separate balance", amountCents: 0, state: "KNOWN", sourceEvidenceId: "ev-balance", unresolvedQuestionIds: ["audit-related-basis"] }];
    const result = review(raw);
    expect(result.account.finalRefundCents).toBe(160000);
    expect(track(result, "RELATED_ACCOUNT").state).not.toBe("FULFILLED");
  });
});
