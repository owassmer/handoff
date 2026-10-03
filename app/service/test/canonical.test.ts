import { describe, expect, it } from "vitest";
import { canonicalJson, contentHash } from "../src/canonical.js";

describe("canonical content", () => {
  it("is independent of key order and drops undefined fields", () => {
    expect(canonicalJson({ b: 1, a: { d: [1, 2], c: null }, z: undefined })).toBe('{"a":{"c":null,"d":[1,2]},"b":1}');
    expect(contentHash({ x: 1, y: 2 })).toBe(contentHash({ y: 2, x: 1 }));
  });

  it("changes with any change of content", () => {
    expect(contentHash({ amountCents: 73259 })).not.toBe(contentHash({ amountCents: 72359 }));
  });

  it("refuses what JSON cannot carry exactly", () => {
    expect(() => canonicalJson({ n: Number.NaN })).toThrow();
    expect(() => canonicalJson([undefined])).toThrow();
    expect(() => canonicalJson({ d: new Date() })).toThrow();
  });
});
