import type { Client } from "@osdk/client";
import { UserFacingError } from "@osdk/functions";
import { parseDetails } from "../handoff/values.js";
import {
  createFoundryWorkModel,
  recommendWork,
  validateWorkContext,
} from "../handoff/reasoner.js";

export const config = { apiName: "recommendPropertyWork" };

/**
 * Recommend property work without creating, updating, approving or ordering anything.
 * @param client - Platform-injected client used only for the managed model proxy.
 * @param contextJson - JSON matching WorkContext, assembled from this handoff's accessible evidence.
 * @returns The validated WorkPlanDraft as JSON. Internal execution evidence is not returned.
 */
export default async function recommendPropertyWork(
  client: Client,
  contextJson: string,
): Promise<string> {
  if (contextJson.length > 400000) {
    throw new UserFacingError("Choose a smaller set of work details and documents.");
  }
  const context = validateWorkContext(parseDetails(contextJson, "Work details"));
  // Rune's managed import assigned the only model the default (empty) alias.
  const model = await createFoundryWorkModel(client, { modelAlias: "workReasoner" });
  const result = await recommendWork(context, model);
  return JSON.stringify(result.draft);
}
