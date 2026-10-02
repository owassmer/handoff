"""Fetch routes shared by every adapter. Access problems are never blockers: fetch() tries each route in order until
the page passes the adapter's check, and reports the route that worked.

Routes:
  curl      plain HTTPS with a browser user agent (system curl, which handles TLS and redirects)
  browser   the page rendered in headless Chrome by Playwright (research/legal-engine/.venv), with automation
            flags off; waits for a selector when given; can also return the page's own network responses (JSON
            API calls the page makes) instead of the HTML
  archive   the closest Internet Archive capture (web.archive.org/web/2026id_/URL), with the capture URL recorded
  manual    Ferro renders the page with browser_exec and saves its HTML under .cache/adapters/manual/; the adapter
            parses that file (fetch() looks there last)
Raw responses are cached under research/legal-engine/.cache/adapters/<adapter>/ (outside the scratch folder, which
is pruned). A saved section text is never refetched by harvest.
"""
from __future__ import annotations

import hashlib
import html as htmlmod
import json
import pathlib
import re
import subprocess
import time

from .. import core

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
RUNNER = pathlib.Path(__file__).with_name("browser_render.py")
REFRESH = {"on": False}  # diff sets this: every fetch bypasses the response cache
CHALLENGE = ("Just a moment", "cf-chl", "Attention Required", "challenge-platform")


def cache_dir(name):
    d = core.PKG.parent / ".cache" / "adapters" / name
    d.mkdir(parents=True, exist_ok=True)
    return d


class Fetched:
    def __init__(self, body, route, url, final_url=None, capture=None, status=None):
        self.body, self.route, self.url = body, route, url
        self.final_url, self.capture, self.status = final_url or url, capture, status

    def __bool__(self):
        return bool(self.body)


def _key(url, extra=""):
    return hashlib.sha256((url + "|" + extra).encode()).hexdigest()[:24]


def curl(url, timeout=90, binary=False, headers=None):
    cmd = ["curl", "-sL", "--compressed", "--max-time", str(timeout), "-A", UA, "-w", "\n%{http_code} %{url_effective}"]
    for h in headers or []:
        cmd += ["-H", h]
    r = subprocess.run(cmd + [url], capture_output=True)
    out = r.stdout
    body, _, tail = out.rpartition(b"\n")
    parts = tail.decode("utf-8", "replace").split(" ", 1)
    status = int(parts[0]) if parts and parts[0].isdigit() else 0
    final = parts[1] if len(parts) > 1 else url
    return (body if binary else body.decode("utf-8", "replace")), status, final


def challenged(body):
    return any(c in (body or "")[:5000] for c in CHALLENGE)


def browser(url, wait_for=None, capture=None, timeout=60):
    """Render url in headless Chrome. capture: regex; returns JSON list of {url, body} for matching responses."""
    py = core.VENV_PYTHON
    if not py.exists():
        return None
    cmd = [str(py), str(RUNNER), url, "--timeout", str(timeout)]
    if wait_for:
        cmd += ["--wait-for", wait_for]
    if capture:
        cmd += ["--capture", capture]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 60)
    except subprocess.TimeoutExpired:
        return None
    if r.returncode != 0:
        return None
    return json.loads(r.stdout.decode("utf-8", "replace"))


def archive(url, timeout=90):
    body, status, final = curl(f"https://web.archive.org/web/2026id_/{url}", timeout)
    if status == 200 and re.search(r"/web/\d{14}id_/", final):
        return body, final
    return None, None


def fetch(name, url, ok, routes=("curl", "browser", "archive", "manual"), wait_for=None, capture=None, refresh=False,
          encoding=None, headers=None):
    """Fetch url by the first route whose body passes ok(body). Caches the winning body; returns Fetched or raises.
    encoding: decode the curl body with this codec (Word-exported pages are windows-1252)."""
    refresh = refresh or REFRESH["on"]
    cdir = cache_dir(name)
    cf = cdir / f"{_key(url, capture or '')}.json"
    if cf.exists() and not refresh:
        d = json.loads(cf.read_text())
        return Fetched(d["body"], d["route"], url, d.get("final_url"), d.get("capture"), d.get("status"))
    tried = []
    for route in routes:
        res = None
        if route == "curl":
            if encoding:
                raw, status, final = curl(url, binary=True, headers=headers)
                body = raw.decode(encoding, "replace")
            else:
                body, status, final = curl(url, headers=headers)
            tried.append(f"curl {status}")
            if status == 200 and not challenged(body) and ok(body):
                res = Fetched(body, "curl", url, final, status=status)
        elif route == "browser":
            d = browser(url, wait_for=wait_for, capture=capture)
            tried.append("browser " + ("ok" if d else "failed"))
            if d:
                body = json.dumps(d["responses"]) if capture else d["html"]
                if not challenged(d.get("html", "")) and ok(body):
                    res = Fetched(body, "browser" + (" (network capture)" if capture else ""), url, d.get("url"))
        elif route == "archive":
            body, cap = archive(url)
            tried.append("archive " + ("ok" if body else "no capture"))
            if body and ok(body):
                res = Fetched(body, "archive", url, cap, capture=cap)
        elif route == "manual":
            mf = cache_dir("manual") / f"{_key(url)}.html"
            tried.append("manual " + ("file" if mf.exists() else "none"))
            if mf.exists() and ok(mf.read_text(errors="replace")):
                res = Fetched(mf.read_text(errors="replace"), "manual (browser_exec)", url)
        if res:
            cf.write_text(json.dumps({"body": res.body, "route": res.route, "final_url": res.final_url,
                                      "capture": res.capture, "status": res.status, "tried": tried,
                                      "at": core.now()}))
            return res
        time.sleep(0.3)
    raise core.PipelineError(f"{name}: every route failed for {url} ({'; '.join(tried)}); save the page with "
                             f"browser_exec to {core.rel(cache_dir('manual') / (_key(url) + '.html'))} and rerun")


def manual_path(url):
    return cache_dir("manual") / f"{_key(url)}.html"


def html_to_text(h, block_tags=("p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section",
                                 "blockquote", "pre", "table", "dd", "dt")):
    """Mechanical HTML to text: scripts and styles dropped, one line per block element, whitespace collapsed."""
    h = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", h or "")
    h = re.sub(r"(?is)<!--.*?-->", " ", h)
    bt = "|".join(block_tags)
    h = re.sub(rf"(?i)<\s*/?\s*(?:{bt})\b[^>]*>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    t = htmlmod.unescape(h).replace("\xa0", " ").replace("­", "")
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def between(h, start_rx, end_rx=None):
    m = re.search(start_rx, h, re.S)
    if not m:
        return ""
    rest = h[m.start():]
    if end_rx:
        e = re.search(end_rx, rest[1:], re.S)
        if e:
            rest = rest[:e.start() + 1]
    return rest


class Adapter:
    """One host. Subclasses set name, hosts and SMOKE, and implement section(ref) and, where the host has one,
    toc(instrument, unit)."""
    name = "base"
    hosts = ()
    SMOKE = None  # {"ref": ..., "expect": "phrase in the text", "label": "what it is"}

    def section(self, ref):
        """Return {text, source_url, route, extra{}} for one section reference (usually its URL)."""
        raise NotImplementedError

    def toc(self, instrument, unit):
        """Return [{number, heading, ref}] for an in-scope unit."""
        raise core.PipelineError(f"{self.name}: no table-of-contents reader; list the unit's sections in "
                                 f"instruments.json units_in_scope[].section_list")

    def save(self, path, sec):
        extra = dict(sec.get("extra") or {})
        text = core.header(sec["source_url"], f"{sec['route']} of {self.name} (pipeline/adapters)", extra=extra) + \
            sec["text"].strip() + "\n"
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(path).write_text(text)
        return text


def pdf_text(raw, layout=True):
    """Text of a PDF (bytes) by pdftotext; '' when pdftotext is missing or fails."""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(raw)
        name = f.name
    try:
        r = subprocess.run(["pdftotext"] + (["-layout"] if layout else []) + [name, "-"], capture_output=True)
        return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""
    except FileNotFoundError:
        return ""
    finally:
        pathlib.Path(name).unlink()


def page(adapter, url, ok, extract, min_chars=40, **kw):
    """Fetch url by adapter's routes and extract its text; returns the section dict save() expects."""
    f = fetch(adapter.name, url, ok, **kw)
    text = extract(f.body)
    if len((text or "").strip()) < min_chars:
        raise core.PipelineError(f"{adapter.name}: no section text at {url} (route {f.route})")
    extra = {}
    if f.capture:
        extra["capture"] = f.capture
    return {"text": text, "source_url": url, "route": f.route, "extra": extra}


def links(h, rx):
    """[(href, anchor text)] for anchors whose href matches rx (text unescaped, tags removed, spaces collapsed)."""
    out = []
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', h, re.S | re.I):
        if re.search(rx, m.group(1)):
            out.append((htmlmod.unescape(m.group(1)), re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()))
    return out
