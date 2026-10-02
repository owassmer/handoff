"""IR5A: build review/independent_review_5a.json from ir5a_findings_*.py, ir5a_coverage.py and the saved universe.

Evidence quotes are copied from the universe (already cut mechanically) or cut from sources by anchors (ir5a_lib.cut).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ir5a_lib import ROOT, cut  # noqa: E402
import ir5a_coverage as C  # noqa: E402
import ir5a_findings_1 as F1  # noqa: E402
import ir5a_findings_2 as F2  # noqa: E402

U = json.load(open(ROOT / "review" / "review5a_universe.json"))
UB = {u["id"]: u for u in U}
num = lambda uid: int(uid.split("-")[1])  # noqa: E731
findings = []
item_status = {}
for f in F1.FINDINGS + F2.FINDINGS:
    ev = [{"source_file": UB[u]["source_file"], "quote": UB[u]["verbatim_quote"], "universe_id": u} for u in f["universe"]]
    for src, a, b in f.get("extra", []):
        ev.append({"source_file": src, "quote": cut(src, a, b)})
    findings.append({"id": f["id"], "kind": f["kind"], "severity": f["severity"], "rule_ids": f["rule_ids"], "step": f["step"],
                     "universe_ids": f["universe"], "finding": f["finding"], "correct_rule": f["correct_rule"], "evidence": ev})
    for u in f["universe"]:
        item_status.setdefault(num(u), []).append(f"{f['kind']}:{f['id']}")
coverage = []
missing = []
for u in U:
    n = num(u["id"])
    if n in item_status:
        st = ";".join(item_status[n])
        rules = C.COVERED.get(n, "")
    elif n in C.COVERED:
        st = "no-decision-change" if C.COVERED[n] == "NODEC" else "covered"
        rules = "" if C.COVERED[n] == "NODEC" else C.COVERED[n]
    else:
        st, rules = "UNASSIGNED", ""
        missing.append(u["id"])
    coverage.append({"universe_id": u["id"], "citation": u["citation"], "status": st, "rule_ids": rules.split() if rules and rules != "NODEC" else [],
                     "note": C.NODEC_REASON.get(n, ""), "in_4a": C.MAP4A.get(n, "").split()})
gap_items = [c for c in coverage if c["status"].startswith(("gap", "partial"))]
new_gap_items = [c["universe_id"] for c in gap_items if not c["in_4a"]]
new_findings = [f["id"] for f in findings if all(not C.MAP4A.get(num(u)) for u in f["universe_ids"])]
over_scope = [
 {"rule_ids": ["NYC:RCNY28-1-01", "NYC:RCNY28-1-12(b)-cap", "NYC:RCNY28-1-12(b)-escrow", "NYC:HPD-ESCROW-no-owner-draw", "NYC:HPD-ESCROW-regulatory-agreement"],
  "severity": "minor",
  "reason": "28 RCNY ch. 1 applies to multiple dwellings with a PHFL article VIII city loan; the rule files' own NYC:RCL-26-403(e)(1)(c) states every unit in such a building is rent-controlled while article VIII requires it, and HPD regulatory agreements attach regulated rents. A unit reached by these rules is routed out of the market-rate engine at Step 0, so for a market-rate unit they change no decision; they belong with the controlled/regulated review (defer, do not cite as market-rate law)."},
]
out = {
 "round": "5A (completeness)", "date": "2026-09-30",
 "universe_count": len(U),
 "summary": {
  "findings": len(findings),
  "by_severity": {s: sum(1 for f in findings if f["severity"] == s) for s in ("critical", "major", "minor")},
  "gap_items": len(gap_items), "covered_items": sum(1 for c in coverage if c["status"] == "covered"),
  "no_decision_items": sum(1 for c in coverage if c["status"] == "no-decision-change"),
  "over_scope_groups": len(over_scope)},
 "findings": findings, "over_scope": over_scope, "coverage": coverage,
 "comparison_4a": {
  "universe_4a": 176, "matched_5a_items": sum(1 for c in coverage if c["in_4a"]),
  "only_in_5a": [f"{c['universe_id']} {c['citation']}" for c in coverage if not c["in_4a"]],
  "only_in_4a": [f"{k} {v}" for k, v in C.ONLY4A.items()],
  "new_gap_items_not_in_4a_or_rules": new_gap_items, "new_gaps_count": len(new_gap_items),
  "new_findings_all_items_absent_from_4a": new_findings},
}
(ROOT / "review" / "independent_review_5a.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out["summary"]), "\nunassigned:", missing, "\nnew gap items:", len(new_gap_items), "new findings:", new_findings,
      "\nonly_in_5a:", len(out["comparison_4a"]["only_in_5a"]), "only_in_4a:", len(C.ONLY4A))
