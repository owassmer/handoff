import { HandoffWorkPlan, HandoffDecision } from "@ontology/sdk";
import type { Client } from "@osdk/client";
import { createEditBatch } from "@osdk/functions";
import { addActivity, command, wasApplied } from "./activity.js";
import { currentCaller, guardWorkspace, loadAgentWork, loadHandoff, loadPlan, one, type HandoffEdit, type Plan } from "./records.js";
import { loadDetails } from "./workDetails.js";
import type { WorkPlanDraft } from "./reasoner.js";
import { cents, details, digest, nextRevision, orderedJson, parseDetails, reference, requireHandoff, whole, wordList, words } from "./values.js";
import { materialBasis, planSelections, readSelections, selectedCost, validateSelection, type Proposal } from "./proposal.js";
import { loadDeliveryRecords } from "./deliveryRecords.js";
import { caseTime } from "./clock.js";
import type { WorkPlanChange } from "./contracts.js";

/** Notice, discussion and scheduled continuation all use the same coordinator. */
export async function preparePlan(client: Client, handoffId: string, commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  const { coordinateHandoff } = await import("./coordinator.js");
  return coordinateHandoff(client, handoffId, commandId, currentUserId);
}
export function planDraft(plan: Partial<WorkPlanDraft>): WorkPlanDraft {
  const estimatedCostCents = cents(plan.estimatedCostCents), budgetCents = cents(plan.budgetCents);
  requireHandoff(BigInt(budgetCents) >= BigInt(estimatedCostCents), "The work budget must cover its estimated cost.");
  const currency = words(plan.currency, "Currency", 3);
  requireHandoff(/^[A-Z]{3}$/.test(currency), "The work plan needs a three-letter currency code.");
  return { title: words(plan.title, "Plan title", 160), summary: words(plan.summary, "Plan summary", 2000),
    desiredOutcome: words(plan.desiredOutcome, "Desired outcome", 1000), scope: wordList(plan.scope, "Proposed work", 48, 1, 1000),
    estimatedCostCents, budgetCents, currency, fixedRequirements: wordList(plan.fixedRequirements, "Fixed requirements", 32, 0, 1000),
    rationale: words(plan.rationale, "Plan explanation", 3000), sourceDocumentIds: wordList(plan.sourceDocumentIds, "Supporting documents", 32, 1),
    providerPartyId: words(plan.providerPartyId, "Provider reference", 160) };
}
/** Old acceptances remain byte-for-byte meaningful; only new reviewed selections use version two. */
export function acceptedContent(plan: Plan): string {
  return orderedJson({ version: plan.selectionJson ? "2" : "1", handoffId: plan.handoffId, workPlanId: plan.workPlanId,
    revision: whole(plan.revision, "Plan revision"), basisRevision: whole(plan.basisRevision, "Handoff revision"), ...planDraft(plan),
    ...(plan.selectionJson ? { selections: planSelections(plan), sourceBasis: plan.sourceBasis,
      fixedProviderPartyId: plan.fixedProviderPartyId ?? null } : {}) });
}
export interface AcceptedWork extends WorkPlanDraft {
  version: string; handoffId: string; workPlanId: string; revision: string; basisRevision: string;
  selections: Proposal["selections"]; fixedProviderPartyId: string | null;
}
export function readAcceptedContent(value: string): AcceptedWork {
  const row = details(parseDetails(value, "Accepted work", 100000),
    ["version", "handoffId", "workPlanId", "revision", "basisRevision", "title", "summary", "desiredOutcome", "scope", "estimatedCostCents", "budgetCents", "currency", "fixedRequirements", "rationale", "sourceDocumentIds", "providerPartyId"],
    ["selections", "sourceBasis", "fixedProviderPartyId"], "Accepted work");
  requireHandoff(row.version === "1" || row.version === "2", "This accepted work format is not supported.");
  // planDraft validates every business field; the cast does not bypass its runtime validation.
  const draft = planDraft(row as unknown as Partial<WorkPlanDraft>);
  return { ...draft, version: row.version, handoffId: words(row.handoffId, "Handoff", 160), workPlanId: words(row.workPlanId, "Work plan", 160),
    revision: whole(row.revision, "Accepted version"), basisRevision: whole(row.basisRevision, "Handoff version"),
    selections: row.version === "2" ? readSelections(row.selections) : [],
    fixedProviderPartyId: row.fixedProviderPartyId == null ? null : words(row.fixedProviderPartyId, "Required provider", 160) };
}
export function readPlanChange(json: string): WorkPlanChange {
  const row = details(parseDetails(json, "Work plan change"), [], ["budgetCents", "selections", "fixedRequirements", "fixedProviderPartyId"], "Work plan change");
  requireHandoff(Object.keys(row).length > 0, "Describe a change to the work plan.");
  return { ...(row.budgetCents === undefined ? {} : { budgetCents: cents(row.budgetCents) }),
    ...(row.selections === undefined ? {} : { selections: readSelections(row.selections) }),
    ...(row.fixedRequirements === undefined ? {} : { fixedRequirements: wordList(row.fixedRequirements, "Requirements", 32, 0, 1000) }),
    ...(row.fixedProviderPartyId === undefined ? {} : { fixedProviderPartyId: row.fixedProviderPartyId === null ? null : words(row.fixedProviderPartyId, "Required provider", 160) }) };
}

/** Precise edits recalculate the same proposal without a compulsory model call. */
export async function changePlan(client: Client, workPlanId: string, expectedRevision: string, budgetCents: string | undefined,
  commandId: string, currentUserId: string, changesJson?: string): Promise<HandoffEdit[]> {
  whole(expectedRevision, "Plan revision");
  requireHandoff((budgetCents !== undefined) !== (changesJson !== undefined), "Provide either a budget or a structured work change.");
  const changes = changesJson === undefined ? { budgetCents: cents(budgetCents) } : readPlanChange(changesJson);
  const caller = await currentCaller(client, currentUserId);
  const { plan, handoff, workspace } = await loadPlan(client, workPlanId, caller, "decide", false);
  const kind = changesJson === undefined ? "Work budget changed" : "Work plan changed";
  const payload = changesJson === undefined ? { workPlanId, expectedRevision, budgetCents } : { workPlanId, expectedRevision, changes };
  const intent = command(workspace.workspaceId, workPlanId, handoff.handoffId, commandId, caller.id, kind, payload);
  if (await wasApplied(client, workspace, caller, intent)) return [];
  requireHandoff(handoff.workPlanId === workPlanId && plan.revision === expectedRevision, "The work plan has changed. Refresh it before changing the proposal.");
  requireHandoff(plan.status === "Ready" || plan.status === "Accepted", "This work plan cannot currently be changed.");
  const [world, delivery, work] = await Promise.all([loadDetails(client, handoff, workspace, caller), loadDeliveryRecords(client, workspace, caller, handoff), loadAgentWork(client, handoff, workspace, caller)]);
  const draft = planDraft(plan), selections = changes.selections ?? planSelections(plan);
  if (selections.length) {
    draft.scope = [...new Set(selections.map((line) => line.scope))];
    if (changes.selections) {
      draft.title = "Proposed property work";
      draft.summary = "Carry out the selected scope using the reviewed quoted work below.";
      draft.desiredOutcome = "Complete the selected scope while preserving the stated requirements.";
      const reasons = selections.map((line) => line.reason).join("\n");
      draft.rationale = reasons.length <= 3000 ? reasons : "The reasons for each selection are shown alongside its quoted work.";
    }
    draft.estimatedCostCents = selectedCost(selections, delivery.quotes, draft.currency);
    draft.sourceDocumentIds = [...new Set([...draft.sourceDocumentIds, ...selections.map((line) => delivery.quotes.find((quote) => quote.quoteId === line.quoteId)!.sourceDocumentId!)])];
  }
  draft.budgetCents = changes.budgetCents ?? draft.budgetCents;
  draft.fixedRequirements = changes.fixedRequirements ?? draft.fixedRequirements;
  requireHandoff((handoff.fixedRequirements ?? []).every((requirement) => draft.fixedRequirements.includes(requirement)), "Keep the handoff's explicit requirements in the work plan.");
  const fixedProviderPartyId = changes.fixedProviderPartyId === undefined ? plan.fixedProviderPartyId : changes.fixedProviderPartyId ?? undefined;
  if (fixedProviderPartyId) requireHandoff(world.parties.some((party) => party.partyId === fixedProviderPartyId), "Choose a provider known to this handoff.");
  if (selections.length) validateSelection({ ...draft, selections, fixedProviderPartyId }, delivery.quotes);
  planDraft(draft);
  const revision = nextRevision(plan.revision), handoffRevision = nextRevision(handoff.revision), now = new Date().toISOString();
  const stamp = caseTime(work, now);
  const batch = createEditBatch<HandoffEdit>(client), fork = plan.status === "Accepted";
  const nextPlanId = fork ? reference("plan", workspace.workspaceId, handoff.handoffId, digest(payload)) : plan.workPlanId;
  const props = { ...draft, revision: fork ? "1" : revision, basisRevision: handoffRevision, sourceBasis: materialBasis(handoff, workspace, world),
    ...(selections.length ? { selectionJson: orderedJson(selections) } : {}), fixedProviderPartyId };
  if (fork) batch.create(HandoffWorkPlan, { ...props, workPlanId: nextPlanId, workspaceId: workspace.workspaceId,
    readerIds: [...workspace.readerIds!], handoffId: handoff.handoffId, status: "Ready" });
  else batch.update(plan, props);
  batch.update(handoff, { workPlanId: nextPlanId, revision: handoffRevision, nextStep: "Review the updated work plan and accept it when ready.",
    ...(fork ? { operativeDecisionId: handoff.operativeDecisionId ?? plan.acceptedDecisionId } : {}) });
  batch.update(work, { status: "Waiting for decision", nextStep: "Review the updated work plan.", updatedAt: now, ...(work.businessTime ? { businessTime: stamp } : {}) });
  guardWorkspace(batch, workspace, commandId);
  addActivity(batch, intent, [...workspace.readerIds!], "Work plan updated", "The proposal was updated. Existing accepted work and commitments remain recorded.", props.revision, stamp);
  return batch.getEdits();
}

export async function acceptPlan(client: Client, workPlanId: string, expectedRevision: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  whole(expectedRevision, "Plan revision");
  const caller = await currentCaller(client, currentUserId);
  const { plan, handoff, workspace } = await loadPlan(client, workPlanId, caller, "decide", false);
  const intent = command(workspace.workspaceId, workPlanId, handoff.handoffId, commandId, caller.id, "Work plan accepted", { workPlanId, expectedRevision });
  if (await wasApplied(client, workspace, caller, intent)) return [];
  requireHandoff(plan.status === "Ready" && !plan.acceptedDecisionId, "This work plan has already been accepted.");
  requireHandoff(handoff.workPlanId === workPlanId && plan.revision === expectedRevision,
    "The work plan has changed. Refresh it before accepting.");
  const [work, world, delivery] = await Promise.all([loadAgentWork(client, handoff, workspace, caller), loadDetails(client, handoff, workspace, caller), loadDeliveryRecords(client, workspace, caller, handoff)]);
  const draft = planDraft(plan);
  requireHandoff(plan.sourceBasis ? plan.sourceBasis === materialBasis(handoff, workspace, world) : plan.basisRevision === handoff.revision,
    "The facts supporting this proposal have changed. Ask Handoff to reconsider it before accepting.");
  requireHandoff(draft.currency === workspace.currency && draft.sourceDocumentIds.every((id) => world.documents.some((document) => document.documentId === id)),
    "The plan's supporting documents need checking before accepting.");
  if (plan.selectionJson) validateSelection({ ...draft, selections: planSelections(plan), fixedProviderPartyId: plan.fixedProviderPartyId }, delivery.quotes);
  else requireHandoff(world.documents.some((document) => document.kind === "Quote" && document.partyId === draft.providerPartyId
    && draft.sourceDocumentIds.includes(document.documentId)), "The plan's supporting quote needs checking before accepting.");
  const decisionId = reference("decision", workspace.workspaceId, plan.workPlanId, expectedRevision);
  requireHandoff(!await one(client(HandoffDecision).where({ decisionId: { $eq: decisionId } })), "This work plan already has a recorded decision.");
  const now = new Date().toISOString(), revision = nextRevision(handoff.revision), batch = createEditBatch<HandoffEdit>(client);
  const stamp = caseTime(work, now);
  batch.create(HandoffDecision, { decisionId, workspaceId: workspace.workspaceId, readerIds: [...workspace.readerIds!],
    handoffId: handoff.handoffId, workPlanId: plan.workPlanId, title: "Work plan accepted", acceptedRevision: expectedRevision,
    contentJson: acceptedContent(plan), decidedBy: caller.id, decidedAt: stamp, commandId });
  batch.update(plan, { status: "Accepted", acceptedDecisionId: decisionId });
  batch.update(handoff, { operativeDecisionId: decisionId, revision, physicalProgress: "Arranging work", nextStep: "Arrange the accepted work and confirm its funding." });
  batch.update(work, { title: "Arrange the accepted work", status: "Ready to continue", operationKey: `continue:${decisionId}`,
    nextStep: "Arrange the accepted work and confirm its funding.", nextWakeAt: now, nextBusinessAt: undefined, updatedAt: now,
    ...(work.businessTime ? { businessTime: stamp } : {}) });
  guardWorkspace(batch, workspace, commandId);
  addActivity(batch, intent, [...workspace.readerIds!], "Work plan accepted", "Plan accepted. Handoff will send the work orders.", revision, stamp);
  return batch.getEdits();
}
