"""Validate reviewer decisions on the register's review queue.

Usage (from research/legal-engine):
    python3 register/work/check_decisions.py 3          # batch 3: register/work/decisions_3.jsonl against batch_3.json
    python3 register/work/check_decisions.py all        # every batch, plus cross-batch id uniqueness
    python3 register/work/check_decisions.py --self-test

One JSON line per queued section:
  {"section_id", "decision", "reason", "atom_ids": [...], "proposed": [...], "reviewer"}
decision is one of:
  stated          an existing rule states the section fully for this chain; atom_ids required.
  partial         existing rules state it only in part; atom_ids required, and each proposed rule carries
                  "amends": <existing atom id> or is a new rule covering the missing branch.
  new_rule        no rule states it and it changes a decision in the chain; proposed required.
  no_decision     it changes nothing in the chain for a market-rate NYC unit; reason says why.
  excluded_regime it decides the matter only for an out-of-aperture regime (stabilized/controlled, public or
                  subsidized housing, commercial, outside NYC); reason names the regime.
Every proposed rule: id, jurisdiction, instrument, provision, actor, modality, condition, effect, determinacy
(RULE|STANDARD|MIXED), judgment_terms (non-empty unless RULE), dependencies, source_file (path from
research/legal-engine, e.g. register/texts/NY_GOL/15-106.txt), source_url, quote (verbatim in source_file),
severity (critical|major|minor), walk_step; optional construction [{source_file, quote}] (then reasoning required).
Applied proposals: once a proposal has been applied to the rule files, register/work/applied.json maps its id to the atom
that carries it. Its id may then exist in the rule files only as that atom ('added': the atom keeps the proposal's quote)
or not at all ('merged': the target atom carries the proposal's quote as a construction entry).
Batches: every register/work/batch_<n>.json is checked ('all').
Exit 1 on any error.
"""
import json
import pathlib
import re
import sys

LE = pathlib.Path(__file__).resolve().parents[2]
WORK = LE / "register/work"
DECISIONS = {"stated", "partial", "new_rule", "no_decision", "excluded_regime"}
REQ = ["id", "jurisdiction", "instrument", "provision", "actor", "modality", "condition", "effect", "determinacy",
       "judgment_terms", "dependencies", "source_file", "source_url", "quote", "severity", "walk_step"]
HEDGE = re.compile(r"\b(unclear|unsettled|open question|working position|conservative position|arguabl\w*|consult counsel|"
                   r"needs counsel|not yet known|undetermined|uncertain whether|may or may not|it is possible that|"
                   r"in practice|typically|persuasive only)\b", re.I)
norm = lambda s: re.sub(r"\s+", " ", s).strip()
_cache = {}


ATOMS = {}


def existing_ids():
    ids = set()
    for k in ("NY", "NYC", "US", "VA"):
        d = json.loads((LE / f"stage-a/{k}.json").read_text())
        ids |= {a["id"] for a in d["atoms"]} | set(d.get("external_references", {}))
        ATOMS.update({a["id"]: a for a in d["atoms"]})
    return ids


def applied_map():
    p = WORK / "applied.json"
    return json.loads(p.read_text()) if p.exists() else {}


APPLIED = applied_map()


def applied_ok(p):
    """None if the proposal's presence in the rule files is its own applied atom, else an error text."""
    rec = APPLIED.get(p["id"])
    if not rec:
        return "id collides with an existing rule"
    a = ATOMS.get(rec["atom_id"])
    if a is None:
        return f"applied atom {rec['atom_id']} missing from the rule files"
    if rec["disposition"] == "added":
        if a["id"] != p["id"] or norm(a["quote"]) != norm(p["quote"]):
            return f"applied atom {a['id']} does not carry the proposal's quote"
    elif not any(norm(c.get("quote", "")) == norm(p["quote"]) for c in a.get("construction", [])):
        return f"merge target {a['id']} does not carry the proposal's quote"
    return None


def verbatim(src, quote):
    f = LE / src
    if not src or not f.is_file():
        return f"source file missing: {src}"
    _cache.setdefault(f, norm(f.read_text(errors="ignore")))
    return None if quote and norm(quote) in _cache[f] else f"quote not verbatim in {src}"


def check_batch(n, known, new_ids, decisions_path=None, batch_path=None):
    errs = []
    batch = json.loads((batch_path or WORK / f"batch_{n}.json").read_text())
    want = {s["section_id"] for s in batch["sections"]}
    path = decisions_path or WORK / f"decisions_{n}.jsonl"
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()] if path.exists() else []
    seen = {}
    for r in rows:
        sid = r.get("section_id")
        if sid in seen:
            errs.append(f"{sid}: decided twice")
        seen[sid] = r
        if sid not in want:
            errs.append(f"{sid}: not in batch {n}")
        d = r.get("decision")
        if d not in DECISIONS:
            errs.append(f"{sid}: decision {d!r}")
            continue
        if not str(r.get("reason", "")).strip():
            errs.append(f"{sid}: reason required")
        if HEDGE.search(str(r.get("reason", ""))):
            errs.append(f"{sid}: hedging in reason")
        if d in ("stated", "partial"):
            if not r.get("atom_ids"):
                errs.append(f"{sid}: {d} needs atom_ids")
            for a in r.get("atom_ids", []):
                if a not in known:
                    errs.append(f"{sid}: atom id {a} does not exist")
        if d in ("partial", "new_rule") and not r.get("proposed"):
            errs.append(f"{sid}: {d} needs proposed rules")
        if d in ("stated", "no_decision", "excluded_regime") and r.get("proposed"):
            errs.append(f"{sid}: {d} must not carry proposed rules")
        for p in r.get("proposed", []):
            pid = p.get("id", "?")
            miss = [k for k in REQ if k not in p]
            if miss:
                errs.append(f"{sid} {pid}: missing {miss}")
                continue
            if pid in known or pid in APPLIED:
                e = applied_ok(p)
                if e:
                    errs.append(f"{sid} {pid}: {e}")
            if pid in new_ids and new_ids[pid] != (n, sid):
                errs.append(f"{sid} {pid}: id also proposed at {new_ids[pid]}")
            new_ids.setdefault(pid, (n, sid))
            if p["determinacy"] not in ("RULE", "STANDARD", "MIXED"):
                errs.append(f"{sid} {pid}: determinacy {p['determinacy']}")
            if p["determinacy"] != "RULE" and not p["judgment_terms"]:
                errs.append(f"{sid} {pid}: STANDARD/MIXED needs judgment_terms")
            if p["severity"] not in ("critical", "major", "minor"):
                errs.append(f"{sid} {pid}: severity {p['severity']}")
            if p.get("amends") and p["amends"] not in known:
                errs.append(f"{sid} {pid}: amends unknown rule {p['amends']}")
            e = verbatim(p["source_file"], p["quote"])
            if e:
                errs.append(f"{sid} {pid}: {e}")
            for c in p.get("construction", []):
                e = verbatim(c.get("source_file", ""), c.get("quote", ""))
                if e:
                    errs.append(f"{sid} {pid}: construction {e}")
            if p.get("construction") and not p.get("reasoning"):
                errs.append(f"{sid} {pid}: construction without reasoning")
            for field in ("condition", "effect", "reasoning"):
                m = HEDGE.search(str(p.get(field, "")))
                if m:
                    errs.append(f"{sid} {pid}: hedging in {field}: '{m.group(0)}'")
    undecided = sorted(want - set(seen))
    counts = {k: sum(1 for r in rows if r.get("decision") == k) for k in sorted(DECISIONS)}
    return errs, undecided, counts, len(want)


def run(which):
    known, new_ids = existing_ids(), {}
    bad = False
    for n in which:
        errs, undecided, counts, total = check_batch(n, known, new_ids)
        print(f"batch {n}: {total - len(undecided)}/{total} decided {counts}; {len(errs)} errors")
        for e in errs[:60]:
            print("   ", e)
        if undecided:
            print(f"    undecided: {len(undecided)} (first: {undecided[:5]})")
        bad |= bool(errs) or bool(undecided)
    return bad


def self_test():
    import tempfile
    known, new_ids = existing_ids(), {}
    some = sorted(known)[0]
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        (td / "b.json").write_text(json.dumps({"sections": [{"section_id": "X:1"}, {"section_id": "X:2"},
                                                            {"section_id": "X:3"}]}))
        rows = [{"section_id": "X:1", "decision": "stated", "reason": "r", "atom_ids": ["NOPE:bad-id"]},
                {"section_id": "X:2", "decision": "new_rule", "reason": "r", "proposed": [{
                    **{k: "x" for k in REQ}, "id": "T:planted", "determinacy": "RULE", "judgment_terms": [],
                    "dependencies": [], "severity": "minor", "source_file": "stage_a_check.py",
                    "quote": "this sentence is not in the file"}]}]
        (td / "d.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
        errs, undecided, _, _ = check_batch(0, known, new_ids, td / "d.jsonl", td / "b.json")
    ok = (any("does not exist" in e for e in errs) and any("not verbatim" in e for e in errs) and undecided == ["X:3"])
    print("self-test: planted bad atom id, bad quote and undecided section caught =", ok)
    return not ok


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg == "--self-test":
        sys.exit(1 if self_test() else 0)
    which = (sorted(int(p.stem.split("_")[1]) for p in WORK.glob("batch_*.json")) if arg == "all" else [int(arg)])
    sys.exit(1 if run(which) else 0)
