import { HandoffActivity, HandoffWorkPlan } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import { currentCaller, inWorkspace, loadHandoff, one } from "../handoff/records.js";
import { details, parseDetails, reference, requireHandoff, whole, words } from "../handoff/values.js";

export const config = { apiName: "getHandoffChange" };

export interface HandoffChange {
  version: "2";
  commandId: string;
  status: "Saved" | "Not found";
  subjectId: string | null;
  kind: string | null;
  payloadHash: string | null;
  resultRevision: string | null;
  at: string | null;
}

/**
 * Check whether the signed-in person's change was saved without sending it again.
 * @param client - The signed-in connection.
 * @param handoffId - The handoff the person was reviewing.
 * @param commandId - The reference kept when the change was sent.
 * @returns The saved change confirmation, or Not found when no activity exists.
 */
export default async function getHandoffChange(client: Client, handoffId: string, commandId: string): Promise<string> {
  words(commandId, "Request reference", 160);
  const caller = await currentCaller(client);
  const { handoff, workspace } = await loadHandoff(client, handoffId, caller, "read");
  const activityId = reference("activity", workspace.workspaceId, commandId);
  const activity = await one(client(HandoffActivity).where({ activityId: { $eq: activityId } }));
  if (!activity) {
    const absent: HandoffChange = { version: "2", commandId, status: "Not found", subjectId: null,
      kind: null, payloadHash: null, resultRevision: null, at: null };
    return JSON.stringify(absent);
  }
  inWorkspace(activity, workspace, caller);
  requireHandoff(activity.activityId === activityId && activity.commandId === commandId
    && activity.actorId === caller.id && activity.handoffId === handoff.handoffId
    && ["Work budget changed", "Work plan changed", "Work plan accepted", "Message sent", "Document received"].includes(activity.kind ?? ""),
  "This saved change is not available for this handoff and signed-in person.");
  const subjectId = words(activity.subjectId, "Work plan reference", 160);
  if (activity.kind === "Message sent" || activity.kind === "Document received") requireHandoff(subjectId === handoffId, "The message belongs to a different handoff.");
  else {
    const plan = await one(client(HandoffWorkPlan).where({ workPlanId: { $eq: subjectId } }));
    requireHandoff(plan && plan.handoffId === handoff.handoffId, "The saved change does not belong to this handoff's work plan.");
    inWorkspace(plan, workspace, caller);
  }
  const stored = details(parseDetails(words(activity.detail, "Activity details", 16000), "Activity details", 16000),
    ["version", "payloadHash", "summary"], ["trace"], "Activity details");
  const payloadHash = words(stored.payloadHash, "Saved change confirmation", 64);
  requireHandoff(stored.version === "1" && /^[a-f0-9]{64}$/.test(payloadHash),
    "The saved change could not be checked. Ask your team to review it.");
  words(stored.summary, "Activity summary", 4000);
  const resultRevision = whole(activity.resultRevision, "Saved revision");
  const at = words(activity.occurredAt, "Saved time", 40);
  requireHandoff(!Number.isNaN(Date.parse(at)), "The saved change needs a valid date.");
  const saved: HandoffChange = { version: "2", commandId, status: "Saved", subjectId,
    kind: activity.kind!, payloadHash, resultRevision, at };
  return JSON.stringify(saved);
}
