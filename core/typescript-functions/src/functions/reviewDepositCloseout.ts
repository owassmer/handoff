import { UserFacingError } from "@osdk/functions";
import { ContractError, canonical_json, from_json, from_wire } from "../deposit_closeout/domain/codec.js";
import { review_request } from "../deposit_closeout/domain/review.js";
import safetyProfile from "../deposit_closeout/resources/phase_b_safety_profile.json" with { type: "json" };
import ruleRelease from "../deposit_closeout/resources/rules/nc_synthetic_review_v1.json" with { type: "json" };

export const config = { apiName: "reviewDepositCloseout" };

/**
 * Review a constructed tenancy with the native TS core, without Ontology or external effects.
 * @param requestJson Strict ReviewRequest 1.0.0 JSON. Cents remain exact integer JSON numbers.
 * @returns Canonical JSON containing the existing ReviewEnvelope 1.1.0 and its six outputs.
 * This compatibility transport is a JSON string, not a native Long-bearing Functions struct.
 */
export default function reviewDepositCloseout(requestJson: string): string {
  if (typeof requestJson !== "string" || requestJson.length > 2_000_000) {
    throw new UserFacingError("Supply a JSON request of at most 1,000,000 characters; inputs are never truncated.");
  }
  let codePoints = 0;
  for (const _character of requestJson) {
    codePoints += 1;
    if (codePoints > 1_000_000) {
      throw new UserFacingError("Supply a JSON request of at most 1,000,000 characters; inputs are never truncated.");
    }
  }
  // These packaged configurations are not caller- or document-selectable.
  from_wire("PhaseBSafetyProfile", safetyProfile);
  const release = from_wire("ReviewRuleRelease", ruleRelease);
  try {
    const request = from_json("ReviewRequest", requestJson);
    return canonical_json(review_request(request, release));
  } catch (error: unknown) {
    if (!(error instanceof ContractError)) throw error;
    // Avoid reflecting arbitrary document/field values through platform error logs.
    throw new UserFacingError("Case input does not satisfy the structured-review contract. Correct the required fields, bounded integer values, and JSON format.");
  }
}
