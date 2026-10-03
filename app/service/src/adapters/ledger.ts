/** The property-management ledger: the books of record. Handoff reads it and posts accepted results to it. */
export type LedgerCode = "rent" | "charge" | "credit" | "payment" | "deposit_received" | "deposit_applied" | "refund" | "write_off" | "collections_transfer";

export interface LedgerTransaction {
  ref: string;
  postedOn: string;
  code: LedgerCode;
  description: string;
  /** Positive is charged to the resident, negative is credited. */
  amountCents: number;
}

export interface LedgerPosting {
  tenancyRef: string;
  postedOn: string;
  code: LedgerCode;
  description: string;
  /** Positive is charged to the resident, negative is credited. */
  amountCents: number;
}

export interface Ledger {
  transactions(tenancyRef: string): Promise<LedgerTransaction[]>;
  post(p: LedgerPosting, key: string): Promise<{ ref: string }>;
  find(key: string): Promise<{ ref: string } | null>;
}
