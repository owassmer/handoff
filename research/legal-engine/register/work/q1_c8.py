import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
for s, r in [
  ("NY:RPAPL 1353", "Vesting of title in the foreclosure-sale purchaser; the tenant's rights and the payee after the sale are stated by NY:RPAPL-1305-successor."),
  ("NY:RPAPL 1355", "Referee's report of a foreclosure sale; mortgage procedure."),
  ("NY:RPAPL 1393", "Local registration of mortgages in default; mortgage regulation, not a tenant settlement."),
  ("NY:RPAPL 211", "Order restraining waste while an action affecting title or possession is pending; no settlement amount, date or payee turns on it."),
  ("NY:RPAPL 221", "Delivery of possession under a judgment allotting or selling real property; partition and sale procedure."),
  ("NY:RPAPL 231", "Notice and conduct of judicial sales of real property; not a tenant settlement."),
  ("NY:RPAPL 241", "Persons bound by a judgment affecting title (after-born persons); not a tenant settlement."),
  ("NY:RPAPL 601", "Damages in an ejectment action; a holdover's use and occupancy is stated by NY:RPL-220 and possession is recovered by summary proceeding, so no settlement amount turns on it."),
  ("NY:RPAPL 612", "Limits actions on reverters and conditions subsequent, expressly excluding lease conditions; not a tenant settlement."),
  ("NY:RPAPL 631", "Who is named defendant in an ejectment action; no settlement step turns on it."),
  ("NY:RPAPL 637", "Effect of an ejectment judgment against a defendant under whom others hold; not a tenant settlement."),
  ("NY:RPAPL 651", "Ejectment where the plaintiff's title expires before trial; not a tenant settlement."),
  ("NY:RPAPL 721", "Who may bring a summary proceeding for possession; it fixes no settlement amount, date or payee."),
  ("NY:RPAPL 732", "Clerk-returnable nonpayment procedure where court rules adopt it; possession procedure that fixes no settlement amount."),
  ("NY:RPAPL 733", "Timing of service of a summary-proceeding petition; possession procedure that fixes no settlement amount."),
  ("NY:RPAPL 749-A", "The NYC marshal's notice of executing a warrant; the eviction date it records is the vacatur fact under NY:GOL-7-108(1-a)(e), which this section does not change."),
]:
    rows.append(D(s, "no_decision", r))
rows.append(D("NY:RPAPL 734", "excluded_regime", "Notice to the Westchester County social services commissioner; applies only in Westchester (outside NYC)."))

S = "NY:RPAPL 713"
rows.append(D(S, "partial",
  "RPL 235-f (occupants gain no tenancy) and the ban on self-help are stated; 713 decides how an occupant who stays after "
  "the tenant leaves, a squatter, or a foreclosure-sale occupant is removed: a ten-day notice to quit and a summary "
  "proceeding.",
  ["NY:RPL-235-f", "NY:RPAPL-768-853-unlawful-eviction", "NY:RPAPL-1305-successor"], [R(
  "NY:RPAPL-713-occupant-after-tenant", S, "RPAPL 713(3), (5), (7), (10)", "landlord", "must",
  "The tenant has surrendered or vacated, but a person who is not a tenant (a roommate, relative or other occupant "
  "admitted by the tenant, a guest, or an intruder) remains in the unit.",
  "The occupant is a licensee whose license ended when the tenant, its licensor, ceased to be entitled to possession "
  "(or was revoked), or a squatter. The landlord removes it only by a summary proceeding after a ten-day notice to "
  "quit served as RPAPL 735 prescribes (no notice is needed where entry or detainer was by force or unlawful means); "
  "until then self-help is barred for an occupant of 30 days or more (NY:RPAPL-768-853-unlawful-eviction). The "
  "tenant's own vacatur and the 14-day statement are not delayed by the occupant's stay, and the occupant's use and "
  "occupancy is the occupant's own liability (NY:RPL-220), not a charge against the departed tenant's deposit unless "
  "the tenant remained liable under the lease for that period. A foreclosure purchaser removes occupants on this "
  "ground only subject to RPAPL 1305 rights.",
  Q(S, "7. He is a licensee of the person entitled to possession of the property at the time of the license, and",
    "(c) the licensor is no longer entitled to possession of the property;"),
  "major", "Step 6.2 when the tenant vacated; Step 3.7 retaking the unit",
  dependencies=["NY:RPL-235-f", "NY:RPAPL-768-853-unlawful-eviction", "NY:RPL-220"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "A special proceeding may be maintained under this article after a ten-day notice to quit has been served upon the respondent",
                  "in the manner prescribed in section 735, upon the following grounds:")}],
  reasoning="The opening clause sets the ten-day notice; subdivision 7(c) makes the tenant's loss of possession end "
            "the occupant's license.")]))

S = "NY:RPAPL 746"
rows.append(D(S, "new_rule",
  "Many tenancies end by a stipulation of surrender or payment in a summary proceeding; with an unrepresented party the "
  "stipulation binds only after the court's allocution, and a nonpayment stipulation carries a rent breakdown.",
  proposed=[R("NY:RPAPL-746-stipulation-allocution", S, "RPAPL 746(1), (2), (4)", "landlord", "must",
  "In a summary proceeding, the landlord and tenant settle by a stipulation (other than one only adjourning or "
  "staying the case) made at a court appearance, and either side has no lawyer, such as a stipulation to surrender "
  "the unit by a date, pay arrears, or apply the deposit.",
  "The court describes its terms on the record and approves it only after an allocution finding the parties and "
  "signatory authority and (unless the court records why a finding is unnecessary) that the unrepresented party "
  "understands it may try the case, was not given legal advice by the other side's lawyer or under duress, knows its "
  "claims and defenses and that they are addressed, understands the terms, the effect of non-compliance and how to "
  "restore the case, and the effect of a judgment and the landlord's duty to provide a satisfaction on payment; in a "
  "nonpayment case the stipulation includes an appropriate rent breakdown. An approved stipulation fixes the move-out "
  "date and the amounts it resolves for the settlement; a stipulation not so allocuted is not approved and does not "
  "bind as a court stipulation.",
  Q(S, "2. No stipulation required to be on the record by subdivision one of this section may be approved by the court unless the court first conducts an allocution",
    "that an appropriate rent breakdown is included in the stipulation; and"),
  "major", "Step 3.8 after an eviction case", dependencies=["NY:CPLR-5020-satisfaction"])]))

save(rows)
