import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 399", N, "Warning labels on cigarette packages; outside the chain."),
    D("NY:GBL 399-AA", N, "Ban on trade in dog and cat fur; outside the chain."),
    D("NY:GBL 399-AAA", N, "Labeling of real and faux fur clothing; outside the chain."),
    D("NY:GBL 399-AAAA", N, "Menstrual product labeling and restricted substances; outside the chain."),
    D("NY:GBL 399-AAAAA", N, "Ban on animal-tested cosmetics; outside the chain."),
    D("NY:GBL 399-AAAAAA", N, "Diaper ingredient labeling; outside the chain."),
    D("NY:GBL 399-B", N, "Misdemeanor to sell private hack-stand rights on public streets; outside the chain."),
    D("NY:GBL 399-BB", N, "Dry cleaners may donate garments unclaimed after six months; limited to retail dry cleaners and gives no rule for a tenant's belongings (stated at Step 6.9)."),
    D("NY:GBL 399-BBB", N, "Labeling and removal of charitable collection bins on private property; outside the tenancy settlement."),
    D("NY:GBL 399-CCCC", N, "Domestic-violence victims may leave shared wireless phone plans; binds wireless carriers, not landlords (the tenancy DV rules are stated at RPL 227-c)."),
    D("NY:GBL 399-CCCCC", N, "Domestic-violence victims may cut off connected-vehicle tracking; binds vehicle manufacturers only."),
    D("NY:GBL 399-D", N, "Admission of children to bowling alleys; outside the chain."),
    D("NY:GBL 399-DD", N, "Ban on alcohol vaporizing devices; outside the chain."),
    D("NY:GBL 399-DD*2", N, "Playground construction standards (exempting one- to three-family property); a construction standard, not a settlement charge or step."),
    D("NY:GBL 399-E", N, "Ban on yo-yo waterball toys; outside the chain."),
]
save(rows)
