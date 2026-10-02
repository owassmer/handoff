import { DcCloseoutCase } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import { canonical_json } from "../domain/codec.js";
import { loadCurrentReview } from "../phase_c/storage.js";
import { identifier, requireCondition, validateRoot } from "../phase_c/validation.js";
import {
  parseIntentSpec,
  previewIntent,
  serializeWorkspace,
  workspaceContract,
  WorkspaceError,
  workspaceMetadata,
} from "./codec.js";
import type { WorkspaceReview } from "./types.js";
import { QUEUE_PROPERTY_KEYS } from "./queue.js";

/** Capture values, not the mutable SDK instance. Include scope, version, clock and access generation. */
function generation(root: Osdk.Instance<DcCloseoutCase>): string {
  const keys = [
    "caseId",
    "managementCompanyId",
    "environmentId",
    "tenancyId",
    "homeId",
    "revision",
    "currentReviewId",
    "currentStatementId",
    "inputHash",
    "projectionVersion",
    "workflowVersion",
    "reviewClock",
    "createdBy",
    "updatedBy",
    "updatedAt",
    "readerIds",
    "adminIds",
    "managerIds",
    "accountantIds",
    ...QUEUE_PROPERTY_KEYS,
  ] as const;
  return canonical_json({
    primaryKey: root.$primaryKey,
    fields: keys.map((key): unknown => root[key] ?? null),
  });
}

/** Policy-protected root -> canonical snapshot -> root check. Not a database snapshot or lock. */
export async function readWorkspace(
  client: Client,
  caseId: string,
  intentSpecJson?: string,
): Promise<string> {
  identifier(caseId, "Case ID");
  const spec =
    intentSpecJson === undefined
      ? undefined
      : workspaceContract("INVALID_INTENT_SPEC", (): ReturnType<typeof parseIntentSpec> =>
          parseIntentSpec(intentSpecJson),
        );
  const root = await client(DcCloseoutCase).fetchOne(caseId);
  requireCondition(root.caseId === caseId, "The case lookup returned a different case.");
  const initialGeneration = generation(root);
  const stored = await loadCurrentReview(client, root);
  const workflow = stored.workflow ?? null;
  const review: WorkspaceReview =
    stored.workflowReview === undefined
      ? { kind: "LEGACY_BASE", value: stored.review }
      : { kind: "WORKFLOW_V2", value: stored.workflowReview };
  // The native envelope stays local: never cast the extended v2 account as native input.
  const intentPreview = previewIntent(stored.request, stored.review, workflow, spec);
  const metadata = workspaceContract(
    "INVALID_WORKSPACE",
    (): ReturnType<typeof workspaceMetadata> =>
      workspaceMetadata(stored.request, review, workflow, stored.workAssignments, {
        caseRevision: root.revision!,
        currentReviewId: root.currentReviewId!,
        projectionVersion: root.projectionVersion === "1" ? "1" : "0",
        snapshotCreatedAt: stored.createdAt!,
        readAt: new Date().toISOString(),
      }),
  );
  const json = workspaceContract("INVALID_WORKSPACE", (): string =>
    serializeWorkspace({
      metadata,
      request: stored.request,
      workAssignments: stored.workAssignments,
      workflow,
      review,
      intentPreview,
    }),
  );
  // Fail rather than mixing generations or silently refreshing a target the caller did not select.
  const finalRoot = await client(DcCloseoutCase).fetchOne(caseId);
  if (generation(finalRoot) !== initialGeneration) {
    throw new WorkspaceError(
      "GENERATION_CHANGED",
      "The case changed during this read. Retry the whole workspace query.",
    );
  }
  validateRoot(finalRoot);
  return json;
}
