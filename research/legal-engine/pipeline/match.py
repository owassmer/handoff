"""match (J3): mark the sections already stated by a rule in this layer or a parent layer. Code only.

A rule states a section when its provision cites the section (pipeline/cites.py, the jurisdiction's citation
config), when its source_file is the section's saved text, or when its source_file name parses as a citation of the
section. Writes match.json ({matcher, sections: {id: [rule ids]}, rule_citations, unmatched, unregistered}) and the
match fields of triage.jsonl. A section matched before and no longer matched loses its match decision.
Deterministic: the same inputs give byte-identical outputs.
"""
from __future__ import annotations

import re

from . import cites, core

MATCHER = "pipeline.match v1"


def index(secs, eng):
    idx = {}
    for s in secs:
        if s.get("source_unit_kind") == "document":
            raise core.PipelineError(f"{s['section_id']}: enumerate the document's internal sections before matching")
        idx.setdefault(eng.section_key(s["section_id"]), []).append(s["section_id"])
    return idx


def resolve(key, num, idx):
    if num.startswith("RANGE:"):
        _, a, b = num.split(":")
        a, b = int(a), int(b)
        out = []
        for (k, n), ids in idx.items():
            m = re.match(r"(\d+)", n)
            if k == key and m and a <= int(m.group(1)) <= b:
                out.extend(ids)
        return out
    return idx.get((key, num), [])


def compute(code):
    eng = cites.engine()
    secs = core.sections(code)
    idx = index(secs, eng)
    by_file = {}
    for s in secs:
        if s.get("text_file"):
            by_file.setdefault(s["text_file"], []).append(s["section_id"])
    res = {s["section_id"]: [] for s in secs}
    rule_cites, unmatched, unregistered = {}, [], []
    for layer in core.layers(code):
        for a in core.load_rules(layer).get("atoms", []):
            cl = [(k, n, "provision") for k, n in eng.parse(a.get("provision", ""))]
            cl += [(k, n, "provision") for k, n in eng.provision_extra(a.get("provision", ""), a.get("instrument", ""))]
            sf = eng.source_file_cite(a.get("source_file"))
            if sf:
                cl.append((sf[0], sf[1], "source_file"))
            rows = []
            for k, n, via in cl:
                inst = eng.cite_instrument(k, n.split(":")[1] if n.startswith("RANGE:") else n)
                hits = resolve(k, n, idx)
                for h in hits:
                    if a["id"] not in res[h]:
                        res[h].append(a["id"])
                rows.append({"key": k, "number": n, "via": via, "instrument": inst, "section_ids": hits})
                if not hits and inst and core.code_of(inst) == code:
                    unmatched.append({"rule_id": a["id"], "key": k, "number": n, "via": via, "instrument": inst})
                elif not hits and not inst:
                    unregistered.append({"rule_id": a["id"], "key": k, "number": n, "via": via})
            for h in by_file.get(a.get("source_file"), []):
                if a["id"] not in res[h]:
                    res[h].append(a["id"])
                rows.append({"key": None, "number": None, "via": "text_file", "instrument": None, "section_ids": [h]})
            if rows:
                rule_cites[a["id"]] = rows
    return {"matcher": MATCHER, "jurisdiction": code, "layers": core.layers(code), "sections": res,
            "rule_citations": rule_cites, "unmatched": unmatched, "unregistered": unregistered}


def empty_row(s):
    return {"section_id": s["section_id"], "instrument": s["instrument"], "unit": s["unit"], "heading": s.get("heading"),
            "match_rule_ids": [], "route": None, "route_reason": None, "routing_version": None, "tier": None,
            "jev": None, "hand_reason": None, "prior_review_citations": [], "review_decision": None,
            "review_batch": None, "decided_by": None, "rule_ids": []}


def apply_match(code, m):
    """Fold a match result into triage.jsonl; returns (rows, changes)."""
    old = {r["section_id"]: r for r in core.triage(code)}
    rows, changed = [], 0
    for s in core.sections(code):
        r = dict(old.get(s["section_id"]) or empty_row(s))
        before = dict(r)
        ids = m["sections"].get(s["section_id"], [])
        r["match_rule_ids"] = ids
        if ids:
            if r.get("decided_by") in (None, "match"):
                r.update(route="stated", route_reason="at least one rule in this or a parent layer cites this section",
                         tier="stated", review_decision="stated", decided_by="match", rule_ids=list(ids))
        elif r.get("decided_by") == "match":
            r.update(route=None, route_reason=None, tier=None, review_decision=None, decided_by=None, rule_ids=[])
        changed += r != before
        rows.append(r)
    return rows, changed


def main(code):
    m = compute(code)
    rows, changed = apply_match(code, m)
    wrote = core.write_json(core.jdir(code) / "match.json", m)
    core.write_jsonl(core.jdir(code) / "triage.jsonl", rows)
    stated = sum(1 for v in m["sections"].values() if v)
    print(f"{code} match ({' -> '.join(m['layers'])}): {len(m['sections'])} sections, {stated} stated by a rule; "
          f"{len(m['unmatched'])} citations to this layer's instruments outside its in-scope sections; "
          f"{len(m['unregistered'])} citations to unregistered instruments; triage rows changed {changed}; "
          f"match.json {'written' if wrote else 'unchanged'}")
    return 0
