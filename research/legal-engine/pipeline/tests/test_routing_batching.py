"""Routing (code-owned thresholds, versions) and batching (250-550 by legal function, highest score first)."""
from pipeline import batch, core, route

from .conftest import write_register

SEC = {"section_id": "T:X 1", "instrument": "T:X", "unit": "u", "heading": "Deposits", "text_file": "t.txt", "chars": 900}
CTX = {"stated": False}


def jev(p, duty, conf=0.95, role="NO_DECISION"):
    return {"role": role, "role_probabilities": {"DECIDES": p}, "role_confidence": conf, "chain_duty": duty}


def cfg(v):
    return route.config(v)[1]


def test_routes():
    v2 = cfg("v2")
    assert route.route(dict(SEC, text_file=None), None, v2, CTX)[0] == "unfetched"
    assert route.route(SEC, None, v2, {"stated": True})[0] == "stated"
    assert route.route(dict(SEC, chars=13000), None, v2, CTX)[1].startswith("LONG")
    assert route.route(SEC, None, v2, CTX) == ("review_queue", "NO_JEV_RECORD")
    assert route.route(SEC, jev(0.2, 0.0), v2, CTX)[0] == "review_queue"          # P(DECIDES) >= 0.15
    assert route.route(SEC, jev(0.0, 0.12), v2, CTX)[0] == "review_queue"         # chain_duty >= 0.10 in v2
    assert route.route(SEC, jev(0.0, 0.12), cfg("v1"), CTX)[0] == "triaged_no_decision"  # v1 threshold 0.3
    assert route.route(SEC, jev(0.0, 0.0, conf=0.5), v2, CTX)[0] == "review_queue"  # low confidence
    assert route.route(SEC, jev(0.0, 0.0), v2, CTX)[0] == "triaged_no_decision"
    ex = jev(0.0, 0.0, role="EXCLUDED_REGIME")
    assert route.route(SEC, ex, v2, CTX)[0] == "review_queue"                      # outside a regime unit
    assert route.route(SEC, ex, v2, {"regime_unit": True})[0] == "triaged_excluded"
    d = dict(SEC, heading="Definitions")
    assert route.route(d, jev(0.0, 0.0), v2, {"definition_in_stated_unit": True})[1].startswith("DEFINITIONS")


def test_tiers():
    v2 = cfg("v2")
    t = lambda j: route.tier(*route.route(SEC, j, v2, CTX), j, v2)
    assert t(jev(0.95, 0.9)) == "strong"
    assert t(jev(0.6, 0.1)) == "likely"
    assert t(jev(0.2, 0.0)) == "possible"
    assert t(jev(0.0, 0.0, conf=0.5)) == "low_confidence"
    assert t(jev(0.0, 0.0)) == "set_aside"


def test_routing_versions_are_recorded():
    r = core.routing()
    assert r["current"] in r["versions"] and set(r["versions"]) >= {"v1", "v2"}


def test_calibrate_recall_over_answered_only(root, monkeypatch):
    """Recall is over positives with a Jev answer; unanswered ones are counted and stated, never scored as recalled."""
    from pipeline import jev as jevmod, triage

    def sec(sid, chars=900):
        return (sid, dict(SEC, section_id=sid, chars=chars), {})
    pos = [sec("P:A 1"), sec("P:A 2"), sec("P:A 3", chars=20000), sec("P:A 4")]
    neg = [sec("P:N %d" % i) for i in range(150)]
    answers = {"P:A 1": jev(0.9, 0.9), "P:A 2": jev(0.0, 0.07)}     # A 3 long (not sent), A 4 unanswered
    answers.update({sid: jev(0.0, 0.0) for sid, _, _ in neg})
    monkeypatch.setattr(triage, "gold", lambda code: (pos, neg, [{}] * len(neg)))
    monkeypatch.setattr(jevmod, "cached_answers", lambda code, items, reg=None: answers)
    rc = triage.calibrate_main("T", cached_only=True)
    ev = {e["version"]: e for e in core.read_json(core.jdir("T") / "calibration.json")["evaluations"]}
    assert ev["v2"]["unanswered"] == 2 and ev["v2"]["unanswered_long"] == 1
    assert (ev["v1"]["recalled"], ev["v1"]["recall"]) == (1, 0.5)   # A 2 (chain_duty 0.07) set aside by v1 and v2
    assert (ev["v2"]["recalled"], ev["v2"]["recall"]) == (1, 0.5)
    assert [m["section_id"] for m in ev["v2"]["missed"]] == ["P:A 2"]
    assert ev["v2"]["negatives_set_aside"] == 150
    assert rc == 1                                                  # current version misses a positive


def test_pack_sizes():
    groups = [("a", list(range(700))), ("b", list(range(100))), ("c", list(range(300)))]
    out = batch.pack(groups)
    assert sum(len(b) for b in out) == 1100
    assert all(len(b) <= batch.MAX for b in out)
    assert all(len(b) >= batch.MIN for b in out)


def test_pooled_calibration_keeps_source_context(root, monkeypatch):
    from pipeline import init, triage, jev as jevmod

    init.main("P", "federal", None, "Pooled jurisdiction")
    write_register("P")
    secs = core.sections("P")
    # The definition has a sibling cited by a rule. Its own gold label is not a match.
    contexts = triage.calibration_contexts([(s["section_id"], s, {}) for s in secs])
    assert contexts["P:TA 2"]["definition_in_stated_unit"]
    assert not contexts["P:TA 2"]["stated"]
    pos = [("P:TA 2", secs[1], {})]
    neg = [(f"X:N {i}", dict(SEC, section_id=f"X:N {i}"), {}) for i in range(150)]
    answers = {sid: jev(0.0, 0.0) for sid, _, _ in pos + neg}
    monkeypatch.setattr(triage, "gold", lambda code: (pos, neg, [{}] * len(neg)))
    monkeypatch.setattr(jevmod, "cached_answers", lambda code, items: answers)
    assert triage.calibrate_main("T", cached_only=True) == 0
    report = core.read_json(core.jdir("T") / "calibration.json")
    assert report["evaluation_version"] == "2.2-attributed-results"
    assert all(not e["missed"] for e in report["evaluations"])


def test_calibration_labels_do_not_create_context(root):
    from pipeline import triage

    orphan = dict(SEC, section_id="ABSENT:X 1", heading="Definitions")
    assert triage.calibration_contexts([("ABSENT:X 1", orphan, {})]) == {}
    write_register("T")
    rows = core.triage("T")
    rows[0]["match_rule_ids"] = []
    rows[0]["review_decision"] = "new_rule"
    core.write_jsonl(core.jdir("T") / "triage.jsonl", rows)
    secs = core.sections("T")
    ctx = triage.calibration_contexts([(s["section_id"], s, {}) for s in secs])
    assert not ctx["T:TA 2"]["definition_in_stated_unit"]


def test_plan_orders_by_score_and_is_incremental(root):
    write_register("T", n_undecided=1)
    rows = core.triage("T")
    rows[1]["review_batch"] = None
    core.write_jsonl(core.jdir("T") / "triage.jsonl", rows)
    import shutil
    shutil.rmtree(core.jdir("T") / "decisions")
    (core.jdir("T") / "decisions").mkdir()
    plan = batch.plan("T")
    assert [[x["section_id"] for x in b] for b in plan] == [["T:TA 2"]]
    assert batch.main("T") == 0
    assert core.triage("T")[1]["review_batch"] == 1
    assert batch.plan("T") == []                     # rerun adds nothing
