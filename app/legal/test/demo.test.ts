import { beforeAll, describe, expect, it } from "vitest";
import { DEMO, DEMO_LINES, type DemoLine, demoFacts, demoFactsForLine, fixtureAnswers } from "../src/demo/index.js";
import { type EvaluateOptions, type EvaluationResult, type Facts, type Jurisdiction, evaluate } from "../src/index.js";
import { california } from "./helpers.js";

/**
 * The demonstration case walked through the California trees, under Owen's October 3 rulings:
 * holdover days are rent at the contract daily rate, documents are a duty attached to each deduction,
 * water's five-day read runs from the return of possession, and the tenant page collects a separate
 * agreement to deal electronically.
 */

let jur: Jurisdiction;
beforeAll(async () => {
  jur = await california();
});

const opts = (extra: Partial<EvaluateOptions> = {}): EvaluateOptions => ({
  jurisdiction: jur,
  eventDate: DEMO.eventDate,
  answers: fixtureAnswers(),
  ...extra,
});
const run = (id: string, facts: Facts = demoFacts(), extra: Partial<EvaluateOptions> = {}) => evaluate(id, facts, opts(extra));
const forLine = (id: string, line: DemoLine, extra: Partial<EvaluateOptions> = {}) => evaluate(id, demoFactsForLine(line), opts(extra));
const effect = (r: EvaluationResult, id: string) => {
  const e = r.effects.find((x) => x.id === id);
  if (!e) throw new Error(`no effect ${id} in ${r.treeId}`);
  return e;
};

describe("before move-out", () => {
  it("the tenant's notice on October 12 makes both written notices due that day", async () => {
    const offer = await run("CA.inspection-offer-notice");
    expect(effect(offer, "send-offer-notice")).toMatchObject({ applies: true, due: { value: "2026-10-12" } });
    const eRefund = await run("CA.electronic-refund-notice");
    expect(effect(eRefund, "send-electronic-refund-notice")).toMatchObject({ applies: true, due: { value: "2026-10-12" } });
  });

  it("the requested inspection may be no earlier than October 27, with 48 hours' notice before November 2 at 10:00", async () => {
    const insp = await run("CA.initial-inspection");
    expect(effect(insp, "inspect")).toMatchObject({ applies: true, due: { value: "2026-11-10" }, notBefore: { value: "2026-10-27" } });
    const notice = await run("CA.inspection-notice-48h");
    // Daylight time ends on November 1, so 48 hours before 10:00 PST is 11:00 PDT on October 31.
    expect(effect(notice, "give-48-hour-notice")).toMatchObject({ applies: true, due: { value: "2026-10-31T11:00:00-07:00" } });
  });
});

describe("rent and holdover", () => {
  it("rent under the lease stops on November 10: no rent was accepted for later days", async () => {
    const answers = fixtureAnswers();
    const r = await run("CA.rent-to-term-end", demoFacts(), { answers });
    expect(r.root).toBe(true);
    expect(effect(r, "rent-through-term-end").applies).toBe(true);
    expect(r.leaves["rent-accepted-after-expiry"]!.value).toBe(false);
    expect(answers.asked).toEqual([]);
  });

  it("holdover-charge: six days at monthly rent ÷ 30 November days is 54,700 cents", async () => {
    const r = await run("CA.holdover-charge");
    expect(r.root).toBe(true);
    expect(effect(r, "may-charge-holdover")).toMatchObject({ applies: true, amount: { status: "known", value: 54_700 } });
    expect(r.diagnostics).toEqual([]);
  });

  it("deduct-holdover holds through holdover-is-rent, because the lease makes holdover days rent; C6 does not arise", async () => {
    const r = await run("CA.deduct-holdover");
    expect(r.root).toBe(true);
    expect(r.leaves["holdover-is-rent"]!.value).toBe(true);
    expect(r.leaves["holdover-chargeable"]!.value).toBe(true);
    expect(r.leaves["any-purpose-reaches-holdover"]!.value).toBe("unknown");
    expect(effect(r, "may-deduct-holdover")).toMatchObject({ applies: true, amount: { value: 54_700 } });
    expect(r.contested[0]!.branches.map((b) => [b.id, b.root])).toEqual([
      ["A", true],
      ["B", true],
    ]);
    expect(r.exposure!.root).toBe(true);
    expect(r.investigation).toEqual([]);
    expect(r.references["CA.holdover-charge"]!.root).toBe(true);
  });

  it("without the holdover clause the deduction turns on C6, and its exposure branch bills it separately", async () => {
    const facts = demoFacts();
    const lease = facts.lease as Record<string, unknown>;
    const r = await run("CA.deduct-holdover", { ...facts, lease: { ...lease, holdoverClause: null } });
    expect(r.root).toBe("unknown");
    expect(r.investigation.map((i) => i.leafId)).toEqual(["any-purpose-reaches-holdover"]);
    expect(r.exposure!.root).toBe(false);
    expect(r.exposure!.effects.find((e) => e.id === "bill-holdover-separately")!.applies).toBe(true);
  });
});

describe("deductions", () => {
  it("deduct-repair: the closet holds on the fixture answers, at the tenant's share of the cost", async () => {
    const answers = fixtureAnswers();
    const r = await forLine("CA.deduct-repair", DEMO_LINES.closet, { answers });
    expect(r.root).toBe(true);
    // $420.00 times half the closet door's 120-month life remaining.
    expect(effect(r, "may-deduct")).toMatchObject({ applies: true, amount: { value: 21_000 } });
    // Documents are a duty attached to the deduction (Owen, point 1), not a condition of it.
    expect(effect(r, "document-deduction")).toMatchObject({ kind: "duty", applies: true, consequence: "CA.bad-faith-retention" });
    expect(r.leaves["inspection-gate"]!.value).toBe(true);
    // The closet was on the list, so the gate's C9 exposure branch does not bar it either.
    expect(r.exposure!.root).toBe(true);
    expect(answers.asked.map((a) => a.leafId)).toEqual(expect.arrayContaining(["caused-by-tenant", "not-preexisting", "extent-beyond-wear", "restores-not-improves", "cost-reasonable"]));
    expect(r.investigation).toEqual([]);
    expect(r.diagnostics).toEqual([]);
  });

  it("deduct-repair: with the move-in photos missing, the questions that need them are not asked and the leaf goes on the investigation list", async () => {
    const answers = fixtureAnswers();
    const facts = demoFactsForLine(DEMO_LINES.closet);
    const photos = { ...(facts.photos as Record<string, unknown>) };
    delete photos.moveIn;
    const r = await evaluate("CA.deduct-repair", { ...facts, photos }, opts({ answers }));
    expect(r.root).toBe("unknown");
    const asked = answers.asked.filter((a) => a.treeId === "CA.deduct-repair").map((a) => a.leafId);
    expect(asked).not.toContain("not-preexisting");
    expect(asked).not.toContain("restores-not-improves");
    expect(asked).toContain("caused-by-tenant");
    expect(r.leaves["not-preexisting"]).toMatchObject({ value: "unknown", basis: { by: "evidence-missing", missing: ["photos.moveIn"] } });
    expect(r.investigation.map((i) => [i.leafId, i.ifTrue, i.ifFalse, i.decisive])).toEqual([
      ["not-preexisting", "unknown", false, true],
      ["restores-not-improves", "unknown", false, true],
    ]);
    expect(r.investigation[0]!.settle).toMatchObject({ by: "question", missing: ["photos.moveIn"] });
    expect(effect(r, "may-deduct")).toMatchObject({ applies: "unknown", amount: { value: 21_000 } });
  });

  it("deduct-repair: paint at two-thirds of its 36-month life remaining", async () => {
    const r = await forLine("CA.deduct-repair", DEMO_LINES.paint);
    expect(r.root).toBe(true);
    expect(effect(r, "may-deduct").amount).toMatchObject({ value: 26_000 });
  });

  it("deduct-cleaning: carpet extraction as necessary professional cleaning, and in-house cleaning at its hours", async () => {
    const carpet = await forLine("CA.deduct-cleaning", DEMO_LINES.carpet);
    expect(carpet.root).toBe(true);
    expect(carpet.leaves["professional-cleaning-necessary"]!.value).toBe(true);
    expect(effect(carpet, "may-deduct").amount).toMatchObject({ value: 18_500 });
    const cleaning = await forLine("CA.deduct-cleaning", DEMO_LINES.cleaning);
    expect(cleaning.root).toBe(true);
    expect(cleaning.leaves["professional-cleaning-necessary"]!.basis.by).toBe("not-needed");
    expect(effect(cleaning, "may-deduct").amount).toMatchObject({ value: 13_500 });
  });

  it("inspection-list-gate bars a condition identifiable at the inspection but left off the list", async () => {
    const answers = fixtureAnswers();
    const gate = await forLine("CA.inspection-list-gate", DEMO_LINES.cabinet, { answers });
    expect(gate.root).toBe(false);
    expect(gate.leaves["listed-in-statement"]!.value).toBe(false);
    expect(gate.leaves["no-inspection-conducted"]!.value).toBe(false);
    expect(gate.leaves["not-cured"]!.basis.by).toBe("not-needed");
    expect(effect(gate, "barred-by-list")).toMatchObject({ kind: "prohibition", applies: true, consequence: "CA.statutory-damages" });
    expect(gate.contested[0]!.branches.map((b) => b.root)).toEqual([false, false]);
    const repair = await forLine("CA.deduct-repair", DEMO_LINES.cabinet);
    expect(repair.root).toBe(false);
    expect(repair.leaves["inspection-gate"]!.value).toBe(false);
    expect(effect(repair, "must-not-deduct").applies).toBe(true);
    // The listed closet passes the same gate.
    expect((await forLine("CA.inspection-list-gate", DEMO_LINES.closet)).root).toBe(true);
  });

  it("deduct-water holds with the final bill attached, and fails without it", async () => {
    const withBill = await run("CA.deduct-water");
    expect(withBill.root).toBe(true);
    expect(effect(withBill, "may-deduct-water")).toMatchObject({ applies: true, amount: { value: 5_475 } });
    expect(withBill.leaves["final-bill-method"]!.value).toBe(true);

    const facts = demoFacts();
    const statement = facts.statement as Record<string, unknown>;
    const without = await run("CA.deduct-water", { ...facts, statement: { ...statement, attachments: ["invoice-closet", "photos-link"] } });
    expect(without.root).toBe(false);
    expect(without.leaves["bill-attached"]!.value).toBe(false);
    expect(effect(without, "must-not-deduct-water").applies).toBe(true);
  });

  it("the water submeter read is due five days after possession returned", async () => {
    const r = await run("CA.water-final-bill");
    expect(effect(r, "read-within-five-days")).toMatchObject({ applies: true, due: { value: "2026-11-21" } });
  });

  it("no unpaid rent: twelve months were paid electronically", async () => {
    const r = await run("CA.deduct-unpaid-rent");
    expect(r.root).toBe(false);
    expect(r.leaves["rent-default"]!.value).toBe(false);
  });
});

describe("statement and refund", () => {
  it("statement-due: December 7, 2026, 21 days after November 16; a Monday, so the margin is the same day", async () => {
    const r = await run("CA.statement-due");
    expect(r.root).toBe(true);
    expect(effect(r, "furnish-statement-and-refund")).toMatchObject({
      applies: true,
      due: { value: "2026-12-07" },
      margin: { value: "2026-12-07" },
      consequence: "CA.bad-faith-retention",
    });
  });

  it("statement-due: a day 21 on a Saturday keeps the nominal date and records the extension only as margin (C5)", async () => {
    const facts = demoFacts();
    const r = await run("CA.statement-due", { ...facts, moveOut: { ...(facts.moveOut as object), vacateDate: "2026-11-14" } });
    expect(effect(r, "furnish-statement-and-refund")).toMatchObject({ due: { value: "2026-12-05" }, margin: { value: "2026-12-07" } });
  });

  it("repair-cleaning-documentation applies when repair and cleaning total more than $125", async () => {
    const r = await run("CA.repair-cleaning-documentation");
    expect(r.root).toBe(true);
    for (const id of ["in-house-work", "vendor-work", "materials", "photographs"]) {
      expect(effect(r, id)).toMatchObject({ kind: "duty", applies: true, due: { value: "2026-12-07" } });
    }
  });

  it("repair-cleaning-documentation does not apply at or under $125 with no request", async () => {
    for (const amounts of [[9_500], [7_500, 5_000]]) {
      const facts = demoFacts();
      const statement = facts.statement as Record<string, unknown>;
      const lines = amounts.map((amount, i) => ({ id: `l${i}`, amount }));
      const r = await run("CA.repair-cleaning-documentation", { ...facts, statement: { ...statement, lines: { repairAndCleaning: lines } } });
      expect(r.root).toBe(false);
      expect(r.leaves["under-documentation-threshold"]!.value).toBe(true);
      expect(effect(r, "photographs").applies).toBe(false);
      expect(effect(r, "documents-on-request-only").applies).toBe(true);
    }
  });

  it("documentation-on-request applies to a request within 14 days of the statement, due 14 days after it", async () => {
    const request = (sent: string) => ({ ...demoFacts(), message: { from: "tenant", sentDate: sent, receivedDate: sent, text: "Please send me the invoices and photos for the charges." } });
    const r = await run("CA.documentation-on-request", request("2026-12-03"));
    expect(r.root).toBe(true);
    expect(effect(r, "send-documents")).toMatchObject({ kind: "duty", applies: true, due: { value: "2026-12-17" } });
    const late = await run("CA.documentation-on-request", request("2026-12-16"));
    expect(late.root).toBe(false);
    expect(late.leaves["request-within-14-days"]!.value).toBe(false);
  });

  it("refund-electronic applies: rent was paid electronically and the tenant designated an account on the page", async () => {
    const r = await run("CA.refund-electronic");
    expect(r.root).toBe(true);
    expect(effect(r, "refund-electronically")).toMatchObject({ applies: true, due: { value: "2026-12-07" } });
    expect(r.leaves["paid-electronically"]!.value).toBe(true);
    // One adult tenant: C8's branches agree.
    expect(r.contested[0]!.branches.map((b) => b.root)).toEqual([true, true]);
    // The other refund methods do not apply.
    for (const id of ["CA.refund-check-to-all", "CA.refund-check-or-delivery", "CA.refund-agreed-method"]) expect((await run(id)).root).toBe(false);
  });

  it("the page designation is a writing through electronic-writing, because of the separate, optional agreement", async () => {
    const r = await run("CA.electronic-writing");
    expect(r.root).toBe(true);
    expect(r.leaves["separate-optional-agreement"]!.value).toBe(true);
    expect(r.leaves["agreement-from-conduct"]!.basis.by).toBe("not-needed");
    expect(effect(r, "electronic-record-is-writing").applies).toBe(true);

    // Without it, a clause in the paper lease does not count, and electronic payment is no agreement.
    const noAgreement = await run("CA.electronic-writing", { ...demoFacts(), eAgreement: null });
    expect(noAgreement.leaves["electronic-lease-agreement"]!.value).toBe(false);
    expect(noAgreement.root).toBe(false);
    expect(effect(noAgreement, "not-a-writing").applies).toBe(true);
  });

  it("the statement may be emailed under the separate agreement; C14's branches agree", async () => {
    const r = await run("CA.statement-delivery");
    expect(r.root).toBe(true);
    expect(r.contested.find((c) => c.issue === "C14")!.branches.map((b) => b.root)).toEqual([true, true]);
  });

  it("the account: the trees' amounts leave $1,045.75 to refund electronically by December 7", async () => {
    const holdover = effect(await run("CA.deduct-holdover"), "may-deduct-holdover");
    const repairs = await Promise.all([DEMO_LINES.closet, DEMO_LINES.paint].map((l) => forLine("CA.deduct-repair", l)));
    const cleanings = await Promise.all([DEMO_LINES.carpet, DEMO_LINES.cleaning].map((l) => forLine("CA.deduct-cleaning", l)));
    const water = effect(await run("CA.deduct-water"), "may-deduct-water");
    const lines = [holdover, ...repairs.map((r) => effect(r, "may-deduct")), ...cleanings.map((r) => effect(r, "may-deduct")), water];
    for (const l of lines) expect(l.applies).toBe(true);
    const deducted = lines.reduce((s, l) => s + (l.amount!.value as number), 0);
    expect(deducted).toBe(54_700 + 21_000 + 26_000 + 18_500 + 13_500 + 5_475);
    expect(DEMO.deposit - deducted).toBe(104_575);
  });
});

describe("consequences on the demonstration facts", () => {
  it("no subdivision (h) failure: no forfeiture and no statutory damages, with the maximum shown", async () => {
    const bad = await run("CA.bad-faith-retention");
    expect(bad.root).toBe(false);
    expect(effect(bad, "no-forfeiture").applies).toBe(true);
    const stat = await run("CA.statutory-damages");
    expect(stat.root).toBe(false);
    expect(effect(stat, "statutory-damages-exposure").amount).toMatchObject({ value: 2 * DEMO.deposit });
  });

  it("a bad-faith failure forfeits the deposit; statutory damages turn on C2, exposed on branch A", async () => {
    const facts = { ...demoFacts(), compliance: { subdivisionHFailures: [{ duty: "photographs", line: "closet" }] } };
    const answers = fixtureAnswers({ "failure-in-bad-faith": true, "claim-in-bad-faith": true });
    const bad = await run("CA.bad-faith-retention", facts, { answers });
    expect(effect(bad, "security-forfeited")).toMatchObject({ applies: true, amount: { value: DEMO.deposit } });
    const stat = await run("CA.statutory-damages", facts, { answers: fixtureAnswers({ "claim-in-bad-faith": true }) });
    expect(stat.root).toBe("unknown");
    expect(stat.investigation.map((i) => i.leafId)).toEqual(["forfeiture-retention-counts"]);
    expect(stat.contested[0]!.branches.map((b) => [b.id, b.root])).toEqual([
      ["A", true],
      ["B", false],
    ]);
    expect(stat.exposure!.root).toBe(true);
    expect(stat.exposure!.effects[0]!.amount).toMatchObject({ value: 487_500 });
  });
});

it("every tree evaluates on the demonstration facts without a formula or binding error", async () => {
  for (const id of jur.ids()) {
    const r = await evaluate(id, demoFactsForLine(DEMO_LINES.closet), opts());
    expect(r.diagnostics, id).toEqual([]);
  }
});
