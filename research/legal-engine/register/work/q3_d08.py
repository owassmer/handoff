import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
nd("NYC:RCNY 28 11-02", "Lead remediation where a young child lives, during the tenancy; the turnover cost rule is "
   "stated at NYC:HMC-27-2056.8-lead-turnover.")
nd("NYC:RCNY 28 11-03", "Lease rider and annual notices inquiring about a young child, and the owner's turnover "
   "certification to the incoming occupant; move-in paperwork that fixes no settlement amount for the departing tenant.")
nd("NYC:RCNY 28 11-04", "Annual visual lead inspections and XRF testing; in-tenancy duties with no settlement effect.")
st("NYC:RCNY 28 11-05", ["NYC:HMC-27-2056.8-lead-turnover"],
   "Turnover lead work between vacancy and reoccupancy is the owner's duty; the rule that it is never a move-out "
   "charge is stated. The 2027-07-01 and three-year pre-turnover duties in occupied units do not touch the settlement.")
nd("NYC:RCNY 28 11-07", "Lead paint presumption and its rebuttal before HPD; no settlement step.")
nd("NYC:RCNY 28 11-07.1", "Challenges to XRF-based lead violations; HPD procedure.")
commit()
