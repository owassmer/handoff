"""check: run every gate and print the stage each jurisdiction has reached.

Gates (skill stages):
  J0 owner   profile.json owner_confirmed has by and date (the owner confirms the jurisdiction)
  J1         `instruments` passes
  J2         every in-scope unit harvested (its recorded section count equals its sections.jsonl rows), no unit TOC gap,
             every section has saved text with a SOURCE/RETRIEVED header
  J3         match.json exists and equals a fresh match (recorded, deterministic); one triage row per section
  J4         register check in strict mode (every section decided, by match or by a reviewer whose decisions file
             agrees), its planted-defect self-tests caught, and `check-decisions all` clean when batches exist
  J5         `authorities` passes
  J6         rule checks pass (verbatim quotes, dependencies, no hedging, no open question)
  J7         the walk covering this layer cites or defers every in-scope rule and cites no unknown id
  J8         the latest correctness review (reviews/review_N.json {findings: [{severity}]}) has no critical finding
  J9 owner   profile status 'accepted' and every file hash in profile acceptance.hashes still matches
The stage reached is the last of J1-J8 passed in order; the owner gates are printed beside it.
  python3 -m pipeline check [CODE ...] [--upto J5]
Exits non-zero when any gate from J1 to --upto (default J8) fails for a jurisdiction checked.
"""
from __future__ import annotations

import io
import contextlib

from . import core

AUTO = ["J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8"]


def g_j0(code):
    oc = core.profile(code).get("owner_confirmed") or {}
    return (True, f"confirmed by {oc['by']} {oc['date']}") if oc.get("by") and oc.get("date") else \
        (False, "owner has not confirmed (profile.json owner_confirmed)")


def g_j1(code):
    from . import instruments
    errs, uncovered, covered, reasons = instruments.check(code)
    n = len(core.instruments(code).get("instruments", []))
    if not n:
        return False, "no instruments"
    bad = errs + [f"function {f} has no instrument and no reason" for f in uncovered]
    return (not bad), (f"{n} instruments, {len(covered)} functions covered, {len(reasons)} with a reason"
                       if not bad else f"{len(bad)} problems, first: {bad[0]}")


def g_j2(code):
    doc = core.instruments(code)
    secs = core.sections(code)
    if not secs:
        return False, "no sections harvested"
    per = {}
    for s in secs:
        per[(s["instrument"], s["unit"])] = per.get((s["instrument"], s["unit"]), 0) + 1
    probs = []
    for i in doc.get("instruments", []):
        for u in i.get("units_in_scope", []):
            if u.get("sections") is None:
                probs.append(f"{i['id']} {u['unit']}: not harvested (no section count)")
            elif u["sections"] != per.get((i["id"], u["unit"]), 0):
                probs.append(f"{i['id']} {u['unit']}: TOC {u['sections']}, sections.jsonl {per.get((i['id'], u['unit']), 0)}")
    probs += [f"unit TOC gap {g.get('instrument')} {g.get('unit')}" for g in (doc.get("fetch_gaps") or {}).get("instrument_gaps", [])
              if g.get("unit")]
    for s in secs:
        if s.get("source_authority") == "mirror":
            probs.append(f"{s['section_id']}: mirror text; official source reconciliation pending")
        if s.get("source_unit_kind") == "document":
            probs.append(f"{s['section_id']}: whole document; internal section enumeration pending")
        if not s.get("text_file"):
            probs.append(f"{s['section_id']}: no saved text")
            continue
        p = core.ROOT / s["text_file"]
        if not p.exists() or not core.has_header(p.read_text(errors="ignore")[:800]):
            probs.append(f"{s['section_id']}: text missing or without SOURCE/RETRIEVED header")
    return (not probs), (f"{len(secs)} sections, all with saved text" if not probs else
                         f"{len(probs)} problems, first: {probs[0]}")


def g_j3(code):
    from . import match
    p = core.jdir(code) / "match.json"
    if not p.exists():
        return False, "match.json missing (run match)"
    fresh = match.compute(code)
    if core.dumps(fresh) != core.dumps(core.read_json(p)):
        return False, "match.json differs from a fresh match (rerun match)"
    rows, secs = core.triage(code), core.sections(code)
    if {r["section_id"] for r in rows} != {s["section_id"] for s in secs} or len(rows) != len(secs):
        return False, f"triage.jsonl has {len(rows)} rows for {len(secs)} sections"
    stated = sum(1 for v in fresh["sections"].values() if v)
    return True, f"{stated} of {len(secs)} sections stated by a rule"


def g_j4(code):
    from . import decisions, registercheck
    d = registercheck.load(code)
    if not d["sections"]:
        return False, "no sections"
    errs = registercheck.check(d)
    ok = registercheck.self_test(d)
    if not all(ok.values()):
        errs.append("register self-test: " + ", ".join(k for k, v in ok.items() if not v) + " not caught")
    nums = decisions.batch_numbers(code)
    if nums:
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            bad = decisions.run(code, nums)
        if bad:
            lines = buf.getvalue().splitlines()
            first = next((l.strip() for l in lines if l.startswith("     ")), lines[-1] if lines else "")
            errs.append(f"check-decisions all fails ({sum(1 for l in lines if l.startswith('     '))} errors): {first[:200]}")
    dec = sum(1 for r in d["triage"] if r.get("review_decision") in core.DECISIONS)
    return (not errs), (f"{dec}/{len(d['sections'])} sections decided; register strict clean"
                        if not errs else f"{len(errs)} problems, first: {errs[0]}")


def g_j5(code):
    from . import authorities
    errs, missing, n, courts = authorities.check(code)
    bad = errs + [f"no search: {m}" for m in missing]
    return (not bad), (f"{n} searches across {len(courts)} binding courts" if not bad else
                       f"{len(bad)} problems, first: {bad[0]}")


def g_j6(code):
    from . import rulecheck
    errs, n = rulecheck.check(code)
    if not n:
        return False, "no rules"
    return (not errs), (f"{n} rules, 0 errors" if not errs else f"{n} rules, {len(errs)} errors, first: {errs[0]}")


def g_j7(code):
    from . import walkcheck
    c, r = walkcheck.covering_walk(code)
    if r is None:
        return False, "no walk.md in this layer or a layer below it"
    errs, missing, summary = r
    if summary.startswith("in scope 0:"):
        return False, f"walk of {c}: no rule in scope"
    bad = errs + [f"not cited: {m}" for m in missing]
    return (not bad), (f"walk of {c}: {summary}" if not bad else f"walk of {c}: {len(bad)} problems, first: {bad[0]}")


def g_j8(code):
    d = core.jdir(code) / "reviews"
    files = sorted(d.glob("review_*.json"), key=lambda p: int(p.stem.split("_")[1])) if d.exists() else []
    if not files:
        return False, "no correctness review recorded (reviews/review_N.json)"
    last = core.read_json(files[-1])
    crit = [f for f in last.get("findings", []) if f.get("severity") == "critical"]
    return (not crit), f"{files[-1].name}: {len(last.get('findings', []))} findings, {len(crit)} critical"


def g_j9(code):
    p = core.profile(code)
    if p.get("status") != "accepted":
        return False, f"status {p.get('status')!r}"
    changed = [f for f, h in ((p.get("acceptance") or {}).get("hashes") or {}).items()
               if not (core.ROOT / f).exists() or core.sha256_file(core.ROOT / f) != h]
    return (not changed), ("accepted; file hashes match" if not changed else f"{len(changed)} files changed since acceptance")


GATES = {"J0": g_j0, "J1": g_j1, "J2": g_j2, "J3": g_j3, "J4": g_j4, "J5": g_j5, "J6": g_j6, "J7": g_j7, "J8": g_j8,
         "J9": g_j9}


def evaluate(code):
    res = {}
    for g, f in GATES.items():
        try:
            res[g] = f(code)
        except core.PipelineError as e:
            res[g] = (False, f"error: {e}")
    reached = "none"
    for g in AUTO:
        if not res[g][0]:
            break
        reached = g
    return res, reached


def main(codes_, upto="J8"):
    codes_ = codes_ or core.codes()
    if not codes_:
        print(f"check: no jurisdictions under {core.rel(core.JUR)}")
        return 1
    if upto not in AUTO:
        print(f"--upto must be one of {AUTO}")
        return 1
    need = AUTO[:AUTO.index(upto) + 1]
    bad = False
    for c in codes_:
        res, reached = evaluate(c)
        print(f"{c}: stage reached {reached}; owner confirmed {'yes' if res['J0'][0] else 'no'}; "
              f"accepted {'yes' if res['J9'][0] else 'no'}")
        for g, (ok, msg) in res.items():
            print(f"  {g} {'PASS' if ok else 'FAIL'}  {msg}")
        bad |= any(not res[g][0] for g in need)
        from . import coverage
        research = coverage.jurisdiction_summary(c)
        print(f"  Research coverage {'COMPLETE' if research['complete'] else 'OPEN'}: {research['message']}")
        for scope in research["scopes"]:
            print(f"    {scope['scope_id']} revision {scope['revision']}: "
                  f"{'complete' if scope['complete'] else str(scope['problems']) + ' unresolved checks'}")
        # Legacy download/routing stages cannot certify substantive research closure.
        if upto == "J8":
            bad |= not research["complete"]
    return 1 if bad else 0
