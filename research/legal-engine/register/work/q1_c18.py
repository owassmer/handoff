import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
rows.append(D("NY:MDL 3", "stated",
  "Makes the MDL apply in New York City and lets the city impose and collect liens on rents; the stated MDL rent bars "
  "and the HPD rent levy depend on this reach and state its consequences.",
  ["NY:MDL-4(7)-multiple-dwelling", "NY:MDL-301(1)", "NY:MDL-302(1)(b)", "NYC:HMC-27-2147-rent-levy"]))
for s, r in [
  ("NY:MDL 302-B", "A foreclosing mortgagee's advances to a receiver for repairs; mortgage and receivership finance, not the tenant's account."),
  ("NY:MDL 306", "The city's enforcement actions and orders under the MDL; no settlement amount or payee turns on them."),
  ("NY:MDL 309-A", "Bars building staff from living in units that may not lawfully be rented; not a settlement matter."),
  ("NY:MDL 31", "Room sizes and sleeping-room occupancy limits; building standards with no settlement consequence."),
  ("NY:MDL 32", "Alcove standards; building standards with no settlement consequence."),
  ("NY:MDL 33", "Kitchen and kitchenette standards; building standards with no settlement consequence."),
]:
    rows.append(D(s, "no_decision", r))

S = "NY:MDL 328"
rows.append(D(S, "partial",
  "The rent bars for rent-impairing violations and non-registration are stated; 328(3) decides how they are proved in "
  "the Housing Part: HPD's computerized violation and registration files are prima facie evidence and judicially noticed.",
  ["NY:MDL-302-a(3)", "NY:MDL-325(2)"], [R(
  "NY:MDL-328-violation-files-evidence", S, "MDL 328(3)", "landlord; former tenant", "may",
  "In an action or proceeding before the Housing Part of the NYC Civil Court, a party relies on the building's "
  "violations, their correction, or the owner's registration (for the rent bars, habitability offsets or the "
  "petition's registration plea).",
  "HPD's displayed or printed computerized violation files and related housing data (including the owner's name, "
  "address and registration status) are prima facie evidence of what they state, and the court takes judicial "
  "notice of them as if certified. The landlord therefore checks those files before keeping rent or suing, since "
  "they will be taken as true unless rebutted.",
  Q(S, "shall be prima facie evidence of any matter stated therein and the courts shall take judicial notice thereof"),
  "minor", "Step 0.5 can rent be recovered; Step 8.10 before suing",
  dependencies=["NY:MDL-302-a(3)", "NY:MDL-325(2)", "NY:22NYCRR-208.42(g)-registration-plea"])]))
save(rows)
