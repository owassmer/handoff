import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:RPL 265", "Fraudulent intent in conveyances is a question of fact; conveyancing, not the tenant settlement."),
  ("NY:RPL 265-B", "Distressed property consultants for homeowners facing foreclosure; not a tenancy settlement, and Handoff does not consult homeowners on mortgage distress."),
  ("NY:RPL 267", "Conveyances revocable at the grantor's will are void against later purchasers; conveyancing."),
  ("NY:RPL 270", "Equity's power to compel specific performance on part performance is preserved; the settlement's lease writing rules are stated (NY:GOL-5-703-15-301-early-termination)."),
  ("NY:RPL 271", "Construction of covenants in mortgages of leaseholds; mortgage finance, not the tenant settlement."),
  ("NY:RPL 274", "Transfers and mortgages of interests in decedents' estates; the refund payee on a tenant's death is stated (NY:ADJ-tenant-death-payee)."),
]:
    rows.append(D(s, "no_decision", r))
save(rows)
