"""NY statutes from newyork.public.law (mirror of the official nysenate.gov text): tables of contents and section text.

Mechanical only: TOC links and headings are read from the site's own pages; section text is the page's
`leaf-statute-body` with the site's added 'pragmatic' cross-reference labels removed (the 'pedantic' anchor keeps
the enacted words). Raw HTML is cached under the profile scratch folder; saved section texts are never refetched.

CLI:
  python3 tools/nylaw.py toc LAWSLUG            print the law's top-level units (articles) with headings
  python3 tools/nylaw.py tree UNITSLUG          print every section under a unit (recursing into titles/parts)
"""
import html
import html.parser
import json
import pathlib
import re
import subprocess
import sys
import time

BASE = "https://newyork.public.law/laws/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
RAW = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/reg/nyraw"
RAW.mkdir(parents=True, exist_ok=True)


def get(slug, sleep=0.25):
    f = RAW / (re.sub(r"[^A-Za-z0-9._-]", "_", slug) + ".html")
    if f.exists() and f.stat().st_size > 2000:
        return f.read_text(errors="replace")
    for attempt in range(3):
        r = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "60", "-A", UA, BASE + slug], capture_output=True)
        page = r.stdout.decode("utf-8", "replace")
        time.sleep(sleep)
        if len(page) > 2000 and "Just a moment" not in page[:2000]:
            f.write_text(page)
            return page
        time.sleep(2 + attempt * 3)
    return ""


def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = s.replace("­", "").replace("‑", "-")
    return re.sub(r"\s+", " ", s).strip()


def links(page):
    out = []
    for m in re.finditer(r'<a[^>]+href="(?:https://newyork\.public\.law)?/?(?:laws/)?(n\.y\.[^"#?]+)"[^>]*>(.*?)</a>', page, re.S):
        out.append((html.unescape(m.group(1)), clean(m.group(2))))
    return out


def law_units(law):
    """Top-level units of a law: [(slug, label)] in page order."""
    page = get(law)
    seen, out = set(), []
    for href, label in links(page):
        if href.startswith(law + "_") and "_section_" not in href and href not in seen:
            rest = href[len(law) + 1:]
            if rest.count("_") == 1:  # article_N / title_N / part_N
                seen.add(href)
                out.append((href, label))
    return out


def tree(slug, depth=0, seen=None):
    """Every section under a unit, in order: [(section_slug, label, path_of_subunit_labels)]."""
    seen = seen if seen is not None else set()
    if slug in seen or depth > 5:
        return []
    seen.add(slug)
    page = get(slug)
    rows = []
    base = slug.split("_section")[0]
    for href, label in links(page):
        if "_section_" in href:
            law = re.sub(r"_(article|title|part|chapter|subpart)_.*$", "", slug)
            if href.startswith(law + "_section_"):
                rows.append((href, label, ()))
        elif href.startswith(slug + "_") and href != slug:
            for s, l, p in tree(href, depth + 1, seen):
                rows.append((s, l, (label,) + p))
    out, s = [], set()
    for r in rows:
        if r[0] not in s:
            s.add(r[0])
            out.append(r)
    return out


class _Body(html.parser.HTMLParser):
    """Text of #leaf-page-title and #leaf-statute-body, skipping <a class="pragmatic"> labels."""

    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "blockquote", "pre", "table"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0  # >0 while inside a wanted div
        self.skip = 0
        self.out = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and a.get("id") in ("leaf-page-title", "leaf-statute-body"):
            self.depth = 1
            self.out.append("\n")
            return
        if self.depth:
            if tag == "div":
                self.depth += 1
            if tag == "a" and "pragmatic" in (a.get("class") or ""):
                self.skip += 1
                self.stack.append("skip-a")
            elif tag == "a":
                self.stack.append("a")
            if tag in ("script", "style"):
                self.skip += 1
            if tag in self.BLOCK:
                self.out.append("\n")

    def handle_endtag(self, tag):
        if not self.depth:
            return
        if tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.out.append("\n")
            return
        if tag == "a" and self.stack:
            if self.stack.pop() == "skip-a":
                self.skip -= 1
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.depth and not self.skip:
            self.out.append(data)


def section_text(page):
    b = _Body()
    b.feed(page)
    t = "".join(b.out).replace("­", "")
    t = re.sub(r"[ \t\r\f\v ]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def original_source(page):
    m = re.search(r"Original Source:</i>\s*<i>(.*?)</i>,\s*<code>(.*?)</code>\s*\((last.*?)\)", page, re.S)
    if not m:
        return None, None
    return clean(m.group(2)).replace(" ", ""), clean(m.group(3))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "toc":
        for law in sys.argv[2:]:
            print("==", law)
            for s, l in law_units(law):
                print(f"{s}\t{l}")
    elif cmd == "tree":
        for u in sys.argv[2:]:
            rows = tree(u)
            print("==", u, len(rows))
            for s, l, p in rows:
                print(f"{s}\t{l}\t{' > '.join(p)}")
