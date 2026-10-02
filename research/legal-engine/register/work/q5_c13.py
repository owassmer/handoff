import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

add("US:11 USC 546", "new_rule",
    "Fixes how long a landlord that received pre-filing payments or took a setoff stays exposed to a trustee's avoidance suit (2 years after the order for relief, or before the case closes).",
    proposed=[rule("US:11 USC 546", "US:11USC546(a)-avoidance-deadline", "11 U.S.C. 546(a)", "landlord; collector", "applies",
                   "A former tenant's trustee (or debtor in possession) could attack a payment or transfer the landlord received as a preference (547), fraudulent transfer (548, 544) or setoff improvement (553).",
                   "The avoidance action must be commenced before the earlier of (1) the later of 2 years after the order for relief or 1 year after the first trustee is appointed or elected, if that happens within the 2 years, and (2) the time the case is closed or dismissed. After that the landlord keeps the payment. A post-petition transfer under 549 has its own limit (US:11USC549-postpetition-payment), and recovery from a transferee after avoidance must be sued within one year (US:11USC550-transferee-liability).",
                   "major", "8.8", "(a) An action or proceeding under section 544, 545, 547, 548, or 553 of this title may not be commenced after the earlier of—", "(2) the time the case is closed or dismissed.",
                   dependencies=[])])

add("US:11 USC 554", "new_rule",
    "When the chapter 7 trustee abandons the deposit refund (or the case closes with it scheduled and not administered), the refund reverts to the tenant, which moves the payee from the trustee to the tenant.",
    proposed=[rule("US:11 USC 554", "US:11USC554-abandoned-refund", "11 U.S.C. 554(a)-(d)", "landlord; manager", "shall",
                   "A former tenant is a chapter 7 debtor and its deposit refund is estate property payable to the trustee (US:11USC542-refund-payee branch (a)).",
                   "If the trustee abandons the refund after notice and a hearing (as burdensome or of inconsequential value), or the court orders it abandoned on a party's request, or the case closes with the refund scheduled and not administered, the refund is no longer estate property and is paid to the tenant. A refund that was not scheduled and not administered remains estate property after closing, and is paid to the trustee if the case is reopened; before the landlord pays the tenant on this ground it confirms the refund was listed in the tenant's schedules or the trustee has abandoned it in writing. An exempted refund leaves the estate the same way (US:11USC522-refund-exemption).",
                   "critical", "6.7", "(a) After notice and a hearing, the trustee may abandon", "remains property of the estate.",
                   dependencies=["US:11USC542-refund-payee"])])

nd("US:11 USC 551", "Preserves an avoided transfer for the estate; the landlord's liability on an avoided transfer is proposed at 550 (US:11USC550-transferee-liability).")
nd("US:11 USC 560", "Contractual rights to liquidate or terminate swap agreements; out of aperture for this chain (financial contracts).")
nd("US:11 USC 561", "Contractual rights under securities, commodity, forward, repurchase, swap and master netting agreements; out of aperture for this chain (financial contracts).")
nd("US:11 USC 562", "Timing of damages under swap, repurchase and master netting agreements; out of aperture for this chain (financial contracts).")
TA = "Chapter 7 trustee administration"
nd("US:11 USC 701", TA + ": appointment of the interim trustee; the trustee's collection and payee role is stated in US:11USC541-704-owner-chapter7 and US:11USC542-refund-payee.")
nd("US:11 USC 702", TA + ": election of the trustee by creditors.")
nd("US:11 USC 703", TA + ": successor trustee.")
nd("US:11 USC 705", TA + ": creditors' committee in chapter 7.")
nd("US:11 USC 706", "The debtor's right to convert a chapter 7 case at any time and the court's power to convert on request; the effects of conversion are proposed at 348 (US:11USC348-conversion).")
nd("US:11 USC 721", TA + ": the court may let the trustee operate the owner's business; that the trustee then collects is stated in US:11USC541-704-owner-chapter7 and US:11USC363-owner-cash-collateral.")
nd("US:11 USC 722", "Redemption of household personal property from a lien; a residential landlord holds no lien on the tenant's personal property.")
nd("US:11 USC 723", "Rights of a partnership trustee against general partners; no chain decision.")
nd("US:11 USC 724", "Avoidance of liens securing penalty claims and subordination of tax liens in chapter 7; a residential landlord holds no such lien for the balance.")
nd("US:11 USC 725", TA + ": disposition of property in which another entity has an interest before final distribution.")
