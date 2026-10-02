import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:EPTL 11-1.11", N, "A trustee's limited power to amend a trust for tax qualification; internal to trusts."),
    D("NY:EPTL 11-1.8", N, "Bank fiduciaries may hold government securities at a Federal Reserve bank; internal to fiduciary custody of securities, not a tenant's deposit."),
    D("NY:EPTL 11-1.9", N, "Fiduciaries and custodians may hold securities in a clearing corporation; internal to securities custody, not a tenant's deposit."),
    D("NY:EPTL 11-2.2", N, "Investment powers of estate and trust fiduciaries; a landlord holding a tenant's deposit is governed by GOL 7-103, not by the fiduciary investment rules."),
    D("NY:EPTL 11-2.3-A", N, "Court review of a trustee's principal-income adjustment; internal to trusts."),
    D("NY:EPTL 13-3.3", N, "Insurance and pension proceeds payable to a designated trustee are not subject to the insured's debts; the landlord's claim against a deceased tenant is paid from estate assets through the fiduciary, and these proceeds are outside the estate, as the stated EPTL 13-3.2 decision already records."),
]
save(rows)
