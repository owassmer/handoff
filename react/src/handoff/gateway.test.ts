import type { Client } from "@osdk/client";
import { MediaSets, Ontologies } from "@osdk/foundry";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { type Change, readChange, readList, readWorkspace } from "./contracts";
import { absentChange, exampleWorkspace, listFor, savedChange } from "./examples.test-support";
import { HANDOFF_BRANCH, createHandoffGateway, isConnected } from "./gateway";

vi.mock("@osdk/foundry", () => ({
  Ontologies: {
    QueryTypes: { get: vi.fn() },
    Queries: { execute: vi.fn() },
    ActionTypesV2: { get: vi.fn() },
    Actions: { apply: vi.fn() },
  },
  MediaSets: { MediaSets: { read: vi.fn() } },
}));
const connection = {
  ontologyRid: "test-ontology",
  workspaceId: "office",
  functionVersion: "7.2.0",
};
const client = {} as Client;
const change: Change = {
  kind: "budget",
  handoffId: "garden-home",
  workPlanId: "work-garden",
  expectedRevision: "2",
  budgetCents: "120025",
  commandId: "one-change",
};
beforeEach(() => {
  vi.resetAllMocks();
});
function actionMetadata(kind: Change["kind"] = "budget") {
  return {
    apiName: kind === "budget" ? "change-handoff-work-plan" : "accept-handoff-work-plan",
    rid: "action",
    status: "ACTIVE" as const,
    operations: [],
    parameters: Object.fromEntries(
      [
        "workPlanId",
        "expectedRevision",
        "commandId",
        ...(kind === "budget" ? ["budgetCents"] : []),
      ].map((key) => [
        key,
        {
          displayName: key,
          typeClasses: [],
          required: true,
          dataType: { type: "string" as const },
        },
      ]),
    ),
  };
}

describe("Handoff reads and saved changes", () => {
  it("requires real workspace and exact version settings instead of substitutes", async () => {
    const gateway = createHandoffGateway(client, { ontologyRid: "test-ontology" });
    await expect(gateway.list()).rejects.toThrow();
    expect(Ontologies.QueryTypes.get).not.toHaveBeenCalled();
    expect(Ontologies.Queries.execute).not.toHaveBeenCalled();
    expect(
      isConnected({ ontologyRid: "test", workspaceId: "office", functionVersion: "latest" }),
    ).toBe(false);
  });
  it("executes the fixed reads on the exact branch and version without metadata", async () => {
    const data = exampleWorkspace();
    vi.mocked(Ontologies.Queries.execute)
      .mockResolvedValueOnce({ value: JSON.stringify(listFor(data)) })
      .mockResolvedValueOnce({ value: JSON.stringify(data) });
    const gateway = createHandoffGateway(client, connection);
    expect((await gateway.list()).handoffs[0].propertyName).toBe("Garden home");
    expect((await gateway.workspace("garden-home")).documents[0].text).toContain("plaster repair");
    expect(Ontologies.QueryTypes.get).not.toHaveBeenCalled();
    expect(Ontologies.Queries.execute).toHaveBeenCalledTimes(2);
    expect(Ontologies.Queries.execute).toHaveBeenNthCalledWith(
      1,
      client,
      "test-ontology",
      "listHandoffs",
      { parameters: { workspaceId: "office" } },
      { branch: HANDOFF_BRANCH, version: "7.2.0" },
    );
    expect(Ontologies.Queries.execute).toHaveBeenNthCalledWith(
      2,
      client,
      "test-ontology",
      "getHandoffWorkspace",
      { parameters: { handoffId: "garden-home" } },
      { branch: HANDOFF_BRANCH, version: "7.2.0" },
    );
  });
  it("checks a saved change through the public query with two required strings and no actor", async () => {
    vi.mocked(Ontologies.Queries.execute).mockResolvedValue({
      value: JSON.stringify(absentChange("one-change")),
    });
    const gateway = createHandoffGateway(client, connection);
    expect(await gateway.receipt("garden-home", "one-change")).toEqual(absentChange("one-change"));
    expect(Ontologies.QueryTypes.get).not.toHaveBeenCalled();
    expect(Ontologies.Queries.execute).toHaveBeenCalledTimes(1);
    expect(Ontologies.Queries.execute).toHaveBeenCalledWith(
      client,
      "test-ontology",
      "getHandoffChange",
      { parameters: { handoffId: "garden-home", commandId: "one-change" } },
      { branch: HANDOFF_BRANCH, version: "7.2.0" },
    );
    expect(Ontologies.Actions.apply).not.toHaveBeenCalled();
    vi.mocked(Ontologies.Queries.execute).mockRejectedValue(new Error("unavailable"));
    await expect(gateway.receipt("garden-home", "one-change")).rejects.toThrow();
  });
  it.each([undefined, null, 7, {}, "", "   "])(
    "rejects an invalid required string %j locally before any request",
    async (invalid) => {
      const gateway = createHandoffGateway(client, connection);
      await expect(gateway.workspace(invalid as string)).rejects.toThrow();
      await expect(gateway.receipt(invalid as string, "one-change")).rejects.toThrow();
      await expect(gateway.receipt("garden-home", invalid as string)).rejects.toThrow();
      await expect(
        createHandoffGateway(client, { ...connection, workspaceId: "" }).list(),
      ).rejects.toThrow();
      expect(Ontologies.QueryTypes.get).not.toHaveBeenCalled();
      expect(Ontologies.Queries.execute).not.toHaveBeenCalled();
    },
  );
  it("validates confirmation identity, status and complete saved details", async () => {
    const receipt = await savedChange(change, exampleWorkspace());
    expect(readChange(JSON.stringify(receipt), change.commandId)).toEqual(receipt);
    for (const patch of [
      { commandId: "other" },
      { version: "1" },
      { status: "Not found" },
      { subjectId: null },
      { payloadHash: "incorrect" },
      { at: "not a date" },
      { resultRevision: 3 },
      { kind: "Something else" },
    ]) {
      expect(() =>
        readChange(JSON.stringify({ ...receipt, ...patch }), change.commandId),
      ).toThrow();
    }
  });
  it("passes only the named change fields, preserving long strings and branch", async () => {
    vi.mocked(Ontologies.ActionTypesV2.get).mockResolvedValue(actionMetadata());
    vi.mocked(Ontologies.Actions.apply).mockResolvedValue({
      validation: { result: "VALID", parameters: {}, submissionCriteria: [] },
    });
    const gateway = createHandoffGateway(client, connection);
    expect(await gateway.apply(change)).toBe("saved");
    expect(Ontologies.Actions.apply).toHaveBeenCalledWith(
      client,
      "test-ontology",
      "change-handoff-work-plan",
      {
        parameters: {
          workPlanId: "work-garden",
          expectedRevision: "2",
          budgetCents: "120025",
          commandId: "one-change",
        },
        options: { mode: "VALIDATE_AND_EXECUTE", returnEdits: "NONE" },
      },
      { branch: HANDOFF_BRANCH },
    );
    vi.mocked(Ontologies.ActionTypesV2.get).mockResolvedValue(actionMetadata("accept"));
    await gateway.apply({ ...change, kind: "accept" });
    const call = vi.mocked(Ontologies.Actions.apply).mock.calls[1];
    expect(call[2]).toBe("accept-handoff-work-plan");
    expect(Object.keys(call[3].parameters).sort()).toEqual([
      "commandId",
      "expectedRevision",
      "workPlanId",
    ]);
  });
  it("separates a rejected change from a lost response without exposing either error", async () => {
    vi.mocked(Ontologies.ActionTypesV2.get).mockResolvedValue(actionMetadata());
    vi.mocked(Ontologies.Actions.apply)
      .mockResolvedValueOnce({
        validation: { result: "INVALID", parameters: {}, submissionCriteria: [] },
      })
      .mockRejectedValueOnce(new Error("connection lost"));
    const gateway = createHandoffGateway(client, connection);
    expect(await gateway.apply(change)).toBe("rejected");
    await expect(gateway.apply(change)).rejects.toThrow();
    expect(Ontologies.Actions.apply).toHaveBeenCalledTimes(2);
  });
  it("reads an original PDF through the public media API only for a returned document", async () => {
    const data = exampleWorkspace();
    vi.mocked(Ontologies.Queries.execute).mockResolvedValue({ value: JSON.stringify(data) });
    vi.mocked(MediaSets.MediaSets.read).mockResolvedValue(
      new Response("%PDF-1.7\ncontent", { headers: { "Content-Type": "application/pdf" } }),
    );
    const gateway = createHandoffGateway(client, connection);
    await expect(gateway.document(data.documents[1])).rejects.toThrow();
    await gateway.workspace("garden-home");
    const blob = await gateway.document(data.documents[1]);
    expect(blob.type).toBe("application/pdf");
    expect(MediaSets.MediaSets.read).toHaveBeenCalledWith(client, "media-set", "media-item");
    await expect(
      gateway.document({ ...data.documents[1], mediaItemRid: "other-item" }),
    ).rejects.toThrow();
  });
  it("rejects malformed or crossed reads rather than filling unknown amounts with zero", () => {
    const data = exampleWorkspace();
    expect(() =>
      readWorkspace(JSON.stringify({ ...data, version: "1" }), "office", "garden-home"),
    ).toThrow();
    expect(() =>
      readWorkspace(
        JSON.stringify({ ...data, workPlan: { ...data.workPlan, budgetCents: 100000 } }),
        "office",
        "garden-home",
      ),
    ).toThrow();
    expect(() => readWorkspace(JSON.stringify(data), "another-office", "garden-home")).toThrow();
    expect(() => readList(JSON.stringify(listFor(data)), "another-office")).toThrow();
    const enormous = { ...data, workPlan: { ...data.workPlan, budgetCents: "9007199254740993" } };
    expect(
      readWorkspace(JSON.stringify(enormous), "office", "garden-home").workPlan?.budgetCents,
    ).toBe("9007199254740993");
  });
});
