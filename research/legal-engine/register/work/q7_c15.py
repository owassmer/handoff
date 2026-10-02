import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 394-CC", N, "Safety notices by internet dating services; outside the chain."),
    D("NY:GBL 394-CCC", N, "Hateful-conduct reporting on social media networks; outside the chain."),
    D("NY:GBL 394-D", N, "Patrons of franchised training facilities may enforce contracts against the franchisor; outside the chain."),
    D("NY:GBL 394-F", N, "New York electronic communication providers may not answer out-of-state warrants on protected health activity; outside the chain."),
    D("NY:GBL 394-G", N, "Ban on geofencing health care facilities for advertising; outside the chain."),
    D("NY:GBL 395", N, "Tagging used appliances offered for retail sale; the chain sells no merchandise."),
    D("NY:GBL 395-A", N, "Termination and review of maintenance agreements for retail products; outside the chain."),
    D("NY:GBL 396-A", N, "Insurance representations by savings and loan associations; outside the chain."),
    D("NY:GBL 396-B", N, "Dealer disclosure and synthetic-performer disclosure in advertisements of property; it governs advertising a unit, not settling or collecting a tenancy."),
    D("NY:GBL 396-BB", N, "Full service at self-service prices for disabled drivers; outside the chain."),
    D("NY:GBL 396-C", N, "Advertising by denture suppliers; outside the chain."),
    D("NY:GBL 396-CC", N, "Pool enclosure notices by pool sellers and installers; outside the chain."),
    D("NY:GBL 396-CC*2", N, "Combining senior citizen discounts with sale prices; the chain has no senior discount program on merchandise."),
    D("NY:GBL 396-DD", N, "Helmets for horse rentals; outside the chain."),
    D("NY:GBL 396-E", N, "Linen labeling of collars and cuffs; outside the chain."),
    D("NY:GBL 396-EE", N, "Gun locks and storage notices on retail firearm sales; outside the chain."),
    D("NY:GBL 396-EEE", N, "Restrictions on sale of body armor; outside the chain."),
]
save(rows)
