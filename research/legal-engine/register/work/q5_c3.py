import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

p = rule("US:11 USC 506", "US:11USC506-deposit-secured-claim", "11 U.S.C. 506(a)(1), (b)", "landlord", "applies",
         "A former tenant is a debtor and the landlord still holds the deposit, which it may set off against pre-petition charges (US:11USC362(a)(7)-deposit-is-setoff), when it files its proof of claim.",
         "The landlord's allowed claim is a secured claim up to the amount subject to setoff (the deposit, with any interest the landlord would otherwise owe on it) and an unsecured claim for the rest; the proof of claim states the secured part as secured by setoff and the unsecured remainder, which is what the plan or chapter 7 distribution pays. If the deposit exceeds the allowed pre-petition claim, the landlord is also allowed interest on the claim and the reasonable fees, costs or charges the lease or a state statute provides (a lease attorney's-fee clause, reciprocal for the tenant under NY RPL 234), up to the excess; without such a provision no fees are allowed. The setoff itself is taken only after stay relief (US:CASE-Strumpf-hold).",
         "major", "8.8", "(a) (1) An allowed claim of a creditor secured by a lien on property in which the estate has an interest, or that is subject to setoff under section 553",
         "provided for under the agreement or State statute under which such claim arose.",
         dependencies=["US:11USC362(a)(7)-deposit-is-setoff", "US:FRBP-3002(c)-claim-deadline"])
add("US:11 USC 506", "partial",
    "Makes the part of the landlord's claim covered by the deposit a secured claim and allows lease fees and interest up to any excess deposit; the existing claim rule only nets the deposit.",
    atom_ids=["US:FRBP-3002(c)-claim-deadline"], proposed=[{**p, "amends": "US:FRBP-3002(c)-claim-deadline"}])

p = rule("US:11 USC 507", "US:11USC507(a)(7)-deposit-priority", "11 U.S.C. 507(a)(7); 507(d)", "tenant; owner; manager; trustee", "has priority",
         "The owner is a debtor in any chapter and a former tenant (an individual) has a claim to return of a residential deposit paid before the filing that is not trust property in the case (commingled and untraceable, US:11USC541-704-owner-chapter7).",
         "The tenant's refund claim is a seventh-priority unsecured claim up to the 507(a)(7) amount in effect when the case was commenced ($3,800 per individual for cases commenced on or after 2025-04-01; $3,350 for cases commenced 2022-04-01 to 2025-03-31; US:11USC104-dollar-amounts), paid ahead of general unsecured claims: in chapter 7 before general claims (726(a)(1)); in chapter 13 in full under the plan unless the tenant agrees otherwise (1322(a)(2)); in chapter 11 in full in cash on the effective date, or in deferred cash of equal present value if the class accepts (1129(a)(9)(B)). Only the deposit itself has priority: statutory damages or penalties for mishandling it (for example twice the deposit) are general unsecured claims. Each co-tenant who is an individual has a separate cap for the part of the deposit that is theirs. An entity that pays the tenant and is subrogated (a buyer or insurer) does not take the priority. A landlord's claim against a debtor-tenant for an unpaid security deposit has no priority. The tenant's proof of claim asserts the priority; the manager for the owner reports the deposit and tenant on the owner's schedules.",
         "critical", "0.5", "(7) Seventh, allowed unsecured claims of individuals", "that were not delivered or provided.",
         dependencies=["US:11USC541-704-owner-chapter7", "US:11USC1107-1306-owner-reorganization", "US:11USC104-dollar-amounts"])
p["reasoning"] = ("The clause 'that were not delivered or provided' modifies the services (a plural verb cannot attach to the singular 'property'), so a residential tenant's deposit qualifies whether or not the unit was delivered: "
                  "Guarracino v. Hoffman, 246 B.R. 130 (D. Mass. 2000); In re River Village Assocs., 161 B.R. 127 (Bankr. E.D. Pa. 1993); In re Wise, 120 B.R. 537 (Bankr. D. Alaska 1990); contra In re Cimaglia, 50 B.R. 9 (Bankr. S.D. Fla. 1985), the minority, rejected here because it would protect a deposit only before possession. "
                  "Guarracino limits the priority to the deposit, not state-law damages. In re Miller (Bankr. S.D. Ala. 2019) denies priority to a landlord's claim for an unpaid deposit. No Second Circuit or S.D.N.Y. decision holds otherwise.")
add("US:11 USC 507", "partial",
    "Gives a former tenant's untraceable deposit refund claim seventh priority up to $3,800 in the owner's bankruptcy; the existing owner rules make it a plain unsecured claim.",
    atom_ids=["US:11USC541-704-owner-chapter7", "US:11USC1107-1306-owner-reorganization"], proposed=[{**p, "amends": "US:11USC541-704-owner-chapter7"}])

nd("US:11 USC 509", "Subrogation and contribution between co-debtors (a co-tenant or guarantor who pays) and the debtor; the landlord's own claim, collection and deadlines are unchanged, and (c) only subordinates the co-debtor to the landlord until paid.")
nd("US:11 USC 525", "Bars discrimination against debtors only by governmental units, private employers (in employment) and student-loan programs; a private market-rate landlord or manager settling a departing tenancy is none of these.")

add("US:11 USC 543", "new_rule",
    "If the owner files bankruptcy while a foreclosure receiver, HPD or 7-A administrator holds the building's rents, the custodian must stop disbursing and turn rents and collections over to the trustee or debtor in possession, changing who collects a former tenant's balance.",
    proposed=[rule("US:11 USC 543", "US:11USC543-custodian-turnover", "11 U.S.C. 543(a)-(d)", "receiver; administrator; manager", "shall",
                   "A custodian (a receiver or administrator appointed under state law, such as a foreclosure receiver, an HPD receiver or a 7-A administrator, or an assignee for the benefit of creditors) holds the building's rents or collections when it learns the owner has filed bankruptcy.",
                   "From the time it knows of the case the custodian may not disburse or administer the owner's property, rents or collections except to preserve them; it must deliver to the trustee (or the debtor in possession) what it holds on that date, including rents and former-tenant balances collected, and file an accounting. The court may excuse compliance if creditors are better served by the custodian staying in possession, and must excuse it for an assignee for the benefit of creditors that took possession more than 120 days before the filing (unless needed to prevent fraud or injustice). A manager acting for the custodian collects and remits former-tenant balances to the trustee or debtor in possession accordingly (US:11USC541-704-owner-chapter7, US:11USC1107-1306-owner-reorganization). A deposit the tenant can trace is not the owner's property and stays refundable as trust money.",
                   "major", "0.5", "(a) A custodian with knowledge of the commencement of a case under this title concerning the debtor may not make any disbursement",
                   "unless compliance with such subsections is necessary to prevent fraud or injustice.",
                   dependencies=["NY:CPLR-6401-foreclosure-receiver", "NYC:HMC-27-2135(c)-receiver-rents", "NY:RPAPL-776-778-administrator", "US:11USC541-704-owner-chapter7"])])

add("US:11 USC 544", "new_rule",
    "Lets a payer's trustee recover rent a non-liable third party paid for the tenant within the state-law look-back (NY: four years), beyond the two-year federal period.",
    proposed=[rule("US:11 USC 544", "US:11USC544(b)-state-lookback", "11 U.S.C. 544(b)(1)", "landlord", "must return",
                   "Someone other than the tenant (a parent, relative or employer) who was not liable on the lease paid the tenant's rent or balance to the landlord, and later becomes a bankruptcy debtor.",
                   "The payer's trustee may avoid the payment if an actual unsecured creditor of the payer could avoid it under state law: under New York's Uniform Voidable Transactions Act a transfer made without reasonably equivalent value to the transferor while insolvent (or that left it insolvent) is voidable within four years. The landlord, as initial transferee, returns the payments made in that period (US:11USC548-constructive-fraud-third-party states the elements and 550 recovery). Payments the tenant made on its own debt, or a guarantor made on its own guarantee, give the payer value and are not avoidable on this ground.",
                   "major", "8.8", "(b) (1) Except as provided in paragraph (2), the trustee may avoid any transfer of an interest of the debtor in property",
                   "that is not allowable only under section 502(e) of this title.",
                   determinacy="MIXED", judgment_terms=["reasonably equivalent value", "insolvent"])])

nd("US:11 USC 545", "Lets the trustee avoid statutory liens for rent and distress for rent; New York gives a residential landlord no lien or distress on the tenant's goods (NY:COMMONLAW-belongings-owner-keeps), so there is nothing to avoid in this chain.")
