import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:GOL 5-1502A"
rows.append(D(S, "new_rule",
  "Decides what an agent under a statutory short-form 'real estate transactions' grant may do in the settlement: give "
  "notice and surrender the lease, and demand and receive the deposit refund, and settle claims arising from the lease.",
  proposed=[R("NY:GOL-5-1502A-agent-lease-authority", S, "GOL 5-1502A(2), (6), (10)", "landlord", "may",
  "The tenant (or an individual owner) acts through an agent holding a valid statutory short-form power "
  "(NY:GOL-5-1501B-poa-validity) that grants authority over 'real estate transactions'; the lease is an interest in "
  "land.",
  "The agent may surrender the lease (give the tenant's notice or sign an agreed early termination), demand and "
  "receive money to which the principal is entitled as proceeds of the interest in land (the deposit refund and "
  "interest), and prosecute, defend, settle or compromise claims involving the lease; the landlord may deal with and "
  "pay the agent on those matters. On the owner side, an individual owner's agent under the same grant may manage "
  "the property, demand rent and settle tenants' claims for the owner. A power not granting this authority, or the "
  "claims authority in NY:GOL-5-1502H-agent-claims-authority, does not permit the agent to do so.",
  Q(S, "To sell, to exchange, to convey either with or without covenants, to quit-claim, to release, to surrender",
    "or otherwise to dispose of, any estate or interest in land;"),
  "minor", "Step 3 how the tenancy ends; Step 6 refund payee", dependencies=["NY:GOL-5-1501B-poa-validity"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "To demand, to receive, to obtain by action, proceeding or otherwise, any money, or other thing of value to which the principal is",
                  "as the proceeds of an interest in land")}],
  reasoning="Subdivision 2 covers surrender of the lease; subdivision 6 receipt of money that is proceeds of the "
            "interest in land, which includes the security returned at the end of the lease.")]))

for s, r in [
  ("NY:GOL 5-1501", "Scope and definitions of the POA title; its operative effects on the settlement are carried in the rules proposed at GOL 5-1501B, 5-1502A, 5-1502H, 5-1507, 5-1511 and 5-1512."),
  ("NY:GOL 5-1502C", "Agent authority over bonds, shares and commodities; no settlement act involves them."),
  ("NY:GOL 5-1502D", "Agent authority over bank accounts; the landlord's dealing with a tenant's agent over the refund turns on the real-estate and claims grants (proposed at GOL 5-1502A and 5-1502H)."),
  ("NY:GOL 5-1502E", "Agent authority over business operations; no settlement act turns on it."),
  ("NY:GOL 5-1502F", "Agent authority over insurance; no settlement act turns on it."),
  ("NY:GOL 5-1502G", "Agent authority over estate transactions of which the principal is a beneficiary; the refund payee on a tenant's own death is stated (NY:ADJ-tenant-death-payee)."),
  ("NY:GOL 5-1502I", "Agent authority to provide living quarters and family maintenance; lease surrender, refund receipt and claims settlement are governed by the grants proposed at GOL 5-1502A and 5-1502H."),
  ("NY:GOL 5-1502J", "Agent authority over government and military benefits; no settlement act turns on it."),
  ("NY:GOL 5-1502K", "Agent authority over health-care matters; no settlement act turns on it."),
  ("NY:GOL 5-1502M", "Agent authority over tax matters; no settlement act turns on it."),
  ("NY:GOL 5-1502N", "'All other matters' grant; lease and refund matters fall under the specific grants proposed at GOL 5-1502A and 5-1502H."),
  ("NY:GOL 5-1503", "Modifications of the statutory short form; whether a given power covers the settlement is read from its grants (proposed at GOL 5-1502A and 5-1502H)."),
  ("NY:GOL 5-1509", "A principal's appointment of a monitor over the agent; no landlord act turns on it."),
  ("NY:GOL 5-1510", "Special proceedings about a power of attorney; a landlord may seek to compel acceptance or construction there, but no settlement amount, date or payee turns on it."),
]:
    rows.append(D(s, "no_decision", r))
save(rows)
