import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
RC = "Rent control (Admin. Code tit. 26 ch. 3): out of aperture."
RS = "Rent stabilization (Admin. Code tit. 26 ch. 4, RSL): out of aperture."
ex("NYC:ADC 26-407.1", RC + " Fuel pass-along ban for controlled tenants.")
ex("NYC:ADC 26-410", RC + " Protest procedure before the city rent agency.")
ex("NYC:ADC 26-501", RS + " Findings and declaration of emergency.")
ex("NYC:ADC 26-502", RS + " Renewed declaration of emergency.")
ex("NYC:ADC 26-506", RS + " Coverage of hotels.")
ex("NYC:ADC 26-511.1", RS + " MCI and IAI increases.")
ex("NYC:ADC 26-514", RS + " Rent reduction for failure to maintain services.")
ex("NYC:ADC 26-518", RS + " Hotel industry stabilization association.")
ex("NYC:ADC 26-519", RS + " Suspension of an owners' association registration.")
nd("NYC:ADC 26-529", "City unlawful-eviction remedies are cumulative with other law; adds no rule beyond "
   "NY:RPAPL-768-853-unlawful-eviction.")
nd("NYC:ADC 27-2007", "Tenant may not disable self-closing doors, block egress, deface required signs or remove a "
   "compliant shower head; a device the tenant removed is charged under the deposit damage rule, and the section "
   "adds no settlement rule.")
nd("NYC:ADC 27-2009.2", "Notice to occupants before major construction; no settlement step.")
commit()
