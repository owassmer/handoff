import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

p = rule("US:11 USC 105", "US:11USC105-discharge-contempt", "11 U.S.C. 105(a); 524(a)(2)", "landlord; manager; collector; Handoff", "is liable",
         "After a former tenant's discharge covering the balance (US:11USC524(a)(2)), the landlord, its manager, a collector or Handoff demands, reports as owed, sues on, sets off or otherwise acts to collect the discharged balance as the tenant's personal liability.",
         "The bankruptcy court enforces the discharge injunction by civil contempt under 105(a). The creditor is held in contempt if there is no fair ground of doubt that the order barred its conduct (Taggart v. Lorenzen, 587 U.S. 554 (2019)); a good-faith belief that the discharge did not apply does not excuse conduct the order plainly covered. Sanctions are compensatory (the tenant's actual damages, including its attorney's fees and costs) and coercive; the court may reopen the case for this without a fee. The creditor's defence is that the debt was excepted from discharge (523, determined as US:FRBP4007-523c-deadline requires) or not provided for. Before a discharge, stay violations are governed by 362(k) and 342(g) (US:11USC342-effective-notice).",
         "critical", "8.8", "(a) The court may issue any order, process, or judgment that is necessary or appropriate to carry out the provisions of this title.",
         "necessary or appropriate to carry out the provisions of this title.",
         determinacy="MIXED", judgment_terms=["fair ground of doubt"], dependencies=["US:11USC524(a)(2)"])
p["reasoning"] = "Section 524(a)(2) makes the discharge an injunction; 105(a) empowers the court to issue orders to carry it out, which is the source of civil contempt for violations. Taggart v. Lorenzen, 587 U.S. 554 (2019), fixes the standard (no fair ground of doubt as to whether the order barred the conduct)."
add("US:11 USC 105", "partial",
    "Supplies the consequence of violating the discharge injunction (civil contempt with compensatory sanctions, Taggart standard); the existing discharge rule states the injunction without its sanction.",
    atom_ids=["US:11USC524(a)(2)"], proposed=[{**p, "amends": "US:11USC524(a)(2)"}])

nd("US:11 USC 107", "Makes bankruptcy filings public records with protective exceptions; it creates no duty or right for the landlord in the settlement chain.")
nd("US:11 USC 110", "Regulates bankruptcy petition preparers; neither the landlord, the manager, Handoff nor a collector prepares a debtor's petition in this chain.")
nd("US:11 USC 111", "Approval of credit counseling and financial-management agencies; affects the debtor's eligibility and discharge conditions, stated in the discharge rules, not the landlord's conduct.")
nd("US:11 USC 112", "Protects the names of the debtor's minor children in public records; no effect on the landlord's conduct.")
nd("US:11 USC 1103", "Powers of a chapter 11 creditors' committee; trustee and committee administration, no effect on the landlord's or manager's chain decisions.")
nd("US:11 USC 1104", "Grounds for appointing a chapter 11 trustee or examiner (trustee administration); the consequence that a serving trustee collects is stated in US:11USC1107-1306-owner-reorganization.")
nd("US:11 USC 1105", "Termination of a chapter 11 trustee's appointment (trustee administration); the resulting debtor-in-possession branch is stated in US:11USC1107-1306-owner-reorganization.")
nd("US:11 USC 1106", "Duties of a chapter 11 trustee and examiner (trustee administration).")
nd("US:11 USC 1108", "Authorizes the chapter 11 trustee or debtor in possession to operate the business; that the owner keeps collecting and refunding is stated in US:11USC1107-1306-owner-reorganization and US:11USC363-owner-cash-collateral.")
nd("US:11 USC 1112", "Grounds and procedure for converting or dismissing a chapter 11 case (court and case administration); the effects of conversion and dismissal on collection and the refund are proposed at 348 and 349.")
nd("US:11 USC 1115", "Adds an individual chapter 11 debtor's post-petition property and earnings to the estate and leaves the debtor in possession; the owner's collection role is unchanged from US:11USC1107-1306-owner-reorganization.")
nd("US:11 USC 1116", "Reporting and operating duties of a small-business chapter 11 debtor to the court and U.S. trustee (case administration).")

add("US:11 USC 1111", "new_rule",
    "In an owner's chapter 11, a former tenant's refund claim scheduled as undisputed is deemed filed; one scheduled as disputed, contingent or unliquidated (or not scheduled) must be filed by the bar date.",
    proposed=[rule("US:11 USC 1111", "US:11USC1111-deemed-filed", "11 U.S.C. 1111(a)", "owner; manager; tenant", "applies",
                   "The owner is a chapter 11 debtor and a former tenant has a pre-petition claim against it (an untraceable deposit refund, US:11USC1107-1306-owner-reorganization).",
                   "If the owner's schedules list the tenant's claim and do not mark it disputed, contingent or unliquidated, a proof of claim is deemed filed for the scheduled amount and the tenant need not file. If the claim is scheduled as disputed, contingent or unliquidated, or not scheduled, or the tenant claims more than scheduled, the tenant must file a proof of claim by the bar date the court fixes, or it is not treated as a creditor for voting and distribution on that claim (US:FRBP3003-ch11-bar-date). The manager supplies the owner the tenant's name, forwarding address and deposit amount for the schedules.",
                   "major", "0.5", "(a) A proof of claim or interest is deemed filed under section 501 of this title", "except a claim or interest that is scheduled as disputed, contingent, or unliquidated.",
                   dependencies=["US:11USC1107-1306-owner-reorganization"])])
