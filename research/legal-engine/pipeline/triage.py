"""triage and calibrate (J4 step 1; references/jev-triage.md).

triage CODE: run Jev on every unmatched section with text of at most 12,000 characters (cached answers are reused),
then route and tier every section with the current routing version and write triage.jsonl. Review decisions are
never touched. Exits non-zero when any target is left without an answer (spend cap, attempt ceiling, errors).

calibrate CODE: run Jev on the gold set and report recall per routing version. Gold positives: this jurisdiction's
stated sections (J3) and the reviewer-labeled deciding sections of other jurisdictions in the same legal functions
(pipeline/data/gold_labels.jsonl). Gold negatives: jurisdictions/<CODE>/calibration_negatives.json, at least 150
hand-checked sections, each with a reason. Exits non-zero when the current version routes any positive to set-aside
or when there are fewer than 150 negatives.
"""
from __future__ import annotations

import collections

from . import core, jev, route

MIN_NEGATIVES = 150


def inst_names(codes_):
    names = {}
    for c in codes_:
        for i in core.instruments(c).get("instruments", []):
            names[i["id"]] = i.get("name", i["id"])
    return names


def jev_subset(r):
    if not r:
        return None
    return {k: r.get(k) for k in ("role", "role_probabilities", "role_confidence", "chain_duty", "model", "cache_key",
                                  "registry_version", "origin", "created_at", "response_hash")}


def current_answers(code):
    """Read current request-bound evidence; embedded projections are never authority."""
    prof = core.profile(code)
    names = inst_names(core.family(code))
    return jev.cached_answers(code, [(s["section_id"], s, prof, names) for s in core.sections(code)])


def current_rows(code):
    rows = core.triage(code)
    reroute(code, rows)
    return rows


def reroute(code, rows, answers=None, version=None):
    """Recompute routes from validated cache evidence, preserving displaced history.

    Optional answer projections cannot establish compatibility. Live calls persist
    the complete envelope before routing, so all callers use the same cache check.
    """
    answers = current_answers(code)
    v, cfg = route.config(version)
    tiers = core.routing()["tiers"]
    prof = core.profile(code)
    secs = {s["section_id"]: s for s in core.sections(code)}
    matched = {r["section_id"]: r.get("match_rule_ids") for r in rows}
    prior = {r["section_id"]: r.get("prior_review_citations") for r in rows}
    ctx = route.contexts(secs, matched, (prof.get("aperture") or {}).get("regime_units", []), prior)
    changed = 0
    for r in rows:
        sid = r["section_id"]
        j = jev_subset(answers.get(sid))
        st, why = route.route(secs[sid], j, cfg, ctx[sid])
        new = dict(r, jev=j, route=st, route_reason=why, routing_version=v, tier=route.tier(st, why, j, cfg, tiers),
                   hand_reason=why[6:] if why.startswith("HAND:") else r.get("hand_reason") if st.startswith("triaged") else None)
        if r.get("jev") and r.get("jev") != j:
            new["jev_history"] = [*r.get("jev_history", []), {
                "retired_at": core.now(), "jev": r["jev"], "route": r.get("route"),
                "route_reason": r.get("route_reason"), "tier": r.get("tier"),
                "routing_version": r.get("routing_version"),
                "reason": "Replaced by current validated evidence or unavailable current answer"}]
        changed += new != r
        r.clear()
        r.update(new)
    return changed


def triage_main(code, cap=2.00, ceiling=12000, concurrency=8, limit=None, cached_only=False, rerun=False):
    """rerun includes compatible cached rows in lookup; it does not force a paid inference."""
    rows = core.triage(code)
    secs = core.sections(code)
    documents = [s["section_id"] for s in secs if s.get("source_unit_kind") == "document"]
    if documents:
        raise core.PipelineError(f"{code}: enumerate document internal sections before triage: {documents[:3]}")
    row_ids = [r["section_id"] for r in rows]
    section_ids = [s["section_id"] for s in secs]
    if (not rows or len(set(row_ids)) != len(row_ids) or len(set(section_ids)) != len(section_ids)
            or set(row_ids) != set(section_ids)):
        raise core.PipelineError(f"{code}: triage.jsonl has {len(rows)} rows for {len(secs)} sections; run match first")
    prof = core.profile(code)
    names = inst_names(core.family(code))
    by = {s["section_id"]: s for s in secs}
    available = current_answers(code)
    targets = [(r["section_id"], by[r["section_id"]], prof, names) for r in rows
               if not r.get("match_rule_ids") and by[r["section_id"]].get("text_file")
               and by[r["section_id"]].get("chars", 0) <= jev.LONG and (rerun or r["section_id"] not in available)]
    deferred = targets[limit:] if limit is not None else []
    if limit is not None:
        targets = targets[:limit]
    if cached_only:
        answers = jev.cached_answers(code, targets)
        usage = {"mode": "cached only (no network)", "outcomes": answers.outcomes}
    else:
        answers, usage = jev.run(code, targets, cap, ceiling, concurrency)
    changed = reroute(code, rows, answers)
    core.write_jsonl(core.jdir(code) / "triage.jsonl", rows)
    missing = [t[0] for t in targets if t[0] not in answers]
    if deferred:
        print(f"  {len(deferred)} eligible sections deferred by limit; triage remains incomplete")
    rc = collections.Counter(r["route"] for r in rows)
    tc = collections.Counter(r["tier"] for r in rows)
    print(f"{code} triage: {len(targets)} sections sent or looked up; {len(answers)} answered; rows changed {changed}")
    print(f"  routes: {dict(rc)}")
    print(f"  tiers:  {dict(tc)}")
    print(f"  usage:  {usage}")
    if missing:
        print(f"  {len(missing)} sections have no Jev answer (first {missing[:5]}); rerun triage")
        return 1
    return 1 if deferred else 0


# ---------- calibration ----------

def gold(code):
    """(positives, negatives): lists of (sid, section dict, profile)."""
    prof = core.profile(code)
    rows = {r["section_id"]: r for r in core.triage(code)}
    pos = [(s["section_id"], s, prof) for s in core.sections(code) if (rows.get(s["section_id"]) or {}).get("match_rule_ids")]
    fns = {f for i in core.instruments(code).get("instruments", []) for f in i.get("functions", [])}
    gl = core.PKG / "data" / "gold_labels.jsonl"
    for g in core.read_jsonl(gl):
        if not g.get("deciding") or g.get("jurisdiction") == code or not (set(g.get("functions") or []) & fns):
            continue
        tf = next((t for t in (g.get("text_file"), g.get("legacy_text_file")) if t and (core.ROOT / t).exists()), None)
        # Missing source text remains an unanswered input in the population.
        gp = core.profile(g["jurisdiction"]) if core.exists(g["jurisdiction"]) else prof
        pos.append((g["section_id"], {"section_id": g["section_id"], "instrument": g["instrument"], "unit": g["unit"],
                                      "heading": g.get("heading"), "text_file": tf, "chars": g.get("chars", 0)}, gp))
    negf = core.read_json(core.jdir(code) / "calibration_negatives.json", {"negatives": []})
    by = {s["section_id"]: s for s in core.sections(code)}
    neg = [(n["section_id"], by.get(n["section_id"], {"section_id": n["section_id"], "text_file": None}), prof)
           for n in negf["negatives"]]
    negrows = list(negf["negatives"])
    # pooled negatives of other jurisdictions (pipeline/data/gold_negatives.jsonl), like the pooled positives
    for g in core.read_jsonl(core.PKG / "data" / "gold_negatives.jsonl"):
        if g.get("jurisdiction") == code or g.get("reviewer_decision") in core.DECIDING:
            continue
        tf = next((t for t in (g.get("text_file"), g.get("legacy_text_file")) if t and (core.ROOT / t).exists()), None)
        # Missing source text remains an unanswered input in the population.
        gp = core.profile(g["jurisdiction"]) if core.exists(g["jurisdiction"]) else prof
        neg.append((g["section_id"], {"section_id": g["section_id"], "instrument": g["instrument"], "unit": g["unit"],
                                      "heading": g.get("heading"), "text_file": tf, "chars": g.get("chars", 0)}, gp))
        negrows.append(g)
    return pos, neg, negrows


def own_label_recall(code):
    """Jev's recall on this jurisdiction's own reviewer labels, by tier (J4 step 4); None before any decision."""
    rows = [r for r in current_rows(code) if r.get("decided_by") == "reviewer" and r.get("review_decision")]
    if not rows:
        return None
    by = collections.OrderedDict()
    for t in route.TIER_ORDER:
        rs = [r for r in rows if r.get("tier") == t]
        if rs:
            by[t] = {"sections": len(rs), "deciding": sum(r["review_decision"] in core.DECIDING for r in rs)}
    dec = [r for r in rows if r["review_decision"] in core.DECIDING]
    return {"reviewer_decided": len(rows), "deciding": len(dec),
            "deciding_queued": sum(r.get("route") == "review_queue" for r in dec),
            "deciding_set_aside": sum(str(r.get("route")).startswith("triaged") for r in dec), "by_tier": by,
            "with_current_jev": sum(bool(r.get("jev")) for r in rows),
            "without_current_jev": sum(not r.get("jev") for r in rows),
            "scope": "Current recomputed routing; routing at the time of review was not captured."}


def calibration_contexts(items):
    """Use each example's source register, without treating its gold label as routing evidence.

    Pooled examples need their own definition/applicability and regime context. Looking only in the
    target register drops those structural routes and measures a different algorithm from triage.
    Missing source registers remain context-free; never synthesize context from reviewer labels.
    """
    contexts = {}
    for code in sorted({core.code_of(sid) for sid, _, _ in items}):
        if not core.exists(code):
            continue
        secs = {s["section_id"]: s for s in core.sections(code)}
        rows = {r["section_id"]: r for r in core.triage(code)}
        contexts.update(route.contexts(
            secs, {sid: r.get("match_rule_ids") for sid, r in rows.items()},
            (core.profile(code).get("aperture") or {}).get("regime_units", []),
            {sid: r.get("prior_review_citations") for sid, r in rows.items()}))
    return contexts


def calibrate_main(code, cached_only=False, versions=None, cap=2.00, ceiling=12000, limit=None):
    pos, neg, negrows = gold(code)
    population = {"positives": len(pos), "negatives": len(neg)}
    if limit is not None:
        pos, neg = pos[:limit], neg[:limit]
    deferred = population["positives"] + population["negatives"] - len(pos) - len(neg)
    names = inst_names(core.codes())
    items = [(sid, s, p, names) for sid, s, p in pos + neg]
    if cached_only:
        answers = jev.cached_answers(code, items)
        usage = {"mode": "cached only (no network)", "outcomes": getattr(answers, "outcomes", [])}
    else:
        answers, usage = jev.run(code, items, cap, ceiling)
    rj = core.routing()
    versions = versions or list(rj["versions"])
    ctx = calibration_contexts(pos + neg)
    evals = []
    for v in versions:
        cfg = rj["versions"][v]
        res = {"version": v, "positives": len(pos), "negatives": len(neg), "missed": [], "negatives_set_aside": 0,
               "unanswered": 0, "unanswered_long": 0, "negatives_unanswered": 0}
        for sid, s, _ in pos:
            if sid not in answers:
                # no Jev answer: routing queues it by default (long rule or no record), which proves nothing about
                # Jev, so recall is computed over answered positives only
                res["unanswered"] += 1
                res["unanswered_long"] += s.get("chars", 0) > jev.LONG
                continue
            st, why = route.route(s, jev_subset(answers.get(sid)), cfg, ctx.get(sid, {}), ignore_stated=True)
            if st != "review_queue":
                res["missed"].append({"section_id": sid, "route": st, "reason": why})
        for sid, s, _ in neg:
            if sid not in answers:
                res["negatives_unanswered"] += 1
                continue
            st, _ = route.route(s, jev_subset(answers.get(sid)), cfg, ctx.get(sid, {}), ignore_stated=True)
            res["negatives_set_aside"] += st.startswith("triaged")
        scored = len(pos) - res["unanswered"]
        res["recalled"] = scored - len(res["missed"])
        res["recall"] = round(res["recalled"] / scored, 4) if scored else None
        evals.append(res)
    out = {"jurisdiction": code, "at": core.now(), "usage": usage, "answered": len(answers),
           "evaluation_version": "2.2-attributed-results",
           "selected_answers": answers, "population": population, "deferred_by_limit": deferred,
           "context_policy": "Each example uses its source register; gold labels never create routing context.",
           "gold_positives": len(pos), "gold_negatives": len(neg), "evaluations": evals}
    for r in evals:
        print(f"{code} {r['version']}: recall {r['recalled']}/{r['positives'] - r['unanswered']} = {r['recall']} over "
              f"positives with a Jev answer ({r['unanswered']} of {r['positives']} positives without one: "
              f"{r['unanswered_long']} longer than the Jev limit, queued unasked by the long rule; "
              f"{r['unanswered'] - r['unanswered_long']} not answered); negatives set aside "
              f"{r['negatives_set_aside']}/{r['negatives'] - r['negatives_unanswered']} answered")
        for x in r["missed"]:
            print("   MISS", x["section_id"], x["route"], x["reason"])
    own = own_label_recall(code)
    if own:
        out["own_reviewer_labels"] = own
        print(f"  own reviewer labels (current validated routing against reviewer labels): deciding {own['deciding']}, "
              f"routed to review {own['deciding_queued']}, set aside {own['deciding_set_aside']}")
        for t, c in own["by_tier"].items():
            print(f"    tier {t}: {c['sections']} sections, {c['deciding']} deciding")
    calibration_path = core.jdir(code) / "calibration.json"
    jev.preserve_file(calibration_path, core.jdir(code) / "calibration-history")
    jev.reuse.atomic_write(calibration_path, jev.redact(jev.reuse.serialized(out)) + "\n")
    print(f"  usage: {usage}")
    bad = bool(deferred)
    if deferred:
        print(f"  INCOMPLETE: {deferred} gold inputs deferred by limit")
    if len(negrows) < MIN_NEGATIVES:
        print(f"  FAIL: {len(negrows)} gold negatives; at least {MIN_NEGATIVES} hand-checked negatives are required")
        bad = True
    cur = next((r for r in evals if r["version"] == rj["current"]), None)
    if cur and cur["missed"]:
        print(f"  FAIL: current routing {rj['current']} sets aside {len(cur['missed'])} gold positives; add a tighter version")
        bad = True
    if not pos:
        print("  FAIL: no gold positives")
        bad = True
    if evals and evals[0]["unanswered"] - evals[0]["unanswered_long"]:
        print(f"  FAIL: {evals[0]['unanswered'] - evals[0]['unanswered_long']} gold positives within the Jev limit have no "
              "Jev answer; recall is over the answered ones only")
        bad = True
    if evals and evals[0]["negatives_unanswered"]:
        print(f"  FAIL: {evals[0]['negatives_unanswered']} gold negatives have no Jev answer")
        bad = True
    return 1 if bad else 0
