"""NY Codes, Rules and Regulations from Cornell LII (law.cornell.edu/regulations/new-york), which republishes the
official NYCRR (govt.westlaw.com/nycrr now Cloudflare-walls curl). Section text = the page's div.statereg-text; the
page's statereg-notes (amendment history) are kept after the text. LII rate-limits: requests are spaced out and
retried on refusal. Raw pages are cached under the profile scratch folder.

CLI:
  python3 tools/nycrr.py crumbs 'SECTION-CITE'     e.g. 19-NYCRR-175.1 -> breadcrumb links (title/chapter/part)
  python3 tools/nycrr.py toc URLPATH               child links of a TOC page (e.g. /regulations/new-york/title-19)
"""
import html
import pathlib
import re
import subprocess
import sys
import time

BASE = "https://www.law.cornell.edu"
RAW = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/reg/nycrr/raw"
RAW.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
SLEEP = 2.5


def get(path):
    f = RAW / (re.sub(r"[^A-Za-z0-9._-]", "_", path.strip("/")) + ".html")
    if f.exists() and f.stat().st_size > 3000:
        return f.read_text(errors="replace")
    for attempt in range(5):
        r = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "60", "-A", UA, "-w", "\n%{http_code}", BASE + path],
                           capture_output=True)
        out = r.stdout.decode("utf-8", "replace")
        body, _, code = out.rpartition("\n")
        time.sleep(SLEEP)
        if code == "200" and len(body) > 3000 and "Just a moment" not in body[:2000]:
            f.write_text(body)
            return body
        if code == "404":
            return ""
        time.sleep(20 * (attempt + 1))
    return ""


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def links(page):
    return [(m.group(1), clean(m.group(2))) for m in
            re.finditer(r'href="(/regulations/new-york/[^"#?]+)"[^>]*>(.*?)</a>', page, re.S)]


def children(path):
    page = get(path)
    crumbs = set()
    m = re.search(r'<ol class="breadcrumb">(.*?)</ol>', page, re.S)
    if m:
        crumbs = {h for h, _ in links(m.group(1))}
    return [(h, l) for h, l in links(page) if h not in crumbs and h != path and (h.startswith(path + "/") or "NYCRR-" in h)]


def section_text(page):
    m = re.search(r'<div class="statereg-text">(.*?)</div>\s*<div class="statereg-notes">(.*?)<div class="tab-pane"', page, re.S)
    if not m:
        m2 = re.search(r'<div class="statereg-text">(.*?)</div>', page, re.S)
        if not m2:
            return "", ""
        body, notes = m2.group(1), ""
    else:
        body, notes = m.group(1), m.group(2)

    def txt(x):
        x = re.sub(r"</(p|div|li|tr|h\d)>", "\n", x)
        x = re.sub(r"<br\s*/?>", "\n", x)
        x = html.unescape(re.sub(r"<[^>]+>", "", x))
        x = re.sub(r"[ \t\r ]+", " ", x)
        x = re.sub(r" *\n *", "\n", x)
        return re.sub(r"\n{2,}", "\n", x).strip()
    return txt(body), txt(notes)


def title_of(page):
    m = re.search(r'<h1 class="title" id="page_title">(.*?)</h1>', page, re.S)
    return clean(m.group(1)) if m else ""


if __name__ == "__main__":
    if sys.argv[1] == "crumbs":
        page = get("/regulations/new-york/" + sys.argv[2])
        m = re.search(r'<ol class="breadcrumb">(.*?)</ol>', page, re.S)
        for h, l in links(m.group(1) if m else ""):
            print(h, "|", l)
    elif sys.argv[1] == "toc":
        for h, l in children(sys.argv[2]):
            print(h, "|", l)
