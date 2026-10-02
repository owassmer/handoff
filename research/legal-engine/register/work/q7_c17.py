import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 396-RR", N, "Unconscionable retail milk prices; outside the chain."),
    D("NY:GBL 396-S", N, "Septic pamphlet to buyers of newly built homes; outside the chain."),
    D("NY:GBL 396-SS", N, "Long-distance warning by dial-up internet providers; outside the chain."),
    D("NY:GBL 396-T", N, "Disclosures for layaway purchases of merchandise; a rent payment plan is not a layaway plan for merchandise."),
    D("NY:GBL 396-TT", N, "Florists misrepresenting their location in directories; outside the chain."),
    D("NY:GBL 396-U", N, "Delivery dates and refunds for furniture and appliance dealers; a landlord renting a furnished unit is not in the business of selling or leasing furniture as such, and deposit refunds follow GOL 7-108."),
    D("NY:GBL 396-V", N, "Warning signs on public blood pressure machines; outside the chain."),
    D("NY:GBL 396-W", N, "Soliciting passengers at NYC airports; outside the chain."),
    D("NY:GBL 396-X", N, "Air pumps at gasoline stations; outside the chain."),
    D("NY:GBL 397-B", N, "Digital billboards near large Mitchell-Lama complexes; outside the chain."),
    D("NY:GBL 398", N, "Bills of lading for vessels between New York ports; outside the chain."),
    D("NY:GBL 398-A", N, "Export papers for shipping motor vehicles abroad; outside the chain."),
    D("NY:GBL 398-B", N, "Discrimination by car rental agencies; motor-vehicle rental, not housing (housing discrimination rules are stated at Step 5.10)."),
    D("NY:GBL 398-C", N, "Unaccompanied children at skating rinks; outside the chain."),
    D("NY:GBL 398-D", N, "Transfer and destruction of plastic-product molds abandoned with a molder; limited to molders and their customers, not a tenant's belongings (Step 6.9 rules govern those)."),
    D("NY:GBL 398-E", N, "Voids indemnity clauses in motor carrier transportation contracts; a lease is not one."),
    D("NY:GBL 398-F", N, "Registration and notice for children's non-regulated camps; outside the chain."),
    D("NY:GBL 398-G", N, "Kratom labeling (effective 2026-12-19); outside the chain."),
]
save(rows)
