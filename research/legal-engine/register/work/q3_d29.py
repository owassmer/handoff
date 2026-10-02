import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

A = "register/texts/NYC_ADC/"
F = A + "27-2004.txt"
ex("NYC:ADC 26-408", "Rent control evictions and certificates of eviction (Admin. Code tit. 26 ch. 3): out of "
   "aperture.")
dec("NYC:ADC 27-2004", "new_rule",
    "Definitions of the Housing Maintenance Code. 'Owner' (including agents and anyone in control) and 'private' and "
    "'multiple dwelling' set the reach of the stated HMC rules; paragraph 48 defines harassment, which 27-2005(d) "
    "bars, and reaches buyout offers, false statements about occupancy, baseless proceedings and contact practices "
    "used to end a tenancy. No rule states the harassment branch.",
    proposed=[
        rule("NYC:HMC-27-2004(48)-buyout-offers", "Admin. Code 27-2004(a)(48)(f-1)-(f-3), 27-2005(d)",
             "owner; managing agent; Handoff or anyone acting on the owner's behalf", "prohibition + duty",
             "Before the tenant has vacated, the owner or someone on its behalf (manager, Handoff) contacts a person "
             "lawfully entitled to occupy an NYC dwelling unit, or that person's relative, offering money or other "
             "consideration (including a waiver of rent or charges or a larger refund) to induce the person to vacate "
             "or surrender or waive occupancy rights (for example an agreed early termination proposed by the owner).",
             "The owner must, at the first such contact and again at the first contact more than 180 days after its "
             "last disclosure, state in writing: the purpose of the contact; that the person may reject the offer and "
             "stay; that the person may consult an attorney and may use HPD's ABCs of Housing guide; that the contact "
             "is by or for the owner; that the person may refuse such contact in writing, barring it for 180 days; "
             "the median asking rent for the community district (with the same bedroom count where HPD reports it); "
             "that there is no guarantee of renting a comparable unit at the same rent; and that employment and "
             "credit history may affect renting. After a written refusal, no offer may be made to the person or a "
             "relative for 180 days unless a court permits it or the person writes asking for offers. No offer may be "
             "made while threatening or using obscene language, contacting with abusive frequency or at unusual "
             "hours, contacting the person at work without written consent, or knowingly misrepresenting facts. Any "
             "of these is harassment, which 27-2005(d) bars; outside a private (one- or two-family) dwelling it is "
             "presumed intended to make the person vacate, and the presumption is rebuttable. A tenant who itself "
             "asks to end the lease early and negotiates terms is not contacted 'to induce' vacating by the owner's "
             "reply to that request.",
             F, q(F, "contacting any person lawfully entitled to occupancy of such dwelling unit to offer money or other valuable consideration to induce such person to vacate such dwelling unit or to surrender or waive any rights in relation to such occupancy, unless such owner discloses",
                  "at the time of the first contact occurring more than 180 days after the prior written disclosure:"),
             "major", "3.3", determinacy="MIXED",
             judgment_terms=["to induce such person to vacate", "such frequency ... as can reasonably be expected to abuse or harass"],
             dependencies=["NYC:ADC-26-2403-buyout-filing"],
             construction=[{"source_file": A + "27-2005.txt",
                            "quote": q(A + "27-2005.txt", "The owner of a dwelling shall not harass any tenants",
                                       "paragraph 48 of subdivision a of section 27-2004 of this chapter.")}],
             reasoning="Paragraph 48 defines harassment as an act by or for an owner that causes or is intended to "
                       "cause a lawful occupant to vacate or surrender rights and that includes a listed act; items "
                       "f-1 to f-3 list the buyout-contact acts. Section 27-2005(d) forbids the owner to harass. "
                       "'Owner' in paragraph 45 includes an agent or anyone in control of the dwelling."),
        rule("NYC:HMC-27-2004(48)-ending-harassment", "Admin. Code 27-2004(a)(45), (48)(a-1), (d), (d-1), (e), (f), (f-4)-(f-6), (g), (h), 27-2005(d)",
             "owner; managing agent; Handoff or anyone acting on the owner's behalf", "prohibition",
             "While a person is still lawfully entitled to occupy an NYC dwelling unit (before surrender or "
             "abandonment), the owner or someone acting for it, in connection with ending the tenancy or settling the "
             "account: tells the person something false or misleading about the occupancy (e.g. that the lease has "
             "ended or must end when Good Cause or another law protects the tenancy, or that rent is owed that is "
             "not); starts repeated baseless or frivolous court proceedings; removes the person's belongings; removes "
             "the door, disables or changes the lock without giving a key; repeatedly contacts or visits on weekends, "
             "legal holidays or outside 9 a.m. to 5 p.m., or in an abusive manner, without the person's written "
             "consent to those times; threatens the person based on a protected status (including lawful source of "
             "income and domestic-violence victim status); requests documents disclosing citizenship after "
             "government ID was given; or does anything barred by the unlawful eviction law (26-521).",
             "Each such act, when it causes or is intended to cause the person to vacate or surrender or waive "
             "occupancy rights, is harassment that the owner may not commit (27-2005(d)); outside a one- or two-family "
             "dwelling the intent is presumed, rebuttably. 'Owner' includes the freeholder, lessee, receiver, agent "
             "and anyone directly or indirectly in control, so the owner answers for its manager and Handoff. "
             "Contacts that law requires or specifically authorizes (the pre-vacate inspection notice, the 14-day "
             "statement) are allowed at any time. Once the tenant has surrendered or abandoned the unit it is no "
             "longer a person lawfully entitled to occupancy, and collection conduct is governed by walk Step 8.",
             F, q(F, "the term \"harassment\" shall mean any act or omission by or on behalf of an owner that",
                  "or to surrender or waive any rights in relation to such occupancy, and"),
             "major", "3.7; 3.8", determinacy="MIXED",
             judgment_terms=["causes or is intended to cause ... to vacate", "false or misleading information",
                             "baseless or frivolous", "manner as can reasonably be expected to abuse or harass"],
             dependencies=["NY:RPAPL-768-853-unlawful-eviction", "NY:RPL-215"],
             construction=[{"source_file": F,
                            "quote": q(F, "knowingly providing to any person lawfully entitled to occupancy of a dwelling unit false or misleading information relating to the occupancy of such unit;", None)},
                           {"source_file": F,
                            "quote": q(F, "The term \"owner\" shall mean and include the owner or owners of the freehold",
                                       "directly or indirectly in control of a dwelling.")}],
             reasoning="The listed items in paragraph 48 are each harassment when joined with the purpose element; "
                       "27-2005(d) bars harassment; paragraph 45 makes agents and anyone in control 'owners'. The "
                       "authorized-contact carve-out comes from item f-4's proviso for contacts authorized or mandated "
                       "by law or rule.")])
nd("NYC:ADC 27-2093", "Certification of no harassment before DOB permits to alter or demolish SRO buildings; a "
   "building-permit precondition, not a settlement step.")
nd("NYC:ADC 27-2093.1", "Certification of no harassment for pilot-program buildings before DOB permits; a "
   "building-permit precondition, not a settlement step.")
st("NYC:ADC 27-2153", ["NYC:HMC-27-2128-owner-debt"],
   "Alternative Enforcement Program charges and fees are the owner's debt and a lien on the building and its rents; "
   "the rule that HPD charges are never a tenant charge is stated. Program selection and work orders decide no "
   "settlement step.")
nd("NYC:RCNY 28 11-01", "Definitions for HPD's lead rules; the turnover rule rests on the Code's own definitions "
   "(27-2056.2) and the owner-cost allocation does not turn on these.")
nd("NYC:RCNY 28 11-06", "Lead-safe work practices, including for turnover work under 27-2056.8; how the work is done, "
   "not who pays, which is stated at NYC:HMC-27-2056.8-lead-turnover.")
nd("NYC:RCNY 28 11-08", "Lead-free and lead-safe exemptions, and notice to HPD when an exempted unit becomes vacant; "
   "an exempt unit has no lead turnover work to allocate.")
nd("NYC:RCNY 28 11-12", "HPD audits and records of turnover lead work; records of the owner's duty, not a charge "
   "question.")
nd("NYC:RCNY 47 2-01", "Definitions for the Commission's employment rules (criminal history, credit); no housing "
   "settlement step.")
nd("NYC:RCNY 47 2-04", "Criminal-history rules for employment; no housing settlement or collection step.")
nd("NYC:RCNY 47 2-05", "Credit-history rules for employers and licensing bodies; no housing settlement step.")
nd("NYC:RCNY 47 2-09", "Pregnancy discrimination, mainly employment, with a housing-application example; no "
   "settlement step turns on pregnancy and equal treatment is stated at NYC:ADC-8-107(5)(a)-terms.")
commit()
