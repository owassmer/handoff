"""Save every section of the in-scope NYCRR parts (Cornell LII) under register/texts/NY_<T>NYCRR/<section>.txt and
write register/toc/NYCRR.json (per part: sections; per parent TOC page: sibling units for units_out).
Stops after --budget seconds; rerun until complete. Never overwrites a saved file."""
import datetime
import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nycrr  # noqa: E402

REG = pathlib.Path(__file__).resolve().parent.parent
P = "/regulations/new-york/"
PARTS = {  # instrument code -> part TOC paths
    "9NYCRR": [P + "title-9/subtitle-J/part-466",
               P + "title-9/subtitle-S/chapter-VIII/subchapter-B/part-2520",
               P + "title-9/subtitle-S/chapter-VII/subchapter-D/part-2200",
               P + "title-9/subtitle-N/part-540"],
    "19NYCRR": [P + "title-19/chapter-V/subchapter-D/part-175"],
    "22NYCRR": [P + "title-22/subtitle-A/chapter-II/part-208", P + "title-22/subtitle-A/chapter-II/part-202"],
    "23NYCRR": [P + "title-23/chapter-I/part-1"],
    "16NYCRR": [P + "title-16/chapter-II/subchapter-A/part-96"],
    "18NYCRR": [P + "title-18/chapter-II/subchapter-B/article-1/part-352"],
}


def main():
    budget = float(sys.argv[sys.argv.index("--budget") + 1]) if "--budget" in sys.argv else 360
    t0 = time.time()
    tocf = REG / "toc" / "NYCRR.json"
    toc = json.loads(tocf.read_text()) if tocf.exists() else {}
    saved = 0
    for code, parts in PARTS.items():
        outdir = REG / "texts" / f"NY_{code}"
        outdir.mkdir(parents=True, exist_ok=True)
        for part in parts:
            if part not in toc:
                kids = nycrr.children(part)
                parent = part.rsplit("/", 1)[0]
                toc[part] = {"code": code, "title": nycrr.title_of(nycrr.get(part)),
                             "sections": [(h, l) for h, l in kids if "NYCRR-" in h],
                             "parent": parent, "siblings": nycrr.children(parent)}
                tocf.write_text(json.dumps(toc, indent=1))
            for h, label in toc[part]["sections"]:
                num = h.split("NYCRR-", 1)[1]
                p = outdir / (re.sub(r"[^0-9A-Za-z.\-]", "_", num) + ".txt")
                if p.exists():
                    continue
                if time.time() - t0 > budget:
                    print("budget reached; saved", saved)
                    return
                page = nycrr.get(h)
                body, notes = nycrr.section_text(page)
                if not body:
                    print("UNFETCHED", h)
                    continue
                p.write_text(f"SOURCE: {nycrr.BASE}{h}\nRETRIEVED: {datetime.date.today().isoformat()} via curl of Cornell LII's "
                             f"republication of the official NYCRR (govt.westlaw.com/nycrr is Cloudflare-walled to curl); text "
                             f"extracted mechanically by register/tools/fetch_nycrr.py\n\n{nycrr.title_of(page)}\n\n{body}\n\n"
                             f"NOTES (LII amendment history):\n{notes}\n")
                saved += 1
    print("complete; saved", saved)


if __name__ == "__main__":
    main()
