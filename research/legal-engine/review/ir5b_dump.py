"""Round 5B: side-by-side dump of every rule cited in the market-rate walk.

For each cited id (walk order), prints the walk paragraph that cites it and every field of the rule.
Writes to $TMPDIR/ir5b_dump_NN.txt in chunks of ~60 rules. Usage: python3 review/ir5b_dump.py
"""
import json
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path("/Users/owenwassmer/.hermes/profiles/ferro/cache/scratch")
ATOMS = {}
for k in ("NY", "NYC", "US"):
    for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
        ATOMS[a["id"]] = a
walk = (ROOT / "review/NYC_MARKET_RATE.md").read_text()
paras = re.split(r"\n(?=\d+\.\d+a? |- |C\d|T-|## )", walk)
order, ctx = [], {}
for p in paras:
    for i in re.findall(r"`((?:NY|NYC|US):[^`\s]+)`", p):
        if "deferred: `" + i in walk:
            continue
        if i not in ctx:
            ctx[i] = []
            order.append(i)
        if len(ctx[i]) < 2:
            ctx[i].append(p.strip())
chunks = [order[i:i + 11] for i in range(0, len(order), 11)]
for n, ch in enumerate(chunks):
    lines = []
    seen = set()
    for i in ch:
        a = ATOMS.get(i)
        lines.append("=" * 100)
        lines.append(f"ID {i}")
        for c in ctx[i]:
            key = c[:80]
            if key in seen:
                lines.append("WALK (see above): " + re.sub(r"\s+", " ", c)[:120])
            else:
                seen.add(key)
                lines.append("WALK: " + re.sub(r"\s+", " ", c)[:1500])
        if not a:
            lines.append("  MISSING")
            continue
        for f in ("determinacy", "modality", "actor", "instrument", "provision", "effective_from", "effective_to",
                  "condition", "effect", "judgment_terms", "quote", "source_file", "source_url", "dependencies"):
            lines.append(f"  {f}: {a.get(f)}")
        for c in a.get("construction", []) or []:
            lines.append(f"  AUTH: [{c.get('source_file')}] {c.get('quote')}")
            extra = {k: v for k, v in c.items() if k not in ("quote", "source_file")}
            if extra:
                lines.append(f"        {extra}")
        if a.get("reasoning"):
            lines.append(f"  REASONING: {a['reasoning']}")
        other = {k: v for k, v in a.items() if k not in (
            "id", "determinacy", "modality", "actor", "instrument", "provision", "effective_from", "effective_to",
            "condition", "effect", "judgment_terms", "quote", "source_file", "source_url", "dependencies",
            "construction", "reasoning", "jurisdiction")}
        if other:
            lines.append(f"  OTHER: {other}")
    (OUT / f"ir5b_dump_{n:02d}.txt").write_text("\n".join(lines))
    print(n, len(ch), sum(len(l) for l in lines))
print("total", len(order))
