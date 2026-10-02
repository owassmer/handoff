"""export-data: build pipeline/data/ from a read-only snapshot of the NY register.

  crosswalk.json      every NY, NYC and US instrument and unit in register/instruments.json with its chain-map
                      function ids (pipeline/crosswalk_rules.py), in or out of scope, with out reasons.
  gold_labels.jsonl   one row per register section: function ids, decision (reviewer decision from
                      register/work/decisions_<n>.jsonl (every batch, 1-9 at export), else 'stated' by match), deciding yes/no, Jev scores.
  gold_negatives.jsonl  the register's hand-checked calibration negatives (register/calibration_negatives.json),
                      each with its reason and the reviewer's later decision.
  SNAPSHOT.md         when the snapshot was taken and the sha256 of every file read.
The register files are copied first (the snapshot) and only the copies are read, so a concurrent writer cannot
produce a mixed state. Nothing under register/ is written.
"""
from __future__ import annotations

import collections
import pathlib
import re
import shutil
import tempfile

from . import core, crosswalk_rules as CW

FILES = ["register/instruments.json", "register/sections.jsonl", "register/triage.jsonl"]


def batch_numbers(root):
    w = pathlib.Path(root) / "register" / "work"
    return sorted(int(p.stem.split("_")[1]) for p in w.glob("decisions_*.jsonl")) if w.exists() else []


def snapshot(src_root, dst):
    src_root, dst = pathlib.Path(src_root), pathlib.Path(dst)
    nums = batch_numbers(src_root)
    files = FILES + ["register/calibration_negatives.json"] + [f"register/work/decisions_{n}.jsonl" for n in nums] + \
        [f"register/work/batch_{n}.json" for n in nums]
    manifest = {}
    taken = core.now()
    for f in files:
        s = src_root / f
        if not s.exists():
            continue
        d = dst / f
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        manifest[f] = {"sha256": core.sha256_file(d), "modified": core.datetime.datetime.fromtimestamp(
            s.stat().st_mtime, core.datetime.timezone.utc).replace(microsecond=0).isoformat()}
    return taken, manifest


def unit_functions(iid, label, out=False):
    rules = (CW.OUT_UNITS if out else CW.UNITS).get(iid, [])
    for pat, fns in rules:
        if re.search(pat, label):
            return list(fns)
    return [] if out else list(CW.INSTRUMENT.get(iid, []))


def crosswalk(inst_doc):
    out = []
    for i in inst_doc["instruments"]:
        units = []
        for u in i["units_in_scope"]:
            units.append({"unit": u["unit"], "heading": u["heading"], "scope": "in", "sections": u.get("sections"),
                          "functions": unit_functions(i["id"], f"{u['unit']} | {u['heading']}")})
        for u in i["units_out"]:
            units.append({"unit": u["unit"], "heading": u["heading"], "scope": "out", "reason": u["reason"],
                          "functions": unit_functions(i["id"], f"{u['unit']} | {u['heading']}", out=True)})
        fns = []
        for u in units:
            for f in u["functions"]:
                if f not in fns:
                    fns.append(f)
        out.append({"id": i["id"], "jurisdiction": i["jurisdiction"], "name": i["name"], "level": i["level"],
                    "functions": fns or list(CW.INSTRUMENT.get(i["id"], [])), "units": units})
    return out


def gold(snap, cw):
    secs = core.read_jsonl(snap / "register/sections.jsonl")
    tri = {r["section_id"]: r for r in core.read_jsonl(snap / "register/triage.jsonl")}
    dec = {}
    for n in batch_numbers(snap):
        for r in core.read_jsonl(snap / f"register/work/decisions_{n}.jsonl"):
            dec[r["section_id"]] = (n, r)
    ufn = {(i["id"], u["unit"]): u["functions"] for i in cw for u in i["units"] if u["scope"] == "in"}
    rows = []
    for s in secs:
        sid = s["section_id"]
        t = tri.get(sid, {})
        j = t.get("jev") or {}
        if sid in dec:
            n, r = dec[sid]
            decision, by, batch, ids, reviewer = r["decision"], "reviewer", n, list(r.get("atom_ids") or []) + \
                [p["id"] for p in r.get("proposed") or []], r.get("reviewer")
        elif t.get("status") == "stated":
            decision, by, batch, ids, reviewer = "stated", "match", None, list(t.get("atom_ids") or []), None
        else:
            decision, by, batch, ids, reviewer = None, None, None, [], None
        code = core.code_of(sid)
        rows.append({"section_id": sid, "jurisdiction": code, "instrument": s["instrument"], "unit": s["unit"],
                     "heading": s["heading"], "chars": s["chars"],
                     "functions": ufn.get((s["instrument"], s["unit"]), list(CW.INSTRUMENT.get(s["instrument"], []))),
                     "decision": decision, "decided_by": by, "deciding": None if decision is None else decision in core.DECIDING,
                     "review_batch": batch, "reviewer": reviewer, "rule_ids": ids, "legacy_route": t.get("status"),
                     "jev": None if not j else {"role": j.get("role"), "p_decides": (j.get("role_probabilities") or {}).get("DECIDES"),
                                                "chain_duty": j.get("chain_duty"), "role_confidence": j.get("role_confidence"),
                                                "model": j.get("returned_model"), "registry_version": j.get("registry_version"),
                                                "cache_key": j.get("cache_key"), "created_at": j.get("created_at"),
                                                "historical_only": True, "source": "register/triage.jsonl"},
                     "text_file": f"jurisdictions/{code}/texts/{s['text_file'][len('texts/'):]}" if s.get("text_file") else None,
                     "legacy_text_file": f"register/{s['text_file']}" if s.get("text_file") else None})
    return rows


def main(src=None, out=None):
    src = pathlib.Path(src or core.ROOT)
    out = pathlib.Path(out or core.PKG / "data")
    with tempfile.TemporaryDirectory() as td:
        snap = pathlib.Path(td)
        taken, manifest = snapshot(src, snap)
        if "register/instruments.json" not in manifest:
            raise core.PipelineError(f"no register/instruments.json under {src}")
        cw = crosswalk(core.read_json(snap / "register/instruments.json"))
        rows = gold(snap, cw)
    fn_ids = {f["id"] for f in core.chain_map()["functions"]}
    bad = sorted({f for i in cw for u in i["units"] for f in u["functions"]} - fn_ids)
    if bad:
        raise core.PipelineError(f"crosswalk names functions not in the chain map: {bad}")
    cov = collections.defaultdict(set)
    for i in cw:
        for u in i["units"]:
            if u["scope"] == "in":
                cov[i["jurisdiction"]] |= set(u["functions"])
    core.write_json(out / "crosswalk.json", {
        "snapshot_taken": taken, "chain_map_version": core.chain_map()["version"],
        "note": "Function ids are chain-map ids (pipeline/chain_map.json). Built by `python3 -m pipeline export-data` from pipeline/crosswalk_rules.py.",
        "coverage": {k: sorted(v) for k, v in sorted(cov.items())},
        "functions_without_instrument": {k: sorted(fn_ids - v) for k, v in sorted(cov.items())},
        "instruments": cw})
    core.write_jsonl(out / "gold_labels.jsonl", rows)
    by = {r["section_id"]: r for r in rows}
    negs = []
    for n in core.read_json(src / "register/calibration_negatives.json", {"negatives": []})["negatives"]:
        g = by.get(n["section_id"])
        if g:
            keep = ("section_id", "jurisdiction", "instrument", "unit", "heading", "chars", "functions", "text_file",
                    "legacy_text_file")
            negs.append(dict({k: g[k] for k in keep}, reason=n.get("reason"), reviewer_decision=g["decision"]))
    core.write_jsonl(out / "gold_negatives.jsonl", negs)
    c = collections.Counter((r["jurisdiction"], r["decision"]) for r in rows)
    lines = ["# pipeline/data snapshot", "",
             f"Snapshot taken {taken} (UTC) from {src}/register. Files read (copies), with sha256 and last-modified time:", ""]
    lines += [f"- `{f}` {m['sha256']} (modified {m['modified']})" for f, m in sorted(manifest.items())]
    lines += ["", "Gold labels by jurisdiction and decision:", ""]
    lines += [f"- {k[0]} {k[1] or 'undecided'}: {v}" for k, v in sorted(c.items(), key=lambda x: (x[0][0], str(x[0][1])))]
    lines += ["", "deciding = decision in stated, partial, new_rule. The decisions are the reviewers' (every batch in register/work) or, for "
              "sections a rule already cited, 'stated' by the register's match (decided_by 'match'). Jev scores are historical observations with their recorded original registry; current compatibility is not asserted.",
              "Calibration (`python3 -m pipeline calibrate CODE`) takes the deciding rows whose functions overlap the "
              "jurisdiction's instruments as gold positives; text_file is the imported path, legacy_text_file the "
              "register path (read when the jurisdiction folders are not imported).", ""]
    (out / "SNAPSHOT.md").write_text("\n".join(lines))
    print(f"export-data: snapshot {taken}; {len(cw)} instruments, {sum(len(i['units']) for i in cw)} units in "
          f"crosswalk.json; {len(rows)} gold labels ({sum(1 for r in rows if r['deciding'])} deciding, "
          f"{sum(1 for r in rows if r['deciding'] is False)} not deciding, {sum(1 for r in rows if r['decision'] is None)} undecided); "
          f"{len(negs)} gold negatives")
    return 0
