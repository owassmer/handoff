import { describe, expect, it } from "vitest";
import { instant } from "../deliveryContracts.js";

describe("SDK millisecond timestamp precision", () => {
  it("accepts every millisecond with SDK trailing-zero omission", () => {
    for (let millisecond = 0; millisecond < 1000; millisecond += 1) {
      const expected = `2026-09-24T22:01:01.${String(millisecond).padStart(3, "0")}Z`;
      const wire = expected.replace(/0+Z$/, "Z").replace(/\.Z$/, "Z");
      expect(instant(wire)).toBe(expected);
    }
  });
  it("preserves genuinely different instants", () => {
    expect(instant("2026-09-24T22:01:01.03Z")).not.toBe(instant("2026-09-24T22:01:01.031Z"));
  });
  it.each([
    "2026-02-30T00:00:00Z", "2026-09-24T24:00:00Z", "2026-09-24",
    "2026-09-24T22:01:01.Z", "2026-09-24T22:01:01.0001Z", "2026-09-24T22:01:01+00:00",
  ])("rejects invalid or unsupported values without rounding: %s", (value) => {
    expect(() => instant(value)).toThrow();
  });
});
