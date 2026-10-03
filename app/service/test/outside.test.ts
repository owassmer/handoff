import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { decide, propose } from "../src/decisions.js";
import { caseEvents } from "../src/events.js";
import { accountBalance, accountEntries, addEntry, addWorkItem, caseWorkItems } from "../src/records.js";
import { seedLedger, setScenario } from "../src/sim/index.js";
import { World } from "../src/world.js";
import { ADMIN, DECIDER, at, noTurn, seedCase, statement } from "./helpers.js";

const AGENT = { kind: "agent", runId: "run-1" } as const;
let w: World;

async function world(start: string) {
  w = await World.create(at(start), noTurn);
  await seedCase(w.db);
}
afterEach(() => w.close());

async function accept(kind: string, content: Record<string, unknown>, caseId: string | null = "case-1") {
  const d = await propose(w.db, AGENT, { caseId, kind, content }, await w.now());
  return decide(w.db, caseId ? DECIDER : ADMIN, d.id, d.contentHash, { verdict: "accept" }, await w.now());
}
const act = (kind: string, req: unknown) => w.gateway.execute(AGENT, "case-1", kind, req);
const eventsOf = async (kind: string) => (await caseEvents(w.db, "case-1")).filter((e) => e.kind === kind);

describe("ledger", () => {
  beforeEach(() => world("2026-12-01T17:00:00Z"));

  it("posts each accepted line once, with the amounts from the decision, and enters it in the account", async () => {
    await seedLedger(w.db, [{ tenancyRef: "ten-1", postedOn: "2025-11-11", code: "deposit_received", description: "Security deposit", amountCents: 0 }], at("2025-11-11T17:00:00Z"));
    await addEntry(w.db, { caseId: "case-1", kind: "deposit_held", description: "Security deposit", amountCents: 243750, effectiveOn: "2025-11-11", source: "ledger", recordedAt: at("2025-11-11T17:00:00Z") });
    const d = await accept("account.statement", statement());
    for (const lineKey of ["holdover", "closet-repair", "cleaning"]) expect((await act("ledger.post", { decisionId: d.id, lineKey })).status).toBe("succeeded");
    expect((await act("ledger.post", { decisionId: d.id, lineKey: "closet-repair" })).status).toBe("succeeded");
    expect((await w.ledger.transactions("ten-1")).filter((t) => t.code !== "deposit_received").map((t) => [t.code, t.amountCents]))
      .toEqual([["rent", 54700], ["charge", 55000], ["charge", 60791]]);
    expect(await accountBalance(w.db, "case-1")).toBe(-73259);
    expect((await act("ledger.post", { decisionId: d.id, lineKey: "carpet" })).reason).toMatch(/no line carpet/);
  });

  it("enters a posting confirmed late in the account exactly once", async () => {
    const d = await accept("account.statement", statement());
    await setScenario(w.db, "ledger", "post", { mode: "timeout-after-send", remaining: 1 });
    expect((await act("ledger.post", { decisionId: d.id, lineKey: "cleaning" })).status).toBe("uncertain");
    expect(await accountEntries(w.db, "case-1")).toHaveLength(0);
    expect((await act("ledger.post", { decisionId: d.id, lineKey: "cleaning" })).status).toBe("succeeded");
    expect(await w.ledger.transactions("ten-1")).toHaveLength(1);
    expect(await accountEntries(w.db, "case-1")).toMatchObject([{ kind: "charge", lineKey: "cleaning", amountCents: 60791 }]);
  });
});

describe("utility biller", () => {
  beforeEach(() => world("2026-11-16T18:00:00Z"));

  it("delivers the final water bill from an actual read, and the late gas bill on its own date", async () => {
    await setScenario(w.db, "utilities", "ten-1", {
      water: { readWithinDays: 3, amountCents: 8412, periodStart: "2026-11-01" },
      others: [{ utility: "gas", issueOn: "2026-12-10", amountCents: 6233, periodStart: "2026-10-20" }],
    });
    expect((await act("utility.request_final_bills", { moveOutOn: "2026-11-16" })).authorityBasis).toMatch(/^routine/);
    expect((await act("utility.request_final_bills", { moveOutOn: "2026-11-16" })).status).toBe("succeeded");
    await w.advanceTo(at("2026-12-11T00:00:00Z"));
    const bills = await eventsOf("utility.bill_issued");
    expect(bills.map((b) => [b.payload.utility, b.payload.readType, b.occurredAt.toISOString().slice(0, 10)])).toEqual([
      ["water", "actual", "2026-11-20"],
      ["gas", "actual", "2026-12-10"],
    ]);
    expect(bills[0]!.trusted).toBe(true);
    expect(await w.utilities.bills("ten-1")).toHaveLength(2);
  });

  it("bills water from the previous month when the submeter could not be read in five days", async () => {
    await setScenario(w.db, "utilities", "ten-1", { water: { readWithinDays: null, amountCents: 7900, periodStart: "2026-11-01" } });
    await act("utility.request_final_bills", { moveOutOn: "2026-11-16" });
    await w.advanceTo(at("2026-11-30T00:00:00Z"));
    expect((await eventsOf("utility.bill_issued")).map((b) => b.payload.readType)).toEqual(["previous_month"]);
  });
});

describe("in-house maintenance", () => {
  beforeEach(() => world("2026-11-25T17:00:00Z"));

  async function paintPlan() {
    const paint = await addWorkItem(w.db, { caseId: "case-1", performer: "in_house", description: "Paint bedroom 2 walls", conditionIds: [] });
    const plan = await accept("work.plan", {
      items: [{ workItemId: paint, performer: "in_house", category: "paint", description: "Paint bedroom 2 walls", budgetCents: 40000 }],
      totalBudgetCents: 40000,
    });
    return { paint, plan };
  }

  it("orders planned work only under the accepted plan, and works around Thanksgiving", async () => {
    await setScenario(w.db, "maintenance", "team", {
      holidays: ["2026-11-26", "2026-11-27"],
      byCategory: { paint: { businessDays: 2, hours: 6.5, hourlyRateCents: 4500, materialsCents: 3800 } },
    });
    const { paint, plan } = await paintPlan();
    expect((await act("maintenance.create_work_order", { key: "paint", workItemId: paint, category: "paint", description: "Paint bedroom 2 walls" })).status).toBe("refused");
    const order = await act("maintenance.create_work_order", { key: "paint", workItemId: paint, decisionId: plan.id, category: "paint", description: "Paint bedroom 2 walls" });
    expect(order.status).toBe("succeeded");
    expect(order.result?.scheduledFor).toBe("2026-11-30T17:00:00.000Z");
    expect((await caseWorkItems(w.db, "case-1"))[0]).toMatchObject({ status: "scheduled", externalRef: order.result?.ref });

    await w.advanceTo(at("2026-12-02T00:00:00Z"));
    const [done] = await eventsOf("work_order.completed");
    expect(done).toMatchObject({ source: "outside_system", payload: { hours: 6.5, hourlyRateCents: 4500, materialsCents: 3800 } });
    expect(done!.occurredAt.toISOString()).toBe("2026-12-01T17:00:00.000Z");
  });

  it("allows routine work a standing instruction names, and nothing else without a plan", async () => {
    await accept("standing.routine-work", { categories: ["inspection", "cleaning"] }, null);
    expect((await act("maintenance.create_work_order", { key: "pre-inspection", category: "inspection", description: "Pre-move-out inspection" })).authorityBasis).toBe("standing");
    expect((await act("maintenance.create_work_order", { key: "fix", category: "repair", description: "Fix closet" })).reason).toMatch(/not routine work/);
  });
});

describe("vendors", () => {
  beforeEach(() => world("2026-11-17T17:00:00Z"));

  it("quotes on request, takes an order only within the accepted budget, and invoices later", async () => {
    await setScenario(w.db, "vendors", "vendor-1", {
      quote: { afterBusinessDays: 1, options: [
        { option: "repair", amountCents: 55000, description: "Rehang door, replace bottom track" },
        { option: "rebuild", amountCents: 128000, description: "Replace door, track and header" },
      ] },
      job: { businessDays: 3 },
      invoice: { afterBusinessDays: 12, amountCents: 52500 },
    });
    expect((await act("vendor.request_quote", { key: "closet-quote", vendorPartyId: "vendor-1", scope: "Bedroom 2 closet door and track" })).status).toBe("succeeded");
    await w.advanceTo(at("2026-11-19T00:00:00Z"));
    const [quote] = await eventsOf("vendor.quote_received");
    expect(quote).toMatchObject({ source: "counterparty", trusted: false });
    expect((quote!.payload.options as unknown[]).length).toBe(2);

    const closet = await addWorkItem(w.db, { caseId: "case-1", performer: "vendor", vendorPartyId: "vendor-1", description: "Rehang door, replace bottom track", conditionIds: [] });
    const plan = await accept("work.plan", {
      items: [{ workItemId: closet, performer: "vendor", vendorPartyId: "vendor-1", category: "repair", description: "Rehang door, replace bottom track", budgetCents: 55000 }],
      totalBudgetCents: 55000,
    });
    const order = (cents: number) => act("vendor.place_order", { decisionId: plan.id, workItemId: closet, vendorPartyId: "vendor-1", scope: "Rehang door, replace bottom track", notToExceedCents: cents });
    expect((await order(128000)).reason).toMatch(/exceeds the accepted budget/);
    expect((await order(55000)).status).toBe("succeeded");
    expect((await caseWorkItems(w.db, "case-1"))[0]).toMatchObject({ status: "ordered", estimateCents: 55000 });

    await w.advanceTo(at("2026-12-15T00:00:00Z"));
    const [invoice] = await eventsOf("vendor.invoice_received");
    expect(invoice!.payload.amountCents).toBe(52500);
    // The invoice lands after the December 7 deadline: the statement must carry a good-faith estimate.
    expect(invoice!.occurredAt.toISOString().slice(0, 10)).toBe("2026-12-10");
  });
});

describe("collector", () => {
  beforeEach(() => world("2026-12-20T17:00:00Z"));

  const pursuit = (total: number) => ({
    route: "collector",
    collector: {
      debtorPartyId: "tenant-1", creditor: "Demo Owner LLC", totalCents: total,
      components: [
        { componentId: "rent", description: "Unpaid rent, December 1-14", amountCents: 127633, consumerCredit: false },
        { componentId: "gas", description: "Final gas bill", amountCents: 6233, consumerCredit: true },
      ],
    },
  });

  it("places a balance only as accepted, and keeps the old amount until a correction is applied", async () => {
    const wrong = await accept("balance.pursuit", pursuit(999));
    expect((await act("collector.place", { decisionId: wrong.id })).reason).toMatch(/add to 133866 cents/);
    const d = await accept("balance.pursuit", pursuit(133866));
    const placed = await act("collector.place", { decisionId: d.id });
    expect(placed.status).toBe("succeeded");
    const placementRef = String(placed.result?.ref);

    await setScenario(w.db, "collector", "behavior", { applyAdjustmentAfterDays: 5 });
    const fix = await accept("balance.correction", { placementRef, componentId: "gas", amountCents: 0, reason: "Gas bill disputed and waived" });
    expect((await act("collector.adjust", { decisionId: fix.id })).status).toBe("succeeded");
    expect((await w.collector.status(placementRef)).balanceCents).toBe(133866);

    await w.advanceTo(at("2026-12-26T00:00:00Z"));
    expect((await w.collector.status(placementRef)).balanceCents).toBe(127633);
    const [report] = await eventsOf("collector.balance_reported");
    expect(report).toMatchObject({ trusted: false, payload: { balanceCents: 127633 } });
  });
});
