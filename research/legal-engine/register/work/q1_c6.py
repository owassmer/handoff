import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
rows.append(D("NY:GOL 5-903", "no_decision",
  "Automatic renewal of contracts for service, maintenance or repair; a residential lease is governed by GOL 5-905 "
  "(stated), and no settlement step turns on a service contract's renewal."))

S = "NY:MDL 15"
rows.append(D(S, "new_rule",
  "The owner's emergency contact list may be used only for emergency evacuation; using it to reach a departed tenant "
  "for the statement, refund or a balance is barred. No rule states this data limit.",
  proposed=[R("NY:MDL-15-emergency-list-use", S, "MDL 15(1)-(3)", "owner, managing agent, Handoff", "must_not",
  "The owner or agent of a multiple dwelling holds an emergency contact list of residents (kept with each resident's "
  "specific written consent, updated on each new lease, renewal or amendment), and needs a departed tenant's contact "
  "details for the move-out statement, refund or collection.",
  "The list is kept only for emergency evacuation; the owner or agent may not use, access or disseminate it for any "
  "other purpose, so it is not a source for the statement's delivery channel, skip-tracing, or a collector hand-off. "
  "Contact details the tenant gave in the lease file, the application or correspondence are used under the delivery "
  "rules (NY:ADJ-provide-address-branches). No resident appears on the list without specific, informed written "
  "consent obtained at each update, after written notice that the owner keeps the list and of the effect of opting "
  "out.",
  Q(S, "3. Such list of names and contact information shall only be maintained for the purpose of an emergency evacuation",
    "for any other purposes."),
  "major", "Step 6.5 where to send it; Step 6.10 data at move-out", dependencies=["NY:ADJ-provide-address-branches"])]))

rows.append(D("NY:MDL 290", "no_decision",
  "Basement and cellar legalization program: certification and a right of first refusal to return after legalization; "
  "it fixes nothing in a market-rate move-out settlement."))
rows.append(D("NY:MDL 304", "no_decision",
  "Criminal and civil penalties payable to the city for MDL violations; the rent consequences of those violations are "
  "stated separately (NY:MDL-302(1)(b), NY:MDL-302-a(3), NY:MDL-325(2)) and these penalties change no settlement amount."))
rows.append(D("NY:MDL 307", "no_decision", "Lien for MDL fines owed to the city; no settlement amount or payee turns on it."))
rows.append(D("NY:MDL 308", "no_decision", "Notice of pendency in the city's MDL enforcement actions; no settlement step turns on it."))

S = "NY:MDL 326"
rows.append(D(S, "partial",
  "The rent-impairing violation bar runs from notice to the owner (NY:MDL-302-a(3)); 326 decides when that notice is "
  "validly served, by posting plus mailing to the registered address.",
  ["NY:MDL-302-a(3)", "NY:MDL-325(2)"], [R(
  "NY:MDL-326-service-on-owner", S, "MDL 326(1), (2)", "landlord", "must",
  "The landlord's rent claim depends on whether and when the owner received a city notice or order on the building "
  "(for example the six months after notice of a rent-impairing violation).",
  "A notice or order is served five days before the time for compliance. Posting it in a conspicuous place in the "
  "dwelling and mailing a copy within five days to each person registered with the department under MDL 325, at the "
  "registered address, is sufficient service; if no address is registered or personal service cannot be made with "
  "due diligence, posting on the premises plus registered mail to the last known address suffices. An owner that "
  "served this way cannot deny notice for the rent bar.",
  Q(S, "The posting of a copy of such notice, order or summons in a conspicuous place in such dwelling, together with the mailing of a copy thereof",
    "shall be sufficient service thereof, except as provided in subdivision three."),
  "minor", "Step 0.5 can rent be recovered", dependencies=["NY:MDL-302-a(3)", "NY:MDL-325(2)"])]))

rows.append(D("NY:MDL 37", "no_decision", "Hall lighting duty in multiple dwellings; it enters no charge, credit or deadline in the settlement."))
rows.append(D("NY:MDL 51-A", "no_decision", "Peephole duty in multiple dwellings; the owner's installation cost is never a tenant charge and no settlement step turns on it."))
rows.append(D("NY:MDL 68", "excluded_regime",
  "MDL 68(7) makes the section inapplicable in cities of one million or more; NYC detectors are governed by the "
  "Housing Maintenance Code (NYC:HMC-27-2045-detector-charge) (outside NYC)."))

S = "NY:MDL 78"
rows.append(D(S, "partial",
  "Deposit deductions for tenant-caused damage are stated (NY:GOL-7-108(1-a)(b)-refundable); MDL 78 allocates repair in a "
  "multiple dwelling: the owner keeps it in repair, and the tenant is liable only for conditions caused by its own "
  "wilful act or negligence or that of its household or guests.",
  ["NY:GOL-7-108(1-a)(b)-refundable", "NY:GOL-7-108(1-a)(b)-excluded-costs"], [R(
  "NY:MDL-78-repair-allocation", S, "MDL 78(1)", "landlord", "must",
  "A multiple-dwelling unit needs repair at move-out and the landlord considers charging it to the tenant.",
  "The owner is responsible for keeping every part of the dwelling in good repair, so the repair is the owner's cost "
  "unless the condition was caused by the wilful act, assistance or negligence of the tenant, a member of its family "
  "or household, or its guest; only then is it damage chargeable to the tenant (within "
  "NY:GOL-7-108(1-a)(b)-refundable). The landlord proves the causation (NY:GOL-7-108(1-a)(f)).",
  Q(S, "The owner shall be responsible for compliance with the provisions of this section; but the tenant also shall be liable",
    "or that of any member of his family or household or his guest."),
  "major", "Step 5.1 what the deposit may be kept for", determinacy="MIXED",
  judgment_terms=["wilful act", "negligence", "member of his family or household", "guest"],
  dependencies=["NY:GOL-7-108(1-a)(b)-refundable", "NY:GOL-7-108(1-a)(f)"])]))

rows.append(D("NY:MDL 79", "no_decision",
  "Heat standards for multiple dwellings; a heat failure enters the settlement only through the habitability offset "
  "(NY:RPL-235-b), which states that consequence."))

save(rows)
