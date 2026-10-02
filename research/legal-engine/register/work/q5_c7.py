import sys
sys.path.insert(0, "register/work")
from q5_lib import add, nd

S = "Outside the three tax events this batch's chain reaches (a deposit kept, interest passed through, a balance written off)"
nd("US:26 USC 6041A", "Reporting of payments for services to non-employees and direct sales; payments to vendors for the turnover are not part of the tenant's financial settlement, and no deposit, interest or write-off amount is remuneration for services.")
nd("US:26 USC 6042", "Returns on dividends; no dividend arises in the settlement chain.")
nd("US:26 USC 6044", "Returns on cooperative patronage dividends; none in the chain.")
nd("US:26 USC 6045", S + ": broker returns on securities and real estate sales and 6045(f) gross proceeds paid to attorneys. A landlord paying a former tenant's deposit claim through the tenant's attorney is a litigation settlement payment, not one of those events (flagged in report_5.md as a boundary item).")
nd("US:26 USC 6046A", "Returns on interests in foreign partnerships; none in the chain.")
nd("US:26 USC 6048", "Information on foreign trusts; a deposit held in trust under GOL 7-103 is not a foreign trust.")
nd("US:26 USC 6050AA", "Returns on passenger-vehicle loan interest; none in the chain.")
nd("US:26 USC 6050B", "Returns on unemployment compensation paid by governments; none in the chain.")
nd("US:26 USC 6050C", "Repealed (Pub. L. 100-418); no text in force.")
nd("US:26 USC 6050E", "Returns on state and local income tax refunds by governments; none in the chain.")
nd("US:26 USC 6050H", "Returns on mortgage interest received from individuals; the landlord's deposit and balance are not mortgages.")
nd("US:26 USC 6050I", S + ": Form 8300 for more than $10,000 in cash received in a trade or business applies if a former tenant pays a balance that large in cash, which is a collection receipt, not a kept deposit, interest or write-off (flagged in report_5.md as a boundary item).")
nd("US:26 USC 6050J", "Returns by lenders on foreclosures and abandonments of security; a residential landlord holds no security interest in a tenant's property.")
nd("US:26 USC 6050N", "Returns on royalties; none in the chain.")
nd("US:26 USC 6050V", "Returns on life insurance contracts acquired by exempt organizations; none in the chain.")
nd("US:26 USC 6050W", S + ": payment-card and third-party network settlements are reported by the settlement entity (or an intermediary that aggregates payees), which matters only if balances are collected by card or network and Handoff settles for several owners (flagged in report_5.md as a boundary item).")
nd("US:26 USC 6050X", "Information on fines and penalties paid to governments; none in the chain.")
