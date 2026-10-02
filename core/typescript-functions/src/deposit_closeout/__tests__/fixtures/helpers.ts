/** Test-only composition of constructed inputs and independently specified expectations. */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { from_wire } from "../../domain/codec.js";
import type { ReviewRuleRelease } from "../../domain/phase_b_types.js";
import { review_request } from "../../domain/review.js";
import type {
  AvailableAction, ItemDecision, RequirementResult, ReviewEnvelope,
  ReviewRequest, ReviewResult, TrackOutcome,
} from "../../domain/types.js";

export interface FixturePatch { op: string; path: string; value: unknown; }
export interface FixtureCase {
  id: string; name: string; extends: string | null; patches: FixturePatch[];
  expectedFields: { pointer: string; value: unknown }[];
}
export interface FixtureCorpus {
  origin: string; expectedOutcomeReviewStatus: string;
  cases: FixtureCase[];
}

export const OUTPUT_FIELDS: (keyof ReviewResult)[] = [
  "scopeRequirements", "itemDecisions", "account", "missingInputs", "actions", "outcomes",
];

export function readFixtureText(name: string): string {
  return readFileSync(fileURLToPath(new URL(name, import.meta.url)), "utf8");
}
export function readFixture(name: string): unknown { return JSON.parse(readFixtureText(name)); }
export function readResource(name: string): unknown {
  return JSON.parse(readFileSync(fileURLToPath(new URL(`../../resources/${name}`, import.meta.url)), "utf8"));
}
export function fixtureCorpus(): FixtureCorpus { return readFixture("cases.json") as FixtureCorpus; }
export function baseRequest(): ReviewRequest { return readFixture("base_request.json") as ReviewRequest; }
export function loadReviewRelease(): ReviewRuleRelease {
  return from_wire("ReviewRuleRelease", readResource("rules/nc_synthetic_review_v1.json"));
}
/** Require a fixture position without weakening noUncheckedIndexedAccess. */
export function requireElement<T>(array: readonly T[], index: number): T {
  const element = array[index];
  if (element === undefined) throw new Error(`Missing fixture element at index ${index}`);
  return element;
}
export function asRecord(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) throw new Error("Expected test object");
  return value as Record<string, unknown>;
}
export function atPointer(document: unknown, pointer: string): unknown {
  return pointer.split("/").slice(1).reduce<unknown>((current: unknown, encoded: string): unknown => {
    const key = encoded.replace(/~1/g, "/").replace(/~0/g, "~");
    return Array.isArray(current) ? current[Number(key)] : asRecord(current)[key];
  }, document);
}
export function applyFixturePatch(document: unknown, patch: FixturePatch): void {
  const parts = patch.path.split("/").slice(1).map((part: string): string => part.replace(/~1/g, "/").replace(/~0/g, "~"));
  const key = parts.pop();
  if (key === undefined) throw new Error("Fixture patch must address a field");
  const target = parts.reduce<unknown>((current: unknown, part: string): unknown =>
    Array.isArray(current) ? current[Number(part)] : asRecord(current)[part], document);
  const value: unknown = structuredClone(patch.value);
  if (patch.op === "add" && Array.isArray(target) && key === "-") { target.push(value); return; }
  if (patch.op !== "replace") throw new Error("Unsupported fixture patch; never silently ignore");
  if (Array.isArray(target)) {
    if (!Number.isInteger(Number(key)) || Number(key) < 0 || Number(key) >= target.length) throw new Error("Missing array position");
    target[Number(key)] = value;
  } else {
    const record = asRecord(target);
    if (!Object.hasOwn(record, key)) throw new Error("Fixture replace must target an existing field");
    record[key] = value;
  }
}
export function materializeCases(): Map<string, ReviewRequest> {
  const byId = new Map(fixtureCorpus().cases.map((entry: FixtureCase): [string, FixtureCase] => [entry.id, entry]));
  const cache = new Map<string, ReviewRequest>();
  function resolve(id: string, trail: string[]): ReviewRequest {
    if (trail.includes(id)) throw new Error("Fixture inheritance cycle");
    const cached = cache.get(id);
    if (cached !== undefined) return structuredClone(cached);
    const entry = byId.get(id);
    if (entry === undefined) throw new Error(`Unknown fixture case ${id}`);
    const document = entry.extends === null ? baseRequest() : resolve(entry.extends, [...trail, id]);
    entry.patches.forEach((patch: FixturePatch): void => applyFixturePatch(document, patch));
    cache.set(id, document);
    return structuredClone(document);
  }
  return new Map([...byId.keys()].map((id: string): [string, ReviewRequest] => [id, resolve(id, [])]));
}
export function caseRequest(id: string = "NC-A-002"): ReviewRequest {
  const request = materializeCases().get(id);
  if (request === undefined) throw new Error(`Unknown case ${id}`);
  return request;
}
export function resultFor(raw: ReviewRequest): ReviewEnvelope {
  const release = loadReviewRelease();
  const supplied = structuredClone(raw);
  supplied.ruleReleaseId = release.ruleReleaseId;
  return review_request(from_wire("ReviewRequest", supplied), release);
}
export function action(result: ReviewResult, key: string): AvailableAction {
  const found = result.actions.find((value: AvailableAction): boolean => value.actionKey === key);
  if (found === undefined) throw new Error(`Missing action ${key}`);
  return found;
}
export function item(result: ReviewResult, key: string = "repair-250"): ItemDecision {
  const found = result.itemDecisions.find((value: ItemDecision): boolean => value.itemId === key);
  if (found === undefined) throw new Error(`Missing item ${key}`);
  return found;
}
export function requirement(result: ReviewResult, key: string): RequirementResult {
  const found = result.scopeRequirements.requirements.find((value: RequirementResult): boolean => value.requirementKey === key);
  if (found === undefined) throw new Error(`Missing requirement ${key}`);
  return found;
}
export function track(result: ReviewResult, key: string): TrackOutcome {
  const found = result.outcomes.tracks.find((value: TrackOutcome): boolean => value.track === key);
  if (found === undefined) throw new Error(`Missing track ${key}`);
  return found;
}
export function questionIds(result: ReviewResult): string[] { return result.missingInputs.map((value): string => value.questionId); }
