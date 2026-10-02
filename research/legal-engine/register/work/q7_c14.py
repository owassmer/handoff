import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 392-A", N, "Labeling of new computers with recycled parts; outside the chain."),
    D("NY:GBL 392-B", N, "False labels on merchandise with intent to defraud; the chain sells no merchandise."),
    D("NY:GBL 392-C", N, "Removing marks of origin from merchandise; outside the chain."),
    D("NY:GBL 392-D", N, "False manufacturer marks on articles; outside the chain."),
    D("NY:GBL 392-E", N, "Odometer statements on motor vehicle transfers; outside the chain."),
    D("NY:GBL 392-F", N, "Taximeter serial numbers; outside the chain."),
    D("NY:GBL 392-G", N, "Warnings and features of tanning devices sold; outside the chain."),
    D("NY:GBL 392-I", N, "Motor fuel price reductions reflecting sales tax changes; outside the chain."),
    D("NY:GBL 392-J", N, "Seasonal sale of sparkling devices; outside the chain."),
    D("NY:GBL 392-K", N, "Vehicle glass repair and ADAS recalibration disclosures; outside the chain."),
    D("NY:GBL 393", N, "Standard barrels and labeling of lime; outside the chain."),
    D("NY:GBL 393-A", N, "Flammability notice on non-fire-rated wood paneling offered for sale; it binds sellers of paneling, not a landlord's turnover charges."),
    D("NY:GBL 393-B", N, "Disclosures in solicitations for credit card protection services; outside the chain."),
    D("NY:GBL 393-C", N, "Sellers of labor-law posters must say the postings are free from government; outside the chain."),
    D("NY:GBL 393-D", N, "Sellers of certified deed copies must say the county clerk sells them cheaply; outside the chain."),
    D("NY:GBL 394", N, "Replacement of lost stock certificates; outside the chain."),
    D("NY:GBL 394-B", N, "Contracts for instruction or use of dance studios and training facilities; a lease of a dwelling is not such a contract, and building amenity charges fall under the stated FARE and lease-charge rules."),
]
save(rows)
