"""Shared fixtures: a temporary legal-engine root with a small jurisdiction (T, parent P) built from scratch."""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from pipeline import core  # noqa: E402

SRC = "The landlord shall return the deposit within fourteen days after the tenant vacates.\n"


def rule(rid, **kw):
    r = {"id": rid, "jurisdiction": rid.split(":")[0], "instrument": "Test Act", "provision": "TA 1",
         "effective_from": "2020-01-01", "effective_to": "", "actor": "landlord", "modality": "must",
         "condition": "The tenancy ends.", "effect": "Return the deposit within 14 days.", "determinacy": "RULE",
         "judgment_terms": [], "dependencies": [], "source_file": "jurisdictions/T/texts/T_TA/1.txt",
         "source_url": "https://example.test/ta/1", "quote": "return the deposit within fourteen days"}
    r.update(kw)
    return r


@pytest.fixture
def root(tmp_path):
    old = core.ROOT
    core.set_root(tmp_path)
    from pipeline import init
    assert init.main("P", "federal", None, "Parent") == 0
    assert init.main("T", "state", "P", "Test State") == 0
    d = core.jdir("T")
    (d / "texts" / "T_TA").mkdir(parents=True)
    (d / "texts" / "T_TA" / "1.txt").write_text(core.header("https://example.test/ta/1", "test") + SRC)
    (d / "texts" / "T_TA" / "2.txt").write_text(core.header("https://example.test/ta/2", "test") + "Definitions.\n")
    core.write_json(d / "rules.json", {"jurisdiction": "T", "layer": "state", "parents": ["P"],
                                       "atoms": [rule("T:TA-1-return")], "external_references": {}})
    yield tmp_path
    core.set_root(old)


def write_register(code, n_undecided=0):
    """Two sections, one stated by match, one decided by a reviewer (batch 1), in jurisdiction code."""
    d = core.jdir(code)
    inst = core.instruments(code)
    inst["instruments"] = [{"id": f"{code}:TA", "jurisdiction": code, "name": "Test Act", "level": "statute",
                            "functions": ["deposit"], "units_in_scope": [{"unit": "ch. 1", "heading": "all", "sections": 2}],
                            "units_out": [], "toc_source_url": "https://example.test/ta", "adapter": "generic"}]
    inst["non_code_sources"] = [{"instrument": "Test Act", "atom_ids": [f"{code}:TA-1-return"]}]
    core.write_json(d / "instruments.json", inst)
    secs = [{"section_id": f"{code}:TA 1", "instrument": f"{code}:TA", "unit": "ch. 1", "heading": "Return",
             "text_file": f"jurisdictions/{code}/texts/{code}_TA/1.txt", "chars": 80, "repealed": False},
            {"section_id": f"{code}:TA 2", "instrument": f"{code}:TA", "unit": "ch. 1", "heading": "Definitions",
             "text_file": f"jurisdictions/{code}/texts/{code}_TA/2.txt", "chars": 12, "repealed": False}]
    core.write_jsonl(d / "sections.jsonl", secs)
    tri = [{"section_id": f"{code}:TA 1", "instrument": f"{code}:TA", "unit": "ch. 1", "match_rule_ids": [f"{code}:TA-1-return"],
            "route": "stated", "review_decision": "stated", "decided_by": "match", "rule_ids": [f"{code}:TA-1-return"]},
           {"section_id": f"{code}:TA 2", "instrument": f"{code}:TA", "unit": "ch. 1", "match_rule_ids": [],
            "route": "review_queue", "review_decision": None if n_undecided else "no_decision",
            "decided_by": None if n_undecided else "reviewer", "review_batch": None if n_undecided else 1, "rule_ids": []}]
    core.write_jsonl(d / "triage.jsonl", tri)
    core.write_json(d / "decisions" / "batch_1.json", {"batch": 1, "sections": [{"section_id": f"{code}:TA 2"}]})
    if not n_undecided:
        core.write_jsonl(d / "decisions" / "decisions_1.jsonl", [{"section_id": f"{code}:TA 2", "decision": "no_decision",
                                                                  "reason": "Defines terms no rule uses.", "atom_ids": []}])
