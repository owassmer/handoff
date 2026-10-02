"""apply (J6 step 4): turn accepted decisions into rules per adjudication.json. Idempotent, with backups.

adjudication.json:
  proposals: {rule id: {ruling: accept | modify | reject, note, conditions: [{condition, met}], set: {field: value}}}
             'modify' must carry 'set' (the fields that change); a condition not met stops the whole apply.
  existing_rule_changes: [{rule_id, change, source_file, quote, set: {field: value}}]
             the quote is asserted verbatim in source_file before the change is made.
  merges: [{into, from: [ids]}]  proposals stating the same law: the 'from' ids are not added; their sections
             cite 'into' instead. Every merge is recorded in DISPOSITION.md.
A proposal's optional 'checks': [{source_file, phrase}] asserts figures stated beyond its quote (like must()).

Nothing is written when the result equals the current rules.json (a rerun changes nothing). Before the first write
of a new state, rules.json is copied to backups/rules.<content hash>.json. Each apply that changes something appends
its counts and the rule-check result to DISPOSITION.md.
"""
from __future__ import annotations

import collections
import copy

from . import core, decisions, rulecheck


def proposals(code):
    out = collections.OrderedDict()
    for n in decisions.batch_numbers(code):
        for r in core.read_jsonl(core.jdir(code) / "decisions" / f"decisions_{n}.jsonl"):
            for p in r.get("proposed", []) or []:
                out.setdefault(p["id"], (n, r["section_id"], p))
    return out


def build(code):
    """Return (new rules doc, report dict, triage rule_ids {sid: [ids]}) without writing anything."""
    adj = core.read_json(core.jdir(code) / "adjudication.json",
                         {"proposals": {}, "existing_rule_changes": [], "merges": []})
    doc = copy.deepcopy(core.load_rules(code))
    atoms = doc.setdefault("atoms", [])
    idx = {a["id"]: i for i, a in enumerate(atoms)}
    props = proposals(code)
    rulings = adj.get("proposals", {})
    rep = collections.Counter()
    errs, notes = [], []
    merged_from = {}
    for m in adj.get("merges", []):
        for f in m.get("from", []):
            merged_from[f] = m["into"]
    for pid, ruling in rulings.items():
        unmet = [c for c in ruling.get("conditions", []) or [] if not (isinstance(c, dict) and c.get("met"))]
        if unmet and ruling.get("ruling") in ("accept", "modify"):
            errs.append(f"{pid}: {len(unmet)} condition(s) not met: {unmet[:2]}")
        if pid not in props:
            errs.append(f"{pid}: ruled on but proposed in no decisions file")
    applied = {}
    for pid, (n, sid, p) in props.items():
        r = rulings.get(pid)
        if not r:
            rep["unruled"] += 1
            continue
        if r.get("ruling") == "reject":
            rep["rejected"] += 1
            continue
        if r.get("ruling") not in ("accept", "modify"):
            errs.append(f"{pid}: ruling {r.get('ruling')!r}")
            continue
        if pid in merged_from:
            rep["merged"] += 1
            notes.append(f"{pid} merged into {merged_from[pid]}")
            continue
        if core.code_of(pid) != code:
            errs.append(f"{pid}: id prefix is not {code}:")
            continue
        if r["ruling"] == "modify" and not r.get("set"):
            errs.append(f"{pid}: modify needs 'set' with the changed fields")
            continue
        rule = decisions.applied_form(p)
        rule.update(r.get("set") or {})
        rule["origin"] = {"batch": n, "section_id": sid, "proposal": pid, "ruling": r["ruling"],
                          "severity": p.get("severity"), "walk_step": p.get("walk_step"),
                          **({"amends": p["amends"]} if p.get("amends") else {})}
        for c in p.get("checks", []) or []:
            e = core.verbatim(c["source_file"], c["phrase"])
            if e:
                errs.append(f"{pid}: check '{c['phrase'][:60]}': {e}")
        e = core.verbatim(rule.get("source_file"), rule.get("quote"))
        if e:
            errs.append(f"{pid}: {e}")
        if pid in idx:
            cur = atoms[idx[pid]]
            if (cur.get("origin") or {}).get("proposal") != pid:
                errs.append(f"{pid}: an existing rule has this id and did not come from this proposal")
                continue
            if cur != rule:
                atoms[idx[pid]] = rule
                rep["updated"] += 1
            else:
                rep["unchanged"] += 1
        else:
            idx[pid] = len(atoms)
            atoms.append(rule)
            rep["added"] += 1
        applied[pid] = sid
    for ch in adj.get("existing_rule_changes", []):
        rid = ch.get("rule_id")
        if rid not in idx:
            errs.append(f"change to {rid}: no such rule in {code}")
            continue
        e = core.verbatim(ch.get("source_file"), ch.get("quote"))
        if e:
            errs.append(f"change to {rid}: {e}")
            continue
        if not ch.get("set"):
            errs.append(f"change to {rid}: needs 'set' with the changed fields")
            continue
        a = atoms[idx[rid]]
        new = dict(a, **ch["set"])
        if new != a:
            atoms[idx[rid]] = new
            rep["existing_changed"] += 1
    for m in adj.get("merges", []):
        if m["into"] not in idx:
            errs.append(f"merge into {m['into']}: not a rule after apply")
    # rule ids per decided section
    rule_ids = {}
    for n in decisions.batch_numbers(code):
        for r in core.read_jsonl(core.jdir(code) / "decisions" / f"decisions_{n}.jsonl"):
            ids = list(r.get("atom_ids") or [])
            for p in r.get("proposed", []) or []:
                t = merged_from.get(p["id"]) or (p["id"] if p["id"] in applied else None)
                if t and t not in ids:
                    ids.append(t)
            rule_ids[r["section_id"]] = ids
    return doc, rep, rule_ids, errs, notes


def main(code):
    doc, rep, rule_ids, errs, notes = build(code)
    if errs:
        print(f"{code} apply: stopped, nothing written ({len(errs)} problems)")
        for e in errs[:60]:
            print("  " + e)
        return 1
    cur = core.load_rules(code)
    rows = core.triage(code)
    for r in rows:
        if r.get("decided_by") == "reviewer" and r["section_id"] in rule_ids:
            r["rule_ids"] = rule_ids[r["section_id"]]
    changed_rules = core.dumps(doc) != core.dumps(cur)
    if changed_rules:
        core.backup(core.rules_file(code), core.jdir(code) / "backups")
        core.write_json(core.rules_file(code), doc)
    changed_triage = core.write_jsonl(core.jdir(code) / "triage.jsonl", rows)
    summary = ", ".join(f"{k} {v}" for k, v in sorted(rep.items())) or "no proposals"
    if not changed_rules and not changed_triage:
        print(f"{code} apply: no changes ({summary})")
        return 0
    errs2, n = rulecheck.check(code)
    lines = [f"\n## Apply {core.now()}\n", f"- Proposals: {summary}.",
             f"- rules.json: {n} rules{' (changed; backup taken)' if changed_rules else ' (unchanged)'}; "
             f"triage rule ids {'updated' if changed_triage else 'unchanged'}."]
    lines += [f"- Merge: {x}." for x in notes]
    lines.append(f"- Rule check: {len(errs2)} errors." + ("" if not errs2 else " First: " + "; ".join(errs2[:5])))
    disp = core.jdir(code) / "DISPOSITION.md"
    with disp.open("a") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{code} apply: {summary}; {n} rules; rule check {len(errs2)} errors; recorded in DISPOSITION.md")
    return 1 if errs2 else 0
