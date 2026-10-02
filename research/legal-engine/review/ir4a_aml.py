"""Independent review 4A: extract NYC Admin Code / RCNY sections from American Legal bulk XML, mechanically.

Usage: python3 review/ir4a_aml.py admin|rules SEC [SEC ...]
Writes sources/REVIEW4A_NYC_ADC_<SEC>.txt (or REVIEW4A_NYC_RCNY_<SEC>.txt). Reuses build/aml2txt.py's parser.
XML: American Legal official bulk XML downloaded 2026-09-28 to the profile scratch folder.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "build"))
import aml2txt  # noqa: E402

aml2txt.ROOT = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/amlxml"
kind = sys.argv[1]
secs = aml2txt.sections(kind)
SRC = pathlib.Path(__file__).resolve().parent.parent / "sources"
doc = "NYCadmin" if kind == "admin" else "NYCrules"
tag = "ADC" if kind == "admin" else "RCNY"
for s in sys.argv[2:]:
    v = secs[s]
    url = f"https://codelibrary.amlegal.com/codes/newyorkcity/latest/{doc}/{v['id']}"
    body = "\n\n".join(v["paras"])
    safe = s.replace(":", "_").replace("@", "_")
    p = SRC / f"REVIEW4A_NYC_{tag}_{safe}.txt"
    if p.exists():
        print("exists", p.name)
        continue
    zipurl = "http://files.amlegal.com/pdffiles/NewYorkCity/Admin/XML.zip" if kind == "admin" else "http://files.amlegal.com/pdffiles/NewYorkCity/Rules/XML.zip"
    p.write_text(f"SOURCE: {url}\nRETRIEVED: 2026-09-29 by independent reviewer 4A from American Legal Publishing official bulk XML "
                 f"({zipurl}, downloaded 2026-09-28), text extracted mechanically from XML file {pathlib.Path(v['file']).name}\n\n"
                 f"{v['heading']}\n\n{body}\n")
    print(p.name, len(body))
