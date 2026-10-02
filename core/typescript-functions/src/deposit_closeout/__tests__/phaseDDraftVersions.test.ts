import { describe, expect, it } from "vitest";
import { canonical_json } from "../domain/codec.js";
import { caseIdFor } from "../phase_c/types.js";
import { nativeReview } from "../phase_c/validation.js";
import { approvalValidity } from "../lifecycle/approvals.js";
import { parseWorkflowState } from "../lifecycle/codec.js";
import { applyLifecycleCommand, reconcileWorkflowAfterCaseChange } from "../lifecycle/commands.js";
import { appendWorkflowEvent, projectNativeFacts, projectRequests } from "../lifecycle/events.js";
import { projectPerformance } from "../lifecycle/performance.js";
import { initializeWorkflow } from "../lifecycle/prerequisites.js";
import { prepareStatement, statementBasisCurrent } from "../lifecycle/statements.js";
import type { PureContext, StatementKind, StatementVersionRecord } from "../lifecycle/types.js";
import { RequestHarness, REQUEST_NOW, refundSpec } from "./phaseDRequestsSupport.js";

function fixture(): RequestHarness {
  const h = new RequestHarness();
  h.request.snapshot.depositBalance.amountCents = 200000;
  Object.assign(h.request.snapshot.charges[0]!, {
    vendorCostCents: 40000, supportedAmountCents: 40000, chosenAmountCents: 40000,
  });
  h.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-balance")!.excerpt =
    "Synthetic draft-version fixture: $2,000 held, no prior movements.";
  h.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-repair")!.excerpt =
    "Synthetic draft-version fixture: $400 supported tenant repair, explicitly chosen.";
  h.request.snapshot.interimConditionState = "ACCEPTED";
  h.request.snapshot.interimConditionEvidenceIds = ["ev-extent"];
  h.request.snapshot.interimConditionReason = "Separately accepted synthetic interim qualification.";
  return h;
}

function prepare(h: RequestHarness, kind: StatementKind = "FINAL", supersedesId: string | null = null,
  extra: Partial<PureContext> = {}): StatementVersionRecord {
  const result = applyLifecycleCommand(h.request, [], h.workflow,
    { kind: "PREPARE_STATEMENT", payload: { kind, supersedesId, reason: "Prepare immutable synthetic version." } }, h.ctx(extra));
  h.request = result.request;
  h.workflow = result.workflow;
  return h.workflow.statements.find((entry): boolean => entry.statementId === result.summary.statementId)!;
}

function reduceChoice(h: RequestHarness): void {
  const next = structuredClone(h.request);
  next.snapshot.charges[0]!.chosenAmountCents = 35000;
  const result = reconcileWorkflowAfterCaseChange(h.request, next, [], h.workflow, h.ctx());
  h.request = result.request;
  h.workflow = result.workflow;
}

function dispatch(h: RequestHarness, statementId: string): string {
  return h.admit({ kind: "STATEMENT_DISPATCH", amountCents: null, statementId,
    dispositionKey: "draft-version-dispatch", replacesRequestId: null, reversesTransactionId: null });
}

function status(h: RequestHarness): ReturnType<typeof projectPerformance>["statementDetails"] {
  const request = projectNativeFacts(h.request, h.workflow);
  return projectPerformance(request, nativeReview(request), h.workflow, REQUEST_NOW).statementDetails;
}

function assertNoIssuance(h: RequestHarness): void {
  expect(status(h).every((entry): boolean => !entry.issued)).toBe(true);
  expect(projectNativeFacts(h.request, h.workflow).snapshot.priorStatements.every((entry): boolean =>
    entry.issuedAt === null && entry.issuanceEvidenceIds.length === 0)).toBe(true);
}

const DRAFT_KINDS = ["FINAL", "INTERIM"] as const;

describe("Phase D immutable unissued draft versions", (): void => {
  it.each(DRAFT_KINDS)("replaces a stale unissued %s with the same kind, preserving content, identity and provenance", (kind): void => {
    const h = fixture();
    const old = structuredClone(prepare(h, kind));
    reduceChoice(h);
    expect(statementBasisCurrent(h.request, nativeReview(h.request), h.workflow, old)).toBe(false);
    const before = structuredClone({ request: h.request, workflow: h.workflow });
    const replacement = prepare(h, kind, old.statementId);
    expect(h.workflow.statements).toHaveLength(2);
    expect(h.workflow.statements[0]).toEqual(old);
    expect(replacement.statementId).not.toBe(old.statementId);
    expect(replacement.contentHash).not.toBe(old.contentHash);
    expect(replacement).toMatchObject({ kind, supersedesStatementId: old.statementId });
    expect(old.content.account).toMatchObject({ totalDeductionsCents: 40000, finalRefundCents: 160000 });
    expect(replacement.content.account).toMatchObject({ totalDeductionsCents: 35000, finalRefundCents: 165000 });
    expect(old.renderedText).toContain("Total deductions: $400.00 USD");
    expect(replacement.renderedText).toContain("Total deductions: $350.00 USD");
    expect(replacement.renderedText).toContain("Unpaid final refund: $1,650.00 USD");
    expect(h.workflow.currentStatementId).toBe(replacement.statementId);
    expect(statementBasisCurrent(h.request, nativeReview(h.request), h.workflow, replacement)).toBe(true);
    expect(h.workflow.events).toEqual(before.workflow.events);
    expect(h.workflow.requests).toEqual(before.workflow.requests);
    expect(h.workflow.approvals).toEqual(before.workflow.approvals);
    expect(h.request.snapshot.moneyEvents).toEqual(before.request.snapshot.moneyEvents);
    expect(h.request.snapshot.revision).toBe(before.request.snapshot.revision);
    assertNoIssuance(h);
    expect(parseWorkflowState(canonical_json(h.workflow))).toEqual(h.workflow);

    const repeated = prepare(h, kind, old.statementId, {
      serverNow: "2026-09-19T12:00:00.000Z", basisReviewId: "later-review",
    });
    expect(repeated).toEqual(replacement);
    expect(h.workflow.statements).toEqual([old, replacement]);
    assertNoIssuance(h);
  });

  it.each(DRAFT_KINDS)("permits replacing queued unattempted %s and lets existing reconciliation supersede READY", (kind): void => {
    const h = fixture();
    const old = structuredClone(prepare(h, kind));
    const requestId = dispatch(h, old.statementId);
    const instruction = structuredClone(h.workflow.requests[0]!);
    const approval = structuredClone(h.workflow.approvals[0]!);
    expect(projectRequests(h.workflow)[0]).toMatchObject({ state: "READY", attemptId: null });
    // Even unchanged content is a distinct, explicitly linked version. No request is auto-created.
    const replacement = prepare(h, kind, old.statementId);
    expect(replacement.contentHash).toBe(old.contentHash);
    expect(replacement.statementId).not.toBe(old.statementId);
    expect(h.workflow.statements[0]).toEqual(old);
    expect(h.workflow.requests).toEqual([instruction]);
    expect(h.workflow.approvals).toEqual([approval]);
    expect(projectRequests(h.workflow)[0]).toMatchObject({ requestId, state: "SUPERSEDED", attemptId: null });
    expect(h.workflow.events.at(-1)!.kind).toBe("SUPERSEDED_BEFORE_ATTEMPT");
    expect(approvalValidity(h.request, nativeReview(h.request), h.workflow, approval, REQUEST_NOW).valid).toBe(false);
    expect(() => h.claim(requestId)).toThrow(/READY/);
    const newRequestId = dispatch(h, replacement.statementId);
    expect(newRequestId).not.toBe(requestId);
    expect(projectRequests(h.workflow)[1]).toMatchObject({ requestId: newRequestId, state: "READY", attemptId: null });
    expect(prepare(h, kind, old.statementId)).toEqual(replacement);
    expect(h.workflow.statements).toHaveLength(2);
    assertNoIssuance(h);
  });

  it.each(DRAFT_KINDS)("requires CORRECTIVE for an issued %s; correction itself issues neither version", (kind): void => {
    const h = fixture();
    const old = structuredClone(prepare(h, kind));
    h.settle(dispatch(h, old.statementId), "accepted-dispatch", null);
    expect(status(h)[0]!.issued).toBe(true);
    reduceChoice(h);
    const before = canonical_json({ request: h.request, workflow: h.workflow });
    expect(() => prepare(h, kind, old.statementId)).toThrow(/issued.*CORRECTIVE/);
    expect(canonical_json({ request: h.request, workflow: h.workflow })).toBe(before);
    const corrected = prepare(h, "CORRECTIVE", old.statementId);
    expect(corrected.supersedesStatementId).toBe(old.statementId);
    expect(h.workflow.statements[0]).toEqual(old);
    expect(status(h).map((entry): boolean => entry.issued)).toEqual([true, false]);
  });

  it.each(DRAFT_KINDS.flatMap((kind) =>
    (["CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN", "FAILED"] as const).map((state) => ({ kind, state }))))(
    "rejects silent $kind replacement after $state, without treating an attempt or unaccepted raw result as issuance", ({ kind, state }): void => {
      const h = fixture();
      const old = prepare(h, kind);
      const requestId = dispatch(h, old.statementId);
      const attemptId = h.claim(requestId);
      if (state !== "CLAIMED") h.raw(requestId, "unaccepted-dispatch", state === "FAILED" ? "FAILED" : "SUCCEEDED", null);
      if (state === "ACKNOWLEDGED") {
        appendWorkflowEvent(h.workflow, h.ctx(), requestId, attemptId, null, {
          category: "REQUEST_LIFECYCLE", kind: "ACKNOWLEDGED",
          payload: { instructionHash: h.workflow.requests[0]!.instructionHash },
        });
      }
      if (state === "OUTCOME_UNKNOWN") h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId, attemptId, reason: "Reconcile dispatch." } });
      if (state === "FAILED") h.ingest("unaccepted-dispatch");
      expect(projectRequests(h.workflow)[0]!.state).toBe(state);
      assertNoIssuance(h);
      const before = canonical_json({ request: h.request, workflow: h.workflow });
      expect(() => prepare(h, kind, old.statementId)).toThrow(/attempted.*CORRECTIVE.*reconcil/i);
      expect(canonical_json({ request: h.request, workflow: h.workflow })).toBe(before);
      const corrective = prepare(h, "CORRECTIVE", old.statementId);
      expect(corrective.supersedesStatementId).toBe(old.statementId);
      expect(projectRequests(h.workflow)[0]!.state).toBe(state);
      assertNoIssuance(h);
    });

  it("FINAL after issued INTERIM is an independent duty, not a generic replacement", (): void => {
    const h = fixture();
    const interim = structuredClone(prepare(h, "INTERIM"));
    h.settle(dispatch(h, interim.statementId), "issued-interim", null);
    expect(() => prepare(h, "FINAL", interim.statementId)).toThrow(/same kind/);
    const final = prepare(h, "FINAL");
    expect(final.supersedesStatementId).toBeNull();
    expect(h.workflow.statements[0]).toEqual(interim);
    expect(status(h).map((entry): boolean => entry.issued)).toEqual([true, false]);
  });

  it.each(["CLAIMED", "SUCCEEDED"] as const)("only considers dispatches targeting the linked draft, not another %s statement", (outcome): void => {
    const h = fixture();
    const interim = prepare(h, "INTERIM");
    const requestId = dispatch(h, interim.statementId);
    h.claim(requestId);
    if (outcome === "SUCCEEDED") { h.raw(requestId, "other-statement", "SUCCEEDED", null); h.ingest("other-statement"); }
    const final = prepare(h, "FINAL");
    const replacement = prepare(h, "FINAL", final.statementId);
    expect(replacement.supersedesStatementId).toBe(final.statementId);
    expect(status(h).slice(1).every((entry): boolean => !entry.issued)).toBe(true);
  });

  it("does not mistake an accepted money result linked to a draft for dispatch issuance", (): void => {
    const h = fixture();
    const old = prepare(h);
    h.settle(h.admit(refundSpec(600, "money-not-dispatch", { statementId: old.statementId })), "money-success", 600);
    const replacement = prepare(h, "FINAL", old.statementId);
    expect(replacement.supersedesStatementId).toBe(old.statementId);
    assertNoIssuance(h);
  });

  it("CORRECTIVE still requires an existing linked earlier version and permits unissued predecessors", (): void => {
    const h = fixture();
    expect(() => prepare(h, "CORRECTIVE")).toThrow(/corrective.*earlier/i);
    const old = prepare(h);
    const corrective = prepare(h, "CORRECTIVE", old.statementId);
    expect(corrective.supersedesStatementId).toBe(old.statementId);
    expect(prepare(h, "CORRECTIVE", old.statementId)).toEqual(corrective);
    assertNoIssuance(h);
  });

  it.each(["FINAL", "INTERIM", "CORRECTIVE"] as const)("rejects missing and foreign-case predecessors for %s", (kind): void => {
    const h = fixture();
    const foreign = fixture();
    foreign.request.snapshot.tenancyId = "different-draft-case";
    foreign.request.snapshot.caseId = caseIdFor(foreign.request.snapshot.managementCompanyId, foreign.request.snapshot.tenancyId);
    foreign.workflow = initializeWorkflow(foreign.request, foreign.ctx());
    const foreignStatement = prepare(foreign);
    expect(() => prepare(h, kind, "missing-statement")).toThrow(/earlier/);
    expect(() => prepare(h, kind, foreignStatement.statementId)).toThrow(/earlier/);
    expect(h.workflow.statements).toEqual([]);
  });

  it("rejects a prospective/self reference and preserves the codec's earlier-version invariant", (): void => {
    const h = fixture();
    const prospective = prepareStatement(h.request, nativeReview(h.request), h.workflow,
      { kind: "FINAL", supersedesId: null, reason: "Not yet stored." }, h.ctx());
    expect(() => prepare(h, "FINAL", prospective.statementId)).toThrow(/earlier/);
    const old = prepare(h);
    const corrupt = structuredClone(h.workflow);
    corrupt.statements[0]!.supersedesStatementId = old.statementId;
    expect(() => parseWorkflowState(canonical_json(corrupt))).toThrow(/identity|earlier/);
  });

  it.each([
    ["FINAL", "INTERIM"], ["INTERIM", "FINAL"], ["FINAL", "CORRECTIVE"], ["INTERIM", "CORRECTIVE"],
  ] as const)("rejects a %s draft replacing an incompatible %s version", (kind, oldKind): void => {
    const h = fixture();
    const priorId = oldKind === "CORRECTIVE" ? prepare(h).statementId : null;
    const old = prepare(h, oldKind, priorId);
    const before = canonical_json(h.workflow);
    expect(() => prepare(h, kind, old.statementId)).toThrow(/same kind/);
    expect(canonical_json(h.workflow)).toBe(before);
  });
});
