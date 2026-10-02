"""Portland City Code on portland.gov (the City's official code pages).

ref: '30.01.085' or https://www.portland.gov/code/30/01/085. Section text: the page's h1 (number and heading) and its
<article> body (amendment note and text).
unit toc_url: the chapter page (https://www.portland.gov/code/30/01); its sections are the /code/30/01/NNN links.
"""
from __future__ import annotations

import re

from . import base

SITE = "https://www.portland.gov/code/"


def url_of(ref):
    return ref if ref.startswith("http") else SITE + ref.replace(".", "/")


def section_text(h):
    t = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    i = h.find("<article")
    j = h.find("</article>", i)
    if i < 0:
        return ""
    body = base.html_to_text(h[i:j if j > 0 else len(h)])
    body = re.sub(r"^Label:\s*City code section\s*", "", body)
    return (base.html_to_text(t.group(1)) + "\n\n" if t else "") + body


class Adapter(base.Adapter):
    name = "portland_code"
    hosts = ("www.portland.gov", "portland.gov")
    SMOKE = {"ref": "30.01.085", "expect": "relocation", "label": "Portland City Code 30.01.085 (relocation assistance)"}

    def section(self, ref):
        return base.page(self, url_of(ref), lambda b: "<article" in b, section_text)

    def toc(self, instrument, unit):
        url = unit["toc_url"].rstrip("/")
        path = url.split("portland.gov")[1]
        h = base.fetch(self.name, url, lambda b: path in b).body
        out = []
        for href, label in base.links(h, "^" + re.escape(path) + r"/\d"):
            m = re.match(r"([0-9.]+[A-Z]?)\s+(.*)", label)
            if m and m.group(1) not in [o["number"] for o in out]:
                out.append({"number": m.group(1), "heading": m.group(2).rstrip("."), "ref": "https://www.portland.gov" + href})
        return out
