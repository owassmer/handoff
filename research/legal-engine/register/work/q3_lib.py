"""Reviewer q3 helpers: print chunks of batch 3 and write decisions idempotently.

Usage (from research/legal-engine):
    python3 register/work/q3_lib.py show <start> <end> [maxchars]   # print sections by batch index
    python3 register/work/q3_lib.py todo                             # undecided sections
In decision scripts: from q3_lib import *  (sys.path insert register/work)
"""
import json
import pathlib
import re
import sys

LE = pathlib.Path(__file__).resolve().parents[2]
WORK = LE / "register/work"
OUT = WORK / "decisions_3.jsonl"
BATCH = json.loads((WORK / "batch_3.json").read_text())["sections"]
BY_ID = {s["section_id"]: s for s in BATCH}
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def text(sid):
    return (LE / BY_ID[sid]["text_file"]).read_text(errors="ignore")


def src_url(path):
    first = (LE / path).read_text(errors="ignore").splitlines()[0]
    assert first.startswith("SOURCE:"), path
    return first.split("SOURCE:", 1)[1].strip()


def q(path, start, end=None):
    """Copy a quote mechanically from path: from `start` through `end` (inclusive), whitespace-normalized."""
    t = norm((LE / path).read_text(errors="ignore"))
    i = t.find(norm(start))
    assert i >= 0, f"start not found in {path}: {start[:60]}"
    if end is None:
        return t[i:i + len(norm(start))]
    j = t.find(norm(end), i)
    assert j >= 0, f"end not found in {path}: {end[:60]}"
    return t[i:j + len(norm(end))]


def must(path, phrase):
    assert norm(phrase) in norm((LE / path).read_text(errors="ignore")), f"must fail {path}: {phrase}"


def load():
    rows = {}
    if OUT.exists():
        for l in OUT.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                rows[r["section_id"]] = r
    return rows


def save(rows):
    order = [s["section_id"] for s in BATCH]
    OUT.write_text("".join(json.dumps(rows[s], ensure_ascii=False) + "\n" for s in order if s in rows))


_pending = {}


def dec(sid, decision, reason, atom_ids=(), proposed=()):
    assert sid in BY_ID, sid
    _pending[sid] = {"section_id": sid, "decision": decision, "reason": reason, "atom_ids": list(atom_ids),
                     "proposed": list(proposed), "reviewer": "q3"}


def nd(sid, reason):
    dec(sid, "no_decision", reason)


def ex(sid, reason):
    dec(sid, "excluded_regime", reason)


def st(sid, atoms, reason):
    dec(sid, "stated", reason, atoms)


def rule(id, provision, actor, modality, condition, effect, source_file, quote, severity, walk_step,
         determinacy="RULE", judgment_terms=(), dependencies=(), instrument=None, amends=None, construction=None,
         reasoning=None, effective_from=None, effective_to=None):
    assert id.startswith("NYC:"), id
    r = {"id": id, "jurisdiction": "NYC",
         "instrument": instrument or ("NYC Administrative Code" if "NYC_ADC" in source_file else
                                      "Rules of the City of New York"),
         "provision": provision, "actor": actor, "modality": modality, "condition": condition, "effect": effect,
         "determinacy": determinacy, "judgment_terms": list(judgment_terms), "dependencies": list(dependencies),
         "source_file": source_file, "source_url": src_url(source_file), "quote": quote, "severity": severity,
         "walk_step": walk_step}
    if amends:
        r["amends"] = amends
    if construction:
        r["construction"] = construction
        r["reasoning"] = reasoning
    if effective_from:
        r["effective_from"] = effective_from
    if effective_to:
        r["effective_to"] = effective_to
    return r


def commit():
    rows = load()
    rows.update(_pending)
    save(rows)
    print(f"committed {len(_pending)}; file has {len(rows)}/{len(BATCH)}")
    _pending.clear()


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "show":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        mx = int(sys.argv[4]) if len(sys.argv) > 4 else 12000
        for i in range(a, b):
            s = BATCH[i]
            t = text(s["section_id"]).split("\n", 3)[-1]
            print(f"\n######## [{i}] {s['section_id']} | {s['unit'][-70:]} | jev {s['jev_p_decides']}")
            print(t[:mx] + (" ...[TRUNC %d]" % len(t) if len(t) > mx else ""))
    elif cmd == "todo":
        rows = load()
        todo = [(i, s["section_id"]) for i, s in enumerate(BATCH) if s["section_id"] not in rows]
        print(len(todo), todo[:40])
