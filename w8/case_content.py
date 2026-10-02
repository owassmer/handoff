"""Content for the 142 West 88th Street move-out case. Single source for the draft and the build."""
import json

SOURCE_SYSTEM = "Whitcomb Holdings"
WORKSPACE_NAME = "Whitcomb Holdings"
GOAL = ("Make the property ready for its next occupant and resolve the departing tenancy's financial relationship, "
        "allowing the two outcomes to progress independently.")
FIXED = ["Keep the kitchen water repair separate from the move-out restoration."]

PARTIES = [
    ("owner", "Eleanor Whitcomb", "Person", "Owner of 142 West 88th Street and principal of Whitcomb Holdings LLC."),
    ("company", "Whitcomb Holdings LLC", "Organization", "Landlord of the triplex at 142 West 88th Street."),
    ("michael", "Michael Brenner", "Person", "Departing tenant. Attended the move-out walk-through."),
    ("laura", "Laura Brenner", "Person", "Departing tenant. Main contact with the owner during the tenancy."),
    ("broker", "Karen Liu", "Person", "Leasing broker at West Side Residential. Listed the triplex in 2022 and attended the walk-through."),
    ("novak", "Paul Novak", "Person", "Attended the walk-through with the owner and recorded a video."),
    ("feld", "Feld Architecture PLLC", "Organization", "Architect already working for the owner on the kitchen water repair. Offers condition assessments and repair scoping."),
    ("hudson", "Hudson Floor Restoration", "Organization", "Hardwood and parquet sanding, refinishing and repair."),
    ("westside", "Westside Plaster & Paint", "Organization", "Plaster repair, painting, woodwork refinishing and general finishing."),
    ("carroll", "Carroll Stair & Millwork", "Organization", "Stair, railing and millwork repair and refinishing."),
    ("broadway", "Broadway Carpet & Runner", "Organization", "Stair runners and carpet supply and installation."),
]

PROPERTY = {"sourceId": "142w88-triplex", "name": "142 West 88th Street, Triplex",
            "address": "142 West 88th Street, New York, NY 10024",
            "description": ("Upper West Side brownstone. The rented triplex runs from the parlor floor to the third floor, with period "
                            "parquet and inlay floors, mahogany woodwork, three fireplaces and a third-floor loft. The owner keeps the "
                            "garden-level media room.")}

TENANCY = {"sourceId": "brenner-lease-2022", "title": "Brenner tenancy, 142 West 88th Street", "landlordPartySourceId": "company",
           "tenantPartySourceIds": ["michael", "laura"], "startDate": "2023-01-01", "endDate": "2026-09-23",
           "noticeDate": "2026-09-02", "endingKind": "Tenancy ending"}

LEASE_TEXT = (
    "Residential lease, 142 West 88th Street, Triplex. Landlord: Whitcomb Holdings LLC. Tenants: Laura and Michael Brenner. "
    "Signed November 22, 2022. Initial term January 1, 2023 to June 30, 2024. Renewed April 9, 2024 through June 30, 2027. "
    "Modified September 2, 2026 to end on September 23, 2026. Security deposit held by landlord: $43,800.\n"
    "Lease ¶31: Tenant has inspected the apartment and building, states they are in good order and repair, and takes the "
    "apartment as-is except for latent defects.\n"
    "Rider ¶4: Tenant pays one half of the water and gas bills within 30 days of receiving copies from the landlord.\n"
    "Rider ¶6: Tenant returns the apartment in its original condition, normal wear and tear excepted. Landlord may apply the "
    "security deposit to damage.\n"
    "Rider ¶14: Tenant must inform landlord of any pre-existing damage within two days of occupancy.\n"
    "Rider ¶39: Landlord permits the tenant's four existing dogs: two small mixed-breed dogs, one bulldog and one miniature "
    "dachshund. No additional pets without the landlord's prior permission.\n"
    "Modification ¶8: Landlord and tenant walk through the apartment for damage within 48 hours of vacancy.")

WALKTHROUGH_TEXT = (
    "Move-out walk-through, September 24, 2026. Present: Eleanor Whitcomb (owner), Michael Brenner (tenant), Karen Liu (broker) and "
    "Paul Novak. Eleanor took 60 photographs; Paul recorded a video.\n"
    "Entrance and stairs: front step chipped; saddle past the vestibule gouged with a broken corner; common-foyer mahogany door "
    "with veneer sheared off one section; newel post chipped and gouged; stair carpet edges scraped and torn on several steps; "
    "top molding and rail edge damaged between the second and third floors.\n"
    "Living room: parquet scraped, scratched and gouged; decorative border missing inlay pieces and stained; finish worn through "
    "in places.\n"
    "Dining room: paint blotches, gouges and a large stain on the parquet; damaged parquet corners; antique hearth tiles missing "
    "and broken; mahogany mantel damaged; a large piece of the doorway casing damaged or missing.\n"
    "Office: carpet heavily stained; floor scratched. Mahogany window sills throughout: stains, ring marks and gouges.\n"
    "West master suite: large dark stains on the plank floor, including in front of the fireplace, with a urine odor; scrapes and "
    "gouges; soot staining on the wall, ceiling, mantel and shelving; a deep gouge in the molding.\n"
    "East master bedroom: ceiling damaged where the period chandeliers were replaced with the tenants' fixtures. East bathroom "
    "ceiling stained and damaged.\n"
    "Third floor: southeast bedroom loft-ladder railing pulled away, with protruding nails and torn wood; not safe to use. "
    "Northeast storage-ladder railing scraped. Northeast bedroom plank floor with a dark urine stain; bedroom door broken and the "
    "plaster behind it damaged. Bathroom tub porcelain chipped and vanity panel broken. Great-room plank floor heavily stained and "
    "gouged with a urine odor; plaster damage and staining down one wall; ceiling damaged around the light fixtures.\n"
    "Karen Liu also noted odors in several rooms.")

CONDITIONS = [
    ("floors", "Parquet, inlay border and plank floors scratched, gouged and stained, with missing inlay pieces.", "Deficient"),
    ("woodwork", "Window sills, doorway casing, moldings and mantels stained, gouged or broken; foyer door veneer sheared.", "Deficient"),
    ("hearth", "Dining-room hearth with missing and broken antique tiles.", "Deficient"),
    ("stairs", "Newel post, stair trim, top molding and rail edge chipped and damaged.", "Deficient"),
    ("railing", "Southeast bedroom loft-ladder railing pulled away, with protruding nails; unsafe to use.", "Deficient"),
    ("carpet", "Stair runner edges torn; office carpet heavily stained.", "Deficient"),
    ("door", "Northeast bedroom door broken.", "Deficient"),
    ("plaster", "Plaster damage in the great room and northeast bedroom; soot staining in the west master suite.", "Deficient"),
    ("ceiling", "Ceiling damage in the east master bedroom, east bathroom and third-floor great room.", "Deficient"),
    ("bath", "Third-floor tub porcelain chipped; vanity panel broken.", "Deficient"),
    ("odors", "Urine odor in the west master suite, great room and other rooms.", "Deficient"),
]
CONDITION_DETAILS = {
    "coverage": {"goal": GOAL, "conditionIds": [c[0] for c in CONDITIONS],
                 "reason": "The walk-through covered every room of the triplex; these are all the conditions found."},
    "conditions": [{"conditionId": i, "description": d, "state": s, "repairable": True, "accessible": True} for i, d, s in CONDITIONS]}

HISTORY_TEXT = (
    "Condition and maintenance history, compiled by Eleanor Whitcomb.\n"
    "Before the tenancy: the apartment was painted and the floors redone in late 2022. Karen Liu's 2022 listing photographs show "
    "intact fireplace tiles and window woodwork, and good floors with a few dark spots and one diagonal scratch in the living room. "
    "A family stayed briefly over the 2022 holidays before the Brenners moved in on January 9, 2023.\n"
    "June 11, 2024: Laura Brenner emailed 22 photographs of screens, a loose dining-room hearth, loose or broken tiles, missing "
    "molding and a small missing parquet piece, describing them as existing on arrival. None of this was reported within the two "
    "days required by rider ¶14.\n"
    "Complaints during the tenancy: uneven room temperatures, a clogged toilet, a roof leak, weak dryer performance, bin lids and "
    "the intercom. Work done: screens repaired, window weather stripping and five temperature sensors added, a new intercom "
    "installed and the leaks repaired.\n"
    "June 2024: during a screen inspection Eleanor found a dog accident on the floor; Laura apologized and cleaned it up.\n"
    "Repeated indoor grilling caused grease odors and set off smoke alarms. Eleanor asked the Brenners to stop.\n"
    "August 2026: Feld Architecture was hired about water in the kitchen. That repair is separate from the move-out work.")

EMAIL_TEXT = (
    "From: Laura Brenner\nTo: Eleanor Whitcomb\nDate: June 11, 2024\nSubject: Apartment condition\n\n"
    "Attached are photographs detailing the condition of the screens and other issues in the apartment, all of which were "
    "existing upon our arrival. I know you're aware of the terrace, the intercom/doorbell and perhaps others of these as well, but "
    "I've included everything that's not strictly cosmetic like the paint and wires. If you have questions about any of this "
    "please let me know.\n\nLaura\n\n22 photographs attached.")

INSTRUCTIONS_TEXT = (
    "From Eleanor Whitcomb, September 25, 2026.\n"
    "I want the triplex back on the market as soon as possible, ideally showing by late October for a December 1 move-in.\n"
    "Have Feld Architecture walk the apartment first and give me a condition schedule and a scope with a budget before we commit "
    "to repairs. Then line up the trades.\n"
    "The loft-ladder railing is dangerous. Keep everyone off that ladder until it is fixed.\n"
    "The kitchen water repair is a separate job Feld is already handling. Keep it out of this.\n"
    "You can approve work within the funds I've set aside; I don't need to sign each contract. Deal with the contractors directly.\n"
    "I'll settle the Brenners' deposit separately once we know what the damage costs.")

ACCESS_TEXT = (
    "The apartment is empty. Eleanor holds the keys and lets contractors in for agreed visits; call her the day before. Power, "
    "heat and water are on. Keep off the southeast bedroom loft ladder until the railing is repaired. Contractors protect the "
    "floors and stairs while they work.")

FUNDING_TEXT = ("Whitcomb Holdings has set aside $65,000 for the move-out restoration of the triplex. This is separate from the "
                "Brenners' security deposit.")


def service(sid, title, kind, lines, deposit, terms, reqs, avail, valid, duration, response, invoice_due, effects):
    return {"serviceId": sid, "title": title, "kind": kind, "currency": "USD",
            "lines": [{"lineId": l, "description": d, "amountCents": c} for l, d, c in lines],
            "depositCents": deposit, "paymentTerms": terms, "requirements": reqs, "availableFrom": avail, "validUntil": valid,
            "durationMinutes": duration, "responseMinutes": response, "invoiceDueMinutes": invoice_due,
            "effects": [{"lineId": l, "conditionIds": ids, "method": m} for l, ids, m in effects]}


ALL = [c[0] for c in CONDITIONS]
PROVIDERS = [
    ("feld", "Feld Architecture: restoration assessment",
     "Feld Architecture offers a restoration assessment of the triplex. One site visit of up to three hours. We produce a "
     "room-by-room condition schedule with photographs and measurements, a written scope of repairs with a preliminary budget, and "
     "flag any immediate safety issues. Fixed fee: site assessment $600; condition and quantity schedule $300; scope and budget "
     "note $300; total $1,200 including travel. Earliest visit Monday, September 28. Report within two business days of the visit. "
     "Invoice on delivery of the report, payable within 14 days. Kitchen water work is covered under our separate engagement and "
     "is excluded. Offer valid through October 31, 2026.",
     service("restoration-assessment", "Restoration assessment", "Assessment",
             [("site-assessment", "Site assessment", "60000"), ("condition-schedule", "Condition and quantity schedule", "30000"),
              ("scope-budget", "Scope and budget note", "30000")],
             "0", "Invoice on delivery of the report, payable within 14 days.", ["Kitchen water work is excluded."],
             "2026-09-28T13:00:00.000Z", "2026-10-31T23:59:59.000Z", 180, 240, 20160,
             [("site-assessment", ALL, "Inspect every room, photograph and measure each condition, and flag safety issues."),
              ("condition-schedule", ALL, "Room-by-room schedule of conditions with quantities."),
              ("scope-budget", ALL, "Written repair scope by trade with a preliminary budget.")])),
    ("hudson", "Hudson Floor Restoration: floor restoration",
     "Hudson Floor Restoration: restore the triplex floors, about 900 sq ft. Sand and refinish parquet and plank floors: $5,400. "
     "Replace damaged parquet and missing inlay border pieces with matched stock: $1,850. Treat and seal urine-stained plank floors: "
     "$769. Total $8,019. Deposit of $2,000 on booking; balance on completion, payable within 7 days. Three working days on site. "
     "Earliest start October 12. Offer valid through November 30, 2026.",
     service("floor-restoration", "Floor restoration", "Repair",
             [("sand-refinish", "Sand and refinish parquet and plank floors", "540000"),
              ("parquet-inlay", "Replace damaged parquet and inlay border pieces", "185000"),
              ("stain-seal", "Treat and seal urine-stained plank floors", "76900")],
             "200000", "Deposit of $2,000 on booking; balance on completion, payable within 7 days.", [],
             "2026-10-12T13:00:00.000Z", "2026-11-30T23:59:59.000Z", 1440, 240, 10080,
             [("sand-refinish", ["floors"], "Sand to bare wood, stain to match and apply three coats of finish."),
              ("parquet-inlay", ["floors"], "Cut out damaged pieces and set matched parquet and inlay."),
              ("stain-seal", ["floors", "odors"], "Bleach and enzyme-treat stained planks, then seal before refinishing.")])),
    ("westside", "Westside Plaster & Paint: plaster, paint and woodwork",
     "Westside Plaster & Paint: plaster repair and soot cleanup in the great room, northeast bedroom and west master suite: "
     "$11,366.67. Paint walls, ceilings and trim throughout, including ceiling repairs at the light fixtures: $12,783.32. Restore "
     "woodwork and fireplaces: window sills, doorway casing, moldings, mantels, hearth tiles, foyer door veneer and the northeast "
     "bedroom door: $10,000. Bathroom repairs and caulking: tub chip repair and vanity panel: $3,762.50. Total $37,912.49. "
     "Deposit of $10,000 at start; balance on completion, payable within 14 days. About two weeks on site. Earliest start October 5. "
     "Offer valid through November 30, 2026.",
     service("finishing", "Plaster, paint and woodwork", "Repair",
             [("plaster", "Plaster repair and soot cleanup", "1136667"), ("paint", "Paint walls, ceilings and trim", "1278332"),
              ("woodwork", "Woodwork and fireplace restoration", "1000000"), ("bath", "Bathroom repairs and caulking", "376250")],
             "1000000", "Deposit of $10,000 at start; balance on completion, payable within 14 days.", [],
             "2026-10-05T13:00:00.000Z", "2026-11-30T23:59:59.000Z", 4800, 240, 20160,
             [("plaster", ["plaster"], "Cut back and patch damaged plaster, clean and seal soot-stained surfaces."),
              ("paint", ["ceiling", "plaster"], "Repair ceilings at the fixtures, prime and paint walls, ceilings and trim."),
              ("woodwork", ["woodwork", "hearth", "door"], "Repair and refinish mahogany woodwork, reset and replace hearth tiles, repair the doors."),
              ("bath", ["bath"], "Repair the tub chip and refit the vanity panel.")])),
    ("carroll", "Carroll Stair & Millwork: loft railing and stair repair",
     "Carroll Stair & Millwork: rebuild and secure the southeast bedroom loft-ladder railing: $1,500, about three hours, as early "
     "as September 29. Repair and refinish the main stair, newel post, trim, top molding and rail edge: $9,000, two working days "
     "from October 5. Each job is invoiced on completion, payable within 14 days. Offers valid through November 30, 2026.",
     [service("loft-railing", "Loft railing repair", "Repair",
              [("loft-railing", "Rebuild and secure loft-ladder railing", "150000")],
              "0", "Invoice on completion, payable within 14 days.", [],
              "2026-09-29T13:00:00.000Z", "2026-11-30T23:59:59.000Z", 180, 240, 20160,
              [("loft-railing", ["railing"], "Remove the damaged railing, rebuild and fasten it, and test it under load.")]),
      service("stair-refinish", "Stair repair and refinishing", "Repair",
              [("stair", "Repair and refinish stair, newel, trim and rail edge", "900000")],
              "0", "Invoice on completion, payable within 14 days.", [],
              "2026-10-05T13:00:00.000Z", "2026-11-30T23:59:59.000Z", 960, 240, 20160,
              [("stair", ["stairs"], "Repair damaged millwork, sand and refinish the stair.")])]),
    ("broadway", "Broadway Carpet & Runner: stair runner and office carpet",
     "Broadway Carpet & Runner: supply and install a new stair runner: $2,500. Replace the office carpet: $2,257.84. Total "
     "$4,757.84. Payment on installation, due within 14 days. One day on site, after floor work is finished. Earliest date "
     "October 19. Offer valid through November 30, 2026.",
     service("carpet", "Stair runner and office carpet", "Repair",
             [("runner", "Supply and install stair runner", "250000"), ("office", "Replace office carpet", "225784")],
             "0", "Payment on installation, due within 14 days.", [],
             "2026-10-19T13:00:00.000Z", "2026-11-30T23:59:59.000Z", 480, 240, 20160,
             [("runner", ["carpet"], "Remove the old runner and install the new runner with pads and rods."),
              ("office", ["carpet"], "Remove stained carpet and install new carpet and pad.")])),
]

OWNER_FUNDING = {"currency": "USD", "confirmedCents": "6500000", "confirmedAt": "2026-09-25T14:00:00.000Z",
                 "paymentBehavior": "Settle", "responseMinutes": 240}


def notice(owner_party_id):
    docs = [
        {"sourceId": "lease", "title": "Lease, renewal and September 2026 modification", "kind": "Agreement", "sourceKind": "Prepared", "sourceVersion": "1",
         "partySourceId": "company", "text": LEASE_TEXT, "availableFrom": "2026-09-02"},
        {"sourceId": "walkthrough", "title": "Move-out walk-through, September 24, 2026", "kind": "Inspection report", "sourceKind": "Source",
         "partySourceId": "owner", "text": WALKTHROUGH_TEXT, "availableFrom": "2026-09-24"},
        {"sourceId": "condition", "title": "Condition after move-out", "kind": "Property condition", "sourceKind": "Prepared",
         "partySourceId": "owner", "sourceVersion": "1", "availableFrom": "2026-09-24",
         "text": "Conditions found at the September 24 walk-through, by area.", "detailsJson": json.dumps(CONDITION_DETAILS)},
        {"sourceId": "history", "title": "Condition and maintenance history", "kind": "Condition report", "sourceKind": "Source",
         "partySourceId": "owner", "text": HISTORY_TEXT, "availableFrom": "2026-09-25"},
        {"sourceId": "laura-email-2024", "title": "Laura Brenner: apartment condition, June 11, 2024", "kind": "Correspondence",
         "sourceKind": "Prepared", "sourceVersion": "1", "partySourceId": "laura", "text": EMAIL_TEXT, "availableFrom": "2024-06-11"},
        {"sourceId": "instructions", "title": "Owner instructions", "kind": "Instruction", "sourceKind": "Source",
         "partySourceId": "owner", "text": INSTRUCTIONS_TEXT, "availableFrom": "2026-09-25"},
        {"sourceId": "access", "title": "Access arrangements", "kind": "Access arrangements", "sourceKind": "Source",
         "partySourceId": "owner", "text": ACCESS_TEXT, "availableFrom": "2026-09-25"},
        {"sourceId": "funds", "title": "Restoration funds", "kind": "Owner funding", "sourceKind": "Prepared", "partySourceId": "company",
         "sourceVersion": "1", "availableFrom": "2026-09-25", "text": FUNDING_TEXT,
         "detailsJson": json.dumps({"ownerPartyId": owner_party_id, **OWNER_FUNDING})},
    ] + [{"sourceId": f"services-{pid}", "title": title, "kind": "Provider information", "sourceKind": "Prepared",
          "partySourceId": pid, "sourceVersion": "1", "availableFrom": "2026-09-25", "text": text,
          "detailsJson": json.dumps({"services": svc if isinstance(svc, list) else [svc]})} for pid, title, text, svc in PROVIDERS]
    return {
        "sourceSystem": SOURCE_SYSTEM, "sourceRecordId": "142w88-moveout-2026", "title": "142 West 88th Street move-out",
        "goal": GOAL, "businessDate": "2026-09-27", "fixedRequirements": FIXED, "property": PROPERTY,
        "parties": [{"sourceId": s, "name": n, "kind": k, "description": d} for s, n, k, d in PARTIES],
        "tenancy": TENANCY, "documents": docs,
        "agreements": [{"sourceId": "lease-terms", "title": "Lease, renewal and September 2026 modification", "kind": "Lease",
                        "termsText": ("Return the apartment in its original condition, normal wear and tear excepted; the deposit may be "
                                      "applied to damage. As-is acceptance except latent defects. Pre-existing damage to be reported "
                                      "within two days of occupancy. Four named dogs permitted. Tenant pays half of water and gas. "
                                      "Walk-through within 48 hours of vacancy. Term ends September 23, 2026."),
                        "sourceDocumentSourceId": "lease", "effectiveFrom": "2022-11-22"}],
        "obligations": [
            {"sourceId": "return-condition", "title": "Return the apartment in its original condition",
             "description": "Return the triplex in its original condition, normal wear and tear excepted.",
             "responsiblePartySourceIds": ["michael", "laura"], "beneficiaryPartySourceIds": ["company"],
             "basisAgreementSourceId": "lease-terms", "basisDocumentSourceId": "lease", "status": "Under assessment"},
            {"sourceId": "utilities-share", "title": "Pay half of water and gas bills",
             "description": "Pay one half of the water and gas bills within 30 days of receiving copies.",
             "responsiblePartySourceIds": ["michael", "laura"], "beneficiaryPartySourceIds": ["company"],
             "basisAgreementSourceId": "lease-terms", "basisDocumentSourceId": "lease", "status": "Open"}],
    }
