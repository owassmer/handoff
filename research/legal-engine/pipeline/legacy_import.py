"""import-legacy DEST: convert the NY-family legacy files into the jurisdictions/<CODE>/ layout, inside DEST only.

  PIPELINE_ROOT=DEST python3 -m pipeline import-legacy DEST [--src research/legal-engine]

DEST must be a copy location, never the live research/legal-engine tree (refused). The legacy inputs are read from
--src (default: the live tree, read-only) and copied into DEST first (stage-a/, register/, review/, sources/,
stage_a_check.py) so the legacy checkers can be rerun there. Then, for US, NY, NYC and VA:
  profile.json      layer and parents (NYC -> NY -> US; VA -> US), the legacy citation configs
                    (pipeline/legacy_citations.py), aperture and Jev chain from register/jev_questions.json, regime
                    units from register/routing.json, and for NYC the walk scope exclusion read from
                    review/check_review.py (REGULATED_ONLY). owner_confirmed is left empty: import is not intake.
  rules.json        stage-a/<CODE>.json unchanged except layer/parents and source paths under register/texts/,
                    which point to the copied text in the section's jurisdiction folder (same bytes).
  instruments.json  register/instruments.json rows of the layer, with chain-map functions per instrument and unit
                    (pipeline/data/crosswalk.json rules), an adapter per instrument (by its TOC host), fetch gaps,
                    non-code sources, and a reason for each chain-map function the layer has no instrument for.
  sections.jsonl, texts/   register/sections.jsonl rows and texts, moved under the layer.
  triage.jsonl      register/triage.jsonl: status -> route, reason -> route_reason, match atoms (register/match.json)
                    -> match_rule_ids, universe 4A/5A -> prior_review_citations, returned_model -> jev.model,
                    review_batch 'match' -> decided_by 'match', numbered batches -> decided_by 'reviewer',
                    atom_ids -> rule_ids.
  decisions/        register/work/batch_N.json and decisions_N.jsonl, split by layer (text paths remapped).
  jev/cache/        the register's Jev cache files for the layer's records.
  calibration_negatives.json, walk.md (NYC: review/NYC_MARKET_RATE.md), match.json (a fresh J3 match),
  authorities.json and adjudication.json (empty), DISPOSITION.md (the import record).
Idempotent: rerunning rebuilds the same files.
"""
from __future__ import annotations

import ast
import collections
import pathlib
import re
import shutil

from . import core, legacy_citations, route

LAYERS = {"US": ("federal", [], "United States (federal)"), "NY": ("state", ["US"], "New York State"),
          "NYC": ("city", ["NY"], "New York City"), "VA": ("state", ["US"], "Virginia")}
COPY = ["stage-a", "register", "review", "sources", "stage_a_check.py"]


def regulated_only(src):
    """The REGULATED_ONLY pattern string from review/check_review.py (read with ast, not retyped)."""
    tree = ast.parse((src / "review" / "check_review.py").read_text())
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "REGULATED_ONLY" for t in n.targets):
            return ast.literal_eval(n.value.args[0])
    raise core.PipelineError("REGULATED_ONLY not found in review/check_review.py")


def legacy_adjudication(reg, code):
    """adjudication.json from register/work/applied.json: every proposal the legacy register applied, by the layer of
    the section that proposed it. 'added' -> accepted; 'merged' -> accepted and recorded as a merge into the atom that
    carries its quote as a construction entry (references/schemas.md merges[{into, from[]}])."""
    applied = core.read_json(reg / "work" / "applied.json", {})
    props, merges = {}, collections.OrderedDict()
    for pid, rec in sorted(applied.items()):
        if core.code_of(rec.get("section_id") or pid) != code:
            continue
        disp = rec.get("disposition")
        props[pid] = {"ruling": "accept", "conditions": [],
                      "note": f"applied in the legacy register (register/work/applied.json: {disp}"
                              + (f" into {rec['atom_id']}" if disp == "merged" else "") + f", batch {rec.get('batch')})"}
        if disp == "merged":
            merges.setdefault(rec["atom_id"], []).append(pid)
    return {"proposals": props, "existing_rule_changes": [],
            "merges": [{"into": k, "from": v} for k, v in merges.items()]}


def copy_inputs(src, dest):
    for name in COPY:
        s, d = src / name, dest / name
        if not s.exists() or d.exists():
            continue
        if s.is_dir():
            shutil.copytree(s, d, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(s, d)


def new_text_path(legacy_rel, code_of_file):
    """'texts/NY_ABP/101.txt' or 'register/texts/NY_ABP/101.txt' -> 'jurisdictions/NY/texts/NY_ABP/101.txt'."""
    rest = legacy_rel[len("register/"):] if legacy_rel.startswith("register/") else legacy_rel
    code = code_of_file.get(rest)
    return f"jurisdictions/{code}/{rest}" if code else None


def remap(obj, code_of_file):
    """Remap every source_file/text_file under register/texts/ in a rule, proposal or batch row (in place)."""
    if isinstance(obj, dict):
        for k in ("source_file", "text_file"):
            v = obj.get(k)
            if isinstance(v, str) and v.startswith("register/texts/"):
                nv = new_text_path(v, code_of_file)
                if nv:
                    obj[k] = nv
        for v in obj.values():
            remap(v, code_of_file)
    elif isinstance(obj, list):
        for v in obj:
            remap(v, code_of_file)
    return obj


def functions_for(code, inst_rows):
    from . import export
    cw = {i["id"]: i for i in export.crosswalk({"instruments": inst_rows})}
    return cw


def main(dest, src=None):
    dest = pathlib.Path(dest).resolve()
    src = pathlib.Path(src or core.PKG.parent).resolve()
    live = core.PKG.parent.resolve()
    if dest == live or live in dest.parents:
        raise core.PipelineError(f"refusing to import into the live tree {live}; give a scratch copy location")
    dest.mkdir(parents=True, exist_ok=True)
    copy_inputs(src, dest)
    core.set_root(dest)
    reg = dest / "register"
    inst_doc = core.read_json(reg / "instruments.json")
    secs = core.read_jsonl(reg / "sections.jsonl")
    tri = {r["section_id"]: r for r in core.read_jsonl(reg / "triage.jsonl")}
    mj = core.read_json(reg / "match.json")["sections"]
    gaps = core.read_json(reg / "fetch_gaps.json", {"section_gaps": [], "instrument_gaps": []})
    jq = core.read_json(reg / "jev_questions.json")
    rv = core.read_json(reg / "routing.json")
    negs = core.read_json(reg / "calibration_negatives.json", {"negatives": []})["negatives"]
    regime = rv["versions"].get("v2", {}).get("regime_units", [])
    code_of_file = {s["text_file"]: core.code_of(s["section_id"]) for s in secs if s.get("text_file")}
    fns_all = [f["id"] for f in core.chain_map()["functions"]]
    counts = {}

    # instruments and functions (crosswalk over the whole register, then split by layer)
    cw = functions_for(None, inst_doc["instruments"])
    coverage = collections.defaultdict(set)
    for i in cw.values():
        for u in i["units"]:
            if u["scope"] == "in":
                coverage[core.code_of(i["id"])] |= set(u["functions"])

    from . import adapters
    for code, (layer, parents, name) in LAYERS.items():
        d = core.jdir(code)
        if d.exists():
            shutil.rmtree(d)
        (d / "decisions").mkdir(parents=True)
        from .init import profile_template
        prof = profile_template(code, layer, parents, name)
        prof.update(status="imported", owner_confirmed={"by": "", "date": "", "note": "Imported from the legacy NY "
                    "register; the owner confirms it at intake of the pipeline version (J0)."},
                    citations=legacy_citations.CONFIGS.get(code, {}),
                    imported={"from": ["stage-a/", "register/", "review/"], "at": core.now()})
        prof["courts"], prof["customer_courts"] = [], []
        prof["aperture"] = {"exclusions": jq.get("aperture_exclusions", ""),
                            "regime_units": [u for u in regime if u.startswith(code + ":")]}
        prof["jev"] = {"scope": "a market-rate residential unit in New York City under New York State, New York City "
                                "and federal law", "chain_description": jq.get("chain_description", "")}
        if code == "NYC":
            prof["walk"] = {"scope_exclude": regulated_only(dest)}
        core.write_json(d / "profile.json", prof)

        # rules
        rules = core.read_json(dest / "stage-a" / f"{code}.json")
        rules = dict({"jurisdiction": code, "layer": layer, "parents": parents}, **{k: v for k, v in rules.items()
                                                                                     if k != "jurisdiction"})
        remap(rules.get("atoms", []), code_of_file)
        core.write_json(d / "rules.json", rules)
        counts[code] = {"rules": len(rules.get("atoms", []))}
        if code == "VA":
            core.write_json(d / "instruments.json", {"jurisdiction": code, "instruments": [],
                                                     "functions_without_instrument": [], "non_code_sources": [],
                                                     "fetch_gaps": {"section_gaps": [], "instrument_gaps": []},
                                                     "note": "Rules only: stage-a/VA.json has no register."})
            for f in ("sections.jsonl", "triage.jsonl"):
                (d / f).write_text("")
            core.write_json(d / "authorities.json", [])
            core.write_json(d / "adjudication.json", {"proposals": {}, "existing_rule_changes": [], "merges": []})
            (d / "DISPOSITION.md").write_text(f"# {code} disposition\n\n- Imported {core.now()}: {counts[code]['rules']} "
                                              "rules from stage-a/VA.json (no register, walk or decisions).\n")
            continue

        # instruments
        own = []
        for i in inst_doc["instruments"]:
            if core.code_of(i["id"]) != code:  # by id: NY:CCA is registered under NYC but its sections are NY:
                continue
            c = cw[i["id"]]
            ufn = {u["unit"]: u["functions"] for u in c["units"]}
            row = {k: v for k, v in i.items() if k not in ("section_status_counts",)}
            row["functions"] = c["functions"]
            if row.get("level") == "rule":  # the register's one 'rule' is the Rules of the City of New York
                row["level"] = "agency rule"
            row["units_in_scope"] = [dict(u, functions=ufn.get(u["unit"], [])) for u in i["units_in_scope"]]
            row["adapter"] = adapters.for_url(i.get("toc_source_url") or "").name
            own.append(row)
        nc = [n for n in inst_doc.get("non_code_sources", [])
              if any(core.code_of(a) == code for a in n.get("atom_ids", []))]
        others = {c: sorted(v) for c, v in coverage.items() if c != code}
        fwi = [{"function": f, "reason": "No instrument of this layer in the legacy register serves this function"
                + (("; covered in " + ", ".join(c for c, v in others.items() if f in v)) if any(f in v for v in others.values())
                   else "; no layer of the legacy register covers it")}
               for f in fns_all if f not in coverage[code]]
        ig = [g for g in gaps.get("instrument_gaps", []) if re.search(r"\b" + re.escape(code) + r":", g.get("instrument", ""))]
        core.write_json(d / "instruments.json", {
            "jurisdiction": code, "instruments": own, "functions_without_instrument": fwi, "non_code_sources": nc,
            "fetch_gaps": {"section_gaps": [g for g in gaps.get("section_gaps", []) if core.code_of(g["section_id"]) == code],
                           "instrument_gaps": ig},
            "considered_not_added": inst_doc.get("considered_not_added", []) if code == "US" else [],
            "legacy": {"generated": inst_doc.get("generated"), "routing_version": inst_doc.get("routing_version")}})

        # sections and texts
        rows_s, rows_t, keys = [], [], set()
        for s in secs:
            if core.code_of(s["section_id"]) != code:
                continue
            s2 = dict(s)
            if s.get("text_file"):
                nt = new_text_path(s["text_file"], code_of_file)
                (dest / nt).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(reg / s["text_file"], dest / nt)
                s2["text_file"] = nt
                s2["sha256"] = core.text_hash((dest / nt).read_text(errors="replace"))
            rows_s.append(s2)
            t = tri[s["section_id"]]
            m = mj.get(s["section_id"], {})
            j = t.get("jev")
            jj = None if not j else {"role": j.get("role"), "role_probabilities": j.get("role_probabilities"),
                                     "role_confidence": j.get("role_confidence"), "chain_duty": j.get("chain_duty"),
                                     "model": j.get("returned_model"), "cache_key": j.get("cache_key"),
                                     "registry_version": j.get("registry_version")}
            if jj and jj["cache_key"]:
                keys.add(jj["cache_key"])
            batch = t.get("review_batch")
            cfg = rv["versions"].get(t.get("routing_version") or rv["current"]) or rv["versions"][rv["current"]]
            rows_t.append({
                "section_id": s["section_id"], "instrument": s["instrument"], "unit": s["unit"], "heading": s.get("heading"),
                "match_rule_ids": list(m.get("atom_ids") or []), "route": t.get("status"), "route_reason": t.get("reason"),
                "routing_version": t.get("routing_version"),
                "tier": route.tier(t.get("status"), t.get("reason"), jj, cfg, core.routing()["tiers"]),
                "jev": None, "hand_reason": t.get("hand_reason"),
                "prior_review_citations": list(m.get("universe_4a") or []) + list(m.get("universe_5a") or []),
                "review_decision": t.get("review_decision"),
                "review_batch": None if batch == "match" else batch,
                "decided_by": "match" if batch == "match" else ("reviewer" if batch is not None else None),
                "rule_ids": list(t.get("atom_ids") or []), "review_reason": t.get("review_reason"),
                "legacy": {**{k: t[k] for k in ("gap_5a", "review_history") if t.get(k)},
                           "jev": j, "route": t.get("status"), "route_reason": t.get("reason"),
                           "routing_version": t.get("routing_version"),
                           "source": "register/triage.jsonl", "current_jev_verified": False}})
        # Imported judgments retain their original attribution as history. Compute
        # current routes without admitting legacy scores as compatible answers.
        sections_by_id = {s["section_id"]: s for s in rows_s}
        contexts = route.contexts(sections_by_id,
            {r["section_id"]: r["match_rule_ids"] for r in rows_t},
            (prof.get("aperture") or {}).get("regime_units", []),
            {r["section_id"]: r["prior_review_citations"] for r in rows_t})
        cfg = rv["versions"][rv["current"]]
        for r in rows_t:
            sid = r["section_id"]
            st, why = route.route(sections_by_id[sid], None, cfg, contexts[sid])
            r.update(route=st, route_reason=why, routing_version=rv["current"],
                     tier=route.tier(st, why, None, cfg, core.routing()["tiers"]),
                     hand_reason=why[6:] if why.startswith("HAND:") else None)
        core.write_jsonl(d / "sections.jsonl", rows_s)
        core.write_jsonl(d / "triage.jsonl", rows_t)
        (d / "jev" / "cache").mkdir(parents=True, exist_ok=True)
        for k in sorted(keys):
            f = reg / "jev_cache" / f"{k}.json"
            if f.exists():
                shutil.copy2(f, d / "jev" / "cache" / f.name)

        # decisions
        nb = 0
        for bf in sorted((reg / "work").glob("batch_*.json"), key=lambda p: int(p.stem.split("_")[1])):
            n = int(bf.stem.split("_")[1])
            b = core.read_json(bf)
            bs = [remap(dict(x), code_of_file) for x in b["sections"] if core.code_of(x["section_id"]) == code]
            if not bs:
                continue
            dec = [remap(r, code_of_file) for r in core.read_jsonl(reg / "work" / f"decisions_{n}.jsonl")
                   if core.code_of(r["section_id"]) == code]
            core.write_json(d / "decisions" / f"batch_{n}.json", {"batch": n, "jurisdiction": code, "family": b.get("family"),
                                                                   "count": len(bs), "sections": bs,
                                                                   "legacy": f"register/work/batch_{n}.json"})
            core.write_jsonl(d / "decisions" / f"decisions_{n}.jsonl", dec)
            nb += 1
        core.write_json(d / "calibration_negatives.json", {"method": "legacy register/calibration_negatives.json rows of this layer",
                                                           "negatives": [n for n in negs if core.code_of(n["section_id"]) == code]})
        core.write_json(d / "authorities.json", [])
        core.write_json(d / "adjudication.json", legacy_adjudication(reg, code))
        if code == "NYC":
            shutil.copy2(dest / "review" / "NYC_MARKET_RATE.md", d / "walk.md")
        counts[code].update(sections=len(rows_s), triage=len(rows_t), batches=nb, jev_cache=len(keys), instruments=len(own))

    # J3 match on the imported layers (after every layer exists, so parent rules resolve)
    from . import match
    for code in ("US", "NY", "NYC"):
        m = match.compute(code)
        core.write_json(core.jdir(code) / "match.json", m)
        legacy = {sid: sorted(mj.get(sid, {}).get("atom_ids") or []) for sid in m["sections"]}
        diff = [sid for sid, ids in m["sections"].items() if sorted(ids) != legacy[sid]]
        counts[code]["match_differs_from_legacy"] = len(diff)
        counts[code]["match_differs_examples"] = diff[:5]
        (core.jdir(code) / "DISPOSITION.md").write_text(
            f"# {code} disposition\n\n## Import {core.now()}\n\n- From the legacy register (stage-a/{code}.json, register/, "
            f"review/): {counts[code]}.\n- match.json is a fresh J3 match over this layer and its parents; triage.jsonl keeps "
            "the legacy match (register/match.json) on which the legacy routes and decisions rest.\n")
    for code, c in counts.items():
        print(f"import-legacy {code}: " + ", ".join(f"{k} {v}" for k, v in c.items()))
    print(f"import-legacy: wrote {core.rel(core.JUR)} under {dest}")
    return 0
