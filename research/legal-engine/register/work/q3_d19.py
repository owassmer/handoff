import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
ex("NYC:RCNY 28 1-17", "28 RCNY ch. 1 governs HPD Article VIII rehabilitation-loan buildings, whose units are "
   "rent-controlled while the loan requires (walk 0.6, NYC:RCL-26-403(e)(1)(c)); Review 2 regime, out of aperture.")
nd("NYC:RCNY 28 11-09", "Owner's certification of correction of lead violations; HPD procedure.")
nd("NYC:RCNY 28 11-10", "Postponement of lead violation correction; HPD procedure.")
nd("NYC:RCNY 28 11-11", "HPD audit of lead records after a DOHMH order; agency enforcement.")
nd("NYC:RCNY 28 12-12", "Form of the gas-leak notice; no settlement step.")
nd("NYC:RCNY 28 12-14", "Buildings without fossil-fuel devices or gas piping need no CO or gas detector; where none "
   "is required and none installed no detector charge arises, and the charge rule attaches to installed devices.")
nd("NYC:RCNY 28 20-01", "Qualifications of RPAPL 7-A administrators; who collects rent under a 7-A judgment is "
   "stated at NY:RPAPL-776-778-administrator.")
nd("NYC:RCNY 28 20-02", "Applicability of HPD's 7-A administrator rules; same as 20-01.")
st("NYC:RCNY 28 25-191", ["NY:MDL-302-a(3)"],
   "HPD's complete list of violations classified as rent impairing sets which recorded violations trigger the "
   "MDL 302-a rent bar, which is stated.")
nd("NYC:RCNY 28 54-03", "Postponement of allergen violation correction; HPD procedure.")
nd("NYC:RCNY 28 54-05", "Owner's certification of correction of pest and mold violations; HPD procedure.")
nd("NYC:RCNY 28 59-01", "Form and filing of the annual bedbug report; no settlement step.")
st("NYC:RCNY 31 5-03", ["NYC:RCNY31-5-06(a)(10)", "NYC:DSS-SOTA-voucher-claim"],
   "HRA pays the SOTA landlord monthly for one year only while the household resides there; the landlord's duty to "
   "return payments for months not occupied and the voucher claim limits are stated. Eligibility decides nothing "
   "in the settlement.")
nd("NYC:RCNY 31 5-04", "Requirements a unit must meet for SOTA approval (reasonable rent, 40% of income, no "
   "stabilized rooms, habitability); decided before the tenancy and fixing no settlement amount.")
commit()
