import type { Client } from "@osdk/client";
import { workspaceView } from "../handoff/readWorkspace.js";

export const config = { apiName: "getHandoffWorkspace" };

/** Read one coherent handoff view for the signed-in person. */
export default async function getHandoffWorkspace(client: Client, handoffId: string): Promise<string> {
  return JSON.stringify(await workspaceView(client, handoffId));
}
