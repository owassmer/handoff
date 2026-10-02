"""Municode Library (library.municode.com) through its public JSON API (api.municode.com), the route the site's
own pages use. Seattle, Denver, Oakland, San Jose, Long Beach and other cities.

ref: a library URL with the section's nodeId
  (https://library.municode.com/wa/seattle/codes/municipal_code?nodeId=TIT7COPR_CH7.24REAGRE_7.24.010SHTI).
The client, product and latest publication job are resolved from the URL (Clients/stateAbbr, ClientContent,
Jobs/latest). Section text: the document with that Id in CodesContent (its title and content), following NextNode
when the section is in a later chunk. The header records the job (supplement) read.
unit toc_url: the library URL of a chapter or article node; its leaf children (codesToc/children, recursing into
articles) are its sections.
"""
from __future__ import annotations

import json
import re
from urllib.parse import parse_qs, urlencode, urlparse

from . import base

API = "https://api.municode.com"
H = ["Accept: application/json"]


def parse_ref(ref):
    u = urlparse(ref)
    parts = [p for p in u.path.split("/") if p]
    return parts[0], parts[1], parts[3] if len(parts) > 3 else None, parse_qs(u.query).get("nodeId", [None])[0]


class Adapter(base.Adapter):
    name = "municode"
    hosts = ("library.municode.com", "api.municode.com")
    SMOKE = {"ref": "https://library.municode.com/wa/seattle/codes/municipal_code?nodeId=TIT7COPR_CH7.24REAGRE_7.24.035SEDENOMOFE",
             "expect": "security deposit", "label": "Seattle Municipal Code 7.24.035 (security deposits and move-in fees)"}

    def api(self, path, **params):
        url = API + path + ("?" + urlencode(params) if params else "")

        def ok(b):
            try:
                json.loads(b)
                return True
            except ValueError:
                return False
        return json.loads(base.fetch(self.name, url, ok, routes=("curl", "archive"), headers=H).body)

    def product(self, st, slug, prod_slug):
        cl = next((c for c in self.api("/Clients/stateAbbr", stateAbbr=st.upper())
                   if c["ClientName"].lower().replace(" ", "_") == slug.lower()), None)
        if not cl:
            raise base.core.PipelineError(f"{self.name}: no municode client {slug} in {st}")
        codes = self.api(f"/ClientContent/{cl['ClientID']}")["codes"]
        code = next((c for c in codes if prod_slug and c["productName"].lower().replace(" ", "_") == prod_slug.lower()), codes[0])
        job = self.api(f"/Jobs/latest/{code['productId']}")
        return code["productId"], job["Id"], job.get("Name")

    def section(self, ref):
        st, slug, prod_slug, node = parse_ref(ref)
        pid, jid, jname = self.product(st, slug, prod_slug)
        cur = node
        for _ in range(8):
            d = self.api("/CodesContent", jobId=jid, nodeId=cur, productId=pid)
            doc = next((x for x in d.get("Docs") or [] if x["Id"] == node), None)
            if doc:
                text = (doc.get("Title") or "") + "\n\n" + base.html_to_text(doc.get("Content") or "")
                return {"text": text, "source_url": ref, "route": "curl (municode API)",
                        "extra": {"publication": f"municode job {jid} ({jname}), product {pid}"}}
            nxt = d.get("NextNode")
            if not nxt:
                break
            cur = nxt["Id"] if isinstance(nxt, dict) else nxt
        raise base.core.PipelineError(f"{self.name}: node {node} not found in CodesContent (routes curl, archive)")

    def toc(self, instrument, unit):
        st, slug, prod_slug, node = parse_ref(unit["toc_url"])
        if not node:
            raise base.core.PipelineError("municode: toc_url needs the selected unit's nodeId, not the code root")
        pid, jid, _ = self.product(st, slug, prod_slug)
        root = unit["toc_url"].split("?")[0]
        out, todo = [], [node]
        while todo:
            for ch in self.api("/codesToc/children", jobId=jid, nodeId=todo.pop(0), productId=pid):
                if ch.get("HasChildren"):
                    todo.append(ch["Id"])
                    continue
                num, _, head = ch["Heading"].partition(" - ")
                out.append({"number": num.strip(), "heading": head.strip().rstrip("."), "ref": f"{root}?nodeId={ch['Id']}"})
        return out
