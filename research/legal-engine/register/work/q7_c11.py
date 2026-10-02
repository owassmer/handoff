import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 143", N, "Sale of false identification documents without a NOVELTY mark; outside the chain."),
    D("NY:GBL 349-B", N, "Disclosure and warranty rules for sellers of residential telephone equipment; outside the chain."),
    D("NY:GBL 349-B-1", N, "911 limitation disclosures by VoIP sellers; outside the chain."),
    D("NY:GBL 349-D", N, "ESCO energy contract rules bind energy services companies and their sellers; a landlord's lease utility charge is not an ESCO contract, and submetered and lease utility charges are stated elsewhere."),
    D("NY:GBL 349-E", N, "Counterfeit and non-functional airbags; outside the chain."),
    D("NY:GBL 349-G", N, "Hospitals and health providers may not fill in patients' medical credit applications; outside the chain."),
    D("NY:GBL 349-H", N, "Labeling of mezuzahs and tefillin; outside the chain."),
    D("NY:GBL 350-B", N, "Disclosure when the title 'doctor' is used to sell health goods or services; outside the chain."),
    D("NY:GBL 350-B-1", N, "Disclosure of the basis of senior-specific designations in advertising services; outside the chain."),
    D("NY:GBL 350-F-1", N, "Bars after-the-fact referral fees in real property sales and purchases; sales only, not rentals or settlement."),
    D("NY:GBL 380", N, "Short title of the New York Fair Credit Reporting Act; its operative sections are decided where they bind a landlord or collector (GBL 380-b, 380-i, 380-l to 380-o, 380-t)."),
    D("NY:GBL 390", N, "Substitution of branded engine lubricating oils; outside the chain."),
]
save(rows)
