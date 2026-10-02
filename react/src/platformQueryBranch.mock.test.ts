import { type Client, createClient } from "@osdk/client";
import { Ontologies } from "@osdk/foundry";
import { isDeepStrictEqual } from "node:util";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

/**
 * TEST-ONLY protocol investigation. No app imports/exports or deployed resource
 * definitions. All query metadata, parameters and DTOs below are FICTIONAL.
 * Nothing here proves server branch resolution, OAuth permissions or the actual
 * getCloseoutWorkspace contract. Do not import this harness into application code.
 *
 * Uses the existing public @osdk/foundry export (installed umbrella 2.78.0),
 * not private client APIs, hand-written QueryDefinitions, patched SDK internals,
 * raw service endpoints, guessed headers, or a generated-SDK replacement.
 * Every request uses a local mock and a reserved .invalid origin. Global fetch
 * is separately disabled. No auth module, environment files or tokens are read.
 */
const target = Object.freeze({
  origin: "https://platform-query-protocol-test.invalid",
  ontology: "ri.ontology.main.ontology.cfb1478a-5b0e-466a-aaff-b212870e8861",
  branch: "ri.branch..branch.87c301c3-efd5-43cd-a108-fb39679dd63b",
  apiName: "localMockWorkspaceQuery",
  functionRid: "local-mock-function-not-deployed",
  version: "0.0.0-local-protocol-test.1",
});
const parameters = Object.freeze({
  caseId: "local-mock-case",
  environmentId: "DC_PHASE_C_SYNTHETIC",
  managementCompanyId: "constructed-company-001",
});
const prefix = `/api/v2/ontologies/${target.ontology}`;
const listPath = `${prefix}/queryTypes`;
const getPath = `${listPath}/${target.apiName}`;
const executePath = `${prefix}/queries/${target.apiName}/execute`;
interface MockWorkspaceDto {
  schemaVersion: "local-workspace-v1";
  caseId: string;
  environmentId: string;
  managementCompanyId: string;
  mode: "SIMULATED";
  totalMinor: string;
}
const dto: Readonly<MockWorkspaceDto> = Object.freeze({
  schemaVersion: "local-workspace-v1",
  ...parameters,
  mode: "SIMULATED",
  totalMinor: "12345",
});
const queryMetadata: Ontologies.QueryTypeV2 = {
  apiName: target.apiName,
  rid: target.functionRid,
  version: target.version,
  parameters: Object.fromEntries(
    Object.keys(parameters).map((name) => [name, { dataType: { type: "string" }, required: true }]),
  ),
  output: {
    type: "struct",
    fields: Object.keys(dto).map((name) => ({ name, fieldType: { type: "string" } })),
  },
  typeReferences: {},
};
const unrelatedMetadata: Ontologies.QueryTypeV2 = {
  ...queryMetadata,
  apiName: "localUnrelatedQuery",
  rid: "local-unrelated-function-not-deployed",
};

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
function assertBinding(branch: string | undefined, version: string | undefined) {
  if (branch !== target.branch || version !== target.version) {
    throw new Error("Local harness rejected branch or exact version");
  }
}
function assertMetadata(value: unknown) {
  if (
    !record(value) ||
    value.apiName !== target.apiName ||
    value.rid !== target.functionRid ||
    value.version !== target.version ||
    !isDeepStrictEqual(value.parameters, queryMetadata.parameters) ||
    !isDeepStrictEqual(value.output, queryMetadata.output) ||
    !isDeepStrictEqual(value.typeReferences, queryMetadata.typeReferences)
  ) {
    throw new Error("Local harness rejected metadata identity/version/schema");
  }
}
function parseDto(value: unknown): typeof dto {
  if (
    !record(value) ||
    !isDeepStrictEqual(Object.keys(value).sort(), Object.keys(dto).sort()) ||
    value.schemaVersion !== dto.schemaVersion ||
    value.caseId !== parameters.caseId ||
    value.environmentId !== parameters.environmentId ||
    value.managementCompanyId !== parameters.managementCompanyId ||
    value.mode !== "SIMULATED" ||
    typeof value.totalMinor !== "string" ||
    !/^-?(0|[1-9][0-9]*)$/.test(value.totalMinor) ||
    value.totalMinor.length > 20
  ) {
    throw new Error("Local harness rejected DTO schema or scope");
  }
  // Reconstruct validated data; never cast arbitrary Platform DataValue to a DTO.
  return {
    schemaVersion: value.schemaVersion,
    caseId: value.caseId,
    environmentId: value.environmentId,
    managementCompanyId: value.managementCompanyId,
    mode: value.mode,
    totalMinor: value.totalMinor,
  };
}

/**
 * Deliberately bounded, per-invocation discovery; no metadata cache, automatic
 * retries, fallback to Main, or fallback to a different function version.
 * list returns LATEST metadata, not metadata for an arbitrary historical pin.
 * This list-only prototype therefore fails closed if latest differs from pin.
 */
async function discoverFromList(client: Client) {
  const seenTokens = new Set<string>();
  let pageToken: string | undefined;
  let match: unknown;
  for (let page = 0; page < 4; page += 1) {
    const result: unknown = await Ontologies.QueryTypes.list(client, target.ontology, {
      branch: target.branch,
      pageSize: 2,
      pageToken,
    });
    if (!record(result) || !Array.isArray(result.data)) {
      throw new Error("Local harness rejected metadata page");
    }
    for (const entry of result.data as unknown[]) {
      if (!record(entry)) {
        throw new Error("Local harness rejected metadata entry");
      }
      if (entry.apiName === target.apiName || entry.rid === target.functionRid) {
        assertMetadata(entry);
        if (match !== undefined) {
          throw new Error("Local harness rejected duplicate metadata identity");
        }
        match = entry;
      }
    }
    if (result.nextPageToken === undefined) {
      if (match === undefined) {
        // Absent and permission-filtered are intentionally indistinguishable.
        throw new Error("Local harness query unavailable; no fallback");
      }
      return;
    }
    if (
      typeof result.nextPageToken !== "string" ||
      result.nextPageToken.length === 0 ||
      result.data.length === 0 ||
      seenTokens.has(result.nextPageToken)
    ) {
      throw new Error("Local harness rejected pagination");
    }
    seenTokens.add(result.nextPageToken);
    pageToken = result.nextPageToken;
  }
  throw new Error("Local harness metadata page budget exceeded");
}

async function runListThenExecute(
  client: Client,
  branch: string | undefined = target.branch,
  version: string | undefined = target.version,
) {
  assertBinding(branch, version);
  await discoverFromList(client);
  const response: unknown = await Ontologies.Queries.execute(
    client,
    target.ontology,
    target.apiName,
    { parameters },
    { branch: target.branch, version: target.version },
  );
  if (!record(response) || !isDeepStrictEqual(Object.keys(response), ["value"])) {
    throw new Error("Local harness rejected execution envelope");
  }
  return parseDto(response.value);
}

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
interface MockOptions {
  pages?: unknown[];
  listFailurePage?: number;
  listFailureStatus?: number;
  executeStatus?: number;
  executeBody?: unknown;
  getBody?: unknown;
}
function setup(options: MockOptions = {}) {
  const pages = options.pages ?? [{ data: [queryMetadata] }];
  const attempts: Request[] = [];
  const requests: Request[] = [];
  let pageIndex = 0;
  // Validation-only mock gate. It never rewrites the SDK request or forwards it.
  const transport = vi.fn<typeof fetch>(async (input, init) => {
    const request = new Request(input, init);
    attempts.push(request);
    const url = new URL(request.url);
    if (
      url.origin !== target.origin ||
      url.searchParams.getAll("branch").length !== 1 ||
      url.searchParams.get("branch") !== target.branch
    ) {
      throw new Error("Local mock denied Main, missing branch or wrong branch");
    }
    const list = request.method === "GET" && url.pathname === listPath;
    const get = request.method === "GET" && url.pathname === getPath;
    const execute = request.method === "POST" && url.pathname === executePath;
    const allowedKeys = list ? ["branch", "pageSize", "pageToken"] : ["branch", "version"];
    if (
      (!list && !get && !execute) ||
      [...url.searchParams.keys()].some((key) => !allowedKeys.includes(key)) ||
      (!list &&
        (url.searchParams.getAll("version").length !== 1 ||
          url.searchParams.get("version") !== target.version))
    ) {
      throw new Error("Local mock denied endpoint or unpinned version");
    }
    if (execute && !isDeepStrictEqual(await request.clone().json(), { parameters })) {
      throw new Error("Local mock denied parameters");
    }
    requests.push(request);
    if (list) {
      const index = pageIndex++;
      if (index === options.listFailurePage) {
        return json(
          { errorCode: "PERMISSION_DENIED", errorName: "PermissionDenied" },
          options.listFailureStatus ?? 403,
        );
      }
      if (index >= pages.length) {
        throw new Error("Local mock exhausted pages; no network fallback");
      }
      return json(pages[index]);
    }
    if (get) {
      return json(options.getBody ?? queryMetadata);
    }
    return json(options.executeBody ?? { value: dto }, options.executeStatus ?? 200);
  });
  const tokenProvider = vi.fn(async () => "local-mock-not-an-oauth-token");
  const client = createClient(
    target.origin,
    target.ontology,
    tokenProvider,
    { UNSTABLE_DO_NOT_USE_BRANCH: target.branch },
    transport,
  );
  return { client, transport, requests, attempts, tokenProvider };
}

beforeEach(() => {
  vi.stubGlobal(
    "fetch",
    vi.fn(() => {
      throw new Error("Live network forbidden in protocol investigation");
    }),
  );
});
afterEach(() => {
  expect(globalThis.fetch).not.toHaveBeenCalled();
  vi.unstubAllGlobals();
});

describe("PUBLIC Platform query APIs: isolated branch + pinned-version protocol", () => {
  it("uses the existing OSDK Client as SharedClient, with no hidden metadata fetch", async () => {
    const mock = setup();
    await expect(runListThenExecute(mock.client)).resolves.toEqual(dto);
    expect(mock.tokenProvider).toHaveBeenCalled();
    expect(mock.requests.map((request) => [request.method, new URL(request.url).pathname])).toEqual(
      [
        ["GET", listPath],
        ["POST", executePath],
      ],
    );
    for (const request of mock.requests) {
      expect(new URL(request.url).searchParams.getAll("branch")).toEqual([target.branch]);
    }
    const execution = mock.requests[1];
    expect(new URL(execution.url).searchParams.getAll("version")).toEqual([target.version]);
    expect(await execution.json()).toEqual({ parameters });
  });

  it("follows smaller pages, filters unrelated metadata, then executes the exact pin", async () => {
    const mock = setup({
      pages: [
        { data: [unrelatedMetadata], nextPageToken: "local-second-page" },
        { data: [queryMetadata] },
      ],
    });
    await expect(runListThenExecute(mock.client)).resolves.toEqual(dto);
    expect(mock.requests).toHaveLength(3);
    expect(new URL(mock.requests[0].url).searchParams.has("pageToken")).toBe(false);
    expect(new URL(mock.requests[1].url).searchParams.get("pageToken")).toBe("local-second-page");
    expect(new URL(mock.requests[1].url).searchParams.get("branch")).toBe(target.branch);
  });

  it.each([
    ["empty", [{ data: [] }]],
    [
      "absent or permission-filtered",
      [{ data: [unrelatedMetadata], nextPageToken: "next" }, { data: [] }],
    ],
  ])("stops when query is %s; never tries get, execute or Main", async (_label, pages) => {
    const mock = setup({ pages });
    await expect(runListThenExecute(mock.client)).rejects.toThrow("query unavailable");
    expect(mock.requests).toHaveLength(pages.length);
    expect(mock.requests.every((request) => new URL(request.url).pathname === listPath)).toBe(true);
  });

  it.each([401, 403])("stops on metadata HTTP %s without execution or fallback", async (status) => {
    const mock = setup({
      pages: [{ data: [unrelatedMetadata], nextPageToken: "next" }],
      listFailurePage: 1,
      listFailureStatus: status,
    });
    await expect(runListThenExecute(mock.client)).rejects.toThrow();
    expect(mock.attempts).toHaveLength(2);
    expect(mock.requests.every((request) => new URL(request.url).pathname === listPath)).toBe(true);
  });

  it.each([401, 403, 404])(
    "stops on execution HTTP %s; does not retry a different version",
    async (status) => {
      const mock = setup({
        executeStatus: status,
        executeBody: { errorCode: "PERMISSION_DENIED", errorName: "PermissionDenied" },
      });
      await expect(runListThenExecute(mock.client)).rejects.toThrow();
      expect(mock.attempts).toHaveLength(2);
    },
  );

  it.each(["", " ", "main", "master", "ri.branch..branch.local-wrong-branch"])(
    "rejects branch %j before discovery",
    async (branch) => {
      const mock = setup();
      await expect(runListThenExecute(mock.client, branch)).rejects.toThrow(
        "branch or exact version",
      );
      expect(mock.attempts).toHaveLength(0);
    },
  );

  it.each([undefined, "", "main", "ri.branch..branch.local-wrong-branch"])(
    "denies raw Platform list/execute branch %j at mock transport",
    async (branch) => {
      const mock = setup();
      await expect(
        Ontologies.QueryTypes.list(mock.client, target.ontology, { branch }),
      ).rejects.toThrow("denied Main");
      await expect(
        Ontologies.Queries.execute(
          mock.client,
          target.ontology,
          target.apiName,
          { parameters },
          { branch, version: target.version },
        ),
      ).rejects.toThrow("denied Main");
      expect(mock.requests).toHaveLength(0);
    },
  );

  it("does NOT inherit client branch when Platform query parameters omit it", async () => {
    const mock = setup();
    await expect(Ontologies.QueryTypes.list(mock.client, target.ontology)).rejects.toThrow(
      "denied Main",
    );
    expect(new URL(mock.attempts[0].url).searchParams.has("branch")).toBe(false);
  });

  it.each([undefined, "", "latest", "^0.0.0", "0.0.0-local-protocol-test.2"])(
    "rejects missing/unpinned/wrong execute version %j",
    async (version) => {
      const mock = setup();
      await expect(
        Ontologies.Queries.execute(
          mock.client,
          target.ontology,
          target.apiName,
          { parameters },
          { branch: target.branch, version },
        ),
      ).rejects.toThrow("unpinned version");
      expect(mock.requests).toHaveLength(0);
    },
  );

  it.each([
    ["RID mismatch", { rid: "wrong-local-rid" }],
    ["API name mismatch", { apiName: "differentLocalName" }],
    ["latest differs from pin", { version: "0.0.0-local-protocol-test.2" }],
    [
      "parameter schema",
      { parameters: { caseId: { dataType: { type: "integer" }, required: true } } },
    ],
    ["output schema", { output: { type: "string" } }],
    ["unreviewed type references", { typeReferences: { unexpected: { type: "string" } } }],
  ])("rejects metadata %s before executing", async (_label, change) => {
    const mock = setup({ pages: [{ data: [{ ...queryMetadata, ...change }] }] });
    await expect(runListThenExecute(mock.client)).rejects.toThrow(
      "metadata identity/version/schema",
    );
    expect(mock.attempts).toHaveLength(1);
  });

  it.each([
    ["missing data", {}],
    ["non-array data", { data: {} }],
    ["null entry", { data: [null] }],
    ["duplicate identity", { data: [queryMetadata, queryMetadata] }],
    ["empty continuation", { data: [], nextPageToken: "unexpected" }],
    ["non-string token", { data: [unrelatedMetadata], nextPageToken: 123 }],
  ])("rejects malformed list response: %s", async (_label, page) => {
    const mock = setup({ pages: [page] });
    await expect(runListThenExecute(mock.client)).rejects.toThrow("Local harness rejected");
    expect(mock.attempts).toHaveLength(1);
  });

  it("rejects cyclic pagination without executing", async () => {
    const page = { data: [unrelatedMetadata], nextPageToken: "same-token" };
    const mock = setup({ pages: [page, page] });
    await expect(runListThenExecute(mock.client)).rejects.toThrow("pagination");
    expect(mock.attempts).toHaveLength(2);
  });

  it("bounds metadata enumeration; partial discovery is not permission to execute", async () => {
    const mock = setup({
      pages: Array.from({ length: 4 }, (_, index) => ({
        data: [index === 0 ? queryMetadata : unrelatedMetadata],
        nextPageToken: `local-page-${index + 1}`,
      })),
    });
    await expect(runListThenExecute(mock.client)).rejects.toThrow("page budget");
    expect(mock.attempts).toHaveLength(4);
  });

  it.each([
    ["wrong schema version", { ...dto, schemaVersion: "unknown" }],
    ["wrong case", { ...dto, caseId: "another-case" }],
    ["wrong environment", { ...dto, environmentId: "MAIN" }],
    ["wrong company", { ...dto, managementCompanyId: "another-company" }],
    ["wrong mode", { ...dto, mode: "LIVE" }],
    ["unsafe number instead of string", { ...dto, totalMinor: 12345 }],
    ["invalid minor units", { ...dto, totalMinor: "12.34" }],
    ["extra field", { ...dto, extra: true }],
    ["missing fields", { schemaVersion: dto.schemaVersion }],
    ["array instead of DTO", [dto]],
    ["null", null],
  ])("rejects result %s without OSDK coercion or fallback", async (_label, value) => {
    const mock = setup({ executeBody: { value } });
    await expect(runListThenExecute(mock.client)).rejects.toThrow("DTO schema or scope");
    expect(mock.attempts).toHaveLength(2);
  });

  it("rejects an unexpected response envelope", async () => {
    const mock = setup({ executeBody: { result: dto } });
    await expect(runListThenExecute(mock.client)).rejects.toThrow("execution envelope");
  });

  it("2.78 PUBLIC get supports exact branch+version metadata without list's latest-only constraint", async () => {
    const mock = setup();
    const metadata: unknown = await Ontologies.QueryTypes.get(
      mock.client,
      target.ontology,
      target.apiName,
      { branch: target.branch, version: target.version },
    );
    assertMetadata(metadata);
    const response = await Ontologies.Queries.execute(
      mock.client,
      target.ontology,
      target.apiName,
      { parameters },
      { branch: target.branch, version: target.version },
    );
    expect(parseDto(response.value)).toEqual(dto);
    expect(mock.requests.map((request) => new URL(request.url).pathname)).toEqual([
      getPath,
      executePath,
    ]);
    expect(new URL(mock.requests[0].url).searchParams.get("version")).toBe(target.version);
    expect(new URL(mock.requests[0].url).searchParams.get("branch")).toBe(target.branch);
  });
});
