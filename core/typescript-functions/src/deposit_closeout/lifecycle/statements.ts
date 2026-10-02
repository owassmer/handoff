/** Immutable, deterministic synthetic text. Preparation is not delivery or legal performance. */
import { ContractError, from_wire } from "../domain/codec.js";
import { review_scope } from "../domain/rules.js";
import type { ReviewEnvelope, ReviewRequest, SourceReference } from "../domain/types.js";
import release from "../resources/rules/nc_synthetic_review_v1.json" with { type: "json" };
import { entitlementReview, routeUsable, statementMaterialityHash, workflowScope } from "./materiality.js";
import { statementContentHash, statementIdFor } from "./ids.js";
import { projectRequests } from "./events.js";
import { SYNTHETIC_STATEMENT_BADGE } from "./types.js";
import type { PrepareStatementPayload, PureContext, StatementContent, StatementKind, StatementVersionRecord, WorkflowStateV2 } from "./types.js";

function statementReadiness(request: ReviewRequest, base: ReviewEnvelope, kind: StatementKind): boolean {
  const scope = review_scope(request.snapshot, from_wire("ReviewRuleRelease", release), request.reviewClock);
  if (!scope.supported || scope.trigger === null || base.result.scopeRequirements.scopeState !== "SUPPORTED") return false;
  return kind === "INTERIM" ? scope.interimQualified : base.result.account.finalAccountReady;
}

export function statementBasisCurrent(
  request: ReviewRequest, _base: ReviewEnvelope, state: WorkflowStateV2, statement: StatementVersionRecord,
): boolean {
  try {
    return statement.caseId === state.caseId && statement.managementCompanyId === state.managementCompanyId
      && statement.environmentId === state.environmentId && statement.recipientVersionId === state.statementInstructions.versionId
      && statementReadiness(request, entitlementReview(request, state), statement.kind)
      && statement.materialityHash === statementMaterialityHash(request, state, statement.kind);
  } catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    return false; // Historical content remains intact when its basis is unverifiable.
  }
}

/** Exact cents render without binary floating point rounding; null is never zero. */
export function renderCents(value: number | null): string {
  if (value === null) return "UNKNOWN";
  if (!Number.isSafeInteger(value)) throw new ContractError("Statement amount is not exact integer cents");
  const integer = BigInt(value);
  const abs = integer < 0n ? -integer : integer;
  const dollars = (abs / 100n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return `${integer < 0n ? "-" : ""}$${dollars}.${(abs % 100n).toString().padStart(2, "0")} USD`;
}

export function renderStatement(content: StatementContent): string {
  const a = content.account;
  return [SYNTHETIC_STATEMENT_BADGE, content.title,
    "Recipients: " + content.parties.map((party): string => `${party.displayLabel} [${party.partyId}]`).join("; "),
    ...content.dates.map((fact): string => `${fact.factKey}: ${fact.value ?? "UNKNOWN"} (${fact.state})`),
    "Itemization:", ...content.items.map((item): string => {
      const d = item.decision;
      return `${item.itemId} | ${item.location} | ${item.description} | ${d.allocation} / ${d.allowability} / ${d.choiceState}`
        + ` | cost ${renderCents(d.vendorCostCents)} | supported ${renderCents(d.supportedAmountCents)} | chosen ${renderCents(d.chosenAmountCents)} | ${d.reason}`;
    }),
    `Recorded deposit: ${renderCents(a.recordedDepositCents)}`,
    `Known chosen deductions: ${renderCents(a.knownChosenDeductionsCents)}`,
    `Total deductions: ${renderCents(a.totalDeductionsCents)}`,
    `Net postings: ${renderCents(a.existingNetPostingCents)}; posting adjustment: ${renderCents(a.postingDeltaCents)}`,
    `Deposit applications: ${renderCents(a.existingDepositApplicationsCents)}; application adjustment: ${renderCents(a.depositApplicationDeltaCents)}`,
    `Prior net refunds: ${renderCents(a.priorNetRefundsCents)}; reserved refunds: ${renderCents(a.pendingReservedRefundCents)}`,
    `Unpaid final refund: ${renderCents(a.finalRefundCents)}`,
    `Proposed excess receivable: ${renderCents(a.proposedExcessReceivableCents)}`,
    `Account: ${a.finalAccountReady ? "FINAL ACCOUNT READY" : "NOT FINAL"}; reconciliation: ${a.reconciliationState}`,
    ...a.notFinalReasons,
    "Unknown amounts remain unknown. Interim money treatment is unresolved; no full-withholding policy is inferred.",
    "Sources:", ...content.sourceReferences.map((source): string => `${source.evidenceId} | ${source.sourceClass} | ${source.sourceVersion} | ${source.locator}`),
    "No dispatch, payment, legal sufficiency or legal performance is asserted.",
  ].join("\n");
}

/** Validate supplied references even when preparation can reuse an existing version. */
function requireValidSupersession(state: WorkflowStateV2, payload: PrepareStatementPayload): StatementVersionRecord | null {
  if (payload.supersedesId === null) {
    if (payload.kind === "CORRECTIVE") throw new ContractError("A corrective statement must reference an earlier statement");
    return null;
  }
  const earlier = state.statements.find((entry): boolean => entry.statementId === payload.supersedesId);
  if (earlier === undefined) throw new ContractError("Statement refers to a missing earlier version");
  if (payload.kind !== "CORRECTIVE" && earlier.kind !== payload.kind) {
    throw new ContractError("Draft replacement must reference an earlier statement of the same kind");
  }
  return earlier;
}

/** FINAL and CORRECTIVE serve the final account; INTERIM is an independent duty. */
function sameStatementDuty(left: StatementKind, right: StatementKind): boolean {
  return (left === "INTERIM") === (right === "INTERIM");
}

function statementLineage(state: WorkflowStateV2, statement: StatementVersionRecord | null): Set<string> {
  const statements = new Map(state.statements.map((entry) => [entry.statementId, entry]));
  const ids = new Set<string>();
  let current = statement;
  while (current !== null && !ids.has(current.statementId)) {
    ids.add(current.statementId);
    current = current.supersedesStatementId === null ? null : statements.get(current.supersedesStatementId) ?? null;
  }
  return ids;
}

/** New versions must preserve authoritative attempted/issued history, not a caller-selected draft. */
function requireCorrectiveLineage(state: WorkflowStateV2, payload: PrepareStatementPayload, earlier: StatementVersionRecord | null): void {
  const currents = new Map(projectRequests(state).map((entry) => [entry.requestId, entry]));
  const dispatches = state.requests.filter((entry): boolean => entry.kind === "STATEMENT_DISPATCH");
  const lineage = statementLineage(state, earlier);
  const duties: StatementKind[] = [payload.kind];
  // A final-account correction explicitly referring to interim history must also
  // retain that history. It cannot use an unrelated interim draft to skip it.
  if (payload.kind === "CORRECTIVE" && state.statements.some((entry): boolean => entry.kind === "INTERIM"
    && lineage.has(entry.statementId))) duties.push("INTERIM");
  duties.forEach((duty): void => {
    const protectedStatement = [...state.statements].reverse().find((statement): boolean => sameStatementDuty(statement.kind, duty)
      && dispatches.some((entry): boolean => entry.intent.statementId === statement.statementId
        && currents.get(entry.requestId)!.attemptId !== null));
    if (protectedStatement === undefined) return;
    const issued = dispatches.some((entry): boolean => entry.intent.statementId === protectedStatement.statementId
      && currents.get(entry.requestId)!.state === "SUCCEEDED");
    // Claiming may already mean sending. An unaccepted raw success is NOT issuance;
    // failure or uncertainty likewise cannot make that attempt an unsent draft.
    if (payload.kind !== "CORRECTIVE") {
      if (issued) throw new ContractError("An issued statement requires a CORRECTIVE version, not a draft replacement");
      throw new ContractError("A potentially attempted dispatch requires CORRECTIVE preparation or reconciliation, not a draft replacement");
    }
    if (!lineage.has(protectedStatement.statementId)) {
      throw new ContractError("A corrective statement must reference the latest issued or potentially attempted statement, or a correction linked to it");
    }
  });
}

/** Caller authorizes the manager; this pure builder never edits earlier versions. */
export function prepareStatement(
  request: ReviewRequest, base: ReviewEnvelope, state: WorkflowStateV2, payload: PrepareStatementPayload, ctx: PureContext,
): StatementVersionRecord {
  if (!statementReadiness(request, base, payload.kind)) {
    throw new ContractError("Statement requires supported scope/trigger and a complete account, or separately accepted supported interim qualification");
  }
  const earlier = requireValidSupersession(state, payload);
  const materialityHash = statementMaterialityHash(request, state, payload.kind);
  // Reuse only the latest version for this duty, never resurrect an ancient match
  // past a more recent correction. Issuance does not itself change frozen content.
  const latest = [...state.statements].reverse().find((entry): boolean => sameStatementDuty(entry.kind, payload.kind));
  if (latest !== undefined && latest.kind === payload.kind && latest.materialityHash === materialityHash
    && latest.recipientVersionId === state.statementInstructions.versionId
    && (payload.supersedesId === null || latest.supersedesStatementId === payload.supersedesId)) {
    return structuredClone(latest);
  }
  requireCorrectiveLineage(state, payload, earlier);
  const parties = [...state.statementInstructions.partyIds].sort().map((id) => {
    const matches = request.snapshot.parties.filter((party): boolean => party.partyId === id);
    if (matches.length !== 1 || !matches[0]!.roles.some((role): boolean => ["RESIDENT", "SIGNATORY"].includes(role))) {
      throw new ContractError("Statement needs known intended resident/signatory parties; no labels are invented");
    }
    return { partyId: id, displayLabel: matches[0]!.displayLabel };
  });
  if (parties.length === 0) throw new ContractError("Select intended statement parties before preparation");
  const sourceIds = new Set([...request.snapshot.agreementEvidenceIds, ...state.statementInstructions.evidenceIds,
    request.snapshot.depositBalance.sourceEvidenceId, ...request.snapshot.dates.flatMap((fact): string[] => fact.evidenceIds),
    ...base.result.itemDecisions.flatMap((item): string[] => item.sourceReferences.map((ref): string => ref.evidenceId)),
    ...(payload.kind === "INTERIM" ? request.snapshot.interimConditionEvidenceIds : [])]);
  const refs: SourceReference[] = request.snapshot.evidence.filter((entry): boolean => sourceIds.has(entry.evidenceId))
    .sort((a, b): number => a.evidenceId.localeCompare(b.evidenceId, "en"))
    .map((entry): SourceReference => ({ evidenceId: entry.evidenceId, sourceClass: entry.sourceClass,
      sourceVersion: entry.sourceVersion, locator: entry.locator, page: null, quote: entry.excerpt }));
  const content: StatementContent = {
    mode: "SIMULATED", syntheticBadge: SYNTHETIC_STATEMENT_BADGE, title: `${payload.kind} deposit closeout statement`, parties,
    dates: request.snapshot.dates.map((fact) => ({ factKey: fact.factKey,
      state: fact.state as StatementContent["dates"][number]["state"], value: fact.state === "ACCEPTED" ? fact.value : null }))
      .sort((a, b): number => a.factKey < b.factKey ? -1 : a.factKey > b.factKey ? 1 : 0),
    items: base.result.itemDecisions.map((decision) => {
      const item = request.snapshot.charges.find((entry): boolean => entry.itemId === decision.itemId);
      if (item === undefined) throw new ContractError("Statement item is outside this case");
      return { itemId: item.itemId, location: item.location, description: item.description, decision: structuredClone(decision) };
    }),
    account: { ...structuredClone(base.result.account), recipientInstructionsVersion: state.statementInstructions.versionId,
      recipientState: routeUsable(request, state.statementInstructions, request.reviewClock) ? "VERIFIED" : "MISSING" },
    sourceReferences: refs,
  };
  const renderedText = renderStatement(content);
  const contentHash = statementContentHash(content, renderedText);
  const basis = { kind: payload.kind, materialityHash, contentHash, recipientVersionId: state.statementInstructions.versionId,
    supersedesStatementId: payload.supersedesId };
  return { ...workflowScope(request), ...basis, statementId: statementIdFor(state, basis),
    createdCommandId: ctx.commandId, createdBy: ctx.actorId, createdAt: ctx.serverNow, businessCreatedAt: state.businessClock,
    sourceReviewId: ctx.basisReviewId, content, renderedText };
}
