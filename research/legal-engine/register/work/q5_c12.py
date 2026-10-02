import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd, rule

add("US:11 USC 501", "stated",
    "Lets the landlord file a proof of claim (and treats rejection damages as a pre-petition claim for filing); the filing deadline and the content are stated in the existing claim-deadline rule and the proposed 3001 rule.",
    atom_ids=["US:FRBP-3002(c)-claim-deadline", "US:11USC365(d)(1)-ch7-rejection"])

add("US:11 USC 503", "new_rule",
    "In an owner's bankruptcy, a deposit refund owed on a tenancy the estate ran after the filing (a deposit taken, or a lease continued, by the debtor in possession or trustee) is an administrative expense paid in full ahead of pre-filing claims; in a tenant's chapter 7 the landlord's post-filing rent is not.",
    proposed=[rule("US:11 USC 503", "US:11USC503-admin-expense-refund", "11 U.S.C. 503(a), (b)(1)(A); 507(a)(2)", "owner; manager; trustee; tenant; landlord", "has priority",
                   "Branch (a): the owner is a debtor and the estate (trustee or debtor in possession) collected a tenant's deposit after the filing, or operated the tenancy after the filing and incurred the refund or other obligations to the tenant in doing so. Branch (b): a former tenant is a chapter 7 debtor who stayed in the unit after filing.",
                   "(a) The tenant's claim arising from the estate's post-petition operation (the refund of a deposit the estate received, and the estate's own post-petition charges and credits) is an actual, necessary cost of preserving the estate, allowed as an administrative expense after notice and a hearing on the tenant's timely request for payment (or a late request the court permits for cause, and by any administrative-claim bar date the court sets). It ranks second in priority (507(a)(2)) and a chapter 11 plan must pay it in cash in full on the effective date unless the tenant agrees otherwise (1129(a)(9)(A)); in chapter 7 it is paid before general unsecured claims. The manager pays such refunds in the ordinary course from estate funds (US:11USC363-owner-cash-collateral). A deposit taken before the filing is governed instead by US:11USC541-704-owner-chapter7 (traceable trust money) and US:11USC507(a)(7)-deposit-priority. (b) The tenant's post-filing occupancy benefits the individual debtor, not the chapter 7 estate, so the landlord's post-filing rent is not an administrative expense; it is the debtor's own post-petition debt, outside the pre-petition claim and not discharged, collectible from the debtor's non-estate property (post-filing earnings), and a lease the trustee does not assume within 60 days is rejected (US:11USC365(d)(1)-ch7-rejection).",
                   "major", "0.5", "(a) An entity may timely file a request for payment of an administrative expense", "the actual, necessary costs and expenses of preserving the estate",
                   determinacy="MIXED", judgment_terms=["actual, necessary costs and expenses of preserving the estate"],
                   dependencies=["US:11USC541-704-owner-chapter7", "US:11USC1107-1306-owner-reorganization", "US:11USC365(d)(1)-ch7-rejection"])])

nd("US:11 USC 504", "Bars fee-sharing by estate professionals; no effect on the landlord's conduct.")
nd("US:11 USC 505", "Court determination of the debtor's or estate's tax liability to governmental units; none of the chain's tax events.")
nd("US:11 USC 508", "Distribution rules for creditors of a partnership debtor paid by a general partner; no chain decision.")
nd("US:11 USC 510", "Contractual and equitable subordination of claims by court order; it sets no duty, deadline or amount the landlord acts on in the chain.")
nd("US:11 USC 511", "Interest rate on tax claims of governmental units; not a landlord or tenant claim.")
