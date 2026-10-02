import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

R = "register/texts/NYC_RCNY_T28/"
DET = "NYC:HMC-27-2045-detector-charge"
st("NYC:RCNY 28 12-01", [DET], "Class A owner installs and replaces smoke devices, posts the notice with the "
   "$25/$50/$75 reimbursement caps and one-year payment window; stated by the detector-charge rule.")
for sid, rid, kind, dev in (("NYC:RCNY 28 12-03", "NYC:RCNY28-12-03-classB-smoke", "smoke detecting devices",
                             "Keep and maintain smoke detecting devices in good repair"),
                            ("NYC:RCNY 28 12-09", "NYC:RCNY28-12-09-classB-CO", "CO alarms",
                             "Keep and maintain CO alarms or systems in good repair")):
    f = R + sid.split()[-1] + ".txt"
    dec(sid, "partial",
        f"The detector-charge rule covers class A multiple dwellings and private dwellings; in a class B multiple "
        f"dwelling the owner, not the occupant, maintains and replaces {kind}, a branch the rule does not state.",
        [DET],
        [rule(rid, f"28 RCNY {sid.split()[-1]}", "owner; manager", "allocation",
              f"The departing occupant's unit is in a class B multiple dwelling (rooming or transient occupancy that "
              f"is within the aperture) and at move-out a {kind[:-1]} is missing, removed, stolen or inoperable.",
              f"The owner keeps and maintains the {kind} in good repair, replaces them at the end of their useful "
              f"life, and replaces any stolen, removed, missing or inoperable device before the next occupancy. The "
              f"class A and private-dwelling occupant duty and $25/$50/$75 reimbursement do not apply, so no "
              f"reimbursement is charged; only a device the occupant destroyed or took is chargeable, as damage "
              f"beyond normal wear and tear at its reasonable cost.",
              f, q(f, dev, None), "minor", "5.5a", determinacy="MIXED",
              judgment_terms=["damage beyond normal wear and tear"],
              dependencies=[DET, "NY:GOL-7-108(1-a)(b)-refundable"], amends=DET)])
st("NYC:RCNY 28 12-06", [DET], "Class A CO alarm duties and the $25/$50/$75 reimbursement including useful-life "
   "replacement during the tenancy; stated by the detector-charge rule.")
st("NYC:RCNY 28 12-09.1", [DET], "Natural gas detecting devices (install by 2027-01-01, owner replaces devices "
   "missing from a prior occupancy before the new one, defect replacement within 30 days); the move-out charge "
   "rule covers natural gas devices.")
nd("NYC:RCNY 28 12-11", "Gas-leak procedure notice at the first lease and posted in common areas; no settlement "
   "step.")
st("NYC:RCNY 28 12-12.1", [DET], "Combined posted notice restating the occupant duty and the $25/$50/$75 amounts; "
   "stated by the detector-charge rule.")
nd("NYC:RCNY 28 12-13", "Safety information about detectors given to an adult occupant; no settlement step.")
commit()
