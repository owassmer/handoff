"""Fetch and save the text of every section in the in-scope NY units listed in register/toc/NY_<CODE>.json.

Writes register/texts/NY_<CODE>/<section>.txt with a SOURCE/RETRIEVED header. Never overwrites a saved file.
Stops cleanly after --budget seconds (default 540) so it can be rerun until complete.
"""
import datetime
import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import nylaw  # noqa: E402

REG = pathlib.Path(__file__).resolve().parent.parent
TEXTS = REG / "texts"


def sections_of(toc):
    for a in toc["articles"]:
        for s in a.get("sections", []):
            yield a, None, s
        for u in a.get("subunits", []):
            for s in u.get("sections", []):
                yield a, u, s


def sec_number(slug, law_slug):
    return slug[len(law_slug) + len("_section_"):]


def fname(num):
    return re.sub(r"[^0-9A-Za-z.\-]", "_", num) + ".txt"


def main():
    budget = float(sys.argv[sys.argv.index("--budget") + 1]) if "--budget" in sys.argv else 540
    codes = [a for a in sys.argv[1:] if not a.startswith("--") and not a.replace(".", "").isdigit()]
    t0 = time.time()
    done = fetched = 0
    for f in sorted((REG / "toc").glob("NY_*.json")):
        toc = json.loads(f.read_text())
        code = toc["code"]
        if codes and code not in codes:
            continue
        outdir = TEXTS / f"NY_{code}"
        outdir.mkdir(parents=True, exist_ok=True)
        for a, u, s in sections_of(toc):
            num = sec_number(s["slug"], toc["law_slug"])
            p = outdir / fname(num)
            if p.exists():
                done += 1
                continue
            if time.time() - t0 > budget:
                print(f"budget reached; saved {fetched} this run, {done} already present")
                return
            page = nylaw.get(s["slug"])
            body = nylaw.section_text(page) if page else ""
            if len(body) < 40:
                print("EMPTY", code, num)
                continue
            orig, accessed = nylaw.original_source(page)
            p.write_text(
                f"SOURCE: {nylaw.BASE}{s['slug']}\n"
                f"OFFICIAL: {orig or 'nysenate.gov (not stated on page)'}"
                f"{' (' + accessed + ' by public.law)' if accessed else ''}\n"
                f"RETRIEVED: {datetime.date.today().isoformat()} via curl of newyork.public.law (mirror of the official "
                f"nysenate.gov text; nysenate.gov is Cloudflare-walled to curl and browser); text extracted mechanically "
                f"by register/tools/fetch_ny.py (site-added 'pragmatic' cross-reference labels removed)\n\n{body}\n")
            fetched += 1
    print(f"complete; saved {fetched} this run, {done} already present")


if __name__ == "__main__":
    main()
