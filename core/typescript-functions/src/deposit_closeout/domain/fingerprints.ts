/** Deterministic review identifiers, never execution or approval authority. */
import { createHash } from "node:crypto";
import { canonical_json } from "./codec.js";

export function fingerprint(value: unknown): string {
  return createHash("sha256").update(canonical_json(value), "utf8").digest("hex");
}
