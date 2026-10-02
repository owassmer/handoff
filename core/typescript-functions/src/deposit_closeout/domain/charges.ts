/** Item decisions use accepted synthetic inputs, never invoice-to-charge copying. */
import { fingerprint } from "./fingerprints.js";
import { to_wire } from "./codec.js";
import type { CaseSnapshot, ChargeInput, EvidenceInput, ItemDecision, OpenQuestion, SourceReference } from "./types.js";
import { question, valid_evidence } from "./validation.js";
import { _compare_text, _compare_timestamps, _same, _sorted_unique } from "./rules.js";

const _CATEGORIES = new Set(["ORDINARY_DAMAGE", "ORDINARY_OWNER_REPAINTING"]);
const _RELEVANT_RECORDS = new Set(["INVOICE", "CONDITION_OBSERVATION", "WORK_COMPLETION", "FACT_ASSERTION", "ESTIMATE"]);

export function _ancestors(evidence_id: string, evidence_by_id: ReadonlyMap<string, EvidenceInput>): Set<string> {
  const visited = new Set<string>();
  let current = evidence_by_id.get(evidence_id);
  while (current !== undefined && current.supersedesEvidenceId !== null) {
    const previous = current.supersedesEvidenceId;
    if (visited.has(previous)) break;
    visited.add(previous);
    current = evidence_by_id.get(previous);
  }
  return visited;
}

/** Quote free-text categories and escape control characters in review reasons. */
function _format_category(value: string): string {
  const quote = value.includes("'") && !value.includes('"') ? '"' : "'";
  const escaped = Array.from(value).map((character): string => {
    if (character === "\\" || character === quote) return `\\${character}`;
    if (character === "\n") return "\\n";
    if (character === "\r") return "\\r";
    if (character === "\t") return "\\t";
    if (character !== " " && /[\p{C}\p{Z}]/u.test(character)) {
      const point = character.codePointAt(0)!;
      if (point <= 0xff) return `\\x${point.toString(16).padStart(2, "0")}`;
      if (point <= 0xffff) return `\\u${point.toString(16).padStart(4, "0")}`;
      return `\\U${point.toString(16).padStart(8, "0")}`;
    }
    return character;
  }).join("");
  return quote + escaped + quote;
}

/**
 * Preserve supported independent item decisions while exposing affected-item review dependencies.
 * @param snapshot Complete constructed snapshot; no input object or array is mutated.
 * @param supported Whether this exact snapshot falls inside the implemented synthetic scope.
 * @param clock Canonical UTC review timestamp including any supplied microseconds.
 * @returns Item decisions and review questions, in that order.
 */
export function review_items(snapshot: CaseSnapshot, supported: boolean, clock: string): [ItemDecision[], OpenQuestion[]] {
  const decisions: ItemDecision[] = [];
  const questions: OpenQuestion[] = [];
  const unique = new Map<string, ChargeInput>();
  const conflicts = new Set<string>();
  snapshot.charges.forEach((item) => {
    if (unique.has(item.itemId) && !_same(unique.get(item.itemId), item)) conflicts.add(item.itemId);
    else unique.set(item.itemId, item);
  });
  const known_questions = new Map(snapshot.questions.map((entry) => [entry.questionId, entry]));
  const evidence_by_id = new Map(snapshot.evidence
    .filter((entry) => snapshot.evidence.filter((other) => other.evidenceId === entry.evidenceId).every((other) => _same(other, entry)))
    .map((entry) => [entry.evidenceId, entry]));

  [...unique.keys()].sort(_compare_text).forEach((item_id) => {
    const item = unique.get(item_id)!;
    const sources = [...new Map(snapshot.evidence
      .filter((entry) => item.evidenceIds.includes(entry.evidenceId) && _compare_timestamps(entry.learnedAt, clock) <= 0)
      .map((entry) => [entry.evidenceId, entry])).values()];
    const refs: SourceReference[] = sources.sort((a, b) => _compare_text(a.evidenceId, b.evidenceId)).map((entry) => ({
      evidenceId: entry.evidenceId,
      sourceClass: entry.sourceClass,
      sourceVersion: entry.sourceVersion,
      locator: entry.locator,
      page: null,
      quote: entry.excerpt,
    }));
    const missing: string[] = [];
    let allocation: ItemDecision["allocation"] = item.acceptedAllocation;
    let allowable: ItemDecision["allowability"] = item.allowabilityState;
    let supported_amount = item.supportedAmountCents;
    let chosen = item.chosenAmountCents;
    let choice: ItemDecision["choiceState"] = item.choiceState;
    let reason = item.reason;
    let cost = item.vendorCostCents;

    if (!supported) {
      allocation = "UNRESOLVED"; allowable = "NOT_EVALUATED"; supported_amount = null; chosen = null; choice = "NOT_DECIDED";
      reason = "No substantive item decision is made outside the implemented synthetic scope.";
    } else if (conflicts.has(item_id)) {
      allocation = "UNRESOLVED"; allowable = "UNRESOLVED"; supported_amount = null; chosen = null; choice = "NOT_DECIDED"; cost = null;
      const q = question(`charge:${item_id}:identity`, "Which version of this charge item is current?", "Contradictory records share the same item ID; do not choose by input order.", "MANAGER", [item_id], undefined, "Reconciled item identity/version");
      questions.push(q); missing.push(q.questionId);
    } else if (!_CATEGORIES.has(item.category)) {
      allocation = "UNRESOLVED"; allowable = "NOT_EVALUATED"; supported_amount = null; chosen = null; choice = "NOT_DECIDED";
      const q = question(`charge:${item_id}:category`, "Which reviewed rule covers this charge category?", `Category ${_format_category(item.category)} is not implemented; an approved or supplied balance is not automatically a deposit deduction.`, "REVIEWER", [item_id], undefined, "Reviewed category rule and accepted item facts");
      questions.push(q); missing.push(q.questionId);
    } else if (!valid_evidence(snapshot, item.evidenceIds, clock)) {
      allocation = "UNRESOLVED"; allowable = "UNRESOLVED"; supported_amount = null; chosen = null; choice = "NOT_DECIDED";
      const q = question(`charge:${item_id}:evidence`, "Which usable source supports this item decision?", "Supporting evidence is absent, conflicting, unassociated, a model proposal, or not yet known at the review clock.", "MANAGER", [item_id], undefined, "Accepted item source and exact location");
      questions.push(q); missing.push(q.questionId);
    } else if (item.category === "ORDINARY_OWNER_REPAINTING" || (allocation === "OWNER" && allowable === "DISALLOWED")) {
      allocation = "OWNER"; allowable = "DISALLOWED"; supported_amount = 0; chosen = 0; choice = "NOT_APPLICABLE";
      reason = "Accepted ordinary owner cost is not a tenant deduction. This is exclusion, not waiver of tenant damage; owner approval cannot override it.";
    } else if (allowable === "DISALLOWED") {
      supported_amount = 0; chosen = 0; choice = "NOT_APPLICABLE";
      reason = "The accepted disallowed basis remains disallowed; approval does not legalize the proposed charge. " + item.reason;
    } else if (allowable === "SUPPORTED" && ["TENANT", "SPLIT"].includes(allocation)
      && item.costState === "KNOWN" && cost !== null
      && item.costVersionId !== null && item.evidenceIds.includes(item.costVersionId)
      && valid_evidence(snapshot, [item.costVersionId], clock)
      && supported_amount !== null && supported_amount <= cost
      && ((choice === "CHOSEN" && chosen !== null && chosen <= supported_amount)
        || (choice === "WAIVED" && chosen === 0))) {
      // This is an already accepted decision; source arrival alone cannot rewrite it.
    } else {
      allowable = "UNRESOLVED"; supported_amount = null; chosen = null; choice = "NOT_DECIDED";
      const existing = item.unresolvedQuestionIds.flatMap((key) => {
        const entry = known_questions.get(key);
        return entry === undefined ? [] : [entry];
      });
      if (existing.length > 0) missing.push(...existing.map((entry) => entry.questionId));
      else {
        const q = question(`charge:${item_id}:decision`, "Resolve this item's actual cost, responsibility and supported chosen amount.", "A known cost requires its source version; chosen amount must not exceed supported amount or actual cost. Unknown/disputed facts are not zero.", "MANAGER", [item_id], ["RECORD_CHARGE_DECISION", "CHOOSE_OR_WAIVE_CHARGE"], "Current cost version and accepted responsibility/choice");
        questions.push(q); missing.push(q.questionId);
      }
    }
    if (supported) {
      const accepted_ids = new Set(item.evidenceIds);
      const superseded_history = new Set<string>();
      accepted_ids.forEach((id) => _ancestors(id, evidence_by_id).forEach((ancestor) => superseded_history.add(ancestor)));
      const pending = snapshot.evidence.filter((entry) => (entry.proposedItemIds.includes(item_id)
        || [..._ancestors(entry.evidenceId, evidence_by_id)].some((ancestor) => accepted_ids.has(ancestor)))
        && !accepted_ids.has(entry.evidenceId) && !superseded_history.has(entry.evidenceId)
        && _RELEVANT_RECORDS.has(entry.recordKind) && _compare_timestamps(entry.learnedAt, clock) <= 0);
      if (pending.length > 0) {
        const q = question(`charge:${item_id}:new-evidence`, "Does the newly arrived evidence change this item?", "Review associated or candidate evidence before using the old affected decision; do not silently accept its amount or change item identity.", "MANAGER", [item_id], undefined, "New evidence: " + _sorted_unique(pending.map((entry) => entry.evidenceId)).join(", "));
        questions.push(q); missing.push(q.questionId);
        if (allocation === "OWNER" || allowable === "DISALLOWED") {
          allocation = "UNRESOLVED"; allowable = "UNRESOLVED"; supported_amount = null; chosen = null; choice = "NOT_DECIDED";
        }
      }
      if (item.reviewRequired && missing.length === 0) {
        const q = question(`charge:${item_id}:review`, "Complete the required review for this item.", "The item is explicitly marked review-required; a previous amount is not a completed review.", "MANAGER", [item_id], undefined, "Current item review decision");
        questions.push(q); missing.push(q.questionId);
        if (allocation === "OWNER" || allowable === "DISALLOWED") {
          allocation = "UNRESOLVED"; allowable = "UNRESOLVED"; supported_amount = null; chosen = null; choice = "NOT_DECIDED";
        }
      }
      missing.push(...item.unresolvedQuestionIds);
      missing.push(...snapshot.questions.filter((entry) => entry.affectedItemIds.includes(item_id)).map((entry) => entry.questionId));
    }
    const payload: Omit<ItemDecision, "fingerprint"> = {
      itemId: item_id,
      costVersionId: item.costVersionId,
      vendorCostCents: cost,
      allocation,
      allowability: allowable,
      supportedAmountCents: supported_amount,
      chosenAmountCents: chosen,
      choiceState: choice,
      reason,
      sourceReferences: refs,
      ruleQuestionIds: supported ? ["DAMAGE"] : [],
      missingInputIds: _sorted_unique(missing),
      requiresReviewer: missing.length > 0 || ["UNRESOLVED", "NOT_EVALUATED"].includes(allowable),
    };
    decisions.push({ ...payload, fingerprint: fingerprint(to_wire(payload)) });
  });
  return [decisions, questions];
}
