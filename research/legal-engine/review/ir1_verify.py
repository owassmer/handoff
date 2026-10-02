"""Independent review 1: check that every evidence quote in independent_review_1.json appears verbatim
(whitespace-normalized) in its source file, and that every cited rule id exists. Exit 1 on any failure.

Usage (from research/legal-engine): python3 review/ir1_verify.py [--selftest]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main(data):
    ids = set()
    for k in ("NY", "NYC", "VA", "US"):
        ids |= {a["id"] for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]}
    bad = 0
    n = 0
    for f in data["findings"]:
        for r in f["rule_ids"]:
            if r not in ids:
                print(f"{f['id']}: unknown rule id {r}")
                bad += 1
        for e in f["evidence"]:
            n += 1
            p = ROOT / e["source_file"]
            if not p.exists():
                print(f"{f['id']}: missing file {e['source_file']}")
                bad += 1
                continue
            if norm(e["quote"]) not in norm(p.read_text(encoding="utf-8", errors="replace")):
                print(f"{f['id']}: quote not found in {e['source_file']}: {e['quote'][:80]}")
                bad += 1
    print(f"{len(data['findings'])} findings, {n} evidence quotes, {bad} failures")
    return bad


if __name__ == "__main__":
    data = json.loads((ROOT / "review/independent_review_1.json").read_text())
    if "--selftest" in sys.argv:
        data["findings"][0]["evidence"][0]["quote"] += " PLANTED"
        data["findings"][0]["rule_ids"].append("NY:NO-SUCH-RULE")
        sys.exit(0 if main(data) == 2 else 1)
    sys.exit(1 if main(data) else 0)
