"""municipal.codes (General Code's platform): Vancouver WA (vancouver.municipal.codes), Bellevue
(bellevue.municipal.codes) and other cities.

The site refuses scripts (HTTP 403 to curl); the headless browser renders it, the Internet Archive is the next route.
ref: a section URL (https://vancouver.municipal.codes/VMC/8.46.010). The page shows the whole chapter; the section
text is its <article id="8.46.010"> element (number, name, subsections, history note).
unit toc_url: the chapter URL (https://vancouver.municipal.codes/VMC/8.46); its sections are the type-Section
articles.
"""
from __future__ import annotations

import re

from . import base


def article(h, sid):
    m = re.search(r'<article\b[^>]*\bid="' + re.escape(sid) + r'"', h)
    if not m:
        return ""
    depth, pos = 0, m.start()
    for t in re.finditer(r"<(/?)article\b", h[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            pos = h.find(">", m.start() + t.end()) + 1
            break
    seg = re.sub(r'(?s)<div class="levelnodeactions.*?</div>\s*</div>', " ", h[m.start():pos])
    seg = re.sub(r'(?s)<div[^>]*class="[^"]*selection-status[^"]*".*?</div>', " ", seg)
    ui = {"Search Within This", "This section is included in your selections.", "Share", "Print", "History"}
    return "\n".join(l for l in base.html_to_text(seg).split("\n") if l.strip() not in ui).strip()


class Adapter(base.Adapter):
    name = "municipal_codes"
    hosts = (".municipal.codes",)
    SMOKE = {"ref": "https://vancouver.municipal.codes/VMC/8.46.010", "expect": "Housing costs",
             "label": "Vancouver Municipal Code 8.46.010 (notice of rent increase: definitions)"}

    def section(self, ref):
        sid = ref.rstrip("/").split("/")[-1]
        f = base.fetch(self.name, ref, lambda b: f'id="{sid}"' in b, wait_for=f'[id="{sid}"]')
        text = article(f.body, sid)
        if len(text) < 40:
            raise base.core.PipelineError(f"{self.name}: no article {sid} at {ref}")
        return {"text": text, "source_url": ref, "route": f.route, "extra": {"capture": f.capture} if f.capture else {}}

    def toc(self, instrument, unit):
        url = unit["toc_url"]
        h = base.fetch(self.name, url, lambda b: "type-Section" in b, wait_for="article.type-Section").body
        root = url.rsplit("/", 1)[0]
        out = []
        for m in re.finditer(r'<article class="[^"]*type-Section[^"]*" id="([^"]+)".*?<span class="name"[^>]*>(.*?)</span>', h, re.S):
            out.append({"number": m.group(1), "heading": base.html_to_text(m.group(2)).rstrip("."), "ref": f"{root}/{m.group(1)}"})
        return out
