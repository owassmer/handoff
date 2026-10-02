import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
RC = "Rent control (Admin. Code tit. 26 ch. 3): out of aperture."
RS = "Rent stabilization (Admin. Code tit. 26 ch. 4, RSL): out of aperture."
ex("NYC:ADC 26-403.1", RC + " Repealed high-income deregulation.")
ex("NYC:ADC 26-403.2", RC + " Repealed MCR increase.")
ex("NYC:ADC 26-404", RC + " DHCR conducts rent control proceedings.")
ex("NYC:ADC 26-406", RC + " SCRIE/DRIE tax abatement for controlled units.")
ex("NYC:ADC 26-409", RC + " City rent agency investigations and records.")
ex("NYC:ADC 26-415", RC + " Surveys of need for rent control.")
ex("NYC:ADC 26-503", RS + " Short title.")
ex("NYC:ADC 26-504.1", RS + " Repealed high-income exclusion.")
ex("NYC:ADC 26-504.2", RS + " Repealed high-rent exclusion.")
ex("NYC:ADC 26-504.3", RS + " Repealed high-income decontrol.")
ex("NYC:ADC 26-505", RS + " Garden-complex coverage.")
ex("NYC:ADC 26-510", RS + " Rent Guidelines Board.")
st("NYC:ADC 26-522", ["NY:RPAPL-768-853-unlawful-eviction"],
   "Definitions of dwelling unit and owner (the HMC owner, which includes managing agents and others in control) "
   "for the city unlawful-eviction chapter that the stated rule applies.")
nd("NYC:ADC 27-2002", "Legislative declaration of the Housing Maintenance Code; no operative rule.")
st("NYC:ADC 27-2003", ["NYC:HMC-27-2013(a)", "NYC:HMC-27-2045-detector-charge", "NYC:HMC-27-2056.8-lead-turnover"],
   "The Housing Maintenance Code applies to all dwellings unless a section says otherwise, which is why its "
   "owner duties reach one- and two-family houses in the stated rules.")
commit()
