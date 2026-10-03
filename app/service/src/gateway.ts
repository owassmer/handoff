import type { z } from "zod";
import { canonicalJson } from "./canonical.js";
import { businessNow } from "./clock.js";
import type { Db, Queryable } from "./db.js";
import { type Decision, currentAccepted, standingInstruction } from "./decisions.js";
import { newId } from "./ids.js";
import { type Principal, NotAllowed, principalLabel } from "./principals.js";

/** What an action relies on. Authority only ever comes from an operator's decision or a stated routine. */
export type Authority =
  | { basis: "decision"; decision: Decision }
  | { basis: "standing"; decision: Decision }
  | { basis: "routine"; why: string };

export interface ActionContext {
  q: Queryable;
  caseId: string | null;
  principal: Principal;
  /** Business time when the action was requested. */
  now: Date;
}

/** How an outside system reports an effect. Throwing means it is unknown whether the effect happened. */
export type Outcome =
  | { status: "succeeded"; result: Record<string, unknown> }
  | { status: "failed"; reason: string };

export interface ActionSpec<Req> {
  kind: string;
  request: z.ZodType<Req>;
  /** Derived from the request, so the same intended effect always carries the same key. */
  key(req: Req, caseId: string | null): string;
  /** Returns the authority relied on, or throws NotAllowed with the reason. */
  authorize(ctx: ActionContext, req: Req): Promise<Authority>;
  /** Further checks (law, money, timing). Each returns a reason to refuse, or null. */
  checks?: Array<(ctx: ActionContext, req: Req) => Promise<string | null>>;
  /** Performs the effect, passing the key to the outside system so it can refuse a duplicate. */
  perform(ctx: ActionContext, req: Req, key: string): Promise<Outcome>;
  /** Asks the outside system whether the effect under this key happened; null if it certainly did not. */
  lookup(ctx: ActionContext, req: Req, key: string): Promise<Outcome | null>;
}

export type ActionStatus = "refused" | "pending" | "succeeded" | "failed" | "uncertain";

export interface ActionRecord {
  id: number;
  caseId: string | null;
  kind: string;
  key: string;
  requestedBy: string;
  status: ActionStatus;
  reason: string | null;
  result: Record<string, unknown> | null;
  authorityDecisionId: string | null;
  authorityBasis: string | null;
  attempts: number;
}

interface ActionRow {
  id: string | number;
  case_id: string | null;
  kind: string;
  idempotency_key: string;
  requested_by: string;
  authority_decision_id: string | null;
  authority_basis: string | null;
  request: unknown;
  status: ActionStatus;
  reason: string | null;
  result: Record<string, unknown> | null;
  attempts: number;
}

function toRecord(r: ActionRow): ActionRecord {
  return {
    id: Number(r.id),
    caseId: r.case_id,
    kind: r.kind,
    key: r.idempotency_key,
    requestedBy: r.requested_by,
    status: r.status,
    reason: r.reason,
    result: r.result,
    authorityDecisionId: r.authority_decision_id,
    authorityBasis: r.authority_basis,
    attempts: r.attempts,
  };
}

// ---- Authority helpers -------------------------------------------------------------------------

/**
 * The action carries out an accepted decision on this case. `matches` compares the request with
 * the decision's content and returns a reason if they differ.
 */
export function byDecision<Req>(
  decisionKinds: string[],
  decisionIdOf: (req: Req) => string | undefined,
  matches: (content: Record<string, unknown>, req: Req) => string | null,
): ActionSpec<Req>["authorize"] {
  return async (ctx, req) => {
    const id = decisionIdOf(req);
    if (!id) throw new NotAllowed("no decision given");
    const decision = await currentAccepted(ctx.q, id, { kinds: decisionKinds, caseId: ctx.caseId });
    const mismatch = matches(decision.content, req);
    if (mismatch) throw new NotAllowed(`request differs from accepted decision ${decision.id}: ${mismatch}`);
    return { basis: "decision", decision };
  };
}

/** The action falls within a company-wide standing instruction an operator has accepted. */
export function byStanding<Req>(
  instructionKind: string,
  allows: (content: Record<string, unknown>, req: Req) => string | null,
): ActionSpec<Req>["authorize"] {
  return async (ctx, req) => {
    const decision = await standingInstruction(ctx.q, instructionKind);
    if (!decision) throw new NotAllowed(`no standing instruction ${instructionKind}`);
    const outside = allows(decision.content, req);
    if (outside) throw new NotAllowed(`outside standing instruction ${decision.id}: ${outside}`);
    return { basis: "standing", decision };
  };
}

/** Tries each way of being authorized in turn; refuses with every reason if none applies. */
export function eitherOf<Req>(...ways: Array<ActionSpec<Req>["authorize"]>): ActionSpec<Req>["authorize"] {
  return async (ctx, req) => {
    const reasons: string[] = [];
    for (const way of ways) {
      try {
        return await way(ctx, req);
      } catch (e) {
        if (!(e instanceof NotAllowed)) throw e;
        reasons.push(e.message);
      }
    }
    throw new NotAllowed(reasons.join("; "));
  };
}

// ---- Gateway -----------------------------------------------------------------------------------

export class UnknownAction extends Error {}

export class Gateway {
  private readonly specs = new Map<string, ActionSpec<any>>();

  constructor(private readonly db: Db, specs: Array<ActionSpec<any>>) {
    for (const s of specs) {
      if (this.specs.has(s.kind)) throw new Error(`action ${s.kind} registered twice`);
      this.specs.set(s.kind, s);
    }
  }

  kinds(): string[] {
    return [...this.specs.keys()];
  }

  /**
   * Requests an action. Returns its record: refused with a reason, succeeded, failed, or uncertain
   * when the outside system did not say whether it happened. Asking again for the same effect
   * returns the first outcome, or settles an uncertain one, and never acts twice.
   */
  async execute(principal: Principal, caseId: string | null, kind: string, rawRequest: unknown): Promise<ActionRecord> {
    const spec = this.specs.get(kind);
    if (!spec) throw new UnknownAction(`no action ${kind}`);
    const ctx: ActionContext = { q: this.db, caseId, principal, now: await businessNow(this.db) };

    const parsed = spec.request.safeParse(rawRequest);
    if (!parsed.success) {
      return this.refuse(ctx, kind, `${kind}:invalid:${newId("x")}`, { given: safeJson(rawRequest) }, `invalid request: ${parsed.error.message}`);
    }
    const req = parsed.data;
    const key = `${kind}:${spec.key(req, caseId)}`;

    const existing = await this.findLive(key);
    if (existing) return this.resume(spec, ctx, existing, req);

    let authority: Authority;
    try {
      authority = await spec.authorize(ctx, req);
      for (const check of spec.checks ?? []) {
        const reason = await check(ctx, req);
        if (reason) throw new NotAllowed(reason);
      }
    } catch (e) {
      if (!(e instanceof NotAllowed)) throw e;
      return this.refuse(ctx, kind, key, req, e.message);
    }

    const decisionId = authority.basis === "routine" ? null : authority.decision.id;
    const basis = authority.basis === "routine" ? `routine: ${authority.why}` : authority.basis;
    const [row] = await this.db.query<ActionRow>(
      `insert into actions (case_id, kind, idempotency_key, requested_by, authority_decision_id, authority_basis, request, status, attempts, requested_at)
       values ($1, $2, $3, $4, $5, $6, $7, 'pending', 1, $8)
       on conflict (idempotency_key) where status <> 'refused' do nothing returning *`,
      [caseId, kind, key, principalLabel(principal), decisionId, basis, req, ctx.now],
    );
    if (!row) {
      // Someone else recorded the same action between our look and our insert.
      const raced = await this.findLive(key);
      if (!raced) throw new Error(`action ${key} vanished`);
      return this.resume(spec, ctx, raced, req);
    }
    return this.performAndRecord(spec, ctx, toRecord(row), req, key);
  }

  /** Settles an uncertain or interrupted action by asking the outside system what happened. */
  async reconcile(actionId: number, principal: Principal = { kind: "system", name: "reconciler" }): Promise<ActionRecord> {
    const [row] = await this.db.query<ActionRow>(`select * from actions where id = $1`, [actionId]);
    if (!row) throw new Error(`no action ${actionId}`);
    const spec = this.specs.get(row.kind);
    if (!spec) throw new UnknownAction(`no action ${row.kind}`);
    const ctx: ActionContext = { q: this.db, caseId: row.case_id, principal, now: await businessNow(this.db) };
    return this.resume(spec, ctx, row, spec.request.parse(row.request));
  }

  async unsettled(): Promise<ActionRecord[]> {
    return (await this.db.query<ActionRow>(`select * from actions where status in ('pending', 'uncertain') order by id`)).map(toRecord);
  }

  private async findLive(key: string): Promise<ActionRow | null> {
    const [row] = await this.db.query<ActionRow>(`select * from actions where idempotency_key = $1 and status <> 'refused'`, [key]);
    return row ?? null;
  }

  private async refuse(ctx: ActionContext, kind: string, key: string, request: unknown, reason: string): Promise<ActionRecord> {
    const [row] = await this.db.query<ActionRow>(
      `insert into actions (case_id, kind, idempotency_key, requested_by, request, status, reason, requested_at, completed_at)
       values ($1, $2, $3, $4, $5, 'refused', $6, $7, $7) returning *`,
      [ctx.caseId, kind, key, principalLabel(ctx.principal), request, reason, ctx.now],
    );
    return toRecord(row!);
  }

  private async resume<Req>(spec: ActionSpec<Req>, ctx: ActionContext, row: ActionRow, req: Req): Promise<ActionRecord> {
    if (canonicalJson(row.request) !== canonicalJson(req)) {
      return this.refuse(ctx, spec.kind, `${row.idempotency_key}:conflict:${newId("x")}`, req,
        `action ${row.idempotency_key} was already requested with different details`);
    }
    if (row.status !== "pending" && row.status !== "uncertain") return toRecord(row);

    // Claim the attempt so two workers never chase the same unsettled action at once.
    const [claimed] = await this.db.query<ActionRow>(
      `update actions set attempts = attempts + 1 where id = $1 and attempts = $2 and status in ('pending', 'uncertain') returning *`,
      [row.id, row.attempts],
    );
    if (!claimed) return toRecord((await this.db.query<ActionRow>(`select * from actions where id = $1`, [row.id]))[0]!);

    let found: Outcome | null;
    try {
      found = await spec.lookup(ctx, req, row.idempotency_key);
    } catch (e) {
      return this.record(claimed, "uncertain", { reason: `could not confirm with the outside system: ${message(e)}` }, ctx.now);
    }
    if (found) return this.settle(claimed, found, ctx.now);

    // It certainly did not happen. Act only if it is still authorized now.
    try {
      await spec.authorize(ctx, req);
      for (const check of spec.checks ?? []) {
        const reason = await check(ctx, req);
        if (reason) throw new NotAllowed(reason);
      }
    } catch (e) {
      if (!(e instanceof NotAllowed)) throw e;
      return this.record(claimed, "failed", { reason: `did not happen, and is no longer allowed: ${e.message}` }, ctx.now);
    }
    return this.performAndRecord(spec, ctx, toRecord(claimed), req, row.idempotency_key);
  }

  private async performAndRecord<Req>(spec: ActionSpec<Req>, ctx: ActionContext, action: ActionRecord, req: Req, key: string): Promise<ActionRecord> {
    let outcome: Outcome;
    try {
      outcome = await spec.perform(ctx, req, key);
    } catch (e) {
      return this.record({ id: action.id }, "uncertain", { reason: `no confirmation from the outside system: ${message(e)}` }, ctx.now);
    }
    return this.settle({ id: action.id }, outcome, ctx.now);
  }

  private settle(row: { id: string | number }, outcome: Outcome, at: Date): Promise<ActionRecord> {
    return outcome.status === "succeeded"
      ? this.record(row, "succeeded", { result: outcome.result }, at)
      : this.record(row, "failed", { reason: outcome.reason }, at);
  }

  private async record(row: { id: string | number }, status: ActionStatus, detail: { reason?: string; result?: Record<string, unknown> }, at: Date): Promise<ActionRecord> {
    const [updated] = await this.db.query<ActionRow>(
      `update actions set status = $2, reason = $3, result = $4,
         completed_at = case when $2 in ('succeeded', 'failed') then $5::timestamptz else completed_at end
       where id = $1 returning *`,
      [row.id, status, detail.reason ?? null, detail.result ?? null, at],
    );
    return toRecord(updated!);
  }
}

function message(e: unknown): string {
  return e instanceof Error ? e.message : String(e);
}

function safeJson(v: unknown): unknown {
  try {
    return v === undefined ? null : JSON.parse(JSON.stringify(v));
  } catch {
    return "unreadable";
  }
}
