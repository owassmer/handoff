import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
nd("NYC:RCNY 68 10-01", "CityFHEPS definitions (household, apartment, SRO, income terms); the stated landlord rules "
   "in 10-14 do not turn on them.")
nd("NYC:RCNY 68 10-02", "HRA administers CityFHEPS (tenant-based, project-based and repair programs); no landlord "
   "settlement step. The project-based subchapter is outside the aperture.")
nd("NYC:RCNY 68 10-03", "CityFHEPS eligibility for city residents not in shelter; HRA's determination.")
nd("NYC:RCNY 68 10-04", "CityFHEPS eligibility for shelter residents; HRA's determination.")
nd("NYC:RCNY 68 10-08", "CityFHEPS renewals and restorations; HRA's determination.")
nd("NYC:RCNY 68 10-10", "HRA approval for a CityFHEPS household's move (for a room lease being broken, good cause or "
   "the landlord's release); program eligibility, while the lease-break consequences are decided by the state rules "
   "and the landlord's notice and refund duties at NYC:RCNY68-10-14(e), (h).")
nd("NYC:RCNY 68 10-11", "Counting prior program time for households transferred into CityFHEPS; HRA's "
   "determination.")
nd("NYC:RCNY 68 10-13", "Household's review and appeal of HRA decisions; no landlord step.")
for s in ("7-02", "7-03", "7-05", "7-06"):
    nd(f"NYC:RCNY 68 {s}", "LINC VI program rule; the chapter expired and was repealed on 2024-12-31 "
       "(68 RCNY 7-08).")
nd("NYC:RCNY 68 7-08", "Expiry and repeal of the LINC VI chapter on 2024-12-31; it removes LINC VI from current law, "
   "so no LINC VI rule applies to a settlement now.")
for s, why in (("9-01", "definitions"), ("9-02", "HRA administration"), ("9-03", "eligibility"),
               ("9-04", "application, lottery and waitlist"), ("9-05", "the coupon for unit search"),
               ("9-07", "household recertification and obligations"), ("9-11", "household separations"),
               ("9-12", "the household's right of review"), ("9-13", "the review conference and appeal")):
    nd(f"NYC:RCNY 68 {s}", f"HRA HOME TBRA {why}; HRA's dealings with the household, not a landlord settlement step "
       "(the landlord-side rules are proposed at 9-06, 9-09, 9-10 and 9-14).")
commit()
