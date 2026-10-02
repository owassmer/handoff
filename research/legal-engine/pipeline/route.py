"""Triage routing and tiers (code owns them; pipeline/routing.json holds the versioned thresholds).

route(section, jev, cfg, ctx) -> (route, reason); the same decision procedure as register/tools/route.py.
Routes: stated, review_queue, triaged_no_decision, triaged_excluded, unfetched. Every route still goes to a
reviewer (J4 step 2); the route and tier only order the work.
ctx: {stated, definition_in_stated_unit, applicability_in_stated_unit, prior_review: [ids], regime_unit}
"""
from __future__ import annotations

import re

from . import core

DEF_RX = re.compile(r"\bdefinitions?\b|meaning of terms|terms defined|rules of construction", re.I)
APP_RX = re.compile(r"applicab|^\s*scope\b|\bapplication of (this|the) (part|chapter|article|title|subchapter)|\bcoverage\b", re.I)
TIER_ORDER = ["strong", "likely", "possible", "low_confidence", "structural", "long", "unscored", "set_aside", "stated"]


def config(version=None):
    r = core.routing()
    v = version or r["current"]
    if v not in r["versions"]:
        raise core.PipelineError(f"unknown routing version {v}")
    return v, r["versions"][v]


def is_definition(sec):
    return bool(DEF_RX.search(sec.get("heading") or ""))


def is_applicability(sec):
    return bool(APP_RX.search(sec.get("heading") or ""))


def repealed_stub(sec):
    return bool(sec.get("repealed")) and sec.get("chars", 0) < 600


def contexts(secs, matched, regime_units=(), prior=None):
    """secs: {section_id: section}; matched: {section_id: [rule ids]}; prior: {section_id: [prior review ids]}."""
    stated_units = {(s["instrument"], s["unit"]) for sid, s in secs.items() if matched.get(sid)}
    regime = set(regime_units)
    prior = prior or {}
    return {sid: {"stated": bool(matched.get(sid)),
                  "definition_in_stated_unit": is_definition(s) and (s["instrument"], s["unit"]) in stated_units,
                  "applicability_in_stated_unit": is_applicability(s) and (s["instrument"], s["unit"]) in stated_units,
                  "prior_review": list(prior.get(sid) or []),
                  "regime_unit": f"{s['instrument']}|{s['unit']}" in regime}
            for sid, s in secs.items()}


def route(sec, jev, cfg, ctx, ignore_stated=False):
    rq = cfg["review_queue_if_any"]
    if not sec.get("text_file"):
        return "unfetched", "no saved text (see instruments.json fetch_gaps); goes to a reviewer"
    if ctx.get("stated") and not ignore_stated:
        return "stated", "at least one rule in this or a parent layer cites this section (provision or source_file)"
    if sec.get("chars", 0) > rq["long_chars_gt"]:
        return "review_queue", f"LONG: {sec['chars']} characters > {rq['long_chars_gt']} (not sent to Jev)"
    if rq.get("definition_section_in_unit_with_stated_rule") and ctx.get("definition_in_stated_unit"):
        return "review_queue", "DEFINITIONS: definition section in a unit that has a stated rule"
    if rq.get("applicability_section_in_unit_with_stated_rule") and ctx.get("applicability_in_stated_unit"):
        return "review_queue", "APPLICABILITY: applicability or scope section in a unit that has a stated rule"
    if (rq.get("cited_by_prior_review") or rq.get("cited_by_review_universe_4a_or_5a")) and ctx.get("prior_review"):
        return "review_queue", "UNIVERSE: cited by an independent review universe item (" + ", ".join(ctx["prior_review"][:4]) + ")"
    if repealed_stub(sec) and jev is None:
        return "triaged_no_decision", "HAND: repealed or reserved section with no operative text (heading/text mark it repealed)"
    if jev is None:
        return "review_queue", "NO_JEV_RECORD"
    p = (jev.get("role_probabilities") or {}).get("DECIDES", 0) or 0
    duty = jev.get("chain_duty")
    conf = jev.get("role_confidence")
    why = []
    if p >= rq["q1_p_decides_gte"]:
        why.append(f"P(DECIDES)={p:.2f}>={rq['q1_p_decides_gte']}")
    if duty is None or duty >= rq["q2_chain_duty_gte"]:
        why.append(f"chain_duty={duty}>={rq['q2_chain_duty_gte']}")
    if conf is None or conf < rq["q1_confidence_lt"]:
        why.append(f"confidence={conf}<{rq['q1_confidence_lt']}")
    if why:
        return "review_queue", "JEV: " + "; ".join(why)
    if jev.get("role") == "EXCLUDED_REGIME" and rq.get("excluded_regime_outside_regime_units") and not ctx.get("regime_unit"):
        return "review_queue", f"EXCLUDED_REGIME outside a regime unit (P(DECIDES)={p:.2f}, chain_duty={duty:.2f}): aperture decides, not Jev"
    if jev.get("role") == "EXCLUDED_REGIME":
        return "triaged_excluded", f"JEV: EXCLUDED_REGIME conf={conf:.2f}, P(DECIDES)={p:.2f}, chain_duty={duty:.2f}"
    if jev.get("role") == "NO_DECISION":
        return "triaged_no_decision", f"JEV: NO_DECISION conf={conf:.2f}, P(DECIDES)={p:.2f}, chain_duty={duty:.2f}"
    return "review_queue", f"JEV: role {jev.get('role')}"


def tier(route_, reason, jev, cfg, tiers=None):
    """Tier for ordering reviewer work (routing.json 'tiers')."""
    tiers = tiers or core.routing()["tiers"]
    if route_ == "stated":
        return "stated"
    if route_ in ("triaged_no_decision", "triaged_excluded"):
        return "set_aside"
    if (reason or "").startswith("LONG"):
        return "long"
    if not jev:
        return "unscored" if route_ != "review_queue" or reason == "NO_JEV_RECORD" else "structural"
    rq = cfg["review_queue_if_any"]
    p = (jev.get("role_probabilities") or {}).get("DECIDES", 0) or 0
    d = jev.get("chain_duty")
    d = 0 if d is None else d
    c = jev.get("role_confidence")
    if p >= tiers["strong"]["p_decides_gte"] and d >= tiers["strong"]["chain_duty_gte"]:
        return "strong"
    if p >= tiers["likely"]["either_gte"] or d >= tiers["likely"]["either_gte"]:
        return "likely"
    if p >= rq["q1_p_decides_gte"] or d >= rq["q2_chain_duty_gte"]:
        return "possible"
    if c is None or c < rq["q1_confidence_lt"]:
        return "low_confidence"
    return "structural"


def tier_rank(t):
    return TIER_ORDER.index(t) if t in TIER_ORDER else len(TIER_ORDER)


def p_decides(row):
    j = row.get("jev") or {}
    return (j.get("role_probabilities") or {}).get("DECIDES")
