import { contentHash } from "./canonical.js";
import type { Db, Queryable } from "./db.js";
import { appendEvent } from "./events.js";
import { newId } from "./ids.js";
import { type Principal, principalLabel, requirePermission, NotAllowed } from "./principals.js";

export type DecisionStatus = "proposed" | "accepted" | "declined" | "superseded";

export interface Decision<C = Record<string, unknown>> {
  id: string;
  caseId: string | null;
  kind: string;
  content: C;
  contentHash: string;
  status: DecisionStatus;
  proposedBy: string;
  proposedAt: Date;
  decidedBy: string | null;
  decidedAt: Date | null;
  note: string | null;
  supersedes: string | null;
}

interface DecisionRow {
  id: string;
  case_id: string | null;
  kind: string;
  content: Record<string, unknown>;
  content_hash: string;
  status: DecisionStatus;
  proposed_by: string;
  proposed_at: Date;
  decided_by: string | null;
  decided_at: Date | null;
  note: string | null;
  supersedes: string | null;
}

function toDecision(r: DecisionRow): Decision {
  return {
    id: r.id,
    caseId: r.case_id,
    kind: r.kind,
    content: r.content,
    contentHash: r.content_hash,
    status: r.status,
    proposedBy: r.proposed_by,
    proposedAt: new Date(r.proposed_at),
    decidedBy: r.decided_by,
    decidedAt: r.decided_at ? new Date(r.decided_at) : null,
    note: r.note,
    supersedes: r.supersedes,
  };
}

/** A decision with no case is a standing instruction for the whole company. */
export interface Proposal {
  caseId: string | null;
  kind: string;
  content: Record<string, unknown>;
  /** A decision this one replaces: a pending one is replaced now, an accepted one when this is accepted. */
  supersedes?: string;
}

export class DecisionRefused extends Error {}

export async function getDecision(q: Queryable, id: string): Promise<Decision | null> {
  const [r] = await q.query<DecisionRow>(`select * from decisions where id = $1`, [id]);
  return r ? toDecision(r) : null;
}

/** Records a proposal. The agent and operators can propose; the content is fixed from here on. */
export async function propose(db: Db, by: Principal, p: Proposal, at: Date): Promise<Decision> {
  return db.transaction(async (tx) => {
    if (p.supersedes) {
      const old = await getDecision(tx, p.supersedes);
      if (!old) throw new DecisionRefused(`no decision ${p.supersedes}`);
      if (old.kind !== p.kind || old.caseId !== p.caseId) throw new DecisionRefused("a decision can only be superseded by one of the same kind for the same case");
      if (old.status === "proposed") await tx.query(`update decisions set status = 'superseded' where id = $1`, [old.id]);
      else if (old.status !== "accepted") throw new DecisionRefused(`decision ${old.id} is ${old.status} and cannot be superseded`);
    }
    const [r] = await tx.query<DecisionRow>(
      `insert into decisions (id, case_id, kind, content, content_hash, status, proposed_by, proposed_at, supersedes)
       values ($1, $2, $3, $4, $5, 'proposed', $6, $7, $8) returning *`,
      [newId("dec"), p.caseId, p.kind, p.content, contentHash(p.content), principalLabel(by), at, p.supersedes ?? null],
    );
    return toDecision(r!);
  });
}

export type Verdict =
  | { verdict: "accept"; note?: string }
  | { verdict: "decline"; note: string }
  /** The operator's own version replaces the proposal and is accepted as theirs. */
  | { verdict: "change"; content: Record<string, unknown>; note?: string };

/**
 * An operator's decision on a proposal. It binds to the content the operator reviewed: if the
 * hash they saw is not the hash on record, or the proposal has since been replaced, it is refused.
 */
export async function decide(db: Db, by: Principal, decisionId: string, reviewedHash: string, v: Verdict, at: Date): Promise<Decision> {
  return db.transaction(async (tx) => {
    const d = await getDecision(tx, decisionId);
    if (!d) throw new DecisionRefused(`no decision ${decisionId}`);
    const userId = await requirePermission(tx, by, d.caseId === null ? "configure" : "decide");
    if (d.status !== "proposed") throw new DecisionRefused(`decision ${d.id} is already ${d.status}`);
    if (reviewedHash !== d.contentHash || contentHash(d.content) !== d.contentHash) {
      throw new DecisionRefused(`decision ${d.id} is not the content that was reviewed`);
    }

    if (v.verdict === "decline") {
      const [r] = await tx.query<DecisionRow>(
        `update decisions set status = 'declined', decided_by = $2, decided_at = $3, note = $4 where id = $1 returning *`,
        [d.id, userId, at, v.note],
      );
      await tellCase(tx, d, r!.id, "decline", at);
      return toDecision(r!);
    }

    let accepted: Decision;
    if (v.verdict === "accept") {
      const [r] = await tx.query<DecisionRow>(
        `update decisions set status = 'accepted', decided_by = $2, decided_at = $3, note = $4 where id = $1 returning *`,
        [d.id, userId, at, v.note ?? null],
      );
      accepted = toDecision(r!);
    } else {
      await tx.query(`update decisions set status = 'superseded' where id = $1`, [d.id]);
      const [r] = await tx.query<DecisionRow>(
        `insert into decisions (id, case_id, kind, content, content_hash, status, proposed_by, proposed_at, decided_by, decided_at, note, supersedes)
         values ($1, $2, $3, $4, $5, 'accepted', $6, $7, $8, $7, $9, $10) returning *`,
        [newId("dec"), d.caseId, d.kind, v.content, contentHash(v.content), principalLabel(by), at, userId, v.note ?? null, d.id],
      );
      accepted = toDecision(r!);
    }

    // Accepting a correction retires the decision it corrects.
    if (d.supersedes) {
      await tx.query(`update decisions set status = 'superseded' where id = $1 and status = 'accepted'`, [d.supersedes]);
    }
    await tellCase(tx, d, accepted.id, v.verdict, at);
    return accepted;
  });
}

/** An operator's decision wakes the case it belongs to. */
async function tellCase(q: Queryable, proposed: Decision, resultId: string, verdict: Verdict["verdict"], at: Date): Promise<void> {
  if (proposed.caseId === null) return;
  await appendEvent(q, {
    caseId: proposed.caseId,
    kind: "decision.decided",
    source: "operator",
    payload: { proposedId: proposed.id, decisionId: resultId, kind: proposed.kind, verdict },
    occurredAt: at,
  });
}

/** The accepted, current decision an action relies on, or a reason it cannot be relied on. */
export async function currentAccepted(q: Queryable, decisionId: string, expect: { kinds: string[]; caseId: string | null }): Promise<Decision> {
  const d = await getDecision(q, decisionId);
  if (!d) throw new NotAllowed(`no decision ${decisionId}`);
  if (!expect.kinds.includes(d.kind)) throw new NotAllowed(`decision ${d.id} is a ${d.kind}, not ${expect.kinds.join(" or ")}`);
  if (d.caseId !== expect.caseId) throw new NotAllowed(`decision ${d.id} belongs to another case`);
  if (d.status !== "accepted") throw new NotAllowed(`decision ${d.id} is ${d.status}, not accepted`);
  if (contentHash(d.content) !== d.contentHash) throw new NotAllowed(`decision ${d.id} content does not match its hash`);
  return d;
}

/** The company's current standing instruction of a kind, if an operator has set one. */
export async function standingInstruction(q: Queryable, kind: string): Promise<Decision | null> {
  const [r] = await q.query<DecisionRow>(
    `select * from decisions where case_id is null and kind = $1 and status = 'accepted' order by decided_at desc, id desc limit 1`,
    [kind],
  );
  return r ? toDecision(r) : null;
}

export async function caseDecisions(q: Queryable, caseId: string): Promise<Decision[]> {
  return (await q.query<DecisionRow>(`select * from decisions where case_id = $1 order by proposed_at, id`, [caseId])).map(toDecision);
}
