# Binding a case to the trees

October 3, 2026 (coordinator). Notes for the service code that turns Handoff's records into the facts the trees read. They settle the open points from the evaluator build (A5).

## Settled
- **Electronic refund destination.** `CA.refund-electronic` makes an electronic refund a duty whenever the tenant paid electronically. The "designated in writing" part of 1950.5(h)(1)(A)(ii)(I) governs where the money may go, not whether the duty applies. So the refund action in the gateway checks it: an `electronic_transfer` refund needs a destination the tenant designated in a writing, and an electronic designation counts only if `CA.electronic-writing` holds (Owen's ruling, October 3). No tree change.
- **Holdover rate.** The schedule's daily rate is monthly rent ÷ days in that month (Owen, October 3). A holdover that crosses a month end needs each day at its own month's rate. When the binding is built, change `CA.holdover-charge`'s amount to a schedule method over the holdover dates, summed and rounded once to whole cents. The demonstration's six November days give 54700 either way.
- **`ledger.rentDueThrough(date)`** is rent accrued through the date. `unpaidRentThrough(date)` is accrued less paid.
- **Accepted evaluator choices:**
  - `null` inputs satisfy the evidence contract, because a known absence is itself evidence;
  - `amount()` of an effect that does not apply is absent;
  - a cross-tree effect formula is skipped when its effect does not apply;
  - one event date per evaluation;
  - `in` with a list on the left is a subset test.

## Rules for the binding
- **Unknown versus absent.** Use `undefined` for something that exists but is not known yet, such as the vacate date while the tenant is still in possession. Use `null` only for something known to be absent.
- **Zero is `0`.** Give zero amounts as `0`, never `null`; `null` turns the arithmetic absent.
- **Holiday functions.** Supply `holidays.civ10Extend(date)` and `holidays.ccp12aExtend(date)` from Gov 6700 and CCP 135, which are saved in the research texts.
- **Exact strings.** The string values must match the trees exactly: `lease.term` "fixed", `tenancy.period` "month", `line.performedBy` "inHouse", `tenancy.terminationGround` "CCP 1161(2)" and the others, `terminationNotice.method` and `water.lastBill.finalMonthBasis`. See `src/demo/index.ts` for the full shape.
- **Which trees run.** The service decides which trees run for each statement line. For example, `CA.deduct-other-charge` has no purpose gate of its own.
- **What the judgment layer receives.** Semantic questions receive raw fact objects as inputs, so the judgment layer must render them into the text or images a provider reads.
- **What a tree reads.** `requiredFacts(tree)` lists the fact paths each tree reads, including the method calls the binding must implement.
