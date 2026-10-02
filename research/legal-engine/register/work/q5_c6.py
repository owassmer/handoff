import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

A166 = "US:26CFR1.166-1(e)-bad-debt"
A6049 = "US:26USC6049-deposit-interest"
A6050P = "US:26USC6050P-no-1099C"
TAXSCOPE = "Outside the three tax events in this chain (a deposit kept, interest passed through, a balance written off)"

# --- 6041 regulations: manager remitting rent, including the kept deposit, to the owner
p = rule("US:26 CFR 1.6041-1", "US:26CFR1.6041-1-agent-reports-rent", "26 CFR 1.6041-1(a)(1)(i)(B), (a)(1)(ii), (a)(1)(iv), (e)(1)-(2), (e)(5) Example 5, (f), (h)", "manager; Handoff", "shall",
         "A managing agent (or Handoff, where it receives the tenant's money and remits it) collects rent and other amounts from the tenancy for an owner, including the part of a former tenant's deposit kept for rent or damage, and pays them to the owner in the course of its business.",
         "The agent is the payor that files Form 1099-MISC (rents) for the owner for the calendar year, whether or not it performs management functions, reporting the gross rents collected for the owner (including the kept deposit, which is the owner's income when kept, US:IRS-Pub527-deposit-income) before deducting its commission, repair costs and other amounts it pays out for the owner. The threshold is the 6041(a) amount ($2,000 for payments made after 2025-12-31; $600 before). An amount counts as paid when it is credited or set apart to the owner without substantial restriction and made available to draw. Where Handoff and the manager both handle the payment, the one closest to the owner in the chain files, unless they agree in writing that the other will. Not reportable: the refund of a tenant's own deposit; interest on the deposit (reported under 6049, US:26USC6049-deposit-interest); amounts settled by payment card or third-party network, which are reported under 6050W; payments to an owner that is a corporation (US:26CFR1.6041-3-exceptions) or a foreign owner documented as foreign (US:26CFR1.6041-4-foreign-owner). The returns are due as US:26CFR1.6041-6-filing-dates states.",
         "major", "8.11", "(a) General rule—(1) Information returns required—(i) Payments required to be reported.", "(B) Interest (including original issue discount), rents, royalties, annuities, pensions, and other gains, profits, and income aggregating $600 or more.",
         dependencies=[A166, "US:IRS-Pub527-deposit-income"],
         construction=[{"source_file": "register/texts/US_26CFR1-info/1.6041-1.txt", "quote": "With respect to the payment of rent to H, G is subject to the information reporting requirements of section 6041 regardless of whether she performs management or oversight functions or has a significant economic interest in the payment."},
                       {"source_file": "register/texts/US_26CFR1-info/1.6041-1.txt", "quote": "the person obligated to report the payment is the person closest in the chain to the payee, unless the parties agree in writing that one of the other parties meeting the requirements set forth in paragraph (e)(1) of this section will report the payment."},
                       {"source_file": "sources/REVIEW5A_US_26USC_6041.txt", "quote": "of $2,000 or more in any calendar year"}],
         reasoning="Example 5 of 1.6041-1(e)(5) makes a rental agent that collects rent and remits it to the owner the reporting payor for the rent; 1.6041-1(f) reports the gross amount includible in the owner's income; the statute's $2,000 threshold for payments after 2025 overrides the regulation's $600.")
add("US:26 CFR 1.6041-1", "partial",
    "Makes the managing agent file Form 1099-MISC to the owner for rents it collects and remits, which includes the part of a deposit kept; the existing rule states only that a deposit refund to the tenant is not reportable.",
    atom_ids=[A166], proposed=[{**p, "amends": A166}])

nd("US:26 CFR 1.6041-2", "Reporting of wages to employees on Form W-2; no payment in the settlement chain is wages.")

add("US:26 CFR 1.6041-3", "new_rule",
    "States the exceptions that decide whether the agent's 1099 to the owner is due (owner a corporation) and that a tenant paying rent to a rental agent files nothing.",
    proposed=[rule("US:26 CFR 1.6041-3", "US:26CFR1.6041-3-exceptions", "26 CFR 1.6041-3(d), (p)(1)", "manager; tenant", "need not",
                   "Rent or a kept deposit moves from a tenant to a rental agent, or from the agent to the owner.",
                   "A tenant (including a company tenant in a trade or business) that pays rent to a rental agent files no information return; the agent reports the rent it pays the landlord. The agent files no 1099-MISC for payments to an owner that is a corporation (an LLC is a corporation for this purpose only if it has elected to be taxed as one; a single-member LLC owned by an individual, or a multi-member LLC taxed as a partnership, is not exempt), a tax-exempt organization, or a governmental unit.",
                   "minor", "8.11", "(d) Payments of rent made to rental agents", "in accordance with § 1.6041-1(a)(1)(i)(B) and (2)).")])

add("US:26 CFR 1.6041-4", "new_rule",
    "If the owner is a foreign person documented as such, the agent's rent remittance (including a kept deposit) is not reported on Form 1099.",
    proposed=[rule("US:26 CFR 1.6041-4", "US:26CFR1.6041-4-foreign-owner", "26 CFR 1.6041-4(a)(1)", "manager; Handoff", "need not",
                   "The agent remits rent (including a kept deposit) to an owner it can, before paying, reliably associate with documentation that the owner is a foreign beneficial owner or foreign payee (Form W-8).",
                   "No Form 1099 is filed for the payment; the payment is instead within the withholding and Form 1042-S reporting rules for U.S.-source rent paid to foreign persons (26 U.S.C. 1441; 26 CFR 1.1461-1), under which rent is subject to 30% withholding unless the owner has furnished Form W-8ECI treating it as effectively connected income. Without reliable documentation the owner is presumed a U.S. payee and 1099 reporting applies (US:26CFR1.6041-1-agent-reports-rent).",
                   "minor", "8.11", "(a) Exempted foreign-related items.(1) Returns of information are not required for payments that a payor can, prior to payment, reliably associate with documentation",
                   "as made to a foreign beneficial owner in accordance with § 1.1441-1(e)(1)(ii)")])

nd("US:26 CFR 1.6041-5", "Lets a payor demand the actual owner's name from a nominee payee; the agent's filing duty and payee for a kept deposit are fixed by US:26CFR1.6041-1-agent-reports-rent and do not turn on it.")

add("US:26 CFR 1.6041-6", "new_rule",
    "Fixes the due date of the agent's Form 1099-MISC for rents (including a kept deposit) remitted to the owner.",
    proposed=[rule("US:26 CFR 1.6041-6", "US:26CFR1.6041-6-filing-dates", "26 CFR 1.6041-6(a), (b)", "manager; Handoff", "shall",
                   "The agent must file Form 1099-MISC for rents (including a kept deposit) it paid an owner in a calendar year (US:26CFR1.6041-1-agent-reports-rent).",
                   "File Forms 1099 with transmittal Form 1096 by February 28 of the following year on paper, or March 31 if filed electronically, stating the payer's and the owner's names, addresses and taxpayer identification numbers (the last known address if the present one is unknown). Nonemployee compensation returns are due January 31. The owner's copy is furnished by January 31 (26 U.S.C. 6041(d)). A payer filing 10 or more information returns of all types for the year must file electronically (26 CFR 301.6011-2).",
                   "major", "8.11", "(a) In general. Except as provided in paragraph (b) of this section, returns made under section 6041", "shall be filed on or before January 31 of the year following the calendar year to which such returns relate.")])

nd("US:26 CFR 1.6041-7", "Magnetic-media permission and health-care carrier returns; the electronic-filing threshold that binds the agent is 301.6011-2, noted in US:26CFR1.6041-6-filing-dates.")
nd("US:26 CFR 1.6041-8", "Cross-reference to the 6721 and 6722 penalty regulations; it states no duty or amount itself.")
nd("US:26 CFR 1.6041-10", "Reporting of bingo, keno and slot-machine winnings; no payment in the settlement chain.")

# --- 6049 regulations: interest on the deposit
p = rule("US:26 CFR 1.6049-4", "US:26CFR1.6049-4-middleman-return", "26 CFR 1.6049-4(a)(2)(ii), (b)(1), (b)(3), (b)(5), (c)(1), (d)(6), (f)(4)", "landlord; manager", "shall",
         "The landlord (or its managing agent) collects the interest earned on a tenant's deposit in a bank account and pays or credits it to the tenant (yearly, as a rent credit, or at the end of the tenancy).",
         "The landlord or agent is a middleman (a nominee collecting interest for another) and files Form 1099-INT for each calendar year in which it pays or credits the tenant $10 or more, showing the aggregate interest, the tenant's name, address and taxpayer identification number, and any backup withholding. Interest counts as paid when credited or set apart to the tenant without substantial restriction and available to draw (the year the lease ends, for interest paid at termination). If the tenant does not furnish a TIN on request, the landlord backup-withholds under 26 U.S.C. 3406 and files even below $10. No return is required for a tenant that is a corporation (an exempt recipient). For a tenant who is a nonresident alien resident in a country listed by revenue procedure, the interest is reported on Form 1042-S instead (US:26CFR1.6049-8-nra-tenant).",
         "major", "8.11", "(ii) Every person who collects on behalf of another person payments of the type and of the amount subject to reporting under this section",
         "acts as a middleman (as defined in paragraph (f)(4) of this section) with respect to such payment.",
         dependencies=[A6049])
add("US:26 CFR 1.6049-4", "partial",
    "Adds to the deposit-interest rule the middleman capacity, the year the interest counts as paid, backup withholding, and the corporate and foreign-tenant branches.",
    atom_ids=[A6049], proposed=[{**p, "amends": A6049}])

add("US:26 CFR 1.6049-5", "new_rule",
    "Decides which deposit interest is reportable under 6049: interest passed through from the bank account is; interest a landlord pays from its own funds is not (and from an individual landlord is excluded outright).",
    proposed=[rule("US:26 CFR 1.6049-5", "US:26CFR1.6049-5-which-interest", "26 CFR 1.6049-5(a)(2), (b)(1)", "landlord", "applies",
                   "The landlord pays or credits a former tenant interest on the deposit.",
                   "(1) Interest the bank pays on the account holding the deposit, which the landlord passes to the tenant, is interest on a deposit with a person carrying on the banking business and is reported under US:26CFR1.6049-4-middleman-return. (2) An amount the landlord pays out of its own funds as interest on its own deposit obligation (not bank interest collected for the tenant) is not 6049 interest: the obligation is not in registered form or offered to the public, and if the landlord is an individual it is an obligation of a natural person, which is excluded. A landlord in a trade or business that pays such an amount of $2,000 or more in a calendar year (payments after 2025) reports it as interest on Form 1099 under 6041 (US:26CFR1.6041-1-agent-reports-rent sets the threshold rule).",
                   "minor", "8.11", "(2) Interest on deposits with persons carrying on the banking business.", "irrespective of whether such interest is collected on behalf of the holder of the obligation by a middleman.")])

p = rule("US:26 CFR 1.6049-6", "US:26CFR1.6049-6-tenant-statement", "26 CFR 1.6049-6(a), (b)(1), (c), (d)", "landlord; manager", "shall",
         "The landlord files Form 1099-INT for interest it passed to a former tenant (US:26CFR1.6049-4-middleman-return).",
         "It furnishes the tenant a statement (a copy of the Form 1099-INT or an acceptable substitute) showing the aggregate interest, any backup withholding, the landlord's name and address, the tenant's name, address and TIN (a truncated TIN may be used), and a legend that the amount is reported to the IRS, after April 30 of the year of payment and by January 31 of the next year, and not before the final interest payment for the year. Mailing it to the tenant's last known address (the forwarding address from the move-out) is furnishing it.",
         "major", "8.11", "(c) Time for furnishing statements.", "but no statement may be furnished before the final interest payment for the calendar year.",
         dependencies=[A6049])
add("US:26 CFR 1.6049-6", "partial",
    "Adds the deadline and content of the statement the landlord must give the former tenant for passed-through deposit interest.",
    atom_ids=[A6049], proposed=[{**p, "amends": A6049}])

add("US:26 CFR 1.6049-8", "new_rule",
    "A former tenant who is a nonresident alien resident in a listed country gets deposit interest reported on Form 1042-S.",
    proposed=[rule("US:26 CFR 1.6049-8", "US:26CFR1.6049-8-nra-tenant", "26 CFR 1.6049-8(a); 1.6049-4(b)(5)", "landlord; manager", "shall",
                   "The landlord passes bank-deposit interest (from an account at a U.S. office) to a former tenant who is a nonresident alien individual resident in a country the IRS lists by revenue procedure (as of December 31 of the prior year) as one with which the United States has an information-exchange agreement.",
                   "The interest is reportable: if it totals $10 or more for the year, the landlord files Form 1042-S (not 1099-INT) at the time and in the manner section 1461 prescribes, and furnishes the tenant a copy. Interest to a nonresident alien resident elsewhere is not reportable under 6049.",
                   "minor", "8.11", "(a) Interest subject to reporting requirement.", "that relates to a deposit maintained at an office within the United States")])

nd("US:26 CFR 1.6049-1", "Interest reporting for calendar years before 1983; superseded for any payment in this chain by 1.6049-4.")
nd("US:26 CFR 1.6049-2", "Definitions of interest and original issue discount for pre-1983 reporting; the operative definition for current payments is 1.6049-5.")
nd("US:26 CFR 1.6049-3", "Statements to recipients for calendar years before 1983; current statements are governed by 1.6049-6.")
nd("US:26 CFR 1.6049-7", "Reporting for REMIC regular interests and collateralized debt obligations; no deposit or balance in this chain is one.")
nd("US:26 CFR 1.6049-9", "Premium on purchased debt instruments; not a deposit, interest pass-through or write-off in this chain.")

# --- 6050P regulations: debt buyer branch
p = rule("US:26 CFR 1.6050P-2", "US:26CFR1.6050P-2-debt-buyer", "26 CFR 1.6050P-2(a), (b), (c), (e)", "debt buyer; landlord", "shall",
         "A former tenant's balance is written off, settled for less, or sold.",
         "A landlord that extends credit only as part of renting (unpaid rent and charges) is not in a trade or business of lending money (seller financing), so it never files Form 1099-C (US:26USC6050P-no-1099C). A buyer of the balance is an applicable entity, and must file 1099-C when it discharges the balance, if it lends money on a regular and continuing basis (acquiring debts from prior holders counts as lending), unless its gross income from lending in its most recent test year was below both $5 million and 15% of its gross income (below $3 million and 10% in each of its three most recent test years if it reported in the prior year), or it has no test year. A collection agency collecting for the landlord without owning the balance is not the creditor and files nothing.",
         "minor", "8.11", "(e) Acquisition of an indebtedness from a person other than the debtor included in lending money.", "the organization is engaged in a significant trade or business of lending money.",
         dependencies=[A6050P])
add("US:26 CFR 1.6050P-2", "partial",
    "Adds the branch where the balance is sold to a debt buyer that is an applicable entity and must file Form 1099-C; the existing rule covers only the landlord.",
    atom_ids=[A6050P], proposed=[{**p, "amends": A6050P}])

p = rule("US:26 CFR 1.6050P-1", "US:26CFR1.6050P-1-identifiable-events", "26 CFR 1.6050P-1(a)(1)-(4), (b)(2), (f)", "debt buyer", "shall",
         "A buyer of a former tenant's balance that is an applicable entity (US:26CFR1.6050P-2-debt-buyer) discharges $600 or more of it in a calendar year.",
         "It files Form 1099-C for the year of the identifiable event: a bankruptcy discharge (reported for the later of the year it occurs or the year the discharged amount becomes ascertainable); a final judgment upholding the tenant's statute-of-limitations defence; an agreement to settle for less than full consideration; or a decision or defined policy (written or established practice) to stop collecting and discharge the debt. It reports the tenant's name, address and TIN, the date, the amount and whether the discharge was in bankruptcy, whether or not the amount is taxable to the tenant, files by February 28 (March 31 electronically), and furnishes the tenant a copy. Separate discharges under $600 are not aggregated unless structured to evade reporting.",
         "minor", "8.11", "(2) Identifiable events—(i) In general. An identifiable event is—", "to discontinue collection activity and discharge debt.",
         dependencies=[A6050P])
add("US:26 CFR 1.6050P-1", "partial",
    "States when and what a debt-buyer applicable entity files on discharging a purchased tenant balance.",
    atom_ids=[A6050P], proposed=[{**p, "amends": A6050P}])

nd("US:26 CFR 1.6050P-0", "Table of contents for 1.6050P-1 and -2; it states no rule.")

# --- 166 and regulations
p = rule("US:26 USC 166", "US:26USC166-writeoff-deduction", "26 U.S.C. 166(a), (b), (d)", "owner", "may",
         "The owner writes off all or part of a former tenant's balance (rent, damage or other charges) as uncollectible.",
         "(1) The deduction is limited to the owner's adjusted basis in the claim: a rent balance has basis only if the rent was included in income (accrual basis, US:26CFR1.166-1(e)-bad-debt); a damage or cost reimbursement claim has basis only to the extent the owner included it in income or did not deduct the underlying cost; a cash-basis owner that deducted the repair cost has no basis and no bad-debt deduction. (2) Timing: the deduction is taken for the year the debt becomes worthless, not the year the owner chooses. (3) Business debt (the rental activity is a trade or business, or the owner is a corporation): a wholly worthless debt is deducted in full; a partly worthless debt is deducted up to the part charged off on the books that year (US:26CFR1.166-3-charge-off). (4) Nonbusiness debt of a non-corporate owner (a rental that is not a trade or business): deductible only when wholly worthless, as a short-term capital loss (US:26CFR1.166-5-nonbusiness).",
         "major", "8.11", "(a) General rule (1) Wholly worthless debts", "of a capital asset held for not more than 1 year.",
         determinacy="MIXED", judgment_terms=["worthless", "trade or business"], dependencies=[A166])
add("US:26 USC 166", "partial",
    "Adds basis, timing, partial worthlessness and the nonbusiness branch to the existing prior-inclusion rule for writing off a balance.",
    atom_ids=[A166], proposed=[{**p, "amends": A166}])

add("US:26 CFR 1.166-2", "new_rule",
    "Fixes what shows a balance is worthless (no suit needed when a judgment would be uncollectible; bankruptcy) and bars moving the deduction to a later year.",
    proposed=[rule("US:26 CFR 1.166-2", "US:26CFR1.166-2-worthlessness-evidence", "26 CFR 1.166-2(a)-(c)", "owner", "may",
                   "The owner decides in which year a former tenant's balance became worthless for the bad-debt deduction (US:26USC166-writeoff-deduction).",
                   "Worthlessness is judged on all pertinent evidence, including any collateral (the deposit applied) and the tenant's financial condition. The owner need not sue: facts showing that legal action would in all probability not produce satisfaction of a judgment suffice. The tenant's bankruptcy indicates at least partial worthlessness of an unsecured debt; the debt may become worthless before or only at the bankruptcy settlement, and the deduction cannot be shifted to the later year in which the case ends.",
                   "minor", "8.11", "(a) General rule. In determining whether a debt is worthless", "shall not authorize the shifting of the deduction under section 166 to such later year.",
                   determinacy="STANDARD", judgment_terms=["worthless and uncollectible", "in all probability not result in the satisfaction"])])

add("US:26 CFR 1.166-3", "new_rule",
    "A partly uncollectible balance is deductible only for the amount charged off on the books that year.",
    proposed=[rule("US:26 CFR 1.166-3", "US:26CFR1.166-3-charge-off", "26 CFR 1.166-3(a)(1)-(2), (b)", "owner", "may",
                   "An owner whose balance is a business debt writes off part of a former tenant's balance (for example, the part beyond what a settlement or payment plan will recover).",
                   "The partial deduction is allowed for the specific debt only to the extent the owner charged it off during that tax year, and the owner must be able to show the worthless amount and the part charged off. A later partial deduction is allowed up to amounts charged off in prior and current years. When the debt becomes wholly worthless, the part not already deducted is deducted that year.",
                   "minor", "8.11", "(a) Partial worthlessness—(1) Applicable to specific debts only.", "shall be allowed as a deduction for the current taxable year.")])

add("US:26 CFR 1.166-5", "new_rule",
    "An individual owner whose rental is not a trade or business deducts a worthless balance only when wholly worthless, as a short-term capital loss.",
    proposed=[rule("US:26 CFR 1.166-5", "US:26CFR1.166-5-nonbusiness", "26 CFR 1.166-5(a), (b)", "owner", "may",
                   "The owner is not a corporation and the former tenant's balance was not created in connection with a trade or business of the owner (the rental is an investment, not a trade or business).",
                   "No deduction for partial worthlessness. When the balance becomes wholly worthless, the loss is a short-term capital loss for that year, subject to the capital-loss limits of sections 1211 and 1212 ($3,000 a year against ordinary income for individuals, with carryover). Whether the balance is a business debt is a question of fact about the owner's rental activity.",
                   "minor", "8.11", "(a) Allowance of deduction as capital loss.", "and in the regulations under those sections.",
                   determinacy="MIXED", judgment_terms=["trade or business of the taxpayer"])])

nd("US:26 CFR 1.166-4", "The reserve method for bad debts, repealed for tax years after 1986 except for specified financial institutions; an owner deducts a written-off balance only under the specific charge-off method (US:26USC166-writeoff-deduction).")
nd("US:26 CFR 1.166-6", "Sale of mortgaged or pledged property by a secured creditor; the landlord holds no such security for a tenant balance (the deposit is applied, not sold).")
nd("US:26 CFR 1.166-7", "Worthless bonds issued by an individual; a tenant balance is not a bond.")
nd("US:26 CFR 1.166-8", "Losses of guarantors on pre-1976 obligations; the landlord is the creditor, not a guarantor.")
nd("US:26 CFR 1.166-9", "Losses of guarantors, endorsers and indemnitors; the landlord is the creditor, and a guarantor's own tax treatment is outside the landlord's chain.")
nd("US:26 CFR 1.166-10", "Reserve for guaranteed debt obligations of dealers; not the landlord's position.")
