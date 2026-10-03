import type { CaseTurn, TurnContext } from "../src/runner.js";

export const at = (iso: string) => new Date(iso);

export const DECIDER = { kind: "operator", userId: "op-decider" } as const;
export const ADMIN = { kind: "operator", userId: "op-admin" } as const;
export const COORDINATOR = { kind: "operator", userId: "op-coordinator" } as const;

export { seedDemoCase as seedCase } from "../src/demo/seed.js";

export function statement(overrides: { amountCents?: number; payeePartyId?: string; method?: "mailed_check" | "electronic_transfer"; closetCents?: number } = {}) {
  const lines = [
    { lineKey: "holdover", kind: "rent_due" as const, description: "Rent for Nov 11-16, 6 days at $91.17", amountCents: 54700, documentIds: [], estimate: false },
    { lineKey: "closet-repair", kind: "charge" as const, description: "Bedroom 2 closet door and track, tenant share", amountCents: overrides.closetCents ?? 55000, documentIds: [], estimate: false },
    { lineKey: "cleaning", kind: "charge" as const, description: "Cleaning, 3.5 hours", amountCents: 60791, documentIds: [], estimate: false },
  ];
  const left = 243750 - lines.reduce((t, l) => t + l.amountCents, 0);
  const amountCents = overrides.amountCents ?? left;
  return {
    depositCents: 243750,
    lines,
    refund: { payeePartyId: overrides.payeePartyId ?? "tenant-1", amountCents, method: overrides.method ?? ("electronic_transfer" as const) },
    message: { toPartyId: "tenant-1", subject: "Your deposit statement", body: `Your refund of $${(amountCents / 100).toFixed(2)} is on its way.` },
  };
}

export function refundOf(decisionId: string, content: ReturnType<typeof statement>) {
  return { decisionId, ...content.refund };
}

/** A turn that does nothing but remember what it was given. */
export function recordingTurn(): { turn: CaseTurn; seen: Array<{ wokeAt: Date; kinds: string[] }> } {
  const seen: Array<{ wokeAt: Date; kinds: string[] }> = [];
  return { seen, turn: async (ctx: TurnContext) => void seen.push({ wokeAt: ctx.wokeAt, kinds: ctx.events.map((e) => e.kind) }) };
}

export const noTurn: CaseTurn = async () => {};
