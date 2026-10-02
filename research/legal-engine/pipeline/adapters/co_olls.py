"""Colorado Revised Statutes, the 2026 official text published by the Office of Legislative Legal Services at
olls.info (one Word-exported page per title, windows-1252).

ref: '38-12-103' (or the title URL with '#38-12-103'). Section text: from the bold paragraph that opens the section
to the next section opening or article/part heading, source note included.
unit toc_url: the title page; unit 'section_prefix' (e.g. '38-12-1' for article 12 part 1) or a unit label 'art. 12'
(prefix '38-12-') selects the sections from the title's table of contents.
"""
from __future__ import annotations

import html as htmlmod
import re

from . import base

YEAR = 2026
SITE = "https://olls.info/crs/crs{}-title-{:02d}.htm"
NUM = r"\d+(?:\.\d+)?-\d+(?:\.\d+)?-\d+(?:\.\d+)?"


def title_url(num):
    return SITE.format(YEAR, int(num.split("-")[0].split(".")[0]))


def paragraphs(h):
    out = []
    for m in re.finditer(r"<p\b([^>]*)>(.*?)</p>", h, re.S | re.I):
        attrs, inner = m.group(1), m.group(2)
        b = re.match(r"\s*<b>(.*?)</b>", inner, re.S | re.I)
        clean = lambda s: re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")).strip()
        out.append((attrs, clean(b.group(1)) if b else "", clean(inner)))
    return out


def sections(h):
    out, cur = {}, None
    for attrs, bold, txt in paragraphs(h):
        m = re.match(r"(" + NUM + r")\.$", bold) if bold else None
        if m and "1.25in" not in attrs:
            cur = m.group(1)
            out[cur] = [txt]
        elif cur and (re.match(r"(ARTICLE|PART) \d", txt) or "text-align:center" in attrs):
            cur = None
        elif cur and txt:
            out[cur].append(txt)
    return {k: "\n".join(v) for k, v in out.items()}


def toc_entries(h):
    out = []
    for attrs, _, txt in paragraphs(h):
        if "1.25in" in attrs:
            m = re.match(r"(" + NUM + r")\.\s+(.*)$", txt)
            if m and m.group(1) not in [o[0] for o in out]:
                out.append((m.group(1), m.group(2).strip()))
    return out


class Adapter(base.Adapter):
    name = "co_olls"
    hosts = ("olls.info", "www.olls.info")
    SMOKE = {"ref": "38-12-103", "expect": "security deposit", "label": "C.R.S. 38-12-103 (return of security deposit)"}

    def title(self, url):
        return base.fetch(self.name, url, lambda b: "MsoNormal" in b, encoding="windows-1252")

    def section(self, ref):
        num = ref.split("#")[-1] if ref.startswith("http") else ref
        url = ref.split("#")[0] if ref.startswith("http") else title_url(num)
        f = self.title(url)
        t = sections(f.body).get(num)
        if not t:
            raise base.core.PipelineError(f"{self.name}: section {num} not found on {url} (route {f.route})")
        return {"text": t, "source_url": f"{url}#{num}", "route": f.route,
                "extra": {"capture": f.capture} if f.capture else {}}

    def toc(self, instrument, unit):
        url = unit["toc_url"]
        pre = unit.get("section_prefix")
        if not pre:
            t = re.search(r"title-(\d+)", url).group(1).lstrip("0")
            art = re.search(r"art\.?\s*(\S+)", unit["unit"]).group(1)
            pre = f"{t}-{art}-"
        return [{"number": n, "heading": hd.rstrip("."), "ref": n} for n, hd in toc_entries(self.title(url).body)
                if n.startswith(pre)]
