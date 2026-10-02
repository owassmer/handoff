"""Harvest the unit tree of each NY statute in the register from newyork.public.law: every article (with heading),
and for articles listed in ARTICLES_IN, their titles/parts and every section (slug, number, heading).

Writes register/toc/NY_<CODE>.json. Resumable (raw pages cached by nylaw.get).
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nylaw  # noqa: E402

REG = pathlib.Path(__file__).resolve().parent.parent
TOC = REG / "toc"
TOC.mkdir(exist_ok=True)

LAWS = {
    "GOL": "n.y._general_obligations_law",
    "RPL": "n.y._real_property_law",
    "RPAPL": "n.y._real_property_actions_&_proceedings_law",
    "MDL": "n.y._multiple_dwelling_law",
    "CPLR": "n.y._civil_practice_law_&_rules",
    "GBL": "n.y._general_business_law",
    "JUD": "n.y._judiciary_law",
    "UCC": "n.y._uniform_commercial_code_law",
    "ABP": "n.y._abandoned_property_law",
    "EPTL": "n.y._estates,_powers_&_trusts_law",
    "MIL": "n.y._military_law",
    "EXEC": "n.y._executive_law",
    "LLC": "n.y._limited_liability_company_law",
    "BCL": "n.y._business_corporation_law",
    "NPCL": "n.y._not-for-profit_corporation_law",
    "GCN": "n.y._general_construction_law",
    "STT": "n.y._state_technology_law",
    "SSL": "n.y._social_services_law",
    "DCL": "n.y._debtor_&_creditor_law",
    "PTR": "n.y._partnership_law",
    "MHY": "n.y._mental_hygiene_law",
}

# Articles taken to section-level classification (generous: any heading not plainly outside the chain).
ARTICLES_IN = {
    "GOL": ["1", "3", "5", "7", "11", "13", "15", "17"],
    "RPL": ["1", "6-a", "7", "8", "12-a"],
    "RPAPL": ["1", "2", "6", "7", "7-a", "7-c", "7-d", "8", "13"],
    "MDL": ["1", "2", "3", "7-d", "8", "9"],
    "CPLR": ["1", "2", "3", "5", "10", "12", "15", "20", "21", "22", "30", "32", "45", "50", "51", "52", "60", "62",
             "64", "80", "81", "82", "83", "84", "85"],
    "GBL": ["9-b", "22-a", "25", "26", "29-h", "29-hh", "29-hhh", "39-f"],
    "JUD": ["15"],
    "UCC": ["1", "3"],
    "ABP": ["1", "13", "14"],
    "EPTL": ["1", "4", "11", "12", "13"],
    "MIL": ["13"],
    "EXEC": ["15"],
    "LLC": ["2", "8"],
    "BCL": ["13"],
    "NPCL": ["13"],
    "GCN": ["1", "2", "2-a", "4", "5", "7"],
    "STT": ["3"],
    "SSL": ["5"],
    "DCL": ["6", "6-a", "9", "10-a"],
    "PTR": ["8-a", "8-b"],
    "MHY": ["e"],
}

# Where an in-scope article is divided into titles/parts, only these subunits go to section level (others are
# recorded with their heading and excluded with a reason in build_instruments.py). Absent key = every subunit.
SUBUNITS_IN = {
    ("GOL", "5"): ["1", "3", "5", "6", "7", "9", "11", "13", "15"],
    ("GOL", "7"): ["1"],
    ("SSL", "5"): ["1"],
    ("EPTL", "13"): ["1", "3"],
    ("MHY", "e"): ["81"],
}


def art_no(slug, law_slug):
    rest = slug[len(law_slug) + 1:]
    m = re.match(r"(article|title|part|chapter)_(.+)$", rest)
    return m.group(2) if m else rest


def subunits(slug):
    page = nylaw.get(slug)
    return [(h, l) for h, l in nylaw.links(page) if h.startswith(slug + "_") and "_section_" not in h
            and h[len(slug) + 1:].count("_") == 1]


def harvest(code):
    law = LAWS[code]
    out = {"code": code, "law_slug": law, "toc_source_url": nylaw.BASE + law, "articles": []}
    for slug, label in nylaw.law_units(law):
        a = {"slug": slug, "number": art_no(slug, law), "label": label}
        if a["number"].lower() in [x.lower() for x in ARTICLES_IN.get(code, [])]:
            subs = subunits(slug)
            a["subunits"] = []
            if subs:
                keep = SUBUNITS_IN.get((code, a["number"].lower()))
                for s, l in subs:
                    sn = s[len(slug) + 1:].split("_", 1)[1]
                    if keep is not None and sn.lower() not in keep:
                        a["subunits"].append({"slug": s, "number": sn, "label": l, "in": False})
                        continue
                    secs = nylaw.tree(s)
                    a["subunits"].append({"slug": s, "number": sn, "label": l, "in": True, "sections": [
                        {"slug": x, "label": y, "path": list(p)} for x, y, p in secs]})
            else:
                secs = nylaw.tree(slug)
                a["sections"] = [{"slug": x, "label": y, "path": list(p)} for x, y, p in secs]
        out["articles"].append(a)
    (TOC / f"NY_{code}.json").write_text(json.dumps(out, indent=1))
    n = sum(len(a.get("sections", [])) + sum(len(s.get("sections", [])) for s in a.get("subunits", [])) for a in out["articles"])
    print(code, len(out["articles"]), "articles;", n, "sections in scoped articles")


if __name__ == "__main__":
    for c in (sys.argv[1:] or LAWS):
        harvest(c)
