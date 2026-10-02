"""Dated eCFR XML units, using the existing register's section/appendix parser.

toc_url: https://www.ecfr.gov/api/versioner/v1/full/YYYY-MM-DD/title-N.xml?part=P
The API also accepts subpart/section filters. Refs add an exact section or appendix
selector; appendices retain their parent path because their letters can repeat.
"""
import re
from urllib.parse import parse_qs, urlencode, urldefrag, urlsplit
import xml.etree.ElementTree as ET

from register.tools.ecfr import parse_xml
from . import base


def read(url):
    if not re.match(r"https://www\.ecfr\.gov/api/versioner/v1/full/\d{4}-\d{2}-\d{2}/title-\d+\.xml\?", url):
        raise base.core.PipelineError("ecfr: use a dated full XML API URL with the selected part")
    if not parse_qs(urlsplit(url).query).get("part"):
        raise base.core.PipelineError("ecfr: select a part rather than enumerate an entire title implicitly")

    def valid(body):
        try:
            return bool(parse_xml(body, include_root=True))
        except ET.ParseError:
            return False

    fetched = base.fetch("ecfr", url, valid)
    return parse_xml(fetched.body, include_root=True), fetched


def entry_number(sec):
    if sec["type"] == "APPENDIX":
        return " > ".join([p.split(":", 1)[0] for p in sec["path"]] + [sec["number"]])
    return sec["number"]


class Adapter(base.Adapter):
    name = "ecfr"
    # Other eCFR URLs still use generic; this adapter requires an explicit date.
    hosts = ()

    def __init__(self):
        self._parts = {}

    def read(self, url):
        if url not in self._parts or base.REFRESH["on"]:
            self._parts[url] = read(url)
        return self._parts[url]

    def toc(self, instrument, unit):
        url = unit["toc_url"]
        sections, _ = self.read(url)
        return [{"number": entry_number(s), "heading": s["heading"],
                 "ref": url + "#" + urlencode({"type": s["type"], "number": s["number"],
                                                 "path": " > ".join(s["path"])})}
                for s in sections]

    def section(self, ref):
        url, fragment = urldefrag(ref)
        sections, fetched = self.read(url)
        if fragment:
            selector = parse_qs(fragment, keep_blank_values=True)
            sections = [s for s in sections if all(selector.get(k) == [v] for k, v in
                        {"type": s["type"], "number": s["number"], "path": " > ".join(s["path"])}.items())]
        if len(sections) != 1:
            raise base.core.PipelineError(f"ecfr: ref must identify exactly one section/appendix, got {len(sections)}")
        return {"text": sections[0]["text"], "source_url": ref, "route": fetched.route,
                "extra": {"publication": url, **({"capture": fetched.capture} if fetched.capture else {})}}
