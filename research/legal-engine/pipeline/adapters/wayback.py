"""The Internet Archive (web.archive.org) as a source route for any official page no live route reaches.

ref: the official page URL (the closest capture is used) or a capture URL (https://web.archive.org/web/<ts>id_/URL).
Section text: the capture's text (HTML converted mechanically, PDF by pdftotext). The header's SOURCE is the official
URL and CAPTURE the capture read, so the text's date is visible.
"""
from __future__ import annotations

import re

from . import base
from . import native

CAP = re.compile(r"https?://web\.archive\.org/web/(\d{14})(?:id_)?/(.+)$")


class Adapter(base.Adapter):
    name = "wayback"
    hosts = ("web.archive.org",)
    SMOKE = {"ref": "https://www.azleg.gov/ars/33/01321.htm", "expect": "one and one-half month's rent",
             "label": "A.R.S. 33-1321 (Internet Archive capture of the official page)"}

    def section(self, ref):
        m = CAP.match(ref)
        if m:
            ts, orig = m.group(1), m.group(2)
            cap = f"https://web.archive.org/web/{ts}id_/{orig}"
        else:
            orig = ref
            probe, status, final = base.curl(f"https://web.archive.org/web/2026id_/{ref}", binary=True)
            cm = re.search(r"/web/(\d{14})id_/", final or "")
            if status != 200 or not cm:
                raise base.core.PipelineError(f"{self.name}: no capture of {ref} (archive {status})")
            cap = f"https://web.archive.org/web/{cm.group(1)}id_/{ref}"
        raw, status, final = base.curl(cap, binary=True)
        if status != 200 or not raw:
            raise base.core.PipelineError(f"{self.name}: capture {cap} returned {status}")
        if raw[:5] == b"%PDF-":
            text = base.pdf_text(raw)
        else:
            converted = native.convert(raw, orig)
            if converted:
                text, converter = converted
            else:
                h = raw.decode("utf-8", "strict")
                b = re.search(r"(?is)<body[^>]*>(.*)</body>", h)
                text = base.html_to_text(b.group(1) if b else h)
        if len(text.strip()) < 40:
            raise base.core.PipelineError(f"{self.name}: capture {cap} has no text")
        extra = {"capture": cap}
        if raw[:5] == b"%PDF-":
            extra["source_format"] = "pdf"
        if raw[:5] != b"%PDF-" and converted:
            extra["conversion"] = converter
        return {"text": text, "source_url": orig, "route": "archive", "extra": extra}
