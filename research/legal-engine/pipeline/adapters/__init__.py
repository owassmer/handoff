"""Fetch adapters, one per host. instruments.json names each instrument's adapter by NAME.

get(name) returns an adapter instance; for_url(url) picks the adapter whose hosts include the URL's host (falling
back to 'wayback' for web.archive.org and 'generic' for any other host). Every adapter's section() tries its routes in
order (base.fetch: curl, headless browser with network capture, Internet Archive, a page saved by Ferro with
browser_exec) and reports the route that worked.
"""
from __future__ import annotations

import importlib
from urllib.parse import urlparse

MODULES = {
    "sharepoint": "sharepoint",
    "laserfiche": "laserfiche",
    "ca_court_forms": "ca_court_forms",
    "usc_court_forms": "usc_court_forms",
    "cornell_ccr": "cornell_ccr",
    "usc": "usc",
    "ecfr": "ecfr",
    "newyork_public_law": "newyork_public_law",
    "nysenate_archive": "nysenate_archive",
    "ca_leginfo": "ca_leginfo",
    "wa_rcw": "wa_rcw",
    "co_olls": "co_olls",
    "or_ors": "or_ors",
    "az_ars": "az_ars",
    "municode": "municode",
    "amlegal": "amlegal",
    "municipal_codes": "municipal_codes",
    "ecode360": "ecode360",
    "portland_code": "portland_code",
    "wayback": "wayback",
    "generic": "generic",
}
NAMES = set(MODULES)
_INST = {}


def get(name):
    if name not in MODULES:
        raise KeyError(f"no adapter {name!r} (have {sorted(MODULES)})")
    if name not in _INST:
        _INST[name] = importlib.import_module(f"{__name__}.{MODULES[name]}").Adapter()
    return _INST[name]


def for_url(url):
    host = (urlparse(url).hostname or "").lower()
    for n in MODULES:
        if n in ("wayback", "generic"):
            continue
        a = get(n)
        if any(host == h or (h.startswith(".") and host.endswith(h)) for h in a.hosts):
            return a
    return get("wayback") if host == "web.archive.org" else get("generic")
