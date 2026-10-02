"""Enumerate a selected CCR hierarchy on Cornell's convenience mirror.

This route establishes mirror acquisition, not authoritative text or currentness.
"""
from urllib.parse import urljoin, urlsplit, urlunsplit
import re

from . import base
from .generic import Adapter as Generic


class Adapter(base.Adapter):
    name = "cornell_ccr"
    hosts = ()

    def toc(self, instrument, unit):
        root = unit.get("toc_url", "").rstrip("/")
        parsed = urlsplit(root)
        match = re.fullmatch(r"/regulations/california/title-(\d+)/(?:division|chapter|part|subchapter|article)-[^/]+(?:/[^/]+)*", parsed.path)
        if parsed.hostname != "www.law.cornell.edu" or parsed.scheme != "https" or not match or parsed.query or parsed.fragment:
            raise base.core.PipelineError("cornell_ccr requires a selected division or narrower hierarchy URL")
        title = match.group(1)
        leaf = re.compile(rf"/regulations/california/{title}-CCR-(.+)")
        seen, entries = set(), {}

        def walk(url):
            if url in seen:
                return
            seen.add(url)
            fetched = base.fetch(self.name, url, lambda h: bool(base.links(h, "/regulations/california/")))
            children = set()
            for href, heading in base.links(fetched.body, ""):
                p = urlsplit(urljoin(url, href))
                if p.hostname != parsed.hostname or p.scheme != "https":
                    continue
                target = urlunsplit((p.scheme, p.netloc, p.path.rstrip("/"), "", ""))
                m = leaf.fullmatch(p.path)
                if m:
                    children.add(target)
                    entries.setdefault(target, {"number": m.group(1), "heading": heading, "ref": target,
                                                "source_authority": "mirror"})
                elif p.path.startswith(urlsplit(url).path.rstrip("/") + "/"):
                    children.add(target)
                    walk(target)
            if not children:
                raise base.core.PipelineError(f"cornell_ccr: no legal descendants found at {url}")

        walk(root)
        if not entries:
            raise base.core.PipelineError(f"cornell_ccr: no section leaves found at {root}")
        return list(entries.values())

    def section(self, ref):
        if not re.fullmatch(r"https://www\.law\.cornell\.edu/regulations/california/\d+-CCR-[^/?#]+", ref):
            raise base.core.PipelineError(f"cornell_ccr: expected section leaf, got {ref}")
        result = Generic().section(ref)
        result.setdefault("extra", {})["source_status"] = "Cornell convenience mirror; official text and currentness require separate reconciliation"
        return result
