"""Print Stage A rules with their quotes and sources.

Usage: python3 review/show.py 'NY:GOL-7-108(1-a)(e)' [more ids or prefixes ending in *]
Example: python3 review/show.py 'NY:ADJ-*'
"""
import json
import pathlib
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATOMS = {}
for k in ("NY", "NYC", "VA", "US"):
    for a in json.loads((ROOT / f"stage-a/{k}.json").read_text())["atoms"]:
        ATOMS[a["id"]] = a


def wrap(label, text):
    return textwrap.fill(str(text), 110, initial_indent=f"  {label}: ", subsequent_indent=" " * (len(label) + 4))


def show(a):
    print(f"\n{a['id']}  [{a['determinacy']}]  in force {a['effective_from']} to {a['effective_to'] or 'open'}")
    print(wrap("Instrument", f"{a['instrument']}, {a['provision']}"))
    print(wrap("If", a["condition"]))
    print(wrap("Then", a["effect"]))
    if a.get("judgment_terms"):
        print(wrap("Judgment terms", ", ".join(map(str, a["judgment_terms"]))))
    print(wrap("Quote", a["quote"]))
    print(wrap("Source", f"{a['source_file']}  ({a['source_url']})"))
    for c in a.get("construction", []):
        print(wrap("Authority", f"{c['quote']}  [{c['source_file']}]"))
    if a.get("reasoning"):
        print(wrap("Reasoning", a["reasoning"]))


for arg in sys.argv[1:]:
    hits = [a for i, a in ATOMS.items() if (i.startswith(arg[:-1]) if arg.endswith("*") else i == arg)]
    if not hits:
        print(f"\n{arg}: no such rule")
    for a in hits:
        show(a)
