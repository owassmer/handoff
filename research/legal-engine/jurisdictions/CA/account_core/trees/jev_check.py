#!/usr/bin/env python3
"""Jev fidelity check for the account-core trees (research aid; decides nothing).

For every leaf, one Noul: does the quoted source text, read within its surrounding subsection, establish the leaf's
statement as a condition of (or an exception to) the tree's effect, in the role the tree gives it? Leaves of one
tree that cite the same top-level subdivision share one request (shared state, one question per leaf).

Uses the pipeline's Jev client (pipeline/jev.py: credential from OPENROUTER_API_KEY, never printed; pinned build).
Responses are cached by request hash under research/legal-engine/.cache/jev-tree-check/, so a re-run spends only on
changed requests. Writes JEV_CHECK.json (requests, answers, cost) next to this script. Spend cap: --cap (default $2).

Run with the venv that has typesafe_sdk:  <venv>/bin/python jev_check.py [--cap 2.00] [--dry-run]
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import pathlib
import sys
from decimal import Decimal

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_trees as ct  # noqa: E402

LE = ct.LE
sys.path.insert(0, str(LE))
from pipeline import core, jev  # noqa: E402

CACHE = LE / ".cache" / "jev-tree-check"
OUT = HERE / "JEV_CHECK.json"
TASK_VERSION = "tree-fidelity-2"
CODE_NAMES = {"Civ": "California Civil Code", "CCP": "California Code of Civil Procedure",
              "Gov": "California Government Code", "PUC": "California Public Utilities Code"}

QUESTION = ("state.structure shows how the conditions combine to decide the effect in state.effect. Read the quote "
            "within state.source_text. Does that text establish the condition below, in the place state.structure "
            "gives it (a requirement, one of several alternatives, part of a bar, or an exception), as a condition of "
            "or an exception to that effect?")
CRITERIA = {
    "true": "The text makes this condition, in that place in the structure, part of what decides whether the effect "
            "follows.",
    "false": "The text does not establish this condition, establishes a materially different condition, or gives it "
             "a different place (for example a requirement presented as an exception, or a duty presented as a "
             "condition of a permission).",
}


def render(node, labels, depth=0):
    """Plain-text rendering of a tree's condition structure, leaves labelled [L1], [L2] ... in order."""
    pad = "  " * depth
    t = node["type"]
    if t == "condition":
        labels[node["id"]] = f"L{len(labels) + 1}"
        return f"{pad}[{labels[node['id']]}] {node['statement']}"
    if t in ("all", "any"):
        head = "ALL of the following:" if t == "all" else "ANY ONE of the following (alternatives):"
        return "\n".join([pad + head] + [render(c, labels, depth + 1) for c in node["children"]])
    if t == "not":
        return "\n".join([pad + "NOT the following (it must not hold):", render(node["child"], labels, depth + 1)])
    if t == "unless":
        return "\n".join([pad + "RULE:", render(node["rule"], labels, depth + 1),
                          pad + "UNLESS (exception: if this holds, the effect does not follow):",
                          render(node["exception"], labels, depth + 1)])
    raise ValueError(t)


def role_of(path):
    """Plain description of a leaf's role from the node path [(kind, polarity)]."""
    neg = sum(1 for k in path if k == "not") % 2 == 1
    in_exception = "exception" in path
    in_any = "any" in path
    if in_exception:
        base = ("An exception: if this condition holds, the effect does not follow" if not neg else
                "Part of an exception, in negated form: the exception applies only if this condition does NOT hold")
    elif neg:
        base = "A bar: the effect follows only if this condition does NOT hold"
    else:
        base = "A requirement: the effect follows only if this condition holds"
    if in_any:
        base += " (it is one of several alternatives; any one alternative suffices)"
    return base + "."


def leaves_with_roles(node, path=()):
    t = node.get("type")
    if t == "condition":
        yield node, path
    elif t in ("all", "any"):
        for c in node["children"]:
            yield from leaves_with_roles(c, path + ((t,) if t == "any" else ()))
    elif t == "not":
        yield from leaves_with_roles(node["child"], path + ("not",))
    elif t == "unless":
        yield from leaves_with_roles(node["rule"], path)
        yield from leaves_with_roles(node["exception"], path + ("exception",))


def context_for(citation):
    """(group key, instrument label, surrounding text): the top-level subdivision the quote sits in."""
    f, cls, sec, sub = ct.resolve(citation)
    code = citation.split(" ", 1)[0]
    if not sub:
        body = core.body_of(f.read_text()) if cls == "statute" else f.read_text()
        start = body.find(f"\n{sec}.")
        return (str(f), ""), f"{CODE_NAMES[code]} section {sec}", ct.norm(body[start:] if start >= 0 else body)
    top = sub[:1]
    rows = ct.section_lines(f, sec)
    intro = [l for p, l in rows if not p]
    span = [l for p, l in rows if p[:1] == top]
    label = f"{CODE_NAMES[code]} section {sec}, subdivision ({top[0]})"
    return (str(f), top[0]), label, ct.norm("\n".join(intro + span))


def build_requests():
    groups = {}
    for p in sorted(HERE.glob("*.json")):
        if p.name == "JEV_CHECK.json":
            continue
        tree = json.loads(p.read_text())
        holds = [e["statement"] for e in tree["effects"] if e["when"] == "holds"]
        fails = [e["statement"] for e in tree["effects"] if e["when"] == "fails"]
        effect = {"rule": tree["title"], "when_conditions_hold": holds, "when_conditions_fail": fails}
        labels = {}
        structure = "The effect follows when:\n" + render(tree["root"], labels)
        for leaf, path in leaves_with_roles(tree["root"]):
            key, label, text = context_for(leaf["source"]["citation"])
            g = groups.setdefault((tree["id"],) + key, {"tree": tree["id"], "instrument": label, "text": text,
                                                       "effect": effect, "structure": structure, "leaves": []})
            g["leaves"].append({"leaf": leaf["id"], "kind": leaf["kind"], "contested": leaf.get("contested"),
                                "label": labels[leaf["id"]], "statement": leaf["statement"],
                                "citation": leaf["source"]["citation"], "quote": leaf["source"]["quote"],
                                "role": role_of(path)})
    reg = core.questions()
    requests = []
    for g in groups.values():
        questions = {}
        for i, lf in enumerate(g["leaves"], 1):
            questions[f"q{i}"] = {"primitive": "noul",
                                  "instructions": {"question": QUESTION,
                                                   "condition": f"[{lf['label']}] {lf['statement']}",
                                                   "quote": lf["quote"]},
                                  "criteria": CRITERIA}
        state = {"instrument": g["instrument"], "source_text": g["text"], "effect": g["effect"],
                 "structure": g["structure"]}
        payload = {"model": reg["model"], "state": state, "questions": questions}
        identity = {"task_version": TASK_VERSION, "pinned_build": reg["pinned_build"], "base_url": reg["base_url"],
                    "payload": payload}
        h = hashlib.sha256(json.dumps(identity, sort_keys=True, ensure_ascii=False,
                                      separators=(",", ":")).encode()).hexdigest()
        requests.append({"request_hash": h, "tree": g["tree"], "instrument": g["instrument"],
                         "leaves": [dict(lf, question_key=f"q{i}") for i, lf in enumerate(g["leaves"], 1)],
                         **identity})
    return requests, reg


async def run(requests, reg, cap):
    from pydantic import BaseModel, ConfigDict
    from typesafe_sdk import AsyncTypeSafeClient, RetryPolicy

    class Raw(BaseModel):
        model_config = ConfigDict(extra="allow")

    CACHE.mkdir(parents=True, exist_ok=True)
    spent = Decimal(0)
    results = {}
    todo = []
    for r in requests:
        c = CACHE / f"{r['request_hash']}.json"
        if c.exists():
            results[r["request_hash"]] = dict(json.loads(c.read_text()), cache_hit=True)
        else:
            todo.append(r)
    if not todo:
        return results, spent
    sem = asyncio.Semaphore(4)
    stop = {"reason": None}
    async with AsyncTypeSafeClient(api_key=jev.api_key(), base_url=reg["base_url"],
                                   retry=RetryPolicy(max_retries=1)) as client:
        async def one(r):
            nonlocal spent
            async with sem:
                if stop["reason"]:
                    return
                if spent + Decimal("0.02") > Decimal(str(cap)):
                    stop["reason"] = f"spend cap ${cap} reached"
                    return
                out = {"status": "execution_error"}
                try:
                    qs = jev.sdk_questions(r["payload"]["questions"])
                    resp = await client.system_one(state=r["payload"]["state"], questions=qs,
                                                   model=r["payload"]["model"], response_model=Raw)
                    raw = resp.model_dump(mode="json")
                    cost = (raw.get("usage") or {}).get("cost")
                    spent += Decimal(str(cost)) if cost is not None else Decimal("0.02")
                    if raw.get("model") != r["pinned_build"]:
                        raise ValueError(f"unexpected build {raw.get('model')}")
                    answers = raw.get("answers") or {}
                    for k in r["payload"]["questions"]:
                        v = (answers.get(k) or {}).get("noul")
                        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                            raise ValueError(f"invalid answer for {k}")
                    out = {"status": "answered", "model": raw.get("model"), "answers": answers,
                           "usage": raw.get("usage")}
                    (CACHE / f"{r['request_hash']}.json").write_text(
                        jev.redact(json.dumps(out, ensure_ascii=False, indent=1)) + "\n")
                except Exception as exc:  # recorded, not raised
                    out["error"] = jev.redact(f"{type(exc).__name__}: {exc}")[:500]
                results[r["request_hash"]] = dict(out, cache_hit=False)
        await asyncio.gather(*(one(r) for r in todo))
    return results, spent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=float, default=2.00)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    requests, reg = build_requests()
    n_leaves = sum(len(r["leaves"]) for r in requests)
    print(f"{len(requests)} requests, {n_leaves} leaf questions")
    if a.dry_run:
        print(json.dumps(requests[0], ensure_ascii=False, indent=1)[:4000])
        return
    results, spent = asyncio.run(run(requests, reg, a.cap))
    prior = json.loads(OUT.read_text()) if OUT.exists() else {}
    reviews = prior.get("reviews", {})
    leaves = []
    for r in requests:
        res = results.get(r["request_hash"], {"status": "not_sent"})
        for lf in r["leaves"]:
            v = ((res.get("answers") or {}).get(lf["question_key"]) or {}).get("noul")
            key = f"{r['tree']}#{lf['leaf']}"
            leaves.append({"key": key, "tree": r["tree"], "leaf": lf["leaf"], "kind": lf["kind"],
                           "contested": lf["contested"], "citation": lf["citation"], "noul": v,
                           "flag": v is not None and v < 0.5, "review": reviews.get(key)})
    total_cost = sum(Decimal(str((x.get("usage") or {}).get("cost") or 0)) for x in results.values())
    doc = {
        "purpose": "Fidelity check of the account-core trees: for each leaf, does the quoted source establish the "
                   "leaf's statement as a condition of (or exception to) the tree's effect? A research aid only; "
                   "low answers are prompts to re-read the statute, not findings.",
        "date": core.today(), "model": reg["model"], "pinned_build": reg["pinned_build"],
        "task_version": TASK_VERSION, "primitive": "noul",
        "question": QUESTION, "criteria": CRITERIA,
        "batching": "One request per tree and cited top-level subdivision; state carries that subdivision's text "
                    "(with the section's lead-in where it has one) and the tree's effects.",
        "summary": {"requests": len(requests), "leaf_questions": n_leaves,
                    "answered": sum(1 for x in leaves if x["noul"] is not None),
                    "below_0.5": sum(1 for x in leaves if x["flag"]),
                    "reported_cost_usd_all_answers": str(total_cost),
                    "spent_this_run_usd": str(spent)},
        "earlier_rounds": prior.get("earlier_rounds", []),
        "reviews": reviews,
        "leaves": leaves,
        "requests": [dict(r, response=results.get(r["request_hash"])) for r in requests],
    }
    OUT.write_text(jev.redact(json.dumps(doc, ensure_ascii=False, indent=1)) + "\n")
    print(json.dumps(doc["summary"]))


if __name__ == "__main__":
    main()
