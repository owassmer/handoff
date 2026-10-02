"""Independent review 5A: walk newyork.public.law table-of-contents pages and list every section with its heading.

Usage: python3 review/ir5a_toc.py SLUG [SLUG ...]   e.g. n.y._general_obligations_law_article_7
Recurses into sub-article/title/part pages. Output: one line per section, 'slug<TAB>heading'. Saves nothing under sources/;
the listing is written to the profile scratch folder ir5a/toc_<slug>.txt for the reviewer's discovery record.
"""
import html
import pathlib
import re
import subprocess
import sys
import time

BASE = "https://newyork.public.law/laws/"
OUT = pathlib.Path.home() / ".hermes/profiles/ferro/cache/scratch/ir5a"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/124 Safari/537.36"


def get(slug):
    r = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "60", "-A", UA, BASE + slug], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def walk(slug, depth=0, seen=None):
    seen = seen if seen is not None else set()
    if slug in seen or depth > 4:
        return []
    seen.add(slug)
    page = get(slug)
    time.sleep(0.3)
    rows = []
    for m in re.finditer(r'<a[^>]+href="(?:https://newyork\.public\.law)?/?(?:laws/)?(n\.y\.[^"#?]+)"[^>]*>(.*?)</a>', page, re.S):
        href, label = html.unescape(m.group(1)), html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))
        label = re.sub(r"\s+", " ", label).strip()
        if not href.startswith(slug.split("_article")[0].split("_section")[0]):
            continue
        if "_section_" in href:
            rows.append((href, label))
        elif href.startswith(slug + "_") and href != slug:
            rows.extend(walk(href, depth + 1, seen))
    out, s = [], set()
    for r in rows:
        if r[0] not in s:
            s.add(r[0])
            out.append(r)
    return out


if __name__ == "__main__":
    for slug in sys.argv[1:]:
        rows = walk(slug)
        txt = "\n".join(f"{h}\t{l}" for h, l in rows)
        (OUT / f"toc_{slug.replace('/', '_')}.txt").write_text(txt + "\n")
        print(f"== {slug} ({len(rows)})")
        print(txt)
