import { instant } from "./deliveryContracts.js";
import { HandoffCase, HandoffProperty, HandoffWorkPlan, HandoffDecision, HandoffMessage, HandoffActivity } from "@ontology/sdk";
import { attachmentsOf } from "./email.js";
import type { Client } from "@osdk/client";
import { activitySummary } from "./activity.js";
import type { HandoffList, HandoffWorkspaceView, WorkPlanView } from "./contracts.js";
import { access, bounded, currentCaller, handoffUnchanged, workspaceUnchanged, inWorkspace, loadAgentWork, loadHandoff, loadWorkspace, one } from "./records.js";
import { loadDetails } from "./workDetails.js";
import { planSelections } from "./proposal.js";
import { deliveryViews } from "./deliveryViews.js";
import { planDraft, readAcceptedContent } from "./workPlans.js";
import { cents, details, parseDetails, requireHandoff, whole, words } from "./values.js";

/** The first 25 handoffs, ordered by their stable reference. No caller-supplied identity is accepted. */
export async function handoffList(client: Client, workspaceId: string): Promise<HandoffList> {
  const caller = await currentCaller(client);
  const workspace = await loadWorkspace(client, workspaceId, caller, "read");
  const page = await client(HandoffCase).where({ workspaceId: { $eq: workspaceId } })
    .fetchPage({ $pageSize: 25, $orderBy: { handoffId: "asc" } });
  page.data.forEach((handoff) => inWorkspace(handoff, workspace, caller));
  const propertyIds = [...new Set(page.data.map((handoff) => words(handoff.propertyId, "Property reference", 160)))];
  const properties = propertyIds.length ? await bounded(client(HandoffProperty).where({
    propertyId: { $in: propertyIds }, workspaceId: { $eq: workspaceId },
  }), 25) : [];
  properties.forEach((property) => inWorkspace(property, workspace, caller));
  const latestWorkspace = await loadWorkspace(client, workspaceId, caller, "read");
  requireHandoff(workspaceUnchanged(workspace, latestWorkspace), "The workspace changed while it was being read. Refresh it to continue.");
  return { version: "2", workspace: { id: workspaceId, name: words(workspace.name, "Workspace name", 200), mode: workspace.mode! },
    handoffs: page.data.map((handoff) => {
      const property = properties.find((candidate) => candidate.propertyId === handoff.propertyId);
      requireHandoff(property, "A handoff's property is not available in this workspace.");
      return { id: handoff.handoffId, title: words(handoff.title, "Handoff title", 200),
        propertyName: words(property.name, "Property name", 200), physicalProgress: words(handoff.physicalProgress, "Physical progress", 200),
        financialProgress: words(handoff.financialProgress, "Financial progress", 200), nextStep: words(handoff.nextStep, "Next step"),
        revision: whole(handoff.revision, "Handoff revision") };
    }) };
}

/** A bounded view assembled from scoped business records; not an authoritative JSON store. */
export async function workspaceView(client: Client, handoffId: string): Promise<HandoffWorkspaceView> {
  const caller = await currentCaller(client);
  const { handoff, workspace } = await loadHandoff(client, handoffId, caller, "read");
  const scope = { handoffId: { $eq: handoffId }, workspaceId: { $eq: workspace.workspaceId } };
  const [world, work, plan, decisions, messages, activity, delivery] = await Promise.all([
    loadDetails(client, handoff, workspace, caller),
    loadAgentWork(client, handoff, workspace, caller),
    handoff.workPlanId ? one(client(HandoffWorkPlan).where({ workPlanId: { $eq: handoff.workPlanId } })) : Promise.resolve(undefined),
    bounded(client(HandoffDecision).where(scope), 25),
    client(HandoffMessage).where(scope).fetchPage({ $pageSize: 50, $orderBy: { createdAt: "desc", messageId: "asc" } }).then((page) => page.data),
    client(HandoffActivity).where(scope).fetchPage({ $pageSize: 100, $orderBy: { occurredAt: "desc", activityId: "asc" } }).then((page) => page.data),
    deliveryViews(client, workspace, caller, handoff),
  ]);
  [...decisions, ...messages, ...activity, ...(plan ? [plan] : [])].forEach((record) => inWorkspace(record, workspace, caller));
  requireHandoff(!handoff.workPlanId || (plan && plan.handoffId === handoffId), "The handoff's current work plan could not be found.");
  const workPlan: WorkPlanView | null = plan ? { id: plan.workPlanId, revision: whole(plan.revision, "Plan revision"),
    status: words(plan.status, "Plan status", 100), ...planDraft(plan), acceptedDecisionId: plan.acceptedDecisionId ?? null, selections: planSelections(plan), fixedProviderPartyId: plan.fixedProviderPartyId ?? null } : null;
  if (plan?.acceptedDecisionId) requireHandoff(decisions.some((decision) => decision.decisionId === plan.acceptedDecisionId), "The work plan's acceptance could not be found.");
  const latest = await loadHandoff(client, handoffId, caller, "read");
  requireHandoff(handoffUnchanged(handoff, latest.handoff) && workspaceUnchanged(workspace, latest.workspace),
    "The handoff changed while it was being read. Refresh it to continue.");
  return {
    version: "2", ...delivery, workspace: { id: workspace.workspaceId, name: words(workspace.name, "Workspace name", 200), mode: workspace.mode! },
    handoff: { id: handoffId, title: words(handoff.title, "Handoff title", 200), goal: words(handoff.goal, "Handoff goal"),
      businessDate: words(handoff.businessDate, "Business date", 40), physicalProgress: words(handoff.physicalProgress, "Physical progress", 200),
      financialProgress: words(handoff.financialProgress, "Financial progress", 200), nextStep: words(handoff.nextStep, "Next step"),
      revision: whole(handoff.revision, "Handoff revision"), operativeDecisionId: handoff.operativeDecisionId ?? plan?.acceptedDecisionId ?? null },
    property: { id: world.property.propertyId, name: words(world.property.name, "Property name", 200),
      address: words(world.property.address, "Property address", 500), description: words(world.property.description, "Property description", 2000) },
    tenancy: { id: world.tenancy.tenancyId, title: words(world.tenancy.title, "Tenancy title", 200),
      startDate: words(world.tenancy.startDate, "Tenancy start date", 40), endDate: world.tenancy.endDate ?? null, endingKind: world.tenancy.endingKind ?? "Tenancy ending" },
    parties: world.parties.map((party) => ({ id: party.partyId, name: words(party.name, "Party name", 200),
      kind: words(party.kind, "Party kind", 100), description: words(party.description, "Party description", 2000) })),
    agreements: world.agreements.map((agreement) => ({ id: agreement.agreementId, title: words(agreement.title, "Agreement title", 200),
      termsText: words(agreement.termsText, "Agreement terms"), sourceDocumentId: words(agreement.sourceDocumentId, "Agreement document reference", 160) })),
    obligations: world.obligations.map((obligation) => ({ id: obligation.obligationId, title: words(obligation.title, "Obligation title", 200),
      description: words(obligation.description, "Obligation description", 1000), status: words(obligation.status, "Obligation status", 100) })),
    documents: [...world.documents, ...(world.supportingFiles ?? [])].map((document) => ({ id: document.documentId, title: words(world.originalTitles?.get(document.documentId) ?? document.title, "Document title", 200),
      ...(document.sourceKind === "Original" || document.sourceKind === "Prepared" ? { sourceKind: document.sourceKind } : {}),
      ...(document.sourceDocumentIds?.length ? { sourceDocumentIds: [...document.sourceDocumentIds] } : {}),
      text: words(document.text, "Document text", 24000), kind: document.kind!, sourceVersion: document.sourceVersion ?? "1",
      mimeType: document.mimeType ?? null, availableFrom: document.availableFrom ?? null, mediaSetRid: document.mediaSetRid ?? null, mediaItemRid: document.mediaItemRid ?? null,
      pageStart: document.pageStart ?? null, pageEnd: document.pageEnd ?? null })),
    workPlan,
    decisions: decisions.sort((a, b) => (a.decidedAt ? instant(a.decidedAt) : "").localeCompare(b.decidedAt ? instant(b.decidedAt) : "")).map((decision) => {
      const content = readAcceptedContent(words(decision.contentJson, "Accepted work", 100000));
      requireHandoff(content.handoffId === handoffId && content.workPlanId === decision.workPlanId
        && content.revision === decision.acceptedRevision, "The accepted work details do not match this handoff.");
      return { id: decision.decisionId, title: words(decision.title, "Decision title", 200),
        workPlanId: words(decision.workPlanId, "Work plan reference", 160), revision: whole(decision.acceptedRevision, "Accepted revision"),
        by: decision.decidedBy === caller.id ? caller.name : "Workspace decision maker", at: words(decision.decidedAt, "Decision time", 40),
        budgetCents: cents(content.budgetCents), currency: words(content.currency, "Currency", 3),
        content: { ...planDraft(content), id: content.workPlanId, revision: content.revision, status: "Accepted",
          acceptedDecisionId: decision.decisionId, selections: content.selections, fixedProviderPartyId: content.fixedProviderPartyId } };
    }),
    messages: messages.sort((a, b) => (a.createdAt ? instant(a.createdAt) : "").localeCompare(b.createdAt ? instant(b.createdAt) : "") || a.messageId.localeCompare(b.messageId))
      .map((message) => ({ id: message.messageId, title: words(message.title, "Message title", 200),
        body: words(message.body, "Message text", 60000), recipientPartyId: message.recipientPartyId ?? null, purpose: message.purpose ?? "Correspondence",
        jobId: message.jobId ?? null, replyToMessageId: message.replyToMessageId ?? null, senderPartyId: message.senderPartyId ?? null,
        attachmentDocumentIds: attachmentsOf(message.detailsJson),
        direction: words(message.direction, "Message direction", 100), status: words(message.status, "Message status", 100),
        createdAt: words(message.createdAt, "Message time", 40) })),
    activity: activity.sort((a, b) => (a.occurredAt ? instant(a.occurredAt) : "").localeCompare(b.occurredAt ? instant(b.occurredAt) : "") || a.activityId.localeCompare(b.activityId))
      .map((entry) => ({ id: entry.activityId, title: words(entry.title, "Activity title", 200), detail: activitySummary(entry), at: words(entry.occurredAt, "Activity time", 40) })),
    agent: { status: words(work.status, "Work status", 100), nextStep: words(work.nextStep, "Next step"), updatedAt: words(work.updatedAt, "Work update time", 40), nextWakeAt: work.nextWakeAt ?? null },
    permissions: access(workspace, caller),
  };
}
