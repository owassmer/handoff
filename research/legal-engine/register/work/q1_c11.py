import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:RPL 238", "Voids exclusive fuel, ice or food dealing privileges in apartment buildings; no settlement charge or credit turns on it."),
  ("NY:RPL 254-B", "Caps late charges on owner-occupied home mortgages and co-op loans; a mortgage rule, not a tenant charge."),
  ("NY:RPL 268", "Disaffirmance of a decedent's or insolvent's fraudulent transfers of real property; not a tenant settlement."),
  ("NY:16 NYCRR 96.4", "Submetering in cooperatives and condominiums billed to owners or shareholders; not a rental tenancy."),
  ("NY:19 NYCRR 175.12", "A broker delivers a copy of an instrument it prepared to the signers; it fixes nothing in the move-out settlement."),
]:
    rows.append(D(s, "no_decision", r))

S = "NY:RPL 248"
rows.append(D(S, "partial",
  "RPL 223 (pre-sale rent stays the seller's) is stated; 248 adds that rent the tenant paid the seller before notice of "
  "the sale binds the buyer, and the tenant is not liable to the buyer for lease breaches before notice.",
  ["NY:RPL-223", "NY:GOL-7-105(1)"], [R(
  "NY:RPL-248-payment-before-notice", S, "RPL 248", "successor landlord", "must",
  "The building was conveyed during the tenancy and the tenant paid rent to the former owner, or breached a lease "
  "condition, before the tenant had notice of the conveyance.",
  "The conveyance is valid without the tenant's attornment. Rent paid to the former owner before notice binds the "
  "buyer: the buyer's account credits it as paid and looks to the former owner for it. The tenant is not liable to "
  "the buyer for breach of any lease condition before notice. After notice, rent and charges falling due are paid to "
  "the buyer (NY:RPL-223).",
  Q(S, "But the payment of rent to a grantor, by his tenant, before notice of the conveyance, binds the grantee",
    "for the breach of any condition of the lease."),
  "critical", "Step 2.1 building sold", dependencies=["NY:RPL-223"])]))

S = "NY:RPL 259-C"
rows.append(D(S, "new_rule",
  "A lease jury waiver is void in suits between landlord and tenant for property damage or personal injury, which "
  "includes the landlord's suit for damage to the unit and the tenant's counterclaim for its property loss.",
  proposed=[R("NY:RPL-259-c-jury-waiver-void", S, "RPL 259-c", "landlord; former tenant", "may",
  "The landlord sues the former tenant for damage to the unit (or the tenant sues or counterclaims for injury or "
  "property damage), and the lease contains a jury-trial waiver.",
  "The waiver is void for any action, proceeding or counterclaim between the parties for personal injury or property "
  "damage, so either side may demand a jury on those claims. A waiver remains effective for claims that are neither "
  "(for example unpaid rent).",
  Q(S, "Any provision in a lease, executed after the effective date of this act, that a trial by jury is waived",
    "is null and void."),
  "minor", "Step 8.10 before suing")]))

rows.append(D("NY:STT 309", "stated",
  "Electronic records are voluntary unless law requires them; the stated rules already bar requiring electronic "
  "payment and fix when an electronic statement or notice is effective.",
  ["NY:STT-305(3)", "NY:STT-307", "NY:ADJ-statement-electronic", "NY:RPL-235-g", "US:15USC7001(c)-esign-consent"]))

rows.append(D("NY:16 NYCRR 96.3", "stated",
  "The procedure by which submetering is authorized; the settlement consequence (a submetered charge is lawful only "
  "under authorization, which survives a change of owner) is stated by NY:16NYCRR96-submetering.",
  ["NY:16NYCRR96-submetering"]))

S = "NY:16 NYCRR 96.5"
rows.append(D(S, "partial",
  "Submetering authorization is stated; 96.5(f)(3) requires the lease to credit submetering refunds to the residents "
  "affected, which reaches a departed tenant when a rebilling refund arrives after move-out.",
  ["NY:16NYCRR96-submetering"], [R(
  "NY:16NYCRR-96.5(f)-submeter-refund-credit", S, "16 NYCRR 96.5(f)", "landlord (submeterer)", "must",
  "Submetered electricity was billed to the tenant, and a submetering refund results from the submeterer's actions "
  "(PSC-ordered rebilling or overcharge credit), including one arriving after the tenant moved out.",
  "The lease must state in plain language the submetering complaint procedures, the residents' HEFPA rights and "
  "responsibilities, and that submetering refunds will be credited to the affected residents where the submeterer has "
  "their contact information; the landlord therefore credits or pays the refund to the former tenant (in the "
  "statement if known by then, otherwise by payment at the contact it holds).",
  Q(S, "(3) a provision stating that submetering refunds will be credited to submetered residents affected by the submeterer's actions",
    "provided that the submeterer has such contact information for such resident."),
  "minor", "Step 5.5a credits", dependencies=["NY:16NYCRR96-submetering"])]))

S = "NY:16 NYCRR 96.7"
rows.append(D(S, "partial",
  "Submetering authorization is stated; 96.7 conditions the accuracy of the charge and gives the resident a free "
  "meter test on complaint.",
  ["NY:16NYCRR96-submetering"], [R(
  "NY:16NYCRR-96.7-submeter-accuracy", S, "16 NYCRR 96.7(a)-(c)", "landlord (submeterer)", "must",
  "The final account carries submetered electricity and the tenant disputes the reading or amount.",
  "The charge rests on submeters meeting 16 NYCRR Parts 92 and 93 with a register or other means the resident can "
  "read, and any register multiplier shown on the bill; submeters found out of limits are corrected. A resident may "
  "have one test a year free on a complaint (further tests at the resident's cost if the meter proves within limits). "
  "A charge from a meter shown out of limits is recomputed before it is kept or pursued.",
  Q(S, "A recipient of submetered service may request and receive one submeter test at no cost during a 12-month period",
    "when the request is made pursuant to a consumer complaint."),
  "minor", "Step 5.5a credits and owner costs", dependencies=["NY:16NYCRR96-submetering"])]))

S = "NY:16 NYCRR 96.8"
rows.append(D(S, "partial",
  "Submetering authorization is stated; 96.8 adds the PSC's power to suspend the landlord's authority to bill and "
  "collect submetered charges, order rebilling or refunds, and cut the rate cap by up to 40%.",
  ["NY:16NYCRR96-submetering"], [R(
  "NY:16NYCRR-96.8-noncompliance", S, "16 NYCRR 96.8(a), (b)", "landlord (submeterer)", "must_not",
  "The PSC has acted on the landlord's failure to submeter in compliance with Part 96 (or Parts 92-93).",
  "While the PSC has rescinded, suspended, limited or stayed the landlord's authority to render bills to and collect "
  "from submetered residents, no submetered electricity is charged or kept from the deposit for that period. A "
  "PSC rebilling or refund order is applied to the final account, and a reduced rate cap (up to 40% lower, effective "
  "at least 20 days after the notice of reduction and tolled by a timely appeal) caps the charge for its period.",
  Q(S, "(1) rescinds, suspends, limits or stays the submeterer's authorization to submeter electricity",
    "or its authority to render bills to and collect payments from submetered residents;"),
  "major", "Step 5.5a credits and owner costs", dependencies=["NY:16NYCRR96-submetering"])]))

save(rows)
