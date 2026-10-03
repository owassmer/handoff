import { createHash } from "node:crypto";

/**
 * JSON with object keys sorted and no insignificant whitespace, so the same content always
 * produces the same text. Undefined object fields are dropped; anything JSON cannot carry
 * exactly (undefined in arrays, non-finite numbers, bigint, functions) is refused.
 */
export function canonicalJson(value: unknown): string {
  if (value === null || typeof value === "boolean" || typeof value === "string") return JSON.stringify(value);
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new Error(`cannot hash non-finite number ${value}`);
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => {
      if (item === undefined) throw new Error("cannot hash undefined inside an array");
      return canonicalJson(item);
    }).join(",")}]`;
  }
  if (typeof value === "object" && value.constructor === Object) {
    const entries = Object.entries(value).filter(([, v]) => v !== undefined).sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0));
    return `{${entries.map(([k, v]) => `${JSON.stringify(k)}:${canonicalJson(v)}`).join(",")}}`;
  }
  throw new Error(`cannot hash ${typeof value}`);
}

/** The hash an operator's acceptance is bound to. */
export function contentHash(value: unknown): string {
  return `sha256:${createHash("sha256").update(canonicalJson(value)).digest("hex")}`;
}
