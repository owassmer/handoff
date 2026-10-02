"""One planted defect per checker: altered quote, hedge word, undeclared dependency, undecided section, uncited
rule, missing authority search. Each checker must pass the clean fixture and catch the planted defect."""
import copy

from pipeline import authorities, core, decisions, registercheck, rulecheck, walkcheck

from .conftest import rule, write_register


def rules_doc():
    return copy.deepcopy(core.load_rules("T"))


def test_clean_rules_pass(root):
    errs, n = rulecheck.check("T")
    assert n == 1 and errs == []


def test_open_source_discovery_cannot_pass_inventory(root):
    from pipeline import instruments
    write_register("T")
    doc = core.instruments("T")
    doc["discovery_status"] = "open"
    core.write_json(core.jdir("T") / "instruments.json", doc)
    assert any("source discovery is open" in e for e in instruments.check("T")[0])


def test_altered_quote(root):
    d = rules_doc()
    d["atoms"][0]["quote"] = "return the deposit within thirty days"
    assert any("quote not verbatim" in e for e in rulecheck.check_data(d, "T"))


def test_hedge_word(root):
    d = rules_doc()
    d["atoms"][0]["effect"] = "The deadline is arguably 14 days."
    assert any("hedging in effect" in e for e in rulecheck.check_data(d, "T"))
    d = rules_doc()
    d["atoms"][0]["reasoning"] = "In practice landlords wait."
    assert any("hedging in reasoning" in e for e in rulecheck.check_data(d, "T"))


def test_undeclared_dependency(root):
    d = rules_doc()
    d["atoms"][0]["dependencies"] = ["P:not-declared"]
    assert any("dependency P:not-declared" in e for e in rulecheck.check_data(d, "T"))
    d["external_references"] = {"P:not-declared": "parent rule"}
    assert not rulecheck.check_data(d, "T")


def test_undecided_section_register(root):
    write_register("T")
    dd = registercheck.load("T")
    assert registercheck.check(dd, verify_jev=False) == []
    write_register("T", n_undecided=1)
    dd = registercheck.load("T")
    assert any(e.startswith("[S]") and "T:TA 2" in e for e in registercheck.check(dd, verify_jev=False))


def test_undecided_section_decisions(root):
    write_register("T", n_undecided=1)
    errs, undecided, _, total = decisions.check_batch("T", 1, set(), {}, {})
    assert undecided == ["T:TA 2"] and total == 1


def test_decision_hedge_and_bad_quote(root):
    write_register("T")
    p = rule("T:TA-2-new", quote="not in the source at all", severity="major", walk_step="1.1")
    core.write_jsonl(core.jdir("T") / "decisions" / "decisions_1.jsonl", [
        {"section_id": "T:TA 2", "decision": "new_rule", "reason": "it is arguably relevant", "proposed": [p]}])
    errs, _, _, _ = decisions.check_batch("T", 1, core.known_ids(["T", "P"]), {}, {})
    assert any("hedging in reason" in e for e in errs) and any("not verbatim" in e for e in errs)


def test_merged_proposal(root):
    """A proposal merged by adjudication.json passes only when the target rule carries its quote."""
    write_register("T")
    p = rule("T:TA-2-merged", severity="minor", walk_step="1.1")
    for k in ("effective_from", "effective_to"):  # legacy proposals lack these; a merge is not re-checked field by field
        p.pop(k)
    core.write_jsonl(core.jdir("T") / "decisions" / "decisions_1.jsonl", [
        {"section_id": "T:TA 2", "decision": "new_rule", "reason": "States the deposit deadline.", "proposed": [p]}])
    known, rules = core.known_ids(["T", "P"]), core.rule_index(["T", "P"])
    errs, _, _, _ = decisions.check_batch("T", 1, known, rules, {})
    assert any("missing" in e for e in errs)                       # not merged: incomplete proposal is an error
    core.write_json(core.jdir("T") / "adjudication.json", {"proposals": {}, "existing_rule_changes": [],
                                                           "merges": [{"into": "T:TA-1-return", "from": ["T:TA-2-merged"]}]})
    errs, _, _, _ = decisions.check_batch("T", 1, known, rules, {})
    assert errs == []                                              # target carries the same quote
    p["quote"] = "within fourteen days after the tenant vacates"
    core.write_jsonl(core.jdir("T") / "decisions" / "decisions_1.jsonl", [
        {"section_id": "T:TA 2", "decision": "new_rule", "reason": "States the deposit deadline.", "proposed": [p]}])
    errs, _, _, _ = decisions.check_batch("T", 1, known, rules, {})
    assert any("does not carry the proposal's quote" in e for e in errs)


def test_uncited_rule_walk(root):
    d = core.load_rules("T")
    d["atoms"].append(rule("T:TA-1-second"))
    core.write_json(core.rules_file("T"), d)
    (core.jdir("T") / "walk.md").write_text("Step 1. The deposit comes back: `T:TA-1-return`.\n")
    errs, missing, summary = walkcheck.check("T")
    assert missing == ["T:TA-1-second"] and not errs
    (core.jdir("T") / "walk.md").write_text("Step 1. `T:TA-1-return`.\n\n- deferred: `T:TA-1-second`\n")
    errs, missing, summary = walkcheck.check("T")
    assert not missing and "deferred 1" in summary


def test_missing_authority_search(root):
    prof = core.profile("T")
    prof["courts"] = [{"id": "TRIAL", "binds": []}, {"id": "APP", "binds": ["TRIAL"]}]
    prof["customer_courts"] = ["TRIAL"]
    core.write_json(core.jdir("T") / "profile.json", prof)
    points = [p["id"] for d in core.chain_map()["decision_points"] for p in d["points"]]
    searches = [{"decision_point": p, "court": c, "query": f"{p} deposit", "date": "2026-09-30", "results": [], "ruling": ""}
                for p in points for c in ("APP",)]
    core.write_json(core.jdir("T") / "authorities.json", searches)
    errs, missing, n, courts = authorities.check("T")
    assert courts == ["APP"] and not errs and not missing
    core.write_json(core.jdir("T") / "authorities.json", searches[1:])
    errs, missing, n, courts = authorities.check("T")
    assert missing == [f"{points[0]} in APP"]


def test_self_tests():
    assert rulecheck.self_test()[0]
    assert decisions.self_test("T")
    assert walkcheck.self_test()[0]
