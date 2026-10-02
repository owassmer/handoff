import type { Client } from "@osdk/client";
import { MediaSets, Ontologies } from "@osdk/foundry";
import { createHash, webcrypto } from "node:crypto";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { Change } from "./contracts";
import { deferred, exampleWorkspace } from "./examples.test-support";
import { HANDOFF_BRANCH, createHandoffGateway } from "./gateway";
import { verifiedOriginal } from "./sources";

vi.mock("@osdk/foundry", () => ({
  Ontologies: {
    Queries: { execute: vi.fn() },
    ActionTypesV2: { get: vi.fn() },
    Actions: { apply: vi.fn() },
  },
  MediaSets: { MediaSets: { read: vi.fn() } },
}));
const connection = {
  ontologyRid: "ontology",
  workspaceId: "office",
  functionVersion: "7.2.1-branch-test",
};
const client = {} as Client;
beforeEach(() => {
  vi.resetAllMocks();
  vi.stubGlobal("crypto", webcrypto);
});
afterEach(() => vi.unstubAllGlobals());
function metadata(message = false): Ontologies.ActionTypeV2 {
  const required = message
    ? ["handoffId", "message", "commandId"]
    : ["workPlanId", "expectedRevision", "commandId"];
  const optional = message ? ["expectedPlanRevision"] : ["budgetCents", "changesJson"];
  return {
    apiName: message ? "send-handoff-message" : "change-handoff-work-plan",
    rid: "action",
    status: "ACTIVE",
    operations: [],
    parameters: Object.fromEntries(
      [...required, ...optional].map((name) => [
        name,
        {
          displayName: name,
          typeClasses: [],
          required: required.includes(name),
          dataType: {
            type: ["expectedRevision", "expectedPlanRevision", "budgetCents"].includes(name)
              ? "long"
              : "string",
          },
        },
      ]),
    ),
  };
}
const budget: Change = {
  kind: "budget",
  handoffId: "garden-home",
  workPlanId: "plan",
  expectedRevision: "7",
  budgetCents: "99999999",
  commandId: "command",
};
describe("Precise changes and discussion transport", () => {
  it("permits omitted optional Long/JSON fields while passing exactly one edit form", async () => {
    vi.mocked(Ontologies.ActionTypesV2.get).mockResolvedValue(metadata());
    vi.mocked(Ontologies.Actions.apply).mockResolvedValue({});
    const gateway = createHandoffGateway(client, connection);
    expect(await gateway.apply(budget)).toBe("saved");
    const changes = {
      budgetCents: "95000",
      fixedProviderPartyId: null,
      fixedRequirements: ["Keep fittings"],
      selections: [
        { quoteId: "quote", quoteLineId: "line", scope: "Repair", reason: "Local damage" },
      ],
    };
    const plan: Change = { ...budget, kind: "plan", changes };
    expect(await gateway.apply(plan)).toBe("saved");
    const calls = vi.mocked(Ontologies.Actions.apply).mock.calls;
    expect(calls[0][3].parameters).toEqual({
      commandId: "command",
      workPlanId: "plan",
      expectedRevision: "7",
      budgetCents: "99999999",
    });
    expect(calls[1][3].parameters).toEqual({
      commandId: "command",
      workPlanId: "plan",
      expectedRevision: "7",
      changesJson: JSON.stringify(changes),
    });
    expect(calls[1][4]).toEqual({ branch: HANDOFF_BRANCH });
  });
  it.each([undefined, "14"])(
    "sends contextual messages with optional reviewed version %s and no caller identity",
    async (expectedPlanRevision) => {
      vi.mocked(Ontologies.ActionTypesV2.get).mockResolvedValue(metadata(true));
      vi.mocked(Ontologies.Actions.apply).mockResolvedValue({});
      const gateway = createHandoffGateway(client, connection);
      const message: Change = {
        kind: "message",
        handoffId: "garden-home",
        message: "Please retain the door.",
        commandId: "discussion",
        expectedPlanRevision,
      };
      expect(await gateway.apply(message)).toBe("saved");
      expect(Ontologies.Actions.apply).toHaveBeenCalledWith(
        client,
        "ontology",
        "send-handoff-message",
        {
          parameters: {
            handoffId: "garden-home",
            message: message.message,
            commandId: "discussion",
            ...(expectedPlanRevision === undefined ? {} : { expectedPlanRevision }),
          },
          options: { mode: "VALIDATE_AND_EXECUTE", returnEdits: "NONE" },
        },
        { branch: HANDOFF_BRANCH },
      );
    },
  );
  it("does not dispatch a slow metadata-preflight command after identity invalidation", async () => {
    const pending = deferred<Ontologies.ActionTypeV2>();
    vi.mocked(Ontologies.ActionTypesV2.get).mockReturnValue(pending.promise);
    const gateway = createHandoffGateway(client, connection);
    const apply = gateway.apply(budget);
    gateway.clearDocuments!();
    pending.resolve(metadata());
    expect(await apply).toBe("rejected");
    expect(Ontologies.Actions.apply).not.toHaveBeenCalled();
  });
  it("rejects a metadata contract exposing an actor instead of widening allowed inputs", async () => {
    const meta = metadata();
    meta.parameters.currentUserId = {
      displayName: "Actor",
      typeClasses: [],
      required: false,
      dataType: { type: "string" },
    };
    vi.mocked(Ontologies.ActionTypesV2.get).mockResolvedValue(meta);
    expect(await createHandoffGateway(client, connection).apply(budget)).toBe("rejected");
    expect(Ontologies.Actions.apply).not.toHaveBeenCalled();
  });
});
describe("Original source access", () => {
  it("removes missing and replaced grants, not a growing cache of earlier documents", async () => {
    const data = exampleWorkspace(),
      gateway = createHandoffGateway(client, connection),
      document = data.documents[1];
    vi.mocked(Ontologies.Queries.execute).mockResolvedValue({ value: JSON.stringify(data) });
    await gateway.workspace("garden-home");
    const invalidated = vi.fn();
    gateway.onDocumentInvalidated!(document, invalidated);
    data.documents[1] = { ...document, sourceVersion: "2" };
    vi.mocked(Ontologies.Queries.execute).mockResolvedValue({ value: JSON.stringify(data) });
    await gateway.workspace("garden-home");
    expect(invalidated).toHaveBeenCalled();
    await expect(gateway.document(document)).rejects.toThrow();
    const replacement = data.documents[1];
    data.documents = [];
    vi.mocked(Ontologies.Queries.execute).mockResolvedValue({ value: JSON.stringify(data) });
    await gateway.workspace("garden-home");
    await expect(gateway.document(replacement)).rejects.toThrow();
    expect(MediaSets.MediaSets.read).not.toHaveBeenCalled();
  });
  it("does not grant an original after a slow read crosses identity invalidation", async () => {
    const pending = deferred<Ontologies.ExecuteQueryResponse>(),
      gateway = createHandoffGateway(client, connection),
      data = exampleWorkspace();
    vi.mocked(Ontologies.Queries.execute).mockReturnValue(pending.promise);
    const read = gateway.workspace("garden-home");
    gateway.clearDocuments!();
    pending.resolve({ value: JSON.stringify(data) });
    await expect(read).rejects.toThrow();
    await expect(gateway.document(data.documents[1])).rejects.toThrow();
  });
  it("discards an in-flight original after a fresh read removes its source", async () => {
    const data = exampleWorkspace(),
      document = data.documents[1],
      gateway = createHandoffGateway(client, connection);
    vi.mocked(Ontologies.Queries.execute).mockResolvedValue({ value: JSON.stringify(data) });
    await gateway.workspace("garden-home");
    const download = deferred<Response>();
    vi.mocked(MediaSets.MediaSets.read).mockReturnValue(download.promise);
    const file = gateway.document(document);
    data.documents = [];
    vi.mocked(Ontologies.Queries.execute).mockResolvedValue({ value: JSON.stringify(data) });
    await gateway.workspace("garden-home");
    download.resolve(new Response("%PDF-1.7"));
    await expect(file).rejects.toThrow();
  });
  it("clears source grants on a failed fresh read", async () => {
    const data = exampleWorkspace(),
      gateway = createHandoffGateway(client, connection);
    vi.mocked(Ontologies.Queries.execute).mockResolvedValue({ value: JSON.stringify(data) });
    await gateway.workspace("garden-home");
    vi.mocked(Ontologies.Queries.execute).mockRejectedValue(new Error("offline"));
    await expect(gateway.workspace("garden-home")).rejects.toThrow();
    await expect(gateway.document(data.documents[1])).rejects.toThrow();
  });
  it.each([
    ["application/pdf", new Blob(["%PDF-1.7"])],
    ["image/png", new Blob([new Uint8Array([137, 80, 78, 71, 13, 10, 26, 10])])],
    ["image/jpeg", new Blob([new Uint8Array([255, 216, 255, 224])])],
    ["image/gif", new Blob(["GIF89a"])],
    ["image/webp", new Blob(["RIFF1234WEBP"])],
  ])(
    "recognizes passive %s originals, not inferred property dimensions",
    async (mimeType, blob) => {
      expect(
        (await verifiedOriginal(blob, { ...exampleWorkspace().documents[1], mimeType })).type,
      ).toBe(mimeType);
    },
  );
  it("rejects active content, mismatched MIME and mismatched original hashes", async () => {
    const doc = exampleWorkspace().documents[1];
    await expect(
      verifiedOriginal(new Blob(["<svg onload='alert(1)'>"]), {
        ...doc,
        mimeType: "image/svg+xml",
      }),
    ).rejects.toThrow();
    await expect(
      verifiedOriginal(new Blob(["%PDF-1.7"]), { ...doc, mimeType: "image/png" }),
    ).rejects.toThrow();
    await expect(
      verifiedOriginal(new Blob(["%PDF-1.7"]), { ...doc, sha256: "0".repeat(64) }),
    ).rejects.toThrow();
    const sha256 = createHash("sha256").update("%PDF-1.7").digest("hex");
    expect((await verifiedOriginal(new Blob(["%PDF-1.7"]), { ...doc, sha256 })).type).toBe(
      "application/pdf",
    );
  });
});
