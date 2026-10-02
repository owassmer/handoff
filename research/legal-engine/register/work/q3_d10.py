import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
nd("NYC:RCNY 28 20-04", "HPD's discretion and technical-violation rule for RPAPL 7-A administrator appointments; "
   "who collects rent under a 7-A judgment is stated at NY:RPAPL-776-778-administrator.")
nd("NYC:RCNY 28 25-101", "Notice and hours for owner access to inspect or repair under HMC 27-2008; the pre-vacate "
   "inspection is governed by GOL 7-108(1-a)(d) (48 hours' written notice), not by this rule, and no settlement "
   "step turns on it.")
for s in ("43-01", "43-02", "43-03", "43-04"):
    nd(f"NYC:RCNY 28 {s}", "A foreclosing mortgagee's filings with HPD; the tenant-facing foreclosure rules are "
       "stated at NY:RPAPL-1305-successor.")
nd("NYC:RCNY 28 54-02", "Allergen lease notice and pamphlet at lease signing; move-in paperwork with no settlement "
   "effect.")
nd("NYC:RCNY 28 54-04", "Work practices for pest and mold correction; the move-out cost allocation is decided by "
   "the owner-duty and turnover rules.")
for s in ("Apendice A: Contrato/Comienzo De Ocupacion Y Medidas De Precaucion Con Los Peligros De Plomo En La Pintura – Encuesta Respecto Al Niño",
          "Apendice B: Aviso Añual Para Medidas De Precaucion Con Los Peligros De Plomo En La Pintura – Encuesta Respecto Al Niño",
          "Appendix A: Lease/Commencement of Occupancy Notice for Prevention of Lead Based Paint Hazards – Inquiry Regarding Child",
          "Appendix B: Annual Notice for Prevention of Lead Based Paint Hazards – Inquiry Regarding Child"):
    nd(f"NYC:RCNY 28 {s}", "Form of the lead child-inquiry notice at lease signing or yearly; move-in and in-tenancy "
       "paperwork with no settlement effect.")
for s in ("Appendix A: Lease/Commencement of Occupancy Notice for Indoor Allergen Hazards",
          "Apéndice A: Aviso De Alquiler/Comienzo De La Ocupación Sobre Riesgo De Alérgenos En Interiores"):
    nd(f"NYC:RCNY 28 {s}", "Form of the allergen lease notice; it restates the owner's turnover duty stated at "
       "NYC:HMC-27-2017.5-turnover and decides nothing further.")
nd("NYC:RCNY 31 5-05", "Duties of the SOTA household toward DSS (report a move, eviction papers, landlord change); "
   "the landlord's duties at move-out are stated at NYC:RCNY31-5-06(a)(10) and NYC:DSS-SOTA-voucher-claim.")
commit()
