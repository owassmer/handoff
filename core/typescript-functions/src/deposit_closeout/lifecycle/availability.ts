/** Shared pure monetary capacity; not approval, authority, reconciliation or source admission. */
import { ContractError } from "../domain/codec.js";
import type { AccountResult, RequestFact } from "../domain/types.js";
import type { CurrentRequest, FinancialOperationKind } from "./types.js";

export const ACTIVE_WORKFLOW_STATES = new Set(["READY", "CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN"]);

/** Exact bounds for ALL new arithmetic; null is handled by callers, never as zero. */
export function checkedCents(value: bigint): number {
  if (value < 0n || value > BigInt(Number.MAX_SAFE_INTEGER)) throw new ContractError("Workflow amount exceeds exact nonnegative cents range");
  return Number(value);
}
function nativeCents(value: number, signed: boolean = false): bigint {
  if (!Number.isSafeInteger(value) || (!signed && value < 0)) throw new ContractError("Workflow amount is not exact nonnegative cents");
  return BigInt(value);
}
export function sumCents(values: readonly number[]): number {
  return checkedCents(values.reduce((sum, value): bigint => sum + nativeCents(value), 0n));
}
function floorCents(value: bigint): number { return checkedCents(value > 0n ? value : 0n); }
export function unreservedCents(amount: number, reserved: number): number {
  return floorCents(nativeCents(amount) - nativeCents(reserved));
}

/** Native unpaid refund still includes reservations; signed adjustments retain their separate kinds. */
export function desiredOperationCents(account: AccountResult, kind: FinancialOperationKind): number | null {
  if (kind === "REFUND") return account.finalRefundCents === null ? null : checkedCents(nativeCents(account.finalRefundCents));
  const delta = kind.startsWith("CHARGE_POSTING") ? account.postingDeltaCents : account.depositApplicationDeltaCents;
  if (delta === null) return null;
  const signed = nativeCents(delta, true);
  return floorCents(kind.endsWith("_REVERSAL") ? -signed : signed);
}

export interface FinancialAvailability {
  kindBudgetCents: number | null;
  heldCashBudgetCents: number | null;
  availableCents: number | null;
}

/**
 * Project NEW-intent capacity by default. Only existing-request claim/send checks
 * (and their claim affordance) exclude that request's own commitment. Never use
 * exclusion for the newlyRequestableRefundCents account readout.
 *
 * @param account Unchanged native account on projectNativeFacts; callers retain verification gates.
 * @param currentRequests D commitments projected from immutable lifecycle events.
 * @param nativeRequests Native/external request facts, to identify unclassified ledger commitments.
 * @param kind Separate operation kind; posting and cash-in reversals are NOT held-cash gated.
 * @param excludeRequestId Existing request being rechecked, or null for a new intent.
 * @returns Exact, floored monetary budgets, or null where capacity cannot be verified.
 */
export function financialAvailability(account: AccountResult, currentRequests: readonly CurrentRequest[],
  nativeRequests: readonly RequestFact[], kind: FinancialOperationKind, excludeRequestId: string | null = null): FinancialAvailability {
  const active = currentRequests.filter((entry): boolean => ACTIVE_WORKFLOW_STATES.has(entry.state));
  const own = active.find((entry): boolean => entry.requestId === excludeRequestId);
  // Native reserves include D AND external refunds. Do not add D refunds again.
  const refundReserved = account.pendingReservedRefundCents === null ? null : nativeCents(account.pendingReservedRefundCents);
  const ownRefundReserved = own?.kind === "REFUND" ? nativeCents(own.reservedAmountCents) : 0n;
  if (refundReserved !== null && refundReserved < ownRefundReserved) {
    throw new ContractError("Native refund reservations do not cover this request's own commitment.");
  }
  const otherRefundReserved = refundReserved === null ? null : refundReserved - ownRefundReserved;
  const desired = desiredOperationCents(account, kind);
  const reserved = kind === "REFUND" ? otherRefundReserved : BigInt(sumCents(active
    .filter((entry): boolean => entry.kind === kind && entry.requestId !== excludeRequestId)
    .map((entry): number => entry.reservedAmountCents)));
  const kindBudgetCents = desired === null || reserved === null ? null : floorCents(BigInt(desired) - reserved);
  if (kind !== "REFUND" && kind !== "DEPOSIT_APPLICATION") {
    return { kindBudgetCents, heldCashBudgetCents: null, availableCents: kindBudgetCents };
  }

  const knownIds = new Set(currentRequests.map((entry): string => entry.requestId));
  // REQUEST_LEDGER_POSTING alone does not say whether cash was promised. Do not
  // invent a subtype or treat ambiguous external pending work as spare cash.
  const ambiguousLedger = nativeRequests.some((entry): boolean => entry.actionKind === "REQUEST_LEDGER_POSTING"
    && ACTIVE_WORKFLOW_STATES.has(entry.state) && !knownIds.has(entry.requestId));
  let heldCashBudgetCents: number | null = null;
  if (account.recordedDepositCents !== null && otherRefundReserved !== null && !ambiguousLedger) {
    const otherApplications = BigInt(sumCents(active
      .filter((entry): boolean => entry.kind === "DEPOSIT_APPLICATION" && entry.requestId !== excludeRequestId)
      .map((entry): number => entry.reservedAmountCents)));
    // Liability is not custody: pending reversals/returns do not fund outflows.
    // Only verified native settlements change held cash; postings are noncash.
    heldCashBudgetCents = floorCents(nativeCents(account.recordedDepositCents) - otherRefundReserved - otherApplications);
  }
  const availableCents = kindBudgetCents === null || heldCashBudgetCents === null ? null
    : checkedCents(BigInt(kindBudgetCents) < BigInt(heldCashBudgetCents) ? BigInt(kindBudgetCents) : BigInt(heldCashBudgetCents));
  return { kindBudgetCents, heldCashBudgetCents, availableCents };
}
