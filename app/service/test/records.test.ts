import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { setupClock } from "../src/clock.js";
import { type PgliteDb, openMemoryDb } from "../src/db.js";
import {
  accountBalance, accountEntries, addCondition, addDocument, addEntry, addFinding, addInspection, addObservation,
  addWorkItem, caseWorkItems, currentFinding, reverseEntry, updateWorkItem,
} from "../src/records.js";
import { at, seedCase } from "./helpers.js";

const NOV16 = at("2026-11-16T18:00:00Z");
let db: PgliteDb;
beforeEach(async () => {
  db = await openMemoryDb();
  await setupClock(db, "simulated", NOV16);
  await seedCase(db);
});
afterEach(() => db.close());

const photo = (title: string, capturedAt: Date) =>
  addDocument(db, { caseId: "case-1", kind: "photo", title, mediaType: "image/jpeg", storageRef: `sim://${title}`, sha256: "00", source: "operator", capturedAt, receivedAt: capturedAt });

describe("condition records", () => {
  it("keeps documents and observations exactly as recorded", async () => {
    const doc = await photo("closet-door", NOV16);
    await expect(db.query(`update documents set sha256 = 'ff' where id = $1`, [doc])).rejects.toThrow(/kept as recorded/);
    const inspection = await addInspection(db, { caseId: "case-1", kind: "move_out", conductedAt: NOV16, conductedBy: "op-coordinator", photos: [{ documentId: doc, area: "bedroom 2" }] });
    const closet = await addCondition(db, { caseId: "case-1", area: "bedroom 2", item: "closet door", summary: "Door off its track", identifiedAt: NOV16, identifiedIn: inspection });
    const obs = await addObservation(db, { conditionId: closet, inspectionId: inspection, observedBy: "agent:evidence-analyst", observedAt: NOV16, text: "Left sliding door is off the lower track; the track is bent near the center.", documentIds: [doc] });
    await expect(db.query(`delete from observations where id = $1`, [obs])).rejects.toThrow(/kept as recorded/);
  });

  it("supersedes a finding instead of rewriting it", async () => {
    const closet = await addCondition(db, { caseId: "case-1", area: "bedroom 2", item: "closet door", summary: "Door off its track", identifiedAt: NOV16 });
    const first = await addFinding(db, { conditionId: closet, responsibility: "tenant_damage", reasoning: "Not on the move-in record; bent track", foundBy: "agent:run-1", foundAt: NOV16 });
    const second = await addFinding(db, { conditionId: closet, responsibility: "present_at_move_in", reasoning: "Tenant produced a move-in photo of the bent track", foundBy: "agent:run-2", foundAt: at("2026-12-04T18:00:00Z") });
    expect(second.supersedes).toBe(first.id);
    expect((await currentFinding(db, closet))?.responsibility).toBe("present_at_move_in");
    expect(await db.query(`select id from findings`)).toHaveLength(2);
  });
});

describe("work items", () => {
  it("links work to the conditions it fixes and mirrors what the doer reports", async () => {
    const closet = await addCondition(db, { caseId: "case-1", area: "bedroom 2", item: "closet door", summary: "Door off its track", identifiedAt: NOV16 });
    const job = await addWorkItem(db, { caseId: "case-1", performer: "vendor", vendorPartyId: "vendor-1", description: "Repair closet door and track", conditionIds: [closet], estimateCents: 55000 });
    await updateWorkItem(db, job, { status: "completed", completedAt: at("2026-11-24T22:00:00Z"), finalCostCents: 52500 });
    const [w] = await caseWorkItems(db, "case-1");
    expect(w).toMatchObject({ id: job, status: "completed", estimateCents: 55000, finalCostCents: 52500, conditionIds: [closet] });
  });

  it("requires a vendor exactly when a vendor does the work", async () => {
    await expect(addWorkItem(db, { caseId: "case-1", performer: "vendor", description: "Carpet cleaning", conditionIds: [] })).rejects.toThrow();
    await expect(addWorkItem(db, { caseId: "case-1", performer: "in_house", vendorPartyId: "vendor-1", description: "Paint", conditionIds: [] })).rejects.toThrow();
  });
});

describe("the account", () => {
  const entry = (kind: Parameters<typeof addEntry>[1]["kind"], amountCents: number, lineKey?: string) =>
    addEntry(db, { caseId: "case-1", kind, amountCents, lineKey, description: lineKey ?? kind, effectiveOn: "2026-12-01", source: "handoff", recordedAt: NOV16 });

  it("nets the deposit against charges, and settles to zero when the refund is paid", async () => {
    await entry("deposit_held", 243750);
    await entry("charge", 54700, "holdover");
    await entry("charge", 55000, "closet-repair");
    await entry("charge", 60791, "cleaning");
    expect(await accountBalance(db, "case-1")).toBe(-73259);
    await entry("refund_paid", 73259);
    expect(await accountBalance(db, "case-1")).toBe(0);
  });

  it("corrects by reversal, once, and never edits an entry", async () => {
    await entry("deposit_held", 243750);
    const closet = await entry("charge", 55000, "closet-repair");
    const reversal = await reverseEntry(db, closet, { description: "Closet damage shown on move-in photos", effectiveOn: "2026-12-04", source: "handoff", recordedAt: at("2026-12-04T18:00:00Z") });
    expect(await accountBalance(db, "case-1")).toBe(-243750);
    expect((await accountEntries(db, "case-1")).find((e) => e.id === reversal)).toMatchObject({ kind: "reversal", amountCents: -55000, lineKey: "closet-repair", reverses: closet });
    await expect(reverseEntry(db, closet, { description: "again", effectiveOn: "2026-12-04", source: "handoff", recordedAt: NOV16 })).rejects.toThrow();
    await expect(reverseEntry(db, reversal, { description: "undo", effectiveOn: "2026-12-04", source: "handoff", recordedAt: NOV16 })).rejects.toThrow(/cannot itself be reversed/);
    await expect(db.query(`update account_entries set amount_cents = 1 where id = $1`, [closet])).rejects.toThrow(/kept as recorded/);
  });

  it("takes only positive whole cents", async () => {
    await expect(entry("charge", 12.5)).rejects.toThrow(/whole number of cents/);
    await expect(entry("charge", -100)).rejects.toThrow(/positive/);
  });
});
