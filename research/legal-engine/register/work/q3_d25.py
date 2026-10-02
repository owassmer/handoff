import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
for s, why in (("27-2017.11", "HPD's annual report on the allergen article"),
               ("27-2017.7", "HPD training, procedures and rules for the allergen article"),
               ("27-2041.2", "HPD's periodic inspection of self-closing doors"),
               ("27-2048", "floor signs in multiple dwellings"),
               ("27-2049", "street numbers on dwellings"),
               ("27-2056.12", "HPD's annual lead report"),
               ("27-2056.13", "HPD's transmittal of lead violations to DOHMH"),
               ("27-2092", "HPD's hearing and subpoena powers"),
               ("27-2104", "posting the building serial number and the rent-stabilization sign"),
               ("27-2109", "voluntary registration of mortgagees and lienors"),
               ("27-2109.2", "HPD's online portfolio report"),
               ("27-2154", "posting of NYCHA violation data")):
    nd(f"NYC:ADC {s}", f"Concerns {why}; binds no chain party in a settlement.")
nd("NYC:ADC 27-2046", "Repealed (L.L. 2016/157); the current detector rules are in 27-2045, stated at "
   "NYC:HMC-27-2045-detector-charge.")
nd("NYC:ADC 27-2046.1", "Repealed (L.L. 2016/157); see NYC:HMC-27-2045-detector-charge.")
nd("NYC:ADC 27-2046.2", "Repealed (L.L. 2016/157); see NYC:HMC-27-2045-detector-charge.")
nd("NYC:ADC 27-2056.18", "Board of Health may set the lead article's child age at under six or seven; it changes "
   "in-tenancy lead duties, not the turnover rule, which applies at every turnover whatever a child's age.")
st("NYC:ADC 27-2056.2", ["NYC:HMC-27-2056.8-lead-turnover"],
   "Article 14 definitions (lead-based paint, turnover, underlying defect, friction surface) set the reach of the "
   "lead turnover rule.")
nd("NYC:ADC 27-2094", "HPD needs a complaint or warrant to inspect an owner-occupied one- or two-family house, and "
   "such owners may notify HPD voluntarily; neither changes a settlement step.")
nd("NYC:ADC 8-102a", "Definitions for the Fair Chance housing provision on criminal background checks, which "
   "applies to screening before a tenancy; no settlement or collection step uses criminal history.")
nd("NYC:ADC 8-107.1", "Repealed; moved to 8-107(27).")
nd("NYC:ADC 8-117", "Commission rules of procedure; litigation procedure only.")
nd("NYC:ADC 8-121", "Commission may reopen its proceedings; litigation procedure only.")
nd("NYC:ADC 8-133", "Commission outreach on single-occupant toilet rooms; binds no chain party.")
nd("NYC:ADC 8-403", "Corporation counsel investigations for pattern-or-practice suits; city enforcement.")
nd("NYC:ADC 8-604", "Discriminatory-harassment penalties go to the general fund; no chain party.")
commit()
