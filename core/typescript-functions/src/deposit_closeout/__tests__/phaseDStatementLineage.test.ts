import { describe, expect, it } from "vitest";
import { canonical_json } from "../domain/codec.js";
import { nativeReview } from "../phase_c/validation.js";
import { parseWorkflowState } from "../lifecycle/codec.js";
import { applyLifecycleCommand, reconcileWorkflowAfterCaseChange } from "../lifecycle/commands.js";
import { appendWorkflowEvent, projectNativeFacts, projectRequests } from "../lifecycle/events.js";
import { projectPerformance } from "../lifecycle/performance.js";
import { prepareStatement, statementBasisCurrent } from "../lifecycle/statements.js";
import type { PureContext, StatementKind, StatementVersionRecord } from "../lifecycle/types.js";
import { RequestHarness, REQUEST_NOW } from "./phaseDRequestsSupport.js";

function fixture(): RequestHarness {
  const h = new RequestHarness();
  h.request.snapshot.depositBalance.amountCents = 200000;
  Object.assign(h.request.snapshot.charges[0]!, {
    vendorCostCents: 40000, supportedAmountCents: 40000, chosenAmountCents: 40000,
  });
  h.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-balance")!.excerpt =
    "Synthetic lineage fixture: $2,000 held, no prior movements.";
  h.request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-repair")!.excerpt =
    "Synthetic lineage fixture: $400 supported tenant repair, explicitly chosen.";
  h.request.snapshot.interimConditionState = "ACCEPTED";
  h.request.snapshot.interimConditionEvidenceIds = ["ev-extent"];
  h.request.snapshot.interimConditionReason = "Separately accepted synthetic interim qualification.";
  return h;
}

function prepare(h: RequestHarness, kind: StatementKind = "FINAL", supersedesId: string | null = null,
  extra: Partial<PureContext> = {}): StatementVersionRecord {
  const result = applyLifecycleCommand(h.request, [], h.workflow,
    { kind: "PREPARE_STATEMENT", payload: { kind, supersedesId, reason: "Synthetic lineage regression." } }, h.ctx(extra));
  h.request = result.request;
  h.workflow = result.workflow;
  return h.workflow.statements.find((entry): boolean => entry.statementId === result.summary.statementId)!;
}

function changeChoice(h: RequestHarness, amount: number = 35000): void {
  const next = structuredClone(h.request);
  next.snapshot.charges[0]!.chosenAmountCents = amount;
  const result = reconcileWorkflowAfterCaseChange(h.request, next, [], h.workflow, h.ctx());
  h.request = result.request;
  h.workflow = result.workflow;
}

function dispatch(h: RequestHarness, statementId: string): string {
  return h.admit({ kind: "STATEMENT_DISPATCH", amountCents: null, statementId,
    dispositionKey: "lineage-dispatch", replacesRequestId: null, reversesTransactionId: null });
}

function issued(h: RequestHarness): boolean[] {
  const request = projectNativeFacts(h.request, h.workflow);
  return projectPerformance(request, nativeReview(request), h.workflow, REQUEST_NOW)
    .statementDetails.map((entry): boolean => entry.issued);
}

function rejectsWithoutMutation(h: RequestHarness, kind: StatementKind, supersedesId: string | null, error: RegExp): void {
  const before = canonical_json({ request: h.request, workflow: h.workflow });
  const statements = structuredClone(h.workflow.statements);
  // Both the pure builder and authorized orchestration must enforce the rule.
  expect(() => prepareStatement(h.request, nativeReview(h.request), h.workflow,
    { kind, supersedesId, reason: "Rejected lineage regression." }, h.ctx())).toThrow(error);
  expect(() => prepare(h, kind, supersedesId)).toThrow(error);
  expect(canonical_json({ request: h.request, workflow: h.workflow })).toBe(before);
  expect(h.workflow.statements.map((entry) => [entry.statementId, entry.contentHash, entry.renderedText]))
    .toEqual(statements.map((entry) => [entry.statementId, entry.contentHash, entry.renderedText]));
}

const DRAFT_KINDS = ["FINAL", "INTERIM"] as const;

describe("Phase D authoritative statement lineage (pure, simulated only)", (): void => {
  it.each(DRAFT_KINDS)("changed issued %s cannot omit its predecessor; a linked correction preserves history", (kind): void => {
    const h = fixture();
    const old = structuredClone(prepare(h, kind));
    h.settle(dispatch(h, old.statementId), "issued-original", null);
    changeChoice(h);
    expect(statementBasisCurrent(h.request, nativeReview(h.request), h.workflow, old)).toBe(false);
    rejectsWithoutMutation(h, kind, null, /issued.*CORRECTIVE/);
    const before = structuredClone({ requests: h.workflow.requests, events: h.workflow.events, money: h.request.snapshot.moneyEvents });
    const correction = prepare(h, "CORRECTIVE", old.statementId);
    expect(correction).toMatchObject({ kind: "CORRECTIVE", supersedesStatementId: old.statementId });
    expect(correction.content.account).toMatchObject({ totalDeductionsCents: 35000, finalRefundCents: 165000 });
    expect(h.workflow.currentStatementId).toBe(correction.statementId);
    expect(h.workflow.statements[0]).toEqual(old);
    expect(old.renderedText).toContain("Total deductions: $400.00 USD");
    expect(correction.renderedText).toContain("Total deductions: $350.00 USD");
    expect(issued(h)).toEqual([true, false]);
    expect({ requests: h.workflow.requests, events: h.workflow.events, money: h.request.snapshot.moneyEvents }).toEqual(before);
    expect(parseWorkflowState(canonical_json(h.workflow))).toEqual(h.workflow);
  });

  it.each(DRAFT_KINDS.flatMap((kind) =>
    (["CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN", "FAILED"] as const).map((state) => ({ kind, state }))))(
    "changed $kind cannot omit a $state predecessor; raw success alone is not issuance", ({ kind, state }): void => {
      const h = fixture();
      const old = structuredClone(prepare(h, kind));
      const requestId = dispatch(h, old.statementId);
      const attemptId = h.claim(requestId);
      if (state !== "CLAIMED") h.raw(requestId, "raw-not-issued", state === "FAILED" ? "FAILED" : "SUCCEEDED", null);
      if (state === "ACKNOWLEDGED") {
        appendWorkflowEvent(h.workflow, h.ctx(), requestId, attemptId, null, {
          category: "REQUEST_LIFECYCLE", kind: "ACKNOWLEDGED",
          payload: { instructionHash: h.workflow.requests[0]!.instructionHash },
        });
      }
      if (state === "OUTCOME_UNKNOWN") h.run({ kind: "RECORD_OUTCOME_UNKNOWN", payload: { requestId, attemptId, reason: "Reconcile dispatch." } });
      if (state === "FAILED") h.ingest("raw-not-issued");
      changeChoice(h);
      expect(projectRequests(h.workflow)[0]!.state).toBe(state);
      rejectsWithoutMutation(h, kind, null, /attempted.*CORRECTIVE.*reconcil/i);
      expect(h.workflow.statements).toEqual([old]);
      expect(issued(h)).toEqual([false]);
      expect(h.request.snapshot.priorStatements[0]!.issuedAt).toBeNull();
    });

  it.each([false, true])("unchanged issued FINAL reuses its exact record, including linked draft history: %s", (linked): void => {
    const h = fixture();
    const first = prepare(h);
    if (linked) { changeChoice(h); prepare(h, "FINAL", first.statementId); }
    const old = structuredClone(h.workflow.statements.at(-1)!);
    h.settle(dispatch(h, old.statementId), "issued-current", null);
    const history = structuredClone(h.workflow.statements);
    const events = structuredClone(h.workflow.events);
    const repeated = prepare(h, "FINAL", null, { serverNow: "2026-09-19T12:00:00.000Z", basisReviewId: "later-review" });
    expect(repeated).toEqual(old);
    expect(h.workflow.statements).toEqual(history);
    expect(h.workflow.events).toEqual(events);
    expect(h.workflow.currentStatementId).toBe(old.statementId);
    expect(statementBasisCurrent(h.request, nativeReview(h.request), h.workflow, repeated)).toBe(true);
  });

  it("unchanged attempted FINAL is also reuse, not a new version or artificial correction", (): void => {
    const h = fixture();
    const old = structuredClone(prepare(h));
    const requestId = dispatch(h, old.statementId);
    h.claim(requestId);
    const events = structuredClone(h.workflow.events);
    expect(prepare(h)).toEqual(old);
    expect(h.workflow.statements).toEqual([old]);
    expect(h.workflow.events).toEqual(events);
    expect(projectRequests(h.workflow)[0]!.state).toBe("CLAIMED");
    expect(issued(h)).toEqual([false]);
  });

  it("issued CORRECTIVE protects the final duty and later corrections link through prepared corrections", (): void => {
    const h = fixture();
    const original = structuredClone(prepare(h));
    h.settle(dispatch(h, original.statementId), "issued-first", null);
    changeChoice(h);
    const correction = structuredClone(prepare(h, "CORRECTIVE", original.statementId));
    h.settle(dispatch(h, correction.statementId), "issued-correction", null);
    expect(prepare(h, "CORRECTIVE", original.statementId)).toEqual(correction);
    changeChoice(h, 30000);
    rejectsWithoutMutation(h, "FINAL", null, /issued.*CORRECTIVE/);
    rejectsWithoutMutation(h, "CORRECTIVE", original.statementId, /latest issued.*linked/);
    const prepared = structuredClone(prepare(h, "CORRECTIVE", correction.statementId));
    changeChoice(h, 25000);
    const latest = prepare(h, "CORRECTIVE", prepared.statementId);
    expect(latest.supersedesStatementId).toBe(prepared.statementId);
    expect(latest.content.account.totalDeductionsCents).toBe(25000);
    expect(h.workflow.statements.slice(0, 3)).toEqual([original, correction, prepared]);
    expect(issued(h)).toEqual([true, true, false, false]);
    expect(parseWorkflowState(canonical_json(h.workflow))).toEqual(h.workflow);
  });

  it("cannot resurrect an ancient exact FINAL match past an issued correction", (): void => {
    const h = fixture();
    const original = structuredClone(prepare(h));
    h.settle(dispatch(h, original.statementId), "old-final", null);
    changeChoice(h);
    const correction = structuredClone(prepare(h, "CORRECTIVE", original.statementId));
    h.settle(dispatch(h, correction.statementId), "later-correction", null);
    changeChoice(h, 40000);
    expect(statementBasisCurrent(h.request, nativeReview(h.request), h.workflow, original)).toBe(true);
    rejectsWithoutMutation(h, "FINAL", null, /issued.*CORRECTIVE/);
    expect(h.workflow.currentStatementId).toBe(correction.statementId);
    expect(h.workflow.statements).toEqual([original, correction]);
  });

  it.each(DRAFT_KINDS)("an irrelevant unattempted %s draft cannot bypass more recent issued lineage", (kind): void => {
    const h = fixture();
    const draft = structuredClone(prepare(h, kind));
    changeChoice(h);
    const later = structuredClone(prepare(h, kind));
    h.settle(dispatch(h, later.statementId), "issued-later", null);
    // This also exactly matches the ancient unissued draft's materiality.
    changeChoice(h, 40000);
    rejectsWithoutMutation(h, kind, null, /issued.*CORRECTIVE/);
    rejectsWithoutMutation(h, kind, draft.statementId, /issued.*CORRECTIVE/);
    rejectsWithoutMutation(h, "CORRECTIVE", draft.statementId, /latest issued.*linked/);
    const correction = prepare(h, "CORRECTIVE", later.statementId);
    expect(correction.supersedesStatementId).toBe(later.statementId);
    expect(h.workflow.statements.slice(0, 2)).toEqual([draft, later]);
    expect(issued(h)).toEqual([false, true, false]);
  });

  it("an unrelated interim draft is not a predecessor for correction of an issued final account", (): void => {
    const h = fixture();
    const interim = prepare(h, "INTERIM");
    const final = prepare(h);
    h.settle(dispatch(h, final.statementId), "issued-final", null);
    changeChoice(h);
    rejectsWithoutMutation(h, "CORRECTIVE", interim.statementId, /latest issued.*linked/);
    expect(prepare(h, "CORRECTIVE", final.statementId).supersedesStatementId).toBe(final.statementId);
  });

  it.each(["CLAIMED", "SUCCEEDED"] as const)("first FINAL after %s INTERIM is an independent duty with no predecessor", (state): void => {
    const h = fixture();
    const interim = structuredClone(prepare(h, "INTERIM"));
    const id = dispatch(h, interim.statementId);
    if (state === "CLAIMED") h.claim(id);
    else h.settle(id, "issued-interim", null);
    changeChoice(h);
    const final = prepare(h);
    expect(final).toMatchObject({ kind: "FINAL", supersedesStatementId: null });
    expect(h.workflow.statements[0]).toEqual(interim);
    expect(issued(h)).toEqual([state === "SUCCEEDED", false]);
    expect(statementBasisCurrent(h.request, nativeReview(h.request), h.workflow, final)).toBe(true);
  });

  it("an unrelated current INTERIM does not hide older final-duty issuance", (): void => {
    const h = fixture();
    const final = prepare(h);
    h.settle(dispatch(h, final.statementId), "issued-final", null);
    const interim = prepare(h, "INTERIM");
    expect(h.workflow.currentStatementId).toBe(interim.statementId);
    changeChoice(h);
    rejectsWithoutMutation(h, "FINAL", null, /issued.*CORRECTIVE/);
    expect(prepare(h, "CORRECTIVE", final.statementId).supersedesStatementId).toBe(final.statementId);
  });

  it.each(DRAFT_KINDS.flatMap((kind) => [false, true].map((explicit) => ({ kind, explicit }))))(
    "unattempted $kind draft replacement remains allowed, explicit link: $explicit", ({ kind, explicit }): void => {
      const h = fixture();
      const draft = structuredClone(prepare(h, kind));
      const requestId = dispatch(h, draft.statementId);
      changeChoice(h);
      const replacement = prepare(h, kind, explicit ? draft.statementId : null);
      expect(replacement).toMatchObject({ kind, supersedesStatementId: explicit ? draft.statementId : null });
      expect(replacement.contentHash).not.toBe(draft.contentHash);
      expect(h.workflow.statements[0]).toEqual(draft);
      expect(projectRequests(h.workflow)[0]).toMatchObject({ requestId, state: "SUPERSEDED", attemptId: null });
      expect(issued(h)).toEqual([false, false]);
      expect(prepare(h, kind, explicit ? draft.statementId : null)).toEqual(replacement);
      expect(h.workflow.statements).toHaveLength(2);
    });

  it("dedup does not excuse supplied missing, prospective/self, or wrong-kind references", (): void => {
    const h = fixture();
    const interim = prepare(h, "INTERIM");
    const final = structuredClone(prepare(h));
    h.settle(dispatch(h, final.statementId), "issued-current", null);
    rejectsWithoutMutation(h, "FINAL", "missing-version", /missing earlier/);
    rejectsWithoutMutation(h, "FINAL", interim.statementId, /same kind/);
    rejectsWithoutMutation(h, "FINAL", final.statementId, /issued.*CORRECTIVE/);
    rejectsWithoutMutation(h, "CORRECTIVE", null, /corrective.*earlier/i);
    expect(prepare(h)).toEqual(final);
  });

  it("late acceptance issues only the linked predecessor, never its prepared correction", (): void => {
    const h = fixture();
    const old = structuredClone(prepare(h));
    const id = dispatch(h, old.statementId);
    h.claim(id);
    h.raw(id, "late-original", "SUCCEEDED", null);
    changeChoice(h);
    rejectsWithoutMutation(h, "FINAL", null, /attempted.*CORRECTIVE/);
    const correction = structuredClone(prepare(h, "CORRECTIVE", old.statementId));
    expect(issued(h)).toEqual([false, false]);
    h.ingest("late-original");
    expect(issued(h)).toEqual([true, false]);
    expect(h.workflow.statements).toEqual([old, correction]);
    expect(h.workflow.currentStatementId).toBe(correction.statementId);
    expect(h.request.snapshot.moneyEvents).toEqual([]);
  });
});
