import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:RPAPL 1321", "Default and reference to compute in foreclosure; mortgage procedure."),
  ("NY:RPAPL 1331", "Notice of pendency before a foreclosure judgment of sale; mortgage procedure."),
  ("NY:RPAPL 1341", "Payment into court by a mortgagor to stop foreclosure; mortgage enforcement."),
  ("NY:RPAPL 1351", "Judgment of foreclosure and sale; the tenant's rights and payee after the sale are stated by NY:RPAPL-1305-successor."),
  ("NY:RPAPL 1354", "Distribution of foreclosure-sale proceeds among lienors; not a tenant settlement."),
  ("NY:RPAPL 1371", "Deficiency judgment against the mortgagor and application of the receiver's surplus to the mortgage debt; rents the receiver collects from tenants are stated by NY:CPLR-6401-foreclosure-receiver, and this changes nothing a tenant owes or is owed."),
  ("NY:RPAPL 1392", "Municipal proceeding compelling mortgagees of abandoned property to foreclose; mortgage enforcement."),
  ("NY:RPAPL 201", "Naming the State tax commission as defendant in real property actions; not a tenant settlement."),
  ("NY:RPAPL 202-A", "Pleading a city's interest in actions affecting real property; not a tenant settlement."),
  ("NY:RPAPL 232", "Bars officers conducting judicial sales from purchasing; not a tenant settlement."),
  ("NY:RPAPL 625", "Ejectment by a reversioner after a life tenant's or termor's default; not a market-rate settlement."),
  ("NY:RPAPL 633", "Ejectment between co-owners requires proof of ouster; co-owners of title, not co-tenants under a lease."),
  ("NY:RPAPL 641", "Contents of an ejectment complaint; possession procedure."),
  ("NY:RPAPL 653", "Ejectment judgment states the plaintiff's estate; possession procedure."),
  ("NY:RPAPL 661", "Liability of a purchaser pending an ejectment action for unsatisfied damages; not a tenant settlement."),
  ("NY:RPAPL 701", "Courts and venue for summary proceedings to recover possession; possession procedure that fixes no settlement amount."),
  ("NY:RPAPL 715", "Neighbours and enforcement agencies may compel removal of an occupant using premises for illegal business, with penalties; the lease's end on illegal use is proposed at RPL 231 (NY:RPL-231-illegal-use-and-exempt-pledge), and this adds no settlement amount or payee."),
  ("NY:RPAPL 769", "Court and venue for the article 7-A proceeding; its settlement effect is stated by NY:RPAPL-776-778-administrator."),
  ("NY:RPAPL 772", "Contents of the article 7-A petition; its settlement effect is stated by NY:RPAPL-776-778-administrator."),
]:
    rows.append(D(s, "no_decision", r))
rows.append(D("NY:RPAPL 713-A", "excluded_regime",
  "Termination of adult home and residence-for-adults admission agreements under SSL 461-h; a licensed care facility, not a market-rate tenancy."))
rows.append(D("NY:RPAPL 796-A", "excluded_regime",
  "Article 7-C jurisdiction; subdivision 4 makes article 7-C inapplicable in New York City (outside NYC)."))
save(rows)
