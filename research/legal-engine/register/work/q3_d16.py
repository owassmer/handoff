import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
nd("NYC:ADC 27-2056.14", "DOHMH investigation of a child's elevated blood lead and HPD correction; in-tenancy "
   "enforcement, no settlement step.")
nd("NYC:ADC 27-2056.16", "Emergency repairs are exempt from lead work practices; no settlement step.")
nd("NYC:ADC 27-2056.17", "Owner keeps lead records (including each turnover date) for ten years and passes them to a "
   "buyer; HPD audits. The records do not change what the departing tenant is charged (lead turnover work is never "
   "a charge: NYC:HMC-27-2056.8-lead-turnover).")
nd("NYC:ADC 27-2056.6.1", "Class of lead violations in common areas; HPD enforcement.")
nd("NYC:ADC 27-2056.7", "HPD audit after a DOHMH order to abate; agency enforcement.")
nd("NYC:ADC 27-2056.9", "HPD lead inspections during occupancy; agency enforcement.")
for s in ("27-2081", "27-2082", "27-2083", "27-2085"):
    nd(f"NYC:ADC {s}", "Occupancy standards for cellar and basement units in multiple dwellings; the rent "
       "consequence of unlawful occupancy runs through the certificate-of-occupancy bar (NY:MDL-301(1), "
       "NY:MDL-302(1)(b)), and these standards set no settlement amount themselves.")
nd("NYC:ADC 27-2091", "HPD's power to issue orders, including orders to correct underlying conditions; agency "
   "enforcement with no settlement step.")
nd("NYC:ADC 27-2096.1", "Languages of HPD application forms; agency administration.")
st("NYC:ADC 27-2098", ["NYC:ADC-27-2097-registration", "NY:MDL-325(2)"],
   "Contents of the HPD registration statement (owner, officers, managing agent, emergency contact); the duty to "
   "register and its rent consequence are stated.")
st("NYC:ADC 27-2100", ["NYC:ADC-27-2097-registration"],
   "Amending the registration within five days of an address or officer change is part of keeping it current, "
   "which the registration rule states.")
commit()
