"""Protect the boundary between reviewed examples and the material sent to Jev."""
import json
import shutil

import pytest

from pipeline.design.agent_jev_code import prepare


@pytest.fixture
def development_copy(tmp_path):
    root = tmp_path / "research"
    design = root / "pipeline/design/agent_jev_code"
    shutil.copytree(prepare.HERE, design, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(prepare.ROOT / "pipeline/jev_questions.json", root / "pipeline/jev_questions.json")
    for source in prepare.read(design / "sources.json")["sources"].values():
        target = root / source["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(prepare.ROOT / source["path"], target)
    return root, design


def save(path, obj):
    path.write_text(json.dumps(obj))


def test_labels_and_agent_conclusions_cannot_change_model_inputs(development_copy):
    root, design = development_copy
    before, labels = prepare.assemble(root, design)
    examples = prepare.read(design / "examples.json")
    for case in examples["cases"]:
        case["review"]["expected"] = "NO"
        case["review"]["reason"] = "ORACLE_SENTINEL"
        case["review"]["agent_next_action"] = "ORACLE_SENTINEL"
    save(design / "examples.json", examples)
    after, changed_labels = prepare.assemble(root, design)
    assert before == after
    assert labels != changed_labels
    assert "ORACLE_SENTINEL" not in json.dumps(after)
    assert len(before) == 22
    assert all(len(row["payload"]["questions"]) == 1 for row in before)


@pytest.mark.parametrize("corruption", ["source", "span", "state_label", "nested_label", "missing_field"])
def test_invalid_preparation_fails_before_output(development_copy, corruption):
    root, design = development_copy
    sources = prepare.read(design / "sources.json")
    examples = prepare.read(design / "examples.json")
    if corruption == "source":
        path = root / next(iter(sources["sources"].values()))["path"]
        path.write_text(path.read_text() + "changed")
    elif corruption == "span":
        next(iter(sources["passages"].values()))["start"] += 1
        save(design / "sources.json", sources)
    elif corruption == "state_label":
        examples["cases"][0]["state"]["expected"] = "YES"
        save(design / "examples.json", examples)
    elif corruption == "nested_label":
        examples["cases"][0]["state"]["focus"]["expected"] = "YES"
        save(design / "examples.json", examples)
    else:
        del examples["cases"][0]["state"]["focus"]
        save(design / "examples.json", examples)
    with pytest.raises(ValueError):
        prepare.assemble(root, design)


def test_request_identity_changes_with_build_and_context(development_copy):
    root, design = development_copy
    before, _ = prepare.assemble(root, design)
    path = root / "pipeline/jev_questions.json"
    model = prepare.read(path)
    model["pinned_build"] += "-different-build"
    save(path, model)
    after, _ = prepare.assemble(root, design)
    assert all(a["request_hash"] != b["request_hash"] for a, b in zip(before, after))
    examples = prepare.read(design / "examples.json")
    examples["cases"][0]["state"]["focus"] = {"passage": "notice_c"}
    save(design / "examples.json", examples)
    changed, _ = prepare.assemble(root, design)
    assert after[0]["request_hash"] != changed[0]["request_hash"]
    assert after[1:] == changed[1:]


def test_missing_context_control_does_not_leak_hierarchy(development_copy):
    root, design = development_copy
    requests, labels = prepare.assemble(root, design)
    row = next(r for r in requests if r["case_id"] == "dev13")
    state = row["payload"]["state"]
    assert state["use_location"]["unit"] is None
    assert "unit" not in state["use"]
    assert "path" not in state["use"]
    assert "INSUFFICIENT" == next(r["expected"] for r in labels if r["case_id"] == "dev13")
