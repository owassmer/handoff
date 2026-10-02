import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

S524 = "sources/US_11USC_524.txt"

add("US:FRBP 4001", "new_rule",
    "Governs how and when the landlord gets relief from the stay to apply the deposit (motion as a contested matter, 14-day stay of the order, court approval of any agreement with the debtor); the existing hold rule requires a prompt motion but not its procedure or timing.",
    proposed=[rule("US:FRBP 4001", "US:FRBP4001-stay-relief-procedure", "FRBP 4001(a)(1)-(4), (d)(1)-(3)", "landlord; collector", "shall",
                   "A former tenant is a debtor and the landlord wants to apply the held deposit to pre-petition charges (US:CASE-Strumpf-hold) or otherwise act on the balance, or has agreed with the tenant or trustee to do so.",
                   "(1) The landlord moves under 362(d) for relief from the stay as a contested matter (FRBP 9014), served on the committee or, in chapter 11 without one, the 20 largest unsecured creditors, and any entity the court designates; the stay terminates 30 days after the motion unless the court continues it after a hearing (362(e)). (2) Relief without prior notice is available only on an affidavit or verified motion showing immediate and irreparable injury before the tenant can be heard, with the attorney's certificate of notice efforts, and the landlord must then give immediate oral notice and promptly send the order. (3) Unless the court orders otherwise, an order granting relief is itself stayed for 14 days after entry: the landlord does not apply the deposit until the 15th day. (4) A stipulation with the tenant or trustee to lift the stay or to apply the deposit is not effective until the court approves it on a motion attaching the agreement and a proposed order; objections are due 14 days after notice is mailed, and without objection the court may approve without a hearing. After relief, the deposit is set off only against pre-petition charges (US:11USC362(a)(7)-deposit-is-setoff) and any rest is refunded to the payee in US:11USC542-refund-payee.",
                   "critical", "6.7", "(a) Relief from the Automatic Stay; Prohibiting or Conditioning the Use, Sale, or Lease of Property. (1) Motion.", "is stayed for 14 days after it is entered.",
                   dependencies=["US:CASE-Strumpf-hold", "US:11USC362(a)(7)-deposit-is-setoff", "US:11USC542-refund-payee"])])

nd("US:FRBP 4002", "The debtor's duties (attend, cooperate, bring identification and financial records); no duty or right of the landlord in the chain.")
nd("US:FRBP 4005", "Places the burden of proof on the plaintiff at a trial objecting to discharge; the landlord's decision to object and its deadline are proposed at 727 and FRBP 4004, and the burden changes no deadline, amount or payee.")

add("US:FRBP 4006", "new_rule",
    "The clerk's notice that a tenant's case closed without a discharge (or that discharge was denied, revoked or waived) tells the landlord the balance survives and may be collected once the stay ends.",
    proposed=[rule("US:FRBP 4006", "US:FRBP4006-no-discharge-notice", "FRBP 4006(a)-(d)", "landlord; collector; manager", "may",
                   "The landlord receives the clerk's notice of an order denying, revoking or waiving a former tenant's discharge, or closing the individual tenant's case without a discharge (for example, for failure to file the financial-management course certificate).",
                   "No discharge covers the balance, so the discharge injunction does not apply to it (US:11USC524(a)(2) does not attach). Once the stay has ended (on closing, dismissal, or denial of discharge under 362(c)), the landlord may collect the whole balance, subject to the limitation period extended by US:11USC108(c)-extension. A case closed without discharge only for a missing course certificate may be reopened for the tenant to file it, and a discharge then entered covers the balance, so collection stops again when the landlord learns of the discharge.",
                   "minor", "8.8", "The clerk must promptly notify in the manner provided by Rule 2002(f)", "closing an individual debtor’s case without entering a discharge.",
                   dependencies=["US:11USC524(a)(2)", "US:11USC108(c)-extension"])])

add("US:FRBP 4008", "new_rule",
    "Sets how a landlord can keep a bankrupt tenant personally liable by agreement (a reaffirmation made before discharge, filed within 60 days after the first 341 date) and confirms that voluntary repayment and co-debtors' liability survive the discharge.",
    proposed=[rule("US:FRBP 4008", "US:FRBP4008-reaffirmation", "FRBP 4008(a)-(b); 11 U.S.C. 524(c), (e), (f)", "landlord; collector; manager", "may",
                   "A former tenant who is an individual is a debtor and the landlord would keep the tenant personally liable for a dischargeable balance by agreement, or the tenant offers to pay after discharge, or a co-tenant or guarantor is also liable.",
                   "(1) An agreement to pay a dischargeable balance binds the tenant only if made before the discharge, with the 524(k) disclosures given at or before signing, filed with the court with the Form 427 cover sheet within 60 days after the first date set for the 341 meeting (the court may extend the time), with the tenant's supporting statement of income and expenses, with the attorney's declaration if the tenant had counsel, and, if the tenant had no counsel, approved by the court as not an undue hardship and in the tenant's best interest; the tenant may rescind until the later of discharge or 60 days after filing. An agreement not meeting these terms is unenforceable, and demanding payment under it after discharge violates the discharge injunction (US:11USC105-discharge-contempt). (2) Nothing bars the tenant from voluntarily repaying a discharged balance, and the landlord may accept it, but may not ask for it. (3) The discharge does not affect the liability of any other entity: a co-tenant or guarantor stays liable for the whole balance and may be pursued after any co-debtor stay ends (US:11USC1301-codebtor-stay).",
                   "major", "8.8", "(a) Time to File; Cover Sheet.", "the supporting statement must explain the difference.",
                   dependencies=["US:11USC524(a)(2)", "US:11USC1301-codebtor-stay"],
                   construction=[{"source_file": S524, "quote": "(1) such agreement was made before the granting of the discharge under section 727, 1141, 1192, 1228, or 1328 of this title;"},
                                 {"source_file": S524, "quote": "(4) the debtor has not rescinded such agreement at any time prior to discharge or within sixty days after such agreement is filed with the court, whichever occurs later, by giving notice of rescission to the holder of such claim;"},
                                 {"source_file": S524, "quote": "(e) Except as provided in subsection (a)(3) of this section, discharge of a debt of the debtor does not affect the liability of any other entity on, or the property of any other entity for, such debt."},
                                 {"source_file": S524, "quote": "(f) Nothing contained in subsection (c) or (d) of this section prevents a debtor from voluntarily repaying any debt."}],
                   reasoning="Rule 4008 times and documents the reaffirmation; 524(c) sets its enforceability conditions, 524(e) preserves co-debtors' liability and 524(f) permits voluntary repayment. Asking a discharged debtor to pay is an act to collect under 524(a)(2), so only unsolicited voluntary payment may be accepted.")])

nd("US:FRBP 3002.1", "Notices by holders of claims secured by the debtor's principal residence in chapter 13; a residential landlord holds no such security interest.")
nd("US:FRBP 3004", "Lets the debtor or trustee file a claim for a creditor that did not file by its deadline; the landlord's own deadline and duties are unchanged (US:FRBP-3002(c)-claim-deadline).")
nd("US:FRBP 3006", "Withdrawal of a proof of claim by the creditor; an optional act that changes no deadline, amount or payee in the chain.")
nd("US:FRBP 3007", "Procedure for objections to claims (30 days' notice to the claimant); the claim's validity turns on the substantive rules (502, 506, 558) proposed or stated elsewhere, and the rule sets no deadline for the landlord.")
nd("US:FRBP 3008", "Reconsideration of an order allowing or disallowing a claim; litigation procedure, no chain decision.")
nd("US:FRBP 3009", "Chapter 7 trustee pays dividends and the clerk's notice; distribution order is proposed at 726 (US:11USC726-ch7-distribution-order).")
nd("US:FRBP 3010", "Small dividends (under $5 in chapter 7, $15 in chapter 13) may be withheld; no chain decision.")
nd("US:FRBP 3011", "Unclaimed funds in chapter 7, subchapter V, 12 and 13 cases are paid into court; the landlord's claim right is unchanged.")
nd("US:FRBP 3012", "Procedure for determining the amount of a secured or priority claim; the substantive result for the deposit setoff is proposed at 506 (US:11USC506-deposit-secured-claim).")
nd("US:FRBP 3013", "Court determination of classes of creditors in chapter 11 and 13 plans; plan process.")
nd("US:FRBP 3014", "Election by a secured class under 1111(b) in chapter 9 or 11; the landlord holds no lien on the owner's property as a tenant creditor, and a tenant holds none either.")
nd("US:FRBP 3015.1.11Secondperiodeditoriallyadded", "Requirements for a district's local chapter 13 plan form; plan form, no chain decision.")
nd("US:FRBP 3016", "Chapter 9 and 11 plan and disclosure statement filing; plan process.")
nd("US:FRBP 3017", "Chapter 9 and 11 disclosure statement hearing and mailing; plan process.")
nd("US:FRBP 3017.1", "Conditional approval of a small business disclosure statement; plan process.")
nd("US:FRBP 3017.2", "Setting dates in a subchapter V case; plan process.")
nd("US:FRBP 3018", "Accepting or rejecting a chapter 9 or 11 plan (balloting); plan process.")
nd("US:FRBP 3019", "Modifying a chapter 9 or 11 plan; plan process.")
nd("US:FRBP 3020", "Deposit of funds and objections to confirmation in chapter 11; plan process (objection by a tenant creditor changes no step of the manager's chain).")
nd("US:FRBP 3021", "Distribution under a chapter 11 plan to record holders; the tenant's receipt follows the plan (US:11USC1141-owner-plan-confirmed).")
nd("US:FRBP 3022", "Final decree closing a chapter 11 case; case administration.")
