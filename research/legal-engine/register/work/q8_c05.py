import sys; sys.path.insert(0, "register/work")
from q8_lib import D, save
N = "no_decision"
I = "internal partnership governance; no effect on the tenancy account"
save([
 D("NY:Partnership Law 121-204", N, "Who signs limited partnership certificates; filing mechanics."),
 D("NY:Partnership Law 121-205", N, "Court-ordered execution of certificates at a partner's petition; " + I + "."),
 D("NY:Partnership Law 121-206", N, "Filing of certificates with the Department of State; filing mechanics."),
 D("NY:Partnership Law 121-207", N, "Liability for materially false statements in a filed certificate to one who relied on it; a tenant does not deal in reliance on the partnership certificate, and nothing in the settlement turns on it."),
 D("NY:Partnership Law 121-208", N, "Restated certificate of limited partnership; filing mechanics."),
 D("NY:Partnership Law 121-301", N, "Admission of limited partners; " + I + "."),
 D("NY:Partnership Law 121-302", N, "Classes and voting of limited partners; " + I + "."),
 D("NY:Partnership Law 121-303", N, "Limited partners' liability for the partnership's debts; the landlord of record (the partnership) owes the refund and damages, and whether a tenant can reach a limited partner personally is enforcement against the owner's principals, not a step any actor takes in the settlement (consistent with the queue's 121-1001 decision)."),
 D("NY:Partnership Law 121-304", N, "Person erroneously believing himself a limited partner; liability to creditors who extended credit in reliance, not a settlement step."),
 D("NY:Partnership Law 121-401", N, "Admission of additional general partners; " + I + "."),
 D("NY:Partnership Law 121-402", N, "Events that end a general partner's status (withdrawal, bankruptcy, death); changes who manages the owner partnership, not the partnership's rights or duties toward the tenant."),
 D("NY:Partnership Law 121-403", N, "General partners carry a general partner's powers and liabilities; the partnership remains the landlord that owes and collects, and reaching a general partner personally is enforcement against the owner's principals outside the settlement steps."),
 D("NY:Partnership Law 121-404", N, "General partner contributions and profit sharing; " + I + "."),
 D("NY:Partnership Law 121-405", N, "Classes and voting of general partners; " + I + "."),
 D("NY:Partnership Law 121-501", N, "Form of partner contributions; " + I + "."),
 D("NY:Partnership Law 121-502", N, "Partner contribution obligations and compromise; " + I + "."),
 D("NY:Partnership Law 121-503", N, "Allocation of profits and losses; " + I + "."),
 D("NY:Partnership Law 121-504", N, "Allocation of distributions; " + I + "."),
 D("NY:Partnership Law 121-601", N, "Interim distributions to partners; " + I + "."),
 D("NY:Partnership Law 121-602", N, "Withdrawal of a general partner; " + I + "."),
 D("NY:Partnership Law 121-603", N, "Withdrawal of a limited partner; " + I + "."),
 D("NY:Partnership Law 121-604", N, "Distribution on a partner's withdrawal; " + I + "."),
 D("NY:Partnership Law 121-605", N, "Distributions in kind; " + I + "."),
 D("NY:Partnership Law 121-606", N, "Partner's creditor status for a declared distribution; " + I + "."),
 D("NY:Partnership Law 121-607", N, "Limit on distributions when liabilities exceed assets, with a limited partner's liability to the partnership; the recovery runs to the partnership, not to the tenant, and no settlement step turns on it."),
 D("NY:Partnership Law 121-701", N, "A partnership interest is personal property; " + I + "."),
 D("NY:Partnership Law 121-702", N, "Assignment of a partnership interest does not dissolve the partnership; the owner remains the same landlord, nothing in the account changes."),
 D("NY:Partnership Law 121-704", N, "Assignee's right to become a limited partner; " + I + "."),
])
