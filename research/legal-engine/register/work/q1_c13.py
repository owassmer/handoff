import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:9 NYCRR 466.6", "The Division of Human Rights' own procedure for access to personal information in its records; not a settlement duty."),
  ("NY:9 NYCRR 540.6", "Confidentiality duties of certification authorities and FOIL treatment of government e-records; no landlord, manager or Handoff act turns on it."),
  ("NY:ABP 1300", "Surplus from sales of pledged property by licensed pawn lenders; not a deposit refund."),
  ("NY:ABP 1301", "Surplus from a pledgee's sale of pledged goods; a landlord holds no pledge and may not hold belongings for rent (NY:COMMONLAW-belongings-owner-keeps)."),
  ("NY:ABP 1304", "Property of persons discharged from state institutions; not a tenancy."),
  ("NY:ABP 1305", "Surplus held by public welfare officials after recovery of assistance costs; not a landlord holder."),
  ("NY:ABP 1309", "Uncashed travelers checks and money orders held by their issuers; a landlord's uncashed refund check is reported under ABP 1315 (NY:ABP-1315(2))."),
  ("NY:ABP 1311", "Taxes erroneously collected by utility corporations; not a landlord holder."),
  ("NY:ABP 1314", "Consumer credit balances transferable under GBL 715; a lease is not consumer credit (NY:ADJ-lease-balance-not-consumer-credit), so the deposit refund is reported under ABP 1315."),
  ("NY:ABP 1316", "Unclaimed non-life insurance proceeds held by insurers; not a landlord holder."),
]:
    rows.append(D(s, "no_decision", r))
rows.append(D("NY:9 NYCRR 540.4", "stated",
  "Electronic signatures have the same validity as handwritten ones; the stated ESRA rules already give electronic "
  "records and signatures in the settlement (a signed release, a forwarding address) full effect.",
  ["NY:STT-305(3)", "NY:STT-307"]))
save(rows)
