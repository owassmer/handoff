import { describe, expect, it } from "vitest";
import { exampleWorkspace } from "./examples.test-support";
import {
  agentLabel,
  conditionLines,
  conversationThread,
  groupFindings,
  reportConditions,
  tone,
} from "./view";

describe("plain wording in the unit page", () => {
  it("keeps Handoff's reply to each message once a decision is no longer pending", () => {
    const data = exampleWorkspace();
    data.messages = [
      {
        ...data.messages[0]!,
        id: "m1",
        direction: "Operator",
        body: "Please go ahead with the accepted work.",
        createdAt: "2026-09-27T18:43:46Z",
      },
      {
        ...data.messages[0]!,
        id: "m2",
        direction: "Operator",
        body: "Any update on the floors?",
        createdAt: "2026-09-27T19:10:00Z",
      },
    ];
    data.activity = [
      {
        id: "a0",
        title: "Message received",
        detail: "Please go ahead",
        at: "2026-09-27T18:43:47Z",
      },
      {
        id: "a1",
        title: "Handoff progressed",
        detail: "Ordered Restoration assessment from Feld Architecture for $1,200.00.",
        at: "2026-09-27T18:43:53Z",
      },
      {
        id: "a2",
        title: "Handoff progressed",
        detail: "Ordered Stair and railing repair from Carroll Stair & Millwork for $1,500.00.",
        at: "2026-09-27T18:44:24Z",
      },
    ];
    data.workPlan = { ...data.workPlan!, status: "Accepted", acceptedDecisionId: "decision" };
    expect(conversationThread(data).map((entry) => [entry.who, entry.body])).toEqual([
      ["You", "Please go ahead with the accepted work."],
      ["Handoff", "Ordered Restoration assessment from Feld Architecture for $1,200.00."],
      ["You", "Any update on the floors?"],
    ]);
  });
  it("names Handoff's state in plain words and marks what needs the operator", () => {
    expect(agentLabel("Ready to continue")).toBe("Working");
    expect(agentLabel("Waiting for provider")).toBe("Waiting on vendors");
    expect(agentLabel("Needs attention")).toBe("Needs your attention");
    expect(tone(agentLabel("Needs attention"))).toBe("attention");
    expect(agentLabel("Something new")).toBe("Something new");
  });
  it("splits a report into one condition per line and shows shared observations once", () => {
    const observation =
      "Parquet floors scratched: needs work\nUrine odor in the great room: not checked";
    expect(conditionLines(observation)).toEqual([
      { text: "Parquet floors scratched", result: "needs work" },
      { text: "Urine odor in the great room", result: "not checked" },
    ]);
    expect(conditionLines("Concealed pipework not examined")).toEqual([
      { text: "Concealed pipework not examined", result: null },
    ]);
    const groups = groupFindings([
      { lineId: "site", observation },
      { lineId: "schedule", observation },
      { lineId: "railing", observation: "Loft railing: satisfactory" },
    ]);
    expect(groups.map((g) => g.findings.map((f) => f.lineId))).toEqual([
      ["site", "schedule"],
      ["railing"],
    ]);
    expect([tone("needs work"), tone("satisfactory"), tone("not checked")]).toEqual([
      "problem",
      "done",
      "waiting",
    ]);
  });
  it("counts a report by its conditions, each once, not by its deliverable lines", () => {
    const schedule =
      "Floors scratched: needs work\nRailing loose: needs work\nBath chipped: satisfactory";
    const conditions = reportConditions([
      { result: "Satisfied", observation: schedule },
      { result: "Satisfied", observation: schedule },
      { result: "Satisfied", observation: schedule },
      { result: "Not checked", observation: "Concealed pipework not examined" },
    ]);
    expect(conditions).toHaveLength(4);
    expect(conditions.filter((c) => c.result === "needs work")).toHaveLength(2);
    expect(conditions.find((c) => c.text === "Concealed pipework not examined")?.result).toBe(
      "not checked",
    );
  });
});
