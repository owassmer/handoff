"""Any other official page or PDF (city ordinance PDFs, session laws, bill text): the fallback adapter.

ref: the URL. Routes: curl, then the headless browser (HTML), then the Internet Archive. HTML is converted to text
mechanically (the <main> element when the page has one, else <body>); a PDF is converted by pdftotext -layout.
"""
from __future__ import annotations

import re
from pathlib import PurePosixPath
from urllib.parse import urlsplit

from . import base
from . import native
from .wayback import Adapter as Wayback


def html_text(h):
    m = re.search(r"(?is)<main\b[^>]*>(.*?)</main>", h) or re.search(r"(?is)<body[^>]*>(.*)</body>", h)
    return base.html_to_text(m.group(1) if m else h)


class Adapter(base.Adapter):
    name = "generic"
    hosts = ()
    SMOKE = {"ref": "https://docs.sandiego.gov/municode/MuniCodeChapter09/Ch09Art08Division07.pdf",
             "expect": "tenant", "label": "San Diego Municipal Code ch. 9 art. 8 div. 7 (official PDF)"}

    def section(self, ref):
        cf = base.cache_dir(self.name) / (base._key(ref) + ".bin")
        tried = []
        raw = cf.read_bytes() if cf.exists() and not base.REFRESH["on"] else None
        route = "curl"
        if raw is None:
            raw, status, _ = base.curl(ref, binary=True)
            tried.append(f"curl {status}")
            if status != 200 or base.challenged(raw[:5000].decode("utf-8", "replace")):
                raw = None
        if raw is not None and raw[:5] == b"%PDF-":
            cf.write_bytes(raw)
            text = base.pdf_text(raw)
            if len(text.strip()) >= 40:
                return {"text": text, "source_url": ref, "route": "curl (pdftotext)", "extra": {"source_format": "pdf"}}
            tried.append("pdftotext empty")
        elif raw is not None:
            converted = native.convert(raw, ref)
            cf.write_bytes(raw)
            if converted:
                text, converter = converted
                if not text.strip():
                    raise base.core.PipelineError(f"generic: native conversion produced no text at {ref}")
                return {"text": text, "source_url": ref, "route": "curl (" + converter + ")", "extra": {"conversion": converter}}
            text = html_text(raw.decode("utf-8", "strict"))
            if len(text.strip()) >= 40:
                return {"text": text, "source_url": ref, "route": route, "extra": {}}
        if PurePosixPath(urlsplit(ref).path).suffix.lower() in (".doc", ".docx", ".xls", ".rtf"):
            # A browser's download/viewer page is not the requested document.
            return Wayback().section(ref)
        d = base.browser(ref)
        tried.append("browser " + ("ok" if d else "failed"))
        if d and not base.challenged(d["html"]):
            text = html_text(d["html"])
            if len(text.strip()) >= 40:
                return {"text": text, "source_url": ref, "route": "browser", "extra": {}}
        try:
            return Wayback().section(ref)
        except base.core.PipelineError as e:
            tried.append(f"archive: {e}")
        raise base.core.PipelineError(f"{self.name}: every route failed for {ref} ({'; '.join(tried)})")
