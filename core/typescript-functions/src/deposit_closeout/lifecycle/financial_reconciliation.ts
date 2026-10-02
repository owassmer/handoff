/** New financial work must honor unresolved evidence, not just the terminal state label. */
import { ContractError } from "../domain/codec.js";
import type { RequestFact } from "../domain/types.js";
import type { CurrentRequest } from "./types.js";

export function isUnresolvedFinancialRequest(current: CurrentRequest): boolean {
  return current.kind !== "STATEMENT_DISPATCH"
    && (current.reconciliationRequired || current.state === "OUTCOME_UNKNOWN");
}

/**
 * Admission only: never use this gate for result ingestion, withdrawal, historical
 * approval validity or statement communications. A FAILED projection with raw
 * possible success still requires reconciliation; zero reserve is not clearance.
 *
 * @param nativeRequests Native/external facts, which lack the D reconciliation flag.
 * @param currentRequests Current D evidence projections, without changing history or reserves.
 */
export function requireResolvedFinancialRequests(
  nativeRequests: readonly RequestFact[], currentRequests: readonly CurrentRequest[],
): void {
  const unresolvedNative = nativeRequests.some((fact): boolean => fact.state === "OUTCOME_UNKNOWN"
    && ["REQUEST_REFUND", "REQUEST_LEDGER_POSTING"].includes(fact.actionKind));
  if (unresolvedNative || currentRequests.some(isUnresolvedFinancialRequest)) {
    throw new ContractError("Resolve unknown or contradictory financial request evidence through explicit reconciliation before new financial work.");
  }
}
