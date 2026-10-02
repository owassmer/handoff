import sys
sys.path.insert(0, "register/work")
from q7_lib import *

N = "no_decision"
rows = [
    D("NY:GBL 390-A", N, "Identification marks on commercially manufactured optical discs; outside the chain."),
    D("NY:GBL 390-C", N, "Minors barred from facilities with unclothed performances; outside the chain."),
    D("NY:GBL 390-C*2", N, "Firewall warning signs where a business offers public internet access; a tenant portal is not public internet access, and data safeguards in the chain are stated (GBL 899-bb)."),
    D("NY:GBL 390-D", N, "Human-trafficking information in truck-stop restrooms; outside the chain."),
    D("NY:GBL 390-E*2", N, "Skimming notice at points of sale accepting EBT cards; rent and balance payments are not point-of-sale EBT transactions."),
    D("NY:GBL 391", N, "Marking retreaded tires; outside the chain."),
    D("NY:GBL 391-A", N, "Deceptive sale of liquid fuels and oils; the fuel-oil credit a tenant may claim is stated at MDL 302-c and this section binds fuel sellers only."),
    D("NY:GBL 391-B", N, "Children's clothing with drawstrings; outside the chain."),
    D("NY:GBL 391-C", N, "Bicycle safety and serial numbers at sale; outside the chain."),
    D("NY:GBL 391-CC", N, "Notice stickers on e-bikes and micromobility devices at retail sale; outside the chain."),
    D("NY:GBL 391-D", N, "Matchbook striking surfaces; outside the chain."),
    D("NY:GBL 391-E", N, "Disclosure of compensation by promoters of children's camps; outside the chain."),
    D("NY:GBL 391-F", N, "Disclosure of compensation by promoters of private schools; outside the chain."),
    D("NY:GBL 391-G", N, "Car rental age discrimination; motor-vehicle rental, not housing."),
    D("NY:GBL 391-H", N, "Used-oil notice on lubricating oil containers; outside the chain."),
    D("NY:GBL 391-I", N, "Notice by sellers and installers of urea-formaldehyde foam insulation to the purchaser or building owner; it binds the installer, not the landlord's account with the tenant."),
    D("NY:GBL 391-J", N, "Standards for fire extinguishers offered for sale; outside the chain."),
    D("NY:GBL 391-JJ", N, "Safety features of electric space heaters sold at retail; outside the chain."),
    D("NY:GBL 391-L*2", N, "Car rental agencies may not require a credit card; motor-vehicle rental, not housing."),
    D("NY:GBL 391-M", N, "Brakes, warnings and protective gear for in-line skates; outside the chain."),
    D("NY:GBL 391-N", N, "Salmonella notice on retail reptile sales; outside the chain."),
]
save(rows)
