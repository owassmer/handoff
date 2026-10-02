"""Render the lease and the June 2016 email as PDFs."""
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
    rows = [["Date of lease", "November 24, 2014"], ["Landlord", "Whitcomb Holdings LLC, 142 West 88th Street, New York, NY 10024"],
            ["Tenants", "Laura Brenner and Michael Brenner"], ["Term", "January 1, 2015 through June 30, 2016"], ["Monthly rent", "$13,500.00"],
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
    p.append(Paragraph("April 8, 2016. Landlord and Tenants renew the lease of November 24, 2014 for the term July 1, 2016 through "
                       "June 30, 2018. All other terms continue. Security deposit on hand: $43,800.00.", body))
    p.append(Spacer(1, 20))
    p.append(Paragraph("LEASE MODIFICATION AGREEMENT", head))
    p.append(Paragraph("February 12, 2018. Landlord and Tenants agree to modify the lease as renewed:", body))
    for n, text in [("1", "The term ends on February 28, 2018. Tenants will vacate and return all keys by that date."),
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
    rows = [["From:", "Laura Brenner <laura.brenner@gmail.com>"], ["To:", "Eleanor Whitcomb <eleanor@whitcombholdings.com>"], ["Date:", "Saturday, June 11, 2016 4:52 PM"],
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


if __name__ == "__main__":
    lease("lease.pdf")
    email("email.pdf")
