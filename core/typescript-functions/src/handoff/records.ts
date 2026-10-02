import {
  HandoffWorkspace, HandoffProperty, HandoffParty, HandoffTenancy, HandoffAgreement,
  HandoffObligation, HandoffCase, HandoffDocument, HandoffWorkPlan, HandoffDecision,
  HandoffMessage, HandoffAgentWork, HandoffActivity,
  HandoffJob, HandoffInspection, HandoffQuote, HandoffInvoice, HandoffFunding, HandoffPayment,
} from "@ontology/sdk";
import type { Client, ObjectSet, ObjectTypeDefinition, Osdk } from "@osdk/client";
import type { Edits, EditBatch } from "@osdk/functions";
import { Admin } from "@osdk/foundry";
import { nextRevision, reference, requireHandoff, words } from "./values.js";

export type HandoffEdit = Edits.Object<HandoffWorkspace> | Edits.Object<HandoffProperty>
  | Edits.Object<HandoffParty> | Edits.Object<HandoffTenancy> | Edits.Object<HandoffAgreement>
  | Edits.Object<HandoffObligation> | Edits.Object<HandoffCase> | Edits.Object<HandoffDocument>
  | Edits.Object<HandoffWorkPlan> | Edits.Object<HandoffDecision> | Edits.Object<HandoffMessage>
  | Edits.Object<HandoffAgentWork> | Edits.Object<HandoffActivity>
  | Edits.Object<HandoffJob> | Edits.Object<HandoffInspection> | Edits.Object<HandoffQuote>
  | Edits.Object<HandoffInvoice> | Edits.Object<HandoffFunding> | Edits.Object<HandoffPayment>;
export type Workspace = Osdk.Instance<HandoffWorkspace>;
export type Handoff = Osdk.Instance<HandoffCase>;
export type Plan = Osdk.Instance<HandoffWorkPlan>;
export interface Caller { id: string; name: string }
export type Permission = "read" | "work" | "decide" | "configure";

export async function currentCaller(client: Client, suppliedId?: string): Promise<Caller> {
  const user = await Admin.Users.getCurrent(client);
  requireHandoff(suppliedId === undefined || suppliedId === user.id,
    "The signed-in person must be the person making this change.");
  return { id: user.id, name: user.givenName || user.familyName
    ? [user.givenName, user.familyName].filter(Boolean).join(" ") : user.username };
}

export function access(workspace: Workspace, caller: Caller): {
  canWork: boolean; canDecide: boolean; canConfigure: boolean;
} {
  requireHandoff(workspace.readerIds?.includes(caller.id), "This workspace is not available to you.");
  return {
    canWork: workspace.workUserIds?.includes(caller.id) ?? false,
    canDecide: workspace.decideUserIds?.includes(caller.id) ?? false,
    canConfigure: workspace.adminUserIds?.includes(caller.id) ?? false,
  };
}

export function authorize(workspace: Workspace, caller: Caller, permission: Permission): void {
  const granted = access(workspace, caller);
  requireHandoff(permission === "read" || (permission === "work" && granted.canWork)
    || (permission === "decide" && granted.canDecide)
    || (permission === "configure" && granted.canConfigure),
  "Ask the workspace owner for permission to make this change.");
  requireHandoff(workspace.mode === "demo", "This workspace is not set up for this way of working.");
}

export function inWorkspace(
  object: { workspaceId?: string; readerIds?: ReadonlyArray<string> }, workspace: Workspace, caller: Caller,
): void {
  requireHandoff(object.workspaceId === workspace.workspaceId && object.readerIds?.includes(caller.id),
    "These details are not available in this workspace.");
  // Recommendations and correspondence inherit workspace readers, so their source records must agree.
  requireHandoff(JSON.stringify([...new Set(object.readerIds)].sort()) === JSON.stringify([...new Set(workspace.readerIds)].sort()),
    "The handoff records have different access settings. Ask the workspace owner to check them.");
}

/** Explicit bounds fail rather than quietly omitting decision-relevant records. */
export async function bounded<T extends ObjectTypeDefinition>(set: ObjectSet<T>, max = 100): Promise<Osdk.Instance<T>[]> {
  const page = await set.fetchPage({ $pageSize: max });
  requireHandoff(!page.nextPageToken && page.data.length <= max,
    "There are too many related records to review together. Narrow the handoff first.");
  return page.data;
}

/** Growing correspondence is paginated by the SDK; its complete correlations remain available.
 * Only use this with an explicitly scoped history set. Operator views fetch recent pages instead. */
export async function historyRecords<T extends ObjectTypeDefinition>(set: ObjectSet<T>): Promise<Osdk.Instance<T>[]> {
  const result: Osdk.Instance<T>[] = [];
  for await (const record of set.asyncIter()) result.push(record);
  return result;
}

export async function one<T extends ObjectTypeDefinition>(set: ObjectSet<T>): Promise<Osdk.Instance<T> | undefined> {
  const result = await bounded(set, 2);
  requireHandoff(result.length <= 1, "More than one matching record was found. Ask the workspace owner to check it.");
  return result[0];
}

export async function loadWorkspace(client: Client, id: string, caller: Caller, permission: Permission): Promise<Workspace> {
  words(id, "Workspace reference", 160);
  const workspace = await one(client(HandoffWorkspace).where({ workspaceId: { $eq: id } }));
  requireHandoff(workspace, "This workspace is not available to you.");
  authorize(workspace, caller, permission);
  return workspace;
}

export async function loadHandoff(client: Client, id: string, caller: Caller, permission: Permission): Promise<{
  handoff: Handoff; workspace: Workspace;
}> {
  words(id, "Handoff reference", 160);
  const handoff = await one(client(HandoffCase).where({ handoffId: { $eq: id } }));
  requireHandoff(handoff?.workspaceId, "This handoff is not available to you.");
  const workspace = await loadWorkspace(client, handoff.workspaceId, caller, permission);
  inWorkspace(handoff, workspace, caller);
  return { handoff, workspace };
}

export async function loadPlan(client: Client, id: string, caller: Caller, permission: Permission, requireCurrent = true): Promise<{
  plan: Plan; handoff: Handoff; workspace: Workspace;
}> {
  words(id, "Work plan reference", 160);
  const plan = await one(client(HandoffWorkPlan).where({ workPlanId: { $eq: id } }));
  requireHandoff(plan?.handoffId, "This work plan is not available to you.");
  const { handoff, workspace } = await loadHandoff(client, plan.handoffId, caller, permission);
  inWorkspace(plan, workspace, caller);
  requireHandoff(!requireCurrent || handoff.workPlanId === plan.workPlanId, "Review the handoff's current work plan before continuing.");
  return { plan, handoff, workspace };
}

export function workReference(handoff: Handoff): string {
  return reference("work", handoff.workspaceId!, handoff.handoffId);
}

export async function loadAgentWork(client: Client, handoff: Handoff, workspace: Workspace, caller: Caller): Promise<Osdk.Instance<HandoffAgentWork>> {
  const work = await one(client(HandoffAgentWork).where({ workId: { $eq: workReference(handoff) } }));
  requireHandoff(work && work.handoffId === handoff.handoffId, "The handoff's next step could not be found.");
  inWorkspace(work, workspace, caller);
  return work;
}

export function handoffUnchanged(before: Handoff, after: Handoff): boolean {
  return JSON.stringify(before.fixedRequirements ?? []) === JSON.stringify(after.fixedRequirements ?? [])
    && ["handoffId", "workspaceId", "readerIds", "revision", "workPlanId", "status", "title", "goal", "propertyId", "tenancyId", "businessDate", "physicalProgress", "financialProgress", "nextStep"]
    .every((key) => JSON.stringify(Reflect.get(before, key)) === JSON.stringify(Reflect.get(after, key)));
}

export function workspaceUnchanged(before: Workspace, after: Workspace): boolean {
  return ["workspaceId", "name", "revision", "readerIds", "workUserIds", "decideUserIds", "adminUserIds", "modelRid", "mode", "currency", "lastCommandId"]
    .every((key) => JSON.stringify(Reflect.get(before, key)) === JSON.stringify(Reflect.get(after, key)));
}

/** Touch the loaded authority record in the same batch as business edits. This is not a world-wide lock. */
export function guardWorkspace(batch: EditBatch<HandoffEdit>, workspace: Workspace, commandId: string): void {
  batch.update(workspace, { lastCommandId: commandId, revision: nextRevision(workspace.revision) });
}
