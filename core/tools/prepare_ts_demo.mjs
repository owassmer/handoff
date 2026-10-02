// Development-only: construct preview inputs from unchanged literal fixtures.
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
const root = resolve(import.meta.dirname, "..");
const fixtureRoot = resolve(root, "typescript-functions/src/deposit_closeout/__tests__/fixtures");
const base = JSON.parse(readFileSync(resolve(fixtureRoot, "base_request.json"), "utf8"));
const corpus = JSON.parse(readFileSync(resolve(fixtureRoot, "cases.json"), "utf8"));
const byId = new Map(corpus.cases.map((item) => [item.id, item]));
function materialize(id, visited = []) {
  if (visited.includes(id)) throw new Error("Fixture cycle");
  const entry = byId.get(id);
  if (!entry) throw new Error("Unknown fixture ID");
  const request = entry.extends ? materialize(entry.extends, [...visited, id]) : structuredClone(base);
  entry.patches.forEach((patch) => {
    const keys = patch.path.split("/").slice(1).map((part) => part.replace(/~1/g, "/").replace(/~0/g, "~"));
    const key = keys.pop();
    const parent = keys.reduce((item, part) => item[part], request);
    if (patch.op === "add" && key === "-" && Array.isArray(parent)) parent.push(structuredClone(patch.value));
    else if (patch.op === "replace" && Object.hasOwn(parent, key)) parent[key] = structuredClone(patch.value);
    else throw new Error("Unsupported or missing fixture path");
  });
  return request;
}
const ordinary = materialize("NC-A-002");
ordinary.ruleReleaseId = "NC_SYNTHETIC_REVIEW_V1";
const changed = structuredClone(ordinary);
const repair = changed.snapshot.charges.find((item) => item.itemId === "repair-250");
if (!repair) throw new Error("Missing repair");
repair.chosenAmountCents = 20000;
const outputDir = resolve(root, "build/tsv2-demo");
mkdirSync(outputDir, { recursive: true });
for (const [name, request] of [["ordinary", ordinary], ["changed", changed]]) {
  writeFileSync(resolve(outputDir, `${name}.json`), JSON.stringify({ requestJson: JSON.stringify(request) }, null, 2) + "\n");
}
process.stdout.write("Prepared two constructed preview inputs under build/tsv2-demo; original fixtures unchanged.\n");
