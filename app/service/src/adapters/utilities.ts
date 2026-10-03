/** The utility billing agent that reads submeters and bills residents. Its bills arrive as events. */
export interface UtilityBill {
  ref: string;
  utility: "water" | "sewer" | "trash" | "gas" | "electric";
  periodStart: string;
  periodEnd: string;
  amountCents: number;
  /** How the final usage was set: an actual read, or the previous month's bill when no read was possible. */
  readType: "actual" | "previous_month" | "estimated";
  issuedOn: string;
}

export interface UtilityBiller {
  /** Asks for the final reads and bills for a tenancy ending on `moveOutOn`. */
  requestFinalBills(r: { caseId: string; tenancyRef: string; moveOutOn: string }, key: string): Promise<{ ref: string }>;
  findRequest(key: string): Promise<{ ref: string } | null>;
  bills(tenancyRef: string): Promise<UtilityBill[]>;
}
