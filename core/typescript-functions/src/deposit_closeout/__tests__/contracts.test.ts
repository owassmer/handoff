/** Structural contract tests; passing these is not legal or Foundry runtime validation.
 * Raw JSON numeric-token rejection is covered by the public adapter's boundary tests.
 */
import { describe, expect, it } from "vitest";
import { ContractError, canonical_json, from_wire, json_schema, to_wire } from "../domain/codec.js";
import { MAX_SAFE_INTEGER, VOCABULARY } from "../domain/vocabulary.js";
import { review_request } from "../domain/review.js";
import {
  OUTPUT_FIELDS, applyFixturePatch, asRecord, atPointer,
  baseRequest, caseRequest, fixtureCorpus, loadReviewRelease, materializeCases,
  readFixture, readResource, requireElement, resultFor,
} from "./fixtures/helpers.js";

describe("constructed fixture integrity", (): void => {
  it("uses distinct case IDs, pending review labels and unexecuted lifecycle expectations", (): void => {
    const corpus = fixtureCorpus(); const lifecycle = asRecord(readFixture("lifecycle_expectations.json"));
    expect(corpus.origin).toBe("CONSTRUCTED");
    expect(corpus.expectedOutcomeReviewStatus).toContain("PENDING");
    expect(new Set(corpus.cases.map((entry): string => entry.id)).size).toBe(corpus.cases.length);
    expect(lifecycle.evaluationStatus).toBe("NOT_RUN_ACTIONS_NOT_IMPLEMENTED");
    const steps = lifecycle.steps;
    if (!Array.isArray(steps)) throw new Error("Missing lifecycle steps");
    expect(new Set(steps.map((step: unknown): unknown => asRecord(step).id)).size).toBe(steps.length);
  });
  it("specifies ordinary deductions and refund independently of the engine", (): void => {
    const ordinary = fixtureCorpus().cases.find((entry): boolean => entry.id === "NC-A-002");
    if (ordinary === undefined) throw new Error("Missing ordinary fixture");
    const expected = new Map(ordinary.expectedFields.map((entry): [string, unknown] => [entry.pointer, entry.value]));
    expect(expected.get("/account/totalDeductionsCents")).toBe(40000);
    expect(expected.get("/account/finalRefundCents")).toBe(160000);
    expect(expected.get("/outcomes/depositComplete")).toBe(false);
  });
  it("clock variant changes exactly one input", (): void => {
    const before = caseRequest(); const after = caseRequest("NC-A-009");
    expect(after.snapshot).toEqual(before.snapshot);
    expect(after.ruleReleaseId).toBe(before.ruleReleaseId);
    expect(after.reviewClock).not.toBe(before.reviewClock);
  });
  it("fixture patch composition fails loudly rather than inventing keys", (): void => {
    expect((): void => applyFixturePatch({}, { op: "replace", path: "/absent", value: 1 })).toThrow();
    expect((): void => applyFixturePatch({}, { op: "remove", path: "/absent", value: null })).toThrow();
  });
});

describe("strict structural codecs and schema", (): void => {
  it("keeps exactly six review outputs", (): void => {
    expect(Object.keys(resultFor(caseRequest()).result)).toEqual(OUTPUT_FIELDS);
  });
  it("round-trips every one of the nine constructed fixtures", (): void => {
    const cases = materializeCases(); expect(cases.size).toBe(9);
    cases.forEach((raw, id): void => {
      const parsed = from_wire("ReviewRequest", raw);
      expect(to_wire(parsed), id).toEqual(raw);
      expect(canonical_json(parsed)).toBe(canonical_json(from_wire("ReviewRequest", raw)));
    });
  });
  it.each([
    ["review-request.schema.json", "ReviewRequest"], ["review-envelope.schema.json", "ReviewEnvelope"],
    ["phase-a-safety.schema.json", "SafetyProfile"], ["synthetic-rule-manifest.schema.json", "SyntheticRuleManifest"],
    ["phase-b-safety.schema.json", "PhaseBSafetyProfile"], ["phase-b-rule-release.schema.json", "ReviewRuleRelease"],
  ] as const)("committed %s matches codec contract", (filename, root): void => {
    expect(json_schema(root)).toEqual(readResource(`schemas/${filename}`));
  });
  it("money schema fields explicitly retain numeric safe-integer Long semantics", (): void => {
    let count = 0;
    ["ReviewRequest", "ReviewEnvelope"].forEach((root): void => {
      const definitions = asRecord(asRecord(json_schema(root as "ReviewRequest" | "ReviewEnvelope")).$defs);
      Object.values(definitions).forEach((definition: unknown): void => {
        const properties = asRecord(asRecord(definition).properties);
        Object.entries(properties).filter(([name]): boolean => name.endsWith("Cents")).forEach(([, value]): void => {
          const schema = asRecord(value);
          const alternatives = schema.anyOf;
          const numeric = Array.isArray(alternatives) ? asRecord(requireElement<unknown>(alternatives, 0)) : schema;
          expect(numeric.type).toBe("integer");
          expect(numeric["x-foundry-type"]).toBe("Long");
          expect(numeric.maximum).toBe(MAX_SAFE_INTEGER);
          count += 1;
        });
      });
    });
    expect(count).toBeGreaterThan(15);
  });
  it.each([true, 0.25, "200000", MAX_SAFE_INTEGER + 1, -1, Number.NaN, Number.POSITIVE_INFINITY])("rejects nonrepresentable cents: %s", (bad): void => {
    const raw = baseRequest(); applyFixturePatch(raw, { op: "replace", path: "/snapshot/depositBalance/amountCents", value: bad });
    expect((): unknown => from_wire("ReviewRequest", raw)).toThrow(ContractError);
  });
  it.each([0, null])("preserves money %s without conflating zero and null", (value): void => {
    const raw = baseRequest(); raw.snapshot.depositBalance.amountCents = value;
    expect(atPointer(to_wire(from_wire("ReviewRequest", raw)), "/snapshot/depositBalance/amountCents")).toBe(value);
  });
  it("rejects unknown fields", (): void => {
    const raw = baseRequest(); asRecord(raw.snapshot).complete = true;
    expect((): unknown => from_wire("ReviewRequest", raw)).toThrow(ContractError);
  });
  it("rejects omitted nullable fields", (): void => {
    const raw = baseRequest(); delete asRecord(requireElement(raw.snapshot.charges, 2)).chosenAmountCents;
    expect((): unknown => from_wire("ReviewRequest", raw)).toThrow(ContractError);
  });
  it("rejects unknown scalar states", (): void => {
    const raw = baseRequest(); requireElement(raw.snapshot.charges, 0).allowabilityState = "OWNER_SAYS_YES";
    expect((): unknown => from_wire("ReviewRequest", raw)).toThrow(ContractError);
  });
  it("rejects unknown roles in arrays", (): void => {
    const raw = baseRequest(); requireElement(raw.snapshot.parties, 0).roles = ["SUPERUSER"];
    expect((): unknown => from_wire("ReviewRequest", raw)).toThrow(ContractError);
  });
  it.each(["2026-09-16", "2026-09-16T12:00:00", "2026-13-16T12:00:00Z", "2026-09-16T12:00:00+00:00"])("rejects invalid or non-Z UTC timestamp %s", (bad): void => {
    const raw = baseRequest(); raw.reviewClock = bad;
    expect((): unknown => from_wire("ReviewRequest", raw)).toThrow(ContractError);
  });
  it("rejects invalid calendar dates", (): void => {
    const raw = baseRequest(); requireElement(raw.snapshot.dates, 0).value = "2026-02-30";
    expect((): unknown => from_wire("ReviewRequest", raw)).toThrow(ContractError);
  });
  it.each([
    ["2026-09-16T12:00:00.1Z", "2026-09-16T12:00:00.100000Z"],
    ["2026-09-16T12:00:00.123456Z", "2026-09-16T12:00:00.123456Z"],
    ["2026-09-16T12:00:00.000000Z", "2026-09-16T12:00:00Z"],
  ])("normalizes timestamps without losing microsecond precision: %s", (instant, expected): void => {
    const raw = baseRequest(); raw.reviewClock = instant;
    expect(atPointer(to_wire(from_wire("ReviewRequest", raw)), "/reviewClock")).toBe(expected);
  });
  it("canonical JSON sorts Unicode keys by code point and preserves text", (): void => {
    expect(canonical_json({ "😀": "astral", "\ue000": "bmp", z: 1, "é": "line\n", a: "quote\"" })).toBe('{"a":"quote\\\"","z":1,"é":"line\\n","\ue000":"bmp","😀":"astral"}');
  });
  it("source dates remain distinct; unknown trigger remains null", (): void => {
    const dates = from_wire("ReviewRequest", baseRequest()).snapshot.dates;
    expect(new Set(dates.map((entry): string => entry.factKey)).size).toBe(7);
    expect(new Set(dates.map((entry): string | null => entry.value)).size).toBeGreaterThan(2);
    const unknown = requireElement(from_wire("ReviewRequest", caseRequest("NC-A-003")).snapshot.dates, 6);
    expect(unknown.state).toBe("UNCONFIRMED"); expect(unknown.value).toBeNull();
  });
  it("currency is explicitly USD", (): void => {
    const raw = baseRequest(); raw.snapshot.currency = "EUR";
    expect((): unknown => from_wire("ReviewRequest", raw)).toThrow(ContractError);
  });
  it("all fixture evidence, party and open-question references resolve", (): void => {
    materializeCases().forEach((raw): void => {
      const s = from_wire("ReviewRequest", raw).snapshot;
      const evidence = new Set(s.evidence.map((entry): string => entry.evidenceId));
      const parties = new Set(s.parties.map((entry): string => entry.partyId));
      const questions = new Set(s.questions.map((entry): string => entry.questionId));
      const references = [...s.agreementEvidenceIds, ...s.interimConditionEvidenceIds, ...s.recipients.evidenceIds, s.depositBalance.sourceEvidenceId,
        ...[...s.charges, ...s.parties, ...s.dates, ...s.authorityGrants].flatMap((entry): string[] => entry.evidenceIds)];
      expect(references.every((id): boolean => evidence.has(id))).toBe(true);
      expect([...s.recipients.statementPartyIds, ...s.recipients.refundPartyIds].every((id): boolean => parties.has(id))).toBe(true);
      s.charges.forEach((charge): void => {
        expect(charge.unresolvedQuestionIds.every((id): boolean => questions.has(id))).toBe(true);
        if (charge.costVersionId !== null) expect(evidence.has(charge.costVersionId)).toBe(true);
      });
      expect(s.authorityGrants.every((grant): boolean => parties.has(grant.partyId))).toBe(true);
    });
  });
});

describe("synthetic-only safety contracts", (): void => {
  it.each(["allowOntologyWrites", "allowExternalEffects", "allowModelAssistance", "allowRuleActivation"])("profiles cannot enable %s", (key): void => {
    const phaseA = asRecord(readResource("safety_profile.json"));
    const phaseB = asRecord(readResource("phase_b_safety_profile.json"));
    expect((): unknown => from_wire("SafetyProfile", { ...phaseA, [key]: true })).toThrow(ContractError);
    expect((): unknown => from_wire("PhaseBSafetyProfile", { ...phaseB, [key]: true })).toThrow(ContractError);
  });
  it("manifest remains nonexecutable and unreviewed", (): void => {
    const manifest = from_wire("SyntheticRuleManifest", readResource("rules/nc_synthetic_demo_v1.json"));
    expect(manifest.implementationStatus).toBe("NOT_IMPLEMENTED");
    expect(manifest.allowLiveUse).toBe(false);
    expect(manifest.legalReviewedBy).toBeNull();
    expect(manifest.legalEffectiveFrom).toBeNull();
    expect(manifest.syntheticAssumptions.interimMoneyHandling).toBe("UNRESOLVED_PENDING_REVIEW");
    expect(manifest.syntheticAssumptions.missingAddressHandling).toBe("UNRESOLVED_PENDING_REVIEW");
    expect(manifest.allowedOrigins).toEqual(["CONSTRUCTED"]);
  });
  it.each([["status", "REVIEWED_FOR_SCOPE"], ["legalReviewedBy", "invented-reviewer"], ["allowLiveUse", true], ["legalEffectiveFrom", "2026-01-01"]] as const)("manifest cannot falsely claim %s", (key, value): void => {
    const raw = asRecord(readResource("rules/nc_synthetic_demo_v1.json"));
    expect((): unknown => from_wire("SyntheticRuleManifest", { ...raw, [key]: value })).toThrow(ContractError);
  });
  it("all ten legal review cards remain pending", (): void => {
    const raw = asRecord(readResource("legal/nc_review_cards.json")); const cards = raw.cards;
    if (!Array.isArray(cards)) throw new Error("Missing legal cards");
    expect(raw.status).toBe("PENDING"); expect(cards).toHaveLength(10);
    const manifest = from_wire("SyntheticRuleManifest", readResource("rules/nc_synthetic_demo_v1.json"));
    expect(new Set(cards.map((card: unknown): unknown => asRecord(card).questionId))).toEqual(new Set(manifest.questionIds));
    const required = ["questionId", "question", "scope", "sourceLocators", "requiredFacts", "possibleAnswers", "consequences", "completionCondition", "reconsiderWhen", "evaluationScenarios", "unresolvedInterpretations", "status", "reviewer"];
    cards.forEach((value: unknown): void => {
      const card = asRecord(value);
      expect(required.every((key): boolean => Object.hasOwn(card, key))).toBe(true);
      expect(card.status).toBe("PENDING"); expect(card.reviewer).toBeNull();
      expect(card.unresolvedInterpretations).not.toEqual([]);
    });
  });
  it("privileged model commands and complete-case actions do not exist", (): void => {
    ["COMPLETE_CASE", "CHANGE_BANK_DETAILS", "PUBLISH_LEGAL_RULE"].forEach((command): void => expect(VOCABULARY.actionKind).not.toContain(command));
  });
  it("Phase A demo release is not enabled as a Phase B review release", (): void => {
    expect((): unknown => review_request(from_wire("ReviewRequest", baseRequest()), loadReviewRelease())).toThrow(ContractError);
  });
});
