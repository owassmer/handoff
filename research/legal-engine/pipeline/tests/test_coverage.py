"""Adverse consistency and persistence cases, not proof of legal sufficiency."""
import copy
import json
import multiprocessing
import os
import sqlite3

import pytest

from pipeline import core, coverage as c


@pytest.fixture
def research(tmp_path):
    old = core.ROOT
    core.set_root(tmp_path)
    (tmp_path / "jurisdictions/T").mkdir(parents=True)
    core.write_json(tmp_path / "jurisdictions/T/profile.json", {"code": "T"})
    for name in ("source", "finding", "review", "toc", "currentness"):
        (tmp_path / f"{name}.txt").write_text(f"Synthetic {name} evidence for consistency tests.")
    ref = lambda name: c.artifact(f"{name}.txt", "entire synthetic fixture")
    core.write_json(tmp_path / "inventory.json", {"source_ids": ["A"], "method": "Fixture enumeration",
                                                "evidence": [ref("toc")]})
    doc = {"schema": 1, "scope_id": "test", "jurisdiction": "T", "purpose": "Resolve the account",
           "scope": "Fixture source A and its operating question", "author": "author", "as_of": "2026-10-01",
           "next_action": "Investigate the named defect and obtain independent recheck.",
           "items": [{"id": "A", "kind": "source", "title": "Fixture A", "status": "resolved",
                      "author": "author", "decisions": ["return property without unsupported storage charges"],
                      "next_action": "Reinvestigate if evidence changes", "conclusion": "Fixture conclusion",
                      "evidence": [ref("finding")], "source": {"selected_version": "v1", "versions": [
                          {"id": "v1", "url": "https://example.org/source", "retrieved_at": "2026-10-01",
                           "effective_from": "2025-01-01", "effective_to": None,
                           "temporal_basis": "Fixture current edition", "evidence": ref("source")}],
                          "applies_on": "2026-10-01", "checked_through": "2026-10-01",
                          "recheck_on": "2026-11-01", "currentness_evidence": ref("currentness")}}],
           "boundaries": [{"id": "unit", "description": "Fixture authoritative unit", "author": "author",
                           "source_ids": ["A"], "enumeration_complete": True,
                           "next_action": "Reconcile inventory", "inventory": c.artifact("inventory.json", "source_ids and evidence")}],
           "dependencies": [], "reviews": []}
    approve(doc, ref("review"))
    yield doc, tmp_path
    core.set_root(old)


def approve(doc, evidence):
    for kind, target in [("item", i["id"]) for i in doc["items"]] + [
            ("boundary", b["id"]) for b in doc["boundaries"]] + [("scope", doc["scope_id"])]:
        doc["reviews"].append({"id": f"review-{len(doc['reviews'])}", "target_kind": kind,
            "target_id": target, "target_sha256": c.review_digest(doc, kind, target), "reviewer": "independent",
            "result": "pass", "unresolved_findings": [], "summary": "Synthetic independent fixture",
            "checked": ["enumeration", "interpretation", "dependencies"], "evidence": evidence})


def problems(doc, **kw):
    return "\n".join(p["problem"] for p in c.assess(doc, **kw)["problems"])


def test_closure_and_open_work(research):
    doc, _ = research
    assert c.assess(doc)["complete"]
    doc["items"][0]["status"] = "open"
    doc["items"][0]["jev"] = {"answer": "NO"}
    report = c.assess(doc)
    assert not report["complete"]
    assert all(p["decisions"] and p["next_action"] for p in report["problems"])


@pytest.mark.parametrize("name", ["source", "finding", "review", "toc", "currentness"])
def test_external_evidence_change_blocks(research, name):
    doc, root = research
    (root / f"{name}.txt").write_text("changed")
    assert "changed evidence" in problems(doc)


def test_equal_count_wrong_source_and_live_register(research):
    doc, root = research
    doc["boundaries"][0]["register_selector"] = {"instrument": "I", "units": ["U"]}
    core.write_jsonl(root / "jurisdictions/T/sections.jsonl", [{"section_id": "B", "instrument": "I", "unit": "U"}])
    approve(doc, c.artifact("review.txt", "fixture"))
    assert "register membership differs" in problems(doc)
    doc["boundaries"][0]["source_ids"] = ["B"]
    assert "enumerated source missing: B" in problems(doc)
    assert "enumeration membership" in problems(doc)


def test_dependency_transitive_invalidation_and_cycle(research):
    doc, _ = research
    for key in ("B", "C"):
        item = copy.deepcopy(doc["items"][0])
        item.update(id=key, kind="question")
        item.pop("source")
        doc["items"].append(item)
    doc["dependencies"] = [{"id": a+b, "from": a, "to": b, "status": "required", "reason": "changes decision"}
                           for a, b in [("A", "B"), ("B", "C"), ("C", "A")]]
    approve(doc, c.artifact("review.txt", "fixture"))
    assert c.assess(doc)["complete"]
    before = {i["id"]: c.review_digest(doc, "item", i["id"]) for i in doc["items"]}
    doc["items"][-1]["conclusion"] = "materially different"
    assert all(c.review_digest(doc, "item", key) != value for key, value in before.items())
    assert not c.assess(doc)["complete"]


def test_unknown_and_excluded_dependency(research):
    doc, _ = research
    doc["dependencies"].append({"id": "unknown", "from": "A", "to": "other applicable law",
                                "status": "required", "reason": "additional protection"})
    assert "untracked dependency endpoint" in problems(doc)
    doc["dependencies"][0]["to"] = "A"
    doc["items"][0]["status"] = "excluded"
    assert "cannot be satisfied by excluded" in problems(doc)


def test_dates_and_older_edition(research):
    doc, _ = research
    assert "currentness not investigated" in problems(doc, as_of="2026-10-02")
    doc["items"][0]["source"]["applies_on"] = "2024-12-31"
    assert "version does not apply" in problems(doc)
    assert "recheck due" in problems(doc, as_of="2026-11-01")


def test_review_independence_and_later_challenge(research):
    doc, _ = research
    doc["reviews"][0]["reviewer"] = "author"
    assert "distinct" in problems(doc)
    approve(doc, c.artifact("review.txt", "fixture"))
    doc["reviews"][-1]["result"] = "changes_required"
    assert "unresolved findings" in problems(doc)


def test_revisions_cas_no_silent_scope_loss(research):
    doc, _ = research
    assert c.save("T", doc, 0) == 1
    assert c.save("T", doc, 1) == 1
    next_doc = copy.deepcopy(doc)
    next_doc["items"][0]["status"] = "investigating"
    assert c.save("T", next_doc, 1) == 2
    with pytest.raises(core.PipelineError, match="stale update"):
        c.save("T", doc, 1)
    assert c.load("T", "test", 1)[1] == doc
    assert c.load("T", "test")[1] == next_doc
    next_doc["items"] = []
    with pytest.raises(core.PipelineError, match="cannot remove"):
        c.save("T", next_doc, 2)


def test_source_versions_and_reviews_immutable(research):
    doc, _ = research
    c.save("T", doc, 0)
    doc["items"][0]["source"]["versions"][0]["temporal_basis"] = "rewrite history"
    with pytest.raises(core.PipelineError, match="versions are immutable"):
        c.save("T", doc, 1)
    doc = c.load("T", "test")[1]
    doc["reviews"][0]["summary"] = "rewritten"
    with pytest.raises(core.PipelineError, match="reviews are immutable"):
        c.save("T", doc, 1)


def crash_write(db_path):
    db = sqlite3.connect(db_path)
    db.execute("BEGIN IMMEDIATE")
    db.execute("UPDATE revisions SET payload='corrupt uncommitted work'")
    os._exit(3)


def test_process_death_rolls_back_and_resume_releases_lock(research):
    doc, _ = research
    c.save("T", doc, 0)
    proc = multiprocessing.get_context("spawn").Process(target=crash_write, args=(str(c.database("T")),))
    proc.start()
    proc.join(10)
    assert proc.exitcode == 3
    assert c.load("T", "test")[1] == doc
    doc["next_action"] = "resumed investigation"
    assert c.save("T", doc, 1) == 2


def test_corrupt_history_not_silently_rolled_back(research):
    doc, _ = research
    c.save("T", doc, 0)
    with sqlite3.connect(c.database("T")) as db:
        db.execute("UPDATE revisions SET payload='{}'")
    with pytest.raises(core.PipelineError, match="integrity"):
        c.load("T", "test")


def test_registry_seed_never_accepts_legacy_or_model_labels(research):
    _, root = research
    core.write_jsonl(root / "jurisdictions/T/sections.jsonl", [{"section_id": "A", "instrument": "I", "unit": "U",
                                                               "text_file": "source.txt"}])
    core.write_jsonl(root / "jurisdictions/T/triage.jsonl", [{"section_id": "A", "review_decision": "no_decision",
                                                           "jev": {"answer": "NO"}}])
    doc = c.seed("T", "import", "Resolve account", "agent")
    assert doc["items"][0]["status"] == "open"
    assert not c.assess(doc)["complete"]


def test_empty_scope_never_complete(research):
    doc, _ = research
    doc.update(items=[], boundaries=[], dependencies=[], reviews=[])
    approve(doc, c.artifact("review.txt", "fixture"))
    assert not c.assess(doc)["complete"]


def test_review_reorder_cannot_hide_later_rejection(research):
    doc, _ = research
    challenge = copy.deepcopy(doc["reviews"][0])
    challenge.update(id="later-challenge", result="changes_required", unresolved_findings=["missing dependency"])
    doc["reviews"].append(challenge)
    c.save("T", doc, 0)
    assert not c.assess(doc)["complete"]
    doc["reviews"].insert(0, doc["reviews"].pop())
    with pytest.raises(core.PipelineError, match="ordered"):
        c.save("T", doc, 1)


def test_register_rebinding_same_id_requires_reinvestigation(research):
    doc, root = research
    row = {"section_id": "A", "instrument": "I", "unit": "U", "text_file": "source.txt"}
    core.write_jsonl(root / "jurisdictions/T/sections.jsonl", [row])
    doc["boundaries"][0]["register_selector"] = {"instrument": "I", "units": ["U"]}
    doc["items"][0]["register_record_sha256"] = c.digest(row)
    approve(doc, c.artifact("review.txt", "fixture"))
    assert c.assess(doc)["complete"]
    row["text_file"] = "new-edition.txt"
    core.write_jsonl(root / "jurisdictions/T/sections.jsonl", [row])
    assert "register source/version differs" in problems(doc)


def test_missing_versions_rejected_before_persistence(research):
    doc, _ = research
    del doc["items"][0]["source"]["versions"]
    with pytest.raises(core.PipelineError, match="source versions"):
        c.save("T", doc, 0)


def test_followup_preserves_negative_and_broad_leads_open(research):
    doc, root = research
    followup = {"scope": "prepared experiment", "rows": [
        {"case_id": "one", "expression": "existing law", "jev_noul": 0.01,
         "diagnostic_majority": "NO", "targets": [], "followup": "Investigate applicable background law"}],
        "next_dependencies": [{"targets": ["unknown local protections"], "cause": "Can change the remedy"}]}
    core.write_json(root / "followup.json", followup)
    result = c.import_followup(doc, "followup.json", "author")
    assert len(result["items"]) == 4
    assert all(i["status"] == "open" for i in result["items"][1:])
    assert result["items"][1]["observation"] == followup["rows"][0]
    c.save("T", result, 0)
    removed = copy.deepcopy(result)
    removed["imports"] = []
    with pytest.raises(core.PipelineError, match="cannot remove imports"):
        c.save("T", removed, 1)
    (root / "followup.json").write_text("changed")
    assert "changed evidence" in problems(result)


def test_seed_binds_bytes_used_to_parse_not_later_inventory(research, monkeypatch):
    _, root = research
    path = root / "jurisdictions/T/sections.jsonl"
    row = {"section_id": "A", "instrument": "I", "unit": "U", "text_file": "source.txt"}
    core.write_jsonl(path, [row])
    original = type(path).read_bytes
    changed = False

    def raced_read(p):
        nonlocal changed
        data = original(p)
        if p == path and not changed:
            changed = True
            core.write_jsonl(path, [row, {**row, "section_id": "B", "unit": "new-unit"}])
        return data

    monkeypatch.setattr(type(path), "read_bytes", raced_read)
    doc = c.seed("T", "raced", "Return property", "agent")
    assert [i["id"] for i in doc["items"]] == ["A"]
    assert "changed evidence" in problems(doc)


def test_historical_source_version_requires_distinct_review(research):
    doc, _ = research
    c.save("T", doc, 0)
    src = doc["items"][0]["source"]
    src["applies_on"] = "2024-12-31"
    assert "version does not apply" in problems(doc)
    earlier = copy.deepcopy(src["versions"][0])
    earlier.update(id="earlier", effective_from="2024-01-01", effective_to="2025-01-01",
                   temporal_basis="Synthetic predecessor version; fixture only")
    src["versions"].append(earlier)
    src["selected_version"] = "earlier"
    assert "version does not apply" not in problems(doc)
    assert not c.assess(doc)["complete"]
    approve(doc, c.artifact("review.txt", "new historical-version review fixture"))
    assert c.assess(doc)["complete"]
    assert c.save("T", doc, 1) == 2
    assert len(c.load("T", "test")[1]["items"][0]["source"]["versions"]) == 2


def test_completed_research_links_keep_accepted_scope_and_detect_change(research):
    doc, root = research
    sha = core.sha256_file(root / "finding.txt")
    (root / "prior-review.txt").write_text("Prior independent acceptance: " + sha)
    core.write_json(root / "verification.json", {"review_bindings": [
        {"finding": "finding.txt", "review": "prior-review.txt", "sha256": sha,
         "review_contains_current_hash": True}]})
    linked = c.link_completed_research(doc, "verification.json")
    assert len(linked["completed_research"]) == 1
    assert not c.assess(linked)["complete"]  # new scope content still needs review
    c.save("T", linked, 0)
    removed = copy.deepcopy(linked)
    removed["completed_research"] = []
    with pytest.raises(core.PipelineError, match="cannot remove completed_research"):
        c.save("T", removed, 1)
    (root / "finding.txt").write_text("New unreviewed claim")
    assert "changed evidence" in problems(linked)


def test_aggregate_report_does_not_hide_open_broader_scope(research):
    doc, _ = research
    c.save("T", doc, 0)
    broad = copy.deepcopy(doc)
    broad.update(scope_id="broader", reviews=[])
    broad["items"][0]["status"] = "open"
    c.save("T", broad, 0)
    summary = c.jurisdiction_summary("T")
    assert not summary["complete"]
    assert {r["scope_id"] for r in summary["scopes"]} == {"test", "broader"}


def test_seed_keeps_unharvested_units_and_pending_families(research):
    _, root = research
    core.write_json(root / "jurisdictions/T/instruments.json", {
        "instruments": [{"id": "I", "units_in_scope": [{"unit": "unharvested", "sections": None}]}],
        "discovery_status": "open", "pending_source_families": ["local ordinances"],
        "fetch_gaps": {"section_gaps": [{"section_id": "I:missing", "reason": "retrieval failed"}]}})
    doc = c.seed("T", "pending", "Resolve account", "agent")
    assert len(doc["boundaries"]) == 1
    assert doc["boundaries"][0]["source_ids"] == []
    assert {i["title"] for i in doc["items"]} >= {"local ordinances", "Establish the complete applicable source universe"}
    assert any("retrieval failed" in str(i) for i in doc["items"])
    assert not c.assess(doc)["complete"]


@pytest.mark.parametrize("field,value", [("selected_version", []), ("versions", None)])
def test_malformed_source_shape_cannot_commit(research, field, value):
    doc, _ = research
    doc["items"][0]["source"][field] = value
    with pytest.raises(core.PipelineError):
        c.save("T", doc, 0)


def test_whitespace_conclusion_and_nontext_review_are_not_acceptance(research):
    doc, _ = research
    doc["items"][0]["conclusion"] = "  "
    approve(doc, c.artifact("review.txt", "fixture"))
    assert "substantive conclusion" in problems(doc)
    doc["items"][0]["conclusion"] = "Supported fixture conclusion"
    approve(doc, c.artifact("review.txt", "fixture"))
    doc["reviews"][-1]["checked"] = [True]
    assert "substantive checks" in problems(doc)
