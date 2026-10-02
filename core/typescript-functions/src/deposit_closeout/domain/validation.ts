/** Pure semantic evidence checks. Unresolved business facts remain questions. */
import type { CaseSnapshot, EvidenceInput, OpenQuestion } from "./types.js";
import { canonical_json, compare_unicode } from "./codec.js";
import { compare_timestamps } from "./datetime.js";

/** Construct a review question with explicit affected items and resolution actions. */
export function question(
  key: string,
  text: string,
  reason: string,
  role: string = "MANAGER",
  items?: readonly string[] | null,
  actions?: readonly string[] | null,
  record: string = "Accepted source record and decision",
): OpenQuestion {
  return {
    questionId: key,
    question: text,
    reason,
    resolverRole: role,
    resolverPartyId: null,
    neededRecord: record,
    affectedItemIds: [...new Set(items ?? [])].sort(compare_unicode),
    // An omitted or empty action list defaults to fact acceptance/correction.
    affectedActionKinds: [...new Set(actions?.length ? actions : ["ACCEPT_OR_CORRECT_FACT"])].sort(compare_unicode),
  };
}

function same(left: unknown, right: unknown): boolean {
  return canonical_json(left) === canonical_json(right);
}

export function valid_evidence(snapshot: CaseSnapshot, ids: readonly string[], clock: string): boolean {
  if (ids.length === 0) return false;
  const byId = new Map<string, EvidenceInput[]>();
  snapshot.evidence.forEach((entry): void => {
    const group = byId.get(entry.evidenceId) ?? [];
    group.push(entry);
    byId.set(entry.evidenceId, group);
  });
  return ids.every((id): boolean => {
    const matches = byId.get(id);
    const evidence = matches?.[0];
    if (matches === undefined || evidence === undefined
        || matches.some((entry): boolean => !same(entry, evidence))) return false;
    const visited = new Set([evidence.evidenceId]);
    let previous = evidence.supersedesEvidenceId;
    while (previous !== null) {
      const parents = byId.get(previous);
      const parent = parents?.[0];
      if (visited.has(previous) || parents === undefined || parent === undefined
          || parents.some((entry): boolean => !same(entry, parent))) return false;
      visited.add(previous);
      previous = parent.supersedesEvidenceId;
    }
    // Ancestor identity is checked above. Usability is checked only on the
    // evidence being accepted, not every historical ancestor.
    return evidence.associationAccepted
      && compare_timestamps(evidence.learnedAt, clock) <= 0
      && (evidence.occurredAt === null
        || (compare_timestamps(evidence.occurredAt, evidence.learnedAt) <= 0
          && compare_timestamps(evidence.occurredAt, clock) <= 0))
      && evidence.sourceClass !== "MODEL_PROPOSAL"
      && evidence.recordKind !== "MODEL_PROPOSAL";
  });
}

export function inspect_snapshot(snapshot: CaseSnapshot, _clock: string): OpenQuestion[] {
  const problems: OpenQuestion[] = [];
  const inspect = <T>(label: string, values: readonly T[], keyOf: (value: T) => string): void => {
    const found = new Map<string, T>();
    values.forEach((value): void => {
      const key = keyOf(value);
      if (found.has(key) && !same(found.get(key), value)) {
        problems.push(question(
          `conflict:${label}:${key}`,
          `Which ${label} record is authoritative?`,
          "The same stable ID has contradictory payloads; input order does not decide truth.",
          "MANAGER", label === "item" ? [key] : [], undefined,
          `Corrected ${label} identity ${key}`,
        ));
      }
      // Compare each occurrence with the last-seen record for the same ID.
      found.set(key, value);
    });
  };
  inspect("evidence", snapshot.evidence, (entry): string => entry.evidenceId);
  inspect("item", snapshot.charges, (entry): string => entry.itemId);
  inspect("party", snapshot.parties, (entry): string => entry.partyId);
  inspect("authority", snapshot.authorityGrants, (entry): string => entry.grantId);
  inspect("date", snapshot.dates, (entry): string => entry.factKey);
  inspect("question", snapshot.questions, (entry): string => entry.questionId);
  inspect("statement", snapshot.priorStatements, (entry): string => entry.versionId);
  inspect("approval", snapshot.priorApprovals, (entry): string => entry.approvalId);
  const knownItems = new Set(snapshot.charges.map((entry): string => entry.itemId));
  const knownParties = new Set(snapshot.parties.map((entry): string => entry.partyId));
  snapshot.questions.forEach((entry): void => {
    if (!entry.affectedItemIds.every((id): boolean => knownItems.has(id))
        || (entry.resolverPartyId !== null && !knownParties.has(entry.resolverPartyId))) {
      problems.push(question(
        `reference:question:${entry.questionId}`,
        "Which case item or person does this question refer to?",
        "An unresolved question contains an invalid case-local reference.",
        "MANAGER", undefined, undefined,
        `Correct question references for ${entry.questionId}`,
      ));
    }
  });
  return problems;
}
