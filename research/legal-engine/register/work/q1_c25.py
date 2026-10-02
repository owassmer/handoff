import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s in ["NY:9 NYCRR 2200.17", "NY:9 NYCRR 2200.4"]:
    rows.append(D(s, "excluded_regime", "NYC Rent and Eviction Regulations (9 NYCRR Part 2200) for controlled units (rent control)."))
for s in ["NY:9 NYCRR 2520.2", "NY:9 NYCRR 2520.3", "NY:9 NYCRR 2520.4", "NY:9 NYCRR 2520.8"]:
    rows.append(D(s, "excluded_regime", "Rent Stabilization Code adoption, construction and administration (9 NYCRR Part 2520); applies only to stabilized units (rent stabilization)."))
for s, r in [
  ("NY:9 NYCRR 466.10", "The Division of Human Rights' procedure for declaratory rulings; no settlement act turns on it."),
  ("NY:9 NYCRR 466.16", "Duty of voucher-administering agencies to notify recipients of source-of-income protections; it binds program administrators, not the landlord, and equal treatment by source of income in settlement is stated (NY:EXEC-296(5)(a)(2)-terms)."),
  ("NY:9 NYCRR 466.7", "The Division of Human Rights' FOIL procedure; not a settlement matter."),
  ("NY:9 NYCRR 540.1", "Purpose and scope of the ESRA regulations; the operative effect of electronic records and signatures is stated (NY:STT-305(3), NY:STT-307)."),
]:
    rows.append(D(s, "no_decision", r))
rows.append(D("NY:9 NYCRR 540.5", "stated",
  "An electronic record used by a person has the force of a paper record; stated by the ESRA rules the settlement "
  "already relies on for electronic statements and notices.", ["NY:STT-305(3)", "NY:STT-307", "NY:ADJ-statement-electronic"]))
save(rows)
