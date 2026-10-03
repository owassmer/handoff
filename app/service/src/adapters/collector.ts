/** The licensed collection agency a balance can be handed to. Its reports come back as events. */
export interface PlacementComponent {
  componentId: string;
  description: string;
  amountCents: number;
  /** Postpaid utilities are consumer credit; rent paid in advance is not. The collector's notices depend on it. */
  consumerCredit: boolean;
}

export interface Placement {
  caseId: string;
  debtorPartyId: string;
  creditor: string;
  components: PlacementComponent[];
}

export interface PlacementStatus {
  ref: string;
  balanceCents: number;
  components: Array<{ componentId: string; amountCents: number }>;
}

export interface Collector {
  place(p: Placement, key: string): Promise<{ ref: string }>;
  adjust(a: { placementRef: string; componentId: string; amountCents: number; reason: string }, key: string): Promise<{ ref: string }>;
  find(key: string): Promise<{ ref: string } | null>;
  /** What the collector currently says the debtor owes. Corrections not yet applied are not in it. */
  status(placementRef: string): Promise<PlacementStatus>;
}
