import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { createClient } from "@osdk/client";
import { $ontologyRid, HandoffFunding } from "@ontology/sdk";
import { instant } from "../deliveryContracts.js";
import { sameRecord, type RecordTimestampKey } from "../deliveryRecords.js";
import { fundingInformation } from "../supportingSources.js";
import { dateOnly, orderedJson } from "../values.js";

// Literal observations from the real branch preview and ontology SQL, not dates shaped by a mock object.
const SDK_WHOLE_SECOND = "2026-09-24T00:00:00Z";
const SQL_MILLISECOND = "2026-09-24T00:00:00.000Z";
const metadata = JSON.parse(readFileSync(new URL("../../../.sdk/@ontology/sdk/experimental/ontology-metadata.json", import.meta.url), "utf8")) as {
  objectTypes: Record<string, unknown>;
};

describe("real OSDK timestamp wire decoding (fixture HTTP, no mocked OSDK objects)", () => {
  it.each([SDK_WHOLE_SECOND, SQL_MILLISECOND])("compares the unmodified wire value %s to confirmed source/SQL time", async (confirmedAt) => {
    const seen: string[] = [];
    // Test-only transport. The actual OSDK loads metadata and hydrates the returned wire object;
    // this callback cannot reach a server and never returns credentials or constructed SDK instances.
    const transport: typeof fetch = async (input): Promise<Response> => {
      const url = new URL(input instanceof Request ? input.url : String(input));
      seen.push(url.pathname);
      if (url.pathname.endsWith("/objectTypes/HandoffFunding/fullMetadata")) {
        return Response.json(metadata.objectTypes.HandoffFunding);
      }
      if (url.pathname.endsWith("/objectSets/loadObjects")) {
        return Response.json({ data: [{ __apiName: "HandoffFunding", __primaryKey: "wire-allocation", fundingId: "wire-allocation",
          ownerPartyId: "wire-owner", currency: "USD", confirmedCents: "6000", confirmedAt }] });
      }
      throw new Error(`Unexpected offline SDK request: ${url.pathname}`);
    };
    const client = createClient("https://offline.example.test", $ontologyRid, async () => "offline-test-only", undefined, transport);
    const saved = (await client(HandoffFunding).fetchPage()).data[0]!;
    const source = fundingInformation({ documentId: "wire-source", partyId: "wire-owner", kind: "Owner funding", detailsJson: JSON.stringify({
      ownerPartyId: "wire-owner", currency: "USD", confirmedCents: "6000", confirmedAt: SDK_WHOLE_SECOND,
      paymentBehavior: "Settle", responseMinutes: 1,
    }) });
    expect(saved.confirmedAt).toBe(confirmedAt);
    expect(saved.confirmedCents).toBe("6000");
    expect(source.confirmedAt).toBe(SQL_MILLISECOND);
    expect(instant(saved.confirmedAt)).toBe(source.confirmedAt);
    expect(() => sameRecord(saved, { confirmedAt: source.confirmedAt }, [], ["confirmedAt"])).not.toThrow();
    expect(seen.some((path) => path.endsWith("/fullMetadata"))).toBe(true);
    expect(seen.some((path) => path.endsWith("/loadObjects"))).toBe(true);
  });
});

describe("explicit record timestamp semantics", () => {
  const keys: RecordTimestampKey[] = ["confirmedAt", "availableFrom", "validUntil", "createdAt", "observedAt", "issuedAt", "dueAt", "responseDueAt"];
  it.each(keys)("normalizes both sides of %s, without ignoring a changed instant", (key) => {
    const before = { [key]: SDK_WHOLE_SECOND }, expected = { [key]: SQL_MILLISECOND };
    expect(() => sameRecord(before, expected, [], [key])).not.toThrow();
    expect(() => sameRecord(expected, before, [], [key])).not.toThrow();
    expect(() => sameRecord(before, { [key]: "2026-09-24T00:00:00.001Z" }, [], [key])).toThrow(/different saved details/);
    expect(() => sameRecord({}, expected, [], [key])).toThrow(/different saved details/);
  });
  it("preserves ignore semantics, null/absent optional metadata, arrays, money and identity equality", () => {
    const saved = { confirmedAt: SDK_WHOLE_SECOND, revision: "2", readerIds: ["owner"], confirmedCents: "6000", sourceVersion: "1", sourceDocumentId: "source", sourceRecordId: "allocation", sourceSystem: "books", title: SQL_MILLISECOND };
    const expected = { ...saved, confirmedAt: SQL_MILLISECOND, revision: "1" };
    expect(() => sameRecord(saved, expected, ["revision"], ["confirmedAt"])).not.toThrow();
    expect(() => sameRecord({ ...saved, mimeType: null }, { ...expected, mimeType: undefined }, ["revision"], ["confirmedAt"])).not.toThrow();
    ["readerIds", "confirmedCents", "sourceVersion", "sourceDocumentId", "sourceRecordId", "sourceSystem", "title"].forEach((key) => {
      const value = key === "readerIds" ? ["other"] : key === "title" ? SDK_WHOLE_SECOND : "different";
      expect(() => sameRecord(saved, { ...expected, [key]: value }, ["revision"], ["confirmedAt"])).toThrow(/different saved details/);
    });
  });
  it("keeps source bodies/preparation, hashes, and document calendar dates byte-semantic", () => {
    const source = { confirmedAt: SDK_WHOLE_SECOND, _preparation: { actorId: "author", purpose: "Demonstration configuration", sourceDocumentIds: [] } };
    expect(() => sameRecord({ detailsJson: orderedJson(source) }, { detailsJson: orderedJson({ ...source, confirmedAt: SQL_MILLISECOND }) })).toThrow();
    expect(() => sameRecord({ availableFrom: "2026-09-24" }, { availableFrom: "2026-09-24" })).not.toThrow();
    expect(() => sameRecord({ availableFrom: "2026-09-24" }, { availableFrom: SDK_WHOLE_SECOND })).toThrow();
    expect(() => sameRecord({ sourceVersion: SDK_WHOLE_SECOND }, { sourceVersion: SQL_MILLISECOND })).toThrow();
    expect(dateOnly("2026-09-24", "Source date")).toBe("2026-09-24");
  });
  it.each(["2026-09-24T00:00:00+00:00", "2026-09-24T01:00:00+01:00", "2026-09-24", "2026-02-30T00:00:00Z", "not a time"])("retains the existing strict UTC contract: %s is not accepted", (value) => {
    expect(() => instant(value)).toThrow();
    expect(() => sameRecord({ confirmedAt: value }, { confirmedAt: value }, [], ["confirmedAt"])).toThrow();
  });
});
