import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 399-EE", N, "Ban on zone pricing of gasoline by wholesalers; outside the chain."),
    D("NY:GBL 399-EEE", N, "Wireless carriers' stolen-phone programs; outside the chain."),
    D("NY:GBL 399-EEE*2", N, "Car wash promotion disclosures; outside the chain."),
    D("NY:GBL 399-F", N, "An apartment building with two or more coin washers or dryers posts the owner's name, prices and the coin-refund contact; an operating duty of the building during occupancy, not a charge, credit or step in the move-out account."),
    D("NY:GBL 399-FF", N, "Hand-washing at petting zoos; outside the chain."),
    D("NY:GBL 399-GG", N, "Child-resistant packaging of e-liquid; outside the chain."),
    D("NY:GBL 399-II", N, "Tip-restraint standards for new furniture sold at retail; binds retail furniture sellers, not a landlord's turnover account."),
    D("NY:GBL 399-II*2", N, "Ban on crib bumper pads for sellers, child care facilities and transient lodging (apartment buildings excluded); outside the chain."),
    D("NY:GBL 399-K", N, "Utility workers' use of employee toilets in businesses open to the public; outside the chain."),
    D("NY:GBL 399-M", N, "Disclosures on unassembled merchandise; outside the chain."),
    D("NY:GBL 399-N", N, "Any qualified laboratory's fire-safety approval satisfies an Underwriters Laboratories requirement; an equipment-approval rule with no settlement step."),
    D("NY:GBL 399-O", N, "Beverage container deposits excluded from displayed prices; a bottle deposit, not a rental security deposit."),
    D("NY:GBL 399-OO", N, "Deceptive solicitation of vehicle warranty policies; outside the chain."),
    D("NY:GBL 399-Q", N, "Removal of marked shopping carts and trade containers; outside the chain."),
    D("NY:GBL 399-QQ", N, "Sale of box cutters to minors; outside the chain."),
    D("NY:GBL 399-R", N, "Sale of paint pellet guns to minors; outside the chain."),
    D("NY:GBL 399-RR", N, "State outreach on the 9/11 victim fund and WTC health program; outside the chain."),
    D("NY:GBL 399-S", N, "Air gun age notice in stores; outside the chain."),
    D("NY:GBL 399-T", N, "Ban on certain CFC and halon products; outside the chain."),
    D("NY:GBL 399-T*2", N, "Owner contact notice on public vending machines; outside the chain."),
    D("NY:GBL 399-U", N, "Motor vehicle alarm reset limits; outside the chain."),
]
save(rows)
