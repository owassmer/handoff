import { describe, expect, it } from "vitest";
import { deliveryStatus } from "../wording.js";

describe("delivery status", () => {
  const now = "2026-10-08T15:00:00.000Z";
  it("names a vendor on site with the day its visit ends, not as waited on", () => {
    expect(deliveryStatus([
      { vendor: "Westside Plaster & Paint", status: "Scheduled", appointmentAt: "2026-10-05T13:00:00.000Z", appointmentEndsAt: "2026-10-16T21:00:00.000Z" },
      { vendor: "Hudson Floor Restoration", status: "Scheduled", appointmentAt: "2026-10-12T13:00:00.000Z", appointmentEndsAt: "2026-10-14T21:00:00.000Z" },
      { vendor: "Broadway Carpet & Runner", status: "Commissioned" },
    ], now)).toBe("Westside Plaster & Paint on site until Friday, October 16. Waiting on Broadway Carpet & Runner. "
      + "Next visit: Hudson Floor Restoration on Monday, October 12.");
  });
  it("waits on a vendor whose visit has ended and whose report is still due", () => {
    expect(deliveryStatus([{ vendor: "Feld Architecture PLLC", status: "Scheduled", appointmentAt: "2026-09-29T13:00:00.000Z",
      appointmentEndsAt: "2026-09-29T16:00:00.000Z" }], now)).toBe("Waiting on Feld Architecture PLLC.");
  });
  it("falls back to the payment when no job is open", () => {
    expect(deliveryStatus([], now)).toBe("Waiting for a payment to be confirmed.");
  });
});
