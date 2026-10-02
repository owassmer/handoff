"""The publisher record is a download resolver, never the acquired form."""
import pytest

from pipeline import core
from pipeline.adapters import base, ca_court_forms, generic, usc_court_forms


def test_record_selects_its_form_not_neighbor_or_translation(monkeypatch):
    record = 'https://selfhelp.courts.ca.gov/jcc-form/GC-400(A)(4)'
    html = '''<main><a href="/help">How to use this form</a>
    <a href="https://courts.ca.gov/system/files/neighbor.pdf">Get form GC-400(A)(5)</a>
    <a href="https://courts.ca.gov/system/files/spanish.pdf">Get form GC-400(A)(4) S</a>
    <a href="https://courts.ca.gov/system/files/actual.pdf"><span>Get form</span> GC-400(A)(4)</a></main>'''
    monkeypatch.setattr(base, 'fetch', lambda name, url, ok: base.Fetched(html, 'fixture', url))
    seen = []
    def fetch_pdf(self, ref):
        seen.append(ref)
        return {'text': 'Acquired PDF body', 'source_url': ref, 'route': 'fixture',
                'extra': {'source_format': 'pdf'}}
    monkeypatch.setattr(generic.Adapter, 'section', fetch_pdf)
    result = ca_court_forms.Adapter().section(record)
    assert seen == ['https://courts.ca.gov/system/files/actual.pdf']
    assert result['text'] == 'Acquired PDF body'
    assert result['extra']['form_record_url'] == record


@pytest.mark.parametrize('html', [
    '<a href="help">Instructions for WG-002</a>',
    '<a href="a.pdf">Get form WG-002</a><a href="b.pdf">Get form WG-002</a>',
])
def test_missing_or_conflicting_download_is_not_guessed(html):
    with pytest.raises(core.PipelineError, match='expected one'):
        ca_court_forms.download_link(html, 'https://selfhelp.courts.ca.gov/jcc-form/WG-002')


def test_pdf_url_returning_html_is_not_saved_as_form(monkeypatch):
    monkeypatch.setattr(generic.Adapter, 'section', lambda *a: {
        'text': 'Please use the viewer to download the form.', 'source_url': 'form.pdf',
        'route': 'browser', 'extra': {}})
    with pytest.raises(core.PipelineError, match='did not produce PDF'):
        ca_court_forms.Adapter().section('https://courts.ca.gov/system/files/form.pdf')


def test_language_variant_never_falls_back_to_english():
    ref = 'https://selfhelp.courts.ca.gov/jcc-form/UD-105#language=Spanish'
    english = '<a href="en.pdf">Get form UD-105</a>'
    spanish = '<a href="es.pdf">Get form UD-105 in Spanish</a>'
    assert ca_court_forms.download_link(english + spanish, ref).endswith('/es.pdf')
    with pytest.raises(core.PipelineError):
        ca_court_forms.download_link(english, ref)


def test_national_primary_form_is_not_notes_or_instructions():
    html = '''<main><h1>Voluntary Petition</h1><a href="form.pdf">Download pdf, 1 MB</a>
    <div>Form Number</div><div>B101</div><h2>Committee Notes</h2>
    <a href="notes.pdf">Download pdf, 12 KB</a><h2>Form Instructions</h2>
    <a href="instructions.pdf">Download pdf, 50 KB</a></main>'''
    url = 'https://www.uscourts.gov/forms-rules/forms/voluntary-petition'
    assert usc_court_forms.download_link(html, url).endswith('/form.pdf')
    with pytest.raises(core.PipelineError):
        usc_court_forms.download_link(html.replace('Form Number', 'Changed publisher layout'), url)
