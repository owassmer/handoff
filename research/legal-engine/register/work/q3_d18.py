import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
nd("NYC:ADC 8-101", "Policy declaration of the Human Rights Law; no operative rule beyond 8-107.")
for s, why in (("8-111", "respondent's answer to a Commission complaint"),
               ("8-112", "withdrawal of a Commission complaint"),
               ("8-113", "Commission dismissal of a complaint"),
               ("8-114", "Commission subpoenas and record-preservation demands during an investigation"),
               ("8-115", "Commission mediation and conciliation"),
               ("8-118", "sanctions for discovery non-compliance in a Commission case"),
               ("8-119", "Commission hearing procedure"),
               ("8-123", "judicial review of Commission orders"),
               ("8-128", "who may sue for the Commission"),
               ("8-131", "police exclusion from chapter 6 jurisdiction"),
               ("8-134", "Commission poster displayed by city agencies")):
    nd(f"NYC:ADC {s}", f"Procedure after a discrimination complaint is filed ({why}); it arises only in litigation "
       "and changes no settlement or collection step. The limits and remedies that bear on the chain are in 8-109, "
       "8-120, 8-126 and 8-502.")
st("NYC:ADC 8-130", ["NYC:ADC-8-107(5)(a)-terms"],
   "Liberal construction and narrow reading of exemptions shape the city equal-treatment rule, which already "
   "applies only the two listed housing exemptions.")
commit()
