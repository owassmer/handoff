import type { Queryable } from "../src/db.js";
import type { CaseTurn, TurnContext } from "../src/runner.js";

export const at = (iso: string) => new Date(iso);

export const DECIDER = { kind: "operator", userId: "op-decider" } as const;
export const ADMIN = { kind: "operator", userId: "op-admin" } as const;
export const COORDINATOR = { kind: "operator", userId: "op-coordinator" } as const;

/** The demonstration tenancy from design/DESIGN.md §1, with placeholder names. */
export async function seedCase(q: Queryable, caseId = "case-1"): Promise<void> {
  await q.query(`insert into users (id, name, email, permissions) values
    ('op-decider', 'Property manager', 'pm@manager.test', '{view,work,decide}'),
    ('op-admin', 'Regional director', 'rd@manager.test', '{view,work,decide,configure}'),
    ('op-coordinator', 'Leasing coordinator', 'lc@manager.test', '{view,work}')`);
  await q.query(`insert into parties (id, kind, name, email) values
    ('tenant-1', 'person', 'Demo Tenant', 'tenant@resident.test'),
    ('owner-1', 'organization', 'Demo Owner LLC', 'owner@owner.test'),
    ('vendor-1', 'organization', 'Demo Carpentry', 'jobs@carpentry.test')`);
  await q.query(`insert into properties (id, name, address, legal_layers) values
    ('prop-1', 'Demo community', 'Huntington Beach, CA', '{US,CA,CA-OC,CA-HB}')`);
  await q.query(`insert into units (id, property_id, label, bedrooms, bathrooms, square_feet) values ('unit-1', 'prop-1', '308', 3, 2, 1028)`);
  await q.query(`insert into tenancies (id, unit_id, starts_on, ends_on, rent_cents, deposit_cents) values
    ('ten-1', 'unit-1', '2025-11-11', '2026-11-10', 273500, 243750)`);
  await q.query(`insert into tenancy_parties (tenancy_id, party_id, relationship) values
    ('ten-1', 'tenant-1', 'tenant'), ('ten-1', 'owner-1', 'owner')`);
  await q.query(`insert into cases (id, tenancy_id, opened_at) values ($1, 'ten-1', '2026-10-12T16:00:00Z')`, [caseId]);
}

export function statement(overrides: { amountCents?: number; payeePartyId?: string; method?: string } = {}) {
  const amountCents = overrides.amountCents ?? 73259;
  return {
    depositCents: 243750,
    lines: [
      { item: "holdover rent, 6 days", cents: 54700 },
      { item: "closet repair, tenant share", cents: 55000 },
      { item: "cleaning, 3.5 hours", cents: 60791 },
    ],
    refund: { payeePartyId: overrides.payeePartyId ?? "tenant-1", amountCents, method: overrides.method ?? "electronic_transfer" },
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
