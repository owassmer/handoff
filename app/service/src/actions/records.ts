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
