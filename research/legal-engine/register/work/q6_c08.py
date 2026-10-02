"""q6 chunk 8: Fair Housing Act (42 USC 3601ff) and 24 CFR part 100."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q6_lib import D, P, q, save, tf

FHA = "Fair Housing Act, 42 U.S.C. 3601-3631"
R100 = "HUD Fair Housing Act regulations, 24 CFR part 100"
g = lambda k: tf(k)
f3603, f3607, f3613, f3610, f3612, f3614, f3602, f3631 = map(g, ["US:42 USC 3603", "US:42 USC 3607", "US:42 USC 3613",
                                                                  "US:42 USC 3610", "US:42 USC 3612", "US:42 USC 3614",
                                                                  "US:42 USC 3602", "US:42 USC 3631"])
f10, f500, f60, f600, f70, f75, f201 = map(g, ["US:24 CFR 100.10", "US:24 CFR 100.500", "US:24 CFR 100.60",
                                               "US:24 CFR 100.600", "US:24 CFR 100.70", "US:24 CFR 100.75", "US:24 CFR 100.201"])

r_ex = P("US:42USC3603(b)-exemptions", "42 U.S.C. 3603(b)-(c); 24 CFR 100.10(c)", "landlord; managing agent", "scope",
         "Deciding whether the federal Fair Housing Act's rules on terms, charges and accommodations (US:24CFR100.65-terms, "
         "US:42USC3604(f)(3)(B)) reach the settlement of a tenancy.",
         "They do not reach (1) a single-family house rented by a private individual owner who owns no more than three "
         "single-family houses (or interests in their proceeds), but only if rented without any broker, agent, "
         "salesperson or any person in the business of renting dwellings (including a manager or its employees; a person "
         "who took part as agent in two or more rentals in 12 months, as principal in three or more, or owns a building for "
         "five or more families is in that business) and without discriminatory advertising after notice; or (2) units in a "
         "building of at most four families in which the owner lives. A house or unit rented through a managing agent or "
         "Handoff acting as the owner's rental agent is not exempt. The advertising and statement ban (3604(c)) applies "
         "even when exempt. New York State and City law reach these units except their own narrower owner-occupied "
         "exemptions (NY:EXEC-296(5)(a)(2)-terms, NYC:ADC-8-107(5)(a)-terms).",
         f3603, q(f3603, "Nothing in section 3604 of this title (other than subsection (c)) shall apply to—"),
         "major", "5.10", determinacy="MIXED", judgment_terms=["in the business of selling or renting dwellings"],
         instrument=FHA, dependencies=["US:24CFR100.65-terms", "NY:EXEC-296(5)(a)(2)-terms", "NYC:ADC-8-107(5)(a)-terms"],
         construction=[(f3603, q(f3603, "without the use in any manner of the sales or rental facilities or the sales or rental services of any real estate broker, agent, or salesman, or of such facilities or services of any person in the business of selling or renting dwellings")),
                       (f3603, q(f3603, "rooms or units in dwellings containing living quarters occupied or intended to be occupied by no more than four families living independently of each other, if the owner actually maintains and occupies one of such living quarters as his residence."))],
         reasoning="3603(b)(1)-(2) set the two exemptions and 3603(c) defines 'in the business'; using a manager's rental "
                   "services defeats the single-family exemption.")

r_older = P("US:42USC3607-religious-older-persons", "42 U.S.C. 3607(a), (b)", "landlord; managing agent", "scope",
            "The unit is in housing owned by a religious organization for non-commercial purposes, a private club's "
            "lodgings, or housing for older persons (62+ only, or 55+ with at least 80% of occupied units having a 55+ "
            "occupant and published age policies and verification), or the tenant has a conviction for illegal manufacture "
            "or distribution of a controlled substance.",
            "The religious organization may prefer members of its religion (unless membership is restricted by race, color "
            "or national origin) and the club its members; familial-status protections do not apply to qualifying "
            "housing for older persons, and a person relying in good faith on a written claim of that exemption without "
            "knowledge that it fails owes no personal damages; conduct based on the drug-manufacture or distribution "
            "conviction is not prohibited; reasonable occupancy limits stand. Every other Fair Housing Act protection in "
            "the settlement still applies.",
            f3607, q(f3607, "Nor does any provision in this subchapter regarding familial status apply with respect to housing for older persons."),
            "minor", "5.10", determinacy="MIXED", judgment_terms=["intended and operated for occupancy by persons 55 years of age or older"],
            instrument=FHA, dependencies=["US:24CFR100.65-terms"],
            construction=[(f3607, q(f3607, "A person shall not be held personally liable for monetary damages for a violation of this subchapter if such person reasonably relied, in good faith, on the application of the exemption under this subsection relating to housing for older persons."))],
            reasoning="3607(a) and (b)(1)-(5) set the religious, club, occupancy, older-persons and drug-conviction limits.")

r_priv = P("US:42USC3613-private-action", "42 U.S.C. 3613(a), (c)", "landlord; managing agent; Handoff; collector", "liable",
           "A former tenant (or other aggrieved person) claims the landlord, manager, Handoff or a collector committed a "
           "discriminatory housing practice in the tenancy or its settlement (for example deductions or collection applied "
           "differently because of a protected class, refusing an assistance-animal waiver, harassment).",
           "The person may sue in federal or state court within 2 years after the practice occurred or ended (the time a "
           "HUD or agency administrative proceeding is pending is excluded), whether or not an administrative complaint "
           "was filed, unless a conciliation agreement was reached (then only to enforce it) or an ALJ hearing on a HUD "
           "charge began. The court may award actual and punitive damages, injunctions and a reasonable attorney's fee and "
           "costs to the prevailing party.",
           f3613, q(f3613, "not later than 2 years after the occurrence or the termination of an alleged discriminatory housing practice"),
           "critical", "5.10", determinacy="MIXED", judgment_terms=["discriminatory housing practice"], instrument=FHA,
           dependencies=["US:24CFR100.65-terms", "US:24CFR100.7-3617-liability"],
           construction=[(f3613, q(f3613, "the court may award to the plaintiff actual and punitive damages"))],
           reasoning="3613(a)(1)-(3) set standing, the 2-year period and its tolling; (c) the relief.")

r_hud = P("US:42USC3610-3612-hud-enforcement", "42 U.S.C. 3610(a)(1), 3612(a), (g)(3), (o), (p)", "landlord; managing agent; Handoff; collector", "liable",
          "An aggrieved former tenant files a complaint with HUD over a discriminatory housing practice in the tenancy or "
          "its settlement.",
          "The complaint may be filed within one year after the practice occurred or ended; HUD serves the respondent "
          "within 10 days, and the respondent may answer within 10 days of notice. If HUD issues a charge, any party may "
          "elect within 20 days of service to have it decided in federal court (with the relief of 3613); otherwise an ALJ "
          "may award actual damages, equitable relief and a civil penalty of up to $10,000 (no prior violation), $25,000 "
          "(one prior in 5 years) or $50,000 (two or more in 7 years), as adjusted for inflation, plus attorney's fees to "
          "the prevailing party.",
          f3612, q(f3612, "in an amount not exceeding $10,000 if the respondent has not been adjudged to have committed any prior discriminatory housing practice;"),
          "critical", "5.10", determinacy="MIXED", judgment_terms=["discriminatory housing practice"], instrument=FHA,
          dependencies=["US:42USC3613-private-action"],
          construction=[(f3610, q(f3610, "An aggrieved person may, not later than one year after an alleged discriminatory housing practice has occurred or terminated, file a complaint with the Secretary")),
                        (f3612, q(f3612, "The election must be made not later than 20 days after the receipt by the electing person of service under section 3610(h) of this title"))],
          reasoning="3610(a) sets the one-year complaint period; 3612(a), (g)(3), (o), (p) the election, ALJ relief, penalties and fees.")

r_ag = P("US:42USC3614-ag-pattern", "42 U.S.C. 3614(a), (d)", "landlord; managing agent; Handoff; collector", "liable",
         "A landlord, manager, Handoff or collector engages in a pattern or practice of discriminatory settlement or "
         "collection practices, or a denial of rights to a group raising an issue of general public importance.",
         "The Attorney General may sue; the court may order injunctive relief, monetary damages to aggrieved persons, and "
         "a civil penalty of up to $50,000 for a first violation and $100,000 for any subsequent violation (as adjusted), "
         "with attorney's fees to the prevailing party other than the United States.",
         f3614, q(f3614, "in an amount not exceeding $50,000, for a first violation; and", "in an amount not exceeding $100,000, for any subsequent violation."),
         "critical", "5.10", determinacy="MIXED", judgment_terms=["pattern or practice", "general public importance"],
         instrument=FHA, dependencies=["US:42USC3613-private-action"])

r_h = P("US:42USC3602(h)-handicap", "42 U.S.C. 3602(h), (k); 24 CFR 100.201", "landlord; managing agent; Handoff", "scope",
        "Deciding whether a tenant, occupant or associate is protected as a person with a handicap (for example for an "
        "assistance-animal waiver or modification restoration at move-out) or for familial status.",
        "Handicap means a physical or mental impairment substantially limiting one or more major life activities, a "
        "record of one, or being regarded as having one; it excludes current illegal use of or addiction to a controlled "
        "substance (recovered or treated addiction and alcoholism are included). Familial status covers a household with a "
        "child under 18 living with a parent, custodian or written designee, and anyone pregnant or securing custody.",
        f3602, q(f3602, "but such term does not include current, illegal use of or addiction to a controlled substance (as defined in section 802 of title 21)."),
        "minor", "5.9", determinacy="MIXED", judgment_terms=["substantially limits one or more major life activities"],
        instrument=FHA, dependencies=["US:42USC3604(f)(3)(B)", "US:42USC3604(f)(3)(A)"],
        construction=[(f201, q(f201, "drug addiction (other than addiction caused by current, illegal use of a controlled substance) and alcoholism."))],
        reasoning="3602(h) and 100.201 define handicap with the drug-use exclusion; 3602(k) defines familial status.")

r_occ = P("US:24CFR100.10(a)(3)-occupancy-limits", "24 CFR 100.10(a)(3)", "landlord; managing agent", "may",
          "A lease charge or deduction is tied to the number of occupants (for example an over-occupancy charge) in a "
          "household with children.",
          "Reasonable local, state or federal occupancy limits may be applied; a charge based on household size beyond "
          "such a limit is not saved by this exemption and is tested as familial-status discrimination.",
          f10, q(f10, "Limit the applicability of any reasonable local, State or Federal restrictions regarding the maximum number of occupants permitted to occupy a dwelling; or"),
          "minor", "5.10", determinacy="MIXED", judgment_terms=["reasonable"], instrument=R100,
          dependencies=["US:24CFR100.65-terms"])

r_de = P("US:24CFR100.500-discriminatory-effect", "24 CFR 100.500", "landlord; managing agent; Handoff; collector", "must not",
         "A neutral settlement or collection policy (for example a flat cleaning or painting charge schedule, automatic "
         "referral to collection or credit reporting of every balance, refusing payment plans, refusing voucher-share "
         "payment arrangements) actually or predictably falls more heavily on a group protected by the Act.",
         "The policy is unlawful unless the landlord proves it is necessary to achieve a substantial, legitimate, "
         "nondiscriminatory interest, shown by evidence and not speculation, and the tenant does not prove that a less "
         "discriminatory practice would serve that interest. Intent is not required; a justification is no defense to "
         "intentional discrimination.",
         f500, q(f500, "Liability may be established under the Fair Housing Act based on a practice's discriminatory effect, as defined in paragraph (a) of this section, even if the practice was not motivated by a discriminatory intent."),
         "major", "5.10", determinacy="STANDARD",
         judgment_terms=["disparate impact", "substantial, legitimate, nondiscriminatory interest", "less discriminatory effect"],
         instrument=R100, dependencies=["US:24CFR100.65-terms", "US:42USC3613-private-action"],
         construction=[(f500, q(f500, "the charging party or plaintiff may still prevail upon proving that the substantial, legitimate, nondiscriminatory interests supporting the challenged practice could be served by another practice that has a less discriminatory effect."))],
         reasoning="100.500(a)-(c) define discriminatory effect and allocate the burdens.")

r_ev = P("US:24CFR100.60(b)(5)-(7)-ending-tenancy", "24 CFR 100.60(b)(5)-(7)", "landlord; managing agent", "must not",
         "The tenancy ends by eviction, non-renewal or the tenant's departure, and the reason is the tenant's (or a guest's) "
         "protected class, or harassment because of a protected class that caused the tenant to vacate.",
         "Ending the tenancy for that reason, or harassment causing the tenant to leave, is a discriminatory housing "
         "practice; the tenant's damages claim (US:42USC3613-private-action) stands against the landlord's move-out "
         "claims, and charges flowing from the forced departure (lease-break or re-letting charges) are not owed as a "
         "matter of the tenant's damages.",
         f60, q(f60, "Evicting tenants because of their race, color, religion, sex, handicap, familial status, or national origin or because of the race, color, religion, sex, handicap, familial status, or national origin of a tenant's guest."),
         "major", "3.6", determinacy="MIXED", judgment_terms=["because of", "harassment"], instrument=R100,
         dependencies=["US:42USC3613-private-action"],
         construction=[(f60, q(f60, "Subjecting a person to harassment because of race, color, religion, sex, handicap, familial status, or national origin that causes the person to vacate a dwelling or abandon efforts to secure the dwelling."))],
         reasoning="100.60(b)(5) and (7) make discriminatory eviction and harassment-driven departure unlawful; the damages "
                   "remedy is 3613(c).")

r_har = P("US:24CFR100.600-harassment", "24 CFR 100.600", "landlord; managing agent; Handoff; collector", "must not",
          "In settling or collecting the account, someone acting for the landlord makes an unwelcome request or demand "
          "(for example sexual) a condition of the terms (waiving a charge, returning the deposit, a payment plan), or "
          "engages in unwelcome conduct because of a protected class that is severe or pervasive.",
          "Quid pro quo harassment is unlawful even if the tenant acquiesces; hostile-environment harassment is judged on "
          "the totality of circumstances from a reasonable person's view and needs no economic change or proven harm. A "
          "single severe incident or one quid pro quo suffices. Written, verbal or other conduct counts, with or without "
          "physical contact. The owner and manager answer for it (US:24CFR100.7-3617-liability).",
          f600, q(f600, "Quid pro quo harassment refers to an unwelcome request or demand to engage in conduct where submission to the request or demand, either explicitly or implicitly, is made a condition related to:"),
          "major", "5.10", determinacy="STANDARD", judgment_terms=["unwelcome", "sufficiently severe or pervasive"],
          instrument=R100, dependencies=["US:24CFR100.7-3617-liability", "US:42USC3613-private-action"],
          construction=[(f600, q(f600, "A single incident of harassment because of race, color, religion, sex, familial status, national origin, or handicap may constitute a discriminatory housing practice"))],
          reasoning="100.600(a)-(c) define both forms, the totality test and the single-incident rule.")

r_ag70 = P("US:24CFR100.70(d)(1)-agent-refusal", "24 CFR 100.70(d)(1)", "landlord; owner", "must not",
           "The owner asks its manager, Handoff or a collector to apply a settlement or collection practice that would "
           "discriminate because of a protected class, and the agent or employee refuses.",
           "The owner may not discharge, penalize or take other adverse action against the employee, broker or agent for "
           "refusing.",
           f70, q(f70, "Discharging or taking other adverse action against an employee, broker or agent because he or she refused to participate in a discriminatory housing practice."),
           "minor", "5.10", instrument=R100, dependencies=["US:24CFR100.7-3617-liability"])

r_st = P("US:24CFR100.75-statements", "24 CFR 100.75(a)-(c)", "landlord; managing agent; Handoff; collector", "must not",
         "The landlord or anyone for it writes or says something in the tenancy's documents or communications, including "
         "the move-out statement, deduction notes and collection letters.",
         "It may not indicate a preference, limitation or discrimination because of race, color, religion, sex, handicap, "
         "familial status or national origin (for example attributing a charge to 'the children' or to a disability as "
         "such); written notices and statements include any document used with respect to the rental. The ban applies "
         "even to owners exempt under US:42USC3603(b)-exemptions.",
         f75, q(f75, "The prohibitions in this section shall apply to all written or oral notices or statements by a person engaged in the sale or rental of a dwelling."),
         "minor", "6.4", determinacy="MIXED", judgment_terms=["indicates any preference, limitation or discrimination"],
         instrument=R100, dependencies=["US:42USC3603(b)-exemptions"])

r_crim = P("US:42USC3631-criminal", "42 U.S.C. 3631", "landlord; managing agent; Handoff; collector", "must not",
           "Anyone uses force or threat of force to injure, intimidate or interfere with a tenant because of a protected "
           "class and because the tenant is renting or occupying a dwelling (for example at a lockout or a collection visit).",
           "It is a federal crime: fine or up to one year's imprisonment, up to ten years if bodily injury results or a "
           "dangerous weapon is used or threatened, and up to life if death results.",
           f3631, q(f3631, "Whoever, whether or not acting under color of law, by force or threat of force willfully injures, intimidates or interferes with, or attempts to injure, intimidate or interfere with—"),
           "minor", "5.10", determinacy="MIXED", judgment_terms=["willfully", "threat of force"], instrument=FHA)

save([
    D("US:42 USC 3603", "new_rule", "The single-family and owner-occupied exemptions decide whether the federal FHA reaches "
      "the settlement; using a manager defeats the single-family exemption. US:24CFR100.65-terms refers to the exemption "
      "without stating it.", proposed=[r_ex]),
    D("US:24 CFR 100.10", "new_rule", "Occupancy-limit exemption bears on household-size charges; the other exemptions "
      "restate 3603(b) and 3607 (proposed there).", proposed=[r_occ]),
    D("US:42 USC 3607", "new_rule", "Religious, private-club, older-persons and drug-conviction limits on FHA coverage.", proposed=[r_older]),
    D("US:42 USC 3613", "new_rule", "Private right of action: 2-year limit, actual and punitive damages, fees; no rule states "
      "the federal remedy.", proposed=[r_priv]),
    D("US:42 USC 3610", "new_rule", "One-year HUD complaint period and respondent notice; carried with the 3612 remedies.",
      proposed=[P("US:42USC3610-complaint-period", "42 U.S.C. 3610(a)(1)", "landlord; managing agent; Handoff", "deadline",
                  "A former tenant complains to HUD about a discriminatory practice in the tenancy or settlement.",
                  "The complaint is timely if filed within one year after the practice occurred or ended; HUD serves the "
                  "respondent within 10 days of filing, the respondent may answer within 10 days of notice, and HUD aims to "
                  "finish investigating within 100 days. Remedies follow US:42USC3610-3612-hud-enforcement.",
                  f3610, q(f3610, "An aggrieved person may, not later than one year after an alleged discriminatory housing practice has occurred or terminated, file a complaint with the Secretary alleging such discriminatory housing practice."),
                  "major", "5.10", instrument=FHA, dependencies=["US:42USC3610-3612-hud-enforcement"])]),
    D("US:42 USC 3612", "new_rule", "HUD administrative enforcement: election to court, ALJ damages and civil penalties.", proposed=[r_hud]),
    D("US:42 USC 3614", "new_rule", "Attorney General pattern-or-practice suits with civil penalties.", proposed=[r_ag]),
    D("US:42 USC 3602", "new_rule", "The handicap and familial-status definitions fix who the stated disability and "
      "familial-status rules protect, including the drug-use exclusion.", proposed=[r_h]),
    D("US:24 CFR 100.500", "new_rule", "Disparate-impact liability for neutral settlement and collection policies.", proposed=[r_de]),
    D("US:24 CFR 100.60", "new_rule", "Discriminatory eviction and harassment-driven departure decide how the tenancy ended "
      "and give the tenant a damages claim against move-out charges.", proposed=[r_ev]),
    D("US:24 CFR 100.600", "new_rule", "Quid pro quo and hostile-environment harassment in settlement or collection.", proposed=[r_har]),
    D("US:24 CFR 100.70", "new_rule", "Protects an agent (manager, Handoff) that refuses to carry out a discriminatory "
      "practice; the steering rules concern applicants.", proposed=[r_ag70]),
    D("US:24 CFR 100.75", "new_rule", "Statements in move-out documents and collection letters may not express a "
      "protected-class preference, even for exempt owners.", proposed=[r_st]),
    D("US:42 USC 3631", "new_rule", "Criminal penalties for forcible interference with a tenant because of a protected class.", proposed=[r_crim]),
    D("US:24 CFR 100.202", "stated", "Discrimination in terms and services because of handicap is stated by "
      "US:24CFR100.65-terms and the accommodation rule US:42USC3604(f)(3)(B); the inquiry ban in (c) concerns applicants.",
      ["US:24CFR100.65-terms", "US:42USC3604(f)(3)(B)"]),
    D("US:24 CFR 100.400", "stated", "Interference, coercion and retaliation for exercising fair-housing rights is stated "
      "by US:24CFR100.7-3617-liability.", ["US:24CFR100.7-3617-liability"]),
    D("US:24 CFR 100.50", "stated", "The settlement-relevant prohibition, discrimination in terms, conditions and services, "
      "is stated by US:24CFR100.65-terms and US:24CFR100.7-3617-liability; the rest concerns sales, applicants and "
      "brokerage.", ["US:24CFR100.65-terms", "US:24CFR100.7-3617-liability"]),
    D("US:24 CFR 100.5", "no_decision", "Scope and policy statement; the effect standard it mentions is decided in 100.500."),
    D("US:24 CFR 100.80", "no_decision", "Misrepresenting availability to applicants; enforcing a discriminatory lease "
      "clause at move-out is already a discriminatory term under US:24CFR100.65-terms."),
    D("US:24 CFR 100.85", "no_decision", "Blockbusting in sales and rentals to induce transactions; no settlement act."),
    D("US:24 CFR 100.90", "no_decision", "Brokerage-service and MLS access discrimination; no settlement act."),
    D("US:24 CFR 100.20", "no_decision", "Definitions (dwelling, aggrieved person, person in the business) used by the "
      "stated and proposed FHA rules; 'person in the business' is carried in US:42USC3603(b)-exemptions."),
    D("US:24 CFR 100.201", "no_decision", "Design-and-construction definitions for new covered multifamily buildings; its "
      "handicap definition is carried in US:42USC3602(h)-handicap."),
    D("US:24 CFR 100.201a", "no_decision", "Incorporates accessibility standards by reference for design and construction."),
    D("US:24 CFR 100.205", "no_decision", "Accessible design and construction of covered multifamily dwellings first "
      "occupied after 1991; no settlement act."),
    D("US:42 USC 3605", "no_decision", "Discrimination in lending, brokering and appraisal of residential real estate; a "
      "landlord's settlement or payment plan is not a residential real estate-related transaction under 3605(b)."),
    D("US:42 USC 3606", "no_decision", "Access to multiple-listing and brokers' organizations."),
    D("US:42 USC 3615", "no_decision", "Preserves state and city fair-housing laws granting the same rights (the stated NY "
      "and NYC rules) and voids laws requiring discrimination; changes nothing in the chain."),
    D("US:42 USC 3608", "no_decision", "HUD administration and affirmatively-furthering duties of federal agencies."),
    D("US:42 USC 3608a", "no_decision", "HUD data collection."),
    D("US:42 USC 3611", "no_decision", "Subpoena and discovery powers in HUD proceedings."),
    D("US:42 USC 3614–1", "no_decision", "Privilege for self-tests of residential real estate lending; a landlord's "
      "settlement is not a lending transaction."),
    D("US:42 USC 3616a", "no_decision", "Fair Housing Initiatives Program grants."),
])
