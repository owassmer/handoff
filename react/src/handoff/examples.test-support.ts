import { webcrypto } from "node:crypto";
import { afterEach, beforeEach, vi } from "vitest";
import type {
  Change,
  HandoffChange,
  HandoffGateway,
  HandoffList,
  HandoffWorkspace,
} from "./contracts";
import { changePayloadHash } from "./state";

beforeEach(() => vi.stubGlobal("crypto", webcrypto));
afterEach(() => vi.unstubAllGlobals());

export function absentChange(commandId: string): HandoffChange {
  return {
    version: "2",
    commandId,
    status: "Not found",
    subjectId: null,
    kind: null,
    payloadHash: null,
    resultRevision: null,
    at: null,
  };
}
export async function savedChange(change: Change, data: HandoffWorkspace): Promise<HandoffChange> {
  return {
    version: "2",
    commandId: change.commandId,
    status: "Saved",
    subjectId: change.kind === "message" ? change.handoffId : change.workPlanId,
    kind:
      change.kind === "budget"
        ? "Work budget changed"
        : change.kind === "plan"
          ? "Work plan changed"
          : change.kind === "message"
            ? "Message sent"
            : "Work plan accepted",
    payloadHash: await changePayloadHash(change),
    resultRevision:
      change.kind === "budget" || change.kind === "plan"
        ? data.workPlan!.revision
        : data.handoff.revision,
    at: "2026-09-22T10:20:00Z",
  };
}

export function exampleWorkspace(): HandoffWorkspace {
  return {
    version: "2",
    workspace: { id: "office", name: "Northside Property Team", mode: "Demo" },
    handoff: {
      id: "garden-home",
      title: "Prepare the garden home for its next residents",
      goal: "Finish the agreed repairs and settle the tenancy fairly.",
      businessDate: "2026-09-22",
      physicalProgress: "Ready for your decision",
      financialProgress: "Final settlement not yet prepared",
      nextStep: "Review the proposed work and budget",
      revision: "4",
      operativeDecisionId: null,
    },
    property: {
      id: "property-garden",
      name: "Garden home",
      address: "18 Garden Street",
      description: "A two-bedroom home with a private garden.",
    },
    tenancy: {
      id: "tenancy-garden",
      title: "Jordan Ellis’s tenancy",
      startDate: "2025-01-01",
      endDate: "2026-09-20",
      endingKind: "Tenancy ending",
    },
    parties: [
      { id: "resident", name: "Jordan Ellis", kind: "Person", description: "Outgoing resident" },
      {
        id: "provider",
        name: "Oak Repairs",
        kind: "Organization",
        description: "Repairs and finishing",
      },
    ],
    agreements: [
      {
        id: "lease",
        title: "Return condition",
        termsText:
          "The home must be returned in the condition agreed in the tenancy, allowing for normal wear.",
        sourceDocumentId: "lease-text",
      },
    ],
    obligations: [
      {
        id: "repair",
        title: "Complete the agreed repairs",
        description: "Repair and inspect before the next handoff.",
        status: "Work to arrange",
      },
    ],
    documents: [
      {
        id: "survey",
        kind: "Inspection",
        sourceVersion: "1",
        mimeType: "application/pdf",
        availableFrom: null,
        title: "Condition survey",
        text: "The kitchen wall needs a small plaster repair. The door handle is loose. All other rooms were inspected and are in good order.\nThe survey recommends repairing only the listed items.",
        mediaSetRid: null,
        mediaItemRid: null,
        pageStart: 1,
        pageEnd: 2,
      },
      {
        id: "quote",
        kind: "Quote",
        sourceVersion: "1",
        mimeType: "application/pdf",
        availableFrom: null,
        title: "Oak Repairs quote",
        text: "Repair the kitchen wall and refit the door handle. Total estimated cost: £875.00. Materials and cleanup included.",
        mediaSetRid: "media-set",
        mediaItemRid: "media-item",
        pageStart: 1,
        pageEnd: 1,
      },
      {
        id: "lease-text",
        kind: "Agreement",
        sourceVersion: "1",
        mimeType: "application/pdf",
        availableFrom: null,
        title: "Tenancy agreement",
        text: "Original agreement text. Normal wear is allowed; agreed repairs must be documented.",
        mediaSetRid: null,
        mediaItemRid: null,
        pageStart: null,
        pageEnd: null,
      },
    ],
    workPlan: {
      id: "work-garden",
      revision: "2",
      title: "Repair the kitchen wall and door handle",
      status: "Ready for your decision",
      summary: "A focused repair visit will prepare the home without replacing sound fittings.",
      desiredOutcome: "A clean, repaired home ready for the next residents.",
      scope: ["Repair and finish the kitchen wall", "Refit and test the loose door handle"],
      estimatedCostCents: "87500",
      budgetCents: "100000",
      currency: "GBP",
      fixedRequirements: ["Retain the existing fittings where they are sound"],
      rationale:
        "The survey and quote agree on a limited repair, avoiding unnecessary replacement.",
      sourceDocumentIds: ["survey", "quote"],
      providerPartyId: "provider",
      acceptedDecisionId: null,
      selections: [],
      fixedProviderPartyId: null,
    },
    decisions: [],
    messages: [],
    activity: [
      {
        id: "prepared",
        title: "Work plan prepared",
        detail: "The survey and provider’s quote have been reviewed.",
        at: "2026-09-22T09:00:00Z",
      },
    ],
    agent: {
      status: "Waiting for your decision",
      nextStep: "Once you accept, arrange a visit with Oak Repairs.",
      updatedAt: "2026-09-22T09:00:00Z",
      nextWakeAt: null,
    },
    jobs: [],
    quotes: [],
    inspections: [],
    invoices: [],
    funding: [],
    payments: [],
    permissions: { canWork: true, canDecide: true, canConfigure: false },
  };
}
export function listFor(data: HandoffWorkspace): HandoffList {
  return {
    version: "2",
    workspace: data.workspace,
    handoffs: [{ ...data.handoff, propertyName: data.property.name }],
  };
}
export function acceptWork(data: HandoffWorkspace): HandoffWorkspace {
  const next = structuredClone(data);
  const plan = next.workPlan!;
  plan.acceptedDecisionId = "decision-saved";
  plan.status = "Accepted";
  next.decisions.push({
    id: "decision-saved",
    title: "Repair work approved",
    workPlanId: plan.id,
    revision: plan.revision,
    by: "Morgan Lee",
    at: "2026-09-22T10:20:00Z",
    budgetCents: plan.budgetCents,
    currency: plan.currency,
    content: structuredClone(plan),
  });
  next.handoff.operativeDecisionId = "decision-saved";
  next.handoff.physicalProgress = "Arranging work";
  next.handoff.revision = (BigInt(next.handoff.revision) + 1n).toString();
  next.agent = {
    status: "Arranging work",
    nextStep: "Agree a visit with Oak Repairs.",
    updatedAt: "2026-09-22T10:20:00Z",
    nextWakeAt: null,
  };
  return next;
}
export function exampleGateway(initial = exampleWorkspace()) {
  const state = { data: initial, receipts: new Map<string, HandoffChange>() };
  const recordChange = async (change: Change): Promise<void> => {
    state.receipts.set(change.commandId, await savedChange(change, state.data));
  };
  const gateway: HandoffGateway = {
    list: vi.fn(async () => structuredClone(listFor(state.data))),
    workspace: vi.fn(async () => structuredClone(state.data)),
    receipt: vi.fn(
      async (_handoffId: string, commandId: string) =>
        state.receipts.get(commandId) ?? absentChange(commandId),
    ),
    apply: vi.fn(async (_change: Change) => "saved" as const),
    document: vi.fn(async () => new Blob(["%PDF-1.7"], { type: "application/pdf" })),
  };
  return { gateway, state, recordChange };
}
export function memoryStorage(): Storage {
  const values = new Map<string, string>();
  return {
    get length() {
      return values.size;
    },
    clear: () => values.clear(),
    getItem: (key) => values.get(key) ?? null,
    key: (index) => [...values.keys()][index] ?? null,
    removeItem: (key) => {
      values.delete(key);
    },
    setItem: (key, value) => {
      values.set(key, value);
    },
  };
}
export function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((yes, no) => {
    resolve = yes;
    reject = no;
  });
  return { promise, resolve, reject };
}
