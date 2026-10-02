"""IR5B: verify review/independent_review_5b.json.

Checks (1) every evidence quote (findings and T-vacate ruling) appears verbatim, whitespace-normalized, in its source
file; (2) every rule id in findings exists in stage-a/{NY,NYC,US}.json. Self-test first: a planted bad quote and a
planted bad id must both be caught. Exit 1 on any failure.
Usage: python3 review/ir5b_verify.py
"""
import copy
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IDS = set()
for k in ("NY", "NYC", "US"):
    IDS |= {a["id"] for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def check(doc):
    errs = []
    ev = []
    for f in doc["findings"]:
        for i in f["rule_ids"]:
            if i not in IDS:
                errs.append(f"{f['id']}: no such rule id {i}")
        ev += [(f["id"], e) for e in f["evidence"]]
    ev += [("T-vacate", e) for e in doc["t_vacate_ruling"]["evidence"]]
    for who, e in ev:
        p = ROOT / e["source_file"]
        if not p.exists():
            errs.append(f"{who}: missing source {e['source_file']}")
            continue
        if norm(e["quote"]) not in norm(p.read_text(errors="replace")):
            errs.append(f"{who}: quote not found in {e['source_file']}: {e['quote'][:80]}")
    return errs, len(ev)


doc = json.loads((ROOT / "review/independent_review_5b.json").read_text())

# self-test
bad = copy.deepcopy(doc)
bad["findings"][0]["evidence"][0]["quote"] += " PLANTED WORDS"
bad["findings"][0]["rule_ids"].append("NY:NO-SUCH-RULE")
e, _ = check(bad)
assert any("quote not found" in x for x in e), "self-test: planted bad quote not caught"
assert any("no such rule id" in x for x in e), "self-test: planted bad id not caught"
print("self-test ok (planted bad quote and bad id caught)")

errs, n = check(doc)
print(f"findings {len(doc['findings'])}, evidence quotes checked {n}, confirmed {len(doc['confirmed'])}")
for x in errs:
    print("  FAIL", x)
sys.exit(1 if errs else 0)
