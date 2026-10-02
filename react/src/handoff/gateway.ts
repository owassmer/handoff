import { ActionValidationError, type Client, PalantirApiError } from "@osdk/client";
import { MediaSets, Ontologies } from "@osdk/foundry";
import { HANDOFF_BRANCH } from "./branchConfig";
import {
  type Change,
  HandoffError,
  type HandoffGateway,
  type SourceDocument,
  type StepResult,
  documentKey,
  readChange,
  readList,
  readWorkspace,
} from "./contracts";
import { verifiedOriginal } from "./sources";

export { HANDOFF_BRANCH } from "./branchConfig";
export interface HandoffConnection {
  ontologyRid: string;
  workspaceId?: string;
  /** Optional query version. Unset reads the newest published release, which the actions also run (Auto upgrade). */
  functionVersion?: string;
  /** Optional action runtime to match when recognizing a structured rejection. Unset matches any version. */
  actionFunctionVersion?: string;
  changeFunctionRid?: string;
  acceptFunctionRid?: string;
  messageFunctionRid?: string;
}
export function isConnected(connection: HandoffConnection): boolean {
  return Boolean(
    connection.workspaceId?.trim() &&
    (connection.functionVersion === undefined ||
      /^\d+\.\d+\.\d+(?:-[\w.-]+)?$/.test(connection.functionVersion)),
  );
}
const readInputs = {
  listHandoffs: ["workspaceId"],
  getHandoffWorkspace: ["handoffId"],
  getHandoffChange: ["handoffId", "commandId"],
} as const;
type ReadName = keyof typeof readInputs;

/** Fixed public query routes on the configured data scope; the newest published release unless a version is configured. */
export function createHandoffGateway(
  client: Client,
  connection: HandoffConnection,
): HandoffGateway {
  const queryOptions = {
    branch: HANDOFF_BRANCH,
    ...(connection.functionVersion ? { version: connection.functionVersion } : {}),
  };
  const documentsByHandoff = new Map<string, SourceDocument[]>();
  const reads = new Map<string, number>();
  const viewers = new Set<{ document: SourceDocument; invalidate(): void }>();
  let generation = 0;
  const known = (doc: SourceDocument) =>
    [...documentsByHandoff.values()].some((docs) =>
      docs.some((d) => documentKey(d) === documentKey(doc)),
    );
  function notifyViewers() {
    viewers.forEach((v) => {
      if (!known(v.document)) {
        v.invalidate();
      }
    });
  }
  function clearDocuments() {
    generation++;
    documentsByHandoff.clear();
    reads.clear();
    notifyViewers();
  }
  function ready() {
    if (!isConnected(connection)) {
      throw new HandoffError("unavailable");
    }
  }
  async function query(apiName: ReadName, parameters: Record<string, string>): Promise<unknown> {
    ready();
    const required = readInputs[apiName];
    if (
      Object.keys(parameters).length !== required.length ||
      required.some((key) => typeof parameters[key] !== "string" || !parameters[key].trim())
    ) {
      throw new HandoffError();
    }
    try {
      const response = await Ontologies.Queries.execute(
        client,
        connection.ontologyRid,
        apiName,
        { parameters },
        queryOptions,
      );
      return response.value;
    } catch (error) {
      if (error instanceof PalantirApiError) {
        if (["PERMISSION_DENIED", "UNAUTHORIZED"].includes(error.errorCode ?? "")) {
          clearDocuments();
          throw new HandoffError(error.errorCode === "UNAUTHORIZED" ? "access" : "permission");
        }
        if (
          error.errorCode === "NOT_FOUND" ||
          ["QueryVersionNotFound", "QueryNotFound"].includes(error.errorName ?? "")
        ) {
          throw new HandoffError("unavailable");
        }
      }
      throw error;
    }
  }
  return {
    clearDocuments,
    onDocumentInvalidated(document, invalidate) {
      const viewer = { document, invalidate };
      viewers.add(viewer);
      if (!known(document)) {
        invalidate();
      }
      return () => {
        viewers.delete(viewer);
      };
    },
    async list() {
      return readList(
        await query("listHandoffs", { workspaceId: connection.workspaceId ?? "" }),
        connection.workspaceId!,
      );
    },
    async workspace(handoffId) {
      const start = generation,
        ticket = (reads.get(handoffId) ?? 0) + 1;
      reads.set(handoffId, ticket);
      try {
        const value = readWorkspace(
          await query("getHandoffWorkspace", { handoffId }),
          connection.workspaceId!,
          handoffId,
        );
        if (start !== generation || reads.get(handoffId) !== ticket) {
          throw new HandoffError();
        }
        documentsByHandoff.set(handoffId, value.documents);
        notifyViewers();
        return value;
      } catch (error) {
        // A failed current read cannot authorize continued use of cached source material.
        if (reads.get(handoffId) === ticket) {
          documentsByHandoff.delete(handoffId);
          notifyViewers();
        }
        throw error;
      }
    },
    async receipt(handoffId, commandId) {
      return readChange(await query("getHandoffChange", { handoffId, commandId }), commandId);
    },
    async apply(change: Change) {
      ready();
      const start = generation;
      const apiName =
        change.kind === "message"
          ? "send-handoff-message"
          : change.kind === "accept"
            ? "accept-handoff-work-plan"
            : "change-handoff-work-plan";
      const parameters: Record<string, string> =
        change.kind === "message"
          ? {
              handoffId: change.handoffId,
              message: change.message,
              commandId: change.commandId,
              ...(change.expectedPlanRevision === undefined
                ? {}
                : { expectedPlanRevision: change.expectedPlanRevision }),
            }
          : {
              workPlanId: change.workPlanId,
              expectedRevision: change.expectedRevision,
              commandId: change.commandId,
              ...(change.kind === "budget"
                ? { budgetCents: change.budgetCents }
                : change.kind === "plan"
                  ? { changesJson: JSON.stringify(change.changes) }
                  : {}),
            };
      const required =
        change.kind === "message"
          ? ["handoffId", "message", "commandId"]
          : ["workPlanId", "expectedRevision", "commandId"];
      const optional =
        change.kind === "message"
          ? ["expectedPlanRevision"]
          : change.kind === "accept"
            ? []
            : ["budgetCents", "changesJson"];
      // Metadata validation precedes apply. Optional Longs may be omitted; no extra or caller-selected actor is allowed.
      try {
        const metadata = await Ontologies.ActionTypesV2.get(
          client,
          connection.ontologyRid,
          apiName,
          { branch: HANDOFF_BRANCH },
        );
        if (
          metadata.apiName !== apiName ||
          required.some((key) => !metadata.parameters[key]?.required) ||
          Object.keys(parameters).some((key) => !metadata.parameters[key]) ||
          Object.entries(metadata.parameters).some(
            ([key, param]) =>
              ![...required, ...optional].includes(key) ||
              (param.required && !(key in parameters)) ||
              !(
                ["expectedRevision", "budgetCents", "expectedPlanRevision"].includes(key)
                  ? ["string", "long"]
                  : ["string"]
              ).includes(param.dataType.type),
          )
        ) {
          return "rejected";
        }
      } catch {
        return "rejected";
      }
      // Disposing an identity while metadata was loading must not send with the next person's token.
      if (start !== generation) {
        return "rejected";
      }
      try {
        const result = await Ontologies.Actions.apply(
          client,
          connection.ontologyRid,
          apiName,
          { parameters, options: { mode: "VALIDATE_AND_EXECUTE", returnEdits: "NONE" } },
          { branch: HANDOFF_BRANCH },
        );
        return result.validation?.result === "INVALID" ? "rejected" : "saved";
      } catch (error) {
        if (error instanceof ActionValidationError) {
          return "rejected";
        }
        const functionRid =
          change.kind === "message"
            ? connection.messageFunctionRid
            : change.kind === "accept"
              ? connection.acceptFunctionRid
              : connection.changeFunctionRid;
        if (
          functionRid &&
          error instanceof PalantirApiError &&
          error.errorName === "FunctionEncounteredUserFacingError" &&
          error.errorCode === "INVALID_ARGUMENT" &&
          error.errorInstanceId &&
          error.parameters?.functionRid === functionRid &&
          (!(connection.actionFunctionVersion ?? connection.functionVersion) ||
            error.parameters?.functionVersion ===
              (connection.actionFunctionVersion ?? connection.functionVersion)) &&
          typeof error.parameters?.message === "string"
        ) {
          return "rejected";
        }
        throw error;
      }
    },
    async resume(handoffId: string): Promise<StepResult> {
      ready();
      if (typeof handoffId !== "string" || !handoffId.trim()) {
        throw new HandoffError();
      }
      // The action exposes only the case; the server binds the caller. Anything else is refused unsent.
      try {
        const metadata = await Ontologies.ActionTypesV2.get(
          client,
          connection.ontologyRid,
          "resume-handoff",
          { branch: HANDOFF_BRANCH },
        );
        const keys = Object.keys(metadata.parameters);
        if (
          metadata.apiName !== "resume-handoff" ||
          keys.length !== 1 ||
          metadata.parameters.handoffId?.dataType.type !== "string"
        ) {
          return { kind: "refused", message: "Resume handoff has unexpected inputs." };
        }
      } catch (error) {
        if (
          error instanceof PalantirApiError &&
          ["PERMISSION_DENIED", "UNAUTHORIZED", "NOT_FOUND"].includes(error.errorCode ?? "")
        ) {
          throw new HandoffError(error.errorCode === "UNAUTHORIZED" ? "access" : "permission");
        }
        throw error;
      }
      try {
        await Ontologies.Actions.apply(
          client,
          connection.ontologyRid,
          "resume-handoff",
          {
            parameters: { handoffId },
            options: { mode: "VALIDATE_AND_EXECUTE", returnEdits: "NONE" },
          },
          { branch: HANDOFF_BRANCH },
        );
        return { kind: "done" };
      } catch (error) {
        if (error instanceof ActionValidationError) {
          return { kind: "refused", message: "Resume handoff isn't available for this case." };
        }
        if (error instanceof PalantirApiError) {
          if (["PERMISSION_DENIED", "UNAUTHORIZED"].includes(error.errorCode ?? "")) {
            throw new HandoffError(error.errorCode === "UNAUTHORIZED" ? "access" : "permission");
          }
          const message = error.parameters?.message;
          return {
            kind: "refused",
            message: typeof message === "string" ? message : (error.errorName ?? "Refused"),
          };
        }
        throw error;
      }
    },
    async document(document) {
      const start = generation;
      if (!known(document) || !document.mediaSetRid || !document.mediaItemRid) {
        throw new HandoffError("document");
      }
      try {
        const response = await MediaSets.MediaSets.read(
          client,
          document.mediaSetRid,
          document.mediaItemRid,
        );
        if (!response.ok) {
          if ([401, 403].includes(response.status)) {
            clearDocuments();
          }
          throw new HandoffError("document");
        }
        const blob = await verifiedOriginal(await response.blob(), document);
        if (start !== generation || !known(document)) {
          throw new HandoffError("document");
        }
        return blob;
      } catch (error) {
        if (
          error instanceof PalantirApiError &&
          ["UNAUTHORIZED", "PERMISSION_DENIED"].includes(error.errorCode ?? "")
        ) {
          clearDocuments();
        }
        throw error;
      }
    },
  };
}
