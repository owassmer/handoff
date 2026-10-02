"""Helpers for reviewer q5 (batch 5). Idempotent: add() replaces any earlier row for the same section."""
import json
import pathlib
import re

LE = pathlib.Path(__file__).resolve().parents[2]
OUT = LE / "register/work/decisions_5.jsonl"
BATCH = json.loads((LE / "register/work/batch_5.json").read_text())
SEC = {s["section_id"]: s for s in BATCH["sections"]}
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def rows():
    if not OUT.exists():
        return {}
    return {r["section_id"]: r for r in (json.loads(l) for l in OUT.read_text().splitlines() if l.strip())}


def add(sid, decision, reason, atom_ids=None, proposed=None):
    assert sid in SEC, sid
    r = rows()
    row = {"section_id": sid, "decision": decision, "reason": reason, "atom_ids": atom_ids or [],
           "proposed": proposed or [], "reviewer": "q5"}
    r[sid] = row
    order = [s["section_id"] for s in BATCH["sections"]]
    OUT.write_text("\n".join(json.dumps(r[k], ensure_ascii=False) for k in order if k in r) + "\n")


def nd(sid, reason):
    add(sid, "no_decision", reason)


def text(sid):
    return (LE / SEC[sid]["text_file"]).read_text(errors="ignore")


def url(sid):
    m = re.search(r"^SOURCE:\s*(\S+)", text(sid), re.M)
    return m.group(1) if m else ""


def quote(sid, start, end):
    """Copy the verbatim span of the section text from `start` through `end` (whitespace-normalised)."""
    t = norm(text(sid))
    f = lambda s: s.replace("’", "'").replace("“", '"').replace("”", '"').replace("—", "-")
    tt = f(t)
    i = tt.find(f(norm(start)))
    assert i >= 0, f"start not found in {sid}: {start}"
    j = tt.find(f(norm(end)), i)
    assert j >= 0, f"end not found in {sid}: {end}"
    return t[i:j + len(norm(end))]


def rule(sid, id, provision, actor, modality, condition, effect, severity, walk_step, q_start, q_end,
         determinacy="RULE", judgment_terms=None, dependencies=None, amends=None, instrument=None,
         construction=None, reasoning=None):
    s = SEC[sid]
    p = {"id": id, "jurisdiction": "US",
         "instrument": instrument or {"US:11USC": "Bankruptcy Code", "US:FRBP": "Federal Rules of Bankruptcy Procedure",
                                      "US:26CFR1-info": "Treasury Regulations"}.get(s["instrument"], "Internal Revenue Code"),
         "provision": provision, "actor": actor, "modality": modality, "condition": condition, "effect": effect,
         "determinacy": determinacy, "judgment_terms": judgment_terms or [], "dependencies": dependencies or [],
         "source_file": s["text_file"], "source_url": url(sid), "quote": quote(sid, q_start, q_end),
         "severity": severity, "walk_step": walk_step}
    if amends:
        p["amends"] = amends
    if construction:
        p["construction"] = construction
        p["reasoning"] = reasoning
    return p


def undecided():
    r = rows()
    return [s for s in BATCH["sections"] if s["section_id"] not in r]
