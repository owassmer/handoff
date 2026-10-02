"""Rule checks (gate J6): the same checks as stage_a_check.py, per jurisdiction, with ids resolved across layers.

A rules.json fails when:
  - a rule lacks a required field or uses an unknown determinacy;
  - a STANDARD or MIXED rule has no judgment_terms;
  - a rule's quote is not verbatim (whitespace-normalized) in its saved source file;
  - a construction quote is not verbatim in its source, or a rule has construction entries but no reasoning;
  - a rule's condition, effect or reasoning uses hedging or weight words;
  - a rule id is duplicated, or a dependency names an id that is neither a rule in the file nor a declared
    external reference;
  - the file lists an open question (bounded_unknowns);
  - an external reference into another jurisdiction that exists in jurisdictions/ names nothing there
    (stage_a_check.py's cross-file check, run over every existing layer instead of the files on the command line).
"""
from __future__ import annotations

import copy
import json
import tempfile

from . import core


def check_data(d, code, other=None, hedge=None):
    """Errors for one rules document d. other: {code: set of ids and declared references} for cross-layer refs."""
    errs = []
    atoms = d.get("atoms", [])
    ids = [a.get("id") for a in atoms]
    seen, dup = set(), set()
    for i in ids:
        (dup if i in seen else seen).add(i)
    if dup:
        errs.append(f"duplicate ids: {sorted(dup)}")
    known = set(ids) | set(d.get("external_references", {}))
    for a in atoms:
        miss = [k for k in core.RULE_REQUIRED if k not in a]
        if miss:
            errs.append(f"{a.get('id')}: missing {miss}")
            continue
        if a["determinacy"] not in core.DETERMINACY:
            errs.append(f"{a['id']}: determinacy {a['determinacy']}")
        if a["determinacy"] != "RULE" and not a.get("judgment_terms"):
            errs.append(f"{a['id']}: STANDARD/MIXED needs judgment_terms")
        e = core.verbatim(a["source_file"], a["quote"])
        if e:
            errs.append(f"{a['id']}: {e}")
        for c in a.get("construction", []) or []:
            e = core.verbatim(c.get("source_file", ""), c.get("quote", ""))
            if e:
                errs.append(f"{a['id']}: construction {e}")
        if a.get("construction") and not a.get("reasoning"):
            errs.append(f"{a['id']}: construction without reasoning")
        for field in ("condition", "effect", "reasoning"):
            m = (hedge or core.HEDGE).search(str(a.get(field, "")))
            if m:
                errs.append(f"{a['id']}: hedging in {field}: '{m.group(0)}'")
        for dep in a["dependencies"]:
            if dep not in known:
                errs.append(f"{a['id']}: dependency {dep} is not a rule or declared external reference")
    for u in d.get("bounded_unknowns", []) or []:
        errs.append(f"open question {u.get('id')}: resolve it into rules")
    for ref in d.get("external_references", {}):
        target = ref.split(":")[0]
        if other and target in other and target != code and ref not in other[target]:
            errs.append(f"{ref} is not a rule or declared reference in jurisdictions/{target}/rules.json")
    return errs


def others():
    out = {}
    for c in core.codes():
        d = core.load_rules(c)
        out[c] = {a["id"] for a in d.get("atoms", [])} | set(d.get("external_references", {}))
    return out


def check(code, legacy_hedge=False):
    d = core.load_rules(code)
    return check_data(d, code, others(), core.HEDGE_LEGACY if legacy_hedge else None), len(d.get("atoms", []))


# ---------- self-test ----------

def self_test():
    """Plant one defect of each kind into a copy of a valid rule and confirm each is caught."""
    with tempfile.TemporaryDirectory() as td:
        src = core.pathlib.Path(td) / "src.txt"
        src.write_text("SOURCE: https://example.test/1\nRETRIEVED: 2026-01-01 via test\n\nThe landlord shall return "
                       "the deposit within fourteen days.\n")
        old_root = core.ROOT
        core.set_root(td)
        try:
            good = {"id": "T:good", "jurisdiction": "T", "instrument": "Test Act", "provision": "s 1",
                    "effective_from": "2020-01-01", "effective_to": "", "actor": "landlord", "modality": "must",
                    "condition": "The tenancy ends.", "effect": "Return the deposit within 14 days.",
                    "determinacy": "RULE", "judgment_terms": [], "dependencies": [], "source_file": "src.txt",
                    "source_url": "https://example.test/1", "quote": "return the deposit within fourteen days"}
            base = {"jurisdiction": "T", "atoms": [good], "external_references": {}}
            if check_data(base, "T"):
                return False, "clean fixture failed: " + "; ".join(check_data(base, "T"))
            plants = {  # name: (plant, text the error must contain)
                "missing field": (lambda a: a.pop("actor"), "missing ['actor']"),
                "determinacy": (lambda a: a.update(determinacy="MAYBE"), "determinacy MAYBE"),
                "judgment terms": (lambda a: a.update(determinacy="STANDARD"), "needs judgment_terms"),
                "quote": (lambda a: a.update(quote="return the deposit within thirty days"), "quote not verbatim"),
                "construction": (lambda a: a.update(construction=[{"source_file": "src.txt",
                                                                   "quote": "The landlord shall"}]),
                                 "construction without reasoning"),
                "hedging": (lambda a: a.update(effect="The deadline is arguably 14 days."), "hedging in effect"),
                "dependency": (lambda a: a.update(dependencies=["T:nothing"]), "dependency T:nothing"),
            }
            results = {}
            for name, (f, want) in plants.items():
                d = copy.deepcopy(base)
                f(d["atoms"][0])
                results[name] = any(want in e for e in check_data(d, "T"))
            d = copy.deepcopy(base)
            d["atoms"].append(copy.deepcopy(good))
            results["duplicate"] = any("duplicate" in e for e in check_data(d, "T"))
            d = copy.deepcopy(base)
            d["bounded_unknowns"] = [{"id": "Q1"}]
            results["open question"] = any("open question" in e for e in check_data(d, "T"))
            d = copy.deepcopy(base)
            d["external_references"] = {"P:missing": "parent rule"}
            results["cross-layer"] = any("P:missing" in e for e in check_data(d, "T", {"P": {"P:other"}}))
        finally:
            core.set_root(old_root)
    missed = [k for k, v in results.items() if not v]
    return not missed, ("all planted defects caught: " + ", ".join(results)) if not missed else f"NOT CAUGHT: {missed}"


def main(code_list, legacy_hedge=False):
    bad = False
    ok, msg = self_test()
    print(f"rule check self-test: {msg}")
    bad |= not ok
    cross = 0
    for c in code_list:
        errs, n = check(c, legacy_hedge)
        print(f"{c}: {n} rules, {len(errs)} errors")
        for e in errs:
            print("  ", e)
        cross += sum(1 for e in errs if "is not a rule or declared reference in jurisdictions/" in e)
        bad |= bool(errs)
    print(f"cross-layer: {cross} errors" + (" (hedge list: stage_a_check.py's)" if legacy_hedge else ""))
    return 1 if bad else 0


if __name__ == "__main__":  # pragma: no cover
    import sys
    sys.exit(main(sys.argv[1:] or core.codes()))
