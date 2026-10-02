"""Independent review 4A: verify evidence and universe quotes and rule ids.

Checks:
  1. every finding evidence quote and every universe verbatim_quote occurs verbatim (whitespace-normalized) in its
     saved source file;
  2. every rule id cited in findings (rule_ids), over_scope and the coverage map exists in stage-a NY/NYC/VA/US;
  3. every finding id cited in the coverage map exists.
Self-test: plants a bad quote and a bad rule id and confirms both are caught.
Usage: python3 review/ir4a_verify.py
"""
import copy
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REV = ROOT / "review"


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


_cache = {}


def src_text(path):
    p = ROOT / path
    if p not in _cache:
        _cache[p] = norm(p.read_text(errors="replace")) if p.exists() else None
    return _cache[p]


def atom_ids():
    ids = set()
    for k in ("NY", "NYC", "VA", "US"):
        for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
            ids.add(a["id"])
    return ids


ID_RE = re.compile(r"\b(?:NY|NYC|US|VA):[A-Za-z0-9][^\s,;]*")


def check(review, universe, coverage, ids):
    errs, nq = [], 0
    for f in review["findings"]:
        for e in f["evidence"]:
            nq += 1
            t = src_text(e["source_file"])
            if t is None:
                errs.append(f"{f['id']}: missing source {e['source_file']}")
            elif norm(e["quote"]) not in t:
                errs.append(f"{f['id']}: quote not verbatim in {e['source_file']}: {e['quote'][:70]!r}")
        for i in f["rule_ids"]:
            if i not in ids:
                errs.append(f"{f['id']}: rule id does not exist: {i}")
    for o in review["over_scope"]:
        for i in o["rule_ids"]:
            if i not in ids:
                errs.append(f"over_scope: rule id does not exist: {i}")
    for u in universe:
        nq += 1
        t = src_text(u["source_file"])
        if t is None:
            errs.append(f"{u['id']}: missing source {u['source_file']}")
        elif norm(u["verbatim_quote"]) not in t:
            errs.append(f"{u['id']}: universe quote not verbatim in {u['source_file']}: {u['verbatim_quote'][:70]!r}")
    fids = {f["id"] for f in review["findings"]}
    for c in coverage:
        for i in ID_RE.findall(c["rules_or_finding"]):
            while i.endswith(".") or (i.endswith(")") and i.count(")") > i.count("(")):
                i = i[:-1]
            if i not in ids:
                errs.append(f"coverage {c['universe_id']}: rule id does not exist: {i}")
        for r in re.findall(r"R4A-\d\d", c["rules_or_finding"]):
            if r not in fids:
                errs.append(f"coverage {c['universe_id']}: finding does not exist: {r}")
    return errs, nq


def main():
    review = json.loads((REV / "independent_review_4a.json").read_text())
    universe = json.loads((REV / "review4a_universe.json").read_text())
    coverage = json.loads((REV / "ir4a_coverage.json").read_text())
    ids = atom_ids()
    errs, nq = check(review, universe, coverage, ids)
    nids = sum(len(f["rule_ids"]) for f in review["findings"]) + sum(len(o["rule_ids"]) for o in review["over_scope"])
    print(f"checked {nq} quotes ({sum(len(f['evidence']) for f in review['findings'])} evidence, {len(universe)} universe), "
          f"{nids} finding rule ids, {len(coverage)} coverage rows: {len(errs)} errors")
    for e in errs:
        print("  ", e)
    # self-test: a planted bad quote and a planted bad id must both be caught
    bad = copy.deepcopy(review)
    bad["findings"][0]["evidence"][0]["quote"] = "PLANTED " + bad["findings"][0]["evidence"][0]["quote"]
    bad["findings"][0]["rule_ids"].append("NY:NO-SUCH-RULE-PLANTED")
    badu = copy.deepcopy(universe)
    badu[0]["verbatim_quote"] = badu[0]["verbatim_quote"] + " PLANTED"
    e2, _ = check(bad, badu, coverage, ids)
    caught_q = any("quote not verbatim" in e and "PLANTED" in e for e in e2)
    caught_id = any("NY:NO-SUCH-RULE-PLANTED" in e for e in e2)
    caught_u = any("universe quote not verbatim" in e for e in e2)
    print(f"self-test: planted bad evidence quote caught={caught_q}, planted bad rule id caught={caught_id}, "
          f"planted bad universe quote caught={caught_u}")
    ok = not errs and caught_q and caught_id and caught_u
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
