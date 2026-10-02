import { describe, expect, it, vi } from "vitest";
import { type StepRecord, runSteps } from "./caseSteps";
import type { HandoffWorkspace, StepResult } from "./contracts";
import { exampleWorkspace } from "./examples.test-support";

/** A case whose revision moves on every successful step, with scripted states after chosen steps. */
function harness(
  results: StepResult[] = [],
  after: Record<number, (d: HandoffWorkspace) => void> = {},
) {
  const data = exampleWorkspace();
  data.handoff.physicalProgress = "Arranging work";
  data.agent.status = "Ready to continue";
  let calls = 0,
    steps = 0;
  const log: StepRecord[] = [];
  const sleep = vi.fn(async () => {});
  let stop = false;
  const options = {
    step: vi.fn(async (): Promise<StepResult> => {
      const result = results[calls++] ?? { kind: "done" };
      if (result.kind === "done") {
        steps += 1;
        data.handoff.revision = String(Number(data.handoff.revision) + 1);
        after[steps]?.(data);
      }
      return result;
    }),
    read: vi.fn(async () => structuredClone(data)),
    onStep: (record: StepRecord) => log.push(record),
    stopped: () => stop,
    sleep,
    now: () => Date.parse("2026-09-28T05:00:00Z"),
  };
  return { data, options, log, sleep, stopNow: () => (stop = true) };
}

describe("running steps", () => {
  it("takes one step for Next step, even when a plan is waiting", async () => {
    const { options, log } = harness([], {});
    const d = await options.read();
    d.handoff.physicalProgress = "Plan ready";
    expect(await runSteps({ ...options, once: true })).toEqual({ reason: "stepped" });
    expect(options.step).toHaveBeenCalledTimes(1);
    expect(log.map((r) => r.outcome)).toEqual(["changed"]);
  });
  it("runs until a plan is ready for a decision", async () => {
    const { options } = harness([], {
      3: (d) => {
        d.handoff.physicalProgress = "Plan ready";
      },
    });
    expect(await runSteps(options)).toEqual({ reason: "decision" });
    expect(options.step).toHaveBeenCalledTimes(3);
  });
  it("stops when Handoff needs attention or the unit is ready", async () => {
    const attention = harness([], { 2: (d) => (d.agent.status = "Needs attention") });
    expect((await runSteps(attention.options)).reason).toBe("attention");
    const ready = harness([], { 1: (d) => (d.handoff.physicalProgress = "Ready") });
    expect((await runSteps(ready.options)).reason).toBe("ready");
  });
  it("stops when a step changes nothing and no wake is near", async () => {
    const { options, data } = harness();
    options.step.mockImplementation(async () => ({ kind: "done" }));
    data.agent.nextWakeAt = null;
    expect(await runSteps(options)).toEqual({ reason: "unchanged" });
    expect(options.step).toHaveBeenCalledTimes(1);
  });
  it("waits for a wake due within two minutes, then carries on", async () => {
    const { options, data, sleep } = harness();
    let calls = 0;
    options.step.mockImplementation(async () => {
      calls += 1;
      if (calls === 2) {
        data.handoff.physicalProgress = "Plan ready";
      }
      if (calls >= 2) {
        data.handoff.revision = String(Number(data.handoff.revision) + 1);
      }
      return { kind: "done" };
    });
    data.agent.nextWakeAt = "2026-09-28T05:00:30Z";
    expect(await runSteps(options)).toEqual({ reason: "decision" });
    expect(sleep).toHaveBeenCalledWith(31_000);
  });
  it("waits 2 seconds after a refused call and carries on", async () => {
    const { options, sleep, log } = harness(
      [{ kind: "refused", message: "The handoff changed." }, { kind: "done" }],
      { 1: (d) => (d.handoff.physicalProgress = "Plan ready") },
    );
    expect(await runSteps(options)).toEqual({ reason: "decision" });
    expect(sleep).toHaveBeenCalledWith(2000);
    expect(log.map((r) => r.outcome)).toEqual(["refused", "changed"]);
  });
  it("gives up after three refusals in a row", async () => {
    const refused: StepResult = { kind: "refused", message: "Not now." };
    const { options } = harness([refused, refused, refused]);
    expect(await runSteps(options)).toEqual({ reason: "refused", detail: "Not now." });
    expect(options.step).toHaveBeenCalledTimes(3);
  });
  it("stops at the step limit and when Stop is pressed", async () => {
    const limited = harness();
    expect(await runSteps({ ...limited.options, max: 5 })).toEqual({ reason: "limit" });
    expect(limited.options.step).toHaveBeenCalledTimes(5);
    const stopped = harness();
    stopped.options.step.mockImplementation(async () => {
      stopped.stopNow();
      stopped.data.handoff.revision = String(Number(stopped.data.handoff.revision) + 1);
      return { kind: "done" };
    });
    expect(await runSteps(stopped.options)).toEqual({ reason: "stopped" });
    expect(stopped.options.step).toHaveBeenCalledTimes(1);
  });
});
