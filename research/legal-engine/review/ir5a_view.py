"""IR5A Phase 2 viewer: print universe items A..B with candidate atoms (from ir5a_map) and their effects, or atoms by regex.

python3 review/ir5a_view.py items 1 40 [N_CANDS]     python3 review/ir5a_view.py grep REGEX [MAXLEN]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCR = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/ir5a"
atoms = {}
for f in ["NY", "NYC", "US"]:
    for a in json.load(open(ROOT / "stage-a" / f"{f}.json"))["atoms"]:
        atoms[a["id"]] = a
if sys.argv[1] == "items":
    U = json.load(open(ROOT / "review" / "review5a_universe.json"))
    m = {l.split("\t")[0]: l.split("\t")[2].split() for l in (SCR / "map.txt").read_text().splitlines()}
    a0, b0 = int(sys.argv[2]), int(sys.argv[3])
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    for u in U[a0 - 1:b0]:
        print(f"## {u['id']} {u['citation']} -- {u['one_line_effect'][:160]}")
        for i in m.get(u["id"], [])[:n]:
            a = atoms[i]
            print(f"   {i}: {str(a.get('effect',''))[:170]}")
else:
    mx = int(sys.argv[3]) if len(sys.argv) > 3 else 220
    for i, a in atoms.items():
        blob = json.dumps(a)
        if re.search(sys.argv[2], blob, re.I):
            print(f"{i} | C: {str(a.get('condition',''))[:mx//2]} | E: {str(a.get('effect',''))[:mx]}")
