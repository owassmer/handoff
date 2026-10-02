import {
  type Change,
  type HandoffChange,
  HandoffError,
  type HandoffGateway,
  type HandoffList,
  type HandoffWorkspace,
  type WorkPlan,
  type WorkPlanChange,
  receiptKinds,
} from "./contracts";
import { pollDelay } from "./model";

export interface ReadState<T> {
  data?: T;
  loading: boolean;
  failed: boolean;
  failureKind?: HandoffError["kind"];
}
/** Shared, deduplicated reads. A subscription owns polling; React effects do not fetch data. */
export class ReadResource<T> {
  private listeners = new Set<() => void>();
  private state: ReadState<T> = { loading: true, failed: false };
  private request?: Promise<void>;
  private timer?: ReturnType<typeof setTimeout>;
  private generation = 0;
  private readonly visibility = () => {
    if (typeof document === "undefined" || document.visibilityState !== "hidden") {
      void this.refresh().then(() => this.schedule());
    }
  };
  /**
   * @param interval Milliseconds between reads, or a function of the last data (0 = no polling).
   *   Reads pause while the tab is hidden and resume with an immediate read when it returns.
   */
  constructor(
    private readonly read: () => Promise<T>,
    private readonly receive: (value: T) => void = () => {},
    private readonly interval: number | ((data?: T) => number) = 7000,
  ) {}
  private delay(): number {
    return typeof this.interval === "function" ? this.interval(this.state.data) : this.interval;
  }
  private schedule() {
    clearTimeout(this.timer);
    const delay = this.delay();
    if (!this.listeners.size || delay <= 0) {
      return;
    }
    this.timer = setTimeout(() => {
      if (typeof document !== "undefined" && document.visibilityState === "hidden") {
        return;
      }
      void this.refresh().then(() => this.schedule());
    }, delay);
  }
  getSnapshot = () => this.state;
  private emit() {
    this.listeners.forEach((fn) => fn());
  }
  subscribe = (fn: () => void) => {
    this.listeners.add(fn);
    if (this.listeners.size === 1) {
      void this.refresh().then(() => this.schedule());
      if (this.delay() > 0 && typeof document !== "undefined") {
        document.addEventListener("visibilitychange", this.visibility);
      }
    }
    return () => {
      this.listeners.delete(fn);
      if (!this.listeners.size) {
        clearTimeout(this.timer);
        if (typeof document !== "undefined") {
          document.removeEventListener("visibilitychange", this.visibility);
        }
      }
    };
  };
  refresh = (): Promise<void> => {
    if (this.request) {
      return this.request;
    }
    const generation = this.generation;
    this.state = { ...this.state, loading: true };
    this.emit();
    this.request = Promise.resolve()
      .then(this.read)
      .then((data) => {
        if (generation !== this.generation) {
          return;
        }
        this.receive(data);
        this.state = { data, loading: false, failed: false };
      })
      .catch((error: unknown) => {
        if (generation !== this.generation) {
          return;
        }
        this.state = {
          ...this.state,
          ...(error instanceof HandoffError && ["access", "permission"].includes(error.kind)
            ? { data: undefined }
            : {}),
          loading: false,
          failed: true,
          failureKind: error instanceof HandoffError ? error.kind : "read",
        };
      })
      .finally(() => {
        if (generation === this.generation) {
          this.request = undefined;
          this.emit();
        }
      });
    return this.request;
  };
  /** Do not let a read started before apply count as its confirming read. */
  fresh = async () => {
    await this.request;
    await this.refresh();
  };
  clear() {
    this.generation++;
    clearTimeout(this.timer);
    this.request = undefined;
    this.state = { loading: false, failed: true };
    this.emit();
  }
}
export interface BudgetDraft {
  value: string;
  revision: string;
  originalBudget: string;
  reviewedPlanId: string;
  changes?: WorkPlanChange;
}
export interface ChangeReference {
  kind: Change["kind"];
  handoffId: string;
  workPlanId: string;
  expectedRevision: string;
  commandId: string;
  payloadHash: string;
}
export interface PendingChange {
  reference: Readonly<ChangeReference>;
  /** The exact retry is available only while this person's page remains open. */
  change?: Change;
  acknowledged: boolean;
  status: "sending" | "checking";
}
interface Journal {
  drafts: Record<string, BudgetDraft>;
  pending: Record<string, PendingChange>;
  unreadable?: boolean;
}
/** The published service's supported work-budget limit, not a default budget. */
export const MAX_WORK_BUDGET_CENTS = 100_000_000n;
const MAX_CHANGES = 32;
const MAX_JOURNAL_BYTES = 64 * 1024;
const UNREADABLE_JOURNAL = JSON.stringify({ version: "2", pending: [], unreadable: true });

export function budgetInput(cents: string): string {
  const n = BigInt(cents);
  return `${n / 100n}.${(n % 100n).toString().padStart(2, "0")}`;
}
export function parseBudget(value: string): string | undefined {
  if (value.length > 24 || !/^\d+(?:\.\d{0,2})?$/.test(value.trim())) {
    return undefined;
  }
  const [whole, fraction = ""] = value.trim().split(".");
  const amount = BigInt(whole) * 100n + BigInt(fraction.padEnd(2, "0"));
  return amount <= 9223372036854775807n ? amount.toString() : undefined;
}
export function acceptedDecision(workspace: HandoffWorkspace) {
  const plan = workspace.workPlan;
  return plan?.acceptedDecisionId
    ? workspace.decisions.find((d) => d.id === plan.acceptedDecisionId && d.workPlanId === plan.id)
    : undefined;
}
/** Matching business values are useful for review, but never prove who saved a change. */
export function matchesChange(workspace: HandoffWorkspace, change: Change): boolean {
  if (change.kind === "message") {
    return false;
  }
  const plan = workspace.workPlan;
  if (!plan || workspace.handoff.id !== change.handoffId || plan.id !== change.workPlanId) {
    return false;
  }
  if (change.kind === "budget") {
    return (
      BigInt(plan.revision) > BigInt(change.expectedRevision) &&
      plan.budgetCents === change.budgetCents
    );
  }
  if (change.kind === "plan") {
    return (
      BigInt(plan.revision) > BigInt(change.expectedRevision) &&
      Object.entries(change.changes).every(
        ([key, value]) => orderedJson(Reflect.get(plan, key)) === orderedJson(value),
      )
    );
  }
  const decision = acceptedDecision(workspace);
  return Boolean(
    decision &&
    decision.budgetCents === change.budgetCents &&
    decision.currency === plan.currency &&
    decision.revision === change.expectedRevision &&
    plan.revision === change.expectedRevision &&
    plan.budgetCents === decision.budgetCents,
  );
}
/** Mirrors backend orderedJson: recursive object ordering, untouched array order. */
export function orderedJson(value: unknown): string {
  function order(v: unknown): unknown {
    if (Array.isArray(v)) {
      return v.map(order);
    }
    if (typeof v === "object" && v !== null) {
      return Object.fromEntries(
        Object.entries(v)
          .filter(([, item]) => item !== undefined)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([key, item]) => [key, order(item)]),
      );
    }
    return v;
  }
  return JSON.stringify(order(value));
}
export async function changePayloadHash(change: Change): Promise<string> {
  const payload =
    change.kind === "message"
      ? {
          handoffId: change.handoffId,
          message: change.message,
          expectedPlanRevision: change.expectedPlanRevision,
        }
      : {
          workPlanId: change.workPlanId,
          expectedRevision: change.expectedRevision,
          ...(change.kind === "budget"
            ? { budgetCents: change.budgetCents }
            : change.kind === "plan"
              ? { changes: change.changes }
              : {}),
        };
  const hash = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(orderedJson(payload)),
  );
  return Array.from(new Uint8Array(hash), (byte) => byte.toString(16).padStart(2, "0")).join("");
}
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
function validReference(value: unknown): value is ChangeReference {
  if (!isRecord(value)) {
    return false;
  }
  const keys = ["kind", "handoffId", "workPlanId", "expectedRevision", "commandId", "payloadHash"];
  return (
    Object.keys(value).length === keys.length &&
    keys.every((key) => Object.prototype.hasOwnProperty.call(value, key)) &&
    ["budget", "accept", "plan", "message"].includes(String(value.kind)) &&
    [value.handoffId, value.workPlanId, value.commandId].every(
      (id) =>
        typeof id === "string" &&
        id.length > 0 &&
        id.length <= 160 &&
        id === id.trim() &&
        !["__proto__", "constructor", "prototype"].includes(id),
    ) &&
    typeof value.expectedRevision === "string" &&
    /^(0|[1-9]\d{0,9})$/.test(value.expectedRevision) &&
    BigInt(value.expectedRevision) <= 1_000_000_000n &&
    typeof value.payloadHash === "string" &&
    /^[a-f0-9]{64}$/.test(value.payloadHash)
  );
}
function loadJournal(storage: Storage | undefined, key: string): Journal {
  try {
    const value = storage?.getItem(key);
    if (value === null || value === undefined) {
      return { drafts: {}, pending: {} };
    }
    if (
      value.length > MAX_JOURNAL_BYTES ||
      new TextEncoder().encode(value).length > MAX_JOURNAL_BYTES
    ) {
      throw new Error();
    }
    const data: unknown = JSON.parse(value);
    if (
      !isRecord(data) ||
      data.version !== "2" ||
      data.unreadable === true ||
      Object.keys(data).some((name) => !["version", "pending"].includes(name)) ||
      !Array.isArray(data.pending) ||
      data.pending.length > MAX_CHANGES
    ) {
      throw new Error();
    }
    const journal: Journal = { drafts: {}, pending: {} };
    const commands = new Set<string>();
    for (const entry of data.pending) {
      if (
        !validReference(entry) ||
        journal.pending[entry.handoffId] ||
        commands.has(entry.commandId)
      ) {
        throw new Error();
      }
      commands.add(entry.commandId);
      journal.pending[entry.handoffId] = {
        reference: Object.freeze(entry),
        acknowledged: false,
        status: "checking",
      };
    }
    return journal;
  } catch {
    // Remove private or malformed legacy values, but retain a lock for uncertain earlier changes.
    try {
      storage?.setItem(key, UNREADABLE_JOURNAL);
    } catch {
      /* Keep the in-memory lock too. */
    }
    return { drafts: {}, pending: {}, unreadable: true };
  }
}
function confirmsChange(
  data: HandoffWorkspace,
  pending: PendingChange,
  receipt: HandoffChange,
): boolean {
  const reference = pending.reference;
  const kind = receiptKinds[reference.kind];
  if (
    receipt.status !== "Saved" ||
    receipt.commandId !== reference.commandId ||
    receipt.subjectId !== reference.workPlanId ||
    receipt.kind !== kind ||
    receipt.payloadHash !== reference.payloadHash ||
    receipt.resultRevision === null ||
    data.handoff.id !== reference.handoffId
  ) {
    return false;
  }
  const plan = data.workPlan;
  if (reference.kind === "message") {
    return BigInt(data.handoff.revision) >= BigInt(receipt.resultRevision);
  }
  if (reference.kind === "budget" || reference.kind === "plan") {
    if (!plan) {
      return false;
    }
    if (plan.id !== reference.workPlanId) {
      // A fork names the old accepted plan; an earlier in-place edit may also have been accepted since.
      const reviewed = data.decisions.find((d) => d.workPlanId === reference.workPlanId);
      if (!reviewed) {
        return false;
      }
      const fork =
        reviewed.revision === reference.expectedRevision && receipt.resultRevision === "1";
      const subsequentlyAccepted =
        BigInt(receipt.resultRevision) === BigInt(reference.expectedRevision) + 1n &&
        BigInt(reviewed.revision) >= BigInt(receipt.resultRevision);
      return fork || subsequentlyAccepted;
    }
    if (
      BigInt(receipt.resultRevision) !== BigInt(reference.expectedRevision) + 1n ||
      BigInt(plan.revision) < BigInt(receipt.resultRevision)
    ) {
      return false;
    }
    if (plan.revision !== receipt.resultRevision || !pending.change) {
      return true;
    }
    if (pending.change.kind === "budget") {
      return plan.budgetCents === pending.change.budgetCents;
    }
    if (pending.change.kind === "plan") {
      const changes = pending.change.changes;
      return Object.entries(changes).every(
        ([key, value]) => orderedJson(Reflect.get(plan, key)) === orderedJson(value),
      );
    }
    return false;
  }
  const decision = data.decisions.find(
    (d) => d.workPlanId === reference.workPlanId && d.revision === reference.expectedRevision,
  );
  return Boolean(
    decision &&
    BigInt(data.handoff.revision) >= BigInt(receipt.resultRevision) &&
    (!pending.change ||
      pending.change.kind === "message" ||
      decision.budgetCents === pending.change.budgetCents) &&
    (plan?.id !== reference.workPlanId ||
      (plan.acceptedDecisionId === decision.id &&
        plan.revision === decision.revision &&
        plan.budgetCents === decision.budgetCents &&
        plan.currency === decision.currency)),
  );
}

export class HandoffStore {
  readonly list: ReadResource<HandoffList>;
  private resources = new Map<string, ReadResource<HandoffWorkspace>>();
  private listeners = new Set<() => void>();
  private version = 0;
  private generation = 0;
  private journal: Journal;
  private sending = new Set<string>();
  private notices = new Map<string, string>();
  private messages = new Map<string, { value: string; planId?: string; revision?: string }>();
  constructor(
    readonly gateway: HandoffGateway,
    private readonly storage?: Storage,
    private readonly storageKey = "handoff.changes",
    private readonly interval = 7000,
  ) {
    this.journal = loadJournal(storage, storageKey);
    this.list = new ReadResource(() => gateway.list(), undefined, interval);
  }
  getSnapshot = () => this.version;
  subscribe = (fn: () => void) => {
    this.listeners.add(fn);
    return () => {
      this.listeners.delete(fn);
    };
  };
  private emit() {
    this.version++;
    this.listeners.forEach((fn) => fn());
  }
  private persist(): boolean {
    try {
      if (!this.storage) {
        return false;
      }
      const pending = Object.values(this.journal.pending).map((entry) => entry.reference);
      if (pending.length > MAX_CHANGES || !pending.every(validReference)) {
        return false;
      }
      const encoded = this.journal.unreadable
        ? UNREADABLE_JOURNAL
        : JSON.stringify({ version: "2", pending });
      if (new TextEncoder().encode(encoded).length > MAX_JOURNAL_BYTES) {
        return false;
      }
      this.storage.setItem(this.storageKey, encoded);
      return true;
    } catch {
      return false;
    }
  }
  workspace(id: string) {
    let resource = this.resources.get(id);
    if (!resource) {
      resource = new ReadResource(
        async () => {
          const generation = this.generation;
          const pending = this.pending(id);
          let receipt: HandoffChange | undefined;
          if (pending) {
            try {
              receipt = await this.gateway.receipt(id, pending.reference.commandId);
            } catch {
              /* A failed check never proves absence or unlocks another change. */
            }
          }
          // Read after the confirmation, so lagging or mixed views cannot clear a pending change.
          let data: HandoffWorkspace;
          try {
            data = await this.gateway.workspace(id);
          } catch (error) {
            if (error instanceof HandoffError && ["access", "permission"].includes(error.kind)) {
              this.generation++;
              this.journal.drafts = {};
              this.messages.clear();
              Object.values(this.journal.pending).forEach((entry) => {
                entry.change = undefined;
                entry.status = "checking";
              });
              this.sending.clear();
              this.gateway.clearDocuments?.();
              this.resources.forEach((other, key) => {
                if (key !== id) {
                  other.clear();
                }
              });
              this.emit();
            }
            throw error;
          }
          const previousPlan = this.resources.get(id)?.getSnapshot().data?.workPlan;
          if (
            generation === this.generation &&
            !this.pending(id) &&
            previousPlan &&
            data.workPlan &&
            previousPlan.id !== data.workPlan.id
          ) {
            const draft = this.draft(previousPlan);
            if (draft) {
              this.journal.drafts[data.workPlan.id] = draft;
              delete this.journal.drafts[previousPlan.id];
            }
          }
          if (
            generation === this.generation &&
            pending &&
            this.pending(id) === pending &&
            receipt
          ) {
            this.reconcile(data, pending, receipt);
          }
          return data;
        },
        undefined,
        // Read often while a step or reply is due, rarely while vendors work.
        this.interval > 0 ? (data?: HandoffWorkspace) => pollDelay(data, this.interval) : 0,
      );
      this.resources.set(id, resource);
    }
    return resource;
  }
  draft(plan: WorkPlan) {
    return this.journal.drafts[plan.id];
  }
  pending(id: string) {
    return this.journal.pending[id];
  }
  blocked() {
    return Boolean(this.journal.unreadable);
  }
  isSending(id: string) {
    return this.sending.has(id);
  }
  dismissNotice(id: string) {
    if (this.notices.delete(id)) {
      this.emit();
    }
  }
  notice(id: string) {
    return this.blocked()
      ? "We couldn't recover your earlier changes. Ask your team to check before making another change."
      : this.notices.get(id);
  }
  edit(plan: WorkPlan, value: string) {
    this.journal.drafts[plan.id] = {
      ...(this.draft(plan) ?? {
        revision: plan.revision,
        originalBudget: plan.budgetCents,
        reviewedPlanId: plan.id,
      }),
      value,
    };
    this.emit();
  }
  discard(plan: WorkPlan) {
    delete this.journal.drafts[plan.id];
    this.emit();
  }
  reviewLatest(plan: WorkPlan) {
    const draft = this.draft(plan);
    if (draft) {
      this.journal.drafts[plan.id] = {
        ...draft,
        revision: plan.revision,
        originalBudget: plan.budgetCents,
        reviewedPlanId: plan.id,
      };
      this.emit();
    }
  }
  editProposal(plan: WorkPlan, changes: WorkPlanChange) {
    this.journal.drafts[plan.id] = {
      ...(this.draft(plan) ?? {
        value: budgetInput(plan.budgetCents),
        revision: plan.revision,
        originalBudget: plan.budgetCents,
        reviewedPlanId: plan.id,
      }),
      changes: structuredClone(changes),
    };
    this.emit();
  }
  messageDraft(id: string) {
    return this.messages.get(id);
  }
  editMessage(data: HandoffWorkspace, value: string) {
    this.messages.set(data.handoff.id, {
      ...(this.messageDraft(data.handoff.id) ?? {
        planId: data.workPlan?.id,
        revision: data.workPlan?.revision,
      }),
      value,
    });
    this.emit();
  }
  reviewMessage(data: HandoffWorkspace) {
    const draft = this.messageDraft(data.handoff.id);
    if (draft) {
      this.messages.set(data.handoff.id, {
        ...draft,
        planId: data.workPlan?.id,
        revision: data.workPlan?.revision,
      });
    }
    this.emit();
  }
  private current(data: HandoffWorkspace, permission: "canWork" | "canDecide") {
    const latest = this.resources.get(data.handoff.id)?.getSnapshot();
    return (
      data.permissions[permission] &&
      !latest?.failed &&
      (!latest?.data ||
        (latest.data.permissions[permission] &&
          latest.data.workPlan?.id === data.workPlan?.id &&
          latest.data.workPlan?.revision === data.workPlan?.revision &&
          latest.data.workPlan?.acceptedDecisionId === data.workPlan?.acceptedDecisionId &&
          latest.data.workPlan?.status === data.workPlan?.status))
    );
  }
  private reconcile(data: HandoffWorkspace, pending: PendingChange, receipt: HandoffChange) {
    if (!confirmsChange(data, pending, receipt)) {
      return;
    }
    this.notices.set(
      data.handoff.id,
      pending.reference.kind === "message"
        ? "Your message is saved. Handoff will consider it with the current work."
        : "Your change was saved.",
    );
    if (pending.reference.kind === "message") {
      this.messages.delete(data.handoff.id);
    }
    delete this.journal.pending[data.handoff.id];
    delete this.journal.drafts[pending.reference.workPlanId];
    this.persist();
    this.emit();
  }
  async submit(
    data: HandoffWorkspace,
    kind: "budget" | "accept" | "plan",
    amount?: string,
    changes?: WorkPlanChange,
  ) {
    const plan = data.workPlan,
      id = data.handoff.id;
    if (
      !plan ||
      (kind === "accept" && plan.acceptedDecisionId) ||
      !this.current(data, "canDecide") ||
      this.pending(id) ||
      this.sending.has(id) ||
      this.blocked()
    ) {
      return;
    }
    const draft = this.draft(plan);
    const budgetCents =
      kind === "budget"
        ? amount
        : kind === "plan"
          ? (changes?.budgetCents ?? plan.budgetCents)
          : plan.budgetCents;
    if (
      !budgetCents ||
      !/^(0|[1-9]\d{0,9})$/.test(budgetCents) ||
      BigInt(budgetCents) > MAX_WORK_BUDGET_CENTS ||
      (kind !== "plan" && BigInt(budgetCents) < BigInt(plan.estimatedCostCents)) ||
      (draft && (draft.revision !== plan.revision || draft.reviewedPlanId !== plan.id)) ||
      (kind === "accept" &&
        draft &&
        (parseBudget(draft.value) !== plan.budgetCents || Boolean(draft.changes))) ||
      (kind === "plan" && (!changes || !Object.keys(changes).length))
    ) {
      return;
    }
    if (changes) {
      changes = {
        ...changes,
        ...(changes.selections
          ? {
              selections: changes.selections.map((line) => ({
                ...line,
                scope: line.scope.trim(),
                reason: line.reason.trim(),
              })),
            }
          : {}),
        ...(changes.fixedRequirements
          ? {
              fixedRequirements: changes.fixedRequirements
                .map((line) => line.trim())
                .filter(Boolean),
            }
          : {}),
      };
    }
    const base = {
      handoffId: id,
      workPlanId: plan.id,
      expectedRevision: plan.revision,
      budgetCents,
      commandId: crypto.randomUUID(),
    };
    const change: Change =
      kind === "plan"
        ? Object.freeze({ ...base, kind, changes: structuredClone(changes!) })
        : Object.freeze({ ...base, kind });
    await this.prepare(data, change);
  }
  async sendMessage(data: HandoffWorkspace) {
    const id = data.handoff.id,
      draft = this.messageDraft(id);
    if (
      !draft?.value.trim() ||
      draft.value.length > 8000 ||
      draft.planId !== data.workPlan?.id ||
      draft.revision !== data.workPlan?.revision ||
      !this.current(data, "canWork") ||
      this.pending(id) ||
      this.sending.has(id) ||
      this.blocked()
    ) {
      return;
    }
    const change: Change = Object.freeze({
      kind: "message",
      handoffId: id,
      commandId: crypto.randomUUID(),
      message: draft.value.trim(),
      ...(draft.revision === undefined ? {} : { expectedPlanRevision: draft.revision }),
    });
    await this.prepare(data, change);
  }
  private async prepare(data: HandoffWorkspace, change: Change) {
    const id = data.handoff.id;
    const generation = this.generation;
    this.sending.add(id);
    this.emit();
    let payloadHash: string;
    try {
      payloadHash = await changePayloadHash(change);
    } catch {
      if (generation === this.generation) {
        this.sending.delete(id);
        this.notices.set(id, "We couldn't prepare your change. Please try again.");
        this.emit();
      }
      return;
    }
    if (generation !== this.generation) {
      return;
    }
    if (!this.current(data, change.kind === "message" ? "canWork" : "canDecide")) {
      this.sending.delete(id);
      this.notices.set(id, "The work changed. Review it before sending your change.");
      this.emit();
      return;
    }
    const reference = Object.freeze({
      kind: change.kind,
      handoffId: id,
      workPlanId: change.kind === "message" ? id : change.workPlanId,
      expectedRevision:
        change.kind === "message" ? (change.expectedPlanRevision ?? "0") : change.expectedRevision,
      commandId: change.commandId,
      payloadHash,
    });
    this.journal.pending[id] = { reference, change, acknowledged: false, status: "sending" };
    this.notices.delete(id);
    if (!this.persist()) {
      delete this.journal.pending[id];
      this.sending.delete(id);
      this.notices.set(
        id,
        "We couldn't keep your change ready. Check earlier changes and allow browser storage before trying again.",
      );
      this.emit();
      return;
    }
    await this.send(change);
  }
  private async send(change: Change, replay = false) {
    const id = change.handoffId;
    const generation = this.generation;
    this.sending.add(id);
    this.emit();
    try {
      const result = await this.gateway.apply(change);
      if (generation !== this.generation) {
        return;
      }
      if (result === "rejected" && !replay) {
        delete this.journal.pending[id];
        this.notices.set(
          id,
          "Your change wasn't saved. Review the latest work plan before trying again.",
        );
      } else if (result === "saved" && this.pending(id)) {
        this.journal.pending[id].acknowledged = true;
        if (change.kind === "message") {
          this.notices.set(id, "Message received. Checking the saved conversation…");
        }
      }
    } catch {
      // Keep the original identity when the response may have been lost after the save.
    } finally {
      if (generation === this.generation) {
        this.sending.delete(id);
        if (this.pending(id)) {
          this.journal.pending[id].status = "checking";
        }
        this.persist();
        this.emit();
        await this.workspace(id).fresh();
        await this.list.refresh();
      }
    }
  }
  /** An exact retry is possible only in memory; a reopened page can only check the saved result. */
  async replay(id: string) {
    if (this.sending.has(id)) {
      return;
    }
    await this.workspace(id).fresh();
    const pending = this.pending(id);
    const latest = this.workspace(id).getSnapshot();
    if (
      latest.failed ||
      !latest.data ||
      !latest.data.permissions[pending?.change?.kind === "message" ? "canWork" : "canDecide"] ||
      !pending?.change ||
      pending.acknowledged ||
      this.sending.has(id)
    ) {
      return;
    }
    pending.status = "sending";
    if (!this.persist()) {
      return;
    }
    await this.send(pending.change, true);
  }
  refresh = async () => {
    await Promise.all([
      this.list.refresh(),
      ...[...this.resources.values()].map((r) => r.refresh()),
    ]);
  };
  clear() {
    this.generation++;
    this.list.clear();
    this.resources.forEach((r) => r.clear());
    this.journal = { drafts: {}, pending: {} };
    this.notices.clear();
    this.messages.clear();
    this.gateway.clearDocuments?.();
    this.sending.clear();
    // Keep only the already-persisted, scoped references if an earlier request may have saved.
    this.emit();
  }
  dispose() {
    this.clear();
  }
}
