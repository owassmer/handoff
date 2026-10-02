"""Arizona Revised Statutes on the Legislature's official site (azleg.gov/ars).

ref: '33-1321' or '12-341.01' or a www.azleg.gov/ars/TT/NNNNN.htm URL. Section text: the page body (one section per
page: number, heading, text).
unit toc_url: https://www.azleg.gov/arsDetail/?title=33 with unit 'chapter' and 'article' (numbers), or a unit label
'ch. 10 art. 2'; the article's sections are listed in the title page's accordion.
"""
from __future__ import annotations

import re

from . import base


def url_of(ref):
    if ref.startswith("http"):
        return ref
    t, s = ref.split("-", 1)
    main, _, dec = s.partition(".")
    return f"https://www.azleg.gov/ars/{t}/{int(main):05d}{('.' + dec) if dec else ''}.htm"


def section_text(h):
    m = re.search(r"<BODY[^>]*>(.*)</BODY>", h, re.S | re.I)
    return base.html_to_text(m.group(1) if m else h)


class Adapter(base.Adapter):
    name = "az_ars"
    hosts = ("www.azleg.gov", "azleg.gov")
    SMOKE = {"ref": "33-1321", "expect": "one and one-half month's rent", "label": "A.R.S. 33-1321 (security deposits)"}

    def section(self, ref):
        return base.page(self, url_of(ref), lambda b: "<p>" in b or "<P>" in b, section_text)

    def toc(self, instrument, unit):
        ch = unit.get("chapter") or re.search(r"ch\.?\s*(\S+)", unit["unit"]).group(1)
        art = unit.get("article") or (re.search(r"art\.?\s*(\S+)", unit["unit"]) or [None, None])[1]
        h = base.fetch(self.name, unit["toc_url"], lambda b: "accordion" in b).body
        m = re.search(r'>Chapter ' + re.escape(str(ch)) + r'</a>(.*?)(?=>Chapter \d|\Z)', h, re.S)
        if not m:
            raise base.core.PipelineError(f"{self.name}: chapter {ch} not on {unit['toc_url']}")
        block = m.group(1)
        if art:
            a = re.search(r'>Article ' + re.escape(str(art)) + r'</a>(.*?)(?=>Article \d|\Z)', block, re.S)
            if not a:
                raise base.core.PipelineError(f"{self.name}: chapter {ch} article {art} not on {unit['toc_url']}")
            block = a.group(1)
        out = []
        for m in re.finditer(r'docName=(https://www\.azleg\.gov/ars/\d+/[\d.]+\.htm)">([^<]+)</a></li><li class="colright">([^<]*)<', block):
            out.append({"number": m.group(2).strip(), "heading": m.group(3).strip(), "ref": m.group(2).strip()})
        return out
