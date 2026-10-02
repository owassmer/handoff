import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

A = "register/texts/NYC_ADC/"
nd("NYC:ADC 20-104", "DCWP's licensing and rulemaking powers; whether a collector needs a licence is stated at "
   "NYC:ADC-20-489(a) and NYC:ADC-20-490.")
dec("NYC:ADC 20-106", "partial",
    "The licensing requirement and 20-494 penalties are stated; the criminal fines and escalating civil penalties "
    "for unlicensed activity are not.", ["NYC:ADC-20-490"],
    [rule("NYC:ADC-20-106-unlicensed-sanctions", "Admin. Code 20-106(a)-(c)", "person acting as a debt collection "
          "agency without a licence (incl. Handoff in the principal-purpose configuration)", "consequence",
          "A person engages in debt collection agency activity for which Admin. Code 20-490 requires a DCWP licence, "
          "without one, or violates a chapter 2 provision or rule.",
          "On conviction: never licensed, a fine of $25 to $500, up to 15 days' imprisonment, or both, and a civil "
          "penalty of the greater of twice the licence fee or $100; a second offense or a lapsed licence, $100 to "
          "$1,000, up to 30 days, and a $1,000 civil penalty; a suspended or revoked licence or two prior convictions, "
          "$200 to $2,000, up to 60 days, and a $2,000 civil penalty. Any other chapter 2 violation: $25 to $500 fine, "
          "up to 15 days, and a $100 civil penalty per violation. A manager or proprietor who consents to or causes "
          "the unlicensed operation is in violation and owes $100 for each day it operates. These are in addition to "
          "the 20-494 penalties.",
          A + "20-106.txt", q(A + "20-106.txt", "Any person who engages without a license therefor in an activity",
                              "shall, upon conviction thereof, be subject to the following sanctions:"),
          "major", "8.6", dependencies=["NYC:ADC-20-490"], amends="NYC:ADC-20-490")])
nd("NYC:ADC 20-109", "Licences are not transferable; a buyer of a collector's business needs its own licence, a "
   "point already inside NYC:ADC-20-490.")
nd("NYC:ADC 20-115", "DCWP may require bonds for licensed activities; no settlement step.")
nd("NYC:ADC 20-488", "Legislative findings for licensing debt collection agencies; no operative rule.")
nd("NYC:ADC 20-702", "DCWP's power to define deceptive practices by rule; the rules themselves are decided where "
   "they appear (6 RCNY 5-76 to 5-78).")
dec("NYC:ADC 20-703", "partial",
    "The Consumer Protection Law hook for the collection rules is stated at NYC:CPL-20-700; its penalties and the "
    "restitution to consumers are not.", ["NYC:CPL-20-700"],
    [rule("NYC:ADC-20-703-CPL-remedies", "Admin. Code 20-703(a)-(c), (e), (g)-(i)", "owner or manager whose staff "
          "collect; Handoff; collector", "consequence",
          "A deceptive or unconscionable practice under Admin. Code 20-700 or a DCWP rule made under it (including "
          "6 RCNY 5-77 and 5-78) occurs in collecting a former NYC tenant's balance or in the settlement.",
          "Civil penalty $350 to $2,500 per violation (the 6 RCNY 6-62 schedule sets DCWP's amounts); each "
          "statement or omission is a separate violation, and each day it is exposed to the public a further one. "
          "The city may sue in Supreme Court, or DCWP may proceed at OATH, for an injunction, penalties and "
          "restitution of all money received through the violation to every affected consumer; restitution "
          "reaches transactions within five years before the action, and a consumer who takes restitution under a "
          "court judgment cannot recover damages again for the same acts up to the judgment. The Consumer "
          "Protection Law gives the tenant no private action of its own.",
          A + "20-703.txt", q(A + "20-703.txt", "The violation of any provision of this subchapter or of any rule promulgated thereunder",
                              "not less than $350 nor more than $2,500."),
          "major", "8.4", dependencies=["NYC:CPL-20-700"], amends="NYC:CPL-20-700")])
nd("NYC:ADC 20-705", "Excludes broadcasters, publishers and ad agencies from the Consumer Protection Law; no chain "
   "party is one.")
nd("NYC:ADC 26-3005", "Security standards a smart access system must meet during operation; the move-out data "
   "removal and non-disclosure rules are stated at NYC:ADC-26-3002(c)-moveout-data and "
   "NYC:ADC-26-3003-3006-data-sale.")
nd("NYC:ADC 26-3904", "HPD sets the voucher's maximum rent at the HCV payment standard (from 2027-01-26); an HPD "
   "calculation, not a settlement step.")
dec("NYC:ADC 26-3905", "new_rule",
    "From 2027-01-26 the city rental assistance voucher splits the rent into HPD's payment to the owner and the "
    "household's contribution; the final account must carry the two separately. Not stated.",
    proposed=[rule("NYC:ADC-26-3905-city-voucher-split", "Admin. Code 26-3905(a)-(c)", "owner; manager", "who is paid",
                   "From 2027-01-26 the departing household holds an HPD rental assistance voucher under Admin. Code "
                   "tit. 26 ch. 39 for an NYC unit (apartment, room or SRO) that is not rent-stabilized.",
                   "HPD pays the owner each month the actual rent up to the maximum rental allowance, minus the "
                   "household's contribution; the household's contribution is the greater of 30% of its monthly "
                   "adjusted income or the housing portion of its public assistance (less a utility allowance where "
                   "utilities are not included). On the move-out account, unpaid rent is split into HPD's payment and "
                   "the household's contribution, each tracked against its own payer; the landlord-requirement and "
                   "move-out rules that 26-3907 directs HPD to adopt bind once HPD promulgates them.",
                   A + "26-3905.txt", q(A + "26-3905.txt", "The department shall provide monthly rental assistance to an owner",
                                        "minus the household rent contribution as described in subdivision b of this section."),
                   "major", "5.8", effective_from="2027-01-26")])
ex("NYC:ADC 26-405.1", "Rent control and rent-regulated MCI/IAI rules (Admin. Code tit. 26 ch. 3): out of aperture.")
nd("NYC:ADC 26-3901", "Definitions for the city rental assistance voucher (unit includes rooms and SROs; HPD "
   "administers); they set the reach of NYC:ADC-26-3905-city-voucher-split only through its stated condition.")
nd("NYC:ADC 26-3902", "Creates the voucher program subject to appropriation; no settlement step.")
nd("NYC:ADC 26-3903", "Voucher eligibility (stabilized tenants in nonpayment cases, shelter households); HPD's "
   "decision, not a settlement step.")
nd("NYC:ADC 26-3906", "Funding and waiting list; no settlement step.")
nd("NYC:ADC 26-3907", "HPD rulemaking mandate for the voucher (landlord requirements, moves); no rule adopted yet, "
   "and the mandate itself binds no chain party.")
nd("NYC:ADC 26-3908", "HPD's annual report; no chain party.")
commit()
