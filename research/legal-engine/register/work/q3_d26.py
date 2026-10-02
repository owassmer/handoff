import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
for s in ("1-02", "1-03", "1-04", "1-05", "1-06", "1-07", "1-08", "1-09", "1-10", "1-11", "1-14", "1-15", "1-16"):
    ex(f"NYC:RCNY 28 {s}", "28 RCNY ch. 1 governs HPD Article VIII rehabilitation-loan buildings (low-income "
       "occupancy covenants; units rent-controlled while the loan requires, walk 0.6): Review 2 and subsidized "
       "regime, out of aperture.")
nd("NYC:RCNY 28 11-13", "Lead violations in owner- or shareholder-occupied co-op and condo units fall on the "
   "occupant-owner; not a rented unit, so no settlement step.")
ex("NYC:RCNY 28 20-03", "HPD regulatory agreement requiring low-income housing for thirty years after a 7-A "
   "transfer: subsidized/regulated housing, out of aperture.")
nd("NYC:RCNY 28 25-81", "Form of identification signs for owners, managing agents and superintendents; no settlement "
   "step.")
nd("NYC:RCNY 28 54-01", "Definitions for HPD's allergen rules (notices, work practices, certifications), none of "
   "which decides a settlement step; the turnover rule rests on the Code's own definitions (27-2017).")
nd("NYC:RCNY 31 5-01", "SOTA definitions (agencies, shelters, household); the stated SOTA landlord rules do not turn "
   "on them.")
nd("NYC:RCNY 31 5-02", "Describes SOTA as one year of monthly rent payments administered by DHS and HRA; the "
   "landlord's settlement duties are stated at NYC:RCNY31-5-06(a)(10) and NYC:DSS-SOTA-voucher-claim.")
nd("NYC:RCNY 31 5-08", "Household's administrative review and appeal of DSS decisions; no landlord step.")
nd("NYC:RCNY 31 5-09", "SOTA program terms (referrals, no waitlist, recoupment from people who misrepresented to "
   "DSS); none decides a settlement step for the landlord.")
commit()
