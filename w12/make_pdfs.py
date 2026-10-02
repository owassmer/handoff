"""Render the lease and the June 2024 email as PDFs."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

S = getSampleStyleSheet()
body = ParagraphStyle("b", parent=S["BodyText"], fontName="Times-Roman", fontSize=10.5, leading=14)
head = ParagraphStyle("h", parent=S["Title"], fontName="Times-Bold", fontSize=15)
sub = ParagraphStyle("s", parent=S["Heading3"], fontName="Times-Bold", fontSize=11, spaceBefore=10)


def lease(path):
    p = []
    p.append(Paragraph("RESIDENTIAL LEASE", head))
    p.append(Paragraph("Apartment: Triplex (parlor floor through third floor)<br/>142 West 88th Street, New York, NY 10024", body))
    p.append(Spacer(1, 10))
    rows = [["Date of lease", "November 22, 2022"], ["Landlord", "Whitcomb Holdings LLC, 142 West 88th Street, New York, NY 10024"],
            ["Tenants", "Laura Brenner and Michael Brenner"], ["Term", "January 1, 2023 through June 30, 2024"], ["Monthly rent", "$13,500.00"],
            ["Security deposit", "$40,500.00"]]
    t = Table(rows, colWidths=[1.6 * inch, 4.9 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Times-Roman", 10.5), ("FONT", (0, 0), (0, -1), "Times-Bold", 10.5),
                           ("GRID", (0, 0), (-1, -1), 0.4, "#888888"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    p.append(t)
    p.append(Paragraph("Lease", sub))
    p.append(Paragraph("<b>31. Space as-is.</b> Tenant has inspected the Apartment and Building. Tenant states they are in good "
                       "order and repair and takes the Apartment as-is except for latent defects.", body))
    p.append(Paragraph("Rider", sub))
    for n, text in [
        ("4", "Tenant shall pay one half (50%) of the water and gas bills for the Building. Landlord will present copies of the "
              "bills and the 50% calculation when received. Payment is due within thirty (30) days."),
        ("6", "At the end of the term Tenant shall return the Apartment in its original condition, normal wear and tear excepted. "
              "Landlord may apply the security deposit to the cost of repairing any damage."),
        ("14", "Tenant must inform Landlord of any preexisting damage within two (2) days of occupancy."),
        ("39", "Landlord is aware and gives permission for tenant to have her 4 (four) dogs in the apartment. 2 small mixed breed "
               "dogs 15 lbs, one Bulldog and one miniature Dachshund 12 lbs. This permission is granted solely with respect to the "
               "four existing dogs as of the signing date of this lease. No additional pets will be permitted without prior "
               "permission of the landlord."),
        ("41", "In the event of a legal dispute: the winning party may recover attorneys' fees in all lease disputes between "
               "landlord and tenant arising out of or in connection with the lease.")]:
        p.append(Paragraph(f"<b>{n}.</b> {text}", body))
        p.append(Spacer(1, 4))
    p.append(Spacer(1, 18))
    p.append(Paragraph("Landlord: Whitcomb Holdings LLC, by Eleanor Whitcomb, Principal&nbsp;&nbsp;&nbsp;______________________", body))
    p.append(Spacer(1, 10))
    p.append(Paragraph("Tenants: Laura Brenner ______________________&nbsp;&nbsp;&nbsp;Michael Brenner ______________________", body))
    p.append(PageBreak())
    p.append(Paragraph("LEASE RENEWAL", head))
    p.append(Paragraph("April 9, 2024. Landlord and Tenants renew the lease of November 22, 2022 for the term July 1, 2024 through "
                       "June 30, 2027. All other terms continue. Security deposit on hand: $43,800.00.", body))
    p.append(Spacer(1, 20))
    p.append(Paragraph("LEASE MODIFICATION AGREEMENT", head))
    p.append(Paragraph("September 2, 2026. Landlord and Tenants agree to modify the lease as renewed:", body))
    for n, text in [("1", "The term ends on September 23, 2026. Tenants will vacate and return all keys by that date."),
                    ("8", "Landlord and Tenants will walk through the Apartment for damage within forty-eight (48) hours of vacancy."),
                    ("9", "All other terms of the lease, rider and renewal remain in effect, including rider paragraphs 4 and 6.")]:
        p.append(Paragraph(f"<b>{n}.</b> {text}", body))
        p.append(Spacer(1, 4))
    p.append(Spacer(1, 18))
    p.append(Paragraph("Landlord: Whitcomb Holdings LLC, by Eleanor Whitcomb ______________________", body))
    p.append(Spacer(1, 10))
    p.append(Paragraph("Tenants: Laura Brenner ______________________&nbsp;&nbsp;&nbsp;Michael Brenner ______________________", body))
    SimpleDocTemplate(path, pagesize=letter, title="Lease, 142 West 88th Street", leftMargin=inch, rightMargin=inch).build(p)


def email(path):
    mono = ParagraphStyle("m", parent=body, fontName="Helvetica", fontSize=10, leading=14)
    p = [Paragraph("<b>Apartment condition</b>", ParagraphStyle("t", parent=mono, fontSize=13, leading=18)), Spacer(1, 6)]
    rows = [["From:", "Laura Brenner <laura.brenner@gmail.com>"], ["To:", "Eleanor Whitcomb <eleanor@whitcombholdings.com>"], ["Date:", "Tuesday, June 11, 2024 4:52 PM"],
            ["Subject:", "Apartment condition"], ["Attachments:", "22 images (IMG_2201.jpg to IMG_2222.jpg)"]]
    t = Table(rows, colWidths=[1.1 * inch, 5.3 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 10), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 10),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, "#666666"), ("BOTTOMPADDING", (0, -1), (-1, -1), 8)]))
    p += [t, Spacer(1, 12)]
    p.append(Paragraph("Hi Eleanor,", mono))
    p.append(Spacer(1, 8))
    p.append(Paragraph("Attached are photographs detailing the condition of the screens and other issues in the apartment, all of "
                       "which were existing upon our arrival. I know you're aware of the terrace, the intercom/doorbell and perhaps "
                       "others of these as well, but I've included everything that's not strictly cosmetic like the paint and "
                       "wires. If you have questions about any of this please let me know.", mono))
    p.append(Spacer(1, 8))
    p.append(Paragraph("Laura", mono))
    SimpleDocTemplate(path, pagesize=letter, title="Apartment condition", leftMargin=inch, rightMargin=inch).build(p)




# ---- Case records added in the w9 rebuild. Content comes from case_content so the PDFs and the records agree. ----
import datetime as _dt

import case_content as C

sans = ParagraphStyle("sans", parent=body, fontName="Helvetica", fontSize=10, leading=14)
sans_b = ParagraphStyle("sansb", parent=sans, fontName="Helvetica-Bold")
small = ParagraphStyle("small", parent=sans, fontSize=8.5, leading=11, textColor="#555555")
big = ParagraphStyle("big", parent=sans, fontName="Helvetica-Bold", fontSize=15, leading=19)

LICENSES = {"feld": "NYS Registered Architect No. 038214", "hudson": "NYC DCWP Home Improvement Contractor Lic. 2081457",
            "westside": "NYC DCWP Home Improvement Contractor Lic. 1967320", "carroll": "NYC DCWP Home Improvement Contractor Lic. 2014988",
            "broadway": "NYC DCWP Home Improvement Contractor Lic. 2102563"}
NUMBERS = {"feld": "P-2609-14", "hudson": "HF-4417", "westside": "WPP-26-212", "carroll": "C-1183", "broadway": "BCR-7706"}

VENDORS = {
    "feld": ("Feld Architecture PLLC", "315 West 36th Street, Suite 804, New York, NY 10018", "(212) 555-0147 · office@feldarch.com"),
    "hudson": ("Hudson Floor Restoration", "41-12 22nd Street, Long Island City, NY 11101", "(718) 555-0192 · estimates@hudsonfloors.com"),
    "westside": ("Westside Plaster & Paint", "2485 Broadway, New York, NY 10025", "(212) 555-0168 · jobs@westsideplaster.com"),
    "carroll": ("Carroll Stair & Millwork", "214 Carroll Street, Brooklyn, NY 11231", "(718) 555-0133 · shop@carrollmillwork.com"),
    "broadway": ("Broadway Carpet & Runner", "2170 Broadway, New York, NY 10024", "(212) 555-0121 · sales@broadwaycarpet.com"),
}
WHITCOMB = ("Whitcomb Holdings LLC", "142 West 88th Street, New York, NY 10024", "eleanor@whitcombholdings.com")


def _doc(path, title, parts):
    SimpleDocTemplate(path, pagesize=letter, title=title, leftMargin=inch, rightMargin=inch, topMargin=0.8 * inch).build(parts)


def _letterhead(name, addr, contact):
    return [Paragraph(name, big), Paragraph(f"{addr}<br/>{contact}", small), Spacer(1, 4),
            Table([[""]], colWidths=[6.5 * inch], style=[("LINEBELOW", (0, 0), (-1, -1), 0.8, "#333333")]), Spacer(1, 14)]


def _grid(rows, widths, head=False):
    t = Table(rows, colWidths=widths)
    style = [("FONT", (0, 0), (-1, -1), "Helvetica", 9.5), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LINEBELOW", (0, 0), (-1, -1), 0.3, "#bbbbbb"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if head:
        style += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9.5), ("LINEBELOW", (0, 0), (-1, 0), 0.8, "#333333")]
    t.setStyle(TableStyle(style))
    return t


def _p(text):
    return Paragraph(text.replace("&", "&amp;").replace("\n", "<br/>"), sans)


def _money(cents):
    return f"${int(cents) / 100:,.2f}"


def _date(iso):
    d = _dt.date.fromisoformat(iso[:10])
    return f"{d.strftime('%A, %B')} {d.day}, {d.year}"


def _email(path, subject, sender, to, when, paragraphs, sign):
    p = [Paragraph(f"<b>{subject}</b>", ParagraphStyle("t", parent=sans, fontSize=13, leading=18)), Spacer(1, 6)]
    t = Table([["From:", sender], ["To:", to], ["Date:", when], ["Subject:", subject]], colWidths=[1.0 * inch, 5.5 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 10), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 10),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, "#666666"), ("BOTTOMPADDING", (0, -1), (-1, -1), 8)]))
    p += [t, Spacer(1, 12)]
    for para in paragraphs:
        p += [_p(para), Spacer(1, 8)]
    p.append(_p(sign))
    _doc(path, subject, p)


def walkthrough(path):
    p = _letterhead(*WHITCOMB) + [Paragraph("Move-out walk-through", big), Spacer(1, 6)]
    p.append(_grid([[a, _p(b)] for a, b in [
        ["Unit", "142 West 88th Street, Triplex (parlor floor through third floor)"],
        ["Date", "Thursday, September 24, 2026, 10:00 AM"],
        ["Tenants", "Laura and Michael Brenner (lease ended September 23, 2026)"],
        ["Present", "Eleanor Whitcomb (owner), Michael Brenner (tenant), Karen Liu (West Side Residential), Paul Novak"],
        ["Record", "60 photographs (Eleanor Whitcomb) and one video (Paul Novak), kept on file"]]], [1.2 * inch, 5.3 * inch]))
    p.append(Spacer(1, 12))
    rooms = [line.split(": ", 1) for line in C.WALKTHROUGH_TEXT.split("\n")[1:] if ": " in line]
    p.append(_grid([["Area", "Condition found"]] + [[_p(a), _p(b)] for a, b in rooms], [1.5 * inch, 5.0 * inch], head=True))
    p.append(Spacer(1, 10))
    p.append(_p("Karen Liu also noted odors in several rooms. The southeast bedroom loft ladder was taped off after the walk-through."))
    p.append(Spacer(1, 18))
    p.append(_p("Recorded by Eleanor Whitcomb ______________________    Acknowledged by Michael Brenner ______________________"))
    _doc(path, "Move-out walk-through, September 24, 2026", p)


def history(path):
    p = _letterhead(*WHITCOMB) + [Paragraph("Condition and maintenance history", big), _p("142 West 88th Street, Triplex. Compiled by "
                                                                                          "Eleanor Whitcomb, September 25, 2026."), Spacer(1, 10)]
    for para in C.HISTORY_TEXT.split("\n")[1:]:
        p += [_p(para), Spacer(1, 6)]
    _doc(path, "Condition and maintenance history", p)


def instructions(path):
    lines = C.INSTRUCTIONS_TEXT.split("\n")[1:]
    _email(path, "142 West 88th: getting the triplex back on the market", "Eleanor Whitcomb <eleanor@whitcombholdings.com>",
           "Whitcomb Holdings property management <manage@whitcombholdings.com>", "Friday, September 25, 2026 9:12 AM",
           ["Hi,", *lines], "Thanks,\nEleanor")


def access(path):
    p = _letterhead(*WHITCOMB) + [_p("September 25, 2026"), Spacer(1, 10), Paragraph("<b>Access to 142 West 88th Street, Triplex</b>", sans),
                                  Spacer(1, 8)]
    for para in ["To contractors working in the triplex:",
                 "The apartment is empty. I hold the keys and will let you in for agreed visits. Please call me the day before at "
                 "(917) 555-0186.",
                 "Power, heat and water are on.",
                 "Keep off the southeast bedroom loft ladder until the railing has been repaired. It is taped off.",
                 "Protect the floors and stairs while you work: runners on the stairs and covers on the parquet."]:
        p += [_p(para), Spacer(1, 8)]
    p += [Spacer(1, 6), _p("Eleanor Whitcomb\nWhitcomb Holdings LLC")]
    _doc(path, "Access arrangements", p)


def funds(path):
    p = _letterhead(*WHITCOMB) + [_p("September 25, 2026"), Spacer(1, 10), Paragraph("<b>Restoration funds, 142 West 88th Street, Triplex</b>", sans),
                                  Spacer(1, 8)]
    for para in ["Whitcomb Holdings has set aside $65,000.00 in its operating account for the move-out restoration of the triplex.",
                 "Approve and pay contractors for this work from these funds. They are separate from the Brenners' security deposit, "
                 "which I will settle once the cost of the damage is known."]:
        p += [_p(para), Spacer(1, 8)]
    p += [Spacer(1, 6), _p("Eleanor Whitcomb, Principal")]
    _doc(path, "Restoration funds", p)


def kitchen(path):
    p = _letterhead(*VENDORS["feld"]) + [_p("August 24, 2026\n\nEleanor Whitcomb\nWhitcomb Holdings LLC\n142 West 88th Street\nNew York, NY 10024"),
                                         Spacer(1, 12), Paragraph("<b>Re: Kitchen water repair, completion and sign-off</b>", sans), Spacer(1, 8)]
    for para in ["Dear Eleanor,",
                 "The leak under the kitchen sink came from a failed supply line. Our plumber replaced both supply lines and the "
                 "shutoff valves, and our carpenter replaced the sink base cabinet and patched 6 sq ft of subfloor. Work finished on "
                 "August 21.",
                 "We took moisture readings at the sink base, subfloor and adjoining wall on August 24. Every point read dry.",
                 "The repair is complete and we sign it off. No further work is needed."]:
        p += [_p(para), Spacer(1, 8)]
    p += [_p("Sincerely,\n\nDaniel Feld, RA\nFeld Architecture PLLC")]
    _doc(path, "Kitchen water repair sign-off", p)


def _duration(minutes):
    return f"about {minutes // 60} hours" if minutes <= 480 else f"{round(minutes / 480)} working days"


def service_sheet(pid, path):
    _, _, _, svc = next(x for x in C.PROVIDERS if x[0] == pid)
    services = svc if isinstance(svc, list) else [svc]
    name = VENDORS[pid][0]
    p = _letterhead(*VENDORS[pid]) + [Paragraph(f"Proposal {NUMBERS[pid]}", big),
                                      _p(f"September 25, 2026\nFor: Whitcomb Holdings LLC, attn. Eleanor Whitcomb\n"
                                         f"Job site: 142 West 88th Street, New York, NY 10024 (triplex, parlor floor to third floor)"),
                                      Spacer(1, 12)]
    for s in services:
        total = sum(int(l["amountCents"]) for l in s["lines"])
        p.append(Paragraph(f"<b>{s['title']}</b>", sans))
        p.append(Spacer(1, 4))
        scope = {e["lineId"]: e["method"] for e in s["effects"]}
        rows = [["Item", "Amount"]] + [[Paragraph(f"<b>{l['description']}</b><br/>{scope.get(l['lineId'], '')}", sans),
                                        _money(l["amountCents"])] for l in s["lines"]] + [["Total", _money(total)]]
        t = _grid(rows, [5.2 * inch, 1.3 * inch], head=True)
        t.setStyle(TableStyle([("ALIGN", (1, 0), (1, -1), "RIGHT"), ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 9.5)]))
        p.append(t)
        p.append(Spacer(1, 6))
        terms = [["Payment", s["paymentTerms"]]]
        terms += [["Time on site", _duration(s["durationMinutes"])], ["Earliest start", _date(s["availableFrom"])],
                  ["Valid until", _date(s["validUntil"])]]
        p.append(_grid([[a, _p(b)] for a, b in terms], [1.3 * inch, 5.2 * inch]))
        p.append(Spacer(1, 14))
    p.append(_p("Price includes materials, labor, floor and stair protection, daily cleanup and debris removal. We carry general "
                "liability and workers' compensation insurance; certificates on request."))
    p.append(Spacer(1, 18))
    sig = Table([["Accepted for Whitcomb Holdings LLC", f"For {name}"], ["______________________________", "______________________________"],
                 ["Date ____________", "Date ____________"]], colWidths=[3.25 * inch, 3.25 * inch])
    sig.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9.5), ("TOPPADDING", (0, 0), (-1, -1), 6)]))
    p += [sig, Spacer(1, 10), Paragraph(LICENSES[pid], small)]
    _doc(path, f"{name} proposal", p)


FILES = [  # (local file, media path shown as the file title, prepared document sourceId)
    ("lease.pdf", "Lease, 142 West 88th Street.pdf", "lease"),
    ("email.pdf", "Laura Brenner email, June 11, 2024.pdf", "laura-email-2024"),
    ("walkthrough.pdf", "Move-out walk-through, September 24, 2026.pdf", "walkthrough"),
    ("history.pdf", "Condition and maintenance history.pdf", "history"),
    ("instructions.pdf", "Eleanor Whitcomb email, September 25, 2026.pdf", "instructions"),
    ("kitchen.pdf", "Feld Architecture, kitchen repair sign-off.pdf", "kitchen-signoff"),
    ("access.pdf", "Access arrangements letter.pdf", "access"),
    ("funds.pdf", "Restoration funds letter.pdf", "funds"),
] + [(f"proposal-{pid}.pdf", f"{VENDORS[pid][0]} proposal.pdf", f"services-{pid}") for pid in VENDORS]


def build_all():
    lease("lease.pdf"); email("email.pdf"); walkthrough("walkthrough.pdf"); history("history.pdf"); instructions("instructions.pdf")
    kitchen("kitchen.pdf"); access("access.pdf"); funds("funds.pdf")
    for pid in VENDORS:
        service_sheet(pid, f"proposal-{pid}.pdf")


if __name__ == "__main__":
    build_all()
