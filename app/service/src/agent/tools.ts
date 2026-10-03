import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { BalanceCorrectionContent, BalancePursuitContent } from "../account/pursuit.js";
import { StatementContent } from "../account/statement.js";
import { addCondition, addFinding, addObservation, addWorkItem } from "../records.js";
import type { TurnContext } from "../runner.js";
import { WorkPlanContent } from "../work/plan.js";
import { businessNow } from "../clock.js";

/** Decisions the coordinator may propose, with the shape each one's content must have. */
export const PROPOSALS: Record<string, { what: string; content: z.ZodType<unknown> }> = {
  "premoveout.list": {
    what: "The itemized list of proposed repairs and cleanings from the pre-move-out inspection, handed to the tenant at the inspection.",
    content: z.object({
      inspectionId: z.string().optional(),
      items: z.array(z.object({ conditionId: z.string().optional(), area: z.string(), item: z.string(), proposed: z.string() })),
      message: z.object({ toPartyId: z.string(), subject: z.string(), body: z.string() }).optional(),
    }),
  },
  "work.plan": { what: "The work plan and budget for the turn.", content: WorkPlanContent },
  "account.statement": { what: "The itemized deposit statement, with the refund or balance due and the message that sends it.", content: StatementContent },
  "balance.pursuit": { what: "What to do about a balance the deposit did not cover.", content: BalancePursuitContent },
  "balance.correction": { what: "A corrected amount for a component placed with the collector.", content: BalanceCorrectionContent },
  "message.approval": {
    what: "A message whose exact wording needs the operator's approval.",
    content: z.object({ message: z.object({ toPartyId: z.string(), subject: z.string(), body: z.string() }), why: z.string() }),
  },
};

const json = (v: unknown) => JSON.stringify(v);

/** The coordinator's tools for one wake. Act tools are generated from the gateway's catalog. */
export function coordinatorTools(ctx: TurnContext) {
  const actTools = ctx.catalog().map((a) =>
    tool(
      async (request) => {
        const r = await ctx.act(a.kind, request);
        return json({ status: r.status, reason: r.reason, result: r.result, key: r.key });
      },
      { name: a.kind.replaceAll(".", "_"), description: a.description, schema: a.request as z.ZodObject },
    ),
  );

  const proposeTool = tool(
    async ({ kind, content, supersedes }) => {
      const shape = PROPOSALS[kind];
      if (!shape) return json({ error: `unknown decision kind ${kind}` });
      const parsed = shape.content.safeParse(content);
      if (!parsed.success) return json({ error: "content does not have the required shape", issues: parsed.error.issues });
      const d = await ctx.propose({ kind, content: parsed.data as Record<string, unknown>, supersedes });
      return json({ decisionId: d.id, status: d.status, contentHash: d.contentHash });
    },
    {
      name: "propose_decision",
      description: `Propose a decision for the operator. Kinds: ${Object.entries(PROPOSALS).map(([k, v]) => `${k} (${v.what})`).join("; ")}. To revise a proposal or correct an accepted decision, give supersedes.`,
      schema: z.object({ kind: z.string(), content: z.record(z.string(), z.unknown()), supersedes: z.string().optional() }),
    },
  );

  const recordCondition = tool(
    async ({ area, item, summary, inspectionId }) =>
      json({ conditionId: await addCondition(ctx.db, { caseId: ctx.caseId, area, item, summary, identifiedAt: await businessNow(ctx.db), identifiedIn: inspectionId }) }),
    {
      name: "record_condition",
      description: "Record something in the unit that may need work or lead to a charge, e.g. the bedroom 2 closet door.",
      schema: z.object({ area: z.string(), item: z.string(), summary: z.string(), inspectionId: z.string().optional() }),
    },
  );

  const recordObservation = tool(
    async ({ conditionId, text, inspectionId, documentIds }) =>
      json({ observationId: await addObservation(ctx.db, { conditionId, text, inspectionId, documentIds, observedBy: `agent:${ctx.runId}`, observedAt: await businessNow(ctx.db) }) }),
    {
      name: "record_observation",
      description: "Record what is visible about a condition, where and how extensive, in neutral terms. Not a conclusion about responsibility.",
      schema: z.object({ conditionId: z.string(), text: z.string(), inspectionId: z.string().optional(), documentIds: z.array(z.string()).optional() }),
    },
  );

  const recordFinding = tool(
    async ({ conditionId, responsibility, reasoning, basis }) => {
      const f = await addFinding(ctx.db, { conditionId, responsibility, reasoning, basis, foundBy: `agent:${ctx.runId}`, foundAt: await businessNow(ctx.db) });
      return json({ findingId: f.id, supersedes: f.supersedes });
    },
    {
      name: "record_finding",
      description: "Record who is responsible for a condition: tenant_damage, ordinary_wear, present_at_move_in, or undetermined. A new finding supersedes the last.",
      schema: z.object({
        conditionId: z.string(),
        responsibility: z.enum(["tenant_damage", "ordinary_wear", "present_at_move_in", "undetermined"]),
        reasoning: z.string(),
        basis: z.record(z.string(), z.unknown()).optional(),
      }),
    },
  );

  const planWork = tool(
    async ({ performer, vendorPartyId, description, conditionIds, estimateCents }) =>
      json({ workItemId: await addWorkItem(ctx.db, { caseId: ctx.caseId, performer, vendorPartyId, description, conditionIds, estimateCents }) }),
    {
      name: "add_work_item",
      description: "Add planned work that fixes one or more conditions, to be included in a work plan proposal.",
      schema: z.object({
        performer: z.enum(["in_house", "vendor"]),
        vendorPartyId: z.string().optional(),
        description: z.string(),
        conditionIds: z.array(z.string()),
        estimateCents: z.number().int().nonnegative().optional(),
      }),
    },
  );

  const schedule = tool(
    async ({ dueAt, reason, key }) => {
      await ctx.schedule({ dueAt: new Date(dueAt), reason, key });
      return json({ scheduled: dueAt, key });
    },
    {
      name: "schedule_wakeup",
      description: "Wake this case at a business date and time (ISO 8601 with offset), e.g. for a deadline or follow-up. The same key moves an existing wake-up.",
      schema: z.object({ dueAt: z.iso.datetime({ offset: true }), reason: z.string(), key: z.string() }),
    },
  );

  const cancel = tool(
    async ({ key }) => {
      await ctx.cancel(key);
      return json({ cancelled: key });
    },
    { name: "cancel_wakeup", description: "Cancel a scheduled wake-up by its key.", schema: z.object({ key: z.string() }) },
  );

  const note = tool(
    async ({ kind, text }) => {
      await ctx.note(kind, { text });
      return json({ noted: kind });
    },
    {
      name: "note",
      description: "Record something you concluded or are waiting for, so your next wake knows it.",
      schema: z.object({ kind: z.string(), text: z.string() }),
    },
  );

  return [...actTools, proposeTool, recordCondition, recordObservation, recordFinding, planWork, schedule, cancel, note];
}
