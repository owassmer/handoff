import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:MDL 309"
rows.append(D(S, "partial",
  "The city layer's HPD receiver and rent levy are stated; MDL 309 is the state source for the same payee shifts: a "
  "nuisance receiver collects accrued and accruing rents, and after the department serves an expense order or "
  "judgment and demands it in writing, rent is paid to the department and its receipt counts as payment to the owner.",
  ["NYC:HMC-27-2135(c)-receiver-rents", "NYC:HMC-27-2147-rent-levy"], [R(
  "NY:MDL-309-receiver-and-rent-demand", S, "MDL 309(5), (7)", "owner, manager; tenant", "must",
  "Branch (a): a court appoints a receiver of the rents, issues and profits of the multiple dwelling under MDL 309(5) "
  "to remove a nuisance. Branch (b): the department serves on the tenant a copy of an order or judgment for MDL 309 "
  "expenses and demands in writing that rent be paid to it.",
  "(a) The receiver collects the accrued and accruing rents, including rent due and unpaid by a departing tenant, and "
  "applies them to the repairs and receivership; the owner and its manager stop collecting that rent. (b) The tenant "
  "must pay rent or compensation to the department, to the extent of the claim, as it becomes due; the department's "
  "receipt is effective as actual payment to the owner for every purpose, so the move-out account credits it as rent "
  "paid and no deduction or balance is taken for it. The owner remains liable for its own deposit and statement duties.",
  Q(S, "He shall collect the accrued and accruing rents, issues and profits of the dwelling"),
  "critical", "Step 0.5 who is owed the rent; Step 5.5a credits",
  dependencies=["NYC:HMC-27-2135(c)-receiver-rents", "NYC:HMC-27-2147-rent-levy"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S,
    "The receipt of the department for any sum so paid shall, in all suits and proceedings and for every purpose, be as effectual in favor of any person holding the same as actual payment of the amount thereof to the owner")}],
  reasoning="Subdivision 7 creates the rent demand and makes the department's receipt payment to the owner.")]))

rows.append(D("NY:MDL 26", "no_decision", "Height, bulk, yard and court standards for multiple dwellings; building standards with no settlement consequence."))
rows.append(D("NY:MDL 67", "no_decision",
  "Fire-safety standards for hotels and class A and B dwellings, and the bar on transient (under 30-day) use of class A "
  "units; the transient-use bar governs short-term rentals, not the settlement of a departing market-rate tenancy."))
rows.append(D("NY:MDL 76", "no_decision", "Water-closet and bath accommodations by class of dwelling; building standards with no settlement consequence."))
save(rows)
