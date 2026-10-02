import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

R6 = "register/texts/NYC_RCNY_T6/"
R47 = "register/texts/NYC_RCNY_T47/"
dec("NYC:RCNY 47 2-06", "new_rule",
    "Deliberately refusing a former tenant's self-identified name, pronoun or title, motivated by gender, is a "
    "violation of 8-107; this governs how the statement, demands and collection letters address the tenant. Not "
    "stated.",
    proposed=[rule("NYC:RCNY47-2-06-self-identified-name", "47 RCNY 2-06(a)", "owner; manager; Handoff; collector",
                   "prohibition",
                   "The departing or former tenant has made known a self-identified name, pronoun or gendered title "
                   "that differs from the one in the lease or the landlord's records, and the landlord, manager, "
                   "Handoff or a collector addresses the move-out statement, refund, demand or collection "
                   "communications to that tenant.",
                   "A deliberate refusal to use the self-identified name, pronoun and title, motivated by the "
                   "tenant's gender, violates Admin. Code 8-107 whatever the tenant's sex assigned at birth or "
                   "identification documents; using it may not be conditioned on a court-ordered name change, "
                   "identification in that name, or medical information. Remedies: NYC:ADC-8-502-private-action, "
                   "NYC:ADC-8-120-commission-remedies, NYC:ADC-8-126-civil-penalty. A refund instrument or payment "
                   "sent to the account or payee the tenant designates is unaffected.",
                   R47 + "2-06.txt", q(R47 + "2-06.txt", "A covered entity's deliberate refusal to use an individual's self-identified name",
                                       "where the refusal is motivated by the individual's gender."),
                   "major", "5.10; 6.4", determinacy="MIXED",
                   judgment_terms=["deliberate refusal", "motivated by the individual's gender"],
                   dependencies=["NYC:ADC-8-107(5)(a)-terms"])])
nd("NYC:RCNY 47 2-08", "Hair-based race and religion discrimination; no settlement or collection decision turns on "
   "a tenant's hair or hairstyle, and equal treatment is stated at NYC:ADC-8-107(5)(a)-terms.")
dec("NYC:RCNY 6 1-15", "new_rule",
    "A DCWP licensee (a licensed collector, or Handoff if licensed) must pay a consumer's judgment within 30 days; "
    "this binds the collector after a former tenant's judgment against it. Not stated.",
    proposed=[rule("NYC:RCNY6-1-15-licensee-judgment", "6 RCNY 1-15", "DCWP-licensed debt collection agency (incl. "
                   "Handoff when licensed)", "duty",
                   "A former tenant obtains a judgment against a DCWP licensee relating to its licensed activity (e.g. "
                   "an FDCPA or city-rule judgment against a licensed collector of the tenant's balance).",
                   "The licensee must satisfy the judgment within 30 days of entry, or within 30 days after a stay is "
                   "lifted or an appeal decided, or on a payment schedule the parties agree; failure is a licence "
                   "violation. An unlicensed owner or manager has no duty under this rule.",
                   R6 + "1-15.txt", q(R6 + "1-15.txt", "A licensee or license applicant must satisfy any outstanding judgment",
                                      "according to a payment schedule the parties agree upon."),
                   "minor", "8.6", dependencies=["NYC:ADC-20-490"])])
nd("NYC:RCNY 6 5-21", "Creditors must follow consumer-credit laws; it adds no duty, and whether a lease balance is "
   "consumer credit is stated at NY:ADJ-lease-balance-not-consumer-credit.")
nd("NYC:RCNY 6 5-265", "Form of the tenant screening sign at rental offices; no settlement step.")
nd("NYC:RCNY 6 5-40", "Bars sellers, including lessors, from stating an invalid negligence disclaimer; concerns lease "
   "terms offered to consumers and decides no settlement step.")
dec("NYC:RCNY 6 5-78", "partial",
    "The federal flat-rating rule is stated; the city rule reaches any person (not only FDCPA debt collectors) and "
    "decides the configuration where letters appear in Handoff's or another name without its real participation.",
    ["US:15USC1692j(a)", "US:HANDOFF-config-owner-name-only"],
    [rule("NYC:RCNY6-5-78-deceptive-forms", "6 RCNY 5-78", "any person, incl. Handoff, a manager or a vendor of "
          "letter templates", "prohibition",
          "A person designs, compiles or furnishes a form (demand letter, collection notice, portal message template) "
          "for collecting a former NYC tenant's balance, knowing it would lead the tenant to believe that someone "
          "other than the creditor (e.g. Handoff, a 'collections department', an agency) is participating in the "
          "collection when that person is not.",
          "It is a deceptive and unconscionable trade practice under the city Consumer Protection Law, whoever "
          "furnishes the form and whether or not it is a federal debt collector; DCWP penalty $525 first, $1,050 "
          "second, $3,500 third and later violation (6 RCNY 6-62). A form naming a person that actually takes part "
          "in the collection is outside the rule.",
          R6 + "5-78.txt", q(R6 + "5-78.txt", "It is a deceptive and unconscionable trade practice for any person",
                             "when in fact such person is not so participating."),
          "major", "8.2; 8.4", determinacy="MIXED", judgment_terms=["knowing", "is not so participating"],
          dependencies=["US:15USC1692j(a)", "US:HANDOFF-config-owner-name-only", "NYC:CPL-20-700"])])
nd("NYC:RCNY 6 6-10", "General $500 per-violation ceiling for DCWP penalties where no other amount is set; the "
   "chain's penalty amounts come from their own schedules.")
nd("NYC:RCNY 6 6-57", "Penalty schedule for the tenant screening sign; no settlement step.")
dec("NYC:RCNY 6 6-62", "partial",
    "Licensing penalties are stated at NYC:ADC-20-490; the schedule's amounts for the 6 RCNY 5-77 practice rules "
    "(which bind landlords' own collecting staff too) and for licensee duties are not.",
    ["NYC:ADC-20-490", "NYC:RCNY6-5-77(g)"],
    [rule("NYC:RCNY6-6-62-collection-penalties", "6 RCNY 6-62", "owner or manager whose staff collect; Handoff; "
          "debt collection agency", "consequence",
          "DCWP finds a violation, in collecting a former NYC tenant's balance, of 6 RCNY 5-77 (location information, "
          "communications, harassment, false representations, unfair means, validation, websites) or 5-78, or of a "
          "licensed agency's duties under Admin. Code 20-493.1, 20-493.2 or 6 RCNY 2-190 to 2-194; a repeat means the "
          "same respondent violating the same provision within two years.",
          "Each subdivision charged is a separate violation. 6 RCNY 5-77 and 5-78: $525 first, $1,050 second, "
          "$3,500 third and later (same on default). Licensed-agency duties (call-back number, agency and creditor "
          "names, amount, payment-plan confirmation, verification, time-barred notice, 2-190 to 2-192, 2-194): "
          "$750 first ($1,000 default), $900 second, $1,000 third. Records (2-193): $375 to $500. Acting as an "
          "agency without a licence: $750 to $1,000 plus $100 per day and $100 per contact. DCWP may also seek "
          "licence suspension or revocation.",
          R6 + "6-62.txt", q(R6 + "6-62.txt", "Failure to comply with requirements pertaining to communicating in connection with the collection of a debt", None),
          "major", "8.4; 8.6", dependencies=["NYC:RCNY6-5-77(g)", "NYC:ADC-20-490"],
          amends="NYC:ADC-20-490")])
dec("NYC:RCNY 6 6-85", "new_rule", "Penalty for a licensee's failure to send DCWP its breach notification copy.",
    proposed=[rule("NYC:RCNY6-6-85-breach-copy-penalty", "6 RCNY 6-85", "DCWP licensee", "consequence",
                   "A DCWP licensee fails to promptly send DCWP a copy of its GBL 899-aa breach notification "
                   "(NYC:ADC-20-117-breach-copy-to-DCWP).",
                   "Each failure is a separate violation: $175 first, $300 second, $500 third and later.",
                   R6 + "6-85.txt", q(R6 + "6-85.txt", "Each failure to comply gives rise to a separate violation", None),
                   "minor", "6.10", dependencies=["NYC:ADC-20-117-breach-copy-to-DCWP"])])
dec("NYC:RCNY 6 6-89", "partial",
    "FARE Act restitution and penalties are stated in general; the penalty amounts per violation are not.",
    ["NYC:FARE-20-699.23(c)", "NYC:FARE-20-699.21-agent-fee-ban"],
    [rule("NYC:RCNY6-6-89-FARE-penalties", "6 RCNY 6-89", "landlord; landlord's agent (incl. a managing agent)",
          "consequence",
          "DCWP finds a FARE Act violation: an agent's unlawful fee, the landlord's liability for its agent's fee, "
          "conditioning a rental on engaging an agent, an unlawful fee in a listing, or failure to disclose fees in "
          "the listing or in the signed itemized disclosure; a repeat means the same respondent and provision within "
          "two years.",
          "20-699.21 violations: $750 first ($1,000 default), $1,800 second ($2,000 default), $2,000 third and "
          "later. 20-699.22(a) and (b) disclosure failures: $375 first ($500 default), $900 second ($1,000 default), "
          "$1,000 third and later. Each subdivision charged is a separate violation. Restitution of the fee is in "
          "addition (NYC:FARE-20-699.23(c)).",
          R6 + "6-89.txt", q(R6 + "6-89.txt", "Failure to provide tenant with itemized fee disclosure for residential rental", None),
          "minor", "5.4", dependencies=["NYC:FARE-20-699.23(c)"], amends="NYC:FARE-20-699.23(c)")])
commit()
