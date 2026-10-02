import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:18 NYCRR 352.29", N, "Budgetary method for the assistance grant; a shelter or utility item paid by voucher is deducted from the household's grant, which binds the district and sets no landlord duty, charge or payee rule."),
    D("NY:18 NYCRR 352.30", N, "Who is counted in the public-assistance household budget; binds the district only."),
    D("NY:18 NYCRR 352.33", N, "Deeming of an immigrant sponsor's income and the district's claim against the sponsor; no landlord or collector step."),
    D("NY:18 NYCRR 352.8", N, "Assistance allowances for room-and-board, shelter and congregate-care residents; it prices the district's payment and sets no duty on a market-rate landlord settling a tenancy."),
    D("NY:18 NYCRR 352.9", N, "Services (child care) the district purchases for recipients; nothing in the tenancy settlement."),
    D("NY:19 NYCRR 175.10", N, "A broker may offer property for sale or lease only with the owner's authorization; it governs listing a unit, not settling a departing tenancy."),
    D("NY:19 NYCRR 175.11", N, "A broker's sign on property needs the owner's consent; no settlement step."),
    D("NY:19 NYCRR 175.13", N, "A broker may not use or reward another broker's salesperson without that broker's knowledge; relations between brokers only."),
    D("NY:19 NYCRR 175.14", N, "A departing salesperson turns listing information over to the broker; no settlement step."),
    D("NY:19 NYCRR 175.15", N, "Bars automatic continuation in an exclusive listing contract between owner and broker; the tenant's lease auto-renewal is governed by the stated GOL 5-905 rule."),
    D("NY:19 NYCRR 175.16", N, "Repealed section; no text in force."),
    D("NY:19 NYCRR 175.18", N, "Department of State may refuse a broker trade name confusingly similar to another's; it does not govern the name a settlement letter goes out in (collection name rules are stated at 15 USC 1692e(14))."),
    D("NY:19 NYCRR 175.19", N, "Bars net listings for the sale of real property; sales only."),
    D("NY:19 NYCRR 175.20", N, "Branch-office ownership, supervision and relocation approval for brokers; it applies only to a broker's branch office and fixes nothing about who may collect a balance, which the stated broker-configuration rules decide."),
]
save(rows)
