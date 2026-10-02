import sys
sys.path.insert(0, "register/work")
from q1_lib import *

rows = []
S = "NY:GOL 15-103"
rows.append(D(S, "partial",
  "Release of a co-tenant is stated; 15-103 adds that any payment or value received from one co-tenant is credited on "
  "the obligation of every co-tenant, unless the payer stood as the others' surety.",
  ["NY:GOL-15-104-105-cotenant-release"], [R(
  "NY:GOL-15-103-payment-credited", S, "GOL 15-103", "landlord", "must",
  "Several co-tenants (or a co-tenant and a guarantor) owe the balance jointly, severally, or jointly and severally, "
  "and one of them pays or gives value in whole or partial satisfaction.",
  "The amount or value received is credited, to that amount, on the obligation of every co-obligor, so the landlord "
  "may pursue the others only for what remains. Exception: it is not credited to a co-obligor for whom the payer "
  "stood as surety (a guarantor's payment does not reduce what the tenant owes the guarantor on reimbursement, but it "
  "does reduce what the landlord may still collect).",
  Q(S, "The amount or value of any consideration received by the obligee from one or more of several obligors",
    "did not stand in the relation of a surety."),
  "major", "Step 8.1b payments and settlements", dependencies=["NY:GOL-15-104-105-cotenant-release"])]))

rows.append(D("NY:GOL 15-108", "no_decision",
  "Releases among joint tortfeasors and contribution under CPLR article 14; the balance is a contract claim under the "
  "lease (GOL 15-101), and no settlement step turns on tortfeasor contribution."))

S = "NY:GOL 15-303"
rows.append(D(S, "new_rule",
  "Decides the write-off branch: a written release of the balance (or of the deposit claim) binds without consideration.",
  proposed=[R("NY:GOL-15-303-written-release", S, "GOL 15-303", "landlord; former tenant", "may",
  "After the claim accrued, the landlord (or its authorized agent) gives the former tenant a written instrument "
  "releasing all or part of the balance, or the former tenant gives the landlord a written release of all or part of "
  "its deposit claim.",
  "The written release is not invalid for want of consideration or seal: a written release of the balance discharges "
  "it to the extent stated, so a letter telling the tenant the balance is released or forgiven ends the claim, while "
  "an internal write-off that is not communicated as a release does not. A tenant's release of an accrued deposit "
  "claim binds the same way; a lease clause waiving deposit rights in advance stays void (NY:GOL-7-108(3), "
  "NY:GOL-7-103(3)). A release of one co-tenant affects the others as NY:GOL-15-104-105-cotenant-release states.",
  Q(S, "A written instrument which purports to be a total or partial release of all claims", "because of the absence of consideration or of a seal."),
  "major", "Step 8 pursue, hand off or write off", dependencies=["NY:GOL-15-104-105-cotenant-release", "NY:GOL-7-108(3)"])]))

S = "NY:GOL 15-503"
rows.append(D(S, "partial",
  "Full-payment checks are stated (NY:UCC-1-308-full-payment-check); 15-503 adds that a written signed offer to accept "
  "a stated performance in satisfaction, once tendered before revocation, discharges the claim even if the tender is "
  "refused.",
  ["NY:UCC-1-308-full-payment-check"], [R(
  "NY:GOL-15-503-offer-of-accord", S, "GOL 15-503(1), (2)", "landlord; former tenant", "must",
  "The landlord (or its agent) makes a written, signed offer to accept a stated payment or other performance in "
  "satisfaction of all or part of the balance (a settlement offer), or the tenant makes such an offer about its "
  "deposit claim, and the other side tenders that performance before the offer is revoked.",
  "The tender takes effect as a defense, or as the basis of an action or counterclaim, even though the offeror or its "
  "agent refused it: the landlord who refuses a timely tender of the offered settlement cannot recover more than the "
  "offer. A settlement offer therefore states a deadline or is revoked in writing before tender. If an agent signs "
  "an offer that affects an interest in real property within GOL 5-703(1) or (2) (for example a surrender of a lease "
  "over one year), the offer is void unless the agent was authorized in writing.",
  Q(S, "1. An offer in writing, signed by the offeror or by his agent, to accept a performance therein designated in satisfaction",
    "by reason of the fact that such tender was not accepted by the offeror or by his agent."),
  "major", "Step 8.1b payments and settlements", dependencies=["NY:UCC-1-308-full-payment-check", "NY:GOL-5-703-15-301-early-termination"])]))

S = "NY:GOL 15-701"
rows.append(D(S, "partial",
  "The guaranty writing rule is stated; 15-701 adds that the landlord's refusal to sue the tenant after the guarantor's "
  "demand does not discharge the guarantor unless they agreed otherwise in writing.",
  ["NY:GOL-5-701(a)(2)-guaranty"], [R(
  "NY:GOL-15-701-guarantor-not-discharged", S, "GOL 15-701", "landlord", "may",
  "A guarantor (surety) of the lease demands that the landlord sue the former tenant, and the landlord does not.",
  "The guarantor is not discharged by the landlord's failure or refusal to sue the tenant, unless the guaranty or "
  "another writing between them provides otherwise; the landlord may pursue the guarantor directly.",
  Q(S, "Unless otherwise agreed between the parties in writing, the failure or refusal by a creditor", "shall not discharge such surety."),
  "major", "Step 8 collecting a balance", dependencies=["NY:GOL-5-701(a)(2)-guaranty"])]))

S = "NY:GOL 3-101"
rows.append(D(S, "new_rule",
  "Decides capacity: a lease signed at 18 or older cannot be disaffirmed for infancy; no rule states the tenant's age "
  "of capacity.",
  proposed=[R("NY:GOL-3-101-age-of-capacity", S, "GOL 3-101(1)", "landlord", "may",
  "The landlord seeks the balance from a tenant or guarantor who was young when the lease or guaranty was signed.",
  "A lease or guaranty signed on or after 1974-09-01 by a person who had turned 18 cannot be disaffirmed on the ground "
  "of infancy; it binds fully. A person who signed before turning 18 may disaffirm the contract (the common-law "
  "infancy rule this section limits), and after disaffirmance the lease's charge and fee terms do not bind that "
  "person, whose liability is for the reasonable value of the housing actually used as a necessary. A suit against a "
  "person still under 18 needs a guardian or representative (NY:CPLR-1203-1015-5208-parties).",
  Q(S, "1. A contract made on or after September first, nineteen hundred seventy-four by a person after he has attained the age of eighteen years",
    "may not be disaffirmed by him on the ground of infancy."),
  "major", "Step 8.10 before suing: capacity", dependencies=["NY:CPLR-1203-1015-5208-parties"])]))

rows.append(D("NY:GOL 3-301", "no_decision",
  "Confirms a married woman contracts, is liable and is sued as if unmarried; no settlement step differs by marital "
  "status, and equal treatment is stated (NY:EXEC-296(5)(a)(2)-terms)."))

S = "NY:GOL 3-501"
rows.append(D(S, "new_rule",
  "Decides whether a refund paid, or a surrender or release signed, by a servicemember-tenant's attorney-in-fact after "
  "the tenant's unknown death binds the estate.",
  proposed=[R("NY:GOL-3-501-servicemember-poa-death", S, "GOL 3-501(1)-(3)", "landlord", "may",
  "The tenant gave a written power of attorney while serving (or later served) in the U.S. armed forces, as a "
  "merchant seaman abroad, or abroad on U.S. war-related assignment, and the agent acts for the tenant in the "
  "settlement (gives notice, receives the refund, signs a release) after the tenant died.",
  "The agency is not revoked by the death as to an agent who acts in good faith without actual knowledge or notice of "
  "it; those acts bind the tenant's heirs and personal representatives, so a refund the landlord paid to that agent "
  "discharges the landlord against the estate. The agent's affidavit that it had no knowledge or notice of "
  "revocation is conclusive absent fraud. A 'missing' or 'missing in action' listing is not notice of death.",
  Q(S, "shall be revoked or terminated by the death of the principal as to the attorney-in-fact", "shall be binding on the heirs, devisees, legatees or personal representatives of the principal."),
  "minor", "Step 2.5 tenant dies; Step 6 refund payee", determinacy="MIXED",
  judgment_terms=["good faith", "actual knowledge", "actual notice"], dependencies=["NY:ADJ-tenant-death-payee"])]))

S = "NY:GOL 5-1103"
rows.append(D(S, "partial",
  "Early termination in writing is stated (NY:GOL-5-703-15-301-early-termination); 5-1103 adds that a written "
  "modification or discharge of the lease or the balance needs no consideration if signed by the party to be charged "
  "or its agent.",
  ["NY:GOL-5-703-15-301-early-termination"], [R(
  "NY:GOL-5-1103-written-modification", S, "GOL 5-1103", "landlord; former tenant", "may",
  "The landlord and tenant change or discharge the lease, a charge, or the balance, in whole or part (an agreed "
  "earlier end date, a reduced balance, a waived charge).",
  "The change or discharge is not invalid for want of consideration if it is in writing and signed by the party "
  "against whom it is enforced, or by its agent (in writing where GOL 5-1111 requires). So a signed landlord letter "
  "waiving a charge or accepting an earlier end date binds the landlord without anything given in return; an "
  "unsigned or oral one binds only if supported by consideration or by surrender or accord rules.",
  Q(S, "An agreement, promise or undertaking to change or modify, or to discharge in whole or in part, any contract, obligation, or lease",
    "by the party against whom it is sought to enforce the change, modification or discharge, or by his agent."),
  "major", "Step 3.3 leaving early; Step 8.1b payments and settlements",
  dependencies=["NY:GOL-5-703-15-301-early-termination"])]))

rows.append(D("NY:GOL 5-1105", "no_decision",
  "Makes a written promise on past consideration enforceable; the balance is already owed under the lease, so a later "
  "promise matters only as an acknowledgment, stated by NY:GOL-17-101-acknowledgment."))

S = "NY:GOL 5-1107"
rows.append(D(S, "new_rule",
  "A written, signed assignment of the balance (for example to an affiliate or collector) transfers it irrevocably "
  "without consideration; this fixes who holds the claim.",
  proposed=[R("NY:GOL-5-1107-written-assignment", S, "GOL 5-1107", "landlord", "may",
  "The owner assigns a former tenant's balance, or the tenant assigns its deposit claim, without payment.",
  "An assignment in writing signed by the assignor or its agent irrevocably transfers the assignor's rights despite "
  "the absence of consideration; an unwritten gratuitous assignment does not. The assignee's position and limits "
  "follow NY:GOL-13-101-105-balance-transfer and NY:JUD-489-champerty.",
  Q(S, "An assignment shall not be denied the effect of irrevocably transferring the assignor’s rights", "signed by the assignor, or by his agent."),
  "minor", "Step 8.1b payments and settlements", dependencies=["NY:GOL-13-101-105-balance-transfer", "NY:JUD-489-champerty"])]))

S = "NY:GOL 5-1111"
rows.append(D(S, "partial",
  "The written-authority requirement for an agent's surrender of a lease over one year is stated through GOL 5-703; "
  "5-1111 extends it to an agent's written modification, discharge or assignment of such a lease.",
  ["NY:GOL-5-703-15-301-early-termination"], [R(
  "NY:GOL-5-1111-agent-written-authority", S, "GOL 5-1111", "managing agent, Handoff", "must",
  "A managing agent or Handoff signs, for the owner, a written modification, discharge, promise or assignment under "
  "GOL 5-1103, 5-1105, 5-1107 or 5-1109 that affects a lease for more than one year (for example an agreed early "
  "end date or release from the remaining term).",
  "The writing is void unless the agent was authorized in writing by the owner; the management agreement or a "
  "separate signed authority must cover it before the agent signs, or the owner signs itself.",
  Q(S, "If executed by an agent, any agreement, promise, undertaking, assignment or offer required by section 5-1103",
    "shall be void unless such agent was thereunto authorized in writing."),
  "critical", "Step 3.3 leaving early", dependencies=["NY:GOL-5-703-15-301-early-termination"])]))

S = "NY:GOL 5-1301"
rows.append(D(S, "partial",
  "The lease-rate interest rule (NY:CASE-NML-contract-rate) is stated; 5-1301 adds that a rate stated without a period "
  "is a yearly rate.",
  ["NY:CASE-NML-contract-rate", "NY:ADJ-lease-interest-on-rent"], [R(
  "NY:GOL-5-1301-rate-per-annum", S, "GOL 5-1301", "landlord", "must",
  "The lease, a payment agreement or any instrument states a rate of interest (for example 'interest at 1.5%') and "
  "no period for which it is calculated.",
  "The rate is a yearly rate, computed as if 'per annum' were written; it may not be applied monthly. Interest on "
  "late rent remains subject to NY:ADJ-lease-interest-on-rent.",
  Q(S, "any certain rate of interest is or shall be mentioned, and no period of time is stated", "“per annum” or “by the year” had been added to such rate."),
  "critical", "Step 8.10 interest", dependencies=["NY:CASE-NML-contract-rate"], amends="NY:CASE-NML-contract-rate")]))

S = "NY:GOL 5-1501A"
rows.append(D(S, "new_rule",
  "Decides whether the landlord may deal with, and pay the refund to, the tenant's agent after the tenant becomes "
  "incapacitated.",
  proposed=[R("NY:GOL-5-1501A-durable-poa", S, "GOL 5-1501A", "landlord", "may",
  "The former tenant has a New York power of attorney and becomes incapacitated before the settlement ends.",
  "The power is durable unless it expressly ends on incapacity, so the agent's acts (receiving the statement and "
  "refund, disputing charges, signing a release) during the incapacity bind the tenant and its estate as if it had "
  "capacity. Once a guardian is appointed, the agent accounts to the guardian, and the landlord deals with whichever "
  "the guardianship order empowers.",
  Q(S, "1. A power of attorney is durable unless it expressly provides that it is terminated by the incapacity of the principal.",
    "as if such principal had capacity."),
  "minor", "Step 6 refund payee")]))

S = "NY:GOL 5-1507"
rows.append(D(S, "new_rule",
  "Decides whether the landlord is protected in accepting an agent's signature on a settlement document.",
  proposed=[R("NY:GOL-5-1507-agent-signature", S, "GOL 5-1507(1)-(3)", "landlord", "may",
  "An agent under a power of attorney signs a settlement document for the former tenant (a release, a forwarding "
  "address, a payment agreement).",
  "The agent signs disclosing the agency ('X as agent for Y', 'Y by X, as agent' or similar); the landlord incurs no "
  "liability for accepting a signature that does not. By signing, the agent attests it has actual authority and no "
  "notice of termination, revocation, incapacity (for a non-durable power) or limiting modification; that attestation "
  "does not protect a landlord that had actual notice the power had ended.",
  Q(S, "(b) A third party shall incur no liability for accepting a signature that does not meet the requirements of this subdivision."),
  "minor", "Step 6 refund payee", dependencies=["NY:GOL-5-1501A-durable-poa"])]))

S = "NY:GOL 5-321"
rows.append(D(S, "new_rule",
  "A lease clause exempting the landlord from its own negligence is void, so it cannot shift to the tenant a move-out "
  "charge for damage the landlord or its agents negligently caused, nor bar the tenant's offset for its own losses.",
  proposed=[R("NY:GOL-5-321-exculpation-void", S, "GOL 5-321", "landlord", "must_not",
  "The landlord relies on a lease clause (exculpation, hold-harmless or indemnity) to charge the tenant for, or to "
  "defeat the tenant's claim for, injury to person or property caused by the negligence of the landlord, its agents, "
  "servants or employees in operating or maintaining the unit or building (for example a leak from a building pipe, a "
  "contractor's damage during repairs).",
  "The clause is void and wholly unenforceable to that extent. Damage so caused is not charged to the tenant or kept "
  "from the deposit, and the tenant's proven property loss from it may be asserted as a claim or offset against the "
  "balance.",
  Q(S, "Every covenant, agreement or understanding in or in connection with or collateral to any lease of real property exempting the lessor",
    "shall be deemed to be void as against public policy and wholly unenforceable."),
  "major", "Step 5.1 what the deposit may be kept for", determinacy="MIXED", judgment_terms=["negligence"],
  dependencies=["NY:GOL-7-108(1-a)(b)-refundable"])]))

rows.append(D("NY:GOL 5-323", "no_decision",
  "Voids negligence exemptions for building service and maintenance contractors in their contracts; it binds no "
  "charge or credit between landlord and tenant."))
rows.append(D("NY:GOL 5-327", "no_decision",
  "Reciprocal attorney's fees in consumer contracts of creditors, sellers and personal-property lessors; a residential "
  "real-property lease is governed by RPL 234 (NY:RPL-234) and RPL 234-a."))
rows.append(D("NY:GOL 5-331", "no_decision",
  "Voids racially restrictive covenants in instruments affecting real property; the settlement's equal-treatment duty "
  "is stated (NY:EXEC-296(5)(a)(2)-terms) and no settlement term turns on such a covenant."))

S = "NY:GOL 5-336"
rows.append(D(S, "new_rule",
  "Subdivision 3 is not limited to employers: a release of any claim whose facts involve unlawful discrimination is "
  "unenforceable if it carries NDA penalties or a no-discrimination disclaimer; this governs a move-out settlement "
  "with a tenant alleging discrimination.",
  proposed=[R("NY:GOL-5-336(3)-discrimination-release", S, "GOL 5-336(3)", "landlord, manager, Handoff", "must_not",
  "The landlord settles a dispute with the former tenant (over the deposit, charges or balance) whose factual basis "
  "involves unlawful discrimination, discriminatory harassment or retaliation, and takes a release.",
  "The release is unenforceable if the agreement requires the tenant to pay liquidated damages for breaching a "
  "nondisclosure or nondisparagement clause, to forfeit any part of the settlement payment for such a breach, or to "
  "state or disclaim that it was not subjected to unlawful discrimination, harassment or retaliation. Such a "
  "settlement omits those terms.",
  Q(S, "3. Notwithstanding any other law to the contrary, no release of any claim, the factual foundation for which involves unlawful discrimination",
    "was not in fact subject to unlawful discrimination, including discriminatory harassment, or retaliation."),
  "major", "Step 8.1b payments and settlements; Step 5.10 equal treatment", determinacy="MIXED",
  judgment_terms=["factual foundation for which involves unlawful discrimination"],
  dependencies=["NY:EXEC-296(5)(a)(2)-terms"])]))

rows.append(D("NY:GOL 5-337", "no_decision",
  "Bars non-disparagement waivers in contracts for the sale or lease of consumer goods or services; a residential lease "
  "of real property and its settlement are neither."))

S = "NY:GOL 5-521"
rows.append(D(S, "new_rule",
  "Branch of the usury rules for a company tenant: a corporation cannot plead civil usury against a forbearance on its "
  "balance, only criminal usury.",
  proposed=[R("NY:GOL-5-521-corporate-tenant-usury", S, "GOL 5-521(1), (3)", "landlord", "may",
  "The former tenant is a corporation (or an association or joint-stock company with corporate powers) and a payment "
  "agreement on its balance carries interest above the civil usury rate (NY:GOL-5-501-payment-plan-usury).",
  "The corporate tenant may not interpose the defense of civil usury, so NY:GOL-5-511-usurious-void does not void the "
  "agreement against it; it may still plead criminal usury under Penal Law 190.40 (interest above 25% a year). An LLC "
  "is treated as a corporation for this purpose only if it has corporate powers not held by individuals or "
  "partnerships.",
  Q(S, "1. No corporation shall hereafter interpose the defense of usury in any action.", "not possessed by individuals or partnerships."),
  "minor", "Step 8.1b payments and settlements", dependencies=["NY:GOL-5-501-payment-plan-usury"],
  construction=[{"source_file": BY_ID[S]["text_file"], "quote": Q(S, "3. The provisions of subdivision one of this section shall not apply to any action in which a corporation interposes a defense of criminal usury")}],
  reasoning="Subdivision 3 preserves the criminal-usury defense.")]))

rows.append(D("NY:GOL 5-527", "no_decision",
  "Compound interest rules for loans and financing over $250,000; no tenant balance or payment plan in this chain is "
  "such a financing."))
rows.append(D("NY:GOL 5-901", "no_decision",
  "Automatic renewal in leases of personal property; the real-property counterpart is stated (NY:GOL-5-905)."))

save(rows)
