import { HandoffDecision, HandoffMessage, HandoffParty } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import { createEditBatch } from "@osdk/functions";
import { addActivity, command, wasApplied } from "./activity.js";
import { currentCaller, guardWorkspace, inWorkspace, loadAgentWork, loadHandoff, loadPlan, one,
  type HandoffEdit } from "./records.js";
import { acceptedContent, planDraft } from "./workPlans.js";
import type { WorkPlanDraft } from "./reasoner.js";
import { nextRevision, reference, requireHandoff, words } from "./values.js";

interface WorkCorrespondence {
  title: string; body: string; replyTitle: string; replyBody: string; externalReference: string;
}

/** The demo correspondence service acknowledges receipt only; it never reports completed work or sends a network request. */
export function requestWorkCorrespondence(mode: string, operationKey: string,
  provider: Osdk.Instance<HandoffParty>, proposal: WorkPlanDraft): WorkCorrespondence {
  requireHandoff(mode === "demo", "Correspondence is not available for this workspace's way of working.");
  requireHandoff(provider.partyId === proposal.providerPartyId, "The work request must go to the accepted provider.");
  const amount = (value: string): string => `${BigInt(value) / 100n}.${(BigInt(value) % 100n).toString().padStart(2, "0")} ${proposal.currency}`;
  const requirements = proposal.fixedRequirements.length ? `\nRequirements:\n${proposal.fixedRequirements.map((item) => `- ${item}`).join("\n")}` : "";
  return {
    title: `Arrange ${proposal.title}`,
    body: `${words(provider.name, "Provider name", 200)}, please arrange the following accepted work.\n\n${proposal.desiredOutcome}\n\n${proposal.scope.map((item) => `- ${item}`).join("\n")}\n\nEstimated cost: ${amount(proposal.estimatedCostCents)}. Maximum accepted budget: ${amount(proposal.budgetCents)}.${requirements}\n\nPlease confirm availability and the proposed appointment. Changes to the accepted scope or budget need a new agreement.`,
    replyTitle: "Work request received",
    replyBody: "The work request has been received. Scheduling confirmation is still pending.",
    externalReference: reference("correspondence", provider.partyId, operationKey),
  };
}

/** One logical correspondence request per accepted decision, regardless of command retries. */
export async function continueWork(client: Client, handoffId: string, commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  const caller = await currentCaller(client, currentUserId);
  const { handoff, workspace } = await loadHandoff(client, handoffId, caller, "work");
  const intent = command(workspace.workspaceId, handoffId, handoffId, commandId, caller.id, "Work requested", { handoffId });
  if (await wasApplied(client, workspace, caller, intent)) return [];
  requireHandoff(handoff.workPlanId, "Accept a work plan before arranging the work.");
  const { plan } = await loadPlan(client, handoff.workPlanId, caller, "work");
  requireHandoff(plan.status === "Accepted" && plan.acceptedDecisionId, "Accept a work plan before arranging the work.");
  const [decision, work, provider] = await Promise.all([
    one(client(HandoffDecision).where({ decisionId: { $eq: plan.acceptedDecisionId } })),
    loadAgentWork(client, handoff, workspace, caller),
    one(client(HandoffParty).where({ partyId: { $eq: words(plan.providerPartyId, "Provider reference", 160) } })),
  ]);
  requireHandoff(decision && provider, "The accepted decision and provider must be available before continuing.");
  inWorkspace(decision, workspace, caller);
  inWorkspace(provider, workspace, caller);
  requireHandoff(decision.handoffId === handoffId && decision.workPlanId === plan.workPlanId
    && decision.acceptedRevision === plan.revision && decision.contentJson === acceptedContent(plan),
  "The work plan no longer matches its accepted decision. Review the handoff before continuing.");
  const operationKey = `continue:${decision.decisionId}`;
  requireHandoff(work.operationKey === operationKey && ["Ready to continue", "Waiting for provider"].includes(work.status ?? ""),
    "The handoff's next step does not match the accepted work plan.");
  const requestId = reference("message", workspace.workspaceId, operationKey, "request");
  const replyId = reference("message", workspace.workspaceId, operationKey, "acknowledgement");
  const [request, reply] = await Promise.all([
    one(client(HandoffMessage).where({ messageId: { $eq: requestId } })),
    one(client(HandoffMessage).where({ messageId: { $eq: replyId } })),
  ]);
  const correspondence = requestWorkCorrespondence(workspace.mode!, operationKey, provider, planDraft(plan));
  if (request || reply) {
    requireHandoff(request && reply && work.status === "Waiting for provider", "The provider correspondence needs to be checked before continuing.");
    [request, reply].forEach((message) => {
      inWorkspace(message, workspace, caller);
      requireHandoff(message.handoffId === handoffId && message.workPlanId === plan.workPlanId
        && message.recipientPartyId === provider.partyId && message.externalReference === correspondence.externalReference,
      "The provider correspondence does not match the accepted work.");
    });
    requireHandoff(request.body === correspondence.body && reply.body === correspondence.replyBody
      && request.direction === "Outgoing" && reply.direction === "Incoming"
      && request.status === "Sent" && reply.status === "Received", "The provider correspondence needs to be checked before continuing.");
    return [];
  }
  requireHandoff(work.status === "Ready to continue", "The provider correspondence needs to be checked before continuing.");
  const now = new Date().toISOString(), revision = nextRevision(handoff.revision);
  const batch = createEditBatch<HandoffEdit>(client);
  const shared = { workspaceId: workspace.workspaceId, readerIds: [...workspace.readerIds!], handoffId,
    workPlanId: plan.workPlanId, recipientPartyId: provider.partyId, createdAt: now, externalReference: correspondence.externalReference };
  batch.create(HandoffMessage, { ...shared, messageId: requestId, title: correspondence.title,
    body: correspondence.body, direction: "Outgoing", status: "Sent" });
  batch.create(HandoffMessage, { ...shared, messageId: replyId, title: correspondence.replyTitle,
    body: correspondence.replyBody, direction: "Incoming", status: "Received" });
  batch.update(handoff, { revision, physicalProgress: "Waiting for provider", nextStep: "Wait for the provider to confirm an appointment." });
  batch.update(work, { title: "Await the provider's appointment", status: "Waiting for provider",
    nextStep: "Wait for the provider to confirm an appointment.", updatedAt: now,
    nextWakeAt: new Date(Date.parse(now) + 24 * 60 * 60 * 1000).toISOString() });
  // These loaded objects bind the correspondence to the same acceptance throughout the Action.
  batch.update(plan, { acceptedDecisionId: decision.decisionId, status: "Accepted" });
  guardWorkspace(batch, workspace, commandId);
  addActivity(batch, intent, shared.readerIds, "Provider contacted", "The accepted work request was received. An appointment has not yet been confirmed.", revision, now);
  return batch.getEdits();
}
