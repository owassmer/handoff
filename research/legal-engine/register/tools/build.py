"""Build register/instruments.json and register/sections.jsonl (Steps 1-2) from the harvested tables of contents,
the scope decisions in tools/scope.py and the saved texts. Saves texts for local-source instruments (NYC XML, USLM,
eCFR) mechanically; NY statutes, CCA/SCPA and NYCRR texts are saved by their fetchers. Idempotent: never overwrites
a saved text. Writes register/fetch_gaps.json for in-scope sections without saved text.
"""
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import aml  # noqa: E402
import ecfr  # noqa: E402
import harvest_ny  # noqa: E402
import nylaw  # noqa: E402
import scope  # noqa: E402
import senate_archive  # noqa: E402
import usc  # noqa: E402

REG = pathlib.Path(__file__).resolve().parent.parent
TEXTS = REG / "texts"
TODAY = datetime.date.today().isoformat()
INSTRUMENTS, SECTIONS, GAPS = [], [], []

NY_NAMES = {"GOL": ("General Obligations Law", "GOL"), "RPL": ("Real Property Law", "RPL"),
            "RPAPL": ("Real Property Actions and Proceedings Law", "RPAPL"), "MDL": ("Multiple Dwelling Law", "MDL"),
            "CPLR": ("Civil Practice Law and Rules", "CPLR"), "GBL": ("General Business Law", "GBL"),
            "JUD": ("Judiciary Law", "Judiciary Law"), "UCC": ("Uniform Commercial Code", "UCC"),
            "ABP": ("Abandoned Property Law", "ABP"), "EPTL": ("Estates, Powers and Trusts Law", "EPTL"),
            "MIL": ("Military Law", "Military Law"), "EXEC": ("Executive Law", "Executive Law"),
            "LLC": ("Limited Liability Company Law", "LLC Law"), "BCL": ("Business Corporation Law", "BCL"),
            "NPCL": ("Not-for-Profit Corporation Law", "N-PCL"), "GCN": ("General Construction Law", "GCN"),
            "STT": ("State Technology Law", "STT"), "SSL": ("Social Services Law", "SSL"),
            "DCL": ("Debtor and Creditor Law", "DCL"), "PTR": ("Partnership Law", "Partnership Law"),
            "MHY": ("Mental Hygiene Law", "MHL"), "CCA": ("New York City Civil Court Act", "CCA"),
            "SCP": ("Surrogate's Court Procedure Act", "SCPA")}
ADDED = {  # instruments not named in the rule files or the 4A/5A universes, and why they govern the chain
    "NY:NPCL": "A not-for-profit corporate landlord that is foreign and unauthorized cannot maintain an action (N-PCL 1312), the analogue of BCL 1312 already stated.",
    "NY:DCL": "Personal bankruptcy exemptions (DCL 282-283) decide whether a debtor-tenant keeps the deposit refund; DCL 150 cancels judgments after discharge; DCL 151 governs setoff on insolvency.",
    "NY:PTR": "A foreign limited partnership or LLP landlord that has not registered cannot maintain an action (Partnership Law 121-907, 121-1502), the analogue of LLC Law 808 and BCL 1312.",
    "NY:MHY": "A guardian appointed under MHL art. 81 acts for an incapacitated tenant and may be the proper payee or party.",
    "US:24CFR5": "24 CFR part 5 subpart L implements VAWA's housing protections (34 USC 12491) for the Housing Choice Voucher program, which a market-rate NYC unit can host.",
    "US:12CFR1005": "Regulation E implements the Electronic Fund Transfer Act (15 USC ch. 41 subch. VI, in scope): preauthorized debits of a former tenant's account for final charges and electronic refunds are governed by 1005.10.",
    "NY:9NYCRR": "Registered for DHR regulations (Part 466) and the RS/RC routing parts; Part 540 (ESRA regulations) added because STT 305 is stated and Part 540 sets how electronic signatures and records are used.",
    "NY:18NYCRR": "18 NYCRR part 352 sets public assistance shelter allowances and security-deposit agreements that a landlord renting to an assisted tenant accepts (the 'shelter rules').",
}


def w(p, header, body):
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(header + "\n\n" + body.rstrip() + "\n")


def fname(num):
    return re.sub(r"[^0-9A-Za-z.\-]", "_", str(num)).strip("_") + ".txt"


def rel(p):
    return str(p.relative_to(REG))


def is_repealed(heading, text=""):
    h = heading or ""
    return bool(re.search(r"\[?(Repealed|Reserved|Renumbered)\]?", h, re.I)) or bool(
        re.match(r"^\W*(\[?Repealed|\[?Reserved)", (text or "").split("\n\n", 1)[-1].strip()[:40], re.I))


def add_section(sid, inst, unit, heading, p, source_url=None, repealed=None):
    if p is not None and p.exists():
        t = p.read_text()
        body = t.split("\n\n", 1)[1] if "\n\n" in t else t
        SECTIONS.append({"section_id": sid, "instrument": inst, "unit": unit, "heading": heading, "text_file": rel(p),
                         "chars": len(body), "repealed": is_repealed(heading, body) if repealed is None else repealed})
    else:
        SECTIONS.append({"section_id": sid, "instrument": inst, "unit": unit, "heading": heading, "text_file": None,
                         "chars": 0, "repealed": bool(repealed)})
        GAPS.append({"section_id": sid, "instrument": inst, "unit": unit, "attempted": source_url,
                     "reason": "section listed in the unit's table of contents but its text could not be saved"})


# ------------------------------------------------------------------------------------------------ NY (public.law)
def build_ny():
    for f in sorted((REG / "toc").glob("NY_*.json")):
        toc = json.loads(f.read_text())
        code = toc["code"]
        name, abbr = NY_NAMES[code]
        iid = f"NY:{code}"
        ins, outs = [], []
        arts_in = [x.lower() for x in harvest_ny.ARTICLES_IN.get(code, [])]
        for a in toc["articles"]:
            num = a["number"].lower()
            label = a["label"]
            if num not in arts_in:
                r = scope.NY_OUT.get(code, {}).get(num)
                outs.append({"unit": f"art. {a['number'].upper()}", "heading": label,
                             "reason": r or (scope.REPEALED_OUT if re.search(r"repeal", label, re.I) else scope.DEFAULT_OUT).format(h=label)})
                continue
            groups = []
            if a.get("subunits"):
                for u in a["subunits"]:
                    uname = f"art. {a['number'].upper()} {u['slug'].rsplit('_', 2)[-2]} {u['number'].upper()}"
                    if not u.get("in"):
                        r = scope.NY_OUT.get(code, {}).get(f"{num}/{u['number'].lower()}")
                        if code == "MHY":
                            r = scope.MHY_E_OUT.format(h=u["label"])
                        outs.append({"unit": uname, "heading": u["label"], "reason": r or scope.NY_SUB_OUT_DEFAULT.format(h=u["label"])})
                    else:
                        groups.append((uname, u["label"], u["sections"], u["slug"]))
            else:
                groups.append((f"art. {a['number'].upper()}", label, a.get("sections", []), a["slug"]))
            for uname, ulabel, secs, uslug in groups:
                ins.append({"unit": uname, "heading": ulabel, "toc_url": nylaw.BASE + uslug, "sections": len(secs)})
                for s in secs:
                    snum = s["slug"][len(toc["law_slug"]) + len("_section_"):]
                    p = TEXTS / f"NY_{code}" / fname(snum)
                    heading = re.sub(r"^\S+\s", "", s["label"], count=1) if re.match(r"^[\dA-Z]", s["label"]) else s["label"]
                    add_section(f"NY:{abbr} {snum.upper() if code != 'UCC' else snum.upper()}", iid, uname, heading, p,
                                nylaw.BASE + s["slug"])
        INSTRUMENTS.append({"id": iid, "jurisdiction": "NY", "name": f"New York {name}", "level": "statute",
                            "units_in_scope": ins, "units_out": outs, "toc_source_url": toc["toc_source_url"],
                            "text_source": "newyork.public.law (mirror of nysenate.gov official text)",
                            **({"added_why": ADDED[iid]} if iid in ADDED else {})})


def build_senate(law, arts_in, out_reasons):
    code = law
    name, abbr = NY_NAMES[code]
    iid = f"NY:{'SCPA' if law == 'SCP' else law}"
    page, cap = senate_archive.get(law)
    ins, outs = [], []
    for slug, nm, desc in senate_archive.items(page, law):
        if slug not in arts_in:
            outs.append({"unit": nm.title().replace("Article", "art."), "heading": desc,
                         "reason": out_reasons.get(slug, scope.DEFAULT_OUT.format(h=desc))})
            continue
        rows = senate_archive.tree(law, slug)
        uname = nm.title().replace("Article", "art.")
        ins.append({"unit": uname, "heading": desc, "toc_url": f"https://www.nysenate.gov/legislation/laws/{law}/{slug}",
                    "toc_capture": senate_archive.get(f"{law}/{slug}")[1], "sections": len(rows)})
        for sslug, snm, sdesc in rows:
            snum = snm.split(None, 1)[1] if " " in snm else sslug
            add_section(f"NY:{abbr} {snum}", iid, uname, sdesc, TEXTS / f"NY_{law}" / fname(snum),
                        f"https://www.nysenate.gov/legislation/laws/{law}/{sslug}")
    INSTRUMENTS.append({"id": iid, "jurisdiction": "NYC" if law == "CCA" else "NY", "name": name, "level": "statute",
                        "units_in_scope": ins, "units_out": outs,
                        "toc_source_url": f"https://www.nysenate.gov/legislation/laws/{law}", "toc_capture": cap,
                        "text_source": "Internet Archive captures of nysenate.gov (official); nysenate.gov and public mirrors wall curl and browser"})


# ------------------------------------------------------------------------------------------------ NYC (XML)
def nyc_unit(s):
    return " > ".join(h for _, h in s["path"])


def pick(label, table):
    best = None
    for k, v in table.items():
        if label.startswith(k) and (best is None or len(k) > len(best[0])):
            best = (k, v)
    return best[1] if best else None


def build_nyc(kind):
    secs = aml.parse(kind)
    titles = json.loads((aml.CACHE / f"{kind}_titles_fixed.json").read_text())
    tin = scope.ADC_TITLES_IN if kind == "admin" else scope.RCNY_TITLES_IN
    table_in = scope.ADC_IN if kind == "admin" else scope.RCNY_IN
    table_out = scope.ADC_OUT if kind == "admin" else scope.RCNY_OUT
    iid = "NYC:ADC" if kind == "admin" else "NYC:RCNY"
    ins, outs = [], []
    units = {}
    for s in secs:
        t = re.match(r"Title\s+([\w-]+)", s["title"] or "")
        tn = t.group(1) if t else "?"
        if tn not in tin:
            continue
        units.setdefault((tn, nyc_unit(s)), []).append(s)
    used = {}
    for (tn, ulabel), ss in units.items():
        ul = f"tit. {tn} > {ulabel}"
        is_in = any(ulabel == p or (p.endswith(":") and ulabel.startswith(p)) for p in table_in.get(tn, []))
        if not is_in:
            r = pick(ulabel, table_out.get(tn, {}))
            if not r:
                r = (scope.REPEALED_OUT if re.search(r"\[Repealed\]", ulabel) else scope.DEFAULT_OUT).format(h=ulabel)
            outs.append({"unit": ul, "heading": ulabel, "reason": r, "sections": len(ss)})
            continue
        ins.append({"unit": ul, "heading": ulabel, "sections": len(ss)})
        for s in ss:
            num = s["number"]
            key = (tn, num)
            if key in used:
                num = f"{num}@{s['file'][:-4]}"
            used[key] = 1
            if kind == "admin":
                sid, p = f"NYC:ADC {num}", TEXTS / "NYC_ADC" / fname(num)
                url = f"https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/{s['id']}"
            else:
                sid, p = f"NYC:RCNY {tn} {num}", TEXTS / f"NYC_RCNY_T{tn}" / fname(num)
                url = f"https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCrules/{s['id']}"
            if s["paras"]:
                w(p, f"SOURCE: {url}\nRETRIEVED: {TODAY} from American Legal Publishing official bulk XML ({aml.ZIP[kind]}, "
                     f"downloaded 2026-09-28/29), XML file {s['file']}; text extracted mechanically by register/tools/aml.py",
                  s["heading"] + "\n\n" + "\n\n".join(s["paras"]))
            add_section(sid, iid, ul, re.sub(r"^§+\s*[\w\-\.]+\.?\s*", "", s["heading"]), p if s["paras"] else None, url,
                        repealed=bool(re.search(r"\[(Repealed|Reserved|Renumbered)\]", s["heading"])) or not s["paras"])
    for tn, h in sorted(titles.items(), key=lambda x: (int(re.match(r"\d+", x[0]).group()), x[0])):
        if tn in tin:
            continue
        spec = scope.ADC_TITLE_OUT if kind == "admin" else scope.RCNY_TITLE_OUT
        outs.append({"unit": f"tit. {tn}", "heading": h,
                     "reason": spec.get(tn) or (scope.ADC_OTHER_TITLE_OUT if kind == "admin" else scope.RCNY_OTHER_TITLE_OUT).format(h=h)})
    INSTRUMENTS.append({"id": iid, "jurisdiction": "NYC",
                        "name": "New York City Administrative Code" if kind == "admin" else "Rules of the City of New York",
                        "level": "statute" if kind == "admin" else "rule", "units_in_scope": ins, "units_out": outs,
                        "toc_source_url": f"https://codelibrary.amlegal.com/codes/newyorkcity/latest/{aml.CODE[kind]}/0-0-0-1",
                        "text_source": f"American Legal Publishing official bulk XML {aml.ZIP[kind]}"})


# ------------------------------------------------------------------------------------------------ USC
def build_usc():
    for spec in scope.USC:
        secs = usc.parse(spec["title"])
        iid = spec["id"]
        ins, outs = [], []
        tdir = TEXTS / iid.replace("US:", "US_")
        if spec.get("note_of"):
            import xml.etree.ElementTree as ET
            NS = usc.NS
            text, url = "", "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title12-section5220&num=0&edition=prelim"
            for ev, e in ET.iterparse(usc.SCR / f"usc{spec['title']}.xml", events=("end",)):
                if e.tag == NS + "section" and e.get("identifier") == f"/us/usc/t{spec['title']}/s{spec['note_of']}":
                    for n in e.iter(NS + "note"):
                        h = n.find(NS + "heading")
                        if h is not None and spec["note_heading"] in "".join(h.itertext()):
                            text = "\n".join(t for t in (usc.body_text(c) for c in n) if t)
                    break
            p = tdir / "5220-note.txt"
            if text:
                w(p, f"SOURCE: {url}\nRETRIEVED: {TODAY} from the Office of the Law Revision Counsel USLM XML "
                     f"(uscode.house.gov release point {usc.RELEASE}), statutory note under 12 U.S.C. 5220; text extracted mechanically", text)
            ins.append({"unit": "12 U.S.C. 5220 note", "heading": spec["note_heading"], "sections": 1})
            add_section("US:12 USC 5220 note", iid, "12 U.S.C. 5220 note", spec["note_heading"], p if text else None, url)
            INSTRUMENTS.append({"id": iid, "jurisdiction": "US", "name": spec["name"], "level": "statute",
                                "units_in_scope": ins, "units_out": outs, "toc_source_url": url,
                                "text_source": f"uscode.house.gov USLM XML release point {usc.RELEASE}"})
            continue
        units = {}
        for s in secs:
            path = s["path"]
            idx = next((i for i, x in enumerate(path) if spec["filter"] in x), None)
            if idx is None:
                continue
            rest = path[idx + 1: idx + 1 + spec["depth"]]
            label = " > ".join(rest) if rest else f"(sections directly under {path[idx][:60]})"
            if spec["depth"] == 0:
                label = f"section {s['number']}" if s["number"] in spec["sections"] else "*"
            units.setdefault(label, []).append(s)
        for label, ss in units.items():
            is_in = any(i in label for i in spec["in"]) or (label.startswith("(") and any(i.startswith("(") for i in spec["in"]))
            if not is_in:
                r = spec["out"].get("*") if label == "*" else next((v for k, v in spec["out"].items() if k in label), None)
                if not r:
                    r = (scope.REPEALED_OUT if re.search(r"Repealed|Reserved|Omitted", label, re.I) else scope.DEFAULT_OUT).format(h=label)
                outs.append({"unit": label if label != "*" else f"other sections under {spec['filter']}", "heading": label,
                             "reason": r, "sections": len(ss)})
                continue
            ins.append({"unit": label, "heading": label, "sections": len(ss)})
            for s in ss:
                num = re.sub(r"[\[\]\s]", "", s["number"])
                if spec["id"] == "US:FRBP":
                    sid = f"US:FRBP {num}"
                    url = f"https://uscode.house.gov/view.xhtml?path=/prelim@title11/title11a&edition=prelim"
                else:
                    sid = f"US:{spec['title']} USC {num}"
                    url = f"https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title{spec['title']}-section{num}&num=0&edition=prelim"
                p = tdir / fname(num)
                if s["text"]:
                    w(p, f"SOURCE: {url}\nRETRIEVED: {TODAY} from the Office of the Law Revision Counsel USLM XML (uscode.house.gov "
                         f"release point {usc.RELEASE}, xml_usc{spec['title']}@{usc.RELEASE}.zip), element {s['identifier']}; text "
                         f"extracted mechanically (editorial notes omitted; source credit appended)",
                      f"{s['number']}. {s['heading']}\n\n{s['text']}\n\nSOURCE CREDIT: {s.get('source_credit', '')}")
                add_section(sid, iid, label, s["heading"], p if s["text"] else None, url,
                            repealed=(s.get("status") in ("repealed", "transferred", "omitted")) or bool(re.search(r"^\s*(Repealed|Omitted|Transferred)", s["heading"] or "")))
        INSTRUMENTS.append({"id": iid, "jurisdiction": "US", "name": spec["name"], "level": spec.get("level", "statute"),
                            "units_in_scope": ins, "units_out": outs,
                            "toc_source_url": f"https://uscode.house.gov/download/releasepoints/us/pl/119/111/xml_usc{spec['title']}@{usc.RELEASE}.zip",
                            "text_source": f"uscode.house.gov USLM XML release point {usc.RELEASE}"})


# ------------------------------------------------------------------------------------------------ eCFR
def build_ecfr():
    for spec in scope.ECFR:
        iid = spec["id"]
        tdir = TEXTS / iid.replace("US:", "US_")
        ins, outs = [], []
        if spec.get("sections"):
            secs, urls = [], {}
            for sec in spec["sections"]:
                ss, url, d = ecfr.parse_part(spec["title"], spec["part"], section=sec)
                for s in ss:
                    s["path"] = ["selected sections"]
                    urls[s["number"]] = url
                secs.extend(ss)
            date = ecfr.latest(spec["title"])
        else:
            secs, url, date = ecfr.parse_part(spec["title"], spec["part"])
            urls = {}
        units = {}
        for s in secs:
            if s["path"]:
                label = s["path"][0].split(":")[0] if s["path"][0].startswith("SUBPART") else s["path"][0]
                heading = s["path"][0]
            else:
                label, heading = "(appendices)", "Appendices and supplements to the part"
            units.setdefault(label, [heading, []])[1].append(s)
        for label, (heading, ss) in units.items():
            is_in = spec["in"] == ["*"] or label in spec["in"] or label.split(" ")[0:2] and label in spec["in"]
            if not is_in:
                r = spec["out"].get(label) or spec["out"].get("*") or scope.DEFAULT_OUT.format(h=heading)
                outs.append({"unit": label, "heading": heading, "reason": r, "sections": len(ss)})
                continue
            ins.append({"unit": label, "heading": heading, "sections": len(ss)})
            for s in ss:
                num = s["number"]
                u = urls.get(num) or f"https://www.ecfr.gov/api/versioner/v1/full/{date}/title-{spec['title']}.xml?part={spec['part']}"
                p = tdir / fname(num)
                if s["text"]:
                    w(p, f"SOURCE: https://www.ecfr.gov/current/title-{spec['title']}/part-{spec['part']}#{'p-' if s['type'] == 'SECTION' else ''}{num}\n"
                         f"API: {u}\nRETRIEVED: {TODAY} from the eCFR versioner API (up to date as of {date}); text extracted "
                         f"mechanically by register/tools/ecfr.py", s["text"])
                add_section(f"US:{spec['title']} CFR {num.replace(' ', '_')}", iid, label, re.sub(r"^§\s*[\d.A-Za-z-]+\s*", "", s["heading"]),
                            p if s["text"] else None, u, repealed=bool(re.search(r"\[Reserved\]|Removed", s["heading"])))
        INSTRUMENTS.append({"id": iid, "jurisdiction": "US", "name": spec["name"], "level": "regulation",
                            "units_in_scope": ins, "units_out": outs,
                            "toc_source_url": f"https://www.ecfr.gov/current/title-{spec['title']}/part-{spec['part']}",
                            "text_source": f"eCFR versioner API, up to date as of {date}",
                            **({"added_why": ADDED[iid]} if iid in ADDED else {})})
    for iid, t, part, name, reason in scope.ECFR_EXCLUDED:
        secs, url, date = ecfr.parse_part(t, part)
        units = {}
        for s in secs:
            units.setdefault(s["path"][0] if s["path"] else "(appendices)", 0)
            units[s["path"][0] if s["path"] else "(appendices)"] += 1
        INSTRUMENTS.append({"id": iid, "jurisdiction": "US", "name": f"{t} CFR part {part} ({name})", "level": "regulation",
                            "units_in_scope": [],
                            "units_out": [{"unit": u.split(":")[0], "heading": u, "reason": reason, "sections": n} for u, n in units.items()]
                            or [{"unit": f"part {part}", "heading": name, "reason": reason}],
                            "toc_source_url": f"https://www.ecfr.gov/current/title-{t}/part-{part}",
                            "note": "Named in the rule files (stated atoms for a parked or out-of-aperture regime); every unit is out of aperture."})


# ------------------------------------------------------------------------------------------------ NYCRR
def build_nycrr():
    toc = json.loads((REG / "toc" / "NYCRR.json").read_text())
    for code, spec in scope.NYCRR.items():
        iid = f"NY:{code}"
        ins, outs, seen = [], [], set()
        for part, d in toc.items():
            if d["code"] != code:
                continue
            pk = part.rsplit("/", 1)[1]
            ins.append({"unit": pk.replace("part-", "Part "), "heading": d["title"], "toc_url": "https://www.law.cornell.edu" + part,
                        "sections": len({h for h, _ in d["sections"]})})
            seen.add(pk)
            seen_secs = set()
            for h, label in d["sections"]:
                if h in seen_secs:
                    continue
                seen_secs.add(h)
                num = h.split("NYCRR-", 1)[1]
                heading = re.sub(r"^§\s*[\d.\-A-Za-z]+\s*-\s*", "", label)
                add_section(f"NY:{code[:-5]} NYCRR {num}", iid, pk.replace("part-", "Part "), heading,
                            TEXTS / f"NY_{code}" / fname(num), "https://www.law.cornell.edu" + h,
                            repealed=bool(re.search(r"Repealed|Reserved", label)))
        for part, d in toc.items():
            if d["code"] != code:
                continue
            for h, label in d["siblings"]:
                pk = h.rsplit("/", 1)[1]
                if pk in seen or not pk.startswith(("part-", "subpart-")):
                    continue
                seen.add(pk)
                r = spec["out"].get(pk) or (scope.REPEALED_OUT if re.search(r"Repealed|Reserved", label) else scope.DEFAULT_OUT).format(h=label)
                if code == "9NYCRR" and re.match(r"part-25(0\d|10)$", pk):
                    r = scope.OUTSIDE_NYC + " (ETPA Tenant Protection Regulations; ETPA units in NYC are under the RSC)"
                outs.append({"unit": pk.replace("part-", "Part "), "heading": label, "reason": r})
        if code == "9NYCRR":
            outs.append({"unit": "Parts 2100-2111", "heading": "State Rent and Eviction Regulations (rent control outside NYC)", "reason": scope.OUTSIDE_NYC})
            outs.append({"unit": "Parts 2500-2510", "heading": "Tenant Protection Regulations (ETPA outside NYC)", "reason": scope.OUTSIDE_NYC})
        outs.append({"unit": "other chapters and subtitles of the title", "heading": f"{code[:-5]} NYCRR outside the parent units listed",
                     "reason": "Agency regulations whose subject matter is outside the settlement chain; the parent chapter or subchapter of each in-scope part is enumerated part by part above."})
        INSTRUMENTS.append({"id": iid, "jurisdiction": "NY", "name": spec["name"],
                            "level": "court rule" if code == "22NYCRR" else "regulation", "units_in_scope": ins, "units_out": outs,
                            "toc_source_url": f"https://www.law.cornell.edu/regulations/new-york/title-{code[:-5]}",
                            "text_source": "Cornell LII republication of the official NYCRR",
                            **({"added_why": ADDED[iid]} if iid in ADDED else {})})


def fix_titles():
    import glob
    import xml.etree.ElementTree as ET
    for kind in ("admin", "rules"):
        f = aml.CACHE / f"{kind}_titles_fixed.json"
        if f.exists():
            continue
        heads = {}
        for x in glob.glob(str(aml.DIRS[kind] / "*.xml")):
            try:
                root = ET.parse(x).getroot()
            except ET.ParseError:
                continue
            top = [lv for lv in root if lv.tag == "LEVEL"]
            if top and top[0].get("style-name") == "Title":
                h = aml.heading(top[0])
                m = re.match(r"Title\s+([\w-]+)", h)
                if m:
                    heads[m.group(1)] = h
        f.write_text(json.dumps(heads))


if __name__ == "__main__":
    fix_titles()
    build_ny()
    build_senate("CCA", scope.CCA_IN, scope.CCA_OUT)
    build_senate("SCP", scope.SCP_IN, scope.SCP_OUT)
    build_nycrr()
    build_nyc("admin")
    build_nyc("rules")
    build_usc()
    build_ecfr()
    ids = [s["section_id"] for s in SECTIONS]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        print("DUPLICATE section ids:", sorted(dup)[:20])
    (REG / "sections.jsonl").write_text("".join(json.dumps(s) + "\n" for s in SECTIONS))
    (REG / ".work").mkdir(exist_ok=True)
    (REG / ".work" / "instruments_core.json").write_text(json.dumps(INSTRUMENTS, indent=1))
    (REG / ".work" / "fetch_gaps_sections.json").write_text(json.dumps(GAPS, indent=1))
    from collections import Counter
    c = Counter(s["instrument"] for s in SECTIONS)
    print(len(INSTRUMENTS), "instruments;", len(SECTIONS), "sections;", len(GAPS), "without text")
    for k, v in c.items():
        print(f"  {k}: {v}")
