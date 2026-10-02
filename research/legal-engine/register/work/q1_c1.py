import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:16 NYCRR 96.6"
rows.append(D(S, "partial",
  "NY:16NYCRR96-submetering states only the authorization condition (96.2); 96.6 adds the rate cap and credit for "
  "overcharges, the time-of-use bar, and HEFPA protections before any collection of submetered electric arrears.",
  ["NY:16NYCRR96-submetering"], [R(
  "NY:16NYCRR-96.6-submeter-charge-limits", S, "16 NYCRR 96.6(c), (d), (e), (h), (j)", "landlord (submeterer)", "must",
  "The final account carries electricity billed to the unit through submeters, or the landlord or a collector pursues "
  "overdue submetered electric charges after move-out.",
  "The submetered charge may not exceed the applicable rate cap; any amount above it is not charged or kept, and the "
  "PSC may direct a credit of the overcharge plus interest. Time-of-use rates are charged only if the tenant agreed "
  "to be billed on them. Bills to the resident go out within 30 days after the submeterer receives the utility's "
  "master-meter bill, and billing records are kept six years. The lease may not require binding arbitration of "
  "submetered billing complaints. Where the submetered premises lack termination-capable equipment, every HEFPA "
  "protection that applies before termination of service for unpaid charges must be given to the resident before any "
  "civil enforcement, collection or other proceeding on overdue electric charges begins; where the equipment exists, "
  "the submeterer must comply with HEFPA directly. The PSC may waive any condition by order for good cause.",
  Q(S, "(c) a condition that the submeterer shall not charge more than the applicable rate cap", "Part 145 of this Title;"),
  "critical", "Step 5.5a Credits and owner costs; Step 8 collecting a balance",
  dependencies=["NY:16NYCRR96-submetering"], amends="NY:16NYCRR96-submetering",
  reasoning="96.6(h) also conditions collection: 'Each protection shall be provided to such resident prior to the "
            "commencement of any other civil enforcement, collection, or other proceeding based on such resident's "
            "overdue electric charges'.",
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "Each protection shall be provided to such resident prior to the commencement", "overdue electric charges;")}])]))

S = "NY:19 NYCRR 175.3"
rows.append(D(S, "partial",
  "Broker escrow (175.1) and licence discipline (RPL 441-c) are stated; 175.3(b) adds that a broker holding a tenant's "
  "security must follow GOL 7-103 including interest, on pain of discipline, and 175.3(a) bars undisclosed rebates on "
  "expenditures the manager makes for the owner (turnover work).",
  ["NY:19NYCRR-175.1-broker-escrow", "NY:RPL-441-c-licence-discipline"], [R(
  "NY:19NYCRR-175.3-broker-manager-deposit", S, "19 NYCRR 175.3(a), (b)", "licensed broker acting as managing agent", "must",
  "A person or firm licensed or acting as a real estate broker manages the unit and has the tenant's security in its "
  "custody or control, or makes expenditures (repairs, cleaning, turnover work) for the owner.",
  "It treats, handles and disposes of the security, including required interest, as GOL 7-103 requires (trust, no "
  "commingling, bank notice, interest paid, applied or credited). Failure, including failure to pay, apply or credit "
  "required interest, is ground for discipline by the Secretary of State, in addition to the tenant's own remedies. "
  "As managing agent it takes no commission, rebate or profit on expenditures made for the owner without the owner's "
  "full knowledge and consent.",
  Q(S, "(b) A person, firm or corporation licensed or acting as a real estate broker", "action by the Secretary of State."),
  "major", "Step 1.2 deposit in trust; Step 8.6a state licensing",
  dependencies=["NY:GOL-7-103(1)-trust", "NY:GOL-7-103(2)-interest-owed", "NY:19NYCRR-175.1-broker-escrow"])]))

for s in ["NY:23 NYCRR 1.2", "NY:23 NYCRR 1.3", "NY:23 NYCRR 1.4", "NY:23 NYCRR 1.5", "NY:23 NYCRR 1.6"]:
    rows.append(D(s, "no_decision",
      "23 NYCRR Part 1 reaches only debts from transactions in which credit was extended; a lease balance is not one "
      "(NY:23NYCRR-1.1(d)-not-lease), so this section binds no collector of a former tenant's balance."))

S = "NY:GOL 15-106"
rows.append(D(S, "partial",
  "Tenant death is stated for a sole or last surviving tenant (NY:ADJ-tenant-death-payee); 15-106 adds that when one "
  "of several co-tenants dies, the estate stays jointly and severally liable with the survivors.",
  ["NY:ADJ-tenant-death-payee", "NY:ADJ-cotenants-payee"], [R(
  "NY:GOL-15-106-cotenant-death", S, "GOL 15-106", "landlord", "may",
  "Two or more tenants are jointly obligated under the lease and one of them dies before the balance is paid.",
  "The deceased co-tenant's estate remains bound jointly and severally with the surviving co-tenants for the lease "
  "obligations. The landlord may pursue the full balance against the survivors or present the claim to the estate's "
  "fiduciary (NY:ADJ-tenant-death-payee for presentation and limitation), and a recovery from one reduces what is owed "
  "by the others.",
  Q(S, "On the death of a joint obligor in contract", "surviving obligor or obligors."),
  "critical", "Step 2.5 tenant dies; Step 8 collecting a balance", dependencies=["NY:ADJ-tenant-death-payee"])]))

usury_q = Q("NY:GOL 5-501", "2. No person or corporation shall, directly or indirectly, charge, take or receive any money",
            "at a rate exceeding the rate above prescribed.")
rows.append(D("NY:GOL 5-501", "new_rule",
  "No rule states the usury cap. A payment plan on a move-out balance in which the landlord agrees to wait in return "
  "for interest is a forbearance; its interest is capped by 5-501 and Banking Law 14-a.",
  proposed=[R("NY:GOL-5-501-payment-plan-usury", "NY:GOL 5-501", "GOL 5-501(1), (2)", "landlord, manager, collector", "must_not",
  "After the balance fell due, the landlord (or a manager or collector for it) agrees with the former tenant to give "
  "time to pay (a payment plan, a settlement payable in instalments, a promissory note) in return for interest or "
  "any other consideration for the delay.",
  "That agreement is a forbearance. The interest, counting every amount paid or payable for the forbearance, may not "
  "exceed the rate in Banking Law 14-a (16% a year), whatever the agreement says. Branch: the lease's own charges for "
  "late payment are not interest on a forbearance; they are governed by RPL 238-a (NY:ADJ-lease-interest-on-rent). "
  "Branch: statutory pre- and post-judgment interest (CPLR 5001, 5004) is not interest charged on a forbearance. "
  "Consequences: NY:GOL-5-511-usurious-void, NY:GOL-5-513-recover-excess.",
  usury_q, "critical", "Step 8.10 interest; Step 8.1b payments and settlements",
  dependencies=["NY:ADJ-lease-interest-on-rent", "NY:CPLR-5004(a)-consumer-2pct"],
  reasoning="5-501(1) sets the rate at six percent 'unless a different rate is prescribed in section fourteen-a of the "
            "banking law'; Banking Law 14-a(1) prescribes 16 percent. A lease is not a loan, so the lease's late "
            "charges are not usury; an agreement after default to extend time for payment in return for interest is "
            "the textbook 'forbearance' the section names.",
  construction=[{"source_file": BY_ID["NY:GOL 5-501"]["text_file"], "quote": Q("NY:GOL 5-501", "The rate of interest, as computed pursuant to this title, upon the loan or forbearance", "section fourteen-a of the banking law.")}])]))

rows.append(D("NY:GOL 5-511", "new_rule",
  "Consequence of a usurious forbearance agreement on a balance: the agreement is void and its enforcement is enjoined.",
  proposed=[R("NY:GOL-5-511-usurious-void", "NY:GOL 5-511", "GOL 5-511(1), (2)", "court", "must",
  "A payment-plan or other forbearance agreement on a former tenant's balance reserves or takes interest above the "
  "5-501 rate (NY:GOL-5-501-payment-plan-usury), and the lender is not a savings bank or savings and loan association.",
  "The forbearance agreement, and any note or security taken under it, is void; on proof or admission the court "
  "declares it void, enjoins any prosecution on it and orders it surrendered and cancelled. The landlord's underlying "
  "lease claim, which arose without usury, is not an instrument taken in violation and is still pursued on its own "
  "terms (within its own limitation period, NY:CPLR-213(2)).",
  Q("NY:GOL 5-511", "the court shall declare the same to be void, and enjoin any prosecution thereon", "surrendered and cancelled."),
  "critical", "Step 8.1b payments and settlements", dependencies=["NY:GOL-5-501-payment-plan-usury"])]))

rows.append(D("NY:GOL 5-513", "new_rule",
  "Tenant's recovery of usurious interest paid under a forbearance on the balance.",
  proposed=[R("NY:GOL-5-513-recover-excess", "NY:GOL 5-513", "GOL 5-513", "former tenant", "may",
  "The former tenant paid interest under a forbearance agreement on its balance above the 5-501 rate.",
  "The tenant, or its personal representative, may recover from whoever received it the amount paid above the lawful "
  "rate. A person who returns the excess is discharged from further forfeiture or penalty under 5-511 and 5-513 "
  "(NY:GOL-5-519-return-discharges).",
  Q("NY:GOL 5-513", "Every person who, for any such loan or forbearance", "above the rate aforesaid."),
  "critical", "Step 8.1b payments and settlements", dependencies=["NY:GOL-5-501-payment-plan-usury"])]))

rows.append(D("NY:GOL 5-519", "new_rule",
  "Cure for a usurious forbearance on a balance: returning the excess discharges further forfeiture or penalty.",
  proposed=[R("NY:GOL-5-519-return-discharges", "NY:GOL 5-519", "GOL 5-519", "landlord, collector", "may",
  "The landlord or collector took interest above the 5-501 rate under a forbearance agreement on a former tenant's "
  "balance (NY:GOL-5-501-payment-plan-usury).",
  "Repaying or returning what was so taken, or its value, discharges it from any further forfeiture or penalty under "
  "5-511 and 5-513 incurred by taking it.",
  Q("NY:GOL 5-519", "Every person who shall repay or return the money", "repaid, or returned, as aforesaid."),
  "major", "Step 8.1b payments and settlements", dependencies=["NY:GOL-5-511-usurious-void", "NY:GOL-5-513-recover-excess"])]))

rows.append(D("NY:GOL 7-101", "no_decision",
  "Governs deposits on rentals of personal property; a dwelling deposit is governed by GOL 7-103 and 7-108."))
rows.append(D("NY:RPAPL 635", "no_decision",
  "Joint judgment in an ejectment action against occupants of different apartments; recovers possession, not a "
  "departed tenant's money balance."))

S = "NY:RPAPL 702"
rows.append(D(S, "partial",
  "RPAPL 749(3) states the separate action after a summary proceeding; 702 adds that the proceeding itself recovers only "
  "rent (the monthly amount), never fees, charges or penalties, whatever the lease says.",
  ["NY:RPAPL-749(3)-after-proceeding"], [R(
  "NY:RPAPL-702-rent-only", S, "RPAPL 702(1), (2)", "landlord", "must_not",
  "The landlord brings a summary proceeding (nonpayment or holdover) for a residential unit before or while the "
  "tenancy ends.",
  "'Rent' in the proceeding is only the monthly or weekly amount charged for use and occupation under the written or "
  "oral rental agreement. No fees, charges or penalties (late fees, legal fees, repair or utility charges called "
  "'additional rent') may be sought in it, notwithstanding any lease language. Those that are lawful are pursued by "
  "separate action or listed on the move-out statement as the deposit rules allow (NY:RPAPL-749(3)-after-proceeding, "
  "NY:ADJ-no-fee-retention). The section does not apply between a cooperative housing corporation (other than one "
  "under PHFL article 2, 4, 5 or 11) and its shareholder-tenant when the proprietary lease makes such charges "
  "recoverable in the proceeding.",
  Q(S, "the term “rent” shall mean the monthly or weekly amount", "notwithstanding any language to the contrary in any lease or rental agreement."),
  "major", "Step 3.8 after an eviction case", dependencies=["NY:RPAPL-749(3)-after-proceeding"])]))

save(rows)
