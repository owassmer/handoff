import { describe, expect, it } from "vitest";
import { validateRequest } from "../phase_c/validation.js";
import { syntheticRequest } from "./phaseCTestSupport.js";

describe("stored-case review clock precision", () => {
  it("accepts an exactly representable millisecond clock", () => {
    const request = syntheticRequest();
    request.reviewClock = "2026-09-16T12:00:00.123000Z";
    expect(() => validateRequest(request)).not.toThrow();
  });
  it("rejects rather than rounds submillisecond clock precision", () => {
    const request = syntheticRequest();
    request.reviewClock = "2026-09-16T12:00:00.123001Z";
    expect(() => validateRequest(request)).toThrow(/never rounded/);
    expect(request.reviewClock).toBe("2026-09-16T12:00:00.123001Z");
  });
});
