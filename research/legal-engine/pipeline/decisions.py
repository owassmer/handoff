"""check-decisions: validate reviewer decision files (J4), generalized from register/work/check_decisions.py.

jurisdictions/<CODE>/decisions/decisions_N.jsonl holds one JSON line per section of batch_N.json:
  {section_id, decision, reason, atom_ids[], proposed[], reviewer}
decision: stated (atom_ids) | partial (atom_ids and proposed; a proposal may carry 'amends': <existing id>) |
new_rule (proposed) | no_decision (reason) | excluded_regime (reason names the regime).
Each proposed rule carries every rule field (references/schemas.md) plus severity (critical|major|minor) and
walk_step; its id uses the prefix <CODE>:; its quote is verbatim in its source_file; construction needs reasoning;
no hedging words.

A proposed id that already exists as a rule is accepted only when that rule is this proposal applied (same
source_file and quote, or a recorded origin); any other existing rule with the id is a collision. An applied
proposal is not re-checked field by field: the applied rule stands and the rule checks (J6) check it. A proposal
merged by adjudication.json (merges[{into, from[]}]) is accepted when the 'into' rule carries its quote, as the rule's
own quote or a construction entry (the legacy checker's 'merged' disposition).
"""
from __future__ import annotations

import json
import tempfile

from . import core

PROPOSED_REQUIRED = core.RULE_REQUIRED + ["severity", "walk_step"]


def batch_numbers(code):
    d = core.jdir(code) / "decisions"
    return sorted(int(p.stem.split("_")[1]) for p in d.glob("batch_*.json")) if d.exists() else []


def all_known():
    """Every rule id and declared reference in the workspace: a decision may name a rule in any layer."""
    return core.known_ids(core.codes())


def applied_form(p):
    return {k: v for k, v in p.items() if k not in ("severity", "walk_step", "amends", "checks")}


def is_applied(p, existing):
    if not existing:
        return False
    o = existing.get("origin")
    if isinstance(o, dict) and o.get("proposal") == p.get("id"):
        return True
    return existing.get("source_file") == p.get("source_file") and core.norm(existing.get("quote")) == core.norm(p.get("quote"))


def check_batch(code, n, known, rules, new_ids, decisions_path=None, batch_path=None):
    errs = []
    ddir = core.jdir(code) / "decisions"
    batch = core.read_json(batch_path or ddir / f"batch_{n}.json")
    want = {s["section_id"] for s in batch["sections"]}
    rows = core.read_jsonl(decisions_path or ddir / f"decisions_{n}.jsonl")
    adj = core.read_json(core.jdir(code) / "adjudication.json", {}) if core.exists(code) else {}
    merged = {f: m["into"] for m in (adj or {}).get("merges", []) for f in m.get("from", [])}
    seen = {}
    for r in rows:
        sid = r.get("section_id")
        if sid in seen:
            errs.append(f"{sid}: decided twice")
        seen[sid] = r
        if sid not in want:
            errs.append(f"{sid}: not in batch {n}")
        d = r.get("decision")
        if d not in core.DECISIONS:
            errs.append(f"{sid}: decision {d!r}")
            continue
        if not str(r.get("reason", "")).strip():
            errs.append(f"{sid}: reason required")
        if core.HEDGE.search(str(r.get("reason", ""))):
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
        for p in r.get("proposed", []) or []:
            pid = p.get("id", "?")
            if pid in known and is_applied(p, rules.get(pid)):
                # already applied: the rule in rules.json is what stands, and the rule checks (J6) check it
                new_ids.setdefault(pid, (n, sid))
                continue
            if pid in merged and pid not in known:
                # merged by adjudication: the target rule must carry the proposal's quote as a construction entry
                tgt = rules.get(merged[pid])
                if tgt is None:
                    errs.append(f"{sid} {pid}: merge target {merged[pid]} is not a rule")
                elif not any(core.norm(c.get("quote")) == core.norm(p.get("quote"))
                             for c in [tgt] + list(tgt.get("construction") or [])):
                    errs.append(f"{sid} {pid}: merge target {merged[pid]} does not carry the proposal's quote")
                new_ids.setdefault(pid, (n, sid))
                continue
            miss = [k for k in PROPOSED_REQUIRED if k not in p]
            if miss:
                errs.append(f"{sid} {pid}: missing {miss}")
                continue
            if core.code_of(pid) != code:
                errs.append(f"{sid} {pid}: id must use the prefix {code}:")
            if pid in known and not is_applied(p, rules.get(pid)):
                errs.append(f"{sid} {pid}: id collides with an existing rule")
            if pid in new_ids and new_ids[pid] != (n, sid):
                errs.append(f"{sid} {pid}: id also proposed at {new_ids[pid]}")
            new_ids.setdefault(pid, (n, sid))
            if p["determinacy"] not in core.DETERMINACY:
                errs.append(f"{sid} {pid}: determinacy {p['determinacy']}")
            if p["determinacy"] != "RULE" and not p["judgment_terms"]:
                errs.append(f"{sid} {pid}: STANDARD/MIXED needs judgment_terms")
            if p["severity"] not in ("critical", "major", "minor"):
                errs.append(f"{sid} {pid}: severity {p['severity']}")
            if p.get("amends") and p["amends"] not in known:
                errs.append(f"{sid} {pid}: amends unknown rule {p['amends']}")
            e = core.verbatim(p["source_file"], p["quote"])
            if e:
                errs.append(f"{sid} {pid}: {e}")
            for c in p.get("construction", []) or []:
                e = core.verbatim(c.get("source_file", ""), c.get("quote", ""))
                if e:
                    errs.append(f"{sid} {pid}: construction {e}")
            if p.get("construction") and not p.get("reasoning"):
                errs.append(f"{sid} {pid}: construction without reasoning")
            for field in ("condition", "effect", "reasoning"):
                m = core.HEDGE.search(str(p.get(field, "")))
                if m:
                    errs.append(f"{sid} {pid}: hedging in {field}: '{m.group(0)}'")
    undecided = sorted(want - set(seen))
    cnt = {k: sum(1 for r in rows if r.get("decision") == k) for k in sorted(core.DECISIONS)}
    return errs, undecided, cnt, len(want)


def run(code, which):
    known, rules, new_ids = all_known(), core.rule_index(core.codes()), {}
    bad = False
    for n in which:
        errs, undecided, cnt, total = check_batch(code, n, known, rules, new_ids)
        print(f"{code} batch {n}: {total - len(undecided)}/{total} decided {cnt}; {len(errs)} errors")
        for e in errs[:60]:
            print("    ", e)
        if len(errs) > 60:
            print(f"     ... {len(errs) - 60} more")
        if undecided:
            print(f"    undecided: {len(undecided)} (first: {undecided[:5]})")
        bad |= bool(errs) or bool(undecided)
    return bad


def self_test(code="T"):
    """Planted bad atom id, bad quote, hedging, wrong prefix and an undecided section must each be caught."""
    with tempfile.TemporaryDirectory() as td:
        td = core.pathlib.Path(td)
        (td / "src.txt").write_text("SOURCE: x\nRETRIEVED: 2026-01-01 via test\n\nThe deposit is returned in 14 days.\n")
        old = core.ROOT
        core.set_root(td)
        try:
            (td / "b.json").write_text(json.dumps({"sections": [{"section_id": f"{code}:X 1"}, {"section_id": f"{code}:X 2"},
                                                                {"section_id": f"{code}:X 3"}, {"section_id": f"{code}:X 4"}]}))
            base = {k: "x" for k in PROPOSED_REQUIRED}
            base.update(id=f"{code}:planted", determinacy="RULE", judgment_terms=[], dependencies=[], severity="minor",
                        source_file="src.txt", quote="this sentence is not in the file")
            other = dict(base, id="ZZ:wrong-prefix", quote="The deposit is returned in 14 days.")
            rows = [{"section_id": f"{code}:X 1", "decision": "stated", "reason": "r", "atom_ids": ["NOPE:bad-id"]},
                    {"section_id": f"{code}:X 2", "decision": "new_rule", "reason": "r", "proposed": [base]},
                    {"section_id": f"{code}:X 3", "decision": "no_decision", "reason": "it is arguably outside"},
                    {"section_id": f"{code}:X 4", "decision": "new_rule", "reason": "r", "proposed": [other]}]
            (td / "d.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
            errs, undecided, _, _ = check_batch(code, 0, set(), {}, {}, td / "d.jsonl", td / "b.json")
            (td / "d.jsonl").write_text("\n".join(json.dumps(r) for r in rows[:3]))
            _, undecided2, _, _ = check_batch(code, 0, set(), {}, {}, td / "d.jsonl", td / "b.json")
        finally:
            core.set_root(old)
    ok = (any("does not exist" in e for e in errs) and any("not verbatim" in e for e in errs)
          and any("hedging in reason" in e for e in errs) and any("prefix" in e for e in errs)
          and not undecided and undecided2 == [f"{code}:X 4"])
    print("check-decisions self-test: planted bad atom id, bad quote, hedging, wrong prefix and undecided section "
          f"caught = {ok}")
    return ok


def main(code, arg):
    if arg == "--self-test":
        return 0 if self_test(code or "T") else 1
    which = batch_numbers(code) if arg in (None, "all") else [int(arg)]
    if not which:
        print(f"{code}: no batch files in {core.rel(core.jdir(code) / 'decisions')}")
        return 1
    return 1 if run(code, which) else 0
