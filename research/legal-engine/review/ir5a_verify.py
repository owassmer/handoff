"""IR5A verification.

Checks: (1) every universe verbatim_quote occurs (whitespace-normalized) in its source_file; (2) every finding evidence
quote occurs in its source_file; (3) every rule id cited in findings, coverage and over_scope exists in stage-a NY/NYC/US;
(4) no banned hedge phrase in findings or the report; (5) self-test: a planted altered quote and a planted bad rule id
must both be caught. Exit 1 on any failure.
"""
import copy
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANNED = ["consult counsel", "unsettled", "arguably", "cautious position", "in practice", "typically", "persuasive only"]


def norm(s):
    s = s.replace(" ", " ").replace("­", "").replace("​", "")
    return re.sub(r"\s+", " ", s).strip()


_cache = {}


def src(p):
    if p not in _cache:
        _cache[p] = norm((ROOT / p).read_text(errors="replace"))
    return _cache[p]


ATOMS = set()
for k in ("NY", "NYC", "US"):
    ATOMS |= {a["id"] for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]}


def check(universe, review, report_text):
    errs = []
    for u in universe:
        if norm(u["verbatim_quote"]) not in src(u["source_file"]):
            errs.append(f"universe quote not verbatim: {u['id']} in {u['source_file']}")
    for f in review["findings"]:
        for e in f["evidence"]:
            if norm(e["quote"]) not in src(e["source_file"]):
                errs.append(f"evidence quote not verbatim: {f['id']} in {e['source_file']}")
        for r in f["rule_ids"]:
            if r not in ATOMS:
                errs.append(f"unknown rule id in {f['id']}: {r}")
        blob = (f["finding"] + " " + f["correct_rule"]).lower()
        for b in BANNED:
            if b in blob:
                errs.append(f"banned phrase '{b}' in {f['id']}")
    for c in review["coverage"]:
        for r in c["rule_ids"]:
            if r not in ATOMS:
                errs.append(f"unknown rule id in coverage {c['universe_id']}: {r}")
    for o in review["over_scope"]:
        for r in o["rule_ids"]:
            if r not in ATOMS:
                errs.append(f"unknown rule id in over_scope: {r}")
    low = report_text.lower()
    for b in BANNED:
        if b in low:
            errs.append(f"banned phrase '{b}' in report")
    for r in set(re.findall(r"`((?:NY|NYC|US):[^`\s]+)`", report_text)):
        if r not in ATOMS:
            errs.append(f"unknown rule id in report: {r}")
    return errs


universe = json.loads((ROOT / "review/review5a_universe.json").read_text())
review = json.loads((ROOT / "review/independent_review_5a.json").read_text())
rp = ROOT / "review/INDEPENDENT_REVIEW_5A.md"
report = rp.read_text() if rp.exists() else ""

# self-test
bad_u = copy.deepcopy(universe)
bad_u[0]["verbatim_quote"] = bad_u[0]["verbatim_quote"].replace("dwelling", "dwellinq", 1)
bad_r = copy.deepcopy(review)
bad_r["findings"][0]["rule_ids"] = bad_r["findings"][0]["rule_ids"] + ["NY:NO-SUCH-RULE"]
bad_r["findings"][1]["evidence"][0]["quote"] += " planted words"
st = check(bad_u, bad_r, report)
caught = (any("universe quote not verbatim: " + universe[0]["id"] in e for e in st)
          and any("NY:NO-SUCH-RULE" in e for e in st)
          and any("evidence quote not verbatim: " + review["findings"][1]["id"] in e for e in st))
print("self-test (planted bad quote, bad evidence, bad id caught):", "PASS" if caught else "FAIL")

errs = check(universe, review, report)
n_ev = sum(len(f["evidence"]) for f in review["findings"])
print(f"universe quotes: {len(universe)}; findings: {len(review['findings'])}; evidence quotes: {n_ev}; errors: {len(errs)}")
for e in errs:
    print("  ", e)
sys.exit(0 if caught and not errs else 1)
