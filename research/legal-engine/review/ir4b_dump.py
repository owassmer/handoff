"""IR4B: side-by-side dump of every rule cited in the NYC market-rate walk.

Writes one text block per cited rule: the walk passage(s) citing it, then every field of the rule,
construction quotes and reasoning, and the first lines (header) of its source file.
Output: $TMPDIR/ir4b_dump.txt (scratch; not part of the review record).
Usage: python3 review/ir4b_dump.py [--all-scope]
"""
import json
import os
import pathlib
import re
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
WALK = (ROOT / "review/NYC_MARKET_RATE.md").read_text()
ATOMS = {}
for k in ("NY", "NYC", "VA", "US"):
    for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
        ATOMS[a["id"]] = a

lines = WALK.splitlines()
deferred = set(re.findall(r"deferred: `([^`]+)`", WALK))
cited = []
for m in re.finditer(r"`((?:NY|NYC|US|VA):[^`]+)`", WALK):
    i = m.group(1)
    if i not in deferred and i not in cited:
        cited.append(i)


def passages(rid):
    out = []
    for n, l in enumerate(lines):
        if f"`{rid}`" in l:
            out.append(f"  [walk L{n+1}]")
    return out


def w(label, text):
    return textwrap.fill(str(text), 140, initial_indent=f"  {label}: ", subsequent_indent="      ")


buf = []
for rid in cited:
    a = ATOMS.get(rid)
    buf.append("=" * 20)
    buf.append(rid)
    buf.extend(passages(rid))
    if not a:
        buf.append("  MISSING RULE")
        continue
    for f in ("instrument", "provision", "effective_from", "effective_to", "determinacy", "actor", "modality",
              "condition", "effect", "judgment_terms", "dependencies", "source_file", "source_url", "quote"):
        buf.append(w(f, a.get(f)))
    for c in a.get("construction", []) or []:
        buf.append(w("AUTH", f"{c.get('authority', '')} | {c.get('quote')} [{c.get('source_file')}]"))
    if a.get("reasoning"):
        buf.append(w("REASONING", a["reasoning"]))
    extra = {k: v for k, v in a.items() if k not in (
        "id", "jurisdiction", "instrument", "provision", "effective_from", "effective_to", "determinacy", "actor",
        "modality", "condition", "effect", "judgment_terms", "dependencies", "source_file", "source_url", "quote",
        "construction", "reasoning")}
    if extra:
        buf.append(w("OTHER", json.dumps(extra)))
out = pathlib.Path("/Users/owenwassmer/.hermes/profiles/ferro/cache/scratch/ir4b_dump.txt")
out.write_text("\n".join(buf))
print(len(cited), "cited rules dumped to", out)
