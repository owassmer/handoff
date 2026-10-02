"""NY laws that newyork.public.law does not carry (NYC Civil Court Act 'CCA', Surrogate's Court Procedure Act 'SCP'),
read from Internet Archive captures of the official nysenate.gov pages (nysenate.gov itself is Cloudflare-walled to
curl and to the browser). Each saved text records the capture timestamp and the page's own 'This entry was
published on' date, so staleness is visible. Text is the page's nys-openleg-result-text block, extracted mechanically.

CLI:
  python3 tools/senate_archive.py toc LAW                 list articles
  python3 tools/senate_archive.py tree LAW ARTICLE ...    list sections of articles (e.g. A18)
  python3 tools/senate_archive.py fetch LAW ARTICLE ...   save every section of the articles under texts/NY_<LAW>/
"""
import datetime
import html
import json
import pathlib
import re
import subprocess
import sys
import time

REG = pathlib.Path(__file__).resolve().parent.parent
RAW = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/reg/senraw"
RAW.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def curl(url, t=90):
    r = subprocess.run(["curl", "-sL", "--max-time", str(t), "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def get(path):
    """Return (html, capture_url) for https://www.nysenate.gov/legislation/laws/<path>, closest capture to today."""
    f = RAW / (path.replace("/", "_") + ".json")
    if f.exists():
        d = json.loads(f.read_text())
        return d["html"], d["capture"]
    page, cap = "", None
    for attempt in range(4):
        r = subprocess.run(["curl", "-sL", "--max-time", "90", "-A", UA, "-w", "\n%{url_effective}",
                            f"https://web.archive.org/web/2026id_/https://www.nysenate.gov/legislation/laws/{path}"],
                           capture_output=True)
        out = r.stdout.decode("utf-8", "replace")
        body, _, eff = out.rpartition("\n")
        if "nys-openleg" in body and re.search(r"/web/\d{14}id_/", eff):
            page, cap = body, eff.strip()
            break
        time.sleep(3 + 4 * attempt)
    time.sleep(0.5)
    if not page:
        return "", cap
    f.write_text(json.dumps({"html": page, "capture": cap}))
    return page, cap


def items(page, law):
    out = []
    for m in re.finditer(r'<a href="https?://www\.nysenate\.gov/legislation/laws/' + law + r'/([^"]+)" class="nys-openleg-result-item-link">\s*'
                         r'<div class="nys-openleg-result-item-name">(.*?)</div>\s*(?:<div class="nys-openleg-result-item-description">(.*?)</div>)?', page, re.S):
        out.append((m.group(1), re.sub(r"\s+", " ", html.unescape(m.group(2))).strip(),
                    re.sub(r"\s+", " ", html.unescape(m.group(3) or "")).strip()))
    return out


def text_of(page):
    m = re.search(r'class="nys-openleg-result-text">(.*?)</div>', page, re.S)
    if not m:
        return ""
    t = m.group(1).replace("<br />", "\n").replace("<br>", "\n")
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return re.sub(r"[ \t]+\n", "\n", t).strip()


def published(page):
    m = re.search(r"This entry was published on (\d{4}-\d{2}-\d{2})", page)
    return m.group(1) if m else None


def tree(law, art):
    page, cap = get(f"{law}/{art}")
    rows = []
    for slug, name, desc in items(page, law):
        if name.upper().startswith("SECTION"):
            rows.append((slug, name, desc))
        elif name.upper().startswith(("PART", "TITLE", "SUBPART")):
            rows.extend(tree(law, slug))
    return rows


def main():
    cmd, law = sys.argv[1], sys.argv[2]
    if cmd == "toc":
        page, cap = get(law)
        print("capture", cap)
        for slug, name, desc in items(page, law):
            print(f"{slug}\t{name}\t{desc}")
    elif cmd == "tree":
        for art in sys.argv[3:]:
            for r in tree(law, art):
                print(art, *r, sep="\t")
    elif cmd == "fetch":
        from concurrent.futures import ThreadPoolExecutor
        outdir = REG / "texts" / f"NY_{law}"
        outdir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        todo = []
        for art in sys.argv[3:]:
            for slug, name, desc in tree(law, art):
                num = name.split(None, 1)[1] if " " in name else slug
                p = outdir / (re.sub(r"[^0-9A-Za-z.\-]", "_", num) + ".txt")
                if not p.exists():
                    todo.append((slug, name, desc, num, p))
        print(len(todo), "to fetch")

        def one(job):
            slug, name, desc, num, p = job
            if time.time() - t0 > 330:
                return "skip"
            page, cap = get(f"{law}/{slug}")
            body = text_of(page)
            if not body:
                return f"UNFETCHED {law} {slug} {cap}"
            p.write_text(
                f"SOURCE: https://www.nysenate.gov/legislation/laws/{law}/{slug}\n"
                f"CAPTURE: {cap}\n"
                f"PUBLISHED: {published(page) or 'not stated'} (nysenate.gov 'This entry was published on' date of the captured version)\n"
                f"RETRIEVED: {datetime.date.today().isoformat()} via curl of the Internet Archive capture of the official "
                f"nysenate.gov page (nysenate.gov is Cloudflare-walled to curl and browser; public.law does not carry "
                f"this law); text extracted mechanically by register/tools/senate_archive.py\n\n"
                f"{name}. {desc}\n\n{body}\n")
            return "saved"
        with ThreadPoolExecutor(2) as ex:
            res = list(ex.map(one, todo))
        from collections import Counter
        print(Counter(r if not r.startswith("UNFETCHED") else "unfetched" for r in res))
        for r in res:
            if r.startswith("UNFETCHED"):
                print(r)


if __name__ == "__main__":
    main()
