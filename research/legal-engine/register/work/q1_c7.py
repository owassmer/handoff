import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
rows.append(D("NY:MDL 80", "stated",
  "The owner's cleaning, vermin and repainting duties and their move-out allocation (owner's cost unless the tenant, its "
  "household or guests caused the condition) are stated by the painting, turnover and wear-and-tear rules.",
  ["NYC:PAINT-wear-and-tear", "NYC:HMC-27-2013(b)(2)", "NYC:HMC-27-2017.5-turnover", "NY:GOL-7-108(1-a)(b)-excluded-costs"]))
rows.append(D("NY:MDL 81", "no_decision", "Waste receptacles and removal duty; it fixes no settlement charge or credit."))
rows.append(D("NY:RPAPL 1301", "no_decision", "Election between suing on a mortgage debt and foreclosing; mortgage enforcement, not a tenant settlement."))
rows.append(D("NY:RPAPL 1303", "no_decision",
  "Notices the foreclosing lender gives mortgagors and tenants; the tenant's right to stay and the payee after a sale "
  "are stated by NY:RPAPL-1305-successor, and no landlord settlement act turns on the lender's notice."))
rows.append(D("NY:RPAPL 1307", "no_decision",
  "The foreclosing plaintiff's duty to maintain vacant or mortgagor-abandoned property and a tenant's right to enforce "
  "it against the plaintiff; it binds the lender, not the landlord's settlement."))
rows.append(D("NY:RPAPL 1309", "no_decision", "Expedited foreclosure of vacant and abandoned property; mortgage procedure."))
rows.append(D("NY:RPAPL 1320", "no_decision", "Summons notice in foreclosure of homes of three units or fewer; mortgage procedure."))

S = "NY:RPAPL 1325"
rows.append(D(S, "partial",
  "The foreclosure receiver's collection of rents and its limited deposit liability are stated; 1325(2-a) adds that the "
  "appointing order directs the owner to turn every security deposit over to the receiver, who holds it subject to "
  "court order under GOL 7-105, which moves custody and the refund.",
  ["NY:CPLR-6401-foreclosure-receiver", "NY:GOL-7-108(2)(e)", "NY:GOL-7-105(1)"], [R(
  "NY:RPAPL-1325(2-a)-receiver-deposits", S, "RPAPL 1325(2-a), (3)", "owner, managing agent", "must",
  "A receiver of rents is appointed in an action to foreclose a mortgage on the building, and the owner or its manager "
  "holds tenants' security deposits.",
  "The order of appointment directs the owner (or lessee) to turn all security deposits over to the receiver, who "
  "holds them subject to a further order of the court under GOL 7-105. From turnover the receiver holds the departing "
  "tenant's deposit; the statement and refund come from, or are made at the direction of, the receiver within the "
  "14 days, and the receiver's liability is limited as NY:GOL-7-108(2)(e) states. A deposit the owner failed to turn "
  "over stays the owner's liability. In NYC the receiver of a multiple dwelling registers with HPD and spends rents "
  "first on correcting hazardous violations.",
  Q(S, "2-a. Where a receiver has been appointed, the order of appointment shall direct the owner or lessee",
    "in accordance with the provisions of section 7-105 of the general obligations law."),
  "critical", "Step 0.5 who is owed the rent; Step 2.1 building sold",
  dependencies=["NY:CPLR-6401-foreclosure-receiver", "NY:GOL-7-108(2)(e)", "NY:GOL-7-105(1)"])]))

save(rows)
