"""Register check: register/check_register.py in strict mode, per jurisdiction.

  [1] Every section of every in-scope unit is listed: a unit's recorded section count equals its sections.jsonl
      rows; every row names a registered instrument and one of its in-scope units; every section has exactly one
      triage row and every triage row a section.
  [2] Every section has a saved text with a SOURCE/RETRIEVED header, or is recorded in instruments.json
      fetch_gaps.section_gaps (and routed 'unfetched').
  [3] Every rule id on a triage row (match_rule_ids, rule_ids) exists in this jurisdiction's family (its layers and
      the layers below it); a 'stated' route carries at least one matched rule id.
  [4] Every embedded Jev record matches a validated current request and pinned build.
      Every set-aside section has compatible evidence producing its route, or a hand reason.
  [5] Every instrument named in this jurisdiction's rule provisions is registered in the family, or listed in
      instruments.json non_code_sources.
  [S] Strict: every section has a decision (review_decision), made by match or by a reviewer; a reviewer decision
      names its batch and agrees with the decisions file.
Self-tests: a planted unclassified section, a planted bad rule id and a planted undecided section must each fail.

check_register.py's check [6] (the rule files unchanged since the register was built) is not a register check here:
rules change by design through J6, and file hashes are recorded and checked at acceptance (J9).
"""
from __future__ import annotations

import collections
import copy

from . import cites, core, route, jev, triage as triage_ops

ROUTES = {"stated", "review_queue", "triaged_no_decision", "triaged_excluded", "unfetched"}


def load(code):
    inst = core.instruments(code)
    d = {"code": code, "profile": core.profile(code), "instruments": inst, "sections": core.sections(code),
         "triage": core.triage(code), "gaps": (inst.get("fetch_gaps") or {}).get("section_gaps", []),
         "family_rules": core.rule_index(core.family(code)), "own_rules": core.load_rules(code).get("atoms", []),
         "family_instruments": {}, "non_code": set(), "decisions": {}}
    for c in core.family(code):
        fi = core.instruments(c)
        for i in fi.get("instruments", []):
            d["family_instruments"][i["id"]] = i
        d["non_code"] |= {n["instrument"] for n in fi.get("non_code_sources", [])}
    ddir = core.jdir(code) / "decisions"
    if ddir.exists():
        for f in sorted(ddir.glob("decisions_*.jsonl")):
            n = f.stem.split("_", 1)[1]
            for r in core.read_jsonl(f):
                d["decisions"][r["section_id"]] = (n, r.get("decision"))
    return d


def check(d, verify_jev=True, strict=True):
    errs = []
    code = d["code"]
    inst = {i["id"]: i for i in d["instruments"].get("instruments", [])}
    secs = {s["section_id"]: s for s in d["sections"]}
    # [1]
    per_unit = collections.Counter((s["instrument"], s["unit"]) for s in d["sections"])
    for iid, i in inst.items():
        for u in i.get("units_in_scope", []):
            n = per_unit.get((iid, u["unit"]), 0)
            if u.get("sections") is not None and n != u["sections"]:
                errs.append(f"[1] {iid} unit '{u['unit']}': TOC lists {u['sections']} sections, sections.jsonl has {n}")
    for s in d["sections"]:
        if s["instrument"] not in inst:
            errs.append(f"[1] {s['section_id']}: instrument {s['instrument']} not in instruments.json")
        elif not any(u["unit"] == s["unit"] for u in inst[s["instrument"]].get("units_in_scope", [])):
            errs.append(f"[1] {s['section_id']}: unit '{s['unit']}' is not an in-scope unit of {s['instrument']}")
    tri = collections.defaultdict(list)
    for r in d["triage"]:
        tri[r["section_id"]].append(r)
    for sid in secs:
        rows = tri.get(sid, [])
        if len(rows) != 1:
            errs.append(f"[1] {sid}: {len(rows)} triage rows (expected exactly 1)")
        elif rows[0].get("route") not in ROUTES:
            errs.append(f"[1] {sid}: route {rows[0].get('route')!r} not allowed")
    for sid in tri:
        if sid not in secs:
            errs.append(f"[1] triage row {sid} has no section")
    # [2]
    gap_ids = {g["section_id"] for g in d["gaps"]}
    for sid, s in secs.items():
        rt = (tri.get(sid) or [{}])[0].get("route")
        if s.get("text_file"):
            p = core.ROOT / s["text_file"]
            if not p.exists():
                errs.append(f"[2] {sid}: text file missing {s['text_file']}")
            elif not core.has_header(p.read_text(errors="ignore")[:800]):
                errs.append(f"[2] {sid}: text file lacks SOURCE/RETRIEVED header")
        elif rt != "unfetched" or sid not in gap_ids:
            errs.append(f"[2] {sid}: no text and not recorded as unfetched in instruments.json fetch_gaps")
    # [3]
    for sid, rows in tri.items():
        for r in rows:
            for a in list(r.get("match_rule_ids") or []) + list(r.get("rule_ids") or []):
                if a not in d["family_rules"]:
                    errs.append(f"[3] {sid}: rule id {a} does not exist in the rule files")
            if r.get("route") == "stated" and not r.get("match_rule_ids"):
                errs.append(f"[3] {sid}: stated without a rule id")
    # [4]
    rv = core.routing()
    if verify_jev:
        matched = {sid: (tri.get(sid) or [{}])[0].get("match_rule_ids") for sid in secs}
        prior = {sid: (tri.get(sid) or [{}])[0].get("prior_review_citations") for sid in secs}
        regime = (d["profile"].get("aperture") or {}).get("regime_units", [])
        ctx = route.contexts(secs, matched, regime, prior)
        names = {iid: i.get("name", iid) for iid, i in d["family_instruments"].items()}
        valid = jev.cached_answers(code, [(sid, sec, d["profile"], names) for sid, sec in secs.items()])
    for sid, rows in tri.items():
        for r in rows:
            if verify_jev and r.get("jev"):
                expected = triage_ops.jev_subset(valid.get(sid))
                if expected is None or r["jev"] != expected:
                    errs.append(f"[4] {sid}: embedded Jev record is not current validated cache evidence")
            if r.get("route") not in ("triaged_no_decision", "triaged_excluded") or r.get("hand_reason"):
                continue
            j = r.get("jev")
            if not j or not j.get("cache_key"):
                errs.append(f"[4] {sid}: set aside without a Jev record or hand reason")
                continue
            if verify_jev:
                j = triage_ops.jev_subset(valid.get(sid))
                if j is None:
                    errs.append(f"[4] {sid}: no compatible validated Jev cache answer")
                    continue
                v = r.get("routing_version")
                if v not in rv["versions"]:
                    errs.append(f"[4] {sid}: unknown routing version {v}")
                elif sid in secs:
                    st2, _ = route.route(secs[sid], j, rv["versions"][v], ctx[sid])
                    if st2 != r.get("route"):
                        errs.append(f"[4] {sid}: route {r.get('route')} but routing {v} on the stored answers gives {st2}")
    # [5]
    eng = cites.engine()
    for a in d["own_rules"]:
        aid = a.get("id")
        cl = eng.parse(a.get("provision", "")) or eng.parse(a.get("instrument", ""))
        if not cl:
            if a.get("instrument") not in d["non_code"]:
                errs.append(f"[5] rule {aid}: provision cites no code section and instrument not in non_code_sources")
            continue
        for k, n in cl:
            num = n.split(":")[1] if n.startswith("RANGE:") else n
            iid = eng.cite_instrument(k, num)
            if not iid or iid not in d["family_instruments"]:
                errs.append(f"[5] rule {aid}: provision cites {k} {n} whose instrument ({iid}) is not registered")
    # [S]
    if strict:
        for sid in secs:
            r = (tri.get(sid) or [{}])[0]
            dec = r.get("review_decision")
            if dec not in core.DECISIONS:
                errs.append(f"[S] {sid}: no decision")
                continue
            if r.get("decided_by") == "reviewer":
                got = d["decisions"].get(sid)
                if r.get("review_batch") is None or not got:
                    errs.append(f"[S] {sid}: reviewer decision without a decisions file row")
                elif got[1] != dec:
                    errs.append(f"[S] {sid}: triage says {dec}, decisions_{got[0]}.jsonl says {got[1]}")
            elif r.get("decided_by") != "match":
                errs.append(f"[S] {sid}: decided_by {r.get('decided_by')!r} (expected match or reviewer)")
    return errs


def counts(d):
    c = collections.Counter(r.get("route") for r in d["triage"])
    dec = collections.Counter(r.get("review_decision") or "undecided" for r in d["triage"])
    return c, dec


def self_test(d):
    """Plant defects into a copy of the loaded data; each must be caught."""
    ok = {}
    t1 = copy.deepcopy(d)
    u = next((i for i in t1["instruments"].get("instruments", []) if i.get("units_in_scope")), None)
    if u is None:
        t1["instruments"] = {"instruments": [{"id": f"{d['code']}:X", "units_in_scope": [{"unit": "u", "sections": 0}],
                                              "units_out": []}]}
        u = t1["instruments"]["instruments"][0]
    t1["sections"].append({"section_id": f"{d['code']}:PLANTED 0-0", "instrument": u["id"],
                           "unit": u["units_in_scope"][0]["unit"], "heading": "planted unclassified section",
                           "text_file": None, "chars": 0, "repealed": False})
    ok["unclassified section"] = any("PLANTED 0-0" in e for e in check(t1, verify_jev=False))
    t2 = copy.deepcopy(d)
    if not t2["triage"]:
        t2["triage"].append({"section_id": "planted", "route": "stated", "match_rule_ids": []})
    t2["triage"][0]["match_rule_ids"] = list(t2["triage"][0].get("match_rule_ids") or []) + [f"{d['code']}:PLANTED-NOT-A-RULE"]
    ok["bad rule id"] = any("PLANTED-NOT-A-RULE" in e for e in check(t2, verify_jev=False))
    t3 = copy.deepcopy(d)
    if t3["triage"]:
        t3["triage"][0]["review_decision"] = None
        sid = t3["triage"][0]["section_id"]
        ok["undecided section"] = any(e.startswith("[S]") and sid in e for e in check(t3, verify_jev=False))
    else:
        ok["undecided section"] = any("[S]" in e for e in check(t1, verify_jev=False))
    return ok


def main(code, verify_jev=True, quiet=False):
    d = load(code)
    errs = check(d, verify_jev)
    c, dec = counts(d)
    if not quiet:
        print(f"{code} register: {len(d['sections'])} sections; routes {dict(c)}; decisions {dict(dec)}")
    ok = self_test(d)
    print(f"{code} register self-test: " + ", ".join(f"{k} {'caught' if v else 'NOT CAUGHT'}" for k, v in ok.items()))
    for e in errs[:60]:
        print("  " + e)
    if len(errs) > 60:
        print(f"  ... {len(errs) - 60} more")
    return errs, all(ok.values())
