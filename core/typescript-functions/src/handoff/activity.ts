import { HandoffActivity } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import type { EditBatch } from "@osdk/functions";
import { inWorkspace, one, type Caller, type HandoffEdit, type Workspace } from "./records.js";
import { details, digest, parseDetails, reference, requireHandoff, words } from "./values.js";

export interface HandoffCommand {
  workspaceId: string; subjectId: string; handoffId?: string; commandId: string; actorId: string;
  kind: string; payloadHash: string;
}

export function command(workspaceId: string, subjectId: string, handoffId: string | undefined,
  commandId: string, actorId: string, kind: string, payload: unknown): HandoffCommand {
  words(commandId, "Request reference", 160);
  return { workspaceId, subjectId, handoffId, commandId, actorId, kind, payloadHash: digest(payload) };
}

export function activityReference(intent: HandoffCommand): string {
  return reference("activity", intent.workspaceId, intent.commandId);
}

/** Check identity and intent before revision checks, so old exact repeats remain harmless. */
export async function wasApplied(client: Client, workspace: Workspace, caller: Caller, intent: HandoffCommand): Promise<boolean> {
  const receipt = await one(client(HandoffActivity).where({ activityId: { $eq: activityReference(intent) } }));
  if (!receipt) return false;
  inWorkspace(receipt, workspace, caller);
  const stored = details(parseDetails(words(receipt.detail, "Activity details", 16000), "Activity details", 16000),
    ["version", "payloadHash", "summary"], ["trace"], "Activity details");
  requireHandoff(receipt.commandId === intent.commandId && receipt.actorId === intent.actorId
    && receipt.subjectId === intent.subjectId && receipt.handoffId === intent.handoffId
    && receipt.kind === intent.kind && stored.version === "1" && stored.payloadHash === intent.payloadHash,
  "This request reference was already used for a different change. Start a new request.");
  return true;
}

export function addActivity(batch: EditBatch<HandoffEdit>, intent: HandoffCommand, readerIds: string[],
  title: string, summary: string, resultRevision: string, now: string,
  trace?: { model: string; usedDocumentIds: string[]; toolCallCount: number; durationMs: number }): void {
  const detail = JSON.stringify({ version: "1", payloadHash: intent.payloadHash, summary, ...(trace ? { trace } : {}) });
  requireHandoff(detail.length <= 16000, "The work summary is too long to save. Narrow the work details.");
  batch.create(HandoffActivity, {
    activityId: activityReference(intent), workspaceId: intent.workspaceId, handoffId: intent.handoffId,
    subjectId: intent.subjectId, commandId: intent.commandId, actorId: intent.actorId, kind: intent.kind,
    title, detail, occurredAt: now, resultRevision, readerIds,
  });
}

/** Only ordinary business copy is returned; receipts and model execution evidence remain internal. */
export function activitySummary(activity: Osdk.Instance<HandoffActivity>): string {
  const stored = details(parseDetails(words(activity.detail, "Activity details", 16000), "Activity details", 16000),
    ["version", "payloadHash", "summary"], ["trace"], "Activity details");
  return words(stored.summary, "Activity summary", 4000);
}
