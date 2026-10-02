"""Build exact development requests from reviewed source selections; no model calls or routing writes.

Run from any directory: python3 <this file> --output-dir /tmp/handoff-dependency-inputs
The output requests contain neither expected answers nor agent review notes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ASSEMBLER_VERSION = "draft-2"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(obj):
    return sha(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def read(path):
    return json.loads(path.read_text())


def assemble(root=ROOT, design=HERE):
    sources = read(design / "sources.json")
    contracts = read(design / "questions.json")
    cases = read(design / "examples.json")["cases"]
    model = read(root / "pipeline/jev_questions.json")
    texts = {}
    for key, source in sources["sources"].items():
        path = (root / source["path"]).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError(f"Source outside research root: {key}")
        raw = path.read_bytes()
        if sha(raw) != source["sha256"]:
            raise ValueError(f"Source changed: {key}; review and version examples before rebuilding")
        texts[key] = raw.decode("utf-8")
    passages = {}
    for key, passage in sources["passages"].items():
        start, end = passage["start"], passage["end"]
        text = texts[passage["source"]]
        if not 0 <= start < end <= len(text) or text[start:end] != passage["text"]:
            raise ValueError(f"Invalid exact source span: {key}")
        source = sources["sources"][passage["source"]]
        passages[key] = {"section_id": source["section_id"], "provision": passage["provision"],
                         "source_sha256": source["sha256"],
                         "start": start, "end": end, "text": text[start:end]}
    requests, expectations = [], []
    seen = set()
    for case in cases:
        if case["id"] in seen:
            raise ValueError(f"Duplicate case: {case['id']}")
        seen.add(case["id"])
        task = contracts["questions"][case["task"]]
        if set(case["state"]) != set(task["required_state_fields"]):
            raise ValueError(f"Unexpected or missing state fields: {case['id']}")
        state = {}
        for key, value in case["state"].items():
            if isinstance(value, dict) and "passage" in value:
                if set(value) != {"passage"}:
                    raise ValueError(f"Extra passage fields: {case['id']}:{key}")
                state[key] = passages[value["passage"]]
            elif key.endswith("_location"):
                if not isinstance(value, dict) or set(value) != {"instrument", "unit", "section_id"}:
                    raise ValueError(f"Invalid location: {case['id']}:{key}")
                state[key] = value
            elif key == "term" and isinstance(value, str) and value:
                state[key] = value
            else:
                raise ValueError(f"Invalid state value: {case['id']}:{key}")
        question = {k: task[k] for k in ("primitive", "instructions", "criteria")}
        payload = {"model": model["model"], "questions": {case["task"]: question}, "state": state}
        identity = {"assembler_version": ASSEMBLER_VERSION, "task_version": task["version"],
                    "pinned_build": model["pinned_build"], "payload": payload}
        expected = case["review"]["expected"]
        if expected not in question["criteria"]:
            raise ValueError(f"Unknown expected answer: {case['id']}")
        key = digest(identity)
        requests.append({"case_id": case["id"], "request_hash": key, **identity})
        expectations.append({"case_id": case["id"], "request_hash": key, **case["review"]})
    return requests, expectations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    requests, expectations = assemble()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in (("requests.jsonl", requests), ("expectations.jsonl", expectations)):
        (args.output_dir / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"Verified sources and spans; prepared {len(requests)} requests and separate development expectations.")
    print("No model calls. No accuracy measurement. Send only each request's payload through an SDK adapter.")


if __name__ == "__main__":
    main()
