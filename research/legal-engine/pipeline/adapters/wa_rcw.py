"""Revised Code of Washington on the Legislature's official site (app.leg.wa.gov/RCW).

ref: '59.18.280' or a default.aspx?cite= URL. Section text: the title block (citation and caption) and the section
body with its history, up to the notes panel.
unit toc_url: the chapter page (default.aspx?cite=59.18); its sections are the cite links with their captions.
"""
from __future__ import annotations

import re

from . import base

RCW = "https://app.leg.wa.gov/RCW/default.aspx?cite="


def url_of(ref):
    return ref if ref.startswith("http") else RCW + ref


def section_text(h):
    i = h.find('id="ContentPlaceHolder1_pnlTitleBlock"')
    if i < 0:
        return ""
    j = h.find('id="ContentPlaceHolder1_pnlExpanded"', i)
    k = h.find('class="footer', i)
    end = min(x for x in (j, k, len(h)) if x > 0)
    block = re.sub(r'(?s)<a id="ContentPlaceHolder1_lnkTitlePdf".*?</a>', " ", h[i:h.rfind("<", 0, end)])
    return base.html_to_text("<div " + block)


class Adapter(base.Adapter):
    name = "wa_rcw"
    hosts = ("app.leg.wa.gov", "apps.leg.wa.gov")
    SMOKE = {"ref": "59.18.280", "expect": "full and specific statement", "label": "RCW 59.18.280 (deposit statement and refund)"}

    def section(self, ref):
        return base.page(self, url_of(ref), lambda b: "pnlTitleBlock" in b, section_text)

    def toc(self, instrument, unit):
        url = unit["toc_url"]
        chap = re.search(r"cite=([0-9A-Za-z.]+)", url).group(1)
        h = base.fetch(self.name, url, lambda b: "cite=" + chap in b).body
        out = []
        rx = re.compile(r"<a href='https?://app\.leg\.wa\.gov/RCW/default\.aspx\?cite=(" + re.escape(chap) +
                        r"\.[0-9A-Za-z]+)'>[^<]+</a></td><td[^>]*>(.*?)</td>", re.S)
        for m in rx.finditer(h):
            if m.group(1) not in [o["number"] for o in out]:
                out.append({"number": m.group(1), "heading": base.html_to_text(m.group(2)), "ref": m.group(1)})
        return out
