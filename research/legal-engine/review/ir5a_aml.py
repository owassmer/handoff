"""Independent review 5A: extract NYC Admin Code / RCNY sections from American Legal official bulk XML, mechanically.

Uses the parsed-section pickles built from http://files.amlegal.com/pdffiles/NewYorkCity/{Admin,Rules}/XML.zip
(profile scratch: ir4a_admin.pkl, ir4a_rules.pkl; dict key -> {heading, id, file, paras}).
Usage: python3 review/ir5a_aml.py admin|rules KEY [KEY ...]   (KEY exactly as in the pickle, e.g. 26-3004 or 'T?:6-89')
Writes sources/REVIEW5A_NYC_ADC_<sec>.txt or REVIEW5A_NYC_RCNY_<sec>_<xmlfile>.txt. Never overwrites.
"""
import pathlib
import pickle
import re
import sys

SCR = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch"
SRC = pathlib.Path(__file__).resolve().parent.parent / "sources"
kind = sys.argv[1]
d = pickle.load(open(SCR / ("ir4a_admin.pkl" if kind == "admin" else "ir4a_rules.pkl"), "rb"))
zipurl = "http://files.amlegal.com/pdffiles/NewYorkCity/" + ("Admin" if kind == "admin" else "Rules") + "/XML.zip"
for k in sys.argv[2:]:
    v = d[k]
    f = pathlib.Path(v["file"]).name
    sec = re.sub(r"[^0-9A-Za-z.\-]", "_", k.split(":")[-1].split("@")[0])
    name = f"REVIEW5A_NYC_ADC_{sec}.txt" if kind == "admin" else f"REVIEW5A_NYC_RCNY_{sec}_{f[:-4]}.txt"
    p = SRC / name
    if p.exists():
        print("exists", name)
        continue
    code = "NYCadmin" if kind == "admin" else "NYCrules"
    url = f"https://codelibrary.amlegal.com/codes/newyorkcity/latest/{code}/{v['id']}"
    body = "\n\n".join(v["paras"])
    p.write_text(f"SOURCE: {url}\nRETRIEVED: 2026-09-30 by independent reviewer 5A from American Legal Publishing official bulk XML "
                 f"({zipurl}), text extracted mechanically from XML file {f}\n\n{v['heading']}\n\n{body}\n")
    print("saved", name, len(body))
