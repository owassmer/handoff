import { describe, expect, it } from "vitest";
import reviewDepositCloseout from "../../functions/reviewDepositCloseout.js";
import { from_wire, parse_json } from "../domain/codec.js";
import { OUTPUT_FIELDS, caseRequest, loadReviewRelease } from "./fixtures/helpers.js";

function requestText(id = "NC-A-002"): string {
  const request = caseRequest(id);
  request.ruleReleaseId = loadReviewRelease().ruleReleaseId;
  return JSON.stringify(request);
}

describe("read-only TSv2 JSON transport", () => {
  it("returns a valid six-output envelope with numeric cents and incomplete outcomes", () => {
    const text = reviewDepositCloseout(requestText());
    expect(typeof text).toBe("string");
    const envelope = from_wire("ReviewEnvelope", parse_json(text));
    expect(Object.keys(envelope.result).sort()).toEqual([...OUTPUT_FIELDS].sort());
    expect(envelope.result.account.recordedDepositCents).toBe(200000);
    expect(envelope.result.account.totalDeductionsCents).toBe(40000);
    expect(envelope.result.account.finalRefundCents).toBe(160000);
    expect(envelope.result.outcomes.depositComplete).toBe(false);
    expect(envelope.result.outcomes.overallCaseComplete).toBe(false);
  });

  it("reproduces a single changed choice without mutating its input", () => {
    const request = caseRequest();
    request.ruleReleaseId = loadReviewRelease().ruleReleaseId;
    const repair = request.snapshot.charges.find((item) => item.itemId === "repair-250");
    if (repair === undefined) throw new Error("Missing literal test repair");
    repair.chosenAmountCents = 20000;
    const original = JSON.stringify(request);
    const envelope = from_wire("ReviewEnvelope", parse_json(reviewDepositCloseout(original)));
    expect(envelope.result.account.totalDeductionsCents).toBe(35000);
    expect(envelope.result.account.finalRefundCents).toBe(165000);
    expect(JSON.stringify(request)).toBe(original);
  });

  it.each(["ruleReleaseId", "rule\\u0052eleaseId"])("rejects duplicate decoded key %s in otherwise valid input", (key) => {
    const request = requestText();
    const duplicated = request.slice(0, -1) + `,"${key}":"${loadReviewRelease().ruleReleaseId}"}`;
    expect(() => reviewDepositCloseout(duplicated)).toThrow(/contract/);
  });

  it.each([".0", "e0"])("rejects lexical non-integer numeric representation %s", (suffix) => {
    const request = requestText();
    const altered = request.replace(/:(-?\d+)(?=[,}])/, (_match, integer: string) => `:${integer}${suffix}`);
    expect(altered).not.toBe(request);
    expect(() => reviewDepositCloseout(altered)).toThrow(/contract/);
  });

  it.each(["NaN", "Infinity", "-Infinity", "9007199254740992"])("rejects numeric token %s", (token) => {
    const request = requestText().replace(/:(-?\d+)(?=[,}])/, `:${token}`);
    expect(() => reviewDepositCloseout(request)).toThrow(/contract/);
  });

  it.each(["", "{", "{}garbage", "[", "null", "[true]", '{"x":undefined}'])("fails malformed or wrong-shaped JSON without echoing it", (text) => {
    expect(() => reviewDepositCloseout(text)).toThrow(/contract/);
  });

  it("rejects over-limit input without truncating", () => {
    expect(() => reviewDepositCloseout(" ".repeat(1_000_001))).toThrow(/1,000,000/);
  });

  it("does not accept caller-selected legal release", () => {
    const request = caseRequest();
    request.ruleReleaseId = "UNREVIEWED_LIVE_RELEASE";
    expect(() => reviewDepositCloseout(JSON.stringify(request))).toThrow(/contract/);
  });
});
