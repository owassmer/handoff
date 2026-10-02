"""Read official Laserfiche WebLink document pages through its observed JSON services.

References are DocView.aspx URLs. An optional #pages=30-43 limits a registered
unit to those document pages. Empty OCR is an acquisition failure, never viewer text.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlsplit, urlunsplit

from . import base


class Adapter(base.Adapter):
    name = "laserfiche"
    hosts = ("records.huntingtonbeachca.gov",)

    def _request(self, url, cookies, payload=None):
        cmd = ["curl", "-fsSL", "--max-time", "45", "-A", base.UA,
               "-c", str(cookies), "-b", str(cookies), url]
        if payload is not None:
            cmd += ["-H", "Content-Type: application/json", "--data", json.dumps(payload)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:
            raise base.core.PipelineError(f"laserfiche: request failed at {url}: {result.stderr.strip()}")
        if payload is None:
            return result.stdout
        try:
            data = json.loads(result.stdout)["data"]
        except (ValueError, KeyError, TypeError) as exc:
            raise base.core.PipelineError(f"laserfiche: expected document-service JSON at {url}") from exc
        return data

    def section(self, ref):
        parsed = urlsplit(ref)
        query = {k.lower(): v for k, v in parse_qs(parsed.query).items()}
        try:
            document_id = int(query["id"][0])
            repo = query["repo"][0]
        except (KeyError, ValueError, IndexError) as exc:
            raise base.core.PipelineError("laserfiche: DocView reference requires id and repo") from exc
        if parsed.hostname not in self.hosts or parsed.path.rsplit("/", 1)[-1].lower() != "docview.aspx":
            raise base.core.PipelineError("laserfiche: unsupported publisher/document route")
        root = urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rsplit("/", 1)[0] + "/", "", ""))
        cache = base.cache_dir(self.name) / (base._key(ref) + ".json")
        if cache.exists() and not base.REFRESH["on"]:
            return json.loads(cache.read_text())
        with tempfile.TemporaryDirectory(prefix="handoff-laserfiche-") as temp:
            cookies = Path(temp) / "cookies"
            self._request(root + "Welcome.aspx", cookies)
            info = self._request(root + "DocumentService.aspx/GetBasicDocumentInfo", cookies,
                                 {"repoName": repo, "entryId": document_id})
            if not isinstance(info, dict) or info.get("id") != document_id or not isinstance(info.get("pageCount"), int) or info["pageCount"] < 1:
                raise base.core.PipelineError("laserfiche: invalid or mismatched document metadata")
            start, end = 1, info["pageCount"]
            if parsed.fragment:
                try:
                    selection = parse_qs(parsed.fragment)["pages"][0].split("-")
                    start = int(selection[0])
                    end = int(selection[-1])
                    if len(selection) > 2 or not 1 <= start <= end <= info["pageCount"]:
                        raise ValueError()
                except (KeyError, IndexError, ValueError) as exc:
                    raise base.core.PipelineError("laserfiche: invalid page selection") from exc
            pages = []
            for number in range(start, end + 1):
                data = self._request(root + "DocumentService.aspx/GetTextHtmlForPage", cookies,
                    {"repoName": repo, "documentId": document_id, "pageNum": number,
                     "showAnn": False, "searchUuid": ""})
                text = data.get("text") if isinstance(data, dict) else None
                if not isinstance(text, str) or not text.strip():
                    raise base.core.PipelineError(f"laserfiche: document {document_id} page {number} has no OCR; retrieve its image before accepting the unit")
                pages.append({"page": number, "text": text})
        result = {"text": "\n\f\n".join(page["text"] for page in pages), "source_url": ref,
                  "route": "Laserfiche official document-service OCR",
                  "extra": {"document_id": document_id, "repository": repo, "document_page_count": info["pageCount"],
                            "page_start": start, "page_end": end, "document_name": info.get("name"),
                            "source_format": "publisher_ocr", "pages": pages}}
        cache.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        return result
