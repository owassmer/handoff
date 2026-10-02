import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:RPL 274-A", "Mortgagee's payoff certificate and mortgage documents; a mortgage rule, not the tenant settlement."),
  ("NY:RPL 280-D", "Reverse-mortgage foreclosure conditions; a mortgage rule."),
  ("NY:RPL 282", "Reciprocal attorneys' fees for mortgagors in foreclosure; the tenant's reciprocal fee right is stated (NY:RPL-234)."),
  ("NY:RPL 283", "Caps on flood insurance a mortgagee may require; a mortgage rule."),
  ("NY:RPL 443-A", "HIV status or a death or felony on the premises is not a material fact to disclose in a sale or lease; it arises at leasing, not in the departing tenancy's settlement."),
  ("NY:19 NYCRR 175.7", "A broker discloses whom it represents and takes compensation from more than one party only with its client's consent; fees a broker-manager may take from the tenant are governed by the stated FARE rules (NYC:FARE-20-699.21-agent-fee-ban) and fee-split rule (NY:RPL-442-fee-split)."),
  ("NY:23 NYCRR 1.7", "Effective date of 23 NYCRR Part 1 (2014-2015); the Part does not reach a lease balance (NY:23NYCRR-1.1(d)-not-lease)."),
]:
    rows.append(D(s, "no_decision", r))
rows.append(D("NY:STT 306", "stated",
  "Electronic records and signatures are admissible under CPLR article 45; the stated ESRA rules already give them "
  "the force of paper in proving the statement, notices and releases.",
  ["NY:STT-305(3)", "NY:STT-307"]))
rows.append(D("NY:STT 308", "no_decision",
  "Confidentiality duties of electronic-signature authenticators and FOIL treatment of government e-records; no landlord, manager or Handoff settlement act turns on it."))
for s in ["NY:9 NYCRR 2200.11", "NY:9 NYCRR 2200.16"]:
    rows.append(D(s, "excluded_regime", "NYC Rent and Eviction Regulations (9 NYCRR Part 2200) for controlled units (rent control)."))

S = "NY:16 NYCRR 96.1"
rows.append(D(S, "partial",
  "Definitions on which NY:16NYCRR96-submetering depends; the rate-cap definition fixes the maximum submetered charge, "
  "which no stated rule gives.",
  ["NY:16NYCRR96-submetering"], [R(
  "NY:16NYCRR-96.1(i)-rate-cap", S, "16 NYCRR 96.1(i), (j), (l)", "landlord (submeterer)", "must",
  "The final account carries submetered electricity billed by the owner (the submeterer, or a billing agent acting "
  "for it) to the unit's resident.",
  "The charge for each billing period may not exceed the rate cap: the distribution utility's delivery and commodity "
  "rates and charges for that period to similarly situated direct-metered residential customers, unless the PSC set a "
  "different cap under 96.2(a) or reduced it under 96.8; where the resident is billed on time-of-use, the cap is "
  "computed on the average annual residential rate. Any amount above the cap is not charged or kept "
  "(NY:16NYCRR-96.6-submeter-charge-limits). A billing agent that arranges submeters and bills for the owner is the "
  "submeterer's agent, so the owner answers for its bills.",
  Q(S, "(i) Rate cap. The maximum rate, calculated in each billing period",
    "the maximum rate for purposes of calculating the rate cap shall be the average annual residential rate."),
  "critical", "Step 5.5a credits and owner costs", dependencies=["NY:16NYCRR96-submetering"],
  amends="NY:16NYCRR96-submetering")]))
save(rows)
