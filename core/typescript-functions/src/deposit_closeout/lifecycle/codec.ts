/** Strict pure sidecar codecs. No SDK, clock reads, authority evaluation, or effects. */
import { canonical_json, ContractError, from_wire, is_plain_object, parse_json } from "../domain/codec.js";
import { compare_timestamps, is_calendar_date, normalize_timestamp } from "../domain/datetime.js";
import { fingerprint } from "../domain/fingerprints.js";
import { VOCABULARY } from "../domain/vocabulary.js";
import type { CaseSnapshot } from "../domain/types.js";
import {
  approvalIdFor, instructionHashFor, instructionKeyFor, recipientVersionIdFor, requestIdFor, statementContentHash,
  statementIdFor, targetVersionIdFor, workflowEventIdFor,
} from "./ids.js";
import {
  LIFECYCLE_COMMAND_KINDS, MAX_WORKFLOW_JSON_BYTES, MAX_WORKFLOW_RECORDS, OPERATION_KINDS,
  REQUEST_STATES, STATEMENT_KINDS, SYNTHETIC_STATEMENT_BADGE, WORKFLOW_COMPANY_ID,
  WORKFLOW_ENVIRONMENT_ID, WORKFLOW_SCHEMA_VERSION,
} from "./types.js";
import type * as T from "./types.js";

export { ContractError } from "../domain/codec.js";
export const canonicalJson = canonical_json;
type Decoder<T> = (value: unknown, path: string) => T;

function requireContract(condition: boolean, message: string): asserts condition {
  if (!condition) throw new ContractError(message);
}
function object(value: unknown, keys: readonly string[], path: string): Record<string, unknown> {
  requireContract(is_plain_object(value), `${path}: expected object`);
  const missing = keys.filter((key): boolean => !Object.hasOwn(value, key));
  const extra = Object.keys(value).filter((key): boolean => !keys.includes(key));
  requireContract(missing.length === 0 && extra.length === 0,
    `${path}: missing=${JSON.stringify(missing)}, unknown=${JSON.stringify(extra)}`);
  return value;
}
function text(value: unknown, path: string, limit: number = 2000): string {
  requireContract(typeof value === "string" && value.trim().length > 0 && value.isWellFormed()
    && Buffer.byteLength(value, "utf8") <= limit, `${path}: expected bounded non-empty well-formed text`);
  return value;
}
function id(value: unknown, path: string): string {
  const result = text(value, path, 200);
  requireContract(/^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$/.test(result), `${path}: invalid identifier`);
  return result;
}
function hash(value: unknown, path: string): string {
  const result = text(value, path, 64);
  requireContract(/^[a-f0-9]{64}$/.test(result), `${path}: expected SHA-256 hex`);
  return result;
}
function bool(value: unknown, path: string): boolean {
  requireContract(typeof value === "boolean", `${path}: expected boolean`);
  return value;
}
function member<T extends string>(value: unknown, values: readonly T[], path: string): T {
  const match = values.find((entry): boolean => entry === value);
  requireContract(match !== undefined, `${path}: unknown value`);
  return match;
}
function nullable<T>(value: unknown, decode: Decoder<T>, path: string): T | null {
  return value === null ? null : decode(value, path);
}
function cents(value: unknown, path: string): number {
  requireContract(typeof value === "number" && Number.isSafeInteger(value) && value >= 0,
    `${path}: expected nonnegative exact safe integer cents`);
  return value === 0 ? 0 : value;
}
function positive(value: unknown, path: string): number {
  const result = cents(value, path);
  requireContract(result > 0, `${path}: must be positive`);
  return result;
}
/** Strict ISO UTC with <= microsecond precision; no silent submicrosecond truncation. */
export function parseWorkflowTimestamp(value: unknown, path: string = "timestamp"): string {
  requireContract(typeof value === "string" && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$/.test(value),
    `${path}: expected explicit UTC timestamp with at most six fractional digits`);
  const result = normalize_timestamp(value);
  requireContract(result !== null, `${path}: invalid timestamp`);
  return result;
}
function date(value: unknown, path: string): string {
  const result = text(value, path, 10);
  requireContract(is_calendar_date(result), `${path}: expected valid calendar date`);
  return result;
}
function array<T>(value: unknown, decode: Decoder<T>, path: string): T[] {
  requireContract(Array.isArray(value) && value.length <= MAX_WORKFLOW_RECORDS,
    `${path}: expected bounded array`);
  return Array.from(value as unknown[], (entry, index): T => decode(entry, `${path}[${index}]`));
}
function unique(values: readonly string[], path: string): void {
  requireContract(new Set(values).size === values.length, `${path}: duplicate identity`);
}
function ids(value: unknown, path: string): string[] {
  const result = array(value, id, path);
  unique(result, path);
  return result;
}
function boundedJson(json: unknown): string {
  requireContract(typeof json === "string" && Buffer.byteLength(json, "utf8") < MAX_WORKFLOW_JSON_BYTES,
    "Workflow JSON must be less than 256 KiB UTF-8; it is never truncated");
  return json;
}
function readJson(json: string): unknown {
  const value = parse_json(boundedJson(json));
  // Also rejects unpaired Unicode surrogates anywhere, including native DTOs.
  canonical_json(value);
  return value;
}
function scope(value: Record<string, unknown>, path: string): T.WorkflowScope {
  return { caseId: id(value.caseId, `${path}.caseId`),
    managementCompanyId: member(value.managementCompanyId, [WORKFLOW_COMPANY_ID], `${path}.managementCompanyId`),
    environmentId: member(value.environmentId, [WORKFLOW_ENVIRONMENT_ID], `${path}.environmentId`) };
}
const SCOPE_KEYS = ["caseId", "managementCompanyId", "environmentId"];
function sameScope(left: T.WorkflowScope, right: T.WorkflowScope, path: string): void {
  requireContract(left.caseId === right.caseId && left.managementCompanyId === right.managementCompanyId
    && left.environmentId === right.environmentId, `${path}: cross-case/company/environment reference`);
}
function noLater(value: string, limit: string, path: string): void {
  requireContract(compare_timestamps(value, limit) <= 0, `${path}: timestamp exceeds its enclosing clock`);
}

/** Long strings never coerce, round, or accept amounts outside native exact bounds. */
export function checkedMoneyLong(value: unknown, path: string = "money"): number {
  requireContract(typeof value === "string" && /^(0|[1-9][0-9]{0,18})$/.test(value),
    `${path}: expected canonical nonnegative Long string`);
  const exact = BigInt(value);
  requireContract(exact <= BigInt(Number.MAX_SAFE_INTEGER), `${path}: outside native exact integer bounds`);
  return Number(exact);
}
export function centsToLong(value: number): string { return String(cents(value, "money")); }

function instructions(value: unknown, path: string, withVersion: true): T.OperationInstructions;
function instructions(value: unknown, path: string, withVersion: false): T.OperationInstructionsInput;
function instructions(value: unknown, path: string, withVersion: boolean): T.OperationInstructionsInput | T.OperationInstructions {
  const v = object(value, ["partyIds", "state", "method", "routeReference", "evidenceIds",
    ...(withVersion ? ["versionId"] : [])], path);
  const route = nullable(v.routeReference, (entry, p): string => text(entry, p, 205), `${path}.routeReference`);
  requireContract(route === null || /^demo-[A-Za-z0-9][A-Za-z0-9._-]{0,199}$/.test(route),
    `${path}: use only an opaque demo- route reference, never a real destination`);
  const result: T.OperationInstructionsInput = {
    partyIds: ids(v.partyIds, `${path}.partyIds`),
    state: member(v.state, ["VERIFIED", "UNCONFIRMED"], `${path}.state`),
    method: nullable(v.method, (entry, p): "DEMO_OUTBOX" => member(entry, ["DEMO_OUTBOX"], p), `${path}.method`),
    routeReference: route, evidenceIds: ids(v.evidenceIds, `${path}.evidenceIds`),
  };
  if (result.state === "VERIFIED") {
    requireContract(result.partyIds.length > 0 && result.evidenceIds.length > 0
      && result.method === "DEMO_OUTBOX" && result.routeReference !== null,
    `${path}: verified instructions require parties, evidence and a demo route`);
  }
  return withVersion ? { ...result, versionId: id(v.versionId, `${path}.versionId`) } : result;
}
function validateIntentShape(intent: T.OperationIntentSpec, path: string): void {
  const reversal = intent.kind === "CHARGE_POSTING_REVERSAL" || intent.kind === "DEPOSIT_APPLICATION_REVERSAL";
  requireContract(reversal === (intent.reversesTransactionId !== null),
    `${path}: reversal operations require an original transaction; other kinds cannot reverse`);
  if (intent.kind === "STATEMENT_DISPATCH") {
    requireContract(intent.amountCents === null && intent.statementId !== null,
      `${path}: statement dispatch needs a statement and null amount`);
  } else {
    requireContract(intent.amountCents !== null && intent.amountCents > 0,
      `${path}: financial operations require positive exact cents`);
  }
}
function intentSpec(value: unknown, path: string): T.OperationIntentSpec {
  const v = object(value, ["kind", "amountCents", "dispositionKey", "statementId", "replacesRequestId", "reversesTransactionId"], path);
  const result: T.OperationIntentSpec = {
    kind: member(v.kind, OPERATION_KINDS, `${path}.kind`), amountCents: nullable(v.amountCents, cents, `${path}.amountCents`),
    dispositionKey: id(v.dispositionKey, `${path}.dispositionKey`), statementId: nullable(v.statementId, id, `${path}.statementId`),
    replacesRequestId: nullable(v.replacesRequestId, id, `${path}.replacesRequestId`),
    reversesTransactionId: nullable(v.reversesTransactionId, id, `${path}.reversesTransactionId`),
  };
  validateIntentShape(result, path);
  return result;
}
function intent(value: unknown, path: string): T.OperationIntent {
  requireContract(is_plain_object(value), `${path}: expected intent`);
  const kind = member(value.kind, OPERATION_KINDS, `${path}.kind`);
  const v = object(value, ["kind", "amountCents", "currency", "dispositionKey", "statementId", "recipientVersionId",
    "materialityHash", "targetVersionId", "replacesRequestId", "reversesTransactionId",
    ...(kind === "STATEMENT_DISPATCH" ? ["contentHash"] : [])], path);
  const spec = intentSpec({ kind, amountCents: v.amountCents, dispositionKey: v.dispositionKey,
    statementId: v.statementId, replacesRequestId: v.replacesRequestId,
    reversesTransactionId: v.reversesTransactionId }, path);
  const common = {
    currency: member(v.currency, ["USD"], `${path}.currency`), dispositionKey: spec.dispositionKey,
    materialityHash: hash(v.materialityHash, `${path}.materialityHash`), targetVersionId: id(v.targetVersionId, `${path}.targetVersionId`),
    replacesRequestId: spec.replacesRequestId,
  };
  if (kind === "STATEMENT_DISPATCH") {
    return { ...common, kind, amountCents: null, statementId: id(v.statementId, `${path}.statementId`),
      recipientVersionId: id(v.recipientVersionId, `${path}.recipientVersionId`),
      contentHash: hash(v.contentHash, `${path}.contentHash`), reversesTransactionId: null };
  }
  const recipient = nullable(v.recipientVersionId, id, `${path}.recipientVersionId`);
  requireContract((kind === "REFUND") === (recipient !== null),
    `${path}: only refunds have financial recipient instructions`);
  return { ...common, kind, amountCents: positive(v.amountCents, `${path}.amountCents`),
    statementId: spec.statementId, recipientVersionId: recipient, reversesTransactionId: spec.reversesTransactionId };
}
function statementContent(value: unknown, path: string): T.StatementContent {
  const v = object(value, ["mode", "syntheticBadge", "title", "parties", "dates", "items", "account", "sourceReferences"], path);
  const result: T.StatementContent = {
    mode: member(v.mode, ["SIMULATED"], `${path}.mode`),
    syntheticBadge: member(v.syntheticBadge, [SYNTHETIC_STATEMENT_BADGE], `${path}.syntheticBadge`),
    title: text(v.title, `${path}.title`),
    parties: array(v.parties, (entry, p): T.StatementPartyLabel => {
      const party = object(entry, ["partyId", "displayLabel"], p);
      return { partyId: id(party.partyId, `${p}.partyId`), displayLabel: text(party.displayLabel, `${p}.displayLabel`) };
    }, `${path}.parties`),
    dates: array(v.dates, (entry, p): T.StatementDate => {
      const fact = object(entry, ["factKey", "state", "value"], p);
      return { factKey: member(fact.factKey, VOCABULARY.dateKey, `${p}.factKey`),
        state: member(fact.state, VOCABULARY.factState, `${p}.state`), value: nullable(fact.value, date, `${p}.value`) };
    }, `${path}.dates`),
    items: array(v.items, (entry, p): T.StatementLine => {
      const line = object(entry, ["itemId", "location", "description", "decision"], p);
      const result: T.StatementLine = { itemId: id(line.itemId, `${p}.itemId`), location: text(line.location, `${p}.location`),
        description: text(line.description, `${p}.description`), decision: from_wire("ItemDecision", line.decision) };
      requireContract(result.itemId === result.decision.itemId, `${p}: line/decision item mismatch`);
      return result;
    }, `${path}.items`),
    account: from_wire("AccountResult", v.account),
    sourceReferences: array(v.sourceReferences, (entry): T.StatementContent["sourceReferences"][number] =>
      from_wire("SourceReference", entry), `${path}.sourceReferences`),
  };
  unique(result.parties.map((entry): string => entry.partyId), `${path}.parties`);
  unique(result.dates.map((entry): string => entry.factKey), `${path}.dates`);
  unique(result.items.map((entry): string => entry.itemId), `${path}.items`);
  requireContract(result.account.currency === "USD", `${path}: expected USD account`);
  return result;
}
function statement(value: unknown, path: string): T.StatementVersionRecord {
  const v = object(value, [...SCOPE_KEYS, "statementId", "kind", "createdCommandId", "createdBy", "createdAt", "businessCreatedAt",
    "sourceReviewId", "materialityHash", "contentHash", "recipientVersionId", "content", "renderedText", "supersedesStatementId"], path);
  const result: T.StatementVersionRecord = { ...scope(v, path),
    statementId: id(v.statementId, `${path}.statementId`), kind: member(v.kind, STATEMENT_KINDS, `${path}.kind`),
    createdCommandId: id(v.createdCommandId, `${path}.createdCommandId`), createdBy: id(v.createdBy, `${path}.createdBy`),
    createdAt: parseWorkflowTimestamp(v.createdAt, `${path}.createdAt`),
    businessCreatedAt: parseWorkflowTimestamp(v.businessCreatedAt, `${path}.businessCreatedAt`),
    sourceReviewId: id(v.sourceReviewId, `${path}.sourceReviewId`), materialityHash: hash(v.materialityHash, `${path}.materialityHash`),
    contentHash: hash(v.contentHash, `${path}.contentHash`), recipientVersionId: id(v.recipientVersionId, `${path}.recipientVersionId`),
    content: statementContent(v.content, `${path}.content`), renderedText: text(v.renderedText, `${path}.renderedText`, 64 * 1024),
    supersedesStatementId: nullable(v.supersedesStatementId, id, `${path}.supersedesStatementId`),
  };
  requireContract(result.renderedText.includes(SYNTHETIC_STATEMENT_BADGE), `${path}: rendered text must retain the synthetic badge`);
  requireContract(result.contentHash === statementContentHash(result.content, result.renderedText), `${path}: content hash mismatch`);
  requireContract(result.statementId === statementIdFor(result, result), `${path}: statement identity mismatch`);
  return result;
}
function approval(value: unknown, path: string): T.ApprovalRecord {
  const v = object(value, [...SCOPE_KEYS, "approvalId", "createdCommandId", "actorId", "actorPartyId", "authorityVersion",
    "scope", "intent", "decision", "decidedAt", "revokesApprovalId"], path);
  const result: T.ApprovalRecord = { ...scope(v, path), approvalId: id(v.approvalId, `${path}.approvalId`),
    createdCommandId: id(v.createdCommandId, `${path}.createdCommandId`), actorId: id(v.actorId, `${path}.actorId`),
    actorPartyId: id(v.actorPartyId, `${path}.actorPartyId`), authorityVersion: id(v.authorityVersion, `${path}.authorityVersion`),
    scope: member(v.scope, OPERATION_KINDS, `${path}.scope`), intent: intent(v.intent, `${path}.intent`),
    decision: member(v.decision, ["APPROVED", "REJECTED", "REVOKED"], `${path}.decision`),
    decidedAt: parseWorkflowTimestamp(v.decidedAt, `${path}.decidedAt`),
    revokesApprovalId: nullable(v.revokesApprovalId, id, `${path}.revokesApprovalId`),
  };
  requireContract(result.scope === result.intent.kind, `${path}: approval scope/intent mismatch`);
  requireContract((result.decision === "REVOKED") === (result.revokesApprovalId !== null), `${path}: invalid revocation reference`);
  requireContract(result.intent.targetVersionId === targetVersionIdFor(result, result.intent), `${path}: target identity mismatch`);
  requireContract(result.approvalId === approvalIdFor(result, result.createdCommandId, result.actorId), `${path}: approval identity mismatch`);
  return result;
}
function request(value: unknown, path: string): T.RequestInstruction {
  const v = object(value, [...SCOPE_KEYS, "requestId", "instructionKey", "createdCommandId", "kind", "intent", "instructions",
    "instructionHash", "approvalIds", "createdBy", "createdAt", "businessCreatedAt", "replacesRequestId", "reversesTransactionId"], path);
  const result: T.RequestInstruction = { ...scope(v, path), requestId: id(v.requestId, `${path}.requestId`),
    instructionKey: id(v.instructionKey, `${path}.instructionKey`), createdCommandId: id(v.createdCommandId, `${path}.createdCommandId`),
    kind: member(v.kind, OPERATION_KINDS, `${path}.kind`), intent: intent(v.intent, `${path}.intent`),
    instructions: nullable(v.instructions, (entry, p): T.OperationInstructions => instructions(entry, p, true), `${path}.instructions`),
    instructionHash: hash(v.instructionHash, `${path}.instructionHash`), approvalIds: ids(v.approvalIds, `${path}.approvalIds`),
    createdBy: id(v.createdBy, `${path}.createdBy`), createdAt: parseWorkflowTimestamp(v.createdAt, `${path}.createdAt`),
    businessCreatedAt: parseWorkflowTimestamp(v.businessCreatedAt, `${path}.businessCreatedAt`),
    replacesRequestId: nullable(v.replacesRequestId, id, `${path}.replacesRequestId`),
    reversesTransactionId: nullable(v.reversesTransactionId, id, `${path}.reversesTransactionId`),
  };
  requireContract(result.kind === result.intent.kind && result.replacesRequestId === result.intent.replacesRequestId
    && result.reversesTransactionId === result.intent.reversesTransactionId, `${path}: inconsistent intent links`);
  const routed = result.kind === "REFUND" || result.kind === "STATEMENT_DISPATCH";
  requireContract(routed === (result.instructions !== null), `${path}: route snapshot is required only for refund/dispatch`);
  requireContract(result.instructions === null || result.instructions.versionId === result.intent.recipientVersionId,
    `${path}: recipient version mismatch`);
  requireContract(result.approvalIds.length > 0, `${path}: approval references required`);
  requireContract(result.intent.targetVersionId === targetVersionIdFor(result, result.intent), `${path}: target identity mismatch`);
  requireContract(result.requestId === requestIdFor(result, result.intent)
    && result.instructionKey === instructionKeyFor(result, result.intent), `${path}: request identity mismatch`);
  requireContract(result.instructionHash === instructionHashFor(result, result.intent, result.instructions), `${path}: instruction hash mismatch`);
  return result;
}
function rawResult(value: unknown, path: string): T.RawSimulatedResult {
  const v = object(value, ["requestId", "attemptId", "sourceEventId", "kind", "operationKind", "instructionHash", "amountCents",
    "currency", "recipientVersionId", "canonicalTransactionId", "returnOfCanonicalTransactionId"], path);
  const result: T.RawSimulatedResult = {
    requestId: id(v.requestId, `${path}.requestId`), attemptId: id(v.attemptId, `${path}.attemptId`),
    sourceEventId: id(v.sourceEventId, `${path}.sourceEventId`), kind: member(v.kind, ["SUCCEEDED", "FAILED", "RETURNED"], `${path}.kind`),
    operationKind: member(v.operationKind, OPERATION_KINDS, `${path}.operationKind`), instructionHash: hash(v.instructionHash, `${path}.instructionHash`),
    amountCents: nullable(v.amountCents, positive, `${path}.amountCents`), currency: member(v.currency, ["USD"], `${path}.currency`),
    recipientVersionId: nullable(v.recipientVersionId, id, `${path}.recipientVersionId`),
    canonicalTransactionId: nullable(v.canonicalTransactionId, id, `${path}.canonicalTransactionId`),
    returnOfCanonicalTransactionId: nullable(v.returnOfCanonicalTransactionId, id, `${path}.returnOfCanonicalTransactionId`),
  };
  requireContract((result.operationKind === "STATEMENT_DISPATCH") === (result.amountCents === null), `${path}: invalid result amount shape`);
  if (result.operationKind === "STATEMENT_DISPATCH" || result.kind === "FAILED") {
    requireContract(result.canonicalTransactionId === null && result.returnOfCanonicalTransactionId === null
      && result.kind !== "RETURNED", `${path}: non-economic result cannot identify a transaction`);
  } else if (result.kind === "SUCCEEDED") {
    requireContract(result.canonicalTransactionId !== null && result.returnOfCanonicalTransactionId === null,
      `${path}: success requires one canonical transaction`);
  } else {
    requireContract(result.canonicalTransactionId !== null && result.returnOfCanonicalTransactionId !== null
      && result.canonicalTransactionId !== result.returnOfCanonicalTransactionId, `${path}: return requires distinct original/return transactions`);
  }
  return result;
}
function event(value: unknown, path: string): T.WorkflowEvent {
  const v = object(value, ["eventId", "sequence", "category", "kind", "caseId", "commandId", "requestId", "attemptId",
    "sourceEventId", "occurredAt", "learnedAt", "recordedAt", "recordedBy", "mode", "payload"], path);
  const common: T.WorkflowEventBase = {
    eventId: id(v.eventId, `${path}.eventId`), sequence: positive(v.sequence, `${path}.sequence`), caseId: id(v.caseId, `${path}.caseId`),
    commandId: id(v.commandId, `${path}.commandId`), requestId: nullable(v.requestId, id, `${path}.requestId`),
    attemptId: nullable(v.attemptId, id, `${path}.attemptId`), sourceEventId: nullable(v.sourceEventId, id, `${path}.sourceEventId`),
    occurredAt: parseWorkflowTimestamp(v.occurredAt, `${path}.occurredAt`), learnedAt: parseWorkflowTimestamp(v.learnedAt, `${path}.learnedAt`),
    recordedAt: parseWorkflowTimestamp(v.recordedAt, `${path}.recordedAt`), recordedBy: id(v.recordedBy, `${path}.recordedBy`),
    mode: member(v.mode, ["SIMULATED"], `${path}.mode`),
  };
  const kind = member(v.kind, ["REQUEST_CREATED", "ATTEMPT_CLAIMED", "REQUESTED", "ACKNOWLEDGED", "OUTCOME_UNKNOWN",
    "CANCELLED_BEFORE_ATTEMPT", "SUPERSEDED_BEFORE_ATTEMPT", "RAW_SIMULATED_RESULT", "RESULT_ACCEPTED"], `${path}.kind`);
  const isResult = kind === "RAW_SIMULATED_RESULT" || kind === "RESULT_ACCEPTED";
  requireContract(v.category === (isResult ? "SIMULATED_RESULT" : "REQUEST_LIFECYCLE"), `${path}: event category mismatch`);
  requireContract(common.requestId !== null, `${path}: this event kind requires a request`);
  const unattempted = ["REQUEST_CREATED", "CANCELLED_BEFORE_ATTEMPT", "SUPERSEDED_BEFORE_ATTEMPT"].includes(kind);
  requireContract(unattempted === (common.attemptId === null) && isResult === (common.sourceEventId !== null),
    `${path}: invalid attempt/source references for event kind`);
  noLater(common.occurredAt, common.learnedAt, `${path}.occurredAt`);
  if (kind === "RAW_SIMULATED_RESULT") {
    const payload = rawResult(v.payload, `${path}.payload`);
    requireContract(payload.requestId === common.requestId && payload.attemptId === common.attemptId
      && payload.sourceEventId === common.sourceEventId, `${path}: raw result identity mismatch`);
    return { ...common, category: "SIMULATED_RESULT", kind, payload };
  }
  if (kind === "RESULT_ACCEPTED") {
    const p = object(v.payload, ["rawEventId", "instructionHash", "canonicalTransactionId", "returnOfCanonicalTransactionId"], `${path}.payload`);
    return { ...common, category: "SIMULATED_RESULT", kind, payload: {
      rawEventId: id(p.rawEventId, `${path}.payload.rawEventId`), instructionHash: hash(p.instructionHash, `${path}.payload.instructionHash`),
      canonicalTransactionId: nullable(p.canonicalTransactionId, id, `${path}.payload.canonicalTransactionId`),
      returnOfCanonicalTransactionId: nullable(p.returnOfCanonicalTransactionId, id, `${path}.payload.returnOfCanonicalTransactionId`),
    } };
  }
  if (kind === "SUPERSEDED_BEFORE_ATTEMPT") {
    const p = object(v.payload, ["reason", "replacementRequestId"], `${path}.payload`);
    return { ...common, category: "REQUEST_LIFECYCLE", kind, payload: {
      reason: text(p.reason, `${path}.payload.reason`), replacementRequestId: nullable(p.replacementRequestId, id, `${path}.payload.replacementRequestId`),
    } };
  }
  if (kind === "OUTCOME_UNKNOWN" || kind === "CANCELLED_BEFORE_ATTEMPT") {
    const p = object(v.payload, ["reason"], `${path}.payload`);
    return { ...common, category: "REQUEST_LIFECYCLE", kind, payload: { reason: text(p.reason, `${path}.payload.reason`) } };
  }
  const p = object(v.payload, ["instructionHash"], `${path}.payload`);
  return { ...common, category: "REQUEST_LIFECYCLE", kind,
    payload: { instructionHash: hash(p.instructionHash, `${path}.payload.instructionHash`) } };
}

/** Structural cross-record invariants only. No approval validity or lifecycle reducer here. */
function validateStateReferences(state: T.WorkflowStateV2): void {
  const statements = new Map(state.statements.map((entry): [string, T.StatementVersionRecord] => [entry.statementId, entry]));
  const approvals = new Map(state.approvals.map((entry): [string, T.ApprovalRecord] => [entry.approvalId, entry]));
  const requests = new Map(state.requests.map((entry): [string, T.RequestInstruction] => [entry.requestId, entry]));
  unique(state.statements.map((entry): string => entry.statementId), "statements");
  unique(state.approvals.map((entry): string => entry.approvalId), "approvals");
  unique(state.requests.map((entry): string => entry.requestId), "requests");
  unique(state.requests.map((entry): string => entry.instructionKey), "instruction keys");
  unique(state.events.map((entry): string => entry.eventId), "events");
  requireContract(state.currentStatementId === null || statements.has(state.currentStatementId), "Missing current statement");
  const routeVersions = new Map<string, string>();
  const checkRouteVersion = (channel: "STATEMENT" | "REFUND", route: T.OperationInstructions): void => {
    const key = `${channel}:${route.versionId}`;
    const content = recipientVersionIdFor(state, channel, route);
    const previous = routeVersions.get(key);
    requireContract(previous === undefined || previous === content, "Recipient version reused with different content");
    routeVersions.set(key, content);
  };
  checkRouteVersion("STATEMENT", state.statementInstructions);
  checkRouteVersion("REFUND", state.refundInstructions);
  const priorStatements = new Set<string>();
  state.statements.forEach((record): void => {
    sameScope(record, state, "statement");
    noLater(state.initializedAt, record.createdAt, "statement creation");
    noLater(record.businessCreatedAt, state.businessClock, "statement business creation");
    requireContract(record.supersedesStatementId === null || priorStatements.has(record.supersedesStatementId),
      "Statement supersession must reference an earlier statement");
    priorStatements.add(record.statementId);
  });
  const checkIntentStatement = (record: T.OperationIntent): void => {
    requireContract(record.replacesRequestId === null || requests.has(record.replacesRequestId), "Intent replacement request is missing");
    if (record.statementId === null) return;
    const basis = statements.get(record.statementId);
    requireContract(basis !== undefined, "Intent refers to a missing statement");
    if (record.kind === "STATEMENT_DISPATCH") {
      requireContract(record.contentHash === basis.contentHash && record.materialityHash === basis.materialityHash
        && record.recipientVersionId === basis.recipientVersionId, "Dispatch intent differs from frozen statement");
    }
  };
  const priorApprovals = new Set<string>();
  state.approvals.forEach((record): void => {
    sameScope(record, state, "approval");
    noLater(state.initializedAt, record.decidedAt, "approval decision");
    checkIntentStatement(record.intent);
    if (record.revokesApprovalId !== null) {
      const revoked = approvals.get(record.revokesApprovalId);
      requireContract(priorApprovals.has(record.revokesApprovalId) && revoked !== undefined
        && revoked.decision === "APPROVED" && revoked.intent.targetVersionId === record.intent.targetVersionId,
      "Revocation must reference an earlier approved decision for the same target");
    }
    priorApprovals.add(record.approvalId);
  });
  const priorRequests = new Set<string>();
  state.requests.forEach((record): void => {
    sameScope(record, state, "request");
    if (record.instructions !== null) {
      checkRouteVersion(record.kind === "REFUND" ? "REFUND" : "STATEMENT", record.instructions);
    }
    noLater(state.initializedAt, record.createdAt, "request creation");
    noLater(record.businessCreatedAt, state.businessClock, "request business creation");
    checkIntentStatement(record.intent);
    requireContract(record.replacesRequestId === null || priorRequests.has(record.replacesRequestId),
      "Replacement must reference an earlier request");
    record.approvalIds.forEach((approvalId): void => {
      const reference = approvals.get(approvalId);
      requireContract(reference !== undefined && reference.decision === "APPROVED"
        && reference.intent.targetVersionId === record.intent.targetVersionId, "Request has a missing or mismatched approval");
      noLater(reference.decidedAt, record.createdAt, "request approval");
    });
    priorRequests.add(record.requestId);
  });
  const events = new Map<string, T.WorkflowEvent>();
  const created = new Set<string>();
  const attempts = new Map<string, string>();
  let previousLearnedAt: string | null = null;
  state.events.forEach((record, index): void => {
    requireContract(record.sequence === index + 1, "Event sequences must be contiguous, ordered and start at one");
    requireContract(record.caseId === state.caseId, "Event refers to another case");
    requireContract(record.eventId === workflowEventIdFor(state, record), "Event identity mismatch");
    noLater(record.learnedAt, state.businessClock, "event learned time");
    noLater(state.initializedAt, record.recordedAt, "event recording");
    if (previousLearnedAt !== null) noLater(previousLearnedAt, record.learnedAt, "event order");
    previousLearnedAt = record.learnedAt;
    const instruction = record.requestId === null ? undefined : requests.get(record.requestId);
    requireContract(instruction !== undefined, "Event refers to a missing request");
    if (record.kind === "REQUEST_CREATED") {
      requireContract(!created.has(instruction.requestId), "Duplicate request creation event");
      created.add(instruction.requestId);
    } else {
      requireContract(created.has(instruction.requestId), "Event precedes request creation");
    }
    if (record.kind === "ATTEMPT_CLAIMED") {
      requireContract(record.attemptId !== null && !attempts.has(record.attemptId), "Duplicate/missing attempt identity");
      attempts.set(record.attemptId, instruction.requestId);
    } else if (record.attemptId !== null) {
      requireContract(attempts.get(record.attemptId) === instruction.requestId, "Event has no earlier matching attempt claim");
    }
    if (record.kind === "REQUEST_CREATED" || record.kind === "ATTEMPT_CLAIMED"
      || record.kind === "REQUESTED" || record.kind === "ACKNOWLEDGED") {
      requireContract(record.payload.instructionHash === instruction.instructionHash, "Lifecycle event instruction mismatch");
    }
    if (record.kind === "SUPERSEDED_BEFORE_ATTEMPT" && record.payload.replacementRequestId !== null) {
      const replacement = requests.get(record.payload.replacementRequestId);
      requireContract(replacement !== undefined && replacement.replacesRequestId === instruction.requestId
        && replacement.kind === instruction.kind, "Supersession must reference its replacement instruction of the same kind");
    }
    if (record.kind === "RESULT_ACCEPTED") {
      const raw = events.get(record.payload.rawEventId);
      requireContract(raw?.kind === "RAW_SIMULATED_RESULT" && raw.requestId === record.requestId
        && raw.attemptId === record.attemptId && raw.sourceEventId === record.sourceEventId,
      "Acceptance requires an earlier matching raw result");
      requireContract(raw.payload.instructionHash === record.payload.instructionHash
        && raw.payload.canonicalTransactionId === record.payload.canonicalTransactionId
        && raw.payload.returnOfCanonicalTransactionId === record.payload.returnOfCanonicalTransactionId,
      "Accepted result must preserve the raw result identity");
    }
    events.set(record.eventId, record);
  });
  requireContract(created.size === state.requests.length, "Each request requires exactly one creation event");
}

/** Full nested decoding and structural integrity. Semantic transitions belong to the reducer. */
export function parseWorkflowState(sourceJson: string): T.WorkflowStateV2 {
  const v = object(readJson(sourceJson), [...SCOPE_KEYS, "schemaVersion", "mode", "initializedBy", "initializedAt", "businessClock",
    "statementInstructions", "refundInstructions", "statements", "approvals", "requests", "events", "currentStatementId"], "WorkflowStateV2");
  const result: T.WorkflowStateV2 = { ...scope(v, "WorkflowStateV2"),
    schemaVersion: member(v.schemaVersion, [WORKFLOW_SCHEMA_VERSION], "schemaVersion"), mode: member(v.mode, ["SIMULATED"], "mode"),
    initializedBy: id(v.initializedBy, "initializedBy"), initializedAt: parseWorkflowTimestamp(v.initializedAt, "initializedAt"),
    businessClock: parseWorkflowTimestamp(v.businessClock, "businessClock"),
    statementInstructions: instructions(v.statementInstructions, "statementInstructions", true),
    refundInstructions: instructions(v.refundInstructions, "refundInstructions", true),
    statements: array(v.statements, statement, "statements"), approvals: array(v.approvals, approval, "approvals"),
    requests: array(v.requests, request, "requests"), events: array(v.events, event, "events"),
    currentStatementId: nullable(v.currentStatementId, id, "currentStatementId"),
  };
  validateStateReferences(result);
  boundedJson(canonical_json(result));
  return result;
}

/** Cross-sidecar/native references, not native review recomputation or authority. */
export function validateWorkflowCaseReferences(state: T.WorkflowStateV2, snapshot: CaseSnapshot): void {
  requireContract(state.caseId === snapshot.caseId && state.managementCompanyId === snapshot.managementCompanyId,
    "Workflow and native snapshot scopes differ");
  const partyIds = new Set(snapshot.parties.map((party): string => party.partyId));
  const evidenceIds = new Set(snapshot.evidence.map((entry): string => entry.evidenceId));
  const check = (route: T.OperationInstructions): void => {
    requireContract(route.partyIds.every((partyId): boolean => partyIds.has(partyId)), "Instructions refer to parties outside this case");
    requireContract(route.evidenceIds.every((evidenceId): boolean => evidenceIds.has(evidenceId)), "Instructions refer to missing evidence");
  };
  check(state.statementInstructions);
  check(state.refundInstructions);
  state.requests.forEach((record): void => { if (record.instructions !== null) check(record.instructions); });
  state.approvals.forEach((record): void => {
    requireContract(partyIds.has(record.actorPartyId), "Approval actor party is outside this case");
  });
  state.statements.forEach((record): void => {
    requireContract(record.content.parties.every((party): boolean => partyIds.has(party.partyId)), "Statement party is outside this case");
  });
}

export function parseLifecycleCommand(kind: string, payloadJson: string): T.LifecycleCommand {
  member(kind, LIFECYCLE_COMMAND_KINDS, "command kind");
  const raw = readJson(payloadJson);
  switch (kind) {
    case "INIT_WORKFLOW": object(raw, [], kind); return { kind, payload: {} };
    case "ACCEPT_SCOPE_FACTS": {
      const v = object(raw, ["jurisdiction", "tenancyRegime", "tenancyEndsInFull", "cashSecurityDeposit", "evidenceIds", "reason"], kind);
      return { kind, payload: { jurisdiction: text(v.jurisdiction, "jurisdiction", 200), tenancyRegime: text(v.tenancyRegime, "tenancyRegime", 200),
        tenancyEndsInFull: nullable(v.tenancyEndsInFull, bool, "tenancyEndsInFull"),
        cashSecurityDeposit: nullable(v.cashSecurityDeposit, bool, "cashSecurityDeposit"),
        evidenceIds: ids(v.evidenceIds, "evidenceIds"), reason: text(v.reason, "reason") } };
    }
    case "SET_INTERIM_QUALIFICATION": {
      const v = object(raw, ["state", "evidenceIds", "reason"], kind);
      return { kind, payload: { state: member(v.state, VOCABULARY.factState, "state"),
        evidenceIds: ids(v.evidenceIds, "evidenceIds"), reason: text(v.reason, "reason") } };
    }
    case "UPSERT_RECIPIENT_PARTY": {
      const v = object(raw, ["party"], kind);
      const party = from_wire("CaseParty", v.party);
      id(party.partyId, "party.partyId");
      text(party.displayLabel, "party.displayLabel");
      unique(party.roles, "party.roles");
      ids(party.evidenceIds, "party.evidenceIds");
      // This narrow endpoint cannot create/update operators, principals, or grants.
      requireContract(party.principalId === null && party.roles.length > 0
        && party.roles.every((role): boolean => role === "RESIDENT" || role === "SIGNATORY"),
      "Recipient upsert accepts only resident/signatory parties without a principal");
      return { kind, payload: { party } };
    }
    case "SET_STATEMENT_INSTRUCTIONS": return { kind, payload: instructions(raw, kind, false) };
    case "SET_REFUND_INSTRUCTIONS": return { kind, payload: instructions(raw, kind, false) };
    case "PREPARE_STATEMENT": {
      const v = object(raw, ["kind", "supersedesId", "reason"], kind);
      return { kind, payload: { kind: member(v.kind, STATEMENT_KINDS, "statement kind"),
        supersedesId: nullable(v.supersedesId, id, "supersedesId"), reason: text(v.reason, "reason") } };
    }
    case "DECIDE_APPROVAL": {
      const v = object(raw, ["intent", "decision"], kind);
      return { kind, payload: { intent: intentSpec(v.intent, "intent"), decision: member(v.decision, ["APPROVED", "REJECTED"], "decision") } };
    }
    case "REVOKE_APPROVAL": {
      const v = object(raw, ["approvalId", "reason"], kind);
      return { kind, payload: { approvalId: id(v.approvalId, "approvalId"), reason: text(v.reason, "reason") } };
    }
    case "REQUEST_OPERATION": {
      const v = object(raw, ["approvalId"], kind);
      return { kind, payload: { approvalId: id(v.approvalId, "approvalId") } };
    }
    case "CLAIM_REQUEST": {
      const v = object(raw, ["requestId"], kind);
      return { kind, payload: { requestId: id(v.requestId, "requestId") } };
    }
    case "RECORD_OUTCOME_UNKNOWN": {
      const v = object(raw, ["requestId", "attemptId", "reason"], kind);
      return { kind, payload: { requestId: id(v.requestId, "requestId"), attemptId: id(v.attemptId, "attemptId"), reason: text(v.reason, "reason") } };
    }
    case "GENERATE_SIMULATED_RESULT": {
      const v = object(raw, ["requestId", "attemptId", "sourceEventId", "outcome", "amountCents", "occurredAt"], kind);
      return { kind, payload: { requestId: id(v.requestId, "requestId"), attemptId: id(v.attemptId, "attemptId"),
        sourceEventId: id(v.sourceEventId, "sourceEventId"), outcome: member(v.outcome, ["SUCCEEDED", "FAILED", "RETURNED"], "outcome"),
        amountCents: nullable(v.amountCents, positive, "amountCents"), occurredAt: nullable(v.occurredAt, parseWorkflowTimestamp, "occurredAt") } };
    }
    case "INGEST_RESULT": {
      const v = object(raw, ["sourceEventId"], kind);
      return { kind, payload: { sourceEventId: id(v.sourceEventId, "sourceEventId") } };
    }
    case "CANCEL_UNATTEMPTED_REQUEST": {
      const v = object(raw, ["requestId", "reason"], kind);
      return { kind, payload: { requestId: id(v.requestId, "requestId"), reason: text(v.reason, "reason") } };
    }
    default: throw new ContractError("Unsupported lifecycle command");
  }
}

function currentRequest(value: unknown, path: string): T.CurrentRequest {
  const v = object(value, ["requestId", "kind", "state", "amountCents", "reservedAmountCents", "attemptId",
    "lastEventId", "canonicalTransactionId", "reconciliationRequired", "reason"], path);
  const result: T.CurrentRequest = {
    requestId: id(v.requestId, `${path}.requestId`), kind: member(v.kind, OPERATION_KINDS, `${path}.kind`),
    state: member(v.state, REQUEST_STATES, `${path}.state`), amountCents: nullable(v.amountCents, positive, `${path}.amountCents`),
    reservedAmountCents: cents(v.reservedAmountCents, `${path}.reservedAmountCents`),
    attemptId: nullable(v.attemptId, id, `${path}.attemptId`), lastEventId: nullable(v.lastEventId, id, `${path}.lastEventId`),
    canonicalTransactionId: nullable(v.canonicalTransactionId, id, `${path}.canonicalTransactionId`),
    reconciliationRequired: bool(v.reconciliationRequired, `${path}.reconciliationRequired`), reason: text(v.reason, `${path}.reason`),
  };
  requireContract((result.kind === "STATEMENT_DISPATCH") === (result.amountCents === null), `${path}: invalid amount shape`);
  requireContract(result.reservedAmountCents <= (result.amountCents ?? 0), `${path}: reservation exceeds instruction amount`);
  return result;
}
function actionDetails(value: unknown, path: string): T.WorkflowActionDetails {
  const v = object(value, ["operationKind", "intent", "approvalDetails", "requestDetails", "statementDetails"], path);
  const result: T.WorkflowActionDetails = {
    operationKind: member(v.operationKind, OPERATION_KINDS, `${path}.operationKind`), intent: nullable(v.intent, intent, `${path}.intent`),
    approvalDetails: array(v.approvalDetails, (entry, p): T.ApprovalValidity => {
      const record = object(entry, ["approvalId", "valid", "reason"], p);
      return { approvalId: id(record.approvalId, `${p}.approvalId`), valid: bool(record.valid, `${p}.valid`), reason: text(record.reason, `${p}.reason`) };
    }, `${path}.approvalDetails`),
    requestDetails: array(v.requestDetails, currentRequest, `${path}.requestDetails`),
    statementDetails: array(v.statementDetails, (entry, p): T.StatementStatus => {
      const record = object(entry, ["statementId", "isCurrent", "dispatchRequestIds", "issued"], p);
      return { statementId: id(record.statementId, `${p}.statementId`), isCurrent: bool(record.isCurrent, `${p}.isCurrent`),
        dispatchRequestIds: ids(record.dispatchRequestIds, `${p}.dispatchRequestIds`), issued: bool(record.issued, `${p}.issued`) };
    }, `${path}.statementDetails`),
  };
  requireContract(result.intent === null || result.intent.kind === result.operationKind, `${path}: action/intent kind mismatch`);
  unique(result.approvalDetails.map((entry): string => entry.approvalId), `${path}.approvalDetails`);
  unique(result.requestDetails.map((entry): string => entry.requestId), `${path}.requestDetails`);
  unique(result.statementDetails.map((entry): string => entry.statementId), `${path}.statementDetails`);
  return result;
}

/** Keep all six native result sections and validate their unchanged core fields. */
export function parseWorkflowReview(sourceJson: string): T.WorkflowReviewV2 {
  const v = object(readJson(sourceJson), ["metadata", "result"], "WorkflowReviewV2");
  requireContract(is_plain_object(v.metadata), "metadata: expected object");
  const { workflowSchemaVersion, workflowStateHash, authorityEvaluatedAt, ...baseMetadata } = v.metadata;
  const r = object(v.result, ["scopeRequirements", "itemDecisions", "account", "missingInputs", "actions", "outcomes"], "result");
  requireContract(is_plain_object(r.account) && is_plain_object(r.outcomes), "Expected account and outcomes objects");
  const { financialCommitments, newlyRequestableRefundCents, ...baseAccount } = r.account;
  const { simulatedDepositWorkflowComplete, simulatedOverallWorkflowComplete, completionMode, legalPerformanceConfirmed,
    ...baseOutcomes } = r.outcomes;
  const actions = array(r.actions, (entry, path): T.WorkflowAction => {
    requireContract(is_plain_object(entry) && Object.hasOwn(entry, "workflow"), `${path}: missing workflow extension`);
    const { workflow, ...baseAction } = entry;
    return { ...from_wire("AvailableAction", baseAction), workflow: nullable(workflow, actionDetails, `${path}.workflow`) };
  }, "actions");
  const base = from_wire("ReviewEnvelope", { metadata: baseMetadata, result: {
    scopeRequirements: r.scopeRequirements, itemDecisions: r.itemDecisions, account: baseAccount,
    missingInputs: r.missingInputs, actions: actions.map(({ workflow: _workflow, ...action }): typeof action => action), outcomes: baseOutcomes,
  } });
  const commitments = array(financialCommitments, (entry, path): T.FinancialCommitment => {
    const record = object(entry, ["kind", "reservedCents", "requestIds"], path);
    return { kind: member(record.kind, ["REFUND", "CHARGE_POSTING", "DEPOSIT_APPLICATION", "CHARGE_POSTING_REVERSAL", "DEPOSIT_APPLICATION_REVERSAL"], `${path}.kind`),
      reservedCents: cents(record.reservedCents, `${path}.reservedCents`), requestIds: ids(record.requestIds, `${path}.requestIds`) };
  }, "financialCommitments");
  unique(commitments.map((entry): string => entry.kind), "financialCommitments");
  const newlyRequestable = nullable(newlyRequestableRefundCents, cents, "newlyRequestableRefundCents");
  if (base.result.account.finalRefundCents === null || base.result.account.reconciliationState !== "RECONCILED") {
    requireContract(newlyRequestable === null, "Unverified account requires null newly requestable refund");
  } else if (newlyRequestable !== null) {
    requireContract(newlyRequestable <= base.result.account.finalRefundCents, "Newly requestable refund exceeds unpaid refund");
  }
  requireContract(base.result.outcomes.depositComplete === false && base.result.outcomes.overallCaseComplete === false
    && legalPerformanceConfirmed === false, "Simulation cannot claim legal/core completion");
  const result: T.WorkflowReviewV2 = {
    metadata: { ...base.metadata,
      workflowSchemaVersion: member(workflowSchemaVersion, [WORKFLOW_SCHEMA_VERSION], "workflowSchemaVersion"),
      workflowStateHash: hash(workflowStateHash, "workflowStateHash"), authorityEvaluatedAt: parseWorkflowTimestamp(authorityEvaluatedAt, "authorityEvaluatedAt") },
    result: { ...base.result, account: { ...base.result.account, financialCommitments: commitments, newlyRequestableRefundCents: newlyRequestable },
      actions, outcomes: { ...base.result.outcomes, depositComplete: false, overallCaseComplete: false,
        simulatedDepositWorkflowComplete: bool(simulatedDepositWorkflowComplete, "simulatedDepositWorkflowComplete"),
        simulatedOverallWorkflowComplete: bool(simulatedOverallWorkflowComplete, "simulatedOverallWorkflowComplete"),
        completionMode: member(completionMode, ["SIMULATED"], "completionMode"), legalPerformanceConfirmed: false } },
  };
  requireContract(!result.result.outcomes.simulatedOverallWorkflowComplete || result.result.outcomes.simulatedDepositWorkflowComplete,
    "Overall workflow completion requires deposit workflow completion");
  boundedJson(canonical_json(result));
  return result;
}

export function serializeWorkflowState(state: T.WorkflowStateV2): string {
  return boundedJson(canonical_json(parseWorkflowState(boundedJson(canonical_json(state)))));
}
export function hashWorkflowState(state: T.WorkflowStateV2): string {
  return fingerprint(parseWorkflowState(boundedJson(canonical_json(state))));
}
export function serializeWorkflowReview(review: T.WorkflowReviewV2): string {
  return boundedJson(canonical_json(parseWorkflowReview(boundedJson(canonical_json(review)))));
}
export function hashWorkflowReview(review: T.WorkflowReviewV2): string {
  return fingerprint(parseWorkflowReview(boundedJson(canonical_json(review))));
}

/** Absent root field is the known Phase C version. Null, numeric Longs and unknown versions fail. */
export function parseWorkflowVersion(value: unknown): 0 | 2 {
  if (value === undefined || value === "0") return 0;
  if (value === "2") return 2;
  throw new ContractError("Unknown or corrupt stored workflow version");
}

/**
 * Decode all-or-none extra snapshot fields and bind hashes, business clock, and
 * actual authority clock. Parent recomputation MUST also use snapshotCreatedAt.
 * No missing v2 field silently falls back to C; no v0 sidecar is silently ignored.
 */
export function parseWorkflowSnapshot(
  rootVersion: unknown, extras: T.WorkflowSnapshotExtras, snapshotCreatedAt: string,
): T.ParsedWorkflowSnapshot | null {
  const version = parseWorkflowVersion(rootVersion);
  const keys = ["workflowStateJson", "workflowStateHash", "workflowReviewJson", "workflowReviewHash"];
  requireContract(is_plain_object(extras) && Object.keys(extras).every((key): boolean => keys.includes(key)),
    "Unknown workflow snapshot fields");
  if (version === 0) {
    requireContract(Object.values(extras).every((entry): boolean => entry === undefined), "V0 cannot contain v2 sidecar fields");
    return null;
  }
  const state = parseWorkflowState(boundedJson(extras.workflowStateJson));
  const review = parseWorkflowReview(boundedJson(extras.workflowReviewJson));
  const stateHash = hash(extras.workflowStateHash, "workflowStateHash");
  const reviewHash = hash(extras.workflowReviewHash, "workflowReviewHash");
  requireContract(fingerprint(state) === stateHash && fingerprint(review) === reviewHash
    && review.metadata.workflowStateHash === stateHash, "Workflow snapshot hash mismatch");
  const createdAt = parseWorkflowTimestamp(snapshotCreatedAt, "snapshotCreatedAt");
  requireContract(compare_timestamps(review.metadata.authorityEvaluatedAt, createdAt) === 0,
    "Authority evaluation must be bound to the recorded snapshot createdAt");
  requireContract(compare_timestamps(review.metadata.reviewClock, state.businessClock) === 0, "Workflow review business clock mismatch");
  noLater(state.initializedAt, createdAt, "workflow initialization");
  state.statements.forEach((record): void => noLater(record.createdAt, createdAt, "statement creation"));
  state.approvals.forEach((record): void => noLater(record.decidedAt, createdAt, "approval decision"));
  state.requests.forEach((record): void => noLater(record.createdAt, createdAt, "request creation"));
  state.events.forEach((record): void => noLater(record.recordedAt, createdAt, "event recording"));
  return { state, review };
}

/** Returns normalized next clock; the adapter supplies clocks, this module never reads one. */
export function assertMonotonicBusinessClock(previous: string, next: string): string {
  const oldClock = parseWorkflowTimestamp(previous);
  const newClock = parseWorkflowTimestamp(next);
  noLater(oldClock, newClock, "business clock");
  return newClock;
}
export function parsePureContext(value: unknown): T.PureContext {
  const v = object(value, ["actorId", "serverNow", "isAdministrator", "commandId", "basisReviewId"], "PureContext");
  return { actorId: id(v.actorId, "actorId"), serverNow: parseWorkflowTimestamp(v.serverNow, "serverNow"),
    isAdministrator: bool(v.isAdministrator, "isAdministrator"), commandId: id(v.commandId, "commandId"), basisReviewId: id(v.basisReviewId, "basisReviewId") };
}
