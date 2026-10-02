"""The command table: every skill command is dispatched; harvest never refetches and records gaps with routes; diff
lists changed sections and their rules; check reports the stage reached."""
import json

import pytest

from pipeline import __main__ as cli
from pipeline import adapters, check, core, diff, harvest, match

SKILL_COMMANDS = ["init", "instruments", "harvest", "match", "calibrate", "triage", "batch", "check-decisions", "apply",
                  "authorities", "check", "show", "diff"]


def test_every_skill_command_is_dispatched():
    choices = cli.parser()._subparsers._group_actions[0].choices
    assert set(SKILL_COMMANDS) <= set(choices)


class FakeAdapter:
    name = "fake"
    calls = 0
    texts = {"1": "The landlord shall return the deposit within fourteen days after the tenant vacates.",
             "2": "Definitions.", "3": None}

    def toc(self, instrument, unit):
        return [{"number": n, "heading": f"Section {n}", "ref": n} for n in ("1", "2", "3")]

    def section(self, ref):
        FakeAdapter.calls += 1
        t = self.texts[ref]
        if t is None:
            raise core.PipelineError("fake: every route failed for x (curl 403; browser failed; archive no capture)")
        return {"text": t, "source_url": f"https://example.test/ta/{ref}", "route": "curl", "extra": {}}

    def save(self, path, sec):
        from pipeline.adapters.base import Adapter
        return Adapter.save(self, path, sec)


@pytest.fixture
def fake(root, monkeypatch):
    fa = FakeAdapter()
    FakeAdapter.calls = 0
    monkeypatch.setattr(adapters, "get", lambda name: fa)
    inst = core.instruments("T")
    inst["instruments"] = [{"id": "T:TB", "jurisdiction": "T", "name": "Test B", "level": "statute", "functions": ["deposit"],
                            "units_in_scope": [{"unit": "ch. 1", "heading": "all", "toc_url": "https://example.test/tb"}],
                            "units_out": [], "toc_source_url": "https://example.test/tb", "adapter": "generic"}]
    core.write_json(core.jdir("T") / "instruments.json", inst)
    return fa


def test_harvest_saves_never_refetches_and_records_gaps(fake):
    assert harvest.main("T") == 1                      # one section fails: J2 gate not met
    secs = {s["section_id"]: s for s in core.sections("T")}
    assert set(secs) == {"T:TB 1", "T:TB 2", "T:TB 3"}
    t1 = (core.ROOT / secs["T:TB 1"]["text_file"]).read_text()
    assert t1.startswith("SOURCE: https://example.test/ta/1") and "RETRIEVED:" in t1
    assert secs["T:TB 1"]["sha256"] == core.text_hash(t1) and secs["T:TB 3"]["text_file"] is None
    gap = core.instruments("T")["fetch_gaps"]["section_gaps"][0]
    assert gap["section_id"] == "T:TB 3" and gap["routes_tried"] == ["curl 403", "browser failed", "archive no capture"]
    assert core.instruments("T")["instruments"][0]["units_in_scope"][0]["sections"] == 3
    n = FakeAdapter.calls
    FakeAdapter.texts["3"] = "Now available."
    assert harvest.main("T") == 0
    assert FakeAdapter.calls == n + 1                  # only the missing section was fetched
    assert core.instruments("T")["fetch_gaps"]["section_gaps"] == []


def test_diff_lists_changed_sections_and_rules(fake):
    FakeAdapter.texts["3"] = "Now available."
    harvest.main("T")
    d = core.load_rules("T")
    d["atoms"][0]["source_file"] = core.sections("T")[0]["text_file"]
    core.write_json(core.rules_file("T"), d)
    assert diff.main("T") == 0                         # nothing changed
    FakeAdapter.texts["1"] = "The landlord shall return the deposit within twenty-one days after the tenant vacates."
    assert diff.main("T") == 1
    rep = json.loads(next((core.jdir("T") / "diff").glob("*/diff.json")).read_text())
    assert [c["section_id"] for c in rep["changed"]] == ["T:TB 1"]
    assert rep["changed"][0]["rules"] == ["T:TA-1-return"]
    saved = (core.ROOT / core.sections("T")[0]["text_file"]).read_text()
    assert "fourteen days" in saved                    # the saved text is not overwritten


def test_check_reports_stage(fake):
    FakeAdapter.texts["3"] = "Now available."
    res, reached = check.evaluate("T")
    assert reached == "none" and not res["J1"][0]
    assert check.main(["T"], "J1") == 1
