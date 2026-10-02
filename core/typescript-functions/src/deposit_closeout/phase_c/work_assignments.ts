import { is_plain_object, parse_json } from "../domain/codec.js";
import { normalize_timestamp, timestamp_microseconds } from "../domain/datetime.js";
import { fingerprint } from "../domain/fingerprints.js";
import type { ReviewRequest } from "../domain/types.js";
import type { WorkAssignment } from "./change_types.js";
import { BOOTSTRAP_ACTOR_ID } from "./types.js";
import { boundedJson, requireCondition, serialize } from "./validation.js";

/** Absence is meaningful only in the known C0 storage contract, never in v1. */
export function loadWorkAssignments(json: string | undefined, hash: string | undefined,
  version: string | undefined, request: ReviewRequest, createdAt: string): WorkAssignment[] {
  if (version === undefined || version === "0") {
    requireCondition(json === undefined && hash === undefined,
      "C0 review unexpectedly contains a work assignment sidecar.");
    return [];
  }
  requireCondition(version === "1" && typeof json === "string" && typeof hash === "string",
    "Current review requires its work assignment sidecar and hash.");
  const raw: unknown = parse_json(boundedJson(json));
  requireCondition(Array.isArray(raw), "Work assignments must be an array.");
  const entries: unknown[] = raw;
  const keys = ["requirementKey", "assigneePartyId", "internalTargetAt", "reason", "assignedBy", "assignedAt"];
  const assignments = entries.map((entry): WorkAssignment => {
    requireCondition(is_plain_object(entry) && Object.keys(entry).length === keys.length
      && keys.every((key): boolean => Object.hasOwn(entry, key)), "Work assignment shape is inconsistent.");
    requireCondition(typeof entry.requirementKey === "string" && entry.requirementKey.length > 0
      && typeof entry.assigneePartyId === "string" && request.snapshot.parties.some((party): boolean => party.partyId === entry.assigneePartyId)
      && typeof entry.reason === "string" && entry.reason.trim().length > 0
      && Buffer.byteLength(entry.reason, "utf8") <= 2000
      && entry.assignedBy === BOOTSTRAP_ACTOR_ID
      && typeof entry.assignedAt === "string" && normalize_timestamp(entry.assignedAt) === entry.assignedAt
      && timestamp_microseconds(entry.assignedAt) <= timestamp_microseconds(createdAt)
      && (entry.internalTargetAt === null || (typeof entry.internalTargetAt === "string"
        && normalize_timestamp(entry.internalTargetAt) === entry.internalTargetAt)),
    "Work assignment content is inconsistent.");
    return { requirementKey: entry.requirementKey, assigneePartyId: entry.assigneePartyId,
      reason: entry.reason, assignedBy: entry.assignedBy, assignedAt: entry.assignedAt,
      internalTargetAt: entry.internalTargetAt as string | null };
  });
  requireCondition(new Set(assignments.map((entry): string => entry.requirementKey)).size === assignments.length
    && json === serialize(assignments) && hash === fingerprint(assignments),
  "Work assignment canonical content or hash is inconsistent.");
  return assignments;
}
