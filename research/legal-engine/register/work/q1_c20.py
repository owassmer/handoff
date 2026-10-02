import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:MDL 57", "Doorbells kept working and mail delivery arranged; building service with no settlement consequence."),
  ("NY:MDL 62", "Parapets, guard rails and roof wires; building standards with no settlement consequence."),
  ("NY:MDL 64", "Lighting fixtures, gas meters and appliance venting; building standards with no settlement consequence."),
  ("NY:MDL 75", "Owner's duty to supply water (hot and cold); a failure enters the settlement only through the habitability offset (NY:RPL-235-b) and the stays for dangerous conditions, which state that consequence."),
  ("NY:MDL 77", "Plumbing and drainage duties; the owner's repair duty and its allocation are stated by MDL 78 (proposed NY:MDL-78-repair-allocation) and habitability (NY:RPL-235-b)."),
  ("NY:MDL 83", "Resident janitor for buildings of thirteen or more families; no settlement consequence."),
  ("NY:RPAPL 121", "New York jurisdiction over actions on real property outside the state; the units in this chain are in New York City."),
  ("NY:RPAPL 1302", "Pleading and defenses in foreclosure of one-to-four family home mortgages; mortgage enforcement, not a tenant settlement."),
  ("NY:RPAPL 1302-A", "Standing defense in home-loan foreclosure; mortgage enforcement."),
  ("NY:RPAPL 1306", "Lender filings with DFS before foreclosure; mortgage enforcement."),
  ("NY:RPAPL 1310", "Lender registry of vacant and abandoned property; mortgage enforcement."),
  ("NY:RPAPL 1311", "Necessary defendants in foreclosure (including tenants for years); a tenant's rights and the payee after a foreclosure sale are stated by NY:RPAPL-1305-successor and NY:CPLR-6401-foreclosure-receiver, which this does not change for the settlement."),
  ("NY:RPAPL 1312", "Trustees and executors as representative defendants in foreclosure; mortgage procedure."),
  ("NY:RPAPL 1313", "Permissible defendants in foreclosure; mortgage procedure."),
]:
    rows.append(D(s, "no_decision", r))
save(rows)
