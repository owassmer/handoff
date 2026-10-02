# AGENTS.md

## Writing basic functions

This repository uses **TypeScript v2 functions** (`@osdk/functions`, module-based, full Node.js runtime). Every function lives in its own file under `typescript-functions/src/functions/`.

### Anatomy of a function file

**Read-only function with Ontology access:**

Every TSv2 function file follows this structure:

```ts
// 1. Imports
import { Client, Osdk, ObjectSet } from "@osdk/client";
import {
  Integer,
  Long,
  Double,
  Float,
  DateISOString,
  TimestampISOString,
  UserFacingError,
  Edits
} from "@osdk/functions";
import { MyObjectType } from "@ontology/sdk";

// 2. (If edit function) Type alias for edits
type OntologyEdit = Edits.Object<MyObjectType>;

// 3. (If query function) Config export for API name / sources
export const config = { apiName: "myQueryName" };

// 4. The function (default export)
export default async function myFunction(
  client: Client, // read-only function without ontology access doesn't need client param
  someObject: Osdk.Instance<MyObjectType>,
  someObjectSet: ObjectSet<MyObjectType>,
  someString: string,
  optionalParam?: string,
): Promise<string> {
  // ...
  return "result";
}
```

### Key rules

- **One registered function per file.** The default export is the registered function. Everything else (like non-default exports) is a private helper and won't be registered.
- **The Function name must also match the file name.**: helloWorld.ts should define and default-export helloWorld. Renaming or moving the file changes the published Function identity."
- **`client: Client` is always the first parameter** when your function needs to query the Ontology (search, aggregate, fetch, edit). The platform injects it at runtime — never construct it yourself.
- **Object type instances use `Osdk.Instance<T>`**, not the raw type. e.g. `Osdk.Instance<Equipment>`, not `Equipment`.
- **Object sets use `ObjectSet<T>`** from `@osdk/client`. Prefer object sets over arrays as inputs — they defer loading.
- **Async functions return `Promise<T>`.** Any function that awaits (data loading, aggregations) must be `async` and return a `Promise`.
- **Object types must be imported into your repository** via the Resource imports sidebar in Authoring or VS Code before you can reference them. The list of imported object types, link types, interface types, query functions, sources, models, and everything else goes in resources.json. This most likely needs human intervention

### Helper functions and shared utilities

Non-default exports are not registered as functions. Use them for shared logic:

```ts
// utils.ts — not a registered function, just a helper module
import { TimestampISOString, UserFacingError } from "@osdk/functions";
import { Client } from "@osdk/client";

export async function validateReservationTime(
  client: Client,
  startTime: TimestampISOString,
  endTime: TimestampISOString,
  equipmentId: string,
): Promise<void> {
  if (new Date(startTime) >= new Date(endTime)) {
    throw new UserFacingError("Start time must be before end time");
  }
  // ... more validation for example
}
```

```ts
// createReservation.ts — imports the shared helper
import { validateReservationTime } from "./utils.js";
// note: use .js extension in imports even though source is .ts
```

## Types

TSv2 uses plain TypeScript types with specific aliases for Ontology-compatible scalars. All numeric/date aliases are imported from `@osdk/functions`. Object types come from `@ontology/sdk`. Container types use standard TypeScript

Basic rules

- Strict typing: no `any`, prefer `unknown` when type is truly unknown
- Use branded types for domain primitives (e.g., `UserId` instead of raw `string`)

### Scalars (import from `@osdk/functions` unless noted):

- `boolean`, `string` — builtin, map directly to TS
- `Integer` → `number` (-2,147,483,648 to 2,147,483,647)
- `Long` → `string` (use `BigInt()` for math, `.toString()` result)
- `Float`, `Double` → `number` (Double is IEEE 754 64-bit)
- Date -> `DateISOString` → `string` ("YYYY-MM-DD")
- Timestamp -> `TimestampISOString` → `string` (ISO 8601: "2024-01-01T00:00:00Z")

```typescript
export default function getCurrentTimestamp(): TimestampISOString {
  const now = new Date();
  return now.toISOString();
}
```

### Ontology

- Single object: `Osdk.Instance<MyType>` @osdk/client + @ontology/sdk
- Object set: `ObjectSet<MyType>` @osdk/client + @ontology/sdk
- Object specifier: `ObjectSpecifier<MyType>` (`@osdk/client` only)
- Edit return: `OntologyEdit[]` (see Writing actions)
- Attachment, UserId, GroupId, Point, Geometry — from `@osdk/functions`

To see objects types, interfaces, query functions, etc that are available, [here is the node modules package](typescript-functions/node_modules/@ontology/sdk/esm/ontology). Resources.json is the source of truth behind it.

- @ontology/sdk is the default, but a user can choose to the package name. If ontology/sdk is not found, check package.json for a different package with /sdk ending.

### Local Ontology SDK

Repositories should use a **local SDK** — the Ontology SDK is automatically generated from resource imports rather than manually versioned and installed as a separate package. This means SDK types are always up-to-date with the latest resource imports, and agents don't need to prompt the user to manually generate or install a new SDK version after importing Ontology entities. It is also required for full Global Branching support.

To enable: set `useSdkSidebar` to `false` in the repository's `functions.json` file. See [Local Ontology SDK in README](README.md#local-ontology-sdk) for full details.

### Other

- Map: `Record<K, V>` — K is `string` or `ObjectSpecifier<T>`. Use builtin `Map` for non-published functions
- list - normal (Integer[])
- Attachment, Notification, Media (see corresponding section)

```typescript
// Good
const workGroupById = new Map<string, WorkGroup>();
workGroupById.set(wg.id, wg);
workGroupById.get(id);

// Avoid
const workGroupById: { [key: string]: WorkGroup } = {};
workGroupById[wg.id] = wg;
workGroupById[id];
```

Optional params: Use `?` after required params. Always use for properties that may be undefined

```ts
function greet(name?: string): string {
  return name === undefined ? "Hello!" : `Hello, ${name}!`;
}

// Default values also work
function greetWithDefault(name: string = "Anonymous"): string {
  return `Hello, ${name}!`;
}
```

### Import cheat sheet. Also packages/places to look at to learn more (if need be)

- @osdk/api - Ton of under-the-hood types like WhereClause and TimeSeriesPoint. Re-exported in some other places like @osdk/client
- @ontology/sdk - Object types, query functions, etc. everything in your OSDK. e.g. `Equipment`
- @osdk/functions - The common types (`Notification`, `createEditBatch`, `Edits`, `UserFacingError`, `Integer`, `Long`, `Double`, `Float`, `DateISOString`, `TimestampISOString`, `TwoDimensionalAggregation`, `ThreeDimensionalAggregation`
- @osdk/foundry - platform SDK types (admin, filesystem, etc). getting the current user for example
- @osdk/client - `Client`, `Osdk`, `ObjectSet`, `ObjectSpecifier`, `WhereClause`
- `crypto`, `fs`, etc. (full Node.js runtime in TSv2) - Node.js builtins (`randomUUID`, `crypto`, etc.)
- @palantir/functions-sources - Sources for external API calls
- @opentelemetry/api-logs - `logs`, `SeverityNumber` for log records (see Logging and telemetry)
- @opentelemetry/api - `trace`, `SpanStatusCode` for spans (see Logging and telemetry)

## Writing actions

A common type of function is an edit function, or a function backed action. This is the logic that allows a user to edit a value in their object type.

TSv2 replaces TSv1's decorator-based mutation model with an explicit edit batch pattern. Instead of mutating objects directly (employee.name = "Bob"), you construct an EditBatch via createEditBatch(), accumulate edits through method calls (batch.update(employee, { name: "Bob" })), and return batch.getEdits(). Edits are explicit, immutable-friendly, and composable.

TSv2 also supports interface edits, struct property edits, and primary-key-only references (edit objects without loading them). The trade-off: edits within the same execution are NOT visible to subsequent reads — batch.update() does not change the in-memory object, and search APIs return stale data until the function completes.

### Edit operations

Updating:

- batch.update(employee, { lastName: "Smith" }) — by instance
- batch.update({ $apiName: "Employee", $primaryKey: 23 }, { lastName: "Smith" }) — by PK
- batch.update(employee1, employee2) — copies ALL props from employee2 onto employee1
- batch.update(person, { firstName: "Jane" }) — through interface
- batch.update(employee, { address: { street: "123 Main", city: "NYC", state: "NY", country: "US", zipcode: "10001" } }) — struct property

Creating:

- batch.create(Ticket, { ticketId: 42, dueDate: "2025-06-01" })
- batch.create(Person, { $objectType: "Employee", firstName: "John", lastName: "Doe" }) — through interface (must specify $objectType)

Deleting:

- batch.delete(ticket) — by instance
- batch.delete({ $apiName: "Ticket", $primaryKey: 12 }) — by PK
- batch.delete(person) — through interface

Linking (many-to-many only):

- batch.link(employee, "assignedTickets", ticket)
- batch.unlink(employee, "assignedTickets", ticket)
- Both support PK references: batch.link({ $apiName: "Employee", $primaryKey: 23 }, "assignedTickets", { $apiName: "Ticket", $primaryKey: 12 })

Linking (one-to-many / one-to-one) — use batch.update() on the FK holder:

- Set: batch.update({ $apiName: "Ticket", $primaryKey: 13 }, { assignedEmployeeId: 52 })
- Clear: batch.update({ $apiName: "Ticket", $primaryKey: 13 }, { assignedEmployeeId: undefined })

Retrieving edits:

- batch.getEdits() — returns OntologyEdit[], the function's return value

Notes

- Primary-key-only references (like { $apiName: "Employee", $primaryKey: 23 }) allow you to edit objects without loading them — this avoids fetch cost when you already know the PK. Particularly useful for batch processing with IDs from external systems
- hard to read so prefer by instance if the obj is already being loaded

### Type declaration pattern

Every edit function declares an OntologyEdit type union covering all entities it will edit.

Rules:

- Each object type you create/update/delete needs Edits.Object<T>
- Each interface you edit through needs Edits.Interface<I> [Interface example in readme](README.md#interface-example)
- Each many-to-many link you modify needs Edits.Link<Source, "linkApiName">
- One-to-many/one-to-one links only need Edits.Object<FKHolder> (no Edits.Link)
- Full example: create a ticket, set due date, assign to employee

```ts
import { Employee, Ticket } from "@ontology/sdk";
import { Client, Osdk } from "@osdk/client";
import { createEditBatch, Edits, Integer } from "@osdk/functions";
import { DateTime } from "luxon";

type OntologyEdit =
  | Edits.Object<Employee>
  | Edits.Object<Ticket>
  | Edits.Link<Employee, "assignedTickets">;
// | Edits.Interface<Person> here's how to add interfaces

export default function createAndAssign(
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
```

### Struct property edit pattern

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

### Edit resolution

How edits land in the Ontology is controlled by the object type's edit resolution strategy, not the function language. TSv2 edits behave identically to TSv1/action-rule edits at the writeback layer.

- Apply User Edits (default): user edit always wins; datasource updates for edited properties ignored forever
- Apply Most Recent Value (OSv2 only): compares edit timestamp vs datasource timestamp; newer wins

### Gotchas

- Edits are invisible during execution. After batch.update(employee, { name: "Bob" }), employee.name still returns the old value. Search APIs also return stale data.
- batch.create() returns no instance. Reference newly created objects by { $apiName, $primaryKey }.
- batch.link()/batch.unlink() are many-to-many only. For one-to-many/one-to-one, use batch.update() on the FK holder.
- Edits type union must be exhaustive. Missing entries cause publish-time rejection.
- Interface properties backed by primary key cannot be updated. PKs are immutable.
- batch.update(obj1, obj2) copies ALL properties including nulls.
- No implicit edit collapsing. Multiple batch.update() calls on the same object produce multiple edit entries.
- client: Client is required. createEditBatch() needs the platform-injected client — never construct it yourself.
- Edits only apply through Action Types. Running in authoring preview does NOT apply edits.
- No webhook support from TSv2. Webhooks require TSv1.
- Optional arrays differ between preview and actions. Omitted optional arrays are undefined in preview but [] when executed through an action.
- Single batch instance: All edits (including from helpers) must flow through the same batch
- Standard testing: Assert on batch.getEdits() — no special test harness needed

### Function backed actions for batched execution

When an action is triggered in batches, such as in Workshop inline edits or in Automate, the backing function is usually called once per request in sequence, and all edits are applied atomically at the end of the action call.

Alternatively, to improve performance or resolve edit conflicts, you may wish to configure a function to receive the whole batch of action calls in a single execution. See <https://www.palantir.com/docs/foundry/action-types/function-actions-batched-execution>

## Query functions

You can call query functions from other repos using the OSDK client (functions need to be added in OSDK resource scope):

```ts
import { Client } from "@osdk/client";
import { Integer } from "@osdk/functions";
import { getEquipmentCount } from "@ontology/sdk";

export default async function myFunction(client: Client): Promise<Integer> {
  const result = await client(getEquipmentCount).executeFunction({
    // pass named parameters as an object
  });
  return result;
}
```

The function being called must be a query function (i.e. it has an `apiName` configured). Import the query function from `@ontology/sdk` like you would an object type, then call it via `client(queryFn).executeFunction({ ...params })`.

To make a query function (function exposed via API gateway) see [query-functions in the README](README.md#query-functions)

## Error handling

Use `UserFacingError` (from `@osdk/functions`) to surface actionable messages to end users in Workshop or wherever the function runs. Regular `Error` produces a generic message — only `UserFacingError` passes the message through to the UI.

For edit functions, the UI prefixes error messages with "Failed to apply change: ", so write messages that read naturally after that prefix. Keep messages short, non-technical, and avoid jargon like "invalid state".

```ts
import { UserFacingError } from "@osdk/functions";

// Good — reads naturally after the UI prefix
throw new UserFacingError("Staff member does not have a home department");
// UI shows: "Failed to apply change: Staff member does not have a home department"

// Bad — redundant/confusing prefix
throw new UserFacingError(
  "Invalid state: Staff member does not have a home department",
);
// UI shows: "Failed to apply change: Invalid state: Staff member does not have a home department"
```

Avoid try/catch blocks in functions code. These often hide the root cause of an error and make debugging more difficult. Instead, explicitly handle edge cases early and let actual errors propagate.

## Logging and telemetry

The runtime registers the global OpenTelemetry logger and tracer providers and exports records and spans to the function's execution history in Foundry — that's how you debug a published function. `logs`/`SeverityNumber` (`@opentelemetry/api-logs`) and `trace`/`SpanStatusCode` (`@opentelemetry/api`) are already dependencies. Never add a logging library (winston, pino, debug) and never construct a LoggerProvider, NodeTracerProvider, or exporter — a second provider silently replaces the one that ships telemetry to Foundry. See [Instrumentation and telemetry](https://www.palantir.com/docs/foundry/functions/instrumentation-telemetry/).

```ts
import { logs, SeverityNumber } from "@opentelemetry/api-logs";

// module scope, kebab-case: the logger late-binds to the provider registered later
const logger = logs.getLogger("create-reservation");

logger.emit({
  severityNumber: SeverityNumber.INFO,
  severityText: "INFO", // set both
  body: "Creating reservation", // short constant; variable parts go in attributes
  attributes: { equipmentId: equipment.equipmentId },
});
```

`console.log`/`info`/`debug`/`warn`/`error` are patched and mirrored to OpenTelemetry, so they're fine for quick messages. Every other console method (`table`, `trace`, `dir`, `group*`, `time*`, `count*`, `assert`, `clear`) emits an "unsupported method" WARN and otherwise only reaches stdout — don't use them.

### Spans

The runtime already wraps each execution (`Executing function` → `Loading arguments` / `Executing user code`) and traces outbound `fetch`, so add spans only to time expensive work _inside_ the function.

```ts
import { trace } from "@opentelemetry/api";

const tracer = trace.getTracer("score-candidates"); // module scope, like the logger

const scores = await tracer.startActiveSpan("Scoring candidates", async (span) => {
  try {
    span.setAttribute("candidateCount", candidates.length);
    return await scoreAll(client, candidates); // the callback's value is returned
  } finally {
    span.end();
  }
});
```

- `startActiveSpan` when the body awaits or contains other instrumented work, so nested spans and fetches attach to it; `startSpan`/`end` for straight-line timing. A `finally` with no `catch` still lets errors propagate, so it doesn't violate the no-try/catch guidance above.
- One span around a loop with the count as an attribute, never a span per iteration.

### Gotchas

- Telemetry emitted outside an execution is dropped — a top-level `console.log` or a log at module load never reaches Foundry. Emit from inside the function body.
- Export is batched: roughly every 5 seconds and on process exit. Live Preview flushes far more aggressively, so iterate there.
- The queue is bounded (2048 records per process) and overflow is dropped. Log aggregates — counts, ids of the few interesting rows — not one record per object in a large object set.
- Log records are for you; `UserFacingError` is what the end user sees. A failure the user must act on needs both.
- Unit tests run without a registered provider, so `emit()` and span calls are no-ops — safe to call, but don't assert on them.

## Data Loading

Most examples in this section use an object model where the main object type is equipment. Equipment has a fk to equipment type and to equipment owner. The relationships are many to one (many eq per eq type, many eq per owner). Then there is a reservation object type. A reservation has a fk to equipment (many reservations on an eq).

A foreign key implies but doesn't guarantee a link exists in the OSDK. A link allows you to traverse from one object type to another using a `pivotTo` statement.

### Object sets

An object set can be thought of as an un-materialized view. The bigger the object set, the longer the request will take to load when you await the subsequent promise. Because of that, it's crucial to create the most specific possible object set before loading data. Most functions can be separated into object set creations, concurrent data loading within a promise.all (or multiple separate promises if you have to), and then performing work on the subsequent objects in memory.

An example of an object set with specific filters is:

```ts
const specificObjectSet = client(ObjectTypeWithAllPropTypes).where({
  $and: [
    // and statement
    { stringProp: { $eq: "some val" } }, // eq to an existing equipmentType objects equipmentTypeId.  every prop type can use eq
    {
      $or: [
        // or statement. In addition to 'and' and 'or' there is also a '$not' statement
        {
          timestampProp: {
            // works for number, double, long, decimal, date, and timestamp prop types.  Also works for string (not that useful though)
            $lt: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
          },
        }, // created before the last 5 minutes.  could do 'lte' to if you want before or equal to the last 5 minutes.  Inverse is 'gt' and 'gte'
        { timestampProp: { $isNull: true } }, // works for number, double, long, decimal, date, timestamp, strings, and booleans
      ],
    },
    { booleanProp: { $ne: false } }, // not equal to false. works with every prop type
    { stringProp: { $startsWith: "prefix" } }, // string only
    { stringProp: { $containsAllTermsInOrder: "exact phrase" } }, // string only. matches the exact phrase
    { stringProp: { $containsAllTerms: "term1 term2" } }, // string only. all terms must be present (any order)
    { stringProp: { $containsAnyTerm: "term1 term2" } }, // string only. at least one term must be present
    { stringProp: { $in: ["val1", "val2", "val3"] } }, // works with every prop type. matches any value in array
    {
      structProp: { stringStructProp: { $startsWith: "foo" } }, // props within structs can do everything a normal prop can do
    },
    {
      geopointProp: {
        $within: { $distance: [100, "centimeters"], $of: [-74.006, 40.7128] }, // $of is [lon, lat]
      }, // geopoint only. units: millimeters, centimeters, meters, kilometers, inches, feet, yards, miles, nautical_miles
    },
    {
      geoshapeProp: {
        $within: { $bbox: [-74.006, 25.123, 80.4231, 40.7128] }, // [topLeftLon, topLeftLat, bottomRightLon, bottomRightLat]
      }, // geopoint and geoshape. $within also accepts a Polygon (see $intersects below)
    },
    {
      geoshapeProp: {
        $intersects: {
          type: "Polygon",
          coordinates: [
            [
              [10.0, 40.0],
              [20.0, 50.0],
              [20.0, 30.0],
              [10.0, 40.0],
            ],
          ],
        },
      }, // geoshape only. also supports $doesNotIntersect. $intersects also accepts $bbox (see $within above)
    },
  ],
});

// dynamic where statement. can get creative here
const phraseGroups = [
  ["exact phrase one", "another exact phrase"],
  ["exact phrase two", "another exact phrase"],
];
const advancedWhereStatements = client(Equipment).where({
  $and: phraseGroups.map((phraseGroup) => ({
    $or: phraseGroup.map((phrase) => ({
      name: { $containsAllTermsInOrder: phrase },
    })),
  })),
});

// Nearest neighbor (vector search)
const exampleNearestNeighbor = client(
  ObjectTypeWithAllPropTypes,
).nearestNeighbors("search text", 10, "vectorProp"); // (query: string | number[], numNeighbors: 1-500, vectorProperty)
```

You can do more advanced things with multiple object sets such as .union, .intersect, and .subtract. Union combines two object sets, intersect takes the overlap between two object sets, and subtracting removes one object set's objects from another.

```ts
const newObjectSet = specificObjectSet.union(objectSet1, objectSet2);
```

### Loading data (object sets, aggregations, or promises in general)

Always load promises concurrently with `Promise.all`. Minimize the number of promises created. Fewer object sets means better performance.

Use `asyncIter` over `fetchPage` when loading object sets (you almost always want to load the full object set vs paginating). Use `fetchPage`/`fetchOne` when needed.

Standard pattern:

```ts
const objectSet1 = ...// some definition here
const objectSet2 = ...// some other definition here
const [objectList1, objectList2] = await Promise.all([
    Array.fromAsync(objectSet1.asyncIter()),
    Array.fromAsync(objectSet2.asyncIter()),
])
```

Keep object set logic outside the Promise.all for readability.

Almost never create promises in loops. Use well-constructed object sets instead. Create maps after loading if you need object-to-linked-object associations (or use derived properties).

BAD WAY

```ts
const promises = eqTypeList.map((obj) =>
  client(Equipment)
    .where({ equipmentTypeId: { $eq: obj.equipmentTypeId } })
    .asyncIter(),
);
await Promise.all(promises);
```

GOOD WAY

```ts
const promise = client(Equipment)
  .where({ equipmentTypeId: { $in: eqList.map((eq) => eq.equipmentTypeId) } })
  .asyncIter();
```

Avoid loading full object sets when unnecessary (since the fewer objects that need to load, the faster). Some examples:

```ts
// if you know the pk of the object you want to load
const promise1 = client(Restaurant).fetchOne("primaryKey");

// if you know you need the "newest" or "first" object by some sortable property
const newestEquipmentPromise = client(Equipment).fetchPage({
  $orderBy: { createdOn: "desc" },
  $pageSize: 1, // could be whatever number makes sense for your use case
});
```

There are other cases where you don't need to load objects at all. For example, counting objects in an object set can be done via aggregation.

Often you only need a subset of properties:

```ts
const propertySubset = client(Equipment).asyncIter({
  $select: ["name", "equipmentId"],
});
```

These practices apply to all promise types. Object sets, aggregations, and platform SDK calls can and should load concurrently.

Avoid multiple sequential awaits unless absolutely necessary; concurrent awaiting is significantly faster.

### Traversing across object types via links

Use `pivotTo` to traverse linked object types without loading intermediate results into memory. Pivots can be chained with other object set operations (e.g., `pivot` → `where` → `pivot`).

Requirements: Object types must be linked, and the link type must exist in the OSDK. `pivotTo` uses the linkType API name.

```ts
const linkedEqOS = equipmentTypeOS.pivotTo("equipment");
const linkedReservationsOS = linkedEqOS.pivotTo("reservations");
const [equipTypeList, linkedEqList, linkedReservations] = await Promise.all([
  Array.fromAsync(equipmentTypeOS.asyncIter()),
  Array.fromAsync(linkedEqOS.asyncIter()),
  Array.fromAsync(linkedReservationsOS.asyncIter()),
]);
```

### Aggregations

If we want to get the count of an object set, or answer questions like "how many shift assignments are there in facility X in department Y?" we can use aggregations. Some examples:

```ts
// get the count of groups with less than or equal to 5 members
const countPromise = client(EquipmentOwner)
  .where({
    memberCount: { $lte: 5 },
  })
  .aggregate({
    $select: { $count: "unordered" },
  });
// Common to add .then(response => response.$count)

// Aggregation don't have to be a count
const example = await client(EquipmentType).aggregate({
  $select: { "partNumber:exactDistinct": "asc" }, // could also be approximateDistinct depending on your needs for accuracy vs performance
  // exactDistinct and approximateDistinct work for every property type
  // Can return in 'asc', 'desc', or 'unordered' order. works for every property type
});

// can also group by. Don't worry about the properties being used below, they are just syntactical examples
const stringAgg = await client(EquipmentType).aggregate({
  $select: { "status:exactDistinct": "unordered" },
  $groupBy: { equipmentTypeName: "exact" }, // any property type can use 'exact'. only option for strings
});

// date / timestamp aggregations and additional group by capabilities
const dateOrTimestampAgg = await client(Reservation).aggregate({
  $select: { "startTime:max": "unordered" }, // Can also be max and min in addition to exactDistinct and approximateDistinct
  $groupBy: { endTime: { $duration: [10, "minutes"] } }, // datetime bucketing. only exists for date / timestamp fields. Can also 'exact' like strings do
  // value must be set to 1 if grouping by weeks, months, quarters, or years
  // options are seconds, minutes, hours, days, weeks, months, quarters or years.  Only exists for date / timestamp fields
});

// another date / timestamp group by option
const dateOrTimestampAggAgain = await client(Reservation).aggregate({
  $select: { $count: "unordered" }, // doesn't have to be count
  $groupBy: {
    startTime: {
      $ranges: [["2026-04-06T23:51:26.387Z", "2026-04-07T23:51:26.387Z"]],
    },
  }, // can specify an array of ranges to group by
});

// numeric aggregations. works with numbers, doubles, longs, decimals
const example3 = await client(EquipmentOwner).aggregate({
  $select: { "memberCount:sum": "unordered" }, // sum, avg, max, min, exactDistinct, and approximateDistinct are all options
  $groupBy: { memberCount: { $ranges: [[123, 234]] } }, // same as date / timestamp range grouping but for numeric fields
});
```

### Derived properties

Derived properties allow you to avoid pivoting and loading an entire additional object set to get a specific property or aggregation from a linked object type.

```ts
// going from one owner to potentially many equipment (or many to many).  Ie aggregating.  If you are aggregating, has to start with a pivotTo and then a link must be specified
const aggregationDerivedPropertiesPromise = client(EquipmentOwner)
  // string and boolean derived properties
  .withProperties({
    newPropertyNameAgain: (baseObjectSet) =>
      baseObjectSet
        .pivotTo("equipment")
        .aggregate("serialNumber:exactDistinct"),
    // options are :approximateDistinct, :exactDistinct, :collectList, :collectSet.  These are the standard for every property type, with types having extra options
  })
  // date / timestamp derived properties
  .withProperties({
    newPropertyNameHere: (baseObjectSet) =>
      baseObjectSet.pivotTo("equipment").aggregate("createdOn:max"),
    // date / timestamp options are :approximateDistinct, :exactDistinct, :collectList, :collectSet and then max and min
  })
  // numeric property types
  .withProperties({
    newPropertyNameHere: (baseObjectSet) =>
      baseObjectSet.pivotTo("equipment").aggregate("someNumber:avg"),
    // numeric options are :sum, :avg, :max, :min, :exactDistinct, :approximateDistinct, :collectList, :collectSet, and :approximatePercentile
  })
  // can also always count.  Can also multi hop by chaining pivots together! extremely useful
  .withProperties({
    newPropertyName3: (baseObjectSet) =>
      baseObjectSet
        .pivotTo("equipment")
        .pivotTo("reservations")
        .aggregate("$count"),
  })
  .asyncIter();

// select properties (no aggregations).  Needs to be going from many to one, or one to one (ie not one to many or many to many)
// Super helpful. Basically just a way of adding a property from a linked object type without having to do a full pivot + object set load
const selectedProperties = client(Equipment)
  .withProperties({
    derivedPropGroupName: (baseObjectSet) =>
      baseObjectSet.pivotTo("equipmentOwner").selectProperty("groupName"),
  })
  .asyncIter();

// additional options: where statements in derived properties, math between two derived aggregation, using derived properties in subsequent operations
const advancedDerivedProperties = client(EquipmentOwner)
  .withProperties({
    someAdvancedProp: (baseObjectSet) => {
      const distinctSerialNumbers = baseObjectSet
        .pivotTo("equipment")
        .where({ isNameInherited: { $eq: false } }) // can use where statements to filter the linked objects before aggregating
        .aggregate("serialNumber:exactDistinct");

      const equipmentCount = baseObjectSet
        .pivotTo("equipment")
        .aggregate("$count");

      // math operations accept other derived properties
      // options: add, subtract, multiply, divide, abs, negate, max, min
      return distinctSerialNumbers.multiply(equipmentCount).abs();
    },
  })
  .where({ someAdvancedProp: { $lt: 100 } }) // can also filter on the derived property itself
  .aggregate({
    $select: { "someAdvancedProp:sum": "unordered" }, // can use derived properties everywhere, like this
  });
```

### Complete example

Given a reservation object set, we want each reservation's equipment details plus the equipment's linked equipment type and owner group name. We combine pivots with derived properties, then build a map from equipment ID to properties.

```ts
// search around to linked equipment and fetch owner group name and equipment type name
const linkedEquipmentOS = reservationOS
  .pivotTo("equipment")
  .withProperties({
    groupName: (baseObjectSet) =>
      baseObjectSet.pivotTo("equipmentOwner").selectProperty("groupName"),
  })
  .withProperties({
    equipmentTypeName: (baseObjectSet) =>
      baseObjectSet
        .pivotTo("equipmentType")
        .selectProperty("equipmentTypeName"),
  });

// load reservations and linked equipment in parallel
const [reservations, linkedEquipmentList] = await Promise.all([
  Array.fromAsync(reservationOS.asyncIter()),
  Array.fromAsync(linkedEquipmentOS.asyncIter()),
]);

// build a map from equipment id to its properties
const equipmentIdToEquipmentMap = new Map(
  linkedEquipmentList.map((eq) => [eq.equipmentId, eq]),
);
```

Note: Multi-hop derived properties could work here, but pivoting is appropriate when you need full materialized objects.

## Interacting with Media

To work with media in Foundry, you need to interact with media sets, media references, and media items. [See Media in README](README.md#media)

## Additional functions features (less common)

### Calling Platform APIs via Platform SDK

Use the Foundry Platform SDK to access administrative workflows, schedules, builds, media sets, user details, and more.

Note: For current user ID in actions, use a `currentUser` action parameter instead. Platform SDK is needed for other user details (ie name) or getting user ID outside actions.

Permission note: Some Platform SDK endpoints may return permission denied errors—this may require using a Foundry service user via an imported source (work in progress).

#### Setup

Install `@osdk/foundry` (add to package.json, then `./gradlew localDev` to rebuild). Find latest version: `npm info @osdk/foundry version` or check <https://www.npmjs.com/package/@osdk/foundry>

#### Usage

```typescript
import { Client } from "@osdk/client";
import { Admin } from "@osdk/foundry";

export default async function getCurrUsername(client: Client): Promise<string> {
  const user = await Admin.Users.getCurrent(client);
  return user.username; // also have user.id etc
}
```

#### More info

[Notifications section of README](README.md#notification-functions) Contains admin API examples (user / group info)

[language-models section of README](README.md#language-models) LLM API examples

To see full platform SDK for typescript: <https://github.com/palantir/foundry-platform-typescript>

### Functions for specific apps (workshop, vertex, maps, quiver)

Several no-code Foundry apps support advanced features that are only enabled via functions. For example, workshop widgets have custom charts, custom pivot tables, custom dynamic scheduling functions, etc.

#### Workshop functions

`Workshop` has a bunch of different custom interactions with Functions. For example, you can define function backed workshop variables. Object sets, Strings, Integers, Structs, etc, are all supported.

Use `interface` for structured return types. Fields can use any supported type:

```ts
import { Integer } from "@osdk/functions";

interface EquipmentSummary {
  name: string | undefined;
  serialNumber: string | undefined;
  reservationCount: Integer;
}
```

For charts, use [Function aggregations for workshop charts](https://www.palantir.com/docs/foundry/workshop/widgets-chart#function-aggregations-function-backed-layers). Use the [Two Dimensional Aggregation](README.md#two-dimensional-aggregation) or [Three Dimensional Aggregation](README.md#three-dimensional-aggregation) section of the README for type help.

```ts
import {
  Double,
  TwoDimensionalAggregation,
  ThreeDimensionalAggregation,
} from "@osdk/functions";

// 2D: array of { key, value } pairs
function myAgg(): TwoDimensionalAggregation<string, Double> {
  return [
    { key: "bucket1", value: 5.0 },
    { key: "bucket2", value: 6.0 },
  ];
}

// 3D: array of { key, groups: [{ key, value }] }
function my3DAgg(): ThreeDimensionalAggregation<string, string, Double> {
  return [
    {
      key: "group1",
      groups: [
        { key: "segment1", value: 5.0 },
        { key: "segment2", value: 6.0 },
      ],
    },
  ];
}
```

Workshop pivot tables

- [Function backed pivot tables](https://www.palantir.com/docs/foundry/workshop/widgets-pivot-table/#function-backed-pivot-tables)

Dynamic scheduling functions

- [Suggestion functions](https://www.palantir.com/docs/foundry/dynamic-scheduling/scheduling-suggestion-functions/) - Visually indicate suitable puck placements based on custom logic. Can optionally enforce placement to highlighted regions. Note: Results are static (evaluated on initial load only).
- [Search functions](https://www.palantir.com/docs/foundry/dynamic-scheduling/scheduling-search-functions/) - Help users find scheduling solutions. Can return pucks, time slots, or both. Supports row-based (right-click empty space) or puck-based (right-click puck) inputs.
- [validation rule functions](https://www.palantir.com/docs/foundry/dynamic-scheduling/scheduling-validation-rules/) -  Codify scheduling constraints. Rules evaluate on initial load and re-evaluate with each modification, showing users how changes comply with restrictions.
- [inline metrics functions](https://www.palantir.com/docs/foundry/dynamic-scheduling/scheduling-inline-metrics/) - Display key data directly in the chart. Header metrics align with the timeline (x-axis); row metrics align with individual resource rows.

Function backed columns

- See this docs page for an overview + examples of function backed columns (sometimes called function derived properties): [Function backed columns](https://www.palantir.com/docs/foundry/workshop/widgets-object-table#function-backed-columns)

#### Vertex

[Generate graphs using Functions](https://www.palantir.com/docs/foundry/vertex/generate-graph-functions/#generate-graphs-using-functions)

- Write complex search-around functions that return a graph of results from one or more objects. Requires exactly one argument (object type or list) and must return IGraphSearchAroundResultV1. A search-around is equivalent to a `pivotTo`

[Derived properties](https://www.palantir.com/docs/foundry/vertex/derive-property-functions/)

- Create derived properties on objects. These can be displayed in the object view, shown in extended node labels and used to color nodes in the layer styling options.

#### Maps

[Function-based styling](https://www.palantir.com/docs/foundry/map/integrate-functions/)

- Generate dynamic values for objects to display in the Selection panel or apply color-based styling.

#### Quiver

[Function-backed Time Series](https://www.palantir.com/docs/foundry/time-series/function-backed-time-series-getting-started/#getting-started-with-function-backed-time-series)

- Create time series for Quiver analyses enabling real-time forecasting workflows.

#### Notepad

[Functions-on-objects in Notepad](https://www.palantir.com/docs/foundry/notepad/widgets-functions)

- Using an object set or object parameter, compute values which will be inserted into a notepad document.

#### Chatbot Studio

[Chatbots as Functions](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions/)

- AIP Chatbots can be published as Functions and called from other functions.

### Calling LLMs

Large language models can be called from inside of functions. [See Language Models in README](README.md#language-models)

### Interacting with Media via attachments (legacy)

An attachment is a file that acts like an object property. Attachments are uploaded as temporary files and attached to objects using actions. Once attached to an object, an attachment is persisted and can be accessed similarly to other properties. Example:

```ts
import { ObjectTypeEx } from "@ontology/sdk";
import { Attachment, Client } from "@osdk/client";

// creates a new reservation for a piece of equipment
export default async function exampleFunc(
  client: Client,
  attachment: Attachment,
): Promise<OntologyEdit[]> {
  //...
  if ((await attachment.fetchMetadata()).filename.split(".").pop() !== "pdf") {
    // throw user facing error
  }

  const contentBlob = await attachment
    .fetchContents()
    .then((res) => res.blob());
  // can do whatever with blob / action in rest of function...

  /* Edit example
  editsBatch.create(ObjectTypeEx, {
    primaryKey_: randomUUID(),
    attachmentProp: attachment,
  }); */
}
```

### Using sources

If you want your function to be able to make external calls, you need to use a source (basically an egress tunnel). You can see added sources in the egress section of resources.json. [read sources.md for more information and examples](README.md#making-api-calls-to-external-systems)

### Notifications

Functions can be used to flexibly configure notifications that should be sent in the platform, including notifications that are sent externally to a user's email address. [Notifications section of README](README.md#notifications)

### Loading time series data

Some properties are time dependent properties, meaning they have associated time series data stored in a custom Foundry datastore. See [typescript v2 functions docs](https://www.palantir.com/docs/foundry/time-series/time-series-in-functions#typescript-v2-functions) for pulling this data.

### Custom aliases

Custom aliases hold configurable string values (config parameters, feature flags, environment-specific settings) in the `custom` section of `resources.json`, so functions stay portable instead of hard-coding values — useful for functions packaged via marketplace. See [Custom aliases](https://www.palantir.com/docs/foundry/functions/custom-aliases) for more info.

```json
"custom": { "myAlias": "someValue" }
```

```typescript
import { Aliases } from "@osdk/functions";

const value = Aliases.custom("myAlias");
```

## Best Practices

### Comments

- **Don't comment what the code literally does** — e.g., `// set x to 5` above `x = 5` is pure noise
- Comments explaining intent, business logic, "why" decisions, trade-offs, or domain context are valuable and should not be flagged
- When reviewing, err on the side of accepting comments — only flag them if they are clearly restating the obvious or are misleading/outdated
- Use `// TODO(@username)` for work that needs to be done later
- Use `// WARNING:` for edge cases or race conditions

  ```typescript
  // Good - explains non-obvious domain logic
  // "No links" means work group matches all facilities/payer plans
  const hasFacilityMatch = workGroupsWithNoFacilityLinks.has(wg.id) || ...

  // Bad - restates what the code obviously does
  // Check if facility matches
  const hasFacilityMatch = ...
  // Build the work group map
  const workGroupMap = new Map<string, WorkGroup>()
  ```

### Function Documentation

- Use JSDoc-style docstrings with Pre/Post conditions for complex functions. Always describe the Args:

```typescript
/**
 * Description of what the function does.
 *
 * @param {string} foo - description of foo
 * @param {Integer} bar - description of bar
 * @returns {Integer} output description
 */
```

### Fail fast

We should perform all validations as early as possible in our Functions. If validations fail, we can return early or throw an error before we perform costly work like fetching data. This both gets error messages to our users quicker and reduces the amount of load put on Foundry's services. This also helps to reduce nesting in our code.

Prefer:

```ts
if (!isValid(myThing)) {
  throw new UserFacingError("...");
}

doSomeWork();
```

### Naming Conventions

**Good names reduce the need for comments.** Code should read like well-written prose. If a name is unclear, consider improving it — but comments that explain intent, business context, or "why" are still valuable even alongside good names.

- Variables: camelCase
- Constants: SCREAMING_SNAKE_CASE for module-level constants
- Enums: PascalCase enum name, SCREAMING_SNAKE_CASE values (e.g., `TaskStatus.OPEN`)
- Classes: PascalCase
- Booleans: use verb prefixes like `is`, `has`, `does`, `should` (e.g., `isValid`, `hasMatch`, `shouldRetry`)
- **Function names must be semantic** - convey both the _what_ and the _why_:

```typescript
// Good - self-documenting, no comment needed
_findDeepestMatchingWorkGroup();
_validateUserPermissions();

// Bad - requires a comment to understand purpose
_traverseWorkGroupTree(); // what does traversing accomplish?
_processItems(); // process how? for what purpose?
```

### Iteration

- **Prefer functional array methods** over explicit loops: use `.forEach()`, `.map()`, `.filter()`, `.some()`, `.every()`, `.reduce()` instead of `for...of` or `for` loops

```typescript
// Good
items.forEach((x) => console.log(x.id))
items.map((x) => x.children.map((y) => y.name))

// Avoid
for (const item of items) { ... }
```

### Conditionals

- **Prefer one-line if statements** when the body is a single statement and fits within 100 characters (the prettier print width):

```typescript
// Good
if (myCondition) return false;
if (!isValid) throw new Error("Invalid");

// Avoid
if (myCondition) {
  return false;
}
```

Avoid complex ternary operations, they are hard to read.

## Review Priority After Writing Code

After writing code, or when reviewing code, prioritize in this order:

1. **Correctness** - Logic errors, missing error handling, type safety violations, Palantir (Functions) diagnostic errors
2. **Style violations** - Naming, formatting, patterns that deviate from standards
3. **Performance** - Inefficient patterns, unnecessary operations
4. **Maintainability** - Missing docs, unclear naming, code organization

## Rune

Use the repo-local Rune binary from the repository root. If `./rune` is missing, run `.palantir-scripts/install-rune`. Run `./rune --help` for current usage and flags.

### General Commands

- Use `./rune resources check` after editing `typescript-functions/resources.json`; it validates the file and prints JSON diagnostics.
- Use `./rune discover` after changing function names, signatures, imports, or parameter types.
- Use `./rune execute --name <functionName> --parameters '{"param":"value"}'` or `./rune execute --name <functionName> --parameters @params.json`. Parameters must be a JSON object. Run `./rune execute --help` for flags, including `--branch-rid` for global-branch preview when available.
- Do not invent RIDs or API names. Load the relevant repository, import, SDK, or Ontology context first.

### Local SDK Commands

- Use `./rune sdk generate` to manually re-generate a local SDK, migrate an existing repository to a local SDK, or generate against a specific Global branch (with `--branch-rid <branch-rid>`).
- To access the full feature set of Global Branching in TSv2, a repository must be using a local SDK.
