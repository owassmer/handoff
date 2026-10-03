import type { Queryable } from "../db.js";
import { decide, propose } from "../decisions.js";
import { receiveMessage } from "../inbound.js";
import type { CaseTurn } from "../runner.js";
import { World } from "../world.js";

/** The demonstration tenancy from design/DESIGN.md §1, with placeholder names until neutral ones are chosen. */
export async function seedDemoCase(q: Queryable, caseId = "case-1"): Promise<void> {
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

export const NOTICE_TIME = new Date("2026-10-12T16:00:00Z");

/**
 * The first moment of the demonstration: October 12, 2026, the tenant gives notice. The operator's
 * standing instructions allow routine messages and routine inspections.
 */
export async function stageNoticeWorld(turn: CaseTurn): Promise<World> {
  const w = await World.create(NOTICE_TIME, turn);
  await seedDemoCase(w.db);
  const admin = { kind: "operator", userId: "op-admin" } as const;
  for (const [kind, content] of [
    ["standing.routine-messages", { purposes: ["acknowledge", "schedule", "notice", "request-information", "follow-up"] }],
    ["standing.routine-work", { categories: ["inspection"] }],
  ] as const) {
    const d = await propose(w.db, admin, { caseId: null, kind, content: { ...content } }, NOTICE_TIME);
    await decide(w.db, admin, d.id, d.contentHash, { verdict: "accept" }, NOTICE_TIME);
  }
  await receiveMessage(w.db, {
    caseId: "case-1", from: "tenant", fromPartyId: "tenant-1", subject: "Notice to vacate",
    body: "Hi, this is my notice that I will be moving out when my lease ends on November 10. Please let me know what I need to do.",
    receivedAt: NOTICE_TIME,
  });
  return w;
}
