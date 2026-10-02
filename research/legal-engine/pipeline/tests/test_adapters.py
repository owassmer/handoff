"""Adapter fixtures (live results saved by `python3 -m pipeline adapter-test --save`) and offline parser tests."""
import json

import pytest

from pipeline import adapters, core
from pipeline.adapters import amlegal, co_olls, ecode360, municipal_codes, or_ors, wa_rcw

FIX = core.PKG / "tests" / "fixtures"
HOLLAND_HOSTS = {
    "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1950.5": "ca_leginfo",
    "https://app.leg.wa.gov/RCW/default.aspx?cite=59.18.280": "wa_rcw",
    "https://olls.info/crs/crs2026-title-38.htm": "co_olls",
    "https://www.oregonlegislature.gov/bills_laws/ors/ors090.html": "or_ors",
    "https://www.azleg.gov/ars/33/01321.htm": "az_ars",
    "https://library.municode.com/co/denver/codes/code_of_ordinances?nodeId=X": "municode",
    "https://codelibrary.amlegal.com/codes/los_angeles/latest/lamc/0-0-0-195228": "amlegal",
    "https://vancouver.municipal.codes/VMC/8.46": "municipal_codes",
    "https://bellevue.municipal.codes/BCC/9.20": "municipal_codes",
    "https://ecode360.com/43347753": "ecode360",
    "https://www.portland.gov/code/30/01/020": "portland_code",
    "https://web.archive.org/web/20250907051547id_/https://ecode360.com/43347753": "wayback",
    "https://docs.sandiego.gov/municode/MuniCodeChapter09/Ch09Art08Division07.pdf": "generic",
}


@pytest.mark.parametrize("name", sorted(n for n in adapters.NAMES if adapters.get(n).SMOKE))
def test_fixture(name):
    meta = json.loads((FIX / f"{name}.json").read_text())
    text = (FIX / f"{name}.txt").read_text()
    assert core.has_header(text)
    assert meta["expect"].lower() in core.norm(text).lower()
    assert core.text_hash(text) == meta["sha256"]
    assert meta["route"] and meta["source_url"].startswith("http")


@pytest.mark.parametrize("url,name", sorted(HOLLAND_HOSTS.items()))
def test_host_routing(url, name):
    assert adapters.for_url(url).name == name


def test_or_ors_sections():
    h = ("<p class=MsoNormal><b><span>90.300 Security deposits; prepaid rent.</span></b><span> (1) As used here.</span></p>"
         "<p class=MsoNormal><span>(2) A landlord may require a deposit.</span></p>"
         "<p class=MsoNormal><b><span>90.302 Fees allowed.</span></b><span> (1) Text.</span></p>"
         "<p class=MsoNormal><b><span>TENANT OBLIGATIONS</span></b></p><p>Not in 90.302.</p>")
    s = or_ors.sections(h)
    assert list(s) == ["90.300", "90.302"]
    assert s["90.300"][0] == "Security deposits; prepaid rent" and "(2) A landlord" in s["90.300"][1]
    assert "Not in" not in s["90.302"][1]


def test_co_olls_sections_and_toc():
    h = ("<p class=MsoNormal style='margin-left:1.25in;text-indent:-1.25in'><span>38-12-103.</span> <span>Return of security deposit.</span></p>"
         "<p class=MsoNormal style='text-indent:.15in'><b><span>38-12-103.</span></b><span> <b>Return of security deposit.</b></span></p>"
         "<p class=MsoNormal><span>(1) A landlord shall return the deposit.</span></p>"
         "<p class=MsoNormal style='text-indent:.15in'><b><span>38-12-104.</span></b><span> <b>Absence of liability.</b></span></p>")
    assert co_olls.toc_entries(h) == [("38-12-103", "Return of security deposit.")]
    s = co_olls.sections(h)
    assert "(1) A landlord shall return" in s["38-12-103"] and "Absence" not in s["38-12-103"]


def test_municipal_codes_article():
    h = ('<article class="level6 type-Section" id="8.46.010"><h6><span class="num">8.46.010</span> <span class="name">Definitions.</span></h6>'
         '<section><p>"Landlord" means.</p><article id="inner"></article></section></article><article id="8.46.020">x</article>')
    t = municipal_codes.article(h, "8.46.010")
    assert "8.46.010" in t and "Landlord" in t and "x" not in t.split("\n")


def test_amlegal_block():
    h = ('<div id="rid-1" class="Section toc-destination rbox"><h6>SEC. 1. TITLE.</h6></div><div id="rid-2" class="rbox Normal-Level">'
         '<p>Body of section one.</p></div><div id="rid-3" class="Section toc-destination rbox"><h6>SEC. 2.</h6></div>')
    t = amlegal.block(h, "1")
    assert "SEC. 1. TITLE." in t and "Body of section one." in t and "SEC. 2" not in t


def test_ecode360_block():
    h = ('<div class="contentTitle barTitle sectionTitle 5" id="5_title" data-guid="5" data-full-title="§&nbsp;9.30.010: Purpose.">'
         '</div><div class="section_content content" id="5_content"><div class="para">Council finds.</div></div></article>'
         '<article><div class="contentTitle barTitle sectionTitle 6" id="6_title" data-full-title="§ 9.30.020: Definitions."></div>')
    t = ecode360.section_block(h, "5")
    assert t.startswith("§ 9.30.010: Purpose.") and "Council finds." in t and "Definitions" not in t


def test_wa_rcw_section_text():
    h = ('<div id="ContentPlaceHolder1_pnlTitleBlock"><a id="ContentPlaceHolder1_lnkTitlePdf" href="x">PDF</a><h1>RCW 59.18.280</h1>'
         '<h2>Moneys paid as deposit.</h2></div><div>(1) Within thirty days.</div><div id="ContentPlaceHolder1_pnlExpanded">footer</div>')
    t = wa_rcw.section_text(h)
    assert t.startswith("RCW 59.18.280") and "(1) Within thirty days." in t and "footer" not in t and "PDF" not in t
