import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:19 NYCRR 175.17"
rows.append(D(S, "partial",
  "Equal treatment in the settlement is stated; 175.17(b) adds that a finding of discrimination against a licensed "
  "broker or salesperson in licensed activity is presumptive untrustworthiness and grounds for licence revocation.",
  ["NY:EXEC-296(5)(a)(2)-terms", "NY:RPL-441-c-licence-discipline"], [R(
  "NY:19NYCRR-175.17(b)-broker-discrimination", S, "19 NYCRR 175.17(b)", "licensed broker or salesperson (manager)", "must_not",
  "A licensed broker or salesperson (a broker-manager, or Handoff staff acting as licensed salespersons) makes "
  "settlement decisions for the owner.",
  "It may not engage in any unlawful discriminatory practice under federal, state or local law; a finding by any "
  "agency or court that it did so in licensed activity is presumptive evidence of untrustworthiness and subjects it "
  "to discipline up to revocation under RPL 441-c.",
  Q(S, "(b) No real estate broker or salesperson shall engage in an unlawful discriminatory practice",
    "will subject such licensee to discipline, including a proceeding for revocation."),
  "minor", "Step 5.10 equal treatment; Step 8.6a state licensing", dependencies=["NY:RPL-441-c-licence-discipline"])]))

S = "NY:19 NYCRR 175.2"
rows.append(D(S, "new_rule",
  "Decides where money a broker-manager collects in the settlement goes: it is accounted for and remitted to the owner "
  "within a reasonable time.",
  proposed=[R("NY:19NYCRR-175.2-broker-remit", S, "19 NYCRR 175.2", "licensed broker (manager)", "must",
  "A licensed broker managing the unit collects money for the owner in the settlement (rent arrears, damage "
  "recoveries, a collected balance) that is not spent for the owner's account.",
  "It renders an account to the owner and remits the money within a reasonable time; failure is a licensing "
  "violation (NY:RPL-441-c-licence-discipline). Tenant deposit money it holds stays in its escrow under "
  "NY:19NYCRR-175.1-broker-escrow until applied or refunded under the statement.",
  Q(S, "A real estate broker shall, within a reasonable time, render an account to his client", "and unexpended for his account."),
  "minor", "Step 8.6a state licensing", determinacy="MIXED", judgment_terms=["within a reasonable time"],
  dependencies=["NY:19NYCRR-175.1-broker-escrow", "NY:RPL-441-c-licence-discipline"])]))

S = "NY:19 NYCRR 175.9"
rows.append(D(S, "new_rule",
  "Limits what a broker-manager may do about a tenancy's ending: it may not induce the tenant to break the lease to "
  "substitute a new lease with another principal.",
  proposed=[R("NY:19NYCRR-175.9-no-induced-breach", S, "19 NYCRR 175.9", "licensed broker (manager)", "must_not",
  "A licensed broker manages or leases the unit while a lease is running.",
  "It may not induce the tenant (or the owner) to break the lease for the purpose of substituting a new lease with "
  "another party; a tenant's early departure it induced is a licensing violation (NY:RPL-441-c-licence-discipline), "
  "and the inducement bears on whether the owner accepted a surrender (NY:CASE-Riverside-surrender-by-operation).",
  Q(S, "No real estate broker shall induce any party to a contract of sale or lease to break such contract",
    "a new contract with another principal."),
  "minor", "Step 3.3 leaving early", dependencies=["NY:RPL-441-c-licence-discipline"])]))

for s, r in [
  ("NY:19 NYCRR 175.26", "Where a broker posts its business sign in an apartment building; no settlement step turns on it."),
  ("NY:19 NYCRR 175.28", "Human Rights Law disclosure notice at first substantive contact with a prospective tenant or landlord; it arises at leasing, not settlement."),
  ("NY:9 NYCRR 466.12", "Instalment payment of Human Rights Law fines by small employers; employment, not tenancy."),
  ("NY:9 NYCRR 466.2", "Posting of Human Rights Law notices at places of public accommodation; not a tenancy settlement."),
]:
    rows.append(D(s, "no_decision", r))
for s in ["NY:9 NYCRR 2200.10", "NY:9 NYCRR 2200.12", "NY:9 NYCRR 2200.9"]:
    rows.append(D(s, "excluded_regime", "NYC Rent and Eviction Regulations (9 NYCRR Part 2200) on decontrol and withdrawal of controlled units (rent control)."))

save(rows)
