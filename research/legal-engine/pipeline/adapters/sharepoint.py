"""Published SharePoint PDFs reached through a public folder share link.

ref = observed share URL + #document=<URL-encoded server-relative PDF path>.
The document path comes from publisher Files metadata, never a guessed filename.
"""
from __future__ import annotations

import base64
import json
import pathlib
import subprocess
from email import policy
from email.parser import BytesParser
from urllib.parse import parse_qs, quote, unquote, urlsplit, urlunsplit

from . import base


def parse_ref(ref):
    parsed = urlsplit(ref)
    paths = parse_qs(parsed.fragment).get("document", [])
    if (parsed.scheme != "https" or not (parsed.hostname or "").endswith(".sharepoint.com")
            or len(paths) != 1):
        raise base.core.PipelineError("sharepoint: expected public share URL with one document fragment")
    path = paths[0]
    if not path.startswith("/teams/") or path.startswith("//") or not path.lower().endswith(".pdf"):
        raise base.core.PipelineError("sharepoint: expected observed server-relative PDF path")
    share = urlunsplit(parsed._replace(fragment=""))
    document = f"https://{parsed.netloc}" + quote(path, safe="/")
    return share, path, document


def pdf_payload(raw, expected_name):
    if raw.startswith(b"%PDF-"):
        return raw
    # The publisher can label a form-data envelope application/pdf. Parse its
    # actual boundary and filename; do not search arbitrary response bytes for PDF magic.
    first, sep, _ = raw.partition(b"\r\n")
    if not sep or not first.startswith(b"--") or len(first) > 200:
        raise base.core.PipelineError("sharepoint: response is not PDF or multipart PDF")
    boundary = first[2:]
    if not boundary or b'"' in boundary or b"\n" in boundary:
        raise base.core.PipelineError("sharepoint: invalid multipart boundary")
    message = BytesParser(policy=policy.default).parsebytes(
        b'Content-Type: multipart/form-data; boundary="' + boundary + b'"\r\nMIME-Version: 1.0\r\n\r\n' + raw)
    matches = [part for part in message.iter_parts()
               if part.get_content_type() == "application/pdf"
               and part.get_filename() == expected_name]
    if len(matches) != 1:
        raise base.core.PipelineError("sharepoint: response has no unique requested PDF filename")
    part = matches[0]
    data = part.get_payload(decode=True)
    declared = part.get("Content-Length")
    if (not data or not data.startswith(b"%PDF-")
            or (declared and (not declared.isdigit() or int(declared) != len(data)))):
        raise base.core.PipelineError("sharepoint: invalid or truncated requested PDF part")
    return data


class Adapter(base.Adapter):
    name = "sharepoint"
    hosts = ()  # Explicit selection: unrelated SharePoint URLs have no folder-share mapping.

    def section(self, ref):
        share, path, source = parse_ref(ref)
        cache = base.cache_dir(self.name) / (base._key(ref) + ".pdf")
        if cache.exists() and not base.REFRESH["on"]:
            raw = pdf_payload(cache.read_bytes(), pathlib.PurePosixPath(path).name)
            route = "cache (public SharePoint PDF)"
        else:
            helper = pathlib.Path(__file__).with_name("sharepoint_fetch.py")
            try:
                run = subprocess.run([str(base.core.VENV_PYTHON), str(helper)],
                                     input=json.dumps({"share_url": share, "document_path": path}),
                                     text=True, capture_output=True, timeout=120)
            except subprocess.TimeoutExpired as exc:
                raise base.core.PipelineError("sharepoint: public browser fetch timed out") from exc
            if run.returncode:
                raise base.core.PipelineError("sharepoint: public browser fetch failed: " + run.stderr[-600:])
            result = json.loads(run.stdout)
            actual = urlsplit(result["url"])
            wanted = urlsplit(source)
            if (result["status"] != 200 or actual.hostname != wanted.hostname
                    or unquote(actual.path) != unquote(wanted.path)):
                raise base.core.PipelineError("sharepoint: requested public PDF did not return successfully")
            raw = pdf_payload(base64.b64decode(result["body"], validate=True), pathlib.PurePosixPath(path).name)
            cache.write_bytes(raw)
            route = "browser (public SharePoint share; PDF)"
        text = base.pdf_text(raw)
        if len(text.strip()) < 40:
            raise base.core.PipelineError("sharepoint: PDF requires OCR; no legal text extracted")
        return {"text": text, "source_url": source, "route": route,
                "extra": {"source_format": "pdf", "public_share_url": share}}
