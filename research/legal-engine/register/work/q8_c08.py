import sys; sys.path.insert(0, "register/work")
from q8_lib import D, save
N = "no_decision"
save([
 D("NY:RPL 441-A", N, "Broker licence form, office, display, two-year term, address-change suspension and a deceased broker's estate use; whether a collector holds a valid licence is a fact the existing licensing rules (NY:RPL-440(1)-rent-collection, NY:RPL-442-d-442-e-unlicensed) already test, and these mechanics add no settlement step."),
 D("NY:RPL 441-B", N, "Licence fees and which officer or member a corporate, partnership or LLC broker licence covers; licensing administration, the rent-collection licence rule is stated in NY:RPL-440(1)-rent-collection."),
 D("NY:RPL 441-D", N, "A salesperson's licence is suspended with its broker's; a licence-status fact already tested under NY:HANDOFF-broker-config-under-broker, no new step."),
 D("NY:RPL 441-E", N, "Department of State hearing procedure for licence denial and discipline; administrative procedure."),
 D("NY:RPL 442-A", N, "Salespersons take compensation only through their broker for appraising, buying, selling, exchanging, leasing, renting or loan negotiation; the same list in RPL 442 is construed in NY:RPL-442-fee-split not to include rent collection (Kreuter, strict construction), so it adds nothing to the rent-collection configurations."),
 D("NY:RPL 442-B", N, "Salesperson may not act after association ends until re-associated; a licence-status fact already covered by NY:HANDOFF-broker-config-under-broker."),
 D("NY:RPL 442-H", N, "Nonsolicitation orders, cease-and-desist zones and homebuyer operating procedures; sales practice, not tenancy settlement."),
 D("NY:RPL 442-I", N, "Composition of the State Real Estate Board; administrative."),
 D("NY:RPL 442-J", N, "Severability clause of the broker article; decides nothing."),
 D("NY:RPL 442-L", N, "After-the-fact referral fees in sales and buyer agency; not a tenancy settlement matter."),
 D("NY:SCPA 101", N, "Short title of the SCPA."),
 D("NY:SCPA 105", N, "Surrogate's courts may make local rules; decides nothing for the account."),
 D("NY:SCPA 106", N, "Official surrogate's court forms; decides nothing for the account."),
 D("NY:SCPA 107", N, "Electronic filing in surrogate's court; court procedure."),
 D("NY:SCPA 1101", N, "Continues the office of public administrator in the NYC counties; the public administrator's powers over a deceased tenant's refund are in the queue's SCPA 1112, 1115 and 1118 proposals."),
 D("NY:SCPA 1102", N, "Appointment and removal of NYC public administrators; administrative."),
 D("NY:SCPA 1105", N, "Public administrators' salaries; administrative."),
 D("NY:SCPA 1108", N, "Public administrator staff, counsel and offices; administrative."),
])
