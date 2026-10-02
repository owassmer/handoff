"""eCode360 (General Code): Glendale CA and other cities.

The site refuses scripts (HTTP 403 to curl); the headless browser renders it, the Internet Archive is the next route.
ref: a section URL https://ecode360.com/<guid> (or the chapter URL with '#<guid>'). The page shows the chapter; the
section text is its title (data-full-title) and its <guid>_content block.
unit toc_url: the chapter URL; its sections are the sectionTitle entries.
"""
from __future__ import annotations

import html as htmlmod
import re

from . import base


def section_block(h, guid):
    t = re.search(r'id="' + guid + r'_title"[^>]*data-full-title="([^"]*)"', h)
    i = h.find(f'id="{guid}_content"')
    if i < 0:
        return ""
    i = h.rfind("<div", 0, i)
    ends = [x for x in (h.find("</article>", i), h.find('<nav id="toc"', i)) if x > 0]
    nxt = re.search(r'class="contentTitle[^"]*sectionTitle', h[i + 10:])
    if nxt:
        ends.append(i + 10 + nxt.start())
    body = base.html_to_text(h[i:min(ends) if ends else len(h)])
    return ((htmlmod.unescape(t.group(1)).replace("\xa0", " ") + "\n\n") if t else "") + body


class Adapter(base.Adapter):
    name = "ecode360"
    hosts = ("ecode360.com", "www.ecode360.com")
    SMOKE = {"ref": "https://ecode360.com/43347754", "expect": "rental housing",
             "label": "Glendale Municipal Code 9.30.010 (just cause eviction: legislative purpose)"}

    def section(self, ref):
        guid = ref.split("#")[-1] if "#" in ref else ref.rstrip("/").split("/")[-1]
        url = ref.split("#")[0]
        f = base.fetch(self.name, url, lambda b: f'id="{guid}_content"' in b, wait_for=f'[id="{guid}_content"]')
        text = section_block(f.body, guid)
        if len(text) < 40:
            raise base.core.PipelineError(f"{self.name}: no section {guid} at {url}")
        return {"text": text, "source_url": f"https://ecode360.com/{guid}", "route": f.route,
                "extra": {"capture": f.capture} if f.capture else {}}

    def toc(self, instrument, unit):
        url = unit["toc_url"]
        if not re.fullmatch(r"https://(?:www\.)?ecode360\.com/\d+(?:#\d+)?", url):
            raise base.core.PipelineError("ecode360: toc_url must identify a numeric chapter page; "
                                          "use section_list for separately enumerated sections")
        h = base.fetch(self.name, url, lambda b: "sectionTitle" in b, wait_for=".sectionTitle").body
        out = []
        for m in re.finditer(r'class="contentTitle barTitle sectionTitle (\d+)"[^>]*data-full-title="([^"]*)"', h):
            label = htmlmod.unescape(m.group(2)).replace("\xa0", " ")
            num = re.match(r"§\s*([0-9A-Za-z.\-]+):?\s*(.*)", label)
            if m.group(1) not in [o["ref"].split("/")[-1] for o in out]:
                out.append({"number": num.group(1) if num else m.group(1), "heading": (num.group(2) if num else label).rstrip("."),
                            "ref": f"https://ecode360.com/{m.group(1)}"})
        return out
