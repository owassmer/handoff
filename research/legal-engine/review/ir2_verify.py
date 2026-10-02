"""Independent review 2: verify review/independent_review_2.json.

Checks (run from research/legal-engine):  python3 review/ir2_verify.py
- every evidence quote appears verbatim in its source file (whitespace-normalized);
- every cited rule id (findings, confirmed) exists in stage-a/{NY,NYC,US,VA}.json;
- every first-round verdict names R1-01..R1-17 once (when present);
- a self-test plants a bad quote and a bad id and confirms both are caught.
Exit status 0 only if all checks pass and the self-test catches both plants.
"""
import copy
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "review/independent_review_2.json"

IDS = set()
for k in ("NY", "NYC", "US", "VA"):
    for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
        IDS.add(a["id"])


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


_cache = {}


def text(path):
    if path not in _cache:
        p = ROOT / path
        _cache[path] = norm(p.read_text(errors="replace")) if p.exists() else None
    return _cache[path]


def check(data):
    errors = []
    for f in data["findings"]:
        for rid in f.get("rule_ids", []):
            if rid not in IDS:
                errors.append(f"{f['id']}: unknown rule id {rid}")
        if not f.get("evidence"):
            errors.append(f"{f['id']}: no evidence")
        for e in f.get("evidence", []):
            t = text(e["source_file"])
            if t is None:
                errors.append(f"{f['id']}: missing source file {e['source_file']}")
            elif norm(e["quote"]) not in t:
                errors.append(f"{f['id']}: quote not found in {e['source_file']}: {e['quote'][:80]}")
        for key in ("id", "kind", "severity", "step", "finding", "correct_rule"):
            if not f.get(key) and key != "step":
                errors.append(f"{f['id']}: empty field {key}")
        if f.get("kind") not in {"error", "gap", "misstatement-in-review", "weak-support", "stale-source", "over-scope", "alignment"}:
            errors.append(f"{f['id']}: bad kind {f.get('kind')}")
        if f.get("severity") not in {"critical", "major", "minor"}:
            errors.append(f"{f['id']}: bad severity {f.get('severity')}")
    for c in data.get("confirmed", []):
        for rid in c.get("rule_ids", []):
            if rid not in IDS:
                errors.append(f"confirmed {c['id']}: unknown rule id {rid}")
    fr = data.get("first_round", [])
    if fr:
        want = {f"R1-{i:02d}" for i in range(1, 18)}
        got = [x["id"] for x in fr]
        if set(got) != want or len(got) != len(want):
            errors.append(f"first_round ids incomplete or duplicated: {sorted(set(want) ^ set(got))}")
        for x in fr:
            if not x.get("verdict") or not x.get("reason"):
                errors.append(f"first_round {x.get('id')}: empty verdict or reason")
    return errors


def main():
    data = json.loads(DATA.read_text())
    errors = check(data)
    nq = sum(len(f["evidence"]) for f in data["findings"])
    nid = sum(len(f["rule_ids"]) for f in data["findings"]) + sum(len(c["rule_ids"]) for c in data.get("confirmed", []))
    # self-test: a planted bad quote and a planted bad id must both be caught
    bad = copy.deepcopy(data)
    bad["findings"][0]["evidence"].append({"source_file": bad["findings"][0]["evidence"][0]["source_file"],
                                           "quote": "No rent shall be recovered by the tenant for ever and ever."})
    bad["findings"][0]["rule_ids"].append("NY:NO-SUCH-RULE-999")
    planted = check(bad)
    caught_quote = any("quote not found" in e for e in planted)
    caught_id = any("NY:NO-SUCH-RULE-999" in e for e in planted)
    print(f"findings {len(data['findings'])}, evidence quotes {nq}, rule-id references {nid}, "
          f"confirmed {len(data.get('confirmed', []))}, first_round {len(data.get('first_round', []))}")
    print(f"self-test: planted bad quote caught={caught_quote}, planted bad id caught={caught_id}")
    for e in errors:
        print("ERROR", e)
    ok = not errors and caught_quote and caught_id
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
