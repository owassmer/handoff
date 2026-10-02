"""diff (keeping a jurisdiction current): re-fetch every saved section, compare hashes, list the changed sections
and the rules citing them.

Each section with a ref is fetched again through its unit's adapter (or instrument default) with the response cache bypassed. The new
body's hash (whitespace-normalized, header excluded) is compared with sections.jsonl sha256. The saved texts are not
touched: new versions go to jurisdictions/<CODE>/diff/<date>/<text path>, and the report to diff/<date>/diff.json
({changed: [{section_id, old, new, new_file, rules}], failed: [{section_id, error}], unchanged}). The rules citing a
section are its match.json rule ids plus the rule ids on its triage row plus every rule in the family whose
source_file is the section's text. A changed section reopens its decision and those rules (J6 to J8).
Exits non-zero when any section changed or could not be re-fetched.
"""
from __future__ import annotations

import pathlib

from . import adapters, core
from .adapters import base


def citing(code, sids):
    m = core.read_json(core.jdir(code) / "match.json", {"sections": {}})["sections"]
    tri = {r["section_id"]: r for r in core.triage(code)}
    secs = {s["section_id"]: s for s in core.sections(code)}
    by_file = {}
    for c in core.family(code):
        for a in core.load_rules(c).get("atoms", []):
            by_file.setdefault(a.get("source_file"), []).append(a["id"])
    out = {}
    for sid in sids:
        ids = list(m.get(sid) or []) + list((tri.get(sid) or {}).get("rule_ids") or [])
        ids += by_file.get((secs.get(sid) or {}).get("text_file"), [])
        out[sid] = sorted(set(ids))
    return out


def main(code, limit=None, instrument=None):
    inst = {i["id"]: i for i in core.instruments(code).get("instruments", [])}
    secs = [s for s in core.sections(code) if s.get("text_file") and s.get("ref")
            and (not instrument or s["instrument"] == instrument)]
    if limit:
        secs = secs[:limit]
    if not secs:
        print(f"{code} diff: no saved section with a ref to re-fetch")
        return 1
    out_dir = core.jdir(code) / "diff" / core.today()
    changed, failed, same = [], [], 0
    base.REFRESH["on"] = True
    try:
        for s in secs:
            try:
                instrument_record = inst[s["instrument"]]
                unit_record = next((u for u in instrument_record.get("units_in_scope", [])
                                    if u["unit"] == s["unit"]), {})
                ad = adapters.get(unit_record.get("adapter", instrument_record["adapter"]))
                sec = ad.section(s["ref"])
            except Exception as e:  # noqa: BLE001
                failed.append({"section_id": s["section_id"], "error": str(e)[:400]})
                continue
            new_file = out_dir / pathlib.Path(s["text_file"]).relative_to(core.rel(core.jdir(code)))
            text = ad.save(new_file, sec)
            h = core.text_hash(text)
            old = s.get("sha256") or core.text_hash((core.ROOT / s["text_file"]).read_text(errors="replace"))
            if h != old:
                changed.append({"section_id": s["section_id"], "old": old, "new": h, "new_file": core.rel(new_file)})
            else:
                same += 1
                new_file.unlink()
    finally:
        base.REFRESH["on"] = False
    cites = citing(code, [c["section_id"] for c in changed])
    for c in changed:
        c["rules"] = cites[c["section_id"]]
    core.write_json(out_dir / "diff.json", {"jurisdiction": code, "date": core.now(), "checked": len(secs),
                                           "unchanged": same, "changed": changed, "failed": failed})
    print(f"{code} diff: {len(secs)} sections re-fetched; {same} unchanged, {len(changed)} changed, {len(failed)} failed; "
          f"report {core.rel(out_dir / 'diff.json')}")
    for c in changed:
        print(f"  CHANGED {c['section_id']}: rules citing it {c['rules'] or 'none'}")
    for f in failed:
        print(f"  FAILED {f['section_id']}: {f['error'][:160]}")
    return 1 if changed or failed else 0
