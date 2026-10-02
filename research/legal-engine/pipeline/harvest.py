"""harvest (J2): fetch tables of contents and section texts through the adapters; write texts/ and sections.jsonl.

For every instrument in instruments.json and every unit in its units_in_scope:
  1. The unit's section list: units_in_scope[].section_list [{number, heading, ref}] when given, else the adapter's
     toc(instrument, unit) (the unit's toc_url). The count is recorded as units_in_scope[].sections.
  2. Every section's text: jurisdictions/<CODE>/texts/<CODE>_<INST>/<number>.txt, saved mechanically with a
     SOURCE/RETRIEVED header by the adapter. Header-backed texts are reused only when the selected source agrees
     with the prior inventory ref (or the saved SOURCE URL). Changed sources stop before writes for explicit
     source/version reconciliation. Same-URL reuse does not establish currentness; diff/refresh remains separate.
  3. sections.jsonl: {section_id (<CODE>:<INST> <number>), instrument, unit, heading, text_file, chars (body
     characters), sha256 (whitespace-normalized body), repealed, ref, source_url}.
A fetch that fails by every route is recorded in instruments.json fetch_gaps.section_gaps with the routes tried; a
table of contents that fails is recorded in fetch_gaps.instrument_gaps. Both are resolved by another route
(principles) and harvest rerun; resolved gaps are removed. Exits non-zero while any in-scope section lacks text
(the J2 gate).
"""
from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlsplit

from . import adapters, core

REPEALED = re.compile(r"\b(repealed|reserved)\b", re.I)


def short(iid):
    return iid.split(":", 1)[1]


def text_path(code, iid, number):
    safe = re.sub(r"[^A-Za-z0-9.\-]+", "_", str(number)).strip("_") or "x"
    return core.jdir(code) / "texts" / f"{code}_{re.sub(r'[^A-Za-z0-9.-]+', '_', short(iid))}" / f"{safe}.txt"


def row_for(code, iid, unit, entry, path, unit_kind=None):
    sid = f"{code}:{short(iid)} {entry['number']}"
    row = {"section_id": sid, "instrument": iid, "unit": unit, "heading": entry.get("heading") or "",
           "text_file": None, "chars": 0, "sha256": None, "repealed": bool(REPEALED.search(entry.get("heading") or "")),
           "ref": entry.get("ref"), "source_url": None}
    row["source_unit_kind"] = entry.get("source_unit_kind", unit_kind or "section")
    if entry.get("source_authority"):
        row["source_authority"] = entry["source_authority"]
    if entry.get("legal_section_number"):
        row["legal_section_number"] = entry["legal_section_number"]
    if path.exists():
        t = path.read_text(errors="replace")
        if core.has_header(t):
            body = core.body_of(t)
            row.update(text_file=core.rel(path), chars=len(body.strip()), sha256=core.text_hash(t),
                       source_url=core.source_url_of(path),
                       repealed=row["repealed"] or bool(re.match(r"\s*\S*\s*(\[)?\s*(repealed|reserved)", body[:200], re.I)))
    return row


def check_identities(code, rows):
    """Refuse ambiguous section identities or filenames before fetching/saving text."""
    ids, paths = {}, {}
    for row in rows:
        sid = row["section_id"]
        path = text_path(code, row["instrument"], sid.split(" ", 1)[1])
        if sid in ids:
            raise core.PipelineError(f"duplicate harvest section {sid}: units {ids[sid]!r} and {row['unit']!r}")
        if path in paths:
            raise core.PipelineError(f"harvest text path collision: {paths[path]} and {sid} -> {path.name}")
        ids[sid], paths[path] = row["unit"], sid


def reference_identity(adapter, ref):
    if adapter.name == "ca_leginfo":
        from .adapters.ca_leginfo import url_of
        ref = url_of(ref)
    if not ref.startswith(("https://", "http://")):
        return ref
    url = urlsplit(ref)
    return url.scheme.lower(), url.netloc.lower(), url.path, sorted(parse_qsl(url.query, keep_blank_values=True)), url.fragment


def check_reuse(adapter, entry, row, old_row):
    if not row["text_file"]:
        return
    if (old_row or {}).get("source_unit_kind") == "document" and row["source_unit_kind"] != "document":
        raise core.PipelineError(f"{row['section_id']}: a saved whole document cannot be relabeled as a section; "
                                 "enumerate/extract its internal sections before reuse")
    prior_ref = (old_row or {}).get("ref") or row["source_url"]
    if not prior_ref or reference_identity(adapter, prior_ref) != reference_identity(adapter, entry["ref"]):
        raise core.PipelineError(f"{row['section_id']}: saved text source {prior_ref!r} differs from selected "
                                 f"source {entry['ref']!r}; reconcile the source/version before harvest; "
                                 "existing text and inventory are preserved")


def main(code, instrument=None, unit=None, limit=None, dry_run=False):
    doc = core.instruments(code)
    gaps = doc.setdefault("fetch_gaps", {"section_gaps": [], "instrument_gaps": []})
    gaps.setdefault("section_gaps", [])
    gaps.setdefault("instrument_gaps", [])
    old_rows = {r["section_id"]: r for r in core.sections(code)}
    kept = [r for r in core.sections(code)
            if (instrument and r["instrument"] != instrument) or (unit and r["unit"] != unit)]
    new_rows, fetched, reused, failed, tocs = [], 0, 0, [], 0
    sec_gaps = {g["section_id"]: g for g in gaps["section_gaps"]}
    inst_gaps = {(g.get("instrument"), g.get("unit")): g for g in gaps["instrument_gaps"]}
    budget = limit
    plans = []
    toc_failed = False
    for i in doc.get("instruments", []):
        if instrument and i["id"] != instrument:
            continue
        for u in i.get("units_in_scope", []):
            if unit and u["unit"] != unit:
                continue
            try:
                ad = adapters.get(u.get("adapter", i["adapter"]))
                toc = u["section_list"] if "section_list" in u else ad.toc(i, u)
                if not toc:
                    raise core.PipelineError("selected unit enumeration is empty; verify its source and scope")
                if any(not str(e.get("number", "")).strip() or not e.get("ref") for e in toc):
                    raise core.PipelineError("selected unit enumeration contains an entry without number/ref")
                tocs += 1
                inst_gaps.pop((i["id"], u["unit"]), None)
            except (core.PipelineError, Exception) as e:  # noqa: BLE001
                toc_failed = True
                inst_gaps[(i["id"], u["unit"])] = {"instrument": i["id"], "unit": u["unit"], "adapter": u.get("adapter", i["adapter"]),
                                                   "gap": "table of contents not read", "error": str(e)[:600],
                                                   "date": core.today()}
                print(f"  TOC FAILED {i['id']} {u['unit']}: {str(e)[:200]}")
                new_rows += [r for r in old_rows.values() if r["instrument"] == i["id"] and r["unit"] == u["unit"]]
                continue
            plans.append((i, u, ad, toc))

    if toc_failed:
        gaps["instrument_gaps"] = list(inst_gaps.values())
        if not dry_run:
            core.write_json(core.jdir(code) / "instruments.json", doc)
        print(f"{code} harvest: enumeration failed; existing sections.jsonl and texts preserved")
        return 1

    planned_rows = [row_for(code, i["id"], u["unit"], e, text_path(code, i["id"], e["number"]), u.get("source_unit_kind"))
                    for i, u, ad, toc in plans for e in toc]
    check_identities(code, kept + new_rows + planned_rows)
    for i, u, ad, toc in plans:
        u["sections"] = len(toc)
        for e in toc:
            row = row_for(code, i["id"], u["unit"], e, text_path(code, i["id"], e["number"]), u.get("source_unit_kind"))
            check_reuse(ad, e, row, old_rows.get(row["section_id"]))
    for i, u, ad, toc in plans:
        for e in toc:
            path = text_path(code, i["id"], e["number"])
            row = row_for(code, i["id"], u["unit"], e, path, u.get("source_unit_kind"))
            sid = row["section_id"]
            if row["text_file"]:
                reused += 1
                sec_gaps.pop(sid, None)
            elif dry_run or (budget is not None and budget <= 0):
                pass
            else:
                if budget is not None:
                    budget -= 1
                try:
                    sec = ad.section(e["ref"])
                    ad.save(path, sec)
                    fetched += 1
                    row = row_for(code, i["id"], u["unit"], e, path, u.get("source_unit_kind"))
                    sec_gaps.pop(sid, None)
                except (core.PipelineError, Exception) as ex:  # noqa: BLE001
                    msg = str(ex)
                    tried = re.search(r"\(([^()]*(?:curl|browser|archive|manual)[^()]*)\)", msg)
                    sec_gaps[sid] = {"section_id": sid, "ref": e["ref"], "adapter": ad.name,
                                     "routes_tried": tried.group(1).split("; ") if tried else [],
                                     "error": msg[:600], "date": core.today()}
                    failed.append(sid)
                    print(f"  FAILED {sid}: {msg[:200]}")
            new_rows.append(row)
    rows = kept + new_rows
    ids = {r["section_id"] for r in rows}
    gaps["section_gaps"] = [g for g in sec_gaps.values() if g["section_id"] in ids]
    gaps["instrument_gaps"] = list(inst_gaps.values())
    if not dry_run:
        order = {i["id"]: n for n, i in enumerate(doc.get("instruments", []))}
        rows.sort(key=lambda r: order.get(r["instrument"], 1 << 20))
        core.write_jsonl(core.jdir(code) / "sections.jsonl", rows)
        core.write_json(core.jdir(code) / "instruments.json", doc)
    missing = [r["section_id"] for r in rows if not r.get("text_file")]
    documents = [r["section_id"] for r in rows if r.get("source_unit_kind") == "document"]
    mirrors = [r["section_id"] for r in rows if r.get("source_authority") == "mirror"]
    print(f"{code} harvest: {tocs} unit tables of contents read; {len(new_rows)} sections listed; {fetched} fetched, "
          f"{reused} already saved (not refetched), {len(failed)} failed; {len(rows)} sections in sections.jsonl; "
          f"{len(missing)} without text; {len(gaps['instrument_gaps'])} unit TOC gaps"
          f"{' (dry run, nothing written)' if dry_run else ''}")
    if missing:
        print(f"  J2 gate not met: {len(missing)} in-scope sections without saved text (first {missing[:5]}); "
              f"resolve each by another route and rerun")
    if documents:
        print(f"  J2 enumeration pending: {len(documents)} whole documents require internal section enumeration")
    if mirrors:
        print(f"  J2 official source reconciliation pending: {len(mirrors)} mirror section texts")
    return 1 if missing or gaps["instrument_gaps"] or documents or mirrors else 0
