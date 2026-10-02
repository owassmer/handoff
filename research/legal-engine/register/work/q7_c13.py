import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 391-OO", N, "Age limits on sale of diet pills and muscle-building supplements; outside the chain."),
    D("NY:GBL 391-P", N, "Previously worn clothing must be cleaned before it is rented; rental of clothing, not housing."),
    D("NY:GBL 391-Q", N, "Consumer rebates redeemed by request after a purchase; a rent concession or credit in the tenancy account is applied by the landlord, not redeemed on the tenant's request, so the rebate timing rules do not reach it."),
    D("NY:GBL 391-S", N, "Ban on novelty lighters; outside the chain."),
    D("NY:GBL 391-T", N, "Care instructions on retail sale of small animals; outside the chain."),
    D("NY:GBL 391-U*2", N, "PFAS firefighting foam and gear; outside the chain."),
    D("NY:GBL 391-V", N, "Third-party food delivery agreements; outside the chain."),
    D("NY:GBL 391-W", N, "Unauthorized restaurant reservation platforms; outside the chain."),
    D("NY:GBL 391-X", N, "Warning labels on hair relaxers (effective 2027-05-21); outside the chain."),
    D("NY:GBL 392", N, "Tagging and invoicing of second-hand watches; outside the chain."),
]
save(rows)
