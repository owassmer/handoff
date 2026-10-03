/** Outside vendors. Quotes, completions and invoices come back from them as untrusted messages. */
export interface QuoteRequest {
  caseId: string;
  vendorPartyId: string;
  scope: string;
}

export interface VendorOrder {
  caseId: string;
  vendorPartyId: string;
  scope: string;
  notToExceedCents: number;
}

export interface Vendors {
  requestQuote(r: QuoteRequest, key: string): Promise<{ ref: string }>;
  placeOrder(o: VendorOrder, key: string): Promise<{ ref: string }>;
  find(key: string): Promise<{ ref: string } | null>;
}
