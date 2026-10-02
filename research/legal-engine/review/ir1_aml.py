"""Independent review 1: extract NYC Admin Code sections from American Legal bulk XML, mechanically.

Usage: python3 review/ir1_aml.py XMLDIR SEC [SEC ...]
Writes sources/REVIEW1_NYC_ADC_<SEC>.txt. Reuses build/aml2txt.py's parser.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "build"))
import aml2txt  # noqa: E402

xmldir = pathlib.Path(sys.argv[1])
aml2txt.ROOT = xmldir
secs = aml2txt.sections("admin")
SRC = pathlib.Path(__file__).resolve().parent.parent / "sources"
for s in sys.argv[2:]:
    v = secs[s]
    url = f"https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/{v['id']}"
    body = "\n\n".join(v["paras"])
    p = SRC / f"REVIEW1_NYC_ADC_{s}.txt"
    p.write_text(f"SOURCE: {url}\nRETRIEVED: 2026-09-28 by independent reviewer 1 from American Legal Publishing official bulk XML "
                 f"(http://files.amlegal.com/pdffiles/NewYorkCity/Admin/XML.zip), text extracted mechanically from XML file "
                 f"{pathlib.Path(v['file']).name}\n\n{v['heading']}\n\n{body}\n")
    print(p.name, len(body))
