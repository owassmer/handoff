import { createClient } from "@osdk/client";
import { loadEnv } from "vite";
import { describe, expect, it } from "vitest";
import { type Change, HandoffError, type HandoffWorkspace } from "./contracts";
import {
  absentChange,
  exampleWorkspace,
  listFor,
  memoryStorage,
  savedChange,
} from "./examples.test-support";
import { HANDOFF_BRANCH, type HandoffConnection, createHandoffGateway } from "./gateway";
import { HandoffStore } from "./state";

// The installed SDK runs against a local HTTP transport, never the live service.
const env = loadEnv("production", process.cwd());
const settings = {
  ontologyRid: env.VITE_FOUNDRY_ONTOLOGY_RID,
  workspaceId: env.VITE_HANDOFF_WORKSPACE_ID,
  functionVersion: env.VITE_HANDOFF_FUNCTION_VERSION,
  actionFunctionVersion: env.VITE_HANDOFF_ACTION_FUNCTION_VERSION,
  changeFunctionRid: env.VITE_HANDOFF_CHANGE_FUNCTION_RID,
  acceptFunctionRid: env.VITE_HANDOFF_ACCEPT_FUNCTION_RID,
  messageFunctionRid: env.VITE_HANDOFF_MESSAGE_FUNCTION_RID,
};
// Explicit historical fixtures, not deployment pins. Keep read/action isolation
// covered even when the actual deployment uses the same exact version for both.
const distinctVersions = {
  ...settings,
  functionVersion: "1.4.0",
  actionFunctionVersion: "1.4.1-branch-20260923-184852",
};
const change: Change = {
  kind: "budget",
  handoffId: "garden-home",
  workPlanId: "work-garden",
  expectedRevision: "2",
  budgetCents: "9007199254740993",
  commandId: "same-change",
};
interface TransportOptions {
  errorFunction?: string;
  errorVersion?: string;
  lostActionResponse?: boolean;
  queryError?: { apiName?: string; status: number; errorName: string; errorCode: string };
  queryValue?: (apiName: string, parameters: Record<string, string>, value: unknown) => unknown;
}
function localTransport(options: TransportOptions = {}, connection: HandoffConnection = settings) {
  const requests: Request[] = [];
  const data = exampleWorkspace();
  data.workspace.id = settings.workspaceId;
  const transport: typeof fetch = async (input, init) => {
    const request = new Request(input, init);
    requests.push(request.clone());
    const url = new URL(request.url);
    const name = url.pathname.split("/").slice(-1)[0];
    const json = (body: unknown, status = 200) =>
      new Response(JSON.stringify(body), {
        status,
        headers: { "Content-Type": "application/json" },
      });
    if (url.pathname.includes("/queryTypes/")) {
      throw new Error("These reads must not request query metadata.");
    }
    if (url.pathname.includes("/queries/")) {
      const apiName = url.pathname.split("/").slice(-2)[0];
      if (
        options.queryError &&
        (!options.queryError.apiName || options.queryError.apiName === apiName)
      ) {
        return json(
          {
            errorCode: options.queryError.errorCode,
            errorName: options.queryError.errorName,
            errorInstanceId: "local-query-error",
            parameters: {},
          },
          options.queryError.status,
        );
      }
      const { parameters } = (await request.json()) as { parameters: Record<string, string> };
      const value = JSON.stringify(
        apiName === "getHandoffChange"
          ? absentChange(parameters.commandId)
          : apiName === "getHandoffWorkspace"
            ? data
            : listFor(data),
      );
      return json({
        value: options.queryValue ? options.queryValue(apiName, parameters, value) : value,
      });
    }
    if (url.pathname.includes("/actionTypes/")) {
      return json({
        apiName: name,
        rid: "work-plan-action",
        status: "ACTIVE",
        operations: [],
        parameters: Object.fromEntries(
          [
            "workPlanId",
            "expectedRevision",
            "commandId",
            ...(name === "change-handoff-work-plan" ? ["budgetCents"] : []),
          ]
            .filter(() => name !== "resume-handoff")
            .concat(name === "resume-handoff" ? ["handoffId"] : [])
            .map((key) => [
              key,
              { dataType: { type: "string" }, required: true, displayName: key, typeClasses: [] },
            ]),
        ),
      });
    }
    if (url.pathname.includes("/actions/")) {
      if (options.lostActionResponse) {
        throw new TypeError("Response lost");
      }
      return options.errorFunction
        ? json(
            {
              errorCode: "INVALID_ARGUMENT",
              errorName: "FunctionEncounteredUserFacingError",
              errorInstanceId: "error-one",
              parameters: {
                functionRid: options.errorFunction,
                functionVersion: options.errorVersion ?? settings.actionFunctionVersion,
                message: "A newer decision exists.",
              },
            },
            400,
          )
        : json({ validation: { result: "VALID", parameters: {}, submissionCriteria: [] } });
    }
    if (url.pathname.startsWith("/api/v2/mediasets/")) {
      return new Response("%PDF-1.7\nOriginal document", {
        headers: { "Content-Type": "application/pdf" },
      });
    }
    throw new Error("Unexpected request");
  };
  const client = createClient(
    "https://handoff.test.invalid",
    settings.ontologyRid,
    async () => "local-token",
    { UNSTABLE_DO_NOT_USE_BRANCH: HANDOFF_BRANCH },
    transport,
  );
  return { gateway: createHandoffGateway(client, connection), requests, data };
}
function expectQueryRequests(requests: Request[], apiName: string, functionVersion?: string) {
  expect(requests).toHaveLength(1);
  expect(requests.filter((request) => request.method === "GET")).toHaveLength(0);
  const request = requests[0];
  expect(request.method).toBe("POST");
  const url = new URL(request.url);
  expect(url.pathname).toBe(
    `/api/v2/ontologies/${settings.ontologyRid}/queries/${apiName}/execute`,
  );
  expect([...url.searchParams.entries()].sort()).toEqual(
    functionVersion ? [["version", functionVersion]] : [],
  );
}
const reads = [
  {
    apiName: "listHandoffs",
    read: (gateway: ReturnType<typeof createHandoffGateway>) => gateway.list(),
  },
  {
    apiName: "getHandoffWorkspace",
    read: (gateway: ReturnType<typeof createHandoffGateway>) => gateway.workspace(change.handoffId),
  },
  {
    apiName: "getHandoffChange",
    read: (gateway: ReturnType<typeof createHandoffGateway>) =>
      gateway.receipt(change.handoffId, change.commandId),
  },
];
describe("Case controls step", () => {
  it("applies Resume handoff with only the case, and reports a refused overlap", async () => {
    const { gateway, requests } = localTransport();
    expect(await gateway.resume!(change.handoffId)).toEqual({ kind: "done" });
    const action = requests.find((request) => request.url.includes("/actions/"))!;
    expect(new URL(action.url).pathname).toContain("/actions/resume-handoff/apply");
    expect(((await action.json()) as { parameters: unknown }).parameters).toEqual({
      handoffId: change.handoffId,
    });
    const busy = localTransport({ errorFunction: "continue-handoff" });
    expect(await busy.gateway.resume!(change.handoffId)).toEqual({
      kind: "refused",
      message: "A newer decision exists.",
    });
  });
});

describe("Public SDK requests", () => {
  it("posts the list's required workspace string directly without metadata", async () => {
    const { gateway, requests, data } = localTransport();
    expect(await gateway.list()).toEqual(listFor(data));
    expectQueryRequests(requests, "listHandoffs");
    expect(await requests[0].json()).toEqual({ parameters: { workspaceId: settings.workspaceId } });
  });
  it("posts the workspace's required handoff string directly without metadata", async () => {
    const { gateway, requests, data } = localTransport();
    expect(await gateway.workspace(change.handoffId)).toEqual(data);
    expectQueryRequests(requests, "getHandoffWorkspace");
    expect(await requests[0].json()).toEqual({ parameters: { handoffId: change.handoffId } });
  });
  it("posts both required confirmation strings directly without metadata or an actor", async () => {
    const { gateway, requests } = localTransport();
    expect(await gateway.receipt(change.handoffId, change.commandId)).toEqual(
      absentChange(change.commandId),
    );
    expectQueryRequests(requests, "getHandoffChange");
    expect(await requests[0].json()).toEqual({
      parameters: { handoffId: change.handoffId, commandId: change.commandId },
    });
  });
  it.each(reads)(
    "keeps repeated $apiName reads free of metadata requests",
    async ({ apiName, read }) => {
      const { gateway, requests } = localTransport();
      await read(gateway);
      await read(gateway);
      expect(requests).toHaveLength(2);
      requests.forEach((request) => expectQueryRequests([request], apiName));
    },
  );
  it.each(reads)(
    "rejects malformed $apiName responses after direct execution",
    async ({ apiName, read }) => {
      for (const invalid of [null, 7, {}, "not JSON", "{}", JSON.stringify({ version: "1" })]) {
        const { gateway, requests } = localTransport({ queryValue: () => invalid });
        await expect(read(gateway)).rejects.toMatchObject({ kind: "read" });
        expectQueryRequests(requests, apiName);
      }
    },
  );
  it.each(reads)(
    "requires $apiName to return a JSON string, not an object",
    async ({ apiName, read }) => {
      const { gateway, requests } = localTransport({
        queryValue: (_name, _parameters, value) => JSON.parse(value as string),
      });
      await expect(read(gateway)).rejects.toMatchObject({ kind: "read" });
      expectQueryRequests(requests, apiName);
    },
  );
  it("rejects missing and non-string read inputs before reaching the installed transport", async () => {
    const { gateway, requests } = localTransport();
    for (const invalid of [undefined, null, 7, {}, "", "   "]) {
      await expect(gateway.workspace(invalid as string)).rejects.toMatchObject({ kind: "read" });
      await expect(gateway.receipt(invalid as string, change.commandId)).rejects.toMatchObject({
        kind: "read",
      });
      await expect(gateway.receipt(change.handoffId, invalid as string)).rejects.toMatchObject({
        kind: "read",
      });
    }
    expect(requests).toHaveLength(0);
  });
  it("denies crossed workspace, handoff and confirmation identities", async () => {
    const { gateway, data } = localTransport();
    data.workspace.id = "another-office";
    await expect(gateway.list()).rejects.toBeInstanceOf(HandoffError);
    await expect(gateway.workspace(change.handoffId)).rejects.toBeInstanceOf(HandoffError);
    data.workspace.id = settings.workspaceId;
    data.handoff.id = "another-handoff";
    await expect(gateway.workspace(change.handoffId)).rejects.toBeInstanceOf(HandoffError);
    const crossed = localTransport({
      queryValue: () => JSON.stringify(absentChange("another-change")),
    });
    await expect(
      crossed.gateway.receipt(change.handoffId, change.commandId),
    ).rejects.toBeInstanceOf(HandoffError);
  });
  it.each(reads)(
    "reports query availability separately from permission for $apiName without fallbacks",
    async ({ apiName, read }) => {
      for (const [status, errorCode, errorName, kind] of [
        [404, "NOT_FOUND", "QueryVersionNotFound", "unavailable"],
        [404, "NOT_FOUND", "QueryNotFound", "unavailable"],
        [403, "PERMISSION_DENIED", "PermissionDenied", "permission"],
        [401, "UNAUTHORIZED", "Unauthorized", "access"],
      ] as const) {
        const { gateway, requests } = localTransport({
          queryError: { status, errorCode, errorName },
        });
        await expect(read(gateway)).rejects.toMatchObject({ kind });
        expectQueryRequests(requests, apiName);
      }
    },
  );
  it.each([false, true])(
    "requires matching confirmation and a later coherent read even with lost response %s",
    async (lostActionResponse) => {
      const options: TransportOptions = { lostActionResponse };
      const { gateway, requests, data } = localTransport(options);
      const store = new HandoffStore(gateway, memoryStorage(), "local-save", 0);
      try {
        const read = store.workspace(change.handoffId);
        await read.fresh();
        await store.submit(data, "budget", "110050");
        const pending = store.pending(change.handoffId)!;
        expect(pending.status).toBe("checking");
        expect(pending.acknowledged).toBe(!lostActionResponse);
        const sent = pending.change!;
        if (sent.kind !== "budget") {
          throw new Error("Expected budget change");
        }
        const saved: HandoffWorkspace = {
          ...data,
          workPlan: { ...data.workPlan!, budgetCents: sent.budgetCents, revision: "3" },
        };
        const receipt = await savedChange(sent, saved);
        // Even an exact confirmation cannot clear a lagging workspace.
        options.queryValue = (name, _parameters, value) =>
          name === "getHandoffChange" ? JSON.stringify(receipt) : value;
        await read.fresh();
        expect(store.pending(change.handoffId)).toBeDefined();
        data.workPlan = saved.workPlan;
        for (const invalid of [
          absentChange(sent.commandId),
          { ...receipt, payloadHash: "a".repeat(64) },
          { ...receipt, commandId: "another-change" },
          { ...receipt, subjectId: "another-plan" },
          { ...receipt, kind: "Work plan accepted" },
        ]) {
          options.queryValue = (name, _parameters, value) =>
            name === "getHandoffChange" ? JSON.stringify(invalid) : value;
          await read.fresh();
          expect(store.pending(change.handoffId)).toBeDefined();
        }
        options.queryError = {
          apiName: "getHandoffChange",
          status: 404,
          errorCode: "NOT_FOUND",
          errorName: "QueryVersionNotFound",
        };
        await read.fresh();
        expect(store.pending(change.handoffId)).toBeDefined();
        // No new command is sent while checking the earlier one.
        await store.submit(data, "budget", "120000");
        options.queryError = undefined;
        options.queryValue = (name, _parameters, value) =>
          name === "getHandoffChange" ? JSON.stringify(receipt) : value;
        await read.fresh();
        expect(store.pending(change.handoffId)).toBeUndefined();
        expect(store.notice(change.handoffId)).toBe("Your change was saved.");
        expect(requests.filter((request) => request.url.includes("/actions/"))).toHaveLength(1);
        expect(requests.filter((request) => request.url.includes("/queryTypes/"))).toHaveLength(0);
        for (const request of requests.filter((request) => request.url.includes("/queries/"))) {
          expectQueryRequests([request], new URL(request.url).pathname.split("/").slice(-2)[0]);
        }
        const last = requests
          .slice(-2)
          .map((request) => new URL(request.url).pathname.split("/").slice(-2)[0]);
        expect(last).toEqual(["getHandoffChange", "getHandoffWorkspace"]);
      } finally {
        store.dispose();
      }
    },
  );
  it.each(["budget", "accept"] as const)(
    "sends only the %s fields with lossless strings and no caller identity",
    async (kind) => {
      const { gateway, requests } = localTransport();
      expect(await gateway.apply({ ...change, kind })).toBe("saved");
      expect(requests).toHaveLength(2);
      const apiName = kind === "budget" ? "change-handoff-work-plan" : "accept-handoff-work-plan";
      expect(new URL(requests[0].url).pathname).toBe(
        `/api/v2/ontologies/${settings.ontologyRid}/actionTypes/${apiName}`,
      );
      expect(requests[0].method).toBe("GET");
      expect(new URL(requests[1].url).pathname).toBe(
        `/api/v2/ontologies/${settings.ontologyRid}/actions/${apiName}/apply`,
      );
      expect(requests[1].method).toBe("POST");
      for (const request of requests) {
        expect([...new URL(request.url).searchParams.entries()]).toEqual([]);
      }
      expect(await requests[1].json()).toEqual({
        parameters: {
          workPlanId: change.workPlanId,
          expectedRevision: change.expectedRevision,
          commandId: change.commandId,
          ...(kind === "budget" ? { budgetCents: change.budgetCents } : {}),
        },
        options: { mode: "VALIDATE_AND_EXECUTE", returnEdits: "NONE" },
      });
    },
  );
  it.each(["budget", "accept"] as const)(
    "recognizes a %s rejection from its own function at whatever release is live",
    async (kind) => {
      expect(settings.functionVersion).toBeUndefined();
      expect(settings.actionFunctionVersion).toBeUndefined();
      const errorFunction =
        kind === "budget" ? settings.changeFunctionRid : settings.acceptFunctionRid;
      const known = localTransport({ errorFunction });
      expect(await known.gateway.apply({ ...change, kind })).toBe("rejected");
      for (const wrongFunction of [
        "another-function",
        kind === "budget" ? settings.acceptFunctionRid : settings.changeFunctionRid,
      ]) {
        const unknown = localTransport({ errorFunction: wrongFunction });
        await expect(unknown.gateway.apply({ ...change, kind })).rejects.toBeDefined();
      }
      for (const errorVersion of ["1.6.0", "1.7.6", "1.8.0"]) {
        const live = localTransport({ errorFunction, errorVersion });
        expect(await live.gateway.apply({ ...change, kind })).toBe("rejected");
      }
      // Reads carry no version: they run the newest published release.
      await known.gateway.list();
      await known.gateway.workspace(change.handoffId);
      await known.gateway.receipt(change.handoffId, change.commandId);
      reads.forEach(({ apiName }, index) =>
        expectQueryRequests([known.requests[index + 2]], apiName),
      );
    },
  );
  it.each(["budget", "accept"] as const)(
    "keeps %s rejection matching separate from reads with distinct configured versions",
    async (kind) => {
      expect(distinctVersions.actionFunctionVersion).not.toBe(distinctVersions.functionVersion);
      const errorFunction =
        kind === "budget" ? distinctVersions.changeFunctionRid : distinctVersions.acceptFunctionRid;
      const known = localTransport(
        { errorFunction, errorVersion: distinctVersions.actionFunctionVersion },
        distinctVersions,
      );
      expect(await known.gateway.apply({ ...change, kind })).toBe("rejected");
      const unknown = localTransport(
        { errorFunction, errorVersion: distinctVersions.functionVersion },
        distinctVersions,
      );
      await expect(unknown.gateway.apply({ ...change, kind })).rejects.toBeDefined();
      await known.gateway.list();
      await known.gateway.workspace(change.handoffId);
      await known.gateway.receipt(change.handoffId, change.commandId);
      reads.forEach(({ apiName }, index) =>
        expectQueryRequests([known.requests[index + 2]], apiName, distinctVersions.functionVersion),
      );
    },
  );
  it("uses the read version for rejection matching only when no separate action version is configured", async () => {
    const options = {
      errorFunction: distinctVersions.changeFunctionRid,
      errorVersion: distinctVersions.functionVersion,
    };
    const { gateway } = localTransport(options, {
      ...distinctVersions,
      actionFunctionVersion: undefined,
    });
    expect(await gateway.apply(change)).toBe("rejected");
    const { gateway: separate } = localTransport(options, distinctVersions);
    await expect(separate.apply(change)).rejects.toBeDefined();
  });
  it.each(["budget", "accept"] as const)(
    "clears a definitive first %s rejection but keeps uncertainty after an exact retry",
    async (kind) => {
      const errorFunction =
        kind === "budget" ? settings.changeFunctionRid : settings.acceptFunctionRid;
      for (const lostActionResponse of [false, true]) {
        const options: TransportOptions = { errorFunction, lostActionResponse };
        const { gateway, data, requests } = localTransport(options);
        const storage = memoryStorage();
        const store = new HandoffStore(gateway, storage, "rejection-check", 0);
        try {
          await store.workspace(change.handoffId).fresh();
          await store.submit(data, kind, kind === "budget" ? "110050" : undefined);
          if (lostActionResponse) {
            const reference = store.pending(change.handoffId)!.reference;
            options.lostActionResponse = false;
            await store.replay(change.handoffId);
            expect(store.pending(change.handoffId)?.reference).toEqual(reference);
            expect(store.pending(change.handoffId)?.status).toBe("checking");
            expect(store.notice(change.handoffId)).toBeUndefined();
            const actions = requests.filter((request) => request.url.includes("/actions/"));
            expect(actions).toHaveLength(2);
            expect(await actions[1].json()).toEqual(await actions[0].json());
          } else {
            expect(store.pending(change.handoffId)).toBeUndefined();
            expect(store.notice(change.handoffId)).toBe(
              "Your change wasn't saved. Review the latest work plan before trying again.",
            );
            expect(JSON.parse(storage.getItem("rejection-check")!).pending).toEqual([]);
            expect(requests.filter((request) => request.url.includes("/actions/"))).toHaveLength(1);
          }
          for (const request of requests.filter((request) => request.url.includes("/queries/"))) {
            expectQueryRequests([request], new URL(request.url).pathname.split("/").slice(-2)[0]);
          }
        } finally {
          store.dispose();
        }
      }
    },
  );
  it("reads the returned original document through the installed public media SDK", async () => {
    const { gateway, requests } = localTransport();
    const workspace = await gateway.workspace(change.handoffId);
    const blob = await gateway.document(workspace.documents[1]);
    expect(blob.type).toBe("application/pdf");
    expect(await blob.text()).toBe("%PDF-1.7\nOriginal document");
    expect(requests).toHaveLength(2);
    expect(new URL(requests[1].url).pathname).toBe(
      "/api/v2/mediasets/media-set/items/media-item/content",
    );
  });
});
