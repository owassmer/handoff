"""Pinned official USLM XML/ZIP and explicit USLM structural identifiers.

Each unit supplies toc_url (official XML or release ZIP) and uslm_identifier
(for example /us/usc/t11/ch1), or its source-grounded uslm_parent_heading.
Legacy child-unit grouping additionally supplies uslm_unit_depth.
Section refs append the exact section identifier read from XML.
The legacy XML parser is reused, retaining source credits and statutory notes.
"""
import io
from urllib.parse import quote, unquote, urldefrag, urlparse
import zipfile
import xml.etree.ElementTree as ET

from register.tools.usc import parse_xml
from . import base


def read(url):
    parsed = urlparse(url)
    if (parsed.hostname != "uscode.house.gov" or "/download/releasepoints/" not in parsed.path
            or not parsed.path.endswith((".zip", ".xml"))):
        raise base.core.PipelineError("usc: toc_url must be pinned to an official USLM release-point XML or ZIP")
    cache = base.cache_dir("usc") / (base._key(url) + ".bin")
    if cache.exists() and not base.REFRESH["on"]:
        raw = cache.read_bytes()
    else:
        raw, status, _ = base.curl(url, binary=True)
        if status != 200:
            raise base.core.PipelineError(f"usc: USLM download failed (curl {status}); resolve the source route")
    try:
        if urlparse(url).path.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                members = [n for n in archive.namelist() if n.lower().endswith(".xml")]
                if len(members) != 1:
                    raise base.core.PipelineError("usc: expected a single-title ZIP with exactly one XML member")
                xml = archive.read(members[0])
        else:
            xml = raw
        sections = parse_xml(xml, include_notes=True)
    except (zipfile.BadZipFile, ET.ParseError) as exc:
        raise base.core.PipelineError(f"usc: invalid USLM source at {url}: {exc}") from exc
    if not sections:
        raise base.core.PipelineError(f"usc: no sections in USLM source {url}")
    cache.write_bytes(raw)
    return sections


class Adapter(base.Adapter):
    name = "usc"
    hosts = ()

    def __init__(self):
        self._titles = {}

    def read(self, url):
        if url not in self._titles or base.REFRESH["on"]:
            self._titles[url] = read(url)
        return self._titles[url]

    def toc(self, instrument, unit):
        url = unit["toc_url"]
        prefix = unit.get("uslm_identifier", "").rstrip("/")
        sections = self.read(url)
        if prefix:
            if not prefix.startswith("/us/"):
                raise base.core.PipelineError("usc: selected unit needs its exact uslm_identifier")
            sections = [s for s in sections if s["identifier"] == prefix or prefix in s["ancestors"]]
        elif unit.get("uslm_parent_heading"):
            # Preserve the grouping used by register/tools/build.py for existing named units.
            selected = []
            for s in sections:
                index = next((n for n, p in enumerate(s["path"]) if unit["uslm_parent_heading"] in p), None)
                if index is None:
                    continue
                depth = unit.get("uslm_unit_depth")
                if depth is None:
                    selected.append(s)
                    continue
                if not isinstance(depth, int) or depth < 0:
                    raise base.core.PipelineError("usc: uslm_unit_depth must be a nonnegative integer")
                rest = s["path"][index + 1:index + 1 + depth]
                label = " > ".join(rest) if rest else f"(sections directly under {s['path'][index][:60]})"
                if depth == 0:
                    label = f"section {s['number']}"
                if label == unit["unit"]:
                    selected.append(s)
            sections = selected
        else:
            raise base.core.PipelineError("usc: selected unit needs uslm_identifier or its recorded parent heading/unit depth")
        return [{"number": s["number"], "heading": s["heading"],
                 "ref": url + "#" + quote(s["identifier"], safe="/")}
                for s in sections]

    def section(self, ref):
        url, ident = urldefrag(ref)
        selected = [s for s in self.read(url) if s["identifier"] == unquote(ident)]
        if len(selected) != 1:
            raise base.core.PipelineError(f"usc: ref must identify exactly one USLM section, got {len(selected)}")
        return {"text": selected[0]["text"], "source_url": ref, "route": "curl (USLM XML)",
                "extra": {"publication": url, "element": selected[0]["identifier"]}}
