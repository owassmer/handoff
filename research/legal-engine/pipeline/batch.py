"""batch (J4 step 2): split every undecided section, queued and set aside, into reviewer batches of 250-550
sections by legal function, highest Jev score first.

A section's legal function is its unit's first function (instruments.json units_in_scope[].functions), else its
instrument's first function. Functions are taken in chain-map order; a function too large for one batch is split
evenly; a batch smaller than 250 is filled from the next function. A section already in a batch file, or already
decided, is never batched again, so rerunning adds only new undecided sections. Numbering continues after the
highest existing batch. Writes decisions/batch_N.json and review_batch on each triage row.
"""
from __future__ import annotations

import math

from . import core, route, triage

MIN, MAX = 250, 550


def function_of(inst):
    fn = {}
    for i in inst.get("instruments", []):
        base = (i.get("functions") or ["unassigned"])[0]
        for u in i.get("units_in_scope", []):
            fn[(i["id"], u["unit"])] = (u.get("functions") or [base])[0]
        fn[i["id"]] = base
    return fn


def already_batched(code):
    d = core.jdir(code) / "decisions"
    out = set()
    for p in sorted(d.glob("batch_*.json")) if d.exists() else []:
        out |= {s["section_id"] for s in core.read_json(p)["sections"]}
    return out


def pack(groups):
    """groups: [(function, [items])] -> [[items]] with every batch <= MAX and, where the total allows, >= MIN."""
    batches, cur = [], []
    for _, g in groups:
        g = list(g)
        while g:
            room = MAX - len(cur)
            if len(g) <= room:
                cur += g
                g = []
            elif len(cur) >= MIN:
                batches.append(cur)
                cur = []
                if len(g) > MAX:
                    k = math.ceil(len(g) / MAX)
                    size = math.ceil(len(g) / k)
                    for i in range(0, len(g) - size, size):
                        batches.append(g[i:i + size])
                    g = g[(k - 1) * size:]
            else:
                cur += g[:room]
                g = g[room:]
                batches.append(cur)
                cur = []
    if cur:
        if batches and len(cur) < MIN and len(batches[-1]) + len(cur) <= MAX:
            batches[-1] += cur
        else:
            batches.append(cur)
    return batches


def plan(code):
    rows = triage.current_rows(code)
    secs = {s["section_id"]: s for s in core.sections(code)}
    fn = function_of(core.instruments(code))
    done = already_batched(code)
    todo = [r for r in rows if r.get("review_decision") is None and r["section_id"] not in done
            and r.get("review_batch") is None]
    order = [f["id"] for f in core.chain_map()["functions"]]
    groups = {}
    semantic_index_path = core.jdir(code) / 'semantic_runs.json'
    semantic_index = core.read_json(semantic_index_path) if semantic_index_path.exists() else {}
    for r in todo:
        f = fn.get((r["instrument"], r["unit"])) or fn.get(r["instrument"]) or "unassigned"
        s = secs[r["section_id"]]
        item = {
            "section_id": r["section_id"], "instrument": r["instrument"], "unit": r["unit"], "heading": r.get("heading"),
            "text_file": s.get("text_file"), "chars": s.get("chars", 0), "function": f, "tier": r.get("tier") or "unscored",
            "jev_p_decides": route.p_decides(r), "jev_chain_duty": (r.get("jev") or {}).get("chain_duty"),
            "route_reason": r.get("route_reason")}
        if r['section_id'] in semantic_index:
            from .semantics.research import for_section
            item['semantic'] = for_section(s, semantic_index[r['section_id']], core.ROOT)
        groups.setdefault(f, []).append(item)
    key = lambda x: (route.tier_rank(x["tier"]), -(x["jev_p_decides"] if x["jev_p_decides"] is not None else -1),
                     x["instrument"], x["section_id"])
    ordered = sorted(groups.items(), key=lambda kv: order.index(kv[0]) if kv[0] in order else len(order))
    out = []
    for b in pack([(f, sorted(g, key=key)) for f, g in ordered]):
        out.append(sorted(b, key=key))
    return out


def main(code, dry_run=False):
    batches = plan(code)
    existing = [int(p.stem.split("_")[1]) for p in (core.jdir(code) / "decisions").glob("batch_*.json")] \
        if (core.jdir(code) / "decisions").exists() else []
    n0 = max(existing or [0])
    if not batches:
        print(f"{code} batch: no undecided section outside an existing batch; nothing to do")
        return 0
    rows = core.triage(code)
    where = {}
    for i, b in enumerate(batches, n0 + 1):
        fns = sorted({x["function"] for x in b})
        print(f"{code} batch {i}: {len(b)} sections, {sum(x['chars'] for x in b)} characters; functions {fns}")
        if not dry_run:
            core.write_json(core.jdir(code) / "decisions" / f"batch_{i}.json", {
                "batch": i, "jurisdiction": code, "functions": fns, "created": core.today(), "count": len(b),
                "chars": sum(x["chars"] for x in b), "order": "tier, then highest P(DECIDES), then instrument",
                "sections": b})
            for x in b:
                where[x["section_id"]] = i
    if not dry_run:
        for r in rows:
            if r["section_id"] in where:
                r["review_batch"] = where[r["section_id"]]
        core.write_jsonl(core.jdir(code) / "triage.jsonl", rows)
    print(f"{code} batch: {sum(len(b) for b in batches)} sections in {len(batches)} batches"
          f"{' (dry run, nothing written)' if dry_run else ''}")
    return 0
