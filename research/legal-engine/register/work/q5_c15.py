import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

add("US:11 USC 521", "new_rule",
    "Gives the landlord two ways to end a former tenant's case early (request the tax return, whose non-delivery forces dismissal; ask for the order confirming automatic dismissal when schedules are missing on day 46), and makes the schedules the listing that decides whether an unlisted balance survives.",
    proposed=[rule("US:11 USC 521", "US:11USC521-schedules-dismissal", "11 U.S.C. 521(a)(1), (e)(2), (i)(1)-(2)", "landlord; collector", "may",
                   "A former tenant who is an individual has filed a voluntary chapter 7 or 13 case while the landlord holds a balance.",
                   "(1) The tenant must file a list of creditors and schedules; whether the landlord is listed decides 523(a)(3) (US:11USC523-landlord-exceptions). (2) If the landlord timely requests a copy of the tenant's most recent federal tax return, the tenant must give it no later than 7 days before the first date set for the 341 meeting; if it does not, the court dismisses the case unless the failure was beyond the tenant's control. (3) If the tenant does not file all the 521(a)(1) information within 45 days after the petition, the case is automatically dismissed on the 46th day (subject to a 45-day extension the tenant requests within the first 45 days, or the trustee's motion); the landlord may ask the court for an order confirming the dismissal, which the court must enter within 7 days. Dismissal ends the stay and the case without a discharge (US:11USC349-dismissal).",
                   "major", "8.8", "(i) (1) Subject to paragraphs (2) and (4) and notwithstanding section 707(a)", "the court shall enter an order of dismissal not later than 7 days after such request.",
                   dependencies=[])])

add("US:11 USC 707", "new_rule",
    "Decides whether a landlord may move to dismiss a former tenant's chapter 7 as an abuse (only if the tenant's income is above the state median) and its fee exposure if the motion fails.",
    proposed=[rule("US:11 USC 707", "US:11USC707(b)-abuse-motion", "11 U.S.C. 707(a), (b)(1), (b)(5)(A), (b)(6)", "landlord; collector", "may",
                   "A former tenant who is an individual with primarily consumer debts (a residential lease balance is a consumer debt) is a chapter 7 debtor, and the landlord considers moving to dismiss the case.",
                   "The court may dismiss (or, with the tenant's consent, convert to chapter 11 or 13) if granting relief would be an abuse, on the motion of a party in interest. A creditor such as the landlord may file the motion only if the tenant's current monthly income (with a spouse's, in a joint case) times 12 exceeds the New York median family income for the household size; at or below the median only the judge or U.S. trustee may move. The motion is due within 60 days after the first date set for the 341 meeting (FRBP 1017(e)). If the court denies a creditor's motion and finds the creditor's position violated FRBP 9011, or the motion was filed to coerce the tenant into waiving a right, it may award the tenant its reasonable costs and attorney's fees. Separately, any party may seek dismissal for cause under 707(a) (unreasonable delay prejudicial to creditors, unpaid fees). A dismissal ends the case without a discharge (US:11USC349-dismissal).",
                   "minor", "8.8", "(b) (1) After notice and a hearing, the court, on its own motion or on a motion by the United States trustee", "plus $525 1 per month for each individual in excess of 4.",
                   determinacy="MIXED", judgment_terms=["abuse", "primarily consumer debts"], dependencies=[])])

nd("US:11 USC 102", "Rules of construction (after notice and a hearing, includes, may not, order for relief); used by every bankruptcy rule and changing none of the chain's stated or proposed outcomes.")
nd("US:11 USC 103", "Which chapters apply in which cases; chapters 1, 3 and 5 apply in chapters 7, 11 and 13, which the stated and proposed rules already assume.")
nd("US:11 USC 1109", "Any party in interest may be heard in a chapter 11 case; it creates no duty, deadline or amount in the chain.")
nd("US:11 USC 306", "Limited appearance of a foreign representative; chapter 15-related and out of aperture for this batch.")
nd("US:11 USC 345", "Investment of estate money by the trustee (trustee administration).")
DRA = "Regulates debt relief agencies, persons that provide bankruptcy assistance to an assisted person for pay; a creditor (the landlord), its manager, Handoff or a collector dealing with a tenant about the balance owed to the landlord is excluded from that definition (101(12A)(C)), so nothing in the chain changes"
nd("US:11 USC 526", DRA + ".")
nd("US:11 USC 527", DRA + ".")
nd("US:11 USC 528", DRA + ".")
nd("US:11 USC 1102", "Appointment of chapter 11 creditors' committees (case administration).")
nd("US:11 USC 1113", "Rejection of collective bargaining agreements; no chain decision.")
nd("US:11 USC 1145", "Securities-law exemption for securities issued under a plan; no chain decision.")
nd("US:11 USC 322", "Qualification and bond of trustees (trustee administration).")
nd("US:11 USC 327", "Employment of professionals by the trustee (trustee administration).")
nd("US:11 USC 330", "Compensation of trustees and professionals (trustee administration).")
