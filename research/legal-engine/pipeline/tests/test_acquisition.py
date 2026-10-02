"""J1 route contracts and J2 enumeration safeguards, without network or live inventory writes."""
import io
import zipfile

import pytest

from pipeline import adapters, check, core, diff, harvest, match, triage
from pipeline.adapters import base, ca_leginfo, ecfr, ecode360, municode, usc
from register.tools import usc as usc_parser, ecfr as ecfr_parser

USLM = b'''<uslm xmlns="http://xml.house.gov/schemas/uslm/1.0"><main>
<title identifier="/us/usc/t11"><num>11</num><heading>BANKRUPTCY</heading>
<chapter identifier="/us/usc/t11/ch1"><num>1</num><heading>GENERAL PROVISIONS</heading>
<section identifier="/us/usc/t11/s101"><num>101</num><heading>Definitions</heading>
<content>The term debtor means the person subject to the proceeding.</content>
<sourceCredit>Pub. L. 95-598</sourceCredit><notes><note>Effective date is October 1.</note></notes></section>
</chapter><chapter identifier="/us/usc/t11/ch3"><num>3</num>
<section identifier="/us/usc/t11/s301"><num>301</num><heading>Voluntary cases</heading>
<content>A voluntary case begins with the filing of a petition.</content></section>
</chapter></title></main></uslm>'''

ECFR = '''<DIV5 TYPE="PART" N="1006"><HEAD>Part 1006</HEAD>
<DIV6 TYPE="SUBPART" N="A"><HEAD>General</HEAD><DIV8 TYPE="SECTION" N="1006.1">
<HEAD>Scope</HEAD><P>The regulation applies to debt collection.</P><CITA>Source: official amendment.</CITA></DIV8>
<DIV9 TYPE="APPENDIX" N="Appendix A"><HEAD>Appendix A to Subpart A</HEAD><P>First appendix.</P></DIV9></DIV6>
<DIV6 TYPE="SUBPART" N="B"><HEAD>Conduct</HEAD><DIV9 TYPE="APPENDIX" N="Appendix A">
<HEAD>Appendix A to Subpart B</HEAD><P>Second appendix.</P></DIV9></DIV6></DIV5>'''


def test_uslm_hierarchy_selects_chapter_and_retains_notes(tmp_path, monkeypatch):
    monkeypatch.setattr(base, "cache_dir", lambda _: tmp_path)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("usc11.xml", USLM)
    monkeypatch.setattr(base, "curl", lambda *a, **k: (buf.getvalue(), 200, a[0]))
    url = "https://uscode.house.gov/download/releasepoints/us/pl/119/111/xml_usc11@119-111.zip"
    ad = usc.Adapter()
    entries = ad.toc({}, {"toc_url": url, "uslm_identifier": "/us/usc/t11/ch1"})
    assert [e["number"] for e in entries] == ["101"]
    result = ad.section(entries[0]["ref"])
    assert "Effective date is October 1" in result["text"]
    assert "Pub. L. 95-598" in result["text"]
    assert "Voluntary" not in result["text"]
    # Historical callers retain their original note-excluding extraction.
    assert "Effective date" not in usc_parser.parse_xml(USLM)[0]["text"]
    legacy = ad.toc({}, {"toc_url": url, "uslm_parent_heading": "BANKRUPTCY", "uslm_unit_depth": 1,
                         "unit": "chapter 1 GENERAL PROVISIONS"})
    assert legacy == entries
    assert ad.toc({}, {"toc_url": url, "uslm_parent_heading": "chapter 1 GENERAL PROVISIONS"}) == entries


def test_ecfr_appendices_keep_parent_identity(monkeypatch):
    monkeypatch.setattr(base, "fetch", lambda name, url, ok: base.Fetched(ECFR, "fixture", url))
    ad = ecfr.Adapter()
    url = "https://www.ecfr.gov/api/versioner/v1/full/2026-09-25/title-12.xml?part=1006"
    entries = ad.toc({}, {"toc_url": url})
    assert len({e["number"] for e in entries}) == 3
    assert entries[0]["number"] == "1006.1"
    assert "Source: official amendment" in ad.section(entries[0]["ref"])["text"]
    assert "First appendix" in ad.section(entries[1]["ref"])["text"]
    assert "Second appendix" not in ad.section(entries[1]["ref"])["text"]
    with pytest.raises(core.PipelineError, match="exactly one"):
        ad.section(url)


def test_ecfr_legacy_parse_part_keeps_return_shape(monkeypatch):
    monkeypatch.setattr(ecfr_parser, "part_xml", lambda *a: (ECFR, "source", "2026-09-25"))
    sections, url, date = ecfr_parser.parse_part("12", "1006")
    assert len(sections) == 3 and (url, date) == ("source", "2026-09-25")


@pytest.mark.parametrize("adapter,url", [
    (ca_leginfo.Adapter(), "https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=CIV"),
    (municode.Adapter(), "https://library.municode.com/ca/orange_county/codes/code_of_ordinances"),
    (ecode360.Adapter(), "https://ecode360.com/HU4937"),
    (ecfr.Adapter(), "https://www.ecfr.gov/current/title-12/part-1006"),
])
def test_directory_urls_fail_before_network(adapter, url, monkeypatch):
    monkeypatch.setattr(base, "fetch", lambda *a, **k: pytest.fail("network attempted"))
    with pytest.raises(core.PipelineError):
        adapter.toc({}, {"toc_url": url})


def register(units):
    doc = core.instruments("T")
    doc["instruments"] = [{"id": "T:TB", "adapter": "generic", "units_in_scope": units}]
    core.write_json(core.jdir("T") / "instruments.json", doc)


class FetchMustNotRun:
    name = "fake"

    def section(self, ref):
        pytest.fail("invalid enumeration attempted text fetch")

    def toc(self, *args):
        pytest.fail("explicit empty section_list must not fall back to TOC")


def test_unit_adapter_routes_official_document_without_changing_parent(root, monkeypatch):
    register([
        {"unit": "chapter", "section_list": [{"number": "1", "ref": "https://test/section"}]},
        {"unit": "approval", "adapter": "official_document", "section_list": [
            {"number": "approval", "ref": "https://test/approval.pdf", "source_unit_kind": "document"}]},
    ])
    calls = []

    class Reader(base.Adapter):
        def __init__(self, name):
            self.name = name

        def section(self, ref):
            calls.append((self.name, ref))
            return {"text": "Exact source text for this acquisition target.", "source_url": ref, "route": "fixture"}

    monkeypatch.setattr(adapters, "get", Reader)
    assert harvest.main("T") == 1  # Whole document still needs subdivision.
    assert calls == [("generic", "https://test/section"), ("official_document", "https://test/approval.pdf")]
    assert all(row["text_file"] for row in core.sections("T"))
    calls.clear()
    assert diff.main("T") == 0
    assert calls == [("generic", "https://test/section"), ("official_document", "https://test/approval.pdf")]


@pytest.mark.parametrize("numbers", [("1", "1"), ("Appendix A", "Appendix/A")])
def test_duplicate_identity_or_filename_preserves_inventory(root, monkeypatch, numbers):
    register([{"unit": str(i), "section_list": [{"number": n, "ref": f"https://test/{i}"}]}
              for i, n in enumerate(numbers)])
    path = core.jdir("T") / "sections.jsonl"
    core.write_jsonl(path, [{"section_id": "T:TB old", "instrument": "T:TB", "unit": "old"}])
    before = path.read_bytes()
    instruments_before = (path.parent / "instruments.json").read_bytes()
    monkeypatch.setattr(adapters, "get", lambda _: FetchMustNotRun())
    with pytest.raises(core.PipelineError, match="duplicate harvest|path collision"):
        harvest.main("T")
    assert path.read_bytes() == before
    assert (path.parent / "instruments.json").read_bytes() == instruments_before


def test_empty_explicit_enumeration_fails_and_preserves_rows(root, monkeypatch):
    register([{"unit": "chapter", "section_list": []}])
    row = {"section_id": "T:TB 1", "instrument": "T:TB", "unit": "chapter", "text_file": None}
    core.write_jsonl(core.jdir("T") / "sections.jsonl", [row])
    monkeypatch.setattr(adapters, "get", lambda _: FetchMustNotRun())
    assert harvest.main("T") == 1
    assert core.sections("T") == [row]
    assert "empty" in core.instruments("T")["fetch_gaps"]["instrument_gaps"][0]["error"]


@pytest.mark.parametrize("with_prior_ref", [False, True])
def test_changed_source_cannot_reuse_saved_text(root, monkeypatch, with_prior_ref):
    register([{"unit": "chapter", "section_list": [{"number": "1", "ref": "https://test/2026/1"}]}])
    path = harvest.text_path("T", "T:TB", "1")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(core.header("https://test/2025/1", "fixture") + "Prior edition text.")
    row = {"section_id": "T:TB 1", "instrument": "T:TB", "unit": "chapter", "text_file": core.rel(path)}
    if with_prior_ref:
        row["ref"] = "https://test/2025/1"
    core.write_jsonl(core.jdir("T") / "sections.jsonl", [row])
    before = path.read_bytes()
    monkeypatch.setattr(adapters, "get", lambda _: FetchMustNotRun())
    with pytest.raises(core.PipelineError, match="reconcile the source/version"):
        harvest.main("T")
    assert path.read_bytes() == before and core.sections("T") == [row]


def test_ca_short_ref_matches_canonical_saved_url():
    ad = ca_leginfo.Adapter()
    assert harvest.reference_identity(ad, "CIV 1950.5") == harvest.reference_identity(
        ad, "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1950.5.")


def test_constitution_section_identity_includes_article(monkeypatch):
    # Official Article I rendering uses SECTION 1., SEC. 1.1., SEC. 2., and Section 25.
    # Source: codes_displayText.xhtml?lawCode=CONS&article=I, checked 2026-10-01.
    html = ('<div id="manylawsections"><h6><a>SECTION 1.</a></h6><p>Text</p>'
            '<h6>SEC. 1.1.</h6><h6>SEC. 2.</h6><h6>Section 25.</h6></div>')
    monkeypatch.setattr(base, "fetch", lambda name, url, ok: base.Fetched(html, "fixture", url))
    ad = ca_leginfo.Adapter()
    a = ad.toc({}, {"toc_url": ca_leginfo.LI + "codes_displayText.xhtml?lawCode=CONS&article=I"})
    b = ad.toc({}, {"toc_url": ca_leginfo.LI + "codes_displayText.xhtml?lawCode=CONS&article=XIII+A"})
    assert [e["number"] for e in a] == ["I 1", "I 1.1", "I 2", "I 25"]
    assert [e["number"] for e in b] == ["XIII A 1", "XIII A 1.1", "XIII A 2", "XIII A 25"]
    assert "article=XIII+A" in b[0]["ref"]
    assert "sectionNum=SECTION+1." in a[0]["ref"]
    assert "sectionNum=SEC.+1.1." in a[1]["ref"]


def test_constitution_preamble_is_extracted_without_other_toc_entries(monkeypatch):
    # The complete provision is the official TOC anchor, not a numbered article section.
    label = ("PREAMBLE: We, the People of the State of California, grateful to Almighty God for our freedom, "
             "in order to secure and perpetuate its blessings, do establish this Constitution.")
    html = f'<a href="codes_displayexpandedbranch.xhtml?heading2=PREAMBLE">{label}</a><a href="x">ARTICLE I</a>'
    monkeypatch.setattr(base, "fetch", lambda name, url, ok: base.Fetched(html, "fixture", url))
    ref = ca_leginfo.LI + "codesTOCSelected.xhtml?tocCode=CONS#preamble"
    result = ca_leginfo.Adapter().section(ref)
    assert result["text"] == label and result["source_url"] == ref


@pytest.mark.parametrize("entry_kind", [False, True])
def test_document_capture_remains_pending_before_section_consumers(root, monkeypatch, entry_kind):
    entry = {"number": "manual", "heading": "Program handbook", "ref": "https://test/manual.pdf"}
    unit = {"unit": "manual", "section_list": [entry]}
    (entry if entry_kind else unit)["source_unit_kind"] = "document"
    register([unit])

    class DocumentAdapter(base.Adapter):
        name = "generic"

        def section(self, ref):
            return {"text": "A whole handbook with several internal sections.", "source_url": ref, "route": "fixture"}

    monkeypatch.setattr(adapters, "get", lambda _: DocumentAdapter())
    assert harvest.main("T") == 1
    row = core.sections("T")[0]
    assert row["text_file"] and row["source_unit_kind"] == "document"
    assert not check.g_j2("T")[0]
    with pytest.raises(core.PipelineError, match="internal sections"):
        match.compute("T")
    with pytest.raises(core.PipelineError, match="internal sections"):
        triage.triage_main("T", cached_only=True)
    entry.pop("source_unit_kind", None)
    unit.pop("source_unit_kind", None)
    register([unit])
    with pytest.raises(core.PipelineError, match="cannot be relabeled"):
        harvest.main("T")


def test_cornell_ccr_walk_deduplicates_and_rejects_empty_branch(monkeypatch):
    from pipeline.adapters import cornell_ccr
    root = 'https://www.law.cornell.edu/regulations/california/title-25/division-1'
    chapter = root + '/chapter-3.5'
    leaf = 'https://www.law.cornell.edu/regulations/california/25-CCR-4900'
    pages = {root: f'<a href="{chapter}">Chapter 3.5</a>' * 2,
             chapter: f'<a href="{root}">Parent</a><a href="{leaf}">Section 4900. Purpose</a>' * 2}
    calls = []
    def fetch(name, url, ok):
        calls.append(url)
        return base.Fetched(pages[url], 'fixture', url)
    monkeypatch.setattr(base, 'fetch', fetch)
    ad = cornell_ccr.Adapter()
    assert ad.toc({}, {'toc_url': root}) == [{'number': '4900', 'heading': 'Section 4900. Purpose', 'ref': leaf, 'source_authority': 'mirror'}]
    assert calls == [root, chapter]
    with pytest.raises(core.PipelineError, match='selected division'):
        ad.toc({}, {'toc_url': root.rsplit('/', 1)[0]})
    pages[chapter] = '<a href="' + root + '">Parent</a>'
    with pytest.raises(core.PipelineError, match='no legal descendants'):
        ad.toc({}, {'toc_url': root})


def test_generic_rejects_binary_without_browser_fallback(tmp_path, monkeypatch):
    from pipeline.adapters import generic
    monkeypatch.setattr(base, 'cache_dir', lambda _: tmp_path)
    monkeypatch.setattr(base, 'curl', lambda *a, **k: (b'PK\x03\x04' + b'x' * 100, 200, a[0]))
    monkeypatch.setattr(base, 'browser', lambda *a, **k: pytest.fail('binary must not become browser HTML'))
    with pytest.raises(core.PipelineError, match='unsupported binary'):
        generic.Adapter().section('https://example.gov/document.zip')


def test_native_xls_missing_dependency_is_explicit(monkeypatch):
    import sys
    from pipeline.adapters import native
    monkeypatch.setitem(sys.modules, 'xlrd', None)
    with pytest.raises(core.PipelineError, match='requires xlrd'):
        native.convert(bytes.fromhex('d0cf11e0a1b11ae1') + b'\x00' * 100, 'https://example.gov/forms.xls')
    with pytest.raises(core.PipelineError, match='does not contain'):
        native.convert(b'<html><body>Download unavailable</body></html>', 'https://example.gov/forms.doc')


@pytest.mark.parametrize('extension', ['doc', 'docx'])
def test_native_word_actual_textutil_conversion(tmp_path, extension):
    import shutil
    import subprocess
    from pipeline.adapters import native
    executable = shutil.which('textutil')
    if not executable:
        pytest.skip('textutil unavailable')
    source = tmp_path / 'source.rtf'
    source.write_bytes(b'{\\rtf1\\ansi This is a legal document fixture.\\par Second paragraph with section 123.}')
    target = tmp_path / ('source.' + extension)
    result = subprocess.run([executable, '-convert', extension, '-output', str(target), str(source)], capture_output=True)
    assert result.returncode == 0, result.stderr
    text, route = native.convert(target.read_bytes(), 'https://example.gov/source.' + extension)
    assert 'This is a legal document fixture.' in text
    assert 'Second paragraph with section 123.' in text
    assert 'textutil' in route


def test_mirror_capture_cannot_close_official_text_gate(root, monkeypatch):
    entry = {'number': '4900', 'heading': 'Purpose', 'ref': 'https://test/mirror', 'source_authority': 'mirror'}
    register([{'unit': 'division 1', 'section_list': [entry]}])
    class MirrorAdapter(base.Adapter):
        def section(self, ref):
            return {'text': 'Mirrored section text has been acquired mechanically.', 'source_url': ref, 'route': 'fixture'}
    monkeypatch.setattr(adapters, 'get', lambda _: MirrorAdapter())
    assert harvest.main('T') == 1
    assert core.sections('T')[0]['source_authority'] == 'mirror'
    passed, explanation = check.g_j2('T')
    assert not passed and 'official source reconciliation pending' in explanation
