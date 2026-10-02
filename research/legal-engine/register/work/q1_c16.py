import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:GOL 3-112"
rows.append(D(S, "new_rule",
  "Gives the landlord a claim, capped at $5,000, against the parent of a child aged 10 to 17 who wilfully damaged the "
  "unit, which matters when the parent is not the tenant (a guest's or occupant's child).",
  proposed=[R("NY:GOL-3-112-parent-liability", S, "GOL 3-112(1)-(3)", "landlord", "may",
  "A child over 10 and under 18 wilfully, maliciously or unlawfully damaged, defaced or destroyed the unit or "
  "building (or unlawfully entered and took property), and the landlord seeks the loss from the child's parent or "
  "legal guardian (not the State, a social services department or a foster parent).",
  "The landlord may sue the parent or guardian for the damages, up to $5,000. Before judgment of $500 or more the "
  "parent may show financial inability to pay above $500, and the judgment is then set within its capacity but not "
  "below $500. Defenses: restitution already paid under the Family Court Act or Penal Law, or the child had "
  "abandoned the home without good cause; the parent's diligent supervision is not a defense. Where the parent is "
  "the tenant, the lease claim for tenant-caused damage (NY:GOL-7-108(1-a)(b)-refundable) applies without this cap.",
  Q(S, "In no event shall such damages portion of a judgment authorized by this section, as described in this subdivision, exceed the sum of five thousand dollars."),
  "major", "Step 8 collecting a balance", determinacy="MIXED",
  judgment_terms=["willfully, maliciously, or unlawfully", "financial inability", "without good cause"],
  dependencies=["NY:GOL-7-108(1-a)(b)-refundable", "NY:MDL-78-repair-allocation"])]))

S = "NY:GOL 3-305"
rows.append(D(S, "new_rule",
  "Decides who may be pursued: a married tenant's lease does not bind the non-signing spouse or the spouse's property.",
  proposed=[R("NY:GOL-3-305-spouse-not-bound", S, "GOL 3-305", "landlord, collector", "must_not",
  "The lease (or guaranty) was signed by one spouse only and the landlord seeks the balance from the other spouse.",
  "The contract made by the signing spouse does not bind the other spouse or that spouse's property; the landlord "
  "pursues the non-signing spouse only on an obligation that spouse itself undertook (its signature on the lease, a "
  "renewal or a written guaranty, NY:GOL-5-701(a)(2)-guaranty). Collection contacts may not tell the spouse it must "
  "pay the tenant's debt (NY:GBL-601-a-family).",
  Q(S, "A contract made by a married woman does not bind her husband or his property."),
  "major", "Step 8 collecting a balance", dependencies=["NY:GOL-5-701(a)(2)-guaranty", "NY:GBL-601-a-family"],
  reasoning="The section speaks of a married woman's contract; New York applies marital-status rules without regard to "
            "sex (Human Rights Law, NY:EXEC-296(5)(a)(2)-terms), and no rule of New York law makes one spouse a party "
            "to the other's lease by marriage.")]))

for s, r in [
  ("NY:GOL 3-307", "Liability for a spouse's antenuptial debts to the extent of property acquired by antenuptial contract; a move-out balance is not collected on that basis."),
  ("NY:GOL 3-313", "Married persons' tort actions and liability; a spouse is liable only for its own torts, and the balance is a lease claim."),
  ("NY:GOL 5-1113", "Written promises of a reward for lost property; not a settlement matter."),
  ("NY:GOL 5-1502B", "Construction of a statutory short-form power over chattels and goods; the refund and deposit claim fall under claims and litigation (proposed at GOL 5-1502H), not this grant."),
  ("NY:GOL 5-1505", "An agent's duties to its own principal; a landlord dealing with the agent is protected by the reliance rules, not this section."),
  ("NY:GOL 5-1506", "An agent's compensation from the principal; no settlement step turns on it."),
]:
    rows.append(D(s, "no_decision", r))

S = "NY:GOL 5-1109"
rows.append(D(S, "new_rule",
  "A written settlement offer stated to be irrevocable for a period cannot be withdrawn during it, which fixes how long "
  "a landlord's (or tenant's) written offer on the balance stays open.",
  proposed=[R("NY:GOL-5-1109-irrevocable-offer", S, "GOL 5-1109", "landlord; former tenant", "must",
  "The landlord (or the tenant) makes a written, signed offer to settle the balance or the deposit claim that states "
  "it is irrevocable for a period or until a time, or states it is irrevocable without a period.",
  "The offer cannot be revoked during the stated period (or, with no period stated, for a reasonable time) despite "
  "the absence of consideration; a timely acceptance or tender binds the offeror (NY:GOL-15-503-offer-of-accord). An "
  "agent signs such an offer affecting a lease of over one year only with written authority (NY:GOL-5-1111-agent-written-authority).",
  Q(S, "when an offer to enter into a contract is made in a writing signed by the offeror, or by his agent",
    "it shall be construed to state that the offer is irrevocable for a reasonable time."),
  "minor", "Step 8.1b payments and settlements", dependencies=["NY:GOL-15-503-offer-of-accord"])]))

S = "NY:GOL 5-1501B"
rows.append(D(S, "new_rule",
  "Decides whether a New York power of attorney presented by a tenant's agent (to receive the refund, dispute charges "
  "or settle) is valid and in effect.",
  proposed=[R("NY:GOL-5-1501B-poa-validity", S, "GOL 5-1501B(1), (3)", "landlord", "must",
  "A person presents a power of attorney executed in New York by the former tenant and asks to receive the statement "
  "or refund, or to settle, for the tenant.",
  "The power is valid only if printed in legible type of at least 12 points, signed and dated by the principal (or at "
  "its direction by a non-agent) with the signature acknowledged and witnessed by two non-agent, non-donee witnesses, "
  "signed by the agent with its signature acknowledged, and substantially containing the statutory 'Caution to the "
  "Principal' and 'Important Information for the Agent'. It takes effect as to an agent when the agent's signature is "
  "acknowledged, or later on a date or contingency the document states. The landlord deals with the agent only under "
  "a power meeting these terms (or one valid where executed, GOL 5-1512).",
  Q(S, "1. To be valid, except as otherwise provided in section 5-1512 of this title, a statutory short form power of attorney, or a non-statutory power of attorney, executed in this state by a principal, must:"),
  "minor", "Step 6 refund payee", dependencies=["NY:GOL-5-1507-agent-signature"])]))

S = "NY:GOL 5-1501C"
rows.append(D(S, "new_rule",
  "The owner's grant of authority to a licensed broker-manager over leases and management is outside the POA title, so "
  "the management agreement need not meet POA formalities; this decides how a manager's written authority "
  "(NY:GOL-5-1111-agent-written-authority) is shown.",
  proposed=[R("NY:GOL-5-1501C-broker-management-power", S, "GOL 5-1501C(9), (4), (1)", "managing agent", "may",
  "The owner authorizes a licensed real estate broker (or a manager acting through one) to act on leases, management "
  "and settlement, or gives a business power for a commercial purpose.",
  "The GOL POA formalities (NY:GOL-5-1501B-poa-validity) do not apply to a power given to a licensed real estate "
  "broker in connection with a lease or management agreement, nor to a power given primarily for a business or "
  "commercial purpose; the written management agreement is the manager's written authority for GOL 5-703 and 5-1111. "
  "A statutory short-form power may still be used for these purposes.",
  Q(S, "9. a power given to a licensed real estate broker to take action in connection with a listing of real property, mortgage loan, lease or management agreement;"),
  "minor", "Step 3.3 leaving early; Step 8.6a state licensing", dependencies=["NY:GOL-5-1111-agent-written-authority"])]))

S = "NY:GOL 5-1502H"
rows.append(D(S, "new_rule",
  "Decides what a tenant's agent under a statutory short-form 'claims and litigation' grant may do in the settlement: "
  "dispute, settle, release, receive and endorse the refund.",
  proposed=[R("NY:GOL-5-1502H-agent-claims-authority", S, "GOL 5-1502H(1), (5), (6), (9)", "landlord", "may",
  "A former tenant's agent holds a valid statutory short-form power (NY:GOL-5-1501B-poa-validity) granting authority "
  "over 'claims and litigation'.",
  "The agent may assert and prosecute the deposit claim or defend the landlord's claim, settle or compromise either, "
  "execute a release or satisfaction, accept service and appear, and receive and endorse the refund check and "
  "deposit it; the landlord may deal with and pay the agent on those matters. A power that does not grant this "
  "authority does not permit the agent to settle or receive the refund.",
  Q(S, "5. To submit to alternative dispute resolution, to settle, and to propose or to accept a compromise with respect to, any claim existing in favor of or against the principal",
    "or be designated a party;"),
  "minor", "Step 6 refund payee; Step 8.1b payments and settlements", dependencies=["NY:GOL-5-1501B-poa-validity"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "to receive and conserve any moneys or other things of value paid in settlement",
                  "to receive and endorse checks and to deposit the same;")}],
  reasoning="Subdivision 9 covers receiving the refund and endorsing the check.")]))

save(rows)
