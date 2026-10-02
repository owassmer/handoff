import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:EPTL 4-1.3", N, "Inheritance by posthumously conceived children; internal to the estate, and the landlord pays the fiduciary."),
    D("NY:EPTL 4-1.4", N, "Disqualification of a parent from a child's intestate share; internal to the estate."),
    D("NY:Executive Law 293", N, "Creates the Division of Human Rights; the discrimination rules and remedies that bind the settlement are stated (Exec 296(5), 297(9))."),
    D("NY:Executive Law 294", N, "Division of Human Rights policy-making; no party duty."),
    D("NY:Executive Law 294-A", N, "Division's diversity awareness campaign; no party duty."),
    D("NY:Executive Law 296-C", N, "Discrimination against unpaid interns by employers; employment, not housing or collection."),
    D("NY:GBL 131", N, "A shop or service establishment displays its owner's name on its window or exterior sign; an office-display rule that changes no statement, charge or collection step."),
    D("NY:GBL 132", N, "Misdemeanor to trade under a partner's name or '& Co.' without such a partner; the name a lease or letter uses is governed by the stated GBL 130 and FDCPA true-name rules."),
    D("NY:GBL 134", N, "Fraudulent use of a secret fraternity's name; outside the chain."),
    D("NY:GBL 135", N, "Use of a charitable corporation's name to gain advantage; outside the chain."),
]

S = "NY:GBL 136"
rows.append(D(S, "new_rule",
  "136(c) makes it a misdemeanor to put a representation of the United States or New York flag on business letterhead, "
  "envelopes, bill heads or checks, or to use such stationery for business correspondence; the move-out statement, "
  "refund check and balance letters are business correspondence. No rule states it.",
  proposed=[R("NY:GBL-136(c)-no-flag-on-business-stationery", S, "GBL 136(c)", "landlord; managing agent; Handoff; collector",
  "must not",
  "A landlord, manager, Handoff or collector prepares or sends business stationery in the settlement chain: the "
  "itemized statement, a refund check, a balance or demand letter, an invoice, or their envelopes.",
  "The stationery may not carry a representation of the flag, standard, color, shield or ensign of the United States or "
  "of New York (including any picture showing the stars and stripes that a reader would take for the flag), and "
  "stationery so marked may not be used for business correspondence; either act is a misdemeanor. The exception for "
  "stationery for private correspondence does not reach a landlord's or collector's business letters. The rule "
  "governs only the form of the document; a statement sent on such stationery is still a written statement for NY:GOL-7-108(1-a)(e).",
  Q(S, "c. Shall print, engrave, or otherwise place or cause to be printed, engraved or otherwise placed on any blank check,",
    "or shall use any such blank check, bill head, letter head, envelope or other stationery for business purposes or correspondence, or"),
  "minor", "Step 6.4 what the statement must be; Step 8 collecting a balance", dependencies=["NY:GOL-7-108(1-a)(e)"])]))

rows += [
    D("NY:GBL 137", N, "Unauthorized wearing of veterans' and fraternal insignia; outside the chain."),
    D("NY:GBL 138", N, "Sellers of merchandise using 'army', 'government' and similar words in trade names; the chain sells no merchandise, and false government implication in collection is stated at 15 USC 1692e and the city rule importing GBL 601."),
    D("NY:GBL 140", N, "Unauthorized wearing of an employer's registered identification badge; outside the chain."),
    D("NY:GBL 141", N, "Unauthorized use of the United Nations name; outside the chain."),
    D("NY:GBL 142", N, "Possession of another person's United Nations identification card; outside the chain."),
]
save(rows)
