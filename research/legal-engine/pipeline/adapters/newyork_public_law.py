"""newyork.public.law: NY statutes (a mirror of the official nysenate.gov text). Ported from register/tools/nylaw.py.

Section text is the page's #leaf-page-title and #leaf-statute-body with the site's added 'pragmatic'
cross-reference labels removed, so the enacted words remain. The page's 'Original Source' line (the nysenate.gov
URL and the mirror's last access date) goes in the header.
ref: a section slug (n.y._general_obligations_law_section_7-108) or its URL.
unit toc_url: an article/title page; every section under it is listed, recursing into titles and parts.
"""
from __future__ import annotations

import html
import html.parser
import re

from . import base

BASE = "https://newyork.public.law/laws/"


class _Body(html.parser.HTMLParser):
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "blockquote", "pre", "table"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = self.skip = 0
        self.out, self.stack = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and a.get("id") in ("leaf-page-title", "leaf-statute-body"):
            self.depth = 1
            self.out.append("\n")
            return
        if self.depth:
            if tag == "div":
                self.depth += 1
            if tag == "a" and "pragmatic" in (a.get("class") or ""):
                self.skip += 1
                self.stack.append("skip-a")
            elif tag == "a":
                self.stack.append("a")
            if tag in ("script", "style"):
                self.skip += 1
            if tag in self.BLOCK:
                self.out.append("\n")

    def handle_endtag(self, tag):
        if not self.depth:
            return
        if tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.out.append("\n")
            return
        if tag == "a" and self.stack and self.stack.pop() == "skip-a":
            self.skip -= 1
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.depth and not self.skip:
            self.out.append(data)


def section_text(page):
    b = _Body()
    b.feed(page)
    t = "".join(b.out).replace("­", "")
    t = re.sub(r"[ \t\r\f\v\xa0]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def original_source(page):
    m = re.search(r"Original Source:</i>\s*<i>(.*?)</i>,\s*<code>(.*?)</code>\s*\((last.*?)\)", page, re.S)
    if not m:
        return None, None
    clean = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
    return clean(m.group(2)).replace(" ", ""), clean(m.group(3))


def url_of(ref):
    return ref if ref.startswith("http") else BASE + ref


class Adapter(base.Adapter):
    name = "newyork_public_law"
    hosts = ("newyork.public.law",)
    SMOKE = {"ref": "n.y._general_obligations_law_section_7-108", "expect": "fourteen days",
             "label": "NY GOL 7-108 (deposit statement and refund)"}

    def get(self, url):
        return base.fetch(self.name, url, lambda b: 'id="leaf-statute-body"' in b or "leaf-page-title" in b)

    def section(self, ref):
        f = self.get(url_of(ref))
        body = section_text(f.body)
        if len(body) < 40:
            raise base.core.PipelineError(f"{self.name}: no statute body at {url_of(ref)}")
        orig, accessed = original_source(f.body)
        return {"text": body, "source_url": url_of(ref), "route": f.route,
                "extra": {"official": (orig or "nysenate.gov (not stated on page)") + (f" ({accessed} by public.law)" if accessed else ""),
                          **({"capture": f.capture} if f.capture else {})}}

    def toc(self, instrument, unit):
        slug = unit["toc_url"].replace(BASE, "").strip("/")
        law = re.sub(r"_(article|title|part|chapter|subpart)_.*$", "", slug)
        out, seen, todo = [], set(), [slug]
        while todo:
            s = todo.pop(0)
            if s in seen:
                continue
            seen.add(s)
            page = base.fetch(self.name, BASE + s, lambda b: "newyork.public.law" in b).body
            for m in re.finditer(r'<a[^>]+href="(?:https://newyork\.public\.law)?/?(?:laws/)?(n\.y\.[^"#?]+)"[^>]*>(.*?)</a>', page, re.S):
                href = html.unescape(m.group(1))
                label = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
                if href.startswith(law + "_section_") and href not in {o["ref"] for o in out}:
                    num = href[len(law) + len("_section_"):]
                    out.append({"number": num.upper() if re.search(r"[a-z]$", num) and "-" in num else num,
                                "heading": label.split(" ", 1)[1] if " " in label else label, "ref": href})
                elif href.startswith(s + "_") and href != s:
                    todo.append(href)
        return out
