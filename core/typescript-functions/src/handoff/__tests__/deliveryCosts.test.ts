import { describe, expect, it } from "vitest";
import { HandoffJob, HandoffPayment } from "@ontology/sdk";
import { createMockOsdkObject } from "@osdk/unit-testing";
import { instant, money } from "../deliveryContracts.js";
import { invoiceMatchesJob, priceCommission, sumQuotedCosts, validateQuoteOffer } from "../quoteCosts.js";
import { fundingPosition } from "../funding.js";
import { providerAppointment, visitEnd } from "../counterparts.js";
import { longDate, nextWorkingStart, plainList, workingEnd, workingSpan } from "../wording.js";
import { mandate, NOW, offer } from "./deliverySupport.js";

const selected = (): { quoteLineId: string; acceptedScope: string }[] => offer().lines.map((line) => ({ quoteLineId: line.lineId, acceptedScope: line.description }));
describe("source costs and mandates", () => {
  it("prices actual lines with exact integer arithmetic", () => {
    expect(priceCommission(mandate(), offer(), selected(), "0", NOW).totalCents).toBe("24500");
    expect(sumQuotedCosts([{ lineId: "a", description: "One", amountCents: "9007199254740993" },
      { lineId: "b", description: "Two", amountCents: "17" }])).toBe("9007199254741010");
  });
  it("checks sums over many amounts without rounding or order dependence", () => {
    Array.from({ length: 250 }, (_, index) => index + 1).forEach((seed) => {
      const amounts = [BigInt(seed) * 7919n, BigInt(seed * seed) * 101n, 9n];
      const lines = amounts.map((amount, index) => ({ lineId: `${index}`, description: "Quoted service", amountCents: amount.toString() }));
      expect(sumQuotedCosts(lines)).toBe(amounts.reduce((sum, amount) => sum + amount, 0n).toString());
      expect(sumQuotedCosts([...lines].reverse())).toBe(sumQuotedCosts(lines));
    });
  });
  it.each([undefined, null, 0, -1, "-1", "1.2", "01", " 2", "1e3", "9223372036854775808"])("rejects absent or noncanonical money %s", (amount) => {
    expect(() => money(amount)).toThrow();
  });
  it.each(["2026-02-30T00:00:00Z", "2026-09-23", "2026-09-23T25:00:00Z", "2026-09-23T10:00:00+00:00"])("rejects invalid time %s", (at) => expect(() => instant(at)).toThrow());
  it("accepts and normalizes UTC seconds", () => expect(instant("2026-09-23T10:00:00Z")).toBe(NOW));
  it("rejects duplicate lines, inconsistent totals, excessive advance and overflow", () => {
    expect(() => validateQuoteOffer({ ...offer(), lines: [offer().lines[0], offer().lines[0]] })).toThrow();
    expect(() => validateQuoteOffer({ ...offer(), totalCents: "20000" })).toThrow();
    expect(() => validateQuoteOffer({ ...offer(), depositCents: "24501" })).toThrow();
    expect(() => sumQuotedCosts([{ lineId: "a", description: "Service", amountCents: "9223372036854775807" },
      { lineId: "b", description: "Service", amountCents: "1" }])).toThrow();
  });
  it("does not reinterpret an accepted assessment as repairs", () => {
    const changed = offer(); changed.lines[0]!.description = "Repair the roof.";
    expect(() => priceCommission(mandate(), changed, selected(), "0", NOW)).toThrow(/different work/);
  });
  it("leaves requirements the offer does not state to the order; enforces fixed provider, currency and accepted evidence", () => {
    expect(priceCommission(mandate(), { ...offer(), requirements: [] }, selected(), "0", NOW).totalCents).toBe("24500");
    expect(() => priceCommission({ ...mandate(), fixedProviderPartyId: "someone-else" }, offer(), selected(), "0", NOW)).toThrow(/provider/);
    expect(() => priceCommission({ ...mandate(), currency: "CAD" }, offer(), selected(), "0", NOW)).toThrow(/currencies/);
    expect(() => priceCommission({ ...mandate(), sourceDocumentIds: [] }, offer(), selected(), "0", NOW)).toThrow(/accepted/);
  });
  it("counts prior commitments against the budget, not only the latest job", () => {
    expect(() => priceCommission(mandate(), offer(), selected(), "5501", NOW)).toThrow(/budget/);
    expect(priceCommission(mandate(), offer(), selected(), "5500", NOW).totalCents).toBe("24500");
  });
  it("does not apportion advance terms to an unquoted partial package", () => {
    expect(() => priceCommission(mandate(), { ...offer(), depositCents: "10000" }, [selected()[0]!], "0", NOW)).toThrow(/terms/);
  });
  it("rejects expired, missing, repeated or out-of-scope selections", () => {
    expect(() => priceCommission(mandate(), offer(), selected(), "0", "2026-10-02T00:00:00Z")).toThrow(/expired/);
    expect(() => priceCommission(mandate(), offer(), [], "0", NOW)).toThrow();
    expect(() => priceCommission(mandate(), offer(), [selected()[0]!, selected()[0]!], "0", NOW)).toThrow();
    expect(() => priceCommission(mandate(), offer(), [{ quoteLineId: "not-offered", acceptedScope: "Other work" }], "0", NOW)).toThrow();
  });
  it("does not conflate invoice cost with matching scope", () => {
    expect(invoiceMatchesJob(offer().lines, offer().lines, "USD", "USD")).toBe(true);
    expect(invoiceMatchesJob([{ ...offer().lines[0]!, description: "Replace fixtures" }], offer().lines, "USD", "USD")).toBe(false);
    expect(invoiceMatchesJob(offer().lines, offer().lines, "USD", "CAD")).toBe(false);
  });
});

describe("owner money is distinct from a budget", () => {
  const funding = { fundingId: "funds", currency: "USD", confirmedCents: "100000" };
  const job = createMockOsdkObject(HandoffJob, { jobId: "job", fundingId: "funds", currency: "USD", committedCents: "60000", status: "Scheduled" });
  const payment = createMockOsdkObject(HandoffPayment, { paymentId: "payment", fundingId: "funds", currency: "USD", jobId: "job", amountCents: "20000", status: "Settled" });
  it("counts commitment and settlement only once", () => expect(fundingPosition(funding, [job], [payment]).availableCents).toBe("40000"));
  it("keeps uncertain payment funds when work is cancelled", () => {
    const cancelled = createMockOsdkObject(HandoffJob, { ...job, status: "Cancelled" });
    const uncertain = createMockOsdkObject(HandoffPayment, { ...payment, status: "Confirming" });
    expect(fundingPosition(funding, [cancelled], [uncertain]).availableCents).toBe("80000");
  });
  it("fails closed on missing confirmations, unknown commitments, duplicate identity and currency mismatch", () => {
    expect(() => fundingPosition({ ...funding, confirmedCents: undefined }, [job], [])).toThrow();
    expect(() => fundingPosition(funding, [createMockOsdkObject(HandoffJob, { ...job, committedCents: undefined })], [])).toThrow();
    expect(() => fundingPosition(funding, [job, job], [])).toThrow();
    expect(() => fundingPosition(funding, [job], [payment, payment])).toThrow();
    expect(() => fundingPosition({ ...funding, currency: "CAD" }, [job], [])).toThrow();
  });
  it("fails closed on overcommitment and orphaned payments", () => {
    expect(() => fundingPosition({ ...funding, confirmedCents: "50000" }, [job], [])).toThrow();
    expect(() => fundingPosition(funding, [], [payment])).toThrow();
  });
  it("preserves exact available funds across many disjoint commitments", () => {
    Array.from({ length: 100 }, (_, count) => count + 1).forEach((count) => {
      const jobs = Array.from({ length: count }, (_, index) => createMockOsdkObject(HandoffJob,
        { jobId: `${index}`, fundingId: "funds", currency: "USD", committedCents: "100", status: "Complete" }));
      expect(fundingPosition(funding, jobs, []).availableCents).toBe((100000 - count * 100).toString());
    });
  });
});

describe("provider availability", () => {
  it("uses offered availability and avoids overlapping reservations", () => {
    const other = createMockOsdkObject(HandoffJob, { jobId: "other", providerPartyId: offer().providerPartyId,
      status: "Scheduled", appointmentAt: offer().availableFrom, appointmentEndsAt: "2026-09-24T10:30:00.000Z" });
    expect(providerAppointment(offer(), NOW, [other], "job")).toEqual({ start: "2026-09-24T10:30:00.000Z", end: "2026-09-24T11:30:00.000Z" });
  });
  it("does not invent an end time for another appointment", () => {
    const other = createMockOsdkObject(HandoffJob, { jobId: "other", providerPartyId: offer().providerPartyId,
      status: "Scheduled", appointmentAt: offer().availableFrom });
    expect(() => providerAppointment(offer(), NOW, [other], "job")).toThrow(/end time/);
  });
  it("writes dates, spans and lists as an operator reads them", () => {
    expect(longDate("2026-10-05T13:00:00Z")).toBe("Monday, October 5");
    expect([workingSpan(1), workingSpan(180), workingSpan(480), workingSpan(4800)]).toEqual(["1 minute", "3 hours", "8 hours", "10 working days"]);
    expect([plainList(["A"]), plainList(["A", "B"]), plainList(["A", "B", "C"])]).toEqual(["A", "A and B", "A, B and C"]);
  });
  it("runs multi-day work in daily working windows, skipping nights and weekends", () => {
    const dayStart = "2026-10-05T13:00:00Z";
    expect(nextWorkingStart("2026-09-27T20:00:00Z", dayStart)).toBe("2026-09-28T13:00:00.000Z");
    expect(workingEnd("2026-10-05T13:00:00Z", 4800, dayStart)).toBe("2026-10-16T21:00:00.000Z");
    expect(workingEnd("2026-10-09T13:00:00Z", 960, dayStart)).toBe("2026-10-12T21:00:00.000Z");
    const twoDays = { ...offer(), durationMinutes: 960 };
    expect(providerAppointment(twoDays, NOW, [], "job")).toEqual({ start: "2026-09-24T09:00:00.000Z", end: "2026-09-25T17:00:00.000Z" });
    expect(visitEnd(offer(), "2026-09-24T09:00:00.000Z")).toBe(instant("2026-09-24T10:00:00Z"));
  });
});
