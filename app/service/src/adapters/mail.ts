/** Outgoing email. Production uses a mail provider; a simulated world uses the imitation in sim/mail.ts. */
export interface OutgoingMessage {
  caseId: string | null;
  toPartyId: string;
  toAddress: string;
  subject: string;
  body: string;
  attachments: Array<{ name: string; ref: string }>;
}

export interface SentMessage {
  messageId: string;
  sentAt: string;
}

export interface Mail {
  /** Sends once per key: the provider refuses a second message under the same key and returns the first. */
  send(message: OutgoingMessage, key: string): Promise<SentMessage>;
  /** The message sent under this key, or null if none was. */
  find(key: string): Promise<SentMessage | null>;
}
