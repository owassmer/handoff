"""Independent review 1 helper: per cited rule, print review paragraph, condition, effect, quote, authorities.

Usage: python3 review/ir1_dump.py review/NYC_MARKET_RATE.md > /tmp/out.txt
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

text = pathlib.Path(sys.argv[1]).read_text()
# split into paragraphs keyed by numbered item (e.g. '5.2') or case (C3)
stop = text.find("## Covered in later reviews")
body = text[:stop]
paras = re.split(r"\n(?=\d\.\d+ |C\d+a?\. |## )", body)
seen = set()
for p in paras:
    ids = re.findall(r"`([A-Z]+:[^`]+)`", p)
    ids = [i for i in ids if i in ATOMS]
    if not ids:
        continue
    print("=" * 120)
    print("REVIEW PARA:", " ".join(p.split()))
    for i in ids:
        if i in seen:
            print(f"  (again) {i}")
            continue
        seen.add(i)
        a = ATOMS[i]
        print("-" * 60)
        print(f"ID {i} [{a['determinacy']}] from={a.get('effective_from')} to={a.get('effective_to') or 'open'}")
        print(f"  PROV: {a.get('instrument')} | {a.get('provision')}")
        print(f"  IF: {a['condition']}")
        print(f"  THEN: {a['effect']}")
        print(f"  QUOTE: {a['quote']}")
        print(f"  SRC: {a['source_file']} ({a['source_url']})")
        for c in a.get("construction", []):
            print(f"  AUTH: {c['quote']} [{c['source_file']}]")
        if a.get("reasoning"):
            print(f"  REASON: {a['reasoning']}")
