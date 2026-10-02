import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
rows.append(D("NY:RPAPL 751", "no_decision",
  "Stays a nonpayment warrant when the tenant deposits the rent, costs and interest or gives an undertaking; it keeps a "
  "tenancy in possession and the deposit reaches the landlord as ordinary rent, so no settlement rule changes."))

S = "NY:RPAPL 756"
rows.append(D(S, "new_rule",
  "A suit for rent against any tenant of the building is stayed while utilities are off because the landlord did not "
  "pay for them; this reaches the landlord's claim for a move-out rent balance.",
  proposed=[R("NY:RPAPL-756-utility-shutoff-stay", S, "RPAPL 756", "landlord", "must_not",
  "Utilities (gas, electricity, water, heat supplied under the landlord's contract) are discontinued in any part of "
  "the dwelling because the landlord or the person in control failed to pay for utilities it contracted for, and the "
  "landlord brings or maintains a proceeding to dispossess, or an action for rent, against a tenant of that building.",
  "The proceeding or action is stayed until the landlord pays what it owes for the utilities and the utilities are "
  "restored to working order. The landlord therefore does not sue for the balance while the shutoff lasts; utility "
  "bills the tenant paid in its place are credited against rent (NY:RPL-235-a).",
  Q(S, "In the event that utilities are discontinued in any part of a dwelling because of the failure of the landlord",
    "until such time as the utilities are restored to working order."),
  "major", "Step 8.10 before suing", dependencies=["NY:RPL-235-a"])]))

rows.append(D("NY:RPAPL 756-A", "no_decision",
  "Stays possession and title proceedings during deed-theft or title-fraud investigations and disputes; it does not "
  "reach a suit for a tenant's rent balance or the deposit, and who holds the rent claim is stated in Step 0.5."))

S = "NY:RPAPL 757"
rows.append(D(S, "new_rule",
  "Court records of a lessee removed after the building's mortgage or tax foreclosure are sealed and may not be used or "
  "disclosed; this limits what a landlord, collector or Handoff may report or use about that tenant.",
  proposed=[R("NY:RPAPL-757-foreclosure-eviction-sealed", S, "RPAPL 757", "landlord, manager, collector, Handoff", "must_not",
  "The tenant was removed from the unit in a summary proceeding, and the building was the subject of a mortgage "
  "foreclosure or tax foreclosure proceeding.",
  "The court records relating to that tenant are sealed and confidential; no disclosure or use of information "
  "relating to the tenant from those records is authorized, so it is not reported to a credit or tenant-screening "
  "bureau, shared with a collector as eviction history, or used in the settlement file beyond what the landlord "
  "itself holds independently of the records.",
  Q(S, "the court records relating to any such lessee shall be sealed and be deemed confidential",
    "and the use of such information shall be prohibited."),
  "major", "Step 8.7 credit reporting; Step 6.10 data at move-out", dependencies=["US:15USC1681s-2(a)(1)(A)"])]))

for s in ["NY:RPAPL 763", "NY:RPAPL 765", "NY:RPAPL 767"]:
    rows.append(D(s, "no_decision",
      "Redemption of a long lease (unexpired term over five years) after a nonpayment warrant; restores possession and "
      "fixes nothing in a market-rate move-out settlement."))
for s in ["NY:RPAPL 770", "NY:RPAPL 773", "NY:RPAPL 774", "NY:RPAPL 775", "NY:RPAPL 777", "NY:RPAPL 779"]:
    rows.append(D(s, "no_decision",
      "Article 7-A proceeding mechanics (grounds, pleading, trial, defenses, owner's repair option, accounts); the "
      "article's settlement effect, rent payable to the administrator, is stated by NY:RPAPL-776-778-administrator."))
for s in ["NY:RPAPL 796-B", "NY:RPAPL 796-C", "NY:RPAPL 796-E", "NY:RPAPL 796-F", "NY:RPAPL 796-G"]:
    rows.append(D(s, "excluded_regime",
      "Article 7-C rent-deposit proceeding; RPAPL 796-A(4) makes the article inapplicable in New York City (outside NYC)."))

save(rows)
