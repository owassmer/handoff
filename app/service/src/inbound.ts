import type { Queryable } from "./db.js";
import { type CaseEvent, appendEvent } from "./events.js";

/**
 * A message from outside: the tenant, a vendor, a collector. It lands in the case inbox as
 * untrusted information. Nothing it says can authorize an action.
 */
export interface InboundMessage {
  caseId: string;
  from: "tenant" | "counterparty";
  fromPartyId: string;
  subject: string;
  body: string;
  attachments?: Array<{ name: string; ref: string }>;
  receivedAt: Date;
}

export function receiveMessage(q: Queryable, m: InboundMessage): Promise<CaseEvent> {
  return appendEvent(q, {
    caseId: m.caseId,
    kind: "message.received",
    source: m.from,
    payload: { fromPartyId: m.fromPartyId, subject: m.subject, body: m.body, attachments: m.attachments ?? [] },
    occurredAt: m.receivedAt,
  });
}
