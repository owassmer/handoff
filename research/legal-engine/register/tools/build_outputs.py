"""Step 5 outputs from sections.jsonl, match.json, jev_results.jsonl and routing.json (current version):
triage.jsonl, review_queue.json, instruments.json, fetch_gaps.json. Code only; idempotent."""
import collections
import datetime
import hashlib
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import calibrate  # noqa: E402
import cites  # noqa: E402
import route  # noqa: E402

REG = pathlib.Path(__file__).resolve().parent.parent
ROOT = REG.parent

NON_CODE_CLASSES = [
    (r"^L\.\d{4}|session|chapter amendment", "session law (effective-date, application or amendment clauses)"),
    (r"AGENCY GUIDANCE|Fact Sheet|fact sheet|FAQ|Handbook|Publication|Property Type Table|website|web page|Guide", "agency guidance"),
    (r"[Ff]orm|[Vv]oucher|[Mm]odel [Ll]ease|Contract", "agency form or prescribed contract"),
    (r"Notice of Change|Department of Defense notice|City Record|Notice of Adoption", "official notice"),
    (r" v\.? |case law|common law|interpretive authority|Court of Appeals|Supreme Court|Cir\.", "case law or common law"),
    (r"SHIELD Rule|Charter", "rule text read with an official notice"),
    (r"Housing Maintenance Code|RSC", "code section read with guidance and case law"),
]
CONSIDERED_NOT_ADDED = [
    {"instrument": "CAN-SPAM Act, 15 U.S.C. 7701-7713", "why_not": "Collection and account e-mails to a former tenant are transactional or relationship messages; the Act's operative duties reach commercial advertising."},
    {"instrument": "Regulation Z, 12 CFR part 1026", "why_not": "TILA credit disclosures do not reach a residential lease; the only TILA provisions the rules use are the 15 U.S.C. 1602 definitions, registered in 15 USC ch. 41 subch. I pt. A."},
    {"instrument": "FTC Disposal Rule, 16 CFR part 682", "why_not": "Duty to dispose of consumer report information securely arises from possession of screening reports, not from any step of the settlement chain; 12 CFR 1022 subpart E/I and 15 U.S.C. 1681w (registered) cover the chain's reporting uses."},
    {"instrument": "Rehabilitation Act 504 (29 U.S.C. 794) and ADA title III", "why_not": "A private market-rate landlord is not a recipient of federal financial assistance by accepting a voucher, and a residential unit is not a public accommodation; disability rules reach the chain through 42 U.S.C. 3604(f), NY Exec. Law art. 15 and NYC Admin. Code tit. 8 (registered)."},
    {"instrument": "NY Public Health Law art. 13 title 10 (lead)", "why_not": "In NYC the lead duties that reach tenancies and turnovers are Admin. Code 27-2056.1-27-2056.18 and 28 RCNY ch. 11 (registered)."},
    {"instrument": "NY Real Property Tax Law 467-b/467-c (SCRIE/DRIE)", "why_not": "Out of aperture: applies to rent-regulated and Mitchell-Lama units."},
    {"instrument": "NY Private Housing Finance Law", "why_not": "Out of aperture: subsidized and limited-profit housing."},
    {"instrument": "NY Lien Law and Personal Property Law", "why_not": "No lien of a residential landlord on a tenant's goods exists (distress abolished, RPL 230 area); storage and sale of goods by warehousemen does not describe a landlord holding a former tenant's belongings (common-law rules are stated by case-law atoms)."},
    {"instrument": "NY Banking Law and Financial Services Law", "why_not": "The deposit-account duties of the chain are GOL 7-103 and 7-105 (registered); bank-side rules govern the bank, not the landlord."},
    {"instrument": "31 CFR 1010.330 (cash over $10,000, Form 8300)", "why_not": "Implements 26 U.S.C. 6050I, which is registered in the IRC information-return unit and triaged there; the Treasury/FinCEN regulation adds form mechanics only."},
    {"instrument": "Virginia and California law", "why_not": "Out of aperture (the chain is a market-rate NYC unit)."},
]
INSTRUMENT_GAPS = [
    {"instrument": "NY:CCA, NY:SCPA", "gap": "Text read from Internet Archive captures of nysenate.gov (2025-04 to 2026-01), not the live site.",
     "attempted": ["https://www.nysenate.gov/legislation/laws/CCA/1801 (Cloudflare challenge to curl and to the browser)",
                   "https://legislation.nysenate.gov/api/3/laws/CCA/1801 (API key required)",
                   "https://codes.findlaw.com/ny/new-york-city-civil-court-act/nyc-civ-ct-act-sect-1801/ (Cloudflare 403)",
                   "https://law.justia.com/codes/new-york/cca/article-18/1801/ (Cloudflare 403)",
                   "https://public.leginfo.state.ny.us/lawssrch.cgi?NVLWO: (Cloudflare challenge)",
                   "newyork.public.law (does not carry CCA or SCPA)"],
     "effect": "An amendment published after a section's capture date would be missing. Each saved text records its capture URL and the page's own 'published on' date."},
    {"instrument": "NY NYCRR (9, 16, 18, 19, 22, 23)", "gap": "Text from Cornell LII's republication of the official NYCRR (quarterly updates); govt.westlaw.com/nycrr now returns a Cloudflare challenge to curl.",
     "attempted": ["https://govt.westlaw.com/nycrr/Browse/Home/NewYork/NewYorkCodesRulesandRegulations (Cloudflare 403)"],
     "effect": "A rule amended since LII's last quarterly load would be stale; LII notes (amendment history) are saved after each text."},
    {"instrument": "NY statutes (public.law)", "gap": "newyork.public.law mirrors nysenate.gov (pages state 'last accessed Sep. 26, 2026'); nysenate.gov itself is walled.",
     "attempted": ["https://www.nysenate.gov/legislation/laws/GOB/7-108 (Cloudflare challenge)"],
     "effect": "Text is as of the mirror's last access date recorded on each page."},
    {"instrument": "NYC:RCNY 6 5-76, 5-77 and ch. 2 subch. S (SHIELD Rule)", "gap": "The register holds the current text from American Legal's XML; the SHIELD amendments adopted 2026-02-26 take effect 2027-01-01 and are not in the current compilation.",
     "attempted": ["http://files.amlegal.com/pdffiles/NewYorkCity/Rules/XML.zip (current compilation)"],
     "effect": "Future-effective text is stated by rule-file atoms from the City Record Notice of Adoption (sources/NYC_DCWP_SHIELD_NOA_2026.txt), not by register sections."},
    {"instrument": "Pending bills (S9760/A10182-A, S947/A3121, S9650/A659)", "gap": "Not law; tracked by rule-file atoms as dated future items, outside the code register.",
     "attempted": [], "effect": "None for the current register."},
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    secs = {json.loads(l)["section_id"]: json.loads(l) for l in (REG / "sections.jsonl").read_text().splitlines() if l.strip()}
    match = json.loads((REG / "match.json").read_text())
    m = match["sections"]
    jev = {}
    for l in (REG / "jev_results.jsonl").read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            jev[r["section_id"]] = r
    rj = json.loads((REG / "routing.json").read_text())
    ver = rj["current"]
    cfg = rj["versions"][ver]
    ctx = calibrate.contexts(secs, m, cfg)
    rows = []
    for sid, s in secs.items():
        j = jev.get(sid)
        st, why = route.route(s, j, cfg, ctx[sid])
        rows.append({"section_id": sid, "instrument": s["instrument"], "unit": s["unit"], "heading": s["heading"],
                     "status": st, "reason": why, "routing_version": ver, "atom_ids": m[sid]["atom_ids"],
                     "universe_4a": m[sid]["universe_4a"], "universe_5a": m[sid]["universe_5a"], "gap_5a": m[sid]["gap_5a"],
                     "jev": None if not j else {k: j[k] for k in ("role", "role_probabilities", "role_confidence", "chain_duty",
                                                                   "returned_model", "cache_key", "registry_version")},
                     "hand_reason": why[6:] if why.startswith("HAND:") else None})
    (REG / "triage.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))

    rq = collections.defaultdict(list)
    for r in rows:
        if r["status"] in ("review_queue", "unfetched"):
            s = secs[r["section_id"]]
            body = ""
            if s.get("text_file"):
                t = (REG / s["text_file"]).read_text()
                body = re.sub(r"\s+", " ", t.split("\n\n", 1)[1] if "\n\n" in t else t).strip()
            p = (r["jev"] or {}).get("role_probabilities") or {}
            rq[r["instrument"]].append({"section_id": r["section_id"], "unit": r["unit"], "heading": r["heading"],
                                        "p_decides": p.get("DECIDES"), "chain_duty": (r["jev"] or {}).get("chain_duty"),
                                        "role": (r["jev"] or {}).get("role"), "reason": r["reason"],
                                        "cited_by": r["universe_4a"] + r["universe_5a"], "excerpt": body[:300]})
    for k in rq:
        rq[k].sort(key=lambda x: (-(x["p_decides"] if x["p_decides"] is not None else -1), x["section_id"]))
    (REG / "review_queue.json").write_text(json.dumps({
        "routing_version": ver, "count": sum(len(v) for v in rq.values()),
        "order": "grouped by instrument; within an instrument highest P(DECIDES) first; sections without a Jev answer (LONG, definitions/applicability in stated units) last",
        "by_instrument": dict(sorted(rq.items(), key=lambda x: -len(x[1])))}, indent=1))

    core = json.loads((REG / ".work" / "instruments_core.json").read_text())
    stc = collections.defaultdict(collections.Counter)
    for r in rows:
        stc[r["instrument"]][r["status"]] += 1
    for i in core:
        i["section_status_counts"] = dict(stc.get(i["id"], {}))
    # non-code sources: atoms whose provision cites no code section
    non_code = collections.OrderedDict()
    for f in ("NY", "NYC", "US"):
        for a in json.loads((ROOT / "stage-a" / f"{f}.json").read_text())["atoms"]:
            if not match["atom_citations"][a["id"]]:
                cls = next((c for rx, c in NON_CODE_CLASSES if re.search(rx, a["instrument"])), "other (see atom)")
                e = non_code.setdefault(a["instrument"], {"instrument": a["instrument"], "class": cls, "atom_ids": []})
                e["atom_ids"].append(a["id"])
    out_cites = collections.defaultdict(list)
    for u in match["unmatched"]:
        out_cites[u["instrument"]].append({"atom_id": u["atom_id"], "citation": f"{u['key']} {u['number']}", "via": u["via"]})
    hashes = {f"stage-a/{f}.json": sha(ROOT / "stage-a" / f"{f}.json") for f in ("NY", "NYC", "US")}
    (REG / "instruments.json").write_text(json.dumps({
        "generated": datetime.date.today().isoformat(), "routing_version": ver, "rule_file_sha256": hashes,
        "summary": {"instruments": len(core), "units_in_scope": sum(len(i["units_in_scope"]) for i in core),
                    "units_out": sum(len(i["units_out"]) for i in core), "sections": len(rows)},
        "instruments": core,
        "non_code_sources": list(non_code.values()),
        "atom_citations_in_out_of_scope_units": {k: {"count": len(v), "citations": v} for k, v in out_cites.items()},
        "considered_not_added": CONSIDERED_NOT_ADDED}, indent=1))
    gaps = json.loads((REG / ".work" / "fetch_gaps_sections.json").read_text())
    (REG / "fetch_gaps.json").write_text(json.dumps({"section_gaps": gaps, "instrument_gaps": INSTRUMENT_GAPS}, indent=1))
    c = collections.Counter(r["status"] for r in rows)
    print("statuses:", dict(c), "review queue:", sum(len(v) for v in rq.values()))


if __name__ == "__main__":
    main()
