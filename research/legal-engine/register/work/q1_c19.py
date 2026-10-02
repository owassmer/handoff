import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:MDL 34", "Construction and occupancy standards for cellar and basement rooms; whether a unit is lawfully occupied enters the chain through the certificate-of-occupancy rent bar (NY:MDL-301(1), NY:MDL-302(1)(b)) and the city cellar rule (NYC:HMC-27-2087-cellar-basement), which this does not change."),
  ("NY:MDL 35", "Entrance door glazing and entrance lighting; building standards with no settlement consequence."),
  ("NY:MDL 50-A", "Self-locking entrance doors and intercoms; the cost-recovery clause reaches only rent-controlled and redevelopment-company buildings, and a tenant's damage to the equipment is ordinary tenant damage already stated (NY:GOL-7-108(1-a)(b)-refundable)."),
  ("NY:MDL 50-C", "Tenants' right to run a lobby attendant service; no settlement charge, credit or deadline turns on it."),
  ("NY:MDL 52", "Stair construction and repair; building standards with no settlement consequence."),
  ("NY:MDL 53", "Fire-escape construction and maintenance; building standards with no settlement consequence."),
]:
    rows.append(D(s, "no_decision", r))
save(rows)
