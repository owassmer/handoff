"""instruments (J1 gate): check the instrument list against the chain map's legal functions.

Fails when an instrument lacks a field, names an unknown level, function or adapter, has an out unit without a
reason or a duplicated unit, or when a chain-map legal function has neither an instrument in this layer nor a
recorded reason in functions_without_instrument. Parent layers' coverage is printed as a hint only.
"""
from __future__ import annotations

from . import core

LEVELS = {"statute", "regulation", "local code", "court rule", "agency rule"}
FIELDS = ["id", "jurisdiction", "name", "level", "functions", "units_in_scope", "units_out", "toc_source_url", "adapter"]


def check(code):
    from . import adapters
    doc = core.instruments(code)
    fns = {f["id"]: f for f in core.chain_map()["functions"]}
    errs = []
    if doc.get("discovery_status") == "open":
        errs.append("source discovery is open; the saved-source inventory is not a completed instrument register")
    covered = set()
    for i in doc.get("instruments", []):
        iid = i.get("id", "?")
        miss = [k for k in FIELDS if k not in i]
        if miss:
            errs.append(f"{iid}: missing {miss}")
            continue
        if core.code_of(iid) != code:
            errs.append(f"{iid}: id must use the prefix {code}:")
        if i["level"] not in LEVELS:
            errs.append(f"{iid}: level {i['level']!r} (one of {sorted(LEVELS)})")
        if i["adapter"] not in adapters.NAMES:
            errs.append(f"{iid}: adapter {i['adapter']!r} is not in pipeline/adapters ({sorted(adapters.NAMES)})")
        bad = [f for f in i["functions"] if f not in fns]
        if bad:
            errs.append(f"{iid}: unknown functions {bad}")
        if not i["functions"] and i["units_in_scope"]:
            errs.append(f"{iid}: in-scope units but no legal function")
        seen = set()
        for u in i["units_in_scope"] + i["units_out"]:
            if u.get("unit") in seen:
                errs.append(f"{iid}: unit {u.get('unit')!r} listed twice")
            seen.add(u.get("unit"))
            for f in u.get("functions", []) or []:
                if f not in fns:
                    errs.append(f"{iid} unit {u.get('unit')}: unknown function {f}")
        for u in i["units_out"]:
            if not str(u.get("reason", "")).strip():
                errs.append(f"{iid}: out unit {u.get('unit')!r} has no reason")
        if i["units_in_scope"]:
            covered |= set(i["functions"])
            for u in i["units_in_scope"]:
                covered |= set(u.get("functions") or [])
    reasons = {x["function"]: x.get("reason") for x in doc.get("functions_without_instrument", [])}
    for f, r in reasons.items():
        if f not in fns:
            errs.append(f"functions_without_instrument names unknown function {f}")
        elif not str(r or "").strip():
            errs.append(f"functions_without_instrument {f}: reason required")
    uncovered = [f for f in fns if f not in covered and not reasons.get(f)]
    return errs, uncovered, covered, reasons


def main(code):
    errs, uncovered, covered, reasons = check(code)
    n = len(core.instruments(code).get("instruments", []))
    print(f"{code} instruments: {n} instruments; functions covered {len(covered)}, with a recorded reason {len(reasons)}, "
          f"uncovered {len(uncovered)}")
    for f in uncovered:
        par = [p for p in core.ancestors(code) if core.exists(p) and f in check(p)[2]]
        print(f"   no instrument and no reason: {f}" + (f" (covered in parent layer {', '.join(par)})" if par else ""))
    for e in errs[:60]:
        print("  ", e)
    return 1 if errs or uncovered else 0
