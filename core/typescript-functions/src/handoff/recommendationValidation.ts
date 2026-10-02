import { UserFacingError } from "@osdk/functions";

const FEEDBACK = {
  format: "Return a complete response matching the requested schema and field limits, without extra fields.",
  proposal: "Provide complete proposal fields and unique quote-line selections with a scope and reason. Scope is derived from selections; do not return proposal.scope.",
  selection: "Use available quoted lines once each, in the workspace currency. Include each quote source, keep the estimate equal to quoted costs, and cover it with the budget.",
  pricing: "Read each selected quote source and call quoteCosts for the same quote IDs and line IDs before proposing them. Do not change quoted prices.",
  sources: "Use sources you have read, an available provider, and retain the stated requirements.",
  requirements: "fixedRequirements may contain only the supplied handoff requirements and those on the current proposal. Put your own conditions or advice in the rationale.",
  requests: "Send requests only to parties in this handoff. For a Quote request, first read that provider's service information with readDocuments in this turn, then use one of its listed services.",
  existing_work: "Continue already ordered work; do not propose ordering the same quoted line again.",
  copy: "Use concise operator language without internal identifiers, field names, amounts in cents, tool references or slash and \"+\" shorthand. Plan titles are short plain phrases without \"+\" or parentheses.",
  readiness: "Report propertyReady only when the latest condition record shows every condition satisfied and accessible, every job is complete, the tenancy is ending, and you propose no new work.",
  turn_limit: "Complete the recommendation within the available reasoning turns and tool calls.",
} as const;

type ValidationCode = keyof typeof FEEDBACK;
/**
 * `detail` names which part of the draft failed, in server-owned words: the field, the party, the rule and
 * the valid choices. It never quotes the model's draft or private source text.
 */
export class RecommendationValidationError extends Error {
  constructor(readonly code: ValidationCode, readonly detail?: string) { super(FEEDBACK[code]); }
}
/** Only this typed exhaustion is recoverable by the coordinator; never transport or authority errors. */
export class RecommendationValidationExhausted extends Error {
  constructor(readonly code: ValidationCode) { super("The recommendation service could not produce a checked recommendation."); }
}
export function requireRecommendation(condition: unknown, code: ValidationCode, detail?: string): asserts condition {
  if (!condition) throw new RecommendationValidationError(code, detail);
}
/** Call only around pure model-input validation, with source records already validated separately. */
export function recommendationInput<T>(code: ValidationCode, validate: () => T): T {
  try { return validate(); }
  catch (error: unknown) {
    if (!(error instanceof UserFacingError)) throw error;
    // Fixed server-owned feedback never echoes model drafts or private/unknown source values.
    throw new RecommendationValidationError(code);
  }
}
