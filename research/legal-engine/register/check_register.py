"""Completeness check for the Stage A source register. Exit 0 only if every check passes AND both planted-defect
self-tests are caught.

Checks:
 1. Every section of every in-scope unit has a status: the sections enumerated for each unit in instruments.json
    (units_in_scope[].sections) equal the sections.jsonl rows for that unit, and every sections.jsonl row has exactly
    one triage.jsonl row with a status in {stated, review_queue, triaged_no_decision, triaged_excluded, unfetched}.
 2. Every in-scope section has a saved text with a SOURCE and RETRIEVED header, or is 'unfetched' and listed in
    fetch_gaps.json.
 3. Every atom id on a triage row exists in the rule files, and 'stated' rows carry at least one atom id.
 4. Every triaged status carries a Jev record (cache file present, returned model carries 'jev-1.13', routing
    recomputed from the stored answers gives the same status) or a hand reason.
 5. Every instrument named in any atom provision is in instruments.json: each citation parsed from an atom's
    provision (or, where the provision names no section, from its instrument field) maps to a registered instrument
    id; an atom citing no code section at all has its instrument listed in instruments.json non_code_sources.
 6. The rule files are unchanged since the register was built (sha256 in instruments.json).
Prints counts per status and per instrument.
Self-tests: a planted unclassified section and a planted bad atom id must each make the check fail.

Strict mode (the default; --no-strict skips it) adds check 7: every section of every in-scope unit carries a reviewer
decision (review_decision in stated | partial | new_rule | no_decision | excluded_regime, and review_batch). A numbered
batch must hold that section with the same decision in register/work/decisions_<n>.jsonl; review_batch 'match' is allowed
only for a section the register marked 'stated' by citation match, whose rules passed review rounds 1-5; a stated,
partial or new_rule decision must name at least one atom (check 3 confirms each exists in the rule files). A third
self-test plants a section with no reviewer decision, which strict mode must catch.
"""
import collections
import copy
import hashlib
import json
import pathlib
import sys

REG = pathlib.Path(__file__).resolve().parent
ROOT = REG.parent
sys.path.insert(0, str(REG / "tools"))
import calibrate  # noqa: E402
import cites  # noqa: E402
import route  # noqa: E402

STATUSES = {"stated", "review_queue", "triaged_no_decision", "triaged_excluded", "unfetched"}


def load():
    d = {
        "instruments": json.loads((REG / "instruments.json").read_text()),
        "sections": [json.loads(l) for l in (REG / "sections.jsonl").read_text().splitlines() if l.strip()],
        "triage": [json.loads(l) for l in (REG / "triage.jsonl").read_text().splitlines() if l.strip()],
        "gaps": json.loads((REG / "fetch_gaps.json").read_text()),
        "routing": json.loads((REG / "routing.json").read_text()),
        "match": json.loads((REG / "match.json").read_text()),
        "atoms": {},
    }
    for f in ("NY", "NYC", "US"):
        for a in json.loads((ROOT / "stage-a" / f"{f}.json").read_text())["atoms"]:
            d["atoms"][a["id"]] = a
    return d


def check(d, verify_jev=True):
    errs = []
    inst = {i["id"]: i for i in d["instruments"]["instruments"]}
    secs = {s["section_id"]: s for s in d["sections"]}
    # 1. enumeration and statuses
    per_unit = collections.Counter((s["instrument"], s["unit"]) for s in d["sections"])
    for iid, i in inst.items():
        for u in i["units_in_scope"]:
            n = per_unit.get((iid, u["unit"]), 0)
            if u.get("sections") is not None and n != u["sections"]:
                errs.append(f"[1] {iid} unit '{u['unit']}': TOC lists {u['sections']} sections, sections.jsonl has {n}")
    for s in d["sections"]:
        if s["instrument"] not in inst:
            errs.append(f"[1] {s['section_id']}: instrument {s['instrument']} not in instruments.json")
        elif not any(u["unit"] == s["unit"] for u in inst[s["instrument"]]["units_in_scope"]):
            errs.append(f"[1] {s['section_id']}: unit '{s['unit']}' is not an in-scope unit of {s['instrument']}")
    tri = collections.defaultdict(list)
    for r in d["triage"]:
        tri[r["section_id"]].append(r)
    for sid in secs:
        rows = tri.get(sid, [])
        if len(rows) != 1:
            errs.append(f"[1] {sid}: {len(rows)} triage rows (expected exactly 1)")
        elif rows[0].get("status") not in STATUSES:
            errs.append(f"[1] {sid}: status {rows[0].get('status')!r} not allowed")
    for sid in tri:
        if sid not in secs:
            errs.append(f"[1] triage row {sid} has no section")
    # 2. texts
    gap_ids = {g["section_id"] for g in d["gaps"]["section_gaps"]}
    for sid, s in secs.items():
        status = (tri.get(sid) or [{}])[0].get("status")
        if s.get("text_file"):
            p = REG / s["text_file"]
            if not p.exists():
                errs.append(f"[2] {sid}: text file missing {s['text_file']}")
            else:
                head = p.read_text()[:600]
                if not head.startswith("SOURCE:") or "RETRIEVED:" not in head:
                    errs.append(f"[2] {sid}: text file lacks SOURCE/RETRIEVED header")
        elif status != "unfetched" or sid not in gap_ids:
            errs.append(f"[2] {sid}: no text and not recorded as unfetched in fetch_gaps.json")
    # 3. atom ids
    for sid, rows in tri.items():
        for r in rows:
            for a in r.get("atom_ids") or []:
                if a not in d["atoms"]:
                    errs.append(f"[3] {sid}: atom id {a} does not exist in the rule files")
            if r.get("status") == "stated" and not r.get("atom_ids"):
                errs.append(f"[3] {sid}: stated without an atom id")
    # 4. Jev records / hand reasons
    rv = d["routing"]
    m = d["match"]["sections"]
    if verify_jev:
        cfg_by_v = rv["versions"]
        ctxs = {}
        for v, cfg in cfg_by_v.items():
            ctxs[v] = calibrate.contexts(secs, m, cfg)
    for sid, rows in tri.items():
        for r in rows:
            st = r.get("status")
            if st in ("triaged_no_decision", "triaged_excluded"):
                if r.get("hand_reason"):
                    continue
                j = r.get("jev")
                if not j or not j.get("cache_key"):
                    errs.append(f"[4] {sid}: triaged without a Jev record or hand reason")
                    continue
                if "jev-1.13" not in str(j.get("returned_model")):
                    errs.append(f"[4] {sid}: Jev record model {j.get('returned_model')!r} lacks jev-1.13")
                if verify_jev:
                    if not (REG / "jev_cache" / f"{j['cache_key']}.json").exists():
                        errs.append(f"[4] {sid}: Jev cache file missing")
                    v = r.get("routing_version")
                    if v not in rv["versions"]:
                        errs.append(f"[4] {sid}: unknown routing version {v}")
                    elif sid in secs:
                        rec = {"role": j["role"], "role_probabilities": j["role_probabilities"],
                               "role_confidence": j["role_confidence"], "chain_duty": j["chain_duty"]}
                        st2, _ = route.route(secs[sid], rec, rv["versions"][v], ctxs[v][sid])
                        if st2 != st:
                            errs.append(f"[4] {sid}: status {st} but routing {v} on the stored answers gives {st2}")
    # 5. instruments named in atom provisions
    non_code = {n["instrument"] for n in d["instruments"].get("non_code_sources", [])}
    for aid, a in d["atoms"].items():
        cl = cites.parse(a.get("provision", ""))
        if not cl:
            # provision names no section (e.g. "'promptly refund'"): the instrument field names the law instead
            cl = cites.parse(a.get("instrument", ""))
        if not cl:
            if a.get("instrument") not in non_code and not (
                    "comment" in a.get("provision", "").lower() and "1006" in a.get("instrument", "")):
                errs.append(f"[5] atom {aid}: provision cites no code section and instrument not in non_code_sources")
            continue
        for k, n in cl:
            num = n.split(":")[1] if n.startswith("RANGE:") else n
            iid = cites.cite_instrument(k, num)
            if not iid or iid not in inst:
                errs.append(f"[5] atom {aid}: provision cites {k} {n} whose instrument ({iid}) is not in instruments.json")
    # 6. rule files unchanged
    for f, h in d["instruments"].get("rule_file_sha256", {}).items():
        if hashlib.sha256((ROOT / f).read_bytes()).hexdigest() != h:
            errs.append(f"[6] {f} changed since the register was built")
    return errs


REVIEW_DECISIONS = {"stated", "partial", "new_rule", "no_decision", "excluded_regime"}


def load_decisions():
    out = {}
    for p in sorted((REG / "work").glob("decisions_*.jsonl")):
        n = int(p.stem.split("_")[1])
        for line in p.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                out[(n, r["section_id"])] = r["decision"]
    return out


def check_strict(d, decisions=None):
    """Check 7: every section has a reviewer decision consistent with the decisions files."""
    decisions = load_decisions() if decisions is None else decisions
    errs = []
    tri = {r["section_id"]: r for r in d["triage"]}
    for s in d["sections"]:
        sid = s["section_id"]
        r = tri.get(sid)
        if r is None:
            continue  # check 1 reports it
        dec, batch = r.get("review_decision"), r.get("review_batch")
        if dec not in REVIEW_DECISIONS or batch is None:
            errs.append(f"[7] {sid}: no reviewer decision")
            continue
        if batch == "match":
            if r.get("status") != "stated" or not r.get("atom_ids"):
                errs.append(f"[7] {sid}: review_batch 'match' without a citation-matched stated rule")
        elif decisions.get((batch, sid)) != dec:
            errs.append(f"[7] {sid}: review_decision {dec} not found in decisions_{batch}.jsonl")
        if dec in ("stated", "partial", "new_rule") and not r.get("atom_ids"):
            errs.append(f"[7] {sid}: {dec} names no atom")
    return errs


def report(d):
    c = collections.Counter(r["status"] for r in d["triage"])
    print("Status counts:")
    for k in ("stated", "review_queue", "triaged_no_decision", "triaged_excluded", "unfetched"):
        print(f"  {k:22s} {c.get(k, 0)}")
    print(f"  {'total':22s} {sum(c.values())}")
    per = collections.defaultdict(collections.Counter)
    for r in d["triage"]:
        per[r["instrument"]][r["status"]] += 1
    print("\nPer instrument (sections: stated / review_queue / triaged_no_decision / triaged_excluded / unfetched):")
    ids = [i["id"] for i in d["instruments"]["instruments"]]
    for iid in ids:
        p = per.get(iid, collections.Counter())
        units = next(i for i in d["instruments"]["instruments"] if i["id"] == iid)
        print(f"  {iid:22s} {sum(p.values()):5d}: {p['stated']:4d} / {p['review_queue']:4d} / {p['triaged_no_decision']:4d} / "
              f"{p['triaged_excluded']:3d} / {p['unfetched']:2d}   units in {len(units['units_in_scope'])}, out {len(units['units_out'])}")


def main():
    strict = "--no-strict" not in sys.argv
    d = load()
    errs = check(d)
    decisions = load_decisions()
    if strict:
        errs += check_strict(d, decisions)
    report(d)
    if strict:
        c = collections.Counter(r.get("review_decision") for r in d["triage"])
        b = collections.Counter("match" if r.get("review_batch") == "match" else "batches 1-9" for r in d["triage"])
        print("\nReviewer decisions (strict): " + ", ".join(f"{k} {v}" for k, v in sorted(c.items(), key=str)) +
              "; " + ", ".join(f"{k} {v}" for k, v in sorted(b.items())))
    print()
    # self-tests
    t1 = copy.deepcopy(d)
    u = next(i for i in t1["instruments"]["instruments"] if i["units_in_scope"])
    t1["sections"].append({"section_id": "NY:PLANTED 0-0", "instrument": u["id"], "unit": u["units_in_scope"][0]["unit"],
                           "heading": "planted unclassified section", "text_file": None, "chars": 0, "repealed": False})
    e1 = check(t1, verify_jev=False)
    t2 = copy.deepcopy(d)
    row = next(r for r in t2["triage"] if r["status"] == "stated")
    row["atom_ids"] = row["atom_ids"] + ["NY:PLANTED-NOT-AN-ATOM"]
    e2 = check(t2, verify_jev=False)
    ok1 = any("NY:PLANTED 0-0" in e for e in e1)
    ok2 = any("NY:PLANTED-NOT-AN-ATOM" in e for e in e2)
    t3 = copy.deepcopy(d)
    u3 = next(i for i in t3["instruments"]["instruments"] if i["units_in_scope"])
    t3["sections"].append({"section_id": "NY:PLANTED-UNDECIDED 0-1", "instrument": u3["id"],
                           "unit": u3["units_in_scope"][0]["unit"], "heading": "planted undecided section",
                           "text_file": None, "chars": 0, "repealed": False})
    t3["triage"].append({"section_id": "NY:PLANTED-UNDECIDED 0-1", "instrument": u3["id"],
                         "unit": u3["units_in_scope"][0]["unit"], "status": "review_queue", "atom_ids": []})
    e3 = check_strict(t3, decisions)
    ok3 = any("NY:PLANTED-UNDECIDED 0-1" in e and "no reviewer decision" in e for e in e3)
    print(f"Self-test planted unclassified section: {'caught' if ok1 else 'NOT CAUGHT'} "
          f"({sum('PLANTED 0-0' in e for e in e1)} errors raised)")
    print(f"Self-test planted bad atom id:         {'caught' if ok2 else 'NOT CAUGHT'} "
          f"({sum('PLANTED-NOT-AN-ATOM' in e for e in e2)} errors raised)")
    print(f"Self-test planted undecided section:   {'caught' if ok3 else 'NOT CAUGHT'} (strict check 7)")
    if errs:
        print(f"\nFAIL: {len(errs)} problems")
        for e in errs[:60]:
            print("  " + e)
    if errs or not (ok1 and ok2 and ok3):
        sys.exit(1)
    print("\nPASS: every section of every in-scope unit has a status" + (" and a reviewer decision" if strict else "") +
          "; every atom id named exists; every triaged section carries a Jev record or hand reason; every instrument "
          "named in an atom provision is registered." + (" (strict)" if strict else " (not strict)"))


if __name__ == "__main__":
    main()
