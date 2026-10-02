import { describe, expect, it } from "vitest";
import { type HandoffWorkspace, readWorkspace } from "./contracts";
import { workExample } from "./work.test-support";

const read = (data: unknown) => readWorkspace(JSON.stringify(data), "office", "garden-home");
describe("Work read contract", () => {
  it("reads delivery facts and the exact earlier assessment, not a copy of the repair proposal", () => {
    const data = read(workExample());
    expect(data.decisions[0].content.scope).toEqual(["Inspect the wall and handle"]);
    expect(data.workPlan?.selections).toHaveLength(2);
    expect(data.handoff.operativeDecisionId).toBe(data.decisions[0].id);
    expect(data.jobs[0].decisionId).toBe(data.decisions[0].id);
    expect(data.payments[0].status).toBe("Uncertain");
  });
  it.each(["Occupant departure", "To confirm", "Tenancy ending"])(
    "allows an unknown end date for %s",
    (endingKind) => {
      const data = workExample();
      data.tenancy = { ...data.tenancy, endingKind, endDate: null };
      expect(read(data).tenancy.endDate).toBeNull();
    },
  );
  it("does not replace missing costs with zero or require an invented acceptance for existing work", () => {
    const data = workExample();
    Object.assign(data.jobs[0], {
      committedCents: null,
      decisionId: null,
      workPlanId: null,
      origin: "External",
    });
    expect(read(data).jobs[0].committedCents).toBeNull();
  });
  const invalid: Array<[string, (data: HandoffWorkspace) => void]> = [
    ["old read version", (d) => Reflect.set(d, "version", "1")],
    ["missing delivery", (d) => Reflect.deleteProperty(d, "jobs")],
    ["numeric cost", (d) => Reflect.set(d.quotes[0], "totalCents", 87500)],
    ["missing cost", (d) => Reflect.deleteProperty(d.invoices[0], "totalCents")],
    ["partial selection", (d) => Reflect.deleteProperty(d.workPlan!.selections[0], "reason")],
    [
      "invented end",
      (d) => {
        d.tenancy.endingKind = "Occupant departure";
      },
    ],
    [
      "duplicate job",
      (d) => {
        d.jobs.push(d.jobs[0]);
      },
    ],
    [
      "invalid finding",
      (d) => Reflect.set(d.inspections[0].findings[0], "result", "Probably fine"),
    ],
    ["missing accepted content", (d) => Reflect.deleteProperty(d.decisions[0], "content")],
    [
      "crossed acceptance",
      (d) => {
        d.decisions[0].content.id = d.workPlan!.id;
      },
    ],
    [
      "changed acceptance budget",
      (d) => {
        d.decisions[0].content.budgetCents = "10001";
      },
    ],
    [
      "missing operative decision",
      (d) => {
        d.handoff.operativeDecisionId = "missing";
      },
    ],
    [
      "unbounded collection",
      (d) => {
        d.activity = Array.from({ length: 101 }, (_, i) => ({
          id: String(i),
          title: "Work",
          detail: "Details",
          at: "2026-09-22",
        }));
      },
    ],
    [
      "bad page range",
      (d) => {
        d.documents[0].pageStart = 4;
        d.documents[0].pageEnd = 2;
      },
    ],
    [
      "incomplete original reference",
      (d) => {
        d.documents[0].mediaSetRid = "set";
      },
    ],
  ];
  it.each(invalid)("rejects %s", (_name, mutate) => {
    const data = workExample();
    mutate(data);
    expect(() => read(data)).toThrow();
  });
});
