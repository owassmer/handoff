"""Resolve a Judicial Council form record to its own published download.

Explicit PDF references remain supported. A form record's explanatory HTML is
never returned as the form. Edition reconciliation remains part of J2.
"""
from __future__ import annotations

import re
from urllib.parse import parse_qs, unquote, urldefrag, urljoin, urlsplit

from . import base
from .generic import Adapter as Generic


def download_link(html, record_url):
    selector = parse_qs(urlsplit(record_url).fragment)
    languages = selector.get('language', [])
    if len(languages) > 1 or set(selector) - {'language'}:
        raise base.core.PipelineError('ca_court_forms: invalid language selector')
    language = languages[0] if languages else None
    form_id = unquote(urlsplit(record_url).path.rstrip('/').rsplit('/', 1)[-1])
    normalize = lambda value: re.sub(r'\s+', '', value).upper()
    matches = set()
    for href, label in base.links(html, r'.'):
        match = re.fullmatch(r'Get\s+form\s+(.+)', label, re.I)
        labels = [form_id] if not language else [f'{form_id} in {language}', f'{form_id} ({language})']
        if match and normalize(match[1]) in {normalize(value) for value in labels}:
            target = urljoin(record_url, href)
            if urlsplit(target).scheme in ('http', 'https'):
                matches.add(target)
    if len(matches) != 1:
        raise base.core.PipelineError(
            f'ca_court_forms: expected one Get form {form_id} download at {record_url}; found {len(matches)}')
    return matches.pop()


class Adapter(base.Adapter):
    name = 'ca_court_forms'
    hosts = ()  # Explicit register selection; other court pages use their own adapters.

    def section(self, ref):
        parsed = urlsplit(ref)
        record = parsed.hostname == 'selfhelp.courts.ca.gov' and parsed.path.startswith('/jcc-form/')
        target, record_fetch = ref, None
        if record:
            def has_download(html):
                try:
                    download_link(html, ref)
                    return True
                except base.core.PipelineError:
                    return False
            record_fetch = base.fetch(self.name, urldefrag(ref)[0], has_download)
            target = download_link(record_fetch.body, ref)
        result = Generic().section(target)
        if result.get('extra', {}).get('source_format') != 'pdf':
            raise base.core.PipelineError(
                f'ca_court_forms: {target} did not produce PDF text; guidance or viewer HTML is not a form')
        if record_fetch:
            result['extra'].update(form_record_url=ref, form_record_route=record_fetch.route)
            if record_fetch.capture:
                result['extra']['form_record_capture'] = record_fetch.capture
        return result
