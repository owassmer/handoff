"""IR5A Phase 2: candidate mapping of universe items to rule atoms (mechanical first pass; adjudicated by hand after).

Match signals: same source file; section token of the citation found in atom instrument/provision/quote/effect/source_file.
Writes scratch ir5a/map.txt and prints items with zero candidates.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/ir5a"
atoms = []
for f in ["NY", "NYC", "US"]:
    d = json.load(open(ROOT / "stage-a" / f"{f}.json"))
    atoms += d["atoms"]
U = json.load(open(ROOT / "review" / "review5a_universe.json"))


def norm_src(s):
    s = pathlib.Path(s or "").name
    s = re.sub(r"\.txt$", "", s)
    s = re.sub(r"^(REVIEW\d[AB]?_|SWEEP_)", "", s)
    s = re.sub(r"_(nysenate|justia|LII|uscode|ecfr|courtlistener|nycourts)$", "", s, flags=re.I)
    return s.upper()


def tokens(cit):
    toks = set()
    for m in re.finditer(r"(\d+[A-Za-z]?(?:[-.]\d+[A-Za-z0-9.\-]*)?)", cit):
        t = m.group(1)
        if len(t) >= 3 or "-" in t:
            toks.add(t.lower())
    return toks


lines, zero = [], []
for u in U:
    us = norm_src(u["source_file"])
    toks = tokens(u["citation"].split("(")[0] if not u["citation"].startswith("(") else u["citation"])
    cands = []
    for a in atoms:
        hay = " ".join(str(a.get(k, "")) for k in ("instrument", "provision", "source_file")).lower()
        score = 0
        if norm_src(a.get("source_file")) == us:
            score += 2
        if any(re.search(r"(?<![\d.])" + re.escape(t) + r"(?![\d])", hay) for t in toks):
            score += 1
        if score:
            cands.append((score, a["id"]))
    cands.sort(reverse=True)
    lines.append(f"{u['id']}\t{u['citation']}\t{' '.join(i for s, i in cands[:12])}")
    if not cands:
        zero.append(f"{u['id']} {u['citation']}")
(OUT / "map.txt").write_text("\n".join(lines))
print(len(zero), "items with no candidate atoms:")
print("\n".join(zero))
