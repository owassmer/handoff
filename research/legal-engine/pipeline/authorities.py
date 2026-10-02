"""authorities (J5): check that every decision point has a recorded search in every court that binds the customer's
courts.

profile.json courts: [{id, name, binds: [court ids it binds]}]; customer_courts: [court ids where the customer's
claims are heard]. A court binds a customer court when the customer court is reachable through 'binds'.
authorities.json: a list of searches {decision_point, court, query, date, results: [{citation, holding,
later_history, source_file}], ruling}. decision_point is a chain-map point (DP6.3) or a step (DP6, covering its
points). A point that cannot arise in the jurisdiction is listed in profile.json decision_points_not_applicable
[{decision_point, reason}].
Fails when a (point, binding court) pair has no search; a search lacks a field; a result lacks its later history or
its saved source; a search with results has no ruling; or a holding or ruling hedges.
"""
from __future__ import annotations

from . import core

FIELDS = ["decision_point", "court", "query", "date", "results", "ruling"]


def binding_courts(prof):
    courts = {c["id"]: c for c in prof.get("courts", [])}
    targets = set(prof.get("customer_courts", []))

    def reaches(cid, seen=()):
        for b in courts.get(cid, {}).get("binds", []):
            if b in targets or (b not in seen and reaches(b, seen + (cid,))):
                return True
        return False
    return sorted(c for c in courts if reaches(c))


def check(code):
    prof = core.profile(code)
    cm = core.chain_map()
    points = [(d["id"], p["id"]) for d in cm["decision_points"] for p in d["points"]]
    na = {x["decision_point"] for x in prof.get("decision_points_not_applicable", []) if x.get("reason")}
    data = core.read_json(core.jdir(code) / "authorities.json", [])
    searches = data if isinstance(data, list) else data.get("searches", [])
    courts = binding_courts(prof)
    errs = []
    if not prof.get("customer_courts"):
        errs.append("profile.json names no customer_courts")
    if not courts:
        errs.append("no court binds the customer's courts (profile.json courts[].binds)")
    covered = set()
    for i, s in enumerate(searches):
        miss = [k for k in FIELDS if k not in s]
        if miss:
            errs.append(f"search {i}: missing {miss}")
            continue
        for r in s["results"]:
            for k in ("citation", "holding", "later_history", "source_file"):
                if not r.get(k):
                    errs.append(f"search {i} ({s['decision_point']}, {s['court']}): result {r.get('citation')} lacks {k}")
            if r.get("source_file") and not (core.ROOT / r["source_file"]).is_file():
                errs.append(f"search {i}: {r.get('citation')} source not saved: {r['source_file']}")
            m = core.HEDGE.search(str(r.get("holding", "")))
            if m:
                errs.append(f"search {i}: hedging in holding: '{m.group(0)}'")
        if s["results"] and not str(s.get("ruling", "")).strip():
            errs.append(f"search {i} ({s['decision_point']}, {s['court']}): results without a ruling on which prevails")
        m = core.HEDGE.search(str(s.get("ruling", "")))
        if m:
            errs.append(f"search {i}: hedging in ruling: '{m.group(0)}'")
        covered.add((s["decision_point"], s["court"]))
    missing = []
    for step, pt in points:
        if pt in na or step in na:
            continue
        for c in courts:
            if (pt, c) not in covered and (step, c) not in covered:
                missing.append(f"{pt} in {c}")
    return errs, missing, len(searches), courts


def main(code):
    errs, missing, n, courts = check(code)
    print(f"{code} authorities: {n} searches; binding courts {courts}; {len(missing)} (point, court) pairs without a search")
    for m in missing[:40]:
        print("   no search:", m)
    if len(missing) > 40:
        print(f"   ... {len(missing) - 40} more")
    for e in errs[:40]:
        print("  ", e)
    return 1 if errs or missing else 0
