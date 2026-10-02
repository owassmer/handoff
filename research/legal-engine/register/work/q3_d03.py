import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *

RC = "Rent control (Admin. Code tit. 26 ch. 3, City Rent and Rehabilitation Law): out of aperture."
RS = "Rent stabilization (Admin. Code tit. 26 ch. 4, RSL): out of aperture."
ex("NYC:ADC 26-406.1", RC + " SCRIE/DRIE notices for rent-controlled units.")
ex("NYC:ADC 26-407", RC + " Labor cost pass-along refunds.")
ex("NYC:ADC 26-411", RC + " Judicial review of city rent agency orders.")
ex("NYC:ADC 26-507", RS + " Units in buildings sold by the city become stabilized.")
ex("NYC:ADC 26-509.1", RS + " SCRIE/DRIE notices for stabilized units.")
ex("NYC:ADC 26-513", RS + " Initial legal regulated rent adjustment.")
ex("NYC:ADC 26-515", RS + " Recovery of possession for charitable use.")
ex("NYC:ADC 26-517.1", RS + " Registration fee per stabilized unit.")
nd("NYC:ADC 26-524", "Corporation counsel enforces the city unlawful-eviction chapter; the prohibition and its "
   "penalties for the chain are stated at NY:RPAPL-768-853-unlawful-eviction, and city enforcement procedure "
   "changes no party's step.")
nd("NYC:ADC 26-525", "A civil penalty for unlawful eviction becomes a lien on the dwelling once a notice of pendency "
   "is filed; it secures a city judgment against the owner and changes no settlement step.")
nd("NYC:ADC 26-526", "Corporation counsel's notice of pendency; city litigation procedure.")
nd("NYC:ADC 26-527", "The city is not liable for costs in unlawful-eviction actions; no chain party is affected.")
nd("NYC:ADC 26-528", "Penalties go to the city's general fund; no chain party is affected.")
nd("NYC:ADC 27-", "HPD violation classes and correction times for pests during occupancy; the turnover pest duty "
   "that bears on the settlement is NYC:HMC-27-2017.5-turnover.")
commit()
