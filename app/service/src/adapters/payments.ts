/** Money leaving the operator. Production uses the operator's bank or payment processor. */
export type PaymentMethod = "mailed_check" | "electronic_transfer";

export interface PaymentOrder {
  caseId: string | null;
  payeePartyId: string;
  amountCents: number;
  method: PaymentMethod;
  memo: string;
}

export interface PaymentReceipt {
  paymentId: string;
  status: "submitted" | "settled" | "returned";
  submittedAt: string;
}

/** A definite refusal by the bank: the payment did not happen. */
export class PaymentDeclined extends Error {}

export interface Payments {
  send(order: PaymentOrder, key: string): Promise<PaymentReceipt>;
  find(key: string): Promise<PaymentReceipt | null>;
}
