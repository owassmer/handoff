"""California Legislative Information (leginfo.legislature.ca.gov), the official California codes and bills.

ref: 'CIV 1950.5' (law code and section) or a codes_displaySection / billTextClient URL.
Section text: the page's codeLawSectionNoHead block from the section number on (the enacted text and its history
note). Bill text: the bill_all block.
unit toc_url: a codes_displayText.xhtml URL (a chapter or article); its sections are the submitCodesValues anchors.
"""
from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urldefrag, urlparse

from . import base

LI = "https://leginfo.legislature.ca.gov/faces/"


def url_of(ref):
    if ref.startswith("http"):
        return ref
    code, num = ref.split(None, 1)
    return f"{LI}codes_displaySection.xhtml?sectionNum={num.rstrip('.')}.&lawCode={code.upper()}"


def section_text(h):
    i = h.find('id="codeLawSectionNoHead"')
    if i < 0:
        return ""
    j = h.find("<h6", i)
    end = h.find('id="footer"', i)
    return base.html_to_text(h[j if j > 0 else i:end if end > 0 else len(h)])


def bill_text(h):
    i = h.find('id="bill_all"')
    return base.html_to_text(h[i:]) if i >= 0 else ""


def preamble_text(h):
    matches = {label for _, label in base.links(h, "") if re.match(r"PREAMBLE\s*:\s*We,", label)}
    return next(iter(matches)) if len(matches) == 1 else ""


class Adapter(base.Adapter):
    name = "ca_leginfo"
    hosts = ("leginfo.legislature.ca.gov",)
    SMOKE = {"ref": "CIV 1950.5", "expect": "security", "label": "Cal. Civ. Code 1950.5 (security deposits)"}

    def section(self, ref):
        url = url_of(ref)
        root, fragment = urldefrag(url)
        if fragment == "preamble" and parse_qs(urlparse(root).query).get("tocCode") == ["CONS"]:
            result = base.page(self, root, lambda b: bool(preamble_text(b)), preamble_text)
            result["source_url"] = url
            result["extra"]["selection"] = "Complete unnumbered preamble in the official Constitution TOC anchor"
            return result
        if "billTextClient" in url or "billNavClient" in url:
            return base.page(self, url, lambda b: 'id="bill_all"' in b, bill_text)
        return base.page(self, url, lambda b: "codeLawSectionNoHead" in b, section_text)

    def toc(self, instrument, unit):
        url = unit["toc_url"]
        law_match = re.search(r"[?&]lawCode=([A-Z]+)(?:&|$)", url)
        if "codes_displayText.xhtml?" not in url or not law_match:
            raise base.core.PipelineError("ca_leginfo: toc_url must identify a codes_displayText unit with lawCode; "
                                          "use section_list for individual sections")
        law = law_match.group(1)
        h = base.fetch(self.name, url, lambda b: "manylawsections" in b).body
        if law == "CONS":
            article = parse_qs(urlparse(url).query).get("article", [""])[0].rstrip(".")
            if not article:
                raise base.core.PipelineError("ca_leginfo: constitution enumeration requires a selected article")
            numbers = {}
            for label in re.findall(r"(?is)<h6\b[^>]*>(.*?)</h6>", h):
                label = base.html_to_text(label).strip()
                match = re.fullmatch(r"(?:Section|SEC\.)\s+([0-9A-Za-z.]+)\.?", label, re.I)
                if match and match[1].rstrip(".") not in numbers:
                    numbers[match[1].rstrip(".")] = label
            return [{"number": f"{article} {n}", "heading": f"Article {article}, Section {n}",
                     "ref": LI + "codes_displaySection.xhtml?" + urlencode(
                         {"lawCode": "CONS", "article": article, "sectionNum": label})}
                    for n, label in numbers.items()]
        out = []
        for m in re.finditer(r"submitCodesValues\('([0-9A-Za-z.]+?)\.?'", h):
            n = m.group(1).rstrip(".")
            if n not in [o["number"] for o in out]:
                out.append({"number": n, "heading": "", "ref": f"{law} {n}"})
        return out
