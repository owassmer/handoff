"""Oregon Revised Statutes on the Legislature's official site (oregonlegislature.gov/bills_laws/ors), one page per
chapter (a Word export in windows-1252).

ref: '90.300' or the chapter URL with '#90.300'. Section text: from the bold paragraph that opens the section
('90.300 Security deposits; prepaid rent.') to the next section or chapter heading, notes included.
unit toc_url: the chapter page; every section opening in it is listed (optionally limited by unit 'from'/'to').
"""
from __future__ import annotations

import html as htmlmod
import re

from . import base

SITE = "https://www.oregonlegislature.gov/bills_laws/ors/ors{:03d}.html"
START = re.compile(r"^\s*(\d{1,3}[A-C]?\.\d{3,4}[A-Za-z]?)\s+(.*)$", re.S)


def chapter_url(num):
    ch = re.match(r"(\d+)([A-C]?)", num)
    return SITE.format(int(ch.group(1))).replace(".html", ch.group(2).lower() + ".html") if ch.group(2) else SITE.format(int(ch.group(1)))


def paragraphs(h):
    """[(bold text at the start or '', paragraph text)] for the chapter page."""
    out = []
    for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", h, re.S | re.I):
        inner = m.group(1)
        b = re.match(r"\s*(?:<span[^>]*>\s*)?<b>(.*?)</b>", inner, re.S | re.I)
        txt = re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", inner)).replace("\xa0", " ")).strip()
        bold = re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", b.group(1))).replace("\xa0", " ")).strip() if b else ""
        out.append((bold, txt))
    return out


def sections(h):
    """{number: (heading, text)} for every section opening on the page, in order."""
    out, cur = {}, None
    for bold, txt in paragraphs(h):
        m = START.match(bold) if bold else None
        if m:
            cur = m.group(1)
            out[cur] = (m.group(2).strip().rstrip("."), [txt])
        elif cur and bold and bold.isupper() and len(bold) > 3:
            cur = None
        elif cur and txt:
            out[cur][1].append(txt)
    return {k: (v[0], "\n".join(v[1])) for k, v in out.items()}


class Adapter(base.Adapter):
    name = "or_ors"
    hosts = ("www.oregonlegislature.gov", "oregonlegislature.gov")
    SMOKE = {"ref": "90.300", "expect": "security deposit", "label": "ORS 90.300 (security deposits)"}

    def chapter(self, url):
        return base.fetch(self.name, url, lambda b: "MsoNormal" in b, encoding="windows-1252")

    def section(self, ref):
        num = ref.split("#")[-1] if ref.startswith("http") else ref
        url = ref.split("#")[0] if ref.startswith("http") else chapter_url(num)
        f = self.chapter(url)
        s = sections(f.body).get(num)
        if not s:
            raise base.core.PipelineError(f"{self.name}: section {num} not found on {url} (route {f.route})")
        extra = {"capture": f.capture} if f.capture else {}
        return {"text": s[1], "source_url": f"{url}#{num}", "route": f.route, "extra": extra}

    def toc(self, instrument, unit):
        secs = sections(self.chapter(unit["toc_url"]).body)
        key = lambda n: float(n.split(".", 1)[1].rstrip("abcdefghijklmnopqrstuvwxyz") or 0)
        lo, hi = unit.get("from"), unit.get("to")
        return [{"number": n, "heading": h, "ref": n} for n, (h, _) in secs.items()
                if (lo is None or key(n) >= key(lo)) and (hi is None or key(n) <= key(hi))]
