import {
  HandoffWorkspace, HandoffProperty, HandoffParty, HandoffTenancy, HandoffAgreement,
  HandoffObligation, HandoffCase, HandoffDocument, HandoffWorkPlan, HandoffDecision,
  HandoffMessage, HandoffAgentWork, HandoffActivity,
  HandoffJob, HandoffInspection, HandoffQuote, HandoffInvoice, HandoffFunding, HandoffPayment,
} from "@ontology/sdk";
import type { Client, ObjectTypeDefinition } from "@osdk/client";
import { createEditBatch } from "@osdk/functions";
import { Admin } from "@osdk/foundry";
import { addActivity, command, wasApplied } from "./activity.js";
import { currentCaller, loadWorkspace, type HandoffEdit, type Workspace } from "./records.js";
import { nextRevision, requireHandoff, words } from "./values.js";

export const ACCESS_LEVELS = ["None", "Read", "Work", "Decide", "Admin"] as const;
export type AccessLevel = typeof ACCESS_LEVELS[number];

/** Every record type that carries the workspace's reader list. The workspace itself is updated separately. */
const RECORD_TYPES = [HandoffProperty, HandoffParty, HandoffTenancy, HandoffAgreement, HandoffObligation, HandoffCase,
  HandoffDocument, HandoffWorkPlan, HandoffDecision, HandoffMessage, HandoffAgentWork, HandoffActivity, HandoffJob,
  HandoffInspection, HandoffQuote, HandoffInvoice, HandoffFunding, HandoffPayment] as const;
/** One action edits every record in the workspace; beyond this a workspace needs a staged migration. */
const MAX_RECORDS = 5000;

export function levelOf(workspace: Workspace, userId: string): AccessLevel {
  if (workspace.adminUserIds?.includes(userId)) return "Admin";
  if (workspace.decideUserIds?.includes(userId)) return "Decide";
  if (workspace.workUserIds?.includes(userId)) return "Work";
  return workspace.readerIds?.includes(userId) ? "Read" : "None";
}
function withLevel(list: readonly string[] | undefined, userId: string, included: boolean): string[] {
  const rest = (list ?? []).filter((id) => id !== userId);
  return included ? [...rest, userId] : rest;
}
function personName(user: { username: string; givenName?: string; familyName?: string }): string {
  return user.givenName || user.familyName ? [user.givenName, user.familyName].filter(Boolean).join(" ") : user.username;
}

/**
 * Grant a person access to a workspace, or remove it. Access is cumulative: Work includes Read, Decide includes Work,
 * Admin includes Decide. The reader list is copied onto every record so reads stay consistent; rerunning the same
 * change also repairs any record whose reader list differs from the workspace.
 */
export async function setAccess(client: Client, workspaceId: string, userId: string, level: string,
  commandId: string, currentUserId: string): Promise<HandoffEdit[]> {
  words(userId, "Person", 160);
  requireHandoff((ACCESS_LEVELS as readonly string[]).includes(level), "Choose None, Read, Work, Decide or Admin.");
  const caller = await currentCaller(client, currentUserId);
  const workspace = await loadWorkspace(client, workspaceId, caller, "configure");
  const intent = command(workspace.workspaceId, workspace.workspaceId, undefined, commandId, caller.id, "Access changed", { userId, level });
  if (await wasApplied(client, workspace, caller, intent)) return [];
  requireHandoff(!(userId === caller.id && level !== "Admin"), "You can't change your own access. Ask another admin.");
  const user = level === "None" ? undefined : await Admin.Users.get(client, userId);
  requireHandoff(level === "None" || (user && user.id === userId && user.status === "ACTIVE"), "That person isn't an active user in your organization.");
  const rank = ACCESS_LEVELS.indexOf(level as AccessLevel);
  const next = {
    readerIds: withLevel(workspace.readerIds, userId, rank >= 1),
    workUserIds: withLevel(workspace.workUserIds, userId, rank >= 2),
    decideUserIds: withLevel(workspace.decideUserIds, userId, rank >= 3),
    adminUserIds: withLevel(workspace.adminUserIds, userId, rank >= 4),
  };
  requireHandoff(next.adminUserIds.length > 0, "A workspace needs at least one admin.");
  const batch = createEditBatch<HandoffEdit>(client), readers = next.readerIds;
  const same = (a: readonly string[] | undefined): boolean => JSON.stringify([...(a ?? [])].sort()) === JSON.stringify([...readers].sort());
  let count = 0;
  for (const type of RECORD_TYPES) {
    const set = client(type as ObjectTypeDefinition) as unknown as { where(filter: object): { asyncIter(): AsyncIterable<{ readerIds?: readonly string[] }> } };
    for await (const row of set.where({ workspaceId: { $eq: workspace.workspaceId } }).asyncIter()) {
      count += 1;
      requireHandoff(count <= MAX_RECORDS, "This workspace has too many records to change access in one step.");
      if (!same(row.readerIds)) batch.update(row as never, { readerIds: [...readers] } as never);
    }
  }
  batch.update(workspace, { ...next, lastCommandId: commandId, revision: nextRevision(workspace.revision) });
  const who = user ? personName(user) : "A teammate";
  addActivity(batch, intent, [...readers], "Access changed",
    level === "None" ? `${who} no longer has access to this workspace.` : `${who} now has ${level.toLowerCase()} access.`, nextRevision(workspace.revision), new Date().toISOString());
  return batch.getEdits();
}
