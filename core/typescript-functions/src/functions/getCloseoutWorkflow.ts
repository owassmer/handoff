import { DcCloseoutCase } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import { loadCurrentReview } from "../deposit_closeout/phase_c/storage.js";
import { identifier, requireCondition } from "../deposit_closeout/phase_c/validation.js";

export const config = { apiName: "getCloseoutWorkflow" };

/**
 * Read the canonical persisted v2 review at its recorded authority time. No edits or current-clock reinterpretation.
 * @param client Platform-injected client; root and complete snapshot are protected by object policies.
 * @param caseId Policy-visible native case ID; not a caller-supplied object or actor.
 * @returns Canonical WorkflowReviewV2 JSON; legacy-only cases must explicitly initialize first.
 */
export default async function getCloseoutWorkflow(client: Client, caseId: string): Promise<string> {
  identifier(caseId, "Case ID");
  const root = await client(DcCloseoutCase).fetchOne(caseId);
  requireCondition(root.caseId === caseId, "The case lookup returned a different case.");
  const stored = await loadCurrentReview(client, root);
  requireCondition(stored.workflowReviewJson !== undefined, "Initialize the closeout workflow before requesting its v2 review.");
  return stored.workflowReviewJson;
}
