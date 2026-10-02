"""IR5A universe items, part 8: remaining items found in the TOC sweep."""
S = "sources/"
def sent(k):
    return r"[^.;]*" + k + r"[^.;]*[.;]"
ITEMS = [
 ("11 USC 1306(b)", "federal", "statute", "S15 bankruptcy (ch. 13 payee)", "In chapter 13 the debtor keeps possession of estate property (refund payable to the debtor).",
  S+"REVIEW1_US_11USC_1306.txt", sent(r"the debtor shall remain in possession of all property of the estate")),
 ("50 USC 3918", "federal", "statute", "S17 military (waiver)", "SCRA waivers must be in a separate written instrument executed during or after service.",
  S+"US_50USC_3918.txt", sent(r"in writing")),
 ("RPL 231-c", "state", "statute", "S1 lease form / S10 preconditions", "Leases/renewals must carry the Good Cause notice; the notice must accompany predicate notices and petitions (RPAPL 741(5-a)).",
  S+"REVIEW5A_NY_RPAPL_741.txt", r"5-a\. Append or incorporate the notice required pursuant to Real Property Law § 231-C"),
 ("RPAPL 741(5)", "state", "statute", "S9 use and occupancy", "Petition may seek rent due and fair value of use and occupancy if the notice of petition demands it.",
  S+"REVIEW5A_NY_RPAPL_741.txt", ("5. State the relief sought.", "a demand for such a judgment has been made.")),
 ("Admin. Code 27-2097", "city", "statute", "S10 preconditions", "Owners of multiple dwellings must register annually with HPD.",
  S+"REVIEW1_NYC_ADC_27-2097.txt", sent(r"register")),
 ("Admin. Code 8-102 (lawful source of income)", "city", "statute", "S21 anti-discrimination", "NYC 'lawful source of income' includes housing vouchers and public assistance.",
  S+"REVIEW5A_NYC_ADC_8-102.txt", r"The term \"lawful source of income\" includes, but is not limited to, child support, alimony, foster care subsidies, income derived from social security, or any form of federal, state, or local public assistance or housing assistance including, but not limited to, section 8 vouchers"),
 ("GOL 7-109", "state", "statute", "S8 exposure", "Attorney General may sue to compel compliance with GOL art. 7 title 1 and enjoin violations.",
  S+"NY_GOL_7-109_nysenate.txt", r"If it appears to the attorney general that any person, association, or corporation has violated or is violating any of the provisions of this title, an action or proceeding may be instituted by the attorney general"),
 ("Executive Law 297(9)", "state", "statute", "S21 exposure", "Person aggrieved by housing discrimination may sue for damages, including punitive damages, and fees.",
  S+"REVIEW5A_NY_EXC_297.txt", sent(r"punitive damages")),
 ("HUD-52641-A HCV Tenancy Addendum", "federal", "guidance", "S5 charges (voucher tenant)", "HCV tenant is not responsible for the HAP portion of rent; only the tenant share is collectible from the family.",
  S+"US_HUD_52641-A_HCV_tenancy_addendum.txt", sent(r"not responsible for paying")),
]
