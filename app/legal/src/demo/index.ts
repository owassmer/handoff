/**
 * The demonstration case (DESIGN.md §1–2) as the facts the California account-core trees read.
 *
 * This is the shape the service's case binding will fill from real records: one object per input
 * name the trees declare (tenancy, deposit, moveOut, ledger...). Money is integer cents; dates are ISO
 * calendar dates in California business time; a moment is an ISO date-time read as California time.
 * A fact left undefined is unknown; null means known to be absent (no such record).
 *
 * The lease, rent, deposit, dates and holdover come from the design. The charge amounts, useful lives,
 * water bill and evidence descriptions are fixture assumptions chosen to be plausible, not decisions.
 */
import type { Answer, AnswerProvider, Facts } from "../evaluate.js";
import type { Condition } from "../schema.js";
import { addDays, daysBetween, daysInMonth } from "../time.js";
import type { Truth } from "../values.js";

export const DEMO = {
  leaseStart: "2025-11-11",
  leaseEnd: "2026-11-10",
  monthlyRent: 273_500,
  deposit: 243_750,
  noticeDate: "2026-10-12",
  inspectionRequested: "2026-10-14",
  inspectionAt: "2026-11-02T10:00",
  vacateDate: "2026-11-16",
  statementSent: "2026-12-01",
  /** The date that selects the law in force: possession returned. */
  eventDate: "2026-11-16",
} as const;

/** One deduction line, as the line-level trees (deduct-repair, deduct-cleaning, the list gate...) read it. */
export interface DemoLine {
  id: string;
  /** The schedule's item key; matches the inspection list and the useful-life table. */
  item: string;
  description: string;
  purpose: "repair" | "cleaning" | "personalProperty" | "utility" | "lateFee" | "noticeFee" | "masterMeteredEnergy";
  involvesRepairOrCleaning: boolean;
  isProfessionalCleaning: boolean;
  performedBy: "inHouse" | "vendor";
  /** Reasonable cost of the work, before the tenant's share: invoice, or hours times rate plus materials. */
  cost: number;
  /** Age of the item when possession returned, for the schedule's useful-life share. */
  itemAgeMonths: number | null;
  /** What the line rests on; "nonrefundableTerm" is barred outright. */
  basis: "damage" | "soiling" | "lease" | "nonrefundableTerm";
  noticeType: string | null;
  owedUnderLease: boolean;
  isLiquidatedDamages: boolean;
  /** The amount billed, for lease charges (deduct-other-charge). */
  amount: number;
  usage: number | null;
  estimate: number | null;
  finalCost: number | null;
  completedOrDocumentedDate: string | null;
  /** Whether the provider's documents are in hand by a date. */
  providerDocumentsReceivedBy(date: string): boolean;
}

function line(l: Omit<DemoLine, "providerDocumentsReceivedBy"> & { documentsReceived: string | null }): DemoLine {
  const { documentsReceived, ...rest } = l;
  return { ...rest, providerDocumentsReceivedBy: (date: string) => documentsReceived !== null && documentsReceived <= date };
}

const common = {
  noticeType: null,
  owedUnderLease: true,
  isLiquidatedDamages: false,
  usage: null,
  estimate: null,
  finalCost: null,
} as const;

/** The four conditions found historically, with their planned work. */
export const DEMO_LINES = {
  closet: line({
    ...common,
    id: "closet",
    item: "closet-door",
    description: "Repair the bedroom closet: rebuild the sliding door track and rehang the door (vendor).",
    purpose: "repair",
    involvesRepairOrCleaning: true,
    isProfessionalCleaning: false,
    performedBy: "vendor",
    cost: 42_000,
    itemAgeMonths: 60,
    basis: "damage",
    amount: 21_000,
    completedOrDocumentedDate: "2026-11-24",
    documentsReceived: "2026-11-24",
  }),
  paint: line({
    ...common,
    id: "paint",
    item: "interior-paint",
    description: "Patch and repaint the living-room and bedroom walls (in-house, 6 hours at $55 plus $60 materials).",
    purpose: "repair",
    involvesRepairOrCleaning: true,
    isProfessionalCleaning: false,
    performedBy: "inHouse",
    cost: 39_000,
    itemAgeMonths: 12,
    basis: "damage",
    amount: 26_000,
    completedOrDocumentedDate: "2026-11-20",
    documentsReceived: "2026-11-20",
  }),
  carpet: line({
    ...common,
    id: "carpet",
    item: "carpet",
    description: "Hot-water extraction of the bedroom carpets (vendor).",
    purpose: "cleaning",
    involvesRepairOrCleaning: true,
    isProfessionalCleaning: true,
    performedBy: "vendor",
    cost: 18_500,
    itemAgeMonths: null,
    basis: "soiling",
    amount: 18_500,
    completedOrDocumentedDate: "2026-11-21",
    documentsReceived: "2026-11-21",
  }),
  cleaning: line({
    ...common,
    id: "cleaning",
    item: "general-cleaning",
    description: "Clean the kitchen and bathrooms (in-house, 3 hours at $45).",
    purpose: "cleaning",
    involvesRepairOrCleaning: true,
    isProfessionalCleaning: false,
    performedBy: "inHouse",
    cost: 13_500,
    itemAgeMonths: null,
    basis: "soiling",
    amount: 13_500,
    completedOrDocumentedDate: "2026-11-19",
    documentsReceived: "2026-11-19",
  }),
  /** A condition that was visible at the pre-move-out inspection but left off the list. */
  cabinet: line({
    ...common,
    id: "cabinet",
    item: "kitchen-cabinet-hinge",
    description: "Replace a broken kitchen cabinet hinge (in-house).",
    purpose: "repair",
    involvesRepairOrCleaning: true,
    isProfessionalCleaning: false,
    performedBy: "inHouse",
    cost: 6_500,
    itemAgeMonths: 60,
    basis: "damage",
    amount: 3_250,
    completedOrDocumentedDate: "2026-11-19",
    documentsReceived: "2026-11-19",
  }),
} satisfies Record<string, DemoLine>;

/** The company charge schedule: useful lives, and the holdover rate set as a standing instruction. */
export const DEMO_SCHEDULE = {
  usefulLifeMonths: { "closet-door": 120, "interior-paint": 36, carpet: 96, "kitchen-cabinet-hinge": 120 } as Record<string, number>,
  /** Monthly rent ÷ the days in the holdover month (November: 30). */
  holdoverDailyRate: DEMO.monthlyRent / daysInMonth(addDays(DEMO.leaseEnd, 1)),
  /** The tenant's share of an item's cost: the part of its useful life left. An item without a life is charged in full. */
  tenantShare(item: string, ageMonths: number | null): number {
    const life = this.usefulLifeMonths[item];
    if (life === undefined || ageMonths === null) return 1;
    return Math.max(0, (life - ageMonths) / life);
  },
};

// California holidays that move a deadline (CCP 135, Gov 6700), late 2026; a fixture, not the holiday law.
const HOLIDAYS = new Set(["2026-11-11", "2026-11-26", "2026-11-27", "2026-12-25", "2027-01-01"]);
const weekday = (d: string) => new Date(`${d}T12:00:00Z`).getUTCDay();
const extend = (skipSaturday: boolean) => (d: string) => {
  let x = d;
  while (HOLIDAYS.has(x) || weekday(x) === 0 || (skipSaturday && weekday(x) === 6)) x = addDays(x, 1);
  return x;
};

function addMonths(date: string, n: number): string {
  const [y, m, d] = date.split("-").map(Number) as [number, number, number];
  return new Date(Date.UTC(y, m - 1 + n, d)).toISOString().slice(0, 10);
}

/** Twelve monthly rent periods from the 11th, each paid electronically on its first day. */
function demoLedger() {
  const periods = Array.from({ length: 12 }, (_, i) => ({ start: addMonths(DEMO.leaseStart, i), rent: DEMO.monthlyRent }));
  const periodEnd = (i: number) => (periods[i + 1] ? addDays(periods[i + 1]!.start, -1) : DEMO.leaseEnd);
  const payments = [
    { kind: "security", amount: DEMO.deposit, method: "ach", date: "2025-11-03" },
    ...periods.map((p) => ({ kind: "rent", amount: p.rent, method: "ach", date: p.start, periodStart: p.start })),
  ];
  const accrued = (through: string) =>
    periods.reduce((sum, p, i) => {
      if (through < p.start) return sum;
      const end = periodEnd(i);
      if (through >= end) return sum + p.rent;
      return sum + Math.round((p.rent * (daysBetween(p.start, through) + 1)) / (daysBetween(p.start, end) + 1));
    }, 0);
  const paid = (through: string) => payments.filter((p) => p.kind === "rent" && p.date <= through).reduce((s, p) => s + p.amount, 0);
  return {
    payments: {
      list: payments,
      /** Whether any payment of these kinds arrived electronically. */
      anyElectronic(kinds: string[]) {
        return payments.some((p) => kinds.includes(p.kind) && ["ach", "card", "online"].includes(p.method));
      },
    },
    /** Rent accrued under the lease through a date, in cents. */
    rentDueThrough: (date: string) => accrued(date),
    /** Rent accrued through a date and not paid, in cents. */
    unpaidRentThrough: (date: string) => Math.max(0, accrued(date) - paid(date)),
    /** Whether rent was accepted for any day after `after` and through `through`. */
    rentAcceptedAfter: (_after: string, _through: string) => false,
    /** Rent the lease would have earned between two dates (abandonment only). */
    rentWouldHaveAccrued: (from: string, to: string) => Math.max(0, accrued(to) - accrued(from)),
  };
}

/** The facts of the demonstration case at about November 30, 2026, when the account is built. */
export function demoFacts(): Record<string, unknown> {
  const repairAndCleaning = [DEMO_LINES.closet, DEMO_LINES.paint, DEMO_LINES.carpet, DEMO_LINES.cleaning].map((l) => ({
    id: l.id,
    item: l.item,
    amount: l.amount,
  }));
  return {
    asOfDate: "2026-11-30",
    tenancy: {
      isDwelling: true,
      rightToOccupyStart: DEMO.leaseStart,
      endDate: DEMO.leaseEnd,
      period: "fixedTerm",
      terminationGround: null,
      terminatedForBreach: false,
      record: {
        lease: "Paper lease, Nov 11 2025 – Nov 10 2026, with a holdover clause (days after the end are rent at the contract daily rate).",
        notices: ["Tenant's written notice of leaving at lease end, Oct 12 2026."],
        messages: [],
        electronicRefusal: false,
      },
    },
    deposit: { amount: DEMO.deposit, imposedAtTenancyStart: true, isAdvanceRent: false, isScreeningFee: false },
    lease: {
      term: "fixed",
      startDate: DEMO.leaseStart,
      endDate: DEMO.leaseEnd,
      monthlyRent: DEMO.monthlyRent,
      isElectronicRecord: false,
      eAgreementClause: true,
      holdoverClause: { rentPayable: true, fixesRate: false, rate: "contract daily rate: monthly rent ÷ days in that month" },
      renewalClause: null,
      personalPropertyClause: {
        authorizesDeposit: true,
        covers: (item: string) => ["unit-key", "mailbox-key", "fob", "garage-remote"].includes(item),
      },
      agreedNoticeDays: null,
      continuationRemedy: null,
    },
    terminationNotice: {
      by: "tenant",
      inWriting: true,
      givenDate: DEMO.noticeDate,
      receivedDate: DEMO.noticeDate,
      terminationDate: DEMO.leaseEnd,
      method: "email",
    },
    moveOut: {
      vacateDate: DEMO.vacateDate,
      evidence: { keysReturnedAt: "2026-11-16T15:00", belongingsRemoved: true, note: "All keys and the fob returned at the office; unit empty at the move-out walk." },
      keysAndDevices: { issued: ["unit-key", "unit-key", "mailbox-key", "fob"], returned: ["unit-key", "unit-key", "mailbox-key", "fob"] },
    },
    landlord: { holdoverPermission: { given: false } },
    udAction: { filed: false },
    market: { rentalValue: { monthly: DEMO.monthlyRent, basis: "Current asking rent for comparable 3-bedroom units at the community." } },
    schedule: DEMO_SCHEDULE,
    ledger: demoLedger(),
    holidays: { civ10Extend: extend(false), ccp12aExtend: extend(true) },
    notices: { inspectionOffer: { sentAt: DEMO.noticeDate }, electronicRefund: { sentAt: DEMO.noticeDate } },
    inspection: {
      request: { made: true, madeAt: DEMO.inspectionRequested, withdrawn: false },
      scheduledAt: DEMO.inspectionAt,
      noticeWaiver: null,
      conductedAt: DEMO.inspectionAt,
      itemizedStatement: { handedOverAt: "2026-11-02T11:00", items: ["closet-door", "interior-paint", "carpet", "general-cleaning"] },
      notes: "Closet door off its track, track bent; scuffs and holes in living-room and bedroom walls; carpet stained in both bedrooms; kitchen needs cleaning. Kitchen cabinet hinge broken and visible. Rooms mostly cleared.",
      photos: ["inspection/closet-1.jpg", "inspection/walls-1.jpg", "inspection/carpet-1.jpg", "inspection/kitchen-1.jpg"],
    },
    observation: {
      moveIn: { "closet-door": "Door on track, slides freely.", "interior-paint": "Freshly painted.", carpet: "Clean, no stains.", "general-cleaning": "Unit cleaned before move-in." },
      preMoveOut: { "closet-door": "Door off its track; track bent.", "interior-paint": "Scuffs and about ten anchor holes.", carpet: "Two large stains.", "general-cleaning": "Grease on range hood." },
      moveOut: { "closet-door": "Door off its track; track bent at the left end.", "interior-paint": "Scuffs and anchor holes unpatched.", carpet: "Two large stains remain.", "general-cleaning": "Grease on range hood; bathroom soap scum." },
    },
    photos: {
      moveIn: ["move-in/closet.jpg", "move-in/walls.jpg", "move-in/carpet.jpg", "move-in/kitchen.jpg"],
      afterPossession: ["move-out/closet.jpg", "move-out/walls.jpg", "move-out/carpet.jpg", "move-out/kitchen.jpg"],
      afterWork: ["after-work/closet.jpg", "after-work/walls.jpg", "after-work/carpet.jpg", "after-work/kitchen.jpg"],
    },
    unit: {
      address: "Unit 214, Huntington Beach, CA",
      workHistory: [
        { item: "closet-door", event: "installed in the 2021 renovation", date: "2021-11-15" },
        { item: "interior-paint", event: "repainted before move-in", date: "2025-11-05" },
      ],
      housingCitation: null,
    },
    workPlan: {
      scope: { "closet-door": "repair track and rehang door", "interior-paint": "patch and repaint two rooms", carpet: "hot-water extraction", "general-cleaning": "kitchen and bathrooms" },
      schedule: { "closet-door": "2026-11-23", "interior-paint": "2026-11-19", carpet: "2026-11-21", "general-cleaning": "2026-11-18" },
      deductibleRepairOrCleaningPlanned: true,
      firstDeductibleWorkStart: "2026-11-18",
      deductibleWorkCompletedDate: "2026-11-24",
    },
    quotes: [
      { item: "closet-door", vendor: "Coastline Doors", amount: 42_000, option: "repair" },
      { item: "closet-door", vendor: "Coastline Doors", amount: 96_000, option: "rebuild" },
      { item: "carpet", vendor: "Surf City Carpet Care", amount: 18_500, option: "extraction" },
    ],
    statement: {
      sentDate: DEMO.statementSent,
      receivedDate: DEMO.statementSent,
      lines: { repairAndCleaning: repairAndCleaning },
      attachments: ["invoice-closet", "invoice-carpet", "work-order-paint", "work-order-cleaning", "photos-link", "water-2026-11-final"],
      includesEstimate: (_line: unknown) => false,
    },
    waiver: null,
    refundAgreement: {
      designatesOtherMethod: false,
      isWriting: true,
      designatedAccount: { kind: "bank", last4: "4321", designatedAt: DEMO.inspectionRequested, via: "tenant page" },
    },
    eAgreement: { separate: true, optional: true, primaryPurposeElectronic: true, agreedAt: DEMO.inspectionRequested, via: "tenant page" },
    record: { kind: "refund account designation", via: "tenant page", at: DEMO.inspectionRequested },
    statementAgreement: { email: { agreed: true, address: "tenant@example.com", separateOptional: true } },
    adultTenants: { residing: [{ id: "tenant-1" }], onLeaseAtTermination: [{ id: "tenant-1" }] },
    cotenantAgreement: null,
    dvTermination: null,
    tenant: { forwardingAddress: "1200 Main St, Apt 3, Long Beach, CA 90802" },
    water: {
      submetersRequiredByStandard: false,
      submetersUsedToBill: true,
      finalReadDate: "2026-11-18",
      previousMonthBill: { amount: 6_240, days: 30 },
      finalPeriod: { days: 23 },
      adminFeeCapAdjusted: 520,
      lastBill: {
        id: "water-2026-11-final",
        totalDue: 5_475,
        usage: 4_100,
        adminFee: 475,
        chargeTypes: ["usage", "fixedShare", "adminFee"],
        finalMonthBasis: "readingWithinFiveDays",
        includesLandlordPenalties: false,
      },
    },
    utility: { tariff: null },
    compliance: { subdivisionHFailures: [] },
    conduct: { knowledge: [], pattern: [] },
    account: { prohibitedRetentions: [], actualDamages: 0, provenDamages: 0 },
    abandonmentNotice: null,
    relet: { rentReceivedThrough: (_date: string) => 0 },
    mitigation: { provenAvoidableLoss: 0 },
  };
}

/** The case facts with one deduction line in place, for the line-level trees. */
export function demoFactsForLine(l: DemoLine, base: Facts = demoFacts()): Record<string, unknown> {
  return { ...base, line: l };
}

/**
 * Fixture answers to the semantic questions, as the judgment layer would give them on this case's
 * evidence. Keyed by leaf id, or "CA.tree#leaf-id" for one tree.
 */
export const DEMO_ANSWERS: Readonly<Record<string, Truth>> = {
  "tenant-vacated": true,
  "rate-within-rental-value": true,
  "mistake-of-fact": false,
  "rate-within-benefit": true,
  "actual-damage-impracticable": false,
  "caused-by-tenant": true,
  "not-preexisting": true,
  "cause-not-normal-use": true,
  "extent-beyond-wear": true,
  "not-cumulative-wear": true,
  "restores-not-improves": true,
  "cost-reasonable": true,
  "possessions-prevented-identification": false,
  "not-cured": true,
  "arose-after-inspection": false,
  "hidden-by-possessions": false,
  "less-clean-than-inception": true,
  "not-wear-soiling": true,
  "professional-cleaning-necessary": true,
  "agreement-from-conduct": false,
  "documentation-requested": true,
  "renewal-rebutted": true,
  "substandard-condition": false,
  "delay-without-good-cause": false,
  "not-tenant-caused": false,
  "waiver-text": false,
  "failure-in-bad-faith": false,
  "damages-proven-reasonable": true,
  "claim-in-bad-faith": false,
  "tenant-defaulted": false,
  "not-ordinary-wear": true,
  "breach-and-abandonment": false,
  "cannot-finish-by-day-21": false,
  "estimate-in-good-faith": true,
  "fixed-sum-valid": false,
};

export interface RecordedQuestion {
  treeId: string;
  leafId: string;
  inputs: Record<string, unknown>;
}

/**
 * An answer provider from a table, recording every question it is asked. A question with no entry is
 * answered "unknown".
 */
export function fixtureAnswers(table: Readonly<Record<string, Truth>> = DEMO_ANSWERS): AnswerProvider & { asked: RecordedQuestion[] } {
  const asked: RecordedQuestion[] = [];
  const provider = async (_leaf: Condition, _q: unknown, inputs: Record<string, unknown>, ctx: { treeId: string; leafId: string }): Promise<Answer> => {
    asked.push({ treeId: ctx.treeId, leafId: ctx.leafId, inputs });
    const value = table[`${ctx.treeId}#${ctx.leafId}`] ?? table[ctx.leafId];
    return value === undefined ? { value: "unknown", provider: "fixture", rationale: "no fixture answer" } : { value, provider: "fixture", confidence: 1 };
  };
  return Object.assign(provider, { asked });
}
