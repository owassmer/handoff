import type { Client } from "@osdk/client";
import { handoffList } from "../handoff/readWorkspace.js";

export const config = { apiName: "listHandoffs" };

/** List up to 25 handoffs visible to the signed-in person. */
export default async function listHandoffs(client: Client, workspaceId: string): Promise<string> {
  return JSON.stringify(await handoffList(client, workspaceId));
}
