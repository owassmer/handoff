"""Independent review 2: dump every rule the walk cites, side by side with the walk's paragraph.

Usage: python3 review/ir2_dump.py [out_path]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATOMS = {}
for k in ("NY", "NYC", "VA", "US"):
    for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
        ATOMS[a["id"]] = a

walk = (ROOT / "review/NYC_MARKET_RATE.md").read_text()
body, _, deferred = walk.partition("## Covered in later reviews")
paras = re.split(r"\n(?=\d+\.\d+ |- |C\d)", body)
cited = []
where = {}
for p in paras:
    for i in re.findall(r"`([A-Z]+:[^`]+)`", p):
        if i not in where:
            cited.append(i)
            where[i] = p.strip()
out = []
last = None
for i in cited:
    a = ATOMS.get(i)
    if where[i] != last:
        out.append("#" * 100)
        out.append("WALK: " + where[i].replace("\n", " "))
        last = where[i]
    out.append("-" * 60)
    out.append(f"ID {i}")
    if not a:
        out.append("  !! NO SUCH RULE")
        continue
    out.append(f"DET {a['determinacy']} | from {a['effective_from']} | to {a['effective_to']}")
    out.append("COND: " + a["condition"])
    out.append("EFFECT: " + a["effect"])
    out.append("QUOTE: " + a["quote"])
    out.append("SRC: " + a["source_file"] + " | " + a["source_url"])
    for c in a.get("construction", []):
        out.append("  AUTH: " + c["quote"] + "  [" + c["source_file"] + "]")
    if a.get("reasoning"):
        out.append("  REASON: " + a["reasoning"])
    if a.get("dependencies"):
        out.append("  DEPS: " + ", ".join(a["dependencies"]))
path = sys.argv[1] if len(sys.argv) > 1 else "/Users/owenwassmer/.hermes/profiles/ferro/cache/scratch/ir2_dump.txt"
pathlib.Path(path).write_text("\n".join(out))
print(len(cited), "cited;", sum(1 for i in cited if i not in ATOMS), "missing;", path)
