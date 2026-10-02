"""The NY Senate's official laws site (nysenate.gov/legislation/laws), reached through the Internet Archive when the
site walls scripts. Ported from register/tools/senate_archive.py. Used for laws newyork.public.law does not carry
(NYC Civil Court Act 'CCA', Surrogate's Court Procedure Act 'SCP').

Section text is the page's nys-openleg-result-text block; the header records the capture URL and the page's own
'This entry was published on' date, so staleness is visible.
ref: 'LAW/SECTION' (CCA/1801) or the nysenate.gov URL.
unit toc_url: the article page (https://www.nysenate.gov/legislation/laws/CCA/A18).
"""
from __future__ import annotations

import html
import re

from . import base

SITE = "https://www.nysenate.gov/legislation/laws/"


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


def items(page, law):
    out = []
    for m in re.finditer(r'<a href="https?://www\.nysenate\.gov/legislation/laws/' + law + r'/([^"]+)" class="nys-openleg-result-item-link">\s*'
                         r'<div class="nys-openleg-result-item-name">(.*?)</div>\s*(?:<div class="nys-openleg-result-item-description">(.*?)</div>)?', page, re.S):
        out.append((m.group(1), re.sub(r"\s+", " ", html.unescape(m.group(2))).strip(),
                    re.sub(r"\s+", " ", html.unescape(m.group(3) or "")).strip()))
    return out


class Adapter(base.Adapter):
    name = "nysenate_archive"
    hosts = ("www.nysenate.gov",)
    SMOKE = {"ref": "CCA/1801", "expect": "small claims", "label": "NYC Civil Court Act 1801 (small claims defined)"}

    def get(self, url):
        return base.fetch(self.name, url, lambda b: "nys-openleg" in b)

    def section(self, ref):
        url = ref if ref.startswith("http") else SITE + ref
        f = self.get(url)
        body = text_of(f.body)
        if not body:
            raise base.core.PipelineError(f"{self.name}: no section text at {url}")
        heads = items(f.body, url.replace(SITE, "").split("/")[0])
        extra = {"published": f"{published(f.body) or 'not stated'} (nysenate.gov 'This entry was published on' date)"}
        if f.capture:
            extra["capture"] = f.capture
        return {"text": body, "source_url": url, "route": f.route, "extra": extra, "items": heads}

    def toc(self, instrument, unit):
        url = unit["toc_url"]
        law = url.replace(SITE, "").split("/")[0]
        out, todo = [], [url]
        while todo:
            u = todo.pop(0)
            for slug, name, desc in items(self.get(u).body, law):
                if name.upper().startswith("SECTION"):
                    out.append({"number": name.split(None, 1)[1] if " " in name else slug, "heading": desc,
                                "ref": SITE + law + "/" + slug})
                elif name.upper().startswith(("PART", "TITLE", "SUBPART")):
                    todo.append(SITE + law + "/" + slug)
        return out
