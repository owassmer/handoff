"""Walk check (gate J7): review/check_review.py for any jurisdiction's walk.md.

Fails when the walk cites a rule id that does not exist, or when a rule in the walk's scope is neither cited nor
listed as deferred ("deferred: `ID`", under a heading that gives the reason). Scope: every rule of the jurisdiction
and its parent layers, minus rules whose id matches the profile's walk.scope_exclude pattern (for NYC, the rules
that govern only stabilized or controlled tenancies, which belong to a later walk).
"""
from __future__ import annotations

import re
import tempfile

from . import core


def cite_rx(codes_):
    alt = "|".join(sorted((re.escape(c) for c in codes_), key=len, reverse=True)) or "NOPE"
    return re.compile(r"`((?:" + alt + r"):[^`\s]+)`"), re.compile(r"deferred: `((?:" + alt + r"):[^`\s]+)`")


def check_text(text, rules, scope_ids, codes_):
    """rules: {id: rule} of every rule the walk may cite; scope_ids: ids that must be cited or deferred."""
    crx, drx = cite_rx(codes_)
    cited = set(crx.findall(text))
    deferred = set(drx.findall(text))
    errs = [f"cited but not a rule: {i}" for i in sorted(cited) if i not in rules]
    scope = set(scope_ids)
    missing = sorted(scope - cited - deferred)
    summary = (f"in scope {len(scope)}: cited {len((cited - deferred) & scope)}, deferred {len(deferred & scope)}, "
               f"not cited {len(missing)}; also cited from outside scope {len((cited - deferred) & set(rules) - scope)}")
    return errs, missing, summary


def scope_for(code):
    p = core.profile(code)
    rules = core.rule_index(core.layers(code))
    rx = (p.get("walk") or {}).get("scope_exclude")
    excl = re.compile(rx) if rx else None
    return rules, [i for i in rules if not (excl and excl.match(i))]


def check(code, walk_path=None):
    walk = walk_path or core.jdir(code) / "walk.md"
    if not walk.exists():
        return None
    rules, scope = scope_for(code)
    return check_text(walk.read_text(), rules, scope, core.layers(code))


def covering_walk(code):
    """The walk that covers this layer: its own, else a descendant's (a city walk covers its state and federal
    layers). Returns (code of the walk's jurisdiction, result) or (None, None)."""
    for c in [code] + core.descendants(code):
        r = check(c)
        if r is not None:
            if c == code:
                return c, r
            rules, scope = scope_for(c)
            own = {i for i in scope if core.code_of(i) == code}
            errs, missing, summary = r
            return c, (errs, [m for m in missing if m in own], summary)
    return None, None


def self_test():
    rules = {"T:a": {}, "T:b": {}, "T:c": {}}
    good = "Step 1. `T:a` and `T:b`.\n\nLater:\n- deferred: `T:c`\n"
    e0, m0, _ = check_text(good, rules, list(rules), ["T"])
    e1, _, _ = check_text(good + "`T:zzz`", rules, list(rules), ["T"])
    _, m2, _ = check_text(good.replace("- deferred: `T:c`\n", ""), rules, list(rules), ["T"])
    ok = not e0 and not m0 and any("T:zzz" in e for e in e1) and m2 == ["T:c"]
    return ok, "planted unknown id and uncited rule caught" if ok else "NOT CAUGHT"


def main(code):
    ok, msg = self_test()
    print(f"walk check self-test: {msg}")
    c, r = covering_walk(code)
    if r is None:
        print(f"{code}: no walk.md in this layer or a layer below it")
        return 1
    errs, missing, summary = r
    print(f"{code}: walk of {c}: {summary}")
    for i in missing:
        print("   not cited:", i)
    for e in errs:
        print("  ", e)
    return 1 if (errs or missing or not ok) else 0
