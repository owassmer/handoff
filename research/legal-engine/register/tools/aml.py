"""NYC Administrative Code and Rules of the City of New York from American Legal Publishing's official bulk XML.

Source zips: http://files.amlegal.com/pdffiles/NewYorkCity/Admin/XML.zip and .../Rules/XML.zip (downloaded
2026-09-28/-09-29 by earlier review rounds; extracted under the profile scratch folder). Everything is read
mechanically from the XML: the LEVEL hierarchy (Title > Chapter > Subchapter > Article > Section) gives units and
headings; a section's text is every PARA inside its Section LEVEL, in document order. RECORD@number is American
Legal's global document order, used to place each RCNY chapter file under the Title file that precedes it.

CLI:  python3 tools/aml.py admin|rules --units TITLE      list chapter/subchapter/article units with section counts
"""
import glob
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

SCR = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch"
DIRS = {"admin": SCR / "amlxml/admin/XML", "rules": SCR / "reg/aml/rules/XML"}
ZIP = {"admin": "http://files.amlegal.com/pdffiles/NewYorkCity/Admin/XML.zip",
       "rules": "http://files.amlegal.com/pdffiles/NewYorkCity/Rules/XML.zip"}
CODE = {"admin": "NYCadmin", "rules": "NYCrules"}
CACHE = SCR / "reg/aml"
STRUCT = ("Title", "Chapter", "Subchapter", "Article", "Subarticle", "Part", "Subtitle", "Subpart")


def ptext(p):
    parts = []

    def rec(e):
        if e.tag in ("TAB",):
            parts.append(" ")
        if e.tag == "LINEBRK":
            parts.append("\n")
        if e.text:
            parts.append(e.text)
        for c in e:
            rec(c)
            if c.tail:
                parts.append(c.tail)
    rec(p)
    t = "".join(parts)
    t = re.sub(r"[ \t\r ]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return t.strip()


def heading(level):
    rec = level.find("RECORD")
    h = rec.find("HEADING") if rec is not None else None
    return re.sub(r"\s+", " ", "".join(h.itertext())).strip() if h is not None else ""


def first_number(root):
    for r in root.iter("RECORD"):
        n = r.get("number")
        if n and n.isdigit():
            return int(n)
    return 0


def section_paras(level):
    """PARA text inside a Section LEVEL (its own RECORD and its non-Section descendant levels)."""
    out = []

    def rec(e):
        for c in e:
            if c.tag == "LEVEL" and c.get("style-name") == "Section":
                continue
            if c.tag == "PARA":
                t = ptext(c)
                if t:
                    out.append(t)
            elif c.tag in ("RECORD", "LEVEL", "TABLE", "ROW", "CELL", "TBODY", "THEAD", "TR", "TD"):
                rec(c)
            else:
                rec(c)
    rec(level)
    return out


def parse(kind):
    cache = CACHE / f"{kind}_sections.json"
    if cache.exists():
        return json.loads(cache.read_text())
    files = []
    for f in glob.glob(str(DIRS[kind] / "*.xml")):
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError:
            continue
        files.append((first_number(root), f, root))
    files.sort()
    secs = []
    title = None
    for num, f, root in files:
        top = [lv for lv in root if lv.tag == "LEVEL"]
        if top and top[0].get("style-name") == "Title":
            h = heading(top[0])
            if re.match(r"Title\s+\w+", h):
                title = h
            if kind == "admin":
                pass

        def walk(e, path):
            for c in e:
                if c.tag != "LEVEL":
                    continue
                style = c.get("style-name")
                if style == "Section":
                    h = heading(c)
                    m = re.match(r"§+\s*([\w\-\.]+?)\.?\s", h + " ")
                    rec = c.find("RECORD")
                    secs.append({"number": m.group(1) if m else h, "heading": h, "path": list(path),
                                 "title": title, "id": rec.get("id") if rec is not None else None,
                                 "file": pathlib.Path(f).name, "order": int(rec.get("number")) if rec is not None and (rec.get("number") or "").isdigit() else 0,
                                 "paras": section_paras(c)})
                    continue
                h = heading(c)
                if style in STRUCT and h and style != "Title":
                    walk(c, path + [(style, h)])
                else:
                    walk(c, path)
        walk(root, [])
    if kind == "admin":
        for s in secs:  # Admin Code titles are fixed by the section number prefix (e.g. 26-504 -> Title 26)
            m = re.match(r"(\d+)-", s["number"])
            s["title"] = f"Title {m.group(1)}" if m else s["title"]
    cache.write_text(json.dumps(secs))
    return secs


def unit_key(s, depth):
    """Unit label list: title + first `depth` structural headings."""
    return [s["title"] or "?"] + [h for _, h in s["path"][:depth]]


if __name__ == "__main__":
    kind = sys.argv[1]
    secs = parse(kind)
    if sys.argv[2] == "--units":
        want = sys.argv[3]
        from collections import OrderedDict
        u = OrderedDict()
        for s in secs:
            t = (s["title"] or "?")
            if not re.match(rf"Title {re.escape(want)}\b", t):
                continue
            key = " > ".join([t] + [f"{st}: {h}" for st, h in s["path"]])
            u.setdefault(key, []).append(s["number"])
        for k, v in u.items():
            print(f"{len(v):4d}  {k}   [{v[0]} .. {v[-1]}]")
