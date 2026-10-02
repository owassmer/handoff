import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s in ["NY:RPAPL 796-D", "NY:RPAPL 796-I", "NY:RPAPL 796-K"]:
    rows.append(D(s, "excluded_regime", "Article 7-C rent-deposit proceeding; RPAPL 796-A(4) makes article 7-C inapplicable in New York City (outside NYC)."))
for s in ["NY:RPAPL 797-B", "NY:RPAPL 797-F", "NY:RPAPL 797-G"]:
    rows.append(D(s, "excluded_regime", "Article 7-D tenant repair proceeding; RPAPL 797(3) bars it in the five New York City counties (outside NYC)."))
for s, r in [
  ("NY:RPAPL 817", "Waste action between co-owners of title with partition; co-owners, not lease co-tenants."),
  ("NY:RPAPL 841", "Common-law nuisance action; no settlement amount or payee turns on it."),
  ("NY:RPAPL 843", "Spite fences over ten feet as private nuisance; not a tenancy settlement."),
  ("NY:RPL 251", "No covenants implied in conveyances; governs deeds, not leases or the settlement."),
  ("NY:RPL 252", "Abolition of lineal and collateral warranties; governs conveyances."),
  ("NY:RPL 254-A", "Prepayment fees on owner-occupied home mortgages on transfer; a mortgage rule."),
  ("NY:RPL 254-C", "Borrower's right to a copy of the lender's appraisal or consumer report; a mortgage rule."),
  ("NY:RPL 254-D", "Bars mortgagee fees for direct payment of taxes; a mortgage rule."),
  ("NY:RPL 257", "Covenants in grants and mortgages bind successors; deed and mortgage covenants, while the successor landlord's position on the lease and deposit is stated (NY:RPL-223, NY:GOL-7-105(2)-transfer-effect, NY:GOL-7-108(2)(a))."),
]:
    rows.append(D(s, "no_decision", r))
rows.append(D("NY:RPL 233-B", "excluded_regime", "Rent increases in manufactured home parks; a manufactured-home park tenancy, not an NYC market-rate dwelling lease."))
rows.append(D("NY:RPL 233-C", "excluded_regime", "Renewal of residential cooperative ground leases by the cooperative corporation; a commercial ground lease, not a dwelling tenancy."))
save(rows)
