# Deposit Closeout — TypeScript v2 case workflow

## Current branch status — Phase E.1 backend only

As of 2026-09-20, **Main remains on 1.2**. This branch adds `getCloseoutWorkspace` and the eight-field compact case queue without changing the three existing query contracts, thirty Action interfaces or native/lifecycle logic. The user-approved sequence is backend first: user merge before frontend SDK/query integration resumes; no frontend changes are included in the backend proposal and no Main data is seeded.

The accepted logic is `159fcf1fee43264fd2014d1d72977dfe1c0d3649`, published as branch tag `1.3.0-branch-20260920-213828` (tag CI passed): **1,107 native tests passed, five unchanged skips, 34 Functions, zero diagnostics**. Fifteen actual E-branch Action submissions produced 13 applied commands, one zero-edit replay and one stale rejection without a receipt; actual stored query previews also passed. This is backend acceptance, **not browser or published-query HTTP acceptance**. `docs/phase_e.md` records the exact cases, SQL null/microsecond checks, hashes, Main-zero isolation and remaining consumer gate. After merge confirmation, verify Main 1.3/new query schema and regenerate the frontend SDK from Main definitions before continuing the already-approved full UI validation on a fresh global branch; no additional GO or Main seed is needed.

## Phase D baseline: explicit simulated lifecycle

The current workflow combines the unchanged native review, guarded stored cases, and an **explicit v2 simulated lifecycle**. It prepares immutable structured statements and exact rendered text, records exact-intent approval decisions, reserves and claims operation requests, and separately generates and accepts simulated results. Supported operations are statement dispatch, charge posting, deposit application, refund, and targeted posting/application reversals. There is no PDF engine or live statement, ledger or payment transport.

Phase D provides **30 named edit functions/Actions** (15 retained case operations and 15 lifecycle operations) and **three existing queries**; Phase E.1 adds a fourth query on the branch. The eight case types remain in use: `DcCloseoutCase`, `DcReviewSnapshot`, `DcExecutionEvent`, `DcChargeItem`, `DcEvidenceRecord`, `DcMoneyEvent`, `DcCaseParty`, and `DcRequirement`. Phase D adds `DcStatementVersion`, `DcApproval`, and `DcActionRequest`, for eleven types total.

All stored operations share the case persistence boundary: create a root on opening, or update the same loaded root once for an existing case, and write its snapshot, command receipt and all projections in one edit batch. Authorized exact command replay returns no edits; conflicting command reuse and stale revisions fail. Request identity additionally prevents a different command ID from creating the same economic instruction twice. Neither a request, a claim, nor a raw simulated result means performance: only validated result ingestion contributes accepted native facts.

- **Operating guide and recovery:** `docs/phase_d.md`.
- **Current configuration and limits:** `docs/tsv2_release_manifest.json`.
- **Retained case interface and its phase-specific acceptance record:** `docs/phase_c.md`. Its Phase C boundary is not a statement that v2 lifecycle features are absent today.
- Named wrappers: `typescript-functions/src/functions/`.
- Shared case persistence and case commands: `typescript-functions/src/deposit_closeout/phase_c/`.
- Workflow contracts, reducers, projections and simulator: `typescript-functions/src/deposit_closeout/lifecycle/`; `types.ts` and `codec.ts` are the canonical payload definitions.

## Use the appropriate review interface

| Query | Input | Returned JSON string |
| --- | --- | --- |
| `reviewDepositCloseout` | Strict `ReviewRequest` 1.0.0 JSON with an explicit review clock | Standalone base `ReviewEnvelope` 1.1.0; read-only, no storage |
| `getCloseoutReview` | Policy-visible `closeoutCase` object | Validated stored base `ReviewEnvelope` 1.1.0, retaining its recorded clock |
| `getCloseoutWorkflow` | Scalar `caseId`, loaded server-side | Explicit `WorkflowReviewV2`; initialize the case workflow first |
| `getCloseoutWorkspace` (Phase E.1 branch only) | Scalar `caseId`, optional strict `intentSpecJson` | `CloseoutWorkspaceV1` 1.0.0 with request, assignments, workflow or null, discriminated review and non-authorizing intent preview; see `docs/phase_e.md` |

The base review retains six result fields: `scopeRequirements`, `itemDecisions`, `account`, `missingInputs`, `actions`, and `outcomes`. The v2 review enriches account commitments, action details and simulated outcomes; it does **not** relabel the base envelope. Its `metadata.workflowSchemaVersion` is `2.0.0`, while `metadata.schemaVersion` remains `1.1.0` and `metadata.codeVersion` remains `phase-b.1`.

The standalone entry point remains `typescript-functions/src/functions/reviewDepositCloseout.ts`, with pure logic under `typescript-functions/src/deposit_closeout/domain/` and adjacent `resources/` and `__tests__/`. It uses the caller's explicit review clock, not the host clock. Input hashes, item fingerprints and supplied evidence/history support deterministic review; no lifecycle initialization or stored case is needed for this interface.

Open a constructed case through the existing bootstrap Action at revision 1, then call `initializeCloseoutWorkflow` with `payloadJson` equal to `"{}"` before other v2 commands. Do not manufacture an unscoped case ID: use the company/ending-tenancy identity helper described in `docs/phase_d.md`. Existing case Actions continue to work; for initialized cases their shared persistence path also reconciles v2 state. Separate statement and refund instructions allow statement work without certifying refund routing. Zero refund means no refund request, not a zero-dollar payment.

## Storage, clocks and safety

- Initialized roots carry `workflowVersion = "2"` and retain `projectionVersion = "1"`. Snapshots retain base `requestJson`/`reviewJson` and add fully typed workflow state/review JSON with separate hashes. Historical workflow equality is checked at the snapshot's recorded `createdAt`, not today's clock.
- Actual actors are bound server-side by the Action's `current_user_id`, never by form input. Scope, readership and current authority are checked at actual server time. A future synthetic business clock does not confer authority. Version-two case rechecks preserve the workflow's non-rewinding business clock; standalone and uninitialized case interfaces retain their own clock behavior.
- Cents are bounded exact integer JSON numbers; native monetary aggregation uses BigInt with checked conversion. Unknown amounts remain explicit `null`, never guessed zero. Financial capacity is constrained by both unpaid liability and verified held cash less other commitments; a pending reversal is not spendable cash.
- JSON is UTF-8 bounded at 256 KiB (workflow JSON must be strictly below the bound); each projection family is capped at 1,000 rows. Over-limit operations fail closed, without truncation. Source timestamps retain exact UTC microseconds; stored review clocks require exact milliseconds or coarser.
- Frozen statement content, approval materiality, full-review hashes and financial identity are distinct. Normal accepted performance does not invalidate the approval it implements. Material corrections preserve earlier issued content and transactions, using linked new versions, explicit positive reversals and replacement instructions where permitted.

**Constructed-only scope:** `constructed-company-001`, approved operator `c47a52a0-0048-4607-931f-f4df283ae7c4`, and stable environment identity `DC_PHASE_C_SYNTHETIC`. The environment name is intentionally unchanged. Read policies cover whole records, including JSON, but the Handoff project has broad Owner access within the organization; this is not production multi-principal isolation certification.

Only the bundled `NC_SYNTHETIC_REVIEW_V1` release is accepted; all legal review cards remain `PENDING`. `depositComplete`, `overallCaseComplete` and `legalPerformanceConfirmed` stay **false**. `simulatedDepositWorkflowComplete` and `simulatedOverallWorkflowComplete` are derived and can become true in `SIMULATED` mode. This is not legal performance, a 30/60-day legal finding, proof of external execution, or provider exactly-once delivery. There are no live connectors, models or automations, and no UI delivery is included in this backend scope. Phase E is branch-only as recorded above; no Main seeding or Phase E merge has occurred. The standalone core remains read-only; review action recommendations do not execute operations.

## Validation reference and development checks

Inherited Phase D validation: logic commit `b37873960e251e4c2aa644313d89e5a968475c75`, branch Function tag `1.2.0-branch-20260920-041008`, tagged CI passed; 959 native tests passed and five unchanged template examples were skipped. This identifies the tested logic, not a later documentation tag or a Main deployment. All 15 new lifecycle Actions were exercised through actual Actions, along with selected inherited case bridges—not every inherited Action or every native matrix variant under Phase D. `docs/phase_d.md` separates these observations from untested production claims.

```sh
cd typescript-functions
npm test
npx tsc --noEmit -p src/tsconfig.json
```

From the repository root, `./rune discover` checks function discovery. Local-SDK mode remains `useSdkSidebar: false`. `node tools/prepare_ts_demo.mjs` creates two constructed inputs under ignored `build/tsv2-demo/` for standalone read-only Rune previews; it does not open or initialize a stored workflow. See `AGENTS.md` for tooling setup. The general TypeScript reference below describes platform capabilities, not additional delivered closeout features.

---

## TypeScript Functions

### Overview
Functions enable code authors to write logic that can be executed quickly in operational contexts, such as dashboards and applications designed to empower decision-making processes. This logic is executed on the server side in an isolated environment.

### Getting Started
To begin writing a TypeScript Function, navigate to the `typescript-functions/src/functions` directory within the repository and create a new file. The following example is written in a file called `helloWorld.ts` and returns a message represented as a `string`:

```typescript
// typescript-functions/src/functions/helloWorld.ts

function helloWorld(): string {
    return "Hello World!";
}

export default helloWorld;
```

This may also be written as an arrow function:

```typescript
// typescript-functions/src/functions/helloWorld.ts

const helloWorld = (): string => {
    return "Hello World!";
};

export default helloWorld;
```

Note that in both examples, the function is exported using the `export default` syntax. This is a requirement to have the function registered and made available to other Foundry applications. The Function name must also match the file name: `helloWorld.ts` should define and default-export `helloWorld`. Renaming or moving the file changes the published Function identity.

Functions within the same file that are not the default export will remain private:
Note that in both examples, the function is exported using the `export default` syntax. This is a requirement to have the function registered and made available to other Foundry applications. The Function name must also match the file name: `helloWorld.ts` should define and default-export `helloWorld`. Renaming or moving the file changes the published Function identity.

Functions within the same file that are not the default export will remain private:

```typescript
// typescript-functions/src/functions/helloWorld.ts

function getRandomValue(array: string[]): string {
    const randomIndex = Math.floor(Math.random() * array.length);
    return array[randomIndex];
}

function helloWorld(): string {
    return getRandomValue(["Hello World!", "Hola!"]);
}

export default helloWorld;
```

### Primitive Types

A TypeScript Function must explicitly declare the types of its input and output parameters. The examples below cover common types used in Functions; see the [Functions type reference](https://www.palantir.com/docs/foundry/functions/types-reference/) for the full supported set and language-specific caveats.

#### Integer
Represents integer values from `-2,147,483,648` to `2,147,483,647` inclusive. If a Function receives an input or returns an output outside of this precision, an error will be thrown.

```typescript
// typescript-functions/src/functions/sum.ts

import { Integer } from "@osdk/functions";

function sum(a: Integer, b: Integer): Integer {
    return a + b;
}

export default sum;
```

#### Long
Represents integer values from `Number.MIN_SAFE_INTEGER` (`−9,007,199,254,740,991`) to `Number.MAX_SAFE_INTEGER` (`9,007,199,254,740,991`) inclusive. If a Function receives an input or returns an output outside of this precision, an error will be thrown.

```typescript
// typescript-functions/src/functions/subtract.ts

import { Long } from "@osdk/functions";

function subtract(a: Long, b: Long): Long {
    return (BigInt(a) - BigInt(b)).toString();
}

export default subtract;
```

#### Double
Represents an IEEE 754 64-bit floating point number.

```typescript
// typescript-functions/src/functions/multiply.ts

import { Double } from "@osdk/functions";

function multiply(a: Double, b: Double): Double {
    return a * b;
}

export default multiply;
```

#### String
```typescript
// typescript-functions/src/functions/greet.ts

function greet(name: string): string {
    return `Hello, ${name}!`;
}

export default greet;
```

#### Boolean
```typescript
// typescript-functions/src/functions/isEven.ts

import { Integer } from "@osdk/functions";

function isEven(num: Integer): boolean {
    return num % 2 === 0;
}

export default isEven;
```

#### Date
Represents a date as a string in YYYY-MM-DD format. If the function receives or returns a date that is not in this format, an error will be thrown.

```typescript
// typescript-functions/src/functions/returnDate.ts

import { DateISOString } from "@osdk/functions";

function returnDate(): DateISOString {
    return "1999-10-17";
}

export default returnDate;
```

#### Timestamp
Represents an instant in time as an ISO 8601 string. If the function receives or returns a date that is not in this format, an error will be thrown.

```typescript
// typescript-functions/src/functions/getCurrentTimestamp.ts

import { TimestampISOString } from "@osdk/functions";

function getCurrentTimestamp(): TimestampISOString {
    const now = new Date();
    return now.toISOString();
}

export default getCurrentTimestamp;
```

### Composite Types

#### Array
```typescript
// typescript-functions/src/functions/filterForEvenIntegers.ts

import { Integer } from "@osdk/functions";

function filterForEvenIntegers(nums: Integer[]): Integer[] {
    return nums.filter(num => num % 2 === 0);
}

export default filterForEvenIntegers;
```

#### Map
You can use the `Record` built-in TypeScript type to represent a mapping from keys to values.

```typescript
// typescript-functions/src/functions/getRecord.ts

function getRecord(): Record<string, string> {
    const dict: Record<string, string> = {};

    dict["Name"] = "Phil";
    dict["Favorite Color"] = "Blue";
    
    return dict;
}

export default getRecord;
```

You can also key by Ontology objects by accessing the `$objectSpecifier` property of each object.

```typescript
// typescript-functions/src/functions/getObjectMap.ts

import { ObjectSpecifier, Osdk } from "@osdk/client";
import { Integer } from "@osdk/functions";
import { Airplane } from "@ontology/sdk";

function getObjectMap(aircraft: Osdk.Instance<Airplane>[]): Record<ObjectSpecifier<Airplane>, Integer | undefined> {
    const dict: Record<ObjectSpecifier<Airplane>, Integer | undefined> = {};
    
    aircraft.forEach(obj => {
        dict[obj.$objectSpecifier] = obj.capacity;
    });
    
    return dict;
}

export default getObjectMap;
```

#### Custom Type
Custom types can be declared using the `interface` keyword in TypeScript. You can use any of the other supported types as fields:

```typescript
// typescript-functions/src/functions/getPassengerInfo.ts

import { Osdk } from "@osdk/client";
import { Integer } from "@osdk/functions";
import { Passenger } from "@ontology/sdk";

interface PassengerInfo {
    name?: string;
    age?: Integer;
}

function getPassengerInfo(passenger: Osdk.Instance<Passenger>): PassengerInfo {
    return {
        name: passenger.name,
        age: passenger.age,
    };
}

export default getPassengerInfo;
```

#### Two-Dimensional Aggregation
```typescript
import { Double, TwoDimensionalAggregation } from "@osdk/functions";

function myTwoDimensionalAggregationFunction(): TwoDimensionalAggregation<string, Double> {
    return [
        { key: "bucket1", value: 5.0 },
        { key: "bucket2", value: 6.0 },
    ];
}

export default myTwoDimensionalAggregationFunction;
```

#### Three-Dimensional Aggregation
```typescript
import { Double, ThreeDimensionalAggregation } from "@osdk/functions";

function myThreeDimensionalAggregation(): ThreeDimensionalAggregation<string, string, Double> {
    return [
        {
            key: "group-by-1",
            groups: [
                { key: "partition-by-1", value: 5.0 },
                { key: "partition-by-2", value: 6.0 },
            ],
        },
        {
            key: "group-by-2",
            groups: [
                { key: "partition-by-1", value: 7.0 },
                { key: "partition-by-2", value: 8.0 },
            ],
        },
    ];
}

export default myThreeDimensionalAggregation;
```

#### Optional
You can use the `?` token to specify that an input may be undefined:

```typescript
// typescript-functions/src/functions/greet.ts

function greet(name?: string): string {
    if (name === undefined) {
        return `Hello!`;
    }
    return `Hello, ${name}!`;
}

export default greet;
```

You can also provide a default value in the event that callers of your Function do not provide a value for the parameter:
```typescript
// typescript-functions/src/functions/greet.ts

function greet(name: string = "Anonymous"): string {
    return `Hello, ${name}!`;
}

export default greet;
```

#### Promise
Functions that perform asynchronous tasks (such as loading data over the network) can specify a `Promise` return type to indicate that a value will be provided at some point in the future.
```typescript
// typescript-functions/src/functions/loadObject.ts

import { Client } from "@osdk/client";
import { Integer } from "@osdk/functions";
import { Airplane } from "@ontology/sdk";

async function getAirplaneCapacityWithId(client: Client, id: string): Promise<Integer> {
    const response = await client(Airplane).fetchOne(id);
    return response.capacity;
}

export default getAirplaneCapacityWithId;
```

### Ontology SDK
You can use the left sidebar in Authoring to import entities from an Ontology and have an Ontology SDK generated for you within the workspace automatically. You can then import these entities from the `@ontology/sdk` package.

Object and interface types can be used in a TypeScript Function's signature. Using the Ontology SDK, an object or interface instance can be typed as `Osdk.Instance<Airplane>`:

```typescript
// typescript-functions/src/functions/getCapacity.ts

import { Osdk } from "@osdk/client";
import { Integer } from "@osdk/functions";
import { Airplane } from "@ontology/sdk";

function getCapacity(airplane: Osdk.Instance<Airplane>): Integer {
    return airplane.capacity;
}

export default getCapacity;
```

An object set represents an unordered collection of objects. Like individual object and interface instances, object sets can be passed into and returned from a TypeScript Function:

```typescript
// typescript-functions/src/functions/filterAircraft.ts

import { ObjectSet } from "@osdk/client";
import { Airplane } from "@ontology/sdk";

function filterAircraft(aircraft: ObjectSet<Airplane>): ObjectSet<Airplane> {
    return aircraft
        .where({
            capacity: {
                $gt: 200 
            } 
        });
}

export default filterAircraft;
```

To access a full client through which you can perform searches and aggregations across your Ontology, import `Client` from the `@osdk/client` package and provide it as the first parameter to your Function:
```typescript
// typescript-functions/src/functions/getAircraftByIdDescending.ts

import { Client, Osdk } from "@osdk/client";
import { Airplane } from "@ontology/sdk";

// Fetches a page of Airplane objects in descending order by ID.
async function getAircraftByIdDescending(client: Client): Promise<Osdk.Instance<Airplane>[]> {
    const { data } = await client(Airplane).fetchPage({
        $orderBy: {
            id: "desc" 
        } 
    });
    
    return data;
}

export default getAircraftByIdDescending;
```

```typescript
// typescript-functions/src/functions/getNumberOfAircraft.ts

import { Client } from "@osdk/client";
import { Integer } from "@osdk/functions";
import { Airplane } from "@ontology/sdk";

// Gets the total number of aircraft in the Ontology.
async function getNumberOfAircraft(client: Client): Promise<Integer> {
    const response = await client(Airplane).aggregate({
        $select: {
            $count: "unordered" 
        } 
    });
    return response.$count;
}

export default getNumberOfAircraft;
```

You can perform a search-around operation by using the `pivotTo` method available on the client and specifying the link type API name:
```typescript
// typescript-functions/src/functions/countPassengers.ts

import { Client } from "@osdk/client";
import { Aircraft } from "@ontology/sdk";

async function countPassengers(client: Client, lastNamePrefix: string): Promise<string> {
    const response = await client(Aircraft)
        .pivotTo("aircraftToPassenger")
        .where({
            lastName: {
                $startsWith: lastNamePrefix,
            } 
        })
        .aggregate({
            $select: {
                "lastName:exactDistinct": "unordered"
            } 
        });

    return `There are ${response.lastName.exactDistinct} passengers whose last name begins with ${lastNamePrefix}`;
}

export default countPassengers;
```

### Local Ontology SDK

This repository supports a **local SDK**, where the Ontology SDK lives fully within your functions repository and is automatically generated from your resource imports.

To enable the local SDK, set `useSdkSidebar` to `false` in your repository's `functions.json` file.

#### How it works

- Changes to your resource imports automatically generate a new version of your SDK, and you can start using the updated types immediately in your code.
- When you tag a version of your function, the SDK is generated in CI and bundled with your function version.
- If this is the first time you are creating an SDK for your repository, you will need to choose an Ontology and package name using the resource imports side panel.
- Use `./rune sdk generate` to manually regenerate a local SDK, migrate an existing repository to a local SDK, or generate against a specific Global branch (with `--branch-rid <branch-rid>`).


### Ontology Edits
You can use the Ontology SDK to produce edits to the Ontology that can be applied by Function-backed Actions. 

First, define a new type that declares the object types, interface, or link types that can be modified by the function using the `Edits` type from the `@osdk/functions` package. If the function modifies multiple object or link types, you can join multiple `Edits` types with the `|` operator:

```typescript
import { Edits } from "@osdk/functions";
import { Employee, LaptopRequest } from "@ontology/sdk";

type EmployeeEdit = 
    | Edits.Object<Employee>
    | Edits.Object<LaptopRequest>
    | Edits.Link<Employee, "lead">;
```

Then, define a function that returns an array of the `EmployeeEdit` type, and use `createEditBatch` from `@osdk/functions` to instantiate and fill a batch with edits to apply to the Ontology. 

Full example: create a ticket, set due date, assign to employee

```typescript
import { Employee, Ticket } from "@ontology/sdk";
import { Client, Osdk } from "@osdk/client";
import { createEditBatch, Edits, Integer } from "@osdk/functions";
import { DateTime } from "luxon";

type OntologyEdit =
  | Edits.Object<Employee>
  | Edits.Object<Ticket>
  | Edits.Link<Employee, "assignedTickets">;

function createAndAssign(
  client: Client,
  employee: Osdk.Instance<Employee>,
  ticketId: Integer,
): OntologyEdit[] {
  const batch = createEditBatch<OntologyEdit>(client);

  batch.create(Ticket, {
    ticketId,
    dueDate: DateTime.now().plus({ days: 7 }).toFormat("yyyy-MM-dd"),
  });

  batch.link(employee, "assignedTickets", {
    $apiName: "Ticket",
    $primaryKey: ticketId,
  });

  return batch.getEdits();
}

export default createAndAssign;
```

Modifying objects through interfaces involves the same process. Interface types that the function can modify should also
be defined using the `Edits` type from the @osdk/functions package.

```typescript
import { Edits } from "@osdk/functions";
import { Athlete } from "@ontology/sdk";

type AthleteEdit = Edits.Interface<Athlete>;
```

#### Interface example

Now let's create a function that returns an array of the `AthleteEdit` type and use `createEditBatch` from `@osdk/functions` to instantiate and fill a batch with edits to apply to the Ontology.

The following function takes in any object that implements the `Athlete` interface and updates its `jerseyNumber` interface property.

```typescript
// typescript-functions/src/functions/updateJersey.ts

import { Client, Osdk } from "@osdk/client";
import { createEditBatch, Edits, Integer } from "@osdk/functions";
import { Client, Osdk } from "@osdk/client";
import { createEditBatch, Edits, Integer } from "@osdk/functions";
import { Athlete } from "@ontology/sdk";

type AthleteEdit = Edits.Interface<Athlete>;

function updateJersey(
    client: Client,
    athlete: Osdk.Instance<Athlete>,
    newJerseyNumber: Integer
): AthleteEdit[] {
    
    const batch = createEditBatch<AthleteEdit>(client);

    batch.update(athlete, {
        jerseyNumber: newJerseyNumber
    });
    return batch.getEdits();
}

export default updateJersey;
```

#### Struct example

Define a TypeScript interface matching the struct's field API names:

```ts
interface Address {
  street: string;
  city: string;
  state: string;
  country: string;
  zipcode: string;
}

export default function updateAddress(
  client: Client,
  employee: Osdk.Instance<Employee>,
  newAddress: Address,
): OntologyEdit[] {
  const batch = createEditBatch<OntologyEdit>(client);
  batch.update(employee, { address: newAddress });
  return batch.getEdits();
}
```

### Function Configuration
You can configure permitted egress and the API name of a Function by exporting a `config` object from the file containing the Function.

The expected shape of this `config` object is as follows:

```typescript
interface Config {
    /**
     * The API name of the Function, to allow it to be invoked in other pro-code contexts or via the public API.
     */
    apiName?: string;

    /**
     * A list of source aliases that the Function may egress to. Any sources specified in this field must also be imported into the repository.
     * 
     * For more information about interacting with sources, see the `Making API Calls` section.
     */
    sources?: string[];
}
```

For example, to configure a Function with an API name of `MyApiName` and egress to the source alias `demoSource`, export the following `config` from the file containing your Function.

```typescript
export const config = {
    apiName: "MyApiName",
    sources: ["demoSource"],
};
```

### Making API Calls to External Systems
By default, Functions cannot egress to external systems. To make API calls, first import a source using the left sidebar and configure a source alias. See [Source aliases](https://www.palantir.com/docs/foundry/functions/source-aliases/) and [Make API calls from functions](https://www.palantir.com/docs/foundry/functions/api-calls/) for the full setup.

Then, declare that your Function can egress to that source alias. The `config` object must be exported from the entry-point Function's file, not from the file of any helper functions.

Source aliases are named, portable references to [Data Connection sources](https://www.palantir.com/docs/foundry/data-connection/set-up-source/). By referring to a source by its alias key instead of a specific source identifier, you decouple your function logic from any one source. This keeps your functions portable across environments.

To use a source alias in your function, reference the alias by its key wherever you declare and retrieve the source. Pass the alias key to the `sources` configuration and to `getSource`:

```typescript
// typescript-functions/src/functions/MyExternalFunction.ts

import { getFetch, getHttpsConnection, getSource } from "@palantir/functions-sources";

export const config = {
    sources: ["myOAuthSourceAlias"]
};

export default async function callExternalApi(): Promise<string> {
    const source = await getSource("myOAuthSourceAlias");
    const { url } = getHttpsConnection(source);
    const fetch = await getFetch(source);

    const response = await fetch(url + "/api/v1/resource");

    return response.text();
}
```

The `@palantir/functions-sources` library exposes a fetch client and HTTP agent pre-configured with any server or client certificates on the source, as well as proxy information to allow egress from all runtime environments. To ensure that egress works correctly from all environments, it is highly recommended to use either the provided fetch or HTTP agent.

```typescript
import { getFetch, getHttpAgent } from "@palantir/functions-sources";

const fetch = await getFetch(source);
const agent = await getHttpAgent(source);
```

If you need the resource identifier (RID) of the source that an alias resolves to, use the `Aliases.source` utility in TypeScript v2. Read the resolved RID from the `.rid` property:

```typescript
import { Aliases } from "@osdk/functions";

const sourceRid = Aliases.source("demoSource").rid;
```

### Additional Capabilities

This template includes examples for the most common Function patterns. For more advanced workflows, see:

- [Instrumentation and telemetry](https://www.palantir.com/docs/foundry/functions/instrumentation-telemetry/) for emitting logs and spans.
- [User-facing errors](https://www.palantir.com/docs/foundry/functions/user-facing-error/) for returning actionable validation failures.
- [Streaming functions](https://www.palantir.com/docs/foundry/functions/streaming-functions/) for producing streamed responses.
- [Foundry platform SDK](https://www.palantir.com/docs/foundry/functions/platform-sdk/) for calling Foundry platform APIs from Functions.
- [Language models in TypeScript v2 and Python functions](https://www.palantir.com/docs/foundry/functions/language-models-python-tsv2/) for model-backed workflows.

### Live Preview

In Authoring, Functions can be previewed before publishing using the “Functions” tab accessible at the bottom of the window. With a file open, select “Live Preview” to execute Functions defined in that file with custom inputs.

### Publishing Functions

Functions can be published on a given branch by tagging a commit. In Authoring, click the “Tag version” button at the top-right of the window and provide a version. Any Functions present in the repository as of the latest commit will be published with that version for use throughout Foundry. Functions follow the [Semantic Versioning (SemVer) specification](https://semver.org/), which enables downstream applications using the Function to declare a particular version or a range of versions with which they're compatible.

### Local Development

It is possible to carry out high-speed, iterative development of TypeScript Functions locally. To get started, click the "Work locally" button in the top right.
Once you've cloned the repository locally, run `./gradlew localDev` in the root directory of the project to set up the environment.

The `./rune` CLI is used for local SDK generation, function discovery, and execution. If `./rune` is missing, run `.palantir-scripts/install-rune` to install it.

### Testing

For the full OSDK unit-testing API, see [Unit testing TypeScript OSDK code](https://www.palantir.com/docs/foundry/ontology-sdk/typescript-osdk-testing/).

This template ships with [Vitest](https://vitest.dev/). Starter tests live under `src/functions/__tests__`, mirroring the `src/functions` structure for the Functions they cover, and run with:

```bash
./gradlew test
```

or

```bash
npm test
```

In Authoring, run the `test` task from the task runner. Tests also run automatically in CI.

For Functions that take an OSDK `Client` or operate on `Osdk.Instance<T>` values, the `@osdk/unit-testing` package provides a mock `Client` and helpers for building object instances, links, object sets, and queries.

A minimal test for a Function that fetches a page of objects looks like:

```typescript
// src/functions/__tests__/searchAircraft.test.ts
import { createMockClient, createMockOsdkObject } from '@osdk/unit-testing';
import { describe, it, expect } from 'vitest';
import { ExampleDataAircraft } from '@ontology/sdk';
import searchAircraft from '../searchAircraft.js';

describe('searchAircraft', () => {
    it('returns aircraft arriving in NYC', async () => {
        const mockClient = createMockClient();
        const mockAircraft = createMockOsdkObject(ExampleDataAircraft, {
            id: '1',
            arrivalCity: 'NYC',
        });

        mockClient
            .when((stub) =>
                stub(ExampleDataAircraft)
                    .where({ arrivalCity: { $eq: 'NYC' } })
                    .fetchPage({ $orderBy: { id: 'asc' } }),
            )
            .thenReturnObjects([mockAircraft]);

        expect(await searchAircraft(mockClient)).toEqual([mockAircraft]);
    });
});
```

A starter version of this file is at `src/functions/__tests__/searchAircraft.test.ts`.


### Query Functions

Queries are the read-only subset of functions that may be optionally exposed through the [API gateway](https://www.palantir.com/docs/foundry/api/general/overview/introduction/). They cannot have any side effects, such as modifying the Ontology or altering external systems. You should use an [Action](https://www.palantir.com/docs/foundry/api/ontology-resources/actions/apply-action/) if you need those additional editing capabilities through the API gateway.

Use the following syntax to define a query function.

```typescript
// Export a config object with an apiName parameter from the file containing the function
export const config = {
    apiName: "myTypeScriptV2Function"
};
```

After publishing your TypeScript or Python query function, navigate to the code repository where you want to consume the function, and import it using the [Resource imports sidebar](https://www.palantir.com/docs/foundry/functions/resource-imports-sidebar/).

Your function will be callable from the consuming repository. For example:

```typescript
import { Client } from "@osdk/client";
import { Double } from "@osdk/functions";
import { getReschedulableAircraftCount } from "@ontology/sdk";

async function callQueryFunction(client: Client): Promise<Double> {
    return client(getReschedulableAircraftCount).executeFunction({ timeUntilNextFlight: 10 });
}

export default callQueryFunction;
```

### Error handling

When running functions in other parts of the platform, such as Workshop or actions, you may want to throw an error with a detailed message. To do so, throw a `UserFacingError`. For example:

```typescript
import { Osdk } from "@osdk/client";
import { Employee } from "@ontology/sdk";
import { UserFacingError } from "@osdk/functions";

export default async function searchExactlyFiveEmployees(employees: Array<Osdk.Instance<Employee>>): Promise<string> {
    if (employees.length != 5) {
        throw new UserFacingError(`Pass in exactly 5 employees. Received ${employees.length}.`);
    }

    // search employees
}
```

By adding a detailed user facing error message, you can help other users of your Function quickly identify and fix the issue.

### Generated SDK Documentation

To see objects types, interfaces, query functions, etc that are available, look at the "Resource Imports" sidebar and click on the docs on the top right.

### Media

For more details on using media in functions, see [Media](https://www.palantir.com/docs/foundry/functions/media/).

Here's an example edit function where you pass media to an action. This function will create a row with a media reference and add the media item to the media set.

```typescript
import { createEditBatch, Edits } from "@osdk/functions";
import { ObjectType } from "@ontology/sdk";
import { Client, Media } from "@osdk/client";

type OntologyEdit = Edits.Object<ObjectType>;

export default async function createObjWithMedia(
  client: Client,
  media: Media
): Promise<OntologyEdit[]> {
  
  const editsBatch = createEditBatch<OntologyEdit>(client);
  
  editsBatch.create(ObjectType, {
    // ...
    mediaProp: media
  });

  return batch.getEdits();
}
```

Use the Ontology SDK `uploadMedia` helper to upload raw bytes within a function. It returns a `Media`, which you can then edit an Ontology object media property with an Ontology edit or return from the function.

```typescript
import type { Client, Media } from "@osdk/client";
import { uploadMedia } from "@osdk/functions";

export default async function uploadMediaItem(
    client: Client,
    body: string,
    fileName: string,
): Promise<Media> {
    const blob = new Blob([body], { type: "text/plain" });
    const media: Media = await uploadMedia(
        client,
        { data: blob, fileName }
    );
    return media;
}
```

### Notifications

Functions can be used to flexibly configure notifications that should be sent in the platform, including notifications that are sent externally to a user's email address. For more details, see [Configure notifications](https://www.palantir.com/docs/foundry/functions/configure-notifications/).

The function itself never sends the notification -- it only shapes the content or computes the recipient list; the platform handles delivery.

```typescript
import { Notification, NotificationLink, Principal } from "@osdk/functions";
import { Users, Groups } from "@osdk/foundry.admin";
import { Issue } from "@ontology/sdk";
import { type Osdk, Client } from "@osdk/client";

/**
 * Builds a personalized notification for the Issue's assignee.
 * issue.assignee / issue.group are just IDs, so we resolve them to full
 * User / Group objects (via @osdk/foundry.admin) to include real names.
 */
export default async function createIssueNotification(
  client: Client,
  issue: Osdk.Instance<Issue>,
): Promise<Notification> {
  const [assignee, group] = await Promise.all([
    Users.get(client, issue.assignee),
    Groups.get(client, issue.group),
  ]);

  const links: NotificationLink[] = [
    { label: "View Issue", linkTarget: { type: "object", object: issue } },
  ];

  return {
    platformNotification: {
      heading: "New issue",
      content: `A new issue was assigned to you in ${group.name}.`,
      links,
    },
    emailNotification: {
      subject: "New issue assigned",
      body: `Hello ${assignee.firstName},\n\nA new issue was assigned to you: ${issue.description}`,
      links,
    },
  };
}
```

When sending a notification, you often need to customize the recipients as well. Recipients are specified via `Principal[]`. A Principal represents either a Foundry user account or group.

```ts
export async function getIssueRecipients(
  client: Client,
  issue: Osdk.Instance<Issue>,
): Promise<Principal[]> {
  const [assignee, reporter] = await Promise.all([
    Users.get(client, issue.assignee),
    Users.get(client, issue.reporter),
  ]);

  return [
    { type: "user", id: assignee.id },
    { type: "user", id: reporter.id },
  ];
}
```

### Language Models

To use Palantir-provided language models, [AIP must be enabled on your enrollment](https://www.palantir.com/docs/foundry/aip/enable-aip-features/). You must also have permissions to use [AIP builder capabilities](https://www.palantir.com/docs/foundry/aip/aip-features/#aip-applications-and-builder-capabilities).

Palantir provides a set of language models that can be used within functions. [Learn more about Palantir-provided LLMs](https://www.palantir.com/docs/foundry/aip/supported-llms/).

Language models in TypeScript v2 and Python functions use proxy endpoints to interact with models. The following example uses the [OpenAI chat completion proxy endpoint](https://www.palantir.com/docs/foundry/api/v2/llm-apis/models/openai-chat-completions-proxy/). You can select other providers from the documentation side panel.

Third-party libraries, such as `openai` in the example below, are not pre-installed. Install them from the **Libraries** section of the left side panel.

```typescript
import { PlatformClient } from "@osdk/client";
import OpenAI from "openai";
import { Aliases } from "@osdk/functions";
import { getFoundryToken, getOpenAiBaseUrl, createFetch } from "@osdk/language-models";

export default async function callOpenAi(client: PlatformClient, prompt: string): Promise<string> {
    const oaiClient = new OpenAI({
        apiKey: await getFoundryToken(client),
        baseURL: getOpenAiBaseUrl(client),
        fetch: createFetch(client),
    });

    const completion = await oaiClient.chat.completions.create({
        model: Aliases.model("{MY_ALIAS}").rid,
        messages: [
            { role: 'user', content: prompt },
        ],
        reasoning_effort: "minimal",
        max_completion_tokens: 200,
    });

    return completion.choices[0]?.message.content ?? "";
}
```

### Additional Function Use Cases

This section documents various ways that you can use functions throughout the Foundry platform. This list is kept mostly up to date, but there may be additional ways to use functions that are not captured here.

- [Use functions in the platform](https://www.palantir.com/docs/foundry/functions/use-functions/)
- [Functions on objects (FOO)](https://www.palantir.com/docs/foundry/workshop/functions-overview/)
- [Derive properties using Functions](https://www.palantir.com/docs/foundry/vertex/derive-property-functions/)
- [Function-based styling](https://www.palantir.com/docs/foundry/map/integrate-functions/)
- [Create and use visual functions](https://www.palantir.com/docs/foundry/quiver/visual-functions-create/)
- [Suggestion Function](https://www.palantir.com/docs/foundry/dynamic-scheduling/scheduling-suggestion-functions/)
- [Chatbots as Functions](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions/)
- [Functions](https://www.palantir.com/docs/foundry/notepad/widgets-functions/)
