import type {
  AuthorityGrant, BalanceSnapshot, ChargeInput, DateFact, EvidenceInput,
  MoneyEvent, RecipientInstructions, RelatedTaskFact, ReviewRequest,
} from "../domain/types.js";

/** Internal work only: never a legal deadline, permission or completion claim. */
export interface WorkAssignment {
  requirementKey: string;
  assigneePartyId: string;
  internalTargetAt: string | null;
  reason: string;
  assignedBy: string;
  assignedAt: string;
}

export type ChangeKind =
  | "ADD_EVIDENCE" | "ASSOCIATE_EVIDENCE" | "ACCEPT_DATE_FACT"
  | "RECORD_CHARGE_DECISION" | "WAIVE_CHARGE" | "SET_RECIPIENTS"
  | "RECORD_MONEY_EVENT" | "RECONCILE_BALANCE" | "UPDATE_AUTHORITY"
  | "ASSIGN_WORK" | "RECORD_RELATED_TASK" | "RECHECK" | "ADVANCE_DEMO_CLOCK";

export interface AssociateEvidencePayload {
  evidenceId: string;
  itemIds: string[];
  accepted: boolean;
  reason: string;
}
export interface ChargeDecisionPayload {
  charge: ChargeInput;
  resolvedQuestionIds: string[];
}
export interface WaiveChargePayload { itemId: string; reason: string; }
export interface AssignWorkPayload {
  requirementKey: string;
  assigneePartyId: string;
  internalTargetAt: string | null;
  reason: string;
}
export interface AdvanceClockPayload { reviewClock: string; reason: string; }

export type CaseChange =
  | { kind: "ADD_EVIDENCE"; payload: EvidenceInput }
  | { kind: "ASSOCIATE_EVIDENCE"; payload: AssociateEvidencePayload }
  | { kind: "ACCEPT_DATE_FACT"; payload: DateFact }
  | { kind: "RECORD_CHARGE_DECISION"; payload: ChargeDecisionPayload }
  | { kind: "WAIVE_CHARGE"; payload: WaiveChargePayload }
  | { kind: "SET_RECIPIENTS"; payload: RecipientInstructions }
  | { kind: "RECORD_MONEY_EVENT"; payload: MoneyEvent }
  | { kind: "RECONCILE_BALANCE"; payload: BalanceSnapshot }
  | { kind: "UPDATE_AUTHORITY"; payload: AuthorityGrant }
  | { kind: "ASSIGN_WORK"; payload: AssignWorkPayload }
  | { kind: "RECORD_RELATED_TASK"; payload: RelatedTaskFact }
  | { kind: "RECHECK"; payload: Record<string, never> }
  | { kind: "ADVANCE_DEMO_CLOCK"; payload: AdvanceClockPayload };

export interface ChangeResult {
  request: ReviewRequest;
  workAssignments: WorkAssignment[];
  summary: Record<string, string | number | boolean | null>;
}
