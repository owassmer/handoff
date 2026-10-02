import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q3_lib import *
A = "register/texts/NYC_ADC/"
RR = "NYC:HMC-27-2135(c)-receiver-rents"
dec("NYC:ADC 27-2103", "partial",
    "The rent stay for non-registration is stated; an HPD extension of the registration period that waives the "
    "27-2107 penalties is a branch it does not state.", ["NYC:ADC-27-2107(b)-rent-stay"],
    [rule("NYC:ADC-27-2103-registration-extension", "Admin. Code 27-2103", "owner", "exception",
          "An owner required to register could not register in time and HPD, on good cause shown, extended its "
          "registration period.",
          "During the extension HPD may waive the 27-2107 penalties, so while a waiver covers the period the court's "
          "discretionary stay of the rent claim under 27-2107(b) does not apply. The extension does not lift the "
          "state bar for an unregistered multiple dwelling (NY:MDL-325(2)), which runs until the owner registers. "
          "Keep HPD's written extension in the file before suing on rent.",
          A + "27-2103.txt", q(A + "27-2103.txt", "the department may, upon good cause shown, extend the registration period",
                               "during such period."),
          "minor", "8.10", dependencies=["NYC:ADC-27-2107(b)-rent-stay", "NY:MDL-325(2)"],
          amends="NYC:ADC-27-2107(b)-rent-stay")])
nd("NYC:ADC 27-2108", "The city, its agencies and NYCHA need not register; public housing is outside the aperture "
   "and a private owner is never within the exemption.")
nd("NYC:ADC 27-2110", "HPD's actions are brought by corporation counsel and moneys go to the city; no chain party.")
nd("NYC:ADC 27-2111", "HPD repair recoveries go to a special fund; no chain party.")
nd("NYC:ADC 27-2113", "HPD's notice of pendency; agency litigation procedure.")
nd("NYC:ADC 27-2125", "HPD's power to correct or order correction of violations; its cost is the owner's debt, stated "
   "at NYC:HMC-27-2128-owner-debt.")
nd("NYC:ADC 27-2127", "HPD's court-ordered repair and lien; agency and owner matter, stated as the owner's debt at "
   "NYC:HMC-27-2128-owner-debt.")
st("NYC:ADC 27-2130", [RR], "Grounds for an HPD receivership of a multiple dwelling; the receiver-rents rule rests "
   "on it (only multiple dwellings).")
nd("NYC:ADC 27-2131", "HPD's notice to owner, mortgagees and lienors before seeking a receiver; the rent consequence "
   "begins only on appointment.")
st("NYC:ADC 27-2132", [RR], "Order to show cause for appointing HPD receiver of the rents; the collection consequence "
   "of the appointment is stated.")
st("NYC:ADC 27-2133", [RR], "A temporary receiver (up to 30 days unless extended) collects rents like any receiver; "
   "stated by the receiver-rents rule, which applies while any receivership is in effect.")
st("NYC:ADC 27-2136", [RR], "On discharge the receivership ends and rent collection returns to the owner; the "
   "receiver-rents rule applies only while the receivership lasts.")
nd("NYC:ADC 27-2137", "Receiver's unrecovered expenses become the owner's debt and a lien; owner and lienor matter.")
nd("NYC:ADC 27-2145", "HPD records its expenses as necessary and proper to establish its lien; agency matter.")
commit()
