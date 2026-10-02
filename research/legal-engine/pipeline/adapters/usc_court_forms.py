"""Resolve the primary download on a national court form record.

The publisher places the form before 'Form Number', followed by any committee
notes and instructions. Those related sources require their own register entries.
"""
import re
from urllib.parse import urljoin, urlsplit

from . import base
from .generic import Adapter as Generic


def download_link(html, record_url):
    boundary = re.search(r'Form\s+Number', html, re.I)
    if not boundary:
        raise base.core.PipelineError(f'usc_court_forms: no Form Number field at {record_url}')
    selected = html[:boundary.start()]
    links = {urljoin(record_url, href) for href, label in base.links(selected, r'.')
             if re.fullmatch(r'Download\s+pdf(?:\s*,.*)?', label, re.I)}
    links = {url for url in links if urlsplit(url).scheme in ('http', 'https')}
    if len(links) != 1:
        raise base.core.PipelineError(f'usc_court_forms: expected one primary form PDF at {record_url}; found {len(links)}')
    return links.pop()


class Adapter(base.Adapter):
    name = 'usc_court_forms'
    hosts = ()

    def section(self, ref):
        parsed = urlsplit(ref)
        record = parsed.hostname == 'www.uscourts.gov' and parsed.path.startswith('/forms-rules/forms/')
        target, fetched = ref, None
        if record:
            def valid(html):
                try:
                    download_link(html, ref)
                    return True
                except base.core.PipelineError:
                    return False
            fetched = base.fetch(self.name, ref, valid)
            target = download_link(fetched.body, ref)
        result = Generic().section(target)
        if result.get('extra', {}).get('source_format') != 'pdf':
            raise base.core.PipelineError(f'usc_court_forms: {target} did not produce PDF text')
        if fetched:
            result['extra'].update(form_record_url=ref, form_record_route=fetched.route)
            if fetched.capture:
                result['extra']['form_record_capture'] = fetched.capture
        return result
