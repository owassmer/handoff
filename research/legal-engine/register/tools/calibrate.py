"""Calibration of routing thresholds against gold labels (Step 4). Code only; reads jev_results.jsonl.

Gold positives: every 'stated' section plus every section cited in a 5A gap finding, routed as if not stated.
Gold negatives: calibration_negatives.json (hand-checked). Recall target: every positive in the review queue.
Writes calibration.json (all versions evaluated, per-section rows) and calibration.md.
Usage: python3 tools/calibrate.py [VERSION ...]   (default: every version in routing.json)
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import route  # noqa: E402

REG = pathlib.Path(__file__).resolve().parent.parent


def load():
    secs = {json.loads(l)["section_id"]: json.loads(l) for l in (REG / "sections.jsonl").read_text().splitlines() if l.strip()}
    m = json.loads((REG / "match.json").read_text())["sections"]
    jev = {}
    for l in (REG / "jev_results.jsonl").read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            jev[r["section_id"]] = r
    return secs, m, jev


def contexts(secs, m, cfg=None):
    stated_units = {(s["instrument"], s["unit"]) for sid, s in secs.items() if m[sid]["atom_ids"]}
    regime = set((cfg or {}).get("regime_units", []))
    return {sid: {"stated": bool(m[sid]["atom_ids"]),
                  "definition_in_stated_unit": route.is_definition(s) and (s["instrument"], s["unit"]) in stated_units,
                  "applicability_in_stated_unit": route.is_applicability(s) and (s["instrument"], s["unit"]) in stated_units,
                  "universe": m[sid]["universe_4a"] + m[sid]["universe_5a"],
                  "regime_unit": f"{s['instrument']}|{s['unit']}" in regime}
            for sid, s in secs.items()}


def evaluate(version):
    secs, m, jev = load()
    v, cfg = route.config(version)
    ctx = contexts(secs, m, route.config(version)[1] if False else json.loads((REG / "routing.json").read_text())["versions"][v])
    negs = json.loads((REG / "calibration_negatives.json").read_text())["negatives"]
    pos = [sid for sid in secs if m[sid]["atom_ids"] or m[sid]["gap_5a"]]
    rows = []
    for sid in pos:
        st, why = route.route(secs[sid], jev.get(sid), cfg, ctx[sid], ignore_stated=True)
        rows.append({"section_id": sid, "gold": "positive", "route": st, "reason": why,
                     "atoms": m[sid]["atom_ids"][:5], "gap_5a": m[sid]["gap_5a"], **_j(jev.get(sid))})
    for n in negs:
        sid = n["section_id"]
        st, why = route.route(secs[sid], jev.get(sid), cfg, ctx[sid], ignore_stated=True)
        rows.append({"section_id": sid, "gold": "negative", "route": st, "reason": why, "hand_reason": n["reason"], **_j(jev.get(sid))})
    P = [r for r in rows if r["gold"] == "positive"]
    N = [r for r in rows if r["gold"] == "negative"]
    missed = [r for r in P if r["route"] != "review_queue"]
    triaged = [r for r in N if r["route"].startswith("triaged")]
    return {"version": v, "thresholds": cfg["review_queue_if_any"], "positives": len(P), "recalled": len(P) - len(missed),
            "recall": round((len(P) - len(missed)) / len(P), 4), "missed": missed, "negatives": len(N),
            "negatives_triaged_away": len(triaged), "negative_triage_rate": round(len(triaged) / len(N), 4),
            "positives_sent_to_jev": sum(1 for r in P if r.get("role")), "rows": rows}


def _j(r):
    if not r:
        return {"role": None}
    return {"role": r["role"], "p_decides": (r["role_probabilities"] or {}).get("DECIDES"), "confidence": r["role_confidence"],
            "chain_duty": r["chain_duty"], "probabilities": r["role_probabilities"]}


def grid():
    """Q1/Q2 threshold sweep with the current version's structural routes; also the full-population queue size."""
    secs, m, jev = load()
    rj = json.loads((REG / "routing.json").read_text())
    base = rj["versions"][rj["current"]]
    ctx = contexts(secs, m, base)
    negs = [n["section_id"] for n in json.loads((REG / "calibration_negatives.json").read_text())["negatives"]]
    pos = [s for s in secs if m[s]["atom_ids"] or m[s]["gap_5a"]]
    nonstated = [s for s in secs if not m[s]["atom_ids"]]
    out = []
    for q2 in (0.3, 0.25, 0.2, 0.15, 0.1):
        for pd in (0.15, 0.1):
            cfg = json.loads(json.dumps(base))
            cfg["review_queue_if_any"]["q2_chain_duty_gte"] = q2
            cfg["review_queue_if_any"]["q1_p_decides_gte"] = pd
            out.append({"base_version": rj["current"], "q2_chain_duty_gte": q2, "q1_p_decides_gte": pd,
                        "positives_in_queue": sum(route.route(secs[s], jev.get(s), cfg, ctx[s], ignore_stated=True)[0] == "review_queue" for s in pos),
                        "positives": len(pos),
                        "negatives_triaged": sum(route.route(secs[s], jev.get(s), cfg, ctx[s], ignore_stated=True)[0].startswith("triaged") for s in negs),
                        "negatives": len(negs),
                        "full_queue_nonstated": sum(route.route(secs[s], jev.get(s), cfg, ctx[s])[0] == "review_queue" for s in nonstated),
                        "nonstated": len(nonstated)})
    return out


if __name__ == "__main__":
    allv = json.loads((REG / "routing.json").read_text())["versions"]
    versions = sys.argv[1:] or list(allv)
    res = [evaluate(v) for v in versions]
    out = {"note": "Recall target: every gold positive routed to the review queue. Every threshold version evaluated is kept.",
           "evaluations": res, "threshold_grid": grid()}
    (REG / "calibration.json").write_text(json.dumps(out, indent=1))
    for r in res:
        print(f"{r['version']}: recall {r['recalled']}/{r['positives']} = {r['recall']}; negatives triaged away "
              f"{r['negatives_triaged_away']}/{r['negatives']} = {r['negative_triage_rate']}")
        for x in r["missed"]:
            print("   MISS", x["section_id"], x["route"], x.get("role"), x.get("p_decides"), x.get("confidence"), x.get("chain_duty"), x["atoms"][:2], x["gap_5a"])
