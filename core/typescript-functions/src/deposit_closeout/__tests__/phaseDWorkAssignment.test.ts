import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import assignCloseoutWork from "../../functions/assignCloseoutWork.js";
import recordCloseoutRelatedTask from "../../functions/recordCloseoutRelatedTask.js";
import recheckCloseoutCase from "../../functions/recheckCloseoutCase.js";
import { normalize_timestamp } from "../domain/datetime.js";
import type { RequirementResult, ReviewRequest } from "../domain/types.js";
import { applyChange, parseChange } from "../phase_c/changes.js";
import { loadCurrentReview } from "../phase_c/storage.js";
import { serialize } from "../phase_c/validation.js";
import { nextInputs, present, rootUpdate, type TestState } from "./phaseCTestSupport.js";
import { ACTOR, NOW, WHY, act, initialized, storageRequest } from "./phaseDStorageSupport.js";

beforeEach((): void => { vi.useFakeTimers(); vi.setSystemTime(new Date(NOW)); });
afterEach((): void => { vi.useRealTimers(); });

interface AssignmentPayload {
  requirementKey: string;
  assigneePartyId: string;
  internalTargetAt: string | null;
  reason: string;
}
interface AssignmentCase {
  state: TestState;
  requirement: RequirementResult;
  payload: AssignmentPayload;
}

/** Real initializer/storage/review path; only SDK IO is replaced by the shared test PK store. */
async function assignmentCase(request: ReviewRequest = storageRequest()): Promise<AssignmentCase> {
  request.snapshot.recipients.state = "MISSING";
  const state = await initialized(request);
  const stored = await loadCurrentReview(state.store.client, state.root);
  const nativeKeys = new Set(stored.review.result.scopeRequirements.requirements.map((entry): string => entry.requirementKey));
  const requirement = present(present(stored.workflowReview).result.scopeRequirements.requirements
    .find((entry): boolean => !nativeKeys.has(entry.requirementKey) && entry.responsibleRole === "MANAGER"));
  const assignee = present(stored.request.snapshot.parties.find((party): boolean =>
    party.roles.includes(requirement.responsibleRole) && party.principalId === ACTOR));
  expect(state.root.workflowVersion).toBe("2");
  expect(nativeKeys.has(requirement.requirementKey)).toBe(false);
  return { state, requirement, payload: { requirementKey: requirement.requirementKey,
    assigneePartyId: assignee.partyId, internalTargetAt: "2026-09-21T12:00:00Z", reason: WHY } };
}

function expectAssignmentProjection(state: TestState, payload: AssignmentPayload): void {
  const row = [...state.store.data.values()].find((entry): boolean =>
    entry.$apiName === "DcRequirement" && entry.requirementKey === payload.requirementKey);
  expect(row).toMatchObject({ assigneePartyId: payload.assigneePartyId, internalTargetAtIso: payload.internalTargetAt,
    isCurrent: true, caseRevision: state.root.revision });
}

describe("Phase D effective requirements remain assignable through the existing C wrapper", (): void => {
  it("assigns a v2-only key in one root batch and preserves its sidecar/projection across C changes and recheck", async (): Promise<void> => {
    const { state: before, requirement, payload } = await assignmentCase();
    const previousRevision = present(before.root.revision);
    let state = await act(before, assignCloseoutWork, payload, "assign-v2-requirement");
    expect(rootUpdate(state.edits).obj).toBe(before.root);
    expect(state.edits.filter((edit): boolean => edit.type === "updateObject" && edit.obj.$apiName === "DcCloseoutCase")).toHaveLength(1);
    expect(state.edits.filter((edit): boolean => edit.type === "createObject" && edit.obj.apiName === "DcReviewSnapshot")).toHaveLength(1);
    expect(state.edits.filter((edit): boolean => edit.type === "createObject" && edit.obj.apiName === "DcExecutionEvent")).toHaveLength(1);
    expect(state.edits.filter((edit): boolean => edit.type === "updateObject" && edit.obj.$apiName === "DcRequirement"
      && "requirementKey" in edit.properties && edit.properties.requirementKey === payload.requirementKey)).toMatchObject([{ properties: {
      assigneePartyId: payload.assigneePartyId, internalTargetAtIso: payload.internalTargetAt, isCurrent: true,
    } }]);
    const assigned = await loadCurrentReview(state.store.client, state.root);
    expect(assigned.workAssignments).toEqual([{ ...payload, assignedBy: ACTOR, assignedAt: normalize_timestamp(NOW) }]);
    expect(assigned.workflowReview?.result.scopeRequirements.requirements.find((entry): boolean => entry.requirementKey === payload.requirementKey))
      .toMatchObject({ internalTargetAt: payload.internalTargetAt, legalDueDate: requirement.legalDueDate, state: requirement.state });
    expect(assigned.review.result.scopeRequirements.requirements.some((entry): boolean => entry.requirementKey === payload.requirementKey)).toBe(false);
    expectAssignmentProjection(state, payload);
    const sidecar = { json: state.snapshot.workAssignmentsJson, hash: state.snapshot.workAssignmentsHash };

    state = await act(state, recordCloseoutRelatedTask, { taskId: "unrelated-v2-assignment-task", description: "Independent follow-up",
      state: "OPEN", responsibleRole: "MANAGER", completionEvidenceIds: [] }, "unrelated-c-change");
    expectAssignmentProjection(state, payload);
    state = nextInputs(state, await recheckCloseoutCase(state.store.client, state.root.caseId, ACTOR, "recheck-v2-assignment", present(state.root.revision)));
    const rechecked = await loadCurrentReview(state.store.client, state.root);
    expect(rechecked.workAssignments).toEqual(assigned.workAssignments);
    expect({ json: state.snapshot.workAssignmentsJson, hash: state.snapshot.workAssignmentsHash }).toEqual(sidecar);
    expect(rechecked.workflowReview?.result.scopeRequirements.requirements.find((entry): boolean => entry.requirementKey === payload.requirementKey))
      .toMatchObject({ internalTargetAt: payload.internalTargetAt, legalDueDate: requirement.legalDueDate });
    expect(state.root.workflowVersion).toBe("2");
    expect(state.root.revision).toBe("5");
    expectAssignmentProjection(state, payload);
    expect(await assignCloseoutWork(state.store.client, state.root.caseId, ACTOR, "assign-v2-requirement", previousRevision, serialize(payload))).toEqual([]);
  });

  it.each([
    ["unknown requirement", { requirementKey: "not-in-current-review" }, /current review/],
    ["out-of-case party", { assigneePartyId: "other-case-manager" }, /Party ID.*this case/],
    ["wrong role", { assigneePartyId: "demo-accountant" }, /responsible role/],
  ] as const)("rejects %s without changing accepted state", async (_label, patch, message): Promise<void> => {
    const { state, payload } = await assignmentCase();
    const accepted = [...state.store.data.entries()];
    await expect(assignCloseoutWork(state.store.client, state.root.caseId, ACTOR, "reject-assignment", present(state.root.revision), serialize({ ...payload, ...patch })))
      .rejects.toThrow(message);
    expect([...state.store.data.entries()]).toEqual(accepted);
  });

  it.each(["inactive", "unaccepted-source"] as const)("still checks a separate assignee's %s evidence/membership", async (invalid): Promise<void> => {
    const request = storageRequest();
    const manager = present(request.snapshot.parties.find((party): boolean => party.roles.includes("MANAGER")));
    const source = present(request.snapshot.evidence.find((entry): boolean => entry.evidenceId === "ev-authority"));
    request.snapshot.evidence.push({ ...source, evidenceId: "assignee-proof", externalRecordId: "assignee-proof-record",
      associationAccepted: invalid !== "unaccepted-source" });
    request.snapshot.parties.push({ ...manager, partyId: "separate-assignee",
      effectiveUntil: invalid === "inactive" ? "2026-09-17" : null, evidenceIds: ["assignee-proof"] });
    const { state, payload } = await assignmentCase(request);
    await expect(assignCloseoutWork(state.store.client, state.root.caseId, ACTOR, "reject-assignee", present(state.root.revision),
      serialize({ ...payload, assigneePartyId: "separate-assignee" })))
      .rejects.toThrow(invalid === "inactive" ? /not currently active/ : /accepted, current case evidence/);
  });

  it("does not accept caller-supplied effective requirements as payload or permission overrides", async (): Promise<void> => {
    const { state, requirement, payload } = await assignmentCase();
    const reads = state.store.reads.length;
    await expect(assignCloseoutWork(state.store.client, state.root.caseId, ACTOR, "payload-override", present(state.root.revision),
      serialize({ ...payload, requirements: [requirement] }))).rejects.toThrow(/must contain exactly/);
    expect(state.store.reads).toHaveLength(reads);
  });

  it("keeps native fallback for callers without effective requirements but respects an explicitly empty trusted list", async (): Promise<void> => {
    const { state, payload } = await assignmentCase();
    const stored = await loadCurrentReview(state.store.client, state.root);
    const nativeRequirement = present(stored.review.result.scopeRequirements.requirements.find((entry): boolean => entry.responsibleRole === "MANAGER"));
    const nativeChange = parseChange("ASSIGN_WORK", serialize({ ...payload, requirementKey: nativeRequirement.requirementKey }));
    expect(applyChange(stored.request, [], nativeChange, ACTOR, NOW, false).workAssignments).toHaveLength(1);
    expect(() => applyChange(stored.request, [], parseChange("ASSIGN_WORK", serialize(payload)), ACTOR, NOW, false)).toThrow(/current review/);
    expect(() => applyChange(stored.request, [], nativeChange, ACTOR, NOW, false, [])).toThrow(/current review/);
  });
});
