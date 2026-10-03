import { z } from "zod";
import type { Mail } from "../adapters/mail.js";
import { type ActionSpec, byDecision, byStanding, eitherOf } from "../gateway.js";
import { NotAllowed } from "../principals.js";
import { caseParties } from "./records.js";

export const SendMessageRequest = z.object({
  /** The agent's name for this message within the case, e.g. "statement" or "ack-dispute-1". Sending again under it does nothing. */
  key: z.string().min(1).max(120),
  toPartyId: z.string(),
  subject: z.string().min(1),
  body: z.string().min(1),
  attachments: z.array(z.object({ name: z.string(), ref: z.string() })).default([]),
  /** For a message an operator approved as part of a decision. */
  decisionId: z.string().optional(),
  /** For a routine message the standing instruction allows, e.g. "acknowledge" or "schedule". */
  purpose: z.string().optional(),
});
export type SendMessageRequest = z.infer<typeof SendMessageRequest>;

/** Decisions whose content can carry an approved message under `message`. */
const MESSAGE_DECISIONS = ["account.statement", "message.approval"];

export function sendMessage(mail: Mail): ActionSpec<SendMessageRequest> {
  return {
    kind: "message.send",
    request: SendMessageRequest,
    key: (req, caseId) => `${caseId ?? "company"}:${req.key}`,
    authorize: eitherOf(
      byDecision(MESSAGE_DECISIONS, (req) => req.decisionId, (content, req) => {
        const m = content.message as Record<string, unknown> | undefined;
        if (!m) return "the decision approves no message";
        if (m.toPartyId !== req.toPartyId) return "different recipient";
        if (m.subject !== req.subject) return "different subject";
        if (m.body !== req.body) return "different wording";
        return null;
      }),
      byStanding("standing.routine-messages", (content, req) => {
        const purposes = (content.purposes as string[] | undefined) ?? [];
        if (!req.purpose) return "no purpose given";
        if (!purposes.includes(req.purpose)) return `purpose ${req.purpose} is not routine`;
        if (req.attachments.length > 0) return "routine messages carry no attachments";
        return null;
      }),
    ),
    checks: [
      async (ctx, req) => {
        if (!ctx.caseId) return null;
        const party = (await caseParties(ctx.q, ctx.caseId)).find((p) => p.partyId === req.toPartyId);
        if (!party) return `${req.toPartyId} is not a party to this tenancy`;
        if (!party.email) return `no email address on record for ${req.toPartyId}`;
        return null;
      },
    ],
    async perform(ctx, req, key) {
      const party = ctx.caseId ? (await caseParties(ctx.q, ctx.caseId)).find((p) => p.partyId === req.toPartyId) : undefined;
      if (!party?.email) throw new NotAllowed("recipient has no address on record");
      const sent = await mail.send(
        { caseId: ctx.caseId, toPartyId: req.toPartyId, toAddress: party.email, subject: req.subject, body: req.body, attachments: req.attachments },
        key,
      );
      return { status: "succeeded", result: { ...sent } };
    },
    async lookup(_ctx, _req, key) {
      const sent = await mail.find(key);
      return sent ? { status: "succeeded", result: { ...sent } } : null;
    },
  };
}
