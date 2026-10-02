"""United States Code from the Office of the Law Revision Counsel's official USLM XML (uscode.house.gov, release
point Public Law 119-111). Hierarchy and headings are read from the XML; a section's text is the text of its
<section> element minus <notes> (editorial and statutory notes) and minus <sourceCredit>, which are kept apart.

CLI:
  python3 tools/usc.py units TITLE [PATHPREFIX]    list chapters/subchapters/parts with section ranges
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

SCR = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/reg/usc"
NS = "{http://xml.house.gov/schemas/uslm/1.0}"
RELEASE = "119-111"
LEVELS = ("title", "subtitle", "chapter", "subchapter", "part", "subpart", "division", "subdivision", "article")


def tag(e):
    return e.tag.replace(NS, "")


def txt(e):
    return re.sub(r"\s+", " ", "".join(e.itertext())).strip() if e is not None else ""


def body_text(sec, include_notes=False):
    """Section text without notes/sourceCredit, with a line break per structural block."""
    out = []

    def rec(e):
        t = tag(e)
        if not include_notes and t in ("notes", "note", "sourceCredit"):
            return
        block = t in ("subsection", "paragraph", "subparagraph", "clause", "subclause", "item", "subitem",
                      "chapeau", "continuation", "content", "p", "heading", "num", "table", "tr", "quotedContent",
                      "note", "sourceCredit")
        if block and t not in ("num",):
            out.append("\n")
        if e.text:
            out.append(e.text)
        for c in e:
            rec(c)
            if c.tail:
                out.append(c.tail)
        if t == "num":
            out.append(" ")
    rec(sec)
    s = "".join(out)
    s = re.sub(r"[ \t\r ]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{2,}", "\n", s)
    return s.strip()


def parse(title):
    cache = SCR / f"usc{title}_sections.json"
    if cache.exists():
        return json.loads(cache.read_text())
    secs = parse_xml((SCR / f"usc{title}.xml").read_bytes())
    cache.write_text(json.dumps(secs))
    return secs


def parse_xml(xml, include_notes=False):
    """Parse supplied USLM without reading or writing the legacy scratch cache."""
    root = ET.fromstring(xml)
    secs = []

    def walk(e, path, ancestors):
        for c in e:
            t = tag(c)
            if t in ("section", "courtRule") and c.get("identifier"):
                num = txt(c.find(NS + "num")).replace("§", "").replace("Rule", "").strip().rstrip(".")
                notes = [txt(n) for n in c.iter(NS + "sourceCredit")]
                secs.append({"identifier": c.get("identifier"), "number": num, "heading": txt(c.find(NS + "heading")),
                             "path": list(path), "status": c.get("status"), "text": body_text(c, include_notes),
                             "ancestors": list(ancestors),
                             "source_credit": notes[0] if notes else ""})
            elif t in LEVELS or t in ("rule",):
                if t == "rule" and c.get("identifier"):
                    num = txt(c.find(NS + "num"))
                    secs.append({"identifier": c.get("identifier"), "number": num, "heading": txt(c.find(NS + "heading")),
                                 "path": list(path), "ancestors": list(ancestors), "status": c.get("status"),
                                 "text": body_text(c, include_notes), "source_credit": ""})
                    continue
                label = f"{t} {txt(c.find(NS + 'num'))} {txt(c.find(NS + 'heading'))}".strip()
                walk(c, path + [label], ancestors + ([c.get("identifier")] if c.get("identifier") else []))
            elif t in ("main", "appendix", "courtRules", "reorganizationPlans", "level"):
                label = ""
                if t in ("courtRules", "level", "appendix"):
                    label = f"{t} {txt(c.find(NS + 'num'))} {txt(c.find(NS + 'heading'))}".strip()
                walk(c, path + ([label] if label else []), ancestors + ([c.get("identifier")] if c.get("identifier") else []))
    walk(root, [], [])
    return secs


if __name__ == "__main__":
    if sys.argv[1] == "units":
        secs = parse(sys.argv[2])
        pre = sys.argv[3] if len(sys.argv) > 3 else ""
        from collections import OrderedDict
        u = OrderedDict()
        depth = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        for s in secs:
            k = " > ".join(s["path"][:depth])
            if pre and pre not in k:
                continue
            u.setdefault(k, []).append(s["number"])
        for k, v in u.items():
            print(f"{len(v):4d}  {k}  [{v[0]} .. {v[-1]}]")
