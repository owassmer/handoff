import { describe, expect, it } from "vitest";
import { documentKey, readWorkspace } from "./contracts";
import { exampleWorkspace } from "./examples.test-support";

function linked() {
  const data = exampleWorkspace();
  data.documents[0] = {
    ...data.documents[0],
    sourceKind: "Prepared",
    sourceDocumentIds: ["quote"],
    mimeType: null,
  };
  data.documents[1] = { ...data.documents[1], sourceKind: "Original" };
  return data;
}
describe("Protected supporting file references", () => {
  it("accepts legacy reads and additive valid supporting files without relabelling the summary", () => {
    const legacy = exampleWorkspace();
    expect(readWorkspace(JSON.stringify(legacy), "office", "garden-home")).toEqual(legacy);
    const data = linked();
    expect(readWorkspace(JSON.stringify(data), "office", "garden-home")).toEqual(data);
    expect(data.documents[0].mediaSetRid).toBeNull();
    expect(data.documents[0].sourceKind).toBe("Prepared");
  });
  it("accepts multiple separately identified originals in the same returned case", () => {
    const data = linked();
    data.documents.push({ ...data.documents[1], id: "second", mediaItemRid: "second-file" });
    data.documents[0].sourceDocumentIds?.push("second");
    expect(readWorkspace(JSON.stringify(data), "office", "garden-home").documents).toHaveLength(4);
  });
  it.each(
    [
      ["missing"],
      ["survey"],
      ["lease-text"],
      ["quote", "quote"],
      [""],
      [" "],
      Array.from({ length: 33 }, (_, i) => `file-${i}`),
    ].map((refs) => ({ refs })),
  )("rejects invalid, dangling, self, prepared and excessive references $refs", ({ refs }) => {
    const data = linked();
    data.documents[0].sourceDocumentIds = refs;
    expect(() => readWorkspace(JSON.stringify(data), "office", "garden-home")).toThrow();
  });
  it("rejects an original from a different case response", () => {
    const data = linked();
    data.documents = data.documents.filter((d) => d.id !== "quote");
    expect(() => readWorkspace(JSON.stringify(data), "office", "garden-home")).toThrow();
  });
  it.each([
    "original-without-file",
    "original-with-children",
    "prepared-with-file",
    "untyped-with-references",
    "unknown-source-kind",
  ])("rejects %s", (scenario) => {
    const data = linked();
    if (scenario === "original-without-file") {
      data.documents[1].mediaSetRid = data.documents[1].mediaItemRid = null;
    }
    if (scenario === "original-with-children") {
      data.documents[1].sourceDocumentIds = ["survey"];
    }
    if (scenario === "prepared-with-file") {
      data.documents[1].sourceKind = "Prepared";
    }
    if (scenario === "untyped-with-references") {
      delete data.documents[0].sourceKind;
    }
    if (scenario === "unknown-source-kind") {
      Object.assign(data.documents[0], { sourceKind: "Verified fact" });
    }
    expect(() => readWorkspace(JSON.stringify(data), "office", "garden-home")).toThrow();
  });
  it("invalidates source identity when supporting references or classification change", () => {
    const doc = linked().documents[0],
      key = documentKey(doc);
    expect(documentKey({ ...doc, sourceDocumentIds: [] })).not.toBe(key);
    expect(documentKey({ ...doc, sourceKind: undefined })).not.toBe(key);
  });
});
