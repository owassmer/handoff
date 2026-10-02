import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:GOL 5-325", "Garage operators may not exempt themselves from negligence liability; a parking operator's rule, while a residential lease's exculpation clause is governed by GOL 5-321 (proposed NY:GOL-5-321-exculpation-void)."),
  ("NY:GOL 5-526", "Usury exemption for secured corporate business loans of $100,000 or more; no payment plan on a tenant balance is such a loan."),
  ("NY:MDL 10", "Time for alterations after the MDL was adopted; historical compliance period with no current settlement effect."),
  ("NY:MDL 30", "Light and ventilation of rooms; building standards with no settlement consequence."),
  ("NY:MDL 303", "HPD enforces the MDL; no settlement amount or payee turns on it."),
  ("NY:MDL 305", "Misdemeanor for builders knowingly violating local construction laws; not a settlement matter."),
  ("NY:MDL 327", "HPD indexes MDL 325 registrations as public records; the registration consequence is stated (NY:MDL-325(2))."),
  ("NY:MDL 329", "HPD certificate of inspection visits posted in the building; no settlement consequence."),
  ("NY:MDL 51-B", "Mirrors in self-service elevators; building standard with no settlement consequence."),
  ("NY:MDL 55", "Wainscoting backing in multiple dwellings; building standard with no settlement consequence."),
  ("NY:MDL 59", "Bakeries and fat boiling in multiple dwellings; building standard with no settlement consequence."),
]:
    rows.append(D(s, "no_decision", r))
save(rows)
