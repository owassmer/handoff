/**
 * Strict pure structural codecs backed by the bundled contract schemas.
 * This is deliberately not legal, authority, balance, or outcome validation.
 * No defaults, omitted nullables, unknown keys, coercion, or lossy money numbers.
 */
import reviewRequestSchema from "../resources/schemas/review-request.schema.json" with { type: "json" };
import reviewEnvelopeSchema from "../resources/schemas/review-envelope.schema.json" with { type: "json" };
import syntheticRuleSchema from "../resources/schemas/synthetic-rule-manifest.schema.json" with { type: "json" };
import safetySchema from "../resources/schemas/phase-a-safety.schema.json" with { type: "json" };
import phaseBSafetySchema from "../resources/schemas/phase-b-safety.schema.json" with { type: "json" };
import reviewRuleSchema from "../resources/schemas/phase-b-rule-release.schema.json" with { type: "json" };
import type * as Types from "./types.js";
import type { PhaseBSafetyProfile, ReviewRuleRelease } from "./phase_b_types.js";
import { is_calendar_date, normalize_timestamp } from "./datetime.js";
import { MAX_SAFE_INTEGER, SCHEMA_VERSION } from "./vocabulary.js";

export class ContractError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "ContractError";
  }
}

export type JsonValue = null | boolean | string | number | JsonValue[] | { [key: string]: JsonValue };

export interface ContractTypes {
  SourceReference: Types.SourceReference;
  EvidenceInput: Types.EvidenceInput;
  DateFact: Types.DateFact;
  CaseParty: Types.CaseParty;
  AuthorityGrant: Types.AuthorityGrant;
  RecipientInstructions: Types.RecipientInstructions;
  OpenQuestion: Types.OpenQuestion;
  ChargeInput: Types.ChargeInput;
  BalanceSnapshot: Types.BalanceSnapshot;
  MoneyEvent: Types.MoneyEvent;
  OtherBalance: Types.OtherBalance;
  StatementFact: Types.StatementFact;
  ApprovalFact: Types.ApprovalFact;
  RequestFact: Types.RequestFact;
  ExecutionFact: Types.ExecutionFact;
  RelatedTaskFact: Types.RelatedTaskFact;
  CaseSnapshot: Types.CaseSnapshot;
  ReviewRequest: Types.ReviewRequest;
  RequirementResult: Types.RequirementResult;
  ScopeRequirements: Types.ScopeRequirements;
  ItemDecision: Types.ItemDecision;
  AccountResult: Types.AccountResult;
  AvailableAction: Types.AvailableAction;
  TrackOutcome: Types.TrackOutcome;
  Outcomes: Types.Outcomes;
  ReviewResult: Types.ReviewResult;
  ReviewMetadata: Types.ReviewMetadata;
  ReviewEnvelope: Types.ReviewEnvelope;
  SyntheticAssumptions: Types.SyntheticAssumptions;
  SyntheticRuleManifest: Types.SyntheticRuleManifest;
  SafetyProfile: Types.SafetyProfile;
  PhaseBSafetyProfile: PhaseBSafetyProfile;
  ReviewRuleRelease: ReviewRuleRelease;
}
export type ContractName = keyof ContractTypes;

/** Schema features supported by the bundled contract validators. */
export interface Schema {
  $schema?: string;
  $id?: string;
  $ref?: string;
  $defs?: Record<string, Schema>;
  type?: string;
  properties?: Record<string, Schema>;
  required?: string[];
  additionalProperties?: boolean;
  anyOf?: Schema[];
  items?: Schema;
  enum?: JsonValue[];
  const?: JsonValue;
  minimum?: number;
  maximum?: number;
  minLength?: number;
  format?: string;
  pattern?: string;
  "x-foundry-type"?: string;
}

// Cast only the bundled static schema documents, never user input.
const DOCUMENTS: Schema[] = [
  reviewRequestSchema as Schema, reviewEnvelopeSchema as Schema,
  syntheticRuleSchema as Schema, safetySchema as Schema,
  phaseBSafetySchema as Schema, reviewRuleSchema as Schema,
];
const DEFINITIONS = new Map<string, Schema>(
  DOCUMENTS.flatMap((document): [string, Schema][] => Object.entries(document.$defs ?? {})),
);

export function is_plain_object(value: unknown): value is Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
  const prototype: unknown = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

/** Compare Unicode scalar values, not UTF-16 units or locale collation. */
export function compare_unicode(left: string, right: string): number {
  const a = Array.from(left, (character): number => character.codePointAt(0) ?? 0);
  const b = Array.from(right, (character): number => character.codePointAt(0) ?? 0);
  const length = Math.min(a.length, b.length);
  for (let index = 0; index < length; index += 1) {
    const x = a[index] ?? 0;
    const y = b[index] ?? 0;
    if (x !== y) return x < y ? -1 : 1;
  }
  return a.length < b.length ? -1 : a.length > b.length ? 1 : 0;
}

export function _optional(annotation: Schema): Schema | null {
  const alternatives = annotation.anyOf;
  if (alternatives?.length !== 2 || !alternatives.some((item): boolean => item.type === "null")) {
    return null;
  }
  return alternatives.find((item): boolean => item.type !== "null") ?? null;
}

function definition(name: string): Schema {
  const found = DEFINITIONS.get(name);
  if (found === undefined) throw new TypeError(`Unsupported contract annotation: ${name}`);
  return found;
}

/** Generate the reachable $defs graph and versioned contract identity. */
export function json_schema(root_type: ContractName): Schema {
  const definitions: Record<string, Schema> = {};
  const visit = (schema: Schema): void => {
    if (schema.$ref !== undefined) {
      const name = schema.$ref.slice("#/$defs/".length);
      if (!Object.hasOwn(definitions, name)) {
        const referenced = definition(name);
        definitions[name] = referenced;
        Object.values(referenced.properties ?? {}).forEach(visit);
      }
    }
    schema.anyOf?.forEach(visit);
    if (schema.items !== undefined) visit(schema.items);
  };
  const reference = { $ref: `#/$defs/${root_type}` };
  visit(reference);
  const version = root_type === "ReviewEnvelope" ? "1.1.0" : SCHEMA_VERSION;
  // Callers must not be able to mutate the shared validator through json_schema().
  return structuredClone({
    $schema: "https://json-schema.org/draft/2020-12/schema",
    $id: `urn:handoff:deposit-closeout:${root_type}:${version}`,
    ...reference,
    $defs: definitions,
  });
}

function assert_metadata(schema: Schema, raw: unknown, path: string): void {
  if (Object.hasOwn(schema, "const") && canonical_json(raw) !== canonical_json(schema.const)) {
    throw new ContractError(`${path}: unexpected constant value`);
  }
  if (schema.enum !== undefined && !schema.enum.some((entry): boolean => entry === raw)) {
    throw new ContractError(`${path}: unknown state ${JSON.stringify(raw)}`);
  }
  if (typeof raw === "number") {
    if (schema.minimum !== undefined && raw < schema.minimum) {
      throw new ContractError(`${path}: violates minimum`);
    }
    if (schema.maximum !== undefined && raw > schema.maximum) {
      throw new ContractError(`${path}: violates maximum`);
    }
  }
}

/** Decode against a DTO name or a generated schema node. */
export function _decode(annotation: ContractName | Schema, value: unknown, path: string): JsonValue {
  const schema = typeof annotation === "string" ? definition(annotation) : annotation;
  const optional = _optional(schema);
  let decoded: JsonValue;
  if (optional !== null) {
    decoded = value === null ? null : _decode(optional, value, path);
  } else if (schema.$ref !== undefined) {
    decoded = _decode(definition(schema.$ref.slice("#/$defs/".length)), value, path);
  } else if (schema.type === "integer") {
    if (typeof value !== "number" || !Number.isSafeInteger(value)
        || value < (schema.minimum ?? -MAX_SAFE_INTEGER)
        || value > (schema.maximum ?? MAX_SAFE_INTEGER)) {
      throw new ContractError(`${path}: expected an exact bounded integer, not bool/float/string`);
    }
    decoded = value === 0 ? 0 : value;
  } else if (schema.type === "boolean") {
    if (typeof value !== "boolean") throw new ContractError(`${path}: expected boolean`);
    decoded = value;
  } else if (schema.type === "string") {
    if (schema.format === "date") {
      if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
        throw new ContractError(`${path}: expected YYYY-MM-DD`);
      }
      if (!is_calendar_date(value)) throw new ContractError(`${path}: invalid calendar date`);
      decoded = value;
    } else if (schema.format === "date-time") {
      if (typeof value !== "string" || !value.endsWith("Z") || !value.includes("T")) {
        throw new ContractError(`${path}: expected an explicit UTC timestamp ending Z`);
      }
      const timestamp = normalize_timestamp(value);
      if (timestamp === null) throw new ContractError(`${path}: invalid timestamp`);
      decoded = timestamp;
    } else {
      if (typeof value !== "string" || value.length === 0) {
        throw new ContractError(`${path}: expected a non-empty string`);
      }
      decoded = value;
    }
  } else if (schema.type === "array") {
    if (!Array.isArray(value)) throw new ContractError(`${path}: expected an array`);
    const items = schema.items;
    if (items === undefined) throw new TypeError("Bundled array schema has no items");
    decoded = Array.from(value as unknown[], (entry, index): JsonValue =>
      _decode(items, entry, `${path}[${index}]`));
  } else if (schema.type === "object") {
    if (!is_plain_object(value)) throw new ContractError(`${path}: expected object`);
    const properties = schema.properties ?? {};
    const expected = Object.keys(properties);
    const actual = Object.keys(value);
    const missing = expected.filter((key): boolean => !Object.hasOwn(value, key));
    const unknown = actual.filter((key): boolean => !Object.hasOwn(properties, key));
    if (missing.length > 0 || unknown.length > 0) {
      throw new ContractError(`${path}: missing=${JSON.stringify(missing.sort(compare_unicode))}, unknown=${JSON.stringify(unknown.sort(compare_unicode))}`);
    }
    decoded = Object.fromEntries(Object.entries(properties).map(([key, property]): [string, JsonValue] =>
      [key, _decode(property, value[key], `${path}.${key}`)]));
  } else if (schema.type === "null" && value === null) {
    decoded = null;
  } else {
    throw new TypeError(`Unsupported contract annotation: ${JSON.stringify(schema)}`);
  }
  assert_metadata(schema, value, path);
  return decoded;
}

/** Validate a named DTO contract; all nullable fields remain required. */
export function from_wire<K extends ContractName>(root_type: K, value: unknown): ContractTypes[K];
export function from_wire<T>(root_type: ContractName, value: unknown): T;
export function from_wire(root_type: ContractName, value: unknown): unknown {
  return _decode(root_type, value, root_type);
}

/**
 * Pure JSON parser for the published JSON-string boundary. Unlike JSON.parse it
 * rejects duplicate decoded keys (including escaped aliases) before information
 * loss, and rejects float/exponent number lexemes even if they evaluate to 1.
 * Every numeric field in the bundled schemas is an exact bounded integer.
 */
export function parse_json(text: string): unknown {
  if (typeof text !== "string") throw new ContractError("Expected JSON text");
  let index = 0;
  const fail = (message: string): never => {
    throw new ContractError(`JSON at offset ${index}: ${message}`);
  };
  const whitespace = (): void => {
    while (index < text.length && /[\x20\t\r\n]/.test(text[index] ?? "")) index += 1;
  };
  const string = (): string => {
    const match = /^"(?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"/.exec(text.slice(index));
    if (match === null) return fail("invalid string");
    index += match[0].length;
    const decoded: unknown = JSON.parse(match[0]);
    if (typeof decoded !== "string") return fail("expected string");
    return decoded;
  };
  const read = (depth: number): JsonValue => {
    if (depth > 256) return fail("JSON nesting exceeds the contract boundary limit");
    whitespace();
    const token = text[index];
    if (token === '"') return string();
    if (token === "{") {
      index += 1;
      whitespace();
      const entries: [string, JsonValue][] = [];
      const names = new Set<string>();
      if (text[index] === "}") { index += 1; return {}; }
      while (index < text.length) {
        whitespace();
        const key = string();
        if (names.has(key)) return fail(`duplicate object key ${JSON.stringify(key)}`);
        names.add(key);
        whitespace();
        if (text[index] !== ":") return fail("expected ':'");
        index += 1;
        entries.push([key, read(depth + 1)]);
        whitespace();
        if (text[index] === "}") { index += 1; return Object.fromEntries(entries); }
        if (text[index] !== ",") return fail("expected ',' or '}'");
        index += 1;
      }
      return fail("unterminated object");
    }
    if (token === "[") {
      index += 1;
      whitespace();
      const values: JsonValue[] = [];
      if (text[index] === "]") { index += 1; return values; }
      while (index < text.length) {
        values.push(read(depth + 1));
        whitespace();
        if (text[index] === "]") { index += 1; return values; }
        if (text[index] !== ",") return fail("expected ',' or ']'");
        index += 1;
      }
      return fail("unterminated array");
    }
    if (text.startsWith("true", index)) { index += 4; return true; }
    if (text.startsWith("false", index)) { index += 5; return false; }
    if (text.startsWith("null", index)) { index += 4; return null; }
    const number = /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/.exec(text.slice(index));
    if (number === null) return fail("expected JSON value");
    const lexeme = number[0];
    if (/[.eE]/.test(lexeme)) return fail("expected integer token, not float/exponent");
    const exact = BigInt(lexeme);
    if (exact < -BigInt(MAX_SAFE_INTEGER) || exact > BigInt(MAX_SAFE_INTEGER)) {
      return fail("integer outside exact safe wire bounds");
    }
    index += lexeme.length;
    return Number(exact);
  };
  const value = read(0);
  whitespace();
  if (index !== text.length) return fail("unexpected trailing content");
  return value;
}

export const strict_json_parse = parse_json;

export function from_json<K extends ContractName>(root_type: K, text: string): ContractTypes[K] {
  return from_wire(root_type, parse_json(text));
}

/**
 * DTOs are plain objects. Strings already normalized by from_wire
 * are preserved; opaque user strings that resemble dates must never be changed.
 */
export function to_wire(value: unknown): JsonValue {
  if (value === null || typeof value === "boolean" || typeof value === "string") return value;
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) throw new ContractError("Unsupported non-exact wire number");
    return value === 0 ? 0 : value;
  }
  if (Array.isArray(value)) return Array.from(value as unknown[], to_wire);
  if (is_plain_object(value)) {
    return Object.fromEntries(Object.entries(value).map(([key, entry]): [string, JsonValue] =>
      [key, to_wire(entry)]));
  }
  throw new ContractError(`Unsupported wire value ${typeof value}`);
}

function encode_json(value: JsonValue): string {
  if (value === null) return "null";
  if (typeof value === "string") {
    // Reject unpaired surrogates to avoid silent replacement during UTF-8 hashing.
    if (!value.isWellFormed()) throw new ContractError("Wire string contains an unpaired surrogate");
    return JSON.stringify(value);
  }
  if (typeof value === "boolean" || typeof value === "number") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(encode_json).join(",")}]`;
  return `{${Object.keys(value).sort(compare_unicode).map((key): string => {
    const entry = value[key];
    if (entry === undefined) throw new ContractError("Unsupported undefined wire field");
    return `${encode_json(key)}:${encode_json(entry)}`;
  }).join(",")}}`;
}

/** ensure_ascii=False, Unicode-sorted keys, compact separators and exact integers. */
export function canonical_json(value: unknown): string {
  return encode_json(to_wire(value));
}
