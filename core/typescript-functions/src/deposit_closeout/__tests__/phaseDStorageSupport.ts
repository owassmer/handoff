/** SDK edit-array integration fixtures, not a permissions or contention model. */
import type { Client } from "@osdk/client";
import type { OntologyEdit } from "../phase_c/types.js";
import type { ReviewRequest } from "../domain/types.js";
import type { OperationIntentSpec, WorkflowStateV2 } from "../lifecycle/types.js";
import { from_json } from "../domain/codec.js";
import { parseWorkflowState } from "../lifecycle/codec.js";
import { BOOTSTRAP_ACTOR_ID, caseIdFor } from "../phase_c/types.js";
import { serialize } from "../phase_c/validation.js";
import initializeCloseoutWorkflow from "../../functions/initializeCloseoutWorkflow.js";
import decideCloseoutApproval from "../../functions/decideCloseoutApproval.js";
import requestCloseoutOperation from "../../functions/requestCloseoutOperation.js";
import claimCloseoutRequest from "../../functions/claimCloseoutRequest.js";
import simulateCloseoutResult from "../../functions/simulateCloseoutResult.js";
import ingestCloseoutResult from "../../functions/ingestCloseoutResult.js";
import { nextInputs, opened, present, type TestState } from "./phaseCTestSupport.js";
import { requestFixture, refundSpec, REQUEST_NOW } from "./phaseDRequestsSupport.js";

export const ACTOR = BOOTSTRAP_ACTOR_ID;
export const NOW = REQUEST_NOW;
export const WHY = "Reviewed synthetic workflow integration evidence.";
export type Wrapper = (client: Client, caseId: string, actorId: string, commandId: string,
  expectedRevision: string, payloadJson: string) => Promise<OntologyEdit[]>;
export function storageRequest(): ReviewRequest {
  const request = requestFixture().request;
  request.snapshot.caseId = caseIdFor(request.snapshot.managementCompanyId, request.snapshot.tenancyId);
  return request;
}
export function current(state: TestState): ReviewRequest { return from_json("ReviewRequest", present(state.snapshot.requestJson)); }
export function workflow(state: TestState): WorkflowStateV2 { return parseWorkflowState(present(state.snapshot.workflowStateJson)); }
export async function act(state: TestState, fn: Wrapper, payload: unknown, id: string): Promise<TestState> {
  return nextInputs(state, await fn(state.store.client, state.root.caseId, ACTOR, id, present(state.root.revision), serialize(payload)));
}
export async function initialized(request: ReviewRequest = storageRequest()): Promise<TestState> {
  return act(await opened(request), initializeCloseoutWorkflow, {}, "init");
}
export async function approved(state: TestState, spec: OperationIntentSpec = refundSpec(), id: string = "approval"): Promise<TestState> {
  return act(state, decideCloseoutApproval, { intent: spec, decision: "APPROVED" }, id);
}
export async function requested(state: TestState, spec: OperationIntentSpec = refundSpec(), id: string = "request"): Promise<TestState> {
  const a = await approved(state, spec, `${id}-approval`);
  return act(a, requestCloseoutOperation, { approvalId: workflow(a).approvals.at(-1)!.approvalId }, id);
}
export async function settled(state: TestState, requestId: string, source: string, amountCents: number | null): Promise<TestState> {
  let next = await act(state, claimCloseoutRequest, { requestId }, `${source}-claim`);
  const attemptId = present(workflow(next).events.find((event): boolean => event.requestId === requestId && event.kind === "ATTEMPT_CLAIMED")?.attemptId ?? undefined);
  next = await act(next, simulateCloseoutResult, { requestId, attemptId, sourceEventId: source, outcome: "SUCCEEDED", amountCents, occurredAt: null }, `${source}-raw`);
  return act(next, ingestCloseoutResult, { sourceEventId: source }, `${source}-ingest`);
}
