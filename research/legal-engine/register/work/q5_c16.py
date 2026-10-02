import sys
sys.path.insert(0, "register/work")
from q5_lib import add, rule, SEC

F = SEC["US:11 USC 101"]["text_file"]
p = rule("US:11 USC 101", "US:11USC101(5)-charge-timing", "11 U.S.C. 101(5), (8), (10)(A), (12)", "landlord; manager; collector", "applies",
         "A former tenant files bankruptcy and the landlord's account contains charges some of which relate to the time before the petition and some to the time after.",
         "A 'claim' is any right to payment, whether or not reduced to judgment, liquidated, fixed, contingent, matured, disputed or secured. So: (1) rent and charges that accrued before the petition, and liability for damage the tenant caused before the petition, are pre-petition claims even if the landlord had not yet inspected, assessed, itemized or billed them at the filing; they are stayed (US:11USC362(a)(6)), claimed by proof of claim, and discharged unless excepted. (2) Damages for rejection of an unexpired lease (future rent) are treated as pre-petition (US:11USC365(d)(1)-ch7-rejection) and capped (US:11USC502(b)(6)-lessor-cap). (3) Rent or use and occupancy for the period after the petition, and damage the tenant causes after it, are post-petition debts: not stayed as pre-petition claims, not discharged in chapter 7, and in chapter 13 claimable only under 1305 (US:11USC1305-postpetition-claim); charges in a chapter 13 later converted become pre-petition (US:11USC348-conversion). The Handoff account splits each charge at the petition date on these lines. (4) A balance owed by an individual tenant under a residential lease is a consumer debt (incurred primarily for a personal, family or household purpose), which brings in the co-debtor stay, the 523(d) fee rule, the $600 preference floor and the 707(b) abuse test; a company tenant's balance is not.",
         "critical", "6.7", "(5) The term “claim” means— (A) right to payment", "disputed, undisputed, legal, equitable, secured, or unsecured; or",
         determinacy="MIXED", judgment_terms=["primarily for a personal, family, or household purpose"],
         dependencies=["US:11USC362(a)(6)", "US:11USC365(d)(1)-ch7-rejection", "US:11USC502(b)(6)-lessor-cap", "US:11USC1301-codebtor-stay"],
         construction=[{"source_file": F, "quote": "(8) The term “consumer debt” means debt incurred by an individual primarily for a personal, family, or household purpose."},
                       {"source_file": F, "quote": "(A) entity that has a claim against the debtor that arose at the time of or before the order for relief concerning the debtor;"}],
         reasoning="The breadth of 'claim' (contingent, unliquidated, unmatured) makes the tenant's liability for pre-petition conduct under the lease a pre-petition claim even when the landlord quantifies it later; a debt for a period after the order for relief is not a claim against the debtor under 101(10)(A). A residential lease is for household use, so the tenant's balance is a consumer debt.")
add("US:11 USC 101", "partial",
    "The definitions of claim and consumer debt decide which move-out charges are stayed and dischargeable (those relating to pre-filing time, even if assessed later) and which provisions reach the balance; the existing stay rule says only 'arose before the filing'.",
    atom_ids=["US:11USC362(a)(6)", "US:11USC1301-codebtor-stay"], proposed=[{**p, "amends": "US:11USC362(a)(6)"}])
