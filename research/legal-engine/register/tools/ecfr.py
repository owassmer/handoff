"""Code of Federal Regulations from the eCFR versioner API (ecfr.gov, official editorial compilation).

Whole-part XML: https://www.ecfr.gov/api/versioner/v1/full/<date>/title-<t>.xml?part=<p>[&section=<s>]
Structure:      https://www.ecfr.gov/api/versioner/v1/structure/<date>/title-<t>.json
Hierarchy (subpart DIV6, subject group DIV7, section DIV8, appendix DIV9) and headings are read from the XML; a
section's text is the text of its DIV8/DIV9 element (headings, paragraphs, notes such as source/authority kept).

CLI: python3 tools/ecfr.py units TITLE PART      list subparts with sections
"""
import html
import json
import pathlib
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

SCR = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/reg/ecfr"
DATES = {}


def curl(url, t=180):
    r = subprocess.run(["curl", "-s", "--compressed", "--max-time", str(t), "-A", "Mozilla/5.0", url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def latest(title):
    SCR.mkdir(parents=True, exist_ok=True)
    if title not in DATES:
        f = SCR / "titles.json"
        if not f.exists():
            f.write_text(curl("https://www.ecfr.gov/api/versioner/v1/titles.json"))
        for t in json.loads(f.read_text())["titles"]:
            DATES[str(t["number"])] = t["up_to_date_as_of"]
    return DATES[str(title)]


def part_xml(title, part, section=None, subpart=None):
    d = latest(title)
    key = f"t{title}_p{part}" + (f"_s{section}" if section else "") + (f"_sp{subpart}" if subpart else "")
    f = SCR / f"{key}_{d}.xml"
    url = f"https://www.ecfr.gov/api/versioner/v1/full/{d}/title-{title}.xml?part={part}" + \
        (f"&section={section}" if section else "") + (f"&subpart={subpart}" if subpart else "")
    if not f.exists() or f.stat().st_size < 300:
        for attempt in range(3):
            x = curl(url)
            if x.startswith("<?xml") or x.startswith("<DIV"):
                f.write_text(x)
                break
            time.sleep(3 + 3 * attempt)
        time.sleep(0.5)
    return f.read_text() if f.exists() else "", url, d


def etext(e):
    out = []

    def rec(x):
        if x.tag in ("P", "FP", "HEAD", "HD", "PSPACE", "NOTE", "EXTRACT", "GPOTABLE", "ROW", "CITA", "SECAUTH",
                     "AUTH", "SOURCE", "EDNOTE", "FTNT"):
            out.append("\n")
        if x.text:
            out.append(x.text)
        for c in x:
            rec(c)
            if c.tail:
                out.append(c.tail)
        if x.tag in ("ENT",):
            out.append(" | ")
    rec(e)
    s = html.unescape("".join(out))
    s = re.sub(r"[ \t\r ]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    return re.sub(r"\n{2,}", "\n", s).strip()


def parse_part(title, part, section=None, subpart=None):
    x, url, d = part_xml(title, part, section, subpart)
    if not x:
        return [], url, d
    return parse_xml(x), url, d


def parse_xml(xml, include_root=False):
    """Parse supplied eCFR XML without fetching or writing the legacy scratch cache."""
    root = ET.fromstring(xml)
    secs = []

    def head(e):
        h = e.find("HEAD")
        return re.sub(r"\s+", " ", "".join(h.itertext())).strip() if h is not None else ""

    def walk(e, path):
        for c in e:
            if not c.tag.startswith("DIV"):
                continue
            typ = c.get("TYPE")
            if typ in ("SECTION", "APPENDIX"):
                secs.append({"number": c.get("N"), "type": typ, "heading": head(c), "path": list(path), "text": etext(c)})
            else:
                walk(c, path + [f"{typ} {c.get('N')}: {head(c)}"])
    if root.tag.startswith("DIV") and root.get("TYPE") in ("SECTION", "APPENDIX"):
        secs.append({"number": root.get("N"), "type": root.get("TYPE"), "heading": head(root), "path": [], "text": etext(root)})
    else:
        root_path = [f"{root.get('TYPE')} {root.get('N')}: {head(root)}"] if include_root and root.tag.startswith("DIV") else []
        walk(root, root_path)
    return secs


def structure(title):
    d = latest(title)
    f = SCR / f"struct_t{title}_{d}.json"
    if not f.exists():
        f.write_text(curl(f"https://www.ecfr.gov/api/versioner/v1/structure/{d}/title-{title}.json", 300))
    return json.loads(f.read_text()), d


def find_node(node, typ, ident):
    if node.get("type") == typ and node.get("identifier") == ident:
        return node
    for c in node.get("children") or []:
        r = find_node(c, typ, ident)
        if r:
            return r
    return None


def parent_of(node, typ, ident, parent=None):
    if node.get("type") == typ and node.get("identifier") == ident:
        return parent
    for c in node.get("children") or []:
        r = parent_of(c, typ, ident, node)
        if r:
            return r
    return None


if __name__ == "__main__":
    if sys.argv[1] == "units":
        secs, url, d = parse_part(sys.argv[2], sys.argv[3])
        from collections import OrderedDict
        u = OrderedDict()
        for s in secs:
            u.setdefault(" > ".join(s["path"]), []).append(s["number"])
        print(url)
        for k, v in u.items():
            print(f"{len(v):4d}  {k}  [{v[0]} .. {v[-1]}]")
