import type { Queryable } from "../db.js";

/** The parties on the tenancy behind a case, as recorded. Addresses always come from here, never from a message. */
export async function caseParties(q: Queryable, caseId: string): Promise<Array<{ partyId: string; relationship: string; name: string; email: string | null }>> {
  return (await q.query<{ party_id: string; relationship: string; name: string; email: string | null }>(
    `select tp.party_id, tp.relationship, p.name, p.email
     from cases c join tenancy_parties tp on tp.tenancy_id = c.tenancy_id join parties p on p.id = tp.party_id
     where c.id = $1 order by tp.party_id`,
    [caseId],
  )).map((r) => ({ partyId: r.party_id, relationship: r.relationship, name: r.name, email: r.email }));
}

/** The tenancy and unit behind a case, as Handoff records them. Outside systems are addressed by these. */
export async function caseTenancy(q: Queryable, caseId: string): Promise<{ tenancyId: string; unitId: string }> {
  const [r] = await q.query<{ tenancy_id: string; unit_id: string }>(
    `select c.tenancy_id, t.unit_id from cases c join tenancies t on t.id = c.tenancy_id where c.id = $1`,
    [caseId],
  );
  if (!r) throw new Error(`no case ${caseId}`);
  return { tenancyId: r.tenancy_id, unitId: r.unit_id };
}
