import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:GOL 5-1508"
rows.append(D(S, "new_rule",
  "Decides whether one of several agents named in the tenant's power may alone receive the refund or settle.",
  proposed=[R("NY:GOL-5-1508-co-agents", S, "GOL 5-1508(1), (2)", "landlord", "must",
  "The former tenant's power of attorney names two or more co-agents, or successor agents.",
  "Unless the power provides otherwise, co-agents act jointly: the landlord takes a release or pays the refund on the "
  "direction of all of them, except that one may act alone when prompt action is needed to avoid irreparable injury "
  "and another is temporarily unavailable, and the remaining agents act after a co-agent's death, resignation or "
  "incapacity. A successor agent has the initial agent's authority once the predecessor resigns, dies, becomes "
  "incapacitated, is unqualified or declines.",
  Q(S, "Unless the principal provides otherwise in the power of attorney, the co-agents must act jointly."),
  "minor", "Step 6 refund payee", dependencies=["NY:GOL-5-1501B-poa-validity"])]))

S = "NY:GOL 5-1511"
rows.append(D(S, "new_rule",
  "Decides whether a refund paid to, or a release taken from, the tenant's agent binds after the power ended: it does if "
  "the landlord acted in good faith without actual notice of the termination.",
  proposed=[R("NY:GOL-5-1511-termination-notice", S, "GOL 5-1511(1), (2), (5)(a)", "landlord", "may",
  "The landlord deals with the former tenant's agent under a power of attorney (receiving the refund, a release, a "
  "forwarding address) and the power or the agent's authority has ended: the tenant died, became incapacitated under "
  "a non-durable power, revoked it, the agent died, resigned or was divorced from the tenant, or the purpose was "
  "accomplished.",
  "Termination is not effective against a landlord that had not received actual notice of it and acted in good faith; "
  "its payment or dealing binds the tenant and its successors (the estate), so the landlord is discharged. After "
  "actual notice (for example of the tenant's death), the landlord deals only with the person then entitled "
  "(NY:ADJ-tenant-death-payee).",
  Q(S, "(a) Termination of an agent’s authority or of the power of attorney is not effective as to any third party who has not received actual notice of the termination and acts in good faith under the power of attorney.",
    "shall bind the principal and the principal’s successors in interest."),
  "major", "Step 6 refund payee; Step 2.5 tenant dies", determinacy="MIXED", judgment_terms=["actual notice", "good faith"],
  dependencies=["NY:ADJ-tenant-death-payee", "NY:GOL-5-1501A-durable-poa"])]))

S = "NY:GOL 5-1512"
rows.append(D(S, "new_rule",
  "A power of attorney executed elsewhere, valid where made, is valid in New York; this decides whether an out-of-state "
  "tenant's agent may act in the settlement.",
  proposed=[R("NY:GOL-5-1512-foreign-poa", S, "GOL 5-1512", "landlord", "may",
  "A former tenant's agent presents a power of attorney executed outside New York, or executed in New York by a "
  "non-domiciliary.",
  "It is valid in New York if it complies with the law of the place of execution (or with New York law), whatever the "
  "tenant's domicile; one executed elsewhere by a New York domiciliary is valid if it meets GOL 5-1501B. The landlord "
  "then deals with the agent within the authority the power grants.",
  Q(S, "a power of attorney executed in another state or jurisdiction in compliance with the law of that state or jurisdiction or the law of this state is valid in this state"),
  "minor", "Step 6 refund payee", dependencies=["NY:GOL-5-1501B-poa-validity"])]))

S = "NY:GOL 5-515"
rows.append(D(S, "new_rule",
  "Branch of the usury consequence: a tenant suing over a usurious payment plan need not first repay or tender anything.",
  proposed=[R("NY:GOL-5-515-no-tender", S, "GOL 5-515", "court; former tenant", "may",
  "The former tenant sues to recover or cancel what was taken under a usurious forbearance on its balance "
  "(NY:GOL-5-501-payment-plan-usury).",
  "It need not pay or offer to pay any principal or interest first, and the court may not require payment or deposit "
  "of any of it as a condition of relief.",
  Q(S, "it shall not be necessary for him to pay or offer to pay any interest or principal on the sum or thing loaned"),
  "minor", "Step 8.1b payments and settlements", dependencies=["NY:GOL-5-511-usurious-void"])]))

for s, r in [
  ("NY:GOL 5-322.1", "Voids indemnity for a promisee's own negligence in construction and repair contracts; it governs the landlord's contractors, not a charge to the tenant (NY:GOL-5-321-exculpation-void governs the lease)."),
  ("NY:GOL 5-332", "Unsolicited merchandise is a gift; not a tenancy settlement."),
  ("NY:GOL 5-517", "Transfer of a usury cause of action tied to security on specific property; no payment plan in this chain carries such security."),
  ("NY:GOL 5-523", "Interest on demand advances of $5,000 or more on documents of title or securities; not a tenant balance."),
  ("NY:GOL 5-524", "Misdemeanor of taking household goods as security for a usurious loan; the landlord takes no such security and may not hold belongings for rent (NY:COMMONLAW-belongings-owner-keeps)."),
  ("NY:GOL 5-531", "Loan brokerage fees; no loan is brokered in the settlement."),
  ("NY:GOL 5-601", "Interest on mortgage escrow accounts of owner-occupied homes and co-ops; not a tenant deposit."),
  ("NY:GOL 7-106", "Deposits on contracts for private sewer connections; not a tenant deposit."),
  ("NY:MDL 12", "Prohibited uses of multiple dwellings (prostitution, livestock, combustibles); no settlement amount or date turns on it."),
  ("NY:MDL 13", "Application of the MDL to dwellings existing in 1929; the certificate-of-occupancy consequences are stated at NY:MDL-301(1), and this changes no settlement step."),
  ("NY:MDL 14", "Application of the MDL to dwellings under construction in 1929; no current tenancy turns on it."),
  ("NY:MDL 289", "Enabling authority for NYC's basement and cellar legalization pilot; any effect on a tenancy comes from the local law adopted under it, in the NYC layer (NYC:HMC-27-2087-cellar-basement)."),
  ("NY:MDL 29", "Painting of courts and shafts; building maintenance with no settlement consequence."),
]:
    rows.append(D(s, "no_decision", r))

save(rows)
