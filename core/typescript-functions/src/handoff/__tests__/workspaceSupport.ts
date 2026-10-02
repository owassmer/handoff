import {
  HandoffWorkspace, HandoffProperty, HandoffParty, HandoffTenancy, HandoffAgreement,
  HandoffObligation, HandoffCase, HandoffDocument, HandoffWorkPlan, HandoffDecision,
  HandoffMessage, HandoffAgentWork, HandoffActivity, HandoffJob, HandoffInspection, HandoffQuote, HandoffInvoice, HandoffFunding, HandoffPayment,
} from "@ontology/sdk";
import type { Client, CompileTimeMetadata, ObjectTypeDefinition, Osdk } from "@osdk/client";
import { createMockOsdkObject } from "@osdk/unit-testing";
import type { HandoffEdit } from "../records.js";
import type { MoveOutNotice } from "../notice.js";
import type { WorkModel, WorkPlanDraft } from "../reasoner.js";
import type { ChatCompletion, ChatCompletionCreateParamsNonStreaming } from "openai/resources/chat/completions";
import { reference } from "../values.js";

const TYPES = [HandoffWorkspace, HandoffProperty, HandoffParty, HandoffTenancy, HandoffAgreement,
  HandoffObligation, HandoffCase, HandoffDocument, HandoffWorkPlan, HandoffDecision,
  HandoffMessage, HandoffAgentWork, HandoffActivity, HandoffJob, HandoffInspection, HandoffQuote, HandoffInvoice, HandoffFunding, HandoffPayment];
export const PERSON = "signed-in-person";
export const MODEL = "selected-work-model";
export const WORKSPACE = reference("workspace", PERSON, "open-workspace");
export const sourceId = (kind: string, id: string): string => reference(kind, WORKSPACE, "lettings", id);
export const HANDOFF = sourceId("handoff", "notice-1");

type Filter = Record<string, { $eq?: unknown; $in?: unknown[] }>;
type Props<T extends ObjectTypeDefinition> = Partial<CompileTimeMetadata<T>["props"]>;

/** A small test store returning generated SDK instances; it is not an Action conflict simulator. */
export class WorkspaceStore {
  private records = new Map<string, Map<string, Osdk.Instance<ObjectTypeDefinition>>>();
  onRead?: (type: ObjectTypeDefinition) => void;
  readonly calls: string[] = [];
  readonly client: Client = ((type: ObjectTypeDefinition): object => this.query(type, {})) as unknown as Client;

  private query(type: ObjectTypeDefinition, filter: Filter): object {
    return {
      where: (next: Filter): object => this.query(type, { ...filter, ...next }),
      asyncIter: () => {
        const store = this;
        return (async function* () {
          store.calls.push(type.apiName);
          store.onRead?.(type);
          const matches = store.all(type).filter((record) => Object.entries(filter).every(([key, test]) =>
            (test.$eq === undefined || Reflect.get(record, key) === test.$eq)
            && (test.$in === undefined || test.$in.includes(Reflect.get(record, key)))));
          for (const record of matches) yield record;
        })();
      },
      fetchPage: async (options: { $pageSize?: number; $orderBy?: Record<string, string> }): Promise<object> => {
        this.calls.push(type.apiName);
        this.onRead?.(type);
        let matches = this.all(type).filter((record) => Object.entries(filter).every(([key, test]) =>
          (test.$eq === undefined || Reflect.get(record, key) === test.$eq)
          && (test.$in === undefined || test.$in.includes(Reflect.get(record, key)))));
        const order = Object.entries(options.$orderBy ?? {})[0];
        if (order) matches = matches.sort((a, b) => String(Reflect.get(a, order[0])).localeCompare(String(Reflect.get(b, order[0]))) * (order[1] === "desc" ? -1 : 1));
        const size = options.$pageSize ?? 100;
        return { data: matches.slice(0, size), ...(matches.length > size ? { nextPageToken: "more" } : {}) };
      },
    };
  }

  put<T extends ObjectTypeDefinition>(type: T, props: Props<T>): Osdk.Instance<T> {
    const record = createMockOsdkObject(type, props);
    let group = this.records.get(type.apiName);
    if (!group) { group = new Map(); this.records.set(type.apiName, group); }
    group.set(String(record.$primaryKey), record as Osdk.Instance<ObjectTypeDefinition>);
    return record;
  }
  get<T extends ObjectTypeDefinition>(type: T, id: string): Osdk.Instance<T> {
    const found = this.records.get(type.apiName)?.get(id);
    if (!found) throw new Error(`Missing ${type.apiName}`);
    return found as Osdk.Instance<T>;
  }
  all<T extends ObjectTypeDefinition>(type: T): Osdk.Instance<T>[] {
    return [...(this.records.get(type.apiName)?.values() ?? [])] as Osdk.Instance<T>[];
  }
  change<T extends ObjectTypeDefinition>(type: T, id: string, props: Props<T>): void {
    const before = this.get(type, id);
    const businessProps = Object.fromEntries(Object.entries(before).filter(([key]) => !key.startsWith("$")));
    this.put(type, { ...businessProps, ...props } as Props<T>);
  }
  apply(edits: HandoffEdit[]): void {
    edits.forEach((edit) => {
      if (edit.type === "createObject") {
        const pk = String(Reflect.get(edit.properties, edit.obj.primaryKeyApiName!));
        if (this.records.get(edit.obj.apiName)?.has(pk)) throw new Error("Duplicate object create");
        this.put(edit.obj, edit.properties as Props<typeof edit.obj>);
      } else if (edit.type === "updateObject") {
        const type = TYPES.find((entry) => entry.apiName === edit.obj.$apiName);
        if (!type) throw new Error("Unknown edited type");
        this.change(type, String(edit.obj.$primaryKey), edit.properties as Props<typeof type>);
      } else throw new Error("Unexpected edit operation");
    });
  }
}

export function notice(): MoveOutNotice {
  return {
    sourceSystem: "lettings", sourceRecordId: "notice-1", title: "Return the garden house", goal: "Prepare a clean home with a secure entrance.", businessDate: "2026-09-22",
    property: { sourceId: "home-1", name: "Garden house", address: "17 Meadow Street", description: "Two-bedroom home with a timber front door." },
    parties: [
      { sourceId: "owner", name: "Morgan", kind: "Person", description: "Owns the house." },
      { sourceId: "tenant", name: "Casey", kind: "Person", description: "Departing tenant." },
      { sourceId: "provider", name: "House Care", kind: "Organization", description: "Cleaning and small repairs.", email: "work@example.test" },
    ],
    tenancy: { sourceId: "tenancy-1", title: "Garden house tenancy", landlordPartySourceId: "owner", tenantPartySourceIds: ["tenant"], startDate: "2025-09-01", endDate: "2026-09-21", noticeDate: "2026-08-20" },
    documents: [
      { sourceId: "lease", title: "Tenancy agreement", text: "Return the home clean with existing serviceable fittings retained. Owner approval is required before arranging work.", kind: "Agreement", sourceKind: "Source" },
      { sourceId: "inspection", title: "Departure inspection", text: "The kitchen needs cleaning and the entrance latch needs adjustment. Replacement is unnecessary.", kind: "Inspection", sourceKind: "Source" },
      { sourceId: "quote", title: "Cleaning and repair quote", text: "House Care offers latch adjustment for 12500 cents and kitchen cleaning for 8000 cents, tax included.", kind: "Quote", partySourceId: "provider", sourceKind: "Source" },
    ],
    agreements: [{ sourceId: "terms", title: "Return of the home", kind: "Tenancy", termsText: "Retain serviceable fittings and ask the owner to approve the work.", sourceDocumentSourceId: "lease", effectiveFrom: "2025-09-01" }],
    obligations: [{ sourceId: "retain", title: "Retain serviceable fittings", description: "Keep serviceable fittings.", responsiblePartySourceIds: ["owner"], beneficiaryPartySourceIds: ["tenant"], basisAgreementSourceId: "terms", basisDocumentSourceId: "lease", status: "Open" }],
  };
}

export function proposedWork(): WorkPlanDraft {
  return { title: "Clean the kitchen and adjust the entrance latch", summary: "House Care can prepare the home with targeted cleaning and adjustment.",
    desiredOutcome: "A clean home with a secure entrance.", scope: ["Clean the kitchen.", "Adjust the entrance latch."],
    estimatedCostCents: "20500", budgetCents: "25000", currency: "USD", fixedRequirements: ["Keep serviceable fittings.", "Obtain owner approval before arranging work."],
    rationale: "The inspection supports adjustment rather than replacement, and the quote covers both tasks including tax.",
    sourceDocumentIds: [sourceId("document", "lease"), sourceId("document", "inspection"), sourceId("document", "quote")],
    providerPartyId: sourceId("party", "provider") };
}

export function seedQuotedWork(store: WorkspaceStore): void {
  store.put(HandoffQuote, { quoteId: sourceId("quote", "quote"), workspaceId: WORKSPACE, readerIds: [PERSON], handoffId: HANDOFF,
    propertyId: sourceId("property", "home-1"), title: "Cleaning and repairs", providerPartyId: sourceId("party", "provider"), kind: "Repair", currency: "USD",
    linesJson: JSON.stringify([{ lineId: "clean", description: "Kitchen clean", amountCents: "8000" }, { lineId: "latch", description: "Adjust latch", amountCents: "12500" }]),
    totalCents: "20500", depositCents: "0", paymentTerms: "On completion", requirements: proposedWork().fixedRequirements,
    availableFrom: "2026-09-01T00:00:00.000Z", validUntil: "2027-01-01T00:00:00.000Z", durationMinutes: 60, responseMinutes: 1,
    sourceSystem: "lettings", sourceRecordId: "quote", sourceDocumentId: sourceId("document", "quote"), status: "Offered", recordedAt: "2026-09-22T00:00:00.000Z" });
}
export const selectedWork = (): Array<{ quoteId: string; quoteLineId: string; scope: string; reason: string }> => [
  { quoteId: sourceId("quote", "quote"), quoteLineId: "clean", scope: "Clean the kitchen.", reason: "The kitchen cleaning price covers this scope." },
  { quoteId: sourceId("quote", "quote"), quoteLineId: "latch", scope: "Adjust the entrance latch.", reason: "The latch adjustment price covers this scope." },
];
export function workModel(onFinal?: () => void): WorkModel & { requests: ChatCompletionCreateParamsNonStreaming[] } {
  const requests: ChatCompletionCreateParamsNonStreaming[] = [];
  const reply = (message: ChatCompletion["choices"][number]["message"], finish_reason: "stop" | "tool_calls"): Pick<ChatCompletion, "choices"> => ({ choices: [{ index: 0, logprobs: null, finish_reason, message }] });
  return { model: MODEL, requests, complete: async (request): Promise<Pick<ChatCompletion, "choices">> => {
    requests.push(request);
    if (requests.length < 3) {
      const name = requests.length === 1 ? "readDocuments" : "quoteCosts";
      const args = requests.length === 1 ? { ids: proposedWork().sourceDocumentIds } : { selections: selectedWork() };
      return reply({ role: "assistant", refusal: null, content: null,
        tool_calls: [{ id: `call-${requests.length}`, type: "function", function: { name, arguments: JSON.stringify(args) } }] }, "tool_calls");
    }
    onFinal?.();
    const { scope: _scope, ...proposal } = proposedWork();
    // A model keeps exactly the supplied handoff requirements; obligations and agreements stay evidence.
    const supplied = JSON.parse(String(request.messages.find((message) => message.role === "user")?.content)) as { fixedRequirements: string[] };
    return reply({ role: "assistant", refusal: null, content: JSON.stringify({ summary: "Review the proposed cleaning and adjustment.", proposal: { ...proposal, fixedRequirements: supplied.fixedRequirements, selections: selectedWork(), fixedProviderPartyId: null }, requests: [], propertyReady: false }) }, "stop");
  } };
}
