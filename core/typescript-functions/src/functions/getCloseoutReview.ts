import type { DcCloseoutCase } from "@ontology/sdk";
import type { Client, Osdk } from "@osdk/client";
import { loadCurrentReview } from "../deposit_closeout/phase_c/storage.js";

export const config = { apiName: "getCloseoutReview" };

/**
 * Read the validated stored review without modifying its legacy envelope or clock.
 * @param client Platform-injected client; object policies enforce reads of root and full JSON child.
 * @param closeoutCase Policy-visible stored root. No caller-supplied principal grants read access.
 * @returns Exact stored canonical ReviewEnvelope JSON after identity/hash/native-core verification.
 */
export default async function getCloseoutReview(
  client: Client, closeoutCase: Osdk.Instance<DcCloseoutCase>,
): Promise<string> {
  return (await loadCurrentReview(client, closeoutCase)).reviewJson;
}
