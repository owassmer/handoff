"""init (J0 step 1): create jurisdictions/<CODE>/ with a profile template and empty files.

  python3 -m pipeline init CA --layer state --parent US --name California
  python3 -m pipeline init CA-OAK --layer city --parent CA --name Oakland
Refuses an existing jurisdiction. The owner fills profile.json (courts, gates, customer units, aperture) and
confirms it (owner_confirmed) before J1.
"""
from __future__ import annotations

from . import core

LAYERS = ("federal", "state", "county", "city")


def profile_template(code, layer, parents, name):
    return {
        "code": code, "name": name or code, "layer": layer, "parents": parents, "status": "intake",
        "owner_confirmed": {"by": "", "date": "", "note": "Owen confirms the jurisdiction, its layers and exclusions (J0 gate)."},
        "courts": [{"id": "EXAMPLE-TRIAL", "name": "trial court where the customer's claims are heard", "binds": []},
                   {"id": "EXAMPLE-APPELLATE", "name": "appellate court", "binds": ["EXAMPLE-TRIAL"]}],
        "customer_courts": ["EXAMPLE-TRIAL"],
        "gates": [{"id": "building_age", "fact": "year the building was completed", "triggers": ""},
                  {"id": "unit_count", "fact": "number of units in the building", "triggers": ""},
                  {"id": "owner_occupancy", "fact": "the owner lives in the building", "triggers": ""},
                  {"id": "affordability", "fact": "regulatory agreement or income restriction", "triggers": ""},
                  {"id": "assistance", "fact": "tenant-based or project-based assistance", "triggers": ""},
                  {"id": "lease_date", "fact": "date the lease was signed or renewed", "triggers": ""}],
        "customer_units": [],
        "aperture": {"exclusions": "", "regime_units": []},
        "jev": {"scope": f"a residential unit in {name or code}",
                "chain_description": "The chain: from facts fixed at move-in and the notice that the tenancy is ending, "
                                     "to the account closed (including collection, suit, judgment, enforcement and "
                                     "write-off, unclaimed funds, bankruptcy, death, military, disability, domestic "
                                     "violence, tax and information reporting, data and privacy, credit reporting, "
                                     "anti-discrimination)."},
        "walk": {"scope_exclude": ""},
        "decision_points_not_applicable": [],
        "citations": {"order": 10, "patterns": [], "instrument_map": [], "label_aliases": {}, "file_patterns": [],
                      "example": {"patterns": [{"prefix": r"(?:Cal\.?\s*)?Civ(?:il)?\.?\s*Code", "key": "CIV",
                                                "number": r"\d+(?:\.\d+)*", "plain_range": False, "titled": False}],
                                  "instrument_map": [{"key": "CIV", "instrument": f"{code}:CIV"}]}},
        "acceptance": {"date": "", "by": "", "hashes": {}},
    }


def main(code, layer, parent, name=None):
    if core.exists(code):
        print(f"{code} already exists at {core.rel(core.jdir(code))}; nothing done")
        return 1
    if layer not in LAYERS:
        print(f"--layer must be one of {LAYERS}")
        return 1
    if layer != "federal" and not parent:
        print("--parent is required for a state, county or city layer")
        return 1
    if parent and not core.exists(parent):
        print(f"parent {parent} does not exist; init it first")
        return 1
    d = core.jdir(code)
    (d / "texts").mkdir(parents=True, exist_ok=True)
    (d / "decisions").mkdir(exist_ok=True)
    core.write_json(d / "profile.json", profile_template(code, layer, [parent] if parent else [], name))
    core.write_json(d / "instruments.json", {"jurisdiction": code, "instruments": [], "functions_without_instrument": [],
                                             "non_code_sources": [], "fetch_gaps": {"section_gaps": [], "instrument_gaps": []},
                                             "considered_not_added": []})
    (d / "sections.jsonl").write_text("")
    (d / "triage.jsonl").write_text("")
    core.write_json(d / "authorities.json", [])
    core.write_json(d / "adjudication.json", {"proposals": {}, "existing_rule_changes": [], "merges": []})
    core.write_json(d / "rules.json", {"jurisdiction": code, "layer": layer, "parents": [parent] if parent else [],
                                       "atoms": [], "external_references": {}})
    core.write_json(d / "calibration_negatives.json", {"negatives": []})
    (d / "walk.md").write_text(f"# {name or code}: the settlement walk\n\nWritten at J7 in chain-map order.\n")
    (d / "DISPOSITION.md").write_text(f"# {code} disposition\n\nEvery apply, in order, with counts and check output.\n")
    print(f"created {core.rel(d)} ({layer}, parents {[parent] if parent else []}); fill profile.json, then confirm it with the owner")
    return 0
