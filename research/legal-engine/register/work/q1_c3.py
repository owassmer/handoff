import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
rows.append(D("NY:9 NYCRR 2200.3", "excluded_regime",
  "Definitions and rent-receipt rules of the NYC Rent and Eviction Regulations (9 NYCRR Part 2200); they govern "
  "rent-controlled units only (rent control)."))
rows.append(D("NY:9 NYCRR 466.13", "stated",
  "The equal-treatment rule already lists gender identity or expression and sex; 466.13 only confirms that reach "
  "(and that gender dysphoria is a disability), which NY:EXEC-296(5)(a)(2)-terms and the disability accommodation "
  "rules cover.", ["NY:EXEC-296(5)(a)(2)-terms", "US:42USC3604(f)(3)(B)"]))

S = "NY:9 NYCRR 466.14"
rows.append(D(S, "partial",
  "The equal-treatment rule states the protected classes of the tenant; 466.14 extends it to adverse treatment because "
  "of the tenant's known relationship or association with a member of a protected class.",
  ["NY:EXEC-296(5)(a)(2)-terms"], [R(
  "NY:9NYCRR-466.14-association", S, "9 NYCRR 466.14(c)", "landlord, manager, Handoff, collector", "must_not",
  "A settlement decision (deduction, damage assessment, pursuit, reporting or write-off of a balance) on a New York "
  "tenancy.",
  "The decision may not treat the tenant worse because of the tenant's known relationship or association with a "
  "member of a class protected by the Human Rights Law (a spouse, partner, roommate, child, guest or friend of a "
  "given race, disability, national origin, etc.). A tenant subjected to such an adverse action is aggrieved and may "
  "complain under Exec. Law 297 (NY:EXC-297(9)-remedies).",
  Q(S, "(1) Where the term \"unlawful discriminatory practice\" is used in the Human Rights Law",
    "covered under the relevant provisions of the Human Rights Law."),
  "minor", "Step 5.10 equal treatment", determinacy="MIXED", judgment_terms=["because of", "known relationship or association"],
  dependencies=["NY:EXEC-296(5)(a)(2)-terms"], amends="NY:EXEC-296(5)(a)(2)-terms")]))

rows.append(D("NY:9 NYCRR 466.3", "no_decision",
  "Posting of Human Rights Law notices at buildings, brokers' offices and lenders; it changes no settlement decision."))
rows.append(D("NY:9 NYCRR 466.8", "no_decision",
  "Governs creditors' inquiries and credit-history attribution under Exec. Law 296-a; a landlord settling a lease "
  "balance extends no credit (NY:ADJ-lease-balance-not-consumer-credit)."))

S = "NY:ABP 1312"
rows.append(D(S, "partial",
  "The 1315 refund-reporting rule is stated; 1312 extends it to an owner entity chartered elsewhere and not authorized "
  "in New York when the tenant's last known address is in New York, without publication.",
  ["NY:ABP-1315(2)", "NY:OSC-MS11-refunds-due"], [R(
  "NY:ABP-1312-foreign-holder", S, "ABP 1312(1)-(3)", "landlord (foreign entity)", "must",
  "The deposit refund is held by an owner entity (corporation, LLC, trust, association or individual in business) "
  "organized under another state's law and not authorized to do business in New York, the refund stays unclaimed for "
  "the ABP 1315 period, and the tenant's last known address on the owner's records is in New York.",
  "The unclaimed refund is abandoned property and is paid or delivered to the State Comptroller on the same dates and "
  "in the same manner as ABP 1315 requires (NY:ABP-1315(2)); the publication otherwise required does not apply. It "
  "ceases to be abandoned once the tenant's right to the refund is established to the holder's satisfaction and it "
  "is paid.",
  Q(S, "1. Any amounts or securities defined as abandoned property by articles three",
    "shall be deemed abandoned property."),
  "major", "Step 6.8 unclaimed refund", dependencies=["NY:ABP-1315(2)"])]))

rows.append(D("NY:ABP 1403", "no_decision",
  "The Comptroller's sale of abandoned property after delivery; nothing the landlord or tenant does in the settlement "
  "turns on it."))

S = "NY:ABP 1404"
rows.append(D(S, "new_rule",
  "No rule states that paying the unclaimed refund to the Comptroller discharges the landlord; 1404 does, and bars "
  "suits against the holder for the property or later interest.",
  proposed=[R("NY:ABP-1404-holder-discharged", S, "ABP 1404(2), (3), (4), (5)", "landlord", "may",
  "The landlord (or its broker-escrow holder) has reported and paid a former tenant's unclaimed deposit refund to the "
  "State Comptroller under ABP 1315 or 1312.",
  "From the payment the landlord is relieved of all liability for any existing or later claim to that refund. No "
  "action lies against it or its officers to recover the refund paid, for interest on it after the date of the report, "
  "or for damages from the payment; the former tenant claims from the Comptroller. If the landlord paid the "
  "Comptroller money it was not required to pay (mistake of fact, calculation or law), the Comptroller may refund it "
  "within six years unless already paid to a claimant, and until refunded it is treated as abandoned property.",
  Q(S, "2. Any person, copartnership, unincorporated association or corporation making a payment of or delivering abandoned property",
    "on account of or in respect of any such abandoned property."),
  "critical", "Step 6.8 unclaimed refund", dependencies=["NY:ABP-1315(2)", "NY:ABP-1400-1412-reporting"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "3. No action shall be maintained against any person",
                  "damages alleged to have resulted from any such payment or delivery.")}],
  reasoning="Subdivision 3 bars the tenant's action for the refund and for interest after the report date.")]))

save(rows)
