"""show: print rules with their quote, sources and reasoning (review/show.py for every jurisdiction).

  python3 -m pipeline show 'NY:GOL-7-108(1-a)(e)' ['NYC:HMC-*' ...]    a trailing * shows every rule with the prefix
"""
from __future__ import annotations

import textwrap

from . import core


def wrap(label, text):
    return textwrap.fill(str(text), 110, initial_indent=f"  {label}: ", subsequent_indent=" " * (len(label) + 4))


def show(a, layer):
    print(f"\n{a['id']}  [{a.get('determinacy')}]  in force {a.get('effective_from')} to {a.get('effective_to') or 'open'}"
          f"  (jurisdictions/{layer}/rules.json)")
    print(wrap("Instrument", f"{a.get('instrument')}, {a.get('provision')}"))
    print(wrap("If", a.get("condition")))
    print(wrap("Then", a.get("effect")))
    if a.get("judgment_terms"):
        print(wrap("Judgment terms", ", ".join(map(str, a["judgment_terms"]))))
    if a.get("gates"):
        print(wrap("Gates", a["gates"]))
    print(wrap("Quote", a.get("quote")))
    print(wrap("Source", f"{a.get('source_file')}  ({a.get('source_url')})"))
    for c in a.get("construction", []) or []:
        print(wrap("Authority", f"{c.get('quote')}  [{c.get('source_file')}]"))
    if a.get("reasoning"):
        print(wrap("Reasoning", a["reasoning"]))
    if a.get("dependencies"):
        print(wrap("Depends on", ", ".join(a["dependencies"])))


def main(args):
    if not args:
        print("usage: python3 -m pipeline show RULE_ID|PREFIX* [...]")
        return 1
    rules = {}
    for c in core.codes():
        for a in core.load_rules(c).get("atoms", []):
            rules[a["id"]] = (a, c)
    missing = 0
    for arg in args:
        hits = [v for i, v in rules.items() if (i.startswith(arg[:-1]) if arg.endswith("*") else i == arg)]
        if not hits:
            print(f"\n{arg}: no such rule")
            missing += 1
        for a, c in hits:
            show(a, c)
    return 1 if missing else 0
