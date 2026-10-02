import sys; sys.path.insert(0, "register/work")
from q8_lib import D, save
N = "no_decision"
M = "mortgage-lending rule between lender and borrower; no effect on a tenancy settlement"
save([
 D("NY:RPL 266", N, "Protection of good-faith purchasers against fraudulent-conveyance claims; title matter, the tenant's position on a sale is under GOL 7-105 and RPL 223."),
 D("NY:RPL 275", N, "Mortgage discharge certificates and payoff handling; " + M + "."),
 D("NY:RPL 276", N, "Easements and fiduciary mortgage investments; " + M + "."),
 D("NY:RPL 277", N, "Pre-1969 fiduciary powers to modify mortgage investments; " + M + "."),
 D("NY:RPL 277-A", N, "Fiduciary assent to guaranty-corporation reorganizations; " + M + "."),
 D("NY:RPL 278", N, "Exchange of mortgage investments for HOLC bonds; " + M + "."),
 D("NY:RPL 278-A", N, "Fiduciary sale of old-law tenement or clearance-area property for redevelopment securities; a financing power, no settlement consequence."),
 D("NY:RPL 279", N, "Graduated payment mortgages; " + M + "."),
 D("NY:RPL 280-B", N, "Reverse mortgage marketing and foreclosure preconditions; " + M + "."),
 D("NY:RPL 281", N, "Credit line mortgages and future-advance priority; " + M + "."),
])
