"""American Legal Publishing code library (codelibrary.amlegal.com): Los Angeles, San Francisco and others.

The site refuses scripts (HTTP 403 to curl); the headless browser renders it, and the Internet Archive is the next
route. ref: a section URL (https://codelibrary.amlegal.com/codes/los_angeles/latest/lamc/0-0-0-195228).
Section text: the page's rid-<doc id> Section block, up to the next rid- block.
unit toc_url: an article or chapter URL; its sections are the table-of-contents links whose data-orig-doc-id is that
node.
"""
from __future__ import annotations

import re

from . import base


def node_of(url):
    return url.rstrip("/").split("/")[-1].split("#")[0]


def block(h, node):
    i = h.find(f'id="rid-{node}"')
    if i < 0:
        return ""
    i = h.rfind("<div", 0, i)
    nxt = re.search(r'<div id="rid-[^"]+" class="Section', h[i + 20:])
    seg = h[i:i + 20 + nxt.start()] if nxt else h[i:]
    seg = re.sub(r'(?s)<div class="code-options.*?</div>\s*</div>', " ", seg)
    seg = re.sub(r"(?s)<button\b.*?</button>", " ", seg)
    return base.html_to_text(seg)


class Adapter(base.Adapter):
    name = "amlegal"
    hosts = ("codelibrary.amlegal.com",)
    SMOKE = {"ref": "https://codelibrary.amlegal.com/codes/los_angeles/latest/lamc/0-0-0-195228",
             "expect": "Rental Unit", "label": "Los Angeles Municipal Code 151.02 (RSO definitions)"}

    def get(self, url, node):
        return base.fetch(self.name, url, lambda b: f'id="rid-{node}"' in b, wait_for=f'[id="rid-{node}"]')

    def section(self, ref):
        node = node_of(ref)
        f = self.get(ref, node)
        text = block(f.body, node)
        if len(text) < 40:
            raise base.core.PipelineError(f"{self.name}: no section block rid-{node} at {ref}")
        return {"text": text, "source_url": ref, "route": f.route, "extra": {"capture": f.capture} if f.capture else {}}

    def toc(self, instrument, unit):
        """Sections under the unit's node in the page's table of contents (the collapse block after the node's
        entry); article, chapter, division and part entries without listed children are opened in turn."""
        url = unit["toc_url"]
        base_url = url[:url.index("/codes/")]
        out, todo, seen = [], [url], set()
        while todo:
            u = todo.pop(0)
            node = node_of(u)
            if node in seen:
                continue
            seen.add(node)
            h = base.fetch(self.name, u, lambda b: f'data-docid="{node}"' in b, wait_for=f'[data-docid="{node}"]').body
            i = h.find(f'data-docid="{node}"')
            j = h.find('<div class="collapse', i)
            if i < 0 or j < 0:
                continue
            depth, k = 0, j
            for t in re.finditer(r"<(/?)div\b", h[j:]):
                depth += -1 if t.group(1) else 1
                if depth == 0:
                    k = j + t.end()
                    break
            blk = h[j:k]
            for m in re.finditer(r'<a class="toc-link" data-docid="([^"]+)"[^>]*href="([^"]+)">([^<]+)</a>', blk):
                label = re.sub(r"\s+", " ", base.htmlmod.unescape(m.group(3))).strip()
                if re.match(r"(ARTICLE|CHAPTER|DIVISION|PART|SUBCHAPTER|SUBARTICLE)\b", label, re.I):
                    todo.append(base_url + m.group(2))
                    continue
                num = re.match(r"(?:SEC\.|SECTION|§)\s*([0-9][0-9A-Za-z.\-]*?)\.?\s+(.*)", label)
                if m.group(1) not in [o["ref"].rsplit("/", 1)[-1] for o in out]:
                    out.append({"number": num.group(1) if num else m.group(1),
                                "heading": (num.group(2) if num else label).rstrip("."), "ref": base_url + m.group(2)})
        return out
