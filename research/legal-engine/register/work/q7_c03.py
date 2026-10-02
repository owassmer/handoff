import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = []
S = "NY:19 NYCRR 175.21"
rows.append(D(S, "partial",
  "Configuration 3 (Handoff's people collect rent as salespersons of the manager's broker) is stated as a licensing "
  "condition only; 175.21(a)-(b) adds what the association requires of the broker and salesperson: regular, frequent "
  "and consistent personal supervision of the collecting salespersons, and written records of the transactions they "
  "handle.",
  ["NY:HANDOFF-broker-config-under-broker", "NY:RPL-441-c-licence-discipline"], [R(
  "NY:19NYCRR-175.21-broker-supervision", S, "19 NYCRR 175.21(a), (b)", "licensed broker; associated salesperson",
  "must",
  "Configuration 3 applies: individuals (for example Handoff's people) collect or attempt to collect a rent balance "
  "as real estate salespersons associated with a licensed broker (for example the manager's brokerage).",
  "The broker supervises each such salesperson by regular, frequent and consistent personal guidance, instruction, "
  "oversight and superintendence of the brokerage business the salesperson conducts, including the collection work; "
  "a broker whose name the salespersons use without that supervision does not meet the association RPL 441(1)(d) "
  "requires, and the broker's licence is exposed under NY:RPL-441-c-licence-discipline. The broker and the "
  "salesperson each keep written records of every transaction the salesperson effects or assists with, sufficient to "
  "identify it and showing its dates.",
  Q(S, "(a) The supervision of a real estate salesman by a licensed real estate broker, required by subdivision 1(d)",
    "with respect to the general real estate brokerage business conducted by the broker, and all matters relating thereto."),
  "major", "Step 8.6a state licensing of whoever collects rent",
  dependencies=["NY:HANDOFF-broker-config-under-broker", "NY:RPL-441-c-licence-discipline"],
  amends="NY:HANDOFF-broker-config-under-broker")]))
rows += [
    D("NY:19 NYCRR 175.22", N, "A salesperson may not own voting stock of the brokerage corporation it is associated with; a corporate-structure rule that changes no collection, statement or payee step."),
    D("NY:19 NYCRR 175.23", N, "Broker record-keeping applies only to sales of one-to-four family homes, condominiums and co-ops; rentals and collections are outside it."),
    D("NY:19 NYCRR 175.24", N, "Mandatory explanation in exclusive sale listings of residential property; sales only."),
    D("NY:19 NYCRR 175.25", N, "Broker advertising rules cover promotion and solicitation of licensed activity (listing a unit for sale or lease); a settlement statement or balance letter is not an advertisement."),
    D("NY:19 NYCRR 175.27", N, "Disclaimer that Part 175 does not decide whether a salesperson is an employee or contractor; no effect on any rule in the chain."),
    D("NY:19 NYCRR 175.29", N, "Fair-housing notice posted at broker offices, on broker websites and at open houses; it arises at leasing and office display, while equal treatment in the settlement is stated at Step 5.10."),
    D("NY:19 NYCRR 175.4", N, "A broker buying property listed with it must disclose its position; sales only."),
    D("NY:19 NYCRR 175.5", N, "A broker buying property for a client discloses its ownership interest; sales only."),
    D("NY:19 NYCRR 175.6", N, "A broker selling property it has an interest in discloses it to the buyer; sales only."),
    D("NY:19 NYCRR 175.8", N, "A broker may not negotiate a sale or lease directly with an owner under another broker's exclusive; governs leasing, not the settlement."),
    D("NY:22 NYCRR 202.14", N, "Authorizes special masters in Supreme Court conferences; no party duty or step."),
    D("NY:22 NYCRR 202.16-a", N, "Automatic orders binding spouses in a matrimonial action; they bind the parties to the divorce, not a landlord refunding a deposit or collecting a balance."),
    D("NY:22 NYCRR 202.16-b", N, "Paper rules for contested matrimonial applications; outside any tenancy action."),
    D("NY:22 NYCRR 202.16-c", N, "Electronic filing rules for matrimonial actions; outside any tenancy action."),
]
save(rows)
