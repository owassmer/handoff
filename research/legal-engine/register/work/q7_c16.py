import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 396-EEEE", N, "Blocking technology on 3D printers sold in New York; outside the chain."),
    D("NY:GBL 396-F", N, "Registration and labeling of blind-made products; outside the chain."),
    D("NY:GBL 396-G", N, "Registration and labeling of products processed by the blind; outside the chain."),
    D("NY:GBL 396-H", N, "Fraudulent sale of patriotic articles for veteran relief; outside the chain."),
    D("NY:GBL 396-HH", N, "Municipalities may not license veterans' sale of patriotic articles; outside the chain."),
    D("NY:GBL 396-J", N, "Possession of master keys for motor vehicles; outside the chain."),
    D("NY:GBL 396-K", N, "Hazardous toys for children; outside the chain."),
    D("NY:GBL 396-K*2", N, "Disclosure of disaster damage when selling motor vehicles; outside the chain."),
    D("NY:GBL 396-KK", N, "Parental controls on video game consoles; outside the chain."),
    D("NY:GBL 396-L", N, "Child restraints in shopping carts; outside the chain."),
    D("NY:GBL 396-N", N, "Meaning of 'money back guarantee' on goods sold; the security deposit is not a guarantee on merchandise."),
    D("NY:GBL 396-O", N, "A buyer chooses refund or credit under a satisfaction guarantee on goods or services; a deposit refund is owed under GOL 7-108 and is not a satisfaction guarantee, so the refund method is decided by the stated rules."),
    D("NY:GBL 396-P", N, "Posted taxicab rates (inapplicable in NYC by its own subdivision 3); outside the chain."),
    D("NY:GBL 396-P*2", N, "Price escalation and deposit rules in new motor vehicle sales; outside the chain."),
    D("NY:GBL 396-Q", N, "Dealer signature, trade-in and financing rules in new motor vehicle sales; outside the chain."),
    D("NY:GBL 396-QQ", N, "Refund of estimated vehicle registration fees by dealers; outside the chain."),
]
save(rows)
