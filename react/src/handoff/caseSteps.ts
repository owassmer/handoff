import type { HandoffWorkspace, StepResult } from "./contracts";
import { awaitsDecision } from "./view";

export type StopReason =
  "decision" | "attention" | "ready" | "unchanged" | "limit" | "stopped" | "refused" | "stepped";
export interface StepRecord {
  n: number;
  at: number;
  ms: number;
  outcome: "changed" | "unchanged" | "refused";
  detail: string;
  caseDate: string;
  status: string;
}
export interface RunOptions {
  step(): Promise<StepResult>;
  read(): Promise<HandoffWorkspace>;
  onStep(record: StepRecord): void;
  /** Checked before each call; Stop sets it. */
  stopped(): boolean;
  sleep(ms: number): Promise<void>;
  now(): number;
  once?: boolean;
  max?: number;
}
export const MAX_STEPS = 60;
const RETRY_MS = 2000;
const MAX_REFUSALS = 3;
/** A wake further out than this is a real wait (a vendor reply on the case clock), not the next step. */
const NEAR_WAKE_MS = 120_000;

/** What a step changes: the case revision, Handoff's saved state, the plan and the records it writes. */
export function fingerprint(data: HandoffWorkspace): string {
  return JSON.stringify([
    data.handoff.revision,
    data.agent.status,
    data.agent.updatedAt,
    data.workPlan?.revision ?? null,
    data.workPlan?.status ?? null,
    data.messages.length,
    data.activity.length,
    data.jobs.map((j) => j.status),
    data.payments.map((p) => p.status),
  ]);
}
/** The points where Handoff needs the operator, or has nothing left to do. */
export function stopFor(data: HandoffWorkspace): StopReason | undefined {
  if (awaitsDecision(data.handoff.physicalProgress)) {
    return "decision";
  }
  if (data.agent.status === "Needs attention") {
    return "attention";
  }
  if (data.handoff.physicalProgress === "Ready") {
    return "ready";
  }
  return undefined;
}

/** Resume handoff one call at a time, each as soon as the last one finishes. */
export async function runSteps(
  options: RunOptions,
): Promise<{ reason: StopReason; detail?: string }> {
  const max = options.once ? 1 : (options.max ?? MAX_STEPS);
  let before = await options.read();
  let steps = 0,
    refusals = 0;
  const record = (
    outcome: StepRecord["outcome"],
    at: number,
    ms: number,
    data: HandoffWorkspace,
    detail: string,
  ) =>
    options.onStep({
      n: steps,
      at,
      ms,
      outcome,
      detail,
      caseDate: data.handoff.businessDate ?? "",
      status: data.agent.status,
    });
  while (steps < max) {
    if (options.stopped()) {
      return { reason: "stopped" };
    }
    if (!options.once) {
      const stop = stopFor(before);
      if (stop) {
        return { reason: stop };
      }
    }
    const at = options.now();
    const result = await options.step();
    const ms = options.now() - at;
    if (result.kind === "refused") {
      refusals += 1;
      record("refused", at, ms, before, result.message);
      if (refusals >= MAX_REFUSALS) {
        return { reason: "refused", detail: result.message };
      }
      // Usually an automation ran the same step first; the next call sees its result.
      await options.sleep(RETRY_MS);
      before = await options.read();
      continue;
    }
    refusals = 0;
    steps += 1;
    const after = await options.read();
    const changed = fingerprint(after) !== fingerprint(before);
    record(changed ? "changed" : "unchanged", at, ms, after, after.agent.nextStep);
    if (options.once) {
      return { reason: "stepped" };
    }
    if (!changed) {
      const wake = after.agent.nextWakeAt
        ? Date.parse(after.agent.nextWakeAt) - options.now()
        : NaN;
      if (!(wake > 0 && wake <= NEAR_WAKE_MS)) {
        return { reason: "unchanged" };
      }
      await options.sleep(wake + 1000);
    }
    before = after;
  }
  return { reason: "limit" };
}
