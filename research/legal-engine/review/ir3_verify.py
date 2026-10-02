"""Verify review/independent_review_3.json.

Checks: every evidence quote appears verbatim (whitespace-normalized) in its source file; every rule id cited in a finding
exists in stage-a/{NY,NYC,VA,US}.json. A self-test plants a bad quote and a bad id and requires both to be caught.

Run from research/legal-engine:  python3 review/ir3_verify.py
"""
import copy
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def rule_ids():
    ids = set()
    for k in ("NY", "NYC", "VA", "US"):
        ids |= {a["id"] for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]}
    return ids


def check(data, ids, cache):
    errors, n_quotes = [], 0
    for f in data["findings"]:
        for r in f["rule_ids"]:
            if r not in ids:
                errors.append(f"{f['id']}: unknown rule id {r}")
        if not f["evidence"]:
            errors.append(f"{f['id']}: no evidence")
        for e in f["evidence"]:
            n_quotes += 1
            p = ROOT / e["source_file"]
            if not p.exists():
                errors.append(f"{f['id']}: missing source {e['source_file']}")
                continue
            if p not in cache:
                cache[p] = norm(p.read_text(errors="replace"))
            if norm(e["quote"]) not in cache[p]:
                errors.append(f"{f['id']}: quote not found in {e['source_file']}: {e['quote'][:80]!r}")
    return errors, n_quotes


def main():
    data = json.loads((ROOT / "review/independent_review_3.json").read_text())
    ids, cache = rule_ids(), {}
    errors, n = check(data, ids, cache)

    # Self-test: one altered word in a real quote, and one invented rule id.
    bad = copy.deepcopy(data)
    e = bad["findings"][0]["evidence"][0]
    words = e["quote"].split()
    words[len(words) // 2] = "XYZZY" + words[len(words) // 2]
    e["quote"] = " ".join(words)
    bad["findings"][0]["rule_ids"].append("NY:NO-SUCH-RULE-R3")
    bad_errors, _ = check(bad, ids, cache)
    caught_quote = any("quote not found" in x for x in bad_errors)
    caught_id = any("NY:NO-SUCH-RULE-R3" in x for x in bad_errors)

    for x in errors:
        print("ERROR", x)
    print(f"findings {len(data['findings'])}, evidence quotes {n}, errors {len(errors)}")
    print(f"self-test: planted bad quote caught={caught_quote}, planted bad id caught={caught_id}")
    ok = not errors and caught_quote and caught_id
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
