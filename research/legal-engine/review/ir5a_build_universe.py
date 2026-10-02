"""IR5A: build review/review5a_universe.json from ir5a_items_*.py mechanically.

Each item: (citation, level, kind, decision_point, one_line_effect, source_file, spec). spec is a regex matched against the
whitespace-normalized source text (the matched span is the quote) or a (start, end) anchor pair cut by ir5a_lib.cut.
Prints every failure; writes nothing if any item fails unless --partial.
"""
import glob
import importlib
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ir5a_lib import ROOT, cut, text  # noqa: E402

items, fails = [], []
for mod in sorted(glob.glob(str(ROOT / "review" / "ir5a_items_*.py"))):
    m = importlib.import_module(pathlib.Path(mod).stem)
    for it in m.ITEMS:
        cit, level, kind, dp, eff, src, spec = it
        try:
            if isinstance(spec, tuple):
                q = cut(src, spec[0], spec[1])
            else:
                mm = re.search(spec, text(src))
                if not mm:
                    raise KeyError(f"regex not found: {spec[:80]!r}")
                q = mm.group(0).strip()
                if len(q) > 1300:
                    raise ValueError(f"regex quote too long {len(q)}")
            items.append({"id": f"U5A-{len(items) + 1:03d}", "citation": cit, "level": level, "kind": kind,
                          "decision_point": dp, "one_line_effect": eff, "source_file": src, "verbatim_quote": q})
        except Exception as e:  # noqa: BLE001
            fails.append(f"{pathlib.Path(mod).stem}: {cit}: {e}")
for f in fails:
    print("FAIL", f)
print(len(items), "items;", len(fails), "failures")
if "--show" in sys.argv:
    for it in items:
        print(f"{it['id']} {it['citation']} :: {it['verbatim_quote'][:220]}")
if not fails or "--partial" in sys.argv:
    (ROOT / "review" / "review5a_universe.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
    print("written review/review5a_universe.json")
