/** Fixed pure fixtures. This helper is NOT a transaction/concurrency or runtime harness. */
import { baseRequest } from "./fixtures/helpers.js";
import type { ReviewRequest } from "../domain/types.js";
import { nativeReview } from "../phase_c/validation.js";
import { decideApproval } from "../lifecycle/approvals.js";
import { versionedRoute, workflowScope } from "../lifecycle/materiality.js";
import { prepareStatement } from "../lifecycle/statements.js";
import { applyRequestCommand, projectRequests, projectNativeFacts } from "../lifecycle/requests.js";
import type { LifecycleCommand, OperationIntentSpec, PureContext, WorkflowStateV2 } from "../lifecycle/types.js";

export const REQUEST_ACTOR = "c47a52a0-0048-4607-931f-f4df283ae7c4";
export const REQUEST_NOW = "2026-09-18T12:00:00.000Z";
export function requestContext(id: string, patch: Partial<PureContext> = {}): PureContext {
  return { actorId: REQUEST_ACTOR, serverNow: REQUEST_NOW, commandId: id, isAdministrator: true,
    basisReviewId: "demo-native-review-1", ...patch };
}
export function requestFixture(): { request: ReviewRequest; workflow: WorkflowStateV2 } {
  const request = structuredClone(baseRequest());
  request.ruleReleaseId = "NC_SYNTHETIC_REVIEW_V1";
  request.snapshot.parties.forEach((party): void => {
    if (party.roles.includes("MANAGER") || party.roles.includes("ACCOUNTANT")) party.principalId = REQUEST_ACTOR;
  });
  request.snapshot.charges = [request.snapshot.charges[0]!];
  Object.assign(request.snapshot.charges[0]!, { vendorCostCents: 400, supportedAmountCents: 400, chosenAmountCents: 400 });
  request.snapshot.questions = [];
  request.snapshot.depositBalance.amountCents = 2000;
  request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-balance")!.excerpt =
    "Fixed pure request fixture: 2000 cents held, no prior movements.";
  request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-repair")!.excerpt =
    "Fixed pure request fixture: 400 cents actual supported tenant repair, explicitly chosen.";
  const scope = workflowScope(request);
  const input = { partyIds: ["demo-resident"], state: "VERIFIED" as const, method: "DEMO_OUTBOX" as const,
    routeReference: "demo-route-no-real-destination", evidenceIds: ["ev-recipients"] };
  const workflow: WorkflowStateV2 = { ...scope, schemaVersion: "2.0.0", mode: "SIMULATED", initializedBy: REQUEST_ACTOR,
    initializedAt: "2026-09-18T10:00:00.000Z", businessClock: request.reviewClock,
    statementInstructions: versionedRoute(scope, "STATEMENT", input), refundInstructions: versionedRoute(scope, "REFUND", input),
    statements: [], approvals: [], requests: [], events: [], currentStatementId: null };
  return { request, workflow };
}
export function refundSpec(amountCents: number = 600, dispositionKey: string = "installment-1", patch: Partial<OperationIntentSpec> = {}): OperationIntentSpec {
  return { kind: "REFUND", amountCents, dispositionKey, statementId: null, replacesRequestId: null,
    reversesTransactionId: null, ...patch };
}
export class RequestHarness {
  request: ReviewRequest;
  workflow: WorkflowStateV2;
  private commandNumber = 0;
  constructor() { const pair = requestFixture(); this.request = pair.request; this.workflow = pair.workflow; }
  ctx(patch: Partial<PureContext> = {}): PureContext { return requestContext(`request-test-${++this.commandNumber}`, patch); }
  approve(spec: OperationIntentSpec = refundSpec()): string {
    const approval = decideApproval(this.request, nativeReview(projectNativeFacts(this.request, this.workflow)), this.workflow,
      { intent: spec, decision: "APPROVED" }, this.ctx());
    this.workflow.approvals.push(approval);
    return approval.approvalId;
  }
  run(command: LifecycleCommand, patch: Partial<PureContext> = {}): ReturnType<typeof applyRequestCommand> {
    const result = applyRequestCommand(this.request, this.workflow, command, this.ctx(patch));
    this.request = result.request; this.workflow = result.workflow;
    return result;
  }
  admit(spec: OperationIntentSpec = refundSpec()): string {
    const approvalId = this.approve(spec);
    return String(this.run({ kind: "REQUEST_OPERATION", payload: { approvalId } }).summary.requestId);
  }
  claim(requestId: string): string {
    this.run({ kind: "CLAIM_REQUEST", payload: { requestId } });
    return projectRequests(this.workflow).find((entry): boolean => entry.requestId === requestId)!.attemptId!;
  }
  raw(requestId: string, sourceEventId: string, outcome: "SUCCEEDED" | "FAILED" | "RETURNED" = "SUCCEEDED",
    amountCents: number | null = 600, occurredAt: string | null = null): void {
    const attemptId = projectRequests(this.workflow).find((entry): boolean => entry.requestId === requestId)!.attemptId!;
    this.run({ kind: "GENERATE_SIMULATED_RESULT", payload: { requestId, attemptId, sourceEventId, outcome, amountCents, occurredAt } });
  }
  ingest(sourceEventId: string, patch: Partial<PureContext> = {}): ReturnType<typeof applyRequestCommand> {
    return this.run({ kind: "INGEST_RESULT", payload: { sourceEventId } }, patch);
  }
  settle(requestId: string, sourceEventId: string = "success-1", amountCents: number | null = 600): void {
    this.claim(requestId); this.raw(requestId, sourceEventId, "SUCCEEDED", amountCents); this.ingest(sourceEventId);
  }
  prepare(kind: "FINAL" | "INTERIM" | "CORRECTIVE" = "FINAL", supersedesId: string | null = null): string {
    const statement = prepareStatement(this.request, nativeReview(projectNativeFacts(this.request, this.workflow)), this.workflow,
      { kind, supersedesId, reason: "Synthetic statement for exact approval." }, this.ctx());
    this.workflow.statements.push(statement); this.workflow.currentStatementId = statement.statementId;
    return statement.statementId;
  }
  account(): ReturnType<typeof nativeReview>["result"]["account"] {
    return nativeReview(projectNativeFacts(this.request, this.workflow)).result.account;
  }
}
