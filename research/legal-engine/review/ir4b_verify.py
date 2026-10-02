"""IR4B verifier.

Checks review/independent_review_4b.json:
  1. every evidence quote occurs verbatim (whitespace-normalized) in its source_file (path relative to
     research/legal-engine);
  2. every rule id in findings[].rule_ids exists in stage-a/{NY,NYC,VA,US}.json;
  3. every finding has the required fields and a valid kind/severity.
Then runs a self-test: a planted bad quote and a planted bad rule id must both be caught.
Exit status 0 only if the real file passes and the self-test catches both plants.
Usage: python3 review/ir4b_verify.py
"""
import copy
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KINDS = {"error", "misread-authority", "missing-exception", "stale-source", "wrong-date", "contradiction",
         "misstatement-in-walk", "hedging"}
SEVS = {"critical", "major", "minor"}
IDS = set()
for k in ("NY", "NYC", "VA", "US"):
    for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
        IDS.add(a["id"])

_cache = {}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def text(path):
    if path not in _cache:
        _cache[path] = norm((ROOT / path).read_text(encoding="utf-8", errors="replace"))
    return _cache[path]


def check(doc):
    errs = []
    for f in doc["findings"]:
        for key in ("id", "kind", "severity", "rule_ids", "step", "finding", "correct_rule", "evidence"):
            if key not in f or f[key] in ("", [], None):
                errs.append(f"{f.get('id')}: missing {key}")
        if f.get("kind") not in KINDS:
            errs.append(f"{f.get('id')}: bad kind {f.get('kind')}")
        if f.get("severity") not in SEVS:
            errs.append(f"{f.get('id')}: bad severity {f.get('severity')}")
        for r in f.get("rule_ids", []):
            if r not in IDS:
                errs.append(f"{f['id']}: unknown rule id {r}")
        for e in f.get("evidence", []):
            p = e["source_file"]
            if not (ROOT / p).exists():
                errs.append(f"{f['id']}: missing source file {p}")
                continue
            if norm(e["quote"]) not in text(p):
                errs.append(f"{f['id']}: quote not found in {p}: {e['quote'][:70]}")
    return errs


def main():
    doc = json.loads((ROOT / "review/independent_review_4b.json").read_text())
    errs = check(doc)
    nq = sum(len(f["evidence"]) for f in doc["findings"])
    nr = sum(len(f["rule_ids"]) for f in doc["findings"])
    print(f"findings {len(doc['findings'])}; evidence quotes {nq}; rule ids {nr}; confirmed lines {len(doc['confirmed'])}")
    for e in errs:
        print("ERROR", e)
    # self-test
    bad = copy.deepcopy(doc)
    bad["findings"][0]["evidence"][0]["quote"] += " PLANTED WORDS NOT IN SOURCE"
    bad["findings"][1]["rule_ids"].append("NY:PLANTED-NO-SUCH-RULE")
    berrs = check(bad)
    caught_q = any("quote not found" in e and bad["findings"][0]["id"] in e for e in berrs)
    caught_id = any("NY:PLANTED-NO-SUCH-RULE" in e for e in berrs)
    print(f"self-test: planted bad quote caught={caught_q}; planted bad id caught={caught_id}")
    ok = not errs and caught_q and caught_id
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
