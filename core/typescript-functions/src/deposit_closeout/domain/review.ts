/**
 * Phase B pure six-output review. No I/O, model calls, writes or wall clock.
 * Pending legal policies remain unresolved. Suggested work is neither an
 * executable Action nor an authority grant.
 */
import { review_items } from "./charges.js";
import { ContractError, from_wire, to_wire } from "./codec.js";
import { fingerprint } from "./fingerprints.js";
import { review_money } from "./money.js";
import type { ReviewRuleRelease } from "./phase_b_types.js";
import { review_scope, _compare_text, _compare_timestamps, _local_date, _same, _sorted_unique } from "./rules.js";
import type { ScopeReview } from "./rules.js";
import type {
  AvailableAction, CaseParty, CaseSnapshot, OpenQuestion, RequirementResult,
  ReviewEnvelope, ReviewRequest, ReviewResult, ScopeRequirements, TrackOutcome,
} from "./types.js";
import { inspect_snapshot, question, valid_evidence } from "./validation.js";

export const OUTPUT_SCHEMA_VERSION = "1.1.0";

export function _unambiguous_parties(snapshot: CaseSnapshot): Map<string, CaseParty> {
  return new Map(snapshot.parties.filter((party) => snapshot.parties
    .filter((other) => other.partyId === party.partyId).every((other) => _same(other, party)))
    .map((party) => [party.partyId, party]));
}

export function _authority(
  snapshot: CaseSnapshot,
  action_kind: string,
  role: string,
  amount: number | null,
  clock: string,
): string[] {
  const parties = _unambiguous_parties(snapshot);
  const eligible: string[] = [];
  const today = _local_date(clock, "America/New_York");
  snapshot.authorityGrants.forEach((grant) => {
    if (snapshot.authorityGrants.some((other) => other.grantId === grant.grantId && !_same(other, grant))) return;
    const party = parties.get(grant.partyId);
    if (party !== undefined && ((party.effectiveFrom !== null && today < party.effectiveFrom)
      || (party.effectiveUntil !== null && today > party.effectiveUntil))) return;
    if (party === undefined || !party.roles.includes(role) || !grant.allowedActionKinds.includes(action_kind)) return;
    if (grant.revoked || _compare_timestamps(grant.effectiveFrom, clock) > 0
      || (grant.effectiveUntil !== null && _compare_timestamps(clock, grant.effectiveUntil) >= 0)
      || !valid_evidence(snapshot, grant.evidenceIds, clock)) return;
    if (amount !== null && (grant.amountLimitCents === null || amount > grant.amountLimitCents)) return;
    eligible.push(grant.grantId);
  });
  return eligible.sort(_compare_text);
}

export function _recipient_questions(snapshot: CaseSnapshot, scope: ScopeReview, clock: string): [boolean, string, OpenQuestion[]] {
  const instructions = snapshot.recipients;
  const parties = _unambiguous_parties(snapshot);
  const selected = [...instructions.statementPartyIds, ...instructions.refundPartyIds];
  const bad_party = selected.some((id) => {
    const party = parties.get(id);
    return party === undefined || !party.roles.some((role) => ["RESIDENT", "SIGNATORY"].includes(role));
  });
  let verified = instructions.state === "VERIFIED" && instructions.statementPartyIds.length > 0
    && instructions.refundPartyIds.length > 0 && !bad_party && instructions.verifiedRouteReference !== null
    && valid_evidence(snapshot, instructions.evidenceIds, clock);
  const questions: OpenQuestion[] = [];
  if (!verified) {
    questions.push(question("recipient:instructions", "Confirm the intended statement and refund recipients and route.", "No last-payer, latest-email, owner-role or invented address default. Verify the exact instruction version against this tenancy.", "MANAGER", [], ["SET_RECIPIENT_INSTRUCTIONS"], "Verified case-party recipient instructions and delivery/refund route"));
    if (scope.supported) {
      questions.push(question("recipient:missing-address-policy", "Which reviewed missing-address procedure applies if the route remains unavailable?", "The source/legal branch is pending. No retention duration, full-withholding rule or completion is inferred.", "REVIEWER", [], undefined, "Reviewed missing-address and recipient/method rule"));
    }
  }
  if (instructions.statementMethod !== "DEMO_OUTBOX" || instructions.refundMethod !== "DEMO_OUTBOX") {
    verified = false;
    questions.push(question("recipient:method", "Select a supported synthetic demonstration route.", "Phase B does not verify or execute external delivery/payment methods.", "MANAGER", [], undefined, "DEMO_OUTBOX route for constructed inputs"));
  }
  const state = instructions.state !== "VERIFIED" || verified ? instructions.state : "REVIEW_REQUIRED";
  return [verified, state, questions];
}

export function _dedup_questions(values: OpenQuestion[]): OpenQuestion[] {
  const grouped = new Map<string, OpenQuestion>();
  values.forEach((q) => {
    const old = grouped.get(q.questionId);
    if (old === undefined) grouped.set(q.questionId, q);
    else if (!_same(old, q)) {
      grouped.set(q.questionId, {
        ...old,
        reason: _sorted_unique([old.reason, q.reason]).join(" "),
        affectedItemIds: _sorted_unique([...old.affectedItemIds, ...q.affectedItemIds]),
        affectedActionKinds: _sorted_unique([...old.affectedActionKinds, ...q.affectedActionKinds]),
      });
    }
  });
  return [...grouped.keys()].sort(_compare_text).map((key) => grouped.get(key)!);
}

/**
 * Project one complete supplied snapshot; all supported work stays explicit.
 * @param snapshot Constructed snapshot, strictly normalized without input mutation.
 * @param rule_release The explicitly loaded Phase B synthetic release.
 * @param review_clock Explicit UTC instant; no implicit current time is used.
 * @returns Six typed outputs with separate outcome tracks and both completion flags false.
 */
export function review_case(snapshot: CaseSnapshot, rule_release: ReviewRuleRelease, review_clock: string): ReviewResult {
  const normalized = from_wire("ReviewRequest", to_wire({ snapshot, ruleReleaseId: rule_release.ruleReleaseId, reviewClock: review_clock })) as ReviewRequest;
  snapshot = normalized.snapshot;
  const clock = normalized.reviewClock;
  const release = from_wire("ReviewRuleRelease", to_wire(rule_release)) as ReviewRuleRelease;
  if (!release.allowedOrigins.includes(snapshot.origin)) {
    throw new ContractError("Phase B accepts constructed inputs only; public/live cases are not enabled");
  }
  const semantic = inspect_snapshot(snapshot, clock);
  let scope = review_scope(snapshot, release, clock);
  if (semantic.some((q) => q.questionId.startsWith("conflict:party:"))) {
    scope = { ...scope, supported: false, state: "MISSING_FACTS", trigger: null, ordinaryDue: null, finalDue: null };
  }
  const [items, item_questions] = review_items(snapshot, scope.supported, clock);
  const money = review_money(snapshot, items, scope.supported, clock);
  let account = money.account;
  let questions: OpenQuestion[] = [...snapshot.questions, ...semantic, ...scope.questions, ...item_questions];
  // Item/scope resolvers remain Manager/Reviewer, not generic Accountant replacements.
  questions.push(...money.questions.filter((q) => !q.questionId.startsWith("money:item:") && q.questionId !== "money:scope"));
  items.forEach((decision) => {
    const known = new Set(questions.map((q) => q.questionId));
    decision.missingInputIds.forEach((key) => {
      if (!known.has(key)) {
        questions.push(question(key, "Resolve this item's referenced review question.", "The item references an unresolved question or decision not otherwise supplied.", "MANAGER", [decision.itemId], undefined, "Current item question/decision record"));
      }
    });
  });
  if (scope.supported && scope.trigger === null) {
    account = { ...account, finalAccountReady: false, finalRefundCents: null,
      notFinalReasons: [...account.notFinalReasons, "Accounting trigger is not established; only preparation is available."] };
  }
  const [recipient_ok, recipient_state, recipient_questions] = _recipient_questions(snapshot, scope, clock);
  account = { ...account, recipientState: recipient_state };
  questions.push(...recipient_questions);
  const today = _local_date(clock, release.timeZone);
  const issued = snapshot.priorStatements.filter((statement) => statement.issuedAt !== null
    && _compare_timestamps(statement.issuedAt, clock) <= 0 && valid_evidence(snapshot, statement.issuanceEvidenceIds, clock));
  const interim_issued = issued.some((statement) => statement.kind === "INTERIM");
  const interim_route = scope.supported && scope.interimQualified && (!account.finalAccountReady || interim_issued);
  if (interim_route) {
    questions.push(question("policy:INTERIM_MONEY", "What money treatment is required for this interim route?", "Qualification does not establish that all funds may be held. The supplied rule card leaves interim money handling unresolved.", "REVIEWER", [], ["REQUEST_REFUND"], "Reviewed interim refund/retention policy"));
  }
  if (interim_issued && !scope.interimQualified) {
    questions.push(question("scope:prior-interim", "What establishes the basis for the previously issued interim account?", "A historical interim document does not itself establish qualification or extend the ordinary period.", "REVIEWER", [], undefined, "Interim qualification facts and prior statement basis"));
  }
  snapshot.priorStatements.forEach((statement) => {
    if (statement.issuedAt !== null && !issued.some((entry) => _same(entry, statement))) {
      questions.push(question(`statement:${statement.versionId}:proof`, "What confirms the recorded statement dispatch?", "Dispatch needs usable case evidence and a nonfuture event time; an issuedAt value alone is insufficient.", "MANAGER", [], undefined, "Dispatch confirmation for the exact statement version"));
    }
  });
  const related_question_ids = new Set(snapshot.otherBalances.flatMap((other) => other.unresolvedQuestionIds));
  snapshot.otherBalances.forEach((other) => {
    other.unresolvedQuestionIds.forEach((key) => {
      if (!questions.some((q) => q.questionId === key)) {
        questions.push(question(key, "Resolve the separately referenced accounting question.", "An explicit unresolved balance reference remains open even when its currently supplied amount is zero.", "ACCOUNTANT", [], undefined, `Accounting question ${key} for balance ${other.balanceId}`));
      }
    });
    if (["UNKNOWN", "DISPUTED"].includes(other.state) || other.amountCents === null || !valid_evidence(snapshot, [other.sourceEvidenceId], clock)) {
      questions.push(question(`related:${other.balanceId}`, "Resolve the separately supplied accounting balance.", "This balance is not treated as an allowable deposit deduction and remains independently unresolved.", "ACCOUNTANT", [], undefined, `Accounting claim/balance record ${other.balanceId}`));
    }
  });
  questions = _dedup_questions(questions);
  const requirements: RequirementResult[] = [];

  function req(
    key: string, text: string, track: string, role: string, due: string | null = null,
    prerequisites: string[] | null = null, rule: string | null = null,
    state: string = "OPEN", reason: string = "Supported work remains incomplete.", proof: string[] | null = null,
  ): void {
    const suffix = due !== null && due < today ? " Overdue under the synthetic calendar." : "";
    requirements.push({
      requirementKey: key, question: text, ruleQuestionId: rule, track,
      dueKind: due !== null ? "LEGAL" : "UNCONFIRMED", legalDueDate: due, internalTargetAt: null,
      triggerFactKeys: due !== null ? ["ACCOUNTING_TRIGGER"] : [], state, responsibleRole: role,
      prerequisiteIds: _sorted_unique(prerequisites ?? []),
      completionCondition: track === "COMMUNICATIONS"
        ? "Record actual requirement-specific evidence; live legal completion predicate remains pending."
        : "Resolve the named prerequisite or record the specific verified outcome; no case-complete override.",
      completionEvidenceIds: _sorted_unique(proof ?? []), reason: reason + suffix,
    });
  }

  questions.forEach((q) => {
    let track = "DECISIONS";
    if (q.questionId.startsWith("money:")) track = "MONEY";
    else if (q.questionId.startsWith("related:") || related_question_ids.has(q.questionId)) track = "RELATED_ACCOUNT";
    req("question:" + q.questionId, q.question, track, q.resolverRole, null, [q.questionId], null, "BLOCKED", q.reason);
  });
  if (scope.supported && scope.trigger !== null) {
    if (interim_route) {
      req("NC:interim-account", "Prepare/verify the required interim account", "COMMUNICATIONS", "MANAGER", scope.ordinaryDue, null, "INTERIM_QUALIFICATION",
        interim_issued ? "PENDING" : "OPEN", interim_issued ? "Interim dispatch recorded; legal sufficiency/currentness not verified." : "Separate qualifying condition accepted for this test; do not wait for a final invoice.", issued.filter((statement) => statement.kind === "INTERIM").flatMap((statement) => statement.issuanceEvidenceIds));
      req("NC:final-account", "Complete final accounting when the remaining facts arrive", "COMMUNICATIONS", "MANAGER", scope.finalDue, account.unresolvedItemIds, "FINAL",
        account.finalAccountReady ? "OPEN" : "BLOCKED", "Final period is anchored to the original synthetic trigger, not to the interim statement date.");
    } else {
      req("NC:ordinary-account", "Prepare and perform ordinary final accounting", "COMMUNICATIONS", "MANAGER", scope.ordinaryDue, account.unresolvedItemIds, "ORDINARY",
        issued.length > 0 ? "PENDING" : account.finalAccountReady ? "OPEN" : "BLOCKED", issued.length > 0 ? "Dispatch has been recorded; legal sufficiency/current-version match remains pending." : "No automatic extension from missing invoices or approvals.", issued.flatMap((statement) => statement.issuanceEvidenceIds));
    }
  } else {
    req("prepare:scope-and-trigger", "Prepare the case and establish supported scope/trigger", "DECISIONS", "MANAGER", null, null, null, "BLOCKED", "No definitive legal deadline before the necessary facts and scope are established.");
  }
  req("approval:current-version", "Obtain approval of the exact current statement and recipient version", "APPROVALS", "MANAGER", null, null, null, snapshot.priorApprovals.length > 0 ? "PENDING" : "OPEN", "Prior approval records are not automatically approval of a changed current account. Exact-version execution checks belong to Phase D.");
  req("money:outstanding-work", "Resolve outstanding refund, reconciliation or ledger work", "MONEY", "ACCOUNTANT", null, null, null, money.moneyState, money.moneyReason);
  snapshot.otherBalances.forEach((other) => {
    const state = other.state === "KNOWN" && other.amountCents === 0 && other.unresolvedQuestionIds.length === 0
      && valid_evidence(snapshot, [other.sourceEvidenceId], clock) ? "NOT_APPLICABLE" : "OPEN";
    req("related:balance:" + other.balanceId, other.description, "RELATED_ACCOUNT", "ACCOUNTANT", null, null, null, state, "Separate accounting claim; not silently deducted from the deposit or marked settled.");
  });
  snapshot.relatedTasks.forEach((task) => {
    const usable_proof = valid_evidence(snapshot, task.completionEvidenceIds, clock);
    const state = task.state !== "FULFILLED" || usable_proof ? task.state : "BLOCKED";
    req("related:task:" + task.taskId, task.description, "RELATED_ACCOUNT", task.responsibleRole, null, null, null, state,
      "Related work has its own completion evidence; it neither settles nor reopens unrelated deposit obligations.", usable_proof ? task.completionEvidenceIds : []);
  });

  const proposal = "proposal:" + fingerprint({
    caseId: snapshot.caseId, rule: release.ruleReleaseId,
    items: items.map((decision) => decision.fingerprint), account: to_wire(account), recipients: to_wire(snapshot.recipients),
    trigger: scope.trigger,
  });
  const actions: AvailableAction[] = [];

  function action(
    key: string, kind: string, role: string, blockers: string[] | null = null,
    amount: number | null = null, target: string | null = null, approval: string[] | null = null,
    check_authority: boolean = true, reason: string = "Suggested work only; Phase B performs no mutation.",
  ): void {
    const pending = [...(blockers ?? [])];
    if (check_authority && _authority(snapshot, kind, role, amount, clock).length === 0) {
      const key_authority = "authority:" + kind;
      pending.push(key_authority);
      questions.push(question(key_authority, "Who has current authority for this action and amount?", `No consistent, unrevoked, effective ${role} grant within the amount limit establishes ${kind}. An owner role or supplied approval is insufficient.`, "AUTHORITY_ADMIN", [], ["SET_OR_REVOKE_AUTHORITY"], "Verified action-specific authority and approval limit"));
    }
    actions.push({
      actionKey: key, actionKind: kind, availability: pending.length > 0 ? "BLOCKED" : "AVAILABLE",
      responsibleRole: role, targetVersionId: target,
      payloadFingerprint: target ? fingerprint({ proposal, kind, amount }) : null,
      amountCents: amount, prerequisiteIds: _sorted_unique(pending), requiredApprovalScopes: approval ?? [],
      reason: reason + (pending.length > 0 ? " Current authority or named prerequisites are missing." : " Assumed synthetic authority is not an actual permission grant."),
      fallbackDescription: pending.length > 0 ? "Continue independent supported preparation; deadlines remain active." : null,
    });
  }

  if (questions.length > 0) {
    action("prepare:correct-facts", "ACCEPT_OR_CORRECT_FACT", "MANAGER", null, null, null, null, true, "Resolve the specific listed facts; do not request unrelated documents.");
  }
  items.forEach((decision) => {
    if (decision.requiresReviewer) {
      action("review-item:" + decision.itemId, "RECORD_CHARGE_DECISION", "MANAGER", scope.supported && decision.allowability !== "NOT_EVALUATED" ? [] : ["supported-scope-and-category"], null, null, null, true, "Review the affected item against its source; retain unrelated supported decisions.");
    }
  });
  const can_prepare = scope.supported && scope.trigger !== null && (account.finalAccountReady || interim_route);
  const draft_blockers = can_prepare ? [] : ["supported-scope-trigger-and-account"];
  let preparation_reason = "Statement preparation awaits the named facts.";
  if (account.finalAccountReady) preparation_reason = "Prepare a final statement proposal.";
  else if (interim_route) preparation_reason = "Prepare supported interim itemization; money policy still needs review.";
  action("prepare:statement", "PREPARE_STATEMENT", "MANAGER", draft_blockers, null, proposal, null, true, preparation_reason + " No document is generated or sent by this review.");
  action("approve:statement", "APPROVE_EXACT_VERSION", "MANAGER", ["current-immutable-statement-version", "phase-d-approval-interface"], null, proposal,
    ["statement-content", "recipient-instructions"], true, "An account calculation is not an approved statement version.");
  const send_blockers = ["exact-current-version-approval", "phase-d-execution-interface", ...(recipient_ok ? [] : ["recipient:instructions"])];
  if (!can_prepare) send_blockers.push("supported-scope-trigger-and-account");
  action("request:dispatch", "REQUEST_STATEMENT_DISPATCH", "MANAGER", send_blockers, null, proposal, ["statement-content", "recipient-instructions"]);
  const refund_blockers = ["exact-current-version-approval", "phase-d-execution-interface"];
  if (!account.finalAccountReady) refund_blockers.push("final-account");
  if (!recipient_ok) refund_blockers.push("recipient:instructions");
  if (interim_route && !account.finalAccountReady) refund_blockers.push("policy:INTERIM_MONEY");
  if (money.hasUnknownResult) refund_blockers.push("reconcile-unknown-result");
  if (account.pendingReservedRefundCents === null || account.pendingReservedRefundCents > 0) refund_blockers.push("existing-reservation-or-unknown");
  if (money.hasReturn) refund_blockers.push("authorize-replacement-after-return");
  action("request:refund", "REQUEST_REFUND", "ACCOUNTANT", refund_blockers, account.finalRefundCents, proposal, ["refund-amount", "recipient-instructions"]);
  if (money.questions.length > 0) {
    action("reconcile:money", "RECONCILE_MONEY_RECORD", "ACCOUNTANT", null, null, null, null, true, "Resolve the named accounting evidence/basis without sending money or posting entries.");
  }
  action("review:repeat", "RECHECK_CASE", "MANAGER", null, null, null, null, false, "Read-only recomputation at an explicit clock; not an executable Ontology Action.");

  questions = _dedup_questions(questions);
  questions.filter((q) => q.questionId.startsWith("authority:")).forEach((q) => {
    req("question:" + q.questionId, q.question, "APPROVALS", "AUTHORITY_ADMIN", null, [q.questionId], null, "BLOCKED", q.reason);
  });

  // Recorded dispatch is not legal sufficiency: pending legal-completion policy forbids Complete.
  const decision_blocked = !scope.supported || scope.trigger === null || items.some((decision) => decision.requiresReviewer);
  const related = requirements.filter((requirement) => requirement.track === "RELATED_ACCOUNT");
  const related_state = related.length === 0 ? "NOT_APPLICABLE"
    : related.every((requirement) => ["FULFILLED", "NOT_APPLICABLE"].includes(requirement.state)) ? "FULFILLED" : "OPEN";
  const states: Array<[string, string, string]> = [
    ["DECISIONS", decision_blocked ? "BLOCKED" : "READY", decision_blocked ? "Specific unresolved inputs remain." : "Supported item decisions are ready; this does not imply approval or execution."],
    ["COMMUNICATIONS", issued.length > 0 ? "PENDING" : "OPEN", issued.length > 0 ? "Dispatch records retained; legal sufficiency/current-version match is not established." : "No verified dispatch has been recorded."],
    ["APPROVALS", questions.some((q) => q.questionId.startsWith("authority:")) ? "BLOCKED" : snapshot.priorApprovals.length > 0 ? "PENDING" : "OPEN", "Exact current-version approval and authority must be checked by the later controlled interface."],
    ["MONEY", money.moneyState, money.moneyReason],
    ["RELATED_ACCOUNT", related_state, "Related claims/tasks are assessed independently of the deposit."],
  ];
  const tracks: TrackOutcome[] = states.map(([track, state, reason]) => ({
    track, state,
    openRequirementKeys: requirements.filter((requirement) => requirement.track === track && !["FULFILLED", "NOT_APPLICABLE"].includes(requirement.state)).map((requirement) => requirement.requirementKey).sort(_compare_text),
    completionEvidenceIds: _sorted_unique(requirements.filter((requirement) => requirement.track === track).flatMap((requirement) => requirement.completionEvidenceIds)),
    reason,
  }));
  const scope_result: ScopeRequirements = {
    scopeState: scope.state, jurisdiction: snapshot.jurisdiction, regime: snapshot.tenancyRegime,
    ruleReleaseId: release.ruleReleaseId, ruleStatus: release.status,
    appliedQuestionIds: scope.supported ? ["SCOPE", "DAMAGE", "TRIGGER", "ORDINARY", ...(interim_route ? ["INTERIM_QUALIFICATION", "INTERIM_MONEY", "FINAL"] : [])] : [],
    limitations: scope.limitations,
    requirements: requirements.sort((a, b) => _compare_text(a.requirementKey, b.requirementKey)),
  };
  const summary = tracks.map((track) => `${track.track}: ${track.state}`).join("; ") + ". Synthetic review only; no live legal completion or execution claim.";
  return {
    scopeRequirements: scope_result, itemDecisions: items, account, missingInputs: questions,
    actions: actions.sort((a, b) => _compare_text(a.actionKey, b.actionKey)),
    outcomes: { tracks, depositComplete: false, overallCaseComplete: false, summary },
  };
}

/**
 * Build a strictly validated, fingerprinted envelope from an explicitly versioned request.
 * @param request Full JSON-contract DTO; nullable fields must be present.
 * @param rule_release Explicit validated Phase B rule release.
 * @returns A normalized envelope; no persistence, approval, dispatch or payment occurs.
 */
export function review_request(request: ReviewRequest, rule_release: ReviewRuleRelease): ReviewEnvelope {
  request = from_wire("ReviewRequest", to_wire(request)) as ReviewRequest;
  const release = from_wire("ReviewRuleRelease", to_wire(rule_release)) as ReviewRuleRelease;
  if (request.ruleReleaseId !== release.ruleReleaseId) {
    throw new ContractError("Requested rule release is not the explicitly loaded synthetic release");
  }
  const result = review_case(request.snapshot, release, request.reviewClock);
  const digest = fingerprint({ request: to_wire(request), ruleRelease: to_wire(release) });
  const envelope: ReviewEnvelope = {
    metadata: {
      schemaVersion: OUTPUT_SCHEMA_VERSION, baseCaseRevision: request.snapshot.revision, inputHash: digest,
      ruleReleaseId: release.ruleReleaseId, codeVersion: release.codeVersion, reviewClock: request.reviewClock,
    },
    result,
  };
  return from_wire("ReviewEnvelope", to_wire(envelope)) as ReviewEnvelope;
}
