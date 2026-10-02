/** Correspondence is saved as the email a person would read: greeting, plain body, sign-off. */
export interface Correspondent { name?: string; kind?: string }

export function greeting(to?: Correspondent): string {
  const first = to?.kind === "Person" ? to.name?.trim().split(/\s+/)[0] : undefined;
  return first ? `Hi ${first},` : "Hello,";
}
/** A letter body. Model-written text is trimmed of any greeting or sign-off it already has. */
export function letter(to: Correspondent | undefined, body: string, from: string, closing = "Thanks,"): string {
  const text = body.trim()
    .replace(/^(hi|hello|dear)\b[^\n]*\n+/i, "")
    .replace(/\n+(thanks|thank you|best|regards|kind regards)[^\n]*(\n[^\n]*)?$/i, "")
    .trim();
  return `${greeting(to)}\n\n${text}\n\n${closing}\n${from}`;
}
export function bullets(items: readonly string[]): string {
  return items.map((item) => `- ${item}`).join("\n");
}
/** Attachment document references kept with an incoming message's details. */
export function attachmentsOf(detailsJson: string | undefined): string[] {
  if (!detailsJson) return [];
  try {
    const value = (JSON.parse(detailsJson) as Record<string, unknown>).attachments;
    return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
  } catch {
    return [];
  }
}
