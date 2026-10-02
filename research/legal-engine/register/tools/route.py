"""Routing owned by code (routing.json). route(section, jev, cfg, ctx) -> (status, reason).

Statuses: stated, review_queue, triaged_no_decision, triaged_excluded, unfetched.
ctx: {"stated": bool, "definition_in_stated_unit": bool}
"""
import json
import pathlib
import re

REG = pathlib.Path(__file__).resolve().parent.parent
DEF_RX = re.compile(r"\bdefinitions?\b|meaning of terms|terms defined|rules of construction", re.I)
APP_RX = re.compile(r"applicab|^\s*scope\b|\bapplication of (this|the) (part|chapter|article|title|subchapter)|\bcoverage\b", re.I)


def config(version=None):
    r = json.loads((REG / "routing.json").read_text())
    v = version or r["current"]
    return v, r["versions"][v]


def is_definition(sec):
    return bool(DEF_RX.search(sec.get("heading") or ""))


def is_applicability(sec):
    return bool(APP_RX.search(sec.get("heading") or ""))


def repealed_stub(sec):
    return bool(sec.get("repealed")) and sec.get("chars", 0) < 600


def route(sec, jev, cfg, ctx, ignore_stated=False):
    rq = cfg["review_queue_if_any"]
    if not sec.get("text_file"):
        return "unfetched", "no saved text (see fetch_gaps.json); goes to the review queue"
    if ctx.get("stated") and not ignore_stated:
        return "stated", "at least one rule-file atom cites this section (provision or source_file)"
    if sec.get("chars", 0) > rq["long_chars_gt"]:
        return "review_queue", f"LONG: {sec['chars']} characters > {rq['long_chars_gt']} (not sent to Jev)"
    if rq.get("definition_section_in_unit_with_stated_rule") and ctx.get("definition_in_stated_unit"):
        return "review_queue", "DEFINITIONS: definition section in a unit that has a stated rule"
    if rq.get("applicability_section_in_unit_with_stated_rule") and ctx.get("applicability_in_stated_unit"):
        return "review_queue", "APPLICABILITY: applicability or scope section in a unit that has a stated rule"
    if rq.get("cited_by_review_universe_4a_or_5a") and ctx.get("universe"):
        return "review_queue", "UNIVERSE: cited by an independent review universe item (" + ", ".join(ctx["universe"][:4]) + ")"
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
