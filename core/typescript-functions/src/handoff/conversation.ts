import { HandoffMessage, HandoffWorkPlan } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import { createEditBatch } from "@osdk/functions";
import { addActivity, command, wasApplied } from "./activity.js";
import { currentCaller, guardWorkspace, loadAgentWork, loadHandoff, one, inWorkspace, type HandoffEdit } from "./records.js";
import { nextRevision, reference, requireHandoff, whole, words } from "./values.js";
import { caseTime } from "./clock.js";

/** Acknowledge discussion promptly; the shared coordinator reasons on its next durable turn. */
export async function discussHandoff(client: Client, handoffId: string, message: string, commandId: string,
  currentUserId: string, expectedPlanRevision?: string): Promise<HandoffEdit[]> {
  words(message, "Message", 8000);
  if (expectedPlanRevision !== undefined) whole(expectedPlanRevision, "Plan version");
  const caller = await currentCaller(client, currentUserId), { handoff, workspace } = await loadHandoff(client, handoffId, caller, "work");
  const intent = command(workspace.workspaceId, handoffId, handoffId, commandId, caller.id, "Message sent", { handoffId, message, expectedPlanRevision });
  if (await wasApplied(client, workspace, caller, intent)) return [];
  if (expectedPlanRevision !== undefined) {
    const plan = handoff.workPlanId ? await one(client(HandoffWorkPlan).where({ workPlanId: { $eq: handoff.workPlanId } })) : undefined;
    requireHandoff(plan && plan.revision === expectedPlanRevision, "The proposal has changed. Refresh it before discussing this version.");
    inWorkspace(plan, workspace, caller);
  }
  const work = await loadAgentWork(client, handoff, workspace, caller), now = new Date().toISOString(), revision = nextRevision(handoff.revision);
  const stamp = caseTime(work, now);
  const batch = createEditBatch<HandoffEdit>(client), messageId = reference("message", workspace.workspaceId, commandId, "operator");
  batch.create(HandoffMessage, { workspaceId: workspace.workspaceId, readerIds: [...workspace.readerIds!], handoffId, messageId,
    title: `${caller.name} to Handoff`, body: message, direction: "Operator", purpose: "Discussion", status: "Received", createdAt: stamp,
    workPlanId: handoff.workPlanId, externalReference: commandId });
  batch.update(work, { status: "Ready to continue", title: "Consider the message", nextStep: "Handoff will consider your message with the current work.",
    nextWakeAt: now, nextBusinessAt: undefined, updatedAt: now, ...(work.businessTime ? { businessTime: stamp } : {}), operationKey: `message:${messageId}` });
  batch.update(handoff, { revision, nextStep: "Handoff is considering your message." });
  guardWorkspace(batch, workspace, commandId);
  addActivity(batch, intent, [...workspace.readerIds!], "Message received", "Your message is saved for Handoff to consider. It is not an acceptance of work.", revision, stamp);
  return batch.getEdits();
}
